#!/usr/bin/env pwsh
# H-CE01: UserPromptSubmit — Context Budget Alert
# Reads transcript_path file size as a session-length proxy. When it exceeds the
# threshold, injects additionalContext directing Claude to apply Sacred Context
# principles from CC-00 engineering/harness-engineering/implementations/context_monitor.py.

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$transcript = $data.transcript_path
if (-not $transcript -or -not (Test-Path $transcript)) { exit 0 }

$sizeKB     = [math]::Round((Get-Item $transcript).Length / 1KB)
$thresholdKB = 500

if ($sizeKB -lt $thresholdKB) { exit 0 }

$additionalContext = @"
[CONTEXT BUDGET ALERT — H-CE01]
Session transcript size: ${sizeKB} KB (threshold: ${thresholdKB} KB)

The session context is growing large. Apply Sacred Context principles before responding:
- Preserve decision-critical context (System and Working slots) losslessly
- Compress or summarize non-critical Conversation context where possible
- If approaching model context limits, invoke context_compressor.py patterns
- Prioritize: active task state > prior decisions > background knowledge
Reference: core-component-00/engineering/harness-engineering/implementations/context_monitor.py
"@

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName     = "UserPromptSubmit"
        additionalContext = $additionalContext
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
