---
description: Git safety rules, commit conventions, and multi-agent worktree patterns — always active
---

# Git Workflow

Git conventions, safety rules, and the multi-agent worktree pattern for this workspace.

---

## Repository Information

**Repository root:** `c:\Users\ASUS\Documents\Code\Local\agent-global-base`
**Default branch:** `master`
**Remote:** No remote configured (local-only repository)

---

## Git Safety Rules

- Never force-push to `master` — escalate to the user
- Only create commits when the user explicitly asks
- Use `--no-verify` only when user explicitly requests
- Never use `-i` (interactive) git flags
- Leave git config unchanged
- Flag files likely containing secrets before committing

---

## Standard Commit Format

```
<type>: <short description>

- Detailed change 1
- Detailed change 2
- Detailed change 3
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

**For multi-agent work:**

```
agent/<name>: <verb-phrase>

- Detailed change 1
- Detailed change 2
```

Single-line commits with no body are a P2 defect.

---

## Multi-Agent Worktree Lifecycle

| Phase             | Action                                      | Key Commands                                                |
| ----------------- | ------------------------------------------- | ----------------------------------------------------------- |
| **1 — Provision** | Orchestrator creates one worktree per agent | `git worktree add ../agent-<name> -b agent/<name>/<task>`   |
| **2 — Execute**   | Each agent works in its worktree            | `git add -A && git commit -m "..."`                         |
| **3 — Integrate** | Merge branches into master                  | `git merge agent/<name>/<task> --no-ff`                     |
| **4 — Resolve**   | Handle merge conflicts                      | `git merge --abort` or manual resolution                    |
| **5 — Clean up**  | Remove worktrees                            | `git worktree remove ../agent-<name> && git worktree prune` |

**Branch naming:** `agent/<role>/<task>` (e.g., `agent/backend/dark-mode-api`)

**Full spec:** `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`
