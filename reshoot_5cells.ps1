# reshoot_5cells.ps1
# Re-runs the 5 cells that came back empty in the first experiment run.
# Cleans state, applies all patches, runs cells one by one, then full analysis.
#
# Cost estimate: ~$3-5 (5 cells x ~15 API calls x bumped max_tokens for reasoning)
# Wall time: ~30-60 minutes

[CmdletBinding()]
param(
    [switch]$AutoConfirm,
    [switch]$SkipAnalysisAfter
)

$ErrorActionPreference = "Stop"
$ProjectDir = "C:\Users\Sergey\archipelago_cross_model"
Set-Location $ProjectDir

# Wall-clock timer for the whole re-shoot
$globalStopwatch = [System.Diagnostics.Stopwatch]::StartNew()
function Get-Elapsed {
    $ts = $globalStopwatch.Elapsed
    "{0:hh\:mm\:ss}" -f $ts
}

# Helper to run a Python snippet from a literal here-string (no PS interpolation)
function Invoke-PythonScript {
    param([string]$Script)
    $tmp = "$env:TEMP\_reshoot_step.py"
    Set-Content -Path $tmp -Value $Script -Encoding UTF8
    & python $tmp
    $code = $LASTEXITCODE
    Remove-Item $tmp -ErrorAction SilentlyContinue
    return $code
}

# Sanity
if (-not (Test-Path "run_experiment.py")) {
    Write-Host "[FATAL] Not in project dir or run_experiment.py missing" -ForegroundColor Red
    exit 1
}
if (-not $env:OPENROUTER_API_KEY) {
    $userKey = [Environment]::GetEnvironmentVariable("OPENROUTER_API_KEY", "User")
    if ($userKey) { $env:OPENROUTER_API_KEY = $userKey }
}
if (-not $env:OPENROUTER_API_KEY) {
    Write-Host "[FATAL] OPENROUTER_API_KEY not set" -ForegroundColor Red
    exit 1
}

$emptyCells = @("A_N_run1","A_P_run1","B_N_run1","B_P_run1","B_N_run2")

Write-Host ""
Write-Host "=== Re-shoot plan ===" -ForegroundColor Cyan
Write-Host "Cells to re-shoot: $($emptyCells -join ', ')"
Write-Host "Estimated cost: ~`$3-5"
Write-Host "Wall time: ~30-60 minutes"
Write-Host ""

if (-not $AutoConfirm) {
    $ans = Read-Host "Type YES to proceed"
    if ($ans -ne "YES") {
        Write-Host "Aborted by user." -ForegroundColor Yellow
        exit 0
    }
}

# 1. Clean state.json of the 5 cells
Write-Host ""
Write-Host "1. Cleaning state.json of empty cells..." -ForegroundColor Cyan
$cleanScript = @'
import json
p = "results/state.json"
with open(p, encoding="utf-8") as f:
    s = json.load(f)
empty = ["A_N_run1","A_P_run1","B_N_run1","B_P_run1","B_N_run2"]
removed = [c for c in empty if c in s["cells"]]
for c in empty:
    s["cells"].pop(c, None)
with open(p, "w", encoding="utf-8") as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
print(f"Removed {len(removed)} stale cells from state.json: {removed}")
'@
Invoke-PythonScript $cleanScript | Out-Host
if ($LASTEXITCODE -ne 0) { Write-Host "[FAIL] state.json cleanup failed" -ForegroundColor Red; exit 1 }

# 2. Wipe leftover folders
Write-Host ""
Write-Host "2. Wiping leftover cell folders..." -ForegroundColor Cyan
foreach ($c in $emptyCells) {
    $patterns = @("results\$c", "results\$c.empty_skip", "results_skipped\$c.empty_skip", "results_skipped\$c")
    foreach ($p in $patterns) {
        $full = Join-Path $ProjectDir $p
        if (Test-Path $full) {
            Remove-Item $full -Recurse -Force
            Write-Host "  Removed $p" -ForegroundColor Green
        }
    }
    # Also wipe per-cell audit logs so finish_reason patterns are fresh
    $auditDir = Join-Path $ProjectDir "logs\api_calls\$c"
    if (Test-Path $auditDir) {
        Remove-Item $auditDir -Recurse -Force
        Write-Host "  Removed audit dir $c" -ForegroundColor Green
    }
}

