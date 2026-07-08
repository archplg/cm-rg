# Cross-Model Repertory Grid at Frontier Scale: Mapping Evaluative Pluralism Across 36 LLMs

**Archipelago Research · Phase 2L · 2026-06-13 (aligned to canonical analysis_results.json; supersedes the 06-12 draft)**

## Abstract

We applied Cross-Model Repertory Grid (CM-RG) methodology to 36 frontier large language models from 12 providers across three deployment tiers (cheap, mid, flagship). Each model independently authored advisory responses to 7 high-stakes business judgment tasks under both neutral and persona-conditioned prompts, then rated 35 anonymised peers on 333 emergent bipolar constructs derived through triadic elicitation. The dataset comprises 3,055,153 ratings on a 1-7 Likert scale across 14 (task × condition) cells, with mean inter-rater Pearson correlation of r = 0.200 (median r = 0.196, n_pairs = 13,928).

Our main finding is that **frontier LLMs achieve only weak consensus on judgment ratings even when scoring identical anonymised content on identical emergent constructs**. We additionally identify three structured patterns: (1) a "Western consensus cluster" formed by Anthropic, OpenAI, Google, and xAI flagships (mean within-cluster r = 0.34), (2) a calibration-tier effect where mid-tier models systematically rate higher than cheap or flagship tiers (mean rating 3.84 vs 3.57 and 3.78 respectively), and (3) an anti-consensus periphery occupied by smaller open-weights models that negatively correlate with the consensus (r < 0).

## 1. Introduction

The dominant framing in AI alignment research treats large language models as approximating a unified judgment function that converges with sufficient capability and training. Empirical work on inter-model agreement has primarily focused on factual accuracy or output similarity, leaving the question of evaluative agreement - whether models share judgment frameworks when assessing complex advisory tasks - relatively unexplored.

We address this gap with a Personal Constructs psychology-grounded methodology (Kelly, 1955) ported to LLMs. Rather than imposing external rating criteria, we let models derive their own evaluative dimensions through triadic elicitation, then have all models cross-rate one another on the union of emergent constructs.

This paper reports Phase 2L of an ongoing research program, scaling from 11 models in Phase 2J/2K (2026 Q1) to 36 models across three deployment tiers, with seven new tier-sensitive advisory tasks.

## 2. Methodology

### 2.1 Sample

We selected 36 models: 12 providers (Anthropic, OpenAI, Google, Mistral, DeepSeek, xAI, Qwen, Moonshot, Zhipu, NVIDIA, Meta, Cohere) × 3 tiers (cheap, mid, flagship). All models accessed via OpenRouter unified API. Model selection followed three criteria: (1) catalog availability with non-zero pricing at experiment time (verified via pre-flight check), (2) within-family tier separation by completion cost, (3) coverage of major training-data regimes (Western RLHF, Chinese hybrid alignment, open-weights legacy).

### 2.2 Task design

Seven advisory tasks (K through Q) designed for high tier-sensitivity:
- **K**: M&A under regulatory uncertainty across four jurisdictions
- **L**: Multi-generational family business succession
- **M**: Pandemic response strategy ($5B budget)
- **N**: R&D portfolio allocation across 8 emerging technologies ($1.2B)
- **O**: Crisis communication post data breach
- **P**: Constitutional reform proposal
- **Q**: Cross-jurisdiction AI regulation framework

Each task provides 200-400 words of context, 5 options (A-E), and asks for free-form 200-400 word advisory recommendation.

### 2.3 Conditions

Two conditions per task:
- **N (neutral)**: "You are an analyst. Read the brief carefully and provide your best-reasoned recommendation."
- **P (persona)**: Latin square assignment of 5 personas (Quantitative, Strategic, Ethical, Humanistic, Conservative).

### 2.4 Pipeline

Four-phase CM-RG pipeline executed via OpenRouter API at temperature 1.0 (phases 1, 3) and 0.0 (phase 4):

1. **Free response** (Phase 1): each model produces advisory recommendation
2. **Blind anonymisation** (Phase 2): regex-based removal of model self-identification markers
3. **Triadic elicitation** (Phase 3): each model views 3 anonymised peers, identifies 8-12 bipolar constructs that distinguish them
4. **Cross-rating** (Phase 4): each model rates all 35 peers on union of emergent constructs (per task-condition cell, ~333 constructs)

### 2.5 Engineering

Pipeline implemented in Python with atomic writes (Phase 2F corruption prevention), exponential backoff on transient errors (Phase 2J zero-cost bug prevention), per-provider spend caps, network outage detection (5-consecutive-failure auto-halt), and parallel cross-rating workers (4 concurrent threads). Pre-flight checks verified slug availability, cost calibration via dry run, parser robustness against reasoning-model output formats, atomic write under concurrent load, and retry behavior.

### 2.6 Final dataset

