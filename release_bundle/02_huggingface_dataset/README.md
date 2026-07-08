---
license: cc-by-4.0
language:
  - en
pretty_name: "Archipelago: Cross-Model Repertory Grid Dataset"
size_categories:
  - 10K<n<100K
task_categories:
  - text-classification
  - other
tags:
  - llm-evaluation
  - cross-model
  - repertory-grid
  - kelly-personal-constructs
  - evaluative-diversity
  - frontier-models
  - llm-as-judge
  - construct-elicitation
configs:
  - config_name: default
    data_files:
      - split: cells
        path: data/cells.parquet
      - split: constructs
        path: data/constructs.parquet
      - split: ratings
        path: data/ratings.parquet
      - split: responses
        path: data/responses.parquet
      - split: api_calls
        path: data/api_calls.parquet
annotations_creators:
  - machine-generated
language_creators:
  - machine-generated
multilinguality:
  - monolingual
source_datasets:
  - original
paperswithcode_id: archipelago-cross-model-repertory-grid
---

# Archipelago: Cross-Model Repertory Grid Dataset

A dataset of evaluative constructs elicited from frontier language models using the Cross-Model Repertory Grid (CM-RG) methodology, a transposition of Kelly's (1955) Personal Construct Psychology onto LLM agents.

## Dataset summary

Archipelago captures how up to **11 frontier LLMs from 10 independent labs** (Anthropic Opus 4.7 + 4.8, OpenAI GPT-5.5, Google Gemini 3.1 Pro, DeepSeek v4 Pro, Moonshot Kimi k2.6, Mistral Large 2512, Cohere Command A, Alibaba Qwen 3.7 Max, Meta Llama 4 Maverick, xAI Grok 4.20) carve up the evaluative space when reasoning about the same decision tasks. For each task, each model first produces a free-form recommendation, then performs triadic construct elicitation against anonymised peer responses, then rates all responses on the elicited constructs. The resulting per-cell grids decompose into PCA dimensions, hierarchical clusters, and cross-model alignment measures.

