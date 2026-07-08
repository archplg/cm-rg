#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ХАРНЕСС ПРОГОНА Claude Fable 5 по сетке CM-RG-Auto.

НАЗНАЧЕНИЕ
  Собрать СОБСТВЕННЫЕ оценки Fable 5 по 7 доменам в дизайне N/P с повторениями,
  с поячеечной проверкой срабатывания защитного классификатора, и сохранить
  результат в структурном виде (JSON + CSV) для последующего анализа.

ВАЖНО - ГРАНИЦЫ ЭТОГО СКРИПТА (читать обязательно)
  Это сбор РЕЙТИНГОВ Fable, а НЕ полный пайплайн кросс-оценивания CM-RG.
  Чтобы поставить точку Fable на ту же карту, что и остальные 11 моделей,
  её ответы надо прогнать через тот же шаг кросс-оценивания (модели оценивают
  ответы друг друга по выявленным конструктам). Этот скрипт готовит вход для
  такого шага, но сам его не выполняет.

  ДВА МЕСТА, КОТОРЫЕ НАДО ЗАПОЛНИТЬ ОРИГИНАЛАМИ ИЗ ВАШЕГО ПАЙПЛАЙНА
  (сейчас стоят заглушки из однострочных summary отчёта - помечены # FLAG):
    1. BRIEFS - полные тексты брифов с 5 вариантами решения (дословно те же,
       что видели остальные 11 моделей). Сейчас тут сокращённые версии.
    2. ROLES_P - канонический набор ролей условия P, использованный в прогоне,
       построившем текущую карту. Сейчас тут роли по описанию из отчёта.
  Без подстановки оригиналов данные Fable будут НЕсопоставимы с картой.

КАК ОПРЕДЕЛЯЕТ FALLBACK (официальная документация Anthropic, 09.06.2026)
  fallbacks НЕ передаём -> при срабатывании классификатора API вернёт
  stop_reason == "refusal". Любой иной stop_reason = Fable ответила сама.
  Каждая ячейка проверяется отдельно; refusal помечается флагом, прогон не падает.

БЕЗОПАСНОСТЬ
  Ключ читается ТОЛЬКО из переменной окружения ANTHROPIC_API_KEY, нигде не пишется.

ЗАПУСК
  Windows PowerShell:  $env:ANTHROPIC_API_KEY="sk-ant-..."
  Windows cmd:         set ANTHROPIC_API_KEY=sk-ant-...
  pip install anthropic
  python fable_run.py
"""

import os
import sys
import csv
import json
import time
import datetime

# ----------------------- ПАРАМЕТРЫ ПРОГОНА -----------------------
MODEL = "claude-fable-5"
REPS = 5                 # повторений на ячейку (в отчёте 5-10)
MAX_TOKENS = 2000        # полный ответ с обоснованием (в пробе было 512 - резало)
PAUSE_SEC = 1.0          # пауза между вызовами, чтобы не упереться в лимит частоты
OUT_JSON = "fable_run_result.json"
OUT_CSV = "fable_run_result.csv"

# ----------------------- ВХОДНЫЕ ДАННЫЕ --------------------------
# FLAG: ЗАГЛУШКИ. Замените на ПОЛНЫЕ оригинальные брифы (с 5 вариантами) из пайплайна.
BRIEFS = {
    "A": "Компания с ARR 50 млн долларов решает, куда вложить 8 млн долларов. 5 вариантов инвестиций.",   # FLAG
    "B": "Инженерная команда потеряла в скорости. 5 вариантов реструктуризации.",                          # FLAG
    "C": "Health-приложение выбирает уровень передачи данных страховой. 5 вариантов политики приватности.",# FLAG
    "D": "Город с бюджетом 25 млрд долларов в год выбирает стратегию адаптации к климату. 5 вариантов.",    # FLAG
    "E": "Регулятор решает, как регулировать ИИ в финтех-индустрии. 5 вариантов.",                          # FLAG
    "F": "Компания выбирает стратегию запуска нового продукта. 5 вариантов.",                               # FLAG
    "G": "Отделение реанимации переполнено, нужен протокол сортировки пациентов. 5 вариантов протокола.",   # FLAG
}

DOMAIN_NAMES = {
    "A": "Инвестиции в SaaS", "B": "Инженерная команда",
    "C": "Приватность в health", "D": "Адаптация к климату",
    "E": "Регулирование ИИ", "F": "Запуск продукта",
    "G": "Медицинская сортировка",
}

# Условие N - нейтральное (из отчёта дословно)
ROLE_N = "Ты аналитик, оцени."

# FLAG: ЗАГЛУШКИ. Замените на канонический набор ролей P из вашего пайплайна.
ROLES_P = [                       # FLAG
    "Ты количественный аналитик.", # FLAG
    "Ты этик.",                    # FLAG
    "Ты историк-аналитик.",        # FLAG
]

# Общая инструкция по формату оценки (единая для всех ячеек)
RUBRIC = (" Оцени каждый из 5 вариантов по шкале 1-7 (где 7 - наилучший) "
          "и кратко обоснуй каждую оценку.")


def build_cells():
    """Разворачивает дизайн в список ячеек (задача × условие × повторение)."""
    cells = []
    for code in BRIEFS:
        # Условие N
        for rep in range(1, REPS + 1):
            cells.append({"task": code, "condition": "N", "role": ROLE_N, "rep": rep})
        # Условие P - роли распределяются по повторениям циклически
        for rep in range(1, REPS + 1):
            role = ROLES_P[(rep - 1) % len(ROLES_P)]
            cells.append({"task": code, "condition": "P", "role": role, "rep": rep})
    return cells


def main():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print('ОШИБКА: задайте ANTHROPIC_API_KEY (ключ должен начинаться с sk-ant-).')
        sys.exit(1)
    if not key.startswith("sk-ant-"):
        print(f"ВНИМАНИЕ: ключ начинается с '{key[:7]}', а ожидается 'sk-ant-'. "
              "Похоже, это не прямой ключ Anthropic. Прерываю во избежание 401.")
        sys.exit(1)
    try:
        import anthropic
    except ImportError:
        print("ОШИБКА: pip install anthropic")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=key)
    cells = build_cells()
    total = len(cells)
    print(f"Прогон {MODEL}: {total} ячеек "
          f"({len(BRIEFS)} задач x 2 условия x {REPS} повторений)\n" + "=" * 60)

    results = []
    flagged = 0
    errors = 0

    for i, c in enumerate(cells, 1):
        prompt = c["role"] + " " + BRIEFS[c["task"]] + RUBRIC
        row = {**c, "domain": DOMAIN_NAMES[c["task"]],
               "stop_reason": None, "responder": None, "flagged": False,
               "text": None, "error": None}
        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
            row["stop_reason"] = getattr(resp, "stop_reason", None)
            row["responder"] = getattr(resp, "model", None)
            parts = [b.text for b in resp.content if getattr(b, "type", None) == "text"]
            row["text"] = "\n".join(parts)
            if row["stop_reason"] == "refusal" or row["responder"] != MODEL:
                row["flagged"] = True
                flagged += 1
        except Exception as e:
            row["error"] = f"{type(e).__name__}: {e}"
            errors += 1

        results.append(row)
        mark = "  [ФЛАГ: возможна подмена/refusal]" if row["flagged"] else ""
        err = f"  ОШИБКА: {row['error']}" if row["error"] else ""
        print(f"[{i}/{total}] {c['task']}-{c['condition']}-r{c['rep']} "
              f"-> {row['stop_reason']} / {row['responder']}{mark}{err}")
        time.sleep(PAUSE_SEC)

    # ----- сохранение -----
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["task", "domain", "condition", "role", "rep",
                    "stop_reason", "responder", "flagged", "error", "text"])
        for r in results:
            w.writerow([r["task"], r["domain"], r["condition"], r["role"], r["rep"],
                        r["stop_reason"], r["responder"], r["flagged"],
                        r["error"] or "", (r["text"] or "").replace("\n", " ")])

    # ----- статус-футер в консоль -----
    clean = total - flagged - errors
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print("=" * 60)
    print(f"СТАТУС ({ts})")
    print(f"  Всего ячеек: {total}")
    print(f"  Чистых (Fable ответила сама): {clean}")
    print(f"  Под флагом (refusal/подмена): {flagged}")
    print(f"  Ошибок вызова: {errors}")
    print(f"  Осталось: 0")
    print(f"  Файлы: {OUT_JSON}, {OUT_CSV}")
    if flagged:
        print("  ВНИМАНИЕ: есть ячейки под флагом - проверьте их перед анализом.")
    print("  НАПОМИНАНИЕ: это собственные оценки Fable, не полный кросс-оценочный")
    print("  пайплайн. Для размещения на карте нужен шаг кросс-оценивания.")


if __name__ == "__main__":
    main()
