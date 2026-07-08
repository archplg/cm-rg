# Mixed-Effects Variance Decomposition

Generated from 14253 ratings across 70 cells.

## 1. Variance components (random-effects only)

Each row shows what proportion of total rating variance is explained when that factor is treated as the sole random-effect grouping.

| Factor | ICC | % of total variance |
|---|---|---|
| task | 0.000 | 0.0% |
| condition | 0.000 | 0.0% |
| rater_persona | 0.000 | 0.0% |
| rater_model | 0.000 | 0.0% |
| cell_id | 0.000 | 0.0% |

## 2. Fixed-effects model

```
rating ~ task + condition + rater_persona + (1 | rater_model)
```

### Wald tests for grouped effects

| Effect group | Wald chi2 | df | p |
|---|---|---|---|
| task | error | - | - |
| condition | error | - | - |
| persona | error | - | - |

### Significant individual coefficients (p < 0.05)

| Coefficient | Estimate | 95% CI | p |
|---|---|---|---|
| C(task)[T.C] | -0.253 | [-0.401, -0.105] | 0.0008 |
| C(task)[T.E] | -0.209 | [-0.358, -0.059] | 0.0062 |
| C(task)[T.F] | -0.424 | [-0.575, -0.273] | 0.0000 |

## How to interpret for paper

- **ICC** (intraclass correlation): proportion of variance attributable to a grouping factor. ICC > 0.2 = strong factor effect.
- **% of total variance**: ICC * residual = how much of the raw rating scale variance this factor explains.
- **Wald chi2 test**: tests whether all levels of a categorical factor are jointly equal (group effect).
- **Significant coefficient with CI not crossing 0**: that specific contrast (e.g., persona vs neutral) has reliable effect.

This analysis is more robust than the ad-hoc variance decomposition in `construct_decomposition.py decomp3` and should be used in the paper.
