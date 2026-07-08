# M5 (Moonshot Kimi) Sensitivity Analysis

Generated from 70 cells.

## M5 participation rate

- **Fully participated**: 22 of 70 (31.4%)
  - Full = has free response AND >=1 constructs AND has ratings dict
- **Partial participation**: 48 cells (response but lost downstream)
- **No response at all**: 0 cells

## Headline metric sensitivity (overall disagreement)

- Mean disagreement with M5: **0.476**
- Mean disagreement WITHOUT M5: **0.477**
- Absolute delta: **+0.0003**
- Relative change: **+0.1%**

Interpretation: **headline finding is robust to M5 exclusion** (< 10% relative change). M5 dropout does not materially affect conclusions.

## Per-task breakdown

| Task | Disagreement w/ M5 | Disagreement w/o M5 | Delta |
|---|---|---|---|
| A | 0.662 | 0.662 | -0.000 |
| B | 0.342 | 0.349 | +0.007 |
| C | 0.512 | 0.535 | +0.023 |
| D | 0.371 | 0.365 | -0.007 |
| E | 0.415 | 0.408 | -0.007 |
| F | 0.536 | 0.524 | -0.012 |
| G | 0.497 | 0.495 | -0.002 |

## How to use this for paper writing

- Report **primary analysis with M5 included** (this is the main dataset).
- In a **Limitations** subsection or supplementary materials, report the M5 dropout rate and this sensitivity analysis.
- If the relative change is < 10%, conclude: 'findings are robust to the M5 missing-data pattern'.
- The full per-cell sensitivity table is in `sensitivity_table.csv`.
