# Shared launcher error handling and logging for ConsumptionMonitor .bat entry points.
# Dot-source at the top of launch.ps1, set-credentials.ps1, and test-connection.ps1.
# Exit-WithError always exits 1 so the .bat layer can catch any non-zero code.

$script:LauncherRoot = Split-Path -Parent $PSScriptRoot
$script:LauncherLogPath = Join-Path $script:LauncherRoot 'data\launcher.log'

function Write-Log([string]$Message) {
    $dir = Split-Path $script:LauncherLogPath -Parent
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Message"
    Add-Content -Path $script:LauncherLogPath -Value $line -Encoding UTF8
}

function Exit-WithError([string]$Message) {
    Write-Log "ERROR: $Message"
    Write-Progress -Activity 'ConsumptionMonitor' -Completed -ErrorAction SilentlyContinue
    Write-Host ''
    Write-Host $Message -ForegroundColor Red
    Write-Host ''
    Write-Host "Details are also in: $script:LauncherLogPath"
    exit 1
}

function Test-TcpPort([string]$TargetHost, [int]$Port, [int]$TimeoutMs = 1000) {
    $tcp = $null
    try {
        $tcp = [System.Net.Sockets.TcpClient]::new()
        $connect = $tcp.BeginConnect($TargetHost, $Port, $null, $null)
        if (-not $connect.AsyncWaitHandle.WaitOne($TimeoutMs)) { return $false }
        $tcp.EndConnect($connect)
        return $tcp.Connected
    }
    catch {
        return $false
    }
    finally {
        if ($tcp) { $tcp.Dispose() }
    }
}

function Wait-ApiReady([string]$TargetHost, [int]$Port, [System.Diagnostics.Process]$Process, [int]$TimeoutSeconds = 30) {
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if ($Process.HasExited) {
            Write-Log "API process exited before port $Port was ready (exit $($Process.ExitCode))"
            return $false
        }
        if (Test-TcpPort $TargetHost $Port) { return $true }
        Start-Sleep -Milliseconds 500
    }
    return $false
}

trap {
    Exit-WithError $_.Exception.Message
}
