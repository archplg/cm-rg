#!/usr/bin/env python3
"""
combined_analysis.py - Wave 4 финальный аналитический модуль.

Объединяет все валидные фазы эксперимента в одну матрицу model × construct,
прогоняет PCA с bootstrap-CI, Procrustes-сравнение между фазами и проверяет
устойчивость ключевых findings на максимально доступном объёме данных.

Сканируемые фазы (results_*/):
  - pilot               42 cells, 5 моделей, 7 задач    (Phase 1 + 2B + ранние)
  - extended            20 cells, 5 моделей, 2 задачи   (Phase 2C / 2G multi-run)
  - phase2h             12 cells, 10 моделей, 2 задачи
  - phase2h_extended    10 cells, 10 моделей, 5 задач
  - phase2j             14 cells, 11 моделей, 7 задач  (с Opus 4.8)

ИГНОРИРУЕТСЯ:
  - results_minitest    1 cell (test only)
  - results_phase2f     30 cells (failed - corrupted write)

Выход в analysis_combined/:
  REPORT.md         финальный отчёт
  coords.csv        PCA-координаты 11 моделей (combined)
  metrics.json      все числа для повторного использования
  map.png           карта моделей с bootstrap CI-эллипсами
  per_phase.csv    PCA-координаты по каждой фазе отдельно (для Procrustes)

Запуск:
  python combined_analysis.py
"""
from __future__ import annotations
import json
import os
import sys
import csv
import warnings
from pathlib import Path
from collections import defaultdict

import numpy as np

warnings.filterwarnings("ignore", category=RuntimeWarning)

OUT_DIR = Path("analysis_combined")
PHASES = {
    "pilot":             Path("results_pilot"),
    "extended":          Path("results_extended"),
    "phase2h":           Path("results_phase2h"),
    "phase2h_extended":  Path("results_phase2h_extended"),
    "phase2j":           Path("results_phase2j"),
}

# Canonical model ordering & labels (11 моделей с Opus 4.8 как M11)
MODEL_LABELS = {
    "M1":  "Claude Opus 4.7",      "M2":  "GPT-5.5",
    "M3":  "Gemini 3.1 Pro",       "M4":  "DeepSeek v4 Pro",
    "M5":  "Kimi k2.6",            "M6":  "Mistral Large 2512",
    "M7":  "Cohere Command A",     "M8":  "Qwen 3.7 Max",
    "M9":  "Llama 4 Maverick",     "M10": "Grok 4.20",
    "M11": "Claude Opus 4.8",
}
LAB_COUNTRY = {
    "M1":  ("Anthropic", "US"),    "M2":  ("OpenAI", "US"),
    "M3":  ("Google", "US"),       "M4":  ("DeepSeek", "CN"),
    "M5":  ("Moonshot", "CN"),     "M6":  ("Mistral", "FR"),
    "M7":  ("Cohere", "CA"),       "M8":  ("Alibaba", "CN"),
    "M9":  ("Meta", "US"),         "M10": ("xAI", "US"),
    "M11": ("Anthropic", "US"),
}
FAMILY_COLOR = {
    "Anthropic": "#D97757", "OpenAI": "#10A37F", "Google": "#4285F4",
    "DeepSeek":  "#6F42C1", "Moonshot": "#FF8C42", "Mistral":  "#FFC857",
    "Cohere":    "#B22222", "Alibaba":  "#2A9D8F", "Meta":     "#2C3E50",
    "xAI":       "#1A1A1A",
}
ALL_MODELS = sorted(MODEL_LABELS.keys(), key=lambda m: int(m[1:]))


# ============================================================
# Data loading
# ============================================================
def load_phase(name: str, path: Path) -> list[dict]:
    """Load all cells from a results folder, attach phase tag."""
    cells = []
    if not path.exists():
        print(f"  WARN: {path} not found, skipping {name}")
        return cells
    for cell_dir in sorted(path.iterdir()):
        if not cell_dir.is_dir(): continue
        cj = cell_dir / "cell.json"
        if not cj.exists(): continue
        try:
            data = json.loads(cj.read_text(encoding='utf-8'))
            data['_phase'] = name
            data['_phase_path'] = str(cell_dir)
            cells.append(data)
        except Exception as e:
            print(f"  WARN: skip {cell_dir.name} in {name}: {e}")
    return cells


