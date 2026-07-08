#!/usr/bin/env python3
"""
Pilot vs Cross-Model head-to-head comparison.

Compares results from two designs on the SAME 7 tasks:
  - Cross-model (results/): 5 different models from 5 labs, one persona each
  - Pilot (results_pilot/): single Claude playing 5 personas

If cross-model shows substantially higher disagreement than pilot, this is
direct evidence that diversity from independent labs exceeds diversity
achievable from persona prompts on a single model. This validates the
methodological premise of CM-RG.

Outputs:
  pilot_vs_crossmodel/PILOT_VS_CROSSMODEL_FINDINGS.md
  pilot_vs_crossmodel/per_task_comparison.csv
  pilot_vs_crossmodel/comparison_plot.png (if matplotlib available)

Run:
    python pilot_vs_crossmodel_comparison.py
    python pilot_vs_crossmodel_comparison.py --cross_dir results --pilot_dir results_pilot
"""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# Loaders
# ============================================================
def load_cells(results_dir: Path) -> list[dict]:
    cells = []
    if not results_dir.exists():
        return cells
    for cd in sorted(results_dir.iterdir()):
        if not cd.is_dir():
            continue
        cell_file = cd / "cell.json"
        if not cell_file.exists():
            continue
        with open(cell_file, encoding="utf-8") as f:
            cell = json.load(f)
        if cell.get("status", "").startswith("complete"):
            cells.append(cell)
    return cells


def parse_cell_id(cell_id: str) -> tuple[str, str, int]:
    parts = cell_id.split("_")
    if len(parts) < 3:
        return cell_id, "", 0
    task = parts[0]
    condition = parts[1]
    try:
        run_n = int(parts[2].replace("run", ""))
    except ValueError:
        run_n = 0
    return task, condition, run_n


# ============================================================
# Metrics
# ============================================================
def cell_disagreement(cell: dict, exclude_models: set = None) -> float:
    """Mean pairwise rater disagreement on shared constructs and elements."""
    exclude_models = exclude_models or set()
    raters = sorted(r for r in cell.get("ratings", {}).keys() if r not in exclude_models)
    if len(raters) < 2:
        return float("nan")
    pair_diffs = []
    for a, b in combinations(raters, 2):
        ra = cell["ratings"].get(a, {})
        rb = cell["ratings"].get(b, {})
        diffs = []
        for cid in set(ra.keys()) & set(rb.keys()):
            for ek in set(ra[cid].keys()) & set(rb[cid].keys()):
                diffs.append(abs(ra[cid][ek] - rb[cid][ek]))
        if diffs:
            pair_diffs.append(np.mean(diffs))
    return float(np.mean(pair_diffs)) if pair_diffs else float("nan")


def cell_n_constructs(cell: dict) -> int:
    total = 0
    for model, constructs in cell.get("constructs", {}).items():
        total += sum(1 for c in constructs if c.get("left", "").strip() and c.get("right", "").strip())
    return total


# ============================================================
# Aggregations
# ============================================================
def aggregate(cells: list[dict], label: str) -> pd.DataFrame:
    rows = []
    for c in cells:
        task, condition, run_n = parse_cell_id(c.get("cell_id", ""))
        rows.append({
            "design": label,
            "cell_id": c.get("cell_id"),
            "task": task,
            "condition": condition,
            "run": run_n,
            "disagreement": cell_disagreement(c),
            "n_constructs": cell_n_constructs(c),
            "n_raters": len(c.get("ratings", {})),
            "status": c.get("status", "unknown"),
        })
    return pd.DataFrame(rows)


def bootstrap_ci(values: np.ndarray, n_boot: int = 1000, alpha: float = 0.05,
                 seed: int = 42) -> tuple[float, float, float]:
    """Returns (mean, lower, upper)."""
    rng = np.random.default_rng(seed)
    values = values[~np.isnan(values)]
    if len(values) == 0:
        return float("nan"), float("nan"), float("nan")
    means = []
    for _ in range(n_boot):
        sample = rng.choice(values, size=len(values), replace=True)
        means.append(np.mean(sample))
    means = np.array(means)
    return float(np.mean(values)), float(np.percentile(means, 100 * alpha / 2)), \
           float(np.percentile(means, 100 * (1 - alpha / 2)))


