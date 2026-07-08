#!/usr/bin/env python3
"""
Post-hoc decomposition of all bipolar constructs elicited across cells.

7 analyses, all run locally (no API calls):
1. Semantic clustering of constructs (embedding-based taxonomy)
2. Construct ownership (model fingerprint - chi2 over clusters)
3. Persona vs Model variance decomposition (mixed-effects)
4. Procrustes alignment between models (Platonic Hypothesis test)
5. Construct -> Recommendation prediction (which axis predicts which choice)
6. Construct novelty vs known baselines (Hofstede / Schwartz / Big Five / NDM)
7. Hierarchical structure (dendrogram of all constructs)

Outputs go to construct_analysis/ with one PNG + interpretation per decomposition,
plus a master CONSTRUCT_DECOMPOSITION_FINDINGS.md.

Run:
    pip install sentence-transformers scikit-learn scipy matplotlib seaborn pandas
    python construct_decomposition.py
"""
from __future__ import annotations
import argparse
import json
import warnings
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist, squareform
from scipy.stats import chi2_contingency
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

RESULTS_DIR = Path("./results")
OPERATOR_DIR = Path("./operator_outputs")
OUT_DIR = Path("./construct_analysis")

# ============================================================
# Embedding backend
# ============================================================
class EmbeddingBackend:
    """Wraps sentence-transformers if available, falls back to TF-IDF."""

    def __init__(self):
        self.kind = None
        self.model = None
        self.tfidf = None
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.kind = "sbert"
            print("Embedding backend: sentence-transformers (384-dim)")
        except ImportError:
            print("sentence-transformers not installed; falling back to TF-IDF")
            self.kind = "tfidf"

    def encode(self, texts: list[str]) -> np.ndarray:
        if self.kind == "sbert":
            return np.asarray(self.model.encode(texts, show_progress_bar=False))
        # TF-IDF fallback
        if self.tfidf is None:
            self.tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=512)
            self.tfidf.fit(texts)
        return self.tfidf.transform(texts).toarray()


# ============================================================
# Persona id -> human-readable name
# ============================================================
PERSONA_NAMES = {
    "Q": "Quantitative", "S": "Systems", "E": "Engineering",
    "H": "Humanist", "C": "Contrarian", "neutral": "Neutral"
}


# ============================================================
# Baselines: established taxonomies for novelty test (decomp 6)
# ============================================================
HOFSTEDE_DIMENSIONS = [
    "individualism vs collectivism",
    "power distance: hierarchical vs egalitarian",
    "uncertainty avoidance vs tolerance for ambiguity",
    "masculinity (achievement) vs femininity (cooperation)",
    "long-term orientation vs short-term focus",
    "indulgence vs restraint",
]
SCHWARTZ_VALUES = [
    "self-direction: independent thought vs conformity",
    "stimulation: novelty vs stability",
    "hedonism: pleasure vs duty",
    "achievement: personal success vs collective good",
    "power: dominance vs cooperation",
    "security: safety vs risk-taking",
    "tradition: respect for custom vs innovation",
    "benevolence: caring for ingroup vs self-interest",
    "universalism: justice for all vs ingroup loyalty",
]
BIG_FIVE = [
    "openness: curious vs conventional",
    "conscientiousness: organized vs spontaneous",
    "extraversion: outgoing vs reserved",
    "agreeableness: cooperative vs competitive",
    "neuroticism: sensitive vs stable",
]
NDM_KLEIN = [
    "intuitive pattern-matching vs deliberate analysis",
    "experiential expert judgment vs novice rule-following",
    "fast satisficing vs slow optimizing",
    "situation awareness vs option enumeration",
    "mental simulation vs explicit comparison",
]


