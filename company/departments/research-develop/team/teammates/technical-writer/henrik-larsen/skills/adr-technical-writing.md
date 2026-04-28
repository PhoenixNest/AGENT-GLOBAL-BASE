---
name: adr-technical-writing
description: >
  ADR and TSD technical writing for mobile architecture — structured ADR authoring, decision documentation, Technology Selection Document synthesis, and editorial standards for engineering audiences. Owned by Henrik Larsen (Technical Writer). Use during Stage 3 (UML Engineering) for ADR/TSD production and Stage 4 (Implementation Plan) for decision traceability. Trigger: ADR writing, technical documentation, TSD authoring, decision documentation, architecture documentation, technical writing.
version: "1.0.0"
---

ADR and TSD technical writing skill for Henrik Larsen — Technical Writer (R&D department).
Produces architecture documentation, ADR/TSD templates, UML diagrams, and pipeline documentation.

## Owner

Henrik Larsen — Technical Writer, Research & Development department.
Reports to: CTO office (primary), Software Architect (dotted-line).
Pipeline stages: 3, 4, 6, 8, 10.

## When to Invoke

- Authoring Architecture Decision Records (ADRs) from raw decision notes during Stage 3 architecture sessions
- Synthesizing multiple technology evaluations into a Technology Selection Document (TSD)
- Facilitating decision-capture sessions with architects and engineers
- Managing ADR lifecycle (draft → superseded → accepted → deprecated) with proper versioning
- Translating complex architectural concepts into precise, accessible prose for engineering audiences
- Enforcing consistent formatting, terminology, and structural conventions across architecture documents
- Reviewing architecture documentation accuracy during code review (Stage 6) and integrity verification (Stage 8)

## Competencies

| Competency                    | Description                                                                                                   | Quality Criteria                                                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| ADR Authoring                 | Write clear, structured ADRs that capture decision context, options, rationale, and consequences              | Publication-ready ADR from raw decision notes in ≤4 hours; zero structural rejections from CTO                  |
| Decision Documentation        | Facilitate decision-capture sessions with architects and engineers; extract signal from discussion            | Captures ≥95% of key decision points from architecture meetings; validates accuracy with decision-makers        |
| TSD Writing                   | Synthesize multiple technology evaluations into a coherent Technology Selection Document                      | TSD passes CIO+CTO review on first submission; covers all evaluated technologies with clear selection rationale |
| Technical Communication       | Translate complex architectural concepts into precise, accessible prose for engineering audiences             | Engineers rate documentation clarity ≥4.3/5; zero ambiguity-related defects traced to ADR content               |
| Documentation Version Control | Manage ADR lifecycle (draft → superseded → accepted → deprecated) with proper versioning and cross-references | ADR catalog has zero orphaned or conflicting records; supersession chains are complete and traceable            |
| Editorial Standards           | Enforce consistent formatting, terminology, and structural conventions across all architecture documents      | Style audit passes ≥95%; terminology consistency score ≥98% across ADR catalog                                  |

## Execution Guidance

### ADR Template

Every ADR follows this canonical structure:

```markdown
# ADR-NNN: [Short Decision Title]

**Status:** [Proposed | Accepted | Superseded | Deprecated]
**Date:** [YYYY-MM-DD]
**Author:** [Name, Role]
**Reviewers:** [CTO, CIO, Software Architect]
**Stage:** [Stage 3 — Architecture]
**Supersedes:** [ADR-XXX or "N/A"]

## Context

[2-4 paragraphs describing the problem, constraints, and upstream artifacts]

## Decision Drivers

- [Driver 1: e.g., "Must support offline-first per PRD requirement R-012"]

## Options Considered

### Option A: [Name]

[Description, pros, cons, effort estimate]

## Decision

**Selected Option:** [Option A/B/C]
**Rationale:** [2-3 paragraphs referencing decision drivers explicitly]

## Consequences

### Positive / Negative (Accepted Trade-offs) / Risks

## Implementation Notes

[Guidance for engineers implementing this decision]

## References

[Links to UML diagrams, TSD sections, PRD requirements, SRD controls]
```

### ADR Lifecycle

