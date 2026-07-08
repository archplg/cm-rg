"""
Phase 2L · Диагностика что произошло с A_FB (Fable) на каждом этапе pipeline.

Проходит все 4 фазы + analysis + map, и показывает где Fable есть, а где нет.
Cost: $0.
"""
from __future__ import annotations

import json
from pathlib import Path

RESULTS = Path("./results_phase2l")

print("=" * 80)
print("ДИАГНОСТИКА A_FB (Claude Fable 5) в pipeline Phase 2L")
print("=" * 80)

# Phase 1 - free response
print("\n[Phase 1] Free responses:")
p1_dir = RESULTS / "phase1_free_response"
p1_cells = list(p1_dir.rglob("A_FB.json"))
print(f"  Найдено A_FB cells: {len(p1_cells)}/14 ожидаемых")
for c in sorted(p1_cells)[:3]:
    try:
        d = json.loads(c.read_text(encoding="utf-8"))
        resp_len = len(d.get("response", ""))
        print(f"    {c.relative_to(p1_dir)}: response_length={resp_len}")
    except Exception as e:
        print(f"    {c.relative_to(p1_dir)}: PARSE_ERROR {e}")
if len(p1_cells) == 0:
    print("  -> Fable Phase 1 НЕ ЗАПУСКАЛАСЬ. Запусти: python run_phase2l.py --phase 1")

# Phase 2 - anonymized
print("\n[Phase 2] Anonymized:")
p2_dir = RESULTS / "phase2_anonymized"
p2_cells = list(p2_dir.rglob("A_FB.json"))
print(f"  Найдено A_FB cells: {len(p2_cells)}/14 ожидаемых")

# Phase 3 - constructs
print("\n[Phase 3] Constructs:")
p3_dir = RESULTS / "phase3_constructs"
p3_cells = list(p3_dir.rglob("A_FB.json"))
print(f"  Найдено A_FB cells: {len(p3_cells)}/14 ожидаемых")
for c in sorted(p3_cells)[:3]:
    try:
        d = json.loads(c.read_text(encoding="utf-8"))
        n = d.get("n_constructs", 0)
        print(f"    {c.relative_to(p3_dir)}: n_constructs={n}")
    except Exception as e:
        print(f"    {c.relative_to(p3_dir)}: PARSE_ERROR {e}")

# Phase 4 - ratings
print("\n[Phase 4] Cross-ratings:")
p4_dir = RESULTS / "phase4_ratings"
p4_cells = list(p4_dir.rglob("A_FB.json"))
print(f"  Найдено A_FB cells (Fable как rater): {len(p4_cells)}/14 ожидаемых")
total_cost = 0
good_cells = 0
for c in sorted(p4_cells):
    try:
        d = json.loads(c.read_text(encoding="utf-8"))
        ok = d.get("ok_batches", 0)
        n = d.get("n_batches", 0)
        cost = d.get("total_cost_usd", 0)
        total_cost += cost
        if ok > 0:
            good_cells += 1
        print(f"    {c.relative_to(p4_dir)}: {ok}/{n} batches, ${cost:.4f}")
    except Exception as e:
        print(f"    {c.relative_to(p4_dir)}: PARSE_ERROR {e}")
print(f"  Хороших cells: {good_cells}/{len(p4_cells)}")
print(f"  Total spent: ${total_cost:.4f}")

# Analysis
print("\n[Analysis] analysis_results.json:")
analysis = RESULTS / "analysis_results.json"
if analysis.exists():
    data = json.loads(analysis.read_text(encoding="utf-8"))
    in_consensus = "A_FB" in (data.get("divergence_summary") or {})
    print(f"  A_FB в divergence_summary: {'ДА' if in_consensus else 'НЕТ'}")
    if in_consensus:
        c = data["divergence_summary"]["A_FB"]
        print(f"    consensus score: {c:.3f}")

    # Check inter-rater correlations
    corrs = data.get("inter_rater_corrs") or {}
    found_in_corrs = 0
    sample_corrs = {}
    for key, corr_dict in corrs.items():
        if any("A_FB" in pair for pair in corr_dict.keys()):
            found_in_corrs += 1
            if not sample_corrs:
                # Get sample correlations for A_FB
                for pair, r in corr_dict.items():
                    if "A_FB" in pair and abs(r) > 0:
                        sample_corrs[pair] = r
                        if len(sample_corrs) >= 5:
                            break
    print(f"  A_FB в inter_rater_corrs: {found_in_corrs} из {len(corrs)} (task, cond) комбинаций")
    if sample_corrs:
        print(f"  Sample корреляции A_FB:")
        for pair, r in list(sample_corrs.items())[:5]:
            print(f"    {pair}: r={r:.3f}")
else:
    print(f"  ОШИБКА: {analysis} не найден. Запусти: python analyze_phase2l.py")

# Map
print("\n[Map] archplg_phase2l_map.html:")
map_path = RESULTS / "archplg_phase2l_map.html"
if map_path.exists():
    text = map_path.read_text(encoding="utf-8")
    in_map = "A_FB" in text
    in_meta = "claude fable" in text.lower()
    print(f"  A_FB в HTML: {'ДА' if in_map else 'НЕТ'}")
    print(f"  'claude fable' в HTML: {'ДА' if in_meta else 'НЕТ'}")
else:
    print(f"  ОШИБКА: {map_path} не найден. Запусти: python generate_archipelago_map.py")

print("\n" + "=" * 80)
print("ВЕРДИКТ:")
print("=" * 80)
if len(p4_cells) == 0:
    print("Phase 4 для A_FB НЕ ВЫПОЛНЯЛАСЬ.")
    print("Что делать: запусти python run_phase2l.py --phase all")
elif good_cells == 0:
    print(f"Phase 4 для A_FB выполнилась но ВСЕ cells битые ({len(p4_cells)} с 0 batches).")
    print("Что делать: удалить плохие cells и перезапустить.")
    print("Команда: del results_phase2l\\phase4_ratings\\*\\*\\A_FB.json (для cleanup)")
elif analysis.exists() and "A_FB" not in (json.loads(analysis.read_text(encoding='utf-8')).get('divergence_summary') or {}):
    print("A_FB есть на диске но НЕ ПОПАЛА в analysis.")
    print("Что делать: python analyze_phase2l.py (пересоберёт analysis_results.json)")
elif map_path.exists() and "A_FB" not in map_path.read_text(encoding="utf-8"):
    print("A_FB в analysis есть но НЕ в map.")
    print("Что делать: python generate_archipelago_map.py")
else:
    print("A_FB ДОЛЖЕН БЫТЬ в map. Проверь визуально - возможно остров маленький и сливается.")