def load_all() -> dict[str, list[dict]]:
    print("[1/8] Loading cells from all phases ...")
    out = {}
    total = 0
    for name, path in PHASES.items():
        cells = load_phase(name, path)
        out[name] = cells
        total += len(cells)
        print(f"      {name}: {len(cells)} cells")
    print(f"      TOTAL: {total} cells across {len(out)} phases")
    return out


# ============================================================
# Rating matrix builder (model × construct)
# ============================================================
def build_matrix(cells: list[dict], models: list[str]) -> tuple[np.ndarray, list[tuple]]:
    """Return (rating_matrix, construct_keys).

    rating_matrix shape: (len(models), n_constructs)
    Each (model, construct) cell is the mean rating that this model
    gave on this construct across all elements it rated.
    NaN if model didn't rate that construct.

    Constructs are globally unique by (phase + cell_id + construct_id).
    """
    construct_keys = []
    for cell in cells:
        phase = cell.get('_phase', '?')
        cell_id = cell.get('cell_id', '?')
        for owner_model, items in cell.get('constructs', {}).items():
            for item in items:
                cid = item.get('id')
                left = item.get('left', '').strip()
                right = item.get('right', '').strip()
                if cid and left and right:
                    construct_keys.append((phase, cell_id, cid))

    n = len(models)
    k = len(construct_keys)
    if k == 0:
        return np.empty((n, 0)), []

    X = np.full((n, k), np.nan)

    # Speedup: index cells by (phase, cell_id)
    cell_lookup = {(c['_phase'], c['cell_id']): c for c in cells}

    for ci, (phase, cell_id, c_id) in enumerate(construct_keys):
        cell = cell_lookup.get((phase, cell_id))
        if not cell: continue
        ratings = cell.get('ratings', {})
        for mi, m in enumerate(models):
            rats = ratings.get(m, {}).get(c_id, {})
            if isinstance(rats, dict) and rats:
                vals = [v for v in rats.values() if isinstance(v, (int, float))]
                if vals:
                    X[mi, ci] = float(np.mean(vals))
    return X, construct_keys


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
        print("ERROR: sklearn not installed. pip install scikit-learn --break-system-packages", file=sys.stderr)
        sys.exit(1)
    Xc = X - X.mean(axis=0, keepdims=True)
    pca = PCA(n_components=min(n_components, min(Xc.shape) - 1))
    coords = pca.fit_transform(Xc)
    return coords, pca.explained_variance_ratio_, pca


# ============================================================
# Bootstrap CI for PCA positions
# ============================================================
def bootstrap_pca(cells: list[dict], models: list[str],
                  n_iterations: int = 200,
                  seed: int = 42) -> dict[str, dict]:
    """For each model, return 95% CI on PC1 and PC2 across bootstrap samples.

    Procedure:
      - Resample cells with replacement (n_cells samples each iteration)
      - Build rating matrix from sample, impute, PCA
      - Procrustes-align coords to reference run (to remove rotation/reflection)
      - Collect (PC1, PC2) for each model across iterations
      - Return mean and 95% CI (2.5%, 97.5% percentiles)
    """
    print(f"[5/8] Bootstrap PCA ({n_iterations} iterations) ...")
    try:
        from scipy.spatial import procrustes
    except ImportError:
        print("ERROR: scipy not installed", file=sys.stderr)
        sys.exit(1)

    rng = np.random.default_rng(seed)
    # Reference PCA on full data
    X_ref, _ = build_matrix(cells, models)
    X_ref = impute_nans(X_ref)
    coords_ref, _, _ = fit_pca(X_ref, n_components=2)

    boot_coords = {m: [] for m in models}
    for it in range(n_iterations):
        # Sample with replacement
        sample = list(rng.choice(cells, size=len(cells), replace=True))
        X, _ = build_matrix(sample, models)
        if X.shape[1] < 3:
            continue
        X = impute_nans(X)
        try:
            coords, _, _ = fit_pca(X, n_components=2)
        except Exception:
            continue
        # Procrustes alignment to reference
        try:
            _, aligned, _ = procrustes(coords_ref, coords)
            # procrustes also rescales - undo by using R from manual alignment
            # We'll just use the aligned coords for stability of comparison
            for mi, m in enumerate(models):
                boot_coords[m].append((float(aligned[mi, 0]), float(aligned[mi, 1])))
        except Exception:
            continue

    summary = {}
    for m, pts in boot_coords.items():
        if not pts:
            summary[m] = {"n_samples": 0}
            continue
        arr = np.array(pts)
        summary[m] = {
            "n_samples": len(pts),
            "PC1_mean": float(arr[:, 0].mean()),
            "PC1_sd":   float(arr[:, 0].std(ddof=1)),
            "PC1_ci_lo": float(np.percentile(arr[:, 0], 2.5)),
            "PC1_ci_hi": float(np.percentile(arr[:, 0], 97.5)),
            "PC2_mean": float(arr[:, 1].mean()),
            "PC2_sd":   float(arr[:, 1].std(ddof=1)),
            "PC2_ci_lo": float(np.percentile(arr[:, 1], 2.5)),
            "PC2_ci_hi": float(np.percentile(arr[:, 1], 97.5)),
        }
    return summary


