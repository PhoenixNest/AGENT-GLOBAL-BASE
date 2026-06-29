# Evaluation: Q2 — Syntax Guard OS-Detection Upgrade

**Investigation ID:** `2026-06-29-cross-platform-compatibility-audit`  
**Document Type:** Solution Evaluation  
**Date:** 2026-06-29  
**Author:** CC-00 Harness Engineering (Dr. Elias Vance, Laboratory Director)  
**Related Report:** `research-report.md` — Open Question 2  
**Status:** Complete

---

## Summary

The CEO's proposed upgrade is **technically straightforward and fully recommended**. PowerShell
7's built-in `$IsWindows`, `$IsLinux`, and `$IsMacOS` automatic variables make OS detection
zero-cost and zero-dependency within the existing `.ps1` hook. The upgrade requires no new
infrastructure: the hook reads the OS once at the top, then branches into one of two pattern
tables. The Windows path is unchanged. The macOS/Linux path is a new inverse guard — it flags
PowerShell-specific constructs (cmdlet names, `$env:VAR`, `Remove-Item`, etc.) and suggests
POSIX equivalents. The hook should be renamed to `system-shell-syntax-guard.ps1` to reflect
its expanded, platform-neutral purpose. A shared OS-detection primitive (a one-liner function)
is identified as a minor design opportunity shared with the Q1 initialization script.

---

## CEO Solution Overview

> "Before Claude Code runs any terminal command, the hook first determines the current user's
> system. If it is Windows, it will choose PowerShell first. If it is another system such as
> macOS, it will choose bash first."

This produces a bidirectional syntax guard:

| Platform    | Guard Direction                            | Action if Triggered             |
| ----------- | ------------------------------------------ | ------------------------------- |
| Windows     | Bash construct detected in planned command | Warn → suggest PowerShell equiv |
| macOS/Linux | PS construct detected in planned command   | Warn → suggest bash/POSIX equiv |

---

## Current Hook Analysis

Reading `system-powershell-syntax-guard.ps1` (112 lines):

**Structure:**

1. Reads stdin JSON → extracts `$data.tool_input.command`
2. Defines `$bashPatterns` — an array of 11 pattern/bash/powershell hashtables
3. Iterates patterns, collects matches into `$detected`
4. If any detected → emits `additionalContext` JSON with `[POWERSHELL SYNTAX GUARD — H-SYS01]` header

**Pattern inventory (11 patterns):**

| Pattern        | Bash Form             | PowerShell Equivalent                        |
| -------------- | --------------------- | -------------------------------------------- |
| `rm -rf`       | `rm -rf <path>`       | `Remove-Item -Recurse -Force <path>`         |
| `grep`         | `grep <pat> <file>`   | `Select-String -Pattern <pat> -Path <file>`  |
| `sed`          | `sed 's/old/new/g'`   | `Get-Content \| ForEach-Object { -replace }` |
| `awk`          | `awk '{print $1}'`    | `\| ForEach-Object { $_.Split()[0] }`        |
| `export VAR=`  | `export VAR=value`    | `$env:VAR = "value"`                         |
| `touch <file>` | `touch <file>`        | `New-Item -ItemType File` (if not exists)    |
| `which`        | `which <cmd>`         | `(Get-Command <cmd>).Source`                 |
| `2>/dev/null`  | `2>/dev/null`         | `2>$null`                                    |
| `chmod`        | `chmod <mode> <file>` | `icacls` (or skip on Windows)                |
| `chown`        | `chown <user> <file>` | `icacls /setowner` (or skip)                 |
| `mkdir -p`     | `mkdir -p <path>`     | `New-Item -ItemType Directory -Force`        |

**Current limitation:** No OS check — the hook fires identically regardless of whether the
system is Windows, macOS, or Linux, producing false positives on POSIX platforms.

---

## Feasibility Assessment — `$IsWindows` / `$IsLinux` / `$IsMacOS`

PowerShell 7 exposes three read-only boolean automatic variables set by the runtime:

