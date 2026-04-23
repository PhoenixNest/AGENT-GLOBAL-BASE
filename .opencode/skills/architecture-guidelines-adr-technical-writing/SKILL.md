---
name: architecture-guidelines-adr-technical-writing
description: 'Architecture skill: Adr Technical Writing'
---

# ADR Technical Writing

**Category:** Technical Documentation / Architecture
**Owner:** Technical Writer

## Overview

Authors, reviews, and maintains Architecture Decision Records (ADRs) and the Technology Selection Document (TSD) for the engineering organization. ADRs are the authoritative record of architectural decisions made during Stage 3 (Architecture), capturing the context, options considered, decision rationale, and consequences of each choice. The TSD synthesizes technology evaluations into a single reference document that locks technology stack decisions before Stage 4 begins.

This skill covers ADR template design, decision documentation best practices, technical communication for engineering audiences, version control for documentation, and the editorial process that ensures ADRs remain accurate, discoverable, and actionable throughout the product lifecycle.

## Competency Dimensions

| Dimension                     | Description                                                                                                   | Proficiency Indicators                                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| ADR Authoring                 | Write clear, structured ADRs that capture decision context, options, rationale, and consequences              | Can produce a publication-ready ADR from raw decision notes in ≤4 hours; zero structural rejections from CTO    |
| Decision Documentation        | Facilitate decision-capture sessions with architects and engineers; extract signal from discussion            | Captures ≥95% of key decision points from architecture meetings; validates accuracy with decision-makers        |
| TSD Writing                   | Synthesize multiple technology evaluations into a coherent Technology Selection Document                      | TSD passes CIO+CTO review on first submission; covers all evaluated technologies with clear selection rationale |
| Technical Communication       | Translate complex architectural concepts into precise, accessible prose for engineering audiences             | Engineers rate documentation clarity ≥4.3/5; zero ambiguity-related defects traced to ADR content               |
| Documentation Version Control | Manage ADR lifecycle (draft → superseded → accepted → deprecated) with proper versioning and cross-references | ADR catalog has zero orphaned or conflicting records; supersession chains are complete and traceable            |
| Editorial Standards           | Enforce consistent formatting, terminology, and structural conventions across all architecture documents      | Style audit passes ≥95%; terminology consistency score ≥98% across ADR catalog                                  |

## Execution Guidance

### ADR Template Design

Every ADR follows this canonical structure. The template is maintained in `company/project/<project>/architecture/decisions/ADR-TEMPLATE.md` and all ADRs reference it.

```markdown
# ADR-NNN: [Short Decision Title]

**Status:** [Proposed | Accepted | Superseded | Deprecated]
**Date:** [YYYY-MM-DD]
**Author:** [Name, Role]
**Reviewers:** [CTO, CIO, Software Architect — as applicable]
**Stage:** [Stage 3 — Architecture]
**Supersedes:** [ADR-XXX or "N/A"]
**Superseded By:** [ADR-XXX or "N/A"]

## Context

[2-4 paragraphs describing the problem or situation that prompted this decision.
Include relevant constraints: technical, business, timeline, team capability, security.
Reference upstream artifacts: PRD requirements, SRD controls, UML diagrams, prior ADRs.]

## Decision Drivers

- [Driver 1: e.g., "Must support offline-first operation per PRD requirement R-012"]
- [Driver 2: e.g., "Team has existing Kotlin expertise; no budget for Swift training"]
- [Driver 3: e.g., "OWASP MASVS Level 2 compliance required per SRD Section 4.3"]
- [Driver 4: e.g., "Release target: Q3 2026; solution must be production-ready by Q2"]

## Options Considered

### Option A: [Name]

[Description of the option. Include pros, cons, and effort estimate.]

**Pros:**

- ...

**Cons:**

- ...

**Effort Estimate:** [T-shirt size or story points]

### Option B: [Name]

[Same structure as Option A]

### Option C: [Name] (Optional — include if ≥3 viable options existed)

[Same structure as Option A]

## Decision

**Selected Option:** [Option A/B/C]

**Rationale:**
[2-3 paragraphs explaining WHY this option was chosen. Reference decision drivers explicitly.
Acknowledge trade-offs and why they are acceptable. If consensus was not unanimous,
document minority viewpoints and why they were overruled.]

**Decision Authority:** [Who made the final call: CTO, CIO, consensus, etc.]

## Consequences

### Positive

- [Benefit 1]
- [Benefit 2]

### Negative (Accepted Trade-offs)

- [Trade-off 1 — and mitigation strategy if applicable]
- [Trade-off 2]

### Risks

- [Risk 1 — with severity and mitigation plan]
- [Risk 2]

## Implementation Notes

[Specific guidance for engineers implementing this decision. Reference implementation
plan sections, code locations, or configuration files. Include any "gotchas" or
common pitfalls discovered during implementation.]

## References

- [Link to UML diagram, TSD section, PRD requirement, SRD control, external resource]
```

