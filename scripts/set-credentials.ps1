# First-time setup: asks for the mycitygrid credentials and stores them encrypted.
# Creates the virtual environment first if it is missing, using the same shared bootstrap
# as launch.ps1. The prompting and the encryption happen in scripts/set_credentials.py.

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'launcher-common.ps1')

$root = $script:LauncherRoot
Set-Location $root
. (Join-Path $PSScriptRoot 'env.ps1')

Write-Log 'set-credentials.ps1 started'

try {
    $python = Initialize-Venv $root 5 95
    Show-Phase 100 'Ready'
    Write-Progress -Activity 'ConsumptionMonitor' -Completed

    & $python (Join-Path $root 'scripts\set_credentials.py')
    if ($LASTEXITCODE -ne 0) { throw 'The credentials were not saved.' }

    Write-Log 'Credentials saved successfully'
    Write-Host ''
    Write-Host 'Credentials saved successfully.' -ForegroundColor Green
}
catch {
    Exit-WithError $_.Exception.Message
}
