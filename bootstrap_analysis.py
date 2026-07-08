#!/usr/bin/env python3
"""
Bootstrap confidence intervals for all key metrics on the Archipelago dataset.

Provides 95% CIs (1000 resamples by default) for:
  - Overall mean pairwise disagreement
  - Per-task mean disagreement (and condition breakdowns)
  - Per-condition (N vs P) mean disagreement
  - Procrustes mean disparity (Platonic Hypothesis test)
  - Variance decomposition (task / persona / model / condition)
  - Cross-model vs pilot delta (per task)

Outputs:
  bootstrap_analysis/bootstrap_results.json
  bootstrap_analysis/BOOTSTRAP_FINDINGS.md
  bootstrap_analysis/forest_plot_*.png

Run:
    pip install pyarrow pandas scipy scikit-learn sentence-transformers matplotlib
    python bootstrap_analysis.py [--n_boot 1000] [--seed 42]
"""
from __future__ import annotations
import argparse
import json
import warnings
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.spatial import procrustes
from sklearn.decomposition import PCA

warnings.filterwarnings("ignore")

RESULTS_DIR = Path("./results")
ANALYSIS_DIR = Path("./analysis")
OUT_DIR = Path("./bootstrap_analysis")

# Pilot reference values (from PROTOCOL.md)
PILOT = {
    "A": {"disagreement": 0.31, "pc1_pc2": 0.776},
    "B": {"disagreement": 0.14, "pc1_pc2": 0.757},
}


# ============================================================
# Data loading
# ============================================================
def load_cell_summaries() -> pd.DataFrame:
    """Load per-cell summary metrics from analysis/all_summaries.json."""
    p = ANALYSIS_DIR / "all_summaries.json"
    if not p.exists():
        return pd.DataFrame()
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    summaries = data.get("summaries", [])
    return pd.DataFrame([s for s in summaries if s.get("status") != "no_data"])


def load_long_ratings() -> pd.DataFrame:
    """Load long-format ratings from results/*/cell.json."""
    if not RESULTS_DIR.exists():
        return pd.DataFrame()
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
        for rater, rdata in cell.get("ratings", {}).items():
            for cid, elem_ratings in rdata.items():
                for ek, val in elem_ratings.items():
                    rows.append({
                        "cell_id": cd.name,
                        "task": cell.get("task"),
                        "condition": cell.get("condition"),
                        "rater": rater,
                        "construct_id": cid,
                        "element": ek,
                        "rating": int(val),
                    })
    return pd.DataFrame(rows)


# ============================================================
# Bootstrap routines
# ============================================================
def bootstrap_ci(values: np.ndarray, n_boot: int = 1000, seed: int = 42, ci: float = 0.95) -> dict:
    """Compute mean + bootstrap CI for a 1D array."""
    rng = np.random.default_rng(seed)
    values = np.asarray(values, dtype=float)
    values = values[~np.isnan(values)]
    if len(values) < 2:
        return {"mean": float(values.mean()) if len(values) else float("nan"),
                "ci_low": None, "ci_high": None, "n": len(values)}
    boots = np.empty(n_boot)
    n = len(values)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        boots[i] = values[idx].mean()
    alpha = (1 - ci) / 2
    return {
        "mean": float(values.mean()),
        "ci_low": float(np.quantile(boots, alpha)),
        "ci_high": float(np.quantile(boots, 1 - alpha)),
        "n": int(n),
        "boot_sd": float(boots.std()),
    }


def bootstrap_paired_delta(values_a: np.ndarray, values_b: np.ndarray,
                            n_boot: int = 1000, seed: int = 42, ci: float = 0.95) -> dict:
    """Bootstrap CI for paired (A - B) difference."""
    rng = np.random.default_rng(seed)
    a = np.asarray(values_a, dtype=float)
    b = np.asarray(values_b, dtype=float)
    mask = ~(np.isnan(a) | np.isnan(b))
    a, b = a[mask], b[mask]
    if len(a) < 2:
        return {"mean_delta": float(a.mean() - b.mean()) if len(a) else float("nan"),
                "ci_low": None, "ci_high": None, "n_pairs": len(a)}
    delta = a - b
    boots = np.empty(n_boot)
    n = len(delta)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        boots[i] = delta[idx].mean()
    alpha = (1 - ci) / 2
    return {
        "mean_delta": float(delta.mean()),
        "ci_low": float(np.quantile(boots, alpha)),
        "ci_high": float(np.quantile(boots, 1 - alpha)),
        "n_pairs": int(n),
        "boot_sd": float(boots.std()),
    }


