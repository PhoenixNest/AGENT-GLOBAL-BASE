# core-component-00/multi-agent-engineering/ — Layer 5: Multi-Agent Engineering

CC-00 Layer 5 — "How agents cooperate." This module provides the orchestration framework for
multi-agent swarm systems, git worktree isolation, and inter-agent context handoff.

---

## What Lives Here

This module combines knowledge documentation with production-grade Python implementations and a
pytest test suite. It is one of three CC-00 modules with runnable code.

---

## Directory Structure

```
multi-agent-engineering/
├── fundamentals/          ← Conceptual docs + git worktree orchestration spec
│   └── git-worktree-orchestration.md   ← Full worktree isolation specification
├── patterns/              ← Swarm topologies, coordination patterns
├── implementations/       ← Production Python code (import from here)
│   ├── swarm_orchestrator.py       ← Swarm topology orchestration
│   ├── git_worktree_manager.py     ← Git worktree isolation for parallel agents
│   └── handoff_packet.py           ← Context Handoff Protocol (Full/Scoped/Minimal)
└── testing/               ← pytest test suite
```

---

## Key Implementations

| File                                      | Class / Entry Point  | Purpose                                                                    |
| ----------------------------------------- | -------------------- | -------------------------------------------------------------------------- |
| `implementations/swarm_orchestrator.py`   | `SwarmOrchestrator`  | Orchestrates multi-agent swarm topologies                                  |
| `implementations/git_worktree_manager.py` | `GitWorktreeManager` | Creates, manages, and cleans up git worktrees for parallel agent isolation |
| `implementations/handoff_packet.py`       | `HandoffPacket`      | Packages context for inter-agent handoff at Full, Scoped, or Minimal tiers |

---

## Running Tests

Run from `core-component-00/` (not workspace root) to avoid import conflicts:

```powershell
pytest multi-agent-engineering/testing/ -v
```

---

## Git Worktree Isolation Pattern

The canonical pattern for parallel multi-agent work in this workspace. Each agent gets an isolated
filesystem and branch, eliminating contention between concurrent agents.

**Five-phase lifecycle:**

| Phase         | Action                        | Key Commands                                                |
| ------------- | ----------------------------- | ----------------------------------------------------------- |
| 1 — Provision | Create one worktree per agent | `git worktree add ../agent-<name> -b agent/<name>/<task>`   |
| 2 — Execute   | Agent works in its worktree   | `git add -A && git commit -m "..."`                         |
| 3 — Integrate | Merge branches                | `git merge agent/<name>/<task> --no-ff`                     |
| 4 — Resolve   | Handle conflicts              | Manual resolution + commit                                  |
| 5 — Clean up  | Remove worktrees              | `git worktree remove ../agent-<name> && git worktree prune` |

**Branch naming:** `agent/<role>/<task>` (e.g., `agent/backend/dark-mode-api`)

**Full spec:** `fundamentals/git-worktree-orchestration.md`

---

## Context Handoff Protocol Tiers

| Tier    | When to Use                           | Content                             |
| ------- | ------------------------------------- | ----------------------------------- |
| Full    | Long-running handoff, complex context | Complete session state              |
| Scoped  | Scoped sub-task delegation            | Relevant task subset                |
| Minimal | Quick specialist delegation           | Task description + result slot only |

Reference: `implementations/handoff_packet.py` and
`core-component-00/context-engineering/patterns/multi-agent-handoff.md`

---

## Commit Conventions for Agent Work

| Convention     | Format                                                                                 |
| -------------- | -------------------------------------------------------------------------------------- |
| Branch name    | `agent/<role>/<task>`                                                                  |
| Commit subject | `agent/<name>: <verb-phrase>` (≤72 chars, imperative, lowercase)                       |
| Commit body    | Hyphen-bulleted list of discrete changes (required — bodyless commits are a P2 defect) |

---

## Rules

- Every parallel agent task must use git worktree isolation. Do not let concurrent agents share
  the same working tree.
- Use `SwarmOrchestrator` for multi-agent coordination — do not invent ad-hoc orchestration logic.
- Handoff packets must use the three-tier protocol (`HandoffPacket`) — do not write freeform
  context dumps.
- Run tests from `core-component-00/` or the module folder, not the workspace root.
- Any implementation change must pass `pytest multi-agent-engineering/testing/ -v` before committing.
- Single-line commits with no body are a P2 defect in agent work.
