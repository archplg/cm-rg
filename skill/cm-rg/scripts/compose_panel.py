#!/usr/bin/env python3
"""Compose a diversity-aware model panel from a CM-RG grid.

The original use case of CM-RG: given YOUR task, find out which models will
give you genuinely different perspectives and which will just agree with each
other - then build an orchestration panel that maximizes independent voices.

Usage:
    python compose_panel.py grid.json outdir/ [--k 3] [--must-include slug]

Input : grid.json produced on YOUR task (subagent demo or run_openrouter.py)
Output: outdir/panel.json  - machine-readable recommendation
        outdir/PANEL.md    - human-readable recommendation

Method: pairwise inter-rater agreement r -> distance (1 - r) -> greedy max-min
dispersion selection (classic diversity maximization), plus agreement-bloc
detection (r > 0.7 = one voice), calibration offsets, and a synthesizer pick
(the most central model). Diversity of the panel is a measured fact; "diverse
panel -> more reliable orchestrated answer" is a working hypothesis the tool
states, not proof.

Dependencies: numpy only.
"""
import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

MIN_SHARED_CELLS = 8
BLOC_R = 0.7  # raters with r above this effectively share one evaluative frame


def load(path):
    grid = json.loads(Path(path).read_text(encoding="utf-8"))
    tensors = {e["rater"]: np.array(
        [[np.nan if v is None else float(v) for v in row] for row in e["matrix"]])
        for e in grid["ratings"]}
    return grid, tensors


def pairwise_r(tensors):
    raters = list(tensors)
    R = {}
    for a, b in combinations(raters, 2):
        va, vb = tensors[a].ravel(), tensors[b].ravel()
        mask = ~np.isnan(va) & ~np.isnan(vb)
        if mask.sum() < MIN_SHARED_CELLS or va[mask].std() == 0 or vb[mask].std() == 0:
            R[(a, b)] = None
            continue
        R[(a, b)] = float(np.corrcoef(va[mask], vb[mask])[0, 1])
    return raters, R


def get_r(R, a, b):
    return R.get((a, b), R.get((b, a)))


def blocs(raters, R):
    """Union-find over pairs with r > BLOC_R -> agreement blocs ("one voice")."""
    parent = {m: m for m in raters}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (a, b), r in R.items():
        if r is not None and r > BLOC_R:
            parent[find(a)] = find(b)
    groups = {}
    for m in raters:
        groups.setdefault(find(m), []).append(m)
    return sorted(groups.values(), key=len, reverse=True)


