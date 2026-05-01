---
version: "1.0.0"
---

# ADR Governance

| Competency                  | Description                                                                                   | Quality Criteria                                                                                                                           |
| --------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| ADR Lifecycle Management    | Proposed → Accepted → Superseded → Deprecated states, state transitions, governance           | Manages ADR state machine with clear transition criteria; ensures no ADR remains in "proposed" indefinitely; tracks supersession chains    |
| ADR Template Standards      | Context, decision, consequences, alternatives sections; severity levels; metadata             | Enforces consistent ADR structure across all teams; tailors templates for decision complexity; ensures all required sections are populated |
| Architecture Review Process | Review panel composition, review cadence, escalation paths, decision authority                | Designs review process appropriate for decision severity; ensures diverse perspectives in review panels; maintains review SLAs             |
| Decision Traceability       | PRD requirements → ADRs → implementation, impact analysis, dependency mapping                 | Maps every ADR to upstream requirements and downstream implementation; identifies affected components when ADR changes                     |
| ADR Quality Assessment      | Completeness check, rationale quality, alternative analysis depth, consequence identification | Evaluates ADRs against quality rubric; identifies gaps in reasoning; ensures alternatives are fairly evaluated                             |

## Execution Guidance

### ADR Lifecycle Management

```
ADR State Machine:

  ┌──────────┐     Review      ┌───────────┐
  │ PROPOSED │ ──────────────▶ │ ACCEPTED  │
  │          │                 │           │
  └──────────┘                 └─────┬─────┘
       ▲                             │
       │  Revision requested          │ Implementation reveals issues
       │                             ▼
  ┌──────────┐                 ┌─────────────┐
  │ REVISING │ ◀────────────── │ SUPERSEDED  │
  └──────────┘  New ADR needed └─────────────┘
                                     │
                                     ▼
                               ┌─────────────┐
                               │ DEPRECATED  │
                               │ (obsolete)  │
                               └─────────────┘
```

**State transition criteria:**

| Transition              | Criteria                                                            | Authority                 |
| ----------------------- | ------------------------------------------------------------------- | ------------------------- |
| Proposed → Accepted     | Review panel approves, all sections complete, alternatives analyzed | Architecture Review Board |
| Proposed → Revising     | Review identifies gaps or concerns                                  | Any reviewer              |
| Accepted → Superseded   | New decision replaces old one, new ADR created                      | Architecture Review Board |
| Accepted → Deprecated   | Technology/practice is obsolete, no replacement needed              | CTO or Architect          |
| Superseded → Deprecated | Superseding ADR has been fully implemented                          | CTO                       |

**ADR numbering and organization:**

```
architecture/decisions/
├── ADR-001.md  — Use PostgreSQL as primary database
├── ADR-002.md  — Adopt microservices architecture
├── ADR-003.md  — Use Kafka for event streaming
├── ADR-004.md  — API versioning strategy (Supersedes ADR-012)
├── ADR-005.md  — Authentication with OAuth2 + JWT
├── ...
├── adr-template.md
├── README.md           # Index of all ADRs with status
└── superseded/
    └── ADR-012.md      — API versioning via query parameters (superseded by ADR-004)
```

### ADR Template Standards