# ============================================================
# Data loading
# ============================================================
def load_all_constructs() -> pd.DataFrame:
    """Load every elicited construct from every completed cell.
    Returns DataFrame with columns:
      cell_id, task, condition, run, model_short, persona,
      construct_id, left, right, combined_text
    """
    if not RESULTS_DIR.exists():
        print(f"ERROR: {RESULTS_DIR} not found. Run experiment first.")
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

        # Persona assignment per model (from api_calls)
        persona_for = {}
        for call in cell.get("api_calls", []):
            if call["phase"] == "phase1_freeresponse":
                persona_for[call["model_short_name"]] = call.get("persona_or_neutral", "neutral")

        for model, constructs in cell.get("constructs", {}).items():
            persona = persona_for.get(model, "neutral")
            for c in constructs:
                left = c.get("left", "").strip()
                right = c.get("right", "").strip()
                if not left or not right:
                    continue
                rows.append({
                    "cell_id": cd.name,
                    "task": cell.get("task"),
                    "condition": cell.get("condition"),
                    "run": cell.get("run_idx"),
                    "model": model,
                    "persona": persona,
                    "construct_id": c.get("id", ""),
                    "left": left,
                    "right": right,
                    "combined_text": f"{left} -- {right}",
                })

    return pd.DataFrame(rows)


def load_all_ratings() -> pd.DataFrame:
    """Long-form ratings matrix across all cells.
    Columns: cell_id, model_rater, construct_id, element, rating
    """
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
                        "model_rater": rater,
                        "construct_id": cid,
                        "construct_origin": cid.split("_")[1] if "_" in cid else "?",
                        "element": ek,
                        "rating": val,
                    })
    return pd.DataFrame(rows)


def load_recommendations() -> pd.DataFrame:
    """Per-cell-per-model recommendation. From operator_insights if available."""
    if not OPERATOR_DIR.exists():
        return pd.DataFrame()
    rows = []
    for d in sorted(OPERATOR_DIR.iterdir()):
        if not d.is_dir():
            continue
        ins_file = d / "operator_insight.json"
        if not ins_file.exists():
            continue
        with open(ins_file, encoding="utf-8") as f:
            ins = json.load(f)
        for model, info in ins.get("consensus_map", {}).get("by_agent", {}).items():
            rows.append({
                "cell_id": d.name,
                "model": model,
                "persona": info.get("persona", "neutral"),
                "recommendation": info.get("recommendation"),
                "element_label": info.get("element_label"),
            })
    return pd.DataFrame(rows)


# ============================================================
# DECOMPOSITION 1: Semantic clustering of constructs
# ============================================================
def decomp1_semantic_clusters(df_c: pd.DataFrame, embed: EmbeddingBackend, out_dir: Path) -> dict:
    print("\n[1/7] Semantic clustering of constructs...")
    out_dir.mkdir(parents=True, exist_ok=True)
    if len(df_c) < 4:
        print(f"  Insufficient constructs ({len(df_c)} < 4); skipping.")
        return {"status": "insufficient"}

    embs = embed.encode(df_c["combined_text"].tolist())

    # Pick K via silhouette score
    best_k, best_score = 3, -1.0
    for k in range(3, min(11, len(df_c))):
        try:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(embs)
            if len(set(labels)) < 2:
                continue
            score = silhouette_score(embs, labels)
            if score > best_score:
                best_score = score
                best_k = k
        except Exception:
            pass

    km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    labels = km.fit_predict(embs)
    df_c = df_c.copy()
    df_c["cluster"] = labels

    # Get exemplar texts per cluster (closest to centroid)
    cluster_examples = {}
    for c in range(best_k):
        idx = np.where(labels == c)[0]
        if len(idx) == 0:
            continue
        centroid = km.cluster_centers_[c]
        dists = np.linalg.norm(embs[idx] - centroid, axis=1)
        sorted_idx = idx[np.argsort(dists)]
        cluster_examples[c] = [df_c.iloc[i]["combined_text"] for i in sorted_idx[:5]]

    # Visualize via PCA
    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(embs)
    fig, ax = plt.subplots(figsize=(12, 9), facecolor="white")
    palette = sns.color_palette("husl", best_k)
    for c in range(best_k):
        mask = labels == c
        ax.scatter(coords[mask, 0], coords[mask, 1], c=[palette[c]],
                   alpha=0.6, s=70, edgecolors="black", linewidth=0.3,
                   label=f"C{c} (n={mask.sum()})")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    ax.set_title(f"Semantic clustering of {len(df_c)} constructs (k={best_k}, silhouette={best_score:.3f})")
    ax.legend(loc="best", fontsize=9, framealpha=0.9)
    plt.tight_layout()
    plt.savefig(out_dir / "semantic_clusters.png", dpi=130, bbox_inches="tight")
    plt.close()

    # Save labelled constructs
    df_c[["cell_id", "model", "persona", "construct_id", "left", "right", "cluster"]].to_csv(
        out_dir / "constructs_with_clusters.csv", index=False
    )
    # Save cluster summary
    summary = pd.DataFrame([
        {"cluster": c, "size": int((labels == c).sum()),
         "examples": " | ".join(cluster_examples.get(c, [])[:3])}
        for c in range(best_k)
    ])
    summary.to_csv(out_dir / "cluster_summary.csv", index=False)

    return {
        "status": "ok", "n_clusters": best_k, "silhouette": float(best_score),
        "n_constructs": len(df_c), "examples": cluster_examples,
        "labels": labels.tolist(),
    }


