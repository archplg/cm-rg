#!/usr/bin/env python3
"""
Generate rich visualizations + interpretations for each cell and across all cells.

Outputs per cell (under analysis/<cell_id>/):
- agreement_network.png       Network graph: agents as nodes, edges = reasoning similarity
- consensus_vs_reasoning.png  Recommendation distribution overlaid with reasoning clusters
- biplot_annotated.png        PCA biplot with axis interpretations
- disagreement_heatmap.png    5x5 matrix of pairwise reasoning distance

Cross-cell outputs (under analysis/cross_cell/):
- landscape.png               All cells in (consensus_strength x reasoning_diversity) space
- severity_distribution.png   Bar chart of severities across cells
- summary_panel.png           4-panel summary

Each PNG comes with a paired .interpretation.md file containing a 2-3 paragraph
plain-English explanation of what the chart shows and how to read it.

Run:
    python visualizations.py                  # all completed cells
    python visualizations.py --cell B_N_run1  # single cell
"""
from __future__ import annotations
import argparse
import json
from itertools import combinations
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA

# Archipelago color palette (matches archplg.co.uk aesthetic)
COLORS = {
    "Q": "#0a558c",  # Quantitative - blue
    "S": "#2d8659",  # Systems - green
    "E": "#8a5a00",  # Engineering - amber
    "H": "#882b6f",  # Humanist - purple
    "C": "#b03030",  # Contrarian - red
    "neutral": "#666666",
    "bg": "#f4f1e8",
    "accent": "#c8a45c",
    "text": "#2b3a55",
    "flag": "#c44",
    "good": "#3a7d44",
}

PERSONA_LABELS = {
    "Q": "Quantitative",
    "S": "Systems",
    "E": "Engineering",
    "H": "Humanist",
    "C": "Contrarian",
    "neutral": "Neutral",
}

RESULTS_DIR = Path("./results")
OPERATOR_DIR = Path("./operator_outputs")
ANALYSIS_DIR = Path("./analysis")


# ============================================================
# Data loading
# ============================================================
def load_cell(cell_id: str) -> dict | None:
    p = RESULTS_DIR / cell_id / "cell.json"
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def load_insight(cell_id: str) -> dict | None:
    p = OPERATOR_DIR / cell_id / "operator_insight.json"
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def build_agent_fingerprint_vectors(cell: dict) -> dict:
    """For each agent, build a flat vector of their ratings across (construct, element)."""
    all_constructs = []
    for sn in sorted(cell.get("constructs", {}).keys()):
        all_constructs.extend(cell["constructs"][sn])
    construct_ids = [c["id"] for c in all_constructs]
    elements = sorted(cell.get("element_summaries", {}).keys())

    fingerprints = {}
    for rater, ratings in cell.get("ratings", {}).items():
        vec = []
        for cid in construct_ids:
            for ek in elements:
                v = ratings.get(cid, {}).get(ek)
                vec.append(float(v) if v is not None else np.nan)
        fingerprints[rater] = np.array(vec)
    return fingerprints


def pairwise_rmse(fingerprints: dict) -> dict:
    """Pairwise RMSE between rating fingerprints."""
    out = {}
    keys = sorted(fingerprints.keys())
    for a, b in combinations(keys, 2):
        va, vb = fingerprints[a], fingerprints[b]
        mask = ~(np.isnan(va) | np.isnan(vb))
        if mask.sum() < 5:
            continue
        rmse = float(np.sqrt(np.mean((va[mask] - vb[mask]) ** 2)))
        out[(a, b)] = rmse
    return out