| Variable     | True when...                     | Available since |
| ------------ | -------------------------------- | --------------- |
| `$IsWindows` | Running on Windows (any version) | PowerShell 6.0  |
| `$IsLinux`   | Running on Linux                 | PowerShell 6.0  |
| `$IsMacOS`   | Running on macOS                 | PowerShell 6.0  |

**Assessment:**

- Available in all PowerShell 7.x versions (the workspace minimum)
- Set before any user code runs — available at top of script with no warmup
- Mutually exclusive and exhaustive for the three supported platforms
- No external calls, no subprocesses, no file reads — pure runtime introspection
- **Verdict: Zero implementation cost, fully reliable, recommended as the detection mechanism**

A minimal guard at the top of the hook:

```powershell
if ($IsWindows) {
    # existing bash-pattern detection
} elseif ($IsLinux -or $IsMacOS) {
    # new PS-pattern detection
} else {
    exit 0  # unknown platform — passthrough silently
}
```

---

## Upgraded Hook Design

### Windows Path (existing behavior — minimal adjustment)

The 11 existing bash patterns are retained without change. One adjustment is recommended: the
`additionalContext` message header should become `[SHELL SYNTAX GUARD — H-SYS01 | PLATFORM:
WINDOWS]` to reflect the renamed hook identity. The body text should replace "This workspace
uses Windows PowerShell (CLAUDE.md §1)" with "You are on Windows. Prefer PowerShell
equivalents for the constructs detected."

The Git Bash / WSL escape clause (last line of current context) is retained unchanged.

### macOS/Linux Path (new POSIX guard)

On macOS/Linux, Claude Code may still emit PowerShell-specific constructs from its training
bias. The new path detects the following PowerShell-only patterns and suggests POSIX
equivalents:

| Pattern (regex)                              | PS Form                         | POSIX Equivalent                                    |
| -------------------------------------------- | ------------------------------- | --------------------------------------------------- |
| `(?<!\w)Get-ChildItem\b`                     | `Get-ChildItem [path]`          | `ls [path]`                                         |
| `(?<!\w)Remove-Item\b`                       | `Remove-Item [-Recurse -Force]` | `rm [-rf] <path>`                                   |
| `(?<!\w)Copy-Item\b`                         | `Copy-Item src dest`            | `cp [-r] src dest`                                  |
| `(?<!\w)Move-Item\b`                         | `Move-Item src dest`            | `mv src dest`                                       |
| `(?<!\w)New-Item\b`                          | `New-Item -ItemType File/Dir`   | `touch <file>` / `mkdir [-p] <dir>`                 |
| `(?<!\w)Set-Location\b`                      | `Set-Location <path>`           | `cd <path>`                                         |
| `(?<!\w)Get-Content\b`                       | `Get-Content <file>`            | `cat <file>`                                        |
| `(?<!\w)Set-Content\b`                       | `Set-Content <file>`            | `> <file>` or `tee`                                 |
| `(?<!\w)Write-Output\b\|(?<!\w)Write-Host\b` | `Write-Output/Write-Host`       | `echo`                                              |
| `\$env:[A-Za-z_]`                            | `$env:VAR`                      | `$VAR` (or `export VAR=value`)                      |
| `(?<!\w)Select-String\b`                     | `Select-String -Pattern`        | `grep <pattern>`                                    |
| `(?<!\w)ForEach-Object\b`                    | `\| ForEach-Object { ... }`     | `\| while read -r line; do ... done`                |
| `(?<!\w)Where-Object\b`                      | `\| Where-Object { $_ -match }` | `\| grep <pattern>`                                 |
| `(?<!\w)Test-Path\b`                         | `Test-Path <path>`              | `[ -e <path> ]` or `test -e <path>`                 |
| `-ExecutionPolicy\s+Bypass`                  | pwsh flag                       | No equivalent needed (no execution policy on POSIX) |

The POSIX path emits a `[SHELL SYNTAX GUARD — H-SYS01 | PLATFORM: POSIX]` context block with
the same non-blocking advisory structure as the Windows path.