# ============================================================
# DECOMPOSITION 2: Construct ownership (model fingerprint)
# ============================================================
def decomp2_model_fingerprint(df_c: pd.DataFrame, clusters: list, out_dir: Path) -> dict:
    print("[2/7] Model fingerprint analysis...")
    if "cluster" not in df_c.columns and clusters is None:
        return {"status": "no_clusters"}
    if clusters is not None:
        df_c = df_c.copy()
        df_c["cluster"] = clusters

    contingency = pd.crosstab(df_c["model"], df_c["cluster"])
    if contingency.size < 4:
        return {"status": "too_small"}

    try:
        chi2, p, dof, expected = chi2_contingency(contingency)
    except Exception as exc:
        return {"status": "failed", "error": str(exc)}

    # Visualize as heatmap with row-normalized proportions
    row_props = contingency.div(contingency.sum(axis=1), axis=0)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor="white")
    sns.heatmap(contingency, annot=True, fmt="d", cmap="Blues", ax=axes[0])
    axes[0].set_title(f"Construct count by model x cluster (chi2={chi2:.2f}, p={p:.4f})")
    sns.heatmap(row_props, annot=True, fmt=".2f", cmap="Reds", ax=axes[1], vmin=0, vmax=1)
    axes[1].set_title("Same, row-normalized (cluster proportion within each model)")
    plt.tight_layout()
    plt.savefig(out_dir / "model_fingerprints.png", dpi=130, bbox_inches="tight")
    plt.close()

    # Same analysis but by persona
    if "persona" in df_c.columns:
        per_contingency = pd.crosstab(df_c["persona"], df_c["cluster"])
        if per_contingency.size >= 4:
            try:
                chi2p, pp, _, _ = chi2_contingency(per_contingency)
                fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
                per_props = per_contingency.div(per_contingency.sum(axis=1), axis=0)
                sns.heatmap(per_props, annot=True, fmt=".2f", cmap="Greens", ax=ax, vmin=0, vmax=1)
                ax.set_title(f"Cluster proportion within each persona (chi2={chi2p:.2f}, p={pp:.4f})")
                plt.tight_layout()
                plt.savefig(out_dir / "persona_fingerprints.png", dpi=130, bbox_inches="tight")
                plt.close()
            except Exception:
                pass

    contingency.to_csv(out_dir / "model_cluster_counts.csv")
    return {
        "status": "ok",
        "chi2_model_cluster": float(chi2), "p_model_cluster": float(p),
        "interpretation": (
            "Model x cluster association is significant" if p < 0.05 else
            "No significant model x cluster association"
        ),
    }


