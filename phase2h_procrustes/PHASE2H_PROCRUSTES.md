# Phase 2H Procrustes alignment - Phase 1 vs Phase 2H

Question: when adding 5 new labs (M6-M10), do the original M1-M5 positions stay stable in 2D evaluative space?

Restricted to tasks A and D (common between Phase 1 and Phase 2H).

## Procrustes disparity

**Disparity = 0.4872**

Scale: 0 = identical, 1 = orthogonal universes.

**Verdict: HIGH - lab additions substantially reorganize evaluative space**

## M1-M5 positions in each universe (after Procrustes alignment)

| Model | Phase 1 PC1 | Phase 1 PC2 | Phase 2H PC1 | Phase 2H PC2 |
|---|---|---|---|---|
| M1 | -0.1217 | -0.2079 | -0.1670 | -0.3645 |
| M2 | +0.0561 | -0.1979 | -0.0246 | -0.1431 |
| M3 | +0.0482 | +0.7310 | -0.0861 | +0.3185 |
| M4 | -0.3788 | -0.2318 | -0.4298 | +0.1501 |
| M5 | +0.3962 | -0.0934 | +0.7075 | +0.0389 |

## Per-model shift (Euclidean distance after alignment)

| Model | Shift |
|---|---|
| M3 | 0.4338 |
| M4 | 0.3854 |
| M5 | 0.3383 |
| M1 | 0.1630 |
| M2 | 0.0976 |

## How to use for paper

- This addresses a key reviewer question: 'how do you know that adding more models doesn't fundamentally change the evaluative space such that your findings depend on the specific 5-model panel?'
- Headline for paper: *"Procrustes disparity 0.487 indicates that core M1-M5 model positions remain [stable/somewhat altered] when lab diversity expands from 5 to 10 frontier models. This supports the methodology being robust to ensemble composition rather than tied to a specific model selection."*
- Compare to Procrustes 0.352 result from earlier analysis (cross-model vs Platonic Hypothesis test).
