# CM-RG mini-grid: M&A task x 4 Claude-family models

*Produced by the `cm-rg` Claude Skill (demo mode, subagents), 2026-07-21.
This is a demonstration of the skill's pipeline, not a research claim.*

## What was measured

Four Claude-family model variants each wrote an advisory recommendation for the
same M&A decision brief (task K from the Archipelago study). The responses were
anonymized and shuffled; each model then derived bipolar constructs from a triad
of anonymized responses, and every model rated every response on the union of
all 47 constructs (1-7 scale). No API keys were used: the models ran as
subagents inside a Claude agent session.

## The grid

| | |
|---|---|
| Models (rater = ratee set) | claude-haiku, claude-sonnet, claude-opus, claude-fable (session aliases) |
| Task / condition | K - M&A under regulatory uncertainty / neutral |
| Date / seed | 2026-07-21 / 42 |
| Constructs elicited | 47 (11 + 12 + 12 + 12 per model; exact-duplicate rate 0%) |
| Ratings | 752 (4 raters x 4 elements x 47 constructs, 0 null cells) |

A first observation before any rating: **all four models independently
recommended Option B** (the geographically partitioned asset purchase), each
naming China's cybersecurity review as the risk to excise. Unanimity on the
decision - and yet, as the grid shows, not on how the responses are construed.

## Agreement

![Inter-rater agreement](analysis/agreement_heatmap.png)

Mean pairwise r = **0.63** (median 0.66). But the mean hides the structure:

- **sonnet x opus = 0.90, sonnet x fable = 0.92, opus x fable = 0.93** - the
  three larger variants form a near-consensus bloc.
- **haiku x others = 0.31-0.42** - the small-tier model applies the same
  constructs differently, sitting closer to the *cross-lab* agreement level
  from the published 36-model study (r = 0.20) than to its own family's bloc.

This echoes the tier structure reported in Archipelago Phase 2L, where rater
tier explained far more variance than ratee tier. In this tiny sample the echo
is directional only - but it emerged unprompted from a 15-minute demo run.

## Calibration

Mean rating per rater: haiku 3.93, sonnet 3.90, opus 3.62, fable 3.65 (group
mean 3.77). The two larger variants rate systematically lower by ~0.3. Note:
the published study found *cheap*-tier raters rating lower on average; here the
small model rated slightly higher. With one task and four raters this is noise
until replicated - reported for completeness, not as a finding.

## The element map

![Element map](analysis/element_map.png)

PC1 (48% of variance) is driven by *sectioned vs continuous prose*, *structured
vs essayistic*, and the treatment of the Asia carve-out (*optionality-preserving
vs clean-break*, *tethered vs severed*): haiku's heavily formatted,
call-option-preserving memo sits at one end, sonnet's unbroken clean-break
prose at the other. PC2 (35%) is a contractual-protection axis (*risk-transfer
terms vs structure-only*, *downside-capped vs uncapped*, *hedged vs unhedged*):
opus - break fees, hell-or-high-water clauses, ticking fees - anchors the
protected pole. Together the two axes carry 83% of the variance.

The most contested element was E2 (sonnet's response): mean absolute pairwise
rating difference 1.24, versus 1.09-1.16 for the others.

## Constructs elicited

Content constructs: which jurisdiction binds (*China-centric vs EU-centric*,
*EU-centric vs UK-centric*), remedy philosophy (*structural vs behavioral*,
*regulator-facing vs structure-facing*), deal protection (*hedged vs unhedged*,
*downside-capped vs uncapped*), fallback logic (*alternative-structure pivot vs
revert-to-binary*). Style constructs: formatting (*sectioned vs prose* - found
independently by three of four raters), voice (*first-person advisor vs
impersonal*), register (*aphoristic vs analytical*). Framing constructs:
*risk-adjusted vs expected-value*, *monetized vs proportional* quantification.

Zero exact duplicates across raters: each model carved the space in its own
vocabulary, even while converging on the same recommendation.

## Limitations

This demo measures **within-family diversity only**: all four raters are
Claude variants, so the published within-family baseline (r ~0.34-0.45) - not
the cross-lab 0.20 - is the relevant comparison, and the observed 0.63 mean
(0.90+ within the larger trio) is expected to exceed it. The models ran inside
an agent harness whose system prompts may color responses - this is not a
clean-API measurement, and the aliases do not pin exact model snapshots. One
task, one run: no stability estimate, no significance anywhere; with 4
elements the PCA is descriptive. For lab-grade numbers, run the full
OpenRouter pipeline in this repository (36 models, pre-registered protocol,
bootstrap CIs).

---

*Method: Kelly (1955) repertory grid, ported per Archipelago CM-RG Phase 2L.
Files: `grid.json` (full data), `analysis/metrics.json` (all numbers),
`phase1_responses.json` / `anonymized.json` / `phase3_constructs.json` (raw
phases). Reproduce: `python scripts/analyze_grid.py grid.json analysis/`.*
