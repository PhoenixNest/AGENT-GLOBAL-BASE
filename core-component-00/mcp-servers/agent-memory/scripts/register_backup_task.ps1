<#
.SYNOPSIS
    Phase 5 DR backup — Windows Task Scheduler registration for the daily
    agent-memory JSONL log snapshot.

.DESCRIPTION
    STATUS: implemented, INACTIVE by default. Running this script with no
    switches performs a DRY RUN only — it prints the task definition it would
    register and registers nothing. Pass -Activate to actually create the
    scheduled task. This split is deliberate: CEO approval (2026-08-08) covers
    writing this script, not activating it — see
    core-component-00/telescope/2026-07-10-agent-memory-architecture/supporting/12-dr-backup-design.md.
    Do not pass -Activate without a fresh, explicit authorization to activate.

.PARAMETER Activate
    Actually register the scheduled task. Omit to dry-run only.

.PARAMETER TaskName
    Scheduled task name. Default: "CC00-AgentMemory-DailyBackup".

.PARAMETER Time
    Daily run time, 24h HH:mm. Default: "03:00".
#>
param(
    [switch]$Activate,
    [string]$TaskName = "CC00-AgentMemory-DailyBackup",
    [string]$Time = "03:00"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AgentMemoryDir = Split-Path -Parent $ScriptDir
$McpServersDir = Split-Path -Parent $AgentMemoryDir
$BackupScript = Join-Path $ScriptDir "backup_memory_log.py"
$PythonExe = Join-Path $McpServersDir ".venv\Scripts\python.exe"

Write-Host "Task name:    $TaskName"
Write-Host "Trigger:      Daily at $Time"
Write-Host "Action:       `"$PythonExe`" `"$BackupScript`""
Write-Host ""

if (-not $Activate) {
    Write-Host "DRY RUN — no task was registered. Pass -Activate to register it for real."
    exit 0
}

$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$BackupScript`""
$Trigger = New-ScheduledTaskTrigger -Daily -At $Time
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings `
    -Description "CC-00 agent-memory JSONL log daily snapshot (Phase 5 DR backup)."

Write-Host "Registered scheduled task '$TaskName'."
