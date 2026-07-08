#!/usr/bin/env python3
"""
Phase 2J analysis: where does Claude Opus 4.8 land relative to Opus 4.7?

Loads results_phase2j/ cells, projects all 11 models into PCA 2D-space,
tests two pre-registered hypotheses, and writes a markdown report.

Pre-registered hypotheses:
  H1 (cluster stability): PCA-distance between M1 (Opus 4.7) and
      M11 (Opus 4.8) on PC1 axis is < 3.0 units.
      Meaning: Opus 4.8 stays in the same neighbourhood as 4.7,
      versions of the same family cluster.
  H2 (calibration shift): absolute difference in mean rating
      |mean(M11) - mean(M1)| > 0.2 on the 7-point scale.
      Meaning: Anthropic's "more honesty" claim manifests as a
      measurable shift in the calibration of evaluations.

Compares M1 position across Phase 2H and Phase 2J to verify run-to-run
stability of the model itself (within-version drift control).

Outputs:
  analysis_phase2j/REPORT.md      - human-readable Markdown report
  analysis_phase2j/coords.csv     - PCA coordinates for all 11 models
  analysis_phase2j/metrics.json   - all numeric metrics for programmatic use
  analysis_phase2j/map.png        - matplotlib PCA scatter (if mpl installed)

Run:
  python analyze_phase2j.py
"""
from __future__ import annotations
import json
import os
import sys
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

PHASE2J_DIR = "results_phase2j"
PHASE2H_DIR = "results_phase2h"
PHASE2HEXT_DIR = "results_phase2h_extended"
OUT_DIR = "analysis_phase2j"

MODEL_LABELS = {
    "M1":  "Claude Opus 4.7",
    "M2":  "GPT-5.5",
    "M3":  "Gemini 3.1 Pro",
    "M4":  "DeepSeek v4 Pro",
    "M5":  "Kimi k2.6",
    "M6":  "Mistral Large 2512",
    "M7":  "Cohere Command A",
    "M8":  "Qwen 3.7 Max",
    "M9":  "Llama 4 Maverick",
    "M10": "Grok 4.20",
    "M11": "Claude Opus 4.8",
}
LAB_COUNTRY = {
    "M1":  ("Anthropic", "US"),  "M2":  ("OpenAI", "US"),
    "M3":  ("Google", "US"),     "M4":  ("DeepSeek", "CN"),
    "M5":  ("Moonshot", "CN"),   "M6":  ("Mistral", "FR"),
    "M7":  ("Cohere", "CA"),     "M8":  ("Alibaba", "CN"),
    "M9":  ("Meta", "US"),       "M10": ("xAI", "US"),
    "M11": ("Anthropic", "US"),
}
ALL_MODELS = sorted(MODEL_LABELS.keys(), key=lambda m: int(m[1:]))
PHASE2J_MODELS = ALL_MODELS                       # 11 models
PHASE2H_MODELS = [m for m in ALL_MODELS if m != "M11"]  # 10 models

# ============================================================
# Loaders
# ============================================================

def load_cells_from_dir(d: str) -> list[dict]:
    cells = []
    if not os.path.isdir(d):
        return cells
    for cell_dir in sorted(os.listdir(d)):
        p = os.path.join(d, cell_dir, "cell.json")
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
            cells.append(data)
        except Exception as e:
            print(f"  WARN: skip {p}: {e}", file=sys.stderr)
    return cells

# ============================================================
# Rating matrix builder
# ============================================================