```markdown
# ADR-NNN: [Decision Title]

## Metadata

| Field          | Value                                         |
| -------------- | --------------------------------------------- |
| **Status**     | Proposed / Accepted / Superseded / Deprecated |
| **Severity**   | High / Medium / Low                           |
| **Author**     | [Name]                                        |
| **Reviewers**  | [Names]                                       |
| **Created**    | YYYY-MM-DD                                    |
| **Updated**    | YYYY-MM-DD                                    |
| **Supersedes** | ADR-XXX (if applicable)                       |
| **Tags**       | [database, architecture, security, etc.]      |

## Context

[2-3 paragraphs describing the problem, constraints, and forces at play.
Include relevant data, metrics, or observations that inform the decision.
Link to PRD requirements, user research, or incident reports if applicable.]

### Constraints

- [List technical, business, or regulatory constraints]
- [Budget limitations, timeline pressures, team expertise]

### Stakeholders

- [Who is affected by this decision]
- [Who needs to be consulted]

## Decision

[Clear, concise statement of the decision. Use "We will..." format.]

We will adopt [technology/approach] because [primary rationale].

### Rationale

[Bullet points explaining why this decision was made:]

- [Reason 1 with supporting data]
- [Reason 2 with supporting data]
- [Trade-off acknowledgment]

### Implications

[What changes as a result of this decision:]

- [Positive implications]
- [Negative implications / costs]
- [Migration requirements]
- [Training needs]

## Alternatives Considered

### Alternative 1: [Name]

**Description:** [Brief description]

**Pros:**

- [Advantage 1]
- [Advantage 2]

**Cons:**

- [Disadvantage 1]
- [Disadvantage 2]

**Why rejected:** [Specific reason this was not selected]

### Alternative 2: [Name]

[Same structure]

## Consequences

### Positive

- [Benefit 1]
- [Benefit 2]

### Negative

- [Cost 1]
- [Risk 1 with mitigation]

### Risks

| Risk               | Likelihood   | Impact       | Mitigation            |
| ------------------ | ------------ | ------------ | --------------------- |
| [Risk description] | High/Med/Low | High/Med/Low | [Mitigation strategy] |

## Compliance

- [ ] Aligned with PRD requirements
- [ ] Security review completed
- [ ] Performance impact assessed
- [ ] Cost analysis completed
- [ ] Team capabilities evaluated

## References

- [Link to related ADRs]
- [Link to evaluation documents]
- [Link to benchmark results]
```

### Architecture Review Process

**Review severity classification:**

| Severity   | Scope                                           | Review Panel                            | SLA             | Examples                                                        |
| ---------- | ----------------------------------------------- | --------------------------------------- | --------------- | --------------------------------------------------------------- |
| **High**   | Company-wide, irreversible, > $100K cost        | CTO, CIO, CSO, affected leads           | 5 business days | Database selection, architecture pattern, authentication system |
| **Medium** | Team-level, reversible with effort, > $10K cost | Architect, team lead, relevant engineer | 3 business days | Library selection, API design pattern, caching strategy         |
| **Low**    | Implementation detail, easily reversible        | Tech lead or senior engineer            | 1 business day  | Utility library choice, code style, logging format              |

**Review process flow:**

```
1. Author drafts ADR (using template)
2. Author self-reviews against quality checklist
3. ADR submitted for review (status: PROPOSED)
4. Reviewers have SLA period to review
   a. Each reviewer adds comments/concerns
   b. Author addresses concerns (may revise)
5. Review panel meets (for High severity) or async approval (Medium/Low)
6. Decision recorded:
   a. ACCEPTED → Implementation begins
   b. REVISING → Author addresses concerns, re-submits
   c. REJECTED → Decision documented with rationale
7. Accepted ADR linked to implementation tasks
8. Implementation validated against ADR during code review
9. ADR superseded when replacement decision is made
```

**Review checklist:**

```markdown
# ADR Quality Checklist

## Completeness

- [ ] All template sections populated
- [ ] Context explains the "why" not just the "what"
- [ ] Decision statement is clear and unambiguous
- [ ] At least 2 alternatives considered
- [ ] Consequences include both positive and negative
- [ ] Risks identified with mitigations

## Reasoning Quality

- [ ] Rationale supported by data (benchmarks, surveys, incidents)
- [ ] Trade-offs explicitly acknowledged
- [ ] Alternatives evaluated fairly (no straw-man arguments)
- [ ] Decision aligns with company architecture principles
- [ ] Decision aligns with business objectives

## Practicality

- [ ] Implementation effort estimated
- [ ] Migration path defined (if replacing existing)
- [ ] Team capability assessed
- [ ] Cost analysis included
- [ ] Rollback plan defined (if applicable)

## Traceability

- [ ] Linked to PRD requirements
- [ ] Linked to related ADRs
- [ ] Tags correctly assigned
- [ ] Stakeholders identified
```

### Decision Traceability

```
Traceability Matrix:

PRD Requirement → ADR → Implementation → Test

Example:
  PRD-012: "System must handle 10K concurrent users"
    → ADR-002: "Adopt microservices architecture"
      → Component: API Gateway (Envoy)
      → Component: Service mesh (Istio)
      → Implementation: platforms/*/code/gateway/
        → Test: testing/load/concurrent-users.test.ts
```

**ADR index with traceability:**

