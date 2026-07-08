#!/usr/bin/env python3
"""
Operator synthesis - turns raw experimental data into human-readable insights.

For each completed cell, produces an `operator_insight.json` with:
- consensus_map: what each agent recommended, distribution
- hidden_disagreement: agents converging on the same recommendation via
  different constructs (the headline interpretability signal)
- blind_spots: dimensions weakly explored in the construct space
- risk_surface: distinct risks raised by minority agents that consensus dilutes
- operator_questions: questions to ask before acting on the consensus

This module makes ZERO additional API calls. It is pure post-processing.

Run:
    python operator_synthesis.py                  # process all complete cells
    python operator_synthesis.py --cell B_P_run1  # one cell only
"""
from __future__ import annotations
import argparse
import json
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from statistics import mean, stdev

import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from scipy.stats import pearsonr
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

RESULTS_DIR = Path("./results")
OPERATOR_DIR = Path("./operator_outputs")


def load_cell(cell_id: str) -> dict | None:
    p = RESULTS_DIR / cell_id / "cell.json"
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_recommendation(response_text: str, n_options: int = 5) -> str | None:
    """Heuristic: find which option (A/B/C/D/E) the response recommends."""
    if not response_text:
        return None
    # Look for "recommend Option X" / "I recommend X" patterns
    patterns = [
        r"recommend(?:s|ed|ing)?\s+(?:[Oo]ption\s+)?([A-E])\b",
        r"choose(?:s|d)?\s+(?:[Oo]ption\s+)?([A-E])\b",
        r"[Oo]ption\s+([A-E])\s+is\s+(?:the\s+)?(?:best|right|correct|appropriate)",
        # "Option E - leadership ... - is the contrarian pick"
        r"[Oo]ption\s+([A-E])\s+[-\u2013\u2014][^.]*?(?:is\s+(?:the\s+)?(?:contrarian|right|best|correct|primary|main)\s+(?:pick|choice|answer|recommendation))",
        # "Option C, but..." or "Option C." at start of paragraph (advocacy)
        r"^[Oo]ption\s+([A-E])[\s,\.]",
        r"\n[Oo]ption\s+([A-E])[\s,\.]",
        # "I would pick/select/go with X"
        r"(?:would|will)\s+(?:pick|select|go\s+with|choose)\s+(?:[Oo]ption\s+)?([A-E])\b",
        # "My pick/choice is X"
        r"[Mm]y\s+(?:pick|choice|recommendation|answer)\s+is\s+(?:[Oo]ption\s+)?([A-E])\b",
        r"primary\s+(?:choice|pick|recommendation).*?[Oo]ption\s+([A-E])",
    ]
    for pat in patterns:
        m = re.search(pat, response_text, re.MULTILINE)
        if m:
            return m.group(1).upper()
    # Fallback: count mentions, take most-emphasized
    counts = Counter()
    for letter in "ABCDE":
        for pat in [rf"\b[Oo]ption\s+{letter}\b", rf"\b{letter}\.\s"]:
            counts[letter] += len(re.findall(pat, response_text))
    if counts:
        top = counts.most_common(1)[0]
        if top[1] >= 2:
            return top[0]
    return None


def build_rating_matrix(cell: dict) -> tuple[np.ndarray, list, list, list]:
    """Return (mean_matrix[elem,construct], elements, constructs, raters)."""
    all_constructs = []
    for sn in sorted(cell.get("constructs", {}).keys()):
        all_constructs.extend(cell["constructs"][sn])
    construct_ids = [c["id"] for c in all_constructs]
    construct_meta = {c["id"]: c for c in all_constructs}
    elements = sorted(cell.get("element_summaries", {}).keys())
    raters = sorted(cell.get("ratings", {}).keys())
    if not (construct_ids and elements and raters):
        return np.array([]), [], [], []
    # Build (rater, element, construct) tensor; mean across raters -> (elem, construct)
    mat = np.full((len(elements), len(construct_ids)), np.nan)
    counts = np.zeros_like(mat)
    for r_sn, r_data in cell.get("ratings", {}).items():
        for cid, elem_ratings in r_data.items():
            if cid not in construct_ids:
                continue
            j = construct_ids.index(cid)
            for ek, val in elem_ratings.items():
                if ek in elements:
                    i = elements.index(ek)
                    mat[i, j] = (
                        val if np.isnan(mat[i, j])
                        else mat[i, j] + val
                    )
                    counts[i, j] += 1
    # Average
    with np.errstate(invalid="ignore"):
        mean_mat = np.where(counts > 0, mat / np.maximum(counts, 1), np.nan)
    return mean_mat, elements, construct_ids, raters


