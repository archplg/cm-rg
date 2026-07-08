# CM-RG Release Bundle - Deploy Guide

**Финальная версия: июнь 2026.** Все артефакты для публикации CM-RG (Cross-Model Repertory Grid) разложены по 7 папкам назначения. Эта инструкция объясняет, что куда отправлять и в каком порядке.

---

## Краткая карта папок

| Папка | Куда отправить | Когда |
|---|---|---|
| `01_arxiv_submission/` | arxiv.org | После external review |
| `02_huggingface_dataset/` | huggingface.co/datasets/sergeydolgov/cross-model-repertory-grid | Шаг 1 |
| `03_github_repo/` | github.com/archplg/cm-rg | Шаг 2 |
| `04_website_deploy/` | crossmodelrg.org (Vercel/Netlify) | Шаг 3 |
| `05_zenodo_bundle/` | zenodo.org через GitHub release | Шаг 4 |
| `06_for_external_reviewer/` | email одному рецензенту | Шаг 5 (параллельно) |
| `07_russian_audience/` | Habr / archplg.co.uk | Шаг 6 (когда готовы) |

---

## ⚠️ Важно: новая команда HuggingFace CLI

С июня 2026 команда `huggingface-cli` помечена как **deprecated**. Используйте новую утилиту `hf`:

```powershell
# Установка (если ещё не установлен)
pip install -U huggingface_hub

# Проверка версии
hf --version

# Login
hf auth login
```

---

## Пошаговая инструкция

### Шаг 1: HuggingFace Dataset Upload

