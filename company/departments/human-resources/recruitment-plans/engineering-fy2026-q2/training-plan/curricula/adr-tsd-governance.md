# ADR/TSD Governance Training

## Module Objectives

After completing this module, the trainee must be able to:

1. Independently produce an Architecture Decision Record (ADR) meeting company standard
2. Classify ADRs using the 3-tier classification system
3. Understand Technology Selection Document (TSD) compliance requirements
4. Navigate the ADR review and sign-off workflow

## Trainees

| Trainee          | Role                            | Deadline | Verification                                   |
| ---------------- | ------------------------------- | -------- | ---------------------------------------------- |
| Marcus Andersson | VP of Mobile Engineering        | Day 30   | Produce 1 compliant ADR independently          |
| Elena Vasquez    | VP of Web & Backend Engineering | Day 30   | Produce 1 compliant ADR independently          |
| Natalia Petrova  | Security Architect              | Day 30   | Produce 1 ADR covering non-security dimensions |

## Prerequisites

None required.

## Course Structure

### Session 1: ADR Structure and Lifecycle (2 hours, led by CIO + CTO)

**Topics covered:**

**ADR Document Structure:**

```markdown
# ADR-{NNN}: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD
**Author:** [Name, Role]
**Reviewers:** [Names, Roles]
**Sign-off Authority:** [Per ADR classification]

## Context

[What is the issue? What forces are at play? Why is a decision needed?
Include relevant background: system constraints, business requirements,
technical limitations, timeline pressures. 2-4 paragraphs.]

## Decision

[What is the decision? State it clearly and specifically.
This should be unambiguous — a reader should know exactly
what was decided without reading the alternatives.]

## Consequences

[What are the outcomes of this decision? Both positive and negative.
Include: impact on architecture, cost, timeline, team, risk.]

## Alternatives Considered

[List 2-3 alternatives that were evaluated and why they were rejected.
Include: alternative description, pros, cons, reason for rejection.]

## Compliance

[For Architecture-Impacting ADRs: how does this decision align with
the TSD? If it deviates, what is the deviation rationale?]
```

**Status Transitions:**

```
Draft → Proposed → (Review) → Accepted
                     ↓
                 Rejected (requires revision)
                     ↓
                 Deprecated (later decision supersedes)
```

**Versioning:** All ADRs follow `architecture/decisions/v{N}/ADR-{NNN}.md` folder structure with `VERSIONS.md` index.

### Session 2: TSD Compliance Framework (2 hours, led by CIO)

**Topics covered:**

**What is the TSD?** The Technology Selection Document records which technologies, frameworks, and platforms have been approved for use in the project. It is owned by the CTO and CIO, established at Stage 3 (Architecture), and locked for the duration of development.

**TSD Compliance Enforcement:**

- Dependency allowlists managed via automated tooling (Dependabot allowlists, custom package registry)
- Import linting rules prevent use of unapproved frameworks
- CI/CD pipeline gates block PRs introducing unapproved technology

**TSD Deviation Request Process:**

1. Engineer identifies need for technology not in TSD
2. Technology evaluation request submitted to CIO + CTO
3. CIO evaluates: security, licensing, community health, alternatives
4. CTO evaluates: architectural fit, maintenance burden, team expertise
5. Decision documented as ADR; if approved, TSD updated

### Session 3: 3-Tier ADR Classification (2 hours, led by CIO + CTO)

| Tier                       | Description                                                                     | Sign-off Authority                   | Example                                                                    |
| -------------------------- | ------------------------------------------------------------------------------- | ------------------------------------ | -------------------------------------------------------------------------- |
| **Architecture-Impacting** | Changes system architecture, technology selection, or cross-division interfaces | CIO sign-off required                | "Adopt Kotlin Multiplatform for shared business logic"                     |
| **Implementation-Detail**  | Internal design decisions within a single chapter                               | Senior Architect sign-off sufficient | "Use StateFlow instead of SharedFlow for UI state in Android login screen" |
| **Informational**          | Documents existing decisions; no new decision                                   | Logged only, no sign-off required    | "Record of current payment processing architecture for future reference"   |

**Decision Matrix for Classification:**

| Question                                             | If Yes | Classification         |
| ---------------------------------------------------- | ------ | ---------------------- |
| Does this change technology selection?               | Yes    | Architecture-Impacting |
| Does this change cross-division interfaces?          | Yes    | Architecture-Impacting |
| Does this introduce a new framework/dependency?      | Yes    | Architecture-Impacting |
| Does this change data model or persistence strategy? | Yes    | Architecture-Impacting |
| Is this contained within one team's codebase?        | Yes    | Implementation-Detail  |
| Is this documenting an existing decision?            | Yes    | Informational          |

### Session 4: Self-Directed ADR Drafting (4 hours, trainee works independently)

Each trainee drafts 1 ADR for a real or hypothetical architecture decision in their domain:

| Trainee          | ADR Topic                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------ |
| Marcus Andersson | "Adopt KMP shared module for authentication flow across Android and iOS"                         |
| Elena Vasquez    | "Migrate payments backend from monolithic Java/Spring to event-driven microservices using Kafka" |
| Natalia Petrova  | "Implement zero-trust mTLS for all internal service communication"                               |

### Session 5: ADR Review and Feedback (1 hour, led by CIO + CTO)

- Trainee presents their drafted ADR
- CIO + CTO review against ADR template standards
- Feedback provided on: clarity, completeness, alternatives analysis, consequences assessment, TSD alignment
- Trainee revises and resubmits if needed

## Verification Method

**Deliverable:** 1 independently produced ADR meeting company standard

**Review Checklist (CIO + CTO):**

| Criterion                                                          | Pass                                        | Fail                                  |
| ------------------------------------------------------------------ | ------------------------------------------- | ------------------------------------- |
| Context is specific, complete, and self-contained                  | 2+ paragraphs with concrete background      | Vague, incomplete, or missing context |
| Decision is stated clearly and unambiguously                       | Reader knows exactly what was decided       | Decision is hedged or ambiguous       |
| Consequences include both positive and negative outcomes           | At least 2 of each                          | Missing or one-sided                  |
| Alternatives include ≥2 options with pros/cons/rejection rationale | 2+ alternatives with full analysis          | 0-1 alternatives or no analysis       |
| Classification tier is correct                                     | Matches decision matrix criteria            | Incorrect tier selected               |
| TSD alignment addressed (for Architecture-Impacting)               | Explicit compliance or deviation documented | Not addressed                         |
| Status transitions are correct                                     | Follows Draft → Proposed → Accepted flow    | Skips stages or incorrect status      |

## Pass/Fail Criteria

**PASS:** ADR meets all 7 checklist criteria on first or second submission (one revision cycle allowed).

**FAIL:** ADR fails any criterion after second submission. This indicates the trainee cannot independently produce compliant architecture documentation — position reopened for recruitment.

**Deadline:** Day 30 of probationary period. No extensions.

## Resources

- ADR template: `company/library/topics/architecture.md` (ADR section)
- Example ADRs: `company/project/*/architecture/decisions/v{N}/ADR-{NNN}.md`
- TSD template: `company/project/*/architecture/technology/TSD.md`
- ADR classification decision matrix: this document, Session 3
