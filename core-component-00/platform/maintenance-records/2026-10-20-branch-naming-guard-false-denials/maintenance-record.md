# Maintenance Record — Branch-Naming Guard False Denials (H-MAE01)

| Field                          | Detail                                                                                                                                                                                                                                                                                                                             |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owner**                      | Kwame Asante, Senior Research Engineer, Harness Engineering (assigned by Dr. Elias Vance, CC-00 Laboratory Director)                                                                                                                                                                                                               |
| **Authorized / reviewed by**   | Authorized by the CEO, who approved the fix. Naming convention confirmed by Dr. Idris Farouk (Multi-Agent Engineering Lead, CC-00): CONFIRMED WITH NOTES. Independent review by Dr. Noor Haddad (BCU-00): NO VETO WITH FINDINGS (four P2 conditions), re-reviews: NO VETO WITH FINDINGS, every condition met, two P3 findings open |
| **System / resource affected** | `.claude/hooks/multi-agent-branch-naming-guard.py` (H-MAE01) and the new `.claude/hooks/test_multi_agent_branch_naming_guard.py`. No `settings.json`, venv or interpreter change. Committed on `bcu00/dev/limiter`                                                                                                                 |
| **Severity**                   | P2 — a guard denied legitimate commands (an existing-branch worktree, `--detach`, laboratory branch names); a workaround existed and no forbidden action was allowed. Not P1: no gate let a violation through and no work was lost                                                                                                 |
| **Status**                     | Completed — 266 tests in the new suite and 795 in the full hook suite passing; the independent re-checks returned no veto with every condition met                                                                                                                                                                                 |

---

## Pipeline Stage Log

| Stage                           | Entry                                                                                                                                  | Summary                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1–4 — Investigation to Verify   | `core-component-00/platform/maintenance-records/2026-10-20-branch-naming-guard-false-denials/log/01-origin-and-fix.md`                 | Three denials of legitimate commands traced to a regex that read a commit-ish or a flag as a new branch name and to missing laboratory prefixes. Fixed by tokenizing git invocations and validating names only where a branch is created, plus `core00/` and `anu00/`. The Opus review revision treats `--orphan` as a flag on `worktree add`, detects `checkout`/`switch --orphan <name>`, and treats a single `&` as a separator |
| 3 — Convention confirmation     | `core-component-00/platform/maintenance-records/2026-10-20-branch-naming-guard-false-denials/log/02-naming-convention-confirmation.md` | Accepted-name list matches the specification and the laboratory model; the new-names-only rule is correct. The specification lags practice, and its Branch Strategy diagram shows `integration/` and `swarm/` branches that are not in use (Dr. Farouk's own follow-up). The existing-branch basename exception is noted                                                                                                           |
| 4 — Independent security review | `core-component-00/platform/maintenance-records/2026-10-20-branch-naming-guard-false-denials/log/03-independent-security-review.md`    | No veto. Four P2 conditions: later commands hidden inside quotes, `(git …)`, `$(…)` and backtick forms, quoted wrappers such as `bash -c`, `pwsh -Command` and `Invoke-Expression`, and a fallback regex whose time grew about 18× per doubling of input (40 s at 13.6 KB); plus P3 items                                                                                                                                          |
| 5 — Re-review                   | `core-component-00/platform/maintenance-records/2026-10-20-branch-naming-guard-false-denials/log/04-security-re-review.md`             | No veto. All four conditions met (raw pass, linear time at 0.142 s for 102 KB, bundled options, differential re-run). One new P2 condition: a bash line continuation hid the creation flag; plus three P3 items                                                                                                                                                                                                                    |
| 5 — Re-check and Close          | `core-component-00/platform/maintenance-records/2026-10-20-branch-naming-guard-false-denials/log/05-continuation-re-check.md`          | No veto. The continuation condition is met with LF and CRLF, and quote-split names such as `g''it` are denied. Two P3 findings stay open: a trailing `\` is joined for PowerShell commands, where it is not a continuation, and bash joins `\` and a newline without a space                                                                                                                                                       |

---

## Final Design

- **Two passes.** The token pass splits the command into segments on `;`, `&`, `&&`, `||`, `|` and newlines outside quotes, tokenizes each segment with `shlex` in non-POSIX mode, and skips git global options, including `-C`, `-c`, `--git-dir`, `--work-tree` and `--attr-source`. The raw pass runs over the whole command and reads explicit creation flags after each `git` word: `worktree add -b`/`-B`, `checkout -b`/`-B`/`--orphan`, `switch -c`/`-C`/`--create`/`--force-create`/`--orphan`, the `=` forms, and bundled clusters such as `-fb`, `-qb` and `-qc`. In the raw pass quotes are dropped, and `;`, `&`, `|`, `(`, `)`, `{`, `}`, backticks and newlines act as separators. A bad name from either pass denies.
- **Names are checked only where a branch is created.** No commit-ish is ever read, so a worktree on an existing branch and `--detach` pass. `git worktree add <path>` alone validates the basename of `<path>`.
- **Linear time.** No lazy regex chains remain. The timing tests hold under 1 s at about 100 KB.
- **Accepted names.** `agent/<role>/<task>`, `stage<N>/agent/<role>/<task>`, `master`, `main`, `develop`, and the prefixes `company/`, `studio/`, `bcu00/`, `core00/`, `anu00/`, `feature/`, `fix/`, `chore/`, `docs/`, `refactor/`, `test/`.
- **Trade-off.** A quoted mention of a bad creation command, for example inside a commit message, is denied.
- **Exit and audit.** The hook always exits 0. The log records only the branch name.

### Stated limits

- `git branch <name>` and ref plumbing are not inspected.
- Abbreviated long options are not recognised.
- Adjacent quoting and variable expansion are not resolved.
- Aliases are not expanded.
- Remote-DWIM `git worktree add <path> <name>`, when only `origin/<name>` exists, is not recognised as a creation.
- `git worktree add <path>` is denied when a branch with that basename already exists; the explicit form `git worktree add <path> <branch>` passes.

---

## Open Follow-Up Items

| Item                                                                                                                                                                                                                           | Owner            | Target                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------- | ----------------------------------------- |
| `core-component-00/framework/05-multi-agent-engineering/fundamentals/git-worktree-orchestration.md` lags practice: document the laboratory, trunk and git-flow names and correct the Branch Strategy diagram                   | Dr. Idris Farouk | Separate change, at the CEO's convenience |
| Line continuations are joined the same way for every shell. Join by `tool_name` instead: for Bash, `\` and a line break become nothing; for PowerShell, a backtick and a line break become a space (entry 05, two P3 findings) | Kwame Asante     | Next change to H-MAE01                    |
| The pre-existing branches `ide-adaptation` and `workspace/inspector` do not follow the convention; their future is for the CEO                                                                                                 | CEO              | At the CEO's convenience                  |
| The fix reaches live sessions only when `bcu00/dev/limiter` is merged onward, which is the CEO's decision                                                                                                                      | CEO              | At the CEO's convenience                  |

---

## Related Records

- `core-component-00/platform/maintenance-records/2026-10-19-prompt-time-gate-false-positives/maintenance-record.md` — the earlier hook record with the same owner and review route
- `.claude/hooks/multi-agent-branch-naming-guard.py`, `.claude/hooks/test_multi_agent_branch_naming_guard.py` — the file changed and the regression suite added
- `CLAUDE.md` §6 and `core-component-00/framework/05-multi-agent-engineering/fundamentals/git-worktree-orchestration.md` — the branch and worktree conventions the guard enforces