---

## Full Upgraded Hook Implementation

The complete upgraded hook (`system-shell-syntax-guard.ps1`) ready for deployment review:

```powershell
#!/usr/bin/env pwsh
# H-SYS01: PreToolUse (Bash|PowerShell) — Cross-Platform Shell Syntax Guard
# On Windows: detects bash-only constructs, suggests PowerShell equivalents.
# On macOS/Linux: detects PowerShell-only constructs, suggests POSIX equivalents.
# Non-blocking: advisory correction note, not a hard block.

param()

$rawInput = [Console]::In.ReadToEnd()

try {
    $data = $rawInput | ConvertFrom-Json
} catch {
    exit 0
}

$command = $data.tool_input.command
if (-not $command) { exit 0 }

# ── Windows path: detect bash constructs ──────────────────────────────────────
if ($IsWindows) {
    $patterns = @(
        @{ pattern = '(?<!\$)\brm\s+-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*\b|(?<!\$)\brm\s+-[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*\b'
           from = 'rm -rf <path>'
           to   = 'Remove-Item -Recurse -Force <path>' },
        @{ pattern = '(?<!\w)grep\s+'
           from = 'grep <pattern> <file>'
           to   = 'Select-String -Pattern <pattern> -Path <file>' },
        @{ pattern = '(?<!\w)sed\s+'
           from = "sed 's/old/new/g'"
           to   = "Get-Content file | ForEach-Object { `$_ -replace 'old','new' }" },
        @{ pattern = '(?<!\w)awk\s+'
           from = "awk '{print \$1}'"
           to   = '... | ForEach-Object { $_.Split()[0] }' },
        @{ pattern = '(?<!\$)export\s+[A-Za-z_][A-Za-z0-9_]*='
           from = 'export VAR=value'
           to   = '$env:VAR = "value"' },
        @{ pattern = '(?<!\w)touch\s+[^\|&;]'
           from = 'touch <file>'
           to   = 'if (-not (Test-Path <file>)) { New-Item -ItemType File <file> }' },
        @{ pattern = '(?<!\w)which\s+\w'
           from = 'which <command>'
           to   = '(Get-Command <command>).Source' },
        @{ pattern = '2>/dev/null|>/dev/null'
           from = '2>/dev/null  or  >/dev/null'
           to   = '2>$null  or  | Out-Null' },
        @{ pattern = '(?<!\w)chmod\s+'
           from = 'chmod <mode> <file>'
           to   = 'icacls <file> /grant <user>:<perm>  (or skip — not needed on Windows)' },
        @{ pattern = '(?<!\w)chown\s+'
           from = 'chown <user> <file>'
           to   = 'icacls <file> /setowner <user>  (or skip — not needed on Windows)' },
        @{ pattern = '(?<!\w)mkdir\s+-p\s+'
           from = 'mkdir -p <path>'
           to   = 'New-Item -ItemType Directory -Force <path>' }
    )

    $detected = @()
    foreach ($p in $patterns) {
        if ($command -match $p.pattern) {
            $detected += "  bash: $($p.from)`n  PS:   $($p.to)"
        }
    }
    if ($detected.Count -eq 0) { exit 0 }

    $list = $detected -join "`n`n"
    $additionalContext = @"
[SHELL SYNTAX GUARD — H-SYS01 | PLATFORM: WINDOWS]
Bash-only construct(s) detected in the planned command. You are on Windows — prefer PowerShell
equivalents:

$list

If you are intentionally targeting Git Bash or WSL, confirm explicitly in your response.
Reference: CLAUDE.md §1, .claude/rules/
"@
}