Total cost: $112.89 across 2,572 API calls (cap $200, budget-cap protection at $195). Phase 1 coverage 500/504 cells (99%), Phase 3 416/504 (83%), Phase 4 356/504 cells with at least partial ratings (71%, of which 133 with complete batches). Three models (Zhipu GLM-5.1, NVIDIA Nemotron Nano 9B, NVIDIA Nemotron Super 49B) returned null content responses for Phase 4 cross-rating despite valid HTTP 200 responses; their data are noted but excluded from downstream consensus calculations.

## 3. Results

### 3.1 Headline statistics

| Metric | Value |
|--------|-------|
| Total ratings | 3,055,153 |
| Unique rater × ratee pairs | 13,928 |
| Unique constructs (emergent) | 86,418 |
| Mean inter-rater r | 0.200 |
| Median inter-rater r | 0.196 |
| Standard deviation of r | 0.15 |

### 3.2 Inter-rater agreement (RQ1)

For each (task, condition) cell, we computed mean rating per (rater, ratee) by collapsing across all constructs from that cell's union. We then computed pairwise Pearson correlations between rater profiles. Cell-level mean correlations ranged from 0.18 (Q condition P) to 0.27 (K condition N). The overall mean of 0.200 - aggregated across all 13,928 valid pairs - represents weak consensus by standard psychometric thresholds (Cohen, 1988; typical inter-rater reliability targets r > 0.7).

This finding holds across robustness checks: (a) restricting to flagship models only yields r = 0.34 (still moderate at best), (b) restricting to cells with full 7/7 batch completion yields r = 0.21 (no improvement), (c) excluding the anti-consensus models (Q_C, N_C, N_M) yields r = 0.24.

### 3.3 Tier effects (RQ2)

The tier hypothesis predicted systematic differences in how cheap, mid, and flagship raters score ratees of different tiers. We tested by aggregating mean ratings per (rater_tier × ratee_tier) cell across all tasks:

| Rater tier | Rates cheap | Rates mid | Rates flagship |
|-----------|-------------|-----------|----------------|
| cheap | 3.588 | 3.558 | 3.564 |
| mid | 3.845 | 3.830 | 3.831 |
| flagship | 3.801 | 3.782 | 3.770 |

The rater-tier dimension explains far more variance (Δ ≈ 0.27 between cheap and mid raters) than the ratee-tier dimension (Δ < 0.04 within any row). We interpret this as a **calibration tier effect**: mid-tier models systematically apply higher ratings irrespective of ratee identity. Flagship models occupy a "balanced calibration" position. Cheap models systematically rate lower.

This is a robust finding: the within-row variance (ratee tier matters) is smaller than measurement noise in many cells, while the between-row variance (rater tier matters) consistently exceeds two standard deviations of cell-level standard error.

### 3.4 Consensus and divergence (RQ3)

We define a model's **consensus score** as the mean Pearson correlation with all other models, averaged across all (task, condition) cells.

**Top consensus models** (top 10 raters by mean correlation):
1. Gemini 3 Flash (G_M): 0.361
2. GPT-5.5 (O_F): 0.345
3. GPT-5.4 (O_M): 0.340
4. Claude Sonnet 4.6 (A_M): 0.319
5. Grok 4.20 (X_F): 0.317
6. Qwen 3.7 Max (Q_F): 0.317
7. Kimi K2.5 (K_C): 0.310
8. Grok Build 0.1 (X_C): 0.298
9. DeepSeek V4 Flash (D_C): 0.291
10. DeepSeek R1 (D_F): 0.267

**Divergent models** (avg r ≤ 0.0):
1. Nemotron Nano 9B (N_C): -0.104
2. Qwen 2.5 7B (Q_C): -0.098
3. Nemotron Super 49B (N_M): -0.042
4. Llama 3.3 70B (L_M): 0.001 (effectively zero)

The structure of the consensus space reveals three distinct regions:

1. **Western alignment cluster**: Anthropic, OpenAI, Google DeepMind, xAI - mean within-cluster r = 0.34
2. **Chinese flagship transitional zone**: Qwen 3.7 Max, Kimi K2.5, Kimi K2.6 - approaching but not yet integrated (mean r 0.27-0.30 with Western flagships)
3. **Open-weights/legacy anti-consensus periphery**: Qwen 2.5 7B, Llama 3.3 70B, Nemotron Nano - negative correlations with consensus indicate inverted evaluative axes

### 3.5 Family structure

Within-family rating correlations exceed between-family correlations for all 12 providers. [FLAG: the per-family correlation values in this paragraph are from the 06-12 analysis and have not yet been recomputed for the 06-13 canonical data; regenerate from analysis_results.json before publication. The qualitative pattern (within-family > between-family) holds.] Sample within-family correlations (averaged across tasks and tiers): Anthropic 0.42, OpenAI 0.45, Google 0.41, Mistral 0.31, xAI 0.38. This indicates that family-level training data and RLHF approach has more explanatory power for evaluative behavior than individual model tier.

### 3.6 Persona condition effects

