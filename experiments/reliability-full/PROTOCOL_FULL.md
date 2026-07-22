# PRE-REGISTRATION (draft to lock): full-scale reliability experiment

**36-model cross-lab test of "a diversity-aware panel gives a more reliable
answer" and of the convergence signal.**

Status: DRAFT prepared 2026-07-21. Sergey locks it by filling the run date
below BEFORE executing `run_reliability.py`. After that, changes go to a
deviations file only.

Run date locked: [fill before running]

## 1. Pool

The 36 Phase 2L models (12 providers x 3 tiers), exact slugs in
`models_catalog.json` (from `config_phase2l.yaml`; re-verify slugs against the
live catalog via dry-run before spending). All 36 are measured as singles.
Panel composition uses the 33 models present in the Phase 2L pairwise-r
matrix; C_C, C_M, Z_C lack pairwise data and can appear only in RANDOM/TOP
panels.

## 2. Items

50 parametric items, tiers 1-5 (`items_bank.py`, seed 20260721, tier mix
1:5, 2:10, 3:15, 4:15, 5:5), ground truth computed by code, freshly generated
- contamination-proof. The pilot (reliability-pilot-2026-07) showed the
Claude family at ceiling on tiers 1-2; tiers 3-5 (7-9-digit exact products,
130+ step iterations, digit sums of 13^120-scale powers, nested constraints)
are designed to put mid and cheap tiers into the 30-70% band.

**Escalation rule (locked):** if pool-MEDIAN single accuracy > 90%, generate
tiers 2-6 with seed 20260722 and re-run; never hand-edit single items after
seeing who failed what.

## 3. Collection

Singles only: every model answers every item once (temperature 0, batches of
10, one retry + one re-ask on missing FINAL lines). Unanswered after retry =
null = incorrect for that model, absent vote in panels. Resumable
(`singles.json` is the state); raw outputs saved per call. Spend cap
`--max-usd 60` (expected $10-40; dry-run prints a live estimate). All panels
are composed post-hoc from the same singles - measuring 36 models once prices
in EVERY panel strategy for free.

## 4. Panels (composed from the REAL Phase 2L r-matrix, locked now)

| Panel | Members (short names) | Panel mean r | What it tests |
|---|---|---|---|
| D3 | N_C, X_M, Q_C | -0.32 | raw max-diversity = anti-consensus periphery |
| D5 | N_C, X_M, Q_C, D_M, L_M | -0.13 | same, k=5 |
| DQ3 | N_M, X_M, D_M | -0.07 | diversity constrained to mid+flagship tiers |
| DQ5 | N_M, X_M, D_M, C_F, L_M | -0.05 | same, k=5 |
| R3 | G_M, O_M, O_F | 0.70 | redundant consensus bloc |
| R5 | G_M, O_M, O_F, A_M, K_C | 0.60 | same, k=5 |
| ATLAS3 | O_F, Q_F, N_C | 0.02 | heuristic: Western flagship + Chinese flagship + divergent open-weights |

Post-hoc comparators from the same data: TOP3/TOP5 (best singles by observed
accuracy) and RANDOM3/RANDOM5 (500 resamples = the null band).

## 5. Hypotheses and locked predictions

- **H1 (primary): DQ3 sits above the RANDOM3 90% null band.** Prediction:
  uncertain overall; on the tier 3-5 subset DQ3 >= R3. This is the honest
  core question.
- **H2: D3 (raw periphery) falls BELOW the RANDOM3 band.** Prediction:
  confirmed - diversity without capability is noise, and the experiment
  quantifies the cost of naive max-diversity selection.
- **H3 (practical): convergence signal.** For DQ3 and ATLAS3:
  accuracy(unanimous) - accuracy(split) >= 20 points, unanimous coverage
  30-80%. Prediction: confirmed. Deliverable: the risk-coverage table -
  "accept when unanimous, escalate when split".
- **H4: TOP3 vs DQ3.** Prediction: TOP3 >= DQ3 on this computational bank;
  a reversal would be the headline surprise.
- Analysis code (`analyze_reliability.py`: strict majority with tie=abstain,
  2000-item bootstrap, 500 random panels) is committed before the run.

## 6. Limitations declared in advance

Computational domain only (judgment-shaped verifiable items - resolved
forecasts, tolerance-band estimation - are a separate follow-up wave);
one call per model-item (no stability estimate); OpenRouter routing and
provider-side variation not controlled; 3 pool models lack pairwise data;
panel definitions depend on Phase 2L's judgment-task grid transferring to
this domain - which the pilot showed is NOT guaranteed, and that transfer
question is itself part of what H1 measures.
