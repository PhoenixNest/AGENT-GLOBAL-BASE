#!/usr/bin/env python3
# H-GIT01: PreToolUse (Bash|PowerShell) — Pre-Commit Line Encoding Validator (Python port)
# Detects git add / git commit commands and validates line-ending issues before the
# command executes.
#   - Advisory (non-blocking): git diff --check whitespace warnings, missing *.ps1 gitattributes
#     rule, and round-trip-unsafe working-tree endings (a file that is internally consistent but
#     disagrees with what checkout would produce under the effective attributes + core.autocrlf —
#     e.g. a pure-LF .md in a core.autocrlf=true repo, which makes every commit emit
#     core.safecrlf warnings). The committed blob is correct in that case, so this is advisory:
#     the Edit/Write/Prettier toolchain writes LF routinely and blocking it would deadlock
#     ordinary work.
#   - Blocking: mixed line endings within a staged file's WORKING-TREE content, or a CR
#     byte in a staged *.ps1/*.sh file's working-tree content — a CRLF shebang breaks bash
#     on Linux/macOS/WSL, so this is a correctness defect, not a style preference.
#     Checked against the working-tree file, not the staged git blob: git's own
#     text=auto/eol clean filter already normalises CR/mixed endings out of anything by
#     the time it reaches the index, so checking the blob can never observe the defect —
#     the working-tree file is what actually gets executed and what the author edited.
#
# Ports .claude/hooks/git-line-encoding-validator.ps1 and .../.sh to a single
# stdlib-only Python 3 implementation. Both originals communicate a block purely via
# hookSpecificOutput.permissionDecision == "deny" in the JSON on stdout — neither ever
# exits with a non-zero status (the bash original's mixed-endings/CR-byte findings are
# blocking in the hook-protocol sense, but the *process* still exits 0). This port
# preserves that: every path below terminates with exit 0, matching both originals.
#
# Where the .ps1 and .sh originals disagree on formatting details (e.g. how trailing
# whitespace is trimmed from `git diff --check` output — the .sh original strips
# trailing whitespace per-line via `sed`, the .ps1 original trims the whole string via
# .Trim()), this port follows the .sh original, since that is the version actually
# wired into settings.json / invoked on this reference environment (see
# context-budget-alert.py for the same precedence rule, established there).
#
# H-GIT01 round-trip coverage-gap fix (commit 961d43f, "fix: close H-GIT01 round-trip
# line-ending coverage gap"): the original byte-level-only version of this hook (commit
# 9de4169) could only ever catch a staged file whose working-tree bytes were internally
# inconsistent (mixed LF/CRLF, or a CR byte in a .ps1/.sh). It had no way to catch a file
# that is internally *consistent* but round-trip-UNSAFE — e.g. a pure-LF file living in a
# core.autocrlf=true repo with no explicit `eol=` override, which is byte-clean but still
# triggers a `core.safecrlf` warning on every git add/commit because checkout would
# produce CRLF. Section 5 below (`autocrlf` + `git ls-files --eol`-derived round-trip
# check) is that fix: it derives the *expected* working-tree ending from git's own
# attribute resolution (via `ls-files --eol`, not a hand-rolled reimplementation) rather
# than assuming a single global convention, so an explicit `eol=lf` declaration is
# honoured for free and a pure-LF *.ps1/*.sh under `text eol=lf` is never misflagged.
# This port must preserve that check — porting only the pre-fix byte-level checks would
# silently regress H-GIT01 back to its known-incomplete state.
#
# Reference: .gitattributes, .claude/rules/git-workflow.md

import json
import os
import re
import subprocess
import sys

from _hook_log import log_invocation

GIT_ADD_COMMIT_RE = re.compile(r"\bgit\s+(add|commit)\b", re.IGNORECASE)
PS1_ATTR_RULE_RE = re.compile(r"^\*\.ps1[ \t]+text", re.MULTILINE)
EOL_LINE_RE = re.compile(r"^i/(\S*)\s+w/(\S*)\s+attr/(.*?)\s*\t(.+)$")
NEG_TEXT_ATTR_RE = re.compile(r"(^|\s)-text(\s|$)")
TEXT_ATTR_RE = re.compile(r"(^|\s)text")


