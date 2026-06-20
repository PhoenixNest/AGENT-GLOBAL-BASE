#!/usr/bin/env pwsh
# H-HE01-RESET: UserPromptSubmit — resets per-turn tool counter and limit for H-HE01
# Fires at the start of every new prompt, ensuring the per-turn tool-call counter
# and any mid-turn extension granted by the user are wiped before the new turn begins.
# The session-level counter and ceiling are NOT touched here.
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

# Reset per-turn counter to 0
Set-Content (Join-Path $base "cc00-tool-counter-turn-$safeId.txt") "0" -NoNewline

# Delete per-turn limit file so any mid-turn extension does not carry over
Remove-Item (Join-Path $base "cc00-tool-limit-turn-$safeId.txt") -ErrorAction SilentlyContinue

exit 0
