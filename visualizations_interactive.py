#!/usr/bin/env python3
"""
Generate INTERACTIVE HTML visualizations for each cell.

The static PNGs (from visualizations.py) are good for embedding in reports,
but for real exploration the user needs:
- Click on an agent -> see their full response, their constructs, their ratings
- Click on a connection -> see WHICH constructs the two agents disagreed on
- Toggle views: by recommendation / by frame / by reasoning distance
- Hover -> highlight neighbors

This uses Cytoscape.js loaded via CDN. Output is a single self-contained
HTML file per cell that opens in any modern browser, no install needed.

Run:
    python visualizations_interactive.py
    python visualizations_interactive.py --cell B_N_run1
"""
from __future__ import annotations
import argparse
import json
from itertools import combinations
from pathlib import Path

import numpy as np

RESULTS_DIR = Path("./results")
OPERATOR_DIR = Path("./operator_outputs")
ANALYSIS_DIR = Path("./analysis")


# Persona colors (same as static viz for consistency)
PERSONA_COLORS = {
    "Q": "#0a558c", "S": "#2d8659", "E": "#8a5a00",
    "H": "#882b6f", "C": "#b03030", "neutral": "#666666",
}
PERSONA_LABELS = {
    "Q": "Quantitative-Empiricist",
    "S": "Systems-Strategist",
    "E": "First-principles Engineer",
    "H": "Humanist-Ethicist",
    "C": "Contrarian-Skeptic",
    "neutral": "Neutral framing",
}
REC_COLORS = {
    "A": "#1f77b4", "B": "#ff7f0e", "C": "#2ca02c",
    "D": "#d62728", "E": "#9467bd",
}


def load_cell(cell_id: str) -> dict | None:
    p = RESULTS_DIR / cell_id / "cell.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def load_insight(cell_id: str) -> dict | None:
    p = OPERATOR_DIR / cell_id / "operator_insight.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def build_pairwise_data(cell: dict) -> tuple[dict, list]:
    """For each agent pair, compute RMSE AND find top differing constructs."""
    # Build per-agent rating vectors
    all_constructs = []
    for sn in sorted(cell.get("constructs", {}).keys()):
        all_constructs.extend(cell["constructs"][sn])
    construct_ids = [c["id"] for c in all_constructs]
    construct_meta = {c["id"]: c for c in all_constructs}
    elements = sorted(cell.get("element_summaries", {}).keys())

    fingerprints = {}
    for rater, ratings in cell.get("ratings", {}).items():
        vec = {}
        for cid in construct_ids:
            for ek in elements:
                v = ratings.get(cid, {}).get(ek)
                vec[(cid, ek)] = float(v) if v is not None else None
        fingerprints[rater] = vec

    agents = sorted(fingerprints.keys())
    pairs = {}
    for a, b in combinations(agents, 2):
        va, vb = fingerprints[a], fingerprints[b]
        # Per-construct deltas
        per_cell_diffs = []
        per_construct = {}
        for (cid, ek), va_val in va.items():
            vb_val = vb.get((cid, ek))
            if va_val is None or vb_val is None:
                continue
            d = va_val - vb_val
            per_cell_diffs.append(abs(d))
            per_construct.setdefault(cid, []).append(abs(d))
        if not per_cell_diffs:
            continue
        rmse = float(np.sqrt(np.mean([d * d for d in per_cell_diffs])))
        # Find top 3 constructs where they differed
        construct_mean_diff = {cid: float(np.mean(diffs))
                               for cid, diffs in per_construct.items()}
        top_diffs = sorted(construct_mean_diff.items(),
                           key=lambda x: -x[1])[:3]
        top_diffs_named = [
            {
                "construct_id": cid,
                "construct_label": f"{construct_meta[cid]['left']} ↔ {construct_meta[cid]['right']}",
                "mean_abs_diff": diff,
                "agent_a_ratings": {
                    ek: fingerprints[a].get((cid, ek)) for ek in elements
                },
                "agent_b_ratings": {
                    ek: fingerprints[b].get((cid, ek)) for ek in elements
                },
            }
            for cid, diff in top_diffs
            if cid in construct_meta
        ]
        pairs[f"{a}__{b}"] = {
            "source": a,
            "target": b,
            "rmse": rmse,
            "top_differing_constructs": top_diffs_named,
        }
    return pairs, agents