# ── macOS/Linux path: detect PowerShell constructs ────────────────────────────
elseif ($IsLinux -or $IsMacOS) {
    $patterns = @(
        @{ pattern = '(?<!\w)Get-ChildItem\b'
           from = 'Get-ChildItem [path]'
           to   = 'ls [path]' },
        @{ pattern = '(?<!\w)Remove-Item\b'
           from = 'Remove-Item [-Recurse -Force] <path>'
           to   = 'rm [-rf] <path>' },
        @{ pattern = '(?<!\w)Copy-Item\b'
           from = 'Copy-Item src dest'
           to   = 'cp [-r] src dest' },
        @{ pattern = '(?<!\w)Move-Item\b'
           from = 'Move-Item src dest'
           to   = 'mv src dest' },
        @{ pattern = '(?<!\w)New-Item\b'
           from = 'New-Item -ItemType File/Directory'
           to   = 'touch <file>  or  mkdir [-p] <dir>' },
        @{ pattern = '(?<!\w)Set-Location\b'
           from = 'Set-Location <path>'
           to   = 'cd <path>' },
        @{ pattern = '(?<!\w)Get-Content\b'
           from = 'Get-Content <file>'
           to   = 'cat <file>' },
        @{ pattern = '(?<!\w)Set-Content\b'
           from = 'Set-Content <file>'
           to   = 'echo "..." > <file>  or  tee <file>' },
        @{ pattern = '(?<!\w)Write-Output\b|(?<!\w)Write-Host\b'
           from = 'Write-Output / Write-Host'
           to   = 'echo' },
        @{ pattern = '\$env:[A-Za-z_]'
           from = '$env:VAR'
           to   = '$VAR  (or export VAR=value to set)' },
        @{ pattern = '(?<!\w)Select-String\b'
           from = 'Select-String -Pattern <pat>'
           to   = 'grep <pat> <file>' },
        @{ pattern = '(?<!\w)ForEach-Object\b'
           from = '| ForEach-Object { $_ }'
           to   = '| while read -r line; do ...; done  or  xargs' },
        @{ pattern = '(?<!\w)Where-Object\b'
           from = '| Where-Object { $_ -match <pat> }'
           to   = '| grep <pat>' },
        @{ pattern = '(?<!\w)Test-Path\b'
           from = 'Test-Path <path>'
           to   = '[ -e <path> ]  or  test -e <path>' },
        @{ pattern = '-ExecutionPolicy\s+Bypass'
           from = 'pwsh -ExecutionPolicy Bypass'
           to   = 'No execution policy on POSIX — omit this flag' }
    )

    $detected = @()
    foreach ($p in $patterns) {
        if ($command -match $p.pattern) {
            $detected += "  PS:   $($p.from)`n  bash: $($p.to)"
        }
    }
    if ($detected.Count -eq 0) { exit 0 }

    $list = $detected -join "`n`n"
    $additionalContext = @"
[SHELL SYNTAX GUARD — H-SYS01 | PLATFORM: POSIX]
PowerShell-only construct(s) detected in the planned command. You are on macOS/Linux — prefer
bash/POSIX equivalents:

$list

If you are intentionally using pwsh on this machine, confirm explicitly in your response.
Reference: CLAUDE.md §1, .claude/rules/
"@
}

else {
    # Unknown platform — passthrough silently
    exit 0
}

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName     = "PreToolUse"
        additionalContext = $additionalContext
    }
} | ConvertTo-Json -Depth 5 -Compress

