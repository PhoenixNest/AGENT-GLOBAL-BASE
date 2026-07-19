#!/usr/bin/env pwsh
# H-HE02: PostToolUse (Bash) — Python Error Boundary Monitor
# Scans tool_output for Python exception patterns and injects additionalContext
# presenting the three recovery actions from CC-00 error_boundary.py:
# retry-with-backoff, fallback-to-safe-default, graceful-degradation.
# Reference: core-component-00/engineering/harness-engineering/implementations/error_boundary.py

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$toolOutput = $data.tool_output
if (-not $toolOutput) { exit 0 }

$errorPatterns = @(
    'Traceback \(most recent call last\)',
    '(?m)^\s*(SyntaxError|ImportError|ModuleNotFoundError|AttributeError|TypeError|ValueError|KeyError|IndexError|RuntimeError|OSError|FileNotFoundError|PermissionError|TimeoutError|ConnectionError|RecursionError):\s*\S',
    '(?m)^(Error|Exception):\s+\S'
)

$matchedLine = $null
foreach ($pattern in $errorPatterns) {
    if ($toolOutput -match $pattern) {
        # Extract the first recognizable error line for the context message
        $matchedLine = ($toolOutput -split "`n" |
            Where-Object { $_ -match '(?:Traceback|Error|Exception)' } |
            Select-Object -First 1).Trim()
        break
    }
}

if (-not $matchedLine) { exit 0 }

$additionalContext = @"
[ERROR BOUNDARY MONITOR — H-HE02]
Python error detected: $matchedLine

Apply CC-00 error_boundary.py recovery protocol (Harness Engineering, Layer 3):

1. RETRY (transient errors — network, timeout, rate-limit)
   - Wait with exponential backoff: 1s, 2s, 4s (max 3 retries)
   - Only retry idempotent operations

2. FALLBACK (recoverable errors — missing module, bad input)
   - Switch to safe-default behavior and continue session
   - Document the fallback in your response

3. GRACEFUL DEGRADATION (fatal errors — unrecoverable state)
   - Log the error with context (session_id, tool, timestamp)
   - Report the failure clearly to the user
   - Stop safely — do not mask or silently swallow the error

Reference: core-component-00/engineering/harness-engineering/implementations/error_boundary.py
"@

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName     = "PostToolUse"
        additionalContext = $additionalContext
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
