# run_all.ps1
# End-to-end runner for the Archipelago cross-model experiment.
# Runs every step from pip install through final paper export, with
# checkpoints, logging, and a bundled-results folder at the end.
#
# Usage (in PowerShell):
#   cd C:\Users\Sergey\archipelago_cross_model
#   .\run_all.ps1                # full run, with confirmation gates
#   .\run_all.ps1 -SkipInstall   # skip pip install (deps already there)
#   .\run_all.ps1 -DryRunOnly    # validate cost + model IDs, do not spend
#   .\run_all.ps1 -Resume        # resume run_experiment.py from last checkpoint
#   .\run_all.ps1 -SkipExperiment  # data already collected, only analyze + render
#   .\run_all.ps1 -AutoConfirm   # skip interactive prompts (DANGEROUS: spends money)

[CmdletBinding()]
param(
    [switch]$SkipInstall,
    [switch]$DryRunOnly,
    [switch]$Resume,
    [switch]$SkipExperiment,
    [switch]$AutoConfirm
)

$ErrorActionPreference = "Stop"
$ProjectDir = "C:\Users\Sergey\archipelago_cross_model"

if (-not (Test-Path $ProjectDir)) {
    Write-Host "[FATAL] Project directory not found: $ProjectDir" -ForegroundColor Red
    Write-Host "        Unzip archipelago_cross_model.zip there first."
    exit 1
}
Set-Location $ProjectDir

$RunStamp = Get-Date -Format "yyyyMMdd_HHmmss"
$RunLogDir = Join-Path $ProjectDir "logs"
if (-not (Test-Path $RunLogDir)) { New-Item -ItemType Directory -Path $RunLogDir | Out-Null }
$RunLog = Join-Path $RunLogDir "run_all_$RunStamp.log"

function LogLine($level, $msg) {
    $stamp = Get-Date -Format "HH:mm:ss"
    $line = "[$stamp] $level $msg"
    $color = switch ($level) {
        "INFO" { "White" }
        "OK"   { "Green" }
        "WARN" { "Yellow" }
        "ERR"  { "Red" }
        "STEP" { "Cyan" }
        default { "White" }
    }
    Write-Host $line -ForegroundColor $color
    Add-Content -Path $RunLog -Value $line -Encoding UTF8
}

function Run-Step($label, $cmd, $required = $true) {
    LogLine "STEP" "--- $label ---"
    LogLine "INFO" "Command: $cmd"
    $stepLog = Join-Path $RunLogDir "step_$($label -replace '[^A-Za-z0-9]','_')_$RunStamp.log"
    try {
        Invoke-Expression "$cmd 2>&1 | Tee-Object -FilePath '$stepLog' -Append"
        $code = $LASTEXITCODE
        if ($null -eq $code) { $code = 0 }
        if ($code -ne 0) {
            LogLine "ERR" "$label exited with code $code (see $stepLog)"
            if ($required) {
                LogLine "ERR" "Required step failed. Aborting."
                Write-FinalReport $false
                exit $code
            } else {
                LogLine "WARN" "Non-required step failed; continuing."
            }
        } else {
            LogLine "OK" "$label finished"
        }
    } catch {
        LogLine "ERR" "$label threw: $($_.Exception.Message)"
        if ($required) {
            Write-FinalReport $false
            exit 1
        }
    }
}

function Confirm-Or-Exit($prompt) {
    if ($AutoConfirm) {
        LogLine "WARN" "AutoConfirm enabled - skipping prompt: $prompt"
        return
    }
    Write-Host ""
    $ans = Read-Host $prompt
    if ($ans -ne "YES") {
        LogLine "INFO" "User did not type YES (entered: '$ans'). Aborting."
        exit 0
    }
}

function Write-FinalReport($success) {
    $reportDir = Join-Path $ProjectDir "FINAL_BUNDLE_$RunStamp"
    if (-not (Test-Path $reportDir)) { New-Item -ItemType Directory -Path $reportDir | Out-Null }

    $manifest = @{
        run_stamp = $RunStamp
        success   = $success
        completed_at = (Get-Date -Format "o")
        project_dir = $ProjectDir
        log_file = $RunLog
    }

    $toCopy = @(
        @{src="analysis\FINDINGS.md"; dst="FINDINGS.md"},
        @{src="analysis\comparison_vs_pilot.md"; dst="comparison_vs_pilot.md"},
        @{src="analysis\per_cell_summary.csv"; dst="per_cell_summary.csv"},
        @{src="analysis\all_summaries.json"; dst="all_summaries.json"},
        @{src="paper_outputs\all_api_calls.csv"; dst="all_api_calls.csv"},
        @{src="paper_outputs\all_constructs.csv"; dst="all_constructs.csv"},
        @{src="paper_outputs\reproducibility_appendix.md"; dst="reproducibility_appendix.md"},
        @{src="results\state.json"; dst="state.json"},
        @{src="results\run_manifest.json"; dst="run_manifest.json"}
    )
    foreach ($item in $toCopy) {
        $src = Join-Path $ProjectDir $item.src
        if (Test-Path $src) {
            Copy-Item -Path $src -Destination (Join-Path $reportDir $item.dst) -Force
            $manifest["bundled_$($item.dst)"] = "present"
        } else {
            $manifest["bundled_$($item.dst)"] = "missing"
        }
    }
    $manifest | ConvertTo-Json -Depth 4 | Set-Content -Path (Join-Path $reportDir "run_manifest.json") -Encoding UTF8

    Write-Host ""
    LogLine "STEP" "==============================="
    if ($success) {
        LogLine "OK" "All steps complete."
    } else {
        LogLine "ERR" "Run failed - see log."
    }
    LogLine "INFO" "Bundle: $reportDir"
    LogLine "INFO" "Full log: $RunLog"
    Write-Host ""
    Write-Host "Send these files back to Claude:" -ForegroundColor Cyan
    foreach ($item in $toCopy) {
        $p = Join-Path $reportDir $item.dst
        if (Test-Path $p) {
            Write-Host "  $p" -ForegroundColor Green
        }
    }
}

