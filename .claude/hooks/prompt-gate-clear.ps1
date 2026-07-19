#!/usr/bin/env pwsh
# H-P01 enforcement — PostToolUse (matcher: AskUserQuestion): clears the pending-confirmation
# marker once AskUserQuestion has been called, releasing the PreToolUse gate for this session.

param()

$rawInput = [Console]::In.ReadToEnd()
try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$sessionId = $data.session_id
if (-not $sessionId) { exit 0 }

$repoRoot = git rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0) { exit 0 }

$markerPath = Join-Path $repoRoot ".claude/hooks/.state/h-p01-pending-$sessionId.json"
Remove-Item $markerPath -Force -ErrorAction SilentlyContinue
exit 0