# ============================================================
# DECOMPOSITION 3: Variance decomposition (persona vs model)
# ============================================================
def decomp3_variance_decomposition(df_c: pd.DataFrame, embed: EmbeddingBackend, out_dir: Path) -> dict:
    print("[3/7] Variance decomposition (persona vs model effect)...")
    if len(df_c) < 10:
        return {"status": "insufficient"}

    embs = embed.encode(df_c["combined_text"].tolist())
    # Reduce to 5 dims for variance partitioning
    pca = PCA(n_components=min(5, embs.shape[1], len(df_c) - 1), random_state=42)
    coords = pca.fit_transform(embs)

    # Compute total variance, between-group variance for: persona, model, task, condition
    def var_explained(coords, labels):
        labels = pd.Series(labels)
        total_var = np.var(coords, axis=0).sum()
        if total_var == 0:
            return 0.0
        between_var = 0.0
        global_mean = coords.mean(axis=0)
        for lbl in labels.unique():
            mask = labels == lbl
            if mask.sum() == 0:
                continue
            group_mean = coords[mask].mean(axis=0)
            between_var += mask.sum() * np.sum((group_mean - global_mean) ** 2)
        between_var /= len(coords)
        return float(between_var / total_var)

    parts = {
        "persona": var_explained(coords, df_c["persona"].values),
        "model": var_explained(coords, df_c["model"].values),
        "task": var_explained(coords, df_c["task"].values),
        "condition": var_explained(coords, df_c["condition"].values),
    }

    # Bar chart
    fig, ax = plt.subplots(figsize=(8, 5), facecolor="white")
    keys = list(parts.keys())
    vals = [parts[k] for k in keys]
    colors = ["#882b6f", "#0a558c", "#2d8659", "#8a5a00"]
    ax.bar(keys, vals, color=colors, edgecolor="black")
    ax.set_ylabel("Proportion of construct-space variance explained")
    ax.set_title("Variance decomposition: which factor drives construct diversity?")
    for i, v in enumerate(vals):
        ax.text(i, v + 0.005, f"{v:.3f}", ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(out_dir / "variance_decomposition.png", dpi=130, bbox_inches="tight")
    plt.close()

    # Interpretation
    top = max(parts, key=parts.get)
    return {
        "status": "ok", "parts": parts, "dominant_factor": top,
        "interpretation": (
            f"The strongest driver of construct diversity is {top.upper()} "
            f"(explains {parts[top]*100:.1f}% of variance). "
            f"Models alone explain {parts['model']*100:.1f}%, "
            f"personas alone explain {parts['persona']*100:.1f}%, "
            f"tasks explain {parts['task']*100:.1f}%."
        ),
    }


# ============================================================
# DECOMPOSITION 4: Procrustes alignment between models (Platonic test)
# ============================================================
def decomp4_procrustes(df_r: pd.DataFrame, out_dir: Path) -> dict:
    print("[4/7] Procrustes alignment (Platonic Representation test)...")
    if len(df_r) == 0:
        return {"status": "no_ratings"}

    models = sorted(df_r["model_rater"].unique())
    if len(models) < 2:
        return {"status": "too_few_models"}

    # For each model, build an (element x construct) rating matrix per cell, then concatenate
    model_matrices = {}
    for m in models:
        sub = df_r[df_r["model_rater"] == m]
        # Pivot: rows = (cell, element), cols = construct_id, vals = rating
        try:
            piv = sub.pivot_table(index=["cell_id", "element"],
                                  columns="construct_id", values="rating", aggfunc="mean")
            model_matrices[m] = piv
        except Exception:
            continue

    # Align all matrices to common (cell, element) x construct grid
    if len(model_matrices) < 2:
        return {"status": "insufficient_pivots"}

    common_idx = None
    common_cols = None
    for m, piv in model_matrices.items():
        common_idx = piv.index if common_idx is None else common_idx.intersection(piv.index)
        common_cols = piv.columns if common_cols is None else common_cols.intersection(piv.columns)

    if len(common_idx) < 3 or len(common_cols) < 2:
        return {"status": "no_common_grid",
                "interpretation": f"Common grid too small: {len(common_idx)} rows, {len(common_cols)} constructs"}

    # Pairwise Procrustes RMSE
    pairs = list(combinations(models, 2))
    rmse_matrix = pd.DataFrame(0.0, index=models, columns=models)
    for a, b in pairs:
        ma = model_matrices[a].loc[common_idx, common_cols].fillna(4.0).values
        mb = model_matrices[b].loc[common_idx, common_cols].fillna(4.0).values
        try:
            _, _, disparity = procrustes(ma, mb)
            rmse_matrix.loc[a, b] = disparity
            rmse_matrix.loc[b, a] = disparity
        except Exception:
            pass

    fig, ax = plt.subplots(figsize=(8, 6), facecolor="white")
    sns.heatmap(rmse_matrix, annot=True, fmt=".3f", cmap="RdYlGn_r",
                vmin=0, vmax=max(0.1, rmse_matrix.values.max()), ax=ax)
    ax.set_title("Procrustes disparity between models\n(low = same internal space, high = different)")
    plt.tight_layout()
    plt.savefig(out_dir / "procrustes_alignment.png", dpi=130, bbox_inches="tight")
    plt.close()
    rmse_matrix.to_csv(out_dir / "procrustes_disparity.csv")

    mean_disp = rmse_matrix.values[np.triu_indices_from(rmse_matrix.values, k=1)].mean()
    return {
        "status": "ok", "mean_disparity": float(mean_disp),
        "interpretation": (
            f"Mean pairwise Procrustes disparity = {mean_disp:.3f}. "
            f"{'Low value supports Platonic Representation Hypothesis (models share internal structure)' if mean_disp < 0.3 else 'High value rejects Platonic Hypothesis (models have structurally distinct spaces)'}."
        ),
    }


# ============================================================
# DECOMPOSITION 5: Construct -> Recommendation prediction
# ============================================================
def decomp5_construct_to_recommendation(
    df_r: pd.DataFrame, df_rec: pd.DataFrame, out_dir: Path
) -> dict:
    print("[5/7] Construct -> Recommendation prediction...")
    if len(df_r) == 0 or len(df_rec) == 0:
        return {"status": "missing_data"}

    # Join: per (cell, model), get the recommendation + average rating each construct gave to its OWN choice's element
    # Strategy: predict recommendation choice from the model's own rating fingerprint
    rec_with_element = df_rec[df_rec["recommendation"].notna() & df_rec["element_label"].notna()].copy()
    if len(rec_with_element) < 10:
        return {"status": "too_few_recommendations"}

    # For each (cell, rater_model), pivot the ratings to one row per (construct x element).
    # Then add target = which element this model recommended.
    feature_rows = []
    target_labels = []
    feature_names = None
    for (cell_id, model), grp in df_r.groupby(["cell_id", "model_rater"]):
        # Find this model's recommendation in this cell
        rec_row = rec_with_element[
            (rec_with_element["cell_id"] == cell_id) & (rec_with_element["model"] == model)
        ]
        if len(rec_row) == 0:
            continue
        elem_label = rec_row.iloc[0]["element_label"]
        # Build feature: per construct, the rating that THIS model gave to its CHOSEN element
        own_grp = grp[grp["element"] == elem_label]
        if own_grp.empty:
            continue
        feat = own_grp.groupby("construct_origin")["rating"].mean().to_dict()
        feature_rows.append(feat)
        target_labels.append(rec_row.iloc[0]["recommendation"])

    if len(feature_rows) < 5:
        return {"status": "too_few_samples", "n": len(feature_rows)}

    feat_df = pd.DataFrame(feature_rows).fillna(4.0)
    feature_names = list(feat_df.columns)
    X = feat_df.values
    y = np.array(target_labels)
    if len(set(y)) < 2:
        return {"status": "single_class"}

    try:
        # sklearn 1.5+ removed multi_class param - it's auto-detected from y
        clf = LogisticRegression(max_iter=2000)
        clf.fit(X, y)
        score = clf.score(X, y)
    except Exception as exc:
        return {"status": "model_failed", "error": str(exc)}

    importance = np.abs(clf.coef_).mean(axis=0)
    order = np.argsort(importance)[::-1]
    top = [(feature_names[i], float(importance[i])) for i in order[:10]]

    fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
    labels = [t[0] for t in top]
    vals = [t[1] for t in top]
    ax.barh(labels[::-1], vals[::-1], color="#0a558c", edgecolor="black")
    ax.set_xlabel("Mean abs coefficient")
    ax.set_title(f"Construct origins most predictive of recommendation (train acc = {score:.2f})")
    plt.tight_layout()
    plt.savefig(out_dir / "construct_to_recommendation.png", dpi=130, bbox_inches="tight")
    plt.close()

    return {"status": "ok", "train_accuracy": float(score), "top_features": top}


# ============================================================
# DECOMPOSITION 6: Construct novelty vs baselines
# ============================================================
def decomp6_novelty(df_c: pd.DataFrame, embed: EmbeddingBackend, out_dir: Path) -> dict:
    print("[6/7] Construct novelty vs known taxonomies...")
    if len(df_c) < 4:
        return {"status": "insufficient"}

    all_baselines = {
        "Hofstede": HOFSTEDE_DIMENSIONS,
        "Schwartz": SCHWARTZ_VALUES,
        "Big Five": BIG_FIVE,
        "NDM-Klein": NDM_KLEIN,
    }
    # Embed every baseline and every construct
    construct_texts = df_c["combined_text"].tolist()
    construct_embs = embed.encode(construct_texts)
    construct_embs = construct_embs / (np.linalg.norm(construct_embs, axis=1, keepdims=True) + 1e-9)

    # Per baseline, find nearest neighbor for each construct
    novelty_rows = []
    for name, items in all_baselines.items():
        be = embed.encode(items)
        be = be / (np.linalg.norm(be, axis=1, keepdims=True) + 1e-9)
        # Cosine similarity
        sims = construct_embs @ be.T  # (n_constructs, n_baseline_items)
        max_sims = sims.max(axis=1)
        novelty_rows.append({
            "baseline": name,
            "mean_max_similarity": float(max_sims.mean()),
            "median_max_similarity": float(np.median(max_sims)),
            "frac_novel_at_0.5": float((max_sims < 0.5).mean()),
            "frac_novel_at_0.4": float((max_sims < 0.4).mean()),
        })

    df_nov = pd.DataFrame(novelty_rows)
    df_nov.to_csv(out_dir / "novelty_vs_baselines.csv", index=False)

    fig, ax = plt.subplots(figsize=(10, 5), facecolor="white")
    x = np.arange(len(df_nov))
    width = 0.35
    ax.bar(x - width/2, df_nov["mean_max_similarity"], width, label="Mean max similarity",
           color="#0a558c", edgecolor="black")
    ax.bar(x + width/2, df_nov["frac_novel_at_0.5"], width, label="Fraction novel (cos<0.5)",
           color="#b03030", edgecolor="black")
    ax.set_xticks(x)
    ax.set_xticklabels(df_nov["baseline"])
    ax.set_ylabel("Score")
    ax.set_title("How novel are model-elicited constructs vs established taxonomies?")
    ax.legend()
    ax.set_ylim(0, 1.05)
    plt.tight_layout()
    plt.savefig(out_dir / "novelty_vs_baselines.png", dpi=130, bbox_inches="tight")
    plt.close()

    return {"status": "ok", "summary": df_nov.to_dict(orient="records")}


# ============================================================
# DECOMPOSITION 7: Hierarchical structure
# ============================================================
def decomp7_hierarchy(df_c: pd.DataFrame, embed: EmbeddingBackend, out_dir: Path) -> dict:
    print("[7/7] Hierarchical structure...")
    if len(df_c) < 4:
        return {"status": "insufficient"}

    texts = df_c["combined_text"].tolist()
    embs = embed.encode(texts)

    # Truncate labels for readability
    labels = [
        f"{r['model']}/{r['persona'][0]} {r['left'][:25]}/{r['right'][:25]}"
        for _, r in df_c.iterrows()
    ]
    # Limit display to first 60 constructs to keep dendrogram readable
    if len(labels) > 60:
        idx = np.linspace(0, len(labels) - 1, 60).astype(int)
        embs = embs[idx]
        labels = [labels[i] for i in idx]

    dist = pdist(embs, metric="cosine")
    link = linkage(dist, method="average")

    fig, ax = plt.subplots(figsize=(14, max(8, len(labels) * 0.18)), facecolor="white")
    dendrogram(link, labels=labels, orientation="left", leaf_font_size=7, ax=ax)
    ax.set_title(f"Hierarchical clustering of {len(labels)} constructs (cosine, average linkage)")
    plt.tight_layout()
    plt.savefig(out_dir / "construct_dendrogram.png", dpi=130, bbox_inches="tight")
    plt.close()

    return {"status": "ok", "n_shown": len(labels)}


# ============================================================
# Master report writer
# ============================================================
def write_findings(results: dict, out_dir: Path, n_constructs: int):
    lines = ["# Construct Decomposition Findings\n"]
    lines.append("Auto-generated by construct_decomposition.py.\n")
    lines.append(f"\n**Total constructs analyzed:** {n_constructs}\n")

    lines.append("\n## 1. Semantic clustering\n")
    r = results.get("decomp1", {})
    if r.get("status") == "ok":
        lines.append(f"Identified **{r['n_clusters']} clusters** (silhouette = {r['silhouette']:.3f}).\n")
        lines.append("Top exemplars per cluster:\n")
        for c, ex in r.get("examples", {}).items():
            lines.append(f"- **Cluster {c}**: {ex[0][:160]}\n")
    else:
        lines.append(f"Skipped: {r.get('status')}\n")

    lines.append("\n## 2. Model fingerprint\n")
    r = results.get("decomp2", {})
    if r.get("status") == "ok":
        lines.append(f"- chi-square = {r['chi2_model_cluster']:.2f}, p = {r['p_model_cluster']:.4f}\n")
        lines.append(f"- {r['interpretation']}\n")
        lines.append("\nSee `model_fingerprints.png` for the heatmap.\n")
    else:
        lines.append(f"Skipped: {r.get('status')}\n")

    lines.append("\n## 3. Variance decomposition (KEY ANALYTICAL RESULT)\n")
    r = results.get("decomp3", {})
    if r.get("status") == "ok":
        lines.append(f"- {r['interpretation']}\n")
        lines.append("\nFull breakdown:\n")
        for k, v in r["parts"].items():
            lines.append(f"  - **{k.title()}**: {v*100:.1f}%\n")
    else:
        lines.append(f"Skipped: {r.get('status')}\n")

    lines.append("\n## 4. Procrustes alignment (Platonic Hypothesis test)\n")
    r = results.get("decomp4", {})
    if r.get("status") == "ok":
        lines.append(f"- Mean pairwise disparity: **{r['mean_disparity']:.3f}**\n")
        lines.append(f"- {r['interpretation']}\n")
    else:
        lines.append(f"Skipped: {r.get('status')}. {r.get('interpretation', '')}\n")

    lines.append("\n## 5. Construct -> Recommendation prediction\n")
    r = results.get("decomp5", {})
    if r.get("status") == "ok":
        lines.append(f"- Logistic regression training accuracy: **{r['train_accuracy']:.2f}**\n")
        lines.append("- Top construct origins (most predictive of recommendation):\n")
        for name, val in r["top_features"]:
            lines.append(f"  - **{name}**: coefficient magnitude {val:.3f}\n")
    else:
        lines.append(f"Skipped: {r.get('status')}\n")

    lines.append("\n## 6. Novelty vs known taxonomies\n")
    r = results.get("decomp6", {})
    if r.get("status") == "ok":
        for row in r["summary"]:
            lines.append(
                f"- **{row['baseline']}**: mean max similarity = {row['mean_max_similarity']:.3f}, "
                f"fraction novel (cos<0.5) = {row['frac_novel_at_0.5']*100:.0f}%\n"
            )
    else:
        lines.append(f"Skipped: {r.get('status')}\n")

    lines.append("\n## 7. Hierarchical structure\n")
    r = results.get("decomp7", {})
    if r.get("status") == "ok":
        lines.append(f"Dendrogram of {r['n_shown']} constructs saved as `construct_dendrogram.png`.\n")
    else:
        lines.append(f"Skipped: {r.get('status')}\n")

    lines.append("\n---\n")
    lines.append("\n## How to read this report\n")
    lines.append("- **Decomp 3 is the headline analysis**: if `persona` dominates over `model`, this supports the rephrased hypothesis 'epistemic framing drives diversity, not architecture'.\n")
    lines.append("- **Decomp 4 tests Platonic Hypothesis**: low Procrustes disparity supports the hypothesis that frontier models share latent representations.\n")
    lines.append("- **Decomp 2 tests model fingerprint**: if chi-square significant, each model has a distinctive 'voice' in what constructs it elicits.\n")

    (out_dir / "CONSTRUCT_DECOMPOSITION_FINDINGS.md").write_text("".join(lines), encoding="utf-8")
    print(f"\nWrote {out_dir / 'CONSTRUCT_DECOMPOSITION_FINDINGS.md'}")


# ============================================================
# Main
# ============================================================
def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=str(OUT_DIR))
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading data from {RESULTS_DIR} and {OPERATOR_DIR}...")
    df_c = load_all_constructs()
    df_r = load_all_ratings()
    df_rec = load_recommendations()
    print(f"  constructs: {len(df_c)}")
    print(f"  ratings: {len(df_r)}")
    print(f"  recommendations: {len(df_rec)}")

    if len(df_c) == 0:
        print("ERROR: no constructs to analyze. Run the experiment first.")
        return 1

    embed = EmbeddingBackend()

    results = {}
    results["decomp1"] = decomp1_semantic_clusters(df_c, embed, out_dir)
    cluster_labels = results["decomp1"].get("labels")
    results["decomp2"] = decomp2_model_fingerprint(df_c, cluster_labels, out_dir)
    results["decomp3"] = decomp3_variance_decomposition(df_c, embed, out_dir)
    results["decomp4"] = decomp4_procrustes(df_r, out_dir)
    results["decomp5"] = decomp5_construct_to_recommendation(df_r, df_rec, out_dir)
    results["decomp6"] = decomp6_novelty(df_c, embed, out_dir)
    results["decomp7"] = decomp7_hierarchy(df_c, embed, out_dir)

    write_findings(results, out_dir, n_constructs=len(df_c))

    # Save full results JSON
    with open(out_dir / "decomposition_results.json", "w", encoding="utf-8") as f:
        json.dump({k: v for k, v in results.items()}, f, indent=2, default=str)

    print(f"\nAll done. See {out_dir}/CONSTRUCT_DECOMPOSITION_FINDINGS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
