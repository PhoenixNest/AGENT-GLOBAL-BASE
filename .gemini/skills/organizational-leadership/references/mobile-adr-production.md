---
name: mobile-adr-production
description: Author production-quality Architecture Decision Records (ADRs) for mobile platform decisions — Android, iOS, and Kotlin Multiplatform — covering technology selection, shared code strategy, and platform-specific architectural patterns, for inclusion in the Stage 3 UML Engineering Package.
version: "1.0.0"
---

# Mobile ADR Production

| Competency              | Description                                                            | Quality Criteria                                                                                                                             |
| ----------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Mobile ADR Authorship   | Write ADRs for platform architecture choices (Android/iOS/KMP/Flutter) | ADR covers: Context (why this decision is needed), Decision (what is chosen), Alternatives considered, Consequences, and Acceptance criteria |
| Technology Comparison   | Evaluate competing mobile technologies with objective criteria         | Comparison table with at least 3 alternatives; criteria include performance, maintenance burden, team competence, and long-term risk         |
| KMP Architecture ADRs   | Specific ADRs for Kotlin Multiplatform shared code strategy            | Defines shared code scope (what goes in common module vs platform-specific); documents expect/actual usage boundaries                        |
| ADR Acceptance Criteria | Verifiable criteria for Stage 6 conformance checks                     | Each ADR includes a ≥3-item Stage 6 checklist that a reviewer can objectively pass or fail against the implementation                        |

## Execution Guidance

### Mobile ADR Template

```markdown
# ADR-MOB-NNN: [Architecture Decision Title]

**Status:** Proposed | Accepted | Superseded by ADR-MOB-NNN
**Date:** YYYY-MM-DD
**Author:** Dr. Elena Rostova, Senior Software Architect
**Approved by:** CTO (Stage 3 User Approval)

## Context

[What is the architectural challenge or decision point? What constraints exist?]

## Decision

[The chosen solution, stated unambiguously]

## Alternatives Considered

| Alternative | Reason Not Chosen                        |
| ----------- | ---------------------------------------- |
| [Option A]  | [Specific technical or strategic reason] |
| [Option B]  | [Specific technical or strategic reason] |

## Consequences

**Positive:** [What improves]
**Negative / Trade-offs:** [What becomes harder or more expensive]

## Stage 6 Acceptance Criteria

- [ ] [Verifiable implementation check 1]
- [ ] [Verifiable implementation check 2]
- [ ] [Verifiable implementation check 3]
```

### Platform Decision Scope Guide

| Decision Type                | ADR Required?                  | Notes                                                     |
| ---------------------------- | ------------------------------ | --------------------------------------------------------- |
| Android architecture pattern | Yes                            | MVVM vs MVI vs Clean Architecture — document trade-offs   |
| iOS architecture pattern     | Yes                            | TCA vs MVVM+Coordinator — document reactive framework     |
| KMP shared code boundary     | Yes                            | Define exactly which layers are shared vs platform-native |
| Third-party SDK selection    | Yes if security/privacy impact | Analytics, crash reporting, payment SDKs                  |
| Build tooling change         | Yes if CI/CD impact            | Gradle plugin major version; Xcode upgrade strategy       |