| Status         | Definition                                      | Trigger                             | Action                                                        |
| -------------- | ----------------------------------------------- | ----------------------------------- | ------------------------------------------------------------- |
| **Proposed**   | ADR drafted but not yet reviewed                | Author completes draft              | Submitted to CTO + CIO for review                             |
| **Accepted**   | ADR reviewed and approved                       | CTO/CIO sign-off                    | Merged to `architecture/decisions/`; referenceable downstream |
| **Superseded** | Replaced by a newer ADR with different decision | New ADR explicitly supersedes       | Status updated; cross-reference added; document preserved     |
| **Deprecated** | Decision no longer applies                      | CTO determines decision is obsolete | Status updated; reason documented; document preserved         |

### Writing Principles

| Principle                             | Application                                                                               |
| ------------------------------------- | ----------------------------------------------------------------------------------------- |
| **Decision-centric, not descriptive** | ADRs record decisions, not tutorials. Every section serves the decision narrative.        |
| **Specific over general**             | "We chose Room over SQLiteOpenHelper because..." not "We chose a good database solution." |
| **Acknowledge trade-offs honestly**   | Document real downsides. Future engineers need to understand the cost.                    |
| **Reference, don't repeat**           | Link to UML diagrams, PRD requirements, and SRD controls rather than restating them.      |
| **Write for the future reader**       | Assume no context. Explain acronyms on first use.                                         |
| **Immutable once accepted**           | Accepted ADRs are never edited. If a decision changes, write a new superseding ADR.       |

### TSD Structure

The Technology Selection Document aggregates all Stage 3 technology evaluations:

- **Executive Summary** — 1-2 paragraph overview of selections and PRD/SRD alignment
- **Selection Methodology** — Evaluation criteria, scoring model, decision authority, timeline
- **Technology Evaluations** — Per-category weighted scorecards (functionality 30%, performance 20%, security 20%, team fit 15%, TCO 10%, ecosystem 5%)
- **Selected Technology Stack** — Table of selected technologies with versions and ADR references
- **Locked Decisions** — Explicit statement that decisions are locked at Stage 3 gate approval

Detailed ADR lifecycle management workflows, decision documentation best practices, TSD writing guidelines, version control workflows, and technical communication standards are maintained as internal reference materials.

## Pipeline Integration

| Pipeline Stage                   | ADR/TSD Relevance                                                                                                         |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Stage 1–2                        | Not applicable — ADRs not yet in scope                                                                                    |
| Stage 3 (Architecture)           | **Primary stage** — ADRs authored, reviewed, and accepted; TSD compiled and locked                                        |
| Stage 4 (Implementation Plan)    | ADRs referenced in implementation plan; no new ADRs unless architectural gap discovered (CTO approval required)           |
| Stage 5 (Development)            | Implementation notes in ADRs guide developers; no ADR changes unless critical issue discovered (superseding ADR required) |
| Stage 6 (Code Review)            | Code reviewed against ADR decisions; deviations flagged as defects                                                        |
| Stage 7 (Testing)                | Test architecture references ADR decisions on testing frameworks and strategies                                           |
| Stage 8 (Integrity Verification) | Panel verifies implementation matches ADR decisions; deviations without superseding ADR are P1 defects                    |
| Stage 9 (i18n)                   | Not applicable — localization decisions tracked separately                                                                |
| Stage 10 (Release)               | ADR catalog reviewed as part of architecture sign-off (Release Checklist item 3)                                          |

## Quality Standards

- **ADR Completeness:** 100% of accepted ADRs contain all required sections (Context, Decision Drivers, Options Considered, Decision, Consequences, Implementation Notes, References)
- **Review Turnaround:** ADR drafts reviewed by CTO/CIO within 3 business days; zero ADRs stalled in review for >5 business days
- **Structural Integrity:** Zero ADRs rejected for structural deficiencies (missing sections, incorrect format, orphaned cross-references)
- **TSD Accuracy:** 100% of technology selections in TSD have corresponding accepted ADRs; zero TSD entries without decision authority sign-off
- **Catalog Consistency:** ADR INDEX is 100% accurate — every ADR listed with correct status, date, and cross-references; audit conducted at each Stage 3 gate review
- **Engineer Satisfaction:** Engineering team rates ADR clarity and usefulness ≥4.3/5 in quarterly documentation survey
- **Supersession Integrity:** 100% of superseded ADRs have valid cross-references to superseding ADRs; zero orphaned supersession chains
- **Immutability Compliance:** Zero accepted ADRs in `final/` are modified post-acceptance; all changes flow through superseding ADRs
