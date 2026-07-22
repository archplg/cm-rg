#!/usr/bin/env python3
"""Extract the 36-model catalog and cell-averaged pairwise r matrix from
Phase 2L artifacts (config_phase2l.yaml + analysis_results.json).

Outputs: models_catalog.json  [{short, slug, family, tier}]
         pairwise_r.json      {"A_C|A_M": mean_r_across_cells, ...}
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

CONFIG = sys.argv[1] if len(sys.argv) > 1 else "config_phase2l.yaml"
RESULTS = sys.argv[2] if len(sys.argv) > 2 else "analysis_results.json"

# --- catalog from config (id / family / tier / short_name blocks) ---
txt = Path(CONFIG).read_text(encoding="utf-8")
blocks = re.findall(
    r"- id: (\S+)\s*\n(?:\s+fallback_id: \S+\s*\n)?\s+family: (\S+)\s*\n\s+tier: (\S+)\s*\n\s+short_name: (\S+)",
    txt)
catalog = [{"short": s, "slug": i, "family": f, "tier": t} for i, f, t, s in blocks]
assert len(catalog) >= 30, f"expected 30+ models, parsed {len(catalog)}"

# --- pairwise r averaged across (task|condition) cells ---
d = json.loads(Path(RESULTS).read_text(encoding="utf-8"))
acc = defaultdict(list)
for cell, pairs in d["inter_rater_corrs"].items():
    for key, r in pairs.items():
        a, b = key.split("|")
        if a == b or r is None:
            continue
        k = "|".join(sorted([a, b]))
        acc[k].append(float(r))
pairwise = {k: round(sum(v) / len(v), 4) for k, v in acc.items()}
n_cells = {k: len(v) for k, v in acc.items()}

Path("models_catalog.json").write_text(json.dumps(catalog, indent=2), encoding="utf-8")
Path("pairwise_r.json").write_text(json.dumps(
    {"pairwise_r": pairwise, "n_cells_per_pair": n_cells,
     "source": "Phase 2L analysis_results.json, mean across task|condition cells"},
    indent=2), encoding="utf-8")

shorts = {c["short"] for c in catalog}
covered = {s for k in pairwise for s in k.split("|")}
print(f"catalog: {len(catalog)} models; pairs with data: {len(pairwise)}; "
      f"models appearing in r-matrix: {len(covered & shorts)}/{len(shorts)}")
missing = sorted(shorts - covered)
if missing:
    print("no pairwise data (excluded from panel composition):", ", ".join(missing))
