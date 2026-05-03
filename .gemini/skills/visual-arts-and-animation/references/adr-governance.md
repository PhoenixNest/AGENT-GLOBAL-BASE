---
name: adr-governance
description: Architecture Decision Record authorship and governance — ADR format, when to write one, technology decision lock at Stage 3, architecture review board process, and cross-functional decision documentation. Use at Stage 3 (Prototype → UML Engineering Package) for any architecture decision that affects multiple teams or locks technology choices.
version: "1.0.0"
---

# ADR Governance

## Purpose

Document every significant architecture decision in a way that future engineers can understand: what was decided, why, and what alternatives were rejected. Architecture decisions without ADRs are folklore — they survive in the heads of the original team and evaporate the moment people leave. An ADR is not bureaucracy; it is the engineering organization's institutional memory.

## Why This Matters

The company pipeline locks technology decisions at Stage 3 (Prototype → UML Engineering Package). Any post-Stage 3 request to change the technology stack requires a new ADR and a full Stage 3 re-entry — not a quiet edit. ADR governance is the enforcement mechanism for this rule. Without it, decisions drift, teams misremember what was agreed, and the CTO + CIO cannot sign off on a package they cannot trace.

## ADR Format (Company Standard)

```markdown
# ADR-[NNN]: [Short Imperative Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Superseded by ADR-[NNN] | Deprecated
**Deciders:** [Names of decision-makers; minimum: CTO + Elena V. + any affected VP]
**Stage:** Stage 3 — Prototype → UML Engineering Package

## Context

[What is the architectural situation that requires a decision? Be specific about the forces in play: scale requirements, team constraints, existing systems, contractual obligations. 2–4 paragraphs.]

## Decision

[What is the decision? State it clearly and without hedging. "We will use X" — not "we might consider X".]

## Alternatives Considered

| Alternative | Reason Rejected                                          |
| ----------- | -------------------------------------------------------- |
| Option B    | [Specific, technical reason — not "we didn't have time"] |
| Option C    | [Specific, technical reason]                             |

## Consequences

**Positive:**

- [Specific, measurable benefit]
- [Specific, measurable benefit]

**Negative / Trade-offs:**

- [Honest trade-off]
- [Migration cost or lock-in risk]

**Risks:**

- [Known risk] — Mitigation: [specific plan]

## Compliance

- [ ] CTO reviewed and approved
- [ ] CIO reviewed (if ADR involves security-affecting decisions)
- [ ] Affected VP(s) reviewed
- [ ] Added to the TSD (Technology Selection Document) if it selects a new tool/framework
```

## When to Write an ADR

An ADR is required for any decision that:

| Trigger                                                        | Example                                          |
| -------------------------------------------------------------- | ------------------------------------------------ |
| Selects or replaces a technology used by >1 team               | Choosing Kafka over RabbitMQ for event streaming |
| Establishes an architecture pattern across services            | Adopting CQRS for all write-heavy services       |
| Introduces a new external dependency                           | Adding a third-party auth provider               |
| Changes the data model in a way that affects multiple services | Adding a new shared domain event schema          |
| Relaxes or tightens a cross-cutting constraint                 | Changing the P99 latency SLO from 500ms to 200ms |
| Resolves a cross-team technical disagreement                   | Backend vs. mobile on API versioning strategy    |

**Does not require an ADR:** Library version upgrades, adding a field to a single service's schema, infrastructure scaling (adding replicas), build tooling changes.

## Architecture Review Board (ARB) Process

For ADRs with `Status: Proposed`, Elena convenes the ARB within 5 business days:

| Role               | Participant                    | Decision Authority                        |
| ------------------ | ------------------------------ | ----------------------------------------- |
| Chair              | Elena Vasquez (VP Web-Backend) | Facilitates; casts deciding vote on tie   |
| CTO representative | Dr. Kenji Nakamura             | Final veto authority                      |
| Security review    | Dr. Priya Mehta (CIO)          | Required if ADR affects security controls |
| Affected VP(s)     | Relevant VP(s)                 | Input; must acknowledge trade-offs        |
| Author             | Whoever wrote the ADR          | Presents; answers questions               |

ARB decisions are recorded in the ADR's Status field and signed by all deciders. A Stage 3 UML Engineering Package with unsigned ADRs is incomplete — CTO will not approve it.

## Stage 3 Technology Decision Lock

Once a Stage 3 UML Engineering Package receives user approval:

1. All ADRs in that package transition to `Status: Accepted`
2. The Technology Selection Document (TSD) is frozen
3. **Any request to change a locked technology choice must:** (a) draft a new ADR, (b) identify all downstream impacts, (c) route through the ARB, (d) trigger a full Stage 3 re-entry
4. No VP, including Elena, may approve a technology change by verbal agreement after Stage 3 lock — it requires a new ADR

## ADR Index (Per Project)

Elena maintains an ADR index in Confluence for each active project:

```markdown
# ADR Index — [Project Name]

| ADR     | Title                                      | Status   | Date       | Stage   |
| ------- | ------------------------------------------ | -------- | ---------- | ------- |
| ADR-001 | Use PostgreSQL + event sourcing for orders | Accepted | 2026-03-15 | Stage 3 |
| ADR-002 | Adopt gRPC for inter-service communication | Accepted | 2026-03-15 | Stage 3 |
| ADR-003 | Use Kafka for async event streaming        | Accepted | 2026-03-20 | Stage 3 |
```

## Quality Standards

- Every Stage 3 UML Engineering Package contains at least one ADR per major technology selection
- Zero undocumented technology decisions entering Stage 5 (Software Development)
- ARB convened within 5 business days of any `Proposed` ADR
- Post-Stage 3 technology change requests that bypassed the ADR process are classified as P1 governance defects
