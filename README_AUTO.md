# Автоматический запуск Archipelago cross-model

Краткая инструкция для запуска эксперимента с минимумом ручных шагов.

## Что внутри

В этой папке (`outputs/`):

- `archipelago_cross_model/` - распакованный архив со всеми скриптами и материалами
- `prereq_check.ps1` - предполётная проверка (Python, ключ, файлы, доступность OpenRouter, model IDs)
- `run_all.ps1` - сквозной запуск: pip install → dry-run → подтверждение → реальный прогон → весь анализ и рендеры → пакет финальных артефактов
- `AUDIT_REPORT.md` - результат аудита всех скриптов перед запуском (читать в первую очередь)
- `README_AUTO.md` - этот файл

## Что нужно сделать руками (один раз)

Эти шаги я физически не могу выполнить за тебя. Заняли бы у тебя ~15 минут:

1. Регистрация на https://openrouter.ai/ (Google или GitHub-логин)
2. Положить $50 на https://openrouter.ai/settings/credits (нужна работающая Visa/MC в долларах)
3. Создать API-ключ на https://openrouter.ai/settings/keys, имя `archipelago-experiment`
4. Установить Python 3.12 с https://www.python.org/downloads/ - **обязательно поставить галочку "Add python.exe to PATH"** на первом экране
5. Скопировать `archipelago_cross_model/` (из этой папки) в `C:\Users\Sergey\archipelago_cross_model\`
6. Открыть PowerShell, прописать ключ:
   ```powershell
   [Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-v1-ТВОЙ-КЛЮЧ", "User")
   ```
   После этого **закрыть и заново открыть** PowerShell.

## Что делает run_all.ps1

После того, как пункты 1-6 выше выполнены:

```powershell
# Шаг А. Проверка готовности (бесплатно, без сетевых вызовов сверх /models)
cd $HOME
.\prereq_check.ps1

# Шаг Б. Полный запуск
.\run_all.ps1
```

Скрипт `run_all.ps1` делает следующее, по порядку:

| Этап | Что | Платный? | Возможно прервать? |
|------|-----|----------|---------------------|
| 0 | Sanity-чек Python и ключа | нет | да, ошибкой |
| 1 | `pip install -r requirements.txt` | нет | да, ошибкой |
| 2 | `python run_experiment.py --dry-run` (проверка моделей, сметы) | нет | да, ошибкой |
| 3 | Интерактивный вопрос "Type YES" | - | да, любым ответом кроме YES |
| 3 | `python run_experiment.py` (реальный прогон, 30-90 мин, ~$45) | **ДА** | через закрытие окна; `--Resume` продолжит |
| 4 | `python analyze.py` | нет | да |
| 5 | `python operator_synthesis.py` | нет | да |
| 6 | `python visualizations.py` | нет | да |
| 7 | `python visualizations_interactive.py` | нет | да |
| 8 | `python render_for_coaches.py` | нет | да |
| 9 | `python render_for_ai_developers.py` | нет | да |
| 10 | `python render_for_business.py` | нет | да |
| 11 | `python export_for_paper.py` | нет | да |
| 12 | Складывает финальные артефакты в `FINAL_BUNDLE_<timestamp>/` | нет | - |

Полный лог пишется в `archipelago_cross_model/logs/run_all_<timestamp>.log` плюс per-step логи рядом.

## Флаги run_all.ps1

- `.\run_all.ps1` - полный прогон с интерактивным подтверждением
- `.\run_all.ps1 -SkipInstall` - не запускать pip install (если уже стоит)
- `.\run_all.ps1 -DryRunOnly` - только сухой прогон, без реальных вызовов
- `.\run_all.ps1 -Resume` - продолжить с прошлого чекпойнта (если предыдущий прогон сорвался)
- `.\run_all.ps1 -SkipExperiment` - данные уже собраны, только анализ и рендеры
- `.\run_all.ps1 -AutoConfirm` - **опасно**: пропустить запрос "Type YES" (потратит $45 без явного подтверждения)

## Что в итоге

После успешного прогона:

В `archipelago_cross_model/`:
- `results/` - сырые данные ячеек, state.json, run_manifest.json
- `logs/api_calls/` - полный аудит каждого API-вызова (system prompt, user prompt, raw response, latency, cost - всё)
- `analysis/` - FINDINGS.md, comparison_vs_pilot.md, per_cell_summary.csv, биплоты, тепловые карты
- `operator_outputs/`, `coach_kit/`, `ai_audit/`, `executive_briefing/`, `paper_outputs/` - целевые рендеры для разных аудиторий
- `FINAL_BUNDLE_<timestamp>/` - копии ключевых файлов в одной папке для удобной отправки

## Если что-то пошло не так

Все ошибки логируются. Открой `archipelago_cross_model/logs/run_all_<timestamp>.log`, найди строку с `ERR`.

Самое частое: `NOT FOUND in OpenRouter catalog` - значит slug модели изменился. Открыть https://openrouter.ai/models, найти текущий slug, обновить `archipelago_cross_model/config.yaml`, запустить `.\run_all.ps1` заново (dry-run снова проверит).

Все остальные сценарии описаны в разделе "Что делать, если что-то сломалось" в `INSTRUKCIYA_RU.md`.

## Аудит

Перед запуском прочитай `AUDIT_REPORT.md`. Там краткий вывод о состоянии всех скриптов и одно среднее замечание (M1 - почти наверняка нужно будет обновить slug модели на этапе dry-run, что штатно).
