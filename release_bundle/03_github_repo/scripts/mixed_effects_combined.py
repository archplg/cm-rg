#!/usr/bin/env python3
"""
mixed_effects_combined.py - Wave 4 mixed-effects analysis on the combined dataset.

Загружает все 5 фаз, строит long-form DataFrame ratings и подгоняет два
random-effects регрессии:

  Модель 1 (rater-effect):
    rating ~ task + condition + (1|rater_model) + (1|phase)
    отвечает: «насколько модель-оценщик влияет на ставимую оценку
              после контроля за задачей и условием?»

  Модель 2 (model-effect on Cohere question):
    rating ~ is_cohere + task + condition + (1|rater_model)
    отвечает: «есть ли systematic offset у Cohere после контроля за
              задачей и оценщиком?»

  Модель 3 (calibration after 2H→2J version refresh):
    rating ~ is_opus_48 + task + condition + (1|rater_model)
    с фильтром по rater = M1 или M11 only
    отвечает: «значимо ли изменилась калибровка между Opus 4.7 и 4.8?»

Запуск:
  python mixed_effects_combined.py
"""
from __future__ import annotations
import json
import sys
import warnings
from pathlib import Path
from collections import defaultdict

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

PHASES = {
    "pilot":             Path("results_pilot"),
    "extended":          Path("results_extended"),
    "phase2h":           Path("results_phase2h"),
    "phase2h_extended":  Path("results_phase2h_extended"),
    "phase2j":           Path("results_phase2j"),
}
OUT_DIR = Path("analysis_combined")


def load_long_form() -> pd.DataFrame:
    """Yield long-form rows: phase, cell_id, task, condition, rater, construct_id, element_id, rating."""
    rows = []
    for phase_name, path in PHASES.items():
        if not path.exists(): continue
        for cell_dir in sorted(path.iterdir()):
            if not cell_dir.is_dir(): continue
            cj = cell_dir / "cell.json"
            if not cj.exists(): continue
            try:
                data = json.loads(cj.read_text(encoding='utf-8'))
            except Exception:
                continue
            task = data.get('task', '?')
            cond = data.get('condition', '?')
            for rater, rater_constructs in data.get('ratings', {}).items():
                for cid, ele_map in rater_constructs.items():
                    if not isinstance(ele_map, dict): continue
                    for ek, v in ele_map.items():
                        if isinstance(v, (int, float)) and 1 <= v <= 7:
                            rows.append({
                                'phase': phase_name,
                                'task': task,
                                'condition': cond,
                                'rater': rater,
                                'construct_id': cid,
                                'element_id': ek,
                                'rating': float(v),
                            })
    return pd.DataFrame(rows)


def fit_mixed_lm(df: pd.DataFrame, formula: str, groups_col: str, label: str):
    """Fit a MixedLM and return key results."""
    import statsmodels.formula.api as smf
    print(f"\n--- {label} ---")
    print(f"Formula: {formula}")
    print(f"Random groups: {groups_col}")
    print(f"N observations: {len(df):,}")
    try:
        model = smf.mixedlm(formula, df, groups=df[groups_col])
        result = model.fit(method="lbfgs", reml=False)
    except Exception as e:
        print(f"  ERROR: {e}")
        return None
    # Extract fixed effects
    fe = result.fe_params.to_dict()
    se = result.bse_fe.to_dict()
    pvals = result.pvalues_fe.to_dict() if hasattr(result, "pvalues_fe") else result.pvalues.to_dict()
    re_var = float(result.cov_re.iloc[0, 0]) if result.cov_re.shape[0] >= 1 else 0
    out = {
        "label": label,
        "formula": formula,
        "n_obs": len(df),
        "fixed_effects": {k: {"beta": float(fe[k]), "se": float(se[k]), "p": float(pvals[k])} for k in fe},
        "random_effect_variance": re_var,
        "scale": float(result.scale),
        "loglik": float(result.llf),
    }
    # Print summary
    print(f"  Random effect variance ({groups_col}): {re_var:.4f}")
    print(f"  Residual variance: {result.scale:.4f}")
    print(f"  ICC (intra-class correlation): {re_var / (re_var + result.scale):.4f}")
    print(f"  Fixed effects (top 5 by |beta|):")
    sorted_fe = sorted(fe.items(), key=lambda kv: -abs(kv[1]))[:8]
    for k, b in sorted_fe:
        p = pvals[k]
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"    {k:<35} β={b:+.4f}  SE={se[k]:.4f}  p={p:.4g} {sig}")
    return out


