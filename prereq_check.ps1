# prereq_check.ps1
# Pre-flight check before launching the Archipelago cross-model experiment.
# Run this BEFORE run_all.ps1 to catch missing prerequisites without spending money.
#
# Usage (in PowerShell, from any folder):
#   .\prereq_check.ps1
#
# Exit codes: 0 = ready to run, non-zero = problem detected

$ErrorActionPreference = "Stop"
$ProjectDir = "C:\Users\Sergey\archipelago_cross_model"
$ExpectedFiles = @(
    "run_experiment.py", "analyze.py", "operator_synthesis.py",
    "visualizations.py", "visualizations_interactive.py",
    "render_for_coaches.py", "render_for_ai_developers.py",
    "render_for_business.py", "export_for_paper.py",
    "config.yaml", "requirements.txt", "PROTOCOL.md"
)
$ExpectedDirs = @("tasks", "personas")

$problems = @()
$warnings = @()

function Write-Header($text) {
    Write-Host ""
    Write-Host "=== $text ===" -ForegroundColor Cyan
}

function Write-Check($ok, $msg) {
    if ($ok) {
        Write-Host "  [OK] $msg" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] $msg" -ForegroundColor Red
    }
}

Write-Header "1. Python"
try {
    $pyver = (& python --version 2>&1) | Out-String
    if ($pyver -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]; $minor = [int]$matches[2]
        if ($major -ge 3 -and $minor -ge 11) {
            Write-Check $true "Python $major.$minor found (>= 3.11)"
        } else {
            Write-Check $false "Python $major.$minor found, need >= 3.11"
            $problems += "Install Python 3.12 with 'Add to PATH' enabled"
        }
    } else {
        Write-Check $false "python command exists but version unparseable: $pyver"
        $problems += "Reinstall Python 3.12"
    }
} catch {
    Write-Check $false "python command not found in PATH"
    $problems += "Install Python 3.12 with 'Add python.exe to PATH' checked. Download: https://www.python.org/downloads/"
}

Write-Header "2. Project directory"
if (Test-Path $ProjectDir) {
    Write-Check $true "Folder exists: $ProjectDir"
    foreach ($f in $ExpectedFiles) {
        $p = Join-Path $ProjectDir $f
        if (Test-Path $p) {
            Write-Check $true $f
        } else {
            Write-Check $false "missing: $f"
            $problems += "File not found: $f"
        }
    }
    foreach ($d in $ExpectedDirs) {
        $p = Join-Path $ProjectDir $d
        if (Test-Path $p -PathType Container) {
            Write-Check $true "subfolder $d/"
        } else {
            Write-Check $false "missing folder: $d/"
            $problems += "Folder not found: $d/"
        }
    }
} else {
    Write-Check $false "$ProjectDir not found"
    $problems += "Unzip archipelago_cross_model.zip into $ProjectDir"
}

Write-Header "3. Python dependencies"
if ((Test-Path $ProjectDir) -and (Get-Command python -ErrorAction SilentlyContinue)) {
    $deps = @("requests", "yaml", "pandas", "numpy", "sklearn", "scipy", "matplotlib", "seaborn")
    foreach ($d in $deps) {
        $check = & python -c "import $d; print($d.__version__ if hasattr($d, '__version__') else 'ok')" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Check $true "$d ($($check.Trim()))"
        } else {
            Write-Check $false "$d not installed"
            $warnings += "Run: pip install -r requirements.txt (in $ProjectDir)"
        }
    }
} else {
    Write-Host "  Skipped (Python or project dir missing)" -ForegroundColor Yellow
}

Write-Header "4. API key (OPENROUTER_API_KEY)"
$key = $env:OPENROUTER_API_KEY
if (-not $key) {
    $key = [Environment]::GetEnvironmentVariable("OPENROUTER_API_KEY", "User")
    if ($key) {
        Write-Host "  [INFO] Key found in User scope but not in current session" -ForegroundColor Yellow
        Write-Host "         Close and reopen PowerShell, or run:" -ForegroundColor Yellow
        Write-Host "         `$env:OPENROUTER_API_KEY = [Environment]::GetEnvironmentVariable('OPENROUTER_API_KEY','User')" -ForegroundColor Yellow
    }
}
if ($key) {
    if ($key -match "^sk-or-v1-") {
        Write-Check $true "Key set (starts with sk-or-v1-, length=$($key.Length))"
    } else {
        Write-Check $false "Key set but does not start with sk-or-v1-"
        $problems += "OPENROUTER_API_KEY value looks wrong; regenerate at https://openrouter.ai/settings/keys"
    }
} else {
    Write-Check $false "OPENROUTER_API_KEY not set in current session or User scope"
    $problems += "Set the key. Temporary: `$env:OPENROUTER_API_KEY = 'sk-or-v1-...'. Permanent: [Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY','sk-or-v1-...','User')"
}