# ============================================================
# Procrustes bootstrap (for Platonic Hypothesis test)
# ============================================================
def compute_pairwise_procrustes(df_long: pd.DataFrame, cell_ids: list) -> float:
    """For a subset of cells, compute mean pairwise Procrustes disparity across models."""
    sub = df_long[df_long["cell_id"].isin(cell_ids)]
    if sub.empty:
        return float("nan")
    models = sorted(sub["rater"].unique())
    if len(models) < 2:
        return float("nan")
    # Build (cell, element) x construct matrix per model
    pivots = {}
    for m in models:
        try:
            piv = sub[sub["rater"] == m].pivot_table(
                index=["cell_id", "element"], columns="construct_id",
                values="rating", aggfunc="mean"
            )
            pivots[m] = piv
        except Exception:
            continue
    # Align grids
    common_idx = None
    common_cols = None
    for piv in pivots.values():
        common_idx = piv.index if common_idx is None else common_idx.intersection(piv.index)
        common_cols = piv.columns if common_cols is None else common_cols.intersection(piv.columns)
    if common_idx is None or len(common_idx) < 3 or len(common_cols) < 2:
        return float("nan")
    disps = []
    for a, b in combinations(models, 2):
        ma = pivots[a].loc[common_idx, common_cols].fillna(4.0).values
        mb = pivots[b].loc[common_idx, common_cols].fillna(4.0).values
        try:
            _, _, d = procrustes(ma, mb)
            disps.append(d)
        except Exception:
            pass
    return float(np.mean(disps)) if disps else float("nan")


def bootstrap_procrustes(df_long: pd.DataFrame, n_boot: int = 200, seed: int = 42, ci: float = 0.95) -> dict:
    """Bootstrap mean Procrustes disparity by resampling cells with replacement."""
    rng = np.random.default_rng(seed)
    all_cells = sorted(df_long["cell_id"].unique())
    point_estimate = compute_pairwise_procrustes(df_long, all_cells)
    if np.isnan(point_estimate):
        return {"mean": None, "ci_low": None, "ci_high": None, "n_boot": 0}
    n = len(all_cells)
    boots = []
    print(f"  Running {n_boot} Procrustes bootstrap resamples (slow)...")
    for i in range(n_boot):
        if (i + 1) % 20 == 0:
            print(f"    {i+1}/{n_boot} done")
        idx = rng.integers(0, n, n)
        sampled = [all_cells[j] for j in idx]
        disp = compute_pairwise_procrustes(df_long, sampled)
        if not np.isnan(disp):
            boots.append(disp)
    if len(boots) < 10:
        return {"mean": point_estimate, "ci_low": None, "ci_high": None, "n_boot": len(boots)}
    boots = np.array(boots)
    alpha = (1 - ci) / 2
    return {
        "mean": float(point_estimate),
        "ci_low": float(np.quantile(boots, alpha)),
        "ci_high": float(np.quantile(boots, 1 - alpha)),
        "n_boot": int(len(boots)),
        "boot_sd": float(boots.std()),
        "boots_n_valid": int(len(boots)),
    }


# ============================================================
# Variance decomposition bootstrap
# ============================================================
def compute_variance_decomp(df_long: pd.DataFrame, cell_ids: list = None) -> dict:
    """Simple variance decomposition on rating values - what fraction of variance
    is explained by task vs condition vs rater vs cell?"""
    sub = df_long if cell_ids is None else df_long[df_long["cell_id"].isin(cell_ids)]
    if len(sub) < 100:
        return {}
    total_var = sub["rating"].var()
    if total_var <= 0:
        return {}
    parts = {}
    for factor in ["task", "condition", "rater", "cell_id"]:
        group_means = sub.groupby(factor)["rating"].transform("mean")
        between = ((group_means - sub["rating"].mean()) ** 2).mean()
        parts[factor] = float(between / total_var)
    return parts


