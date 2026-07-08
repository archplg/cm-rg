#!/usr/bin/env python3
"""
lab_vs_persona_combined.py - replication-analog of the 2.3× Lab>Persona finding
on the combined dataset (98 cells, 110,882 ratings, 11 models).

The original Phase 1 measurement used paired N-P design with shared constructs.
This is structurally absent in later phases (each cell has unique constructs).

This script implements a DEFENSIBLE ANALOG:
  Lab variance = variance across models of within-cell mean ratings (in N cells, per task)
  Persona variance = variance within model across P cells (different personas, per task)
                     minus baseline run-noise (within model across N cells, per task)

Per-task ratio is computed, then median across 7 tasks.

Output:
  analysis_combined/lab_vs_persona_combined.json   metrics + ratio
  Console: per-task table + final ratio

Запуск:
  python lab_vs_persona_combined.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np

PHASES = ["pilot", "extended", "phase2h", "phase2h_extended", "phase2j"]
OUT = Path("analysis_combined")


def load_cell_means() -> dict:
    """Return: {(task, condition, model): [list of cell means]}"""
    out = defaultdict(list)
    for ph in PHASES:
        d = Path(f"results_{ph}")
        if not d.exists(): continue
        for cell_dir in sorted(d.iterdir()):
            if not cell_dir.is_dir(): continue
            cj = cell_dir / "cell.json"
            if not cj.exists(): continue
            try:
                data = json.loads(cj.read_text(encoding='utf-8'))
            except Exception:
                continue
            task = data.get('task', '?')
            cond = data.get('condition', '?')
            for rater, rmap in data.get('ratings', {}).items():
                vals = []
                for cid, ele in rmap.items():
                    if isinstance(ele, dict):
                        for v in ele.values():
                            if isinstance(v, (int, float)) and 1 <= v <= 7:
                                vals.append(v)
                if len(vals) >= 5:
                    out[(task, cond, rater)].append(float(np.mean(vals)))
    return out


def main() -> int:
    OUT.mkdir(exist_ok=True)
    print("[1/3] Loading per-(task, condition, model) cell means ...")
    means = load_cell_means()

    # Get task universe
    tasks = sorted(set(k[0] for k in means.keys()))
    print(f"      Tasks found: {tasks}")
    print()

    # Per-task computation
    print(f"{'Task':<5} {'Lab var (N)':>13} {'Persona var':>13} {'Noise (N)':>11} {'Net persona':>13} {'Ratio':>9}")
    print("-" * 75)

    per_task = {}
    for task in tasks:
        # Lab variance under N condition: across-model variance of cell-mean ratings
        # Collect: for each cell in N, mean rating per model
        # Then: variance ACROSS models of these means (averaged across N cells of this task)
        # Implementation: for this task, gather all N cell-means per model, compute their model-level means,
        #                 then variance across model-level means
        model_avg_in_N = {}
        model_avg_in_P = {}
        model_var_in_N = {}  # within-model spread across N cells (run noise)
        model_var_in_P = {}  # within-model spread across P cells (persona + run noise)

        for (t, c, m), cell_means in means.items():
            if t != task: continue
            if c == 'N':
                if len(cell_means) >= 1:
                    model_avg_in_N[m] = float(np.mean(cell_means))
                if len(cell_means) >= 2:
                    model_var_in_N[m] = float(np.var(cell_means, ddof=1))
            elif c == 'P':
                if len(cell_means) >= 1:
                    model_avg_in_P[m] = float(np.mean(cell_means))
                if len(cell_means) >= 2:
                    model_var_in_P[m] = float(np.var(cell_means, ddof=1))

        # Lab variance: across-model variance of N averages
        n_avg_values = list(model_avg_in_N.values())
        if len(n_avg_values) >= 3:
            lab_var = float(np.var(n_avg_values, ddof=1))
        else:
            lab_var = float('nan')

        # Persona variance: average within-model variance under P
        p_vars = list(model_var_in_P.values())
        persona_var_raw = float(np.mean(p_vars)) if p_vars else float('nan')

        # Run-noise baseline: average within-model variance under N
        n_vars = list(model_var_in_N.values())
        noise_var = float(np.mean(n_vars)) if n_vars else float('nan')

        # Net persona effect = P variance - N variance (subtract noise floor)
        if not np.isnan(persona_var_raw) and not np.isnan(noise_var):
            net_persona = max(persona_var_raw - noise_var, 0.0001)  # floor at small positive
        else:
            net_persona = float('nan')

        # Ratio
        if not np.isnan(lab_var) and not np.isnan(net_persona) and net_persona > 0:
            ratio = lab_var / net_persona
        else:
            ratio = float('nan')

        per_task[task] = {
            "lab_var": lab_var,
            "persona_var_raw": persona_var_raw,
            "n_run_noise": noise_var,
            "net_persona": net_persona,
            "ratio": ratio,
            "n_models_N": len(model_avg_in_N),
            "n_models_with_p_var": len(p_vars),
            "n_models_with_n_var": len(n_vars),
        }
        print(f"{task:<5} {lab_var:>13.4f} {persona_var_raw:>13.4f} {noise_var:>11.4f} {net_persona:>13.4f} {ratio:>9.2f}")

    # Final median ratio
    ratios = [v["ratio"] for v in per_task.values() if not np.isnan(v["ratio"])]
    if ratios:
        median_ratio = float(np.median(ratios))
        mean_ratio = float(np.mean(ratios))
    else:
        median_ratio = mean_ratio = float('nan')

    print()
    print(f"=== FINAL ===")
    print(f"Median ratio across {len(ratios)}/7 tasks: {median_ratio:.2f}x")
    print(f"Mean ratio:                             {mean_ratio:.2f}x")
    print()
    print(f"Original Phase 1 claim: 2.3x")

    if not np.isnan(median_ratio):
        if median_ratio > 2.0:
            verdict = f"CONFIRMS Phase 1 finding (median {median_ratio:.2f}x ≥ 2.0). Lab dominates Persona."
        elif median_ratio > 1.2:
            verdict = f"QUALITATIVELY consistent (median {median_ratio:.2f}x > 1.0). Lab dominates Persona but weaker than Phase 1."
        elif median_ratio > 0.8:
            verdict = f"WEAK signal (median {median_ratio:.2f}x ≈ 1.0). Lab and Persona comparable on combined data."
        else:
            verdict = f"CONTRADICTS Phase 1 (median {median_ratio:.2f}x < 1.0). Persona dominates on combined!"
        print(f"Verdict: {verdict}")

    # Save
    out_data = {
        "method": "Lab var = across-model variance of N cell means per task. "
                  "Persona var = within-model variance across P cells minus within-model variance across N cells (run noise floor). "
                  "Ratio computed per task, median across tasks.",
        "n_tasks_evaluated": len(ratios),
        "median_ratio_lab_over_persona": median_ratio,
        "mean_ratio_lab_over_persona": mean_ratio,
        "phase_1_original_ratio": 2.3,
        "per_task": per_task,
    }
    out_path = OUT / "lab_vs_persona_combined.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved -> {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
