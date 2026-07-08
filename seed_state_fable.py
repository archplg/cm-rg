#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ЗАСЕВ state.json для Phase 2L (добавление Fable как M12).

ЧТО ДЕЛАЕТ
  Читает готовый state.json из results_phase2j и строит новый state.json в
  results_phase2L, в котором у каждой из 14 ячеек СОХРАНЕНЫ свободные ответы
  11 моделей (Фаза 1), но СБРОШЕНЫ результаты Фаз 2-4 и статус.

ЗАЧЕМ
  При последующем запуске run_experiment.py --resume:
    - Фаза 1 пропустит 11 моделей (у них уже есть ответ) и догенерирует только
      Fable (M12) - экономия и, главное, изоляция эффекта Fable;
    - Фазы 2-4 пересчитаются заново на 12 элементах (новая анонимизация,
      новые конструкты, новая матрица оценок).

БЕЗОПАСНОСТЬ ДАННЫХ
  Ничего не перезаписывает в results_phase2j (только читает).
  Если results_phase2L/state.json уже существует - скрипт остановится, чтобы
  не затереть прогресс. Удалите его вручную, если нужен чистый засев.

ЗАПУСК (из корня проекта, там же где run_experiment.py)
  python seed_state_fable.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime

SRC = Path("./results_phase2j/state.json")
DST_DIR = Path("./results_phase2L")
DST = DST_DIR / "state.json"

# Какие модели считаем "старыми" - их ответы переносим. Fable (M12) НЕ переносим:
# его Фаза 1 должна выполниться заново под нужным промптом.
KEEP_MODELS = {f"M{i}" for i in range(1, 12)}   # M1..M11

# Поля Фаз 2-4, которые надо обнулить, чтобы они пересчитались на 12 элементах.
RESET_FIELDS = {
    "element_mapping": {},
    "element_summaries": {},
    "triad_assignments": {},
    "constructs": {},
    "constructs_raw": {},
    "ratings": {},
    "api_calls": [],
    "per_model_cost": {},
    "per_model_tokens": {},
    "cost_usd": 0.0,
    "tokens_in": 0,
    "tokens_out": 0,
    "errors": [],
}


def main():
    if not SRC.exists():
        print(f"ОШИБКА: не найден {SRC}.")
        print("Запустите скрипт из корня проекта (там, где папка results_phase2j).")
        sys.exit(1)
    if DST.exists():
        print(f"ОШИБКА: {DST} уже существует - не затираю прогресс.")
        print("Если нужен чистый засев, удалите этот файл вручную и запустите снова.")
        sys.exit(1)

    with open(SRC, "r", encoding="utf-8") as f:
        src_state = json.load(f)

    src_cells = src_state.get("cells", {})
    new_cells = {}
    report = []

    for cid, cell in src_cells.items():
        fr = cell.get("free_responses", {})
        # переносим только непустые строковые ответы старых моделей
        kept = {sn: txt for sn, txt in fr.items()
                if sn in KEEP_MODELS and isinstance(txt, str) and txt.strip()}

        new_cell = {
            "cell_id": cell["cell_id"],
            "task": cell["task"],
            "condition": cell["condition"],
            "run_idx": cell["run_idx"],
            "status": "pending",          # НЕ complete - чтобы ячейка пересчиталась
            "started_at": "",
            "completed_at": "",
            "random_seed": 0,
            "free_responses": kept,       # 11 ответов сохранены, M12 отсутствует
        }
        new_cell.update(RESET_FIELDS)
        new_cells[cid] = new_cell
        report.append((cid, len(kept)))

    DST_DIR.mkdir(parents=True, exist_ok=True)
    out = {
        "started_at": datetime.now().isoformat(),
        "total_cost_usd": 0.0,
        "cells": new_cells,
    }
    with open(DST, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    # ----- статус-футер -----
    print(f"Засев готов: {DST}")
    print(f"Ячеек перенесено: {len(new_cells)}")
    print("Свободных ответов сохранено по ячейкам (ожидается 11 в каждой):")
    problems = 0
    for cid, n in sorted(report):
        flag = "" if n == 11 else "  <-- ВНИМАНИЕ: не 11"
        if n != 11:
            problems += 1
        print(f"  {cid}: {n}{flag}")
    print("-" * 50)
    print("СТАТУС")
    print(f"  Ячеек: {len(new_cells)} из 14 ожидаемых")
    print(f"  Ячеек с неполным набором ответов (не 11): {problems}")
    print("  Дальше: запустить run_experiment.py --resume с config_phase2L_fable.yaml")
    if problems:
        print("  ФЛАГ: в части ячеек не 11 ответов - проверьте 2J перед прогоном,")
        print("  иначе элементов в этих ячейках будет меньше 12.")


if __name__ == "__main__":
    main()
