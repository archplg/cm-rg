# PRE-REGISTRATION: Archipelago-for-Agents cross-model experiment

**Status:** locked before any data is collected. Once data collection starts, this document does not change. Any deviation must be documented in a separate `deviations.md` file with reason.

**Date locked:** [Sergey fills before running]
**Experimenter:** Sergey Dolgov (Archipelago) + Claude (analysis support)

---

## 1. Purpose

Test whether the Archipelago pipeline (free response → anonymization → triadic construct elicitation → rating matrix → PCA + clustering) produces structurally meaningful output when applied to **genuinely heterogeneous LLM agents** from different model families and training distributions.

This experiment addresses the main limitation of the pilot, which used a single base model (Claude Opus 4.7) role-played five ways. In the pilot, the agent diversity was prompt-induced; here, the agent diversity is also distribution-induced.

## 2. Three nested hypotheses (carried from pilot, formalized)

**H1 (foundation):** Cross-model agents generate **content-distinct** constructs that capture structurally different evaluation axes.

**H2 (utility):** The resulting construct map provides operator-readable low-dimensional structure that reveals disagreement axes invisible in raw recommendations.

**H3 (detection):** The method surfaces premature convergence quantitatively.

H1 is gating. If H1 fails, H2 and H3 are vacuous.

## 3. Pre-registered falsification criteria (locked)

Each hypothesis fails if:

**H1 fails if:** the number of distinct semantic clusters at hierarchical clustering with k chosen by gap statistic is < 4 (vs 6 in pilot). Or: max pairwise construct correlation |r| across the matrix exceeds 0.95 for more than 25% of all construct pairs (vs ~15% in pilot).

**H2 fails if:** PC1+PC2 variance explained is < 60% in any of the 3 tasks. Or: PC1 and PC2 cannot be assigned coherent semantic labels on inspection.