**Папка:** `02_huggingface_dataset/`
**Содержит:** README.md, CITATION.cff, LICENSE, metadata.json, data/*.parquet (5 файлов)

```powershell
cd C:\Users\Sergey\archipelago_cross_model\release_bundle\02_huggingface_dataset

# Login (если ещё не сделано)
hf auth login

# Upload
hf upload sergeydolgov/cross-model-repertory-grid . --repo-type=dataset
```

**Что произойдёт:** parquet файлы и метаданные загрузятся на HF Hub. README.md автоматически станет dataset card.

**Время:** ~3-5 минут (объём ~1.9 MB).

---

### Шаг 2: GitHub Repo Push

**Папка:** `03_github_repo/`
**Содержит:** README.md, DATASET_CARD.md, .gitignore, scripts/, configs/, tasks/, analysis_outputs/

```powershell
cd C:\Users\Sergey\archipelago_cross_model\release_bundle\03_github_repo

# Инициализация git репо
git init
git add .
git commit -m "CM-RG v1.0: 11 frontier LLMs, 5 phases, 110,882 ratings + Phase 2K paired"

# Push на GitHub (репо archplg/cm-rg должен быть создан заранее на github.com)
git remote add origin https://github.com/archplg/cm-rg.git
git branch -M main
git push -u origin main

# Создать v1.0 release (для Zenodo DOI)
git tag v1.0
git push origin v1.0
```

**Что произойдёт:** код, конфиги, briefs задач, результаты анализа загрузятся в публичный репо. README.md появится на главной странице.

**Время:** ~5 минут.

**Размер:** ~250 KB кода + конфигов.

---

### Шаг 3: Website Deploy

**Папка:** `04_website_deploy/`
**Содержит:** index.html, styles.css, app.js, translations.json (RU/EN/ZH), README.md

#### Опция A: Vercel (рекомендую)

```powershell
cd C:\Users\Sergey\archipelago_cross_model\release_bundle\04_website_deploy
npx vercel
# Выбрать: scope, project name, "Y" на defaults
```

После деплоя:
1. Открыть проект на vercel.com
2. Settings → Domains → Add → crossmodelrg.org
3. У регистратора домена добавить DNS-записи (Vercel покажет какие)

#### Опция B: Netlify

1. Открыть https://app.netlify.com/drop
2. Перетащить папку `04_website_deploy/` целиком
3. Netlify выдаст временный URL → переименовать в Settings → Domain management

#### Опция C: Cloudflare Pages

```powershell
npx wrangler pages deploy . --project-name=cm-rg
```

**Время:** ~5 минут на деплой + DNS-настройка может занять до 24 часов.

---

### Шаг 4: Zenodo DOI

**Папка:** `05_zenodo_bundle/INSTRUCTIONS.md`

После шага 2 (GitHub push):

1. Зайти на https://zenodo.org/account/settings/github/
2. Authorize Zenodo для GitHub доступа
3. Включить toggle для `archplg/cm-rg`
4. На GitHub: создать release v1.0 (`Releases → Draft a new release → Tag v1.0`)
5. Zenodo автоматически создаст DOI

После получения DOI:
- Обновить `CITATION.cff` в HuggingFace dataset (Шаг 1) с реальным DOI
- Обновить README badges на GitHub
- Обновить translations.json на сайте

**Время:** ~10 минут.

---

### Шаг 5: External Reviewer Send

**Папка:** `06_for_external_reviewer/`
**Содержит:** 00_REVIEWER_LETTER.md (готовое сопроводительное письмо) + 7 файлов с данными

**Кому послать (в порядке вероятности позитивного ответа):**
1. **Niels Rogge** (HuggingFace, Datasets/Papers-with-Code lead) - идеален для dataset publication
2. **Thomas Wolf** (HuggingFace co-founder) - публичный контакт
3. **Rishi Bommasani** (Stanford CRFM, HELM team lead) - методологический peer
4. **James Ehrlich** (Stanford referral, если есть знакомство)
5. **Scott** (Anthropic partner, если есть знакомство)

**Зип папку и приложить к email** + текст из `00_REVIEWER_LETTER.md`.

**Время на рецензию:** 1-2 недели ожидания + 2-4 часа их работы.

---

### Шаг 6: arxiv Submission

**Папка:** `01_arxiv_submission/`
**Содержит:** paper_draft_v1.md, arxiv_abstract_v1.md

**Только после получения external review feedback** (Шаг 5):

1. Конвертировать paper_draft_v1.md в .pdf (Pandoc) или .tex (для arxiv preferred):
   ```powershell
   # Markdown → PDF (быстрее)
   pandoc paper_draft_v1.md -o paper_v1.pdf --pdf-engine=xelatex --variable mainfont="DejaVu Sans"

   # Или Markdown → LaTeX (для arxiv стандарта)
   pandoc paper_draft_v1.md -o paper_v1.tex
   ```

2. Зайти на https://arxiv.org/submit
3. Выбрать категорию: cs.CL (Computation and Language) + co-list cs.AI, cs.LG
4. Заполнить metadata из arxiv_abstract_v1.md:
   - Title: «Cross-Model Repertory Grid: Lab-Specific Persona Volatility in Frontier LLM Ensembles»
   - Authors: Sergey Dolgov (ORCID: 0000-0001-5455-7048)
   - Abstract: первые 250 слов из abstract секции
   - Keywords: cross-model evaluation, evaluative diversity, repertory grid, frontier LLMs, calibration drift
5. Upload paper_v1.pdf (или .tex)
6. Submit

**Время на arxiv approval:** 1-3 дня. После одобрения - paper становится публично доступен.

---

### Шаг 7: Russian Content Distribution

**Папка:** `07_russian_audience/`
**Содержит:** АНАЛИТИЧЕСКИЙ_ОТЧЁТ_ДЛЯ_ВСЕХ_v2.md (~127 KB), визуализации_отчёта.html

**Куда:**
- **Habr (https://habr.com)**: основной отчёт как long-form статью. Разбить на 3-4 части если слишком длинный.
- **LinkedIn**: краткое summary с ссылкой на главный отчёт.
- **Telegram channel Archipelago**: ссылки на arxiv + HF + сайт + отчёт.
- **archplg.co.uk blog**: полный отчёт как страница.

**Время:** ~2 часа на адаптацию текста + размещение.

---

## Зависимости между шагами

```
Шаг 1 (HF dataset) ─────┐
Шаг 2 (GitHub repo) ────┤── параллельно
Шаг 3 (Website) ────────┘
        ↓
Шаг 4 (Zenodo DOI) ── requires Шаг 2
        ↓
Update CITATION.cff с реальным DOI на HF и GitHub
        ↓
Шаг 5 (External reviewer) ── параллельно с 1-4
        ↓ (через 1-2 недели)
Шаг 6 (arxiv submission) ── после feedback от reviewer
        ↓
Шаг 7 (Russian distribution) ── после arxiv approval
```

---

## Чек-лист готовности

Перед каждым шагом проверьте:

**Шаг 1 (HF):**
- [ ] HF account создан и подтверждён email
- [ ] `hf --version` показывает версию
- [ ] `hf auth login` успешно выполнен (введён HF access token)
- [ ] Пустой dataset `sergeydolgov/cross-model-repertory-grid` создан на huggingface.co

**Шаг 2 (GitHub):**
- [ ] Git установлен (`git --version`)
- [ ] GitHub аккаунт `archplg` создан
- [ ] Пустое репо `archplg/cm-rg` создано на github.com
- [ ] SSH key или Personal Access Token настроен

**Шаг 3 (Website):**
- [ ] Node.js установлен (для `npx vercel`)
- [ ] Vercel account создан (или Netlify/Cloudflare)
- [ ] Домен crossmodelrg.org куплен и доступ к DNS-настройкам есть

**Шаг 4 (Zenodo):**
- [ ] Zenodo account создан (можно через ORCID login)
- [ ] GitHub integration authorized

**Шаг 5 (Reviewer):**
- [ ] Контакт ревьюера актуален
- [ ] Готовы ответить на feedback в течение 1-3 дней

**Шаг 6 (arxiv):**
- [ ] arxiv account создан (через ORCID или вручную)
- [ ] Endorsement получен (если первая публикация в категории cs.CL)
- [ ] PDF из markdown сконвертирован и проверен
- [ ] Reviewer feedback инкорпорирован в финальный paper

---

## Полезные ссылки

- **HuggingFace docs (новый hf CLI):** https://huggingface.co/docs/huggingface_hub/main/en/guides/cli
- **arxiv submission guide:** https://info.arxiv.org/help/submit/index.html
- **Zenodo GitHub integration:** https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content
- **Vercel deploy docs:** https://vercel.com/docs/getting-started

---

**Confidence в этом плане:** 9/10. Снимаю 1 пункт потому что: a) `hf` CLI новая, поведение в edge cases может отличаться от прежнего `huggingface-cli`; b) arxiv endorsement (если требуется) - неопределённый по времени блокирующий шаг для первой публикации в cs.CL.

---

*Bundle создан: июнь 2026. Каждые 3 месяца стоит пересоздавать с обновлёнными данными новых фронтирных моделей (Quarterly Diversity Report).*
