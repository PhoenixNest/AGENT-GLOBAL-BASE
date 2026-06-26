#!/usr/bin/env pwsh
# H-RAG02: PostToolUse — RAG Index Sync on Doc Write (toggle-aware, phase-adaptive)
# Fires after Write or Edit tools modify .md files in KEY_DIRS.
# Behavior is governed by .claude/hooks/rag-sync-state.json (mode: auto|warn|off).
# Phase adaptation: reads SEARCH_BACKEND env var to determine rebuild vs upsert path.

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$toolName = $data.tool_name
if ($toolName -notin @("Write", "Edit")) { exit 0 }

$filePath = $data.tool_input.file_path
if (-not $filePath) { exit 0 }

# Normalize to forward slashes for matching
$normalizedPath = $filePath -replace '\\', '/'

$keyDirs = @("company/", "studio/", "core-component-00/", "telescope/")
$inKeyDir = $false
foreach ($dir in $keyDirs) {
    if ($normalizedPath -match "(^|/)$($dir)") {
        $inKeyDir = $true
        break
    }
}

if (-not $inKeyDir) { exit 0 }
if ($normalizedPath -notmatch '\.md$') { exit 0 }

# --- Read toggle state (defaults to warn if state file absent) ---
$stateFile = Join-Path $PSScriptRoot "rag-sync-state.json"
$mode            = "warn"
$debounceSeconds = 30
$lastRebuildAt   = 0

if (Test-Path $stateFile) {
    try {
        $state           = Get-Content $stateFile -Raw | ConvertFrom-Json
        $mode            = if ($state.mode)             { $state.mode }             else { "warn" }
        $debounceSeconds = if ($state.debounce_seconds) { $state.debounce_seconds } else { 30 }
        $lastRebuildAt   = if ($state.last_rebuild_at)  { $state.last_rebuild_at }  else { 0 }
    } catch {
        $mode = "warn"
    }
}

# --- Detect active migration phase via SEARCH_BACKEND ---
$backend = if ($env:SEARCH_BACKEND) { $env:SEARCH_BACKEND } else { "faiss" }
$updateTool = if ($backend -eq "qdrant") { "upsert_document" } else { "rebuild_index" }

# --- Mode: off — exit silently ---
if ($mode -eq "off") { exit 0 }

# --- Mode: warn — passive notice only, no rebuild ---
if ($mode -eq "warn") {
    $additionalContext = @"
[RAG INDEX SYNC — H-RAG02 | MODE: WARN]
Indexed workspace document modified: $filePath

The workspace-knowledge index is now stale. Auto-sync is in WARN mode.
If you need up-to-date retrieval results this turn, call $updateTool via the
workspace-knowledge MCP before issuing search_docs, find_related_documents, or
summarize_context queries.
To enable automatic rebuilds: /rag-sync auto
"@
    $output = [ordered]@{
        hookSpecificOutput = [ordered]@{
            hookEventName     = "PostToolUse"
            additionalContext = $additionalContext
        }
    } | ConvertTo-Json -Depth 5 -Compress
    Write-Output $output
    exit 0
}

# --- Mode: auto — debounce check, then emit rebuild instruction ---
$now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
if (($now - $lastRebuildAt) -lt $debounceSeconds) { exit 0 }  # within debounce window — suppress

# Update last_rebuild_at in state file
try {
    $newState = [ordered]@{
        mode             = $mode
        debounce_seconds = $debounceSeconds
        last_rebuild_at  = $now
    }
    $newState | ConvertTo-Json -Compress | Set-Content $stateFile
} catch { }

$additionalContext = @"
[RAG INDEX SYNC — H-RAG02 | MODE: AUTO]
Indexed workspace document modified: $filePath

Before issuing any search_docs, find_related_documents, summarize_context, or agent_knowledge_brief
query this turn, call $updateTool via the workspace-knowledge MCP to ensure retrieval results
reflect your changes.
To switch to passive mode: /rag-sync warn    To disable: /rag-sync off
Reference: telescope/2026-06-25-qdrant-migration-plan/plans/05-hook-design.md
"@

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName     = "PostToolUse"
        additionalContext = $additionalContext
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
