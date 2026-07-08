#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ФАЗА 1 для Claude Fable 5: свободные ответы по 7 задачам CM-RG.

ЧТО ДЕЛАЕТ
  Прогоняет Fable 5 через Фазу 1 (free response) по тем же 7 брифам и с теми же
  промптами, что и остальные 11 моделей в Фазе 2J. Это превращает Fable в новый
  элемент (E12), который дальше встанет в кросс-оценивание.

ПОЧЕМУ ЗАНОВО
  Прежняя проба Fable шла по сокращённым русским заглушкам - несопоставимо с картой.
  Здесь используются НАСТОЯЩИЕ брифы (англоязычные, 5 вариантов) из task_*_brief.md
  и дословные промпты из run_experiment.py.

СРЕДА
  OpenRouter, slug anthropic/claude-fable-5 - та же среда, что у остальных 11 моделей.
  Ключ читается ТОЛЬКО из переменной окружения OPENROUTER_API_KEY, нигде не пишется.

ГРАНИЦА
  Это только Фаза 1 (Fable как элемент). Чтобы добавить Fable на карту (Вариант Б),
  дальше нужны Фазы 2-4 на 12 элементах для ВСЕХ моделей - см. примечание в конце.

ВХОД
  Положите рядом 7 файлов брифов: task_A_brief.md ... task_G_brief.md
  (5-вариантные версии, НЕ A10/D10/G10).

ЗАПУСК
  Windows PowerShell:  $env:OPENROUTER_API_KEY="sk-or-..."
  Windows cmd:         set OPENROUTER_API_KEY=sk-or-...
  pip install requests
  python fable_phase1.py
"""

import os
import sys
import json
import time
import glob
import datetime
import requests

# ----------------------- ПАРАМЕТРЫ -----------------------
OR_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_SLUG = "anthropic/claude-fable-5"           # подтверждено в каталоге OpenRouter
MODEL_FALLBACK = "anthropic/claude-opus-4.8"      # как у M11 в вашем конфиге

# FLAG: точные значения free_response заданы в config_phase2j.yaml, которого нет.
# Это разумные дефолты для свободных ответов; ЗАМЕНИТЕ на значения из 2J для точности.
TEMPERATURE = 0.7        # FLAG - сверить с config_phase2j.yaml
MAX_TOKENS = 4000        # FLAG - сверить с config_phase2j.yaml

REPS = 5                 # повторений на (задача, условие); в дизайне 5-10
CONDITION = "N"          # Фаза 1 для карты строится на N-ячейках (2K переиспользует N из 2J)
PAUSE_SEC = 1.5
RETRIES = 3
RETRY_BACKOFF = [2, 5, 15]
TIMEOUT = 180
OUT = "fable_phase1_result.json"

TASKS = ["A", "B", "C", "D", "E", "F", "G"]
BRIEF_PATTERN = "task_{t}_brief.md"

# Дословно из run_experiment.py (условие N)
NEUTRAL_PROMPT = ("You are an analyst. Read the brief carefully and provide your "
                  "best-reasoned recommendation.")
USER_SUFFIX = ("\n\nProvide your recommendation in 200-400 words. Advocate for a "
               "specific position; do not enumerate all options.")


def load_brief(task):
    path = BRIEF_PATTERN.format(t=task)
    if not os.path.exists(path):
        print(f"ОШИБКА: не найден файл брифа {path} в текущей папке.")
        print("Положите 5-вариантные брифы task_A_brief.md ... task_G_brief.md рядом.")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def call_openrouter(key, sys_prompt, user_msg):
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body = {
        "model": MODEL_SLUG,   # OpenRouter авто-фолбэк при ошибке
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "system", "content": sys_prompt},
                     {"role": "user", "content": user_msg}],
    }
    last = None
    for attempt in range(RETRIES):
        try:
            r = requests.post(OR_URL, headers=headers, json=body, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.json()
            last = f"HTTP {r.status_code}: {r.text[:300]}"
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        if attempt < RETRIES - 1:
            time.sleep(RETRY_BACKOFF[min(attempt, len(RETRY_BACKOFF) - 1)])
    raise RuntimeError(last)


def main():
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print('ОШИБКА: задайте OPENROUTER_API_KEY (ключ начинается с sk-or-).')
        sys.exit(1)

    briefs = {t: load_brief(t) for t in TASKS}
    results = []
    flagged = 0
    errors = 0
    total = len(TASKS) * REPS

    print(f"Фаза 1 для {MODEL_SLUG}: {total} ячеек "
          f"({len(TASKS)} задач x условие {CONDITION} x {REPS} повторений)\n" + "=" * 60)

    i = 0
    for t in TASKS:
        user_msg = briefs[t] + USER_SUFFIX
        for rep in range(1, REPS + 1):
            i += 1
            row = {"task": t, "condition": CONDITION, "rep": rep,
                   "responder": None, "text": None, "len_words": None,
                   "flagged": False, "error": None}
            try:
                data = call_openrouter(key, NEUTRAL_PROMPT, user_msg)
                msg = data["choices"][0]["message"]
                text = msg.get("content") or ""
                row["text"] = text
                row["len_words"] = len(text.split())
                # какая модель реально ответила (OpenRouter возвращает в поле model)
                row["responder"] = data.get("model")
                # флаг: ответил не Fable (фолбэк/подмена) или подозрительно короткий ответ
                if row["responder"] and MODEL_SLUG.split("/")[-1] not in row["responder"]:
                    row["flagged"] = True
                if row["len_words"] is not None and row["len_words"] < 120:
                    row["flagged"] = True
                if row["flagged"]:
                    flagged += 1
            except Exception as e:
                row["error"] = str(e)
                errors += 1
            results.append(row)
            mark = "  [ФЛАГ]" if row["flagged"] else ""
            err = f"  ОШИБКА: {row['error']}" if row["error"] else ""
            print(f"[{i}/{total}] {t}-{CONDITION}-r{rep} -> "
                  f"{row['responder']} / {row['len_words']} слов{mark}{err}")
            time.sleep(PAUSE_SEC)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    clean = total - flagged - errors
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print("=" * 60)
    print(f"СТАТУС ({ts})")
    print(f"  Всего ячеек: {total}")
    print(f"  Чистых: {clean}")
    print(f"  Под флагом (подмена/короткий ответ): {flagged}")
    print(f"  Ошибок: {errors}")
    print(f"  Осталось: 0")
    print(f"  Файл: {OUT}")
    print("  ВНИМАНИЕ: ответы под флагом проверьте вручную перед вводом в пайплайн.")
    print("  ГРАНИЦА: это только Фаза 1 (Fable как элемент E12). Для карты на 12")
    print("  моделях дальше нужны Фазы 2-4 для ВСЕХ моделей на расширенном наборе")
    print("  элементов - это уже работа в коде вашего пайплайна.")


if __name__ == "__main__":
    main()
