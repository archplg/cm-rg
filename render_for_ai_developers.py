#!/usr/bin/env python3
"""
Renders operator_insight.json into formats useful for AI/ML DEVELOPERS
building multi-agent systems.

Outputs (per cell):
- ai_audit/<cell>/audit_report.md - audit-style report with metrics and flags
- ai_audit/<cell>/audit_report.json - machine-readable audit summary
- ai_audit/aggregate_dashboard.html - dashboard across all cells

Also writes a minimal demo library skeleton:
- ai_audit/archipelago_audit/__init__.py - the importable Python package
- ai_audit/archipelago_audit/README.md - usage docs

Run:
    python render_for_ai_developers.py
"""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path

OPERATOR_DIR = Path("./operator_outputs")
AUDIT_DIR = Path("./ai_audit")


def load_insights():
    p = OPERATOR_DIR / "all_insights.json"
    if not p.exists():
        print("Run operator_synthesis.py first.")
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def severity_for(insight: dict) -> tuple[str, str]:
    """Return (severity, reason)."""
    cm = insight["consensus_map"]
    hidden = insight["hidden_disagreement"]
    score = hidden.get("reasoning_diversity_score", 0) if hidden.get("status") == "computed" else 0
    strength = cm.get("consensus_strength")

    if strength == "strong" and score > 1.0:
        return ("HIGH", f"Strong reported consensus hides substantial reasoning-level disagreement (RMSE={score:.2f}).")
    if strength == "strong" and score > 0.5:
        return ("MEDIUM", f"Strong consensus with moderate framing differences (RMSE={score:.2f}). Probe reasoning before deployment.")
    if strength == "strong":
        return ("LOW", "Genuine consensus: agents agree on output AND reasoning.")
    if strength == "partial":
        return ("MEDIUM", "Partial consensus; dissenting voices may carry information lost to majority aggregation.")
    if strength == "split":
        return ("INFO", "Agents are split; standard aggregation would average over genuine disagreement.")
    return ("MEDIUM", "Mixed signal; review the case-by-case detail.")


# ============================================================
# Per-cell audit report
# ============================================================
AUDIT_TEMPLATE = """# Multi-Agent Decision Audit

**Audit subject:** `{cell_id}`
**Task domain:** {task}
**Configuration:** {condition_label}, run {run_idx}
**Date generated:** see `operator_insight.json`

---

## Severity: {severity}

> {severity_reason}

## Headline

{headline}

## Reasoning agreement network

![Reasoning agreement network]({network_path})

{network_interpretation}

## Cross-cell context

This case sits in the broader experimental landscape:

![Cross-cell landscape](../cross_cell/landscape.png)

## Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Agents in ensemble | {n_agents} | Number of models that produced recommendations |
| Distinct recommendations | {n_distinct_rec} | Output-level diversity |
| Consensus strength | `{consensus_strength}` | strong=4-5 agree; partial=3; split=<3 |
| Reasoning diversity (RMSE in rating space) | {reasoning_diversity:.3f} | 0 = identical reasoning, 2+ = substantially different |
| Blind-spot constructs | {n_blind_spots} | Dimensions where all options scored mid-scale (4 +/- 1) |

## Pairwise reasoning distance heatmap

![Disagreement heatmap]({heatmap_path})

{heatmap_interpretation}

## Recommendations distribution

```
{dist_block}
```

![Consensus split]({consensus_path})

{consensus_interpretation}

## Agent fingerprints

{agent_table}

## Decision space (PCA biplot)

![Decision-space biplot]({biplot_path})

{biplot_interpretation}

## Hidden disagreement detail

{hidden_block}

## Risk surface (minority concerns)

{risks_block}

## Operator action items

{questions_block}

---

## How to use this audit in your pipeline

```python
from archipelago_audit import AuditResult
result = AuditResult.load("operator_outputs/{cell_id}/operator_insight.json")
if result.severity == "HIGH":
    # block deployment, route to human review
    raise EnsembleConvergenceAlert(result.headline)
elif result.severity == "MEDIUM":
    # log but continue
    logger.warning(result.headline)
```
"""


