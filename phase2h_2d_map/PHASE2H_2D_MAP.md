# Phase 2H: 2D map of 10 frontier LLMs in evaluative space

Source: 12 cells from results_phase2h, 335 unique constructs.

## PCA decomposition

| Component | Variance explained |
|---|---|
| PC1 | 0.433 (43.3%) |
| PC2 | 0.169 (16.9%) |
| PC3 | 0.148 (14.8%) |
| PC4 | 0.098 (9.8%) |
| PC5 | 0.067 (6.7%) |
| **PC1+PC2** | **0.602 (60.2%)** |

## Model coordinates

| Model | Lab | Country | PC1 | PC2 |
|---|---|---|---|---|
| Claude Opus 4.7 (Anthropic) | Anthropic | US | -4.315 | -2.507 |
| GPT-5.5 (OpenAI) | OpenAI | US | -4.482 | -3.220 |
| Gemini 3.1 Pro (Google) | Google | US | -5.081 | -4.264 |
| DeepSeek v4 Pro | DeepSeek | CN | -5.072 | -5.679 |
| Kimi k2.6 (Moonshot) | Moonshot | CN | -2.374 | -2.335 |
| Mistral Large 2512 | Mistral | FR | -2.032 | +10.992 |
| Command A (Cohere) | Cohere | CA | +26.096 | -3.214 |
| Qwen 3.7 Max (Alibaba) | Alibaba | CN | -4.615 | -3.384 |
| Llama 4 Maverick (Meta) | Meta | US | +0.020 | +8.667 |
| Grok 4.20 (xAI) | xAI | US | +1.854 | +4.945 |

## How to interpret

- Models with similar (PC1, PC2) coordinates produce similar evaluative judgments
- Distance in PC1-PC2 space measures evaluative divergence
- Country clustering (if present) suggests lab tradition effects
- Outlier models on PC1 or PC2 represent distinct evaluative styles

## Notes

- 218 to 335 constructs rated per model (median 335)
- M5 Kimi has lower coverage; this analysis used column-mean imputation for missing entries
- For paper figure, consider larger n by including Phase 1 constructs as well