def synthesize_consensus_map(cell: dict) -> dict:
    """Who recommended what, plus 1-sentence rationale per recommendation."""
    mapping = cell.get("element_mapping", {})  # {E1: M1, ...}
    inv_map = {v: k for k, v in mapping.items()}  # {M1: E1, ...}
    free_responses = cell.get("free_responses", {})

    recommendations = {}
    persona_for_model = {}
    for call in cell.get("api_calls", []):
        if call["phase"] == "phase1_freeresponse":
            persona_for_model[call["model_short_name"]] = call["persona_or_neutral"]

    for sn, text in free_responses.items():
        rec = extract_recommendation(text)
        recommendations[sn] = {
            "model_id": next(
                (c["model_id_used"] for c in cell.get("api_calls", [])
                 if c["phase"] == "phase1_freeresponse" and c["model_short_name"] == sn),
                "unknown",
            ),
            "persona": persona_for_model.get(sn, "neutral"),
            "recommendation": rec,
            "element_label": inv_map.get(sn),
            "rationale_snippet": (text or "").strip().split("\n\n")[0][:300],
        }

    # Distribution
    dist = Counter([r["recommendation"] for r in recommendations.values() if r["recommendation"]])

    return {
        "by_agent": recommendations,
        "distribution": dict(dist),
        "n_agents": len(recommendations),
        "consensus_strength": (
            "strong" if dist and dist.most_common(1)[0][1] >= 4
            else "partial" if dist and dist.most_common(1)[0][1] == 3
            else "split"
        ),
        "majority_recommendation": (
            dist.most_common(1)[0][0] if dist and dist.most_common(1)[0][1] >= 3
            else None
        ),
    }


def detect_hidden_disagreement(cell: dict, consensus: dict) -> dict:
    """
    Headline finding: agents who recommended the SAME option but are placed in
    DIFFERENT regions of construct space. This is what standard MoA aggregation
    cannot detect.

    Returns: {majority_option, agents_in_consensus, pairwise_distances_in_pc_space,
              max_distance, reasoning_diversity_score, interpretation}
    """
    mean_mat, elements, constructs, raters = build_rating_matrix(cell)
    if mean_mat.size == 0 or mean_mat.shape[0] < 3:
        return {"status": "insufficient_data"}

    # Find agents in the majority consensus
    by_agent = consensus["by_agent"]
    majority = consensus["majority_recommendation"]
    if not majority:
        return {
            "status": "no_majority",
            "interpretation": "Agents split across recommendations; no hidden-consensus to expose.",
        }
    in_consensus = [
        sn for sn, r in by_agent.items()
        if r["recommendation"] == majority
    ]
    if len(in_consensus) < 2:
        return {"status": "majority_too_small"}

    # Get each agent's rating vector across all constructs (their "reasoning fingerprint")
    elem_labels = elements
    agent_vectors = {}
    for sn in in_consensus:
        if sn not in cell.get("ratings", {}):
            continue
        ratings = cell["ratings"][sn]
        # Flatten ratings into a vector in (construct, element) order
        vec = []
        for cid in constructs:
            for ek in elem_labels:
                v = ratings.get(cid, {}).get(ek)
                vec.append(v if v is not None else np.nan)
        agent_vectors[sn] = np.array(vec, dtype=float)

    if len(agent_vectors) < 2:
        return {"status": "no_overlapping_ratings"}

    # Pairwise distances between rating fingerprints, ignoring NaNs
    distances = {}
    for a, b in combinations(sorted(agent_vectors.keys()), 2):
        va, vb = agent_vectors[a], agent_vectors[b]
        mask = ~(np.isnan(va) | np.isnan(vb))
        if mask.sum() < 5:
            continue
        d = float(np.sqrt(np.mean((va[mask] - vb[mask]) ** 2)))
        distances[f"{a}_vs_{b}"] = d

    max_d = max(distances.values()) if distances else 0.0
    mean_d = mean(distances.values()) if distances else 0.0

    # Score: how much the agents who agree on output disagree on reasoning
    # Scale: 0 = identical reasoning, 2+ = substantially different
    reasoning_diversity = mean_d

    if reasoning_diversity > 1.0:
        interpretation = (
            f"FLAG: {len(in_consensus)} agents recommended option {majority}, "
            f"but their underlying reasoning differs substantially (mean RMSE in "
            f"rating space = {reasoning_diversity:.2f} on a 1-7 scale). "
            f"Standard ensemble aggregation would report 'strong consensus' here; "
            f"this is hidden disagreement that may surface as execution conflicts."
        )
    elif reasoning_diversity > 0.5:
        interpretation = (
            f"Moderate hidden disagreement: {len(in_consensus)} agents recommended "
            f"option {majority} but differ on framing (mean RMSE = "
            f"{reasoning_diversity:.2f}). Worth probing what each is emphasizing."
        )
    else:
        interpretation = (
            f"Low hidden disagreement: {len(in_consensus)} agents recommended option "
            f"{majority} and their reasoning is correspondingly aligned "
            f"(mean RMSE = {reasoning_diversity:.2f}). Genuine consensus."
        )

    return {
        "status": "computed",
        "majority_option": majority,
        "agents_in_consensus": in_consensus,
        "n_in_consensus": len(in_consensus),
        "pairwise_distances": distances,
        "max_distance": max_d,
        "mean_distance": mean_d,
        "reasoning_diversity_score": reasoning_diversity,
        "interpretation": interpretation,
    }


