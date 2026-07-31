#!/usr/bin/env python3
"""
H-SYS01: PreToolUse (Bash|PowerShell) — Bidirectional OS-Aware Shell Syntax Guard (Python port)

On Windows: detects bash-only constructs and suggests PowerShell equivalents.
On macOS/Linux: detects PowerShell-only constructs and suggests POSIX equivalents.
Non-blocking: usage may be intentional; this is a correction note, not a hard block.
Reference: CLAUDE.md §1 — "Shell is Windows PowerShell. All terminal commands must be
PowerShell-compatible. Avoid bash-only syntax."

Behavioral parity source: .claude/hooks/system-shell-syntax-guard.ps1 (pwsh) and
.claude/hooks/system-shell-syntax-guard.sh (bash). This port collapses both scripts'
platform branches into a single `platform.system()` check since Python's interpreter
identity is not tied to the invoking shell the way pwsh vs. Git-Bash/WSL is.

This hook never blocks: every code path — malformed JSON, missing/empty command, no
pattern match, a match found, or an unrecognized platform — terminates with exit 0.
It only ever *adds* advisory `additionalContext`; it never emits a "deny"/"block"
decision. Fidelity to that always-exit-0, advisory-only contract (never silently
upgrading to a block, never crashing into a non-zero exit on a code path the
originals treat as a silent no-op) is the correctness bar for this port, in place of
"fail closed" semantics that would apply to an actual security/governance gate.

Case-sensitivity note: sh's macOS/Linux branch uses `grep -qiP` (case-insensitive)
while its Windows/MINGW branch uses `grep -qP` (case-SENSITIVE, no `-i`) — an
internal inconsistency within the bash original itself. ps1 uses PowerShell's
`-match` (case-insensitive by default) uniformly on both its Windows and
Linux/macOS branches. Since this hook is advisory-only (never blocks/denies) and
the sh Windows/MINGW branch is not "live" on this reference Linux environment
either way, this port applies `re.IGNORECASE` uniformly on both platform branches,
matching ps1's uniform behavior and sh's POSIX branch — the only effect is
detecting a couple of additional uppercase-variant constructs on the Windows path,
which is the more helpful direction for an advisory correction note, never a
security-relevant choice.
"""

import json
import platform
import re
import sys

# ─── Windows path: bash-only constructs → PowerShell equivalents ─────────────
# (pattern, bash_label, powershell_label)
WINDOWS_PATTERNS = [
    (
        r"(?<!\$)\brm\s+-[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*\b|(?<!\$)\brm\s+-[a-zA-Z]*f[a-zA-Z]*r[a-zA-Z]*\b",
        "rm -rf <path>",
        "Remove-Item -Recurse -Force <path>",
    ),
    (
        r"(?<!\w)grep\s+",
        "grep <pattern> <file>",
        "Select-String -Pattern <pattern> -Path <file>",
    ),
    (
        r"(?<!\w)sed\s+",
        "sed 's/old/new/g'",
        "Get-Content file | ForEach-Object { $_ -replace 'old','new' }",
    ),
    (
        r"(?<!\w)awk\s+",
        "awk '{print $1}'",
        "... | ForEach-Object { $_.Split()[0] }",
    ),
    (
        r"(?<!\$)export\s+[A-Za-z_][A-Za-z0-9_]*=",
        "export VAR=value",
        '$env:VAR = "value"',
    ),
    (
        r"(?<!\w)touch\s+[^\|&;]",
        "touch <file>",
        "if (-not (Test-Path <file>)) { New-Item -ItemType File <file> }",
    ),
    (
        r"(?<!\w)which\s+\w",
        "which <command>",
        "(Get-Command <command>).Source",
    ),
    (
        r"2>/dev/null|>/dev/null",
        "2>/dev/null  or  >/dev/null",
        "2>$null  or  | Out-Null",
    ),
    (
        r"(?<!\w)chmod\s+",
        "chmod <mode> <file>",
        "icacls <file> /grant <user>:<perm>  (or skip — not usually needed on Windows)",
    ),
    (
        r"(?<!\w)chown\s+",
        "chown <user> <file>",
        "icacls <file> /setowner <user>  (or skip — not usually needed on Windows)",
    ),
    (
        r"(?<!\w)mkdir\s+-p\s+",
        "mkdir -p <path>",
        "New-Item -ItemType Directory -Force <path>",
    ),
]

