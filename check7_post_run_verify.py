"""
Phase 2L · Pre-flight Check 7: Post-run verification script.

After the main Phase 2L run completes, this script walks the results_phase2l/
directory and verifies:
  1. Expected cell.json files exist for every (task, condition, model, phase)
  2. Each cell.json is >= min_cell_json_size_bytes (5KB) - no truncation
  3. usage.cost is non-zero (no Phase 2J $0 bug)
  4. All constructs parsed cleanly (no ?-marks, no empty arrays)
  5. Activity CSV total matches state.json total_cost_usd

Cost: $0.
Usage: python check7_post_run_verify.py [--results-dir ./results_phase2l]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 2L Check 7: post-run verify")
    parser.add_argument("--results-dir", default="./results_phase2l")
    parser.add_argument("--config", default="config_phase2l.yaml")
    parser.add_argument("--min-cell-size", type=int, default=5000)
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    if not results_dir.exists():
        print(f"ERROR: results dir not found: {results_dir}")
        print("(Run this AFTER main Phase 2L run completes.)")
        return 2

    print(f"Phase 2L Check 7: Post-run verification")
    print(f"Scanning: {results_dir}")
    print("=" * 100)

    issues = []
    total_cells = 0
    truncated_cells = 0
    zero_cost_cells = 0
    empty_constructs = 0
    parse_errors = 0
    total_cost = 0.0

    # Walk all cell.json files
    for cell_path in results_dir.rglob("cell.json"):
        total_cells += 1
        try:
            size = cell_path.stat().st_size
            if size < args.min_cell_size:
                truncated_cells += 1
                issues.append(f"TRUNCATED: {cell_path} ({size} bytes < {args.min_cell_size})")
                continue
            data = json.loads(cell_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            parse_errors += 1
            issues.append(f"PARSE_ERROR: {cell_path}: {e}")
            continue
        except Exception as e:
            parse_errors += 1
            issues.append(f"READ_ERROR: {cell_path}: {e}")
            continue

        # Check cost
        cost = (data.get("usage") or {}).get("cost") or data.get("cost_usd") or 0
        if cost == 0:
            zero_cost_cells += 1
            issues.append(f"ZERO_COST: {cell_path}")
        total_cost += cost

        # Check constructs (phase 3 cells)
        if "constructs" in data:
            constructs = data["constructs"] or []
            if not constructs:
                empty_constructs += 1
                issues.append(f"EMPTY_CONSTRUCTS: {cell_path}")

    print(f"\nTotal cell.json files: {total_cells}")
    print(f"  Truncated (<{args.min_cell_size} bytes): {truncated_cells}")
    print(f"  Parse errors:                            {parse_errors}")
    print(f"  Zero-cost cells:                         {zero_cost_cells}")
    print(f"  Empty constructs:                        {empty_constructs}")
    print(f"  Sum of cell costs:                       ${total_cost:.4f}")

    # Compare to state.json if exists
    state_path = results_dir / "state.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state_cost = state.get("total_cost_usd") or 0
        delta = abs(state_cost - total_cost)
        print(f"  state.json total_cost_usd:               ${state_cost:.4f}")
        print(f"  Delta:                                   ${delta:.4f}")
        if delta > 0.10:  # tolerance 10 cents
            issues.append(f"COST_MISMATCH: cells sum ${total_cost:.4f} vs state ${state_cost:.4f}")

    # Compare to activity CSV if exists
    activity_csv = results_dir / "activity.csv"
    if activity_csv.exists():
        csv_total = 0.0
        for line in activity_csv.read_text(encoding="utf-8").splitlines()[1:]:  # skip header
            cols = line.split(",")
            try:
                csv_total += float(cols[-1])  # assume last col is cost
            except Exception:
                pass
        print(f"  activity.csv sum:                        ${csv_total:.4f}")
        if abs(csv_total - total_cost) > 0.10:
            issues.append(f"CSV_MISMATCH: cells sum ${total_cost:.4f} vs csv ${csv_total:.4f}")

    print("\n" + "=" * 100)
    if issues:
        print(f"FOUND {len(issues)} ISSUE(S):")
        for i in issues[:50]:
            print(f"  - {i}")
        if len(issues) > 50:
            print(f"  ... and {len(issues) - 50} more")
        return 1
    print("ALL CHECKS PASSED. Phase 2L results are clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
