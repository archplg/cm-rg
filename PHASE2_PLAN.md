# Phase 2 Experimental Plan

**Budget:** $100. **Estimated actual cost:** ~$50-65. **Wall time:** ~12-18 hours over 2-3 days. **Goal:** turn Phase 1 (10 cells, marginal findings) into a paper-quality dataset capable of supporting the three main findings from construct decomposition with stable statistics.

---

## 1. What Phase 1 told us (locking in before Phase 2)

Three findings have **already** reached preliminary statistical significance on n=82 constructs from 10 cells:

| Finding | Statistic | Status |
|---|---|---|
| F1: Task structure dominates construct diversity | 35.3% variance vs 14.2% persona vs 7.9% model | **Robust to N**, holds even with our small sample. Phase 2 will only strengthen. |
| F2: Persona effect is statistically significant | chi2(15) = 30.20, **p = 0.011** | **Already significant**; Phase 2 will tighten effect size and per-persona attribution. |
| F3: Cross-model constructs are novel vs human taxonomies | 100% of constructs at cos < 0.5 from Hofstede/Schwartz/Big5/NDM | **Saturated**; Phase 2 should retest on more tasks to ensure generalization. |
| F4: Models share internal representations (Platonic Hyp.) | Mean Procrustes disparity = 0.277; M3 outlier | **Suggestive but small N**; needs more cells. |
| F5: Headline H3 (cross-model > pilot) | Partially supported, A_N=0.843 in predicted range, but task-dependent | **Needs pilot replication** on same tasks, plus more task variety. |

Phase 2 is designed to **lock in F1-F4** with paper-quality stats and **resolve F5** by adding pilot replication and more tasks.

---

## 2. Three sub-experiments

### Phase 2A: Cross-model expansion to 7 tasks ($15-25, ~6 hours wall)

**Goal:** stabilize F1 (task dominance) and F4 (Platonic hypothesis) with more tasks; reach n=5 per (task, condition) for variance estimation.

**Design:** 7 tasks (A, B, C existing + D, E, F, G new) × 2 conditions (N, P) × 5 runs per cell.

**Cells needed:**

| Task | N runs needed | P runs needed | Already have | Net new |
|---|---|---|---|---|
| A | 5 | 5 | 1+1 = 2 | **8 new** |
| B | 5 | 5 | 3+3 = 6 | **4 new** |
| C | 5 | 5 | 1+1 = 2 | **8 new** |
| D (new) | 5 | 5 | 0 | **10 new** |
| E (new) | 5 | 5 | 0 | **10 new** |
| F (new) | 5 | 5 | 0 | **10 new** |
| G (new) | 5 | 5 | 0 | **10 new** |
| **Total** | | | | **60 new cells** |

At ~$0.30 per cell (with bumped max_tokens): **~$18-25**.

**Statistical power after:** 70 total cells. Each (task, condition) has n=5 → can estimate within-cell SD reliably. Cohen's d for N vs P paired across 7 tasks → power 0.8 at d=0.6 with n=7 pairs.

### Phase 2B: Pilot replication ($12-20, ~4 hours wall)

**Goal:** resolve F5 - directly compare cross-model to single-model on same tasks. Without this, all "cross-model is X% better than pilot" claims are confounded by task differences.

**Design:** single Claude Opus 4.7 in 5 roles × 7 tasks × 2 conditions × 3 runs = 42 cells.

Use a stripped-down config that calls Claude Opus 4.7 for all 5 model slots (treating each "model" call as Claude Opus 4.7 with the relevant persona). Same task pool as Phase 2A.

At ~$0.40 per cell (Opus is more expensive, $5/M in, $25/M out): **~$15-20**.

**Statistical power after:** direct paired comparison on 7 tasks × cross-model vs pilot. Wilcoxon signed-rank test on disagreement difference.

### Phase 2C: Element-count stress test ($10-15, ~3 hours wall)

**Goal:** resolve a recurring artifact - PC1+PC2 = 1.000 in our small-n cells is a small-sample artifact, not signal. Need cells with 10 elements instead of 5 to confirm PCA structure is real.

