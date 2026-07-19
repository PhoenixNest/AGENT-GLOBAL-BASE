#!/usr/bin/env pwsh
# H-P01 enforcement — PreToolUse: denies any tool other than AskUserQuestion while a
# prompt-optimizer confirmation is pending for this session. Real enforcement companion
# to prompt-optimizer.ps1, which only injects advisory additionalContext on its own.

param()

$rawInput = [Console]::In.ReadToEnd()
try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

if ($data.tool_name -eq 'AskUserQuestion') { exit 0 }

$sessionId = $data.session_id
if (-not $sessionId) { exit 0 }

$repoRoot = git rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0) { exit 0 }

$markerPath = Join-Path $repoRoot ".claude/hooks/.state/h-p01-pending-$sessionId.json"
if (-not (Test-Path $markerPath)) { exit 0 }

# Stale-marker fail-safe: if the marker is older than 15 minutes, the confirmation step
# never completed for some other reason (e.g. the turn ended without one). Clear it and
# stop blocking rather than deadlock the session. This does not select an answer for the
# user — it only restores pre-gate behavior.
try {
    $marker = Get-Content $markerPath -Raw | ConvertFrom-Json
    $age = (Get-Date) - [DateTime]::Parse($marker.ts)
} catch {
    Remove-Item $markerPath -Force -ErrorAction SilentlyContinue
    exit 0
}

if ($age.TotalSeconds -gt 900) {
    Remove-Item $markerPath -Force -ErrorAction SilentlyContinue
    exit 0
}

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName             = "PreToolUse"
        permissionDecision        = "deny"
        permissionDecisionReason  = "H-P01 confirmation pending — answer the prompt-optimization question (AskUserQuestion) before using other tools."
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
