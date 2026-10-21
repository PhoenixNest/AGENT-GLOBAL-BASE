# 05 — Continuation Re-Check

| Field    | Value                                                                                                            |
| -------- | ---------------------------------------------------------------------------------------------------------------- |
| Reviewer | Dr. Noor Haddad                                                                                                  |
| Role     | Staff Engineer, Security, Safety & Evaluation (BCU-00), independent of the delivery chain, holding a review veto |
| Scope    | Revised, uncommitted H-MAE01 hook and tests in the `agb-guard` worktree, against the condition in record 04      |
| Verdict  | NO VETO WITH FINDINGS                                                                                            |

The record-04 condition is met. The two remaining findings are P3 and do not block commit. Approval rests with
the user.

## Method

- `python -m pytest -q test_multi_agent_branch_naming_guard.py` from the hooks folder: `266 passed in 29.00s`.
- Ran the differential harness against the committed version, with the command name assembled at runtime.
  - Record-04 inputs, 12 cases:
    - All six bash continuation forms are denied, with LF and CRLF line endings.
    - The two backtick forms with valid names give ALLOW.
    - `g''it checkout -b bad` and `-b 'master'x` are denied.
    - `--attr-source=HEAD checkout -b bad` is denied.
  - Approved-scope inputs: all 10 give ALLOW.
  - New probes, 6 cases: results are below.

## Condition Checked

**Finding 1 of record 04 closed, with LF and CRLF tests: met.** `git worktree add \⏎ -b bad ../wt`,
`git checkout \⏎ -b bad` and `git \⏎ checkout -b bad` are denied with both line endings, and the test file
holds the continuation cases. Finding 2 is also closed: `git worktree add `⏎` -b agent/a/b ../wt` and
`git worktree add `⏎` ../wt ide-adaptation` give ALLOW. Findings 3 and 4 are closed as well.

## Remaining Findings

1. **P3 — Backslash continuation is applied to PowerShell commands.** PowerShell does not treat a trailing `\`
   as a continuation. `git worktree add ..\bad\⏎Get-Date` gives ALLOW. PowerShell runs the first line on its
   own, and git names the branch after the basename, `bad`. The record-04 version denied this input. Reaching
   it needs the path-only form, a trailing separator and a following line.
2. **P3 — A bash continuation in the middle of a word joins with no space.** Bash removes `\`+newline
   completely, so `git checkout -b agent/a/b\⏎/c` creates `agent/a/b/c`. The guard reads it as `agent/a/b`
   and `/c`, and gives ALLOW. Only deliberate evasion produces this.

Fix for both: choose the collapse by `tool_name`. For Bash, `\`+`\r?\n` becomes nothing. For PowerShell,
backtick+`\r?\n` becomes a space.

Stated limit, accepted: `-b 'agent'/a/b` is denied. It fails closed.