def build_rating_matrix(cells: list[dict], models: list[str]) -> tuple[np.ndarray, list[tuple]]:
    """
    For each model, build a vector of mean ratings across (cell, construct).

    Returns:
      X : (len(models), n_constructs) matrix of mean ratings
      construct_keys : list of (cell_id, construct_id) tuples, length n_constructs
    """
    construct_keys = []
    for cell in cells:
        for owner_model, items in cell.get("constructs", {}).items():
            for item in items:
                cid = item.get("id")
                left = item.get("left", "").strip()
                right = item.get("right", "").strip()
                if cid and left and right:
                    construct_keys.append((cell["cell_id"], cid))

    n_models = len(models)
    n_constructs = len(construct_keys)
    if n_constructs == 0:
        return np.empty((n_models, 0)), []

    rating_matrix = np.full((n_models, n_constructs), np.nan)
    cell_by_id = {c["cell_id"]: c for c in cells}

    for ci, (cell_id, c_id) in enumerate(construct_keys):
        cell = cell_by_id.get(cell_id, {})
        ratings = cell.get("ratings", {})
        for mi, model in enumerate(models):
            rats = ratings.get(model, {}).get(c_id, {})
            if isinstance(rats, dict) and rats:
                vals = [v for v in rats.values() if isinstance(v, (int, float))]
                if vals:
                    rating_matrix[mi, ci] = float(np.mean(vals))

    return rating_matrix, construct_keys

def impute_nans(X: np.ndarray) -> np.ndarray:
    Y = X.copy()
    col_means = np.nanmean(Y, axis=0)
    inds = np.where(np.isnan(Y))
    Y[inds] = np.take(col_means, inds[1])
    if np.isnan(Y).any():
        Y[np.isnan(Y)] = float(np.nanmean(Y[~np.isnan(Y)])) if np.any(~np.isnan(Y)) else 0.0
    return Y

# ============================================================
# PCA helper
# ============================================================

def fit_pca(X: np.ndarray, n_components: int = 5):
    try:
        from sklearn.decomposition import PCA
    except ImportError:
        print("ERROR: sklearn not installed. Run: pip install scikit-learn --break-system-packages", file=sys.stderr)
        sys.exit(1)
    Xc = X - X.mean(axis=0, keepdims=True)
    pca = PCA(n_components=min(n_components, min(Xc.shape) - 1))
    coords = pca.fit_transform(Xc)
    return coords, pca.explained_variance_ratio_

# ============================================================
# Rating aggregation for calibration analysis
# ============================================================

def collect_all_ratings_per_model(cells: list[dict], models: list[str]) -> dict[str, np.ndarray]:
    """Return dict: model -> 1D numpy array of all integer ratings made by that model."""
    bucket = {m: [] for m in models}
    for cell in cells:
        for rater, rater_constructs in cell.get("ratings", {}).items():
            if rater not in bucket:
                continue
            for cid, ele_map in rater_constructs.items():
                if isinstance(ele_map, dict):
                    for ek, v in ele_map.items():
                        if isinstance(v, (int, float)) and 1 <= v <= 7:
                            bucket[rater].append(float(v))
    return {m: np.array(vs) for m, vs in bucket.items()}

# ============================================================
# Hypothesis tests
# ============================================================

def test_h1(coords_2j: np.ndarray, models_2j: list[str]) -> dict:
    """H1: PCA-distance between M1 and M11 on PC1 < 3.0 units."""
    idx_m1 = models_2j.index("M1")
    idx_m11 = models_2j.index("M11")
    pc1_m1 = float(coords_2j[idx_m1, 0])
    pc1_m11 = float(coords_2j[idx_m11, 0])
    pc2_m1 = float(coords_2j[idx_m1, 1])
    pc2_m11 = float(coords_2j[idx_m11, 1])
    pc1_dist = abs(pc1_m1 - pc1_m11)
    euclid_2d = float(np.hypot(pc1_m1 - pc1_m11, pc2_m1 - pc2_m11))
    # Also compute average pairwise distance in the cluster for comparison
    core_idx = [models_2j.index(m) for m in ["M1","M2","M3","M4","M5","M8"] if m in models_2j]
    if len(core_idx) >= 2:
        dists = []
        for i, a in enumerate(core_idx):
            for b in core_idx[i+1:]:
                dists.append(float(np.hypot(coords_2j[a,0]-coords_2j[b,0],
                                            coords_2j[a,1]-coords_2j[b,1])))
        median_core_dist = float(np.median(dists))
    else:
        median_core_dist = float("nan")
    threshold = 3.0
    return {
        "PC1_M1": pc1_m1, "PC1_M11": pc1_m11,
        "PC2_M1": pc2_m1, "PC2_M11": pc2_m11,
        "PC1_distance": pc1_dist,
        "euclidean_2d_distance": euclid_2d,
        "threshold_PC1": threshold,
        "supported": pc1_dist < threshold,
        "median_core_pairwise_dist": median_core_dist,
        "interpretation": (
            f"Opus 4.8 lands {euclid_2d:.2f} units from Opus 4.7 in 2D PCA space. "
            f"Median pairwise distance among 6 core models is {median_core_dist:.2f}. "
            f"Opus 4.8 is {'INSIDE' if euclid_2d < median_core_dist*1.5 else 'OUTSIDE'} the core cluster."
        )
    }

