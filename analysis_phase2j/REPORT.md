# Phase 2J - Analysis Report

**Data:** 14 cells from Phase 2J (443 constructs aggregated).
**Models analyzed:** 11 (M1-M11, where M11 = Claude Opus 4.8).
**Wall time:** 12 часов 16 минут (28.05.2026 19:42 - 29.05.2026 07:59).
**Cost (из первичного источника - `usage.cost` в audit-файлах):** **$15.32 actual Phase 2J cost** (455 API calls × 14 cells × 4 phases). Скрипт записал $12.27 (недосчёт +$3.05 = +$2.32 на M11 из-за slug mismatch + $0.73 на reasoning tokens у M4/M5/M9). OpenRouter activity CSV показал $18.96 в окне Phase 2J - разница $3.64 это **параллельные эксперименты пользователя** на той же учётке (не Phase 2J). Полная сверка - в `cost_audit_phase2j.md`.

## H1. Cluster stability (Opus 4.7 vs 4.8)

- M1 (Opus 4.7) at: PC1=-4.852, PC2=2.778
- M11 (Opus 4.8) at: PC1=-4.777, PC2=2.551
- PC1 distance: 0.075 (threshold for H1 support: < 3.0)
- Euclidean 2D distance: 0.239
- Median pairwise distance in core (6 models): 2.637
- **H1 SUPPORTED**.
- Opus 4.8 lands 0.24 units from Opus 4.7 in 2D PCA space. Median pairwise distance among 6 core models is 2.64. Opus 4.8 is INSIDE the core cluster.

## H2. Calibration drift (Opus 4.7 -> 4.8)

- M1 (Opus 4.7) mean rating: 3.569
- M11 (Opus 4.8) mean rating: 3.574
- Delta: +0.005 (Opus 4.8 is more generous (higher))
- |Delta| = 0.005 vs threshold 0.2
- p-value (Welch's t-test): 0.9158
- Rate of '7 out of 7' ratings: M1 = 19.0%, M11 = 17.9% (delta -1.1 pp)
- **H2 NOT SUPPORTED**.
- Opus 4.8 mean rating 3.574 vs Opus 4.7 mean 3.569 (delta=+0.005). Opus 4.8 is more generous (higher). P-value (Welch t-test): 0.9158.

## M1 stability check (Phase 2H vs Phase 2J)

- M1 mean: Phase 2H=3.535 (n=5607) vs Phase 2J=3.569 (n=3987). Drift=+0.035. STABLE - threshold 0.15.

## All 11 model PCA coordinates

| Model | Lab | PC1 | PC2 |
|---|---|---|---|
| M1 Claude Opus 4.7 | Anthropic, US | -4.852 | 2.778 |
| M2 GPT-5.5 | OpenAI, US | -5.239 | 4.182 |
| M3 Gemini 3.1 Pro | Google, US | -1.618 | 2.800 |
| M4 DeepSeek v4 Pro | DeepSeek, CN | -5.379 | 0.976 |
| M5 Kimi k2.6 | Moonshot, CN | -3.471 | 3.250 |
| M6 Mistral Large 2512 | Mistral, FR | 4.329 | -6.146 |
| M7 Cohere Command A | Cohere, CA | 25.318 | 5.354 |
| M8 Qwen 3.7 Max | Alibaba, CN | -5.432 | 5.015 |
| M9 Llama 4 Maverick | Meta, US | 0.650 | -18.303 |
| M10 Grok 4.20 | xAI, US | 0.471 | -2.458 |
| M11 Claude Opus 4.8 (NEW) | Anthropic, US | -4.777 | 2.551 |

## Variance explained

- PC1: 34.8%
- PC2: 20.9%
- PC3: 17.4%
- PC4: 8.4%
- PC1+PC2 cumulative: 55.7%

## Quick verdicts (Plain Russian)

- **H1:** Opus 4.8 живёт рядом с Opus 4.7 в кластере «ядра».
- **H2:** Калибровка не изменилась заметно. Заявление Anthropic про 'more honesty' либо не повторяется в нашем измерении, либо проявляется в более тонком измерении.
