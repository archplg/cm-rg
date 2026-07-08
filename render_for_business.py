#!/usr/bin/env python3
"""
Renders operator_insight.json into formats useful for BUSINESS DECISION MAKERS
considering whether to retain Archipelago as a service.

Outputs (per cell):
- executive_briefing/<cell>/briefing.md - 3-page executive briefing
- executive_briefing/<cell>/detailed_appendix.md - longer analytical appendix
- executive_briefing/sample_case.md - one polished "sales sample" case

Run:
    python render_for_business.py
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

OPERATOR_DIR = Path("./operator_outputs")
EXEC_DIR = Path("./executive_briefing")


def load_insights():
    p = OPERATOR_DIR / "all_insights.json"
    if not p.exists():
        print("Run operator_synthesis.py first.")
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def task_brief(task_id: str) -> str:
    p = Path("./tasks") / f"task_{task_id}_brief.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _read_interp(cell_id: str, viz_name: str) -> str:
    p = Path("./analysis") / cell_id / f"{viz_name}.interpretation.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _viz_relpath(cell_id: str, viz_name: str) -> str:
    """Copy viz into executive_briefing/<cell>/viz/ and return relative path."""
    src = Path("./analysis") / cell_id / f"{viz_name}.png"
    if not src.exists():
        return ""
    target_dir = EXEC_DIR / cell_id / "viz"
    target_dir.mkdir(parents=True, exist_ok=True)
    import shutil
    target = target_dir / src.name
    shutil.copy(src, target)
    return f"viz/{src.name}"


# ============================================================
# Executive briefing (3-page)
# ============================================================
EXEC_TEMPLATE = """# Strategic AI Council Briefing

**Case identifier:** {cell_id}
**Decision domain:** {task_domain}
**Analysis configuration:** {configuration}
**Date:** generated from operator_insight.json

---

## Executive summary

{headline}

**Recommendation strength:** {consensus_strength}.
**Reasoning alignment:** {reasoning_alignment}.

{summary_paragraph}

---

## 1. What the AI Council recommends

Five frontier AI models, each operating under a distinct epistemological frame, analyzed this decision independently. Their recommendations:

{distribution_table}

{interpretation_of_distribution}

![Recommendations and reasoning]({consensus_path})

{consensus_interpretation}

## 2. The hidden disagreement check

The most consequential finding in any multi-perspective analysis is not where the experts disagreed - it is where they appeared to agree but did so for incompatible reasons.

![Reasoning agreement network]({network_path})

{network_interpretation}

{hidden_paragraph}

{hidden_implication}

## 3. What no one weighted enough

The analysis surfaced dimensions of this decision that all five voices treated as middling - neither strongly for nor strongly against.

{blind_spots_paragraph}

## 4. Risks raised by minority voices

Risks that consensus aggregation tends to dilute, but that minority voices flagged:

{risks_paragraph}

## 5. Questions for your leadership team

The following questions are designed to surface what the AI Council could not resolve on its own - they require your team's judgment, your organizational context, and your accountability:

{questions_block}

---

## Methodology note

This briefing was produced using the Archipelago method - a structured procedure derived from personal construct theory (Kelly, 1955) applied to multi-agent LLM analysis. The method does not aim to give you "the right answer." It aims to give you a legible map of where reasonable analyses would diverge and why, so your team can decide with eyes open.

The five voices are: Q (quantitative-empirical), S (systems-strategic), E (engineering-fundamentals), H (humanist-ethical), C (contrarian-skeptical). Each voice was provided by a different frontier model family to control for shared training distribution.

---

