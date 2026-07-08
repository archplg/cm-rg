# Construct Cluster Validation: KMeans vs Claude

Sampled 200 constructs (from 812 total). Asked anthropic/claude-opus-4.7 to classify each into one of the clusters identified by KMeans clustering in construct_decomposition.py.

**Successfully classified by Claude**: 200 of 200

## Headline metrics

- **Accuracy** (Claude agrees with KMeans on cluster assignment): **56.0%**
- **Cohen's kappa** (agreement adjusted for chance): **0.510**

## How to interpret

- **kappa < 0.4**: poor agreement - KMeans clusters may not be semantically valid
- **kappa 0.4-0.6**: moderate agreement - KMeans captures some structure but Claude sees different boundaries
- **kappa 0.6-0.8**: substantial agreement - KMeans clusters are reasonable approximations of human-readable categories
- **kappa > 0.8**: almost perfect agreement - KMeans matches semantic intuitions strongly

**Verdict**: KMeans clusters have **moderate semantic validity**. Acceptable for exploratory analysis; report with caveat.

## Caveats

- This is **LLM-as-rater**, not human inter-rater. Real inter-rater study with 3+ humans on Prolific would give stronger validation.
- Claude as classifier may share biases with Claude as construct-elicitor (M1). Truly independent validation requires non-Anthropic model.
- Confidence in kappa drops with small n. Run with --n_sample 200 for tighter estimate.
