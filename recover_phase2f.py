#!/usr/bin/env python3
"""
Recover Phase 2F data from truncated state.json.

state.json was truncated at ~97% during final write but contains valid cell
data up to that point. Individual cell.json files are 2578-byte stubs.

This script:
1. Reads state.json byte-by-byte, finding the last complete cell entry
2. Extracts all complete cells
3. Writes proper cell.json for each recovered cell
4. Reports how much data was salvaged

Run:
    python recover_phase2f.py
"""
import json
import os
import re
import sys


def find_last_valid_cell(state_text):
    """Truncate state_text just before any incomplete cell entry."""
    # JSON structure: {"started_at": "...", "total_cost_usd": X, "cells": {"H_N_run1": {...}, "H_N_run2": {...}, ...}}
    # Find each '    "X_Y_runN": {' boundary by indentation level 4 (inside cells dict)

    # Try parsing the full thing first
    try:
        return json.loads(state_text)
    except json.JSONDecodeError:
        pass

    # Find cell entry boundaries: lines that start with 4 spaces, quote, then cell_id pattern
    cell_boundary = re.compile(r'\n    "([A-Z]_[NP]_run\d+)": \{')

    matches = list(cell_boundary.finditer(state_text))
    if not matches:
        print("ERROR: no cell entries found in state.json")
        return None

    print(f"Found {len(matches)} cell entry boundaries")

    # Try truncating just before each boundary (going backwards from last)
    for i in range(len(matches) - 1, 0, -1):
        # Truncate at the position right BEFORE the i-th match (so we keep i cells)
        truncate_at = matches[i].start()
        # Build a valid JSON: state[:truncate_at] + close brackets
        partial = state_text[:truncate_at].rstrip()
        # Remove trailing comma if present
        if partial.endswith(','):
            partial = partial[:-1]
        # Close cells dict + close outer dict
        candidate = partial + "\n  }\n}"
        try:
            data = json.loads(candidate)
            print(f"Successfully parsed with {i} cells (truncated after {matches[i-1].group(1)})")
            return data
        except json.JSONDecodeError as e:
            continue

    print("ERROR: could not recover any cells")
    return None


def main():
    base = "results_phase2f"
    state_file = os.path.join(base, "state.json")

    print(f"Reading {state_file}...")
    with open(state_file, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="ignore")
    print(f"  {len(raw)} bytes")

    print("\nAttempting recovery...")
    state = find_last_valid_cell(text)
    if state is None:
        return 1

    cells = state.get("cells", {})
    print(f"\nRecovered cells: {len(cells)}")

    # Audit each recovered cell
    recovered = []
    incomplete = []
    for cell_id, cell in cells.items():
        n_fr = sum(1 for v in cell.get("free_responses", {}).values()
                   if isinstance(v, str) and v.strip())
        n_constructs = 0
        for m, items in cell.get("constructs", {}).items():
            if isinstance(items, list):
                n_constructs += sum(1 for c in items if isinstance(c, dict)
                                     and c.get("left", "").strip()
                                     and c.get("right", "").strip())
        n_ratings = 0
        for m, by_c in cell.get("ratings", {}).items():
            if isinstance(by_c, dict):
                for cid, by_e in by_c.items():
                    if isinstance(by_e, dict):
                        n_ratings += len(by_e)
        if n_fr >= 3 and n_constructs >= 5 and n_ratings >= 100:
            recovered.append(cell_id)
            print(f"  + {cell_id}: fr={n_fr}, constructs={n_constructs}, ratings={n_ratings}")
        else:
            incomplete.append(cell_id)
            print(f"  - {cell_id}: fr={n_fr}, constructs={n_constructs}, ratings={n_ratings} (incomplete)")

    print(f"\nFully recovered: {len(recovered)}")
    print(f"Incomplete: {len(incomplete)}")

    # Backup current broken cell.json files
    print("\nBacking up broken cell.json files...")
    for cell_id in cells:
        cell_dir = os.path.join(base, cell_id)
        old_file = os.path.join(cell_dir, "cell.json")
        if os.path.isfile(old_file):
            backup = old_file + ".broken"
            try:
                os.rename(old_file, backup)
            except FileExistsError:
                os.remove(backup)
                os.rename(old_file, backup)

    # Write recovered cell.json files
    print("\nWriting recovered cell.json files...")
    for cell_id, cell in cells.items():
        cell_dir = os.path.join(base, cell_id)
        os.makedirs(cell_dir, exist_ok=True)
        out_file = os.path.join(cell_dir, "cell.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(cell, f, indent=2, ensure_ascii=False)
        # verify
        with open(out_file, encoding="utf-8") as f:
            json.load(f)

    print(f"\nWrote {len(cells)} cell.json files")
    print(f"  Fully usable: {len(recovered)}")
    print(f"  Need re-run: {len(incomplete)}")
    if incomplete:
        print("\nCells that need re-running (delete + --resume):")
        for c in incomplete:
            print(f"  {c}")

    # Backup and rewrite state.json properly
    state_backup = state_file + ".broken"
    if os.path.isfile(state_backup):
        os.remove(state_backup)
    os.rename(state_file, state_backup)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    print(f"\nRewrote {state_file} from recovered data")
    print(f"Original saved as {state_backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
