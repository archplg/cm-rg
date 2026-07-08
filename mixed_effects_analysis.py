#!/usr/bin/env python3
"""
Formal mixed-effects variance decomposition.

Replaces the ad-hoc variance decomposition in construct_decomposition.py with
proper statistical inference. Uses statsmodels.MixedLM to fit:

    rating ~ task + condition + persona + model + cell_id + (random | rater)

Reports:
  - Fixed effect coefficients with 95% CIs
  - Random effect variances (ICC for each factor)
  - F-tests / Wald tests for each fixed effect
  - Variance components decomposition (proportion of variance per factor)

Outputs:
  mixed_effects/MIXED_EFFECTS_FINDINGS.md
  mixed_effects/variance_components.csv
  mixed_effects/fixed_effects_table.csv

Run:
    pip install statsmodels
    python mixed_effects_analysis.py
"""
from __future__ import annotations
import argparse
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

RESULTS_DIR = Path("./results")
OUT_DIR = Path("./mixed_effects")


def load_long_ratings_with_meta() -> pd.DataFrame:
    """Long-format ratings table with task/condition/persona attached."""
    rows = []
    for cd in sorted(RESULTS_DIR.iterdir()):
        if not cd.is_dir():
            continue
        cell_file = cd / "cell.json"
        if not cell_file.exists():
            continue
        with open(cell_file, encoding="utf-8") as f:
            cell = json.load(f)
        if not cell.get("status", "").startswith("complete"):
            continue
        # Persona per model from api_calls
        persona_for = {}
        for call in cell.get("api_calls", []):
            if call.get("phase") == "phase1_freeresponse":
                persona_for[call.get("model_short_name")] = call.get("persona_or_neutral", "neutral")
        for rater, rdata in cell.get("ratings", {}).items():
            rater_persona = persona_for.get(rater, "neutral")
            for cid, elem_ratings in rdata.items():
                construct_origin = cid.split("_")[1] if "_" in cid else "?"
                for ek, val in elem_ratings.items():
                    rows.append({
                        "cell_id": cd.name,
                        "task": cell.get("task"),
                        "condition": cell.get("condition"),
                        "rater_model": rater,
                        "rater_persona": rater_persona,
                        "construct_id": cid,
                        "construct_origin": construct_origin,
                        "element": ek,
                        "rating": float(val),
                    })
    return pd.DataFrame(rows)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=str(OUT_DIR))
    args = p.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        import statsmodels.formula.api as smf
        import statsmodels.api as sm
    except ImportError:
        print("ERROR: statsmodels not installed. Run: pip install statsmodels")
        return 1

    print("Loading data...")
    df = load_long_ratings_with_meta()
    if df.empty:
        print("ERROR: no ratings data found")
        return 1
    print(f"  {len(df)} ratings, {df['cell_id'].nunique()} cells")

    # Drop rows with missing key fields
    df = df.dropna(subset=["task", "condition", "rater_model", "rater_persona", "rating"])

    # ============================================================
    # 1. Variance components via random-effects only model
    # ============================================================
    print("\n[1/3] Variance components (random effects only)...")
    # Fit: rating ~ 1 + (1|task) + (1|condition) + (1|rater_persona) + (1|rater_model) + (1|cell_id)
    # statsmodels MixedLM supports only ONE level of random effects per fit, so we fit several.
    var_components = {}
    total_var = float(df["rating"].var())
    print(f"  Total rating variance: {total_var:.4f}")

    for factor in ["task", "condition", "rater_persona", "rater_model", "cell_id"]:
        try:
            md = smf.mixedlm("rating ~ 1", df, groups=df[factor])
            mdf = md.fit(method=["lbfgs"], maxiter=200)
            re_var = float(mdf.cov_re.iloc[0, 0])
            resid_var = float(mdf.scale)
            icc = re_var / (re_var + resid_var)
            var_components[factor] = {
                "random_effect_var": re_var,
                "residual_var": resid_var,
                "icc": icc,
                "pct_of_total_var": (re_var / total_var * 100) if total_var > 0 else 0,
            }
            print(f"  {factor}: ICC = {icc:.3f}, % of total var = {var_components[factor]['pct_of_total_var']:.1f}%")
        except Exception as exc:
            var_components[factor] = {"error": str(exc)}
            print(f"  {factor}: FAILED ({exc})")

    df_var = pd.DataFrame([
        {"factor": k, **(v if isinstance(v, dict) else {"error": str(v)})}
        for k, v in var_components.items()
    ])
    df_var.to_csv(out_dir / "variance_components.csv", index=False)

    # ============================================================
    # 2. Fixed-effects model with rater as random effect
    # ============================================================
    print("\n[2/3] Fixed-effects model: rating ~ task + condition + persona (rater random)...")
    try:
        md2 = smf.mixedlm("rating ~ C(task) + C(condition) + C(rater_persona)",
                          df, groups=df["rater_model"])
        mdf2 = md2.fit(method=["lbfgs"], maxiter=200)
        coef_df = pd.DataFrame({
            "coef": mdf2.params,
            "se": mdf2.bse,
            "z": mdf2.tvalues,
            "p": mdf2.pvalues,
            "ci_low": mdf2.conf_int()[0],
            "ci_high": mdf2.conf_int()[1],
        })
        coef_df.to_csv(out_dir / "fixed_effects_table.csv")
        print(f"  Model fit: log-likelihood = {mdf2.llf:.2f}")
        print(f"  Significant effects (p<0.05):")
        sig = coef_df[(coef_df["p"] < 0.05) & (coef_df.index != "Intercept")]
        for name, row in sig.iterrows():
            print(f"    {name}: coef={row['coef']:+.3f}, p={row['p']:.4f}")
        mdf2_summary = str(mdf2.summary())
    except Exception as exc:
        coef_df = None
        mdf2_summary = f"ERROR: {exc}"
        print(f"  FAILED: {exc}")

    # ============================================================
    # 3. ANOVA-style F-tests for fixed effects
    # ============================================================
    print("\n[3/3] ANOVA-style F-tests (Type II via Wald)...")
    f_test_results = {}
    if coef_df is not None:
        for grp_name, prefix in [("task", "C(task)"), ("condition", "C(condition)"),
                                  ("persona", "C(rater_persona)")]:
            grp_coefs = [name for name in coef_df.index if name.startswith(prefix)]
            if not grp_coefs:
                continue
            try:
                hypotheses = " = ".join(grp_coefs) + " = 0"
                test = mdf2.wald_test(hypotheses)
                f_stat = float(test.statistic)
                p_val = float(test.pvalue)
                f_test_results[grp_name] = {"wald_chi2": f_stat, "df": len(grp_coefs), "p": p_val}
                print(f"  {grp_name}: Wald chi2 = {f_stat:.2f}, df = {len(grp_coefs)}, p = {p_val:.4f}")
            except Exception as exc:
                f_test_results[grp_name] = {"error": str(exc)}

    # ============================================================
    # Markdown report
    # ============================================================
    lines = ["# Mixed-Effects Variance Decomposition\n\n"]
    lines.append(f"Generated from {len(df)} ratings across {df['cell_id'].nunique()} cells.\n\n")

    lines.append("## 1. Variance components (random-effects only)\n\n")
    lines.append("Each row shows what proportion of total rating variance is explained "
                  "when that factor is treated as the sole random-effect grouping.\n\n")
    lines.append("| Factor | ICC | % of total variance |\n")
    lines.append("|---|---|---|\n")
    for k, v in var_components.items():
        if "error" in v:
            lines.append(f"| {k} | error | {v['error'][:60]} |\n")
        else:
            lines.append(f"| {k} | {v['icc']:.3f} | {v['pct_of_total_var']:.1f}% |\n")

    lines.append("\n## 2. Fixed-effects model\n\n")
    lines.append("```\n")
    lines.append("rating ~ task + condition + rater_persona + (1 | rater_model)\n")
    lines.append("```\n\n")
    if coef_df is not None:
        lines.append("### Wald tests for grouped effects\n\n")
        lines.append("| Effect group | Wald chi2 | df | p |\n")
        lines.append("|---|---|---|---|\n")
        for k, v in f_test_results.items():
            if "error" in v:
                lines.append(f"| {k} | error | - | - |\n")
            else:
                lines.append(f"| {k} | {v['wald_chi2']:.2f} | {v['df']} | {v['p']:.4f} |\n")

        lines.append("\n### Significant individual coefficients (p < 0.05)\n\n")
        lines.append("| Coefficient | Estimate | 95% CI | p |\n")
        lines.append("|---|---|---|---|\n")
        sig_df = coef_df[(coef_df["p"] < 0.05) & (coef_df.index != "Intercept")]
        for name, row in sig_df.iterrows():
            lines.append(f"| {name} | {row['coef']:+.3f} | [{row['ci_low']:+.3f}, {row['ci_high']:+.3f}] | {row['p']:.4f} |\n")
    else:
        lines.append(f"Model fit failed: {mdf2_summary[:300]}\n")

    lines.append("\n## How to interpret for paper\n\n")
    lines.append("- **ICC** (intraclass correlation): proportion of variance attributable to a grouping factor. "
                 "ICC > 0.2 = strong factor effect.\n")
    lines.append("- **% of total variance**: ICC * residual = how much of the raw rating scale variance "
                 "this factor explains.\n")
    lines.append("- **Wald chi2 test**: tests whether all levels of a categorical factor are jointly equal (group effect).\n")
    lines.append("- **Significant coefficient with CI not crossing 0**: that specific contrast (e.g., persona vs neutral) "
                 "has reliable effect.\n\n")
    lines.append("This analysis is more robust than the ad-hoc variance decomposition in "
                 "`construct_decomposition.py decomp3` and should be used in the paper.\n")

    (out_dir / "MIXED_EFFECTS_FINDINGS.md").write_text("".join(lines), encoding="utf-8")
    print(f"\nWritten: {out_dir}/MIXED_EFFECTS_FINDINGS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
