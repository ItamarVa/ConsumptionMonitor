# One-time copy of the local SQLite history to the Home Assistant Samba share.
# The add-on imports /share/consumptionmonitor/consumption.sqlite on first start.
# Dot-sources the same launcher helpers as the other .bat entry points.

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'launcher-common.ps1')
. (Join-Path $PSScriptRoot 'env.ps1')

$root = $script:LauncherRoot
Set-Location $root

$shareRoot = '\\homeassistant\share'
$destDir = Join-Path $shareRoot 'consumptionmonitor'
$src = Join-Path $root 'data\consumption.sqlite'
$dest = Join-Path $destDir 'consumption.sqlite'

Write-Log 'copy-db-to-ha.ps1 started'

try {
    Show-Phase 5 'Checking database'
    if (-not (Test-Path $src)) {
        Exit-WithError @(
            'No local database found at data\consumption.sqlite.',
            'Run run.bat at least once so readings are stored, then try again.'
        ) -join ' '
    }

    $sizeMb = [math]::Round((Get-Item $src).Length / 1MB, 1)
    Write-Log "Source database: $src ($sizeMb MB)"

    Show-Phase 20 'Checking Samba share'
    $shareJob = Start-Job -ScriptBlock { param($Path) Test-Path -LiteralPath $Path } -ArgumentList $shareRoot
    $shareReady = $shareJob | Wait-Job -Timeout 8
    $shareReachable = $false
    if ($shareReady) {
        $shareReachable = [bool](Receive-Job $shareJob)
    }
    Remove-Job $shareJob -Force -ErrorAction SilentlyContinue
    if (-not $shareReachable) {
        Exit-WithError @(
            "Cannot reach $shareRoot within 8 seconds.",
            'Install the official Samba share add-on in Home Assistant,',
            'confirm the share opens in File Explorer, then run this again.'
        ) -join ' '
    }

    Show-Phase 35 'Preparing folder'
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        Write-Log "Created $destDir"
    }

    Show-Phase 45 'Copying database'
    $job = Start-Job -ScriptBlock {
        param($Source, $Destination)
        Copy-Item -LiteralPath $Source -Destination $Destination -Force
    } -ArgumentList $src, $dest

    $tick = 0
    while ($job.State -eq 'Running') {
        $tick++
        $percent = 45 + [math]::Min(49, [int](50 * (1 - [math]::Exp(-$tick / 18.0))))
        Show-Phase $percent 'Copying database'
        Start-Sleep -Milliseconds 350
    }

    $copyError = Receive-Job $job -ErrorAction Continue
    if ($job.State -eq 'Failed') {
        $detail = if ($copyError) { ($copyError | Out-String).Trim() } else { 'Copy job failed.' }
        Remove-Job $job -Force -ErrorAction SilentlyContinue
        throw $detail
    }
    Remove-Job $job -Force

    if (-not (Test-Path $dest)) {
        throw "Copy finished but $dest was not found."
    }

    Show-Phase 100 'Done'
    Write-Progress -Activity 'ConsumptionMonitor' -Completed

    Write-Log "Copied database to $dest"
    Write-Host ''
    Write-Host 'Database copied to Home Assistant.' -ForegroundColor Green
    Write-Host "  $dest"
    Write-Host ''
    Write-Host 'Start or restart the ConsumptionMonitor add-on so it adopts this history.'
    Write-Host 'If the add-on already has a database in /data, remove it first or the copy is skipped.'
}
catch {
    Exit-WithError $_.Exception.Message
}
