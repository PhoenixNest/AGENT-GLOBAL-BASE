---
name: company-architecture-decision-records
description: ADR authorship — context-decision-consequence structure, alternatives analysis, UML-embedded records, traceability from product requirement to architectural choice, success/failure criteria. Owned by Rafael Okonkwo (Software Architect).
disable-model-invocation: false
---

# Architecture Decision Records (ADRs)

## Purpose

Document every significant architectural decision as a traceable, permanent record. An ADR answers: what was the context, what decision was made, what alternatives were considered, and what are the consequences. ADRs are immutable once approved — they record history, not current state. If a decision changes, a new ADR is written that supersedes the old one.

## ADR Template

```markdown
---
adr-id: ADR-{NNN}
title: {Short imperative title — e.g., "Use Hilt for dependency injection on Android"}
status: [Proposed | Accepted | Superseded by ADR-{NNN} | Deprecated]
date: YYYY-MM-DD
deciders: [CTO, CIO, Software Architect]
supersedes: [ADR-{NNN} | N/A]
---

## Context

[2–4 sentences. What is the problem or situation that requires a decision?
What constraints exist (platform, performance, team capability, timeline)?
What forces are in tension?]

## Decision

[1–2 sentences. The decision, stated directly in active voice.
"We will use X" not "It was decided that X would be used."]

## Alternatives Considered

| Option          | Pros   | Cons   | Eliminated Reason |
| --------------- | ------ | ------ | ----------------- |
| [Option A]      | [pros] | [cons] | [why rejected]    |
| [Option B]      | [pros] | [cons] | [why rejected]    |
| [Chosen option] | [pros] | [cons] | N/A — selected    |

## Consequences

**Positive:**

- [Consequence 1]
- [Consequence 2]

**Negative / Trade-offs:**

- [Consequence 1]
- [Consequence 2]

**Risks:**

- [Risk 1 — and how it is mitigated]

## UML Reference

[Embed or link the relevant diagram that shows this decision's effect on the architecture.
If a class or component diagram illustrates the decision, include it here as PlantUML source.]

## Traceability

- **PRD requirement:** [Section and requirement number that motivated this decision]
- **SRD requirement:** [If security-motivated, cite the SRD section]
- **Superseded by:** [ADR-NNN if this decision is later overridden]
```

## ADR Numbering

ADRs are numbered sequentially per project: `ADR-001`, `ADR-002`, etc.
A project-level `ADR-INDEX.md` lists all ADRs with status and one-line summary.

## When to Write an ADR

Write an ADR for every decision that:

- Affects more than one module or platform
- Cannot be easily reversed without significant rework
- Involves a technology selection (library, framework, API, database)
- Establishes a pattern that other engineers will follow
- Is controversial or had meaningful alternatives

Do NOT write an ADR for:

- Implementation details within a single function or class
- Naming conventions (document in a style guide instead)
- Decisions with no meaningful alternatives

## ADR Review and Approval

1. Architect drafts ADR and circulates to CTO and CIO
2. CTO and CIO review: does the decision align with the TSD and SRD?
3. If approved: status → `Accepted`, date recorded
4. If rejected: Architect revises and resubmits
5. Accepted ADRs are immutable — any change requires a new superseding ADR

## ADR Index Format

```markdown
# ADR Index — {Project Name}

| ID      | Title   | Status   | Date       | Deciders            |
| ------- | ------- | -------- | ---------- | ------------------- |
| ADR-001 | [title] | Accepted | YYYY-MM-DD | CTO, CIO, Architect |
| ADR-002 | [title] | Accepted | YYYY-MM-DD | CTO, CIO, Architect |
```
