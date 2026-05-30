---
paths:
  - "**/multi-agent-engineering/**"
  - "**/*orchestrat*.py"
description: Multi-Agent Engineering (Layer 5) patterns and behavior rules
---

# Multi-Agent Engineering — Layer 5

**Scope:** Swarm topology, git worktree isolation, context handoff, orchestration patterns

---

## Five Swarm Topologies

| Topology         | Structure                        | When to Use                           |
| ---------------- | -------------------------------- | ------------------------------------- |
| **Hierarchical** | Tree with coordinator at root    | Complex projects with clear hierarchy |
| **Flat**         | All agents → single orchestrator | Simple parallel tasks                 |
| **Mesh**         | Peer-to-peer communication       | Collaborative problem-solving         |
| **Pipeline**     | Sequential handoff (A → B → C)   | Multi-stage workflows                 |
| **Hybrid**       | Combination of above             | Real-world complex systems            |

---

## Git Worktree Isolation (Mandatory for Parallel Agents)

Each parallel agent gets an isolated worktree. See `git-workflow.md` for the five-phase lifecycle.

---

## Context Handoff Protocol

| Tier        | What's Shared                            | When to Use                   |
| ----------- | ---------------------------------------- | ----------------------------- |
| **Full**    | Complete context window (all four slots) | Successor continues same task |
| **Scoped**  | Task-specific subset                     | Specialist handles subtask    |
| **Minimal** | Task description only                    | Independent parallel agent    |

---

## Anti-Patterns to Avoid

| Anti-Pattern          | Problem                  | Solution                         |
| --------------------- | ------------------------ | -------------------------------- |
| Over-sharing context  | Wasted tokens            | Use Scoped or Minimal handoff    |
| Under-sharing context | Wrong output             | Use Full handoff for continuity  |
| No isolation          | Filesystem conflicts     | Use git worktree isolation       |
| Silent failures       | Undetected agent failure | Implement progress sync protocol |

---

## Behavior Rules

1. Choose topology matching task structure
2. **Mandatory:** Parallel agents use git worktree isolation
3. Apply correct handoff tier (Full / Scoped / Minimal)
4. Orchestrator detects and handles agent failures
5. Review Agent inspects combined diff before merging to master
6. Clean up worktrees after integration
