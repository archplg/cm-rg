#!/usr/bin/env python3
"""
analyze_phase2k_paired.py - paired Lab>Persona ratio replication analysis.

Сравнивает:
  rating_N[model, construct, element] из Phase 2J N cells (neutral)
  rating_K[model, construct, element] из Phase 2K cells (под persona)

Метрики:
  Lab variance per task = variance across models of mean rating_N (same as before)
  Persona variance per task = within-model variance of (rating_N - rating_K) deltas

  Ratio = Lab variance / Persona variance
  Target (replication Phase 1): 2.3x

Запуск:
  python analyze_phase2k_paired.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np

PHASE2J_DIR = Path("results_phase2j")
PHASE2K_DIR = Path("results_phase2k")
OUT_DIR = Path("analysis_phase2k")


def load_ratings_from_phase(phase_dir: Path, condition: str) -> dict:
    """Load ratings into {(task, model, construct, element): rating}."""
    out = {}
    if not phase_dir.exists():
        return out
    for cell_dir in sorted(phase_dir.iterdir()):
        if not cell_dir.is_dir(): continue
        cj = cell_dir / "cell.json"
        if not cj.exists(): continue
        try:
            data = json.loads(cj.read_text(encoding='utf-8'))
        except Exception:
            continue
        if condition and data.get("condition") != condition:
            continue
        task = data.get("task", "?")
        for rater, rmap in data.get("ratings", {}).items():
            for cid, ele_map in rmap.items():
                if not isinstance(ele_map, dict): continue
                for ek, v in ele_map.items():
                    if isinstance(v, (int, float)) and 1 <= v <= 7:
                        out[(task, rater, cid, ek)] = float(v)
    return out


def main():
    OUT_DIR.mkdir(exist_ok=True)
    print("[1/3] Loading Phase 2J N ratings and Phase 2K paired ratings ...")
    ratings_N = load_ratings_from_phase(PHASE2J_DIR, "N")
    ratings_K = load_ratings_from_phase(PHASE2K_DIR, "K")
    print(f"      N ratings:  {len(ratings_N):,}")
    print(f"      K ratings:  {len(ratings_K):,}")

    if not ratings_K:
        print("ERROR: no Phase 2K ratings found. Run run_phase2k_paired.py first.", file=sys.stderr)
        return 1

    # Build paired set: only (task, model, construct, element) tuples present in BOTH
    paired_keys = set(ratings_N.keys()) & set(ratings_K.keys())
    print(f"      Paired (N+K) tuples: {len(paired_keys):,}")
    if len(paired_keys) < 100:
        print("ERROR: too few paired tuples. Verify Phase 2K reused Phase 2J N constructs.", file=sys.stderr)
        return 1

    # Per task aggregation
    print("\n[2/3] Per-task computation ...")
    by_task = defaultdict(lambda: {"N": defaultdict(list), "K": defaultdict(list), "delta": defaultdict(list)})
    for key in paired_keys:
        task, model, cid, ek = key
        n_val = ratings_N[key]
        k_val = ratings_K[key]
        by_task[task]["N"][model].append(n_val)
        by_task[task]["K"][model].append(k_val)
        by_task[task]["delta"][model].append(k_val - n_val)

    print(f"{'Task':<5} {'Lab var':>10} {'Persona var':>12} {'Ratio':>8} {'n_pairs':>10} {'n_models':>10}")
    print("-" * 60)
    per_task = {}
    for task in sorted(by_task.keys()):
        td = by_task[task]
        # Lab variance: variance across models of mean N rating
        model_n_means = []
        for m, vals in td["N"].items():
            if len(vals) >= 3:
                model_n_means.append(float(np.mean(vals)))
        if len(model_n_means) < 3:
            print(f"{task:<5}: insufficient data")
            continue
        lab_var = float(np.var(model_n_means, ddof=1))

        # Persona variance: within-model variance of (K - N) deltas
        # i.e., how much does persona shift the same model on the same items?
        within_model_delta_vars = []
        for m, deltas in td["delta"].items():
            if len(deltas) >= 5:
                within_model_delta_vars.append(float(np.var(deltas, ddof=1)))
        if not within_model_delta_vars:
            continue
        persona_var = float(np.mean(within_model_delta_vars))

        ratio = lab_var / persona_var if persona_var > 0 else float('inf')
        n_pairs = sum(len(v) for v in td["delta"].values())
        per_task[task] = {
            "lab_var": lab_var,
            "persona_var": persona_var,
            "ratio": ratio,
            "n_pairs": n_pairs,
            "n_models_with_data": len(within_model_delta_vars),
        }
        print(f"{task:<5} {lab_var:>10.4f} {persona_var:>12.4f} {ratio:>8.2f} {n_pairs:>10,} {len(within_model_delta_vars):>10}")

    # Median ratio
    ratios = [v["ratio"] for v in per_task.values() if np.isfinite(v["ratio"])]
    if ratios:
        median_ratio = float(np.median(ratios))
        mean_ratio = float(np.mean(ratios))
        print()
        print(f"=== FINAL ===")
        print(f"Median ratio across {len(ratios)} tasks: {median_ratio:.2f}x")
        print(f"Mean ratio:                            {mean_ratio:.2f}x")
        print(f"Phase 1 original (5 models, n=42):    2.30x")
        print()
        if median_ratio >= 2.0:
            print(f"CONFIRMS Phase 1 finding at scale (n_models=11, paired design).")
        elif median_ratio >= 1.2:
            print(f"PARTIAL replication - Lab dominates but weaker than Phase 1.")
        else:
            print(f"DOES NOT REPLICATE Phase 1 finding.")
    else:
        median_ratio = mean_ratio = float('nan')

    # Save
    out_data = {
        "method": "Lab var = across-model variance of mean N ratings. "
                  "Persona var = within-model variance of (rating_K - rating_N) paired deltas, averaged across models.",
        "n_tasks_evaluated": len(per_task),
        "median_ratio": median_ratio,
        "mean_ratio": mean_ratio,
        "phase_1_original_ratio": 2.30,
        "per_task": per_task,
        "n_paired_tuples_total": len(paired_keys),
    }
    print("\n[3/3] Writing outputs ...")
    with open(OUT_DIR / "paired_ratio.json", "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)
    print(f"      Results -> {OUT_DIR / 'paired_ratio.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
