#!/usr/bin/env pwsh
# H-HE01: PreToolUse (Bash|PowerShell) — Tool Rate Limiter v2 (per-turn + session ceiling)
#
# Maintains two independent counters per session:
#   1. Per-turn counter  — resets at the start of every prompt (via H-HE01-RESET hook)
#   2. Session counter   — cumulative for the entire chat session; never resets
#
# Two independent AskUserQuestion trigger paths:
#   Path A (per-turn limit, default 150):
#     Block + ask: A) Extend this turn by 50  B) End this response
#   Path B (session ceiling, default 1000):
#     Block + ask: A) Extend session by 500  B) Remove ceiling  C) End conversation
#
# Config files (Claude writes these to extend or cancel limits at runtime):
#   cc00-tool-limit-turn-<id>.txt    — per-turn cap override (deleted on each new prompt)
#   cc00-tool-limit-session-<id>.txt — session ceiling override (persists for whole session)
#
# Reference: core-component-00/harness-engineering/implementations/tool_registry.py

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$sessionId = $data.session_id
if (-not $sessionId) { exit 0 }

$safeId = $sessionId -replace '[^a-zA-Z0-9]', '-'
$base   = $env:TEMP

# --- File paths ---
$turnCounterFile    = Join-Path $base "cc00-tool-counter-turn-$safeId.txt"
$turnLimitFile      = Join-Path $base "cc00-tool-limit-turn-$safeId.txt"
$sessionCounterFile = Join-Path $base "cc00-tool-counter-session-$safeId.txt"
$sessionLimitFile   = Join-Path $base "cc00-tool-limit-session-$safeId.txt"

# --- Read limits ---
$defaultTurnLimit    = 150
$defaultSessionLimit = 1000

$maxTurnCalls = $defaultTurnLimit
if (Test-Path $turnLimitFile) {
    $raw = Get-Content $turnLimitFile -Raw -ErrorAction SilentlyContinue
    $parsed = 0
    if ($raw -and [int]::TryParse($raw.Trim(), [ref]$parsed) -and $parsed -gt 0) {
        $maxTurnCalls = $parsed
    }
}

$maxSessionCalls = $defaultSessionLimit
if (Test-Path $sessionLimitFile) {
    $raw = Get-Content $sessionLimitFile -Raw -ErrorAction SilentlyContinue
    $parsed = 0
    if ($raw -and [int]::TryParse($raw.Trim(), [ref]$parsed) -and $parsed -gt 0) {
        $maxSessionCalls = $parsed
    }
}

# --- Increment counters ---
$turnCount = 0
if (Test-Path $turnCounterFile) {
    $raw = Get-Content $turnCounterFile -Raw -ErrorAction SilentlyContinue
    if ($raw) { $turnCount = [int]$raw.Trim() }
}
$turnCount++
Set-Content $turnCounterFile $turnCount -NoNewline

$sessionCount = 0
if (Test-Path $sessionCounterFile) {
    $raw = Get-Content $sessionCounterFile -Raw -ErrorAction SilentlyContinue
    if ($raw) { $sessionCount = [int]$raw.Trim() }
}
$sessionCount++
Set-Content $sessionCounterFile $sessionCount -NoNewline

# --- Path A: Per-turn limit check ---
if ($turnCount -gt $maxTurnCalls) {
    $newTurnLimit     = $maxTurnCalls + 100
    $turnLimitPath    = $turnLimitFile

    $additionalContext = @"
[TOOL RATE LIMITER — H-HE01 PATH A] Per-turn tool-call limit reached: $turnCount / $maxTurnCalls calls this prompt.

MANDATORY: Use the AskUserQuestion tool to ask the user:

Question: "Per-turn tool-call limit reached ($turnCount / $maxTurnCalls this prompt). How would you like to proceed?"

Options:
  A) "Extend this turn by 100" — raise the per-turn cap to $newTurnLimit for the remainder of this response only.
     Action: use the Write tool to write "$newTurnLimit" to: $turnLimitPath
     Then retry the blocked command.

  B) "Set a custom limit" — raise the per-turn cap to a number of the user's choosing.
     Action: ask the user "How many additional tool calls would you like to allow this turn?" then
     add their answer to $maxTurnCalls and use the Write tool to write the result to: $turnLimitPath
     Then retry the blocked command.

  C) "End this response" — wrap up the current response and stop.
     Action: summarise progress and do not retry the blocked command.

NOTE: Any extension granted here is automatically removed at the start of the next prompt.
Reference: core-component-00/harness-engineering/implementations/tool_registry.py
"@

    $output = [ordered]@{
        hookSpecificOutput = [ordered]@{
            hookEventName            = "PreToolUse"
            permissionDecision       = "deny"
            permissionDecisionReason = "[TOOL RATE LIMITER — H-HE01] Per-turn limit reached: $turnCount / $maxTurnCalls. See additionalContext for AskUserQuestion instructions."
            additionalContext        = $additionalContext
        }
    } | ConvertTo-Json -Depth 5 -Compress

    Write-Output $output
    exit 0
}

# --- Path B: Session ceiling check (only if Path A passed) ---
if ($sessionCount -gt $maxSessionCalls) {
    $newSessionLimit  = $maxSessionCalls + 500
    $sessionLimitPath = $sessionLimitFile

    $additionalContext = @"
[TOOL RATE LIMITER — H-HE01 PATH B] Session tool-call ceiling reached: $sessionCount / $maxSessionCalls total this session.

MANDATORY: Use the AskUserQuestion tool to ask the user:

Question: "Session tool-call ceiling reached ($sessionCount / $maxSessionCalls total). How would you like to proceed?"

Options:
  A) "Extend session by 500" — raise the session ceiling to $newSessionLimit.
     Action: use the Write tool to write "$newSessionLimit" to: $sessionLimitPath
     Then retry the blocked command.

  B) "Set a custom session ceiling" — raise the session ceiling to a number of the user's choosing.
     Action: ask the user "How many additional session tool calls would you like to allow?" then
     add their answer to $maxSessionCalls and use the Write tool to write the result to: $sessionLimitPath
     Then retry the blocked command.

  C) "Remove session ceiling" — no ceiling for the rest of this session.
     Action: use the Write tool to write "999999" to: $sessionLimitPath
     Then retry the blocked command.

  D) "End conversation" — wrap up and stop.
     Action: summarise progress and do not retry the blocked command.

Reference: core-component-00/harness-engineering/implementations/tool_registry.py
"@

    $output = [ordered]@{
        hookSpecificOutput = [ordered]@{
            hookEventName            = "PreToolUse"
            permissionDecision       = "deny"
            permissionDecisionReason = "[TOOL RATE LIMITER — H-HE01] Session ceiling reached: $sessionCount / $maxSessionCalls. See additionalContext for AskUserQuestion instructions."
            additionalContext        = $additionalContext
        }
    } | ConvertTo-Json -Depth 5 -Compress

    Write-Output $output
    exit 0
}

# Under both limits — allow through
exit 0
