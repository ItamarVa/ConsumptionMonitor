# Sets up the virtual environment if needed, then starts the API.
# Named phases are mapped to percentage ranges because pip gives no usable progress signal.

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$venv = Join-Path $root '.venv'
$python = Join-Path $venv 'Scripts\python.exe'
$stamp = Join-Path $venv 'requirements.stamp'

function Show-Phase([int]$Percent, [string]$Text) {
    Write-Progress -Activity 'ConsumptionMonitor' -Status "$Percent% - $Text" -PercentComplete $Percent
}

# Animates the bar across a range while a background job runs, so the window never sits still.
function Wait-WithProgress([System.Management.Automation.Job]$Job, [int]$From, [int]$To, [string]$Text) {
    $tick = 0
    while ($Job.State -eq 'Running') {
        $tick++
        $percent = $From + [math]::Min($To - $From - 1, [int](($To - $From) * (1 - [math]::Exp(-$tick / 25.0))))
        Show-Phase $percent $Text
        Start-Sleep -Milliseconds 400
    }
    Receive-Job $Job -ErrorAction Continue | Out-Null
    $failed = $Job.State -eq 'Failed'
    Remove-Job $Job -Force
    if ($failed) { throw "$Text failed" }
    Show-Phase $To $Text
}

try {
    Show-Phase 3 'Checking Python'
    $base = if (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { 'python' }
    & $base --version | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Python 3.11 or newer is required. Install it from python.org, then run this again.' }

    if (-not (Test-Path $python)) {
        Show-Phase 10 'Creating virtual environment'
        & $base -m venv $venv
        if (-not (Test-Path $python)) { throw 'Could not create the .venv folder' }
    }

    $reqHash = (Get-FileHash (Join-Path $root 'requirements.txt') -Algorithm SHA256).Hash
    if (-not (Test-Path $stamp) -or (Get-Content $stamp -Raw).Trim() -ne $reqHash) {
        Show-Phase 25 'Installing dependencies'
        $job = Start-Job -ScriptBlock {
            param($py, $req)
            & $py -m pip install --disable-pip-version-check --quiet --upgrade pip
            & $py -m pip install --disable-pip-version-check --quiet -r $req
            if ($LASTEXITCODE -ne 0) { throw 'pip install failed' }
        } -ArgumentList $python, (Join-Path $root 'requirements.txt')
        Wait-WithProgress $job 25 78 'Installing dependencies'
        Set-Content -Path $stamp -Value $reqHash -NoNewline
    }
    else {
        Show-Phase 78 'Dependencies already installed'
    }

    Show-Phase 85 'Running self-check'
    & $python (Join-Path $root 'tests\test_aggregation.py')
    if ($LASTEXITCODE -ne 0) { throw 'Self-check failed. The API was not started.' }

    if (-not (Test-Path (Join-Path $root '.env'))) {
        Write-Host ''
        Write-Host 'No .env file found. Copy .env.example to .env and fill in your mycitygrid'
        Write-Host 'credentials - until then the API serves an empty database.' -ForegroundColor Yellow
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