### ADR Lifecycle Management

| Status         | Definition                                                       | Trigger                                                  | Action                                                                                       |
| -------------- | ---------------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Proposed**   | ADR drafted but not yet reviewed                                 | Author completes draft                                   | Submitted to CTO + CIO for review                                                            |
| **Accepted**   | ADR reviewed and approved by decision authority                  | CTO/CIO sign-off                                         | Merged to `architecture/decisions/`; referenceable in downstream stages                      |
| **Superseded** | ADR replaced by a newer ADR with a different decision            | New ADR-NNN accepted that explicitly supersedes this one | Status updated; cross-reference to superseding ADR added; document preserved (never deleted) |
| **Deprecated** | Decision no longer applies (feature removed, technology retired) | CTO determines decision is obsolete                      | Status updated; deprecation reason documented; document preserved                            |

#### Versioning Workflow

```
draft/ADR-NNN.md          →  Work-in-progress (author iterates)
     ↓ (submitted for review)
v1/ADR-NNN.md             →  First reviewed version
     ↓ (revisions requested)
v2/ADR-NNN.md             →  Second reviewed version
     ↓ (accepted)
final/ADR-NNN.md          →  Accepted baseline; frozen for downstream stages
     ↓ (superseded by ADR-MMM)
final/ADR-NNN.md          →  Status changed to "Superseded"; cross-reference to ADR-MMM
```

### Decision Documentation Best Practices

#### Capturing Decisions from Architecture Sessions

1. **Pre-Session Preparation:**
   - Review meeting agenda and identify decision points
   - Prepare ADR skeleton (title, context placeholder, options placeholder)
   - Confirm decision authority (who has final say: CTO, CIO, consensus, or vote)

2. **During Session:**
   - Record all options presented (even those quickly dismissed — document WHY they were dismissed)
   - Capture decision drivers explicitly (ask: "What's driving this choice?")
   - Note dissenting opinions and the rationale for overruling them
   - Record implementation notes verbatim if they contain actionable technical guidance
   - Flag any unresolved questions for follow-up

3. **Post-Session Drafting (within 24 hours):**
   - Complete ADR draft using captured notes
   - Validate technical accuracy with decision-maker (CTO or Software Architect)
   - Submit for review with clear deadline (typically 3 business days)
   - Track review feedback and iterate

#### Writing Principles for ADRs

| Principle                             | Application                                                                                                                                                   |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Decision-centric, not descriptive** | ADRs record decisions, not tutorials. Every section should serve the decision narrative.                                                                      |
| **Specific over general**             | "We chose Room over SQLiteOpenHelper because..." not "We chose a good database solution."                                                                     |
| **Acknowledge trade-offs honestly**   | If the chosen option has real downsides, document them. Future engineers need to understand the cost.                                                         |
| **Reference, don't repeat**           | Link to UML diagrams, PRD requirements, and SRD controls rather than restating them.                                                                          |
| **Write for the future reader**       | Assume the reader has no context. Explain acronyms on first use. Provide enough background to understand the decision without attending the original meeting. |
| **Immutable once accepted**           | Accepted ADRs are never edited. If a decision changes, write a new ADR that supersedes the old one.                                                           |

