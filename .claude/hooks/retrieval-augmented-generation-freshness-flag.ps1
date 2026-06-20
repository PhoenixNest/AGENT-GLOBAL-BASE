#!/usr/bin/env pwsh
# H-RAG01: UserPromptSubmit — RAG Knowledge Freshness Flag
# Detects prompts containing time-sensitive language and injects additionalContext
# requiring Claude to disclose knowledge cutoff, flag stale claims, and cite
# retrieval dates. Grounded in CC-00 RAG Engineering freshness architecture.

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$prompt = $data.prompt
if (-not $prompt) { exit 0 }
if ($prompt -match '^\s*/') { exit 0 }

$freshnessPatterns = @(
    '(?i)\b(latest version|most recent version|current version)\b',
    '(?i)\b(as of today|as of now|right now|currently|at the moment)\b',
    '(?i)\b(latest release|new release|recent release)\b',
    '(?i)\b(up to date|up-to-date|what.s new)\b',
    '(?i)\b(this year|in \d{4}|recent changes|recently added|just released)\b',
    '(?i)\b(what version|which version|is.+supported|does.+support)\b'
)

$detected = $false
foreach ($pattern in $freshnessPatterns) {
    if ($prompt -match $pattern) {
        $detected = $true
        break
    }
}

if (-not $detected) { exit 0 }

$additionalContext = @"
[RAG FRESHNESS FLAG — H-RAG01]
This prompt contains time-sensitive language.

Before responding, apply CC-00 RAG freshness protocol:
1. Disclose your knowledge cutoff (August 2025) when it affects accuracy
2. Mark potentially stale claims with [Knowledge Cutoff - verify]
3. If workspace telescope/ research reports exist on this topic, cite them
4. Prefer workspace documents (pipeline.md, library/, CC-00 docs) over training knowledge for workspace-specific facts
5. If retrieving external information, state the retrieval date
Reference: CC-00 RAG Engineering — retrieval freshness and source attribution
"@

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName     = "UserPromptSubmit"
        additionalContext = $additionalContext
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
