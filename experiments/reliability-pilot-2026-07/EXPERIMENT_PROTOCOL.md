# PRE-REGISTRATION: Does a diverse panel give a more reliable answer?

**Status: locked 2026-07-21, before any data collection. Deviations go to a
deviations note in the report.**
**Experimenter: Claude (Cowork session) + Sergey Dolgov (Archipelago).**

## 1. Question

CM-RG panel composition assumes: a diversity-aware panel improves the
reliability of an orchestrated answer. That claim has never been tested with
this pipeline. This pilot tests it on tasks with verifiable ground truth.

## 2. Items

20 freshly generated computational problems (combinatorics, modular
arithmetic, calendar, clock angles, probability, digit sums), ground truth
computed by code (`generate_items.py`, seedless deterministic math). Freshly
generated = not present in training corpora; contamination-resistant.
Answers: integer, reduced fraction, or weekday name. Exact-match scoring
after normalization. Items are fixed before any model sees them.

## 3. Conditions

**Arm 1 (cross-model, confounded by capability - acknowledged).** Each of
haiku, sonnet, opus, fable (Claude family via subagents, the same pool whose
CM-RG grid was measured on 2026-07-21) answers all 20 items independently,
neutral prompt, 2 batches of 10. Panels composed post-hoc from the SAME
singles (no extra calls):
- Panel D (diverse, from compose_panel.py on the task-K grid): haiku, fable, sonnet.
- Panel R (redundant bloc trio): opus, fable, sonnet.
- Aggregation: majority vote; 3-way tie scores as incorrect (strict); tie
  rate reported separately.

**Arm 2 (same-model, capability-controlled prompt diversity).** fable x 3
personas (Q, S, C - verbatim from the Archipelago persona set) vs fable x 3
independent neutral runs (sampling diversity only). Majority vote each.

## 4. Hypotheses and locked predictions

- **H-A**: Panel D differs from Panel R in accuracy. Signal: net margin >= 3
  items. **Prediction: R >= D.** In this pool the only out-bloc voice (haiku)
  is also the weakest model; on verifiable items the diversity-vs-capability
  confound should dominate. A D win would be a surprise worth publishing.
- **H-B**: persona-panel beats neutral-panel (same model, so capability is
  controlled - this is the clean diversity manipulation). Signal: net margin
  >= 3 items. **Prediction: approximate tie** - personas are a weak
  manipulation for computational items; a null here bounds WHERE prompt
  diversity matters.
- **H-C (primary)**: cross-bloc convergence predicts correctness. Split items
  by whether haiku's answer matches the trio majority answer. Criterion:
  accuracy(converged) - accuracy(not converged) >= 20 percentage points, with
  converged coverage >= 30% of items. **Prediction: confirmed.** This is the
  operational claim: the panel as an escalation detector ("when the divergent
  voice agrees with the bloc, trust; when it splits, verify").
- **Secondary (headroom)**: union accuracy (any of 4 correct) minus best
  panel accuracy = what better aggregation than majority could still win.

## 5. What this pilot cannot show

n = 20 items: only large effects are detectable; report counts, not
significance theater. One model family: cross-lab diversity is not tested
here (requires OpenRouter runs - next step). Agent harness, single run per
condition (except neutral x3): no stability estimate. Computational items
only: results may not transfer to judgment tasks - the domain where CM-RG
diversity was measured. These limits go verbatim into the report.

## 6. Procedure locks

Prompts fixed before collection (neutral solver prompt; personas prepended
verbatim; "do not use any tools"; FINAL-lines output format). One retry per
call on format failure. All raw outputs saved before parsing. Scoring script
committed with the report; every reported number must be reproducible from
raw responses + `score.py`.

**END OF PRE-REGISTRATION.**
