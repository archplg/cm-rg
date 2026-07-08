#!/usr/bin/env python3
"""
Phase 2H 2D map: project 10 frontier LLMs into PC1-PC2 evaluative space.

For each cell, computes mean rating per (model, construct) pair, then
aggregates across cells and tasks. PCA on the (model, mean_rating_vector)
matrix yields a 2D coordinate for each model. The result is a publishable
figure showing how the 10 models sit relative to each other in evaluative
space - which models cluster, which are outliers, which axes separate them.

Run:
    python phase2h_2d_map.py
"""
from __future__ import annotations
import json
import os
import sys
from collections import defaultdict

import numpy as np

BASE = "results_phase2h"
OUT_DIR = "phase2h_2d_map"
MODEL_LABELS = {
    "M1": "Claude Opus 4.7 (Anthropic)",
    "M2": "GPT-5.5 (OpenAI)",
    "M3": "Gemini 3.1 Pro (Google)",
    "M4": "DeepSeek v4 Pro",
    "M5": "Kimi k2.6 (Moonshot)",
    "M6": "Mistral Large 2512",
    "M7": "Command A (Cohere)",
    "M8": "Qwen 3.7 Max (Alibaba)",
    "M9": "Llama 4 Maverick (Meta)",
    "M10": "Grok 4.20 (xAI)",
}
LAB_COUNTRY = {
    "M1": ("Anthropic", "US"), "M2": ("OpenAI", "US"),
    "M3": ("Google", "US"), "M4": ("DeepSeek", "CN"),
    "M5": ("Moonshot", "CN"), "M6": ("Mistral", "FR"),
    "M7": ("Cohere", "CA"), "M8": ("Alibaba", "CN"),
    "M9": ("Meta", "US"), "M10": ("xAI", "US"),
}