# ============================================================
# Visualization 1: Agreement network graph
# ============================================================
def plot_agreement_network(cell: dict, insight: dict, out_path: Path) -> str:
    """
    Network graph where:
    - Each node = an agent, colored by persona, sized by NaN
    - Each edge = reasoning similarity (1 / RMSE), thicker = more agreement
    - Node placement = force-directed layout (agents with similar reasoning cluster)
    - Color of agent's recommendation halo = which option they chose
    """
    fingerprints = build_agent_fingerprint_vectors(cell)
    rmses = pairwise_rmse(fingerprints)
    if not rmses or len(fingerprints) < 2:
        return ""

    consensus = insight["consensus_map"]
    by_agent = consensus["by_agent"]
    agents = sorted(fingerprints.keys())
    n = len(agents)

    # Compute 2D positions using PCA on rating fingerprints (or fallback to circle)
    max_len = max(len(v) for v in fingerprints.values())
    mat = np.array([
        np.pad(v, (0, max_len - len(v)), constant_values=np.nan)
        for v in [fingerprints[a] for a in agents]
    ])
    # Replace NaN with column mean for layout purposes only.
    # Suppress benign RuntimeWarning when an entire column is NaN (happens
    # when a model has no ratings at all - then column mean is undefined).
    with np.errstate(invalid="ignore"):
        import warnings as _w
        with _w.catch_warnings():
            _w.simplefilter("ignore", category=RuntimeWarning)
            col_mean = np.nanmean(mat, axis=0)
    # If a whole column is NaN, col_mean is NaN; replace those with 0
    # so PCA doesn't propagate NaN into all positions.
    col_mean = np.where(np.isnan(col_mean), 0.0, col_mean)
    mat_filled = np.where(np.isnan(mat), col_mean, mat)
    if mat_filled.shape[1] > 1:
        try:
            pca = PCA(n_components=2)
            pos = pca.fit_transform(mat_filled)
            # Scale to reasonable plot range
            for col in range(2):
                rng = pos[:, col].max() - pos[:, col].min()
                if rng > 0:
                    pos[:, col] = (pos[:, col] - pos[:, col].min()) / rng * 2 - 1
        except Exception:
            angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
            pos = np.column_stack([np.cos(angles), np.sin(angles)])
    else:
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
        pos = np.column_stack([np.cos(angles), np.sin(angles)])

    # Make figure
    fig, ax = plt.subplots(figsize=(11, 9), facecolor="white")
    ax.set_facecolor(COLORS["bg"])

    # Draw edges (one per pair)
    max_rmse = max(rmses.values()) if rmses else 1.0
    min_rmse = min(rmses.values()) if rmses else 0.0
    rmse_range = max_rmse - min_rmse + 1e-6
    for (a, b), rmse in rmses.items():
        i, j = agents.index(a), agents.index(b)
        # Edge width inversely proportional to RMSE (closer reasoning = thicker)
        norm = 1.0 - (rmse - min_rmse) / rmse_range  # 1.0 = strongest agreement
        width = 0.5 + norm * 7.0
        alpha = 0.35 + norm * 0.55
        color = COLORS["good"] if rmse < 0.5 else COLORS["accent"] if rmse < 1.0 else COLORS["flag"]
        ax.plot([pos[i, 0], pos[j, 0]], [pos[i, 1], pos[j, 1]],
                color=color, linewidth=width, alpha=alpha, zorder=1)
        # Label edge with RMSE near midpoint
        midx, midy = (pos[i, 0] + pos[j, 0]) / 2, (pos[i, 1] + pos[j, 1]) / 2
        ax.text(midx, midy, f"{rmse:.2f}", fontsize=8, color="#444",
                ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                          edgecolor="none", alpha=0.85))

    # Draw nodes
    for i, sn in enumerate(agents):
        info = by_agent.get(sn, {})
        persona = info.get("persona", "neutral")
        node_color = COLORS.get(persona, COLORS["neutral"])
        rec = info.get("recommendation") or "?"

        # Outer halo colored by recommendation
        rec_colors = {
            "A": "#cce0ff", "B": "#ffdfbf", "C": "#bfe6c8",
            "D": "#f5c8e1", "E": "#fff0a8", None: "#dddddd", "?": "#dddddd"
        }
        halo_color = rec_colors.get(rec, "#dddddd")
        ax.scatter(pos[i, 0], pos[i, 1], s=2200, c=halo_color,
                   edgecolors="white", linewidth=2, zorder=2)
        # Inner node colored by persona
        ax.scatter(pos[i, 0], pos[i, 1], s=900, c=node_color,
                   edgecolors="white", linewidth=2, zorder=3)
        # Agent label inside node
        ax.text(pos[i, 0], pos[i, 1], sn, color="white",
                ha="center", va="center", fontsize=13, fontweight="bold", zorder=4)
        # Persona + recommendation label below node
        persona_lbl = PERSONA_LABELS.get(persona, persona)
        ax.text(pos[i, 0], pos[i, 1] - 0.18,
                f"{persona_lbl}\nrec: {rec}",
                ha="center", va="top", fontsize=9, color="#222")

    # Legend
    legend_elements = [
        mpatches.Patch(color=COLORS["good"], label="Strong reasoning alignment (RMSE < 0.5)"),
        mpatches.Patch(color=COLORS["accent"], label="Moderate (0.5 - 1.0)"),
        mpatches.Patch(color=COLORS["flag"], label="Substantial disagreement (RMSE > 1.0)"),
    ]
    ax.legend(handles=legend_elements, loc="lower left", fontsize=9,
              framealpha=0.9, edgecolor="#ccc")

    # Title and meta
    headline = insight.get("headline", "")
    ax.set_title(
        f"Reasoning agreement network - cell {cell['cell_id']}\n"
        + headline[:110],
        fontsize=13, color=COLORS["text"], pad=20
    )
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)

    plt.tight_layout()
    plt.savefig(out_path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close()

    # Write interpretation
    interp = (
        "## How to read this network\n\n"
        "Each circle is an LLM agent in the panel. Position on the canvas reflects "
        "how similarly the agent rated all the elements: agents close together "
        "reason about the decision in similar ways, agents far apart reason "
        "differently.\n\n"
        "The lines between circles encode reasoning agreement. Green-and-thick = "
        "the two agents reason almost identically. Yellow-medium = they differ on "
        "framing. Red-thin = substantial disagreement at the reasoning level even "
        "if their final recommendations might match.\n\n"
        "Inside each circle is the agent label and its epistemological frame "
        "(Quantitative, Systems, Engineering, Humanist, Contrarian). The "
        "halo color around each circle indicates which option that agent "
        "recommended.\n\n"
        f"For this case: **{headline}**\n\n"
    )
    cm = insight["consensus_map"]
    hidden = insight["hidden_disagreement"]
    if cm.get("consensus_strength") == "strong" and hidden.get("reasoning_diversity_score", 0) > 0.5:
        interp += (
            "**Operator note:** the recommendation halos look unified (most "
            "agents chose the same option), but the network edges reveal "
            "underlying reasoning differences. Standard aggregation would "
            "miss this. Probe the framings before committing to execution.\n"
        )
    elif cm.get("consensus_strength") == "split":
        interp += (
            "**Operator note:** halos show different recommendations - the "
            "panel is split. The network helps you see WHICH agents reason "
            "alike and which don't, which is more useful than counting "
            "votes.\n"
        )
    else:
        interp += (
            "**Operator note:** both halos and network edges suggest aligned "
            "thinking. The consensus appears robust.\n"
        )

    return interp


# ============================================================
# Visualization 2: Disagreement heatmap (5x5)
# ============================================================
def plot_disagreement_heatmap(cell: dict, insight: dict, out_path: Path) -> str:
    fingerprints = build_agent_fingerprint_vectors(cell)
    if len(fingerprints) < 2:
        return ""
    agents = sorted(fingerprints.keys())
    by_agent = insight["consensus_map"]["by_agent"]
    n = len(agents)
    mat = np.zeros((n, n))
    for i, a in enumerate(agents):
        for j, b in enumerate(agents):
            if i == j:
                continue
            va, vb = fingerprints[a], fingerprints[b]
            mask = ~(np.isnan(va) | np.isnan(vb))
            if mask.sum() < 5:
                mat[i, j] = np.nan
            else:
                mat[i, j] = float(np.sqrt(np.mean((va[mask] - vb[mask]) ** 2)))

    # Labels with persona
    labels = []
    for a in agents:
        p = by_agent.get(a, {}).get("persona", "?")
        rec = by_agent.get(a, {}).get("recommendation", "?")
        labels.append(f"{a}\n({p})\n→{rec}")

    fig, ax = plt.subplots(figsize=(8.5, 7), facecolor="white")
    sns.heatmap(
        pd.DataFrame(mat, index=labels, columns=labels),
        annot=True, fmt=".2f", cmap="RdYlGn_r",
        vmin=0, vmax=2.5, center=1.0,
        cbar_kws={"label": "RMSE in rating space (1-7 scale)"},
        linewidths=0.5, square=True, ax=ax,
    )
    ax.set_title(
        f"Pairwise reasoning distance - cell {cell['cell_id']}",
        fontsize=12, color=COLORS["text"], pad=15
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close()

    interp = (
        "## How to read this heatmap\n\n"
        "Each cell shows the reasoning distance between two agents. Values are "
        "in RMSE (root-mean-square error) on the 1-7 Likert rating scale. "
        "Roughly: 0.0-0.5 = aligned reasoning, 0.5-1.0 = moderate differences, "
        "1.0-2.0 = substantial differences, 2.0+ = very different framings.\n\n"
        "Read along a row or column to see how that agent's reasoning compares "
        "to each other agent. Hot spots (red) mark pairs that reason differently "
        "even if they may have reached the same recommendation.\n\n"
        "Each label shows: agent ID, epistemological frame in parentheses, "
        "and the option that agent recommended (→).\n"
    )
    return interp


# ============================================================
# Visualization 3: Annotated PCA biplot
# ============================================================
def plot_annotated_biplot(cell: dict, insight: dict, out_path: Path) -> str:
    elements = sorted(cell.get("element_summaries", {}).keys())
    all_constructs = []
    for sn in sorted(cell.get("constructs", {}).keys()):
        all_constructs.extend(cell["constructs"][sn])
    if not (elements and all_constructs):
        return ""
    construct_ids = [c["id"] for c in all_constructs]
    construct_meta = {c["id"]: c for c in all_constructs}

    # Build mean rating matrix (elements x constructs)
    mean_mat = np.zeros((len(elements), len(construct_ids)))
    counts = np.zeros_like(mean_mat)
    for rater, rdata in cell.get("ratings", {}).items():
        for cid, elem_ratings in rdata.items():
            if cid not in construct_ids:
                continue
            j = construct_ids.index(cid)
            for ek, val in elem_ratings.items():
                if ek in elements:
                    i = elements.index(ek)
                    mean_mat[i, j] += val
                    counts[i, j] += 1
    valid = counts > 0
    mean_mat = np.where(valid, mean_mat / np.maximum(counts, 1), np.nan)
    valid_cols = ~np.isnan(mean_mat).any(axis=0)
    if valid_cols.sum() < 2 or mean_mat.shape[0] < 2:
        return ""
    clean = mean_mat[:, valid_cols]
    valid_cids = [c for c, v in zip(construct_ids, valid_cols) if v]

    n_comp = min(2, clean.shape[0] - 1, clean.shape[1])
    if n_comp < 2:
        return ""
    pca = PCA(n_components=2)
    coords = pca.fit_transform(clean)
    loadings = pca.components_.T  # (constructs, 2)

    # Find top loading on each PC to label the axis
    def axis_label(pc_idx):
        top_pos = max(range(len(valid_cids)), key=lambda i: loadings[i, pc_idx])
        top_neg = min(range(len(valid_cids)), key=lambda i: loadings[i, pc_idx])
        pos_c = construct_meta[valid_cids[top_pos]]
        neg_c = construct_meta[valid_cids[top_neg]]
        var = pca.explained_variance_ratio_[pc_idx] * 100
        return (f"PC{pc_idx + 1} ({var:.1f}%): {neg_c['right'][:35]} ← → {pos_c['left'][:35]}",
                neg_c, pos_c)

    pc1_label, pc1_neg, pc1_pos = axis_label(0)
    pc2_label, pc2_neg, pc2_pos = axis_label(1)

    fig, ax = plt.subplots(figsize=(11, 8.5), facecolor="white")
    ax.set_facecolor("#fafaf7")

    # Plot elements
    by_agent = insight["consensus_map"]["by_agent"]
    element_mapping = cell.get("element_mapping", {})  # E1 -> M1
    elem_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    for i, e in enumerate(elements):
        sn = element_mapping.get(e, "?")
        info = by_agent.get(sn, {})
        persona = info.get("persona", "neutral")
        rec = info.get("recommendation", "?")
        ax.scatter(coords[i, 0], coords[i, 1], s=420, c=elem_colors[i % 5],
                   edgecolors="white", linewidth=2.5, zorder=3, alpha=0.85)
        ax.annotate(f"{e}\n(by {sn}/{PERSONA_LABELS.get(persona, persona)[:5]} → {rec})",
                    (coords[i, 0], coords[i, 1]), xytext=(8, 8),
                    textcoords="offset points", fontsize=10, fontweight="bold",
                    color="#222")

    # Plot top construct loadings (top 6 by magnitude)
    magnitudes = np.linalg.norm(loadings, axis=1)
    top_idx = np.argsort(-magnitudes)[:6]
    scale = max(np.abs(coords).max(), 1.0) * 0.7
    for idx in top_idx:
        cid = valid_cids[idx]
        meta = construct_meta[cid]
        x, y = loadings[idx, 0] * scale, loadings[idx, 1] * scale
        ax.arrow(0, 0, x, y, alpha=0.4, color="#888",
                 head_width=0.04, length_includes_head=True, zorder=1)
        ax.annotate(
            f"{meta['left'][:25]} ↔ {meta['right'][:25]}",
            (x * 1.1, y * 1.1), fontsize=7.5, color="#666",
            ha="center", alpha=0.85
        )

    ax.axhline(0, color="#ccc", linestyle="--", alpha=0.5, zorder=0)
    ax.axvline(0, color="#ccc", linestyle="--", alpha=0.5, zorder=0)
    ax.set_xlabel(pc1_label, fontsize=10, color=COLORS["text"])
    ax.set_ylabel(pc2_label, fontsize=10, color=COLORS["text"])
    ax.set_title(
        f"Decision space - cell {cell['cell_id']}\n"
        f"Where each option lives in the space the agents construed it through",
        fontsize=12, color=COLORS["text"], pad=15
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close()

    interp = (
        "## How to read this decision-space map\n\n"
        "Each colored dot is one of the 5 options under consideration, "
        "positioned in a 2D space derived from how all the agents rated all the "
        "constructs. Options close together were seen similarly by the panel; "
        "options far apart were seen as fundamentally different kinds of "
        "choices.\n\n"
        "The axes are interpretable. The horizontal axis (PC1) is dominated by "
        f"**{pc1_neg['right'][:50]}** on one end and **{pc1_pos['left'][:50]}** "
        f"on the other - this is the single biggest dimension along which the "
        f"options differ. The vertical axis (PC2) is dominated by "
        f"**{pc2_neg['right'][:50]}** vs **{pc2_pos['left'][:50]}**.\n\n"
        "Gray arrows show which construct dimensions point in which direction. "
        "If two options are far apart along one arrow, the construct that arrow "
        "represents is what makes them feel different. If an arrow is short, "
        "that construct does not strongly differentiate the options.\n\n"
        "Each label shows: option ID, the agent who authored that response, "
        "their epistemological frame, and the option they recommended.\n"
    )
    return interp


# ============================================================
# Visualization 4: Consensus split with reasoning clusters
# ============================================================
def plot_consensus_split(cell: dict, insight: dict, out_path: Path) -> str:
    by_agent = insight["consensus_map"]["by_agent"]
    dist = insight["consensus_map"].get("distribution", {})
    if not dist:
        return ""
    hidden = insight["hidden_disagreement"]
    score = hidden.get("reasoning_diversity_score", 0) if hidden.get("status") == "computed" else 0

    options = sorted(dist.keys())
    counts = [dist[o] for o in options]

    fig, ax = plt.subplots(figsize=(11, 6), facecolor="white")
    # Bars by recommendation count, color-coded by recommendation
    rec_colors = {
        "A": "#1f77b4", "B": "#ff7f0e", "C": "#2ca02c",
        "D": "#d62728", "E": "#9467bd"
    }
    bar_colors = [rec_colors.get(o, "#888") for o in options]
    bars = ax.bar(options, counts, color=bar_colors, edgecolor="white",
                  linewidth=2, alpha=0.7, width=0.5)
    for bar, c in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                str(c), ha="center", va="bottom", fontsize=13, fontweight="bold")

    # Overlay: for each option, plot the agents who chose it as small circles
    # vertically arranged inside the bar, colored by persona
    for o, c in zip(options, counts):
        agents_for_o = [sn for sn, info in by_agent.items()
                        if info.get("recommendation") == o]
        for k, sn in enumerate(agents_for_o):
            persona = by_agent[sn].get("persona", "neutral")
            yp = (k + 1) / (c + 1) * c
            ax.scatter(options.index(o), yp, s=400,
                       c=COLORS.get(persona, COLORS["neutral"]),
                       edgecolors="white", linewidth=2, zorder=3)
            ax.text(options.index(o), yp, sn, color="white", ha="center",
                    va="center", fontsize=9, fontweight="bold", zorder=4)

    ax.set_xlabel("Option recommended", fontsize=11)
    ax.set_ylabel("Number of agents", fontsize=11)
    ax.set_ylim(0, max(counts) + 1)
    ax.set_yticks(range(max(counts) + 1))
    ax.grid(axis="y", alpha=0.3)

    # Annotation box for hidden disagreement
    if score > 0.5:
        msg = (
            f"⚠ Hidden disagreement detected\n"
            f"Reasoning RMSE: {score:.2f}\n"
            f"Agents share the output but not the framing"
        )
        bg = "#fdf0ed" if score > 1.0 else "#fdfaf2"
        ec = COLORS["flag"] if score > 1.0 else COLORS["accent"]
    else:
        msg = (
            f"✓ Consensus appears robust\n"
            f"Reasoning RMSE: {score:.2f}\n"
            f"Output and framing aligned"
        )
        bg = "#f0f7ed"
        ec = COLORS["good"]
    ax.text(
        0.98, 0.95, msg, transform=ax.transAxes,
        ha="right", va="top", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor=bg, edgecolor=ec, linewidth=1.5)
    )

    ax.set_title(
        f"Recommendations - cell {cell['cell_id']}\n"
        "Each dot = one agent (colored by epistemological frame)",
        fontsize=12, color=COLORS["text"], pad=15
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close()

    interp = (
        "## How to read this chart\n\n"
        "Bars show how many agents recommended each option. Each bar is annotated "
        "with the individual agents who supported it, color-coded by epistemological "
        "frame.\n\n"
        "**The key signal is in the corner box.** A check-mark means the "
        "panel's agreement runs deep - they share both the recommendation and "
        "the reasoning. A warning means they share the recommendation but not "
        "the underlying logic; this is the configuration most likely to produce "
        "execution surprises.\n"
    )
    return interp


# ============================================================
# Visualization 5: Cross-cell landscape
# ============================================================
def plot_cross_cell_landscape(out_path: Path) -> str:
    """Plot all cells in (consensus_strength x reasoning_diversity) space."""
    if not OPERATOR_DIR.exists():
        return ""
    all_insights = []
    for d in OPERATOR_DIR.iterdir():
        if d.is_dir() and (d / "operator_insight.json").exists():
            all_insights.append(json.loads(
                (d / "operator_insight.json").read_text(encoding="utf-8")
            ))
    if not all_insights:
        return ""

    fig, ax = plt.subplots(figsize=(11, 8), facecolor="white")
    ax.set_facecolor(COLORS["bg"])

    # x = number of agents in majority (1-5)
    # y = reasoning diversity score
    for ins in all_insights:
        cm = ins["consensus_map"]
        hidden = ins["hidden_disagreement"]
        dist = cm.get("distribution", {})
        majority = cm.get("majority_recommendation")
        n_majority = dist.get(majority, 0) if majority else 0
        score = hidden.get("reasoning_diversity_score", 0) if hidden.get("status") == "computed" else 0

        # Color by severity
        if cm.get("consensus_strength") == "strong" and score > 1.0:
            color = COLORS["flag"]
            severity = "HIGH"
        elif cm.get("consensus_strength") == "strong" and score > 0.5:
            color = COLORS["accent"]
            severity = "MEDIUM"
        elif cm.get("consensus_strength") == "strong":
            color = COLORS["good"]
            severity = "LOW"
        elif cm.get("consensus_strength") == "split":
            color = "#888"
            severity = "INFO"
        else:
            color = COLORS["accent"]
            severity = "MEDIUM"

        ax.scatter(n_majority, score, s=300, c=color, edgecolors="white",
                   linewidth=2, alpha=0.85, zorder=3)
        ax.annotate(ins["cell_id"], (n_majority, score),
                    xytext=(7, 7), textcoords="offset points", fontsize=9)

    # Quadrant lines
    ax.axhline(1.0, color="#c44", linestyle="--", alpha=0.4)
    ax.axhline(0.5, color="#c8a45c", linestyle="--", alpha=0.4)
    ax.axvline(3.5, color="#888", linestyle="--", alpha=0.4)

    # Quadrant labels
    ax.text(4.5, 1.5, "DANGER ZONE\nStrong consensus\nbut reasoning split",
            ha="center", va="center", fontsize=10, color=COLORS["flag"],
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=COLORS["flag"], alpha=0.85))
    ax.text(4.5, 0.2, "SAFE ZONE\nGenuine consensus",
            ha="center", va="center", fontsize=10, color=COLORS["good"],
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=COLORS["good"], alpha=0.85))
    ax.text(2, 1.5, "DISPERSED\nGenuine disagreement",
            ha="center", va="center", fontsize=10, color="#666",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor="#aaa", alpha=0.85))

    ax.set_xlabel("Agents in majority recommendation", fontsize=11)
    ax.set_ylabel("Reasoning diversity within consensus (RMSE)", fontsize=11)
    ax.set_title(
        "Cross-cell landscape\n"
        "Where do the cases sit on the consensus vs reasoning axes?",
        fontsize=12, color=COLORS["text"], pad=15
    )
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(-0.1, max(2.5, max([
        ins["hidden_disagreement"].get("reasoning_diversity_score", 0)
        for ins in all_insights if ins["hidden_disagreement"].get("status") == "computed"
    ], default=2.5) + 0.3))
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(out_path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close()

    n_total = len(all_insights)
    n_danger = sum(1 for ins in all_insights
                   if ins["consensus_map"].get("consensus_strength") == "strong"
                   and ins["hidden_disagreement"].get("reasoning_diversity_score", 0) > 1.0)
    n_safe = sum(1 for ins in all_insights
                 if ins["consensus_map"].get("consensus_strength") == "strong"
                 and ins["hidden_disagreement"].get("reasoning_diversity_score", 0) < 0.5)

    interp = (
        f"## What this landscape shows\n\n"
        f"All {n_total} cells of the experiment plotted in two dimensions: "
        f"how many agents agreed on the recommendation (x-axis) and how much "
        f"their reasoning differed within that consensus (y-axis).\n\n"
        f"**The danger zone** (top-right) is the methodologically important "
        f"region: many agents agreed on the output, but their underlying "
        f"reasoning was substantially different. Standard ensemble methods "
        f"cannot detect this. {n_danger} of {n_total} cells fell into this zone.\n\n"
        f"**The safe zone** (bottom-right) is where consensus is genuine: "
        f"agents agreed on output AND reasoning. {n_safe} of {n_total} cells "
        f"fell here.\n\n"
        f"**Dispersed cases** (left half) had genuine disagreement at the "
        f"recommendation level. These are clearly hard decisions and the panel "
        f"says so honestly.\n"
    )
    return interp


# ============================================================
# Main entry point
# ============================================================
def process_cell(cell_id: str) -> None:
    cell = load_cell(cell_id)
    insight = load_insight(cell_id)
    if not cell or not insight:
        print(f"  {cell_id}: skipping (missing data)")
        return
    out_dir = ANALYSIS_DIR / cell_id
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"  {cell_id}: generating visualizations...")

    interp_network = plot_agreement_network(cell, insight, out_dir / "agreement_network.png")
    if interp_network:
        (out_dir / "agreement_network.interpretation.md").write_text(interp_network, encoding="utf-8")

    interp_heat = plot_disagreement_heatmap(cell, insight, out_dir / "disagreement_heatmap.png")
    if interp_heat:
        (out_dir / "disagreement_heatmap.interpretation.md").write_text(interp_heat, encoding="utf-8")

    interp_biplot = plot_annotated_biplot(cell, insight, out_dir / "biplot_annotated.png")
    if interp_biplot:
        (out_dir / "biplot_annotated.interpretation.md").write_text(interp_biplot, encoding="utf-8")

    interp_split = plot_consensus_split(cell, insight, out_dir / "consensus_vs_reasoning.png")
    if interp_split:
        (out_dir / "consensus_vs_reasoning.interpretation.md").write_text(interp_split, encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--cell", default=None)
    args = p.parse_args()

    ANALYSIS_DIR.mkdir(exist_ok=True)

    if args.cell:
        process_cell(args.cell)
    else:
        for d in sorted(OPERATOR_DIR.iterdir() if OPERATOR_DIR.exists() else []):
            if d.is_dir() and (d / "operator_insight.json").exists():
                process_cell(d.name)
    cross_cell_dir = ANALYSIS_DIR / "cross_cell"
    cross_cell_dir.mkdir(parents=True, exist_ok=True)
    plot_cross_cell_landscape(cross_cell_dir / "landscape.png")
    print("Done. See analysis/")


if __name__ == "__main__":
    main()
