"""
Phase 2L · Analysis pipeline.

Computes Cross-Model Repertory Grid metrics from Phase 4 ratings:
  - Tier hypothesis: cheap vs mid vs flagship differences
  - Inter-rater correlations: how similarly raters score the same content
  - Family clustering: which providers cluster together
  - Calibration offsets: per-model rating tendencies
  - Persona volatility: rating SD under neutral vs persona conditions
  - Divergence Index: which models are outliers
  - Construct consensus: most agreed-upon dimensions

Outputs:
  - results_phase2l/analysis_results.json   (machine-readable metrics)
  - results_phase2l/analysis_summary.md      (human-readable summary)
  - results_phase2l/report_phase2l.html      (interactive visual report)

Cost: $0 (pure local computation).
Usage: python analyze_phase2l.py
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

RESULTS_DIR = Path("./results_phase2l")
PHASE4_DIR = RESULTS_DIR / "phase4_ratings"
PHASE3_DIR = RESULTS_DIR / "phase3_constructs"
PHASE1_DIR = RESULTS_DIR / "phase1_free_response"

# Model metadata - mirrors config_phase2l.yaml
MODEL_META = {
    "A_C": {"family": "anthropic", "tier": "cheap",    "name": "Claude Haiku 4.5"},
    "A_M": {"family": "anthropic", "tier": "mid",      "name": "Claude Sonnet 4.6"},
    "A_F": {"family": "anthropic", "tier": "flagship", "name": "Claude Opus 4.8"},
    "O_C": {"family": "openai",    "tier": "cheap",    "name": "GPT-5 mini"},
    "O_M": {"family": "openai",    "tier": "mid",      "name": "GPT-5.4"},
    "O_F": {"family": "openai",    "tier": "flagship", "name": "GPT-5.5"},
    "G_C": {"family": "google",    "tier": "cheap",    "name": "Gemini 2.5 Flash Lite"},
    "G_M": {"family": "google",    "tier": "mid",      "name": "Gemini 3 Flash"},
    "G_F": {"family": "google",    "tier": "flagship", "name": "Gemini 3.1 Pro"},
    "M_C": {"family": "mistral",   "tier": "cheap",    "name": "Ministral 3B"},
    "M_M": {"family": "mistral",   "tier": "mid",      "name": "Mistral Small 4"},
    "M_F": {"family": "mistral",   "tier": "flagship", "name": "Mistral Medium 3.5"},
    "D_C": {"family": "deepseek",  "tier": "cheap",    "name": "DeepSeek V4 Flash"},
    "D_M": {"family": "deepseek",  "tier": "mid",      "name": "DeepSeek V3.1"},
    "D_F": {"family": "deepseek",  "tier": "flagship", "name": "DeepSeek R1"},
    "X_C": {"family": "xai",       "tier": "cheap",    "name": "Grok Build 0.1"},
    "X_M": {"family": "xai",       "tier": "mid",      "name": "Grok 4.3"},
    "X_F": {"family": "xai",       "tier": "flagship", "name": "Grok 4.20 Multi-agent"},
    "Q_C": {"family": "qwen",      "tier": "cheap",    "name": "Qwen 2.5 7B"},
    "Q_M": {"family": "qwen",      "tier": "mid",      "name": "Qwen Plus"},
    "Q_F": {"family": "qwen",      "tier": "flagship", "name": "Qwen 3.7 Max"},
    "K_C": {"family": "moonshot",  "tier": "cheap",    "name": "Kimi K2.5"},
    "K_M": {"family": "moonshot",  "tier": "mid",      "name": "Kimi K2 Thinking"},
    "K_F": {"family": "moonshot",  "tier": "flagship", "name": "Kimi K2.6"},
    "Z_C": {"family": "zhipu",     "tier": "cheap",    "name": "GLM 4.7 Flash"},
    "Z_M": {"family": "zhipu",     "tier": "mid",      "name": "GLM 4.5 Air"},
    "Z_F": {"family": "zhipu",     "tier": "flagship", "name": "GLM 5.1"},
    "N_C": {"family": "nvidia",    "tier": "cheap",    "name": "Nemotron Nano 9B"},
    "N_M": {"family": "nvidia",    "tier": "mid",      "name": "Nemotron Super 49B"},
    "N_F": {"family": "nvidia",    "tier": "flagship", "name": "Nemotron Ultra 550B"},
    "L_C": {"family": "meta",      "tier": "cheap",    "name": "Llama 4 Scout"},
    "L_M": {"family": "meta",      "tier": "mid",      "name": "Llama 3.3 70B"},
    "L_F": {"family": "meta",      "tier": "flagship", "name": "Llama 4 Maverick"},
    "C_C": {"family": "cohere",    "tier": "cheap",    "name": "Command R7B"},
    "C_M": {"family": "cohere",    "tier": "mid",      "name": "Command R"},
    "C_F": {"family": "cohere",    "tier": "flagship", "name": "Command A"},
}

ORDERED_SHORTS = list(MODEL_META.keys())

TASK_NAMES = {
    "K": "M&A under regulatory uncertainty",
    "L": "Family business succession",
    "M": "Pandemic response strategy",
    "N_task": "R&D portfolio allocation",
    "O": "Crisis communication post-breach",
    "P": "Constitutional reform proposal",
    "Q": "Cross-jurisdiction AI regulation",
}


# ============================================================================
# Data loading
# ============================================================================

def load_phase4_ratings() -> list[dict]:
    """Load all Phase 4 cells, return list of cell records with parsed ratings."""
    cells = []
    if not PHASE4_DIR.exists():
        return cells
    for cell_path in PHASE4_DIR.rglob("*.json"):
        if "_backups" in cell_path.parts:
            continue
        try:
            d = json.loads(cell_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if d.get("ok_batches", 0) == 0:
            continue
        cells.append(d)
    return cells


def build_long_format(cells: list[dict]) -> list[dict]:
    """Build (task, cond, rater, ratee, construct_idx, rating) records."""
    records = []
    for c in cells:
        rater = c.get("rater_short")
        if not rater or rater not in MODEL_META:
            continue
        task = c.get("task")
        cond = c.get("condition")
        rated_responses = c.get("rated_responses") or []
        for batch in c.get("batches", []) or []:
            if batch.get("parse_error"):
                continue
            ratings = batch.get("ratings") or []
            constructs = batch.get("constructs") or []
            batch_idx = batch.get("batch", 0)
            for response_idx, rating_row in enumerate(ratings):
                if response_idx >= len(rated_responses):
                    continue
                ratee = rated_responses[response_idx]
                if not isinstance(rating_row, list):
                    continue
                for construct_idx, rating in enumerate(rating_row):
                    if construct_idx >= len(constructs):
                        continue
                    if not isinstance(rating, (int, float)):
                        continue
                    r = int(rating)
                    if r < 1 or r > 7:
                        continue
                    construct = constructs[construct_idx]
                    records.append({
                        "task": task,
                        "cond": cond,
                        "rater": rater,
                        "ratee": ratee,
                        "batch": batch_idx,
                        "construct_local_idx": construct_idx,
                        "pole_a": construct.get("pole_a", ""),
                        "pole_b": construct.get("pole_b", ""),
                        "rating": r,
                    })
    return records


# ============================================================================
# Statistics utilities
# ============================================================================

def pearson(x: list[float], y: list[float]) -> float | None:
    """Pearson correlation between two equal-length sequences."""
    if len(x) != len(y) or len(x) < 3:
        return None
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    sx2 = sum((xi - mx) ** 2 for xi in x)
    sy2 = sum((yi - my) ** 2 for yi in y)
    den = math.sqrt(sx2 * sy2)
    if den == 0:
        return None
    return num / den


def safe_mean(xs: list[float]) -> float | None:
    return statistics.mean(xs) if xs else None


def safe_sd(xs: list[float]) -> float | None:
    return statistics.stdev(xs) if len(xs) >= 2 else None


# ============================================================================
# Aggregations
# ============================================================================

def aggregate_rater_ratee_means(records: list[dict]) -> dict:
    """For each (task, cond, rater, ratee), compute mean rating across all constructs.

    Returns nested dict: {(task, cond): {(rater, ratee): mean_rating}}
    """
    grouped = defaultdict(lambda: defaultdict(list))
    for r in records:
        key = (r["task"], r["cond"])
        grouped[key][(r["rater"], r["ratee"])].append(r["rating"])
    result = {}
    for key, pair_dict in grouped.items():
        result[key] = {pair: statistics.mean(vals) for pair, vals in pair_dict.items()}
    return result


def compute_tier_summary(rater_ratee_means: dict) -> dict:
    """For each (task, cond), summarize ratings by tier of rater AND ratee.

    Returns: {(task, cond): {(rater_tier, ratee_tier): mean_rating}}
    """
    out = {}
    for key, pair_means in rater_ratee_means.items():
        tier_buckets = defaultdict(list)
        for (rater, ratee), mean_rating in pair_means.items():
            rt = MODEL_META.get(rater, {}).get("tier")
            et = MODEL_META.get(ratee, {}).get("tier")
            if rt and et:
                tier_buckets[(rt, et)].append(mean_rating)
        out[key] = {f"{rt}_rates_{et}": statistics.mean(vals)
                    for (rt, et), vals in tier_buckets.items() if vals}
    return out


def compute_inter_rater_correlations(rater_ratee_means: dict) -> dict:
    """For each (task, cond), compute pairwise Pearson correlations between raters.

    Each rater's "profile" is their mean rating across all 36 ratees.
    Returns: {(task, cond): {(raterA, raterB): correlation}}
    """
    out = {}
    for key, pair_means in rater_ratee_means.items():
        # Build profile per rater
        rater_profiles = defaultdict(dict)
        for (rater, ratee), mean_rating in pair_means.items():
            rater_profiles[rater][ratee] = mean_rating
        # Compute pairwise correlations
        raters = sorted(rater_profiles.keys())
        corrs = {}
        for i, r1 in enumerate(raters):
            for r2 in raters[i:]:
                if r1 == r2:
                    corrs[(r1, r2)] = 1.0
                    continue
                common_ratees = set(rater_profiles[r1].keys()) & set(rater_profiles[r2].keys())
                if len(common_ratees) < 5:
                    continue
                x = [rater_profiles[r1][ra] for ra in sorted(common_ratees)]
                y = [rater_profiles[r2][ra] for ra in sorted(common_ratees)]
                c = pearson(x, y)
                if c is not None:
                    corrs[(r1, r2)] = c
                    corrs[(r2, r1)] = c
        out[key] = corrs
    return out


def compute_calibration_offsets(records: list[dict]) -> dict:
    """Per (task, cond, rater): mean of all their ratings minus grand mean.

    A positive offset = rater tends to give high ratings; negative = low.
    """
    grand_means = {}
    rater_means = defaultdict(list)
    grouped = defaultdict(list)
    for r in records:
        key = (r["task"], r["cond"])
        grouped[key].append(r["rating"])
        rater_means[(key, r["rater"])].append(r["rating"])
    out = defaultdict(dict)
    for key, all_ratings in grouped.items():
        grand = statistics.mean(all_ratings)
        grand_means[key] = grand
    for (key, rater), ratings in rater_means.items():
        out[key][rater] = {
            "mean": statistics.mean(ratings),
            "offset": statistics.mean(ratings) - grand_means[key],
            "sd": safe_sd(ratings),
            "n": len(ratings),
        }
    return out


def compute_persona_volatility(records: list[dict]) -> dict:
    """Compare each model's rating SD under neutral (N) vs persona (P).

    High volatility under P = model is sensitive to persona prompt.
    """
    by_task_model_cond = defaultdict(list)
    for r in records:
        by_task_model_cond[(r["task"], r["rater"], r["cond"])].append(r["rating"])
    out = defaultdict(dict)
    for (task, rater, cond), ratings in by_task_model_cond.items():
        sd = safe_sd(ratings)
        if sd is None:
            continue
        out[task].setdefault(rater, {})[cond] = sd
    return out


def compute_family_clustering(rater_ratee_means: dict) -> dict:
    """For each (task, cond), compute mean rating profile per family.

    Returns: {(task, cond): {family: avg_profile_per_ratee}}
    """
    out = {}
    for key, pair_means in rater_ratee_means.items():
        family_profiles = defaultdict(lambda: defaultdict(list))
        for (rater, ratee), mean_rating in pair_means.items():
            fam = MODEL_META.get(rater, {}).get("family")
            if fam:
                family_profiles[fam][ratee].append(mean_rating)
        out[key] = {fam: {ratee: statistics.mean(vs) for ratee, vs in ratees.items()}
                    for fam, ratees in family_profiles.items()}
    return out


def compute_divergence_index(corrs_by_key: dict) -> dict:
    """For each (task, cond, rater): mean correlation with all other raters.

    Low value = rater diverges from consensus.
    """
    out = defaultdict(dict)
    for key, corrs in corrs_by_key.items():
        raters_in_key = set(r for pair in corrs.keys() for r in pair)
        for rater in raters_in_key:
            others = []
            for other in raters_in_key:
                if other == rater:
                    continue
                c = corrs.get((rater, other))
                if c is not None:
                    others.append(c)
            if others:
                out[key][rater] = {
                    "mean_corr_others": statistics.mean(others),
                    "n_compared": len(others),
                }
    return out


# ============================================================================
# Coverage analysis
# ============================================================================

def compute_coverage(cells: list[dict]) -> dict:
    """How complete is the data per (task, cond, rater)?"""
    coverage = defaultdict(lambda: defaultdict(dict))
    for c in cells:
        task = c.get("task")
        cond = c.get("condition")
        rater = c.get("rater_short")
        ok = c.get("ok_batches", 0)
        n = c.get("n_batches", 0)
        coverage[task][cond][rater] = {
            "ok_batches": ok,
            "n_batches": n,
            "completion": (ok / n) if n else 0,
        }
    return coverage


# ============================================================================
# Main analysis
# ============================================================================

def run_analysis() -> dict:
    print("=" * 100)
    print(" Phase 2L Analysis Pipeline")
    print("=" * 100)

    print("\n1. Loading Phase 4 cells...")
    cells = load_phase4_ratings()
    print(f"   Loaded {len(cells)} cells with ok_batches >= 1.")

    print("\n2. Building long-format records...")
    records = build_long_format(cells)
    print(f"   Total ratings: {len(records):,}")
    if not records:
        print("ERROR: No valid records loaded. Cannot proceed.")
        return {}

    print("\n3. Aggregating rater × ratee mean ratings...")
    rater_ratee_means = aggregate_rater_ratee_means(records)
    print(f"   Aggregated for {len(rater_ratee_means)} (task, cond) combinations.")

    print("\n4. Computing tier summaries...")
    tier_summary = compute_tier_summary(rater_ratee_means)

    print("\n5. Computing inter-rater correlations...")
    corrs = compute_inter_rater_correlations(rater_ratee_means)

    print("\n6. Computing calibration offsets...")
    offsets = compute_calibration_offsets(records)

    print("\n7. Computing persona volatility...")
    volatility = compute_persona_volatility(records)

    print("\n8. Computing family clustering...")
    family_clustering = compute_family_clustering(rater_ratee_means)

    print("\n9. Computing divergence index...")
    divergence = compute_divergence_index(corrs)

    print("\n10. Computing coverage stats...")
    coverage = compute_coverage(cells)

    # Aggregate top-level stats
    n_unique_pairs = len({(r["task"], r["cond"], r["rater"], r["ratee"]) for r in records})
    n_unique_constructs = len({(r["task"], r["cond"], r["rater"], r["batch"], r["construct_local_idx"])
                                for r in records})

    # Tier hypothesis aggregate test - across ALL tasks/conds
    grand_tier_means = defaultdict(list)
    for key, ts in tier_summary.items():
        for tier_pair, mean_rating in ts.items():
            grand_tier_means[tier_pair].append(mean_rating)
    tier_overall = {tp: statistics.mean(vs) for tp, vs in grand_tier_means.items() if vs}

    # Inter-rater agreement - mean of all pairwise corrs across all (task, cond)
    all_corrs = []
    for key, corr_dict in corrs.items():
        for (r1, r2), c in corr_dict.items():
            if r1 != r2:
                all_corrs.append(c)
    mean_inter_rater_corr = safe_mean(all_corrs)
    median_inter_rater_corr = statistics.median(all_corrs) if all_corrs else None

    # Top divergent models
    div_overall = defaultdict(list)
    for key, rater_data in divergence.items():
        for rater, info in rater_data.items():
            div_overall[rater].append(info["mean_corr_others"])
    div_summary = {r: statistics.mean(vs) for r, vs in div_overall.items() if vs}
    most_divergent = sorted(div_summary.items(), key=lambda kv: kv[1])[:10]
    most_consensus = sorted(div_summary.items(), key=lambda kv: -kv[1])[:10]

    print("\n11. Summary statistics:")
    print(f"   Unique rater×ratee pairs: {n_unique_pairs:,}")
    print(f"   Unique constructs:        {n_unique_constructs:,}")
    print(f"   Mean inter-rater corr:    {mean_inter_rater_corr:.3f}" if mean_inter_rater_corr else "   No correlations.")
    print(f"   Median inter-rater corr:  {median_inter_rater_corr:.3f}" if median_inter_rater_corr else "")
    if tier_overall:
        print(f"\n   Tier-pair grand means:")
        for tp in sorted(tier_overall.keys()):
            print(f"     {tp:<28} {tier_overall[tp]:.3f}")

    print(f"\n   Most divergent raters (low avg corr with others):")
    for rater, score in most_divergent[:5]:
        name = MODEL_META.get(rater, {}).get("name", rater)
        print(f"     {rater:<6} {name:<35} {score:.3f}")
    print(f"\n   Most consensus raters (high avg corr with others):")
    for rater, score in most_consensus[:5]:
        name = MODEL_META.get(rater, {}).get("name", rater)
        print(f"     {rater:<6} {name:<35} {score:.3f}")

    return {
        "n_cells_loaded": len(cells),
        "n_ratings": len(records),
        "n_unique_pairs": n_unique_pairs,
        "n_unique_constructs": n_unique_constructs,
        "mean_inter_rater_corr": mean_inter_rater_corr,
        "median_inter_rater_corr": median_inter_rater_corr,
        "tier_overall": tier_overall,
        "tier_summary": {f"{k[0]}|{k[1]}": v for k, v in tier_summary.items()},
        "rater_ratee_means": {f"{k[0]}|{k[1]}": {f"{r}|{e}": v for (r, e), v in pm.items()}
                              for k, pm in rater_ratee_means.items()},
        "inter_rater_corrs": {f"{k[0]}|{k[1]}": {f"{r1}|{r2}": v for (r1, r2), v in cd.items()}
                              for k, cd in corrs.items()},
        "calibration_offsets": {f"{k[0]}|{k[1]}": v for k, v in offsets.items()},
        "persona_volatility": dict(volatility),
        "family_clustering": {f"{k[0]}|{k[1]}": v for k, v in family_clustering.items()},
        "divergence_index": {f"{k[0]}|{k[1]}": v for k, v in divergence.items()},
        "divergence_summary": div_summary,
        "most_divergent_raters": most_divergent,
        "most_consensus_raters": most_consensus,
        "coverage": dict(coverage),
        "model_meta": MODEL_META,
        "task_names": TASK_NAMES,
    }


def save_results(results: dict) -> None:
    """Save JSON + Markdown summary."""
    out_json = RESULTS_DIR / "analysis_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nSaved: {out_json}")

    # Markdown summary
    out_md = RESULTS_DIR / "analysis_summary.md"
    lines = []
    lines.append(f"# Phase 2L Analysis Summary\n")
    lines.append(f"## Overview\n")
    lines.append(f"- Cells loaded: **{results.get('n_cells_loaded', 0)}**")
    lines.append(f"- Total ratings: **{results.get('n_ratings', 0):,}**")
    lines.append(f"- Unique rater×ratee pairs: **{results.get('n_unique_pairs', 0):,}**")
    lines.append(f"- Unique constructs: **{results.get('n_unique_constructs', 0):,}**")
    mirc = results.get("mean_inter_rater_corr")
    if mirc is not None:
        lines.append(f"- Mean inter-rater correlation: **{mirc:.3f}**")
    miirc = results.get("median_inter_rater_corr")
    if miirc is not None:
        lines.append(f"- Median inter-rater correlation: **{miirc:.3f}**\n")

    lines.append("\n## Tier Hypothesis - grand means across all tasks\n")
    lines.append("| Rater tier rates → Ratee tier | Mean rating |")
    lines.append("|-------------------------------|-------------|")
    tier_overall = results.get("tier_overall", {})
    for tp in sorted(tier_overall.keys()):
        lines.append(f"| {tp.replace('_rates_', ' → ')} | {tier_overall[tp]:.3f} |")

    lines.append("\n## Most divergent raters\n")
    lines.append("| Short | Name | Avg correlation with others |")
    lines.append("|-------|------|------------------------------|")
    for rater, score in results.get("most_divergent_raters", [])[:10]:
        name = MODEL_META.get(rater, {}).get("name", rater)
        lines.append(f"| {rater} | {name} | {score:.3f} |")

    lines.append("\n## Most consensus raters\n")
    lines.append("| Short | Name | Avg correlation with others |")
    lines.append("|-------|------|------------------------------|")
    for rater, score in results.get("most_consensus_raters", [])[:10]:
        name = MODEL_META.get(rater, {}).get("name", rater)
        lines.append(f"| {rater} | {name} | {score:.3f} |")

    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Saved: {out_md}")


def generate_html_report(results: dict) -> None:
    """Generate interactive single-file HTML report with embedded data."""
    out_html = RESULTS_DIR / "report_phase2l.html"

    data_json = json.dumps(results, default=str, ensure_ascii=False)

    html = (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<title>Phase 2L · Cross-Model Repertory Grid Report</title>\n'
        '<style>\n'
        '  :root {\n'
        '    --bg: #0f1419; --panel: #1a2028; --border: #2a3441;\n'
        '    --text: #e6e6e6; --muted: #8a98a8;\n'
        '    --ok: #4ade80; --warn: #fbbf24; --err: #ef4444; --acc: #60a5fa;\n'
        '    --cheap: #7dd3fc; --mid: #a3e635; --flagship: #f9a8d4;\n'
        '  }\n'
        '  * { box-sizing: border-box; }\n'
        '  body { background: var(--bg); color: var(--text); font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 18px; max-width: 1400px; }\n'
        '  h1 { margin: 0 0 6px; font-size: 22px; }\n'
        '  h2 { margin: 24px 0 10px; font-size: 16px; color: var(--acc); text-transform: uppercase; letter-spacing: 0.5px; }\n'
        '  h3 { margin: 14px 0 8px; font-size: 14px; color: var(--muted); }\n'
        '  .subtitle { color: var(--muted); font-size: 13px; margin-bottom: 24px; }\n'
        '  .panel { background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 16px; }\n'
        '  .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }\n'
        '  .stat { background: #0a0e13; border: 1px solid var(--border); padding: 12px; border-radius: 6px; }\n'
        '  .stat .label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.5px; }\n'
        '  .stat .value { font-size: 22px; font-weight: 600; margin-top: 4px; color: var(--ok); }\n'
        '  .stat .sub { font-size: 11px; color: var(--muted); margin-top: 4px; }\n'
        '  table { width: 100%; border-collapse: collapse; font-size: 12px; }\n'
        '  th, td { text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--border); }\n'
        '  th { color: var(--muted); font-weight: normal; font-size: 11px; text-transform: uppercase; background: #0a0e13; }\n'
        '  .tier-cheap { color: var(--cheap); }\n'
        '  .tier-mid { color: var(--mid); }\n'
        '  .tier-flagship { color: var(--flagship); }\n'
        '  .heatmap-table { border-collapse: collapse; }\n'
        '  .heatmap-table td, .heatmap-table th { padding: 0 !important; border: 1px solid #0a0e13; }\n'
        '  .heatmap-cell { width: 28px; height: 22px; min-width: 28px; max-width: 28px; font-size: 9px; color: #000; text-align: center; line-height: 22px; font-family: SF Mono, monospace; }\n'
        '  .heatmap-rowhead, .heatmap-colhead { width: 32px; min-width: 32px; max-width: 32px; height: 22px; padding: 0 4px !important; font-size: 9px; color: var(--muted); text-align: center; background: #0a0e13; }\n'
        '  .tabs { display: flex; gap: 4px; margin-bottom: 12px; flex-wrap: wrap; }\n'
        '  .tab { padding: 6px 14px; background: #0a0e13; border: 1px solid var(--border); border-radius: 4px; cursor: pointer; font-size: 12px; }\n'
        '  .tab.active { background: var(--acc); color: #000; }\n'
        '  .bar { display: inline-block; height: 12px; background: var(--acc); border-radius: 2px; }\n'
        '  .bar-bg { display: inline-block; width: 100px; height: 12px; background: #0a0e13; border-radius: 2px; vertical-align: middle; }\n'
        '  .legend { font-size: 11px; color: var(--muted); margin-top: 8px; }\n'
        '  .num { font-family: SF Mono, Monaco, monospace; }\n'
        '  .footer { color: var(--muted); font-size: 11px; text-align: center; padding: 20px; }\n'
        '</style>\n'
        '</head>\n'
        '<body>\n'
        '  <h1>Phase 2L · Cross-Model Repertory Grid Report</h1>\n'
        '  <div class="subtitle">36 models × 7 advisory tasks × 2 conditions · Archipelago Research</div>\n'
        '\n'
        '  <div class="panel">\n'
        '    <h2>Overview</h2>\n'
        '    <div class="stat-grid">\n'
        '      <div class="stat"><div class="label">Cells loaded</div><div class="value" id="s-cells">-</div></div>\n'
        '      <div class="stat"><div class="label">Total ratings</div><div class="value" id="s-ratings">-</div></div>\n'
        '      <div class="stat"><div class="label">Rater×ratee pairs</div><div class="value" id="s-pairs">-</div></div>\n'
        '      <div class="stat"><div class="label">Unique constructs</div><div class="value" id="s-constructs">-</div></div>\n'
        '      <div class="stat"><div class="label">Mean inter-rater r</div><div class="value" id="s-rcorr">-</div></div>\n'
        '      <div class="stat"><div class="label">Median r</div><div class="value" id="s-rcorr-med">-</div></div>\n'
        '    </div>\n'
        '  </div>\n'
        '\n'
        '  <div class="panel">\n'
        '    <h2>Tier hypothesis - rater tier × ratee tier</h2>\n'
        '    <p class="subtitle">Mean rating (1-7 scale) when rater of tier X rates ratee of tier Y, averaged across all tasks and conditions.</p>\n'
        '    <table id="tier-table"></table>\n'
        '  </div>\n'
        '\n'
        '  <div class="panel">\n'
        '    <h2>Most divergent models (low consensus with others)</h2>\n'
        '    <table id="divergent-table"></table>\n'
        '  </div>\n'
        '\n'
        '  <div class="panel">\n'
        '    <h2>Most consensus models (high agreement with others)</h2>\n'
        '    <table id="consensus-table"></table>\n'
        '  </div>\n'
        '\n'
        '  <div class="panel">\n'
        '    <h2>Inter-rater correlation heatmap</h2>\n'
        '    <div class="tabs" id="task-tabs"></div>\n'
        '    <div id="heatmap-container"></div>\n'
        '    <div class="legend">Cell color: red (low correlation) → blue (high). Diagonal = 1.0 (self).</div>\n'
        '  </div>\n'
        '\n'
        '  <div class="panel">\n'
        '    <h2>Model Map - similarity space</h2>\n'
        '    <p class="subtitle">Force-directed layout. Models close together rate things similarly. Color = family. Border thickness = consensus level.</p>\n'
        '    <svg id="model-map" width="100%" height="600" viewBox="0 0 800 600"></svg>\n'
        '    <div class="legend">Hover dot for model details. The "Western consensus cluster" should appear in one region; divergent models scatter outward.</div>\n'
        '  </div>\n'
        '\n'
        '  <div class="panel">\n'
        '    <h2>Coverage by task × condition × model</h2>\n'
        '    <div id="coverage-container"></div>\n'
        '  </div>\n'
        '\n'
        '  <div class="footer">Phase 2L · Archipelago Research · 2026</div>\n'
        '\n'
        '<script id="data" type="application/json">' + data_json + '</script>\n'
        '<script>\n'
        'const DATA = JSON.parse(document.getElementById("data").textContent);\n'
        '\n'
        '// Top stats\n'
        'document.getElementById("s-cells").textContent = DATA.n_cells_loaded;\n'
        'document.getElementById("s-ratings").textContent = DATA.n_ratings.toLocaleString();\n'
        'document.getElementById("s-pairs").textContent = DATA.n_unique_pairs.toLocaleString();\n'
        'document.getElementById("s-constructs").textContent = DATA.n_unique_constructs.toLocaleString();\n'
        'document.getElementById("s-rcorr").textContent = (DATA.mean_inter_rater_corr || 0).toFixed(3);\n'
        'document.getElementById("s-rcorr-med").textContent = (DATA.median_inter_rater_corr || 0).toFixed(3);\n'
        '\n'
        '// Tier table\n'
        'const tierTable = document.getElementById("tier-table");\n'
        'let tierHtml = "<thead><tr><th>Rater tier</th><th>Ratee tier</th><th>Mean rating</th><th>Bar</th></tr></thead><tbody>";\n'
        'Object.entries(DATA.tier_overall || {}).sort((a,b) => b[1]-a[1]).forEach(([k, v]) => {\n'
        '  const [rt, , et] = k.split("_");\n'
        '  const pct = (v / 7) * 100;\n'
        '  tierHtml += `<tr><td class="tier-${rt}">${rt}</td><td class="tier-${et}">${et}</td><td class="num">${v.toFixed(3)}</td><td><div class="bar-bg"><div class="bar" style="width: ${pct}%"></div></div></td></tr>`;\n'
        '});\n'
        'tierHtml += "</tbody>";\n'
        'tierTable.innerHTML = tierHtml;\n'
        '\n'
        '// Divergent / consensus tables\n'
        'function renderModelTable(tableId, list) {\n'
        '  const tbl = document.getElementById(tableId);\n'
        '  let html = "<thead><tr><th>Short</th><th>Name</th><th>Family</th><th>Tier</th><th>Avg corr</th></tr></thead><tbody>";\n'
        '  list.slice(0, 10).forEach(([s, c]) => {\n'
        '    const m = DATA.model_meta[s] || {};\n'
        '    html += `<tr><td>${s}</td><td>${m.name||s}</td><td>${m.family||""}</td><td class="tier-${m.tier||""}">${m.tier||""}</td><td class="num">${c.toFixed(3)}</td></tr>`;\n'
        '  });\n'
        '  html += "</tbody>";\n'
        '  tbl.innerHTML = html;\n'
        '}\n'
        'renderModelTable("divergent-table", DATA.most_divergent_raters || []);\n'
        'renderModelTable("consensus-table", DATA.most_consensus_raters || []);\n'
        '\n'
        '// Heatmap\n'
        'const taskCondKeys = Object.keys(DATA.inter_rater_corrs || {}).sort();\n'
        'const tabsEl = document.getElementById("task-tabs");\n'
        'taskCondKeys.forEach((k, i) => {\n'
        '  const tab = document.createElement("div");\n'
        '  tab.className = "tab" + (i === 0 ? " active" : "");\n'
        '  tab.textContent = k;\n'
        '  tab.onclick = () => {\n'
        '    document.querySelectorAll("#task-tabs .tab").forEach(t => t.classList.remove("active"));\n'
        '    tab.classList.add("active");\n'
        '    renderHeatmap(k);\n'
        '  };\n'
        '  tabsEl.appendChild(tab);\n'
        '});\n'
        '\n'
        'function corrColor(c) {\n'
        '  // -1 = red, 0 = grey, 1 = blue\n'
        '  if (c === null || c === undefined) return "#222";\n'
        '  const r = c < 0 ? 1 : 1 - c;\n'
        '  const b = c > 0 ? 1 : 1 + c;\n'
        '  const g = 0.5 - Math.abs(c) * 0.3;\n'
        '  return `rgb(${Math.round(r*220)}, ${Math.round(g*200)}, ${Math.round(b*240)})`;\n'
        '}\n'
        '\n'
        'function renderHeatmap(key) {\n'
        '  const corrs = DATA.inter_rater_corrs[key] || {};\n'
        '  const raters = Object.keys(DATA.model_meta);\n'
        '  let html = "<div style=\\"overflow: auto; max-width: 100%;\\"><table class=\\"heatmap-table\\"><thead><tr><th class=\\"heatmap-rowhead\\"></th>";\n'
        '  raters.forEach(r => html += `<th class=\\"heatmap-colhead\\">${r}</th>`);\n'
        '  html += "</tr></thead><tbody>";\n'
        '  raters.forEach(r1 => {\n'
        '    html += `<tr><th class=\\"heatmap-rowhead\\">${r1}</th>`;\n'
        '    raters.forEach(r2 => {\n'
        '      const k = `${r1}|${r2}`;\n'
        '      const c = corrs[k];\n'
        '      if (c === undefined || c === null) {\n'
        '        html += `<td class=\\"heatmap-cell\\" style=\\"background: #222; color: #555\\">-</td>`;\n'
        '      } else {\n'
        '        html += `<td class=\\"heatmap-cell\\" style=\\"background: ${corrColor(c)}\\" title=\\"${r1} vs ${r2}: ${c.toFixed(3)}\\">${c.toFixed(1)}</td>`;\n'
        '      }\n'
        '    });\n'
        '    html += "</tr>";\n'
        '  });\n'
        '  html += "</tbody></table></div>";\n'
        '  document.getElementById("heatmap-container").innerHTML = html;\n'
        '}\n'
        'if (taskCondKeys.length > 0) renderHeatmap(taskCondKeys[0]);\n'
        '\n'
        '// Model Map - force-directed similarity layout\n'
        'function renderModelMap() {\n'
        '  const svg = document.getElementById("model-map");\n'
        '  const w = 800, h = 600;\n'
        '  const familyColors = {\n'
        '    anthropic: "#D97757", openai: "#10A37F", google: "#4285F4",\n'
        '    mistral: "#FF7000", deepseek: "#536DFE", xai: "#000000",\n'
        '    qwen: "#615CED", moonshot: "#1E88E5", zhipu: "#F9A825",\n'
        '    nvidia: "#76B900", meta: "#1877F2", cohere: "#FF7759",\n'
        '  };\n'
        '  const tierStroke = {cheap: "#7dd3fc", mid: "#a3e635", flagship: "#f9a8d4"};\n'
        '\n'
        '  // Aggregate avg correlation across all (task, cond)\n'
        '  const allCorrs = DATA.inter_rater_corrs || {};\n'
        '  const pairAvg = {};\n'
        '  Object.values(allCorrs).forEach(corrDict => {\n'
        '    Object.entries(corrDict).forEach(([k, v]) => {\n'
        '      const [a, b] = k.split("|");\n'
        '      if (a === b) return;\n'
        '      const key = a < b ? `${a}|${b}` : `${b}|${a}`;\n'
        '      if (!pairAvg[key]) pairAvg[key] = [];\n'
        '      pairAvg[key].push(v);\n'
        '    });\n'
        '  });\n'
        '  const avgPairs = {};\n'
        '  Object.entries(pairAvg).forEach(([k, vs]) => {\n'
        '    avgPairs[k] = vs.reduce((a, b) => a + b, 0) / vs.length;\n'
        '  });\n'
        '\n'
        '  // Build nodes\n'
        '  const consensusByModel = DATA.divergence_summary || {};\n'
        '  const nodes = Object.keys(DATA.model_meta).map(m => {\n'
        '    const meta = DATA.model_meta[m];\n'
        '    return {\n'
        '      id: m, name: meta.name, family: meta.family, tier: meta.tier,\n'
        '      consensus: consensusByModel[m] || 0,\n'
        '      x: w/2 + (Math.random() - 0.5) * 200,\n'
        '      y: h/2 + (Math.random() - 0.5) * 200,\n'
        '      vx: 0, vy: 0,\n'
        '    };\n'
        '  });\n'
        '  const nodeMap = Object.fromEntries(nodes.map(n => [n.id, n]));\n'
        '\n'
        '  // Build edges (positive correlations only, |r| > 0.2)\n'
        '  const edges = [];\n'
        '  Object.entries(avgPairs).forEach(([k, r]) => {\n'
        '    if (Math.abs(r) < 0.15) return;\n'
        '    const [a, b] = k.split("|");\n'
        '    if (nodeMap[a] && nodeMap[b]) {\n'
        '      edges.push({source: nodeMap[a], target: nodeMap[b], strength: r});\n'
        '    }\n'
        '  });\n'
        '\n'
        '  // Simple force simulation (no D3 lib needed)\n'
        '  const k = 0.1, repulsion = 800, damping = 0.85;\n'
        '  const center = {x: w/2, y: h/2};\n'
        '  for (let iter = 0; iter < 300; iter++) {\n'
        '    // Repulsion between all nodes\n'
        '    for (let i = 0; i < nodes.length; i++) {\n'
        '      for (let j = i + 1; j < nodes.length; j++) {\n'
        '        const a = nodes[i], b = nodes[j];\n'
        '        const dx = b.x - a.x, dy = b.y - a.y;\n'
        '        const dist = Math.sqrt(dx*dx + dy*dy) + 0.1;\n'
        '        const force = repulsion / (dist * dist);\n'
        '        const fx = (dx / dist) * force, fy = (dy / dist) * force;\n'
        '        a.vx -= fx; a.vy -= fy;\n'
        '        b.vx += fx; b.vy += fy;\n'
        '      }\n'
        '    }\n'
        '    // Attraction along edges (positive r pulls together; negative pushes apart)\n'
        '    edges.forEach(e => {\n'
        '      const dx = e.target.x - e.source.x, dy = e.target.y - e.source.y;\n'
        '      const dist = Math.sqrt(dx*dx + dy*dy) + 0.1;\n'
        '      const ideal = 200 * (1 - e.strength);  // higher r = closer\n'
        '      const force = (dist - ideal) * 0.02;\n'
        '      const fx = (dx / dist) * force, fy = (dy / dist) * force;\n'
        '      e.source.vx += fx; e.source.vy += fy;\n'
        '      e.target.vx -= fx; e.target.vy -= fy;\n'
        '    });\n'
        '    // Gravity to center\n'
        '    nodes.forEach(n => {\n'
        '      n.vx += (center.x - n.x) * 0.005;\n'
        '      n.vy += (center.y - n.y) * 0.005;\n'
        '    });\n'
        '    // Apply velocity\n'
        '    nodes.forEach(n => {\n'
        '      n.vx *= damping; n.vy *= damping;\n'
        '      n.x += n.vx; n.y += n.vy;\n'
        '      n.x = Math.max(40, Math.min(w - 40, n.x));\n'
        '      n.y = Math.max(40, Math.min(h - 40, n.y));\n'
        '    });\n'
        '  }\n'
        '\n'
        '  // Render edges first (behind nodes)\n'
        '  const NS = "http://www.w3.org/2000/svg";\n'
        '  svg.innerHTML = "";\n'
        '  edges.forEach(e => {\n'
        '    if (Math.abs(e.strength) < 0.2) return;\n'
        '    const line = document.createElementNS(NS, "line");\n'
        '    line.setAttribute("x1", e.source.x);\n'
        '    line.setAttribute("y1", e.source.y);\n'
        '    line.setAttribute("x2", e.target.x);\n'
        '    line.setAttribute("y2", e.target.y);\n'
        '    line.setAttribute("stroke", e.strength > 0 ? "#60a5fa" : "#ef4444");\n'
        '    line.setAttribute("stroke-width", Math.abs(e.strength) * 3);\n'
        '    line.setAttribute("stroke-opacity", "0.25");\n'
        '    svg.appendChild(line);\n'
        '  });\n'
        '\n'
        '  // Render nodes\n'
        '  nodes.forEach(n => {\n'
        '    const g = document.createElementNS(NS, "g");\n'
        '    g.setAttribute("transform", `translate(${n.x},${n.y})`);\n'
        '    const r = 8 + Math.max(0, n.consensus) * 30;\n'
        '    const circle = document.createElementNS(NS, "circle");\n'
        '    circle.setAttribute("r", r);\n'
        '    circle.setAttribute("fill", familyColors[n.family] || "#888");\n'
        '    circle.setAttribute("stroke", tierStroke[n.tier] || "#fff");\n'
        '    circle.setAttribute("stroke-width", "3");\n'
        '    circle.setAttribute("opacity", "0.85");\n'
        '    g.appendChild(circle);\n'
        '    const tip = document.createElementNS(NS, "title");\n'
        '    tip.textContent = `${n.id}: ${n.name}\\nfamily: ${n.family}, tier: ${n.tier}\\nconsensus: ${n.consensus.toFixed(3)}`;\n'
        '    g.appendChild(tip);\n'
        '    const text = document.createElementNS(NS, "text");\n'
        '    text.setAttribute("text-anchor", "middle");\n'
        '    text.setAttribute("dy", r + 12);\n'
        '    text.setAttribute("fill", "#e6e6e6");\n'
        '    text.setAttribute("font-size", "10");\n'
        '    text.setAttribute("font-family", "SF Mono, monospace");\n'
        '    text.textContent = n.id;\n'
        '    g.appendChild(text);\n'
        '    svg.appendChild(g);\n'
        '  });\n'
        '}\n'
        'renderModelMap();\n'
        '\n'
        '// Coverage table\n'
        'const cov = DATA.coverage || {};\n'
        'let covHtml = "<table><thead><tr><th>Task</th><th>Cond</th><th>Models with data</th><th>Avg completion</th></tr></thead><tbody>";\n'
        'Object.keys(cov).sort().forEach(task => {\n'
        '  Object.keys(cov[task]||{}).sort().forEach(cond => {\n'
        '    const raters = cov[task][cond] || {};\n'
        '    const n = Object.keys(raters).length;\n'
        '    const avgComp = Object.values(raters).reduce((a,b) => a + (b.completion||0), 0) / Math.max(1, n);\n'
        '    covHtml += `<tr><td>${task}</td><td>${cond}</td><td class="num">${n}/36</td><td class="num">${(avgComp*100).toFixed(0)}%</td></tr>`;\n'
        '  });\n'
        '});\n'
        'covHtml += "</tbody></table>";\n'
        'document.getElementById("coverage-container").innerHTML = covHtml;\n'
        '</script>\n'
        '</body>\n'
        '</html>\n'
    )
    out_html.write_text(html, encoding="utf-8")
    print(f"Saved: {out_html}")


def main() -> int:
    if not RESULTS_DIR.exists():
        print(f"ERROR: {RESULTS_DIR} not found.")
        return 2
    if not PHASE4_DIR.exists():
        print(f"ERROR: {PHASE4_DIR} not found. Phase 4 must complete first.")
        return 2

    results = run_analysis()
    if not results:
        return 1
    save_results(results)
    generate_html_report(results)

    print("\n" + "=" * 100)
    print(" Done. Outputs:")
    print(f"   {RESULTS_DIR}/analysis_results.json")
    print(f"   {RESULTS_DIR}/analysis_summary.md")
    print(f"   {RESULTS_DIR}/report_phase2l.html")
    print("\n Open report in browser:")
    print(f"   start {RESULTS_DIR}/report_phase2l.html")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
