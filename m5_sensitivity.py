#!/usr/bin/env python3
"""
M5 dropout sensitivity analysis.

Re-runs the key analyses TWICE:
  1. Full data (all 5 models)
  2. Excluding M5 (Moonshot Kimi) entirely
And reports how each headline metric changes. If findings are robust to M5
exclusion, the missing-data limitation is contained.

Outputs:
  m5_sensitivity/M5_SENSITIVITY_FINDINGS.md
  m5_sensitivity/sensitivity_table.csv
  m5_sensitivity/m5_dropout_per_cell.csv

Run:
    python m5_sensitivity.py
"""
from __future__ import annotations
import argparse
import json
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

RESULTS_DIR = Path("./results")
OUT_DIR = Path("./m5_sensitivity")


# ============================================================
# Loaders
# ============================================================
def load_cells() -> list[dict]:
    cells = []
    if not RESULTS_DIR.exists():
        return cells
    for cd in sorted(RESULTS_DIR.iterdir()):
        if not cd.is_dir():
            continue
        cell_file = cd / "cell.json"
        if not cell_file.exists():
            continue
        with open(cell_file, encoding="utf-8") as f:
            cell = json.load(f)
        if cell.get("status", "").startswith("complete"):
            cells.append(cell)
    return cells


# ============================================================
# Per-cell metrics (replicates analyze.py logic, but with model exclusion option)
# ============================================================
def cell_disagreement(cell: dict, exclude_models: set = None) -> float:
    """Mean pairwise rater disagreement, optionally excluding specified models."""
    exclude_models = exclude_models or set()
    raters = sorted(r for r in cell.get("ratings", {}).keys() if r not in exclude_models)
    if len(raters) < 2:
        return float("nan")
    pair_diffs = []
    for a, b in combinations(raters, 2):
        ra = cell["ratings"].get(a, {})
        rb = cell["ratings"].get(b, {})
        diffs = []
        for cid in set(ra.keys()) & set(rb.keys()):
            for ek in set(ra[cid].keys()) & set(rb[cid].keys()):
                diffs.append(abs(ra[cid][ek] - rb[cid][ek]))
        if diffs:
            pair_diffs.append(np.mean(diffs))
    return float(np.mean(pair_diffs)) if pair_diffs else float("nan")


def cell_n_constructs(cell: dict, exclude_models: set = None) -> int:
    exclude_models = exclude_models or set()
    total = 0
    for model, constructs in cell.get("constructs", {}).items():
        if model in exclude_models:
            continue
        total += sum(1 for c in constructs if c.get("left", "").strip() and c.get("right", "").strip())
    return total


def cell_n_raters(cell: dict, exclude_models: set = None) -> int:
    exclude_models = exclude_models or set()
    return sum(1 for r in cell.get("ratings", {}).keys() if r not in exclude_models)


def m5_status_per_cell(cell: dict) -> dict:
    """How well M5 participated in this cell."""
    fr = cell.get("free_responses", {}).get("M5")
    # BUG FIX: `isinstance(fr, str) and fr.strip()` returns the STRING when truthy.
    # Must wrap in bool() to get an actual boolean for CSV output.
    has_response = bool(isinstance(fr, str) and fr.strip())
    n_constructs = sum(1 for c in cell.get("constructs", {}).get("M5", []) if c.get("left"))
    has_ratings = bool(cell.get("ratings", {}).get("M5"))
    return {
        "has_response": has_response,
        "n_constructs": int(n_constructs),
        "has_ratings": has_ratings,
        "fully_participated": bool(has_response and n_constructs >= 1 and has_ratings),
    }


