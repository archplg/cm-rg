#!/usr/bin/env python3
"""Score the reliability pilot: singles, panels, convergence signal, arm 2."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
OK, BAD = "#9ec5f4", "#d03b3b"  # sequential-light for correct, status-critical for error

W1_GOLD = json.loads(Path("answers.json").read_text())          # Q1..Q20
W2_GOLD = json.loads(Path("wave2_answers.json").read_text())    # W1..W10
R = json.loads(Path("responses.json").read_text())

MODELS = ["haiku", "sonnet", "opus", "fable"]
ITEMS = [f"Q{i}" for i in range(1, 21)] + [f"W{i}" for i in range(1, 11)]
GOLD = {**W1_GOLD, **W2_GOLD}


def norm(s):
    return str(s).strip().lower().replace(",", "").replace(" ", "")


def correct(model, item):
    return norm(R["singles"][model][item]) == norm(GOLD[item])


# singles
singles = {m: sum(correct(m, it) for it in ITEMS) for m in MODELS}

# panels (majority of 3; tie -> incorrect)
def majority(answers):
    from collections import Counter
    c = Counter(norm(a) for a in answers)
    top, n = c.most_common(1)[0]
    return top if n >= 2 else None

PANEL_D = ["haiku", "fable", "sonnet"]
PANEL_R = ["opus", "fable", "sonnet"]
panels = {}
for name, panel in [("D_diverse", PANEL_D), ("R_redundant", PANEL_R)]:
    acc = sum(majority([R["singles"][m][it] for m in panel]) == norm(GOLD[it]) for it in ITEMS)
    panels[name] = acc

# convergence signal: haiku (out-bloc) vs trio majority
conv, split = [], []
for it in ITEMS:
    trio_maj = majority([R["singles"][m][it] for m in ["sonnet", "opus", "fable"]])
    (conv if norm(R["singles"]["haiku"][it]) == trio_maj else split).append(it)
conv_acc = sum(majority([R["singles"][m][it] for m in MODELS[:3]]) == norm(GOLD[it]) for it in conv)
split_detail = [{"item": it, "haiku": R["singles"]["haiku"][it], "gold": GOLD[it],
                 "haiku_correct": correct("haiku", it)} for it in split]

# arm 2 (wave 2 only)
arm2 = {}
for cond in ["persona_Q", "persona_S", "persona_C", "neutral_1", "neutral_2", "neutral_3"]:
    arm2[cond] = sum(norm(R["arm2"][cond][it]) == norm(W2_GOLD[it]) for it in W2_GOLD)
persona_panel = sum(
    majority([R["arm2"][c][it] for c in ["persona_Q", "persona_S", "persona_C"]]) == norm(W2_GOLD[it])
    for it in W2_GOLD)
neutral_panel = sum(
    majority([R["arm2"][c][it] for c in ["neutral_1", "neutral_2", "neutral_3"]]) == norm(W2_GOLD[it])
    for it in W2_GOLD)
identical_across_runs = all(
    len({norm(R["arm2"][c][it]) for c in R["arm2"]}) == 1 for it in W2_GOLD)

scores = {
    "n_items": len(ITEMS),
    "singles_accuracy": {m: f"{singles[m]}/{len(ITEMS)}" for m in MODELS},
    "panel_D_diverse": f"{panels['D_diverse']}/{len(ITEMS)}",
    "panel_R_redundant": f"{panels['R_redundant']}/{len(ITEMS)}",
    "convergence": {
        "converged_items": len(conv), "split_items": len(split),
        "converged_majority_accuracy": f"{conv_acc}/{len(conv)}",
        "split_details": split_detail,
    },
    "arm2_wave2": {**{k: f"{v}/10" for k, v in arm2.items()},
                   "persona_panel_majority": f"{persona_panel}/10",
                   "neutral_panel_majority": f"{neutral_panel}/10",
                   "all_six_runs_identical": identical_across_runs},
}
Path("scores.json").write_text(json.dumps(scores, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(scores, indent=2, ensure_ascii=False))

# figure: correctness matrix 4 models x 30 items
fig, ax = plt.subplots(figsize=(11, 2.6), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
M = [[1 if correct(m, it) else 0 for it in ITEMS] for m in MODELS]
ax.imshow(M, cmap=ListedColormap([BAD, OK]), aspect="auto", vmin=0, vmax=1)
ax.set_yticks(range(4), MODELS, color=INK2, fontsize=10)
ax.set_xticks(range(len(ITEMS)), ITEMS, color=MUTED, fontsize=6.5, rotation=90)
for i in range(4):
    for j, it in enumerate(ITEMS):
        if not correct(MODELS[i], it):
            ax.text(j, i, "x", ha="center", va="center", color="#ffffff",
                    fontsize=9, fontweight="bold")
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(length=0)
ax.set_title("Correctness across 30 verifiable items (wave 1 + wave 2): one error in 120 answers",
             color=INK, fontsize=11, pad=10)
fig.tight_layout()
fig.savefig("correctness_matrix.png", dpi=200, facecolor=SURFACE)
print("figure written: correctness_matrix.png")
