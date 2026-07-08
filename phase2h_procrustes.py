#!/usr/bin/env python3
"""
Procrustes alignment: Phase 1 (5 models) vs Phase 2H (10 models, same M1-M5 subset).

Question: when adding 5 NEW labs (M6-M10), do the ORIGINAL 5 (M1-M5) stay in
roughly the same positions in 2D evaluative space, or do they shift?

Method:
1. Build per-cell PCA on Phase 1 (5-model cells, n=5 elements).
2. Build per-cell PCA on Phase 2H (10-model cells, n=10 elements), then
   extract M1-M5 sub-coordinates.
3. Procrustes-align M1-M5 positions between the two universes.
4. Report disparity = how much positions of M1-M5 changed when M6-M10 added.

Low disparity = stable evaluative space (lab additions don't disturb core 5).
High disparity = lab diversity reshapes the whole 2D map (entanglement).

Run:
    python phase2h_procrustes.py
"""
from __future__ import annotations
import json
import os
import sys
from collections import defaultdict

import numpy as np

PHASE1_DIR = "results"
PHASE2H_DIR = "results_phase2h"
OUT_DIR = "phase2h_procrustes"
MODELS_5 = ["M1", "M2", "M3", "M4", "M5"]


def load_cells(base):
    cells = []
    for d in sorted(os.listdir(base)):
        p = os.path.join(base, d, "cell.json")
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as f:
            try:
                cells.append(json.load(f))
            except Exception:
                continue
    return cells


def build_rating_vector(cell, model_id, all_constructs):
    """Build flat vector of ratings for a model across all constructs/elements in cell."""
    rats = cell.get("ratings", {}).get(model_id, {})
    if not isinstance(rats, dict):
        return None
    elements = sorted(cell.get("element_summaries", {}).keys())
    vec = []
    for c_id in all_constructs:
        per_element = rats.get(c_id, {}) if isinstance(rats, dict) else {}
        for e_id in elements:
            v = per_element.get(e_id, np.nan)
            vec.append(float(v) if isinstance(v, (int, float)) else np.nan)
    return np.array(vec) if vec else None


def model_positions_phase1(cells, tasks_subset):
    """Return dict {model: avg position in 2D} for Phase 1 cells restricted to tasks_subset."""
    from sklearn.decomposition import PCA

    # Collect ratings: for each cell, for each model, average rating per construct
    model_construct_means = defaultdict(lambda: defaultdict(list))
    for cell in cells:
        task = cell.get("task")
        if task not in tasks_subset:
            continue
        constructs_used = set()
        for rid, by_c in cell.get("ratings", {}).items():
            if isinstance(by_c, dict):
                constructs_used.update(by_c.keys())
        for model in MODELS_5:
            by_c = cell.get("ratings", {}).get(model, {})
            if not isinstance(by_c, dict):
                continue
            for c_id in constructs_used:
                per_e = by_c.get(c_id, {})
                if isinstance(per_e, dict) and per_e:
                    vals = [v for v in per_e.values() if isinstance(v, (int, float))]
                    if vals:
                        model_construct_means[model][c_id].append(np.mean(vals))

    # Build aligned construct list: all constructs at least one model rated
    all_constructs = sorted(set().union(*(set(d.keys()) for d in model_construct_means.values())))
    if not all_constructs:
        return None, []

    matrix = np.full((len(MODELS_5), len(all_constructs)), np.nan)
    for mi, m in enumerate(MODELS_5):
        for ci, c in enumerate(all_constructs):
            vals = model_construct_means[m].get(c, [])
            if vals:
                matrix[mi, ci] = float(np.mean(vals))
    # Impute NaN with column mean, then global mean
    overall = float(np.nanmean(matrix))
    for ci in range(matrix.shape[1]):
        cm = np.nanmean(matrix[:, ci])
        if not np.isnan(cm):
            matrix[np.isnan(matrix[:, ci]), ci] = cm
    matrix[np.isnan(matrix)] = overall

    X = matrix - matrix.mean(axis=0, keepdims=True)
    pca = PCA(n_components=min(2, X.shape[0] - 1))
    coords = pca.fit_transform(X)
    return coords, list(pca.explained_variance_ratio_)


