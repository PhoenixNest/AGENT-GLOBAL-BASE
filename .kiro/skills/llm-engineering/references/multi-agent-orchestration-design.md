---
name: core-component-00-director-multi-agent-orchestration-design
description: Design multi-agent swarm architectures — topology selection, task decomposition, agent role specification, context handoff strategy, and orchestration pattern definition. Use when a problem requires coordinated specialist agents rather than a single agent, or when an existing multi-agent system needs architectural review and redesign.
version: "1.0.0"
source: core-component-00/director/skills/multi-agent-orchestration-design.md
agents:
  - core-component-00-director-elias-vance
---

# Multi-Agent Orchestration Design

## Purpose

Given a problem that benefits from multiple coordinated agents, produce a complete
orchestration architecture: which agents exist, what each one does, how work flows between
them, how context is handed off, and which CC-00 patterns govern the execution. The
specification should be implementable directly against
`core-component-00/multi-agent-engineering/`.

## Why Multi-Agent Architecture Requires Deliberate Design

The most common failure in multi-agent systems is not a failure of the individual agents —
it is a failure of the architecture between them. Agents that are too tightly coupled
produce circular dependencies and context explosion. Agents that are too loosely coupled
lose information at handoff boundaries. Topologies chosen for the wrong reasons produce
bottlenecks, race conditions, and redundant work.

A well-chosen topology, combined with precise role boundaries and a specified handoff
protocol, prevents these failure modes before the first line of code is written.

## Reference Materials

| Document                                                                               | Purpose                                      |
| -------------------------------------------------------------------------------------- | -------------------------------------------- |
| `core-component-00/multi-agent-engineering/fundamentals/swarm-topologies.md`           | Topology catalogue with selection criteria   |
| `core-component-00/multi-agent-engineering/patterns/orchestration-patterns.md`         | Orchestration pattern library                |
| `core-component-00/multi-agent-engineering/patterns/anti-patterns.md`                  | Failure modes to avoid                       |
| `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md` | Parallel agent isolation using git worktrees |
| `core-component-00/context-engineering/patterns/multi-agent-handoff.md`                | Context Handoff Protocol tiers               |
| `core-component-00/multi-agent-engineering/implementations/swarm_orchestrator.py`      | Reference orchestrator implementation        |
| `core-component-00/multi-agent-engineering/implementations/handoff_packet.py`          | Handoff packet construction                  |

## Design Process

### Step 1 — Problem Decomposition Analysis

Before selecting a topology, assess whether multi-agent architecture is actually
warranted. If the problem is small and sequential, document why a single-agent approach
was preferred and stop here — an unnecessary swarm creates coordination overhead that
exceeds any gain.

| Criterion             | Assessment Question                                                                                                                     |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Parallelisability** | Can sub-tasks run concurrently, or must they execute in sequence?                                                                       |
| **Specialisation**    | Does the problem benefit from agents with distinct capabilities, or would a single capable agent handle it more efficiently?            |
| **Scale**             | Is the problem large enough that a single agent's context budget would be exhausted? Would multiple agents reduce per-agent complexity? |
| **Dependency graph**  | What does the task graph look like? (Fan-out, chain, tree, diamond, mesh?)                                                              |

### Step 2 — Topology Selection

Select the topology that matches the task graph. Justify the selection against the
decision criteria in `swarm-topologies.md`.

| Topology         | Best For                                                                      | Avoid When                                                |
| ---------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------- |
| **Hierarchical** | Tree-structured tasks with a clear orchestrator and specialist sub-agents     | Tasks are flat or agents need peer-to-peer communication  |
| **Flat**         | Homogeneous parallel workloads with independent subtasks and shared synthesis | Subtasks have strong inter-dependencies                   |
| **Mesh**         | Problems where agents must consult each other with no fixed authority         | Strict audit trails or deterministic ordering is required |
| **Pipeline**     | Sequential transformation chains where each stage feeds the next              | Stages are not strictly ordered or require backtracking   |
| **Hybrid**       | Complex systems that combine multiple patterns (e.g. hierarchical + pipeline) | The team cannot afford the coordination overhead          |

Document the topology choice, the decision criteria that led to it, and any topologies
considered and rejected.

### Step 3 — Agent Role Specification

Define each agent in the swarm:

For each agent, specify:

