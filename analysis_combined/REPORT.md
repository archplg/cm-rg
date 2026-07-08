# Combined Analysis - финальный отчёт по всем фазам CM-RG

**Объём данных:** 98 cells, 1861 конструктов, 5 фаз, до 11 моделей.

## Состав данных

| Фаза | Cells | Models | Constructs | Tasks |
|---|---|---|---|---|
| pilot | 42 | 5 | 549 | (см metrics.json) |
| extended | 20 | 5 | 246 | (см metrics.json) |
| phase2h | 12 | 10 | 335 | (см metrics.json) |
| phase2h_extended | 10 | 10 | 288 | (см metrics.json) |
| phase2j | 14 | 11 | 443 | (см metrics.json) |

## Combined PCA (все ячейки, все 11 моделей)

PC1+PC2 cumulative explained variance: **57.3%**

| Model | Lab | PC1 mean | PC1 95% CI | PC2 mean | PC2 95% CI |
|---|---|---|---|---|---|
| M1 Claude Opus 4.7 | Anthropic | -0.125 | [-0.139, -0.104] | -0.068 | [-0.098, -0.012] |
| M2 GPT-5.5 | OpenAI | -0.130 | [-0.156, -0.103] | -0.098 | [-0.136, -0.015] |
| M3 Gemini 3.1 Pro | Google | -0.090 | [-0.130, -0.052] | -0.101 | [-0.160, -0.020] |
| M4 DeepSeek v4 Pro | DeepSeek | -0.130 | [-0.163, -0.093] | -0.089 | [-0.170, +0.001] |
| M5 Kimi k2.6 | Moonshot | -0.080 | [-0.112, -0.049] | -0.078 | [-0.117, -0.027] |
| M6 Mistral Large 2512 | Mistral | -0.006 | [-0.135, +0.174] | +0.237 | [-0.161, +0.434] |
| M7 Cohere Command A | Cohere | +0.729 | [+0.581, +0.786] | -0.078 | [-0.131, +0.020] |
| M8 Qwen 3.7 Max | Alibaba | -0.136 | [-0.161, -0.108] | -0.120 | [-0.163, -0.035] |
| M9 Llama 4 Maverick | Meta | -0.006 | [-0.069, +0.065] | +0.323 | [-0.135, +0.500] |
| M10 Grok 4.20 | xAI | +0.018 | [-0.021, +0.068] | +0.103 | [-0.006, +0.221] |
| M11 Claude Opus 4.8 | Anthropic | -0.045 | [-0.076, -0.017] | -0.031 | [-0.055, -0.006] |

## Procrustes-сравнение между фазами

Procrustes disparity 0 = идентичные карты, → 1 = полностью разные. Низкие значения = структура устойчива.

| Phase A | Phase B | Disparity |
|---|---|---|
| pilot | extended | 0.5956 |
| pilot | phase2h | 0.7321 |
| pilot | phase2h_extended | 0.4967 |
| pilot | phase2j | 0.3230 |
| extended | phase2h | 0.5435 |
| extended | phase2h_extended | 0.4197 |
| extended | phase2j | 0.3308 |
| phase2h | phase2h_extended | 0.0396 |
| phase2h | phase2j | 0.1541 |
| phase2h_extended | phase2j | 0.1275 |

## Cohere outlier - устойчивость через фазы

| Phase | M7 PC1 | Others mean PC1 | Offset |
|---|---|---|---|
| phase2h | +26.096 | -2.900 | **+28.996** |
| phase2h_extended | -22.817 | +2.535 | **-25.353** |
| phase2j | +25.318 | -2.532 | **+27.850** |
| **combined** | - | - | **+47.611** |

**Вердикт:** Cohere PC1 offset > 5 единиц на 2/3 phases and +47.61 in combined analysis.

## Calibration drift summary - средние оценки по моделям

| Model | Overall mean | Overall %7 | n |
|---|---|---|---|
| M1 Claude Opus 4.7 | 3.542 | 19.5% | 13,569 |
| M2 GPT-5.5 | 3.565 | 21.3% | 13,569 |
| M3 Gemini 3.1 Pro | 3.601 | 25.3% | 10,431 |
| M4 DeepSeek v4 Pro | 3.555 | 23.1% | 11,947 |
| M5 Kimi k2.6 | 3.654 | 23.7% | 9,646 |
| M6 Mistral Large 2512 | 3.549 | 18.7% | 9,592 |
| M7 Cohere Command A | 4.072 | 41.5% | 9,359 |
| M8 Qwen 3.7 Max | 3.581 | 24.1% | 9,594 |
| M9 Llama 4 Maverick | 3.649 | 22.4% | 9,594 |
| M10 Grok 4.20 | 3.627 | 15.5% | 9,594 |
| M11 Claude Opus 4.8 | 3.574 | 17.9% | 3,987 |

## Ключевые числа для arxiv preprint

- **Total cells analysed:** 98
- **Total constructs:** 1861
- **Total ratings collected:** 110,882
- **Models compared:** 11 (включая обе версии Opus 4.7 и 4.8)
- **Tasks across domains:** 7 (HR, governance, ethics, engineering, product launch, medical triage, AI policy)
- **Cohere PC1 offset (combined):** +47.61 units
- **Max Procrustes disparity between phases:** 0.7321
- **Min Procrustes disparity between phases:** 0.0396
