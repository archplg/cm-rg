"""
Phase 2L · Recovery: re-parse Phase 3 cells with improved parser.

Many Phase 3 cells have n_constructs=0 because the original parser couldn't handle
reasoning model output (<thinking> tags). The model DID respond - we have the raw text.

This script re-parses every Phase 3 cell using the updated check3_parser_test.parse_constructs
function (which now strips reasoning tags) and updates n_constructs in-place.

Cost: $0 (no API calls).
Usage: python reparse_phase3.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, ".")
from check3_parser_test import parse_constructs


def atomic_save(path: Path, data: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    import os
    os.replace(tmp, path)


def main() -> int:
    p3_dir = Path("./results_phase2l/phase3_constructs")
    if not p3_dir.exists():
        print(f"ERROR: {p3_dir} not found.")
        return 2

    print(f"Re-parsing Phase 3 cells with improved parser...")
    print("=" * 100)
    print(f"{'cell':<60} {'before':>8} {'after':>8} {'gained':>8}")
    print("-" * 100)

    total = 0
    recovered = 0
    total_before = 0
    total_after = 0
    still_zero = []

    for cell_path in p3_dir.rglob("*.json"):
        if "_backups" in cell_path.parts:
            continue
        try:
            data = json.loads(cell_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"  PARSE_FAIL {cell_path}")
            continue
        total += 1

        before = data.get("n_constructs", 0)
        raw = data.get("raw_response", "")
        if not raw:
            continue

        new_constructs = parse_constructs(raw)
        after = len(new_constructs)
        total_before += before
        total_after += after

        if after > before:
            data["constructs"] = new_constructs
            data["n_constructs"] = after
            data["reparsed"] = True
            atomic_save(cell_path, data)
            recovered += 1
            rel = cell_path.relative_to(p3_dir)
            gain = after - before
            print(f"  {str(rel):<58} {before:>8} {after:>8} {'+'+str(gain):>8}")
        elif after == 0:
            rel = cell_path.relative_to(p3_dir)
            still_zero.append(str(rel))

    print("-" * 100)
    print(f"\nTotal Phase 3 cells: {total}")
    print(f"Recovered: {recovered} cells got new constructs")
    print(f"Total constructs before: {total_before}")
    print(f"Total constructs after:  {total_after}")
    print(f"Net gain: +{total_after - total_before} constructs")
    if still_zero:
        print(f"\nStill ZERO constructs ({len(still_zero)} cells - may need API redo):")
        for s in still_zero[:30]:
            print(f"  {s}")
        if len(still_zero) > 30:
            print(f"  ... and {len(still_zero) - 30} more")

    return 0


if __name__ == "__main__":
    sys.exit(main())