- **Name and role codename:** What is this agent called?
- **Responsibility boundary:** What is this agent responsible for, and what is explicitly
  out of scope?
- **Input:** What does this agent receive (from the user, from the orchestrator, or from
  a peer agent)?
- **Output:** What does this agent produce, and in what format?
- **Authority:** What decisions can this agent make autonomously vs. what must be
  escalated to the orchestrator or user?
- **Context handoff tier required:** What level of context does this agent need from its
  predecessor? (Full / Scoped / Minimal)

A well-specified role boundary is the single most important design decision in a
multi-agent system. Overlapping responsibilities produce duplicated work and conflicting
outputs; gaps produce work that nobody does.

### Step 4 — Orchestration Pattern Selection

Select the orchestration pattern that governs how agents are tasked, how results are
collected, and how the system responds to agent failures. Reference:
`multi-agent-engineering/patterns/orchestration-patterns.md`

| Design Question      | Decision Space                                                           |
| -------------------- | ------------------------------------------------------------------------ |
| **Agent lifecycle**  | Who creates and destroys agents? (Orchestrator, user, or self-spawning?) |
| **Task assignment**  | Static decomposition upfront vs. dynamic assignment as results arrive?   |
| **Result synthesis** | Sequential merge, parallel reduce, or designated Integration Agent?      |
| **Failure handling** | Retry, fallback, abort, or accept partial result?                        |

### Step 5 — Context Handoff Design

For each agent transition in the topology, specify the handoff explicitly. The handoff
design must be consistent with the downstream agent's context budget — a Full handoff to
an agent with a small context window produces a budget overflow on the first call.

Reference: `context-engineering/patterns/multi-agent-handoff.md`

| Field               | Specification                                                            |
| ------------------- | ------------------------------------------------------------------------ |
| **Tier**            | Full / Scoped / Minimal                                                  |
| **Packet contents** | Which memory types are included: Episodic, Semantic, Procedural, Working |
| **Exclusions**      | What is deliberately omitted and why                                     |
| **Format**          | How the handoff packet is structured for the downstream agent            |

### Step 6 — Parallel Isolation Strategy (if applicable)

If agents will execute in parallel and share a filesystem or repository:

- Specify the git worktree isolation pattern to prevent filesystem contention.
- Reference: `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`
- Document the five-phase lifecycle: Provision → Execute → Integrate → Resolve → Clean up.

### Step 7 — Anti-Pattern Review

Before finalising the design, check it against the anti-patterns in
`multi-agent-engineering/patterns/anti-patterns.md`.

| Anti-Pattern                  | Presence Check                                                                              |
| ----------------------------- | ------------------------------------------------------------------------------------------- |
| **God orchestrator**          | Does the orchestrator do work rather than purely coordinate?                                |
| **Context explosion**         | Do any handoffs carry entire session histories when a scoped or minimal tier would suffice? |
| **Implicit dependencies**     | Do any agents assume context that was never specified in their handoff packet?              |
| **Missing integration agent** | Do parallel workloads have no designated merge step for combining results?                  |

## Output Format

Deliver as a structured Markdown document:

```
# Multi-Agent Orchestration Design — [System Name]

## Problem Decomposition
[Task graph analysis · Justification for multi-agent approach]

## Topology
[Selected topology · Justification · Alternatives rejected]

## Agent Roster
### [Agent Name / Role]
[Responsibility · Input · Output · Authority · Handoff tier required]
(repeat per agent)

## Orchestration Pattern
[Pattern selected · Task assignment · Result synthesis · Failure handling]

## Context Handoff Specification
[Per-transition: Tier · Packet contents · Exclusions · Format]

## Parallel Isolation Strategy
[Git worktree lifecycle if applicable]
OR: [Rationale for not needing isolation]

## Anti-Pattern Review
[Checklist against known failure modes]

## Implementation Entry Point
[Which CC-00 implementation files to start from:
 swarm_orchestrator.py · handoff_packet.py · git_worktree_manager.py]
```

## Quality Signal

A well-formed orchestration design is immediately buildable:

- Every agent has a defined input, output, and authority boundary with no overlaps or gaps.
- Every context handoff is specified by tier and packet contents — not described vaguely
  as "pass the context."
- The topology choice is justified by the task graph, not chosen by default.
- The anti-pattern checklist is signed off, not skipped.