def test_h2(ratings_per_model: dict[str, np.ndarray]) -> dict:
    """H2: |mean(M11) - mean(M1)| > 0.2 on 7-point scale."""
    m1 = ratings_per_model.get("M1", np.array([]))
    m11 = ratings_per_model.get("M11", np.array([]))
    if len(m1) == 0 or len(m11) == 0:
        return {"supported": False, "error": "missing data for M1 or M11"}
    mean_m1 = float(m1.mean())
    mean_m11 = float(m11.mean())
    delta = mean_m11 - mean_m1
    abs_delta = abs(delta)
    threshold = 0.2

    # Welch's t-test (unequal variance)
    try:
        from scipy import stats
        t_stat, p_val = stats.ttest_ind(m11, m1, equal_var=False)
        p_val = float(p_val)
    except Exception:
        t_stat, p_val = float("nan"), float("nan")

    # 7-rating rate (the "sycophancy" measure)
    p7_m1 = float((m1 == 7).sum() / len(m1) * 100)
    p7_m11 = float((m11 == 7).sum() / len(m11) * 100)
    direction = "stricter (lower)" if delta < 0 else "more generous (higher)"
    return {
        "mean_M1": mean_m1, "mean_M11": mean_m11,
        "delta": delta, "abs_delta": abs_delta, "threshold": threshold,
        "supported": abs_delta > threshold,
        "p_value_welch": p_val,
        "p7_M1_percent": p7_m1, "p7_M11_percent": p7_m11,
        "p7_delta_pp": p7_m11 - p7_m1,
        "direction": direction,
        "interpretation": (
            f"Opus 4.8 mean rating {mean_m11:.3f} vs Opus 4.7 mean {mean_m1:.3f} (delta={delta:+.3f}). "
            f"Opus 4.8 is {direction}. P-value (Welch t-test): {p_val:.4g}."
        )
    }

# ============================================================
# Stability check: M1 position across phases
# ============================================================

def check_m1_stability(cells_2j: list[dict], cells_2h: list[dict]) -> dict:
    """Did M1 (Opus 4.7) drift in calibration between Phase 2H and Phase 2J runs?"""
    r_2j = collect_all_ratings_per_model(cells_2j, ["M1"])["M1"]
    r_2h = collect_all_ratings_per_model(cells_2h, ["M1"])["M1"]
    if len(r_2j) == 0 or len(r_2h) == 0:
        return {"available": False, "note": "Phase 2H data missing"}
    m_2j = float(r_2j.mean())
    m_2h = float(r_2h.mean())
    return {
        "available": True,
        "M1_mean_phase2H": m_2h,
        "M1_mean_phase2J": m_2j,
        "drift": m_2j - m_2h,
        "n_2H": int(len(r_2h)),
        "n_2J": int(len(r_2j)),
        "interpretation": (
            f"M1 mean: Phase 2H={m_2h:.3f} (n={len(r_2h)}) vs Phase 2J={m_2j:.3f} (n={len(r_2j)}). "
            f"Drift={m_2j - m_2h:+.3f}. "
            f"{'STABLE' if abs(m_2j - m_2h) < 0.15 else 'DRIFTED'} - threshold 0.15."
        )
    }