def bootstrap_variance_decomp(df_long: pd.DataFrame, n_boot: int = 200, seed: int = 42, ci: float = 0.95) -> dict:
    """Bootstrap variance decomposition by resampling cells."""
    rng = np.random.default_rng(seed)
    all_cells = sorted(df_long["cell_id"].unique())
    point = compute_variance_decomp(df_long, all_cells)
    if not point:
        return {}
    boots_by_factor = {k: [] for k in point}
    n = len(all_cells)
    print(f"  Running {n_boot} variance-decomp bootstrap resamples...")
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        sampled = [all_cells[j] for j in idx]
        parts = compute_variance_decomp(df_long, sampled)
        for k, v in parts.items():
            boots_by_factor[k].append(v)
    alpha = (1 - ci) / 2
    out = {}
    for k, vals in boots_by_factor.items():
        if len(vals) < 10:
            out[k] = {"point": point.get(k), "ci_low": None, "ci_high": None}
            continue
        arr = np.array(vals)
        out[k] = {
            "point": float(point.get(k, 0)),
            "ci_low": float(np.quantile(arr, alpha)),
            "ci_high": float(np.quantile(arr, 1 - alpha)),
            "n_boot": int(len(vals)),
        }
    return out


# ============================================================
# Forest plot
# ============================================================
def forest_plot(results: dict, out_path: Path):
    """Plot all metrics with mean +- 95% CI."""
    items = []
    for name, r in results.items():
        if isinstance(r, dict) and r.get("ci_low") is not None and r.get("ci_high") is not None:
            items.append((name, r.get("mean", r.get("point", r.get("mean_delta", 0))),
                          r["ci_low"], r["ci_high"]))
    if not items:
        return
    items.reverse()
    labels = [it[0] for it in items]
    means = [it[1] for it in items]
    lows = [it[2] for it in items]
    highs = [it[3] for it in items]
    yy = range(len(items))
    fig, ax = plt.subplots(figsize=(10, max(4, len(items) * 0.45)), facecolor="white")
    for i, (m, l, h) in enumerate(zip(means, lows, highs)):
        ax.plot([l, h], [i, i], color="#0a558c", linewidth=3)
        ax.scatter(m, i, color="#0a558c", s=80, zorder=5, edgecolor="black", linewidth=1)
    ax.set_yticks(list(yy))
    ax.set_yticklabels(labels, fontsize=9)
    ax.axvline(0, color="gray", linestyle="--", alpha=0.4)
    ax.set_xlabel("Estimate (mean +- 95% CI)")
    ax.set_title("Bootstrap confidence intervals")
    plt.tight_layout()
    plt.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close()