**H3 fails if:** mean pairwise agent rating disagreement is < 0.5 across ALL tasks (i.e. cross-model agents converge as severely as same-model agents did - meaning the method's diagnostic signal is not driven by genuine model diversity). Note: H3 also fails if mean disagreement is > 2.5, indicating the agents are too divergent for the method to extract structure.

**Predicted outcome for H3 specifically:** mean pairwise disagreement will rise from pilot range (0.14-0.31) to 0.6-1.5 range. This is the headline prediction of the experiment.

## 4. Experimental design

### 4.1 Models (5 agents)

| Role | Model family | Primary ID | Fallback ID |
|------|-------------|------------|-------------|
| M1   | Anthropic   | `anthropic/claude-opus-4.7` | `anthropic/claude-sonnet-4.6` |
| M2   | OpenAI      | `openai/gpt-5.5`            | `openai/gpt-5.4`             |
| M3   | Google      | `google/gemini-3.1-pro-preview` | `google/gemini-3-pro` |
| M4   | DeepSeek    | `deepseek/deepseek-v4-pro`  | `deepseek/deepseek-v4-flash` |
| M5   | Moonshot    | `moonshotai/kimi-k2.6`      | `moonshotai/kimi-k2.5`       |

These cover 4-5 distinct training distributions (Western frontier, Chinese frontier closed, Chinese open-weight via Moonshot if applicable). Sergey will verify exact OpenRouter slugs at run time and update.

### 4.2 Tasks (3 total)

- **Task A:** SaaS investment decision ($8M, 5 options) - same as pilot
- **Task B:** Engineering team decline diagnosis (5 candidates) - same as pilot
- **Task C:** Health-app data privacy policy (5 options) - new, cross-validation

Tasks A and B replicate pilot directly. Task C is new domain (ethics/product), unseen by the analyst, to control for any inadvertent task-specific tuning.

### 4.3 Conditions (factorial, 2 levels)

- **Cond N (neutral):** Each model gets a neutral system prompt: "You are an analyst. Read the brief carefully and provide your best-reasoned recommendation."
- **Cond P (persona):** Each model gets one of 5 personas (Q/S/E/H/C). Persona assignment is rotated across tasks via a Latin square design to partially identify model effects vs persona effects.

Latin square (model × task → persona):
|       | Task A | Task B | Task C |
|-------|--------|--------|--------|
| M1 (Anthropic) | Q | S | E |
| M2 (OpenAI)    | S | E | H |
| M3 (Google)    | E | H | C |
| M4 (DeepSeek)  | H | C | Q |
| M5 (Moonshot)  | C | Q | S |

### 4.4 Repetitions

- 3 tasks × 2 conditions × 1 repetition = 6 base cells (each cell = full pipeline run with all 5 models)
- + 1 task × 2 conditions × 2 additional repetitions = 4 additional cells (for variance estimation)
- **Repeat task choice (locked):** Task B (team decline) - because it had the strongest premature convergence in pilot, so variance estimation matters most there.
- **Total cells:** 10
- **Total model-trials:** 50

Each repetition uses independent randomization for: element label permutation, triad assignment to agents, and (in Cond P) temperature seeds. Same task brief.

### 4.5 Parameters

- Temperature: 1.0 (for diversity in free response and constructs); 0.0 for ratings (for stability)
- Max tokens: 800 (free response), 600 (constructs), 200 (ratings)
- Random seed: cell-specific, logged
- All raw API responses logged verbatim to disk in JSON before any processing

### 4.6 Pipeline (4 phases, per cell)

1. **Divergent free response.** Each of 5 models gets the task brief + condition-appropriate system prompt. Generates 200-400 word recommendation.
2. **Anonymization.** Responses randomly permuted, labeled E1-E5. Short summaries (3-4 sentences) generated programmatically from each response.
3. **Triadic construct elicitation.** Each model assigned 3 specific triads. For each, model identifies bipolar construct: "Two of these are similar in being X, distinct from the third which is Y". Total: 15 elicited constructs per cell.
4. **Rating.** Each model rates all 5 elements on all 15 constructs (1-7 Likert). Total: 75 ratings per model = 375 ratings per cell.

Trial assignments for triads are fixed per cell and logged.

## 5. Analyses (locked before data collection)

### 5.1 Primary analyses (pre-registered)

For each of the 10 cells, compute:
- Pairwise construct correlation matrix (15×15)
- Number of distinct semantic clusters (hierarchical clustering on 1-|r|, k chosen by gap statistic)
- PCA on (element × mean-construct-rating) matrix: variance explained by PC1, PC2, PC3
- Inter-agent rating disagreement: mean absolute difference across all (element, construct) pairs, for all 10 agent pairs
- Element coordinates in PC space

### 5.2 Cross-cell comparisons

- **Condition effect (N vs P):** does adding personas change construct diversity / PC structure / disagreement? Paired t-test on each metric across the 3 paired tasks.
- **Task effect:** is the pattern consistent across A, B, C?
- **Variance from repeats (Task B only):** how stable is each metric across 3 independent runs? Coefficient of variation for each metric.
- **Pilot vs cross-model comparison:** compare pilot metrics (single base model) vs cross-model metrics on Tasks A and B. This is the headline H3 test.

### 5.3 Exploratory analyses (clearly labeled as such)

- Per-model agreement patterns (which models converge with which?)
- Construct ownership (does each model elicit characteristic constructs?)
- Latin-square decomposition attempting to separate model from persona effects

Exploratory results will be flagged as "not pre-registered" in the writeup.

## 6. What this experiment cannot test

- Decision quality: still requires human-subject study.
- Generalization beyond these 5 models: future work.
- Lacuna detection: pilot found method limitation here; revised method is for future work.
- Reliability over time: all runs happen within one week, same prompts.

## 7. Stop conditions / aborts

- Hard stop if total API spend exceeds $80 (2x estimated, safety margin).
- Soft stop if any cell takes more than 30 minutes wall time (likely API issue).
- Per-call retry: 3 attempts with exponential backoff. After 3 failures, log and continue with that model's slot empty for the cell, with cell marked as incomplete.

## 8. Reporting plan

Regardless of results (including null/negative), full data and analyses will be released as a research note alongside the eventual paper.

If H1 fails: paper position changes - method does not produce content diversity in cross-model setting, and we report this as a negative finding worth publishing.

If H3 fails (disagreement still <0.5 across all tasks): major surprise; likely indicates contemporary frontier models share more than expected. We would investigate and report.

If experiment validates pilot: we proceed to paper revision and product thinking.

---

**END OF PRE-REGISTRATION. This document does not change after data collection starts.**
