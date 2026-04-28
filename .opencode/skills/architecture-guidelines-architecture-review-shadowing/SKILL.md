---
name: architecture-guidelines-architecture-review-shadowing
description: Architecture review shadowing for mobile projects — independent platform-lead evaluation of UML packages, ADRs, and TSD during Stage 3 before gate review. Owned by Rafael Okonkwo (Software Architect). Use during Stage 3 (UML Engineering) for shadow review execution and Stage 4 (Implementation Plan) for effort estimation. Trigger: architecture review shadowing, shadow review, UML review, architecture feasibility, platform lead review.
prerequisites:
  - architecture-overview

version: "1.0.0"
---

# Architecture Review Shadowing

**Category:** Engineering Process
**Owner:** Platform Leads / Software Architect

## Purpose

Execute a shadow review during Stage 3 (Architecture) where platform leads and senior engineers independently evaluate the UML engineering package produced by the CTO and CIO. This process ensures architecture decisions are scrutinized by those who will implement them, catches misalignments before the gate review, and provides knowledge transfer to platform teams.

## Execution Guidance

### Shadowing Objectives

| Objective                         | How It's Achieved                                   |
| --------------------------------- | --------------------------------------------------- |
| Implementation feasibility review | Platform leads assess whether UML can be coded      |
| Technology stack validation       | Verify ADR choices are practical for each platform  |
| Knowledge transfer                | Implementers understand architecture before Stage 4 |
| Risk identification               | Surface concerns before formal gate review          |
| Estimation preparation            | Platform leads begin effort estimation for Stage 4  |

### Shadowing Process Flow

```
Stage 3 Production (CTO/CIO)
         │
         ├── UML diagrams published to architecture/uml/
         ├── ADRs published to architecture/decisions/
         └── TSD published to architecture/technology/
              │
              ▼
Stage 3 Shadow Period (48 hours)
         │
         ├── iOS Lead: Reviews iOS-relevant diagrams and ADRs
         ├── Android Lead: Reviews Android-relevant diagrams and ADRs
         ├── Cross-Platform Lead: Reviews shared architecture
         ├── Software Architect: Independent review of all UML
         └── Each produces a Shadow Review Report
              │
              ▼
Shadow Review Consolidation
         │
         ├── CTO collects all shadow reviews
         ├── Identifies common concerns (flagged by 2+ reviewers)
         ├── Classifies concerns by severity
         └── Addresses concerns before gate review OR documents as known trade-offs
              │
              ▼
Stage 3 Gate Review (with user)
         │
         ├── Present UML Engineering Package
         ├── Present Shadow Review findings
         ├── Address user questions
         └── User approves or requests revisions
```

### Shadow Review Report Template

```markdown
# Shadow Review: Stage 3 — {Project Name}

**Reviewer:** {name, role}
**Date:** {date}
**Platform:** iOS / Android / Cross-Platform

## UML Diagram Review

### Class Diagrams

- [ ] Entities match platform data model capabilities
- [ ] Relationships are implementable (not just theoretical)
- [ ] No missing entities needed by this platform
- **Findings:** {list any issues}

### Sequence Diagrams

- [ ] Interactions are feasible within platform constraints
- [ ] Error paths are included in sequences
- [ ] Async operations correctly shown
- **Findings:** {list any issues}

### Component Diagrams

- [ ] Component boundaries align with platform module boundaries
- [ ] Dependency directions are feasible (no cycles)
- [ ] External service interfaces are clearly defined
- **Findings:** {list any issues}

## ADR Review

| ADR #   | Title   | Assessment                              | Concerns            |
| ------- | ------- | --------------------------------------- | ------------------- |
| ADR-001 | {title} | ✅ Supported / ⚠️ Concern / ❌ Blocking | {details or "none"} |
| ADR-002 | {title} | ✅ Supported / ⚠️ Concern / ❌ Blocking | {details or "none"} |

## TSD Review

- [ ] Selected technologies have mature platform support
- [ ] Version compatibility confirmed for minimum OS
- [ ] No technology introduces unacceptable risk
- **Findings:** {list any issues}

## Implementation Feasibility

- **Estimated effort (platform):** {person-weeks}
- **Key risks:** {list}
- **Blockers:** {list, or "none"}
- **Dependencies on other platforms:** {list}

## Recommendations

1. {Specific, actionable recommendation}
2. {Specific, actionable recommendation}
```

### Escalation Protocol

| Scenario                               | Action                                | Timeline           |
| -------------------------------------- | ------------------------------------- | ------------------ |
| Shadow review finds blocking issue     | CTO convenes emergency review         | Within 4 hours     |
| ADR conflicts with platform constraint | CTO + platform lead discuss amendment | Within 8 hours     |
| TSD specifies unsupported technology   | Platform lead provides alternatives   | Within 12 hours    |
| UML missing platform-specific details  | CTO amends diagrams                   | Before gate review |

### Shadow Reviewer Responsibilities

| Reviewer            | Shadow Scope                                            |
| ------------------- | ------------------------------------------------------- |
| iOS Lead            | iOS-relevant class/sequence diagrams, iOS ADRs, iOS TSD |
| Android Lead        | Android-relevant diagrams, Android ADRs, Android TSD    |
| Cross-Platform Lead | Shared architecture, Flutter/KMP ADRs, cross-platform   |
| Software Architect  | Full UML package, independent of platform perspective   |
| Test Lead           | Testability of architecture, mock points, test seams    |

## Pipeline Integration

**Stage 3 (Architecture):** Shadowing runs in parallel with architecture production. Shadow review reports are consolidated before the gate review.

**Stage 4 (Implementation Plan):** Platform leads use their shadow review understanding to produce accurate effort estimates and identify task dependencies.

**Stage 5 (Development):** Knowledge transferred during shadowing reduces implementation ramp-up time. Platform leads already understand architecture decisions.

## Quality Standards

| Metric                   | Target                                  | Measurement                   |
| ------------------------ | --------------------------------------- | ----------------------------- |
| Shadow review completion | 100% of assigned reviewers submit       | CTO tracking                  |
| Concern resolution rate  | > 90% resolved before gate review       | Shadow review log             |
| Estimation accuracy      | Within 20% of actual effort             | Stage 4 vs Stage 5 comparison |
| Knowledge transfer       | Platform leads can explain architecture | Stage 4 kickoff meeting       |

## Reference Materials

- `company/pipeline/mobile-development/pipeline.md` — Stage 3 specification
- `company/library/topics/architecture.md` — UML engineering guidance
- `company/pipeline/mobile-development/monitoring.md` — Progress monitoring system
- ADR production skill: `mobile-adr-production.md`