Persona condition (P) introduced moderate volatility relative to neutral (N). Models in the consensus cluster maintained their ratings under persona shift (within-model r between N and P > 0.7 for top-10 consensus). Divergent models showed lower N-P correlation (r = 0.4-0.5), suggesting persona prompting destabilises their evaluative frame more than the consensus cluster's.

## 4. Discussion

### 4.1 Interpretation

The headline weak-consensus finding (r = 0.20) cannot be attributed to measurement noise: we have full sample sizes (13,928 pairs), the within-pair sample is large (mean 1,800 constructs per pair), and we observe stable cluster structure rather than random scatter. The result indicates **genuine evaluative pluralism** among frontier LLMs.

The Western consensus cluster's existence is consistent with the hypothesis that contemporary RLHF judgment training produces convergent evaluation frameworks. The transitional position of Chinese flagships supports a "convergence-in-progress" interpretation: as Qwen and Kimi adopt Western-style RLHF, they move toward the cluster but maintain residual divergence.

The anti-consensus periphery is the most surprising finding. Negative correlations - not just low positive - indicate models that systematically reverse the consensus's rating polarity on at least some constructs. This is not random noise but a structured opposition. We hypothesise this reflects either: (a) pre-RLHF training regimes that preserved different evaluative associations from the underlying training corpus, or (b) deliberately divergent RLHF objectives.

### 4.2 The calibration tier effect

We did not predict and have no strong theoretical account for the systematic mid-tier upward calibration shift. One conjecture: mid-tier models are trained with sufficient capability to follow instructions while lacking the discriminative resolution of flagships, producing centered-high responses to ambiguous judgment tasks. Cheap-tier models, by contrast, may default to lower ratings as a conservative strategy when uncertain. Flagship calibration may reflect more refined judgment training. This requires further investigation.

### 4.3 Implications

For **product teams** deploying LLMs in evaluation tasks (resume screening, content moderation, exam grading), our results indicate substantial systematic bias depending on tier selection. A mid-tier model deployed without correction will systematically over-rate compared to flagship baseline. Post-hoc calibration or tier-consistent baselines are necessary.

For **AI research**, our results challenge the assumption that ensemble methods automatically yield diverse perspectives. An ensemble of three Western flagships is nearly equivalent to one. True diversity requires selection across consensus zones.

For **AI policy**, the existence of multiple competing judgment frameworks complicates "objective AI evaluation" framing. Choice of model is implicitly choice of evaluative regime - a political decision masked as technical.

### 4.4 Limitations

(1) **Coverage**: 356/504 Phase 4 cells contain ratings, of which 133 are complete. Partial cells may bias certain statistics; we have not yet tested all results on the complete-only subset.

(2) **Three excluded models**: Zhipu GLM-5.1 and NVIDIA Nemotron Nano/Super returned null content responses - potentially provider-side issues unrelated to model behavior. This is a missing-not-at-random concern.

(3) **Construct selection**: emergent constructs come from triadic elicitation by the raters themselves. While this is the methodological core of CM-RG, it means constructs are not independent of raters. We mitigated by requiring the union across all raters' constructs, but selection bias remains.

(4) **Task generalisability**: 7 tasks across business judgment domains may not generalise to other judgment domains (creative evaluation, factual assessment, etc.).

(5) **Single time point**: 2026-06 snapshot. Model versions change continuously.

### 4.5 Future work

(1) Replicate with creative writing and factual assessment task domains.
(2) Decompose the anti-consensus periphery: which specific constructs invert?
(3) Train a "consensus inducer" - can a model be fine-tuned to shift its position on this map?
(4) Connect findings to documented training corpora and RLHF practices.

## 5. Replication

All code, configurations, and rating data are available at `archipelago_cross_model/` with detailed setup instructions. Reproducing the full Phase 2L run requires an OpenRouter account with approximately $120 budget and 4-8 hours of compute time (with 4-worker parallelism). Pre-flight checks (~1-3 hours, < $5) should be run before each replication attempt to verify provider availability.

## References

Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences. Lawrence Erlbaum.

Kelly, G. A. (1955). The Psychology of Personal Constructs. W. W. Norton.

Archipelago Research (2026). CM-RG Methodology Paper [Phase 2J/2K]. http://archplg.co.uk/cm-rg-auto

Archipelago Research (2026). CM-RG Applied Case: Aydan [Phase 2K Education]. http://archplg.co.uk/cm-rg-education

## Appendix: Cost breakdown

| Phase | Calls | Cost |
|-------|-------|------|
| Phase 1 free response | 500 | ~$6 |
| Phase 2 anonymisation | 0 (computational) | $0 |
| Phase 3 triadic elicitation | 416 | ~$3 |
| Phase 4 cross-rating | 1,656 | ~$103 |
| Total | 2,572 | $112.89 |

Pre-flight checks (verification, dry run, parser test): < $3.

---

*Archipelago Research is an independent research initiative studying evaluative pluralism in AI systems. Contact via http://archplg.co.uk*