### Technology Selection Document (TSD) Writing

The TSD is a synthesized document that aggregates all technology evaluations conducted during Stage 3 into a single reference. It is owned by the CIO but authored by the Technical Writer in collaboration with the Software Architect.

#### TSD Structure

```markdown
# Technology Selection Document (TSD)

**Project:** [Project Name]
**Version:** v1
**Date:** [YYYY-MM-DD]
**Author:** [Technical Writer]
**Approved By:** [CIO, CTO]

## Executive Summary

[1-2 paragraph overview of technology selections and their alignment with PRD/SRD requirements]

## Selection Methodology

[Evaluation criteria, scoring model, decision authority, timeline]

## Technology Evaluations

### [Category 1: e.g., Mobile Framework]

| Technology              | Score  | Pros | Cons | Recommendation |
| ----------------------- | ------ | ---- | ---- | -------------- |
| Flutter                 | 8.2/10 | ...  | ...  | Selected       |
| React Native            | 7.1/10 | ...  | ...  | Not selected   |
| Native (Kotlin + Swift) | 6.8/10 | ...  | ...  | Not selected   |

**Rationale:** [Why the selected technology wins]

### [Category 2: e.g., Database]

[Same structure]

### [Category 3: e.g., CI/CD Platform]

[Same structure]

## Selected Technology Stack

| Category         | Technology                       | Version       | ADR Reference |
| ---------------- | -------------------------------- | ------------- | ------------- |
| Mobile Framework | Flutter                          | 3.x           | ADR-003       |
| Database         | Room (Android) / SwiftData (iOS) | Latest stable | ADR-007       |
| CI/CD            | GitHub Actions                   | Latest        | ADR-012       |
| ...              | ...                              | ...           | ...           |

## Locked Decisions

[Explicit statement that technology decisions in this document are locked upon Stage 3 gate approval and are not revisable in Stage 4+]

## References

- [Links to all ADRs, vendor evaluations, TCO analyses, proof-of-concept results]
```

#### TSD Writing Guidelines

- **Evaluation Criteria Consistency:** All technology categories use the same weighted criteria: functionality (30%), performance (20%), security (20%), team capability fit (15%), TCO (10%), ecosystem maturity (5%)
- **Evidence-Based Scoring:** Each score is backed by specific evidence (benchmark results, POC outcomes, vendor documentation, team survey results)
- **Vendor-Neutral Language:** Avoid marketing language. Use objective, measurable criteria.
- **Cross-Reference ADRs:** Every technology selection references the ADR that formally records the decision
- **Version Locking:** TSD explicitly states that decisions are locked at Stage 3 gate approval

### Technical Communication for Engineering Audiences

#### Audience Analysis

| Audience                                      | Technical Depth          | Communication Style                                                               |
| --------------------------------------------- | ------------------------ | --------------------------------------------------------------------------------- |
| CTO / CIO / Software Architect                | Expert                   | Concise, decision-focused, assumes deep technical context                         |
| Platform Leads (Android, iOS, Cross-Platform) | Advanced                 | Implementation-focused, includes code references and configuration details        |
| Individual Contributor Engineers              | Intermediate to Advanced | Clear explanations of concepts, includes examples and links to reference material |
| Test Lead / QA Engineers                      | Intermediate             | Focus on testability implications, defect classification impact                   |
| Non-Technical Stakeholders (CPO, CDO)         | Basic                    | High-level summary, business impact, timeline implications                        |

#### Writing Standards

- **Terminology:** Use canonical terms from the company glossary. Define acronyms on first use (e.g., "Architecture Decision Record (ADR)").
- **Code Examples:** When including code, use the language and framework relevant to the audience. Annotate non-obvious patterns.
- **Diagrams:** Embed Mermaid or PlantUML diagrams where they clarify architecture. Reference UML diagrams by their file path.
- **Tone:** Objective, precise, professional. Avoid opinionated language ("X is the best choice") unless quoting a decision-maker.
- **Length:** ADRs should be 2-4 pages maximum. If longer, the decision is too complex and should be decomposed into multiple ADRs.

