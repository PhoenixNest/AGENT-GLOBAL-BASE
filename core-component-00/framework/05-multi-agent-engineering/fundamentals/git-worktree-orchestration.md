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

### Phase 3.5: Branch Topology — Parallel-Fork Base (Mandatory for Independent Batch Work)

**The problem.** Phase 1's example above provisions worktrees one at a time. If an orchestrator
instead provisions them **sequentially** — creating agent B's worktree only after agent A's branch
has already merged, then agent C's only after B's — every branch's single parent is the tip of the
previous merge, not a shared point in history. The resulting graph (`git log --graph`) renders as
a flat vertical line: each merge commit sits directly under the last, and the fact that the work
was logically independent and could have run concurrently is invisible. A reviewer scanning the
graph cannot tell "5 independent fixes, done one after another for no reason" from "5 fixes that
had to be sequenced because each depended on the last" — the topology carries no signal.

**The rule.** When N agents' work is genuinely independent — no agent's task depends on another's
output, and (ideally) no two agents touch the same file — **provision all N worktrees from the
same base commit before merging any of them**:

```bash
# All three worktrees fork from the SAME commit (the current tip, captured once)
BASE=$(git rev-parse HEAD)
git worktree add ../agent-backend -b agent/backend/dark-mode-api "$BASE"
git worktree add ../agent-frontend -b agent/frontend/dark-mode-ui "$BASE"
git worktree add ../agent-tester -b agent/tester/dark-mode-tests "$BASE"

# Each agent commits in its own worktree (Phase 2, unchanged)

# Merge one at a time — order doesn't matter for independent work, but do it deterministically
git merge agent/backend/dark-mode-api --no-ff -m "Merge agent/backend/dark-mode-api"
git merge agent/frontend/dark-mode-ui --no-ff -m "Merge agent/frontend/dark-mode-ui"
git merge agent/tester/dark-mode-tests --no-ff -m "Merge agent/tester/dark-mode-tests"
```

