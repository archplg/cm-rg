---
name: cm-rg
description: Run a Cross-Model Repertory Grid (CM-RG) - measure how AI models judge, which evaluative constructs they use, and how much they disagree (Kelly's repertory grid ported to LLMs) - and compose a diversity-aware model panel for orchestrating a specific task. Zero-API-key mode on Claude subagents, or ANY OpenRouter models via the bundled spend-capped runner. Use whenever the user wants to pick which models to combine for a hard question or ensemble ("which models should answer this", "build a panel", "who will disagree"); compare models' judgment, values or evaluative style; measure inter-model or LLM-as-judge agreement; run a grid on GPT/Gemini/Qwen/DeepSeek; replicate the Archipelago study; or asks "how do models judge each other", "do LLMs agree", "which model should be the judge" - even if they never say "repertory grid".
---

# Cross-Model Repertory Grid (CM-RG)

CM-RG transposes the Repertory Grid technique (Kelly, 1955) from human psychology
onto language models. Instead of imposing external rating criteria, each model
derives its own bipolar evaluative dimensions ("constructs") from anonymized peer
responses, then every model rates every response on the union of constructs. The
output is a structured grid revealing how each model carves the evaluative space.

Why this design matters: there is **no gold answer** to memorize (contamination
resistant), constructs are **emergent** at runtime, responses are **anonymized**
before rating, and scaling is **relative** (compare responses to each other, not
to an absolute standard). Keep these four properties intact in every mode - they
are the methodological core. Reference study: Archipelago Phase 2L, 36 models,
3.05M ratings, mean inter-rater r = 0.200 (github.com/archplg/cm-rg).

## Pick a mode

1. **Demo grid (no API keys)** - if the environment can spawn subagents on
   different models (e.g. Claude family via the Agent/Task tool), run a real
   mini-grid right here. ~10-15 min. Default when the user "just wants to see it".
2. **Any OpenRouter models (API key required)** - the user names models from
   other labs (GPT, Gemini, Qwen, DeepSeek, ...) or wants a cross-lab grid.
   Run `scripts/run_openrouter.py` - it executes all four phases against any
   3-12 OpenRouter slugs with a hard spend cap. For the full pre-registered
   36-model design, use the CM-RG repository pipeline instead.
3. **Analysis only** - the user has grid data (their run, or the published
   dataset) and wants metrics, maps, interpretation.
4. **Panel for a task** - the user wants to know WHICH models to combine to
   answer a specific hard question reliably. This is the original use case:
   run a grid on THEIR task (mode 1 or 2 mechanics), then
   `scripts/compose_panel.py` turns the grid into a panel recommendation.

Ask which mode only if the intent is unclear from context.

## Mode 1 - Demo grid

Follow the four-phase protocol exactly. The exact system prompts are in
`references/protocol.md` - use them **verbatim** (they are copied from the
Archipelago Phase 2L pipeline; changed wording = changed measurement, and
results stop being comparable to the published baselines).

**Setup.** Choose a decision task brief: use the user's own decision brief if
they have one (any 200-400 word brief with ~5 options works), otherwise
`assets/task_brief_ma.md` (M&A under regulatory uncertainty, task K from the
study). List the models you can actually spawn (for Claude Code / Cowork:
haiku, sonnet, opus + the session's own model). 3 models minimum, 4-6 ideal.
Create a run directory; save every phase's raw output to JSON files as you go -
raw-first, parse later, so nothing is lost to a parsing bug.

**Phase 1 - free response.** Spawn one subagent per model, in parallel, with the
Phase 1 neutral prompt + the brief. Each returns a 300-500 word recommendation.
Instruct subagents to use no tools and return only the recommendation text.
Save `phase1_responses.json`: `[{"model": "...", "text": "..."}]`.

**Phase 2 - anonymization.** Run `scripts/anonymize.py phase1_responses.json outdir/`.
It strips self-identifying patterns, shuffles order with a seed, labels responses
E1..EN, and writes `anonymized.json` + `mapping.json`. Never include the mapping
in any later prompt - raters must not know who wrote what.

**Phase 3 - triadic elicitation.** Assign each model one triad of anonymized
responses (distinct triads, assignment table in `references/protocol.md`).
Spawn parallel subagents with the Phase 3 system prompt; each returns 8-12
bipolar constructs as strict JSON. If a response fails to parse, retry that
model once with an explicit "previous output was not valid JSON" note. Save
`phase3_constructs.json` with the source model recorded per construct.

**Phase 4 - cross-rating.** Build the union of all elicited constructs
(deduplicate only exact string duplicates - near-synonyms from different raters
are signal, not noise). Spawn one subagent per model with the Phase 4 system
prompt, the construct list, and all anonymized responses; each rates every
response on every construct, 1-7. More than 50 constructs - split into batches
of 50. Validate dimensions (n_responses x n_constructs); re-ask once on
mismatch. Save `phase4_ratings.json`.

**Analysis.** Assemble `grid.json` (schema below), then run
`scripts/analyze_grid.py grid.json outdir/`. It computes inter-rater agreement,
per-rater calibration, an element PCA map, and writes `metrics.json` plus two
figures. Read `references/analysis.md` before interpreting - it defines each
metric and gives the published baselines to compare against.

**Report.** Write `REPORT.md` using exactly this structure:

```
# CM-RG mini-grid: [task] x [N] models
## What was measured   (2-3 sentences, method in plain words)
## The grid            (models, task, date, counts: constructs, ratings)
## Agreement           (mean pairwise r + heatmap figure + 1-paragraph reading)
## Calibration         (mean rating per rater; who rates high/low)
## The element map     (PCA figure + which constructs drive the axes)
## Constructs elicited (grouped by theme, with pole_a vs pole_b examples)
## Limitations         (mandatory - see below)
```

The Limitations section is not optional. State plainly: same-family models
measure within-family diversity only (published within-family r is ~0.34-0.45
vs 0.20 across labs - expect higher agreement here, and say so); subagents run
inside an agent harness whose system prompt may color responses (not a clean
API measurement); one task, one run - no stability claim. A demo that hides
its limits reads as hype and damages the method's credibility; one that states
them reads as science.

## Mode 2 - Any OpenRouter models

`scripts/run_openrouter.py` runs the full four-phase protocol on any 3-12
OpenRouter model slugs and writes a `grid.json` for `analyze_grid.py`. Never
reimplement the API loop - the script already handles retries, robust JSON
parsing (reasoning tags, fences), construct batching, slug validation against
the live catalog, cost estimation, and a hard spend cap.

Workflow:

1. Confirm `OPENROUTER_API_KEY` is set in the environment. Never write the key
   into a file, a prompt, or the chat; if it is missing, ask the user to set it
   themselves and wait.
2. Pick models with the user (exact slugs from openrouter.ai/models). Mixed
   tiers and labs give the most interesting grids.
3. Always run `--dry-run` first and show the user the call count and estimated
   cost; proceed only after they confirm. Default cap is $5 (`--max-usd`).
4. Run, then analyze:

```bash
python scripts/run_openrouter.py --models "anthropic/claude-sonnet-4.6,openai/gpt-5.5,google/gemini-3.1-pro" \
    --brief assets/task_brief_ma.md --out run1 --dry-run   # plan + cost, $0
python scripts/run_openrouter.py --models "..." --brief assets/task_brief_ma.md --out run1 --max-usd 5
python scripts/analyze_grid.py run1/grid.json run1/analysis
```

`--selftest` runs the whole pipeline offline with a fake transport ($0, no
key) - use it to verify the environment before a paid run. The runner also
adds dynamic slug redaction on top of the standard anonymization patterns, so
arbitrary models' self-identification is stripped too.

Write the report from the same template as Mode 1. In Limitations, state the
model list with exact slugs and date (catalog slugs change), and note this is
one task / one run unless repeated. For the full pre-registered 36-model
design (personas, repeats, bootstrap CIs), use the CM-RG repository pipeline:
pick a config (`config_phase2b_pilot.yaml` ~$5, `config_phase2j.yaml` ~$15,
`config_phase2l.yaml` ~$120), copy over `config.yaml`, run pre-flight checks
(`pre_flight/`, <$5), then `python run_experiment.py` - and warn about real
costs before any paid run.

## Mode 3 - Analysis only

Get grid data from the user's run directory or the published dataset
(`huggingface.co/datasets` - see repository README for the current dataset id).
Convert to `grid.json` if needed, run `scripts/analyze_grid.py`, interpret via
`references/analysis.md`. Ground every number you state in `metrics.json` -
if a metric was not computed, say so instead of estimating.

## Mode 4 - Panel for a task (diversity-aware orchestration)

Goal: for the user's REAL task, identify which models give independent
perspectives and which merely echo each other, then recommend an orchestration
panel. Two tiers - pick by stakes:

- **Fast prior (no measurement)**: for routine questions, reason from the
  published 36-model atlas: Western flagships (Anthropic, OpenAI, Google, xAI)
  form one agreement bloc (within-cluster r = 0.34, 3x average) - picking three
  of them buys one voice, not three. Chinese flagships sit in a transitional
  zone; small open-weights models are the anti-consensus periphery. A
  diversity-first default: one Western flagship + one Chinese flagship + one
  open-weights model.
- **Measured panel (high stakes)**: run the grid ON THE USER'S TASK - their
  actual brief is the Phase 1 brief (works with any decision-shaped prompt;
  if the user's question has no options, ask them for 30 seconds of framing or
  synthesize a brief from it and show them first). Use mode 1 (subagents,
  free) or mode 2 (OpenRouter, ~$0.5-3). Then:

```bash
python scripts/compose_panel.py run1/grid.json run1/ --k 3
# optional: --must-include anthropic/claude-sonnet-4.6
```

`compose_panel.py` outputs `PANEL.md` + `panel.json`: the max-diversity panel
(greedy max-min dispersion on 1-r distances), agreement blocs (r > 0.7 = one
voice), effective number of independent voices, a synthesizer suggestion (most
central model), per-model calibration offsets to subtract when aggregating
scores, and warnings when the pool cannot supply more real diversity (the fix
is a wider pool, not a bigger k).

Present the recommendation with its honesty block intact: diversity is
measured, "diverse panel -> more reliable answer" is a working hypothesis;
agreement structure is task-conditional. For factual (single-right-answer)
questions, use the panel differently: convergence ACROSS blocs is the
reliability signal; convergence inside one bloc proves little.

## grid.json schema

```json
{
  "meta": {"task": "K", "condition": "N", "date": "2026-07-21", "runner": "subagents|openrouter"},
  "elements": [{"id": "E1", "model": "claude-haiku"}],
  "constructs": [{"id": "C1", "pole_a": "decisive", "pole_b": "deliberative",
                  "context": "decision style", "source_model": "claude-opus"}],
  "ratings": [{"rater": "claude-haiku", "matrix": [[1, 4, 7]]}]
}
```

`matrix[i][j]` = rater's 1-7 rating of element i on construct j; `null` for
missing cells. 1 = pole_a, 7 = pole_b, 4 = neutral.

## Honesty rules

Report only numbers that `analyze_grid.py` actually computed. Never extrapolate
a demo grid to claims about "AI models in general" - the published 36-model
study exists for that; cite it instead. Always disclose model list, date, and
runner, because model versions drift and results are snapshots.
