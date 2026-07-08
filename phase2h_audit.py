#!/usr/bin/env python3
"""Phase 2H comprehensive participation audit across all 10 models."""
from __future__ import annotations
import json
import os
import sys

BASE = "results_phase2h"
MODELS = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"]
LABELS = {
    "M1": "Claude Opus 4.7",
    "M2": "GPT-5.5",
    "M3": "Gemini 3.1 Pro",
    "M4": "DeepSeek v4 Pro",
    "M5": "Kimi k2.6",
    "M6": "Mistral Large 2512",
    "M7": "Cohere Command A",
    "M8": "Qwen 3.7 Max",
    "M9": "Llama 4 Maverick",
    "M10": "Grok 4.20",
}


def audit():
    if not os.path.isdir(BASE):
        print(f"ERROR: {BASE} not found")
        return 1

    cells = sorted(d for d in os.listdir(BASE)
                   if os.path.isdir(os.path.join(BASE, d)))
    print(f"\n=== Phase 2H audit: {len(cells)} cells ===\n")

    per_model = {m: {"resp": 0, "constructs": 0, "ratings": 0, "ratings_total": 0,
                     "ratings_max": 0} for m in MODELS}
    per_cell_summary = []

    for cell_dir in cells:
        p = os.path.join(BASE, cell_dir, "cell.json")
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as f:
            cell = json.load(f)

        row = {"cell": cell_dir, "status": cell.get("status", "")}
        for m in MODELS:
            resp = cell.get("free_responses", {}).get(m)
            has_resp = bool(resp and isinstance(resp, str) and resp.strip())
            cons = cell.get("constructs", {}).get(m, [])
            n_c = sum(1 for c in cons
                      if isinstance(c, dict)
                      and c.get("left", "").strip()
                      and c.get("right", "").strip())
            rats = cell.get("ratings", {}).get(m, {})
            n_r = sum(len(v) for v in rats.values()) if isinstance(rats, dict) else 0

            per_model[m]["resp"] += 1 if has_resp else 0
            per_model[m]["constructs"] += 1 if n_c > 0 else 0
            per_model[m]["ratings"] += 1 if n_r > 0 else 0
            per_model[m]["ratings_total"] += n_r
            per_model[m]["ratings_max"] = max(per_model[m]["ratings_max"], n_r)
            row[m] = (has_resp, n_c, n_r)

        per_cell_summary.append(row)

    print(f"{'Model':<22} {'Resp':<8} {'Constructs':<12} {'Ratings':<11} {'TotalRatings':<13}")
    print("-" * 70)
    total = len(cells)
    for m in MODELS:
        d = per_model[m]
        print(f"{m} {LABELS[m]:<18} "
              f"{d['resp']}/{total} ({100*d['resp']/total:.0f}%)   "
              f"{d['constructs']}/{total} ({100*d['constructs']/total:.0f}%)    "
              f"{d['ratings']}/{total} ({100*d['ratings']/total:.0f}%)    "
              f"{d['ratings_total']:>5}")

    # Per-cell detail
    print(f"\n=== Per-cell detail (cell: model_resp/constructs/ratings_count) ===\n")
    header = "Cell".ljust(13) + " " + " ".join(m.center(8) for m in MODELS)
    print(header)
    print("-" * len(header))
    for row in per_cell_summary:
        parts = [row["cell"].ljust(13)]
        for m in MODELS:
            r, c, n = row.get(m, (False, 0, 0))
            mark = f"{'Y' if r else 'N'}/{c}/{n:>3}"
            parts.append(mark.center(8))
        print(" ".join(parts))

    # Total summary
    print(f"\n=== Total counts ===")
    print(f"Total cells: {total}")
    print(f"Total free responses: {sum(d['resp'] for d in per_model.values())}")
    print(f"Total constructs (cell-models with >=1): {sum(d['constructs'] for d in per_model.values())}")
    print(f"Total individual constructs: {sum(d['constructs'] for d in per_model.values()) * 3}")
    print(f"Total ratings recorded: {sum(d['ratings_total'] for d in per_model.values())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(audit())
