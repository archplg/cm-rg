#!/usr/bin/env python3
"""
Renders operator_insight.json into formats useful for COACHES and CONSULTANTS.

Outputs (per cell):
- coach_kit/<cell>/one_pager.html  - interactive single-page summary to share with a client
- coach_kit/<cell>/session_guide.md - 90-minute team session structured around the insight
- coach_kit/<cell>/facilitator_questions.md - questions to drive the conversation

Run:
    python render_for_coaches.py
"""
from __future__ import annotations
import argparse
import html
import json
import re
from pathlib import Path

OPERATOR_DIR = Path("./operator_outputs")
COACH_DIR = Path("./coach_kit")


def load_insights():
    if not (OPERATOR_DIR / "all_insights.json").exists():
        print(f"Run operator_synthesis.py first.")
        return []
    with open(OPERATOR_DIR / "all_insights.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_cell_raw(cell_id: str) -> dict | None:
    p = Path("./results") / cell_id / "cell.json"
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def task_brief(task_id: str) -> str:
    p = Path("./tasks") / f"task_{task_id}_brief.md"
    if p.exists():
        return p.read_text(encoding="utf-8")
    return f"(brief not found for task {task_id})"


# ============================================================
# One-pager HTML
# ============================================================
ONE_PAGER_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AI Council Briefing - {cell_id}</title>
<style>
body {{ font-family: Georgia, serif; max-width: 820px; margin: 40px auto; padding: 0 24px; color: #1a1a1a; line-height: 1.55; }}
h1 {{ font-size: 1.7em; margin-bottom: 0.2em; color: #2b3a55; }}
h2 {{ font-size: 1.2em; margin-top: 1.8em; color: #2b3a55; border-bottom: 2px solid #2b3a55; padding-bottom: 4px; }}
h3 {{ font-size: 1em; margin-top: 1.3em; color: #555; }}
.meta {{ color: #888; font-size: 0.85em; margin-bottom: 1.5em; }}
.headline {{ background: #f4f1e8; border-left: 4px solid #c8a45c; padding: 14px 18px; margin: 1em 0; font-size: 1.05em; }}
.flag {{ background: #fdf0ed; border-left: 4px solid #c44; padding: 14px 18px; margin: 1em 0; }}
.good {{ background: #f0f7ed; border-left: 4px solid #3a7d44; padding: 14px 18px; margin: 1em 0; }}
.dist {{ display: flex; gap: 10px; flex-wrap: wrap; margin: 1em 0; }}
.dist-cell {{ background: #f6f6f6; padding: 8px 14px; border-radius: 4px; }}
.dist-cell.majority {{ background: #2b3a55; color: white; }}
.q {{ margin: 0.8em 0; padding-left: 1em; border-left: 3px solid #c8a45c; }}
table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
th, td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid #ddd; vertical-align: top; }}
th {{ background: #f4f1e8; }}
.persona-Q {{ color: #0a558c; }}
.persona-S {{ color: #2d8659; }}
.persona-E {{ color: #8a5a00; }}
.persona-H {{ color: #882b6f; }}
.persona-C {{ color: #b03030; }}
.persona-neutral {{ color: #666; }}
.snippet {{ font-style: italic; color: #555; font-size: 0.9em; }}
.viz {{ margin: 1em 0; text-align: center; }}
.viz img {{ max-width: 100%; height: auto; border: 1px solid #e6e1d4; border-radius: 4px; }}
.viz-caption {{ font-size: 0.9em; color: #555; font-style: italic; margin-top: 6px; line-height: 1.4; }}
.footer {{ margin-top: 3em; color: #999; font-size: 0.8em; }}
</style>
</head>
<body>

<h1>AI Council Briefing</h1>
<div class="meta">Case <strong>{cell_id}</strong> &mdash; task {task} &mdash; {condition_label} &mdash; run {run_idx}</div>

<div class="headline">{headline}</div>

<h2>The decision under analysis</h2>
<details>
<summary>Task brief (click to expand)</summary>
<pre style="white-space: pre-wrap; background: #f9f9f9; padding: 14px; border-radius: 4px; font-family: Georgia, serif;">{brief}</pre>
</details>

<h2>What 5 perspectives recommended</h2>
<div class="dist">{distribution_html}</div>

{consensus_split_viz}

<table>
<thead><tr><th>Voice</th><th>Recommends</th><th>Why (in their words)</th></tr></thead>
<tbody>
{agent_rows}
</tbody>
</table>

<h2>How the voices align - the reasoning network</h2>
{network_viz}

<h2>Hidden disagreement check</h2>
<div class="{hidden_class}">{hidden_text}</div>

<h2>Where each option sits in the decision space</h2>
{biplot_viz}

<h2>Blind spots: what no one really weighted</h2>
{blind_spots_html}

<h2>Risks raised by individual voices</h2>
<p style="font-size: 0.9em; color: #666;">Concerns each voice flagged in passing - worth surfacing before action:</p>
{risks_html}

<h2>Questions to bring to the room</h2>
{questions_html}

<div class="footer">
Produced by Archipelago AI Council. The five voices here are role-played LLM analysts;
they are a structured starting point for human conversation, not a substitute for it.
</div>

</body>
</html>
"""


def _embed_viz(cell_id: str, viz_name: str, caption_default: str) -> str:
    """Read a PNG from analysis/<cell>/ and its .interpretation.md, embed both."""
    analysis_dir = Path("./analysis") / cell_id
    png = analysis_dir / f"{viz_name}.png"
    interp = analysis_dir / f"{viz_name}.interpretation.md"
    if not png.exists():
        return f'<p style="color: #999; font-style: italic;">{caption_default} (not yet generated - run visualizations.py)</p>'
    # Copy into coach_kit so the HTML is self-contained
    out_assets = COACH_DIR / cell_id / "viz"
    out_assets.mkdir(parents=True, exist_ok=True)
    target_png = out_assets / png.name
    import shutil
    shutil.copy(png, target_png)
    interp_text = ""
    if interp.exists():
        # Convert markdown headings/bold to lightweight HTML
        raw = interp.read_text(encoding="utf-8")
        # Simple replacements
        raw = html.escape(raw)
        raw = re.sub(r"^## (.+)$", r"<h3>\1</h3>", raw, flags=re.MULTILINE)
        raw = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", raw)
        raw = raw.replace("\n\n", "</p><p>")
        interp_text = f"<div class='viz-caption'><p>{raw}</p></div>"
    return (
        f'<div class="viz">'
        f'<img src="viz/{html.escape(png.name)}" alt="{html.escape(caption_default)}">'
        f'{interp_text}'
        f'</div>'
    )


def render_one_pager(insight: dict, cell: dict) -> str:
    cm = insight["consensus_map"]
    by_agent = cm["by_agent"]
    dist = cm["distribution"]
    majority = cm.get("majority_recommendation")
    cid = insight["cell_id"]

    distribution_html = ""
    for opt, n in sorted(dist.items()):
        css = "majority" if opt == majority else ""
        distribution_html += f'<div class="dist-cell {css}">Option {html.escape(opt)}: {n} voice{"s" if n != 1 else ""}</div>'

    rows = []
    for sn in sorted(by_agent.keys()):
        info = by_agent[sn]
        persona = info.get("persona", "neutral")
        rec = info.get("recommendation") or "—"
        snippet = html.escape(info.get("rationale_snippet", "")[:280])
        rows.append(
            f'<tr><td class="persona-{html.escape(persona)}">{html.escape(sn)} '
            f'<small>({html.escape(persona)})</small></td>'
            f'<td><strong>{html.escape(rec)}</strong></td>'
            f'<td class="snippet">{snippet}</td></tr>'
        )

    hidden = insight["hidden_disagreement"]
    if hidden.get("status") == "computed":
        score = hidden.get("reasoning_diversity_score", 0)
        hidden_class = "flag" if score > 1.0 else "good" if score < 0.5 else "headline"
        hidden_text = html.escape(hidden.get("interpretation", ""))
    else:
        hidden_class = "headline"
        hidden_text = "Hidden disagreement could not be computed for this case."

    blind = insight["blind_spots"]
    if blind.get("low_discrimination_constructs"):
        items = []
        for c in blind["low_discrimination_constructs"]:
            items.append(
                f'<li><strong>{html.escape(c["left_pole"] or "?")} '
                f'&harr; {html.escape(c["right_pole"] or "?")}</strong>: '
                f'{html.escape(c.get("interpretation", "") or "")}</li>'
            )
        blind_spots_html = "<ul>" + "".join(items) + "</ul>"
    else:
        blind_spots_html = '<p style="color: #666;">No obvious blind spots detected. The voices collectively explored the dimensions of this decision.</p>'

    risks = insight["risk_surface"]
    if risks.get("risks_by_agent"):
        items = []
        for sn, rlist in risks["risks_by_agent"].items():
            if not rlist:
                continue
            persona = by_agent.get(sn, {}).get("persona", "neutral")
            items.append(
                f'<li><strong class="persona-{html.escape(persona)}">{html.escape(sn)}</strong>: '
                + "; ".join(html.escape(r) for r in rlist[:3]) + "</li>"
            )
        risks_html = "<ul>" + "".join(items) + "</ul>" if items else '<p style="color: #666;">No specific risks were flagged by individual voices.</p>'
    else:
        risks_html = '<p style="color: #666;">No specific risks were extracted.</p>'

    questions_html = ""
    for q in insight.get("operator_questions", []):
        questions_html += f'<div class="q">{html.escape(q)}</div>'
    if not questions_html:
        questions_html = '<p style="color: #666;">No specific questions generated.</p>'

    condition_label = "neutral framing" if insight["condition"] == "N" else "persona framing"

    # Embedded visualizations
    consensus_split_viz = _embed_viz(cid, "consensus_vs_reasoning", "Recommendations distribution chart")
    network_viz = _embed_viz(cid, "agreement_network", "Reasoning agreement network")
    biplot_viz = _embed_viz(cid, "biplot_annotated", "Decision-space map")

    return ONE_PAGER_TEMPLATE.format(
        cell_id=html.escape(insight["cell_id"]),
        task=html.escape(str(insight["task"])),
        condition_label=condition_label,
        run_idx=insight["run_idx"],
        headline=html.escape(insight["headline"]),
        brief=html.escape(task_brief(insight["task"])),
        distribution_html=distribution_html,
        agent_rows="\n".join(rows),
        hidden_class=hidden_class,
        hidden_text=hidden_text,
        blind_spots_html=blind_spots_html,
        risks_html=risks_html,
        questions_html=questions_html,
        consensus_split_viz=consensus_split_viz,
        network_viz=network_viz,
        biplot_viz=biplot_viz,
    )


# ============================================================
# Session guide markdown
# ============================================================
SESSION_GUIDE = """# 90-Minute Session Guide: Working with the AI Council Briefing

**Case:** {cell_id} (task {task}, {condition_label})
**Materials needed:** printed one-pager, flipchart, markers, 90 minutes

---

## Pre-session (15 min before)
- Send the one-pager (one_pager.html) to participants 24h ahead
- Ask them to read it once before the session
- Print 1 copy of one-pager per participant

## Opening (10 min)
1. Frame the session: "We are NOT here to defer to the AI Council. We are here to use its perspectives as a structured starting point for our own thinking."
2. Have each participant share their initial reaction in 1 sentence: "What surprised you, what felt off, what did you find useful?"

## Round 1: Surface the dynamics (25 min)

Use the **distribution table** from the briefing.

{distribution_summary}

Questions to facilitate:
- Where in our team does each voice tend to be represented? Who tends to argue from Q (measurement), S (systems), E (engineering), H (humanist), or C (contrarian) positions?
- Which voice is most absent in our usual conversations? Why?
- If we had to physically embody each voice, who in this room would naturally take which?

## Round 2: Examine the hidden disagreement (20 min)

{hidden_section}

Questions to facilitate:
- If we proceeded with the apparent consensus, which framing would actually drive our execution? Who would set the metrics, the priorities, the tone?
- Have we conflated agreement-on-outcome with agreement-on-reasons before, in this team? What was the cost?

## Round 3: Probe the blind spots (15 min)

{blind_spots_section}

Questions to facilitate:
- Is there an axis here that we, as a team, also routinely underweight? Why?
- If we deliberately overweighted this dimension, which option would emerge as best?

## Round 4: Work through the operator questions (15 min)

Pick the 2-3 questions from the briefing that hit closest to home. Discuss as a group.

## Closing (5 min)
- Each participant: one decision or action they'll take as a result of this conversation
- Identify the SINGLE most uncomfortable question the briefing surfaced and assign someone to bring it back next session

---

## Facilitator notes

- This briefing is structured, not authoritative. If participants treat it as oracle, push back: "The AI Council is a tool. We are the decision-makers."
- The hidden-disagreement insight is often the most valuable - lean into it.
- Resist the urge to "land on a decision" within 90 minutes if the team needs more time. The briefing's job is to surface, not resolve.
"""


def render_session_guide(insight: dict) -> str:
    cm = insight["consensus_map"]
    dist = cm.get("distribution", {})
    if dist:
        majority = cm.get("majority_recommendation")
        if majority:
            n_majority = dist.get(majority, 0)
            dist_summary = (
                f"The five voices recommended:\n\n"
                + "\n".join(f"- **Option {o}**: {n} voice(s)" for o, n in sorted(dist.items()))
                + f"\n\nMajority (option {majority}) carried {n_majority} of 5 voices."
            )
        else:
            dist_summary = "The five voices were split across all options - no majority emerged."
    else:
        dist_summary = "Recommendations could not be parsed clearly."

    hidden = insight["hidden_disagreement"]
    if hidden.get("status") == "computed":
        hidden_section = "**" + hidden.get("interpretation", "") + "**"
    else:
        hidden_section = "Hidden disagreement analysis was not applicable to this case (no clear majority)."

    blind = insight["blind_spots"]
    if blind.get("low_discrimination_constructs"):
        items = []
        for c in blind["low_discrimination_constructs"]:
            items.append(
                f"- **{c['left_pole']} &harr; {c['right_pole']}**: all options "
                f"scored near the middle. Worth probing whether this dimension "
                f"should be weighted more strongly."
            )
        blind_section = "Constructs where all options scored near the middle:\n\n" + "\n".join(items)
    else:
        blind_section = "No obvious blind spots detected."

    condition_label = "neutral framing" if insight["condition"] == "N" else "persona framing"

    return SESSION_GUIDE.format(
        cell_id=insight["cell_id"],
        task=insight["task"],
        condition_label=condition_label,
        distribution_summary=dist_summary,
        hidden_section=hidden_section,
        blind_spots_section=blind_section,
    )


# ============================================================
# Main
# ============================================================
def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--cell", default=None)
    args = p.parse_args()

    COACH_DIR.mkdir(exist_ok=True)
    insights = load_insights()
    if not insights:
        return 1

    if args.cell:
        insights = [i for i in insights if i["cell_id"] == args.cell]

    for insight in insights:
        cid = insight["cell_id"]
        cell = load_cell_raw(cid)
        if not cell:
            continue
        out_dir = COACH_DIR / cid
        out_dir.mkdir(exist_ok=True)

        html_out = render_one_pager(insight, cell)
        (out_dir / "one_pager.html").write_text(html_out, encoding="utf-8")

        guide = render_session_guide(insight)
        (out_dir / "session_guide.md").write_text(guide, encoding="utf-8")

        # Quick facilitator questions
        qs = insight.get("operator_questions", [])
        fq = "# Facilitator questions for " + cid + "\n\n"
        for i, q in enumerate(qs, 1):
            fq += f"{i}. {q}\n\n"
        (out_dir / "facilitator_questions.md").write_text(fq, encoding="utf-8")

        print(f"  {cid}: wrote one_pager.html, session_guide.md, facilitator_questions.md")

    print(f"\nCoach kit ready in {COACH_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