This costs nothing extra — the same number of worktrees, commits, and merges as the sequential
version — but the graph now shows every branch forking from one shared point and fanning back in,
which is what actually happened. Reserve genuine sequential chaining (each worktree forked from the
previous merge's tip) for batches with a real dependency between steps; don't default to it out of
habit when the work is independent.

**Retroactive rebuild.** If a batch was already committed sequentially and needs its topology
corrected after the fact (e.g., a later reviewer or the orchestrator's principal asks for it), this
is safe to do without losing work, using cherry-pick rather than interactive rebase (this workspace
never uses `-i` flags):

1. `git branch backup-before-topology-rewrite <current-tip>` — a disposable safety ref, not a
   permanent branch; delete it once step 4 passes.
2. For each individual (non-merge) commit in the range, create a fresh worktree from the intended
   common base and `git cherry-pick <that-commit>` onto it. A clean cherry-pick with matching
   insertion/deletion counts confirms the diff reproduced exactly.
3. Reset the target branch to the common base (`git reset --hard <base>`) and merge every rebuilt
   branch in the original relative order, `--no-ff`.
4. **Verify before cleaning up:** `git diff --quiet backup-before-topology-rewrite HEAD` must exit 0. This is a topology-only change — if the file tree differs at all from before the rewrite,
   something was reordered or dropped, and you stop and investigate rather than proceeding to
   cleanup. Don't rely on eyeballing the graph shape as sufficient verification; the byte-identity
   check is the actual acceptance criterion.
5. Only after step 4 passes: remove the temporary worktrees, delete the temporary branches
   (`git branch -d`, safe mode), and delete the backup ref.

This pattern was proven in production on 2026-08-27 rebuilding a 22-branch, two-phase batch (ANU-00
curriculum remediation) from sequential-chain into parallel-fork topology, confirmed byte-identical
via `git diff --quiet` before the safety backup was removed.

---

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

## Known Violation — Progress-Tracking Files Not Created During Execution (2026-07-14)

The same embedder-service/EX-001 build also surfaced a second process violation, unrelated to the
junction incident above: the orchestrator (Dr. Vance) had already decided, in writing, exactly
where `progress.md`/`session-log.md`/`checkpoint.json` should live for that build
(`telescope/2026-07-13-mcp-embedder-service-redesign/supporting/implementation-tracking/`, per
`workspace-conventions.md`'s progress-monitoring convention) — but never actually instructed any
worker agent to create or update them, and never created them directly. All six phases plus the
EX-001 remediation executed and merged with zero real-time tracking artifacts; the CEO went
looking for them and found nothing. This is logged as a process violation, not a mere gap —
`REFLECT-004` in the `memory_reflection` collection. The tracking files were subsequently
compiled from git history as the official record — accurate, but their after-the-fact compilation
does not excuse the violation itself.

**Root cause:** the orchestrator briefs in this build's `agent()`/subagent prompts specified phase
gates, acceptance criteria, and git-worktree conventions in detail, but never included
tracking-file creation as a deliverable. A location decision on paper is not the same as an
execution instruction.

**Rule going forward:** any orchestrator brief for multi-agent work covered by the workspace's
progress-monitoring convention must include tracking-file creation/update as an explicit,
checked deliverable in the _first_ phase that produces code — not left as a standing intention in
a planning document. If no owner is obviously right for it, the orchestrator owns it directly
rather than assuming a worker agent will infer it.

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

| Consideration                 | Detail                                                                                                | Mitigation                                                                 |
| ----------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Disk space**                | Each worktree duplicates the working tree (not `.git/`)                                               | Use sparse checkout for large repos: `git sparse-checkout set src/ tests/` |
| **Windows path limits**       | Default 260-char limit                                                                                | `git config --system core.longpaths true`                                  |
| **Concurrent Git ops**        | Multiple worktrees share one `.git/` directory                                                        | Each worktree has its own index; lock contention is minimal                |
| **Stale worktrees**           | Forgotten worktrees waste disk space                                                                  | Schedule `git worktree prune` in cleanup phase                             |
| **Submodules**                | Worktrees don't auto-initialise submodules                                                            | Run `git submodule update --init` in each new worktree                     |
| **Merge conflicts**           | Two agents editing the same file in the same region                                                   | Pre-assign file ownership where possible; use Integration Agent            |
| **Agent failure**             | Agent crashes mid-work; worktree left in dirty state                                                  | Orchestrator checks worktree status; force-removes if unrecoverable        |
| **Shared large-asset caches** | Sharing a heavy directory (model weights, datasets) across worktrees via a directory junction/symlink | **Never junction. Always plain-copy.** See incident below.                 |

---

## Known Incident — Directory Junctions and `git worktree remove` (2026-07-14)

During the embedder-service build (`core-component-00/telescope/2026-07-13-mcp-embedder-service-redesign/`),
an agent needed to give a new worktree access to a large, slow-to-populate shared cache
(`core-component-00/platform/model-context-protocol-servers/_shared/models/`) without re-downloading it per worktree. It used
a Windows directory **junction** to point the worktree's copy at the real shared cache directory.

When that worktree was later removed with `git worktree remove`, Git's recursive cleanup followed
the junction as if it were a real subdirectory and **deleted the shared cache's actual contents in
the main repository** — not a copy, the source. This is a known Windows junction/recursive-delete
footgun: a junction is transparent to most recursive filesystem walks, so tooling that assumes
"remove this directory tree" cannot tell where the junction's real target lives and treats it as
disposable.

**Recovery in this incident:** both cached models were restored (one from an intact local
Hugging Face hub cache with no re-download, one by re-copying from a second consumer's still-intact
private copy). No permanent data loss — but only because a second copy happened to exist elsewhere.
That will not always be true.

**Rule going forward:** if a worktree needs read access to a large shared asset directory that
lives outside the repo's normal working tree, **copy it in, never junction or symlink it in**. The
extra disk/time cost of a copy is bounded and known; the failure mode of a junction plus a
recursive-delete tool is unbounded (it can take out the one real copy). This applies to any shared
cache — model weights, datasets, or similar — not just the embedding-model cache that triggered
this incident.

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

**Version:** 1.1
**Last Updated:** 2026-08-27 (added Phase 3.5 — Branch Topology: Parallel-Fork Base, per Dr. Idris
Farouk, Multi-Agent Engineering Lead)
**See also:** [Swarm Topologies](./swarm-topologies.md) · [Swarm Orchestrator](core-component-00/framework/05-multi-agent-engineering/implementations/swarm_orchestrator.py) · [Git Worktree Manager](core-component-00/framework/05-multi-agent-engineering/implementations/git_worktree_manager.py)
