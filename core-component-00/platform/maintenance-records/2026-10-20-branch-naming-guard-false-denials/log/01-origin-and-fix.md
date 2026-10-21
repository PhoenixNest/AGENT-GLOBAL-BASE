# 01 — Origin and Fix — 2026-10-20

| Field            | Detail                                                                                                                                                                                                                                                                                                                 |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-10-20-branch-naming-guard-false-denials/maintenance-record.md`, pipeline stages 1–4 (`core-component-00/platform/maintenance-records/pipeline.md`)                                                                                                                |
| **Trigger**      | The CEO approved the fix. H-MAE01 denied a whole compound command in a BCU-00 session on 2026-10-20: a worktree on the existing branch `core00/dev/engineering`. The workaround was `git switch` inside an existing worktree                                                                                           |
| **State before** | `.claude/hooks/multi-agent-branch-naming-guard.py` (H-MAE01, `PreToolUse` on `Bash\|PowerShell`) matched the command text with a regex and validated whatever it captured as a new branch name. The allowed prefixes did not include the laboratory prefixes `core00/` and `anu00/`. No test file existed for the hook |

## 1. Investigation

**Three denials of legitimate commands.**

| Id  | Command form                                     | Cause                                                                                                                                                                         |
| --- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D1  | `git worktree add <path> core00/dev/engineering` | Checks out an existing branch. The regex `git\s+worktree\s+add\s+\S+\s+(?:-b\s+)?([a-zA-Z0-9/._-]+)` read the commit-ish after the path as a new branch name and validated it |
| D2  | `git worktree add --detach <path> <commit>`      | `\S+` consumed `--detach`, so the path was read as the name and the commit as a further token                                                                                 |
| D3  | A branch created under `core00/` or `anu00/`     | The two laboratory prefixes were absent from the allowed list, so a correct laboratory branch name was denied                                                                 |

**Root cause.** The hook inferred intent from the position of tokens with a pattern, so it could not tell a creation flag from a checkout target. A branch name needs validating only where a branch is created; an existing branch, a commit and a path are never new names.

## 2. Execution

First revision:

1. The command is split into git invocations before any matching.
2. Each invocation is tokenized with `shlex` in non-POSIX mode, which keeps backslash paths intact.
3. Git global options are skipped before the subcommand is identified.
4. Names are validated only where a branch is created: `worktree add -b` and `-B`; `worktree add <path>` alone, where the basename of the path becomes the branch name; `checkout -b` and `-B`; `switch -c`, `-C`, `--create` and `--force-create`.
5. `core00/` and `anu00/` were added to the allowed prefixes.

Opus review revision:

1. `--orphan` is a flag on `worktree add` (the official synopsis is `[--orphan] [(-b | -B) <new-branch>] <path>`), so it no longer shifts the path into the name position.
2. `checkout --orphan <name>` and `switch --orphan <name>` are detected as branch creation.
3. A single `&` is treated as a command separator.

New test file: `.claude/hooks/test_multi_agent_branch_naming_guard.py`.

## 3. Verification

| Check performed                                                                     | Result     |
| ----------------------------------------------------------------------------------- | ---------- |
| New suite `test_multi_agent_branch_naming_guard.py`, after the Opus review revision | 168 passed |
| Full hook suite in `.claude/hooks`, after the first revision                        | 679 passed |
| D1, D2 and D3 forms replayed against the revised hook                               | All pass   |

Independent review: naming convention confirmed in log entry 02 (Dr. Idris Farouk); security review in log entry 03 (Dr. Noor Haddad); re-review in log entry 04; continuation re-check in log entry 05.

| Field                     | Detail                                                                                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Outcome**               | The first-revision and review-revision fixes are in place and covered by the new suite                                                                 |
| **Handoff to next stage** | Naming convention confirmation (entry 02) and independent security review (entry 03). Open follow-up items are in this topic's `maintenance-record.md` |
