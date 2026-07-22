# Using the cm-rg skill: step by step

[Русская версия](USAGE.ru.md)

The skill runs a Cross-Model Repertory Grid: models answer a decision task,
see each other's anonymized answers, derive their own bipolar constructs, and
cross-rate everyone on everything. Output: a grid, agreement metrics, and maps.

## 1. Install (once)

Pick one:

- **Save skill button** - if you received `cm-rg.skill` in a Claude chat,
  click Save skill on the file card (if your org allows skill saving).
- **Claude Code, personal**: copy the `skill/cm-rg` folder to
  `~/.claude/skills/cm-rg` (Windows: `C:\Users\<you>\.claude\skills\cm-rg`).
- **Claude Code, per-project**: copy it to `.claude/skills/cm-rg` inside the
  repository - active only in that project.

For the analysis scripts you need Python 3.10+ with
`pip install numpy matplotlib requests`.

## 2. Demo grid - no API keys (~15 min, free)

Works where Claude can spawn subagents (Claude Code, Cowork). Say:

> Run a CM-RG mini-grid on the models you can spawn as subagents.

Claude executes all four phases and writes `grid.json`,
`analysis/metrics.json`, two figures, and `REPORT.md` into the working
directory. To use your own decision case instead of the bundled M&A task,
paste a 200-400 word brief with ~5 options and say "use this as the grid task".

## 3. Any OpenRouter models

1. Get a key: openrouter.ai - Sign in - Keys - Create Key; add $5-10 credits.
   Never paste the key into files or chats.
2. Set it in your shell: `export OPENROUTER_API_KEY="sk-or-v1-..."`
   (PowerShell: `$env:OPENROUTER_API_KEY = "sk-or-v1-..."`).
3. Pick 3-12 exact slugs from openrouter.ai/models.
4. From `skill/cm-rg/scripts/`:

```bash
python run_openrouter.py --selftest                      # offline check, $0
python run_openrouter.py --models "anthropic/claude-sonnet-4.6,openai/gpt-5.5,google/gemini-3.1-pro" \
    --brief ../assets/task_brief_ma.md --out run1 --dry-run   # plan + cost, $0
python run_openrouter.py --models "..." --brief ../assets/task_brief_ma.md --out run1 --max-usd 5
python analyze_grid.py run1/grid.json run1/analysis
```

The runner validates slugs against the live catalog, estimates cost, retries
transient failures, parses reasoning-model output robustly, adds dynamic slug
redaction on top of the standard anonymization, and enforces a hard spend cap
(default $5). Typical cost for 3-5 models on one task: cents to a couple of
dollars, tier-dependent - the cap protects you either way.

With the skill installed you can simply tell Claude: "run CM-RG on GPT-5.5,
Gemini 3.1 Pro and Qwen 3.7 Max via OpenRouter, cap $5" - it drives these
commands and writes the report (you still set the key yourself).

## 4. Analysis only

Have a grid already (your run or the published dataset)? Ask Claude to
"analyze grid.json per CM-RG", or run `analyze_grid.py` directly.

## 5. Panel for your task (the original use case)

Before orchestrating a hard question across models, find out which candidates
give independent perspectives and which just echo each other - so you don't
pay for three copies of one opinion.

1. Run a grid ON YOUR TASK (your working prompt is the Phase 1 brief) - via
   subagents (free) or OpenRouter with your candidate models. Or just tell
   Claude: "compose a model panel for this task: <task>, candidates: ...".
2. Then:
   ```bash
   python compose_panel.py run1/grid.json run1 --k 3   # --must-include <slug> to pin a model
   ```
3. `PANEL.md` gives you: the max-diversity panel, agreement blocs (r > 0.7 =
   effectively one voice), the number of real independent voices, a
   synthesizer suggestion (most central model), calibration offsets for score
   aggregation, and a warning when the pool cannot supply more diversity
   (widen the pool, not k).

Orchestration rules of thumb: query panel models independently; let the
central model synthesize; treat convergence as a strong signal only when it
crosses bloc boundaries. For routine questions skip measurement and use the
study's atlas as a prior: one Western flagship + one Chinese flagship + one
open-weights model. Honest limit: panel diversity is measured; "diverse panel
gives a more reliable answer" is a working hypothesis, not something this run
proves.

## Reading the results

`mean_pairwise_r`: published reference points - 0.20 across 36 models from 12
labs; 0.34-0.45 within one family; above 0.7 the raters share one evaluative
frame. `calibration_mean_rating`: who rates systematically high/low. The
heatmap shows agreement blocks; the PCA map shows which responses the group
construes as similar (axis meaning in `pca_top_loadings`).

## Troubleshooting

401 - key not set or wrong. 402 - top up OpenRouter credits. "not in
OpenRouter catalog" - typo in a slug. "batch unparseable - cells left null" -
a model returned broken JSON after retry; nulls are disclosed in metrics,
re-run if needed. "STOPPED: spend cap" - partial results saved, raise
`--max-usd`. Raw responses for every phase live in the run directory.
