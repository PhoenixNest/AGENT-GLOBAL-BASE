# Git-as-Substrate Multi-Agent Coordination Pattern

## Overview

Git is the canonical coordination substrate for multi-agent swarms in this workspace.
Rather than introducing a separate coordination service, agents use git's existing
primitives — atomic commits, branch isolation, and the immutable object store — to
achieve safe, auditable, distributed coordination.

### Why Git Is the Right Substrate

| Property                       | Git Mechanism                       | Coordination Benefit                                              |
| ------------------------------ | ----------------------------------- | ----------------------------------------------------------------- |
| **Persistent versioned state** | Object store + reflog               | Every coordination event is durable and replayable                |
| **Atomic writes**              | Commits are all-or-nothing          | No partial lock states; readers see consistent snapshots          |
| **File-based locking**         | `current_tasks/<id>.lock` existence | Lock claim/release maps directly onto file create/delete          |
| **Branch isolation**           | One worktree per agent              | Agents cannot accidentally corrupt each other's working state     |
| **Distributed by default**     | No central broker required          | The repository itself is the coordination bus                     |
| **Human-readable audit trail** | `git log`                           | Any engineer can reconstruct the swarm execution history post-hoc |

This approach is validated at scale: Anthropic's C-compiler experiment ran 16 concurrent
agents producing a 100 K-line output using this pattern (see §5).

---

## The `current_tasks/` File Locking Protocol

### Directory Layout

```
current_tasks/
├── <task_id>.lock    ← exists = task claimed; absent = task available
└── README.md         ← describes the protocol (optional, for human readers)
```

### Step-by-Step Protocol

#### Step 1 — Availability Check

Before claiming a task, an agent checks whether the lock file exists.

```python
# Pseudocode
lock_path = f"current_tasks/{task_id}.lock"
if os.path.exists(lock_path):
    # Task already claimed — skip and move to the next available task
    continue
```

The check is non-blocking. Agents never wait on a lock; they skip and look for
another available task.

#### Step 2 — Claim (Write + Commit)

The claiming agent writes its identity and a UTC timestamp to the lock file,
then commits immediately. The commit is the atomic claim event.

```python
# Pseudocode
lock_content = {
    "agent_id": agent_id,
    "claimed_at": datetime.utcnow().isoformat(),
    "task_description": task.description,
}
write_json(lock_path, lock_content)
git_commit(files=[lock_path], message=f"lock: claim task {task_id}")
```

Other agents observing the repository (via `git fetch` or shared worktree
visibility) see the commit and skip that task.

#### Step 3 — Execute

The claiming agent performs the task work inside its own worktree. The lock file
remains in place for the duration. No other agent should write to `current_tasks/`
for this `task_id` while the lock exists.

#### Step 4 — Release (Delete + Commit)

On successful completion (or on failure with an error recorded), the agent
deletes the lock file and commits the deletion.

```python
# Pseudocode
os.remove(lock_path)
git_commit(files=[lock_path], message=f"lock: release task {task_id}")
```

The absence of the lock file signals to the orchestrator and to peer agents that
the task is no longer in-flight.

#### Step 5 — Stale Lock Detection and Reclaim

A lock is considered **abandoned** when no commit has been made to the
repository under that agent's authorship for **10 minutes** after the claim
commit.

```python
# Pseudocode — orchestrator stale-lock sweep (runs every 60 seconds)
for lock_file in list_lock_files("current_tasks/"):
    task_id = extract_task_id(lock_file)
    claim_commit = git_log(paths=[lock_file], limit=1)
    age_minutes = (now() - claim_commit.timestamp) / 60
    if age_minutes > 10:
        # Stale — reclaim
        os.remove(lock_file)
        git_commit(
            files=[lock_file],
            message=f"lock: reclaim abandoned task {task_id} (stale > 10 min)",
        )
        logger.warning("Reclaimed stale lock for task %s (agent: %s)",
                       task_id, claim_commit.author)
```

The 10-minute threshold is conservative by design. It accommodates slow agent
starts and network jitter while still recovering from crashed agents promptly.

### Race Condition Handling

Two agents may attempt to claim the same task in the same git second. The
**first writer to push wins**: git's fast-forward rejection causes the slower
agent's commit to fail on push, at which point the slower agent re-reads the
remote state and skips the now-claimed task.

```
Agent A: write lock → git commit → git push          (succeeds — wins)
Agent B: write lock → git commit → git push → REJECT (non-fast-forward)
Agent B: git pull → sees Agent A's lock → skip task
```

This is a safe, lossless resolution requiring no additional coordination
infrastructure.

---

## Agent Coordination Lifecycle (5 Phases)

### Phase 1 — Provision

The **Orchestrator** creates one git worktree per agent before any work begins.

```powershell
# One worktree per agent
git worktree add ../agent-<name> -b agent/<name>/<task>
```

- Each worktree gets a dedicated branch: `agent/<role>/<task>`
- The `current_tasks/` directory is initialized (or confirmed present) in the
  shared workspace root
- Agent profiles and task assignments are written to the worktree and committed

**Invariant:** No two agents share a worktree. Cross-worktree file access is
forbidden except via git merge or explicit handoff commits.

### Phase 2 — Execute

Each agent works exclusively inside its own worktree.

- Agents poll `current_tasks/` (via `git fetch` + file check) for available tasks
- On each task: check → claim → execute → release (§2 protocol)
- Agents commit work products to their branch using the format:
  ```
  agent/<name>: <verb-phrase>

  - Discrete change 1
  - Discrete change 2
  ```