def build_graph_data(cell: dict, insight: dict) -> dict:
    """Build the JSON data structure that Cytoscape.js consumes, plus side-panel data."""
    by_agent = insight["consensus_map"]["by_agent"]
    pairs, agents = build_pairwise_data(cell)

    # Get model_id and persona from api_calls (phase1_freeresponse)
    model_id_by_sn = {}
    persona_by_sn = {}
    for call in cell.get("api_calls", []):
        if call["phase"] == "phase1_freeresponse":
            model_id_by_sn[call["model_short_name"]] = call["model_id_used"]
            persona_by_sn[call["model_short_name"]] = call["persona_or_neutral"]

    nodes = []
    for sn in agents:
        info = by_agent.get(sn, {})
        persona = info.get("persona") or persona_by_sn.get(sn, "neutral")
        rec = info.get("recommendation")
        full_response = cell.get("free_responses", {}).get(sn, "")
        # Constructs owned by this agent
        own_constructs = cell.get("constructs", {}).get(sn, [])
        # Triad assignments
        triads = cell.get("triad_assignments", {}).get(sn, [])
        nodes.append({
            "data": {
                "id": sn,
                "label": sn,
                "persona": persona,
                "persona_label": PERSONA_LABELS.get(persona, persona),
                "persona_color": PERSONA_COLORS.get(persona, PERSONA_COLORS["neutral"]),
                "recommendation": rec or "?",
                "rec_color": REC_COLORS.get(rec, "#cccccc"),
                "model_id": model_id_by_sn.get(sn, "?"),
                "full_response": full_response,
                "rationale_snippet": info.get("rationale_snippet", ""),
                "constructs": own_constructs,
                "triads": triads,
            }
        })

    edges = []
    rmses = [p["rmse"] for p in pairs.values()] or [0]
    max_rmse = max(rmses) if rmses else 1.0
    min_rmse = min(rmses) if rmses else 0.0
    rmse_range = max_rmse - min_rmse + 1e-6

    for pid, pdata in pairs.items():
        rmse = pdata["rmse"]
        # Edge color: green-amber-red by RMSE thresholds
        if rmse < 0.5:
            color = "#3a7d44"
            level = "strong-alignment"
        elif rmse < 1.0:
            color = "#c8a45c"
            level = "moderate"
        else:
            color = "#c44"
            level = "substantial-disagreement"
        # Edge width: inversely proportional to RMSE within this cell
        normalized = 1.0 - (rmse - min_rmse) / rmse_range
        width = 1.5 + normalized * 8.0
        edges.append({
            "data": {
                "id": pid,
                "source": pdata["source"],
                "target": pdata["target"],
                "rmse": round(rmse, 3),
                "level": level,
                "color": color,
                "width": width,
                "top_differing_constructs": pdata["top_differing_constructs"],
                "label": f"{rmse:.2f}",
            }
        })

    return {"nodes": nodes, "edges": edges}


# ============================================================
# HTML template
# ============================================================
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Interactive AI Council - {cell_id}</title>
<script src="https://unpkg.com/cytoscape@3.30.2/dist/cytoscape.min.js"></script>
<script src="https://unpkg.com/layout-base@2.0.1/layout-base.js"></script>
<script src="https://unpkg.com/cose-base@2.2.0/cose-base.js"></script>
<script src="https://unpkg.com/cytoscape-cose-bilkent@4.1.0/cytoscape-cose-bilkent.js"></script>
<style>
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Georgia, sans-serif;
       margin: 0; padding: 0; background: #f4f1e8; color: #1a1a1a; }}