Write-Header "5. OpenRouter reachability"
if ($key) {
    try {
        $headers = @{ "Authorization" = "Bearer $key" }
        $resp = Invoke-WebRequest -Uri "https://openrouter.ai/api/v1/models" -Headers $headers -TimeoutSec 30 -UseBasicParsing
        if ($resp.StatusCode -eq 200) {
            $body = $resp.Content | ConvertFrom-Json
            $count = $body.data.Count
            Write-Check $true "OpenRouter responded with $count models in catalog"

            # Verify config models exist - parse the ACTUAL config.yaml via Python
            $configPath = Join-Path $ProjectDir "config.yaml"
            if (Test-Path $configPath) {
                $pyScript = @"
import yaml, json, sys
with open(r'$configPath', 'r', encoding='utf-8') as f:
    cfg = yaml.safe_load(f)
wanted = []
for m in cfg.get('models', []):
    if m.get('id'): wanted.append(m['id'])
    if m.get('fallback_id'): wanted.append(m['fallback_id'])
print(json.dumps(wanted))
"@
                try {
                    $wantedJson = & python -c $pyScript 2>&1
                    if ($LASTEXITCODE -ne 0) { throw "python parse failed: $wantedJson" }
                    $wanted = $wantedJson | ConvertFrom-Json
                } catch {
                    Write-Host "  [WARN] Could not parse config.yaml ($($_.Exception.Message)), skipping model check" -ForegroundColor Yellow
                    $warnings += "Could not parse config.yaml to check model IDs"
                    $wanted = @()
                }
                if ($wanted.Count -gt 0) {
                    $ids = $body.data | ForEach-Object { $_.id }
                    $idSet = @{}
                    foreach ($id in $ids) { $idSet[$id] = $true }
                    Write-Host "  Model availability check (config IDs vs OpenRouter catalog):" -ForegroundColor Cyan
                    $missing = @()
                    foreach ($w in $wanted) {
                        if ($idSet.ContainsKey($w)) {
                            Write-Host "    [OK] $w" -ForegroundColor Green
                        } else {
                            Write-Host "    [MISSING] $w" -ForegroundColor Yellow
                            $missing += $w
                        }
                    }
                    if ($missing.Count -gt 0) {
                        $warnings += "Some model IDs missing from catalog. Open https://openrouter.ai/models, find current slugs, update config.yaml. Missing: $($missing -join ', ')"
                    }
                }
            }
        } else {
            Write-Check $false "OpenRouter HTTP $($resp.StatusCode)"
            $problems += "OpenRouter API call returned HTTP $($resp.StatusCode)"
        }
    } catch {
        Write-Check $false "Network call failed: $($_.Exception.Message)"
        $problems += "Cannot reach https://openrouter.ai/api/v1/models. Check internet/proxy/VPN."
    }
} else {
    Write-Host "  Skipped (no API key)" -ForegroundColor Yellow
}

Write-Header "6. Disk space"
try {
    $drive = (Get-Item $ProjectDir -ErrorAction SilentlyContinue).PSDrive
    if (-not $drive) { $drive = (Get-PSDrive -Name C) }
    $freeGB = [math]::Round($drive.Free / 1GB, 1)
    if ($freeGB -ge 1) {
        Write-Check $true "Drive $($drive.Name): has $freeGB GB free (need ~50 MB for outputs)"
    } else {
        Write-Check $false "Only $freeGB GB free"
        $warnings += "Low disk space"
    }
} catch {
    Write-Host "  Could not determine free space" -ForegroundColor Yellow
}

Write-Header "Summary"
if ($problems.Count -eq 0 -and $warnings.Count -eq 0) {
    Write-Host "All checks passed. You can run .\run_all.ps1 next." -ForegroundColor Green
    exit 0
} else {
    if ($problems.Count -gt 0) {
        Write-Host ""
        Write-Host "Problems (must fix before running):" -ForegroundColor Red
        $problems | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    }
    if ($warnings.Count -gt 0) {
        Write-Host ""
        Write-Host "Warnings (should review):" -ForegroundColor Yellow
        $warnings | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
    }
    if ($problems.Count -gt 0) { exit 1 } else { exit 0 }
}
