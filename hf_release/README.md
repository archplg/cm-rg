---
license: cc-by-4.0
language:
  - en
pretty_name: "Cross-Model Repertory Grid (CM-RG)"
size_categories:
  - 1M<n<10M
task_categories:
  - other
tags:
  - llm-evaluation
  - cross-model
  - repertory-grid
  - kelly-personal-constructs
  - evaluative-diversity
  - frontier-models
  - llm-as-judge
annotations_creators:
  - machine-generated
language_creators:
  - machine-generated
multilinguality:
  - monolingual
source_datasets:
  - original
configs:
  - config_name: phase2l_36models
    data_files:
      - split: ratings
        path: phase2l_36models/ratings.parquet
      - split: constructs
        path: phase2l_36models/constructs.parquet
      - split: responses
        path: phase2l_36models/responses.parquet
      - split: cells
        path: phase2l_36models/cells.parquet
      - split: api_calls
        path: phase2l_36models/api_calls.parquet
  - config_name: combined_11models
    data_files:
      - split: ratings
        path: combined_11models/ratings.parquet
      - split: constructs
        path: combined_11models/constructs.parquet
      - split: responses
        path: combined_11models/responses.parquet
      - split: cells
        path: combined_11models/cells.parquet
      - split: api_calls
        path: combined_11models/api_calls.parquet
---

# Cross-Model Repertory Grid (CM-RG)

When several large language models advise on a task that has no verifiable correct
answer (strategy, ethics, policy, crisis trade-offs), "which model is right" is the
wrong question. The useful question is how, and how much, the models differ in the
structure of their judgment. CM-RG measures exactly that. It adapts George Kelly's
Personal Construct Psychology (1955): each model writes a free-text advisory
response, elicits its own bipolar evaluation constructs by triadic comparison, and
then cross-rates anonymized peers on the union of emergent constructs. Because the
constructs are emergent and there is no answer key, the method is resistant to
contamination - there is nothing for a model to memorize.

This repository contains two configs from two runs of the program. They come from
different generations of the pipeline and therefore have slightly different schemas;
each is documented below.

| Config | Run | Models | Ratings | Cells | Constructs | Mean r | Notes |
|---|---|---|---|---|---|---|---|
| `phase2l_36models` | Phase 2L (2026-06) | 36 | 3,055,153 | 395 | 86,418 | 0.200 | primary |
| `combined_11models` | Phases pilot-2J (2026 Q1) | 11 | 110,882 | 98 | 1,861 | - | companion paper |

DOI: `10.5281/zenodo.20717308` - License: CC-BY-4.0

---

## Config `phase2l_36models` (primary)

The Phase 2L run: 36 frontier models from 12 provider families across three
deployment tiers (cheap, mid, flagship), on 7 advisory tasks under 2 prompting
conditions (neutral and persona). All figures are computed from
`results_phase2l/analysis_results.json`, dated **2026-06-13**, the canonical
analysis of record.

| Metric | Value |
|---|---|
| Models | 36 (12 families x 3 tiers) |
| Rating cells loaded | 395 |
| Total ratings | 3,055,153 |
| Distinct rater x ratee pairs | 13,928 |
| Emergent constructs | 86,418 |
| Free responses | 504 |
| Mean inter-rater correlation | 0.200 (median 0.196) |
| Run cost (ledger) | USD 112.89 across 2,572 API calls |

**Tables / splits.**

- **ratings** (3,055,153) - `rating_id, task, condition, rater, ratee,
  rater_family, rater_tier, ratee_family, ratee_tier, batch, construct_id, rating`.
  Join `construct_id` to `constructs`.
- **constructs** (86,418) - `construct_id, task, condition, rater, batch,
  construct_local_idx, pole_a, pole_b, context, from_rater`.
- **responses** (504) - `response_id, task, condition, model, model_slug, family,
  tier, persona, response, anonymized_text, cost_usd, latency_ms, timestamp`.
- **cells** (395) - per rater-cell summary: `cell_id, task, condition, rater,
  rater_slug, family, tier, n_batches, ok_batches, n_constructs_total,
  total_cost_usd, total_latency_ms, timestamp`.
