#!/usr/bin/env pwsh
# Runs Prettier on the file that was just written or edited.
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
$supported = @('.md', '.json', '.yaml', '.yml', '.ts', '.tsx', '.js', '.jsx', '.css', '.html')

if ($ext -notin $supported) {
    exit 0
}

if (-not (Test-Path $filePath)) {
    exit 0
}

$result = & prettier --write "$filePath" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Prettier could not format ${filePath}: $result"
    exit 0
}