# ============================================================
# Per-phase PCA (for Procrustes between phases)
# ============================================================
def per_phase_pca(by_phase: dict[str, list[dict]], models: list[str]) -> dict[str, dict]:
    print("[3/8] Per-phase PCA (for Procrustes comparison) ...")
    out = {}
    for name, cells in by_phase.items():
        if not cells: continue
        # Skip phases where these models don't appear
        present_models = set()
        for c in cells:
            for m in c.get('ratings', {}):
                present_models.add(m)
        if not present_models & set(models):
            out[name] = None
            continue
        # Only build matrix for models that have data in this phase
        phase_models = [m for m in models if m in present_models]
        X, _ = build_matrix(cells, phase_models)
        if X.shape[1] < 3:
            out[name] = None
            continue
        X = impute_nans(X)
        coords, evr, _ = fit_pca(X, n_components=min(2, len(phase_models)-1))
        out[name] = {
            "models": phase_models,
            "coords": {m: (float(coords[i, 0]), float(coords[i, 1] if coords.shape[1] > 1 else 0))
                       for i, m in enumerate(phase_models)},
            "evr": [float(v) for v in evr.tolist()],
            "n_cells": len(cells),
            "n_constructs": X.shape[1],
        }
        print(f"      {name}: {len(phase_models)} models, {X.shape[1]} constructs, PC1+PC2={evr[0]+evr[1] if len(evr) > 1 else evr[0]:.3f}")
    return out


def procrustes_pairwise(per_phase: dict) -> dict[tuple[str, str], float]:
    print("[4/8] Procrustes pairwise comparison between phases ...")
    try:
        from scipy.spatial import procrustes
    except ImportError:
        return {}
    out = {}
    phases = [p for p in per_phase if per_phase[p] is not None]
    for i, a in enumerate(phases):
        for b in phases[i+1:]:
            ma = per_phase[a]["models"]
            mb = per_phase[b]["models"]
            common = [m for m in ma if m in mb]
            if len(common) < 3:
                out[(a, b)] = None
                continue
            A = np.array([per_phase[a]["coords"][m] for m in common])
            B = np.array([per_phase[b]["coords"][m] for m in common])
            try:
                _, _, disparity = procrustes(A, B)
                out[(a, b)] = float(disparity)
                print(f"      {a:20s} ↔ {b:20s}: Procrustes disparity = {disparity:.4f} (n={len(common)} common models)")
            except Exception as e:
                print(f"      {a} ↔ {b}: ERROR {e}")
                out[(a, b)] = None
    return out


# ============================================================
# Cohere outlier robustness across phases
# ============================================================
def cohere_outlier_robustness(per_phase: dict, full_coords: dict) -> dict:
    print("[6/8] Cohere outlier robustness across phases ...")
    out = {"per_phase_pc1": {}, "verdict": ""}
    for phase, info in per_phase.items():
        if info is None: continue
        if "M7" in info["coords"]:
            pc1 = info["coords"]["M7"][0]
            other_pc1s = [c[0] for m, c in info["coords"].items() if m != "M7"]
            mean_others = float(np.mean(other_pc1s)) if other_pc1s else 0
            offset = pc1 - mean_others
            out["per_phase_pc1"][phase] = {
                "M7_PC1": pc1,
                "others_mean_PC1": mean_others,
                "offset": offset,
            }
            print(f"      {phase:20s}: M7 PC1={pc1:+.3f}, others mean PC1={mean_others:+.3f}, offset={offset:+.3f}")
    # Combined PCA
    combined_offset = full_coords["M7"][0] - np.mean([full_coords[m][0] for m in full_coords if m != "M7"])
    out["combined_offset"] = float(combined_offset)
    n_offset_positive = sum(1 for v in out["per_phase_pc1"].values() if v["offset"] > 5)
    out["verdict"] = (
        f"Cohere PC1 offset > 5 единиц на {n_offset_positive}/{len(out['per_phase_pc1'])} phases "
        f"and {combined_offset:+.2f} in combined analysis."
    )
    return out


