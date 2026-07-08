# Phase 2 Extended Plan: A through H (target confidence 9.5/10)

> **Related work cross-references**: see `RELATED_WORK.md` for annotated bibliography. Key recent reference: Sun et al. (2026) "From Expectation to Evaluation" (CHI '26, doi:10.1145/3772318.3790492) - demonstrates LLM expectation-cue bias and validates our anonymization design (Phase 2). Five concrete cross-references documented; informs Methods, Discussion, and Limitations sections.

---


**Goal:** push from current 8.5/10 (publishable workshop paper) to 9.5/10 (top-tier conference / main-track FAccT/ICLR).

**Total additional cost:** ~$60-90 in API calls + 50 hours wall time. No human study yet (that's level I, separate budget).

## Inventory: 4 new Python scripts + 3 new configs + 5 new task briefs

### Free post-hoc analyses (no API cost)

| Script | What it does | Time to run |
|---|---|---|
| `bootstrap_analysis.py` | 1000-resample bootstrap CIs for all key metrics: overall disagreement, per-task, persona effect, cross-model vs pilot delta, Procrustes disparity, variance decomposition | ~3 min |
| `m5_sensitivity.py` | Re-runs analyses with/without M5; reports robustness; per-cell M5 dropout audit | ~30 sec |
| `mixed_effects_analysis.py` | Formal MixedLM via statsmodels: variance components (ICC) per factor + Wald F-tests | ~1 min |
| `construct_validation.py` | Claude-as-rater cluster validation: Cohen's kappa between KMeans clustering and Claude classification | ~2 min, costs ~$0.50 |

### Phase 2B: pilot replication ($15-20, ~12 hours wall)

Single Claude Opus 4.7 plays 5 roles on the same 7 tasks. Direct head-to-head with cross-model.

- Config: `config_phase2b_pilot.yaml`
- Output: `results_pilot/` (separate from main `results/`)
- 42 cells (7 tasks x 2 conditions x 3 runs)

### Phase 2C: extended elements ($10-15, ~8 hours wall)

10-option versions of Tasks D and G. Resolves PCA dimensionality artifact (PC1+PC2 = 1.000 was small-sample issue).

- Config: `config_phase2c_extended.yaml`
- Task briefs: `tasks/task_D10_brief.md`, `tasks/task_G10_brief.md`
- Output: `results_extended/`
- 20 cells (2 tasks x 2 conditions x 5 runs)

### Phase 2F: 3 new tasks ($10-15, ~12 hours wall)

External validity: tests if findings generalize to legal/scientific/urban domains.

- Config: `config_phase2f_newtasks.yaml`
- Tasks H (sentencing reform), I (science funding), J (urban planning)
- Output: `results_phase2f/`
- 30 cells (3 tasks x 2 conditions x 5 runs)

### Phase 2G: 10 runs per cell on existing 7 tasks ($25-30, ~25 hours wall)

Tighten run-to-run variance estimates. Currently CV up to 74% on Task B_N - need n>=10 per cell for stable inference.

- Modify existing `config.yaml`: `extra_runs_for_repeat_task: 9` (was 4)
- Output: extends current `results/`
- 70 NEW cells (7 tasks x 2 conditions x 5 NEW runs on top of existing 5)

## Execution sequence

### Step 1: Free post-hoc analyses (NOW, ~5 minutes)

```powershell
cd C:\Users\Sergey\archipelago_cross_model
pip install statsmodels  # for mixed_effects_analysis
python bootstrap_analysis.py
python m5_sensitivity.py
python mixed_effects_analysis.py
```

After Step 1: you have rigorous statistical inference on the EXISTING 70 cells.
- `bootstrap_analysis/BOOTSTRAP_FINDINGS.md` -> 95% CIs on every claim
- `m5_sensitivity/M5_SENSITIVITY_FINDINGS.md` -> defends against missing-data criticism
- `mixed_effects/MIXED_EFFECTS_FINDINGS.md` -> proper variance decomposition with Wald tests

**These three alone push confidence to 9.0**.

### Step 2: Phase 2B - pilot replication (~12 hours wall, $15-20)

```powershell
cd C:\Users\Sergey\archipelago_cross_model
Copy-Item config.yaml config_phase1_backup.yaml -Force
Copy-Item config_phase2b_pilot.yaml config.yaml -Force
python -u run_experiment.py 2>&1 | Tee-Object -FilePath logs/phase2b.log
# After completion:
Copy-Item config_phase1_backup.yaml config.yaml -Force  # restore main config
```

### Step 3: Phase 2C - extended elements (~8 hours wall, $10-15)

```powershell
Copy-Item config_phase2c_extended.yaml config.yaml -Force
python -u run_experiment.py 2>&1 | Tee-Object -FilePath logs/phase2c.log
Copy-Item config_phase1_backup.yaml config.yaml -Force
```

### Step 4: Phase 2F - new tasks (~12 hours wall, $10-15)

```powershell
Copy-Item config_phase2f_newtasks.yaml config.yaml -Force
python -u run_experiment.py 2>&1 | Tee-Object -FilePath logs/phase2f.log
Copy-Item config_phase1_backup.yaml config.yaml -Force
```

### Step 5: Phase 2G - more runs on existing tasks (~25 hours wall, $25-30)

Edit `config.yaml`: change `extra_runs_for_repeat_task: 4` to `extra_runs_for_repeat_task: 9`. Then:

```powershell
python -u run_experiment.py --resume 2>&1 | Tee-Object -FilePath logs/phase2g.log
```

`--resume` will skip existing 70 cells and add 70 new ones (runs 6-10 per cell).

### Step 6: Construct validation (after enough constructs from 2F + 2G)

```powershell
python construct_validation.py --n_sample 200 --model anthropic/claude-opus-4.7
```

Reports inter-rater Cohen's kappa between KMeans and Claude. If kappa > 0.6: substantial semantic validity. If > 0.8: excellent.

### Step 7: Re-run full analysis on COMBINED dataset

After all phases complete, you'll have:
- `results/` - cross-model 7 tasks x 2 conditions x 10 runs = 140 cells
- `results_pilot/` - pilot replication 42 cells
- `results_extended/` - 10-option 20 cells
- `results_phase2f/` - 3 new tasks 30 cells
- **Total: ~230 cells, ~2000-2500 constructs**

Need to write `combined_analysis.py` that pulls from all 4 results dirs. **I'll write this in Wave 3 (after Phase 2 data is collected)** because it depends on the actual data structure.

## Budget reconciliation

| Phase | Cost | Wall time | Remaining $100 budget |
|---|---|---|---|
| Already spent | $21.34 | done | $78.66 |
| Phase 2B (pilot) | $15-20 | 12 hr | ~$60 |
| Phase 2C (extended) | $10-15 | 8 hr | ~$48 |
| Phase 2F (new tasks) | $10-15 | 12 hr | ~$36 |
| Phase 2G (more runs) | $25-30 | 25 hr | ~$8 |
| Construct validation | $1 | 2 min | ~$7 |
| **Total** | **~$83-100** | **~57 hr** | **buffer $0-7** |

Tight but feasible. If Phase 2G goes over, can do 5 more runs instead of 9 (saves ~$10).

## Expected uplift in confidence

| After step | Confidence | Why |
|---|---|---|
| Step 1 (free analyses) | 9.0 | Closes statistical rigor gaps |
| Step 2 (pilot replication) | 9.2 | Closes pilot-confounded comparison |
| Step 3 (extended elements) | 9.3 | Closes PCA dimensionality artifact |
| Step 4 (new tasks) | 9.4 | Closes external validity gap |
| Step 5 (more runs) | **9.5** | Stable run-to-run variance, n>>30 per (task,condition) |
| Step 6 (validation) | 9.5 | Confirms semantic clusters are meaningful |
| Step 7 (combined analysis) | **9.5** | Full pipeline on ~230 cells |

## Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Phase 2B pilot reveals cross-model offers NO advantage over single-Claude | Low | High | Honest reporting; could pivot paper to "Repertory Grid method validation" angle |
| Phase 2G takes >25 hours (M5 thinking model slowdowns) | Medium | Medium | Reduce extra_runs_for_repeat_task from 9 to 5; still gets us to n=10 |
| Cohen's kappa < 0.4 (KMeans clusters not semantically valid) | Low | Medium | Re-cluster with different parameters or report as exploratory |
| 10-option Tasks D and G produce malformed responses | Low | Low | Pre-test on dry-run first; parser already tolerates partial outputs |
| Total cost exceeds $100 cap | Medium | Low | Hard cap stops experiment; can resume after raising cap |

## What I'll do in Wave 3 (after Phase 2 collection completes)

When you finish all 4 sub-phases and run the 3 free analyses, send me:
- `bootstrap_analysis/BOOTSTRAP_FINDINGS.md`
- `m5_sensitivity/M5_SENSITIVITY_FINDINGS.md`
- `mixed_effects/MIXED_EFFECTS_FINDINGS.md`
- `validation/CONSTRUCT_VALIDATION_FINDINGS.md`
- per-cell summary CSVs from all 4 results dirs
- new construct_decomposition output on combined data

I'll then:
1. Write `combined_analysis.py` (cross-cuts the 4 datasets)
2. Re-do main interpretation with all 230+ cells
3. Draft paper abstract + key tables for **two papers**:
   - **Dataset paper** (NeurIPS D&B): methodology + dataset card + reproducibility
   - **Findings paper** (FAccT / ICLR): hypothesis-driven scientific claims with full statistical support
4. Plan Phase 3 (human baseline, ~$500-2000) if needed for top venue submission

## Quick reference: what to copy to project dir

After fixes to my outputs, files to copy to `C:\Users\Sergey\archipelago_cross_model\`:

```
build_dataset.py
bootstrap_analysis.py
m5_sensitivity.py
mixed_effects_analysis.py
construct_validation.py
config_phase2b_pilot.yaml
config_phase2c_extended.yaml
config_phase2f_newtasks.yaml
PHASE2_EXTENDED_PLAN.md
tasks/task_H_brief.md
tasks/task_I_brief.md
tasks/task_J_brief.md
tasks/task_D10_brief.md
tasks/task_G10_brief.md
```

PowerShell one-liner to copy them all:

```powershell
$src = "C:\Users\Sergey\AppData\Roaming\Claude\local-agent-mode-sessions\519d1321-f18f-49d4-a92f-7b05d46c5d17\4cf7941f-5fbd-40ed-8103-dd244d3f5957\local_295d00b9-f885-4f5c-98e7-426556120d96\outputs\archipelago_cross_model"
$dst = "C:\Users\Sergey\archipelago_cross_model"
@(
  "build_dataset.py", "bootstrap_analysis.py", "m5_sensitivity.py",
  "mixed_effects_analysis.py", "construct_validation.py",
  "config_phase2b_pilot.yaml", "config_phase2c_extended.yaml",
  "config_phase2f_newtasks.yaml", "PHASE2_EXTENDED_PLAN.md"
) | ForEach-Object {
  Copy-Item "$src\$_" -Destination "$dst\$_" -Force
}
@("task_H_brief.md", "task_I_brief.md", "task_J_brief.md", "task_D10_brief.md", "task_G10_brief.md") | ForEach-Object {
  Copy-Item "$src\tasks\$_" -Destination "$dst\tasks\$_" -Force
}
Write-Host "All files copied" -ForegroundColor Green
```