**Design:** Tasks D and G are well-suited (open structure, many sensible options). Create extended versions with 10 options. Run 2 conditions × 5 runs × 2 tasks = 20 cells.

At ~$0.50 per cell (more elements = more rating prompt, more output): **~$10-15**.

**Statistical analysis:** confirm PC1+PC2 < 0.95 at 10 elements (showing real dimensionality emerges). If still 1.000, PCA is still saturated and we need to use spectral methods instead.

### Optional Phase 2D: Temperature sensitivity ($5-8, ~2 hours wall)

**Goal:** confirm findings are robust to sampling. Re-run 5 cells at temperature=0.7 (lower) and 5 at 1.5 (higher), compare to baseline T=1.0.

**Design:** 5 tasks × 1 condition (N) × 2 temperatures × 2 runs = 20 cells.

**Use only if budget remains after 2A, 2B, 2C.**

---

## 3. Total budget reconciliation

| Phase | Cells | Cost estimate | Wall time |
|---|---|---|---|
| Already done (Phase 1) | 10 | ~$3 actual | 4 hours |
| 2A: cross-model expansion | 60 | $18-25 | 6 hours |
| 2B: pilot replication | 42 | $15-20 | 4 hours |
| 2C: element-count stress | 20 | $10-15 | 3 hours |
| 2D: temperature (optional) | 20 | $5-8 | 2 hours |
| **Subtotal mandatory (2A+2B+2C)** | 122 new | **$43-60** | 13 hours |
| **Plus optional 2D** | 142 new | **$48-68** | 15 hours |
| **Headroom for retries / surprises** | - | **~$30-50** | - |

**Conclusion:** $100 is comfortably enough. The bottleneck is wall time (12-15 hours), not money.

---

## 4. Statistical analyses planned (paper outline)

After Phase 2 collection, run:

**Primary analyses (pre-registered):**

1. **Variance decomposition (mixed-effects)** on full construct space embedding:
   - Model: `embedding ~ task + condition + persona + model + (1|cell)`
   - Hypothesis: task remains dominant (>30% variance); persona second (>10%); model marginal (<10%); condition negligible.
   - Test: nested model comparison via likelihood ratio. Expected p < 0.001 for task and persona effects.

2. **Cross-model vs pilot comparison** (Wilcoxon signed-rank, paired by task):
   - Compute mean disagreement per (task, condition) for cross-model and single-Claude.
   - Test: cross-model disagreement > pilot disagreement, paired across 7 tasks × 2 conditions = 14 pairs.
   - Expected: p < 0.01, effect size r > 0.6.

3. **Persona effect (paired t-test)** on disagreement, N vs P, across 7 tasks:
   - Compute mean(P-N) per task across 5 runs each.
   - Test: t-statistic with df=6. **Expected null result** based on Phase 1 (Task A goes -, Task B goes +). If null, conclude "persona effect is task-dependent in direction" - this is the **most counter-intuitive** finding for paper.

4. **Procrustes disparity confidence** (bootstrap):
   - Bootstrap 1000 resamples of cells, compute mean pairwise Procrustes disparity each time.
   - 95% CI on mean disparity.
   - Test: 95% CI upper bound < 0.4 → Platonic Hypothesis supported.

**Exploratory analyses:**

5. **Cross-cell stability of model fingerprints** (chi2 on subsamples).
6. **Construct novelty by task type** - do open tasks elicit MORE novel constructs than constrained tasks?
7. **Meta-construct emergence** - is Cluster 3 (quality-of-argumentation constructs) stable across tasks?
8. **M3 (Gemini) outlier deep-dive** - is its Procrustes outlier due to task-specific behavior or general?

---

## 5. Paper outline (target: ICLR workshop or FAccT)

**Title (working):** "Frontier LLMs Share Internal Representations: Diversity Comes from Tasks and Epistemic Framing, Not Architecture"

**Abstract structure (200 words):**
- 5 frontier LLMs from different labs, evaluated via Repertory Grid on 7 decision tasks
- Construct decomposition shows task >> persona >> model in driving epistemic diversity
- 100% of elicited constructs are novel relative to established human taxonomies (Hofstede, Schwartz, Big Five, NDM)
- Procrustes disparity supports Platonic Representation Hypothesis (mean 0.277, 4/5 models cluster)
- Practical implication: model diversity is not a substitute for epistemic framing

