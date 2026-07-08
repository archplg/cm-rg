# Phase 2L Plan: Bulletproof Tier-aware CM-RG Experiment

**Status**: Planning · Created: 2026-06-06 · Estimated budget: $80-120

## What we're doing

Replicating CM-RG methodology on **39 frontier LLMs** (13 providers × 3 tiers each), on **new tier-aware advisory tasks**, with full pre-flight checks and post-run verification.

## Tier × Provider matrix (kanban)

13 providers × 3 tiers = 39 models. SLUGs need verification in OpenRouter catalog before any spend (this was the M11 Opus 4.8 bug in Phase 2J).

| Provider | Cheap (Haiku-class) | Mid (Sonnet-class) | Flagship (Opus-class) |
|---|---|---|---|
| Anthropic | Claude Haiku 4.5 | Claude Sonnet 4.6 | Claude Opus 4.7 |
| OpenAI | GPT-5 mini | GPT-5.4 | GPT-5.5 |
| Google | Gemini 3.0 Flash | Gemini 3.0 Pro | Gemini 3.1 Pro |
| Mistral | Mistral Small 3 | Mistral Medium | Mistral Large 2512 |
| DeepSeek | DeepSeek v3 chat | DeepSeek v4 | DeepSeek v4 Pro |
| xAI | Grok 3 mini | Grok 4 | Grok 4.20 |
| Qwen/Alibaba | Qwen 3 Turbo | Qwen 3.5 Max | Qwen 3.7 Max |
| Moonshot/Kimi | Kimi k2 nano | Kimi k2 | Kimi k2.6 |
| Zhipu/GLM | GLM-4 Flash | GLM-4 | GLM-4.5 |
| NVIDIA | Nemotron Nano 9B | Nemotron 51B | Nemotron Super 70B |
| Meta/Llama | Llama 4 Scout | Llama 4 | Llama 4 Maverick |
| Cohere | Command R | Command R+ | Command A |
| IBM | Granite 3.1 8B | Granite 3.1 mid | Granite 3.5 |

**IMPORTANT**: each row needs OpenRouter slug verification + per-token pricing audit. Half of these may not exist on OpenRouter or may have different exact slug. Step 1 below catches this.

## Pre-flight checks (mandatory before any real run)

### Check 1: OpenRouter slug verification

**Script**: `verify_phase2l_slugs.py`

For each of 39 candidate models:
1. Query `https://openrouter.ai/api/v1/models` once, cache
2. Match candidate slug against catalog
3. Report: `[OK] provider/model — $X/$Y per Mtok` or `[MISSING] provider/model — try alternative slug`

**Outcome**: final list of confirmed slugs + pricing. If providers like IBM Granite or Zhipu GLM aren't on OpenRouter, either swap to alternative or note as unavailable.

### Check 2: Cost dry-run (single mini cell)

**Script**: `dry_run_phase2l.py`

- 1 task (cheapest one), 1 condition, 1 run
- All 39 models (or whatever survived check 1)
- Full 4-phase pipeline: free response → anonymize → triadic → cross-rate
- **Verify** `usage.cost` returned non-zero for every model. If zero, log + use manual fallback.
- Log actual cost vs. estimated cost - calibrate before full run.

**Outcome**: realistic cost per model per task. Extrapolate to full run. **Abort if total estimate > 1.5× budget**.

### Check 3: Parser robustness

The Phase 2H/2J bug: Mistral and Grok produced non-standard construct output formats; parser failed silently.

**Script**: `test_parsers.py`

For each model from check 1:
1. Send minimal triad elicitation prompt
2. Verify parser extracts left_pole / right_pole / triad
3. Report failures with raw output excerpt

**Outcome**: model list confirmed for triad parsing. Models that fail get model-specific parser patches or are excluded.

### Check 4: Atomic write strategy

Phase 2F killed by Windows write corruption (`cell.json` truncated to 2576 bytes). Must enforce:

- Write to `cell.json.tmp` first
- `fsync()` after write
- Verify size matches `len(content)`
- Atomic rename `cell.json.tmp → cell.json`
- Backup `cell.json` before any overwrite (keep last 3 versions in `_backups/`)

**Patch**: `run_experiment.py::save_cell()` enforces all of the above.

### Check 5: Real-time monitoring dashboard

Long runs are vulnerable to silent failures. Need live view:

- `monitor_phase2l.py` opens an HTML dashboard
- Reads `state.json` every 5 seconds
- Shows: cells_complete / cells_planned, spend, per-model success rate, errors in last 60s
- Browser tab stays open during run; you watch it

### Check 6: Auto-retry with backoff

Some providers (especially Cohere, Llama via OpenRouter) drop requests sporadically. Retry strategy:

- 3 attempts, exponential backoff (10s, 30s, 90s)
- On 3rd failure: log to `failed_calls.log`, continue pipeline
- After run: review failed_calls.log, manually retry or exclude