# ============================================================
# Markdown report writer
# ============================================================

def write_report(out_dir: str, summary: dict):
    out = Path(out_dir) / "REPORT.md"
    h1 = summary["H1"]
    h2 = summary["H2"]
    stab = summary["M1_stability"]
    coords = summary["coords"]
    evr = summary["evr"]
    n_cells_2j = summary["n_cells_2J"]
    n_constructs = summary["n_constructs"]

    lines = []
    lines.append("# Phase 2J - Analysis Report")
    lines.append("")
    lines.append(f"**Data:** {n_cells_2j} cells from Phase 2J ({n_constructs} constructs aggregated).")
    lines.append(f"**Models analyzed:** 11 (M1-M11, where M11 = Claude Opus 4.8).")
    lines.append("")
    lines.append("## H1. Cluster stability (Opus 4.7 vs 4.8)")
    lines.append("")
    lines.append(f"- M1 (Opus 4.7) at: PC1={h1['PC1_M1']:.3f}, PC2={h1['PC2_M1']:.3f}")
    lines.append(f"- M11 (Opus 4.8) at: PC1={h1['PC1_M11']:.3f}, PC2={h1['PC2_M11']:.3f}")
    lines.append(f"- PC1 distance: {h1['PC1_distance']:.3f} (threshold for H1 support: < {h1['threshold_PC1']:.1f})")
    lines.append(f"- Euclidean 2D distance: {h1['euclidean_2d_distance']:.3f}")
    lines.append(f"- Median pairwise distance in core (6 models): {h1['median_core_pairwise_dist']:.3f}")
    lines.append(f"- **H1 {'SUPPORTED' if h1['supported'] else 'NOT SUPPORTED'}**.")
    lines.append(f"- {h1['interpretation']}")
    lines.append("")

    lines.append("## H2. Calibration drift (Opus 4.7 -> 4.8)")
    lines.append("")
    if "error" in h2:
        lines.append(f"- ERROR: {h2['error']}")
    else:
        lines.append(f"- M1 (Opus 4.7) mean rating: {h2['mean_M1']:.3f}")
        lines.append(f"- M11 (Opus 4.8) mean rating: {h2['mean_M11']:.3f}")
        lines.append(f"- Delta: {h2['delta']:+.3f} (Opus 4.8 is {h2['direction']})")
        lines.append(f"- |Delta| = {h2['abs_delta']:.3f} vs threshold {h2['threshold']:.1f}")
        lines.append(f"- p-value (Welch's t-test): {h2['p_value_welch']:.4g}")
        lines.append(f"- Rate of '7 out of 7' ratings: M1 = {h2['p7_M1_percent']:.1f}%, M11 = {h2['p7_M11_percent']:.1f}% (delta {h2['p7_delta_pp']:+.1f} pp)")
        lines.append(f"- **H2 {'SUPPORTED' if h2['supported'] else 'NOT SUPPORTED'}**.")
        lines.append(f"- {h2['interpretation']}")
    lines.append("")

    lines.append("## M1 stability check (Phase 2H vs Phase 2J)")
    lines.append("")
    if stab.get("available"):
        lines.append(f"- {stab['interpretation']}")
    else:
        lines.append(f"- Phase 2H data not available for direct comparison.")
    lines.append("")

    lines.append("## All 11 model PCA coordinates")
    lines.append("")
    lines.append("| Model | Lab | PC1 | PC2 |")
    lines.append("|---|---|---|---|")
    for m in PHASE2J_MODELS:
        lab, country = LAB_COUNTRY[m]
        c = coords[m]
        marker = " (NEW)" if m == "M11" else ""
        lines.append(f"| {m} {MODEL_LABELS[m]}{marker} | {lab}, {country} | {c[0]:.3f} | {c[1]:.3f} |")
    lines.append("")

    lines.append(f"## Variance explained")
    lines.append("")
    for i, v in enumerate(evr[:4]):
        lines.append(f"- PC{i+1}: {100*v:.1f}%")
    if len(evr) >= 2:
        lines.append(f"- PC1+PC2 cumulative: {100*(evr[0]+evr[1]):.1f}%")
    lines.append("")

    lines.append("## Quick verdicts (Plain Russian)")
    lines.append("")
    verdict_h1 = (
        "Opus 4.8 живёт рядом с Opus 4.7 в кластере «ядра»."
        if h1['supported'] else
        "Opus 4.8 заметно отъехал от Opus 4.7. Это серьёзный finding - между поколениями одной модели накопилась структурная разница."
    )
    verdict_h2 = (
        "Калибровка не изменилась заметно. Заявление Anthropic про 'more honesty' либо не повторяется в нашем измерении, либо проявляется в более тонком измерении."
        if not h2.get("supported", False) else
        f"Калибровка сдвинулась на {h2.get('delta', 0):+.2f} балла. Anthropic заявление 'more honesty' частично эмпирически подтверждается."
    )
    lines.append(f"- **H1:** {verdict_h1}")
    lines.append(f"- **H2:** {verdict_h2}")
    lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Report saved -> {out}")