# ─── macOS/Linux path: PowerShell-only constructs → POSIX equivalents ────────
# (pattern, powershell_label, posix_label)
POSIX_PATTERNS = [
    (r"\bWrite-Output\b|\bWrite-Host\b", "Write-Output / Write-Host", "echo or printf"),
    (r"\bGet-ChildItem\b|\bgci\b|\bdir\s+", "Get-ChildItem / gci / dir", "ls"),
    (r"\bRemove-Item\b", "Remove-Item / Remove-Item -Recurse", "rm -rf <path>"),
    (r"\bCopy-Item\b", "Copy-Item", "cp <src> <dst>"),
    (r"\bMove-Item\b", "Move-Item", "mv <src> <dst>"),
    (r"\bNew-Item\b", "New-Item -ItemType", "mkdir <dir>  or  touch <file>"),
    (r"\bSet-Location\b", "Set-Location", "cd <path>"),
    (r"\bGet-Content\b", "Get-Content", "cat <file>"),
    (r"\bSelect-String\b", "Select-String", "grep <pattern> <file>"),
    (r"\bForEach-Object\b", "ForEach-Object / %", "for loop  or  xargs"),
    (r"\bWhere-Object\b", "Where-Object / ?", "grep or awk"),
    (
        r"\bConvertTo-Json\b",
        "ConvertTo-Json",
        'python3 -c "import json; print(json.dumps(...))"',
    ),
    (
        r"\bConvertFrom-Json\b",
        "ConvertFrom-Json",
        'python3 -c "import json; data=json.load(open(...))"',
    ),
    (
        r"\$env:[A-Za-z_][A-Za-z0-9_]*",
        "$env:VAR syntax",
        "$VAR  or  export VAR=value",
    ),
    (
        r"\bInvoke-WebRequest\b|\biwr\b",
        "Invoke-WebRequest / iwr",
        "curl <url>  or  wget <url>",
    ),
]


def emit(additional_context: str) -> None:
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": additional_context,
        }
    }
    print(json.dumps(payload))


def extract_command(data: object) -> str:
    """Mirrors `(d.get('tool_input') or {}).get('command','') or ''` from the bash
    port, but defensively guards against non-dict shapes at either level instead of
    letting a stray AttributeError escape into an uncaught traceback (the bash port's
    inline python3 helper *would* crash on a non-dict `tool_input`/root payload —
    harmlessly, since the crash happens before anything is printed and the caller
    only checks for an empty string — but a clean, deliberate exit-0 here is more
    faithful to the *intended* behavior than reproducing an incidental crash)."""
    if not isinstance(data, dict):
        return ""
    tool_input = data.get("tool_input")
    if not isinstance(tool_input, dict):
        return ""
    command = tool_input.get("command")
    if not command:
        return ""
    return str(command)


def main() -> int:
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        return 0

    command = extract_command(data)
    if not command:
        return 0

    system = platform.system()

    if system == "Windows":
        detected = []
        for pattern, bash_label, powershell_label in WINDOWS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                detected.append(f"  bash: {bash_label}\n  PS:   {powershell_label}")

        if not detected:
            return 0

        listing = "\n\n".join(detected)
        message = (
            "[SHELL SYNTAX GUARD — H-SYS01 | Windows]\n"
            "Bash-only construct(s) detected in the planned command. This workspace uses Windows PowerShell\n"
            "(CLAUDE.md §1). Please substitute the PowerShell equivalents before executing:\n"
            "\n"
            f"{listing}\n"
            "\n"
            "If you are intentionally targeting Git Bash or WSL, confirm explicitly in your response.\n"
            "Reference: CLAUDE.md §1, .claude/rules/ (approved command set for this workspace)"
        )
        emit(message)
        return 0

    if system in ("Linux", "Darwin"):
        detected = []
        for pattern, powershell_label, posix_label in POSIX_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                detected.append(f"  PS:    {powershell_label}\n  POSIX: {posix_label}")

        if not detected:
            return 0

        listing = "\n\n".join(detected)
        message = (
            "[SHELL SYNTAX GUARD — H-SYS01 | macOS/Linux]\n"
            "PowerShell-only construct(s) detected in the planned command. This system uses POSIX bash/sh.\n"
            "Please substitute the POSIX equivalents before executing:\n"
            "\n"
            f"{listing}\n"
            "\n"
            "If you are intentionally targeting pwsh on this POSIX system, confirm explicitly in your response.\n"
            "Reference: CLAUDE.md §1, .claude/rules/ (approved command set for this workspace)"
        )
        emit(message)
        return 0

    # Unknown platform — pass through silently
    return 0


if __name__ == "__main__":
    sys.exit(main())
