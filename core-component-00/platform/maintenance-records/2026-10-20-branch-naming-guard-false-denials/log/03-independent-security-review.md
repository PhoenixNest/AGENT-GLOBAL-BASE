# 03 — Independent Security Review

| Field    | Value                                                                                                                                                                                           |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reviewer | Dr. Noor Haddad                                                                                                                                                                                 |
| Role     | Staff Engineer, Security, Safety & Evaluation (BCU-00), independent of the delivery chain, holding a review veto                                                                                |
| Scope    | Uncommitted `.claude/hooks/multi-agent-branch-naming-guard.py` (H-MAE01) and `.claude/hooks/test_multi_agent_branch_naming_guard.py` in the `agb-guard` worktree, against the committed version |
| Verdict  | NO VETO WITH FINDINGS                                                                                                                                                                           |

No finding is P0 or P1. A misnamed branch can be undone, loses no data and breaches nothing, and the guard is
defence in depth, not the approval boundary. The P2 findings are regressions against the committed guard and
are carried as conditions. Approval rests with the user.

## Method

- Read the full hook, `_hook_log.py`, the `settings.json` registration (`uv run`, no `timeout` set) and
  `git diff` against `HEAD` (read-only).
- `python -m pytest -q test_multi_agent_branch_naming_guard.py` from the hooks folder: `168 passed in 14.16s`.
- Ran a differential harness: the new `_find_invalid_name` against the committed regexes (loaded from
  `git show HEAD:...`) on 32 adversarial inputs. Results are quoted in Findings.
- Timing on untokenizable segments (`time.perf_counter`, Python 3.13.5): `echo "\"" ` + `git worktree add ` × N +
  `; git switch -c bad` gave N=0: 0.0 s; N=400 (6,829 chars): 2.2 s; N=800 (13,629 chars): 40.1 s. On the
  tokenized path, 225,000 balanced chars took 0.129 s, and 200,000 separators took 0.037 s.
- Hook run as a subprocess with UTF-8 non-ASCII commands (`€`, `é`, `—`), cp65001 locale: rc 0, deny each time.
- Exception paths: `shlex` `ValueError` is caught and `log_invocation` swallows every exception; no crash path
  between decision and deny print was found. Logging records only the branch name.

## Findings

1. **P2 — Only the first git invocation in a segment is examined.** When the guard's view of the quoting
   differs from the shell's, separate commands merge into one segment. This happens with a comment that holds
   a quote, `\"` in bash, or `` `" `` in PowerShell. The guard then reads only the first `git`.
   - Failing input: `git status # it's fine⏎git checkout -b bad` gives ALLOW. The committed guard: deny.
   - Also ALLOW: `git status #"⏎git checkout -b bad⏎#"`, `echo \"; git status; git checkout -b bad; echo \"`
     and ``echo `"; git status; git checkout -b bad; echo `"``.
   - Fix: examine every git token in the segment, and treat `#` at the start of a token as a comment that runs
     to the end of the line in `_split_segments`.

2. **P2 — Grouping and substitution prefixes hide git.** A token such as `(git` or `$(git` fails `_is_git`.
   - Failing input: `(git checkout -b bad)` gives ALLOW. The committed guard: deny.
   - Also ALLOW: `echo $(git checkout -b bad)` and ``echo `git checkout -b bad` ``.
   - Fix: strip a leading `(`, `$(`, `@(`, `{` or backtick from a token before `_is_git`, or split segments on
     them.

3. **P2 — The quoted-wrapper limit is wider than declared.** The accepted limit names `cmd /c "git ..."`.
   The same gap covers `bash -c 'git checkout -b bad'`, `pwsh -Command "git checkout -b bad"` and
   `Invoke-Expression "git checkout -b bad"`: all ALLOW, all denied by the committed guard.
   - Mitigation: also run the `-b`/`-B`/`-c`/`-C`/`--create`/`--orphan` regexes over the raw command. These
     forms always create a name, so this does not bring back the commit-ish false denials, and it closes
     Findings 1 and 2 for these forms.
   - Trade-off: a quoted mention of such a command, such as one in a commit message, is denied, as the
     committed guard does today.

4. **P2 — The fallback regex is cubic.** The lazy `.*?` chains in `_FALLBACK_PATTERNS` slow about 18× per
   doubling of input (40.1 s at 13.6 KB). A hook that outruns the host's timeout gives no decision, so the call
   proceeds. Reaching it takes deliberate construction.
   - Failing input (bash): `echo "\"" ` + `git worktree add ` × 800 + `; git switch -c bad`.
   - Fix: deny an untokenizable segment over 4 KB that names a creating subcommand, or replace the regexes
     with a linear token scan.
   - Doubt: I did not verify the host's default hook timeout.

5. **P3 — Bundled short options are missed.** `git worktree add -fb bad ../wt` and
   `git worktree add -qb bad ../wt` give ALLOW; the committed guard denied both. `git checkout -qb bad` and
   `git switch -qc bad` give ALLOW in both versions.
   - Fix: when a short-option cluster ends in `b`/`B` (or `c`/`C` for switch), read the next token as the name.
     When those letters fall mid-cluster, read the rest of the cluster as an attached name.

6. **P3 — Abbreviated long options and one global option are missed.** These give ALLOW in both versions,
   so this is not a regression:
   - `git switch --cre bad` and `git checkout --orph bad`
   - `git --attr-source HEAD checkout -b bad`: the guard does not consume the value of `--attr-source`, so it
     reads `HEAD` as the subcommand.

7. **P3 — Adjacent quoting and expansion are missed.** `git checkout -b 'master'x` and
   `git checkout -b agent/a/b$x` give ALLOW in both versions; static parsing cannot resolve them.

8. **P3 — The new-names-only rule meets git's remote guessing.** `git worktree add ../wt bad` passes. When only
   `origin/bad` exists, git creates a local `bad`; `git checkout -t origin/bad` does the same in both versions.
   The name already exists on a remote that only the user writes to. This does not materially weaken the
   control.

The new-names-only rule otherwise weakens nothing. The commit-ish check it removes was a source of false
denials, not a control.

## Accepted Limits

- `git branch <name>` is not inspected. Ref creation through plumbing (`git update-ref`, `git fetch . A:B`)
  falls in the same class.
- `cmd /c "git ..."` as one quoted token is not parsed. Finding 3 widens this limit.
- `git worktree add <path>` with no commit-ish checks `basename(<path>)` even when that branch exists. This
  fails closed and is acceptable.
- Git aliases, shell variables and adjacent-quote concatenation cannot be resolved statically (Finding 7).

## Conditions

1. Findings 1, 2 and 3 are closed, with a regression test for each failing input above, before the change
   is committed.
2. Finding 4 is bounded and has a timing test, for example less than 1 s at 64 KB.
3. Findings 5 to 8 are fixed or added to the docstring's stated limits, at Harness Engineering's discretion.
4. I re-run the differential harness on the revised hook before the change is committed.