def main():
    OUT_DIR.mkdir(exist_ok=True)
    print("[1/4] Loading long-form ratings from all phases ...")
    df = load_long_form()
    print(f"      {len(df):,} ratings loaded")
    print(f"      Models: {sorted(df['rater'].unique())}")
    print(f"      Tasks: {sorted(df['task'].unique())}")
    print(f"      Conditions: {sorted(df['condition'].unique())}")
    print(f"      Phases: {sorted(df['phase'].unique())}")

    # Categoricals
    df['task'] = df['task'].astype('category')
    df['condition'] = df['condition'].astype('category')
    df['rater'] = df['rater'].astype('category')
    df['phase'] = df['phase'].astype('category')
    df['is_cohere'] = (df['rater'] == 'M7').astype(int)
    df['is_opus_48'] = (df['rater'] == 'M11').astype(int)

    results = {}

    # Model 1: full rater-effect after task+condition control
    print("\n[2/4] Model 1: rater-effect after controlling for task + condition")
    m1_df = df.copy()
    res1 = fit_mixed_lm(
        m1_df,
        formula="rating ~ C(task) + C(condition)",
        groups_col="rater",
        label="Model 1: rating ~ task + condition + (1|rater)",
    )
    results["model_1_rater_effect"] = res1

    # Model 2: Cohere offset after model-rater random effect
    print("\n[3/4] Model 2: is_cohere offset")
    m2_df = df.copy()
    res2 = fit_mixed_lm(
        m2_df,
        formula="rating ~ is_cohere + C(task) + C(condition)",
        groups_col="rater",
        label="Model 2: rating ~ is_cohere + task + condition + (1|rater)",
    )
    results["model_2_cohere_offset"] = res2

    # Model 3: Opus 4.7 vs 4.8 within-family
    print("\n[4/4] Model 3: Opus 4.7 vs 4.8 calibration shift")
    m3_df = df[df['rater'].isin(['M1', 'M11'])].copy()
    print(f"      Subset N = {len(m3_df):,}")
    res3 = fit_mixed_lm(
        m3_df,
        formula="rating ~ is_opus_48 + C(task) + C(condition)",
        groups_col="construct_id",  # random effect per construct
        label="Model 3: rating ~ is_opus_48 + task + condition + (1|construct), rater∈{M1,M11}",
    )
    results["model_3_opus48_calibration"] = res3

    # Save
    out_path = OUT_DIR / "mixed_effects.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults -> {out_path}")

    # Quick verdicts
    print("\n=== VERDICTS ===")
    if res2:
        cohere_fx = res2["fixed_effects"].get("is_cohere", {})
        beta = cohere_fx.get("beta", 0); p = cohere_fx.get("p", 1)
        verdict = (
            f"Cohere offset after controlling for task/condition/rater: "
            f"β = {beta:+.3f}, p = {p:.2g}. "
            f"{'CONFIRMED (significant)' if p < 0.001 else 'WEAK' if p > 0.05 else 'MODERATE'}"
        )
        print(f"  {verdict}")
    if res3:
        opus48_fx = res3["fixed_effects"].get("is_opus_48", {})
        beta = opus48_fx.get("beta", 0); p = opus48_fx.get("p", 1)
        verdict = (
            f"Opus 4.8 vs 4.7 calibration shift after controlling for task/condition: "
            f"β = {beta:+.4f}, p = {p:.2g}. "
            f"{'NO SHIFT (null result)' if p > 0.05 else 'WEAK shift' if p < 0.05 else 'shift'}"
        )
        print(f"  {verdict}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
