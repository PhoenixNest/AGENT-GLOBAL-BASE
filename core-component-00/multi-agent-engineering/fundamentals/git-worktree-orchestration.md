# Git Worktree Orchestration

> Using `git worktree` as infrastructure for multi-agent parallel development — giving each agent an isolated filesystem, a dedicated branch, and Git-native merge, rollback, and audit capabilities.

---

## The Problem

Multi-agent coding systems face a fundamental infrastructure challenge: **filesystem contention**.

| Scenario                                   | Without Git Worktree                    | With Git Worktree                                   |
| ------------------------------------------ | --------------------------------------- | --------------------------------------------------- |
| Two agents edit the same file              | One overwrites the other                | Each has an isolated copy; merge deferred           |
| Agent A's work needs to be rolled back     | Manual undo; may corrupt Agent B's work | `git revert` on Agent A's branch; B is unaffected   |
| Who changed what?                          | No built-in attribution                 | `git log --author=<agent>`, `git blame`             |
| Agent C's work depends on Agent B's output | Must wait for B to finish and save      | B commits to branch; C's worktree merges B's branch |
| Five agents work on the same codebase      | Sequential or chaotic                   | Five worktrees, five branches, controlled merge     |

---

## Prerequisites

| Requirement        | Detail                                            |
| ------------------ | ------------------------------------------------- |
| Git version        | ≥ 2.5 (worktree support)                          |
| Repository         | Must be a Git repository (`.git/` present)        |
| Disk space         | Each worktree is ~1× repo size (minus `.git`)     |
| Windows long paths | Enable: `git config --system core.longpaths true` |

---

## Lifecycle

### Phase 1: Provisioning

The orchestrator creates one worktree per agent:

```bash
# Create worktree for backend agent
git worktree add ../agent-backend -b agent/backend/dark-mode-api

# Create worktree for frontend agent
git worktree add ../agent-frontend -b agent/frontend/dark-mode-ui

# Create worktree for test agent
git worktree add ../agent-tester -b agent/tester/dark-mode-tests
```

Each command:

1. Creates a new directory (`../agent-backend`)
2. Checks out a new branch (`agent/backend/dark-mode-api`) from the current HEAD
3. The new directory is a full working copy with its own index

### Phase 2: Agent Execution

Each agent operates exclusively within its worktree:

```bash
# Agent backend works in ../agent-backend/
cd ../agent-backend
# ... agent edits files ...
git add -A
git commit -m "$(cat <<'EOF'
agent/backend: add dark mode API endpoint

- add POST /api/settings/theme endpoint accepting { mode: light | dark }
- validate unknown theme values and return HTTP 400 with descriptive error
- register new endpoint in the application router module
- add unit test stubs covering validation and happy-path scenarios

EOF
)"
```

**Key property:** Agents cannot see each other's uncommitted changes. Each worktree has its own index and working tree.

> **Commit message standard:** All agent commits use a multi-line HEREDOC with a hyphenated body. The subject line follows `agent/<name>: <brief verb-phrase>` (lowercase, imperative mood, ≤72 chars). The body lists each discrete change as a `- ` bullet. Omitting the body is a P2 defect; a single-line message provides no audit trail.

### Phase 3: Integration

The orchestrator (or a dedicated Integration Agent) merges agent work:

```bash
# Return to main worktree
cd ../main-repo

# Merge backend agent's work
git merge agent/backend/dark-mode-api --no-ff -m "$(cat <<'EOF'
integrate agent/backend/dark-mode-api into main

- merge dark mode API endpoint implementation from backend agent
- resolves task agent/backend/task-2026-0429-001

EOF
)"

# Merge frontend agent's work
git merge agent/frontend/dark-mode-ui --no-ff -m "$(cat <<'EOF'
integrate agent/frontend/dark-mode-ui into main

- merge dark mode UI components and settings screen from frontend agent
- resolves task agent/frontend/task-2026-0429-002

EOF
)"
```

### Phase 4: Conflict Resolution

If merge conflicts occur:

```bash
# Option 1: Abort and re-dispatch
git merge --abort

# Option 2: Resolve conflicts (manually or via Integration Agent)
# Edit conflicting files...
git add <resolved-files>
git commit -m "$(cat <<'EOF'
resolve merge conflict: agent/backend vs agent/frontend dark mode

- reconcile overlapping changes in src/theme/ThemeContext.ts
- backend uses REST API; frontend uses local state; unified via context provider
- integration agent verification complete

EOF
)"
```

