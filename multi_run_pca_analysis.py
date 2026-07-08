#!/usr/bin/env python3
"""
Multi-run PCA analysis: runs-as-elements at higher dimensionality.

Addresses the PCA dimensionality artifact (PC1+PC2 sums to 1.000 in small-n
within-cell PCA) by pooling free responses across runs within each (task,
condition) pair, treating each (model, run) pair as a separate element.

This gives 5 models x 5 runs = 25 elements per (task, condition) instead of 5,
so PCA can spread variance across many more components.

The headline finding: if PC1+PC2 < 1.000 at n_elements=25, the within-cell
artifact was indeed a small-n effect, not a structural property of model space.

No API calls required. Uses sentence-transformers for embeddings (falls back
to TF-IDF if not installed).

Outputs:
  multi_run_pca/MULTI_RUN_PCA_FINDINGS.md
  multi_run_pca/per_taskcondition_pca.csv
  multi_run_pca/pc_variance_plot.png (if matplotlib available)

Run:
    python multi_run_pca_analysis.py
    python multi_run_pca_analysis.py --results_dir results_pilot
    python multi_run_pca_analysis.py --results_dir results --min_runs 3
"""
from __future__ import annotations
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

# ============================================================
# Embeddings: try sentence-transformers, fall back to TF-IDF
# ============================================================
def get_embeddings(texts: list[str], verbose: bool = True) -> tuple[np.ndarray, str]:
    """Return (n_texts, dim) embedding matrix and method name."""
    if not texts:
        return np.zeros((0, 0)), "empty"
    try:
        from sentence_transformers import SentenceTransformer
        if verbose:
            print("  Using sentence-transformers (all-MiniLM-L6-v2)...")
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        emb = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return emb, "sentence-transformers"
    except ImportError:
        pass
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        if verbose:
            print("  sentence-transformers not available; falling back to TF-IDF...")
        vec = TfidfVectorizer(max_features=512, ngram_range=(1, 2))
        emb = vec.fit_transform(texts).toarray()
        return emb, "tfidf"
    except ImportError:
        print("  ERROR: neither sentence-transformers nor scikit-learn available", file=sys.stderr)
        return np.zeros((len(texts), 0)), "none"


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
    """Parse '<task>_<condition>_run<n>' -> (task, condition, run_n)."""
    parts = cell_id.split("_")
    if len(parts) < 3:
        return cell_id, "", 0
    task = parts[0]
    condition = parts[1]
    run_str = parts[2].replace("run", "")
    try:
        run_n = int(run_str)
    except ValueError:
        run_n = 0
    return task, condition, run_n


# ============================================================
# Within-cell PCA (baseline, replicates existing analysis)
# ============================================================
def within_cell_pca(cell: dict, emb_method_seed: list[str] = None) -> dict:
    """PCA on 5 elements (free responses) within a single cell."""
    responses = cell.get("free_responses", {})
    texts = [v for v in responses.values() if isinstance(v, str) and v.strip()]
    if len(texts) < 2:
        return {"cell_id": cell.get("cell_id"), "n_elements": len(texts),
                "pc1": float("nan"), "pc2": float("nan"), "pc1_pc2_sum": float("nan")}
    emb, method = get_embeddings(texts, verbose=False)
    if emb_method_seed is not None:
        emb_method_seed.append(method)
    if emb.shape[1] == 0:
        return {"cell_id": cell.get("cell_id"), "n_elements": len(texts),
                "pc1": float("nan"), "pc2": float("nan"), "pc1_pc2_sum": float("nan")}
    try:
        from sklearn.decomposition import PCA
    except ImportError:
        return {"cell_id": cell.get("cell_id"), "n_elements": len(texts),
                "pc1": float("nan"), "pc2": float("nan"), "pc1_pc2_sum": float("nan")}
    # On few elements, PCA has at most n_elements - 1 components.
    # Center and scale before PCA.
    emb_c = emb - emb.mean(axis=0, keepdims=True)
    n_comp = min(len(texts), emb.shape[1]) - 1
    if n_comp < 2:
        return {"cell_id": cell.get("cell_id"), "n_elements": len(texts),
                "pc1": float("nan"), "pc2": float("nan"), "pc1_pc2_sum": float("nan")}
    pca = PCA(n_components=n_comp)
    pca.fit(emb_c)
    evr = pca.explained_variance_ratio_
    return {
        "cell_id": cell.get("cell_id"),
        "n_elements": len(texts),
        "pc1": float(evr[0]),
        "pc2": float(evr[1]) if len(evr) > 1 else float("nan"),
        "pc1_pc2_sum": float(evr[0] + (evr[1] if len(evr) > 1 else 0.0)),
    }


