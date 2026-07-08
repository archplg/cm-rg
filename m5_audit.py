#!/usr/bin/env python3
"""
M5 (Kimi) participation audit for Phase 2C (results_extended/).

Counts per-cell: did M5 produce a free response, how many constructs, how many ratings.
More reliable than PowerShell version due to PowerShell PSObject array quirks.

Run:
    python m5_audit.py
    python m5_audit.py --results_dir results_extended
    python m5_audit.py --results_dir results            # for Phase 1 baseline
"""
from __future__ import annotations
import argparse
import json
import os
import sys


def audit(base: str) -> int:
    if not os.path.isdir(base):
        print(f"ERROR: directory not found: {base}", file=sys.stderr)
        return 1

    results = []
    for d in sorted(os.listdir(base)):
        p = os.path.join(base, d, "cell.json")
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as f:
            try:
                cell = json.load(f)
            except Exception as exc:
                print(f"WARN: could not parse {p}: {exc}")
                continue

        m5_resp = cell.get("free_responses", {}).get("M5")
        has_resp = bool(m5_resp and isinstance(m5_resp, str) and m5_resp.strip())
        resp_len = len(m5_resp) if isinstance(m5_resp, str) else 0

        m5_constructs = cell.get("constructs", {}).get("M5", [])
        n_constructs = 0
        if isinstance(m5_constructs, list):
            n_constructs = sum(
                1 for c in m5_constructs
                if isinstance(c, dict)
                and c.get("left", "").strip()
                and c.get("right", "").strip()
            )

        m5_ratings = cell.get("ratings", {}).get("M5", {})
        n_ratings = 0
        if isinstance(m5_ratings, dict):
            for cid, by_element in m5_ratings.items():
                if isinstance(by_element, dict):
                    n_ratings += len(by_element)

        results.append({
            "cell": d,
            "task": d.split("_")[0],
            "condition": d.split("_")[1] if "_" in d else "",
            "has_resp": has_resp,
            "resp_len": resp_len,
            "n_constructs": n_constructs,
            "n_ratings": n_ratings,
        })

    if not results:
        print(f"No cells found in {base}")
        return 1

    # Print per-cell table
    print(f"\n=== M5 audit on {base} ({len(results)} cells) ===\n")
    print(f"{'Cell':<14} {'Resp':<5} {'RespLen':<8} {'Constructs':<11} {'Ratings':<8}")
    print("-" * 52)
    for r in results:
        print(f"{r['cell']:<14} "
              f"{'Y' if r['has_resp'] else 'N':<5} "
              f"{r['resp_len']:<8} "
              f"{r['n_constructs']:<11} "
              f"{r['n_ratings']:<8}")

    total = len(results)
    wr = sum(1 for r in results if r["has_resp"])
    wc = sum(1 for r in results if r["n_constructs"] > 0)
    wt = sum(1 for r in results if r["n_ratings"] > 0)
    full = sum(1 for r in results if r["has_resp"] and r["n_constructs"] > 0 and r["n_ratings"] > 0)

    print("\n=== Aggregates ===")
    print(f"Total cells:           {total}")
    print(f"M5 has free response:  {wr}/{total} ({100*wr/total:.0f}%)")
    print(f"M5 has >= 1 construct: {wc}/{total} ({100*wc/total:.0f}%)")
    print(f"M5 has >= 1 rating:    {wt}/{total} ({100*wt/total:.0f}%)")
    print(f"M5 fully participated: {full}/{total} ({100*full/total:.0f}%)")
    print(f"\nTotal M5 constructs across all cells: {sum(r['n_constructs'] for r in results)}")
    print(f"Total M5 ratings across all cells:    {sum(r['n_ratings'] for r in results)}")

    # Per-task breakdown
    print("\n=== Per-task breakdown ===")
    tasks = sorted(set(r["task"] for r in results))
    for t in tasks:
        sub = [r for r in results if r["task"] == t]
        st = len(sub)
        sr = sum(1 for r in sub if r["has_resp"])
        sc = sum(1 for r in sub if r["n_constructs"] > 0)
        srt = sum(1 for r in sub if r["n_ratings"] > 0)
        print(f"Task {t}: resp={sr}/{st}, constructs={sc}/{st}, ratings={srt}/{st}")

    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--results_dir", default="results_extended",
                   help="Directory containing per-cell sub-dirs with cell.json")
    args = p.parse_args()
    return audit(args.results_dir)


if __name__ == "__main__":
    raise SystemExit(main())
