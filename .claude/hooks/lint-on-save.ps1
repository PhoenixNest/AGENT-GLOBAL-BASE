#!/usr/bin/env pwsh
# Runs ruff lint + format on Python files that were just written or edited.
# Claude Code passes tool input as JSON on stdin.

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $jsonData = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$filePath = $jsonData.tool_input.file_path

if (-not $filePath) {
    exit 0
}

$ext = [System.IO.Path]::GetExtension($filePath).ToLower()
if ($ext -ne '.py') {
    exit 0
}

if (-not (Test-Path $filePath)) {
    exit 0
}

# Skip gracefully if ruff is not installed (optional dev tool).
if (-not (Get-Command ruff -ErrorAction SilentlyContinue)) {
    Write-Host "ruff not installed — skipping lint. Install with: pip install ruff"
    exit 0
}

& ruff check --fix "$filePath" 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Warning "ruff check warnings on $filePath"
}

& ruff format "$filePath" 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Error "ruff format failed on $filePath"
    exit 1
}
