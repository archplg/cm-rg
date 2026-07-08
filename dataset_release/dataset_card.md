# ACME-CrossLLM Dataset

**Archipelago Construct Mapping Experiment: Cross-Model LLM Diversity Data**

Version: v1.0
License: CC-BY 4.0
DOI: [to be assigned via Zenodo upload]

## Overview

This dataset captures how five frontier large language models from different
labs (Anthropic Claude, OpenAI GPT, Google Gemini, DeepSeek, Moonshot Kimi)
respond to decision tasks and elicit bipolar evaluation constructs, in the
Personal Construct Psychology (Kelly's Repertory Grid) tradition adapted for
LLM agents.

Each "cell" represents one complete run of the pipeline (free responses ->
anonymization -> triadic construct elicitation -> ratings) on one (task,
condition) pair. Models work under two conditions: Neutral (analyst persona)
and Persona (one of five epistemological frames: Quantitative, Systems,
Engineering, Humanist, Contrarian; assigned via Latin square across tasks).

## Statistics

- **Total cells**: 70
- **Total constructs elicited**: 812
- **Total ratings**: 14253
- **Total free responses**: 350
- **Total API calls (audit trail)**: 984
- **Total cost (USD)**: $21.34
- **Tasks**: A, B, C, D, E, F, G
- **Models**: M1, M2, M3, M4, M5
- **Personas**: C, E, H, Q, S, neutral
- **M5 (Moonshot Kimi) dropout rate**: 0.0%

Model IDs used (snapshot at collection time):
  - `anthropic/claude-opus-4.7`
  - `deepseek/deepseek-v4-pro`
  - `google/gemini-3.1-pro-preview`
  - `moonshotai/kimi-k2.5`
  - `moonshotai/kimi-k2.6`
  - `openai/gpt-5.5`

Finish reason distribution (top 5):
  - **stop**: 810 calls
  - **length**: 174 calls


## Files

| File | Description | Schema |
|---|---|---|
| `cells.parquet` | One row per cell, with metadata and summary metrics | cell_id, task, condition, run_idx, status, started_at, completed_at, random_seed, n_valid_responses, n_constructs, n_raters, mean_pairwise_disagreement, pca_pc1, pca_pc2, pca_pc3, pc1_plus_pc2, n_high_corr_pairs, cost_usd, tokens_in, tokens_out, n_errors |
| `constructs.parquet` | One row per elicited bipolar construct | construct_id, cell_id, task, condition, run_idx, model, persona, construct_order_in_model, left_pole, right_pole, triad, raw_output_excerpt, semantic_cluster |
| `ratings.parquet` | Long-format ratings (each rating is one row) | rating_id, cell_id, task, condition, run_idx, rater_model, rater_persona, construct_id, construct_origin_model, element_label, element_origin_model, rating (1-7) |
| `responses.parquet` | Free responses from each model on each cell | response_id, cell_id, task, condition, run_idx, model, model_id_used, used_fallback, persona, element_label, response_text, response_length_chars, tokens_prompt, tokens_completion, reasoning_tokens, latency_ms, cost_usd, finish_reason, timestamp_iso |
| `api_calls.parquet` | Full audit trail of every API call | call_id, cell_id, task, condition, run_idx, phase, model_short_name, model_id_used, used_fallback, persona_or_neutral, attempts, timestamp_iso, latency_ms, prompt_tokens, completion_tokens, reasoning_tokens, finish_reason, cost_usd, audit_file |

## Data collection methodology

See `PROTOCOL.md` for the pre-registered protocol (locked before data collection).

Each cell follows this pipeline:

1. **Free response (Phase 1)**: 5 models each receive the task brief plus a
   condition-appropriate system prompt; generate 200-400 word recommendation.
2. **Anonymization (Phase 2)**: responses are shuffled, labeled E1..E5; short
   summaries are computed programmatically (first 3 sentences).
3. **Triadic construct elicitation (Phase 3)**: each model is assigned 3
   triads. For each, identifies a bipolar construct that distinguishes two
   responses from the third.
4. **Ratings (Phase 4)**: each model rates all 5 responses on all collected
   constructs (1-7 Likert).

All API calls are logged to `logs/api_calls/<cell_id>/...json` with full
prompts, raw responses, usage, latency, finish reason.

## Limitations and biases

- **M5 dropout**: Moonshot Kimi (a thinking model) routinely hits output token
  limits due to extensive internal reasoning. Approximately 0.0% of
  M5 calls return empty content even after retries. This means many cells
  have 4 active models instead of 5. Models are not interchangeable for the
  same prompt - this is a known limitation when using thinking models in
  output-constrained settings.
- **English only**: all tasks and responses are in English.
- **Frontier-only**: models tested are 2026 frontier; smaller/older models
  may exhibit different patterns.
- **5-option tasks**: all tasks present exactly 5 options. PCA dimensionality
  is constrained by this.
- **Model versioning**: OpenRouter slugs can change over time. The exact
  model_id used at collection time is preserved in `responses.parquet`,
  `api_calls.parquet`, and `results/run_manifest.json`.
- **Task pool size**: 7 tasks across 3 domains is modest. Generalization
  beyond these tasks is unverified.

## Intended use

- Studying LLM behavioral diversity and convergence
- Benchmarking ensemble/mixture-of-agents methods
- Cross-model alignment research
- Evaluating Repertory Grid as an LLM evaluation method
- Comparing Western vs Chinese-trained frontier models

## NOT intended for

- Training models (this is behavioral evaluation data, not training data)
- Drawing strong claims without acknowledging the limitations above
- Diagnosing real-world cases mentioned in tasks (Task G medical triage
  is a hypothetical for evaluation, not a treatment protocol)

## Ethical considerations

- All data is generated by commercial LLM APIs; no human subjects.
- Task G (medical triage under scarcity) is sensitive content. Discussion of
  triage protocols was conducted as a structured decision exercise. Outputs
  should not be interpreted as endorsement of any specific protocol.
- Task E (AI safety governance) is politically sensitive; outputs reflect
  model behavior, not authoritative policy positions.
- Models may exhibit biases inherited from training data. The dataset
  preserves these for study, not for amplification.

## Citation

```
@dataset{{dolgov2026acme,
  title = {{ACME-CrossLLM: Cross-Model LLM Construct Elicitation Dataset}},
  author = {{Dolgov, Sergey}},
  note = {{Technical implementation by Claude assistant}},
  year = {{2026}},
  publisher = {{Zenodo}},
  version = {{{version}}},
  doi = {{[to be assigned]}},
  url = {{https://zenodo.org/...}}
}}
```

## Contact

Sergey Dolgov - https://archplg.co.uk
