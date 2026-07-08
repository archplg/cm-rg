# SETUP - Windows step-by-step

For Sergey's machine. Path uses `C:\Users\Sergey` (the symlinked path).

## Step 1: Get OpenRouter access

1. Open https://openrouter.ai/ in browser
2. Click "Sign up" - use Google or GitHub login (fastest)
3. Once logged in, go to https://openrouter.ai/settings/credits
4. Click "Add credits" - load **$50 USD** via credit card
   - Budget needed: ~$45. Buffer: $5.
   - Credits do not expire.
5. Go to https://openrouter.ai/settings/keys
6. Click "Create new key", name it `archipelago-experiment`
7. **Copy the key (starts with `sk-or-v1-...`) immediately and save it somewhere safe.** You cannot see it again.

## Step 2: Verify model IDs

Before running, confirm the 5 model IDs are available. Open https://openrouter.ai/models and search for each:

- `anthropic/claude-opus-4.7`
- `openai/gpt-5.5` (if not found, edit config.yaml to use `openai/gpt-5.4`)
- `google/gemini-3.1-pro-preview`
- `deepseek/deepseek-v4-pro`
- `moonshotai/kimi-k2.6`

If any ID is missing or has changed, edit `config.yaml` and update the `id:` field for that model. The `fallback_id:` will be used automatically if the primary fails.

## Step 3: Install Python

Skip this step if Python 3.11+ is already on your machine.

1. Go to https://www.python.org/downloads/
2. Download Python 3.12 for Windows (64-bit installer)
3. Run installer. **Important: check "Add python.exe to PATH"** on the first screen.
4. Click "Install Now"
5. After install, open PowerShell and verify:
   ```
   python --version
   ```
   Should show `Python 3.12.x` or similar.

## Step 4: Set up the experiment directory

1. Open PowerShell (Windows key, type "powershell", Enter)
2. Create the directory and navigate to it:
   ```
   mkdir C:\Users\Sergey\archipelago_cross_model
   cd C:\Users\Sergey\archipelago_cross_model
   ```
3. Copy these 5 files into that directory (you will receive them):
   - `run_experiment.py`
   - `config.yaml`
   - `analyze.py`
   - `requirements.txt`
   - `PROTOCOL.md`
4. Also copy the `tasks/` and `personas/` subdirectories into the same place.
5. Verify structure:
   ```
   dir
   ```
   You should see the 5 files and 2 subdirectories.

## Step 5: Install Python dependencies

In the same PowerShell window:
```
pip install -r requirements.txt
```
This downloads `requests`, `pyyaml`, `pandas`, `numpy`, `scikit-learn`, `scipy`, `matplotlib`, `seaborn`. Takes 2-5 minutes. If you see warnings about cached versions, ignore them; errors stop the installation, warnings do not.

## Step 6: Set the API key

In the same PowerShell window, paste your key:
```
$env:OPENROUTER_API_KEY = "sk-or-v1-...your-key-here..."
```
**Do not put the key in any file.** Setting it this way keeps it only in the current PowerShell session.

To make it permanent (so you don't have to set it every time):
```
[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-v1-...your-key-here...", "User")
```
After running this, close and reopen PowerShell.

## Step 7: Dry-run validation

Before any API spend, run the script in dry-run mode:
```
python run_experiment.py --dry-run
```

This will:
- Verify all 5 model IDs exist on OpenRouter
- Print pricing for each model
- Estimate total cost
- Confirm the 10 cells are correctly enumerated
- Make zero API calls beyond the `/models` listing

If you see "DRY RUN complete - no API spend.", the setup is correct. If you see errors, send them to Claude before proceeding.

## Step 8: Real run

```
python run_experiment.py
```

The script will:
1. Re-run pre-flight checks
2. Ask you to type `YES` to confirm
3. Run all 10 cells sequentially (~30-90 minutes total wall time)
4. Print progress: each model call, each cost, each cell completion
5. Save results to `./results/<cell_id>/cell.json` per cell
6. Save running state to `./results/state.json`
7. Stop hard if total cost exceeds $80

You can leave it running and check back. Logs go to `./logs/run_YYYYMMDD_HHMMSS.log`.

If interrupted (you close the window, network drops, etc.), resume with:
```
python run_experiment.py --resume
```
Already-completed cells are skipped.

To re-run a single cell:
```
python run_experiment.py --cell A_N_run1
```

## Step 9: Analyze results

After all cells complete, run:
```
python analyze.py
```
This produces:
- Per-cell PCA biplots in `./analysis/<cell_id>/`
- Cross-cell comparison plots in `./analysis/comparison/`
- Summary report: `./analysis/FINDINGS.md`
- Comparison to pilot: `./analysis/comparison_vs_pilot.md`

Send `FINDINGS.md` and the `comparison_vs_pilot.md` to Claude for joint interpretation.

## Troubleshooting

**"Set OPENROUTER_API_KEY environment variable"** - you did not set the key in Step 6, or you opened a new PowerShell window after setting it temporarily. Set again.

**"X NOT FOUND in OpenRouter catalog"** - the model ID changed since this script was written. Update `config.yaml`, replacing the `id:` for that model with what you see on https://openrouter.ai/models.

**"All attempts failed for X"** - that specific model had repeated API errors. Check `./logs/` for details. Likely transient; try `--resume` after 5 minutes.

**"BUDGET HARD STOP at $X"** - cost exceeded the cap in `config.yaml`. This is a safety brake. Open `config.yaml`, raise `total_budget_usd` if you trust the run, then `--resume`.

**Rate limits** - if you see HTTP 429 repeatedly on one model, OpenRouter is throttling. Wait 10 minutes and resume.

**"parsed only N constructs from output"** - the model returned constructs in an unexpected format. Check `./results/<cell>/cell.json`, look at `raw_output_excerpt`. May need to manually edit or accept N<3 for that model/cell.

## Cost monitoring

In another PowerShell window during the run:
```
type results\state.json | findstr total_cost_usd
```
Shows current spend.

## What to send to Claude when done

1. `./results/state.json` (high-level summary)
2. `./analysis/FINDINGS.md`
3. `./analysis/comparison_vs_pilot.md`
4. Any error messages from `./logs/`

That is enough for joint interpretation.
