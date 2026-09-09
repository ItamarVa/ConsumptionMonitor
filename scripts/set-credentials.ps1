# First-time setup: asks for the mycitygrid credentials and stores them encrypted.
# Creates the virtual environment first if it is missing, using the same shared bootstrap
# as launch.ps1. The prompting and the encryption happen in scripts/set_credentials.py.

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
. (Join-Path $PSScriptRoot 'env.ps1')

try {
    $python = Initialize-Venv $root 5 95
    Show-Phase 100 'Ready'
    Write-Progress -Activity 'ConsumptionMonitor' -Completed

    & $python (Join-Path $root 'scripts\set_credentials.py')
    if ($LASTEXITCODE -ne 0) { throw 'The credentials were not saved.' }
    Write-Host ''
    Read-Host 'Press Enter to close'
}
catch {
    Write-Progress -Activity 'ConsumptionMonitor' -Completed
    Write-Host ''
    Write-Host 'Setup failed:' -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ''
    Write-Host 'What to do: read the line above, fix it, then double-click set-credentials.bat again.'
    Read-Host 'Press Enter to close'
    exit 1
}