# ============================================================
# Main
# ============================================================
def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=str(OUT_DIR))
    args = p.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading cells...")
    cells = load_cells()
    print(f"  {len(cells)} cells")
    if not cells:
        return 1

    # === M5 dropout audit per cell ===
    dropout_rows = []
    for c in cells:
        s = m5_status_per_cell(c)
        dropout_rows.append({
            "cell_id": c.get("cell_id"),
            "task": c.get("task"),
            "condition": c.get("condition"),
            "M5_has_response": s["has_response"],
            "M5_n_constructs": s["n_constructs"],
            "M5_has_ratings": s["has_ratings"],
            "M5_fully_participated": s["fully_participated"],
        })
    df_dropout = pd.DataFrame(dropout_rows)
    df_dropout.to_csv(out_dir / "m5_dropout_per_cell.csv", index=False)

    n_cells = len(df_dropout)
    n_full = int(df_dropout["M5_fully_participated"].sum())
    n_response_only = int((df_dropout["M5_has_response"] & ~df_dropout["M5_fully_participated"]).sum())
    n_no_response = int((~df_dropout["M5_has_response"]).sum())
    full_pct = n_full / n_cells * 100

    print(f"\nM5 participation breakdown:")
    print(f"  Fully participated: {n_full}/{n_cells} ({full_pct:.1f}%)")
    print(f"  Partial (response but no constructs/ratings): {n_response_only}")
    print(f"  No response at all: {n_no_response}")

    # === Sensitivity analysis: compute metrics with and without M5 ===
    rows = []
    for c in cells:
        full = cell_disagreement(c, exclude_models=set())
        no_m5 = cell_disagreement(c, exclude_models={"M5"})
        nc_full = cell_n_constructs(c, exclude_models=set())
        nc_no_m5 = cell_n_constructs(c, exclude_models={"M5"})
        nr_full = cell_n_raters(c, exclude_models=set())
        nr_no_m5 = cell_n_raters(c, exclude_models={"M5"})
        rows.append({
            "cell_id": c.get("cell_id"),
            "task": c.get("task"),
            "condition": c.get("condition"),
            "disagreement_full": full,
            "disagreement_no_M5": no_m5,
            "disagreement_delta": (no_m5 - full) if not (np.isnan(full) or np.isnan(no_m5)) else float("nan"),
            "n_constructs_full": nc_full,
            "n_constructs_no_M5": nc_no_m5,
            "n_raters_full": nr_full,
            "n_raters_no_M5": nr_no_m5,
        })
    df_sens = pd.DataFrame(rows)
    df_sens.to_csv(out_dir / "sensitivity_table.csv", index=False)

    # === Aggregate sensitivity stats ===
    print(f"\nDisagreement sensitivity (per-cell deltas):")
    deltas = df_sens["disagreement_delta"].dropna()
    print(f"  Mean delta (no-M5 minus full): {deltas.mean():+.4f}")
    print(f"  Median delta: {deltas.median():+.4f}")
    print(f"  SD of deltas: {deltas.std():.4f}")
    print(f"  Range: [{deltas.min():+.4f}, {deltas.max():+.4f}]")

    # By-task means
    print(f"\nBy-task means:")
    for task in sorted(df_sens["task"].dropna().unique()):
        sub = df_sens[df_sens["task"] == task]
        f_mean = sub["disagreement_full"].mean()
        n_mean = sub["disagreement_no_M5"].mean()
        print(f"  Task {task}: full={f_mean:.3f}, no-M5={n_mean:.3f}, delta={n_mean - f_mean:+.3f}")

    # === Markdown report ===
    lines = ["# M5 (Moonshot Kimi) Sensitivity Analysis\n\n"]
    lines.append(f"Generated from {n_cells} cells.\n\n")
    lines.append("## M5 participation rate\n\n")
    lines.append(f"- **Fully participated**: {n_full} of {n_cells} ({full_pct:.1f}%)\n")
    lines.append(f"  - Full = has free response AND >=1 constructs AND has ratings dict\n")
    lines.append(f"- **Partial participation**: {n_response_only} cells (response but lost downstream)\n")
    lines.append(f"- **No response at all**: {n_no_response} cells\n\n")

    lines.append("## Headline metric sensitivity (overall disagreement)\n\n")
    full_mean = df_sens["disagreement_full"].dropna().mean()
    no_m5_mean = df_sens["disagreement_no_M5"].dropna().mean()
    lines.append(f"- Mean disagreement with M5: **{full_mean:.3f}**\n")
    lines.append(f"- Mean disagreement WITHOUT M5: **{no_m5_mean:.3f}**\n")
    lines.append(f"- Absolute delta: **{no_m5_mean - full_mean:+.4f}**\n")
    pct_change = (no_m5_mean - full_mean) / full_mean * 100 if full_mean else 0
    lines.append(f"- Relative change: **{pct_change:+.1f}%**\n\n")
    if abs(pct_change) < 10:
        lines.append("Interpretation: **headline finding is robust to M5 exclusion** "
                     "(< 10% relative change). M5 dropout does not materially affect conclusions.\n\n")
    elif abs(pct_change) < 25:
        lines.append("Interpretation: **headline finding is moderately sensitive to M5** "
                     "(10-25% relative change). Report both versions in paper; "
                     "primary analysis includes M5, sensitivity excludes.\n\n")
    else:
        lines.append("Interpretation: **headline finding is HIGHLY sensitive to M5** "
                     "(>25% relative change). M5 dropout is a serious confound; need to "
                     "report M5-excluded as primary, M5-included as sensitivity.\n\n")

    lines.append("## Per-task breakdown\n\n")
    lines.append("| Task | Disagreement w/ M5 | Disagreement w/o M5 | Delta |\n")
    lines.append("|---|---|---|---|\n")
    for task in sorted(df_sens["task"].dropna().unique()):
        sub = df_sens[df_sens["task"] == task]
        f_mean = sub["disagreement_full"].mean()
        n_mean = sub["disagreement_no_M5"].mean()
        lines.append(f"| {task} | {f_mean:.3f} | {n_mean:.3f} | {n_mean - f_mean:+.3f} |\n")

    lines.append("\n## How to use this for paper writing\n\n")
    lines.append("- Report **primary analysis with M5 included** (this is the main dataset).\n")
    lines.append("- In a **Limitations** subsection or supplementary materials, report the M5 dropout rate and this sensitivity analysis.\n")
    lines.append("- If the relative change is < 10%, conclude: 'findings are robust to the M5 missing-data pattern'.\n")
    lines.append("- The full per-cell sensitivity table is in `sensitivity_table.csv`.\n")

    (out_dir / "M5_SENSITIVITY_FINDINGS.md").write_text("".join(lines), encoding="utf-8")
    print(f"\nWritten: {out_dir}/M5_SENSITIVITY_FINDINGS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