```markdown
# ADR Index

| #   | Title                        | Status     | Severity | PRD Link | Implementation         |
| --- | ---------------------------- | ---------- | -------- | -------- | ---------------------- |
| 001 | PostgreSQL as primary DB     | Accepted   | High     | PRD-003  | database/schema/       |
| 002 | Microservices architecture   | Accepted   | High     | PRD-012  | architecture/          |
| 003 | Kafka for event streaming    | Accepted   | High     | PRD-015  | messaging/             |
| 004 | API versioning: URL path     | Accepted   | Medium   | PRD-020  | routes/v1/, routes/v2/ |
| 005 | OAuth2 + JWT auth            | Accepted   | High     | SRD-001  | auth/                  |
| 012 | API versioning: query params | Superseded | Medium   | PRD-020  | —                      |
```

**Impact analysis when ADR changes:**

```markdown
# Impact Analysis: ADR-002 Change Proposal

## Proposed Change

Switch from microservices to modular monolith.

## Affected ADRs

- ADR-003 (Kafka event streaming) — May need simplification
- ADR-007 (Service mesh) — Would be superseded
- ADR-011 (Distributed tracing) — Scope reduced

## Affected Implementation

- Service decomposition → Module boundaries
- Network communication → In-process calls
- Deployment units → Single deployable
- Team structure → Feature teams vs service teams

## Affected Tests

- Integration tests across services → Module integration tests
- Chaos engineering tests → Not needed
- Performance tests → Different baseline

## Migration Effort

- Estimated: 8-12 weeks
- Risk: High (architectural change mid-project)
- Recommendation: Only if compelling evidence outweighs migration cost
```

### ADR Quality Assessment Rubric

```markdown
# ADR Quality Scoring

Score each dimension 1-5 (1=Poor, 5=Excellent):

| Dimension                | Score | Notes                                   |
| ------------------------ | ----- | --------------------------------------- |
| **Context clarity**      |       | Does it explain the problem well?       |
| **Decision specificity** |       | Is the decision actionable?             |
| **Rationale strength**   |       | Is reasoning data-driven?               |
| **Alternative depth**    |       | Are alternatives fairly evaluated?      |
| **Consequence honesty**  |       | Are negative consequences acknowledged? |
| **Risk identification**  |       | Are risks realistic with mitigations?   |
| **Traceability**         |       | Can implementation be traced back?      |

## Scoring Guide

- 28-35: Excellent — Approve
- 21-27: Good — Approve with minor comments
- 14-20: Needs improvement — Request revisions
- 7-13: Inadequate — Reject, restart

## Common Quality Issues

1. **Straw-man alternatives** — Alternatives presented unfairly to make decision look better
2. **Missing consequences** — Only positive outcomes listed
3. **Vague decision** — "We will consider X" is not a decision
4. **No data** — Decisions based on opinion without evidence
5. **No rollback plan** — Irreversible decisions without exit strategy
6. **Stakeholder blind spots** — Affected teams not consulted
```

## Pipeline Integration

**Stage 3 (UML Engineering Package):** ADRs are primary output alongside UML diagrams and TSD. Each ADR reviewed per severity level. ADR index maintained with traceability to PRD requirements.

**Stage 4 (Implementation Plan):** Accepted ADRs linked to implementation tasks. Superseded ADRs documented with migration plan. ADR compliance checklist included in implementation review.

**Stage 6 (Code Review):** Code review validates implementation against accepted ADRs. Deviations require ADR amendment or new ADR.

**Stage 8 (Integrity Verification):** Panel verifies that implementation matches ADR decisions. Superseded ADRs properly archived. ADR index up to date.

## Quality Standards

| Metric                           | Target                                        | Measurement            |
| -------------------------------- | --------------------------------------------- | ---------------------- |
| ADR coverage                     | 100% of significant decisions documented      | Architecture audit     |
| ADR review SLA compliance        | > 95% reviewed within SLA                     | Review timing metrics  |
| ADR quality score                | Average > 25/35                               | Quality rubric scoring |
| Decision traceability            | 100% of ADRs linked to PRD and implementation | Traceability matrix    |
| Superseded ADR cleanup           | < 5% of ADRs in superseded state              | ADR index audit        |
| ADR compliance in implementation | 100% implementation matches accepted ADRs     | Code review findings   |
