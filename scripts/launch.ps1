# Sets up the virtual environment if needed, starts the API quickly, opens the dashboard,
# then runs self-checks in the background. The bootstrap lives in scripts/env.ps1.

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
    'tests\test_hourly.py',
    'tests\test_api_contract.py'
)

try {
    $python = Initialize-Venv $root 3 25

    $hostAddr = (& $python -c "from consumption import config; print(config.HOST)").Trim()
    $port = [int](& $python -c "from consumption import config; print(config.PORT)")

    Show-Phase 30 'Stopping previous sessions'
    Stop-PreviousConsumptionSessions $root $port
    if (Test-TcpPort $hostAddr $port) {
        Exit-WithError "Port $port is still in use by another program. Close it and run again."
    }

    Write-RecentStartupDiagnostics $root

    & $python -c "from consumption import config; raise SystemExit(0 if config.credentials_present() else 1)"
    if ($LASTEXITCODE -ne 0) {
        Write-Host ''
        Write-Host 'No mycitygrid credentials are stored yet. Close this window and double-click'
        Write-Host 'set-credentials.bat to enter them - until then the API serves an empty database.' -ForegroundColor Yellow
    }

    Show-Phase 55 'Starting API'
    Write-Progress -Activity 'ConsumptionMonitor' -Completed

    $apiLog = Join-Path $root 'data\api.log'
    $apiErrLog = Join-Path $root 'data\api.stderr.log'
    foreach ($logPath in @($apiLog, $apiErrLog)) {
        $logDir = Split-Path $logPath -Parent
        if (-not (Test-Path $logDir)) {
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        }
        if (Test-Path $logPath) {
            Add-Content -Path $logPath -Value "`n--- launch $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ---" -Encoding UTF8
        }
    }

    $api = Start-Process -FilePath $python `
        -ArgumentList '-m', 'consumption' `
        -PassThru -NoNewWindow `
        -WorkingDirectory $root `
        -RedirectStandardOutput $apiLog `
        -RedirectStandardError $apiErrLog
    Write-Log "Started API process PID $($api.Id) on ${hostAddr}:$port (logs: data\api.log)"

    if (-not (Wait-ApiReady $hostAddr $port $api 30)) {
        if (-not $api.HasExited) {
            Stop-Process -Id $api.Id -Force -ErrorAction SilentlyContinue
        }
        $tail = Get-ApiLogTail $root
        Exit-WithError "The API did not start listening on http://${hostAddr}:$port within 30 seconds. $tail"
    }

    Write-Log "API is listening on http://${hostAddr}:$port"
    Show-Phase 85 'Opening dashboard'
    Start-Process "http://127.0.0.1:${port}/ui"

    $selfCheckLog = Join-Path $root 'data\selfcheck.log'
    $checkList = ($selfChecks | ForEach-Object { "'$_'" }) -join ', '
    $bgScript = @"
Set-Location '$root'
`$log = '$selfCheckLog'
`$python = '$python'
`$checks = @($checkList)
`$failed = 0
Add-Content -Path `$log -Value "`n--- self-check $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ---" -Encoding UTF8
foreach (`$check in `$checks) {
    & `$python (Join-Path '$root' `$check) 2>&1 | Out-File -Append -FilePath `$log -Encoding UTF8
    if (`$LASTEXITCODE -ne 0) { `$failed++ }
}
if (`$failed -eq 0) {
    Add-Content -Path `$log -Value 'All self-checks passed' -Encoding UTF8
} else {
    Add-Content -Path `$log -Value "WARNING: `$failed self-check file(s) failed" -Encoding UTF8
}
"@
    Start-Job -ScriptBlock ([scriptblock]::Create($bgScript)) | Out-Null
    Write-Log "Background self-checks started (log: data\selfcheck.log)"

    Show-Phase 100 'Running'
    $api.WaitForExit()
    $exitCode = $api.ExitCode
    if ($null -eq $exitCode -or $exitCode -eq 0) {
        Write-Log "API process ended (exit $(Format-ExitCode $exitCode))"
        exit 0
    }
    $tail = Get-ApiLogTail $root
    Exit-WithError "The API stopped unexpectedly (exit code: $(Format-ExitCode $exitCode)). $tail"
}
catch {
    Exit-WithError $_.Exception.Message
}