# ============================================================
# Pooled (across runs) PCA - the headline analysis
# ============================================================
def pooled_pca(cells_in_group: list[dict], min_runs: int) -> dict:
    """Treat each (model, run) free response as a separate element."""
    texts = []
    labels = []
    runs_seen = set()
    for cell in cells_in_group:
        _, _, run_n = parse_cell_id(cell.get("cell_id", ""))
        runs_seen.add(run_n)
        for model_id, resp in cell.get("free_responses", {}).items():
            if isinstance(resp, str) and resp.strip():
                texts.append(resp)
                labels.append(f"{model_id}_run{run_n}")

    if len(texts) < 4:
        return {
            "n_elements": len(texts),
            "n_runs": len(runs_seen),
            "pc1": float("nan"),
            "pc2": float("nan"),
            "pc1_pc2_sum": float("nan"),
            "pc1_to_pc5_sum": float("nan"),
            "elbow_pc": -1,
        }
    if len(runs_seen) < min_runs:
        return {
            "n_elements": len(texts),
            "n_runs": len(runs_seen),
            "pc1": float("nan"),
            "pc2": float("nan"),
            "pc1_pc2_sum": float("nan"),
            "pc1_to_pc5_sum": float("nan"),
            "elbow_pc": -1,
        }

    emb, method = get_embeddings(texts, verbose=False)
    if emb.shape[1] == 0:
        return {
            "n_elements": len(texts),
            "n_runs": len(runs_seen),
            "pc1": float("nan"),
            "pc2": float("nan"),
            "pc1_pc2_sum": float("nan"),
            "pc1_to_pc5_sum": float("nan"),
            "elbow_pc": -1,
        }

    from sklearn.decomposition import PCA
    emb_c = emb - emb.mean(axis=0, keepdims=True)
    n_comp = min(len(texts) - 1, emb.shape[1], 20)
    pca = PCA(n_components=n_comp)
    pca.fit(emb_c)
    evr = pca.explained_variance_ratio_

    # Elbow heuristic: first PC where cumulative variance crosses 0.9
    cum = np.cumsum(evr)
    elbow = int(np.argmax(cum >= 0.9)) + 1 if (cum >= 0.9).any() else len(evr)

    return {
        "n_elements": len(texts),
        "n_runs": len(runs_seen),
        "pc1": float(evr[0]),
        "pc2": float(evr[1]) if len(evr) > 1 else float("nan"),
        "pc1_pc2_sum": float(evr[0] + (evr[1] if len(evr) > 1 else 0.0)),
        "pc1_to_pc5_sum": float(sum(evr[:5])),
        "elbow_pc": elbow,
        "evr_full": evr.tolist(),
    }


