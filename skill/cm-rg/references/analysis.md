# CM-RG analysis reference

`scripts/analyze_grid.py` computes everything below into `metrics.json`.
Interpret against the published Archipelago baselines - a number without a
baseline is a Rorschach blot.

## Metrics

**Inter-rater agreement.** For each pair of raters, Pearson r between their
rating vectors over all shared non-null (element, construct) cells (minimum 8
shared cells per pair, else the pair is skipped and listed in
`metrics.json.skipped_pairs`). `mean_pairwise_r` is the headline number.

Baselines from the 36-model Phase 2L study (June 2026): overall mean r =
0.200 (weak consensus); Western flagship cluster within-cluster r = 0.34;
within-family (same lab) r ~0.34-0.45; divergent open-weights models r <= 0.
Psychometric convention treats r > 0.7 as acceptable inter-rater reliability -
no model cluster reaches it. For a same-family demo grid expect r roughly in
the 0.3-0.6 band; below that band is a notable finding about within-family
diversity, above ~0.7 means the models largely share one evaluative frame on
this task.

**Calibration.** Mean rating per rater across all cells. The study found a
tier effect: mid-tier raters ~3.84 mean, cheap ~3.57, flagship ~3.78. In a
demo grid, a rater sitting >0.3 above or below the group mean is showing a
calibration offset - report it as "rates systematically higher/lower", not as
"is more positive" (poles are arbitrary directions, not sentiment).

**Element map (PCA).** Elements x mean-rating matrix (cell = mean over raters
of that element's rating on that construct), column-centered, SVD. Report PC1
and PC2 variance shares. Loadings name the axes: take the 3-5 constructs with
the largest |loading| per PC and read their poles - if PC1's top loadings are
"decisive vs deliberative", "risk-embracing vs risk-averse", PC1 is a
decisiveness/risk axis. With few elements (4-6) PCA is descriptive, not
inferential - never quote significance for it.

**Construct profile.** Count per rater, total union size, and duplicate rate
(exact-duplicate constructs across raters / total). High duplicate rate means
raters converge on the same evaluative language - itself a finding.

**Disagreement per element.** Mean absolute pairwise rating difference per
element. The element models disagree about most is usually the most
interesting response - quote it in the report.

## Reading the figures

`agreement_heatmap.png` - pairwise r matrix, diverging scale centered at 0.
Look for blocks (clusters that agree internally) and cold rows (a rater that
agrees with nobody - check its parse quality before calling it divergent).

`element_map.png` - elements in PC1/PC2 space. Distance = evaluative
dissimilarity as seen by the raters collectively. An isolated element drew a
distinctive response; a tight pair got construed as near-equivalent.

## Reporting discipline

State n everywhere (models, constructs, ratings, null cells). Round r to two
decimals. One task = one snapshot: no stability or generality claims without
repeat runs (the study used repeats and bootstrap CIs for its headline
numbers; a demo has neither). When comparing to baselines, compare like with
like: same-family demo vs the within-family baseline, not vs the 0.200
cross-lab figure.
