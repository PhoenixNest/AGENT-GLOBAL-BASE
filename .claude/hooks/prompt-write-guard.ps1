#!/usr/bin/env pwsh
# H-P04: PreToolUse (Edit|Write|NotebookEdit) — Prompt Write Guard
# Blocks any file write operation targeting denied paths:
# GEMINI.md, .gemini/**, or any path that matches the settings.json deny rules.
# Enforces CLAUDE.md §1 at the tool-execution layer.

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$filePath = $data.tool_input.file_path
if (-not $filePath) { exit 0 }

$normalizedPath = $filePath -replace '\\', '/'

$deniedPatterns = @(
    @{
        pattern = '(^|/)GEMINI\.md$'
        rule    = 'GEMINI.md is off-limits to Claude Code — CLAUDE.md §1 explicit guardrail'
    },
    @{
        pattern = '(^|/)\.gemini(/|$)'
        rule    = '.gemini/** is explicitly denied in settings.json deny rules — CLAUDE.md §1'
    }
)

$blockedRule = $null
foreach ($d in $deniedPatterns) {
    if ($normalizedPath -match $d.pattern) {
        $blockedRule = $d.rule
        break
    }
}

if (-not $blockedRule) { exit 0 }

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName             = "PreToolUse"
        permissionDecision        = "deny"
        permissionDecisionReason  = "[WRITE GUARD — H-P04] Write blocked to denied path. Path: $filePath | Reason: $blockedRule | Modify CLAUDE.md or .claude/ files instead."
    }
} | ConvertTo-Json -Depth 3 -Compress

Write-Output $output
exit 0