*This briefing is decision support, not decision substitution. The reasoning, judgment, and accountability remain with you.*
"""


def render_briefing(insight: dict) -> str:
    cm = insight["consensus_map"]
    hidden = insight["hidden_disagreement"]
    blind = insight["blind_spots"]
    risks = insight["risk_surface"]

    # Distribution table (markdown)
    dist = cm.get("distribution", {})
    if dist:
        lines = ["| Option | Voices in favor | Source frames |", "|---|---|---|"]
        by_opt = {opt: [] for opt in dist}
        for sn, info in cm["by_agent"].items():
            rec = info.get("recommendation")
            if rec in by_opt:
                by_opt[rec].append(f"{sn}/{info.get('persona', '?')}")
        for opt in sorted(dist.keys()):
            lines.append(f"| **Option {opt}** | {dist[opt]} of 5 | {', '.join(by_opt[opt])} |")
        distribution_table = "\n".join(lines)
    else:
        distribution_table = "_Recommendations could not be parsed clearly._"

    majority = cm.get("majority_recommendation")
    if cm.get("consensus_strength") == "strong":
        interpretation_of_distribution = (
            f"The AI Council reached strong consensus on **Option {majority}** "
            f"({dist.get(majority, 0)} of 5 voices). Standard ensemble methods "
            f"would report this as a confident recommendation. The next section "
            f"examines whether this confidence is warranted."
        )
    elif cm.get("consensus_strength") == "partial":
        interpretation_of_distribution = (
            f"A partial consensus emerged on **Option {majority}** "
            f"({dist.get(majority, 0)} of 5 voices), with the remainder split "
            f"across other options. This is the configuration most likely to "
            f"produce surprises in execution: enough agreement to feel decisive, "
            f"not enough alignment to actually be."
        )
    else:
        interpretation_of_distribution = (
            "The AI Council was split across options. No standard aggregation "
            "method will produce a confident recommendation here. The value of "
            "this analysis is in the structure of the disagreement, not in "
            "averaging it away."
        )

    # Hidden disagreement
    if hidden.get("status") == "computed":
        score = hidden.get("reasoning_diversity_score", 0)
        hidden_paragraph = hidden.get("interpretation", "")
        if score > 1.0:
            hidden_implication = (
                "> **Implication for execution:** if you proceed with this "
                "recommendation, the framing that drives it will matter. "
                "Different framings produce different execution paths, "
                "different metrics, and different definitions of success. "
                "Make explicit which framing your team is operating from before "
                "committing resources."
            )
        elif score > 0.5:
            hidden_implication = (
                "> **Implication:** moderate framing differences exist among "
                "the voices that recommended the majority option. This is not "
                "an obstacle, but it is worth surfacing in execution planning."
            )
        else:
            hidden_implication = (
                "> **Implication:** the consensus is robust at the reasoning "
                "level. You can proceed with a single coherent narrative."
            )
    else:
        hidden_paragraph = "_Hidden disagreement analysis was not applicable to this case._"
        hidden_implication = ""

    # Blind spots
    blind_list = blind.get("low_discrimination_constructs", [])
    if blind_list:
        paras = []
        for c in blind_list[:3]:
            paras.append(
                f"**{c['left_pole']} vs {c['right_pole']}.** All options "
                f"scored near the middle on this dimension. Probe: should any "
                f"option emphasize this axis more strongly? If yes, the current "
                f"options may need refinement before commitment."
            )
        blind_spots_paragraph = "\n\n".join(paras)
    else:
        blind_spots_paragraph = (
            "_The analysis did not surface obvious blind spots. The voices "
            "collectively explored the relevant dimensions of this decision._"
        )

    # Risks
    risk_data = risks.get("risks_by_agent", {})
    risk_lines = []
    for sn, rs in risk_data.items():
        if rs:
            persona = cm["by_agent"].get(sn, {}).get("persona", "?")
            risk_lines.append(f"- **{persona} frame ({sn}):** {'; '.join(rs[:2])}")
    risks_paragraph = "\n".join(risk_lines) if risk_lines else "_No specific risks extracted from individual voices._"

    # Questions
    qs = insight.get("operator_questions", [])
    questions_block = "\n\n".join(f"**Q{i+1}.** {q}" for i, q in enumerate(qs)) or "_None generated._"

    # Top-level summary paragraph
    if cm.get("consensus_strength") == "strong":
        if hidden.get("reasoning_diversity_score", 0) > 1.0:
            summary_paragraph = (
                f"The five voices reached strong consensus on Option {majority}, "
                f"but their reasoning differs substantially. This is the configuration "
                f"most likely to produce execution surprises: the recommendation is "
                f"shared, the path to it is not."
            )
        else:
            summary_paragraph = (
                f"The five voices reached strong consensus on Option {majority} "
                f"with substantially aligned reasoning. This is the configuration "
                f"most safe to act on, conditional on the blind-spot check."
            )
    elif cm.get("consensus_strength") == "partial":
        summary_paragraph = (
            f"Partial consensus formed around Option {majority}. The remaining "
            f"voices saw the decision differently. Both perspectives have merit "
            f"and the choice involves an explicit value tradeoff."
        )
    else:
        summary_paragraph = (
            "The five voices did not converge. Each saw a different option as "
            "most appropriate, and their disagreement reflects genuine value "
            "tradeoffs rather than analytical error. Your team's judgment matters more here than the AI Council's."
        )

    return EXEC_TEMPLATE.format(
        cell_id=insight["cell_id"],
        task_domain=insight["task"],
        configuration=("neutral framing" if insight["condition"] == "N" else "persona framing"),
        headline=insight["headline"],
        consensus_strength=cm.get("consensus_strength", "unknown").upper(),
        reasoning_alignment=(
            "high" if hidden.get("reasoning_diversity_score", 0) < 0.5
            else "moderate" if hidden.get("reasoning_diversity_score", 0) < 1.0
            else "low"
        ),
        summary_paragraph=summary_paragraph,
        distribution_table=distribution_table,
        interpretation_of_distribution=interpretation_of_distribution,
        hidden_paragraph=hidden_paragraph,
        hidden_implication=hidden_implication,
        blind_spots_paragraph=blind_spots_paragraph,
        risks_paragraph=risks_paragraph,
        questions_block=questions_block,
        consensus_path=_viz_relpath(insight["cell_id"], "consensus_vs_reasoning") or "(viz not generated)",
        consensus_interpretation=_read_interp(insight["cell_id"], "consensus_vs_reasoning"),
        network_path=_viz_relpath(insight["cell_id"], "agreement_network") or "(viz not generated)",
        network_interpretation=_read_interp(insight["cell_id"], "agreement_network"),
    )


# ============================================================
# Detailed appendix
# ============================================================
APPENDIX_TEMPLATE = """# Detailed Appendix: {cell_id}

