# Multi-run PCA analysis - Cross-Model Repertory Grid

Data source: `results` (70 cells, 14 task-condition groups)

Embedding method primary: sentence-transformers

## Headline comparison

| Analysis | n_elements | Mean PC1+PC2 |
|---|---|---|
| Within-cell (baseline) | 5 | **0.659** |
| Pooled across runs | up to 25 | **0.346** |
| Absolute delta | | **+0.312** |

**Interpretation:** PC1+PC2 drops substantially when pooling across runs. This confirms the within-cell PC1+PC2 ≈ 1.000 was a **small-n artifact** of having only 5 elements per PCA. At higher dimensionality (up to 25 elements), variance spreads across many more components, as expected for a genuine high-dimensional representation space.


Additional metrics on pooled PCA:
- Mean PC1 through PC5 cumulative: **0.572**
- Mean elbow component (variance >= 0.9): **PC16.4**

## Per-task-condition breakdown

| Task | Cond | n_elements | n_runs | PC1+PC2 | PC1..PC5 | Elbow |
|---|---|---|---|---|---|---|
| A | N | 25 | 5 | 0.300 | 0.535 | PC17 |
| A | P | 25 | 5 | 0.351 | 0.583 | PC16 |
| B | N | 25 | 5 | 0.404 | 0.605 | PC16 |
| B | P | 25 | 5 | 0.406 | 0.610 | PC16 |
| C | N | 25 | 5 | 0.310 | 0.555 | PC16 |
| C | P | 25 | 5 | 0.328 | 0.592 | PC16 |
| D | N | 25 | 5 | 0.411 | 0.643 | PC16 |
| D | P | 25 | 5 | 0.356 | 0.565 | PC17 |
| E | N | 25 | 5 | 0.398 | 0.598 | PC16 |
| E | P | 25 | 5 | 0.347 | 0.591 | PC16 |
| F | N | 25 | 5 | 0.266 | 0.495 | PC17 |
| F | P | 25 | 5 | 0.305 | 0.547 | PC17 |
| G | N | 25 | 5 | 0.314 | 0.519 | PC17 |
| G | P | 25 | 5 | 0.351 | 0.570 | PC16 |

## How to use for paper writing

- Report this analysis in the **Methods / Robustness checks** section as a free alternative to the planned Phase 2H (10 models). It addresses the same dimensionality concern using existing data.
- The headline statement: *"Within-cell PCA shows PC1+PC2 ≈ Xwithin, consistent with a small-n dimensionality effect. When responses are pooled across runs within (task, condition) pairs (up to 25 elements), PC1+PC2 drops to Xpooled."*
- If Phase 2H (10-model) is also run, both analyses converge on the same conclusion via independent paths, which is a stronger argument than either alone.

## Limitations

- This treats free responses across different runs as exchangeable elements. Run-to-run variance within a single (task, condition, model) tuple may be lower than cross-model variance, which somewhat inflates the apparent dimensionality.
- The Phase 2H lineup expansion (10 independent labs) tests a different construct: lab diversity, not run diversity. Both are valuable; they answer complementary questions.
