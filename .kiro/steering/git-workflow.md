---
inclusion: auto
description: Git safety rules and worktree patterns from AGENTS.md
version: "1.0.0"
---

# Git Workflow

This steering file defines git conventions, safety rules, and the multi-agent worktree pattern for the `agent-global-base` workspace.

---

## Repository Information

**Repository root:** `c:\Users\ASUS\Documents\Code\Local\agent-global-base`  
**Default branch:** `master`  
**Remote:** No remote configured (local-only repository)

---

## Git Safety Rules

### Pushing and PRs

- Always push to a new branch, never directly to main/master, unless explicitly asked.
- Use `git push` with -u flag to set up remote tracking when pushing a new branch.
- Use the appropriate CLI to create pull/merge requests (e.g., gh pr create for GitHub, glab mr create for GitLab).
- Keep PR titles concise, under 70 characters. Use the description for details.
- Structure PR descriptions with a summary of changes, what was tested, and any blocked features.

### Commit Policy

- Only create commits when the user explicitly asks. If unclear, ask first.
- Prefer staging specific files over `git add .` to avoid accidentally committing unrelated changes.
- Flag files that likely contain secrets (.env, credentials.json, etc.) before committing.
- Prefer new commits over `--amend`. Only amend your own unpushed commits when explicitly asked or incorporating pre-commit hook changes.
- Leave git config unchanged.
- Use non-destructive git commands by default. Destructive operations (force push, reset --hard, clean -f, branch -D) require explicit user's permission.
- Preserve hooks (--no-verify) unless the user explicitly asks to skip them.
- Use non-interactive git commands since interactive flags (-i) require unsupported input.

### What to Commit

**Commit finalized workspace additions:**

- Agent profiles
- Pipeline definitions
- Skill files
- Steering files
- Hooks
- Powers
- This AGENTS.md file

**Never force-push to `master`** — escalate to the user if a destructive git operation is being considered.

---

## Multi-Agent Swarm Workflow — Git Worktree

For parallel multi-agent (swarm) work, this workspace follows the **git worktree isolation pattern** defined in `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`.

### Core Principle

Each agent receives an isolated filesystem and branch, eliminating filesystem contention between concurrent agents.

### Five-Phase Lifecycle

| Phase             | Action                                                                  | Key Commands                                                |
| ----------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------- |
| **1 — Provision** | Orchestrator creates one worktree per agent                             | `git worktree add ../agent-<name> -b agent/<name>/<task>`   |
| **2 — Execute**   | Each agent works exclusively in its worktree; commits on its own branch | `git add -A && git commit -m "..."` (within worktree)       |
| **3 — Integrate** | Orchestrator or Integration Agent merges branches into master           | `git merge agent/<name>/<task> --no-ff`                     |
| **4 — Resolve**   | Integration Agent handles any merge conflicts                           | `git merge --abort` or manual resolution + commit           |
| **5 — Clean up**  | Remove worktrees and prune stale entries                                | `git worktree remove ../agent-<name> && git worktree prune` |

### Agent Roles

| Role             | Responsibility                                                                |
| ---------------- | ----------------------------------------------------------------------------- |
| **Orchestrator** | Creates/destroys worktrees; manages the task graph; triggers merges           |
| **Worker**       | Operates within its assigned worktree; commits atomic, well-described changes |
| **Integration**  | Merges branches; resolves conflicts; ensures cross-agent code coherence       |
| **Review**       | Inspects the combined diff before merge to `master`                           |

### Naming Conventions

| Convention     | Format                                   | Notes                                                                                      |
| -------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------ |
| Branch name    | `agent/<role>/<task>`                    | Stage-scoped variant: `stage<N>/agent/<role>/<task>` (e.g., `agent/backend/dark-mode-api`) |
| Commit subject | `agent/<name>: <verb-phrase>`            | ≤72 chars · imperative mood · lowercase                                                    |
| Commit body    | Hyphen-bulleted list of discrete changes | Required — single-line commits with no body are a P2 defect; no audit trail                |

### Programmatic Control

**Implementation:** `core-component-00/multi-agent-engineering/implementations/git_worktree_manager.py`  
**Full specification:** `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`

---

## Standard Commit Message Format

### For Single-Agent Work

```
<type>: <short description>

- Detailed change 1
- Detailed change 2
- Detailed change 3
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `kiro`

### For Multi-Agent Work

```
agent/<name>: <verb-phrase>

- Detailed change 1
- Detailed change 2
- Detailed change 3
```

**Example:**

```
agent/backend: implement dark mode api endpoint

- Add POST /api/v1/theme/dark endpoint
- Implement theme preference storage in user model
- Add validation for theme parameter
- Update API documentation
```

---

## When to Use Worktrees

**Use git worktrees when:**

- Running parallel multi-agent tasks (swarm orchestration)
- Multiple agents need to work on different features simultaneously
- Filesystem isolation is required to prevent conflicts

**Use standard git workflow when:**

- Single agent working sequentially
- Simple, non-parallel tasks
- Quick fixes or documentation updates

---

## Git Commands Reference

### Standard Workflow

```powershell
# Stage specific files
git add <file1> <file2>

# Commit with message
git commit -m "type: description"

# Push to new branch
git push -u origin <branch-name>
```

### Worktree Workflow

```powershell
# Create worktree for agent
git worktree add ../agent-backend -b agent/backend/dark-mode

# List all worktrees
git worktree list

# Remove worktree
git worktree remove ../agent-backend

# Prune stale worktree entries
git worktree prune
```

---

_This steering file is automatically included in all Kiro sessions. It ensures safe git operations and proper multi-agent coordination._
