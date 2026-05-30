#!/usr/bin/env pwsh
# Runs the relevant pytest suite when a CC-00 implementation file changes.
# Only triggers for core-component-00/*/implementations/*.py files.
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

if ($filePath -notmatch 'core-component-00[/\\].+[/\\]implementations[/\\].+\.py$') {
    exit 0
}

if (-not (Test-Path $filePath)) {
    exit 0
}

$implementationsDir = Split-Path $filePath -Parent
$moduleDir = Split-Path $implementationsDir -Parent
$testDir = Join-Path $moduleDir "testing"

if (-not (Test-Path $testDir)) {
    Write-Host "No testing/ directory at $testDir — skipping"
    exit 0
}

# Skip gracefully if pytest is not installed (optional dev tool).
& python -c "import pytest" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "pytest not installed — skipping tests. Install with: pip install pytest pytest-xdist"
    exit 0
}

# Use parallel workers only if pytest-xdist is available.
$pytestArgs = @("$testDir", "-v", "--tb=short")
& python -c "import xdist" 2>$null
if ($LASTEXITCODE -eq 0) {
    $pytestArgs += @("-n", "4")
}

Write-Host "Running tests for $([System.IO.Path]::GetFileName($filePath))..."
& python -m pytest @pytestArgs 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Tests failed — review output above"
    exit 1
}

Write-Host "Tests passed."