def _run(args, combine_stderr=False):
    """Best-effort subprocess runner: returns stdout text, or '' on any failure.

    Mirrors the bash original's liberal use of `2>/dev/null` (errors silently
    discarded) and, for the one call that uses `2>&1` (git diff --check --cached),
    the combine_stderr=True path folds stderr into the captured text instead.

    Deliberately captures raw bytes and decodes without universal-newline
    translation (no text=True/universal_newlines=True). Python's text mode
    silently rewrites every lone \r and \r\n in stdout to \n, which would
    corrupt/hide the very CR bytes this hook exists to detect (e.g. a stray
    \r inside `git diff --check --cached` output for a CR-only-terminated
    line) — the bash original's `$(...)` command substitution captures raw
    bytes with no such translation, so this must too for byte-exact parity.

    Also strips ALL trailing "\n" characters (only "\n", never "\r") from the
    result, mirroring bash `$(...)` command substitution, which always trims
    every trailing newline from captured output. A trailing "\r" that is not
    itself followed by a stripped "\n" is deliberately left in place.
    """
    try:
        stderr_target = subprocess.STDOUT if combine_stderr else subprocess.DEVNULL
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=stderr_target,
        )
        text = (result.stdout or b"").decode("utf-8", errors="replace")
        return text.rstrip("\n")
    except Exception:
        return ""