def _read_interp(cell_id: str, viz_name: str) -> str:
    """Read interpretation markdown for a viz; return empty string if missing."""
    p = Path("./analysis") / cell_id / f"{viz_name}.interpretation.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _viz_relpath(cell_id: str, viz_name: str) -> str:
    """Path relative to ai_audit/<cell>/audit_report.md location."""
    src = Path("./analysis") / cell_id / f"{viz_name}.png"
    if not src.exists():
        return ""
    # Copy into ai_audit/<cell>/viz/ for self-containment
    target_dir = AUDIT_DIR / cell_id / "viz"
    target_dir.mkdir(parents=True, exist_ok=True)
    import shutil
    target = target_dir / src.name
    shutil.copy(src, target)
    return f"viz/{src.name}"


def render_audit_md(insight: dict) -> str:
    cm = insight["consensus_map"]
    hidden = insight["hidden_disagreement"]
    blind = insight["blind_spots"]
    risks = insight["risk_surface"]
    severity, severity_reason = severity_for(insight)

    dist = cm.get("distribution", {})
    dist_block = "\n".join(
        f"  Option {opt}: {'#' * n} ({n})"
        for opt, n in sorted(dist.items())
    ) or "  (no parsed recommendations)"

    rows = ["| Agent | Persona | Recommendation | Model |", "|---|---|---|---|"]
    for sn, info in cm.get("by_agent", {}).items():
        rows.append(
            f"| {sn} | {info.get('persona', '?')} | "
            f"{info.get('recommendation') or '—'} | "
            f"`{info.get('model_id', '?')}` |"
        )
    agent_table = "\n".join(rows)

    if hidden.get("status") == "computed":
        score = hidden.get("reasoning_diversity_score", 0)
        hidden_block = (
            f"- **Reasoning diversity score:** {score:.3f}\n"
            f"- **Agents in majority consensus:** "
            f"{', '.join(hidden.get('agents_in_consensus', []))}\n"
            f"- **Max pairwise RMSE:** {hidden.get('max_distance', 0):.3f}\n\n"
            f"{hidden.get('interpretation', '')}"
        )
    else:
        hidden_block = f"Status: {hidden.get('status', 'unknown')}. {hidden.get('interpretation', '')}"

    if risks.get("risks_by_agent"):
        risk_items = []
        for sn, rlist in risks["risks_by_agent"].items():
            if rlist:
                risk_items.append(f"- **{sn}**: {'; '.join(rlist[:3])}")
        risks_block = "\n".join(risk_items) if risk_items else "_None extracted._"
    else:
        risks_block = "_None extracted._"

    qs = insight.get("operator_questions", [])
    questions_block = "\n".join(f"{i+1}. {q}" for i, q in enumerate(qs)) or "_None generated._"

    return AUDIT_TEMPLATE.format(
        cell_id=insight["cell_id"],
        task=insight["task"],
        condition_label="neutral" if insight["condition"] == "N" else "persona",
        run_idx=insight["run_idx"],
        severity=severity,
        severity_reason=severity_reason,
        headline=insight["headline"],
        n_agents=cm.get("n_agents", 0),
        n_distinct_rec=len(dist),
        consensus_strength=cm.get("consensus_strength", "unknown"),
        reasoning_diversity=hidden.get("reasoning_diversity_score", 0),
        n_blind_spots=len(blind.get("low_discrimination_constructs", [])),
        dist_block=dist_block,
        agent_table=agent_table,
        hidden_block=hidden_block,
        risks_block=risks_block,
        questions_block=questions_block,
        network_path=_viz_relpath(insight["cell_id"], "agreement_network") or "(not generated)",
        network_interpretation=_read_interp(insight["cell_id"], "agreement_network"),
        heatmap_path=_viz_relpath(insight["cell_id"], "disagreement_heatmap") or "(not generated)",
        heatmap_interpretation=_read_interp(insight["cell_id"], "disagreement_heatmap"),
        consensus_path=_viz_relpath(insight["cell_id"], "consensus_vs_reasoning") or "(not generated)",
        consensus_interpretation=_read_interp(insight["cell_id"], "consensus_vs_reasoning"),
        biplot_path=_viz_relpath(insight["cell_id"], "biplot_annotated") or "(not generated)",
        biplot_interpretation=_read_interp(insight["cell_id"], "biplot_annotated"),
    )