def load_cells():
    cells = []
    for cell_dir in sorted(os.listdir(BASE)):
        p = os.path.join(BASE, cell_dir, "cell.json")
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as f:
            cells.append(json.load(f))
    return cells


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    cells = load_cells()
    print(f"Loaded {len(cells)} cells from {BASE}")

    # Build a master construct list across all cells
    all_constructs = []
    construct_owner = {}  # construct_id -> (cell_id, model_who_made_it)
    for cell in cells:
        for model, items in cell.get("constructs", {}).items():
            for item in items:
                cid = item.get("id")
                if cid and item.get("left", "").strip() and item.get("right", "").strip():
                    all_constructs.append((cell["cell_id"], cid))
                    construct_owner[(cell["cell_id"], cid)] = model

    print(f"Total constructs: {len(all_constructs)}")
    if not all_constructs:
        print("No constructs found")
        return 1

    # For each model, build a vector of mean ratings across (cell, construct, element)
    # Vector dimension = len(all_constructs) * 10 (max elements)
    # But we'll use per-construct means averaged across elements
    # That gives one number per construct per rater model

    models = sorted(MODEL_LABELS.keys(), key=lambda m: int(m[1:]))
    n_constructs = len(all_constructs)
    rating_matrix = np.full((len(models), n_constructs), np.nan)

    for cell in cells:
        cell_id = cell["cell_id"]
        for ci, (c_cell, c_id) in enumerate(all_constructs):
            if c_cell != cell_id:
                continue
            for mi, model in enumerate(models):
                rats = cell.get("ratings", {}).get(model, {}).get(c_id, {})
                if isinstance(rats, dict) and rats:
                    vals = [v for v in rats.values() if isinstance(v, (int, float))]
                    if vals:
                        rating_matrix[mi, ci] = float(np.mean(vals))

    # Diagnostic
    coverage = np.sum(~np.isnan(rating_matrix), axis=1)
    print(f"\nRating coverage per model:")
    for mi, m in enumerate(models):
        print(f"  {m} {MODEL_LABELS[m]:<30}: {coverage[mi]}/{n_constructs} ({100*coverage[mi]/n_constructs:.0f}%)")

    # Fill NaN with column (construct) mean
    col_means = np.nanmean(rating_matrix, axis=0)
    inds = np.where(np.isnan(rating_matrix))
    rating_matrix[inds] = np.take(col_means, inds[1])
    if np.isnan(rating_matrix).any():
        print(f"WARNING: {np.isnan(rating_matrix).sum()} ratings still NaN after column-mean fill; using overall mean")
        rating_matrix[np.isnan(rating_matrix)] = float(np.nanmean(rating_matrix))

    # PCA
    from sklearn.decomposition import PCA
    X = rating_matrix - rating_matrix.mean(axis=0, keepdims=True)
    pca = PCA(n_components=min(len(models) - 1, 5))
    coords = pca.fit_transform(X)
    evr = pca.explained_variance_ratio_

    print(f"\nPCA variance explained:")
    for i, v in enumerate(evr):
        print(f"  PC{i+1}: {v:.3f}")
    print(f"  PC1+PC2 cumulative: {evr[0] + evr[1]:.3f}")

    # Save coordinates
    import csv
    with open(os.path.join(OUT_DIR, "model_coordinates.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["model", "label", "lab", "country", "PC1", "PC2", "PC3", "PC4"])
        for mi, m in enumerate(models):
            lab, country = LAB_COUNTRY[m]
            row = [m, MODEL_LABELS[m], lab, country]
            row.extend([f"{coords[mi, j]:.4f}" for j in range(min(4, coords.shape[1]))])
            w.writerow(row)

    # Print summary
    print(f"\n=== Model 2D coordinates ===")
    print(f"{'Model':<25} {'Lab':<12} {'PC1':>7} {'PC2':>7}")
    for mi, m in enumerate(models):
        lab, country = LAB_COUNTRY[m]
        print(f"{MODEL_LABELS[m]:<25} {lab:<12} {coords[mi, 0]:>7.3f} {coords[mi, 1]:>7.3f}")

    # Generate plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 8))
        # Color by country
        country_colors = {"US": "#2563eb", "CN": "#dc2626", "FR": "#0ea5e9", "CA": "#a855f7"}

        for mi, m in enumerate(models):
            lab, country = LAB_COUNTRY[m]
            x, y = coords[mi, 0], coords[mi, 1]
            ax.scatter(x, y, s=200, color=country_colors[country],
                       edgecolor="black", linewidth=1.2, zorder=3)
            ax.annotate(MODEL_LABELS[m], (x, y),
                        xytext=(10, 8), textcoords="offset points",
                        fontsize=10, fontweight="medium")

        ax.axhline(0, color="grey", linewidth=0.5, alpha=0.5)
        ax.axvline(0, color="grey", linewidth=0.5, alpha=0.5)
        ax.set_xlabel(f"PC1 ({100*evr[0]:.1f}% variance)", fontsize=11)
        ax.set_ylabel(f"PC2 ({100*evr[1]:.1f}% variance)", fontsize=11)
        ax.set_title(f"Cross-Model Repertory Grid: 10 frontier LLMs in evaluative space\n"
                     f"Phase 2H, 12 cells (Tasks A and D), {n_constructs} constructs, "
                     f"PC1+PC2 = {evr[0]+evr[1]:.1%}",
                     fontsize=11)
        ax.grid(alpha=0.3)

        # Legend for countries
        from matplotlib.patches import Patch
        legend_items = [Patch(color=c, label=f"{country}") for country, c in country_colors.items()]
        ax.legend(handles=legend_items, loc="lower right", title="Lab country")

        plt.tight_layout()
        plot_path = os.path.join(OUT_DIR, "model_2d_map.png")
        fig.savefig(plot_path, dpi=140, bbox_inches="tight")
        print(f"\nWritten: {plot_path}")

    except ImportError:
        print("matplotlib not available; skipping plot")

    # Markdown report
    lines = [f"# Phase 2H: 2D map of 10 frontier LLMs in evaluative space\n\n"]
    lines.append(f"Source: {len(cells)} cells from {BASE}, {n_constructs} unique constructs.\n\n")
    lines.append(f"## PCA decomposition\n\n")
    lines.append(f"| Component | Variance explained |\n|---|---|\n")
    for i, v in enumerate(evr):
        lines.append(f"| PC{i+1} | {v:.3f} ({100*v:.1f}%) |\n")
    lines.append(f"| **PC1+PC2** | **{evr[0]+evr[1]:.3f} ({100*(evr[0]+evr[1]):.1f}%)** |\n\n")

    lines.append(f"## Model coordinates\n\n")
    lines.append(f"| Model | Lab | Country | PC1 | PC2 |\n|---|---|---|---|---|\n")
    for mi, m in enumerate(models):
        lab, country = LAB_COUNTRY[m]
        lines.append(f"| {MODEL_LABELS[m]} | {lab} | {country} | {coords[mi, 0]:+.3f} | {coords[mi, 1]:+.3f} |\n")

    lines.append("\n## How to interpret\n\n")
    lines.append("- Models with similar (PC1, PC2) coordinates produce similar evaluative judgments\n")
    lines.append("- Distance in PC1-PC2 space measures evaluative divergence\n")
    lines.append("- Country clustering (if present) suggests lab tradition effects\n")
    lines.append("- Outlier models on PC1 or PC2 represent distinct evaluative styles\n")
    lines.append("\n## Notes\n\n")
    lines.append(f"- {coverage.min()} to {coverage.max()} constructs rated per model (median {int(np.median(coverage))})\n")
    lines.append(f"- M5 Kimi has lower coverage; this analysis used column-mean imputation for missing entries\n")
    lines.append(f"- For paper figure, consider larger n by including Phase 1 constructs as well\n")

    with open(os.path.join(OUT_DIR, "PHASE2H_2D_MAP.md"), "w", encoding="utf-8") as f:
        f.write("".join(lines))
    print(f"Written: {OUT_DIR}/PHASE2H_2D_MAP.md")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
