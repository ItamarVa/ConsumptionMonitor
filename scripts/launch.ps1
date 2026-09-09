# Sets up the virtual environment if needed, runs the self-check, then starts the API.
# The bootstrap itself lives in scripts/env.ps1, shared with set-credentials.ps1.

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'launcher-common.ps1')

$root = $script:LauncherRoot
Set-Location $root
. (Join-Path $PSScriptRoot 'env.ps1')

Write-Log 'launch.ps1 started'

$selfChecks = @(
    'tests\test_db_readings.py',
    'tests\test_reading_log.py',
    'tests\test_jobs.py',
    'tests\test_source_parsing.py',
    'tests\test_source_session.py',
    'tests\test_api_contract.py'
)

try {
    $python = Initialize-Venv $root 3 70

    $phaseStart = 72
    $phaseSpan = [math]::Max(1, [int](24 / $selfChecks.Count))
    $i = 0
    foreach ($check in $selfChecks) {
        $pct = [math]::Min(96, $phaseStart + ($i * $phaseSpan))
        Show-Phase $pct "Running $(Split-Path $check -Leaf)"
        & $python (Join-Path $root $check)
        if ($LASTEXITCODE -ne 0) { throw "Self-check failed: $check. The API was not started." }
        $i++
    }

    & $python -c "from consumption import config; raise SystemExit(0 if config.credentials_present() else 1)"
    if ($LASTEXITCODE -ne 0) {
        Write-Host ''
        Write-Host 'No mycitygrid credentials are stored yet. Close this window and double-click'
        Write-Host 'set-credentials.bat to enter them - until then the API serves an empty database.' -ForegroundColor Yellow
    }

    Show-Phase 100 'Starting API'
    Write-Progress -Activity 'ConsumptionMonitor' -Completed

    $hostAddr = (& $python -c "from consumption import config; print(config.HOST)").Trim()
    $port = [int](& $python -c "from consumption import config; print(config.PORT)")

    $api = Start-Process -FilePath $python -ArgumentList '-m', 'consumption' -PassThru -NoNewWindow -WorkingDirectory $root
    Write-Log "Started API process PID $($api.Id) on ${hostAddr}:$port"

    if (-not (Wait-ApiReady $hostAddr $port $api 30)) {
        if (-not $api.HasExited) {
            Stop-Process -Id $api.Id -Force -ErrorAction SilentlyContinue
        }
        Exit-WithError "The API did not start listening on http://${hostAddr}:$port within 30 seconds."
    }

    Write-Log "API is listening on http://${hostAddr}:$port"
    $api.WaitForExit()
    if ($api.ExitCode -ne 0) {
        Exit-WithError "The API stopped with exit code $($api.ExitCode)."
    }
}
catch {
    Exit-WithError $_.Exception.Message
}