def detect_blind_spots(cell: dict) -> dict:
    """
    Blind spots = (a) constructs that all agents rated near the middle (4) -
    no element discriminates on this dimension, suggesting agents collectively
    underweighted it; and (b) PCA components that capture small variance
    despite being orthogonal to main axes - undeveloped dimensions of the
    problem space.
    """
    mean_mat, elements, constructs, raters = build_rating_matrix(cell)
    if mean_mat.size == 0:
        return {"status": "insufficient_data"}

    candidates = []
    for j, cid in enumerate(constructs):
        col = mean_mat[:, j]
        col = col[~np.isnan(col)]
        if len(col) < 3:
            continue
        col_mean = float(np.mean(col))
        col_std = float(np.std(col, ddof=0))
        # Low discrimination + mid-scale = blind spot
        if col_std < 1.0 and 3.0 <= col_mean <= 5.0:
            construct_meta = None
            for sn, items in cell.get("constructs", {}).items():
                for item in items:
                    if item["id"] == cid:
                        construct_meta = item
                        break
            candidates.append({
                "construct_id": cid,
                "left_pole": construct_meta["left"] if construct_meta else None,
                "right_pole": construct_meta["right"] if construct_meta else None,
                "mean_rating": col_mean,
                "rating_std": col_std,
                "interpretation": (
                    f"All options score near the middle on this axis "
                    f"({construct_meta['left']} <-> {construct_meta['right']}). "
                    f"Either none of the options addresses this dimension, "
                    f"or agents collectively underweighted it. Worth probing "
                    f"explicitly: does any option strongly hit one pole here?"
                ) if construct_meta else None,
            })

    # PCA: look at the 3rd+ components - if they capture meaningful variance
    # (say > 5%) and aren't well-aligned with the strong axes, they hint at
    # under-explored dimensions
    underexplored_dims = []
    valid_mask = ~np.isnan(mean_mat).any(axis=0)
    if valid_mask.sum() >= 3 and mean_mat.shape[0] >= 3:
        clean = mean_mat[:, valid_mask]
        try:
            n_comp = min(4, clean.shape[0] - 1, clean.shape[1])
            pca = PCA(n_components=n_comp)
            pca.fit(clean)
            for i in range(2, n_comp):
                if pca.explained_variance_ratio_[i] > 0.05:
                    # Find top-loading construct on this component
                    loadings = pca.components_[i]
                    top_idx = int(np.argmax(np.abs(loadings)))
                    cid = [c for c, m in zip(constructs, valid_mask) if m][top_idx]
                    underexplored_dims.append({
                        "pc_index": i + 1,
                        "variance_explained": float(pca.explained_variance_ratio_[i]),
                        "top_construct_id": cid,
                    })
        except Exception:
            pass

    return {
        "status": "computed",
        "low_discrimination_constructs": candidates,
        "underexplored_components": underexplored_dims,
        "summary": (
            f"{len(candidates)} construct(s) where agents agreed all options are "
            f"middling - candidate blind spots to probe."
            if candidates else "No obvious blind spots detected in construct space."
        ),
    }