# ============================================================
# Main
# ============================================================
def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--cross_dir", default="./results", help="Cross-model results directory")
    p.add_argument("--pilot_dir", default="./results_pilot", help="Pilot results directory")
    p.add_argument("--out", default="./pilot_vs_crossmodel")
    p.add_argument("--n_boot", type=int, default=1000)
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    cross_cells = load_cells(Path(args.cross_dir))
    pilot_cells = load_cells(Path(args.pilot_dir))
    print(f"Cross-model cells: {len(cross_cells)} from {args.cross_dir}")
    print(f"Pilot cells:       {len(pilot_cells)} from {args.pilot_dir}")
    if not cross_cells or not pilot_cells:
        print("ERROR: one or both directories empty")
        return 1

    df_cross = aggregate(cross_cells, "cross_model")
    df_pilot = aggregate(pilot_cells, "pilot")

    # Tasks common to both designs
    tasks_cross = set(df_cross["task"].unique())
    tasks_pilot = set(df_pilot["task"].unique())
    common_tasks = sorted(tasks_cross & tasks_pilot)
    cross_only = sorted(tasks_cross - tasks_pilot)
    pilot_only = sorted(tasks_pilot - tasks_cross)

    print(f"\nTasks in common: {common_tasks}")
    if cross_only:
        print(f"Cross-model only: {cross_only}")
    if pilot_only:
        print(f"Pilot only: {pilot_only}")

    # Per-task aggregates
    per_task_rows = []
    for task in common_tasks:
        c_vals = df_cross[df_cross["task"] == task]["disagreement"].dropna().values
        p_vals = df_pilot[df_pilot["task"] == task]["disagreement"].dropna().values

        c_mean, c_lo, c_hi = bootstrap_ci(c_vals, args.n_boot)
        p_mean, p_lo, p_hi = bootstrap_ci(p_vals, args.n_boot)
        delta_vals = []
        rng = np.random.default_rng(42)
        for _ in range(args.n_boot):
            cs = rng.choice(c_vals, size=len(c_vals), replace=True) if len(c_vals) else np.array([np.nan])
            ps = rng.choice(p_vals, size=len(p_vals), replace=True) if len(p_vals) else np.array([np.nan])
            delta_vals.append(np.mean(cs) - np.mean(ps))
        delta_vals = np.array(delta_vals)
        delta_mean = c_mean - p_mean
        delta_lo = float(np.percentile(delta_vals, 2.5))
        delta_hi = float(np.percentile(delta_vals, 97.5))
        per_task_rows.append({
            "task": task,
            "n_cross_cells": len(c_vals),
            "cross_mean": c_mean,
            "cross_lo95": c_lo,
            "cross_hi95": c_hi,
            "n_pilot_cells": len(p_vals),
            "pilot_mean": p_mean,
            "pilot_lo95": p_lo,
            "pilot_hi95": p_hi,
            "delta_cross_minus_pilot": delta_mean,
            "delta_lo95": delta_lo,
            "delta_hi95": delta_hi,
            "ci_excludes_zero": (delta_lo > 0) or (delta_hi < 0),
        })

    df_per_task = pd.DataFrame(per_task_rows)
    df_per_task.to_csv(out_dir / "per_task_comparison.csv", index=False)

    # Overall comparison
    c_all = df_cross["disagreement"].dropna().values
    p_all = df_pilot["disagreement"].dropna().values
    c_all_mean, c_all_lo, c_all_hi = bootstrap_ci(c_all, args.n_boot)
    p_all_mean, p_all_lo, p_all_hi = bootstrap_ci(p_all, args.n_boot)
    delta_all = c_all_mean - p_all_mean
    delta_vals_all = []
    rng = np.random.default_rng(42)
    for _ in range(args.n_boot):
        cs = rng.choice(c_all, size=len(c_all), replace=True)
        ps = rng.choice(p_all, size=len(p_all), replace=True)
        delta_vals_all.append(np.mean(cs) - np.mean(ps))
    delta_vals_all = np.array(delta_vals_all)
    delta_all_lo = float(np.percentile(delta_vals_all, 2.5))
    delta_all_hi = float(np.percentile(delta_vals_all, 97.5))

    # Print summary
    print("\n=== Headline comparison ===")
    print(f"Cross-model overall:   {c_all_mean:.3f} [{c_all_lo:.3f}, {c_all_hi:.3f}] "
          f"(n={len(c_all)} cells)")
    print(f"Pilot overall:         {p_all_mean:.3f} [{p_all_lo:.3f}, {p_all_hi:.3f}] "
          f"(n={len(p_all)} cells)")
    print(f"Delta (cross - pilot): {delta_all:+.3f} [{delta_all_lo:+.3f}, {delta_all_hi:+.3f}]")
    sig = "SIGNIFICANT" if (delta_all_lo > 0 or delta_all_hi < 0) else "not significant"
    print(f"95% CI on delta: {sig}")

    # Markdown report
    lines = ["# Pilot vs Cross-Model: head-to-head comparison\n\n"]
    lines.append(f"Cross-model design: {len(cross_cells)} cells from `{args.cross_dir}`\n")
    lines.append(f"Pilot design (single Claude in 5 roles): {len(pilot_cells)} cells from `{args.pilot_dir}`\n\n")
    lines.append(f"Tasks in common: {', '.join(common_tasks)}\n\n")

    lines.append("## Headline finding\n\n")
    lines.append(f"| Design | Mean disagreement | 95% CI | n cells |\n")
    lines.append("|---|---|---|---|\n")
    lines.append(f"| Cross-model (5 labs) | **{c_all_mean:.3f}** | [{c_all_lo:.3f}, {c_all_hi:.3f}] | {len(c_all)} |\n")
    lines.append(f"| Pilot (single Claude in 5 roles) | **{p_all_mean:.3f}** | [{p_all_lo:.3f}, {p_all_hi:.3f}] | {len(p_all)} |\n")
    lines.append(f"| **Delta (cross - pilot)** | **{delta_all:+.3f}** | [{delta_all_lo:+.3f}, {delta_all_hi:+.3f}] | - |\n\n")

    if delta_all_lo > 0:
        lines.append("**Interpretation:** Cross-model disagreement is **significantly higher** than "
                     "pilot. The 95% CI on the delta excludes zero, meaning lab diversity provides "
                     "evaluative diversity that single-model persona prompting cannot achieve. This "
                     "is direct evidence that the CM-RG methodology is not redundant with prompt-based "
                     "perspective elicitation.\n\n")
    elif delta_all_hi < 0:
        lines.append("**Interpretation:** Pilot disagreement is **significantly higher** than "
                     "cross-model. Counterintuitive: single-Claude persona role-play generates more "
                     "evaluation diversity than 5 different frontier models. This deserves careful "
                     "investigation; one explanation is that persona prompts unlock latent diversity "
                     "more effectively than swapping providers.\n\n")
    else:
        lines.append("**Interpretation:** Cross-model and pilot disagreement are **not statistically "
                     "distinguishable**. This is a major finding: 5 frontier models produce no more "
                     "evaluative diversity than a single Claude playing 5 roles. CM-RG provides no "
                     "additional signal beyond what's achievable with persona prompting on Claude alone. "
                     "If this holds, the cost-benefit of cross-model audits is severely weakened.\n\n")

    lines.append("## Per-task breakdown\n\n")
    lines.append("| Task | Cross mean | Pilot mean | Delta | 95% CI on delta | CI excludes 0? |\n")
    lines.append("|---|---|---|---|---|---|\n")
    for _, row in df_per_task.iterrows():
        ci_str = f"[{row['delta_lo95']:+.3f}, {row['delta_hi95']:+.3f}]"
        excludes = "YES" if row["ci_excludes_zero"] else "no"
        lines.append(f"| {row['task']} | {row['cross_mean']:.3f} | {row['pilot_mean']:.3f} | "
                     f"{row['delta_cross_minus_pilot']:+.3f} | {ci_str} | {excludes} |\n")

    n_sig_tasks = int(df_per_task["ci_excludes_zero"].sum())
    n_total_tasks = len(df_per_task)
    lines.append(f"\nTasks where 95% CI on delta excludes zero: **{n_sig_tasks} of {n_total_tasks}**.\n\n")

    lines.append("## How to use for paper writing\n\n")
    lines.append("- This analysis goes in **Methods / Methodological validity** section as a "
                 "core argument that lab diversity is not equivalent to persona diversity.\n")
    lines.append("- The headline statement: *\"To rule out that our methodology reduces to "
                 "single-model persona prompting, we replicated the experimental design with a "
                 "single Claude Opus 4.7 playing all 5 personas in turn. Cross-model disagreement "
                 "exceeded pilot disagreement by X.XX (95% CI Y.YY, Z.ZZ), confirming lab diversity "
                 "contributes evaluative variance distinct from prompt-based elicitation.\"*\n")
    lines.append("- Where ci_excludes_zero == YES, that specific task supports the conclusion. "
                 "Tasks where it does not exclude zero are reported in the appendix as caveats.\n\n")

    lines.append("## Caveats\n\n")
    lines.append("- The pilot used a single Claude model snapshot. Other backbones (GPT-5.5 in 5 roles, "
                 "Gemini in 5 roles, etc.) might produce different pilot baselines. We chose Claude "
                 "as the most aligned single-model baseline.\n")
    lines.append("- Run-to-run variance can mimic cross-design variance. The bootstrap CI on delta "
                 "accounts for sampling variability within each design but does not partition "
                 "run-level vs design-level variance. The mixed-effects analysis (see "
                 "MIXED_EFFECTS_FINDINGS.md) provides a complementary view.\n")
    lines.append("- M5 (Kimi) partial dropout (~30% of cells) may inflate cross-model disagreement "
                 "if the dropout pattern is non-random. See M5_SENSITIVITY_FINDINGS.md for "
                 "robustness check.\n")

    (out_dir / "PILOT_VS_CROSSMODEL_FINDINGS.md").write_text("".join(lines), encoding="utf-8")
    print(f"\nWritten: {out_dir}/PILOT_VS_CROSSMODEL_FINDINGS.md")
    print(f"Written: {out_dir}/per_task_comparison.csv")

    # Optional plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Per-task comparison
        ax = axes[0]
        x = np.arange(len(df_per_task))
        width = 0.35
        ax.bar(x - width/2, df_per_task["cross_mean"], width,
               yerr=[df_per_task["cross_mean"] - df_per_task["cross_lo95"],
                     df_per_task["cross_hi95"] - df_per_task["cross_mean"]],
               label="Cross-model", color="steelblue", alpha=0.85, capsize=4)
        ax.bar(x + width/2, df_per_task["pilot_mean"], width,
               yerr=[df_per_task["pilot_mean"] - df_per_task["pilot_lo95"],
                     df_per_task["pilot_hi95"] - df_per_task["pilot_mean"]],
               label="Pilot (single Claude)", color="seagreen", alpha=0.85, capsize=4)
        ax.set_xticks(x)
        ax.set_xticklabels(df_per_task["task"])
        ax.set_xlabel("Task")
        ax.set_ylabel("Mean pairwise disagreement (1-7 scale)")
        ax.set_title("Per-task disagreement: cross-model vs pilot")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)

        # Delta with CI
        ax = axes[1]
        deltas = df_per_task["delta_cross_minus_pilot"].values
        order = np.argsort(deltas)
        deltas_sorted = deltas[order]
        lo_sorted = df_per_task["delta_lo95"].values[order]
        hi_sorted = df_per_task["delta_hi95"].values[order]
        task_sorted = df_per_task["task"].values[order]
        y = np.arange(len(deltas_sorted))
        ax.errorbar(deltas_sorted, y,
                    xerr=[deltas_sorted - lo_sorted, hi_sorted - deltas_sorted],
                    fmt="o", color="darkred", capsize=4)
        ax.axvline(0, color="grey", linestyle="--", alpha=0.7)
        ax.set_yticks(y)
        ax.set_yticklabels(task_sorted)
        ax.set_xlabel("Delta: cross-model - pilot")
        ax.set_title("Per-task delta with 95% bootstrap CI")
        ax.grid(axis="x", alpha=0.3)

        fig.tight_layout()
        plot_path = out_dir / "comparison_plot.png"
        fig.savefig(plot_path, dpi=120)
        print(f"Written: {plot_path}")
    except ImportError:
        print("matplotlib not available; skipping plot")
    except Exception as e:
        print(f"plot error: {e}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