### Check 7: Post-run verification (7-check)

After run: `verify_phase2l.py` runs 7 sanity checks (like `verify_phase2j.py`):

1. n_cells_complete == n_planned (no silent dropouts)
2. n_responses_per_model >= 0.7 × expected (model didn't crash mid-run)
3. n_constructs per cell in [25, 45] range (parser worked)
4. n_ratings per cell == n_models × n_constructs × n_elements (Phase 4 complete)
5. Cost reconciliation: sum(per_model_cost) ≈ OpenRouter activity CSV total (within 5%)
6. No truncated JSON files (size > 100KB for typical cell.json)
7. PCA on combined ratings explains >50% variance in PC1+PC2 (sanity that data has structure)

**Outcome**: report card. Anything failing → don't proceed to publication.

## New tier-aware tasks (7 new)

You wanted "tier-сравнение" — tasks where cheap vs flagship should show a difference. Designed to require:
- Multi-factor judgment
- Long-horizon thinking
- Domain expertise

Working titles (need full briefs in next step):

| ID | Domain | Hypothesis: tier-sensitive? |
|---|---|---|
| K | Complex M&A under regulatory uncertainty (4 jurisdictions, antitrust risk) | High - flagship should articulate tradeoffs better |
| L | Multi-generational succession in family business ($200M, 3 heirs, varying competence) | High - flagship handles human nuance |
| M | Pandemic response strategy for mid-income country ($5B budget, 6 options) | Medium - reasoning depth matters |
| N | R&D portfolio allocation across 8 emerging technologies (5-year horizon) | High - long-horizon |
| O | Crisis communication after a $50M data breach (6 strategy frames) | Low-medium - mostly intuition |
| P | Constitutional reform proposal in fractured democracy (5 institutional options) | High - polish + integration |
| Q | Cross-jurisdiction AI regulation harmonization (5 approaches) | Very high - domain expertise + tradeoffs |

Each task brief defines 5 options + free response prompt + research justification.

## Cost estimate

Phase 2J: $15.32 for 11 models × 7 tasks × 2 conditions = 154 cells × ~$0.10/cell.

Phase 2L:
- 39 models × 7 new tasks × 2 conditions = 546 model-cells
- 4 phases per cell (free, anonymize, triad, rate)
- Avg per phase: $0.04 for cheap, $0.20 for flagship
- Mid-estimate: 546 × $0.13 = **$71** for base run
- Phase 2K paired (if doing): +$20-30
- Buffer for reasoning-heavy retries: +$15-20

**Total estimate: $90-120.** Within "$100+" budget.

If budget tight: exclude IBM Granite + Zhipu GLM (least proven on advisory tasks) to drop to 11 providers × 3 = 33 models, save ~$15.

## Workflow / next steps

1. **Today (no spend)**: Run Check 1 — verify_phase2l_slugs.py. Confirm 39 models exist on OpenRouter with valid pricing. Update matrix above.
2. **After confirmation**: Write 7 task briefs (K-Q).
3. **Then**: Patch run_experiment.py for atomic writes + cost validation + parser robustness.
4. **Then ($1-2 spend)**: Run Check 2 — dry_run_phase2l.py on single task. Validate cost estimates.
5. **Then ($5-10 spend)**: Pilot run on 2 tasks × all models. Reveal hidden issues at smaller scale before going full.
6. **Then ($80-100 spend)**: Full Phase 2L run with monitor dashboard open.
7. **Then**: post-run verification + analysis + dataset update on HuggingFace.

Each step gates the next. **Anything failing means stop and fix, not proceed.**

## Key risks (lessons from Phase 2F-2J)

| Risk | Mitigation |
|---|---|
| Model slug missing on OpenRouter → $0 cost bug | Check 1 verifies all slugs + pricing |
| Cell.json truncated during write | Atomic write with size verify + backup |
| Parser silently fails on non-standard output | Check 3 tests every model |
| Reasoning-heavy models exhaust token budget | Set max_tokens explicitly, monitor cost in real-time |
| Run dies mid-pipeline | Auto-retry + state.json with resume capability |
| Inflated cost from a few providers | Daily spend cap; halt + alert if 1 provider > 2× expected |
| Self-similar models (e.g. Llama 4 vs Llama 4 Scout) skew PCA | Note in analysis - they're tier comparison, not independent |

## What I deliver next

If you say "go" — I generate:
1. `config_phase2l.yaml` with candidate slug list
2. `verify_phase2l_slugs.py` — pre-flight check 1 script
3. `dry_run_phase2l.py` — pre-flight check 2 script
4. 7 new task briefs (K-Q) drafted to ~80% — you review domain accuracy

**You then run check 1 yourself** (it makes a single $0 API call) and report results. I update the matrix. We move to next step.

This is the "no косяки" path.
