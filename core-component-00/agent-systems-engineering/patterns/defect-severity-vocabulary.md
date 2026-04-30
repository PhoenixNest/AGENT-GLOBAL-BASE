# Pattern: Defect Severity Vocabulary

| Field        | Value                                  |
| ------------ | -------------------------------------- |
| **Category** | Governance · Inter-Agent Communication |
| **Layer**    | Cross-cutting (Layers 1 + 3)           |
| **Status**   | Ratified — ADR-ASE-001                 |

---

## Problem

In a multi-agent system, different agents apply different thresholds for what constitutes
a "serious" issue. A security agent classifies a missing input validation as critical;
the feature agent calls it minor. A quality gate agent blocks a release; the development
agent considers it optional. Without a shared vocabulary, escalation decisions are
inconsistent, agents second-guess each other's classifications, and severity becomes a
matter of negotiation rather than objective assessment.

The cost of this inconsistency is high: P0 issues are delayed because they are
classified as P2; P3 issues block releases because they are elevated to P1 without
criteria.

---

## Solution

Define a **shared defect severity vocabulary** that all agents in the system use without
interpretation. Every agent's identity prompt and every quality gate references the same
four levels with the same definitions. Severity is determined by criteria, not by the
agent making the assessment.

---

## The Four Severity Levels

| Level  | Name     | Definition                                                       | Required Action                    | Override Authority   |
| ------ | -------- | ---------------------------------------------------------------- | ---------------------------------- | -------------------- |
| **P0** | Critical | Crash, data loss, security breach, or compliance violation       | Non-negotiable fix. Block release. | None — absolute      |
| **P1** | Major    | Core feature broken, major UX failure, or data integrity concern | Non-negotiable fix. Block release. | None — absolute      |
| **P2** | Minor    | Partial degradation, non-blocking UX issue, or technical debt    | Fix recommended. User decides.     | User / Product Owner |
| **P3** | Cosmetic | Polish item, style inconsistency, or nice-to-have improvement    | Fix optional. User decides.        | User / Product Owner |

**P0 and P1 are absolute.** No agent, supervisor, or human operator may override a P0
or P1 classification except to escalate it further. An agent that attempts to reclassify
a P0 as P2 to pass a gate is exhibiting the Trim-to-Pass anti-pattern (see
`anti-pattern-firewall.md`).

---

## Classification Criteria

Agents must use objective criteria to assign severity — not qualitative judgment alone.
Apply the following decision tree:

```
Is there a crash, data loss, or security/compliance breach?
  YES → P0 (Critical)
  NO  ↓

Is a core feature broken or completely unavailable to users?
  YES → P1 (Major)
  NO  ↓

Is functionality degraded but still partially available?
  YES → P2 (Minor)
  NO  ↓

Is the issue purely cosmetic or a polish improvement?
  YES → P3 (Cosmetic)
```

When uncertain between two levels, **escalate to the higher severity**. Downgrading
requires explicit rationale and is a P2 gap if done without documentation.

---

## Mandatory Inclusions in Agent Prompts

Every agent that performs quality assessment, code review, security review, or pipeline
gating must include the following in its identity prompt:

```markdown
## Defect Severity Classification

All defects are classified using the organisational severity vocabulary:

- **P0 — Critical:** Crash, data loss, security/compliance breach. Non-negotiable.
  Block release. No override authority.
- **P1 — Major:** Core feature broken, major UX failure, data integrity concern.
  Non-negotiable. Block release. No override authority.
- **P2 — Minor:** Partial degradation, non-blocking issue. User decides.
- **P3 — Cosmetic:** Polish, style, nice-to-have. User decides.

P0 and P1 findings are never reclassified downward. When uncertain, escalate.
```

This inclusion is **required** per the ASE Compliance Standard, Layer 1.

---

## In Pipeline Gating

Quality gates evaluate severity distributions, not individual defect counts:

| Gate condition                 | Action                                 |
| ------------------------------ | -------------------------------------- |
| Any P0 defect present          | Gate holds. Release blocked.           |
| Any P1 defect present          | Gate holds. Release blocked.           |
| P2 defects present, none P0/P1 | Gate passes with notification to user. |
| P3 defects only                | Gate passes. Defects logged.           |

---

## Cross-Agent Consistency

When multiple agents assess the same artifact (e.g., a security agent and a code
review agent both review the same PR), their severity assignments must be reconcilable:

- If both agents agree on severity: adopt the shared classification.
- If agents disagree: the **higher severity classification wins** and is recorded in the
  audit trail with both agents' rationales.
- The disagreement is not resolved by negotiation — it is escalated to the supervisor
  agent, who documents the resolution.

---

## ASE Layer Alignment

| Issue Type                        | Applies At Layer | Severity Reference Used By          |
| --------------------------------- | ---------------- | ----------------------------------- |
| Prompt quality gaps               | Layer 1          | Code review, quality gate agents    |
| Context assembly failures         | Layer 2          | Integration agent, supervisor agent |
| Harness / execution failures      | Layer 3          | Harness error boundary, QA agents   |
| Retrieval accuracy issues         | Layer 4          | RAG evaluation agent                |
| Multi-agent coordination failures | Layer 5          | Integration agent, supervisor agent |

---

## Related Patterns

- [`anti-pattern-firewall.md`](./anti-pattern-firewall.md) — Explicitly prohibits
  severity reclassification as a forbidden behaviour
- [`progress-sync-protocol.md`](./progress-sync-protocol.md) — Uses severity
  vocabulary to classify detected variance events
- [`canonical-source-of-truth.md`](./canonical-source-of-truth.md) — This vocabulary
  is defined in the canonical source and referenced by all agent adapters

## CC-00 References

- `core-component-00/harness-engineering/patterns/prompt-templates.md` — Error boundary
  prompts that reference this severity vocabulary
- `core-component-00/multi-agent-engineering/patterns/orchestration-patterns.md` —
  Pipeline pattern's quality gate mechanism
