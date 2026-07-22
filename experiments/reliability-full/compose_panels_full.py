#!/usr/bin/env python3
"""Pre-compose the panels for the full reliability experiment from the REAL
Phase 2L pairwise-r matrix - run BEFORE data collection, output goes into the
pre-registration.

Panels:
  D3, D5   - max-diversity (greedy max-min dispersion on 1-r)
  R3, R5   - redundant consensus bloc (top mean-r models)
  ATLAS3   - heuristic: top-consensus Western flagship + Chinese flagship
             + most divergent open-weights model
(TOP-k by individual accuracy and RANDOM-k nulls are defined in analysis,
 post-hoc, from the same singles data.)
"""
import json
from itertools import combinations
from pathlib import Path

catalog = {c["short"]: c for c in json.loads(Path("models_catalog.json").read_text())}
PR = json.loads(Path("pairwise_r.json").read_text())["pairwise_r"]


def r(a, b):
    return PR.get("|".join(sorted([a, b])))


eligible = sorted({s for k in PR for s in k.split("|")} & set(catalog))
mean_r = {m: sum(r(m, o) for o in eligible if o != m and r(m, o) is not None) /
             max(1, sum(1 for o in eligible if o != m and r(m, o) is not None))
          for m in eligible}


def dist(a, b):
    v = r(a, b)
    return 1.0 - v if v is not None else 1.0


def greedy(k):
    pair = max(combinations(eligible, 2), key=lambda p: dist(*p))
    panel = list(pair)
    while len(panel) < k:
        rest = [m for m in eligible if m not in panel]
        panel.append(max(rest, key=lambda m: min(dist(m, p) for p in panel)))
    return panel


def panel_mean_r(panel):
    vals = [r(a, b) for a, b in combinations(panel, 2) if r(a, b) is not None]
    return round(sum(vals) / len(vals), 3) if vals else None


WESTERN = {"anthropic", "openai", "google", "xai"}
CHINESE = {"qwen", "moonshot", "deepseek", "zhipu"}
OPENW = {"meta", "nvidia", "mistral"}  # open-weights-leaning families in the pool

west_f = max((m for m in eligible if catalog[m]["family"] in WESTERN
              and catalog[m]["tier"] == "flagship"), key=lambda m: mean_r[m])
chin_f = max((m for m in eligible if catalog[m]["family"] in CHINESE
              and catalog[m]["tier"] == "flagship"), key=lambda m: mean_r[m])
open_d = min((m for m in eligible if catalog[m]["family"] in OPENW),
             key=lambda m: mean_r[m])

def greedy_within(k, pool):
    pool = list(pool)
    pair = max(combinations(pool, 2), key=lambda p: dist(*p))
    panel = list(pair)
    while len(panel) < k:
        rest = [m for m in pool if m not in panel]
        panel.append(max(rest, key=lambda m: min(dist(m, p) for p in panel)))
    return panel


strong = [m for m in eligible if catalog[m]["tier"] in ("mid", "flagship")]

panels = {
    "D3": greedy(3), "D5": greedy(5),
    "DQ3": greedy_within(3, strong), "DQ5": greedy_within(5, strong),
    "R3": sorted(eligible, key=lambda m: -mean_r[m])[:3],
    "R5": sorted(eligible, key=lambda m: -mean_r[m])[:5],
    "ATLAS3": [west_f, chin_f, open_d],
}
out = {
    "eligible_models": eligible,
    "excluded_no_pairwise_data": sorted(set(catalog) - set(eligible)),
    "mean_r_per_model": {m: round(v, 3) for m, v in
                         sorted(mean_r.items(), key=lambda kv: -kv[1])},
    "panels": {name: {"members": p,
                      "slugs": [catalog[m]["slug"] for m in p],
                      "panel_mean_r": panel_mean_r(p)}
               for name, p in panels.items()},
    "source": "Phase 2L pairwise_r.json (cell-averaged), composed pre-registration",
}
Path("panels.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
for name, p in panels.items():
    print(f"{name}: {p}  mean_r={panel_mean_r(p)}")
print("\ntop consensus:", list(out["mean_r_per_model"])[:5])
print("most divergent:", list(out["mean_r_per_model"])[-5:])