# ============================================================
# Mean rating per model (calibration drift summary)
# ============================================================
def mean_ratings_per_model(by_phase: dict[str, list[dict]], models: list[str]) -> dict:
    print("[7/8] Mean ratings per model per phase (calibration audit) ...")
    out = {}
    for m in models:
        per_phase_means = {}
        all_ratings = []
        for phase, cells in by_phase.items():
            phase_ratings = []
            for cell in cells:
                rmap = cell.get('ratings', {}).get(m, {})
                for cid, ele_map in rmap.items():
                    if isinstance(ele_map, dict):
                        for v in ele_map.values():
                            if isinstance(v, (int, float)) and 1 <= v <= 7:
                                phase_ratings.append(v)
                                all_ratings.append(v)
            if phase_ratings:
                per_phase_means[phase] = {
                    "n": len(phase_ratings),
                    "mean": float(np.mean(phase_ratings)),
                    "sd": float(np.std(phase_ratings, ddof=1)),
                    "p7_rate": float(np.mean(np.array(phase_ratings) == 7)) * 100,
                }
        if all_ratings:
            out[m] = {
                "phases": per_phase_means,
                "overall_n": len(all_ratings),
                "overall_mean": float(np.mean(all_ratings)),
                "overall_sd": float(np.std(all_ratings, ddof=1)),
                "overall_p7_rate": float(np.mean(np.array(all_ratings) == 7)) * 100,
            }
    return out