# ============================================================
# Plotting (optional)
# ============================================================

def plot_map(out_dir: str, coords: dict, evr: list[float]):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    family_colors = {
        "Anthropic": "#D97757", "OpenAI": "#10A37F", "Google": "#4285F4",
        "DeepSeek":  "#6F42C1", "Moonshot": "#FF8C42", "Mistral":  "#FFC857",
        "Cohere":    "#B22222", "Alibaba":  "#2A9D8F", "Meta":     "#2C3E50",
        "xAI":       "#1A1A1A",
    }
    fig, ax = plt.subplots(figsize=(10, 8))
    for m in PHASE2J_MODELS:
        lab, country = LAB_COUNTRY[m]
        x, y = coords[m]
        color = family_colors.get(lab, "#888")
        marker = "*" if m == "M11" else "o"
        size = 320 if m == "M11" else 220
        ax.scatter(x, y, s=size, color=color, edgecolor="white",
                   linewidth=2, marker=marker, zorder=4)
        ax.annotate(m, (x, y), xytext=(10, 6), textcoords="offset points",
                    fontsize=10, fontweight="bold")
    ax.axhline(0, color="grey", linewidth=0.5, alpha=0.5)
    ax.axvline(0, color="grey", linewidth=0.5, alpha=0.5)
    ax.set_xlabel(f"PC1 ({100*evr[0]:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({100*evr[1]:.1f}% variance)")
    ax.set_title("Phase 2J: 11 frontier LLMs in 2D evaluative space\n"
                 "M11 = Claude Opus 4.8 (star marker)")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = Path(out_dir) / "map.png"
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"  Map saved -> {path}")

# ============================================================
# Main
# ============================================================