**Sections:**
1. Introduction - the cross-model diversity question
2. Related work - Platonic Hypothesis, LLM ensembling, Repertory Grid
3. Method - Archipelago pipeline, 7 tasks, 5 models, 5 personas
4. Results
   - 4.1 Variance decomposition (F1)
   - 4.2 Persona effect (F2)
   - 4.3 Construct novelty (F3)
   - 4.4 Platonic alignment (F4)
   - 4.5 Cross-model vs pilot (F5)
5. Discussion - what this means for practice (model selection, ensembling, eval)
6. Limitations - 7 tasks, 5 models, English-only, frontier-only
7. Future work - human baseline, more model families, more domains

**Submission targets (in priority):**
- FAccT 2026 (deadline ~Feb): fits methodological + ethics-of-LLMs angle
- ICLR 2026 workshop on AI evaluation (deadline ~Jan)
- AIES 2026 (deadline ~Mar)
- arXiv preprint immediately after Phase 2 collection

---

## 6. Implementation steps

### Step 1: Update config.yaml for 7 tasks

Add tasks D, E, F, G with persona_assignment Latin squares. Set repetitions to give 5 runs per (task, cond).

### Step 2: Run Phase 2A
```
python run_experiment.py --resume    # picks up where Phase 1 left off
```
Will auto-detect already-complete cells and add new ones.

### Step 3: Build pilot_replication.py
Mirror of run_experiment.py but with all 5 model slots = Claude Opus 4.7 (different system prompts per persona).

### Step 4: Run pilot replication (Phase 2B)

### Step 5: Build extended task versions D-10, G-10 (10 options each). Run Phase 2C.

### Step 6: Full re-analysis with all data
```
python analyze.py
python operator_synthesis.py
python construct_decomposition.py
python pilot_vs_crossmodel_comparison.py    # NEW
python statistical_tests.py                 # NEW
```

### Step 7: Write paper draft (separate task)

---

## 7. Risk register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| M3 (Gemini) continues to fail on new tasks | Medium | Medium | M3 has fallback to gemini-2.5-pro; data still usable with M3 excluded if persistent |
| Pilot replication shows Claude Opus 4.7 also produces 0.8+ disagreement on Task A (refutes cross-model premise) | Low-medium | High | **Honest reporting**; could reframe paper as "Task A is just hard for everyone" with smaller scope |
| One of new tasks D-G systematically yields parsing failures | Low | Medium | Pre-test each new task on dry run before full batch |
| Sentence-transformer "all-MiniLM-L6-v2" gives weaker novelty signal than expected | Low | Low | Re-run with larger model (e.g., "all-mpnet-base-v2") |
| API costs spike (model price changes) | Low | Medium | Hard cap remains $80; can pause and reassess |

---

## 8. What I need from you to proceed

To start Phase 2A immediately, I need:

1. **Confirmation** that the Phase 1 budget is closed (or how much remains)
2. **Final approval** of Task D, E, F, G briefs (they're in `tasks/task_D_brief.md` through `task_G_brief.md` - review and reject any that don't fit the question you actually want to answer)
3. **Approval to expand `config.yaml`** to 7 tasks with the persona Latin squares I'll provide
4. **Time budget confirmation** - 12-18 hours of wall time over 2-3 days is needed for collection. Background prog is fine; no manual interaction needed once started.

After your approval, I'll:
- Update `config.yaml` to Phase 2 design
- Verify all 7 task briefs render correctly via dry-run
- Start Phase 2A
- Notify you when ready for 2B and 2C
- Final paper-quality analysis pass

---

**Confidence in this plan:** 8/10. Snapped down from 9 because (a) pilot replication assumes Opus 4.7 still gives comparable behavior to the original pilot which was done some time ago (might have model drift); (b) the cost estimates are based on Phase 1's averages, which may not generalize to new task types (D, E, F, G); (c) Task G specifically (medical triage) may hit content filters in some models and require alternate framing.