- Single-line bodyless commits are a **P2 defect** in this workspace

### Phase 3 — Monitor

The Orchestrator monitors swarm progress by reading the repository state.

- Completed tasks: lock files absent, result commits present on agent branches
- In-progress tasks: lock files present with recent commit timestamps
- Stale tasks: lock files present with timestamps older than 10 minutes
  (trigger reclaim; see §2 Step 5)
- Failed tasks: lock files absent, agent branch contains an error commit

The Orchestrator does **not** modify agent branches during this phase.

### Phase 4 — Integrate

Once all tasks reach a terminal state (completed or failed), the Orchestrator
merges agent branches back into the integration branch.

```powershell
# Per-agent merge with no-fast-forward to preserve branch topology
git checkout master
git merge agent/<name>/<task> --no-ff -m "integrate: merge agent/<name>/<task>"
```

Merge conflicts are resolved by the Orchestrator according to the
conflict-resolution policy defined in the SwarmConfig. The Orchestrator
**never** silently drops work; unresolved conflicts are escalated to the user.

### Phase 5 — Cleanup

After integration is confirmed, worktrees and branches are removed.

```powershell
git worktree remove ../agent-<name>
git worktree prune
git branch -d agent/<name>/<task>
```

The `current_tasks/` directory is cleared of any residual lock files. A final
`git log` is captured as the audit record for the swarm run.

---

## Anthropic C-Compiler Experiment Reference

The canonical validation of git-as-substrate coordination comes from Anthropic's
published C-compiler experiment:

| Dimension                  | Value                                                           |
| -------------------------- | --------------------------------------------------------------- |
| **Fleet size**             | 16 concurrent agents                                            |
| **Output size**            | ~100 K lines of C code                                          |
| **Coordination mechanism** | Git worktrees + file-based locking                              |
| **Result**                 | Correct, integrated multi-module compiler                       |
| **Status**                 | Canonical Anthropic recommendation for multi-agent coordination |

This experiment established that git-substrate coordination scales to at least
16 agents on a single repository without coordination bottlenecks, provided each
agent maintains worktree isolation and commits frequently (every logical unit of
work, not just at task completion).

**Key lessons from the experiment:**

1. **Commit granularity matters** — agents that batch too much work lose
   recoverability; commit on every logical boundary
2. **Lock files are cheap** — the overhead of `current_tasks/` lock commits
   is negligible relative to the work performed
3. **Stale lock reclaim is essential** — at 16 agents, crash scenarios are
   common enough that a 10-minute reclaim threshold is necessary for liveness
4. **Branch-per-agent is non-negotiable** — shared branches at this scale
   produce merge conflicts that outweigh any coordination savings

---

## Integration with SwarmOrchestrator

The `SwarmOrchestrator` class integrates with git-as-substrate coordination
via `SwarmConfig.enable_git_worktree`.

```python
from core_component_00.multi_agent_engineering.implementations.swarm_orchestrator import (
    SwarmConfig,
    SwarmOrchestrator,
)

config = SwarmConfig(
    topology="hybrid",
    max_agents=16,
    enable_git_worktree=True,   # Activates the git-substrate coordination path
    timeout_seconds=600.0,
)

orchestrator = SwarmOrchestrator(config=config, agents=agent_profiles)
plan = orchestrator.plan(user_request, subtasks=subtasks)
result = await orchestrator.execute(plan)
```

When `enable_git_worktree=True`:

- The Orchestrator provisions one worktree per agent before calling `execute()`
- `_dispatch()` writes the lock claim before starting the agent task
- On task completion or failure, `_dispatch()` releases the lock
- The Orchestrator's stale-lock sweep runs as a background coroutine during
  `_execute_hybrid()` and `_execute_pipeline()` phases

When `enable_git_worktree=False` (default):

- Coordination falls back to in-process asyncio task management
- No `current_tasks/` directory is created or managed
- Suitable for single-process development and testing only

---

## Cross-Fleet Isolation

**Rule: worktrees are never shared across fleets.**

A _fleet_ is one instantiation of a SwarmOrchestrator with its provisioned
agents. Multiple fleets may run concurrently (e.g., a frontend fleet and a
backend fleet working in parallel on different subsystems), but each fleet's
worktrees are strictly private to that fleet.

### Why This Matters

- Lock files in `current_tasks/` use `task_id` as the filename. If two fleets
  manage overlapping task namespaces, false lock collisions occur.
- Agent branches from different fleets may diverge from incompatible base
  commits, making integration unpredictable.
- The Governed Shared Memory (GSM) scope predicate (`fleet_id` matching)
  prevents cross-fleet memory leakage, but only if worktrees are also isolated.

### Enforcement

- Each fleet assigns a unique `fleet_id` (UUID) at provisioning time
- `current_tasks/` lock files are namespaced: `current_tasks/<fleet_id>/<task_id>.lock`
- The Orchestrator's stale-lock sweep only touches lock files under its own
  `fleet_id/` prefix
- Agent branches are named `agent/<fleet_id>/<role>/<task>` when multiple
  fleets operate on the same repository

**Never pass a worktree path from Fleet A as a working directory for an agent
in Fleet B.** This violates isolation and is a P0 defect.

---

_Pattern Owner: CC-00 Multi-Agent Engineering_
_Validated: Anthropic C-compiler experiment (2024), 16-agent scale_
_Related: `git-worktree-orchestration.md`, `orchestration-patterns.md`, `shared_memory_log.py`_