# ============================================================
# Main
# ============================================================
def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--results_dir", default="./results", help="Directory with completed cells")
    p.add_argument("--out", default="./multi_run_pca")
    p.add_argument("--min_runs", type=int, default=3,
                   help="Min runs required per (task, condition) for pooled PCA")
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    results_dir = Path(args.results_dir)
    print(f"Loading cells from {results_dir}...")
    cells = load_cells(results_dir)
    print(f"  {len(cells)} completed cells")

    if not cells:
        print("ERROR: no cells found", file=sys.stderr)
        return 1

    # Group cells by (task, condition)
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for cell in cells:
        task, condition, _ = parse_cell_id(cell.get("cell_id", ""))
        groups[(task, condition)].append(cell)

    print(f"  {len(groups)} (task, condition) groups")

    # Within-cell baseline (replicate existing finding)
    print("\nWithin-cell PCA (baseline, n_elements=5):")
    methods_seen = []
    within_rows = []
    for cell in cells:
        within_rows.append(within_cell_pca(cell, methods_seen))
    df_within = pd.DataFrame(within_rows)
    mean_pc1_pc2_within = df_within["pc1_pc2_sum"].dropna().mean()
    print(f"  Mean PC1+PC2 (n_elements=5): {mean_pc1_pc2_within:.3f}")
    print(f"  Min: {df_within['pc1_pc2_sum'].dropna().min():.3f}, "
          f"Max: {df_within['pc1_pc2_sum'].dropna().max():.3f}")
    if methods_seen:
        method_counts = pd.Series(methods_seen).value_counts()
        print(f"  Embedding methods used: {method_counts.to_dict()}")

    # Pooled across runs (headline analysis)
    print("\nPooled PCA across runs (n_elements up to 25):")
    pooled_rows = []
    for (task, condition), group in sorted(groups.items()):
        result = pooled_pca(group, min_runs=args.min_runs)
        result["task"] = task
        result["condition"] = condition
        pooled_rows.append(result)
        if not np.isnan(result["pc1_pc2_sum"]):
            print(f"  Task {task} cond {condition}: "
                  f"n={result['n_elements']:2d} elements ({result['n_runs']} runs), "
                  f"PC1+PC2={result['pc1_pc2_sum']:.3f}, "
                  f"PC1..5={result['pc1_to_pc5_sum']:.3f}, "
                  f"elbow@PC{result['elbow_pc']}")
        else:
            print(f"  Task {task} cond {condition}: insufficient data "
                  f"(n_runs={result['n_runs']}, min required={args.min_runs})")

    df_pooled = pd.DataFrame(pooled_rows)
    df_pooled.drop(columns=["evr_full"], errors="ignore").to_csv(
        out_dir / "per_taskcondition_pca.csv", index=False
    )

    # Headline aggregates
    valid_pooled = df_pooled.dropna(subset=["pc1_pc2_sum"])
    if len(valid_pooled):
        mean_pc1_pc2_pooled = valid_pooled["pc1_pc2_sum"].mean()
        mean_pc1_to_5 = valid_pooled["pc1_to_pc5_sum"].mean()
        mean_elbow = valid_pooled["elbow_pc"].mean()
    else:
        mean_pc1_pc2_pooled = float("nan")
        mean_pc1_to_5 = float("nan")
        mean_elbow = float("nan")

    delta = mean_pc1_pc2_within - mean_pc1_pc2_pooled

    # Markdown report
    lines = ["# Multi-run PCA analysis - Cross-Model Repertory Grid\n\n"]
    lines.append(f"Data source: `{results_dir}` ({len(cells)} cells, "
                 f"{len(groups)} task-condition groups)\n\n")
    lines.append(f"Embedding method primary: {methods_seen[0] if methods_seen else 'unknown'}\n\n")

    lines.append("## Headline comparison\n\n")
    lines.append("| Analysis | n_elements | Mean PC1+PC2 |\n")
    lines.append("|---|---|---|\n")
    lines.append(f"| Within-cell (baseline) | 5 | **{mean_pc1_pc2_within:.3f}** |\n")
    lines.append(f"| Pooled across runs | up to 25 | **{mean_pc1_pc2_pooled:.3f}** |\n")
    lines.append(f"| Absolute delta | | **{delta:+.3f}** |\n\n")

    if delta > 0.2:
        lines.append("**Interpretation:** PC1+PC2 drops substantially when pooling across runs. "
                     "This confirms the within-cell PC1+PC2 ≈ 1.000 was a **small-n artifact** of having "
                     "only 5 elements per PCA. At higher dimensionality (up to 25 elements), variance "
                     "spreads across many more components, as expected for a genuine high-dimensional "
                     "representation space.\n\n")
    elif delta > 0.05:
        lines.append("**Interpretation:** PC1+PC2 drops modestly when pooling. The within-cell "
                     "artifact is partially small-n, but a genuine 2D structure persists.\n\n")
    else:
        lines.append("**Interpretation:** PC1+PC2 remains high even at higher dimensionality. "
                     "This is a structural finding: cross-model variance genuinely compresses to "
                     "a low-dimensional subspace, not a small-n artifact. Consider this strong "
                     "evidence against the Platonic Representation Hypothesis being a high-dim phenomenon.\n\n")

    lines.append(f"\nAdditional metrics on pooled PCA:\n")
    lines.append(f"- Mean PC1 through PC5 cumulative: **{mean_pc1_to_5:.3f}**\n")
    lines.append(f"- Mean elbow component (variance >= 0.9): **PC{mean_elbow:.1f}**\n\n")

    lines.append("## Per-task-condition breakdown\n\n")
    lines.append("| Task | Cond | n_elements | n_runs | PC1+PC2 | PC1..PC5 | Elbow |\n")
    lines.append("|---|---|---|---|---|---|---|\n")
    for _, row in df_pooled.iterrows():
        if np.isnan(row["pc1_pc2_sum"]):
            lines.append(f"| {row['task']} | {row['condition']} | "
                         f"{row['n_elements']} | {row['n_runs']} | -- | -- | -- |\n")
        else:
            lines.append(f"| {row['task']} | {row['condition']} | "
                         f"{row['n_elements']} | {row['n_runs']} | "
                         f"{row['pc1_pc2_sum']:.3f} | "
                         f"{row['pc1_to_pc5_sum']:.3f} | "
                         f"PC{int(row['elbow_pc'])} |\n")

    lines.append("\n## How to use for paper writing\n\n")
    lines.append("- Report this analysis in the **Methods / Robustness checks** section as a "
                 "free alternative to the planned Phase 2H (10 models). It addresses the same "
                 "dimensionality concern using existing data.\n")
    lines.append("- The headline statement: *\"Within-cell PCA shows PC1+PC2 ≈ Xwithin, consistent "
                 "with a small-n dimensionality effect. When responses are pooled across runs within "
                 "(task, condition) pairs (up to 25 elements), PC1+PC2 drops to Xpooled.\"*\n")
    lines.append("- If Phase 2H (10-model) is also run, both analyses converge on the same conclusion "
                 "via independent paths, which is a stronger argument than either alone.\n\n")

    lines.append("## Limitations\n\n")
    lines.append("- This treats free responses across different runs as exchangeable elements. "
                 "Run-to-run variance within a single (task, condition, model) tuple may be lower "
                 "than cross-model variance, which somewhat inflates the apparent dimensionality.\n")
    lines.append("- The Phase 2H lineup expansion (10 independent labs) tests a different "
                 "construct: lab diversity, not run diversity. Both are valuable; they answer "
                 "complementary questions.\n")

    (out_dir / "MULTI_RUN_PCA_FINDINGS.md").write_text("".join(lines), encoding="utf-8")
    print(f"\nWritten: {out_dir}/MULTI_RUN_PCA_FINDINGS.md")
    print(f"Written: {out_dir}/per_taskcondition_pca.csv")

    # Optional plot
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        ax[0].hist(df_within["pc1_pc2_sum"].dropna(), bins=15, alpha=0.7, color="steelblue")
        ax[0].axvline(mean_pc1_pc2_within, color="red", linestyle="--",
                      label=f"mean={mean_pc1_pc2_within:.3f}")
        ax[0].set_xlabel("PC1+PC2 variance ratio")
        ax[0].set_ylabel("Frequency")
        ax[0].set_title(f"Within-cell PCA (n=5 elements)\n{len(df_within)} cells")
        ax[0].legend()
        ax[0].set_xlim(0, 1.05)

        if len(valid_pooled):
            ax[1].hist(valid_pooled["pc1_pc2_sum"], bins=10, alpha=0.7, color="seagreen")
            ax[1].axvline(mean_pc1_pc2_pooled, color="red", linestyle="--",
                          label=f"mean={mean_pc1_pc2_pooled:.3f}")
            ax[1].set_xlabel("PC1+PC2 variance ratio")
            ax[1].set_ylabel("Frequency")
            ax[1].set_title(f"Pooled PCA (n up to 25 elements)\n{len(valid_pooled)} groups")
            ax[1].legend()
            ax[1].set_xlim(0, 1.05)

        fig.suptitle("Cross-Model Repertory Grid: PCA dimensionality at two scales")
        fig.tight_layout()
        plot_path = out_dir / "pc_variance_plot.png"
        fig.savefig(plot_path, dpi=120)
        print(f"Written: {plot_path}")
    except ImportError:
        print("matplotlib not available; skipping plot")
    except Exception as e:
        print(f"plot error: {e}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