def main() -> int:
    raw_input = sys.stdin.read()

    try:
        data = json.loads(raw_input)
    except Exception:
        # Unparseable JSON: the bash original's inline python helper exits 0 with no
        # output, so `command` resolves to "" and the outer script exits 0 immediately.
        # This hook cannot tell whether the tool call was even a git command, so it
        # deliberately fails OPEN (allow, no denial) rather than guessing — an advisory
        # linter blocking an unrelated tool call on malformed input would be worse than
        # missing a check. This mirrors context-budget-alert.py's identical precedent.
        return 0

    if not isinstance(data, dict):
        return 0

    tool_input = data.get("tool_input")
    command = (tool_input or {}).get("command", "") if isinstance(tool_input, dict) else ""
    if not isinstance(command, str) or not command:
        return 0

    # Only intercept git staging / commit commands
    if not GIT_ADD_COMMIT_RE.search(command):
        return 0

    cwd = data.get("cwd")
    if not isinstance(cwd, str) or not cwd:
        cwd = os.getcwd()

    # --- 1. Check staged files for whitespace / line-ending issues (advisory) ---
    diff_check_output = _run(["git", "-C", cwd, "diff", "--check", "--cached"], combine_stderr=True)
    has_diff_issues = bool(re.sub(r"\s", "", diff_check_output))

    # --- 2. Identify staged .ps1 files (advisory) ---
    staged_raw = _run(["git", "-C", cwd, "diff", "--cached", "--name-only"])
    # split("\n") rather than .splitlines(): the latter also splits on a lone \r
    # (and several other unicode line-boundary characters), which would silently
    # fragment/corrupt any output containing embedded CR bytes. The bash original
    # (`echo "$staged_files" | grep ...` / a `for` loop) only ever splits on "\n".
    staged_files = [line for line in staged_raw.split("\n") if line]
    has_staged_ps1 = any(p.lower().endswith(".ps1") for p in staged_files)

    # --- 3. Verify .gitattributes covers .ps1 (advisory) ---
    ps1_rule_missing = True
    gitattributes = os.path.join(cwd, ".gitattributes")
    if os.path.isfile(gitattributes):
        try:
            with open(gitattributes, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            if PS1_ATTR_RULE_RE.search(content):
                ps1_rule_missing = False
        except Exception:
            pass

    # --- 4. Byte-level checks against staged files' WORKING-TREE content (blocking) ---
    mixed_eol_files = []
    bad_cr_scripts = []
    for path in staged_files:
        full_path = os.path.join(cwd, path)
        if not os.path.isfile(full_path):
            continue
        try:
            with open(full_path, "rb") as f:
                file_bytes = f.read()
        except Exception:
            continue
        if not file_bytes:
            continue

        # Binary heuristic (mirrors git's own NUL-in-first-8000-bytes rule) — skip binaries
        if b"\x00" in file_bytes[:8000]:
            continue

        has_crlf = b"\r\n" in file_bytes
        has_lf_only = False
        prev = -1
        for byte in file_bytes:
            if byte == 10 and prev != 13:
                has_lf_only = True
                break
            prev = byte
        has_any_cr = b"\r" in file_bytes

        if has_crlf and has_lf_only:
            mixed_eol_files.append(path)
        if (path.endswith(".ps1") or path.endswith(".sh")) and has_any_cr:
            bad_cr_scripts.append(path)

    has_blocking_issues = bool(mixed_eol_files) or bool(bad_cr_scripts)

    # --- 5. Round-trip safety: working-tree endings vs what checkout would produce ---
    # (advisory — this is the H-GIT01 coverage-gap fix; see module docstring above)
    # Uses git's own `ls-files --eol` rather than reimplementing attribute resolution, so
    # explicit `eol=` declarations are honoured for free — a pure-LF .ps1/.sh under
    # `text eol=lf` is CORRECT and must never be flagged here.
    autocrlf = _run(["git", "-C", cwd, "config", "--get", "core.autocrlf"]).strip().lower()
    if not autocrlf:
        autocrlf = "false"

    roundtrip_entries = []
    if staged_files:
        eol_report = _run(["git", "-C", cwd, "ls-files", "--eol", "--", *staged_files])
        for line in eol_report.split("\n"):
            m = EOL_LINE_RE.match(line)
            if not m:
                continue
            w_eol, attr, rt_path = m.group(2), m.group(3).strip(), m.group(4)
            # Skip binaries, empty files, files with no terminators, and mixed
            # (mixed is already a blocking finding above — do not double-report it).
            if w_eol in ("", "none", "mixed", "-text"):
                continue
            if NEG_TEXT_ATTR_RE.search(attr):
                continue
            if "eol=lf" in attr:
                expected = "lf"
            elif "eol=crlf" in attr:
                expected = "crlf"
            elif TEXT_ATTR_RE.search(attr):
                expected = "crlf" if autocrlf == "true" else "lf"
            else:
                continue
            if w_eol != expected:
                roundtrip_entries.append(
                    "    - %s  (working tree: %s, checkout would produce: %s)" % (rt_path, w_eol, expected)
                )

    has_roundtrip_issues = bool(roundtrip_entries)

    # Exit if nothing to report at all
    if (
        not has_diff_issues
        and not (has_staged_ps1 and ps1_rule_missing)
        and not has_blocking_issues
        and not has_roundtrip_issues
    ):
        return 0

    # --- 6. Build additionalContext ---
    lines = [
        "[LINE ENCODING VALIDATOR — H-GIT01]",
        "Line-ending check triggered by git add/commit.",
        "",
    ]

    if has_blocking_issues:
        lines.append("BLOCKING LINE-ENDING DEFECTS:")
        if mixed_eol_files:
            lines.append("  Mixed line endings within a single file (some lines LF, some CRLF):")
            lines.extend("    - %s" % p for p in mixed_eol_files)
        if bad_cr_scripts:
            lines.append(
                "  CR byte present in a shell/PowerShell script (breaks execution on "
                "Linux/macOS/WSL — must be pure LF):"
            )
            lines.extend("    - %s" % p for p in bad_cr_scripts)
        lines.append("")
        lines.append("Action: fix the offending file(s) (re-save with consistent LF, or run")
        lines.append("  git add --renormalize <path>) and re-stage before committing.")
        lines.append("")

    if has_diff_issues:
        lines.append("WHITESPACE/LINE-ENDING WARNINGS (git diff --check --cached):")
        # sed -e 's/[[:space:]]*$//' strips trailing whitespace per LINE (not the whole
        # string) in the .sh original — replicated exactly here rather than a single
        # str.strip() (which is what the .ps1 original's .Trim() does instead). Split on
        # "\n" only (not .splitlines(), which also treats a lone \r as a line boundary
        # and would silently destroy any embedded CR byte on rejoin) so this matches
        # sed's own \n-delimited notion of "line" exactly.
        lines.append("\n".join(line.rstrip() for line in diff_check_output.split("\n")))
        lines.append("")
        lines.append("Action: Review the flagged files and normalise line endings before committing.")
        lines.append("  - For .ps1/.sh files: must be stored as LF (*.ps1/*.sh text eol=lf in .gitattributes).")
        lines.append(
            "  - For all other text files: left to ` * text=auto` — normalised to the OS of "
            "whoever checks the repo out, not hardcoded."
        )
        lines.append("  - Run: git add --renormalize . && git status to see the effect.")
        lines.append("")

    if has_roundtrip_issues:
        lines.append("ROUND-TRIP-UNSAFE WORKING-TREE ENDINGS (advisory):")
        lines.append("  These staged files are internally consistent, but their on-disk endings differ")
        lines.append("  from what checkout would write (core.autocrlf=%s + .gitattributes), so git" % autocrlf)
        lines.append("  emits a core.safecrlf warning for each one on every add/commit:")
        lines.extend(roundtrip_entries)
        lines.append("")
        lines.append("  Typical cause: a formatter or editor that always writes LF (Prettier, most agent")
        lines.append("  Edit/Write tools) touching a file in a core.autocrlf=true repo.")
        lines.append("  The COMMITTED CONTENT IS NOT AFFECTED — `* text=auto` normalises the blob to LF")
        lines.append("  either way. This is a working-copy consistency defect, not a content defect,")
        lines.append("  which is why it is advisory rather than blocking.")
        lines.append("")
        lines.append("  Action (representation only — changes no content):")
        lines.append("    git add --renormalize <path>")
        lines.append("    git checkout-index -f -- <path>   # rewrites the working copy in the expected form")
        lines.append("  Or re-save the file(s) with the expected endings before staging.")
        lines.append("")

    if has_staged_ps1 and ps1_rule_missing:
        lines.append("STAGED .ps1 FILES DETECTED — .gitattributes has no explicit *.ps1 rule.")
        lines.append('Add "*.ps1 text eol=lf" to .gitattributes then re-stage:')
        lines.append("  git add .gitattributes")
        lines.append("  git add --renormalize <your-ps1-file>")
        lines.append("")

    lines.append("Reference: .gitattributes, .claude/rules/git-workflow.md")

    msg = "\n".join(lines)

    hook_output = {"hookEventName": "PreToolUse"}
    session_id = data.get("session_id")

    if has_blocking_issues:
        # Mirrors the .sh original's incremental string-append exactly: each clause gets
        # its own trailing "; " (including the LAST clause), then "See additionalContext
        # for details." is appended after — producing "...bytes; See additionalContext...",
        # not "...bytes. See additionalContext..." (a single ". " join would be wrong).
        reason = "H-GIT01: blocking line-ending defect(s) —"
        if mixed_eol_files:
            reason += " %d file(s) with mixed line endings;" % len(mixed_eol_files)
        if bad_cr_scripts:
            reason += " %d .ps1/.sh file(s) with CR bytes;" % len(bad_cr_scripts)
        reason += " See additionalContext for details."
        hook_output["permissionDecision"] = "deny"
        hook_output["permissionDecisionReason"] = reason
        system_message = f"[H-GIT01: blocked git add/commit — {len(mixed_eol_files) + len(bad_cr_scripts)} line-ending defect(s)]"
        log_invocation("git-line-encoding-validator", "PreToolUse", decision="deny",
                        session_id=session_id,
                        extra={"mixed_eol": len(mixed_eol_files), "bad_cr": len(bad_cr_scripts)})
    else:
        system_message = "[H-GIT01: line-ending advisory — see additionalContext]"
        log_invocation("git-line-encoding-validator", "PreToolUse", decision="advisory",
                        session_id=session_id)

    hook_output["additionalContext"] = msg

    print(json.dumps({"systemMessage": system_message, "hookSpecificOutput": hook_output}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # Fail open, matching the bash original's resilience: it has no `set -e`, so an
        # unexpected mid-script failure (e.g. a transient git error) degrades to a plain
        # `exit 0` rather than crashing the hook and disrupting the calling tool call.
        # This hook is advisory-first; only deliberately detected byte-level line-ending
        # defects are meant to trigger `permissionDecision: deny`, communicated via the
        # JSON payload above — never via a non-zero process exit code (this hook never
        # exits 2; that is Claude Code's separate stderr-based blocking channel, unused
        # here in either original).
        sys.exit(0)