# ============================================================
# Report generation
# ============================================================
def write_report(out_dir: Path, summary: dict):
    out_path = out_dir / "REPORT.md"
    s = summary
    lines = []
    lines.append("# Combined Analysis - финальный отчёт по всем фазам CM-RG")
    lines.append("")
    lines.append(f"**Объём данных:** {s['n_cells_total']} cells, {s['n_constructs']} конструктов, {s['n_phases']} фаз, до 11 моделей.")
    lines.append("")
    lines.append("## Состав данных")
    lines.append("")
    lines.append("| Фаза | Cells | Models | Constructs | Tasks |")
    lines.append("|---|---|---|---|---|")
    for name, info in s["phases"].items():
        if info is None:
            lines.append(f"| {name} | (skipped/empty) | - | - | - |")
        else:
            lines.append(f"| {name} | {info['n_cells']} | {len(info['models'])} | {info['n_constructs']} | (см metrics.json) |")
    lines.append("")

    lines.append("## Combined PCA (все ячейки, все 11 моделей)")
    lines.append("")
    lines.append(f"PC1+PC2 cumulative explained variance: **{100*(s['combined_evr'][0] + s['combined_evr'][1]):.1f}%**")
    lines.append("")
    lines.append("| Model | Lab | PC1 mean | PC1 95% CI | PC2 mean | PC2 95% CI |")
    lines.append("|---|---|---|---|---|---|")
    for m in ALL_MODELS:
        c = s["combined_coords"].get(m)
        b = s["bootstrap"].get(m, {})
        if c is None or "PC1_mean" not in b: continue
        lab, _ = LAB_COUNTRY[m]
        lines.append(
            f"| {m} {MODEL_LABELS[m]} | {lab} | "
            f"{b['PC1_mean']:+.3f} | [{b['PC1_ci_lo']:+.3f}, {b['PC1_ci_hi']:+.3f}] | "
            f"{b['PC2_mean']:+.3f} | [{b['PC2_ci_lo']:+.3f}, {b['PC2_ci_hi']:+.3f}] |"
        )
    lines.append("")

    lines.append("## Procrustes-сравнение между фазами")
    lines.append("")
    lines.append("Procrustes disparity 0 = идентичные карты, → 1 = полностью разные. Низкие значения = структура устойчива.")
    lines.append("")
    lines.append("| Phase A | Phase B | Disparity |")
    lines.append("|---|---|---|")
    for pair_key, d in s["procrustes_pairwise"].items():
        if "__" in pair_key:
            a, b = pair_key.split("__", 1)
        else:
            a, b = pair_key, "?"
        if d is None:
            lines.append(f"| {a} | {b} | n/a (< 3 общих моделей) |")
        else:
            lines.append(f"| {a} | {b} | {d:.4f} |")
    lines.append("")

    lines.append("## Cohere outlier - устойчивость через фазы")
    lines.append("")
    lines.append("| Phase | M7 PC1 | Others mean PC1 | Offset |")
    lines.append("|---|---|---|---|")
    for phase, info in s["cohere"]["per_phase_pc1"].items():
        lines.append(f"| {phase} | {info['M7_PC1']:+.3f} | {info['others_mean_PC1']:+.3f} | **{info['offset']:+.3f}** |")
    lines.append(f"| **combined** | - | - | **{s['cohere']['combined_offset']:+.3f}** |")
    lines.append("")
    lines.append(f"**Вердикт:** {s['cohere']['verdict']}")
    lines.append("")

    lines.append("## Calibration drift summary - средние оценки по моделям")
    lines.append("")
    lines.append("| Model | Overall mean | Overall %7 | n |")
    lines.append("|---|---|---|---|")
    for m in ALL_MODELS:
        if m not in s["mean_ratings"]: continue
        info = s["mean_ratings"][m]
        lines.append(
            f"| {m} {MODEL_LABELS[m]} | {info['overall_mean']:.3f} | {info['overall_p7_rate']:.1f}% | {info['overall_n']:,} |"
        )
    lines.append("")

    lines.append("## Ключевые числа для arxiv preprint")
    lines.append("")
    lines.append(f"- **Total cells analysed:** {s['n_cells_total']}")
    lines.append(f"- **Total constructs:** {s['n_constructs']}")
    lines.append(f"- **Total ratings collected:** {s['n_ratings_total']:,}")
    lines.append(f"- **Models compared:** 11 (включая обе версии Opus 4.7 и 4.8)")
    lines.append(f"- **Tasks across domains:** 7 (HR, governance, ethics, engineering, product launch, medical triage, AI policy)")
    lines.append(f"- **Cohere PC1 offset (combined):** {s['cohere']['combined_offset']:+.2f} units")
    lines.append(f"- **Max Procrustes disparity between phases:** {s['procrustes_max']:.4f}")
    lines.append(f"- **Min Procrustes disparity between phases:** {s['procrustes_min']:.4f}")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding='utf-8')
    print(f"      Report saved -> {out_path}")


# ============================================================
# Plot
# ============================================================
def plot_combined(out_dir: Path, coords: dict, bootstrap: dict, evr: list[float]):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Ellipse
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(11, 8))
    for m in ALL_MODELS:
        c = coords.get(m)
        b = bootstrap.get(m, {})
        if c is None: continue
        lab, _ = LAB_COUNTRY[m]
        col = FAMILY_COLOR.get(lab, "#888")
        x, y = c
        # 95% CI ellipse from bootstrap percentiles
        if "PC1_ci_lo" in b:
            w = b["PC1_ci_hi"] - b["PC1_ci_lo"]
            h = b["PC2_ci_hi"] - b["PC2_ci_lo"]
            xc = (b["PC1_ci_hi"] + b["PC1_ci_lo"]) / 2
            yc = (b["PC2_ci_hi"] + b["PC2_ci_lo"]) / 2
            ell = Ellipse((xc, yc), w, h, fc=col, ec=col, alpha=0.18, zorder=2)
            ax.add_patch(ell)
        marker = "*" if m == "M11" else "o"
        size = 320 if m == "M11" else 200
        ax.scatter(x, y, s=size, color=col, edgecolor="white", linewidth=2, marker=marker, zorder=4)
        ax.annotate(m, (x, y), xytext=(10, 6), textcoords="offset points", fontsize=11, fontweight="bold")
    ax.axhline(0, color="grey", linewidth=0.5, alpha=0.5)
    ax.axvline(0, color="grey", linewidth=0.5, alpha=0.5)
    ax.set_xlabel(f"PC1 ({100*evr[0]:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({100*evr[1]:.1f}% variance)")
    ax.set_title("Combined PCA - all phases, 11 models\nShaded ellipse = 95% bootstrap CI")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = out_dir / "map.png"
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"      Map saved -> {path}")


