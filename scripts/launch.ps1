# Sets up the virtual environment if needed, runs the self-check, then starts the API.
# The bootstrap itself lives in scripts/env.ps1, shared with set-credentials.ps1.

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
. (Join-Path $PSScriptRoot 'env.ps1')

try {
    $python = Initialize-Venv $root 3 78

    Show-Phase 82 'Running self-check'
    & $python (Join-Path $root 'tests\test_aggregation.py')
    if ($LASTEXITCODE -ne 0) { throw 'Self-check failed. The API was not started.' }

    Show-Phase 86 'Checking the portal parser'
    & $python (Join-Path $root 'tests\test_source_parsing.py')
    if ($LASTEXITCODE -ne 0) { throw 'Self-check failed. The API was not started.' }

    Show-Phase 92 'Checking the portal session'
    & $python (Join-Path $root 'tests\test_source_session.py')
    if ($LASTEXITCODE -ne 0) { throw 'Self-check failed. The API was not started.' }

    # Asks the app itself rather than looking for a file, so an environment override counts.
    & $python -c "from consumption import config; raise SystemExit(0 if config.credentials_present() else 1)"
    if ($LASTEXITCODE -ne 0) {
        Write-Host ''
        Write-Host 'No mycitygrid credentials are stored yet. Close this window and double-click'
        Write-Host 'set-credentials.bat to enter them - until then the API serves an empty database.' -ForegroundColor Yellow
    }

    Show-Phase 100 'Starting API'
    Write-Progress -Activity 'ConsumptionMonitor' -Completed
    & $python -m consumption
}
catch {
    Write-Progress -Activity 'ConsumptionMonitor' -Completed
    Write-Host ''
    Write-Host 'Startup failed:' -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ''
    Write-Host 'What to do: read the line above, fix it, then double-click run.bat again.'
    Read-Host 'Press Enter to close'
    exit 1
}
