#!/usr/bin/env python3
"""Analyze the full reliability experiment: panel strategies vs nulls,
convergence signal, risk-coverage.

Usage:
    python analyze_reliability.py --run run/ --items items/ --panels panels.json

Reads run/singles.json, items/answers.json, panels.json. Writes into run/:
    reliability_metrics.json, panel_accuracy.png, risk_coverage.png
"""
import argparse
import json
import random
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"


def norm(s):
    return None if s is None else str(s).strip().lower().replace(",", "").replace(" ", "")


def majority(answers):
    votes = Counter(a for a in (norm(x) for x in answers) if a is not None)
    if not votes:
        return None
    top, n = votes.most_common(1)[0]
    second = votes.most_common(2)[1][1] if len(votes) > 1 else 0
    return top if n > second else None  # strict: tie -> abstain (wrong)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--items", required=True)
    ap.add_argument("--panels", required=True)
    ap.add_argument("--selftest-panels", action="store_true",
                    help="ignore panel membership (use first models) - for offline selftest")
    ap.add_argument("--boot", type=int, default=2000)
    args = ap.parse_args()

    run = Path(args.run)
    singles = json.loads((run / "singles.json").read_text())
    gold = json.loads((Path(args.items) / "answers.json").read_text())
    items = sorted(gold)
    models = sorted(singles)
    panels_cfg = json.loads(Path(args.panels).read_text())["panels"]
    if args.selftest_panels:
        panels_cfg = {"D3": {"members": models[:3]}, "R3": {"members": models[-3:]},
                      "ATLAS3": {"members": [models[0], models[len(models) // 2], models[-1]]}}

    def correct_flags(model):
        return {it: int(norm(singles[model].get(it)) == norm(gold[it])) for it in items}

    flags = {m: correct_flags(m) for m in models}
    acc = {m: sum(flags[m].values()) / len(items) for m in models}

    def panel_flags(members):
        avail = [m for m in members if m in singles]
        return {it: int(majority([singles[m].get(it) for m in avail]) == norm(gold[it]))
                for it in items}, avail

    results = {}
    for name, cfg in panels_cfg.items():
        pf, avail = panel_flags(cfg["members"])
        results[name] = {"members": cfg["members"], "available": avail,
                         "accuracy": round(sum(pf.values()) / len(items), 3),
                         "flags": pf}

    # TOP-k by individual accuracy (post-hoc, as pre-registered)
    ranked = sorted(models, key=lambda m: -acc[m])
    for k in (3, 5):
        pf, avail = panel_flags(ranked[:k])
        results[f"TOP{k}"] = {"members": ranked[:k], "available": avail,
                              "accuracy": round(sum(pf.values()) / len(items), 3),
                              "flags": pf}

    # RANDOM-k null distribution
    rng = random.Random(42)
    nulls = {}
    for k in (3, 5):
        accs = []
        for _ in range(500):
            pf, _a = panel_flags(rng.sample(models, k))
            accs.append(sum(pf.values()) / len(items))
        nulls[f"RANDOM{k}"] = {"mean": round(float(np.mean(accs)), 3),
                               "p05": round(float(np.percentile(accs, 5)), 3),
                               "p95": round(float(np.percentile(accs, 95)), 3)}

    # bootstrap CI over items for each named panel
    rng2 = np.random.default_rng(42)
    for name, resu in results.items():
        f = np.array([resu["flags"][it] for it in items])
        boots = [f[rng2.integers(0, len(f), len(f))].mean() for _ in range(args.boot)]
        resu["ci90"] = [round(float(np.percentile(boots, 5)), 3),
                        round(float(np.percentile(boots, 95)), 3)]

    # convergence signal + risk-coverage for the best pre-registered panel (DQ3 if present)
    focus = "DQ3" if "DQ3" in results else list(results)[0]
    members = [m for m in results[focus]["members"] if m in singles]
    conv_correct = conv_total = split_correct = split_total = 0
    coverage_curve = []
    for it in items:
        answers = [norm(singles[m].get(it)) for m in members]
        answered = [a for a in answers if a is not None]
        unanimous = len(set(answered)) == 1 and len(answered) == len(members)
        maj_ok = results[focus]["flags"][it]
        if unanimous:
            conv_total += 1
            conv_correct += maj_ok
        else:
            split_total += 1
            split_correct += maj_ok
    if conv_total:
        coverage_curve = [
            {"policy": "accept only unanimous", "coverage": round(conv_total / len(items), 3),
             "accuracy_on_accepted": round(conv_correct / conv_total, 3)},
            {"policy": "accept all (majority)", "coverage": 1.0,
             "accuracy_on_accepted": results[focus]["accuracy"]},
        ]

    metrics = {
        "n_items": len(items), "n_models": len(models),
        "singles_accuracy": {m: round(a, 3) for m, a in
                             sorted(acc.items(), key=lambda kv: -kv[1])},
        "panels": {n: {k: v for k, v in r.items() if k != "flags"}
                   for n, r in results.items()},
        "random_nulls": nulls,
        "convergence_signal": {
            "panel": focus, "unanimous_items": conv_total, "split_items": split_total,
            "accuracy_when_unanimous": round(conv_correct / conv_total, 3) if conv_total else None,
            "accuracy_when_split": round(split_correct / split_total, 3) if split_total else None,
        },
        "risk_coverage": coverage_curve,
    }
    (run / "reliability_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps({k: metrics[k] for k in
                      ["panels", "random_nulls", "convergence_signal"]}, indent=2))

    # figure 1: panel accuracy with CIs vs random null band
    names = list(results)
    vals = [results[n]["accuracy"] for n in names]
    los = [results[n]["accuracy"] - results[n]["ci90"][0] for n in names]
    his = [results[n]["ci90"][1] - results[n]["accuracy"] for n in names]
    fig, ax = plt.subplots(figsize=(8.5, 4.6), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    if "RANDOM3" in nulls:
        ax.axhspan(nulls["RANDOM3"]["p05"], nulls["RANDOM3"]["p95"],
                   color=GRID, alpha=0.5, zorder=0)
    ax.bar(names, vals, yerr=[los, his], color=BLUE, width=0.55,
           error_kw={"ecolor": INK2, "capsize": 3}, zorder=2)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.015, f"{v:.2f}", ha="center", color=INK2, fontsize=9)
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", color=GRID, lw=0.6, zorder=1)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=MUTED)
    ax.set_ylabel("Majority-vote accuracy", color=INK2)
    ax.set_title("Panel strategies vs random-panel band (gray)", color=INK, pad=10)
    fig.tight_layout()
    fig.savefig(run / "panel_accuracy.png", dpi=200, facecolor=SURFACE)
    print(f"figures -> {run}/panel_accuracy.png")


if __name__ == "__main__":
    main()
