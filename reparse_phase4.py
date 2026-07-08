"""
Phase 2L · Recovery: re-parse Phase 4 ratings cells with improved parser.

Cells with ok_batches=0 but raw_content saved can be recovered WITHOUT new API calls.
Uses the robust parse_ratings_json function from run_phase2l.py.

Cost: $0.
Usage: python reparse_phase4.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, ".")
from run_phase2l import parse_ratings_json


def atomic_save(path: Path, data: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    import os
    os.replace(tmp, path)


def main() -> int:
    p4_dir = Path("./results_phase2l/phase4_ratings")
    if not p4_dir.exists():
        print(f"ERROR: {p4_dir} not found.")
        return 2

    print(f"Re-parsing Phase 4 cells with improved ratings parser...")
    print("=" * 100)

    total_cells = 0
    recovered_cells = 0
    still_zero_cells = 0
    total_batches_recovered = 0
    cells_to_redo = []

    for cell_path in p4_dir.rglob("*.json"):
        if "_backups" in cell_path.parts:
            continue
        total_cells += 1
        try:
            data = json.loads(cell_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue

        ok_batches_before = data.get("ok_batches", 0)
        n_batches = data.get("n_batches", 0)

        if ok_batches_before == n_batches:
            continue  # fully done, no need

        # Re-parse each batch that has raw_content
        new_ok = 0
        batches = data.get("batches", [])
        changed = False
        for batch in batches:
            existing_ratings = batch.get("ratings", [])
            if existing_ratings:
                new_ok += 1
                continue
            raw = batch.get("raw_content", "")
            if not raw:
                continue
            recovered_ratings = parse_ratings_json(raw)
            if recovered_ratings:
                batch["ratings"] = recovered_ratings
                batch.pop("parse_error", None)
                new_ok += 1
                changed = True

        if changed:
            data["ok_batches"] = new_ok
            data["reparsed"] = True
            atomic_save(cell_path, data)
            gain = new_ok - ok_batches_before
            total_batches_recovered += gain
            if new_ok > 0:
                recovered_cells += 1
            print(f"  {cell_path.relative_to(p4_dir)}: {ok_batches_before}/{n_batches} -> {new_ok}/{n_batches}  (+{gain} batches)")

        if new_ok == 0 and n_batches > 0:
            still_zero_cells += 1
            cells_to_redo.append(str(cell_path))

    print("=" * 100)
    print(f"Total cells: {total_cells}")
    print(f"Cells with recovered batches: {recovered_cells}")
    print(f"Total batches recovered: +{total_batches_recovered}")
    print(f"Cells still at 0/N (need redo): {still_zero_cells}")

    if cells_to_redo:
        with open("cleanup_phase4_unsalvageable.ps1", "w", encoding="utf-8") as f:
            f.write("# Delete Phase 4 cells where reparse failed - they need fresh API call\n")
            for c in cells_to_redo:
                f.write(f'Remove-Item "{c}" -ErrorAction SilentlyContinue\n')
        print(f"\nUnsalvageable cleanup script: cleanup_phase4_unsalvageable.ps1")
        print(f"Run if you want to re-do those {still_zero_cells} cells with fresh API calls.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