# ============================================================
# Main
# ============================================================
def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)
    by_phase = load_all()
    all_cells = [c for cells in by_phase.values() for c in cells]
    if not all_cells:
        print("ERROR: no cells loaded", file=sys.stderr)
        return 1

    print(f"[2/8] Build combined rating matrix (11 models × all constructs) ...")
    X, construct_keys = build_matrix(all_cells, ALL_MODELS)
    print(f"      Matrix: {X.shape[0]} models × {X.shape[1]} constructs")
    coverage = np.sum(~np.isnan(X), axis=1)
    print(f"      Coverage per model:")
    for mi, m in enumerate(ALL_MODELS):
        pct = 100 * coverage[mi] / X.shape[1]
        print(f"        {m} {MODEL_LABELS[m]:<22}: {int(coverage[mi]):>5}/{X.shape[1]} ({pct:.0f}%)")
    X = impute_nans(X)
    coords_arr, evr, _ = fit_pca(X, n_components=5)
    combined_coords = {m: (float(coords_arr[i, 0]), float(coords_arr[i, 1]))
                       for i, m in enumerate(ALL_MODELS)}
    print(f"      PCA variance: PC1={100*evr[0]:.1f}%, PC2={100*evr[1]:.1f}%, "
          f"PC1+PC2={100*(evr[0]+evr[1]):.1f}%")

    per_phase = per_phase_pca(by_phase, ALL_MODELS)
    procrustes_pw = procrustes_pairwise(per_phase)
    valid_proc = [d for d in procrustes_pw.values() if d is not None]
    procrustes_max = max(valid_proc) if valid_proc else 0
    procrustes_min = min(valid_proc) if valid_proc else 0

    bootstrap = bootstrap_pca(all_cells, ALL_MODELS, n_iterations=200)

    cohere = cohere_outlier_robustness(per_phase, combined_coords)
    mean_ratings = mean_ratings_per_model(by_phase, ALL_MODELS)
    n_ratings_total = sum(info.get("overall_n", 0) for info in mean_ratings.values())

    print("[8/8] Writing outputs ...")
    # CSV
    with open(OUT_DIR / "coords.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["model", "label", "lab", "country", "PC1", "PC2",
                    "PC1_ci_lo", "PC1_ci_hi", "PC2_ci_lo", "PC2_ci_hi"])
        for mi, m in enumerate(ALL_MODELS):
            lab, country = LAB_COUNTRY[m]
            b = bootstrap.get(m, {})
            row = [m, MODEL_LABELS[m], lab, country,
                   f"{coords_arr[mi, 0]:.4f}", f"{coords_arr[mi, 1]:.4f}",
                   f"{b.get('PC1_ci_lo', 0):.4f}", f"{b.get('PC1_ci_hi', 0):.4f}",
                   f"{b.get('PC2_ci_lo', 0):.4f}", f"{b.get('PC2_ci_hi', 0):.4f}"]
            w.writerow(row)
    print(f"      Coords -> {OUT_DIR/'coords.csv'}")

    # Metrics JSON
    metrics = {
        "n_cells_total": len(all_cells),
        "n_constructs": X.shape[1],
        "n_phases": len(by_phase),
        "n_ratings_total": n_ratings_total,
        "phases": {name: ({"n_cells": info["n_cells"], "n_constructs": info["n_constructs"], "models": info["models"]} if info else None) for name, info in per_phase.items()},
        "combined_coords": combined_coords,
        "combined_evr": [float(v) for v in evr.tolist()],
        "bootstrap": bootstrap,
        "procrustes_pairwise": {f"{a}__{b}": d for (a, b), d in procrustes_pw.items()},
        "procrustes_max": procrustes_max,
        "procrustes_min": procrustes_min,
        "cohere": cohere,
        "mean_ratings": mean_ratings,
    }
    with open(OUT_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(f"      Metrics -> {OUT_DIR/'metrics.json'}")

    write_report(OUT_DIR, metrics)
    plot_combined(OUT_DIR, combined_coords, bootstrap, evr)

    print(f"\nDone. Open {OUT_DIR/'REPORT.md'} to read findings.")
    print(f"      Total cells: {len(all_cells)}, constructs: {X.shape[1]}, ratings: {n_ratings_total:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
 constructs: {X.shape[1]}, ratings: {n_ratings_total:,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