def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"[1/5] Loading Phase 2J cells from {PHASE2J_DIR}/ ...")
    cells_2j = load_cells_from_dir(PHASE2J_DIR)
    print(f"      Loaded {len(cells_2j)} cells from Phase 2J.")
    if len(cells_2j) == 0:
        print("ERROR: No Phase 2J cells found. Run the experiment first.", file=sys.stderr)
        return 1

    print(f"[2/5] Loading Phase 2H/2H-extended (for M1 stability check) ...")
    cells_2h = load_cells_from_dir(PHASE2H_DIR) + load_cells_from_dir(PHASE2HEXT_DIR)
    print(f"      Loaded {len(cells_2h)} cells from prior phases.")

    print(f"[3/5] Building rating matrix for Phase 2J (11 models) ...")
    rating_matrix, construct_keys = build_rating_matrix(cells_2j, PHASE2J_MODELS)
    print(f"      Matrix shape: {rating_matrix.shape} (models x constructs).")
    if rating_matrix.shape[1] == 0:
        print("ERROR: No constructs found in Phase 2J cells.", file=sys.stderr)
        return 1
    coverage = np.sum(~np.isnan(rating_matrix), axis=1)
    print(f"      Coverage:")
    for mi, m in enumerate(PHASE2J_MODELS):
        pct = 100 * coverage[mi] / rating_matrix.shape[1]
        print(f"        {m} {MODEL_LABELS[m]:<24}: {int(coverage[mi]):>4}/{rating_matrix.shape[1]} ({pct:.0f}%)")
    X = impute_nans(rating_matrix)

    print(f"[4/5] Running PCA and hypothesis tests ...")
    coords_arr, evr = fit_pca(X, n_components=5)
    coords = {m: (float(coords_arr[i, 0]), float(coords_arr[i, 1]))
              for i, m in enumerate(PHASE2J_MODELS)}
    print(f"      PCA variance: PC1={100*evr[0]:.1f}%, PC2={100*evr[1]:.1f}%, "
          f"PC1+PC2={100*(evr[0]+evr[1]):.1f}%")

    h1 = test_h1(coords_arr, PHASE2J_MODELS)
    print(f"      H1 (cluster stability): {'SUPPORTED' if h1['supported'] else 'NOT SUPPORTED'}")
    print(f"        PC1 distance M1-M11: {h1['PC1_distance']:.3f} (threshold {h1['threshold_PC1']:.1f})")
    print(f"        Euclidean 2D distance: {h1['euclidean_2d_distance']:.3f}")

    ratings_per_model = collect_all_ratings_per_model(cells_2j, PHASE2J_MODELS)
    h2 = test_h2(ratings_per_model)
    if "error" not in h2:
        print(f"      H2 (calibration shift): {'SUPPORTED' if h2['supported'] else 'NOT SUPPORTED'}")
        print(f"        Mean delta: {h2['delta']:+.3f} ({h2['direction']})")
        print(f"        p-value: {h2['p_value_welch']:.4g}")

    stab = check_m1_stability(cells_2j, cells_2h)
    if stab.get("available"):
        print(f"      M1 stability: drift {stab['drift']:+.3f} balls between phases.")

    print(f"[5/5] Writing outputs to {OUT_DIR}/ ...")
    # Coordinates CSV
    csv_path = Path(OUT_DIR) / "coords.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["model", "label", "lab", "country", "PC1", "PC2", "PC3", "PC4"])
        for mi, m in enumerate(PHASE2J_MODELS):
            lab, country = LAB_COUNTRY[m]
            row = [m, MODEL_LABELS[m], lab, country]
            row.extend([f"{coords_arr[mi, j]:.4f}" for j in range(min(4, coords_arr.shape[1]))])
            w.writerow(row)
    print(f"  Coords CSV -> {csv_path}")

    # Metrics JSON
    metrics = {
        "n_cells_phase2J": len(cells_2j),
        "n_cells_phase2H_combined": len(cells_2h),
        "n_constructs": rating_matrix.shape[1],
        "H1": h1,
        "H2": h2,
        "M1_stability": stab,
        "evr": [float(v) for v in evr.tolist()],
        "coordinates": {m: list(coords[m]) for m in PHASE2J_MODELS},
        "ratings_count_per_model": {m: int(len(ratings_per_model[m])) for m in PHASE2J_MODELS},
    }
    json_path = Path(OUT_DIR) / "metrics.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(f"  Metrics JSON -> {json_path}")

    # Markdown report
    write_report(OUT_DIR, {
        "n_cells_2J": len(cells_2j),
        "n_constructs": rating_matrix.shape[1],
        "H1": h1, "H2": h2,
        "M1_stability": stab,
        "coords": coords,
        "evr": evr,
    })

    # Optional plot
    plot_map(OUT_DIR, coords, evr)

    print(f"\nDone. Open {OUT_DIR}/REPORT.md to read findings.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