- **api_calls** (1,462) - per-cell telemetry. `cost_usd` is the per-cell logged
  spend and is **cumulative over any re-parses / re-runs**, so summing it
  overcounts; the authoritative run cost is USD 112.89 / 2,572 calls (run ledger).

**Codes.** Models are `FAMILY_TIER`, e.g. `A_C` = Anthropic / cheap. Families: A
Anthropic, O OpenAI, G Google, X xAI, D DeepSeek, Q Qwen, K Moonshot/Kimi, M
Mistral, L Meta/Llama, N NVIDIA/Nemotron, C Cohere, Z Zhipu. Tiers: C cheap, M mid,
F flagship. Tasks: K (M&A under regulatory uncertainty), L (Family business
succession), M (Pandemic response strategy), N_task (R&D portfolio allocation), O
(Crisis communication post-breach), P (Constitutional reform proposal), Q
(Cross-jurisdiction AI regulation). Conditions: N (neutral), P (persona).

**Notes.** Phase 4 reached 395 of 504 design cells. Three models (Zhipu GLM-5.1,
NVIDIA Nemotron Nano 9B, Nemotron Super 49B) returned null content on valid HTTP 200
and are excluded from downstream consensus statistics (missing-not-at-random).
Because responses are anonymized, a model can rate its own (anonymized) response;
such pairs are retained, matching the analysis of record. Model versions and prices
are a June 2026 snapshot.

---

## Config `combined_11models` (companion)

The earlier 11-model run, pooled across five phases (pilot, extended, phase2h,
phase2h_extended, phase2j). This is the "Combined" dataset reported in the companion
11-model paper: 110,882 cross-ratings, 98 cells, 1,861 constructs, 7 tasks. The
paired-design Phase 2K analysis (n = 18,140 paired tuples) is reported separately in
that paper and is not included in this config.

**Tables / splits.**

- **ratings** (110,882) - `rating_id, phase, cell_id, task_id, condition_id,
  run_id, construct_id, element_id, rated_model_id, rater_model_id, rating`.
- **constructs** (1,861) - `phase, cell_id, task_id, condition_id, run_id,
  construct_id, owner_model_id, left_pole, right_pole, triad_elements`.
- **responses** (684) - `phase, cell_id, task_id, condition_id, run_id, model_id,
  response_text, response_length_chars`.
- **cells** (98) - `phase, cell_id, task_id, condition_id, run_id, status,
  started_at, completed_at, random_seed, n_models, n_constructs,
  cost_usd_script_reported`.
- **api_calls** (2,004) - per-call telemetry with tokens, latency, and recorded cost.

**Model codes (M1-M11).**

| Code | Family | Model |
|---|---|---|
| M1 | Anthropic | claude-opus-4.7 |
| M2 | OpenAI | gpt-5.5 |
| M3 | Google | gemini-3.1-pro-preview |
| M4 | DeepSeek | deepseek-v4-pro |
| M5 | Moonshot | kimi-k2.6 |
| M6 | Mistral | mistral-large-2512 |
| M7 | Cohere | command-a |
| M8 | Qwen | qwen3.7-max |
| M9 | Meta | llama-4-maverick |
| M10 | xAI | grok-4.20 |
| M11 | Anthropic | claude-opus-4.8 |

In this run, `rated_model_id` / `rater_model_id` use these M-codes; `element_id`
(E1-E11) is the anonymized element resolved to a model via the per-cell
`element_mapping`. M7 (Cohere Command A) is the structural outlier analyzed in the
paper; M1 and M11 are the Opus 4.7 / 4.8 version pair.

---

## Quick start

```python
from datasets import load_dataset

# 36-model Phase 2L
ds = load_dataset("sergeydolgov/cross-model-repertory-grid",
                  "phase2l_36models", split="ratings")

# 11-model combined
ds2 = load_dataset("sergeydolgov/cross-model-repertory-grid",
                   "combined_11models", split="ratings")
```

## Citation

```
Dolgov, S., & Tkacheva, D. (2026). Cross-Model Repertory Grid.
Archipelago Research. DOI: 10.5281/zenodo.20717308
```
