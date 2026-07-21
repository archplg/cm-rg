# Cross-Model Repertory Grid (CM-RG)

A methodology and dataset for measuring evaluative diversity across frontier language models using Kelly's Personal Construct Psychology.

[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code-MIT-green.svg)](LICENSE-CODE)
[![Dataset](https://img.shields.io/badge/HuggingFace-Dataset-yellow.svg)](huggingface.co/datasets/sergeydolgov/cross-model-repertory-grid)
[![DOI](https://img.shields.io/badge/DOI-pending-lightgrey.svg)](https://doi.org/10.5281/zenodo.20717308)
[![arXiv](https://img.shields.io/badge/arXiv-pending-red.svg)](#)

## What this is

CM-RG transposes the Repertory Grid technique (Kelly, 1955) from human psychology onto frontier language models. Each model produces a free response to a decision task, then participates in triadic construct elicitation against anonymised peer responses. The result is a structured grid that reveals how each model carves the evaluative space differently from its peers.

This repository contains the full pipeline, the elicited dataset (codename "Archipelago"), and the analyses behind the accompanying paper.

---

Interactive dashboard + Papers: http://crossmodelrg.org

<img src=http://crossmodelrg.org/36.jpg>


## Phase 2L (June 2026) - frontier scale

**Largest empirical M×M cross-model rating study to date.**

| Metric | Value |
|--------|-------|
| Total ratings | **3,055,153** |
| Emergent constructs (union) | **86,418** |
| Rater × ratee pairs | **13,928** |
| Mean inter-rater Pearson r | **0.200** |
| Models × providers × tiers | **36 × 12 × 3** |
| Total compute budget | **$112.89** |

Three headline findings:

1. **Frontier LLMs achieve only weak consensus** on identical judgment ratings (r = 0.200), even when scoring identical anonymised content on identical emergent constructs. The myth of the "objective AI judge" is empirically falsified.
2. **Western consensus cluster** - Anthropic, OpenAI, Google, xAI flagships form a coherent cluster (mean within-cluster r = 0.34, 3× above average), reflecting shared RLHF judgment training.
3. **Calibration tier effect** - mid-tier models rate systematically higher (mean 3.84) than cheap (3.57) or flagship (3.78) tiers, irrespective of ratee identity.

Reports: [`REPORT_SCIENTIFIC.md`](REPORT_SCIENTIFIC.md) (academic) · [`REPORT_BLOG.md`](REPORT_BLOG.md) (plain-language).

Interactive: run `python generate_archipelago_map.py && python serve_map.py` to open the archipelago map.

---

## Phase 2J/2K legacy (May 2026) - 11-model foundation

- **11 frontier LLMs** from 10 independent labs: Anthropic (Claude Opus 4.7 + 4.8), OpenAI (GPT-5.5), Google (Gemini 3.1 Pro), DeepSeek (v4 Pro), Moonshot (Kimi k2.6), Mistral (Large 2512), Cohere (Command A), Alibaba (Qwen 3.7 Max), Meta (Llama 4 Maverick), xAI (Grok 4.20)
- **5 experimental phases**, 98 cells, 1,861 constructs
- **110,882 cross-ratings** at 11-model scale
- 7 advisory tasks across HR, governance, ethics, engineering, product launch, medical triage, AI policy

## Key findings

1. **Persona effect dominates lab effect at scale, with 5× lab-specific persona volatility.** Phase 2K paired design (n=18,140) shows median Lab/Persona = 0.07×, reversing Phase 1's small-cohort 2.3× finding. Decomposition reveals persona-stable cluster (Claude, GPT, Gemini, Kimi: SD<0.6 on persona-induced shifts) vs persona-volatile cluster (Cohere SD=3.20 highest, Llama/Mistral/DeepSeek/Grok SD>1.4).
2. **Cohere Command A is a structural outlier** - calibration shift of +0.48 points on 7-point scale (mixed-effects β = +0.483, p = 1.6×10⁻³⁵, n = 110,882), replicated across 3 independent phases and triangulated by a parallel single-coder study (CM-RG-Education).
3. **Platonic Representation Hypothesis empirically refuted at evaluation layer** - Procrustes disparity between independent phases ranges 0.04-0.73; pairwise model offsets up to 25 PCA units.
4. **Null result: Claude Opus 4.7 → 4.8 cross-version refresh shows no significant calibration shift** (β = +0.025, p = 0.54, n = 17,556), despite Anthropic's "more honesty" marketing claim. Within-lab versioning is not a source of evaluative diversity.

## Contamination resistance

Unlike answer-based benchmarks (e.g., SWE-Bench Pro, exploited by Claude Opus via `git log` in 18-25% of cells per Datacurve, 2026), CM-RG has **no gold answer** that a model could memorize. Three structural protections:

- *Emergent constructs* generated at runtime, never present in training corpora
- *Anonymization* of all responses before any rating phase
- *Relative scaling* (rating: how this response compares to others on this construct) rather than absolute correctness

## Quick start

### Install

```bash
git clone https://github.com/archplg/cm-rg.git
cd cm-rg
pip install -r requirements.txt
```

### Run the experiment

```bash
# Set your OpenRouter API key
export OPENROUTER_API_KEY="sk-or-v1-..."

# Run the full 7-task, 11-model experiment - Phase 2J (~$15, ~12h wall time)
python run_experiment.py

# Run pilot (5 frontier models, baseline)
cp config_phase2b_pilot.yaml config.yaml
python run_experiment.py

# Run with 11 models including Opus 4.8 (Phase 2J, ~$15)
cp config_phase2j.yaml config.yaml
python run_experiment.py
```

### Load the published dataset

```python
from datasets import load_dataset

ds = load_dataset("sergeydolgov/cross-model-repertory-grid")
ds["cells"]        # 98 cells across 5 experimental phases
ds["constructs"]   # 1,861 elicited bipolar constructs
ds["ratings"]      # 110,882 element-construct ratings
ds["responses"]    # free responses (one per model per cell)
```

## Methodology in one paragraph

For each (task, condition, run) cell, up to 11 frontier models from 10 independent labs each produce a free-form recommendation. Responses are stripped of authorship and shuffled into anonymous labels E1 through E11 (depending on phase n_models) to prevent quality-attribution anchoring (see Sun et al., 2026). Each model then performs triadic construct elicitation: from a sampled triple of responses, the model articulates a bipolar construct (e.g., "risk-tolerant vs risk-averse") that distinguishes two responses from the third. Every model then rates every response on every construct on a 1-7 scale, yielding a per-cell rating tensor. Cross-cell aggregation produces PCA decompositions, hierarchical clusters, Procrustes alignments, and variance decompositions reported in the paper. Full methodology in METHODOLOGY.md.

## Repository structure

```
cross-model-repertory-grid/
  run_experiment.py              4-phase pipeline orchestrator
  config.yaml                    active experiment config
  config_phase2b_pilot.yaml      pilot config (single Claude in 5 roles)
  config_phase2c_extended.yaml   10-option brief variant
  config_phase2h.yaml            10-model lineup
  tasks/                         task briefs (A through J, plus _10 variants)
  bootstrap_analysis.py          1000-resample CIs for headline metrics
  construct_decomposition.py     PCA, clustering, Procrustes, novelty analyses
  construct_validation.py        LLM-as-rater inter-rater agreement
  mixed_effects_analysis.py      variance components and Wald tests
  m5_sensitivity.py              robustness check for missing-data model
  build_dataset.py               Parquet + dataset card + Croissant metadata
  multi_run_pca_analysis.py      runs-as-elements PCA at higher dimensionality
  data/                          final published Parquet tables (after build)
  results/                       raw cells (Phase 1: 7 tasks x 2 conditions x 5 runs)
  results_pilot/                 pilot replication cells
  results_extended/              10-option Phase 2C cells
  results_phase2h/               10-model Phase 2H cells
```

## Reproducing the paper

| Section | Script | Output |
|---|---|---|
| Headline disagreement | `bootstrap_analysis.py` | `bootstrap_analysis/BOOTSTRAP_FINDINGS.md` |
| Variance decomposition | `mixed_effects_analysis.py` | `mixed_effects/MIXED_EFFECTS_FINDINGS.md` |
| Missing data robustness | `m5_sensitivity.py` | `m5_sensitivity/M5_SENSITIVITY_FINDINGS.md` |
| Cluster semantic validity | `construct_validation.py` | `validation/CONSTRUCT_VALIDATION_FINDINGS.md` |
| Construct space | `construct_decomposition.py` | `construct_decomposition/` (7 sub-analyses) |
| PCA dimensionality | `multi_run_pca_analysis.py` | `multi_run_pca/` |

Estimated total reproduction cost: ~$250 OpenRouter API spend across all 5 phases.

## Citing this work

```bibtex
@dataset{dolgov2026archipelago,
  author       = {Dolgov, Sergey},
  title        = {Archipelago: A Cross-Model Repertory Grid Dataset of Frontier LLM Evaluative Diversity},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {pending},
  url          = {https://github.com/archplg/cm-rg}
}

@misc{dolgov2026crossmodelrg,
  author       = {Dolgov, Sergey},
  title        = {Cross-Model Repertory Grid: Eliciting Evaluative Diversity Across Frontier Language Models},
  year         = {2026},
  eprint       = {pending},
  archivePrefix= {arXiv}
}
```

## License

- Dataset: CC-BY 4.0 - free to use with attribution.
- Code: MIT - free to use, modify, redistribute.

## Acknowledgements

Methodology builds on George Kelly's Personal Construct Psychology (1955) and the Repertory Grid technique. Anonymisation design informed by Sun et al. (2026) on expectation cues in LLM judgment. Technical implementation in collaboration with Anthropic's Claude assistant.

## Contributing

Issues and pull requests welcome. For methodology questions or replication advice, open a GitHub Discussion.