# ============================================================
# Aggregate dashboard
# ============================================================
DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Archipelago Audit Dashboard</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 1100px; margin: 30px auto; padding: 0 20px; color: #1a1a1a; }}
h1 {{ font-size: 1.7em; }}
.subtitle {{ color: #666; margin-bottom: 2em; }}
.card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(330px, 1fr)); gap: 16px; }}
.card {{ border: 1px solid #ddd; border-radius: 6px; padding: 18px; background: #fafafa; }}
.card.high {{ border-color: #c44; background: #fdf0ed; }}
.card.medium {{ border-color: #c8a45c; background: #fdfaf2; }}
.card.low {{ border-color: #3a7d44; background: #f0f7ed; }}
.card.info {{ border-color: #aaa; background: #f6f6f6; }}
.cell-id {{ font-family: monospace; font-size: 0.85em; color: #888; }}
.severity {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.75em; font-weight: bold; }}
.severity.high {{ background: #c44; color: white; }}
.severity.medium {{ background: #c8a45c; color: white; }}
.severity.low {{ background: #3a7d44; color: white; }}
.severity.info {{ background: #999; color: white; }}
.metrics {{ font-size: 0.85em; color: #555; margin-top: 10px; }}
table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
th, td {{ text-align: left; padding: 6px 10px; border-bottom: 1px solid #eee; }}
th {{ background: #f6f6f6; }}
</style>
</head>
<body>
<h1>Archipelago Audit Dashboard</h1>
<div class="subtitle">{n_cells} multi-agent decisions analyzed for premature convergence, hidden disagreement, and blind spots.</div>

<h2>Summary</h2>
<table>
<thead><tr><th>Severity</th><th>Count</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td><span class="severity high">HIGH</span></td><td>{n_high}</td><td>Strong reported consensus hides substantial reasoning-level disagreement</td></tr>
<tr><td><span class="severity medium">MEDIUM</span></td><td>{n_medium}</td><td>Mixed signals worth case-by-case review</td></tr>
<tr><td><span class="severity low">LOW</span></td><td>{n_low}</td><td>Genuine consensus on output AND reasoning</td></tr>
<tr><td><span class="severity info">INFO</span></td><td>{n_info}</td><td>Agents split; no consensus claim</td></tr>
</tbody>
</table>

<h2>Per-cell audit cards</h2>
<div class="card-grid">
{cards}
</div>

<p style="margin-top: 3em; color: #888; font-size: 0.8em;">
Generated from operator_outputs/. Individual audit reports in ai_audit/&lt;cell_id&gt;/.
</p>

</body>
</html>
"""


def render_dashboard(insights: list) -> str:
    n_high = sum(1 for i in insights if severity_for(i)[0] == "HIGH")
    n_medium = sum(1 for i in insights if severity_for(i)[0] == "MEDIUM")
    n_low = sum(1 for i in insights if severity_for(i)[0] == "LOW")
    n_info = sum(1 for i in insights if severity_for(i)[0] == "INFO")

    cards = []
    for i in insights:
        sev, reason = severity_for(i)
        cm = i["consensus_map"]
        hidden = i["hidden_disagreement"]
        cards.append(
            f'<div class="card {sev.lower()}">'
            f'<div class="cell-id">{html.escape(i["cell_id"])}</div>'
            f'<h3>Task {html.escape(str(i["task"]))} '
            f'<span class="severity {sev.lower()}">{sev}</span></h3>'
            f'<p>{html.escape(i["headline"])}</p>'
            f'<div class="metrics">'
            f'Consensus: <strong>{cm.get("consensus_strength", "?")}</strong>; '
            f'Reasoning diversity: <strong>{hidden.get("reasoning_diversity_score", 0):.2f}</strong>; '
            f'Blind spots: <strong>{len(i["blind_spots"].get("low_discrimination_constructs", []))}</strong>'
            f'</div>'
            f'</div>'
        )

    return DASHBOARD_TEMPLATE.format(
        n_cells=len(insights),
        n_high=n_high,
        n_medium=n_medium,
        n_low=n_low,
        n_info=n_info,
        cards="\n".join(cards),
    )


# ============================================================
# Minimal library skeleton
# ============================================================
LIB_INIT = '''"""
archipelago_audit - Cognitive diversity audit for multi-agent LLM systems.

Quick start:
    from archipelago_audit import AuditResult

    # Load an audit produced by the experimental pipeline
    result = AuditResult.load("operator_outputs/B_P_run1/operator_insight.json")
    print(result.headline)
    print(result.severity)

    # Block deployment if severity is high
    if result.is_blocking():
        raise RuntimeError(f"Ensemble audit failed: {result.headline}")
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AuditResult:
    """Loaded operator_insight.json with convenient accessors."""
    raw: dict

    @classmethod
    def load(cls, path: str | Path) -> "AuditResult":
        with open(path, "r", encoding="utf-8") as f:
            return cls(raw=json.load(f))

    @property
    def cell_id(self) -> str:
        return self.raw.get("cell_id", "?")

    @property
    def headline(self) -> str:
        return self.raw.get("headline", "")

    @property
    def consensus_strength(self) -> str:
        return self.raw["consensus_map"].get("consensus_strength", "unknown")

    @property
    def reasoning_diversity_score(self) -> float:
        return float(self.raw["hidden_disagreement"].get("reasoning_diversity_score", 0))

    @property
    def severity(self) -> str:
        if self.consensus_strength == "strong" and self.reasoning_diversity_score > 1.0:
            return "HIGH"
        if self.consensus_strength == "strong" and self.reasoning_diversity_score < 0.3:
            return "LOW"
        if self.consensus_strength == "split":
            return "INFO"
        return "MEDIUM"

    def is_blocking(self) -> bool:
        return self.severity == "HIGH"

    def operator_questions(self) -> list[str]:
        return self.raw.get("operator_questions", [])

    def blind_spots(self) -> list[dict]:
        return self.raw["blind_spots"].get("low_discrimination_constructs", [])


__all__ = ["AuditResult"]
'''

LIB_README = '''# archipelago_audit

A behavioral interpretability layer for multi-agent LLM systems.

## What it does

When you run an ensemble of LLM agents on a decision, this library lets you ask:

- Did they really agree, or are they pretending to?
- What dimensions of the problem did they collectively underweight?
- What risks did minority agents raise that majority-voting drowned out?
- Should an operator block this decision and route to human review?

## What it does NOT do

- It does not run your agents for you. Use OpenRouter, LangChain, CrewAI, your stack.
- It does not improve agent accuracy. It improves your visibility into how agents reasoned.
- It is not a substitute for human judgment on consequential decisions.

## Status

Alpha. Built from a research experiment on 5 frontier models across 3 task types.

## Citation

If you use this in research, please cite the accompanying paper (in preparation).
'''


def write_library_skeleton(out_dir: Path) -> None:
    lib_dir = out_dir / "archipelago_audit"
    lib_dir.mkdir(parents=True, exist_ok=True)
    (lib_dir / "__init__.py").write_text(LIB_INIT, encoding="utf-8")
    (lib_dir / "README.md").write_text(LIB_README, encoding="utf-8")


# ============================================================
# Main
# ============================================================
def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--cell", default=None)
    args = p.parse_args()

    AUDIT_DIR.mkdir(exist_ok=True)
    insights = load_insights()
    if not insights:
        return 1

    if args.cell:
        insights = [i for i in insights if i["cell_id"] == args.cell]

    for i in insights:
        out_dir = AUDIT_DIR / i["cell_id"]
        out_dir.mkdir(exist_ok=True)
        (out_dir / "audit_report.md").write_text(render_audit_md(i), encoding="utf-8")
        # Machine-readable summary
        sev, reason = severity_for(i)
        machine = {
            "cell_id": i["cell_id"],
            "severity": sev,
            "severity_reason": reason,
            "headline": i["headline"],
            "consensus_strength": i["consensus_map"].get("consensus_strength"),
            "reasoning_diversity_score": i["hidden_disagreement"].get("reasoning_diversity_score", 0),
            "n_blind_spots": len(i["blind_spots"].get("low_discrimination_constructs", [])),
        }
        with open(out_dir / "audit_summary.json", "w", encoding="utf-8") as f:
            json.dump(machine, f, indent=2, ensure_ascii=False)
        print(f"  {i['cell_id']}: {sev} - {i['headline'][:90]}")

    # Aggregate dashboard
    if not args.cell:
        all_insights = load_insights()
        (AUDIT_DIR / "aggregate_dashboard.html").write_text(
            render_dashboard(all_insights), encoding="utf-8"
        )
        print(f"  Wrote aggregate_dashboard.html")

        # Library skeleton
        write_library_skeleton(AUDIT_DIR)
        print(f"  Wrote archipelago_audit/ library skeleton")

    print(f"\nAI/ML audit kit ready in {AUDIT_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
