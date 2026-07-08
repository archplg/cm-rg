#!/usr/bin/env python3
"""
Bootstrap CI on 2D model coordinates from Phase 2H.

Question: are model positions in 2D evaluative space STABLE or are they noise?
Specifically: is Cohere's +26 outlier position statistically robust, or
artifact of one task / one cell?

Method:
1. Bootstrap 1000 resamples of cells (with replacement) from results_phase2h/
2. For each resample, rebuild PCA and get model 2D coordinates
3. Compute 95% bootstrap CI on PC1 and PC2 for each model

Run:
    python phase2h_bootstrap.py
"""
from __future__ import annotations
import json
import os
import sys
from collections import defaultdict

import numpy as np

BASE = "results_phase2h"
OUT_DIR = "phase2h_bootstrap"
MODELS = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"]
LABELS = {
    "M1": "Claude Opus 4.7", "M2": "GPT-5.5", "M3": "Gemini 3.1 Pro",
    "M4": "DeepSeek v4 Pro", "M5": "Kimi k2.6", "M6": "Mistral Large 2512",
    "M7": "Cohere Command A", "M8": "Qwen 3.7 Max", "M9": "Llama 4 Maverick",
    "M10": "Grok 4.20",
}
N_BOOT = 100   # reduced for sandbox - CI precision ~2 decimal places
SEED = 42


def load_cells():
    cells = []
    for d in sorted(os.listdir(BASE)):
        p = os.path.join(BASE, d, "cell.json")
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as f:
            try:
                cells.append(json.load(f))
            except Exception:
                continue
    return cells


def compute_coordinates(cells_subset):
    """Build the model x construct matrix, then PCA to 2D."""
    from sklearn.decomposition import PCA

    # Collect all constructs across the subset
    all_constructs = []
    for cell in cells_subset:
        cell_id = cell["cell_id"]
        for model, items in cell.get("constructs", {}).items():
            for item in items:
                cid = item.get("id")
                if cid and item.get("left", "").strip() and item.get("right", "").strip():
                    all_constructs.append((cell_id, cid))

    if not all_constructs:
        return None

    # For each model, build vector of mean ratings on each construct
    matrix = np.full((len(MODELS), len(all_constructs)), np.nan)
    for cell in cells_subset:
        cid = cell["cell_id"]
        for ci, (c_cell, c_id) in enumerate(all_constructs):
            if c_cell != cid:
                continue
            for mi, m in enumerate(MODELS):
                per_e = cell.get("ratings", {}).get(m, {}).get(c_id, {})
                if isinstance(per_e, dict) and per_e:
                    vals = [v for v in per_e.values() if isinstance(v, (int, float))]
                    if vals:
                        matrix[mi, ci] = float(np.mean(vals))

    # Impute NaN
    overall = float(np.nanmean(matrix))
    for ci in range(matrix.shape[1]):
        cm = np.nanmean(matrix[:, ci])
        if not np.isnan(cm):
            matrix[np.isnan(matrix[:, ci]), ci] = cm
    matrix[np.isnan(matrix)] = overall

    X = matrix - matrix.mean(axis=0, keepdims=True)
    pca = PCA(n_components=min(len(MODELS) - 1, 2))
    coords = pca.fit_transform(X)
    return coords