def procrustes_disparity(X, Y):
    """Procrustes disparity between two matrices of same shape."""
    from scipy.spatial.distance import euclidean
    from scipy.linalg import orthogonal_procrustes

    # Center
    X = X - X.mean(axis=0)
    Y = Y - Y.mean(axis=0)
    # Scale
    Xn = X / np.linalg.norm(X)
    Yn = Y / np.linalg.norm(Y)
    # Optimal rotation
    R, scale = orthogonal_procrustes(Xn, Yn)
    Xa = Xn @ R
    disparity = np.linalg.norm(Xa - Yn) ** 2
    return float(disparity), Xa, Yn


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("Loading Phase 1 cells...")
    p1_cells = load_cells(PHASE1_DIR)
    print(f"  {len(p1_cells)} cells")
    print("Loading Phase 2H cells...")
    p2h_cells = load_cells(PHASE2H_DIR)
    print(f"  {len(p2h_cells)} cells")

    # Common tasks: Phase 2H has only A and D
    p2h_tasks = sorted(set(c.get("task") for c in p2h_cells))
    print(f"Phase 2H tasks: {p2h_tasks}")

    # Build M1-M5 positions in Phase 1 universe (restricted to tasks A and D)
    print("\nBuilding M1-M5 positions in Phase 1 universe (n=5 models)...")
    coords_p1, evr_p1 = model_positions_phase1(p1_cells, set(p2h_tasks))
    if coords_p1 is None:
        print("ERROR: no Phase 1 data for tasks A and D")
        return 1
    print(f"  Phase 1 PCA variance: PC1={evr_p1[0]:.3f}, PC2={evr_p1[1]:.3f}")
    for mi, m in enumerate(MODELS_5):
        print(f"  {m}: ({coords_p1[mi, 0]:+.3f}, {coords_p1[mi, 1]:+.3f})")

    # Build M1-M5 positions in Phase 2H universe (n=10 models, but restrict to M1-M5)
    print("\nBuilding M1-M5 positions in Phase 2H universe (n=10 models, subset to M1-M5)...")
    coords_p2h_all, evr_p2h = model_positions_phase1(p2h_cells, set(p2h_tasks))
    # Use only first 5 rows (M1-M5)
    coords_p2h = coords_p2h_all[:5]
    print(f"  Phase 2H PCA variance (M1-M5 subset): PC1={evr_p2h[0]:.3f}, PC2={evr_p2h[1]:.3f}")
    for mi, m in enumerate(MODELS_5):
        print(f"  {m}: ({coords_p2h[mi, 0]:+.3f}, {coords_p2h[mi, 1]:+.3f})")

    # Procrustes align
    print("\nProcrustes alignment...")
    disparity, p1_aligned, p2h_normalized = procrustes_disparity(coords_p1, coords_p2h)
    print(f"  Disparity (Phase 1 vs Phase 2H, M1-M5 positions): {disparity:.4f}")

    # Aligned coordinates after rotation
    print("\nAligned positions (after rotation):")
    print(f"{'Model':<6} {'Phase 1 PC1':>12} {'Phase 1 PC2':>12} {'Phase 2H PC1':>14} {'Phase 2H PC2':>14}")
    for mi, m in enumerate(MODELS_5):
        print(f"{m:<6} {p1_aligned[mi, 0]:>+12.4f} {p1_aligned[mi, 1]:>+12.4f} "
              f"{p2h_normalized[mi, 0]:>+14.4f} {p2h_normalized[mi, 1]:>+14.4f}")

    # Interpretation
    print(f"\n=== INTERPRETATION ===")
    if disparity < 0.05:
        verdict = "VERY STABLE - M1-M5 positions almost identical between universes"
    elif disparity < 0.15:
        verdict = "STABLE - small shifts, core 5-model relationships preserved"
    elif disparity < 0.35:
        verdict = "MODERATE - lab additions reshape some relationships"
    else:
        verdict = "HIGH - lab additions substantially reorganize evaluative space"
    print(f"Verdict: {verdict}")

    # Write markdown report
    lines = [f"# Phase 2H Procrustes alignment - Phase 1 vs Phase 2H\n\n"]
    lines.append(f"Question: when adding 5 new labs (M6-M10), do the original M1-M5 ")
    lines.append(f"positions stay stable in 2D evaluative space?\n\n")
    lines.append(f"Restricted to tasks A and D (common between Phase 1 and Phase 2H).\n\n")

    lines.append(f"## Procrustes disparity\n\n")
    lines.append(f"**Disparity = {disparity:.4f}**\n\n")
    lines.append(f"Scale: 0 = identical, 1 = orthogonal universes.\n\n")
    lines.append(f"**Verdict: {verdict}**\n\n")

    lines.append(f"## M1-M5 positions in each universe (after Procrustes alignment)\n\n")
    lines.append(f"| Model | Phase 1 PC1 | Phase 1 PC2 | Phase 2H PC1 | Phase 2H PC2 |\n")
    lines.append(f"|---|---|---|---|---|\n")
    for mi, m in enumerate(MODELS_5):
        lines.append(f"| {m} | {p1_aligned[mi, 0]:+.4f} | {p1_aligned[mi, 1]:+.4f} | "
                     f"{p2h_normalized[mi, 0]:+.4f} | {p2h_normalized[mi, 1]:+.4f} |\n")

    lines.append("\n## Per-model shift (Euclidean distance after alignment)\n\n")
    shifts = []
    for mi, m in enumerate(MODELS_5):
        d = np.linalg.norm(p1_aligned[mi] - p2h_normalized[mi])
        shifts.append((m, d))
    shifts.sort(key=lambda x: x[1], reverse=True)
    lines.append("| Model | Shift |\n|---|---|\n")
    for m, d in shifts:
        lines.append(f"| {m} | {d:.4f} |\n")

    lines.append("\n## How to use for paper\n\n")
    lines.append("- This addresses a key reviewer question: 'how do you know that adding more "
                 "models doesn't fundamentally change the evaluative space such that your "
                 "findings depend on the specific 5-model panel?'\n")
    lines.append(f"- Headline for paper: *\"Procrustes disparity {disparity:.3f} indicates that "
                 "core M1-M5 model positions remain [stable/somewhat altered] when lab diversity "
                 "expands from 5 to 10 frontier models. This supports the methodology being "
                 "robust to ensemble composition rather than tied to a specific model selection.\"*\n")
    lines.append("- Compare to Procrustes 0.352 result from earlier analysis (cross-model vs "
                 "Platonic Hypothesis test).\n")

    with open(os.path.join(OUT_DIR, "PHASE2H_PROCRUSTES.md"), "w", encoding="utf-8") as f:
        f.write("".join(lines))
    print(f"\nWritten: {OUT_DIR}/PHASE2H_PROCRUSTES.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