def greedy_panel(raters, R, k, must_include=None):
    """Max-min dispersion: start from the most distant pair, grow greedily."""
    def dist(a, b):
        r = get_r(R, a, b)
        return 1.0 - r if r is not None else 1.0  # unknown agreement = assume diverse

    if k >= len(raters):
        return list(raters)
    if must_include:
        panel = [must_include]
    else:
        pair = max(combinations(raters, 2), key=lambda p: dist(*p))
        panel = list(pair)
    while len(panel) < k:
        rest = [m for m in raters if m not in panel]
        best = max(rest, key=lambda m: min(dist(m, p) for p in panel))
        panel.append(best)
    return panel[:k]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("grid")
    ap.add_argument("outdir")
    ap.add_argument("--k", type=int, default=3, help="panel size (default 3)")
    ap.add_argument("--must-include", default=None,
                    help="model that must be in the panel (e.g. your default model)")
    args = ap.parse_args()

    grid, tensors = load(args.grid)
    raters, R = pairwise_r(tensors)
    if args.must_include and args.must_include not in raters:
        print(f"ERROR: --must-include '{args.must_include}' is not a rater in this grid "
              f"(raters: {', '.join(raters)})")
        return 1

    bloc_list = blocs(raters, R)
    panel = greedy_panel(raters, R, args.k, args.must_include)

    # metrics
    def mean_r(models):
        vals = [get_r(R, a, b) for a, b in combinations(models, 2)]
        vals = [v for v in vals if v is not None]
        return float(np.mean(vals)) if vals else None

    pool_r, panel_r = mean_r(raters), mean_r(panel)
    centrality = {m: float(np.mean([v for p in raters if p != m
                                    for v in [get_r(R, m, p)] if v is not None]))
                  for m in raters}
    synthesizer = max(centrality, key=centrality.get)
    calibration = {m: round(float(np.nanmean(t)), 3) for m, t in tensors.items()}
    group_mean = float(np.mean(list(calibration.values())))

    dup_warnings = [
        {"pair": [a, b], "r": round(get_r(R, a, b), 3)}
        for a, b in combinations(panel, 2)
        if get_r(R, a, b) is not None and get_r(R, a, b) > BLOC_R
    ]
    real_voices = len(blocs(panel, {p: r for p, r in R.items()
                                    if p[0] in panel and p[1] in panel}))

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    result = {
        "task": grid.get("meta", {}).get("task", "?"),
        "date": grid.get("meta", {}).get("date", "?"),
        "pool": raters,
        "panel": panel,
        "panel_size": len(panel),
        "effective_independent_voices": real_voices,
        "pool_mean_r": None if pool_r is None else round(pool_r, 3),
        "panel_mean_r": None if panel_r is None else round(panel_r, 3),
        "agreement_blocs": bloc_list,
        "bloc_threshold_r": BLOC_R,
        "synthesizer_suggestion": synthesizer,
        "centrality_mean_r": {m: round(v, 3) for m, v in centrality.items()},
        "calibration_offsets": {m: round(v - group_mean, 3) for m, v in calibration.items()},
        "duplicate_warnings": dup_warnings,
        "pairwise_r": {f"{a} x {b}": (None if r is None else round(r, 3))
                       for (a, b), r in R.items()},
    }
    (out / "panel.json").write_text(json.dumps(result, indent=2, ensure_ascii=False),
                                    encoding="utf-8")

    # human-readable report
    lines = [
        f"# Panel recommendation: {result['task']}",
        "",
        f"*From a CM-RG grid of {len(raters)} models, {result['date']}. "
        f"Pool mean pairwise r = {result['pool_mean_r']}.*",
        "",
        "## Recommended panel",
        "",
    ]
    for m in panel:
        tags = []
        b = next((i for i, bl in enumerate(bloc_list) if m in bl and len(bl) > 1), None)
        tags.append(f"bloc {b + 1} representative" if b is not None else "independent voice")
        off = result["calibration_offsets"][m]
        if abs(off) >= 0.2:
            tags.append(f"rates {'high' if off > 0 else 'low'} ({off:+.2f})")
        lines.append(f"- **{m}** ({'; '.join(tags)})")
    lines += [
        "",
        f"Panel mean pairwise r = {result['panel_mean_r']} vs pool {result['pool_mean_r']} "
        f"(lower = more independent perspectives). Effective independent voices in the "
        f"panel: **{real_voices} of {len(panel)}**.",
        "",
        "## Agreement blocs in the pool (r > 0.7 = effectively one voice)",
        "",
    ]
    for i, bl in enumerate(bloc_list, 1):
        lines.append(f"- Bloc {i}: {', '.join(bl)}" + ("" if len(bl) > 1 else " (solo)"))
    if dup_warnings:
        lines += ["", "**Warning:** the panel still contains near-duplicates: " +
                  "; ".join(f"{w['pair'][0]} x {w['pair'][1]} (r={w['r']})" for w in dup_warnings) +
                  ". This pool cannot supply more independent voices - to add real "
                  "diversity, extend the pool (another lab, another tier) and re-run."]
    lines += [
        "",
        "## Calibration offsets (vs pool mean rating)",
        "",
    ]
    for m in raters:
        off = result["calibration_offsets"][m]
        lines.append(f"- {m}: {off:+.2f}")
    lines += [
        "",
        "## How to orchestrate",
        "",
        f"1. Query each panel model **independently** - no cross-talk before answers "
        f"are in (independence is what diversity buys you).",
        f"2. Synthesize with **{synthesizer}** (most central model, mean r = "
        f"{result['centrality_mean_r'][synthesizer]} with the pool) - or have it "
        f"chair a comparison of the panel's answers.",
        "3. If panel answers **converge**, treat that as a strong signal only when it "
        "crosses bloc boundaries - agreement inside one bloc is one opinion, not "
        "several.",
        "4. When aggregating numeric scores from these models, subtract each rater's "
        "calibration offset (listed above) before averaging.",
        "",
        "## Honest limits",
        "",
        "Panel diversity is measured; the claim that a diverse panel yields a more "
        "reliable orchestrated answer is a working hypothesis (supported by ensemble "
        "literature, not proven by this run). This grid is one task, one run: "
        "agreement structure is task-conditional - re-measure for a very different "
        "task, or rely on the published 36-model atlas as a prior.",
    ]
    (out / "PANEL.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({k: result[k] for k in
                      ["panel", "effective_independent_voices", "panel_mean_r",
                       "pool_mean_r", "synthesizer_suggestion"]}, indent=2))
    print(f"\nWritten: panel.json, PANEL.md -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