def map_risk_surface(cell: dict, consensus: dict) -> dict:
    """
    Look for risk/concern keywords in free responses. Minority risks are
    those raised by 1-2 agents (likely diluted by aggregation).
    """
    risk_patterns = [
        r"risk[s]?\s+(?:of|that|is|are)?\s*([^\.]+)",
        r"concern[s]?\s+(?:about|that|is|are)?\s*([^\.]+)",
        r"danger\s+(?:of|that)?\s*([^\.]+)",
        r"failure\s+mode[s]?\s*[:\-]?\s*([^\.]+)",
        r"watch\s+(?:out\s+)?for\s+([^\.]+)",
        r"may\s+fail\s+(?:if|when|because)\s+([^\.]+)",
        r"could\s+go\s+wrong\s+(?:if|when|because)?\s*([^\.]+)",
        r"what\s+if\s+([^\.]+)",
    ]
    risks_by_agent = {}
    for sn, text in cell.get("free_responses", {}).items():
        # Skip agents whose response was None/empty (model returned no content)
        if not isinstance(text, str) or not text.strip():
            risks_by_agent[sn] = []
            continue
        risks = []
        for pat in risk_patterns:
            for m in re.finditer(pat, text, re.IGNORECASE):
                snippet = m.group(1).strip()[:200]
                if 10 < len(snippet) < 200:
                    risks.append(snippet)
        risks_by_agent[sn] = list(dict.fromkeys(risks))[:5]  # dedupe, top 5

    # Risks raised by minority (1-2 agents)
    all_risks_flat = []
    for sn, rs in risks_by_agent.items():
        for r in rs:
            all_risks_flat.append((sn, r))

    return {
        "status": "computed",
        "risks_by_agent": risks_by_agent,
        "total_risks_raised": sum(len(rs) for rs in risks_by_agent.values()),
        "agents_raising_risks": sum(1 for rs in risks_by_agent.values() if rs),
        "note": (
            "Risks listed here were extracted by pattern matching on agent free "
            "responses. They are minority signals worth probing before acting on "
            "consensus."
        ),
    }


def generate_operator_questions(cell: dict, consensus: dict,
                                hidden: dict, blind: dict) -> list[str]:
    """Generate 5-10 questions an operator should ask before acting."""
    qs = []
    by_agent = consensus["by_agent"]

    # Q1: was there hidden disagreement?
    if hidden.get("status") == "computed":
        score = hidden.get("reasoning_diversity_score", 0)
        if score > 0.5:
            in_consensus = hidden["agents_in_consensus"]
            framings = []
            for sn in in_consensus:
                p = by_agent.get(sn, {}).get("persona", "?")
                framings.append(f"{sn} ({p})")
            qs.append(
                f"Agents {', '.join(framings)} agreed on option "
                f"{hidden['majority_option']} - but their reasoning differs "
                f"(diversity={score:.2f}). Which framing will drive execution? "
                f"Different framings will produce different execution paths."
            )

    # Q2: blind spots
    if blind.get("low_discrimination_constructs"):
        for c in blind["low_discrimination_constructs"][:2]:
            qs.append(
                f"All options scored near the middle on the axis '{c['left_pole']}' "
                f"vs '{c['right_pole']}'. Does any option deserve a strong "
                f"position here? If not, is this a dimension being underweighted?"
            )

    # Q3: minority recommendations
    dist = consensus.get("distribution", {})
    if dist:
        majority = consensus.get("majority_recommendation")
        for opt, n in dist.items():
            if opt != majority and n == 1:
                # Find who recommended it
                minority_sn = next(
                    (sn for sn, r in by_agent.items() if r["recommendation"] == opt),
                    None,
                )
                if minority_sn:
                    persona = by_agent[minority_sn].get("persona", "?")
                    qs.append(
                        f"Option {opt} was recommended only by {minority_sn} "
                        f"({persona}). What does this agent see that others "
                        f"missed - or what is it weighing differently?"
                    )

    # Q4: contrarian preservation
    contrarian_sn = next(
        (sn for sn, r in by_agent.items() if r.get("persona") == "C"),
        None,
    )
    if contrarian_sn and by_agent[contrarian_sn].get("recommendation"):
        contr_opt = by_agent[contrarian_sn]["recommendation"]
        majority = consensus.get("majority_recommendation")
        if contr_opt != majority:
            qs.append(
                f"The contrarian agent recommended {contr_opt} against the "
                f"majority. Contrarian disagreement is a useful signal: what is "
                f"the strongest argument against the majority choice that "
                f"hasn't been answered?"
            )

    # Q5: meta - is this a real consensus or theatrical?
    if consensus.get("consensus_strength") == "strong":
        qs.append(
            "Consensus is strong (4-5 agents agree). Is this because the "
            "answer is genuinely obvious, or because agents share a common "
            "training distribution? If you cannot articulate why the OTHER "
            "options were rejected, the consensus may be inherited, not earned."
        )

    return qs[:8]


