# Pilot vs Cross-Model: head-to-head comparison

Cross-model design: 70 cells from `results`
Pilot design (single Claude in 5 roles): 42 cells from `results_pilot`

Tasks in common: A, B, C, D, E, F, G

## Headline finding

| Design | Mean disagreement | 95% CI | n cells |
|---|---|---|---|
| Cross-model (5 labs) | **0.476** | [0.430, 0.528] | 70 |
| Pilot (single Claude in 5 roles) | **0.206** | [0.190, 0.224] | 42 |
| **Delta (cross - pilot)** | **+0.270** | [+0.215, +0.327] | - |

**Interpretation:** Cross-model disagreement is **significantly higher** than pilot. The 95% CI on the delta excludes zero, meaning lab diversity provides evaluative diversity that single-model persona prompting cannot achieve. This is direct evidence that the CM-RG methodology is not redundant with prompt-based perspective elicitation.

## Per-task breakdown

| Task | Cross mean | Pilot mean | Delta | 95% CI on delta | CI excludes 0? |
|---|---|---|---|---|---|
| A | 0.662 | 0.218 | +0.444 | [+0.271, +0.641] | YES |
| B | 0.342 | 0.224 | +0.118 | [+0.014, +0.218] | YES |
| C | 0.512 | 0.192 | +0.320 | [+0.247, +0.401] | YES |
| D | 0.371 | 0.213 | +0.158 | [+0.057, +0.259] | YES |
| E | 0.415 | 0.162 | +0.253 | [+0.150, +0.354] | YES |
| F | 0.536 | 0.229 | +0.307 | [+0.205, +0.418] | YES |
| G | 0.497 | 0.208 | +0.289 | [+0.142, +0.450] | YES |

Tasks where 95% CI on delta excludes zero: **7 of 7**.

## How to use for paper writing

- This analysis goes in **Methods / Methodological validity** section as a core argument that lab diversity is not equivalent to persona diversity.
- The headline statement: *"To rule out that our methodology reduces to single-model persona prompting, we replicated the experimental design with a single Claude Opus 4.7 playing all 5 personas in turn. Cross-model disagreement exceeded pilot disagreement by X.XX (95% CI Y.YY, Z.ZZ), confirming lab diversity contributes evaluative variance distinct from prompt-based elicitation."*
- Where ci_excludes_zero == YES, that specific task supports the conclusion. Tasks where it does not exclude zero are reported in the appendix as caveats.

## Caveats

- The pilot used a single Claude model snapshot. Other backbones (GPT-5.5 in 5 roles, Gemini in 5 roles, etc.) might produce different pilot baselines. We chose Claude as the most aligned single-model baseline.
- Run-to-run variance can mimic cross-design variance. The bootstrap CI on delta accounts for sampling variability within each design but does not partition run-level vs design-level variance. The mixed-effects analysis (see MIXED_EFFECTS_FINDINGS.md) provides a complementary view.
- M5 (Kimi) partial dropout (~30% of cells) may inflate cross-model disagreement if the dropout pattern is non-random. See M5_SENSITIVITY_FINDINGS.md for robustness check.
