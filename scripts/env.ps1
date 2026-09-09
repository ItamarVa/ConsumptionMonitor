# Shared launcher setup: the Python check, the .venv and the pinned dependencies.
# Dot-source it to get Show-Phase, Wait-WithProgress and Initialize-Venv. Both launch.ps1
# and set-credentials.ps1 use it, so the bootstrap exists in exactly one place.
# Named phases are mapped to percentage ranges because pip gives no usable progress signal.

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

# Creates .venv and installs requirements.txt if needed, and returns the path to its python.
# Everything else is piped to Out-Null: only the path may reach the caller.
function Initialize-Venv([string]$Root, [int]$From, [int]$To) {
    $venv = Join-Path $Root '.venv'
    $python = Join-Path $venv 'Scripts\python.exe'
    $stamp = Join-Path $venv 'requirements.stamp'
    $req = Join-Path $Root 'requirements.txt'

    Show-Phase $From 'Checking Python'
    $base = if (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { 'python' }
    & $base --version | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Python 3.11 or newer is required. Install it from python.org, then run this again.' }

    if (-not (Test-Path $python)) {
        Show-Phase ($From + 7) 'Creating virtual environment'
        & $base -m venv $venv | Out-Null
        if (-not (Test-Path $python)) { throw 'Could not create the .venv folder' }
    }

    $reqHash = (Get-FileHash $req -Algorithm SHA256).Hash
    if (-not (Test-Path $stamp) -or (Get-Content $stamp -Raw).Trim() -ne $reqHash) {
        Show-Phase ($From + 22) 'Installing dependencies'
        $job = Start-Job -ScriptBlock {
            param($py, $reqFile)
            & $py -m pip install --disable-pip-version-check --quiet --upgrade pip
            & $py -m pip install --disable-pip-version-check --quiet -r $reqFile
            if ($LASTEXITCODE -ne 0) { throw 'pip install failed' }
        } -ArgumentList $python, $req
        Wait-WithProgress $job ($From + 22) $To 'Installing dependencies'
        Set-Content -Path $stamp -Value $reqHash -NoNewline
    }
    else {
        Show-Phase $To 'Dependencies already installed'
    }
    return $python
}