# ============================================================
# Start
# ============================================================
LogLine "STEP" "Archipelago cross-model run starting at $RunStamp"
LogLine "INFO" "Project: $ProjectDir"
LogLine "INFO" "Switches: SkipInstall=$SkipInstall DryRunOnly=$DryRunOnly Resume=$Resume SkipExperiment=$SkipExperiment AutoConfirm=$AutoConfirm"

# --- 0. Sanity: python + key
LogLine "STEP" "0. Sanity check"
try {
    $pyver = (& python --version 2>&1) | Out-String
    LogLine "OK" "Python: $($pyver.Trim())"
} catch {
    LogLine "ERR" "python not in PATH. Install Python 3.12 first."
    exit 1
}

if (-not $env:OPENROUTER_API_KEY) {
    $userKey = [Environment]::GetEnvironmentVariable("OPENROUTER_API_KEY", "User")
    if ($userKey) {
        $env:OPENROUTER_API_KEY = $userKey
        LogLine "INFO" "Imported OPENROUTER_API_KEY from User scope into current session."
    } else {
        LogLine "ERR" "OPENROUTER_API_KEY not set in current session or User scope."
        LogLine "ERR" "Temporary set: `$env:OPENROUTER_API_KEY = 'sk-or-v1-...your-key-here...'"
        LogLine "ERR" "Permanent set: [Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY','sk-or-v1-...','User')"
        exit 1
    }
}
if ($env:OPENROUTER_API_KEY -notmatch "^sk-or-v1-") {
    LogLine "WARN" "API key does not start with 'sk-or-v1-'. May be malformed."
}
LogLine "OK" "OPENROUTER_API_KEY present (length: $($env:OPENROUTER_API_KEY.Length))"

# --- 1. pip install
if (-not $SkipInstall) {
    Run-Step "1_pip_install" "python -m pip install --upgrade pip"
    Run-Step "1_pip_install_deps" "python -m pip install -r requirements.txt"
} else {
    LogLine "INFO" "Skipping pip install (per -SkipInstall)"
}

# --- 2. dry-run
if (-not $SkipExperiment) {
    Run-Step "2_dry_run" "python run_experiment.py --dry-run"

    if ($DryRunOnly) {
        LogLine "OK" "DryRunOnly mode - stopping after dry-run."
        Write-FinalReport $true
        exit 0
    }

    # --- 3. real run
    LogLine "STEP" "3. Real experiment run (this spends money)"
    LogLine "WARN" "Estimated cost: ~`$45, hard cap: `$80 (see config.yaml)."
    LogLine "WARN" "About to call OpenRouter API across 10 cells x 5 models x 3 phases = 150 calls."
    Confirm-Or-Exit "Type YES to proceed with the real run, anything else to abort"

    # Auto-feed YES into the script's input prompt (the script asks again).
    # cmd.exe is more reliable for stdin redirection to native processes than PS pipes.
    $realRunArgs = "run_experiment.py"
    if ($Resume) { $realRunArgs += " --resume" }
    Run-Step "3_real_run" "cmd /c `"echo YES| python $realRunArgs`""
} else {
    LogLine "INFO" "Skipping experiment (per -SkipExperiment). Will run analyses on existing results/."
}

# --- 4. analysis pipeline (all non-API steps)
Run-Step "4_analyze"                    "python analyze.py"
Run-Step "5_operator_synthesis"         "python operator_synthesis.py"
Run-Step "6_visualizations"             "python visualizations.py"             $false
Run-Step "7_visualizations_interactive" "python visualizations_interactive.py" $false
Run-Step "8_render_coaches"             "python render_for_coaches.py"         $false
Run-Step "9_render_ai_developers"       "python render_for_ai_developers.py"   $false
Run-Step "10_render_business"           "python render_for_business.py"        $false
Run-Step "11_export_for_paper"          "python export_for_paper.py"           $false

Write-FinalReport $true
exit 0
