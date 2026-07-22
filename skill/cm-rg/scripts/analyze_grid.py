#!/usr/bin/env python3
"""CM-RG analysis: agreement, calibration, element PCA map, construct profile.

Usage:
    python analyze_grid.py grid.json outdir/

Input : grid.json (schema in SKILL.md)
Output: outdir/metrics.json
        outdir/agreement_heatmap.png
        outdir/element_map.png
        outdir/report_stub.md

Dependencies: numpy, matplotlib.
"""
import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Palette (validated defaults; swap for your brand's - see dataviz references)
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
CATEGORICAL = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7", "#e87ba4", "#eda100"]
DIVERGING = LinearSegmentedColormap.from_list(
    "cmrg_div", ["#b03a39", "#f0efec", "#0d366b"])

MIN_SHARED_CELLS = 8


def load_grid(path):
    grid = json.loads(Path(path).read_text(encoding="utf-8"))
    elements = [e["id"] for e in grid["elements"]]
    models = {e["id"]: e.get("model", e["id"]) for e in grid["elements"]}
    constructs = grid["constructs"]
    tensors = {}
    for entry in grid["ratings"]:
        m = np.array([[np.nan if v is None else float(v) for v in row]
                      for row in entry["matrix"]], dtype=float)
        if m.shape != (len(elements), len(constructs)):
            print(f"ERROR: rater {entry['rater']} matrix shape {m.shape} != "
                  f"({len(elements)}, {len(constructs)})", file=sys.stderr)
            sys.exit(1)
        tensors[entry["rater"]] = m
    return grid, elements, models, constructs, tensors


def pairwise_agreement(tensors):
    raters = list(tensors)
    pairs, skipped = {}, []
    for a, b in combinations(raters, 2):
        va, vb = tensors[a].ravel(), tensors[b].ravel()
        mask = ~np.isnan(va) & ~np.isnan(vb)
        if mask.sum() < MIN_SHARED_CELLS:
            skipped.append({"pair": [a, b], "reason": f"only {int(mask.sum())} shared cells"})
            continue
        xa, xb = va[mask], vb[mask]
        if xa.std() == 0 or xb.std() == 0:
            skipped.append({"pair": [a, b], "reason": "constant ratings"})
            continue
        pairs[(a, b)] = float(np.corrcoef(xa, xb)[0, 1])
    return raters, pairs, skipped


def element_pca(tensors, elements):
    stack = np.stack(list(tensors.values()))           # raters x elem x constr
    mean_matrix = np.nanmean(stack, axis=0)            # elem x constr
    col_ok = ~np.isnan(mean_matrix).any(axis=0)        # drop constructs with gaps
    X = mean_matrix[:, col_ok]
    Xc = X - X.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    var = S**2
    share = var / var.sum() if var.sum() > 0 else var
    scores = U * S                                     # elements in PC space
    return mean_matrix, col_ok, scores, Vt, share


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("grid")
    ap.add_argument("outdir")
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    grid, elements, models, constructs, tensors = load_grid(args.grid)
    raters, pairs, skipped = pairwise_agreement(tensors)

    # --- agreement ---
    r_values = list(pairs.values())
    mean_r = float(np.mean(r_values)) if r_values else None
    median_r = float(np.median(r_values)) if r_values else None

    # --- calibration ---
    calibration = {r: float(np.nanmean(t)) for r, t in tensors.items()}
    group_mean = float(np.mean(list(calibration.values())))

    # --- per-element disagreement ---
    stack = np.stack(list(tensors.values()))
    disagreement = {}
    for i, el in enumerate(elements):
        diffs = []
        for a, b in combinations(range(stack.shape[0]), 2):
            d = np.abs(stack[a, i, :] - stack[b, i, :])
            d = d[~np.isnan(d)]
            if d.size:
                diffs.append(float(d.mean()))
        disagreement[el] = float(np.mean(diffs)) if diffs else None

    # --- constructs profile ---
    per_rater_counts = {}
    for c in constructs:
        src = c.get("source_model", "unknown")
        per_rater_counts[src] = per_rater_counts.get(src, 0) + 1
    keys = [f"{c['pole_a'].strip().lower()}|{c['pole_b'].strip().lower()}" for c in constructs]
    dup_rate = 1.0 - len(set(keys)) / len(keys) if keys else 0.0

    # --- PCA ---
    mean_matrix, col_ok, scores, Vt, share = element_pca(tensors, elements)
    kept = [c for c, ok in zip(constructs, col_ok) if ok]
    top_loadings = {}
    for pc in range(min(2, Vt.shape[0])):
        idx = np.argsort(-np.abs(Vt[pc]))[:5]
        top_loadings[f"PC{pc+1}"] = [
            {"construct": f"{kept[j]['pole_a']} vs {kept[j]['pole_b']}",
             "loading": round(float(Vt[pc, j]), 3)} for j in idx]

    n_ratings = int(np.sum(~np.isnan(stack)))
    n_null = int(np.sum(np.isnan(stack)))
    metrics = {
        "meta": grid.get("meta", {}),
        "n_models": len(raters),
        "n_elements": len(elements),
        "n_constructs": len(constructs),
        "n_ratings": n_ratings,
        "n_null_cells": n_null,
        "mean_pairwise_r": None if mean_r is None else round(mean_r, 3),
        "median_pairwise_r": None if median_r is None else round(median_r, 3),
        "pairwise_r": {f"{a} x {b}": round(v, 3) for (a, b), v in pairs.items()},
        "skipped_pairs": skipped,
        "calibration_mean_rating": {k: round(v, 3) for k, v in calibration.items()},
        "calibration_group_mean": round(group_mean, 3),
        "disagreement_per_element": {
            k: (None if v is None else round(v, 3)) for k, v in disagreement.items()},
        "constructs_per_rater": per_rater_counts,
        "construct_exact_duplicate_rate": round(dup_rate, 3),
        "pca_variance_share": [round(float(s), 3) for s in share[:3]],
        "pca_top_loadings": top_loadings,
    }
    (outdir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    # --- figure 1: agreement heatmap ---
    n = len(raters)
    M = np.full((n, n), np.nan)
    for (a, b), v in pairs.items():
        ia, ib = raters.index(a), raters.index(b)
        M[ia, ib] = M[ib, ia] = v
    fig, ax = plt.subplots(figsize=(6.4, 5.4), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    im = ax.imshow(M, cmap=DIVERGING, vmin=-1, vmax=1)
    short = [models.get(r, r).replace("claude-", "") for r in raters]
    ax.set_xticks(range(n), short, color=INK_2, fontsize=9)
    ax.set_yticks(range(n), short, color=INK_2, fontsize=9)
    for i in range(n):
        for j in range(n):
            if i == j:
                ax.text(j, i, "-", ha="center", va="center", color=MUTED, fontsize=10)
            elif not np.isnan(M[i, j]):
                lum_dark = abs(M[i, j]) > 0.55
                ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                        color="#ffffff" if lum_dark else INK, fontsize=10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("Inter-rater agreement (Pearson r)", color=INK, fontsize=12, pad=12)
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(color=MUTED, labelcolor=INK_2, labelsize=8)
    fig.tight_layout()
    fig.savefig(outdir / "agreement_heatmap.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)

    # --- figure 2: element map ---
    fig, ax = plt.subplots(figsize=(6.8, 5.4), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    for i, el in enumerate(elements):
        color = CATEGORICAL[i % len(CATEGORICAL)]
        x, y = scores[i, 0], (scores[i, 1] if scores.shape[1] > 1 else 0.0)
        ax.scatter(x, y, s=140, color=color, zorder=3,
                   edgecolors=SURFACE, linewidths=2)
        ax.annotate(f"{el} · {models.get(el, '')}", (x, y),
                    textcoords="offset points", xytext=(10, 6),
                    color=INK, fontsize=10)
    ax.axhline(0, color=GRID, lw=1, zorder=1)
    ax.axvline(0, color=GRID, lw=1, zorder=1)
    ax.grid(color=GRID, lw=0.6, alpha=0.6, zorder=0)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8)
    p1 = share[0] * 100 if len(share) > 0 else 0
    p2 = share[1] * 100 if len(share) > 1 else 0
    ax.set_xlabel(f"PC1 ({p1:.0f}% variance)", color=INK_2, fontsize=10)
    ax.set_ylabel(f"PC2 ({p2:.0f}% variance)", color=INK_2, fontsize=10)
    ax.set_title("Element map - how the group construes the responses",
                 color=INK, fontsize=12, pad=12)
    fig.tight_layout()
    fig.savefig(outdir / "element_map.png", dpi=200, facecolor=SURFACE)
    plt.close(fig)

    # --- report stub ---
    stub = [
        "# CM-RG mini-grid report (stub - fill narrative sections)",
        "",
        f"Models: {', '.join(models[e] for e in elements)}",
        f"Constructs: {len(constructs)} | Ratings: {n_ratings} | Null cells: {n_null}",
        f"Mean pairwise r: {metrics['mean_pairwise_r']}",
        f"Calibration: {metrics['calibration_mean_rating']}",
        f"Most contested element: "
        f"{max((k for k, v in disagreement.items() if v is not None), key=lambda k: disagreement[k], default='n/a')}",
        "",
        "![agreement](agreement_heatmap.png)",
        "![map](element_map.png)",
    ]
    (outdir / "report_stub.md").write_text("\n".join(stub), encoding="utf-8")

    print(json.dumps({k: metrics[k] for k in
                      ["n_models", "n_constructs", "n_ratings",
                       "mean_pairwise_r", "pca_variance_share"]}, indent=2))
    print(f"\nWritten: metrics.json, agreement_heatmap.png, element_map.png, "
          f"report_stub.md -> {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