# 3. Re-shoot each cell with patched script
Write-Host ""
Write-Host "3. Running 5 cells with patched script (validate-on-skip + bumped max_tokens)..." -ForegroundColor Cyan
$failed = @()
$cellTimings = @()
foreach ($c in $emptyCells) {
    Write-Host ""
    Write-Host "  === $c === (elapsed so far: $(Get-Elapsed))" -ForegroundColor Yellow
    $cellSw = [System.Diagnostics.Stopwatch]::StartNew()
    python -u run_experiment.py --cell $c
    $cellSw.Stop()
    $cellElapsed = "{0:mm\:ss}" -f $cellSw.Elapsed
    $cellTimings += [PSCustomObject]@{ cell = $c; elapsed = $cellElapsed }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  [FAIL] cell $c exit code $LASTEXITCODE (took $cellElapsed)" -ForegroundColor Red
        $failed += $c
    } else {
        Write-Host "  [OK] $c finished in $cellElapsed" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Per-cell timing:" -ForegroundColor Cyan
$cellTimings | ForEach-Object { Write-Host ("  {0,-15} {1}" -f $_.cell, $_.elapsed) }

# 4. Show status
Write-Host ""
Write-Host "4. Status after re-shoot:" -ForegroundColor Cyan

$statusScript = @'
import json
with open("results/state.json", encoding="utf-8") as f:
    s = json.load(f)
cost = s.get("total_cost_usd", 0.0)
print(f"  total cost (state.json): ${cost:.4f}")
print(f"  cells in state.json:")
for cid, c in sorted(s["cells"].items()):
    fr = len(c.get("free_responses", {}))
    valid_fr = sum(1 for v in c.get("free_responses", {}).values() if isinstance(v, str) and v.strip())
    co = len([k for k, v in c.get("constructs", {}).items() if v])
    ra = len([k for k, v in c.get("ratings", {}).items() if v])
    er = len(c.get("errors", []))
    status = c.get("status", "?")
    print(f"    {cid:<15} status={status:<23} valid_resp={valid_fr}/{fr} constructs_from={co} ratings_from={ra} errors={er}")

import os, glob
print()
print("  finish_reason patterns from this run audit files:")
audit_dirs = ["logs/api_calls/" + c for c in ["A_N_run1","A_P_run1","B_N_run1","B_P_run1","B_N_run2"]]
counts = {}
empties = 0
for d in audit_dirs:
    if not os.path.isdir(d):
        continue
    for f in glob.glob(d + "/*.json"):
        try:
            with open(f, encoding="utf-8") as fp:
                rec = json.load(fp)
            fr = rec.get("finish_reason", "?")
            counts[fr] = counts.get(fr, 0) + 1
            content = rec.get("raw_response_content")
            if not isinstance(content, str) or not content.strip():
                empties += 1
        except Exception:
            pass
for fr in sorted(counts.keys(), key=lambda k: -counts[k]):
    print(f"    {fr}: {counts[fr]}")
print(f"    empty/None content calls: {empties}")
'@
Invoke-PythonScript $statusScript | Out-Host

if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Host "[WARN] $($failed.Count) cells failed: $($failed -join ', ')" -ForegroundColor Yellow
}

if (-not $SkipAnalysisAfter) {
    Write-Host ""
    Write-Host "5. Running full analysis + render pipeline on 10 cells..." -ForegroundColor Cyan
    @("analysis","operator_outputs","coach_kit","ai_audit","executive_briefing","paper_outputs") | ForEach-Object {
        $p = Join-Path $ProjectDir $_
        if (Test-Path $p) {
            Remove-Item $p -Recurse -Force
            Write-Host "  Cleared $_/" -ForegroundColor Green
        }
    }
    & "$ProjectDir\run_all.ps1" -SkipExperiment -SkipInstall
}

$globalStopwatch.Stop()
$totalElapsed = "{0:hh\:mm\:ss}" -f $globalStopwatch.Elapsed

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green
Write-Host "Total wall time: $totalElapsed" -ForegroundColor Cyan
Write-Host ""
Write-Host "Send these files back to Claude:" -ForegroundColor Cyan
Write-Host "  analysis\FINDINGS.md"
Write-Host "  analysis\comparison_vs_pilot.md"
Write-Host "  analysis\per_cell_summary.csv"
Write-Host "  analysis\all_summaries.json"
Write-Host "  operator_outputs\all_insights.json"
