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

function Get-ProjectRootPath([string]$ProjectRoot) {
    try {
        return (Resolve-Path $ProjectRoot).Path
    }
    catch {
        return $ProjectRoot
    }
}

function Test-IsConsumptionApiProcess([object]$Process, [string]$ProjectRoot) {
    if (-not $Process) { return $false }

    $root = Get-ProjectRootPath $ProjectRoot
    $cmd = [string]$Process.CommandLine
    $exe = [string]$Process.ExecutablePath
    if ($cmd -match '(?i)-m\s+consumption\b') {
        if ($cmd -like "*$root*" -or $exe -like "*$root*") { return $true }
    }
    $venvPython = Join-Path $root '.venv\Scripts\python.exe'
    if ($exe -and (Test-Path $venvPython)) {
        try {
            $sameExe = [string]::Equals(
                (Resolve-Path $exe -ErrorAction Stop).Path,
                (Resolve-Path $venvPython -ErrorAction Stop).Path,
                [StringComparison]::OrdinalIgnoreCase)
            if ($sameExe -and $cmd -match '(?i)-m\s+consumption\b') { return $true }
        }
        catch {
            return $false
        }
    }
    return $false
}

function Get-ConsumptionApiProcessIds([string]$ProjectRoot, [int]$Port) {
    $pids = [System.Collections.Generic.HashSet[int]]::new()
    $pythonNames = @('python.exe', 'python3.exe', 'pythonw.exe', 'python3w.exe')

    foreach ($proc in Get-CimInstance Win32_Process -ErrorAction SilentlyContinue) {
        if ($pythonNames -notcontains $proc.Name) { continue }
        if (-not (Test-IsConsumptionApiProcess $proc $ProjectRoot)) { continue }
        $pids.Add([int]$proc.ProcessId) | Out-Null
    }

    try {
        $listeners = @(Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction Stop)
        foreach ($conn in $listeners) {
            $processId = [int]$conn.OwningProcess
            if ($pids.Contains($processId)) { continue }
            $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $processId" -ErrorAction SilentlyContinue
            if (Test-IsConsumptionApiProcess $proc $ProjectRoot) {
                $pids.Add($processId) | Out-Null
            }
        }
    }
    catch {
        # Get-NetTCPConnection may be unavailable; command-line detection above is enough.
    }

    return @($pids)
}

function Stop-PreviousConsumptionSessions([string]$ProjectRoot, [int]$Port) {
    $pids = Get-ConsumptionApiProcessIds $ProjectRoot $Port
    if ($pids.Count -eq 0) {
        Write-Log 'No previous ConsumptionMonitor API processes found'
        return
    }

    foreach ($processId in $pids) {
        Write-Log "Stopping previous API process PID $processId"
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }

    $deadline = (Get-Date).AddSeconds(5)
    while ((Get-Date) -lt $deadline) {
        if (-not (Test-TcpPort '127.0.0.1' $Port 300)) { break }
        Start-Sleep -Milliseconds 200
    }

    if (Test-TcpPort '127.0.0.1' $Port 300) {
        Write-Log "WARNING: port $Port still in use after stopping $($pids.Count) previous process(es)"
    }
    else {
        Write-Log "Port $Port released after stopping $($pids.Count) previous process(es)"
    }
}

function Write-RecentStartupDiagnostics([string]$ProjectRoot) {
    $patterns = 'ERROR:|WARNING:|exited before|did not start'
    foreach ($name in @('launcher.log', 'api.log', 'api.stderr.log')) {
        $logPath = Join-Path $ProjectRoot "data\$name"
        if (-not (Test-Path $logPath)) { continue }

        $issues = @(Get-Content $logPath -Tail 80 -Encoding UTF8 -ErrorAction SilentlyContinue |
            Where-Object {
                $_ -match $patterns -and
                $_ -notmatch '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}   ' -and
                $_ -notmatch 'Recent issues from'
            } |
            Select-Object -Last 5)
        if ($issues.Count -eq 0) { continue }

        Write-Log "Recent issues from ${name}:"
        foreach ($line in $issues) {
            Write-Log "  $line"
        }
    }
}

function Get-ApiLogTail([string]$ProjectRoot, [int]$Lines = 6) {
    $chunks = @()
    foreach ($name in @('api.log', 'api.stderr.log')) {
        $logPath = Join-Path $ProjectRoot "data\$name"
        if (-not (Test-Path $logPath)) { continue }
        $tail = @(Get-Content $logPath -Tail $Lines -Encoding UTF8 -ErrorAction SilentlyContinue)
        if ($tail.Count -eq 0) { continue }
        $chunks += "${name}: $($tail -join ' | ')"
    }
    if ($chunks.Count -eq 0) { return 'No API log output yet.' }
    return ($chunks -join ' ')
}

function Format-ExitCode([object]$ExitCode) {
    if ($null -eq $ExitCode) { return 'unknown' }
    return [string]$ExitCode
}

function Wait-ApiReady([string]$TargetHost, [int]$Port, [System.Diagnostics.Process]$Process, [int]$TimeoutSeconds = 30) {
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if ($Process.HasExited) {
            Write-Log "API process exited before port $Port was ready (exit $(Format-ExitCode $Process.ExitCode))"
            return $false
        }
        if (Test-TcpPort $TargetHost $Port) {
            if ($Process.HasExited) {
                Write-Log "Port $Port is open but our API process already exited (exit $(Format-ExitCode $Process.ExitCode))"
                return $false
            }
            return $true
        }
        Start-Sleep -Milliseconds 500
    }
    return $false
}

trap {
    Exit-WithError $_.Exception.Message
}