### Phase 5: Cleanup

```bash
# Remove worktrees
git worktree remove ../agent-backend
git worktree remove ../agent-frontend
git worktree remove ../agent-tester

# Delete agent branches (if no longer needed)
git branch -d agent/backend/dark-mode-api
git branch -d agent/frontend/dark-mode-ui
git branch -d agent/tester/dark-mode-tests

# Prune stale worktree entries
git worktree prune
```

---

## Architecture Roles

| Role                   | Responsibility                                                  | Git Operations                                    |
| ---------------------- | --------------------------------------------------------------- | ------------------------------------------------- |
| **Orchestrator Agent** | Creates/destroys worktrees; triggers merges; manages task graph | `git worktree add/remove`, `git merge`, `git log` |
| **Worker Agent**       | Operates within its assigned worktree; commits changes          | `git add`, `git commit` (within worktree)         |
| **Integration Agent**  | Handles merge conflicts; ensures code coherence across agents   | `git merge`, `git diff`, conflict resolution      |
| **Review Agent**       | Reviews combined diff before merge to main                      | `git diff main..integration`, `git log`           |

---

## Branch Strategy

### Recommended Structure

```
main
├── integration/sprint-42           ← Intermediate merge target
│   ├── agent/backend/task-001      ← Backend agent's branch
│   ├── agent/frontend/task-002     ← Frontend agent's branch
│   ├── agent/tester/task-003       ← Test agent's branch
│   └── agent/security/task-004     ← Security agent's branch
└── swarm/dark-mode-feature         ← Swarm grouping (optional)
```

### Naming Convention

| Component       | Format                         | Example                                 |
| --------------- | ------------------------------ | --------------------------------------- |
| Agent prefix    | `agent/`                       | `agent/`                                |
| Agent name      | `<role>` or `<name>`           | `backend`, `ios-lead`                   |
| Task identifier | `task-<id>` or `<feature>`     | `task-2026-0429-001`, `dark-mode-api`   |
| Full branch     | `agent/<name>/<task>`          | `agent/backend/dark-mode-api`           |
| Stage-scoped    | `stage<N>/agent/<name>/<task>` | `stage5/agent/ios-lead/settings-screen` |

---

## Practical Considerations

| Consideration           | Detail                                                  | Mitigation                                                                 |
| ----------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Disk space**          | Each worktree duplicates the working tree (not `.git/`) | Use sparse checkout for large repos: `git sparse-checkout set src/ tests/` |
| **Windows path limits** | Default 260-char limit                                  | `git config --system core.longpaths true`                                  |
| **Concurrent Git ops**  | Multiple worktrees share one `.git/` directory          | Each worktree has its own index; lock contention is minimal                |
| **Stale worktrees**     | Forgotten worktrees waste disk space                    | Schedule `git worktree prune` in cleanup phase                             |
| **Submodules**          | Worktrees don't auto-initialise submodules              | Run `git submodule update --init` in each new worktree                     |
| **Merge conflicts**     | Two agents editing the same file in the same region     | Pre-assign file ownership where possible; use Integration Agent            |
| **Agent failure**       | Agent crashes mid-work; worktree left in dirty state    | Orchestrator checks worktree status; force-removes if unrecoverable        |

---

## Integration with Swarm Orchestrator

The `git_worktree_manager.py` implementation provides programmatic control:

```python
from implementations.git_worktree_manager import GitWorktreeManager

manager = GitWorktreeManager(repo_path="/path/to/repo")

# Provision
worktree = manager.create_worktree(
    agent_name="backend",
    task_id="dark-mode-api"
)

# Agent works in worktree.path ...

# Commit — subject line + hyphenated body (required)
manager.commit(
    worktree,
    message="add dark mode API endpoint",
    details=[
        "add POST /api/settings/theme endpoint accepting { mode: light | dark }",
        "validate unknown theme values and return HTTP 400 with descriptive error",
        "register new endpoint in the application router module",
        "add unit test stubs covering validation and happy-path scenarios",
    ],
)

# Merge
manager.merge(worktree, target_branch="main")

# Cleanup
manager.remove_worktree(worktree)
```

---

**Version:** 1.0
**Last Updated:** 2026-04-29
**See also:** [Swarm Topologies](./swarm-topologies.md) · [Swarm Orchestrator](core-component-00/multi-agent-engineering/implementations/swarm_orchestrator.py) · [Git Worktree Manager](core-component-00/multi-agent-engineering/implementations/git_worktree_manager.py)
