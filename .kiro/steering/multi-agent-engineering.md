---
inclusion: fileMatch
fileMatchPattern: "**/multi-agent-engineering/**,**/*orchestrat*.py"
description: Multi-Agent Engineering (Layer 5) patterns and implementations
version: "1.0.0"
---

# Multi-Agent Engineering — Layer 5

**Steering File:** Multi-Agent Engineering (CC-00 Layer 5)  
**Inclusion:** Conditional — Activated when working in `multi-agent-engineering/` or orchestration-related Python files  
**Authority:** CC-00 Laboratory — Layer 5: How agents cooperate

---

## Module Identity

**Multi-Agent Engineering (MAE)** is Layer 5 of the CC-00 engineering stack — the discipline of designing, orchestrating, and operating coordinated systems of specialist LLM-powered agents.

| Field          | Detail                                                                                           |
| -------------- | ------------------------------------------------------------------------------------------------ |
| **Layer**      | 5 — How agents cooperate                                                                         |
| **Type**       | Production framework                                                                             |
| **Scope**      | Swarm topology, git worktree isolation, context handoff, orchestration patterns, agent lifecycle |
| **Output**     | Orchestration implementations, handoff protocols, isolation patterns                             |
| **Has Code**   | Yes — 3 Python implementations                                                                   |
| **Upstream**   | Orchestrates all four lower layers (Prompt, Context, Harness, RAG)                               |
| **Downstream** | Every agent's model call routes through `harness-engineering/`                                   |

---

## Core Concepts

### Multi-Agent System Architecture

```
Orchestrator Agent
    ↓
Task Graph (dependencies, parallelism)
    ↓
Worker Agents (isolated worktrees, scoped context)
    ↓
Integration Agent (merge results, resolve conflicts)
    ↓
Review Agent (quality gate before production)
```

### Five Swarm Topologies

| Topology         | Structure                                | When to Use                           |
| ---------------- | ---------------------------------------- | ------------------------------------- |
| **Hierarchical** | Tree structure with coordinator at root  | Complex projects with clear hierarchy |
| **Flat**         | All agents report to single orchestrator | Simple parallel tasks                 |
| **Mesh**         | Agents communicate peer-to-peer          | Collaborative problem-solving         |
| **Pipeline**     | Sequential handoff (A → B → C)           | Multi-stage workflows                 |
| **Hybrid**       | Combination of above patterns            | Real-world complex systems            |

---

## Key Production Implementations

All paths relative to `core-component-00/multi-agent-engineering/implementations/`:

| File                      | Purpose                                            | Test Suite                        |
| ------------------------- | -------------------------------------------------- | --------------------------------- |
| `swarm_orchestrator.py`   | Swarm topology orchestration                       | `../testing/test_orchestrator.py` |
| `git_worktree_manager.py` | Git worktree isolation for parallel agents         | `../testing/test_worktree.py`     |
| `handoff_packet.py`       | Context Handoff Protocol (Full / Scoped / Minimal) | `../testing/test_handoff.py`      |

---

## Git Worktree Isolation Pattern

For parallel multi-agent work, use git worktree isolation per AGENTS.md § 8.5:

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

---

## Context Handoff Protocol

When passing context between agents (from `context-engineering/patterns/multi-agent-handoff.md`):

| Tier        | What's Shared                                            | When to Use                         |
| ----------- | -------------------------------------------------------- | ----------------------------------- |
| **Full**    | Complete context window (all four slots)                 | Successor agent continues same task |
| **Scoped**  | Task-specific subset (working memory + relevant history) | Specialist agent handles subtask    |
| **Minimal** | Task description only (no history)                       | Independent parallel agent          |

**Implementation:** `implementations/handoff_packet.py`

---

## Orchestration Patterns

All paths relative to `core-component-00/multi-agent-engineering/patterns/`:

| Pattern                    | Purpose                                                      |
| -------------------------- | ------------------------------------------------------------ |
| `task-decomposition.md`    | Breaking complex tasks into agent-sized subtasks             |
| `dependency-management.md` | Managing task dependencies and execution order               |
| `conflict-resolution.md`   | Resolving conflicts when agents produce incompatible outputs |
| `quality-gates.md`         | Review and approval gates before integration                 |

---

## Anti-Patterns to Avoid

All paths relative to `core-component-00/multi-agent-engineering/anti-patterns/`:

| Anti-Pattern              | Problem                                                  | Solution                         |
| ------------------------- | -------------------------------------------------------- | -------------------------------- |
| **Over-sharing context**  | Agents receive irrelevant history, waste tokens          | Use Scoped or Minimal handoff    |
| **Under-sharing context** | Agents lack critical information, produce wrong output   | Use Full handoff for continuity  |
| **No isolation**          | Agents conflict on filesystem, corrupt each other's work | Use git worktree isolation       |
| **Silent failures**       | Agent fails but orchestrator doesn't detect it           | Implement progress sync protocol |

---

## Agent Behavior Rules for Multi-Agent Engineering

When orchestrating multiple agents:

1. **Choose appropriate topology** — Match swarm topology to task structure (Hierarchical, Flat, Mesh, Pipeline, Hybrid)
2. **Use git worktree isolation** — Parallel agents must work in isolated worktrees (mandatory per AGENTS.md § 8.5)
3. **Apply correct handoff tier** — Use Full / Scoped / Minimal based on task continuity requirements
4. **Implement progress sync** — Orchestrator must detect and handle agent failures
5. **Review before integration** — Review Agent inspects combined diff before merging to master
6. **Clean up worktrees** — Remove worktrees after integration to avoid filesystem clutter

---

## Integration Points

| From                    | To                     | What Flows                                      |
| ----------------------- | ---------------------- | ----------------------------------------------- |
| Multi-Agent Engineering | `context-engineering/` | Handoff packets (Full / Scoped / Minimal)       |
| Multi-Agent Engineering | `harness-engineering/` | Every agent's model call routes through harness |
| Multi-Agent Engineering | Git worktrees          | Isolated filesystem per agent                   |

---

## Active Research Programme

**Multi-Agent Memory Coherence** — How do distributed agents maintain consistent shared memory without a central store?

See `core-component-00/README.md` § Active Research Programmes for current status.

---

## Foundational Paper

The theoretical basis for multi-agent systems:

> **_Agent Systems Engineering: The Convergence of Four Disciplines_**  
> `core-component-00/agent-systems-engineering/CONCEPTS.md`

---

## Related Steering Files

- `context-engineering.md` — Layer 2: Context handoff protocol implementation
- `harness-engineering.md` — Layer 3: Every agent's model call routes through harness
- `git-workflow.md` — Git worktree isolation patterns (auto-included)
- `ase-framework.md` — ASE governance and compliance requirements
- `cc00-overview.md` — Complete CC-00 laboratory overview

---

**This steering file is automatically activated when working in `multi-agent-engineering/` directories or orchestration-related Python files.**
