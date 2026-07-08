# Phase 2L · Safe launcher
# Проверяет API key валидность ПЕРЕД запуском долгого процесса.

Write-Host "`n=== Phase 2L Launcher ===" -ForegroundColor Cyan

# 1. Check env var exists
if (-not $env:OPENROUTER_API_KEY) {
    Write-Host "ERROR: `$env:OPENROUTER_API_KEY not set in this window." -ForegroundColor Red
    Write-Host ""
    Write-Host "Fix:" -ForegroundColor Yellow
    Write-Host '  $env:OPENROUTER_API_KEY = "sk-or-v1-..."'
    Write-Host ""
    Write-Host "Or permanent (close+reopen window after):" -ForegroundColor Yellow
    Write-Host '  setx OPENROUTER_API_KEY "sk-or-v1-..."'
    exit 1
}

# 2. Show masked key
$key = $env:OPENROUTER_API_KEY
$mask = $key.Substring(0, [Math]::Min(10, $key.Length)) + "..." + $key.Substring([Math]::Max(0, $key.Length - 4))
Write-Host "API key set: $mask (length: $($key.Length))" -ForegroundColor Green

# 3. Sanity check format
if (-not $key.StartsWith("sk-or-")) {
    Write-Host "WARNING: key does not start with 'sk-or-' - may be wrong format" -ForegroundColor Yellow
}

# 4. Live auth check via OpenRouter
Write-Host "`nChecking auth with OpenRouter..." -ForegroundColor Cyan
try {
    $resp = Invoke-RestMethod -Uri "https://openrouter.ai/api/v1/auth/key" `
        -Headers @{"Authorization" = "Bearer $key"} `
        -ErrorAction Stop
    $usage = if ($resp.data.usage) { [math]::Round($resp.data.usage, 4) } else { 0 }
    $limit = if ($resp.data.limit) { $resp.data.limit } else { "unlimited" }
    $remaining = if ($resp.data.limit_remaining) { [math]::Round($resp.data.limit_remaining, 2) } else { "n/a" }
    Write-Host "OK - account valid" -ForegroundColor Green
    Write-Host "  Label:        $($resp.data.label)"
    Write-Host "  Usage:        `$$usage"
    Write-Host "  Limit:        `$$limit"
    Write-Host "  Remaining:    `$$remaining"
} catch {
    Write-Host "FAIL: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "API key is set but OpenRouter rejected it." -ForegroundColor Yellow
    Write-Host "Get a fresh key: https://openrouter.ai/keys"
    exit 1
}

# 5. Parse args - pass through to run_phase2l.py
$pyArgs = $args
if (-not $pyArgs) {
    $pyArgs = @("--phase", "4", "--workers", "4", "--budget-cap", "195")
}

Write-Host "`nLaunching: python run_phase2l.py $pyArgs" -ForegroundColor Cyan
Write-Host "(Ctrl+C to stop; resume picks up where you stopped)`n"

python run_phase2l.py @pyArgs