## A. Full task brief

```
{brief}
```

## B. Each voice in their own words

{voice_blocks}

## C. The construct space

Each voice produced bipolar constructs through a triadic elicitation procedure.
The full list of {n_constructs} constructs is in `results/{cell_id}/cell.json`.

Constructs where all options scored near the middle (potential blind spots):

{blind_constructs}

## D. Pairwise reasoning distance matrix

| Pair | RMSE (rating space) |
|---|---|
{distance_rows}

Interpretation: pairs with RMSE > 1.0 indicate that the two voices, although they
may agree on the output recommendation, reason about it through substantially
different frames. RMSE < 0.3 indicates aligned reasoning.

## E. Risks extracted from each voice

{risks_per_voice}

## F. Methodology summary

The Archipelago method consists of four phases:
1. **Divergent free response.** Each voice generates an independent analysis.
2. **Anonymization.** Responses are labeled E1-E5 to remove identity bias.
3. **Triadic construct elicitation.** Each voice identifies bipolar evaluative axes by comparing triples of anonymized responses.
4. **Rating.** Each voice rates all responses on all elicited constructs.

The resulting tensor is analyzed for: inter-voice agreement, content distinctness of constructs, principal-component structure of the decision space, and hidden disagreement among voices reaching the same conclusion.
"""


def render_appendix(insight: dict) -> str:
    cm = insight["consensus_map"]
    blind = insight["blind_spots"]

    # Voices in their own words
    cell_path = Path("./results") / insight["cell_id"] / "cell.json"
    cell = json.loads(cell_path.read_text(encoding="utf-8")) if cell_path.exists() else {}
    free_resp = cell.get("free_responses", {})
    voice_blocks = []
    for sn in sorted(free_resp.keys()):
        info = cm["by_agent"].get(sn, {})
        voice_blocks.append(
            f"### {sn} (frame: {info.get('persona', '?')}, model: `{info.get('model_id', '?')}`)\n\n"
            f"{free_resp[sn]}"
        )

    # Blind constructs
    blind_list = blind.get("low_discrimination_constructs", [])
    if blind_list:
        blind_block = "\n".join(
            f"- {c['left_pole']} <-> {c['right_pole']} (mean rating {c['mean_rating']:.2f}, std {c['rating_std']:.2f})"
            for c in blind_list
        )
    else:
        blind_block = "_None._"

    # Distance matrix
    hidden = insight["hidden_disagreement"]
    distances = hidden.get("pairwise_distances", {})
    distance_rows = "\n".join(
        f"| {k.replace('_vs_', ' vs ')} | {v:.3f} |"
        for k, v in sorted(distances.items())
    ) or "| _no pairs computed_ | |"

    # Risks per voice
    risks_data = insight["risk_surface"].get("risks_by_agent", {})
    risk_blocks = []
    for sn, rs in risks_data.items():
        if rs:
            persona = cm["by_agent"].get(sn, {}).get("persona", "?")
            risk_blocks.append(f"**{sn} ({persona}):**\n" + "\n".join(f"- {r}" for r in rs))
    risks_per_voice = "\n\n".join(risk_blocks) if risk_blocks else "_None extracted._"

    return APPENDIX_TEMPLATE.format(
        cell_id=insight["cell_id"],
        brief=task_brief(insight["task"]),
        voice_blocks="\n\n".join(voice_blocks),
        n_constructs=sum(len(v) for v in cell.get("constructs", {}).values()),
        blind_constructs=blind_block,
        distance_rows=distance_rows,
        risks_per_voice=risks_per_voice,
    )


# ============================================================
# Main
# ============================================================
def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--cell", default=None)
    args = p.parse_args()

    EXEC_DIR.mkdir(exist_ok=True)
    insights = load_insights()
    if not insights:
        return 1

    if args.cell:
        insights = [i for i in insights if i["cell_id"] == args.cell]

    best_sample = None
    best_sample_score = -1

    for i in insights:
        out_dir = EXEC_DIR / i["cell_id"]
        out_dir.mkdir(exist_ok=True)
        (out_dir / "briefing.md").write_text(render_briefing(i), encoding="utf-8")
        (out_dir / "detailed_appendix.md").write_text(render_appendix(i), encoding="utf-8")
        # Pick the "best demo" - one with both strong consensus AND high hidden disagreement
        cm = i["consensus_map"]
        hidden = i["hidden_disagreement"]
        score = 0
        if cm.get("consensus_strength") == "strong":
            score += hidden.get("reasoning_diversity_score", 0) * 2
        if score > best_sample_score:
            best_sample_score = score
            best_sample = i
        print(f"  {i['cell_id']}: briefing + appendix written")

    if best_sample and not args.cell:
        sample_md = "# Sample Strategic AI Council Briefing\n\n"
        sample_md += "_This is a representative sample of the Strategic AI Council service. "
        sample_md += "Real engagements analyze your specific decision with full confidentiality._\n\n---\n\n"
        sample_md += render_briefing(best_sample)
        (EXEC_DIR / "sample_case.md").write_text(sample_md, encoding="utf-8")
        print(f"  Wrote sample_case.md (best illustrative case: {best_sample['cell_id']})")

    print(f"\nExecutive briefing kit ready in {EXEC_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