**Scale (Wave 4, finalised May 2026):** 5 experimental phases, 98 cells, 1,861 unique constructs, **110,882 cross-ratings** - one of the largest M×M cross-rating LLM matrices in the published literature (closest comparable: JudgeLM-100K single-judge 100K, Judge's Verdict 2025 ~108K judge-vs-human; no published M×M LLM cross-rating dataset at our scale).

**Headline findings:**
1. **Persona effect dominates lab effect at scale, but persona robustness is highly lab-specific.** Phase 2K paired design (n=18,140) shows median Lab/Persona = 0.07×, reversing the Phase 1 small-cohort 2.3× finding. Decomposition reveals 5× spread in persona-volatility: persona-stable cluster (Claude, GPT, Gemini, Kimi: SD<0.6) vs persona-volatile cluster (Cohere SD=3.20 highest).
2. **Cohere Command A is a structural outlier** with +0.48-point calibration shift (mixed-effects β = +0.483, p = 1.6×10⁻³⁵), replicated 7/7 tasks and independently triangulated by a parallel single-coder study.
3. **Platonic Representation Hypothesis is empirically refuted** at the evaluation layer: Procrustes disparity between independent phases ranges from 0.04 (near-identical) to 0.73 (substantially divergent).
4. **Null result: Claude Opus 4.7 → 4.8 cross-version refresh shows no significant calibration shift** (β = +0.025, p = 0.54, n = 17,556) despite Anthropic's "more honesty" marketing claim.

## Languages

- English (`en`)

## Dataset structure

The dataset is provided as five Parquet tables, each one row per logical unit:

| Table | Rows | Description | Primary keys |
|---|---|---|---|
| `cells` | **98** | One row per (task, condition, run) experimental cell across all 5 phases | `phase`, `cell_id` |
| `responses` | ~900 | Free-form responses (one per model per cell) | `phase`, `cell_id`, `model_id` |
| `constructs` | **1,861** | Bipolar constructs elicited via triadic procedure | `phase`, `cell_id`, `model_id`, `construct_id` |
| `ratings` | **110,882** | Element-construct rating tuples on 1-7 scale | `phase`, `cell_id`, `rater_model_id`, `construct_id`, `element_id` |
| `api_calls` | ~3,500 | Audit log of every API call (cost, latency, finish_reason) including OpenRouter `usage.cost` | `call_id` |

### Schema for `cells`

| Column | Type | Description |
|---|---|---|
| `cell_id` | string | Unique cell identifier (e.g., `A_N_run1`) |
| `task_id` | string | Task identifier (A through J, plus _10 variants) |
| `condition_id` | string | `N` (neutral) or `P` (persona-conditioned) |
| `run_id` | int | Run number within the (task, condition) pair |
| `status` | string | `complete` or `complete_with_errors` |
| `n_models_participated` | int | Number of models with usable output (typically 10-11; lower in pilot/extended phases which used 5 models) |
| `phase` | string | Experiment phase (1=cross-model, 2B=pilot, 2C=10-option, 2H=10-model) |

### Schema for `constructs`

| Column | Type | Description |
|---|---|---|
| `construct_id` | string | Unique construct identifier |
| `cell_id` | string | Cell where construct was elicited |
| `model_id` | string | Model that elicited the construct |
| `left_pole` | string | Left pole of the bipolar construct (e.g., "risk-tolerant") |
| `right_pole` | string | Right pole (e.g., "risk-averse") |
| `persona_id` | string | Persona used when eliciting (Q/S/E/H/C or `NULL` for neutral) |
| `triad_elements` | list[string] | Three element IDs that the construct was elicited from |

### Schema for `ratings`

| Column | Type | Description |
|---|---|---|
| `rating_id` | string | Unique rating identifier |
| `cell_id` | string | Cell context |
| `construct_id` | string | Construct being applied |
| `element_id` | string | Element being rated (anonymous label E1 through E5) |
| `rater_model_id` | string | Model providing the rating |
| `rating` | int | 1 to 7 (1 = strongly left pole, 7 = strongly right pole) |

## Data collection

### Tasks

Seven primary decision tasks running across all phases (1, 2C, 2H, 2H-ext, 2J), spanning advisory contexts. Phase 2F (three additional tasks: legal, science funding, urban planning) was attempted but failed due to write corruption; not included in this release:

| ID | Domain | Element count |
|---|---|---|
| A | SaaS investment | 5 (and 10-option variant A10) |
| B | Engineering team decisions | 5 |
| C | Health-app privacy | 5 |
| D | Climate adaptation strategy | 5 (and 10-option variant D10) |
| E | AI governance | 5 |
| F | Product launch | 5 |
| G | Medical triage protocol | 5 (and 10-option variant G10) |
| H | Sentencing reform | 5 |
| I | Science funding allocation | 5 |
| J | Urban planning under climate stress | 5 |

### Models

Phase 2J final lineup: 11 frontier models from 10 independent labs (Phase 1 pilot used the first 5; phase2h+ added 5 more; phase2j added Claude Opus 4.8):

| ID | Model | Lab | Country | First seen in |
|---|---|---|---|---|
| M1 | Claude Opus 4.7 | Anthropic | US | pilot |
| M2 | GPT-5.5 | OpenAI | US | pilot |
| M3 | Gemini 3.1 Pro | Google DeepMind | US/UK | pilot |
| M4 | DeepSeek v4 Pro | DeepSeek | China | pilot |
| M5 | Kimi k2.6 | Moonshot AI | China | pilot |
| M6 | Mistral Large 2512 | Mistral | France | phase2h |
| M7 | Command A | Cohere | Canada | phase2h |
| M8 | Qwen 3.7 Max | Alibaba | China | phase2h |
| M9 | Llama 4 Maverick | Meta | US | phase2h |
| M10 | Grok 4.20 | xAI | US | phase2h |
| M11 | Claude Opus 4.8 | Anthropic | US | phase2j |

### Personas

Five epistemological framings (assigned via Latin square in persona condition):

| Code | Persona | Frame |
|---|---|---|
| Q | Quantitative | data-driven, ROI-focused |
| S | Stakeholder | multi-party, consensus-seeking |
| E | Ethics | principles-first, harm-aware |
| H | Historical | precedent-aware, pattern-matching |
| C | Contrarian | challenger, devil's advocate |

### Anonymisation

To prevent quality-attribution anchoring (Sun et al., 2026), free responses are stripped of authorship and shuffled into anonymous labels E1-E5 before any rater (the same or different model) evaluates them. Original authorship is preserved in the dataset for analysis but not surfaced to any rater during the pipeline.

## Considerations for using the data

### Strengths

- 11 frontier models from 10 genuinely independent labs (Anthropic appears twice for cross-version comparison; all other labs are unique)
- Anonymised peer evaluation prevents authority-bias confounds
- Construct-elicitation methodology yields explanatory dimensions rather than opaque preference scores
- Full audit trail: every API call logged with cost, latency, finish_reason, reasoning_tokens
- Sensitivity analyses provided for missing-data patterns (M5 partial dropout ~30%)

### Limitations

- LLM raters share training-data biases with LLM authors; human raters would be a stronger validation (planned for v1.0)
- Cohen's kappa for cluster validation moderate (0.510 with Claude-as-rater, X with GPT-as-rater)
- Free-form English only; no multilingual coverage in v0.1
- Task briefs are advisory-framed (may introduce implicit authority cues per Sun et al., 2026)

### Recommended uses

- Multi-model evaluation benchmark for diversity-sensitive applications
- Test of the Platonic Representation Hypothesis at the evaluation layer
- Source data for ensemble or mixture-of-agents designs
- Pedagogical material for LLM-as-judge methodology

### Not recommended for

- Reproducing exact model behaviour (model snapshots may drift)
- Inferring ground truth on decision tasks (no canonical correct answer)
- Single-cell predictions (cell-level data is noisy; aggregate across runs)

## Loading the dataset

```python
from datasets import load_dataset

ds = load_dataset("sergeydolgov/cross-model-repertory-grid")

# Inspect cells
print(ds["cells"].column_names)
print(ds["cells"][0])

# Filter to one task
task_a = ds["constructs"].filter(lambda x: x["cell_id"].startswith("A_"))

# Compute mean rating per construct per element
import pandas as pd
df = ds["ratings"].to_pandas()
mean_ratings = df.groupby(["construct_id", "element_id"])["rating"].mean()
```

## Reproducibility

Full pipeline code, configs, and analysis scripts are available at:

- GitHub: https://github.com/archplg/cm-rg
- Zenodo (versioned snapshots): pending DOI

Estimated reproduction cost: ~$120 in OpenRouter API spend across all phases.

## Citation

```bibtex
@dataset{dolgov2026archipelago,
  author       = {Dolgov, Sergey},
  title        = {Archipelago: A Cross-Model Repertory Grid Dataset of Frontier LLM Evaluative Diversity},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {pending},
  url          = {https://huggingface.co/datasets/sergeydolgov/cross-model-repertory-grid}
}
```

## Licensing

Released under [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to share and adapt the data with attribution.

## Contact

- Issues and discussions: https://github.com/archplg/cm-rg/issues
- Maintainer: Sergey Dolgov (with technical implementation by Anthropic's Claude)

## Acknowl