def run_synthesis(cell_id: str, cell: dict) -> dict:
    consensus = synthesize_consensus_map(cell)
    hidden = detect_hidden_disagreement(cell, consensus)
    blind = detect_blind_spots(cell)
    risks = map_risk_surface(cell, consensus)
    questions = generate_operator_questions(cell, consensus, hidden, blind)

    return {
        "cell_id": cell_id,
        "task": cell.get("task"),
        "condition": cell.get("condition"),
        "run_idx": cell.get("run_idx"),
        "consensus_map": consensus,
        "hidden_disagreement": hidden,
        "blind_spots": blind,
        "risk_surface": risks,
        "operator_questions": questions,
        "headline": _make_headline(consensus, hidden, blind),
    }


def _make_headline(consensus: dict, hidden: dict, blind: dict) -> str:
    """One-sentence summary fit for a Slack message or dashboard tile."""
    n_total = consensus.get("n_agents", 0)
    strength = consensus.get("consensus_strength")
    majority = consensus.get("majority_recommendation")
    dist = consensus.get("distribution", {})
    n_in_majority = dist.get(majority, 0) if majority else 0
    n_dissenting = n_total - n_in_majority
    score = hidden.get("reasoning_diversity_score", 0) if hidden.get("status") == "computed" else 0

    if strength == "strong" and score > 1.0:
        return (
            f"{n_in_majority}/{n_total} agents recommended option {majority}, "
            f"but with substantially different reasoning (RMSE={score:.2f}). "
            f"Reported consensus hides actionable disagreement."
        )
    if strength == "strong" and 0.5 < score <= 1.0:
        return (
            f"{n_in_majority}/{n_total} agents recommended option {majority} "
            f"with moderately different framings (RMSE={score:.2f}). "
            f"Worth probing what each is emphasizing."
        )
    if strength == "strong":
        if n_dissenting > 0:
            return (
                f"{n_in_majority}/{n_total} agents converged on option {majority} "
                f"with aligned reasoning. {n_dissenting} dissenter(s) - examine the minority view."
            )
        return f"All {n_total} agents converged on option {majority} with aligned reasoning."
    if strength == "partial":
        return (
            f"Partial consensus on option {majority} ({n_in_majority}/{n_total}); "
            f"remaining agents split. Worth probing the dissent before acting."
        )
    if strength == "split":
        return f"Agents are split across options; no clear consensus to act on."
    return "Analysis incomplete."


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--cell", default=None)
    args = p.parse_args()

    OPERATOR_DIR.mkdir(exist_ok=True)

    cell_ids = []
    if args.cell:
        cell_ids = [args.cell]
    else:
        for d in sorted(RESULTS_DIR.iterdir()):
            if d.is_dir() and (d / "cell.json").exists():
                cell_ids.append(d.name)

    if not cell_ids:
        print(f"No cells found in {RESULTS_DIR}/")
        return 1

    all_insights = []
    for cid in cell_ids:
        cell = load_cell(cid)
        if not cell:
            continue
        if not cell.get("status", "").startswith("complete"):
            print(f"  {cid}: skipping (status={cell.get('status')})")
            continue
        print(f"Synthesizing {cid}...")
        insight = run_synthesis(cid, cell)
        out_dir = OPERATOR_DIR / cid
        out_dir.mkdir(exist_ok=True)
        with open(out_dir / "operator_insight.json", "w", encoding="utf-8") as f:
            json.dump(insight, f, indent=2, ensure_ascii=False)
        print(f"  -> {insight['headline']}")
        all_insights.append(insight)

    # Cross-cell summary
    with open(OPERATOR_DIR / "all_insights.json", "w", encoding="utf-8") as f:
        json.dump(all_insights, f, indent=2, ensure_ascii=False)

    print(f"Wrote operator insights for {len(all_insights)} cells to {OPERATOR_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
