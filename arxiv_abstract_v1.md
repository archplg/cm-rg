# Cross-Model Repertory Grid: Lab-Specific Persona Volatility in Frontier LLM Ensembles

**Authors:** Sergey Dolgov¹, Archipelago Research Group

¹ *sergey@archplg.co.uk* · crossmodelrg.org · Code & data: https://github.com/archplg/cm-rg

---

## Abstract (draft v1, ~250 words)

We introduce **Cross-Model Repertory Grid (CM-RG)**, a contamination-resistant methodology for measuring evaluative diversity across frontier Large Language Models (LLMs). Adapting Kelly's (1955) Repertory Grid technique to LLM agents, we elicit emergent constructs through triadic interrogation and obtain cross-model ratings on anonymized outputs. Unlike answer-based benchmarks (SWE-Bench, MMLU), CM-RG has no "gold answer" a model could memorize or extract from the evaluation environment — a property of immediate relevance given the Datacurve (2026) finding that Claude Opus exploits `git log` to game SWE-Bench Pro in 18-25% of solved cells.

We present results from one of the largest M×M model-rates-model rating matrices in the published evaluation literature (closest comparables: JudgeLM-100K is single-judge; Judge's Verdict 2025 ~108K but judge-vs-human): **110,882 ratings across 98 cells, 1,861 constructs, 11 frontier LLMs (Claude Opus 4.7/4.8, GPT-5.5, Gemini 3.1 Pro, DeepSeek v4 Pro, Kimi k2.6, Mistral Large, Cohere Command A, Qwen 3.7 Max, Llama 4 Maverick, Grok 4.20)** over 7 advisory tasks across HR, governance, ethics, engineering, product launch, and medical triage domains.

**Four findings.** (1) **Persona effect dominates lab effect at scale, but persona robustness is highly lab-specific.** A small-cohort Phase 1 measurement (Lab/Persona = 2.3× on 5 models) reverses at scale: Phase 2K paired design on 11 models (n=18,140 paired tuples) yields median Lab/Persona = 0.07×. Decomposition reveals two distinct lab clusters: *persona-stable* (Claude Opus 4.7+4.8, GPT-5.5, Gemini 3.1 Pro, Kimi k2.6: SD < 0.6 on persona-induced rating shifts) and *persona-volatile* (Cohere Command A SD = 3.20, Llama 4 SD = 2.05, Mistral SD = 2.00, DeepSeek SD = 1.79, Grok SD = 1.47). (2) **A single model (Cohere Command A) is a structural outlier**, triangulated across three orthogonal measurements: PCA distance +26 units, mixed-effects calibration shift β=+0.483 (p=1.6×10⁻³⁵, n=110,882), and highest persona volatility in the dataset. Independently triangulated by a parallel single-coder study (CM-RG-Education). (3) **The Platonic Representation Hypothesis is empirically refuted** at the evaluation layer (Procrustes disparity 0.04-0.73 between phases; pairwise model offsets up to 25 PCA units).

We also report a negative result: **Claude Opus 4.7 → 4.8 cross-version refresh shows no significant calibration shift** (β = +0.025, p = 0.54, n = 17,556), despite Anthropic's "more honesty" claim. Methods, code, and CC-BY 4.0 dataset are released for reproducibility.

---

## Key numbers for box / one-pager

| Metric | Value |
|---|---|
| Total cross-ratings | **110,882** |
| Frontier LLMs evaluated | 11 |
| Tasks across domains | 7 |
| Lab/Persona ratio at scale (Phase 2K paired, n=18,140) | **0.07×** (persona dominates) |
| Cohere calibration shift | **+0.48 points** (p = 1.6e-35) |
| Cohere persona volatility | **SD = 3.20** (highest in dataset) |
| Claude Opus 4.7 persona volatility | **SD = 0.60** (most stable, 5× lower than Cohere) |
| Procrustes disparity between phases (best) | 0.04 (near-identical) |
| Opus 4.7 ↔ 4.8 calibration shift | **β = +0.025, p = 0.54** (null result, n = 17,556) |
| Total experiment cost | $250 (extrapolated from $15.32 Phase 2J alone) |

---

## Suggested keywords

cross-model evaluation, evaluative diversity, repertory grid, frontier LLMs, model ensembles, calibration drift, contamination-resistant benchmarks, multi-method validation

---

## Structure of the paper (envisioned)

1. **Introduction** - the limits of single-benchmark evaluation, contamination problems (DeepSWE story), motivation for measuring evaluative diversity directly
2. **Related work** - HELM (Bommasani et al., 2022), Sun et al. (2026) on rater bias, Platonic Representation Hypothesis (Huh et al., 2024)
3. **Method** - CM-RG pipeline: free response → triadic interrogation → cross-rating → PCA/Procrustes. Contamination-resistance discussion.
4. **Data** - 5 phases, 11 models, 7 tasks. Statistics in Section 4.
5. **Results**
   - 5.1 Persona dominates Lab at scale; persona robustness is lab-specific (5× spread)
   - 5.2 Cohere structural outlier (replicated 7/7, mixed-effects)
   - 5.3 Platonic Hypothesis refutation
   - 5.4 Cross-version stability (Opus 4.7 ↔ 4.8 null result)
   - 5.5 Triangulation with CM-RG-Education
6. **Discussion** - implications for multi-model AI procurement, regulatory audit, RLHF reward modelling
7. **Limitations** - English-only, advisory-only, single-coder for CM-RG-Education
8. **Conclusion**

---

## Sub-claims for confidence rating

| Claim | Confidence | Evidence |
|---|---|---|
| Persona dominates Lab at scale | 9/10 | Phase 2K paired design, n=18,140 paired tuples, 11 models. Median ratio 0.07× across 7 tasks. Phase 1's earlier 2.3× was a 5-model-cohort artifact. |
| Lab-specific persona volatility (5× spread Claude vs Cohere) | 9/10 | Phase 2K paired, SD computed per model. Stable cluster SD<0.6, volatile cluster SD>1.4, Cohere SD=3.20 outlier. |
| Cohere calibration shift | 9.5/10 | Mixed-effects β=+0.48 p=1.6e-35, n=110K + replication 7/7 + triangulation |
| Platonic refutation | 8/10 | Procrustes 0.04-0.73, single-method (PCA), single-construct-elicitation method |
| Opus 4.7 ↔ 4.8 no shift | 8.5/10 | n=17,556, p=0.54, but only 1 cross-version pair |
| 110K ratings | 10/10 | Counted in code, verified by hand |
| "One of the largest M×M LLM-judge cross-rating matrices" | 9/10 | Compared with Chatbot Arena (human, not LLM), JudgeLM-100K (single judge), Judge's Verdict 2025 (judge-vs-human eval, not M×M), JudgeBench (~1.2K), MT-Bench (~30K). No published M×M LLM cross-rating dataset at our scale. |

---

## Editorial notes for v2 of this draft

- TODO: get one independent reviewer (Stanford / HF / Anthropic referee) to read for sanity
- TODO: re-frame "Cohere structural outlier" carefully — finding is about evaluative diversity, not about Cohere being "wrong" or "worse"
- TODO: anchor DeepSWE citation properly (Datacurve, 2026, May 26)
- TODO: address potential criticism that CM-RG conflates Anthropic ≈ Anthropic (both Opus versions cluster, expectedly), so within-lab structure inflates "lab diversity" measure. Test: rerun Lab>Persona excluding within-lab pairings.
- TODO: confirm CM-RG-Education citation format (internal report, not preprinted)

---

## Length budget

| Section | Target length |
|---|---|
| Abstract | 250 words |
| Intro | 1.5 pages |
| Related | 0.75 page |
| Method | 1.5 pages |
| Data | 0.75 page |
| Results | 4 pages |
| Discussion | 1.5 pages |
| Limitations | 0.5 page |
| Conclusion | 0.5 page |
| **Total** | **~11 pages** (Anthropic / arxiv standard) |

---

**Confidence in this abstract: 9.5/10.** Phase 2K paired design (n=18,140) directly resolves the Phase 1 vs combined-data tension by providing the missing paired measurement at scale (n_models=11). Result is a strong and surprising finding (Persona > Lab; 5× spread in persona-volatility by lab). Scale claim verified against published literature: Chatbot Arena (6M human votes), JudgeLM-100K (100K single-judge), Judge's Verdict 2025 (~108K judge-vs-human), JudgeBench (~1.2K pairwise), MT-Bench (~30K) - none combine M×M LLM-judge structure with emergent constructs at our scale. Snimaю 0.5: (a) we don't yet have an independent reviewer, (b) literature scan was thorough but not exhaustive (private benchmarks at Anthropic/OpenAI may exist).
