# Panel recommendation: K (M&A under regulatory uncertainty)

*From a CM-RG grid of 4 models, 2026-07-21. Pool mean pairwise r = 0.633.*

## Recommended panel

- **claude-haiku** (independent voice)
- **claude-fable** (bloc 1 representative)
- **claude-sonnet** (bloc 1 representative)

Panel mean pairwise r = 0.514 vs pool 0.633 (lower = more independent perspectives). Effective independent voices in the panel: **2 of 3**.

## Agreement blocs in the pool (r > 0.7 = effectively one voice)

- Bloc 1: claude-sonnet, claude-opus, claude-fable
- Bloc 2: claude-haiku (solo)

**Warning:** the panel still contains near-duplicates: claude-fable x claude-sonnet (r=0.921). This pool cannot supply more independent voices - to add real diversity, extend the pool (another lab, another tier) and re-run.

## Calibration offsets (vs pool mean rating)

- claude-haiku: +0.15
- claude-sonnet: +0.12
- claude-opus: -0.16
- claude-fable: -0.12

## How to orchestrate

1. Query each panel model **independently** - no cross-talk before answers are in (independence is what diversity buys you).
2. Synthesize with **claude-opus** (most central model, mean r = 0.751 with the pool) - or have it chair a comparison of the panel's answers.
3. If panel answers **converge**, treat that as a strong signal only when it crosses bloc boundaries - agreement inside one bloc is one opinion, not several.
4. When aggregating numeric scores from these models, subtract each rater's calibration offset (listed above) before averaging.

## Honest limits

Panel diversity is measured; the claim that a diverse panel yields a more reliable orchestrated answer is a working hypothesis (supported by ensemble literature, not proven by this run). This grid is one task, one run: agreement structure is task-conditional - re-measure for a very different task, or rely on the published 36-model atlas as a prior.