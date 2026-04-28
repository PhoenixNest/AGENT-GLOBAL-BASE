# Context Engineering Strategy — This Workspace

## What This Workspace Is, Through a Context Engineering Lens

This workspace is a **77-agent, multi-pipeline orchestration system**. Every agent invocation is a context window construction problem. The quality of every agent output is determined not just by the agent's skill, but by the precision of the context it receives.

At this scale, context engineering is not optional — it is the operating infrastructure.

---

## The Three Context Layers of This Workspace

| Layer           | Mechanism                                                  | Context Engineering Problem                                              |
| --------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Strategic**   | `AGENTS.md`, pipeline definitions, platform adapters       | What persistent instructions to carry in every agent's system slot       |
| **Tactical**    | 77 agent profiles, 213+ skill files                        | Which procedural memory to activate; how to scope system slots per agent |
| **Operational** | User prompts, agent-to-agent messages, artifact generation | How to assemble context for each specific task at runtime                |

---

## Layer 1: Strategic — System Slot Architecture

`AGENTS.md` (265 lines) is the master system prompt for the orchestrator agent. It defines:

- The full agent roster (procedural memory: who does what)
- Pipeline stage ownership (procedural memory: routing rules)
- Non-negotiable rules (system slot: hard constraints)
- Defect severity definitions (system slot: classification rules)

**Context engineering recommendation:**

The `AGENTS.md` currently delivers all content uniformly to every agent. Context engineering suggests a **scoped delivery** approach: each subagent's system slot should contain only the sections of `AGENTS.md` relevant to its role and pipeline stage.

| Agent Type       | System Slot Should Contain                             |
| ---------------- | ------------------------------------------------------ |
| iOS Lead         | Non-negotiable rules + iOS pipeline stages (5, 8) only |
| Backend engineer | Non-negotiable rules + backend pipeline stages only    |
| Orchestrator     | Full AGENTS.md                                         |

This reduces noise in subagent system slots and improves instruction-following accuracy.

---

## Layer 2: Tactical — Procedural Memory as Skill Files

The 213+ skill files in `.cursor/skills/` are the workspace's **procedural memory store**. Each skill file encodes "how to do X" for a specific domain.

**Current state:** Skills are loaded wholesale at session start (all 213+).
**Context engineering optimisation:** Load only skills relevant to the current task.

```
Task: "Design the iOS authentication module"
→ Activate: ios-implementation SKILL, mobile-security-architecture SKILL, architecture-decision-records SKILL
→ Do NOT load: localization, backend, Android, RAG skills
```

**Impact:** Reduces system slot bloat by 60–80% for single-domain tasks. Improves model focus on the active skill domain.

---

## Layer 3: Operational — Per-Turn Context Assembly

This is the most impactful layer and the most absent from the current workspace. Every agent conversation currently relies on the model's implicit context management. Explicit context engineering here means:

### 3.1 Memory Discipline by Agent Type

| Agent          | Working Memory                       | Episodic Memory                  | Semantic Memory                        |
| -------------- | ------------------------------------ | -------------------------------- | -------------------------------------- |
| Orchestrator   | Current pipeline stage + active task | All decisions made across stages | User preferences, project constraints  |
| Technical Lead | Current sub-task + sub-steps         | Stage-specific decisions         | Architecture decisions, ADRs           |
| Engineer       | Current implementation task          | Code decisions, API contracts    | Patterns, conventions for this project |
| Reviewer       | Current defect triage                | Prior defects in this codebase   | Defect classification standards        |

### 3.2 Inter-Stage Context Handoff

The 10-stage pipeline is a chain of agent handoffs. Each stage gate is a context handoff decision:

| Stage Transition                     | Handoff Tier | What to Forward                         |
| ------------------------------------ | ------------ | --------------------------------------- |
| Stage 1 → Stage 2 (PRD → Prototype)  | Scoped       | PRD + SRD + user requirements decisions |
| Stage 2 → Stage 3 (Prototype → UML)  | Scoped       | PRD + IDS + approved prototype          |
| Stage 3 → Stage 4 (UML → Plan)       | Scoped       | Architecture decisions + ADRs + TSD     |
| Stage 4 → Stage 5 (Plan → Dev)       | Full         | Full implementation plan + all ADRs     |
| Stage 5 → Stage 6 (Dev → Review)     | Scoped       | Code + architecture requirements only   |
| Stage 6 → Stage 7 (Review → Testing) | Scoped       | Defect report + test requirements       |

### 3.3 Sacred Context for Multi-Stage Projects

Decisions that must persist across all 10 stages (examples):

- Technology stack choices (ADRs from Stage 3)
- P0/P1 defect classifications
- Security requirements (SRD from Stage 1)
- Release blocking criteria

These must be promoted to **semantic memory** at the moment they are made and re-injected into every subsequent stage's context window.

---

## Gap Analysis

| Gap                                        | Current State                              | Target State                                          | Priority |
| ------------------------------------------ | ------------------------------------------ | ----------------------------------------------------- | -------- |
| No runtime context assembly                | Context managed implicitly by model        | `ContextAssembler` used for every agent call          | High     |
| No episodic memory across turns            | Each turn starts from scratch              | `EpisodicMemory` tracks session events                | High     |
| No semantic memory for cross-session facts | User preferences re-elicited every session | `SemanticMemory` persists preferences across sessions | Medium   |
| No sacred context management               | Decisions drift or are forgotten           | All ADRs and stage decisions marked as sacred         | High     |
| No inter-stage handoff protocol            | Stage transitions forward full history     | Scoped handoff packets per stage gate                 | Medium   |
| No skill-scoped system slots               | All 213+ skills implicitly available       | Task-aware skill activation                           | Low      |

---

## Recommended Implementation Order

1. **Add `EpisodicMemory` to the orchestrator agent** — tracks decisions, commitments, stage completions within a session
2. **Implement sacred context for ADRs** — all Architecture Decision Records from Stage 3 become sacred context for Stages 4–10
3. **Implement scoped system slots per agent type** — reduce system prompt noise for specialist agents
4. **Add `SemanticMemory` for user and project preferences** — survives between sessions
5. **Implement stage gate handoff packets** — formalise what context each stage receives

---

**Version:** 1.0
**Last Updated:** 2026-04-28
**See also:** [Integration Guide](./integration-guide.md) · [CONCEPTS.md](../CONCEPTS.md) · [Assembly Patterns](../patterns/assembly-patterns.md)
