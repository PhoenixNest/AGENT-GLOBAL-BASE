# 02 — Naming Convention Confirmation

| Field    | Value                                                                                                                                      |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Reviewer | Dr. Idris Farouk                                                                                                                           |
| Role     | Staff Research Engineer, Multi-Agent Engineering Lead (CC-00), owner of the worktree naming spec                                           |
| Scope    | The accepted-name list (`_VALID_BRANCH_PATTERNS`) and the "only new branch names are checked" rule in `multi-agent-branch-naming-guard.py` |
| Verdict  | CONFIRMED WITH NOTES                                                                                                                       |

This is a naming-convention confirmation. It is not a code review; the parser, tokenizer and
test coverage belong to Harness Engineering (Kwame Asante) and to the independent review by
Dr. Noor Haddad (BCU-00).

## Spec Checked

- `core-component-00/framework/05-multi-agent-engineering/fundamentals/git-worktree-orchestration.md`
  — § Naming Convention (`agent/<name>/<task>`, `stage<N>/agent/<name>/<task>`) and § Branch
  Strategy (the recommended structure diagram).
- `CLAUDE.md` §6 — `agent/<role>/<task>` or `stage<N>/agent/<role>/<task>`.
- `.claude/rules/git-workflow.md` — branch naming `agent/<role>/<task>`, and the integration rule
  that names `bcu00/dev/*` branches.
- The guard's module docstring and its `_VALID_BRANCH_PATTERNS` list.
- The branches in the repository: two `agent/harness-engineering/...` branches,
  `anu00/dev/thinking`, `bcu00/dev/central`, `bcu00/dev/governance`, `bcu00/dev/limiter`,
  `bcu00/dev/workbench`, `company/dev/mapaper`, `core00/dev/engineering`, `ide-adaptation`,
  `master`, `workspace/inspector`.

## Findings

1. **The agent patterns match the spec exactly.** `^agent/[^/]+/[^/]+$` and
   `^stage\d+/agent/[^/]+/[^/]+$` are the two forms in the spec's Naming Convention table and in
   `CLAUDE.md` §6, each with exactly one role segment and one task segment. Case-sensitive matching
   is correct: the spec's names are lowercase kebab-case.

2. **The laboratory prefixes match the workspace's branch model.** `company/`, `bcu00/`,
   `core00/` and `anu00/` cover every laboratory branch in the repository (`company/dev/mapaper`,
   `bcu00/dev/*`, `core00/dev/engineering`, `anu00/dev/thinking`). `studio/` has no branch today
   but names a co-resident system, so accepting it is consistent. Accepting `core00/` and `anu00/`
   is the fix the CEO approved, and it removes the false denials for those two laboratories.

3. **The trunk and git-flow names are acceptable.** `master`, `main`, `develop` and the
   `feature/`, `fix/`, `chore/`, `docs/`, `refactor/`, `test/` prefixes are ordinary human-branch
   names. None conflicts with the agent namespace, and none weakens it.

4. **The "only new branch names are checked" rule is right.** The naming convention governs
   branches agents create. A checkout of an existing branch,
   `git worktree add <path> <commit-ish>`, and `git worktree add --detach` create no name, so
   there is nothing to validate, and denying them blocked legitimate work on the laboratory branches. Validating
   `-b`/`-B`, `--orphan`, `checkout -b/-B` and `switch -c/-C/--create/--force-create` covers the
   branch-creating forms the spec's Phase 1 uses.

5. **Gap, guard broader than spec.** The spec's Naming Convention table lists only the two agent
   forms. The laboratory prefixes, the trunk names and the git-flow prefixes appear in no
   section of `git-worktree-orchestration.md`; `git-workflow.md` names only `bcu00/dev/*`. The
   guard reflects practice; the spec lags it. This does not block the fix. The spec is
   Multi-Agent Engineering's document, and bringing its table up to the accepted list is my
   follow-up, as a separate change.

6. **Gap, spec broader than guard.** The spec's Branch Strategy diagram shows
   `integration/sprint-42` and `swarm/dark-mode-feature`. The guard denies both prefixes. No such
   branch exists, and the workspace integrates by merging each agent branch into the branch it was
   created from, so these prefixes are not in use. I do not ask for them to be added to the guard;
   the diagram will be brought into line with the integration model in the same spec change as
   Finding 5.

7. **`ide-adaptation` and `workspace/inspector` do not affect this fix.** Both are existing
   branches outside the convention. Checking either out, or adding a worktree on either with an
   explicit commit-ish, creates no name and passes. Neither is renamed or blessed by this fix;
   their disposition is a separate decision for the user.

## Notes for the Record

- **Edge case in the path-basename form.** `git worktree add <path>` with no commit-ish makes
  git use `basename(<path>)` as the branch name, and git checks out that branch when it already
  exists rather than creating it. The guard checks the basename without asking git whether the
  branch exists, so `git worktree add ..\ide-adaptation` is denied although it would check out
  an existing branch. The explicit form `git worktree add ..\ide-adaptation ide-adaptation`
  passes. This is a narrow exception to "a worktree on any existing branch passes"; Harness
  Engineering should either state it in the docstring and deny message or accept it as known.
- **`-B` on an existing non-conforming branch is denied.** `git checkout -B workspace/inspector`
  resets an existing branch and is denied. That is acceptable: `-B` is a force-create, and the
  convention applies to it.
- **Prefix patterns do not check depth.** `^(company|studio|bcu00|core00|anu00)/.*$` accepts any
  name under a laboratory prefix, not only `<lab>/dev/<area>`. That matches the approved scope,
  which accepts the prefixes; a tighter `<lab>/dev/<area>` rule would need its own decision.
- **`git branch <name>` is not inspected.** A name created that way can then be checked out
  without a check. This is outside the approved scope; the guard is defence in depth, not the
  boundary for branch naming.
- This confirmation covers naming only. Approval of the fix rests with the user.
