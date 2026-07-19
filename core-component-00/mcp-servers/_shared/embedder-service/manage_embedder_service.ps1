<#
.SYNOPSIS
    Manual supervisor for the shared embedder-service (start/stop/status/cleanup).

.DESCRIPTION
    The service is normally self-launched by the first MCP server consumer
    that needs it (embedder_client.ensure_service_running(), atomic-lock
    guarded) and self-shuts-down after an idle timeout — this script is not
    required for normal operation. It exists per implementation-plan.md §2.1
    for manual control and, in particular, orphan cleanup: this session's own
    repeated experience with orphaned agent-memory MCP processes was the
    explicit reason a supervisor script was scoped into this plan rather than
    relying on self-management alone.

.PARAMETER Action
    start | stop | status | cleanup

.EXAMPLE
    .\manage_embedder_service.ps1 -Action status
    .\manage_embedder_service.ps1 -Action start
    .\manage_embedder_service.ps1 -Action stop
    .\manage_embedder_service.ps1 -Action cleanup
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("start", "stop", "status", "cleanup")]
    [string]$Action
)

$ErrorActionPreference = "Stop"

$ServiceDir = $PSScriptRoot
$RunDir = Join-Path $ServiceDir "run"
$PidFile = Join-Path $RunDir "embedder-service.pid"
$LockFile = Join-Path $RunDir "embedder-service.lock"
$ServerScript = Join-Path $ServiceDir "server.py"

$Host_ = if ($env:EMBEDDER_SERVICE_HOST) { $env:EMBEDDER_SERVICE_HOST } else { "127.0.0.1" }
$Port = if ($env:EMBEDDER_SERVICE_PORT) { $env:EMBEDDER_SERVICE_PORT } else { "8791" }
$BaseUrl = "http://${Host_}:${Port}"

function Get-ServiceHealth {
    try {
        return Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get -TimeoutSec 2
    } catch {
        return $null
    }
}

function Get-PidFileInfo {
    if (Test-Path $PidFile) {
        try { return Get-Content $PidFile -Raw | ConvertFrom-Json } catch { return $null }
    }
    return $null
}

switch ($Action) {
    "status" {
        $health = Get-ServiceHealth
        if ($health) {
            Write-Output "RUNNING — pid=$($health.pid) models=$($health.models_loaded -join ',') uptime_s=$($health.uptime_s) idle_timeout_s=$($health.idle_timeout_s)"
        } else {
            $pidInfo = Get-PidFileInfo
            if ($pidInfo) {
                Write-Output "NOT RESPONDING — stale PID file present (pid=$($pidInfo.pid)); run -Action cleanup"
            } else {
                Write-Output "STOPPED"
            }
        }
    }

    "start" {
        $health = Get-ServiceHealth
        if ($health) {
            Write-Output "Already running — pid=$($health.pid)"
            break
        }
        Write-Output "Starting embedder-service ($ServerScript)..."
        $proc = Start-Process -FilePath "python" -ArgumentList "`"$ServerScript`"" `
            -WindowStyle Hidden -PassThru
        $deadline = (Get-Date).AddSeconds(45)
        while ((Get-Date) -lt $deadline) {
            Start-Sleep -Milliseconds 500
            $health = Get-ServiceHealth
            if ($health) {
                Write-Output "Started — pid=$($health.pid) models=$($health.models_loaded -join ',')"
                break
            }
        }
        if (-not $health) {
            Write-Warning "Service did not come up within 45s (launcher pid=$($proc.Id))"
        }
    }

    "stop" {
        $health = Get-ServiceHealth
        if (-not $health) {
            Write-Output "Not running (no response from $BaseUrl/health)"
            break
        }
        $targetPid = $health.pid
        try {
            Invoke-RestMethod -Uri "$BaseUrl/shutdown" -Method Post -TimeoutSec 2 -ContentType "application/json" -Body "{}" | Out-Null
        } catch {
            # Graceful shutdown request may itself race the socket closing — fall through to a hard stop below.
        }
        $deadline = (Get-Date).AddSeconds(10)
        while ((Get-Date) -lt $deadline) {
            Start-Sleep -Milliseconds 300
            if (-not (Get-ServiceHealth)) { break }
        }
        if (Get-ServiceHealth) {
            Write-Warning "Graceful shutdown did not take effect — force-stopping pid=$targetPid"
            Stop-Process -Id $targetPid -Force -Confirm:$false -ErrorAction SilentlyContinue
        }
        Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
        Remove-Item $LockFile -Force -ErrorAction SilentlyContinue
        Write-Output "Stopped"
    }

    "cleanup" {
        # Orphan detection: any python.exe whose command line references this
        # server.py but which (a) has no live /health response tied to its PID,
        # or (b) is not the PID currently on record in the PID file.
        $health = Get-ServiceHealth
        $livePid = if ($health) { [int]$health.pid } else { $null }

        $candidates = Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" |
            Where-Object { $_.CommandLine -and $_.CommandLine -like "*embedder-service*server.py*" }

        $orphanCount = 0
        foreach ($proc in $candidates) {
            if ($livePid -and $proc.ProcessId -eq $livePid) { continue }
            Write-Output "Killing orphaned embedder-service process pid=$($proc.ProcessId)"
            Stop-Process -Id $proc.ProcessId -Force -Confirm:$false -ErrorAction SilentlyContinue
            $orphanCount++
        }

        if (-not $livePid) {
            Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
        }
        Remove-Item $LockFile -Force -ErrorAction SilentlyContinue

        Write-Output "Cleanup complete — $orphanCount orphaned process(es) removed"
    }
}
