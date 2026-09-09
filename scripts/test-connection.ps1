# First-contact check: signs in to mycitygrid once and reports what the portal returns.
# The virtual environment bootstrap is the shared one in scripts/env.ps1. The work itself
# runs in a background job so the progress bar keeps moving while the portal is answering;
# the job's output is printed once it finishes. scripts/connection_report.py does the work.

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
. (Join-Path $PSScriptRoot 'env.ps1')

try {
    $python = Initialize-Venv $root 3 40

    Show-Phase 45 'Talking to the portal'
    $job = Start-Job -ScriptBlock {
        param($py, $script)
        $env:PYTHONUTF8 = '1'
        & $py $script 2>&1
    } -ArgumentList $python, (Join-Path $root 'scripts\connection_report.py')

    $tick = 0
    while ($job.State -eq 'Running') {
        $tick++
        $percent = 45 + [math]::Min(49, [int](50 * (1 - [math]::Exp(-$tick / 20.0))))
        Show-Phase $percent 'Talking to the portal'
        Start-Sleep -Milliseconds 400
    }
    $output = Receive-Job $job -ErrorAction Continue
    Remove-Job $job -Force
    Show-Phase 100 'Done'
    Write-Progress -Activity 'ConsumptionMonitor' -Completed

    Write-Host ''
    $output | ForEach-Object { Write-Host $_ }
    Write-Host ''
    Write-Host 'Open the report file above and send it on if the parser did not understand'
    Write-Host 'the responses - it contains everything needed to fix that, with the password'
    Write-Host 'and the tokens removed.'
    Read-Host 'Press Enter to close'
}
catch {
    Write-Progress -Activity 'ConsumptionMonitor' -Completed
    Write-Host ''
    Write-Host 'The connection check could not run:' -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ''
    Write-Host 'What to do: if it mentions credentials, double-click set-credentials.bat and'
    Write-Host 'enter them again. Otherwise check that this PC is online, then try again.'
    Read-Host 'Press Enter to close'
    exit 1
}
