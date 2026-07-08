#!/usr/bin/env python3
"""
Archipelago-for-Agents cross-model - analysis pipeline.

Loads all cell results from ./results/<cell_id>/cell.json, computes metrics
per cell and across cells, generates plots and FINDINGS.md.

Run:
    python analyze.py                  # process all complete cells
    python analyze.py --cell A_N_run1  # one cell only
"""
from __future__ import annotations
import argparse
import json
import warnings
from itertools import combinations
from pathlib import Path
from statistics import mean, stdev

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from scipy.stats import pearsonr, ttest_rel
from sklearn.decomposition import PCA

warnings.filterwarnings("ignore", category=RuntimeWarning)

RESULTS_DIR = Path("./results")
ANALYSIS_DIR = Path("./analysis")

# Reference values from the pilot (Claude-only, role-played, May 2026)
PILOT_REFERENCE = {
    "A": {
        "mean_pairwise_disagreement": 0.31,
        "pc1_pc2_variance": 0.776,
        "n_high_corr_pairs": 16,
        "n_constructs": 15,
    },
    "B": {
        "mean_pairwise_disagreement": 0.14,
        "pc1_pc2_variance": 0.757,
        "n_high_corr_pairs": 18,
        "n_constructs": 15,
    },
}


# ============================================================
# Load cells
# ============================================================
def load_cell(cell_dir: Path) -> dict | None:
    cell_file = cell_dir / "cell.json"
    if not cell_file.exists():
        return None
    with open(cell_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_cells() -> dict[str, dict]:
    cells = {}
    for cd in RESULTS_DIR.iterdir():
        if cd.is_dir() and cd.name not in ("state",):
            data = load_cell(cd)
            if data and data.get("status", "").startswith("complete"):
                cells[cd.name] = data
    return cells


# ============================================================
# Per-cell analysis
# ============================================================
def cell_to_long_dataframe(cell: dict) -> pd.DataFrame | None:
    """Convert cell ratings to long-form DataFrame for analysis."""
    rows = []
    all_constructs = []
    for sn in sorted(cell.get("constructs", {}).keys()):
        all_constructs.extend(cell["constructs"][sn])
    if not all_constructs:
        return None
    construct_lookup = {c["id"]: c for c in all_constructs}
    for rater_sn, rating_dict in cell.get("ratings", {}).items():
        for cid, elem_ratings in rating_dict.items():
            for ek, val in elem_ratings.items():
                rows.append({
                    "rater": rater_sn,
                    "construct": cid,
                    "construct_origin": cid.split("_")[1] if "_" in cid else "?",
                    "element": ek,
                    "rating": val,
                    "left": construct_lookup.get(cid, {}).get("left", ""),
                    "right": construct_lookup.get(cid, {}).get("right", ""),
                })
    if not rows:
        return None
    return pd.DataFrame(rows)


def analyze_cell(cell_id: str, cell: dict) -> dict:
    """Run full per-cell analysis. Return summary metrics."""
    out_dir = ANALYSIS_DIR / cell_id
    out_dir.mkdir(parents=True, exist_ok=True)
    df = cell_to_long_dataframe(cell)
    if df is None or df.empty:
        return {"cell_id": cell_id, "status": "no_data"}

    constructs = sorted(df["construct"].unique())
    elements = sorted(df["element"].unique())
    raters = sorted(df["rater"].unique())

    # Build mean-rating matrix: (element x construct)
    mean_mat = np.zeros((len(elements), len(constructs)))
    for j, c in enumerate(constructs):
        sub = df[df["construct"] == c]
        for i, e in enumerate(elements):
            vals = sub[sub["element"] == e]["rating"].values
            if len(vals) > 0:
                mean_mat[i, j] = np.mean(vals)
            else:
                mean_mat[i, j] = np.nan

    # Drop incomplete columns/rows
    valid_cols = ~np.isnan(mean_mat).any(axis=0)
    valid_rows = ~np.isnan(mean_mat).any(axis=1)
    constructs_v = [c for c, v in zip(constructs, valid_cols) if v]
    elements_v = [e for e, v in zip(elements, valid_rows) if v]
    mat = mean_mat[np.ix_(valid_rows, valid_cols)]

    # Construct correlation matrix
    n_c = len(constructs_v)
    corr = np.zeros((n_c, n_c))
    for i in range(n_c):
        for j in range(n_c):
            v1, v2 = mat[:, i], mat[:, j]
            if np.std(v1) > 1e-9 and np.std(v2) > 1e-9:
                corr[i, j], _ = pearsonr(v1, v2)
            else:
                corr[i, j] = 0.0
    high_corr_pairs = [
        (constructs_v[i], constructs_v[j], corr[i, j])
        for i in range(n_c) for j in range(n_c)
        if i < j and abs(corr[i, j]) > 0.85
    ]
    saturated_pairs = [
        (constructs_v[i], constructs_v[j], corr[i, j])
        for i in range(n_c) for j in range(n_c)
        if i < j and abs(corr[i, j]) > 0.95
    ]

    # Hierarchical clustering
    n_clusters_at_k = {}
    if n_c >= 2:
        dist = 1 - np.abs(corr)
        np.fill_diagonal(dist, 0)
        try:
            cond = squareform(dist, checks=False)
            linkage_mat = linkage(cond, method="average")
            for k in [3, 4, 5, 6, 7]:
                if k <= n_c:
                    clusters = fcluster(linkage_mat, t=k, criterion="maxclust")
                    n_clusters_at_k[k] = len(set(clusters))
        except Exception:
            pass

    # PCA
    pca_summary = {"pc1": 0.0, "pc2": 0.0, "pc3": 0.0}
    if mat.shape[0] >= 2 and mat.shape[1] >= 2:
        try:
            n_comp = min(3, mat.shape[0] - 1, mat.shape[1])
            pca = PCA(n_components=n_comp)
            coords = pca.fit_transform(mat)
            evr = pca.explained_variance_ratio_
            for i, key in enumerate(["pc1", "pc2", "pc3"]):
                pca_summary[key] = float(evr[i]) if i < len(evr) else 0.0
            # Save biplot
            plt.figure(figsize=(9, 7))
            for i, e in enumerate(elements_v):
                plt.scatter(coords[i, 0], coords[i, 1], s=200, alpha=0.7, edgecolors="black")
                plt.annotate(e, (coords[i, 0], coords[i, 1]), xytext=(7, 7),
                             textcoords="offset points", fontsize=11, fontweight="bold")
            plt.axhline(0, color="gray", linestyle="--", alpha=0.3)
            plt.axvline(0, color="gray", linestyle="--", alpha=0.3)
            plt.xlabel(f"PC1 ({pca_summary['pc1']*100:.1f}%)")
            plt.ylabel(f"PC2 ({pca_summary['pc2']*100:.1f}%)")
            plt.title(f"Element biplot - {cell_id}")
            plt.tight_layout()
            plt.savefig(out_dir / "biplot.png", dpi=130, bbox_inches="tight")
            plt.close()
        except Exception as e:
            pca_summary["error"] = str(e)

    # Pairwise rater agreement
    pair_disagreements = {}
    for r1, r2 in combinations(raters, 2):
        d1 = df[df["rater"] == r1].set_index(["construct", "element"])["rating"]
        d2 = df[df["rater"] == r2].set_index(["construct", "element"])["rating"]
        common = d1.index.intersection(d2.index)
        if len(common) == 0:
            continue
        diffs = (d1.loc[common] - d2.loc[common]).abs()
        pair_disagreements[f"{r1}_{r2}"] = float(diffs.mean())
    mean_disagreement = float(np.mean(list(pair_disagreements.values()))) if pair_disagreements else float("nan")

    # Lacuna candidates: low discrimination + mid-scale
    lacuna_candidates = []
    for j, c in enumerate(constructs_v):
        col = mat[:, j]
        if np.std(col) < 1.0 and 3.5 <= np.mean(col) <= 4.5:
            lacuna_candidates.append(c)

    # Save corr heatmap
    if n_c >= 2:
        plt.figure(figsize=(max(8, n_c * 0.6), max(7, n_c * 0.55)))
        sns.heatmap(pd.DataFrame(corr, index=constructs_v, columns=constructs_v),
                    annot=True, fmt=".2f", cmap="RdBu_r", center=0, vmin=-1, vmax=1,
                    square=True, cbar_kws={"label": "r"})
        plt.title(f"Construct correlations - {cell_id}")
        plt.tight_layout()
        plt.savefig(out_dir / "corr_heatmap.png", dpi=130, bbox_inches="tight")
        plt.close()

    # Save ratings long form
    df.to_csv(out_dir / "ratings_long.csv", index=False)

    summary = {
        "cell_id": cell_id,
        "task": cell.get("task"),
        "condition": cell.get("condition"),
        "run_idx": cell.get("run_idx"),
        "n_constructs": n_c,
        "n_elements": len(elements_v),
        "n_raters": len(raters),
        "mean_pairwise_disagreement": mean_disagreement,
        "n_high_corr_pairs": len(high_corr_pairs),
        "n_saturated_pairs": len(saturated_pairs),
        "pct_high_corr": len(high_corr_pairs) / max(1, n_c * (n_c - 1) / 2),
        "pca_pc1": pca_summary["pc1"],
        "pca_pc2": pca_summary["pc2"],
        "pca_pc3": pca_summary["pc3"],
        "pca_pc1_plus_pc2": pca_summary["pc1"] + pca_summary["pc2"],
        "n_clusters_at_k": n_clusters_at_k,
        "lacuna_candidates": lacuna_candidates,
        "pair_disagreements": pair_disagreements,
        "cost_usd": cell.get("cost_usd", 0.0),
        "errors": cell.get("errors", []),
    }
    return summary


# ============================================================
# Cross-cell analyses
# ============================================================
def hypothesis_evaluation(summaries: list[dict]) -> dict:
    """Evaluate against pre-registered falsification criteria."""
    evals = {}
    # Per task A and B vs pilot
    for task in ["A", "B"]:
        per_task = [s for s in summaries if s.get("task") == task]
        if not per_task:
            continue
        pilot = PILOT_REFERENCE[task]
        means = {
            "mean_pairwise_disagreement": mean(s["mean_pairwise_disagreement"] for s in per_task if not np.isnan(s["mean_pairwise_disagreement"])),
            "pc1_pc2_variance": mean(s["pca_pc1_plus_pc2"] for s in per_task),
        }
        evals[f"task_{task}"] = {
            "pilot_disagreement": pilot["mean_pairwise_disagreement"],
            "cross_model_disagreement": means["mean_pairwise_disagreement"],
            "delta": means["mean_pairwise_disagreement"] - pilot["mean_pairwise_disagreement"],
            "predicted_range": "0.6 to 1.5",
            "headline_test": (
                "EXPECTED" if 0.6 <= means["mean_pairwise_disagreement"] <= 1.5
                else "BELOW expected (still convergent)" if means["mean_pairwise_disagreement"] < 0.6
                else "ABOVE expected (high divergence)"
            ),
        }

    # H1: distinct cluster count
    h1_failures = []
    for s in summaries:
        n_clust = s["n_clusters_at_k"].get(6, 0) if isinstance(s["n_clusters_at_k"], dict) else 0
        if n_clust < 4:
            h1_failures.append(s["cell_id"])
    evals["H1_failures"] = h1_failures

    # H2: PC1+PC2 < 60%
    h2_failures = [s["cell_id"] for s in summaries if s["pca_pc1_plus_pc2"] < 0.60]
    evals["H2_failures"] = h2_failures

    # H3: mean disagreement
    all_d = [s["mean_pairwise_disagreement"] for s in summaries if not np.isnan(s["mean_pairwise_disagreement"])]
    if all_d:
        evals["H3_overall_mean_disagreement"] = mean(all_d)
        evals["H3_min_disagreement"] = min(all_d)
        evals["H3_max_disagreement"] = max(all_d)
        if all(d < 0.5 for d in all_d):
            evals["H3_status"] = "FAILED - cross-model agents converge as severely as same-model"
        elif any(d > 2.5 for d in all_d):
            evals["H3_status"] = "FAILED - excessive divergence; method extracts noise not structure"
        elif mean(all_d) >= 0.6:
            evals["H3_status"] = "SUPPORTED - cross-model produces meaningful disagreement signal"
        else:
            evals["H3_status"] = "MARGINAL - some signal but below predicted range"

    return evals


def condition_comparison(summaries: list[dict]) -> dict:
    """Compare N (neutral) vs P (persona) conditions."""
    n_cells = {s["task"]: s for s in summaries if s["condition"] == "N" and s["run_idx"] == 1}
    p_cells = {s["task"]: s for s in summaries if s["condition"] == "P" and s["run_idx"] == 1}
    shared = set(n_cells.keys()) & set(p_cells.keys())
    if len(shared) < 2:
        return {"note": "insufficient paired data"}
    out = {}
    for metric in ["mean_pairwise_disagreement", "pca_pc1_plus_pc2", "n_high_corr_pairs"]:
        n_vals = [n_cells[t][metric] for t in shared]
        p_vals = [p_cells[t][metric] for t in shared]
        out[metric] = {
            "neutral_mean": float(mean(n_vals)),
            "persona_mean": float(mean(p_vals)),
            "delta_persona_minus_neutral": float(mean(p_vals) - mean(n_vals)),
        }
        if len(shared) >= 3:
            try:
                t, p = ttest_rel(p_vals, n_vals)
                out[metric]["t_stat"] = float(t)
                out[metric]["p_value"] = float(p)
            except Exception:
                pass
    return out


def repeat_variance(summaries: list[dict]) -> dict:
    """Estimate run-to-run variance for Task B repeats."""
    out = {}
    for cond in ["N", "P"]:
        runs = [s for s in summaries if s["task"] == "B" and s["condition"] == cond]
        if len(runs) < 2:
            continue
        for metric in ["mean_pairwise_disagreement", "pca_pc1_plus_pc2", "n_high_corr_pairs"]:
            vals = [r[metric] for r in runs]
            m = mean(vals)
            sd = stdev(vals) if len(vals) > 1 else 0.0
            cv = (sd / m) if m else 0.0
            out[f"B_{cond}_{metric}"] = {
                "n_runs": len(runs),
                "mean": float(m),
                "sd": float(sd),
                "coef_var": float(cv),
                "values": [float(v) for v in vals],
            }
    return out


# ============================================================
# Reporting
# ============================================================
def write_findings(summaries: list[dict], evals: dict, cond_comp: dict, rep_var: dict) -> None:
    ANALYSIS_DIR.mkdir(exist_ok=True)
    lines = []
    lines.append("# Archipelago Cross-Model - FINDINGS\n")
    lines.append("Auto-generated by analyze.py. See PROTOCOL.md for pre-registered hypotheses and criteria.\n")
    lines.append(f"Cells analyzed: {len(summaries)}\n")

    lines.append("\n## Per-cell summary\n")
    df = pd.DataFrame([{
        "cell": s["cell_id"],
        "task": s["task"],
        "cond": s["condition"],
        "run": s["run_idx"],
        "n_constr": s["n_constructs"],
        "disagreement": round(s["mean_pairwise_disagreement"], 3),
        "PC1+PC2": round(s["pca_pc1_plus_pc2"], 3),
        "high_corr_pairs": s["n_high_corr_pairs"],
        "cost_$": round(s["cost_usd"], 3),
        "errs": len(s["errors"]),
    } for s in summaries])
    lines.append("```\n" + df.to_string(index=False) + "\n```\n")
    df.to_csv(ANALYSIS_DIR / "per_cell_summary.csv", index=False)

    lines.append("\n## Hypothesis evaluations (pre-registered)\n")
    lines.append("### H1 (construct content distinctness)\n")
    h1f = evals.get("H1_failures", [])
    if h1f:
        lines.append(f"- Cells where cluster count at k=6 is <4 (H1 fails): {h1f}\n")
    else:
        lines.append("- No cells fail H1 falsification criterion (all have ≥4 distinct clusters at k=6).\n")

    lines.append("\n### H2 (operator-useful map)\n")
    h2f = evals.get("H2_failures", [])
    if h2f:
        lines.append(f"- Cells where PC1+PC2 < 60% (H2 fails): {h2f}\n")
    else:
        lines.append("- No cells fail H2 falsification criterion (all have PC1+PC2 ≥ 60%).\n")

    lines.append("\n### H3 (premature convergence detection)\n")
    lines.append(f"- Overall mean inter-agent disagreement: {evals.get('H3_overall_mean_disagreement', 'n/a'):.3f}\n")
    lines.append(f"- Range across cells: {evals.get('H3_min_disagreement', 'n/a'):.3f} to {evals.get('H3_max_disagreement', 'n/a'):.3f}\n")
    lines.append(f"- Status: **{evals.get('H3_status', 'unknown')}**\n")

    lines.append("\n## Pilot vs cross-model (headline comparison)\n")
    for task in ["A", "B"]:
        key = f"task_{task}"
        if key in evals:
            e = evals[key]
            lines.append(f"### Task {task}\n")
            lines.append(f"- Pilot disagreement (Claude-only, role-played): {e['pilot_disagreement']:.3f}\n")
            lines.append(f"- Cross-model disagreement: {e['cross_model_disagreement']:.3f}\n")
            lines.append(f"- Delta: {e['delta']:+.3f}\n")
            lines.append(f"- Predicted range: {e['predicted_range']}\n")
            lines.append(f"- Result: **{e['headline_test']}**\n")

    lines.append("\n## Condition effect (Neutral vs Persona)\n")
    for metric, data in cond_comp.items():
        if isinstance(data, dict):
            lines.append(f"- **{metric}**: neutral={data['neutral_mean']:.3f}, persona={data['persona_mean']:.3f}, "
                         f"delta={data['delta_persona_minus_neutral']:+.3f}")
            if "p_value" in data:
                lines.append(f" (paired t-test p={data['p_value']:.3f})")
            lines.append("\n")

    lines.append("\n## Run-to-run variance (Task B repeats)\n")
    for key, data in rep_var.items():
        lines.append(f"- {key}: mean={data['mean']:.3f}, sd={data['sd']:.3f}, CV={data['coef_var']:.2%}, n={data['n_runs']}\n")

    lines.append("\n## Cost summary\n")
    total_cost = sum(s["cost_usd"] for s in summaries)
    lines.append(f"- Total API spend: ${total_cost:.2f}\n")
    lines.append(f"- Cells with errors: {sum(1 for s in summaries if s['errors'])}\n")

    lines.append("\n## Next steps\n")
    lines.append("1. Send this file and `per_cell_summary.csv` to Claude for joint interpretation.\n")
    lines.append("2. Inspect `analysis/<cell_id>/biplot.png` for any cell whose pattern looks unusual.\n")
    lines.append("3. If H1 or H2 failed: investigate which models drove the failure - is it a parsing issue or a real result?\n")
    lines.append("4. If results align with pilot direction (cross-model > Claude-only on diversity), proceed to paper revision.\n")

    out = ANALYSIS_DIR / "FINDINGS.md"
    out.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


def write_pilot_comparison(summaries: list[dict], evals: dict) -> None:
    lines = ["# Pilot vs Cross-Model comparison\n"]
    lines.append("\nPilot reference values (Claude Opus 4.7, role-played 5 ways):\n")
    for t, v in PILOT_REFERENCE.items():
        lines.append(f"- Task {t}: disagreement={v['mean_pairwise_disagreement']}, "
                     f"PC1+PC2={v['pc1_pc2_variance']}\n")
    lines.append("\nCross-model results:\n")
    for s in summaries:
        if s["task"] in ["A", "B"]:
            lines.append(f"- {s['cell_id']}: disagreement={s['mean_pairwise_disagreement']:.3f}, "
                         f"PC1+PC2={s['pca_pc1_plus_pc2']:.3f}\n")
    lines.append("\nKey question: does cross-model raise the disagreement signal above 0.5 (pilot threshold for premature convergence)?\n")
    out = ANALYSIS_DIR / "comparison_vs_pilot.md"
    out.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


# ============================================================
# Main
# ============================================================
def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--cell", default=None)
    args = p.parse_args()

    ANALYSIS_DIR.mkdir(exist_ok=True)
    cells = load_all_cells()
    if not cells:
        print(f"No completed cells found in {RESULTS_DIR}")
        return 1
    if args.cell:
        if args.cell not in cells:
            print(f"Cell {args.cell} not found or not complete")
            return 1
        cells = {args.cell: cells[args.cell]}
    summaries = []
    for cid, cell in sorted(cells.items()):
        print(f"Analyzing {cid}...")
        s = analyze_cell(cid, cell)
        summaries.append(s)
        if s.get("status") == "no_data":
            print(f"  no_data (cell had no ratings to analyze)")
            continue
        d = s.get("mean_pairwise_disagreement", float("nan"))
        p = s.get("pca_pc1_plus_pc2", float("nan"))
        try:
            print(f"  disagreement={d:.3f}, PC1+PC2={p:.3f}")
        except (ValueError, TypeError):
            print(f"  disagreement={d}, PC1+PC2={p}")
    # Filter no_data summaries before downstream aggregation that assumes metrics exist
    valid_summaries = [s for s in summaries if s.get("status") != "no_data"]
    skipped = [s["cell_id"] for s in summaries if s.get("status") == "no_data"]
    if skipped:
        print(f"Skipping {len(skipped)} no-data cells from aggregates: {skipped}")
    if not valid_summaries:
        print("ERROR: no cells with usable data; cannot produce findings.")
        print("Check results/state.json - cells likely failed phase 3 (constructs) or phase 4 (ratings).")
        return 1
    evals = hypothesis_evaluation(valid_summaries)
    cond_comp = condition_comparison(valid_summaries)
    rep_var = repeat_variance(valid_summaries)
    write_findings(valid_summaries, evals, cond_comp, rep_var)
    write_pilot_comparison(valid_summaries, evals)
    # Save full summary JSON (including the no-data cells for audit)
    with open(ANALYSIS_DIR / "all_summaries.json", "w", encoding="utf-8") as f:
        json.dump({
            "summaries": summaries,
            "skipped_no_data": skipped,
            "evaluations": evals,
            "condition_comparison": cond_comp,
            "repeat_variance": rep_var,
        }, f, indent=2, default=str)
    print(f"Analysis complete: {len(valid_summaries)} cells analyzed, {len(skipped)} skipped. See analysis/FINDINGS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