# ============================================================
# Main
# ============================================================
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_boot", type=int, default=1000, help="Bootstrap resamples")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default=str(OUT_DIR))
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading data...")
    df_cells = load_cell_summaries()
    df_long = load_long_ratings()
    print(f"  Cells: {len(df_cells)}")
    print(f"  Long ratings: {len(df_long)}")
    if df_cells.empty:
        print("ERROR: no summaries. Run analyze.py first.")
        return 1

    results = {}

    # 1. Overall mean disagreement
    print("\n[1/6] Overall mean disagreement...")
    r = bootstrap_ci(df_cells["mean_pairwise_disagreement"].values, args.n_boot, args.seed)
    results["overall_disagreement"] = r
    print(f"  {r['mean']:.3f} (95% CI {r['ci_low']:.3f} - {r['ci_high']:.3f}, n={r['n']})")

    # 2. Per-task disagreement
    print("\n[2/6] Per-task disagreement...")
    for task in sorted(df_cells["task"].dropna().unique()):
        vals = df_cells[df_cells["task"] == task]["mean_pairwise_disagreement"].values
        r = bootstrap_ci(vals, args.n_boot, args.seed)
        results[f"task_{task}_disagreement"] = r
        print(f"  Task {task}: {r['mean']:.3f} ({r['ci_low']:.3f} - {r['ci_high']:.3f}, n={r['n']})")

    # 3. Per-condition disagreement (N vs P)
    print("\n[3/6] Condition effect (N vs P paired by task)...")
    # Pair by task: mean N vs mean P per task
    n_means = df_cells[df_cells["condition"] == "N"].groupby("task")["mean_pairwise_disagreement"].mean()
    p_means = df_cells[df_cells["condition"] == "P"].groupby("task")["mean_pairwise_disagreement"].mean()
    common_tasks = sorted(set(n_means.index) & set(p_means.index))
    if common_tasks:
        n_arr = np.array([n_means[t] for t in common_tasks])
        p_arr = np.array([p_means[t] for t in common_tasks])
        r = bootstrap_paired_delta(p_arr, n_arr, args.n_boot, args.seed)
        results["persona_minus_neutral_paired"] = r
        print(f"  Δ(P-N): {r['mean_delta']:+.3f} ({r['ci_low']:+.3f} - {r['ci_high']:+.3f}, n_pairs={r['n_pairs']})")

    # 4. Cross-model vs pilot delta (per task A and B)
    print("\n[4/6] Cross-model vs pilot delta...")
    for task in ["A", "B"]:
        vals = df_cells[df_cells["task"] == task]["mean_pairwise_disagreement"].values
        if len(vals) == 0:
            continue
        pilot_val = PILOT[task]["disagreement"]
        delta_vals = vals - pilot_val
        r = bootstrap_ci(delta_vals, args.n_boot, args.seed)
        results[f"task_{task}_cross_minus_pilot"] = r
        print(f"  Task {task} delta vs pilot ({pilot_val:.2f}): {r['mean']:+.3f} ({r['ci_low']:+.3f} - {r['ci_high']:+.3f})")

    # 5. Procrustes disparity bootstrap
    print("\n[5/6] Procrustes disparity (Platonic Hypothesis)...")
    if not df_long.empty:
        r = bootstrap_procrustes(df_long, n_boot=min(args.n_boot, 200), seed=args.seed)
        results["procrustes_disparity"] = r
        if r.get("ci_low") is not None:
            verdict = "rejected" if r["ci_low"] > 0.3 else ("supported" if r["ci_high"] < 0.3 else "ambiguous")
            print(f"  {r['mean']:.3f} (95% CI {r['ci_low']:.3f} - {r['ci_high']:.3f}) - Platonic Hyp: {verdict}")

    # 6. Variance decomposition bootstrap
    print("\n[6/6] Variance decomposition (task / condition / rater / cell)...")
    if not df_long.empty:
        var_results = bootstrap_variance_decomp(df_long, n_boot=min(args.n_boot, 200), seed=args.seed)
        for factor, r in var_results.items():
            results[f"variance_{factor}"] = r
            if r.get("ci_low") is not None:
                print(f"  {factor}: {r['point']*100:.1f}% ({r['ci_low']*100:.1f}% - {r['ci_high']*100:.1f}%)")

    # Save JSON
    with open(out_dir / "bootstrap_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, default=str)

    # Forest plot
    forest_plot(results, out_dir / "forest_plot.png")

    # Markdown report
    lines = ["# Bootstrap Confidence Intervals\n\n"]
    lines.append(f"Generated by bootstrap_analysis.py with {args.n_boot} resamples, seed={args.seed}\n\n")
    lines.append("## Headline numbers\n\n")
    lines.append("| Metric | Point estimate | 95% CI | Interpretation |\n")
    lines.append("|---|---|---|---|\n")
    for name, r in results.items():
        if not isinstance(r, dict):
            continue
        point = r.get("mean", r.get("point", r.get("mean_delta")))
        if point is None or r.get("ci_low") is None:
            continue
        ci_str = f"[{r['ci_low']:.3f}, {r['ci_high']:.3f}]"
        if "variance_" in name:
            pct = point * 100
            ci_lo = r['ci_low'] * 100
            ci_hi = r['ci_high'] * 100
            ci_str = f"[{ci_lo:.1f}%, {ci_hi:.1f}%]"
            lines.append(f"| {name} | {pct:.1f}% | {ci_str} | |\n")
        else:
            lines.append(f"| {name} | {point:+.3f} | {ci_str} | |\n")

    lines.append("\n## How to read\n\n")
    lines.append("- **CI excludes 0** -> effect is reliably non-zero in the bootstrapped distribution.\n")
    lines.append("- **CI width** = uncertainty. Tight CI = stable estimate. Wide CI = need more data.\n")
    lines.append("- **Procrustes < 0.3** -> Platonic Hypothesis supported. **> 0.3** -> rejected. CI tells you the conclusion's robustness.\n")
    lines.append("- **Variance decomposition**: each factor's share of total rating variance. Higher = bigger driver.\n")

    (out_dir / "BOOTSTRAP_FINDINGS.md").write_text("".join(lines), encoding="utf-8")
    print(f"\nAll done. See {out_dir}/BOOTSTRAP_FINDINGS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