Write-Output $output
exit 0
```

---

## Renaming Recommendation

**Recommendation: Rename to `system-shell-syntax-guard.ps1`.**

The current name `system-powershell-syntax-guard.ps1` is accurate for the Windows-only
implementation but becomes misleading post-upgrade. The hook now guards shell syntax
symmetrically in both directions. `system-shell-syntax-guard.ps1` is platform-neutral,
describes the function correctly, and aligns with the hook's new identity code
`[SHELL SYNTAX GUARD — H-SYS01]`.

The file rename requires updating the corresponding `command` args in
`.claude/settings.json` (the `PreToolUse` `Bash|PowerShell` hook entry) to reference the
new filename.

---

## Shared Primitives with Q1

Both Q1 (initialization script) and Q2 (this hook upgrade) share the same OS-detection
requirement:

| Concern                  | Q1 Init Script                        | Q2 Syntax Guard Hook               |
| ------------------------ | ------------------------------------- | ---------------------------------- |
| **Detection mechanism**  | Shell script checks `$OSTYPE`/`uname` | PowerShell `$IsWindows`/`$IsMacOS` |
| **Detection timing**     | Once at first-run setup               | Per-command at runtime             |
| **Result used for**      | pwsh install decision + config swap   | Pattern table branch selection     |
| **Shared utility value** | Low — different runtimes (bash vs PS) | Not applicable                     |

**Conclusion on shared utility:** The detection mechanisms are different because Q1's init
script runs in the user's native shell (bash/zsh on POSIX, PS on Windows) _before_ pwsh
is guaranteed to be present. Q2 runs _inside_ pwsh, where the automatic variables are
always available. No shared utility module is warranted. The design principle is shared
(detect OS, branch), but the implementation layers are distinct and should remain separate.

---

## Edge Cases

| Scenario                                           | Behavior                                                                                                                                                                                               | Risk                                   |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| **WSL on Windows**                                 | `$IsLinux = $true` inside WSL. The POSIX guard fires. This is correct — WSL is a Linux environment even when hosted on Windows.                                                                        | Low — correct behavior                 |
| **Git Bash on Windows**                            | Git Bash does not use `pwsh` — the hook won't fire at all via the Bash tool if invoked through Git Bash's own shell. If invoked via the PowerShell tool, `$IsWindows = $true` and Windows guard fires. | Low — existing escape clause covers it |
| **Docker container (Linux image on Windows host)** | pwsh inside the container reports `$IsLinux = $true`. POSIX guard fires. Correct for container's OS.                                                                                                   | Low — correct behavior                 |
| **macOS with pwsh installed via Homebrew**         | `$IsMacOS = $true`. POSIX guard fires. Correct.                                                                                                                                                        | None                                   |
| **Unknown/exotic platform**                        | Falls through to `else { exit 0 }` — silent passthrough. No false positives.                                                                                                                           | Low                                    |
| **Pattern false positives**                        | e.g., a variable named `$GetContent` might match `Get-Content`. Regex `(?<!\w)` word-boundary prefix on all PS patterns mitigates this.                                                                | Low                                    |

---

## Open Implementation Questions

1. **Rename file or keep existing name?**  
   Renaming `system-powershell-syntax-guard.ps1` → `system-shell-syntax-guard.ps1` requires
   updating the `settings.json` hook entry. CEO/user approval needed before rename to avoid
   breaking the hook chain.

2. **Should the POSIX pattern list be expanded before deployment?**  
   The 15 patterns above cover the most common PS constructs Claude emits. A wider audit of
   actual Claude Code outputs on POSIX could surface additional patterns. This is a P3
   enhancement — the current list is sufficient for an initial deployment.

3. **Should the hook be non-blocking for both paths (current behavior)?**  
   The current Windows hook is advisory, not blocking. The proposed POSIX guard inherits the
   same non-blocking design. If the CEO prefers a hard block for either platform, this can
   be implemented by changing `exit 0` to `exit 2` with a `stopReason` field. Current
   recommendation: retain non-blocking for both paths.

---

## Next Steps

1. **CEO/user approves rename** → rename file and update `settings.json` hook entry
2. **Deploy upgraded hook** → replace current script content with the implementation above
3. **Update hook header comment** → change `H-SYS01` description from "Windows PowerShell
   Syntax Guard" to "Cross-Platform Shell Syntax Guard"
4. **Update `CLAUDE.md §1` reference** → the hook currently cites `CLAUDE.md §1`
   ("Shell is Windows PowerShell"). After the `CLAUDE.md §1` update (separate P2 task),
   the hook's internal comment should reference the updated platform-conditional guidance
5. **Note commonality with Q1** → if the Q1 init script introduces an OS-detection
   utility module, assess whether Q2's per-command detection can delegate to it at low cost

---

**Document version:** 1.0  
**Prettier-formatted:** Yes  
**Related:** `research-report.md`, `q1-init-script-evaluation.md`