### Version Control for Documentation

#### Git Workflow for ADRs

```
architecture/decisions/
├── ADR-TEMPLATE.md          # Canonical template
├── ADR-001.md               # Current version (symlink or copy from final/)
├── ADR-002.md
├── ...
├── draft/                   # Work-in-progress ADRs
│   └── ADR-015.md
├── v1/                      # Versioned iterations
│   ├── ADR-001.md
│   └── README.md            # Version metadata
├── v2/
│   └── ...
└── final/                   # Accepted ADRs (frozen)
    ├── ADR-001.md
    └── README.md            # Acceptance metadata (panel, date, criteria)
```

#### Commit Message Conventions

```
docs(adr): draft ADR-015 — [Short Title]
docs(adr): revise ADR-015 v2 — [Summary of changes]
docs(adr): accept ADR-015 — [CTO/CIO sign-off]
docs(adr): supersede ADR-007 with ADR-015 — [Reason]
```

#### Change Tracking

- All ADR changes tracked via Git commit history
- Major revisions (v1 → v2 → v3) documented in version folder `README.md`
- Accepted ADRs (in `final/`) are immutable — changes require a new superseding ADR
- ADR index (`architecture/decisions/INDEX.md`) maintained with status, date, and cross-references for every ADR

## Pipeline Integration

| Pipeline Stage                   | ADR/TSD Relevance                                                                                                                       |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 1 (Requirements)           | Not applicable — ADRs not yet in scope                                                                                                  |
| Stage 2 (Design)                 | Not applicable — design decisions captured in IDS, not ADRs                                                                             |
| Stage 3 (Architecture)           | **Primary stage** — ADRs authored, reviewed, and accepted; TSD compiled and locked                                                      |
| Stage 4 (Implementation Plan)    | ADRs referenced in implementation plan; no new ADRs created unless plan reveals architectural gap (requires CTO approval)               |
| Stage 5 (Development)            | Implementation notes in ADRs guide developers; no ADR changes unless critical architectural issue discovered (superseding ADR required) |
| Stage 6 (Code Review)            | Code reviewed against ADR decisions; deviations flagged as defects                                                                      |
| Stage 7 (Testing)                | Test architecture references ADR decisions on testing frameworks and strategies                                                         |
| Stage 8 (Integrity Verification) | Panel verifies implementation matches ADR decisions; deviations without superseding ADR are P1 defects                                  |
| Stage 9 (i18n)                   | Not applicable — localization decisions tracked separately                                                                              |
| Stage 10 (Release)               | ADR catalog reviewed as part of architecture sign-off (Release Checklist item 3)                                                        |

## Quality Standards

- **ADR Completeness:** 100% of accepted ADRs contain all required sections (Context, Decision Drivers, Options Considered, Decision, Consequences, Implementation Notes, References)
- **Review Turnaround:** ADR drafts reviewed by CTO/CIO within 3 business days of submission; zero ADRs stalled in review for >5 business days
- **Structural Integrity:** Zero ADRs rejected for structural deficiencies (missing sections, incorrect format, orphaned cross-references)
- **TSD Accuracy:** 100% of technology selections in TSD have corresponding accepted ADRs; zero TSD entries without decision authority sign-off
- **Catalog Consistency:** ADR INDEX is 100% accurate — every ADR listed with correct status, date, and cross-references; audit conducted at each Stage 3 gate review
- **Engineer Satisfaction:** Engineering team rates ADR clarity and usefulness ≥4.3/5 in quarterly documentation survey
- **Supersession Integrity:** 100% of superseded ADRs have valid cross-references to superseding ADRs; zero orphaned supersession chains
- **Immutability Compliance:** Zero accepted ADRs in `final/` are modified post-acceptance; all changes flow through superseding ADRs