.header {{ background: #2b3a55; color: white; padding: 14px 24px; }}
.header h1 {{ margin: 0; font-size: 1.2em; }}
.header .subtitle {{ font-size: 0.85em; opacity: 0.85; margin-top: 3px; }}
.layout {{ display: flex; height: calc(100vh - 60px); }}
#graph-container {{ flex: 1; background: #f9f7f0; position: relative; }}
#cy {{ width: 100%; height: 100%; }}
.legend {{ position: absolute; bottom: 16px; left: 16px;
           background: rgba(255,255,255,0.96); padding: 12px 16px;
           border-radius: 6px; border: 1px solid #d8d0bf; font-size: 0.82em;
           max-width: 280px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }}
.legend h3 {{ margin: 0 0 8px; font-size: 0.9em; color: #2b3a55; }}
.legend-row {{ display: flex; align-items: center; margin: 4px 0; }}
.legend-swatch {{ display: inline-block; width: 24px; height: 4px; margin-right: 8px;
                  border-radius: 2px; }}
.legend-dot {{ display: inline-block; width: 14px; height: 14px; margin-right: 8px;
               border-radius: 50%; }}
.help {{ position: absolute; top: 16px; left: 16px;
         background: rgba(255,255,255,0.96); padding: 10px 14px;
         border-radius: 6px; border: 1px solid #d8d0bf; font-size: 0.8em;
         color: #555; max-width: 320px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }}
.controls {{ position: absolute; top: 16px; right: 16px;
             background: rgba(255,255,255,0.96); padding: 10px 14px;
             border-radius: 6px; border: 1px solid #d8d0bf; font-size: 0.85em;
             box-shadow: 0 2px 6px rgba(0,0,0,0.08); }}
.controls button {{ display: block; width: 100%; padding: 6px 10px; margin: 3px 0;
                    background: white; border: 1px solid #c8a45c; border-radius: 4px;
                    cursor: pointer; font-size: 0.9em; }}
.controls button.active {{ background: #c8a45c; color: white; }}
.controls button:hover {{ background: #e6dfc9; }}
.controls button.active:hover {{ background: #b8945a; }}

#info-panel {{ width: 420px; background: white; border-left: 1px solid #d8d0bf;
               overflow-y: auto; padding: 20px 24px; }}
#info-panel h2 {{ font-size: 1.1em; margin: 0 0 8px; color: #2b3a55;
                  border-bottom: 2px solid #c8a45c; padding-bottom: 6px; }}
#info-panel h3 {{ font-size: 0.95em; margin: 18px 0 6px; color: #2b3a55; }}
#info-panel h4 {{ font-size: 0.85em; margin: 12px 0 4px; color: #555;
                  text-transform: uppercase; letter-spacing: 0.5px; }}
#info-panel .placeholder {{ color: #888; font-style: italic; }}
.badge {{ display: inline-block; padding: 2px 9px; border-radius: 11px;
          font-size: 0.78em; font-weight: 600; color: white; margin-right: 4px; }}
.kv {{ margin: 6px 0; font-size: 0.92em; }}
.kv strong {{ color: #555; }}
.response-text {{ font-size: 0.88em; line-height: 1.55; color: #333;
                  background: #faf8f1; padding: 12px 14px; border-radius: 4px;
                  border-left: 3px solid #c8a45c; }}
.construct-card {{ font-size: 0.85em; margin: 6px 0; padding: 8px 11px;
                   background: #faf8f1; border-radius: 4px;
                   border-left: 3px solid {persona_color_for_default}; }}
.construct-pole {{ display: inline; padding: 2px 6px; background: white;
                   border-radius: 3px; border: 1px solid #e6dfc9;
                   font-family: Georgia, serif; }}
.rating-grid {{ display: grid; grid-template-columns: 60px repeat(5, 1fr);
                gap: 2px; margin: 8px 0; font-size: 0.78em; }}
.rg-cell {{ padding: 4px 6px; background: #f4f1e8; text-align: center;
            border-radius: 3px; }}
.rg-cell.head {{ background: #2b3a55; color: white; font-weight: 600; }}
.rg-cell.diff-high {{ background: #fdc; }}
.rg-cell.diff-med {{ background: #ffe9c0; }}
.rg-cell.diff-low {{ background: #e2efd9; }}
.alert-banner {{ padding: 10px 14px; border-radius: 5px; margin: 10px 0;
                 font-size: 0.9em; }}
.alert-danger {{ background: #fdf0ed; border-left: 4px solid #c44;
                 color: #6b1313; }}
.alert-warn {{ background: #fdfaf2; border-left: 4px solid #c8a45c;
               color: #6b4920; }}
.alert-ok {{ background: #f0f7ed; border-left: 4px solid #3a7d44;
             color: #1f4a26; }}
hr {{ border: none; border-top: 1px solid #e6dfc9; margin: 14px 0; }}
</style>
</head>
<body>

<div class="header">
  <h1>AI Council - Interactive View</h1>
  <div class="subtitle">Cell <strong>{cell_id}</strong> &middot; Task {task} &middot; {condition_label}</div>
</div>

<div class="layout">
  <div id="graph-container">
    <div id="cy"></div>

    <div class="help">
      <strong>How to explore:</strong><br>
      &middot; Click a circle (agent) to see their full response and reasoning<br>
      &middot; Click a connecting line to see <em>where</em> two agents disagreed<br>
      &middot; Drag agents around if the layout is hard to read
    </div>

    <div class="controls">
      <strong style="font-size: 0.85em; color: #555;">Layout</strong>
      <button id="btn-cose" class="active">Force-directed</button>
      <button id="btn-circle">Circle</button>
      <button id="btn-grid">Grid</button>
    </div>

    <div class="legend">
      <h3>Reading the network</h3>
      <div><strong>Circle color</strong> = epistemological frame</div>
      <div class="legend-row"><span class="legend-dot" style="background:#0a558c"></span>Quantitative</div>
      <div class="legend-row"><span class="legend-dot" style="background:#2d8659"></span>Systems</div>
      <div class="legend-row"><span class="legend-dot" style="background:#8a5a00"></span>Engineering</div>
      <div class="legend-row"><span class="legend-dot" style="background:#882b6f"></span>Humanist</div>
      <div class="legend-row"><span class="legend-dot" style="background:#b03030"></span>Contrarian</div>
      <div class="legend-row"><span class="legend-dot" style="background:#666"></span>Neutral (no persona)</div>
      <hr>
      <div><strong>Line color</strong> = reasoning agreement</div>
      <div class="legend-row"><span class="legend-swatch" style="background:#3a7d44"></span>RMSE &lt; 0.5 - aligned</div>
      <div class="legend-row"><span class="legend-swatch" style="background:#c8a45c"></span>0.5-1.0 - moderate</div>
      <div class="legend-row"><span class="legend-swatch" style="background:#c44"></span>&gt; 1.0 - substantial</div>
      <hr>
      <div style="color: #555; font-size: 0.92em">
        <strong>Line thickness</strong> = relative agreement within this case<br>
        <strong>RMSE</strong> = root-mean-square error on 7-point rating scale
      </div>
    </div>
  </div>

  <div id="info-panel">
    <h2>{headline}</h2>

    {hidden_banner}

    <div class="kv"><strong>Cell:</strong> {cell_id}</div>
    <div class="kv"><strong>Task:</strong> {task} ({condition_label})</div>
    <div class="kv"><strong>Agents:</strong> {n_agents}</div>
    <div class="kv"><strong>Reasoning RMSE (mean across pairs):</strong> {mean_rmse:.3f}</div>

    <hr>

    <div id="detail-area">
      <div class="placeholder">
        <p>Click an agent or a connecting line to see details here.</p>
        <p>The colored circles are the LLM agents. The lines between them show how similarly they reasoned: thicker and greener means they rated the options in similar patterns, thinner and redder means they disagreed at the level of how they evaluated each option.</p>
        <p>Hidden disagreement is the case where two agents recommend the same option but their connecting line is yellow or red - they agree on the answer but not on the reasoning. Click such a line to see exactly which dimensions they diverged on.</p>
      </div>
    </div>

    <hr>

    <h3>About this view</h3>
    <p style="font-size: 0.85em; color: #555;">
      The reasoning network shows behavioral disagreement, not topic disagreement.
      Two agents with thick green connection rated the options similarly on every
      construct elicited by the panel. Two agents with thin red connection
      saw the options through different evaluative lenses - even if they
      may have recommended the same option in the end.
    </p>

    <p style="font-size: 0.85em; color: #555;">
      Generated by Archipelago. <em>The five voices are LLM analysts; this view is
      decision support, not decision substitution.</em>
    </p>
  </div>
</div>

<script>
const graphData = {graph_data_json};
const insightData = {insight_json};

cytoscape.use(cytoscapeCoseBilkent);

const cy = cytoscape({{
  container: document.getElementById('cy'),
  elements: [...graphData.nodes, ...graphData.edges],
  style: [
    {{
      selector: 'node',
      style: {{
        'background-color': 'data(persona_color)',
        'label': 'data(label)',
        'color': 'white',
        'text-valign': 'center',
        'text-halign': 'center',
        'font-size': '18px',
        'font-weight': 'bold',
        'width': 70,
        'height': 70,
        'border-width': 5,
        'border-color': 'data(rec_color)',
      }}
    }},
    {{
      selector: 'node:selected',
      style: {{
        'border-color': '#2b3a55',
        'border-width': 6,
        'width': 80,
        'height': 80,
      }}
    }},
    {{
      selector: 'edge',
      style: {{
        'line-color': 'data(color)',
        'width': 'data(width)',
        'curve-style': 'bezier',
        'label': 'data(label)',
        'font-size': '11px',
        'text-background-color': 'white',
        'text-background-opacity': 0.85,
        'text-background-padding': 3,
        'text-background-shape': 'round-rectangle',
        'color': '#444',
        'opacity': 0.8,
      }}
    }},
    {{
      selector: 'edge:selected',
      style: {{
        'opacity': 1.0,
        'width': 'mapData(width, 1, 9, 4, 12)',
        'overlay-color': '#c8a45c',
        'overlay-opacity': 0.2,
      }}
    }},
    {{
      selector: '.dimmed',
      style: {{
        'opacity': 0.18,
      }}
    }},
  ],
  layout: {{
    name: 'cose-bilkent',
    quality: 'default',
    randomize: true,
    nodeRepulsion: 8000,
    idealEdgeLength: 220,
    edgeElasticity: 0.45,
    gravity: 0.25,
    numIter: 2500,
    animate: false,
  }},
  wheelSensitivity: 0.2,
  minZoom: 0.3,
  maxZoom: 3,
}});

// Render detail panel for a clicked NODE
function renderNodeDetail(node) {{
  const d = node.data();
  const personaColor = d.persona_color;
  let html = `<h2 style="border-bottom-color: ${{personaColor}}">${{d.label}} - ${{d.persona_label}}</h2>`;
  html += `<div class="kv"><strong>Model:</strong> <code>${{d.model_id}}</code></div>`;
  html += `<div class="kv"><strong>Recommended:</strong> <span class="badge" style="background:${{d.rec_color}}">Option ${{d.recommendation}}</span></div>`;
  html += `<h3>Full response</h3>`;
  html += `<div class="response-text">${{escapeHtml(d.full_response)}}</div>`;
  if (d.constructs && d.constructs.length) {{
    html += `<h3>Bipolar constructs this agent elicited</h3>`;
    html += `<p style="font-size: 0.83em; color: #666;">
      In Phase 3, each agent was given three triads of responses and asked,
      for each triad, to name the bipolar dimension that distinguishes two
      from the third. These are this agent's three constructs.
    </p>`;
    for (const c of d.constructs) {{
      const triadStr = c.triad ? c.triad.join(', ') : '';
      html += `<div class="construct-card" style="border-left-color: ${{personaColor}}">
        <div style="font-size: 0.78em; color: #888; margin-bottom: 4px;">
          <code>${{escapeHtml(c.id)}}</code> &middot; from triad ${{escapeHtml(triadStr)}}
        </div>
        <span class="construct-pole">${{escapeHtml(c.left)}}</span>
        <span style="color:#888"> ↔ </span>
        <span class="construct-pole">${{escapeHtml(c.right)}}</span>
      </div>`;
    }}
  }}
  document.getElementById('detail-area').innerHTML = html;
}}

// Render detail panel for a clicked EDGE
function renderEdgeDetail(edge) {{
  const d = edge.data();
  const src = cy.getElementById(d.source).data();
  const tgt = cy.getElementById(d.target).data();
  let levelLabel, levelClass, levelBg;
  if (d.rmse < 0.5) {{
    levelLabel = 'Strong reasoning alignment';
    levelClass = 'alert-ok';
  }} else if (d.rmse < 1.0) {{
    levelLabel = 'Moderate framing differences';
    levelClass = 'alert-warn';
  }} else {{
    levelLabel = 'Substantial disagreement at the reasoning level';
    levelClass = 'alert-danger';
  }}

  let html = `<h2>${{src.label}} ↔ ${{tgt.label}}</h2>`;
  html += `<div class="kv"><strong>${{src.label}}</strong> (${{src.persona_label}}) recommended <strong>Option ${{src.recommendation}}</strong></div>`;
  html += `<div class="kv"><strong>${{tgt.label}}</strong> (${{tgt.persona_label}}) recommended <strong>Option ${{tgt.recommendation}}</strong></div>`;
  html += `<div class="alert-banner ${{levelClass}}">
    <strong>RMSE = ${{d.rmse}}</strong> - ${{levelLabel}}
  </div>`;

  if (src.recommendation === tgt.recommendation && d.rmse > 0.5) {{
    html += `<div class="alert-banner alert-warn">
      <strong>Hidden disagreement.</strong> Both agents recommended Option ${{src.recommendation}},
      but their underlying reasoning differs (RMSE = ${{d.rmse}}). Standard
      ensemble methods would mask this. The dimensions where they diverged
      most are listed below - probe these before treating this as a robust consensus.
    </div>`;
  }} else if (src.recommendation !== tgt.recommendation) {{
    html += `<div class="alert-banner alert-warn" style="font-size: 0.87em">
      These two agents reached different recommendations. The dimensions where
      they rated options most differently explain why.
    </div>`;
  }}

  if (d.top_differing_constructs && d.top_differing_constructs.length) {{
    html += `<h3>Top dimensions where they rated options differently</h3>`;
    html += `<p style="font-size: 0.83em; color: #666;">
      Each construct below is one of the bipolar dimensions the panel elicited.
      The numbers show how each agent rated each option (E1-E5) on this dimension,
      1-7 scale (1 = strong left pole, 7 = strong right pole). Cells highlighted
      red indicate large rating differences.
    </p>`;
    for (const tc of d.top_differing_constructs) {{
      html += `<div class="construct-card">
        <div style="font-size: 0.83em; color: #666; margin-bottom: 4px;">
          <code>${{escapeHtml(tc.construct_id)}}</code> &middot;
          mean diff: <strong>${{tc.mean_abs_diff.toFixed(2)}}</strong>
        </div>
        <div style="margin-bottom: 8px;">
          <span class="construct-pole">${{escapeHtml(tc.construct_label.split('↔')[0].trim())}}</span>
          <span style="color:#888"> ↔ </span>
          <span class="construct-pole">${{escapeHtml(tc.construct_label.split('↔')[1] ? tc.construct_label.split('↔')[1].trim() : '')}}</span>
        </div>`;
      const elems = Object.keys(tc.agent_a_ratings).sort();
      html += `<div class="rating-grid">
        <div class="rg-cell head">Agent</div>`;
      for (const e of elems) html += `<div class="rg-cell head">${{e}}</div>`;
      html += `<div class="rg-cell" style="background:${{src.persona_color}};color:white;font-weight:600">${{src.label}}</div>`;
      for (const e of elems) {{
        const va = tc.agent_a_ratings[e];
        const vb = tc.agent_b_ratings[e];
        const diff = (va !== null && vb !== null) ? Math.abs(va - vb) : 0;
        const cls = diff >= 3 ? 'diff-high' : diff >= 2 ? 'diff-med' : 'diff-low';
        html += `<div class="rg-cell ${{cls}}">${{va !== null ? va : '-'}}</div>`;
      }}
      html += `<div class="rg-cell" style="background:${{tgt.persona_color}};color:white;font-weight:600">${{tgt.label}}</div>`;
      for (const e of elems) {{
        const va = tc.agent_a_ratings[e];
        const vb = tc.agent_b_ratings[e];
        const diff = (va !== null && vb !== null) ? Math.abs(va - vb) : 0;
        const cls = diff >= 3 ? 'diff-high' : diff >= 2 ? 'diff-med' : 'diff-low';
        html += `<div class="rg-cell ${{cls}}">${{vb !== null ? vb : '-'}}</div>`;
      }}
      html += `</div></div>`;
    }}
  }}
  document.getElementById('detail-area').innerHTML = html;
}}

// Hover highlighting
cy.on('mouseover', 'node', evt => {{
  const node = evt.target;
  cy.elements().not(node.neighborhood()).not(node).addClass('dimmed');
}});
cy.on('mouseout', 'node', () => cy.elements().removeClass('dimmed'));

cy.on('mouseover', 'edge', evt => {{
  const edge = evt.target;
  cy.elements().not(edge.connectedNodes()).not(edge).addClass('dimmed');
}});
cy.on('mouseout', 'edge', () => cy.elements().removeClass('dimmed'));

cy.on('tap', 'node', evt => renderNodeDetail(evt.target));
cy.on('tap', 'edge', evt => renderEdgeDetail(evt.target));
cy.on('tap', evt => {{
  if (evt.target === cy) {{
    document.getElementById('detail-area').innerHTML = `<div class="placeholder">
      <p>Click an agent or a line to see detail.</p></div>`;
  }}
}});

// Layout switching
function setLayout(name) {{
  const opts = {{
    'cose-bilkent': {{ name: 'cose-bilkent', quality: 'default', nodeRepulsion: 8000,
                       idealEdgeLength: 220, animate: false }},
    'circle': {{ name: 'circle', animate: false, radius: 200 }},
    'grid': {{ name: 'grid', animate: false }},
  }};
  cy.layout(opts[name]).run();
}}
document.getElementById('btn-cose').onclick = e => {{
  setActiveBtn(e.target); setLayout('cose-bilkent');
}};
document.getElementById('btn-circle').onclick = e => {{
  setActiveBtn(e.target); setLayout('circle');
}};
document.getElementById('btn-grid').onclick = e => {{
  setActiveBtn(e.target); setLayout('grid');
}};
function setActiveBtn(btn) {{
  document.querySelectorAll('.controls button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}}

function escapeHtml(s) {{
  if (!s) return '';
  return String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/\\n/g, '<br>');
}}

// Auto-fit on load
setTimeout(() => cy.fit(undefined, 60), 100);
</script>

</body>
</html>
"""


def render_interactive_html(cell: dict, insight: dict) -> str:
    graph_data = build_graph_data(cell, insight)

    hidden = insight["hidden_disagreement"]
    score = hidden.get("reasoning_diversity_score", 0) if hidden.get("status") == "computed" else 0
    cm = insight["consensus_map"]

    if cm.get("consensus_strength") == "strong" and score > 1.0:
        banner = (
            '<div class="alert-banner alert-danger"><strong>Danger zone.</strong> '
            'Strong recommendation consensus, but reasoning is substantially '
            'misaligned. Standard ensemble methods mask this. Click the connecting '
            'lines between agents who recommended the same option to see exactly '
            'where they diverged.</div>'
        )
    elif cm.get("consensus_strength") == "strong" and score > 0.5:
        banner = (
            '<div class="alert-banner alert-warn"><strong>Moderate hidden '
            'disagreement.</strong> Most agents agree on the recommendation but '
            'frame it differently. Click lines below to explore.</div>'
        )
    elif cm.get("consensus_strength") == "strong":
        banner = (
            '<div class="alert-banner alert-ok"><strong>Genuine consensus.</strong> '
            'Agents agree on both the output and the reasoning.</div>'
        )
    elif cm.get("consensus_strength") == "split":
        banner = (
            '<div class="alert-banner alert-warn"><strong>Split panel.</strong> '
            'Agents disagree at the recommendation level. The network shows whose '
            'reasoning patterns cluster together.</div>'
        )
    else:
        banner = ""

    # Compute mean RMSE
    rmses = [e["data"]["rmse"] for e in graph_data["edges"]]
    mean_rmse = sum(rmses) / len(rmses) if rmses else 0.0

    return HTML_TEMPLATE.format(
        cell_id=cell["cell_id"],
        task=cell.get("task", "?"),
        condition_label="neutral framing" if cell.get("condition") == "N" else "persona framing",
        headline=insight.get("headline", ""),
        hidden_banner=banner,
        n_agents=cm.get("n_agents", 0),
        mean_rmse=mean_rmse,
        graph_data_json=json.dumps(graph_data),
        insight_json=json.dumps(insight),
        persona_color_for_default="#666",
    )


# ============================================================
# Main
# ============================================================
def process_cell(cell_id: str) -> None:
    cell = load_cell(cell_id)
    insight = load_insight(cell_id)
    if not cell or not insight:
        print(f"  {cell_id}: skipping (missing data)")
        return
    out_dir = ANALYSIS_DIR / cell_id
    out_dir.mkdir(parents=True, exist_ok=True)
    html_text = render_interactive_html(cell, insight)
    out_path = out_dir / "interactive_network.html"
    out_path.write_text(html_text, encoding="utf-8")
    print(f"  {cell_id}: wrote interactive_network.html ({len(html_text) // 1024} KB)")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--cell", default=None)
    args = p.parse_args()
    if args.cell:
        process_cell(args.cell)
    else:
        if not OPERATOR_DIR.exists():
            print("Run operator_synthesis.py first.")
            return 1
        for d in sorted(OPERATOR_DIR.iterdir()):
            if d.is_dir() and (d / "operator_insight.json").exists():
                process_cell(d.name)
    print(f"\nDone. Open each analysis/<cell>/interactive_network.html in any browser.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