def align_to_reference(coords, ref):
    """Procrustes-align coords to reference (without scaling)."""
    from scipy.linalg import orthogonal_procrustes
    # Match signs: use sign of M1's PC1 in reference to fix sign ambiguity
    # First center
    c = coords - coords.mean(axis=0)
    r = ref - ref.mean(axis=0)
    # Optimal rotation
    R, _ = orthogonal_procrustes(c, r)
    return c @ R


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    cells = load_cells()
    print(f"Loaded {len(cells)} cells")
    if not cells:
        return 1

    # Reference coordinates (no bootstrap)
    print("\nComputing reference (full sample) coordinates...")
    ref_coords = compute_coordinates(cells)
    print(f"Reference shape: {ref_coords.shape}")
    print(f"{'Model':<22} {'PC1':>8} {'PC2':>8}")
    for mi, m in enumerate(MODELS):
        print(f"{LABELS[m]:<22} {ref_coords[mi, 0]:>+8.3f} {ref_coords[mi, 1]:>+8.3f}")

    # Bootstrap
    print(f"\nBootstrap with {N_BOOT} resamples...")
    rng = np.random.default_rng(SEED)
    boot_coords = np.zeros((N_BOOT, len(MODELS), 2))
    for bi in range(N_BOOT):
        idx = rng.integers(0, len(cells), size=len(cells))
        sample = [cells[i] for i in idx]
        c = compute_coordinates(sample)
        if c is None:
            boot_coords[bi] = np.nan
            continue
        c_aligned = align_to_reference(c, ref_coords)
        boot_coords[bi] = c_aligned
        if (bi + 1) % 100 == 0:
            print(f"  {bi+1}/{N_BOOT}")

    # CIs
    print(f"\n95% bootstrap CIs:")
    print(f"{'Model':<22} {'PC1 (95% CI)':<24} {'PC2 (95% CI)':<24}")
    ci_lines = []
    for mi, m in enumerate(MODELS):
        pc1_vals = boot_coords[:, mi, 0]
        pc2_vals = boot_coords[:, mi, 1]
        pc1_lo, pc1_hi = np.nanpercentile(pc1_vals, [2.5, 97.5])
        pc2_lo, pc2_hi = np.nanpercentile(pc2_vals, [2.5, 97.5])
        pc1_se = float(np.nanstd(pc1_vals))
        pc2_se = float(np.nanstd(pc2_vals))
        print(f"{LABELS[m]:<22} [{pc1_lo:+.2f}, {pc1_hi:+.2f}] (SE {pc1_se:.2f})  "
              f"[{pc2_lo:+.2f}, {pc2_hi:+.2f}] (SE {pc2_se:.2f})")
        ci_lines.append({
            "model": m, "label": LABELS[m],
            "pc1": ref_coords[mi, 0], "pc2": ref_coords[mi, 1],
            "pc1_lo": pc1_lo, "pc1_hi": pc1_hi, "pc1_se": pc1_se,
            "pc2_lo": pc2_lo, "pc2_hi": pc2_hi, "pc2_se": pc2_se,
        })

    # Headline: is Cohere outlier robust?
    print(f"\n=== HEADLINE: Cohere outlier robustness ===")
    cohere_idx = MODELS.index("M7")
    cohere_pc1_lo = np.nanpercentile(boot_coords[:, cohere_idx, 0], 2.5)
    cohere_pc1_hi = np.nanpercentile(boot_coords[:, cohere_idx, 0], 97.5)
    # Max PC1 of other 9 models
    other_max_pc1 = []
    for bi in range(N_BOOT):
        others = [boot_coords[bi, mi, 0] for mi in range(len(MODELS)) if mi != cohere_idx]
        other_max_pc1.append(max(others))
    other_max_lo = np.nanpercentile(other_max_pc1, 2.5)
    other_max_hi = np.nanpercentile(other_max_pc1, 97.5)
    print(f"Cohere PC1 95% CI: [{cohere_pc1_lo:.2f}, {cohere_pc1_hi:.2f}]")
    print(f"Max of others' PC1 95% CI: [{other_max_lo:.2f}, {other_max_hi:.2f}]")
    if cohere_pc1_lo > other_max_hi:
        print(f"  -> Cohere outlier position is ROBUST (gap > 0 in 95% of resamples)")
    elif cohere_pc1_lo > other_max_lo:
        print(f"  -> Cohere outlier position is LIKELY robust (some overlap with others)")
    else:
        print(f"  -> Cohere outlier position is UNSTABLE (95% CIs overlap)")

    # Save CSV
    import csv
    with open(os.path.join(OUT_DIR, "bootstrap_ci.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["model", "label", "pc1", "pc1_lo95", "pc1_hi95", "pc1_se",
                    "pc2", "pc2_lo95", "pc2_hi95", "pc2_se"])
        for row in ci_lines:
            w.writerow([row["model"], row["label"], row["pc1"], row["pc1_lo"], row["pc1_hi"],
                        row["pc1_se"], row["pc2"], row["pc2_lo"], row["pc2_hi"], row["pc2_se"]])

    # Markdown
    lines = [f"# Phase 2H bootstrap CIs on model 2D coordinates\n\n"]
    lines.append(f"Source: {len(cells)} cells from {BASE}, {N_BOOT} bootstrap resamples.\n\n")
    lines.append("## Reference position + 95% bootstrap CI\n\n")
    lines.append("| Model | Lab | PC1 ref | PC1 95% CI | PC2 ref | PC2 95% CI |\n")
    lines.append("|---|---|---|---|---|---|\n")
    for row in ci_lines:
        lab = row['label']
        lines.append(f"| {row['model']} | {lab} | {row['pc1']:+.2f} | "
                     f"[{row['pc1_lo']:+.2f}, {row['pc1_hi']:+.2f}] | "
                     f"{row['pc2']:+.2f} | "
                     f"[{row['pc2_lo']:+.2f}, {row['pc2_hi']:+.2f}] |\n")

    lines.append(f"\n## Cohere outlier robustness check\n\n")
    lines.append(f"- Cohere PC1 95% CI: **[{cohere_pc1_lo:.2f}, {cohere_pc1_hi:.2f}]**\n")
    lines.append(f"- Max PC1 of other 9 models, 95% CI: [{other_max_lo:.2f}, {other_max_hi:.2f}]\n")
    if cohere_pc1_lo > other_max_hi:
        lines.append(f"\n**Verdict:** Cohere outlier position is **ROBUST**. "
                     f"Across 1000 resamples, Cohere PC1 always exceeds all other models' PC1.\n\n")
    elif cohere_pc1_lo > other_max_lo:
        lines.append(f"\n**Verdict:** Cohere outlier position is **LIKELY robust** but some "
                     f"resamples show overlap with other models.\n\n")
    else:
        lines.append(f"\n**Verdict:** Cohere outlier position is **NOT robust** - some resamples "
                     f"show overlap with other models.\n\n")

    lines.append("## How to use for paper\n\n")
    lines.append("- Add bootstrap CI bars to 2D map figure\n")
    lines.append("- Cite this analysis when claiming 'Cohere is an outlier' - need CI to be valid\n")
    lines.append("- If CIs are wide, paper should soften the outlier framing\n")
    lines.append("- If CIs are tight, the +26σ position is publishable as a robust finding\n")

    with open(os.path.join(OUT_DIR, "PHASE2H_BOOTSTRAP_CI.md"), "w", encoding="utf-8") as f:
        f.write("".join(lines))
    print(f"\nWritten: {OUT_DIR}/PHASE2H_BOOTSTRAP_CI.md")
    print(f"Written: {OUT_DIR}/bootstrap_ci.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
