---
name: developer-documentation
description: >
  Developer portal architecture, getting started guides, integration tutorials, troubleshooting documentation, changelog management, and all developer experience (DX) content for the platform engineering ecosystem — covering information architecture, 5-minute quick starts, tested integration tutorials, symptom-first troubleshooting guides, and versioned changelogs with migration guides. Owned by Amina Razak (Technical Writer). Use when writing developer documentation, building developer portals, creating API getting started guides, authoring integration tutorials, writing troubleshooting docs, or managing changelogs. Trigger: developer documentation, developer portal, getting started guide, API tutorial, integration guide, troubleshooting doc, changelog, developer experience, DX writing, API reference.
version: "1.0.0"
---

Developer documentation skill for Amina Razak — Technical Writer (R&D department).
Produces developer portal architecture, getting started guides, integration tutorials, troubleshooting documentation, changelog management, and DX content.

## Owner

Amina Razak — Technical Writer, Research & Development department.
Reports to: CTO office.
Pipeline stages: 5, 6, 10.

## When to Invoke

- Designing information architecture, navigation, search, and content organization for developer-facing portals
- Writing onboarding guides that take a developer from zero to first successful API call in ≤5 minutes
- Authoring step-by-step integration tutorials for common patterns with complete, tested code examples
- Creating diagnostic guides, FAQ entries, and error resolution documentation
- Maintaining structured, versioned changelogs with clear release notes, deprecation notices, and migration guides
- Applying DX writing principles that reduce cognitive load, accelerate comprehension, and respect developer time

## Competencies

| Competency                    | Description                                                                                                   | Quality Criteria                                                                                           |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Developer Portal Architecture | Design information architecture, navigation, search, and content organization for developer-facing portals    | Portal IA achieves ≥90% search success rate; navigation task completion ≥95% in usability testing          |
| Getting Started Guides        | Write onboarding guides that take a developer from zero to first successful API call in ≤5 minutes            | ≥80% of developers complete the getting started flow on first attempt; time-to-first-call ≤5 minutes       |
| Integration Tutorials         | Author step-by-step tutorials for common integration patterns with complete, tested code examples             | Tutorial completion rate ≥75%; zero critical gaps reported by developers following the tutorial end-to-end |
| Troubleshooting Documentation | Create diagnostic guides, FAQ entries, and error resolution documentation                                     | ≥70% of support tickets deflected by troubleshooting docs; mean time to resolution reduced by ≥30%         |
| Changelog Management          | Maintain structured, versioned changelogs with clear release notes, deprecation notices, and migration guides | Changelog read rate ≥60%; zero developer complaints about undocumented breaking changes                    |
| Developer Experience Writing  | Apply DX writing principles that reduce cognitive load, accelerate comprehension, and respect developer time  | DX writing score ≥4.3/5 in developer surveys; documentation NPS ≥+40                                       |

## Execution Guidance

Detailed developer portal architecture patterns, quick start templates, integration tutorial structures, and DX writing principles are in `references/`:

- [`architecture-overview.md`](references/architecture-overview.md) — Developer portal architecture overview and information architecture principles
- [`quality-standards.md`](references/quality-standards.md) — Quality standards for developer documentation
- [`pipeline-integration.md`](references/pipeline-integration.md) — Pipeline integration guidance for documentation workflows
- [`common-pitfalls.md`](references/common-pitfalls.md) — Common pitfalls in developer documentation
- [`complete-code-example.md`](references/complete-code-example.md) — Complete code example patterns
- [`next-steps.md`](references/next-steps.md) — Next steps and progression guidance for developers

## Pipeline Integration

| Pipeline Stage                   | Developer Documentation Relevance                                                                                                              |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 1–4                        | Not applicable — developer documentation not in scope during requirements, design, architecture, or planning                                   |
| Stage 5 (Development)            | **Primary creation stage** — developer portal content, getting started guides, and integration tutorials authored alongside API implementation |
| Stage 6 (Code Review)            | Developer documentation reviewed as part of code review; documentation accuracy validated against implementation                               |
| Stage 7 (Testing)                | Tutorial examples tested against staging environment; getting started flow validated end-to-end                                                |
| Stage 8 (Integrity Verification) | Panel verifies developer portal content matches implementation; discrepancies flagged as defects                                               |
| Stage 9 (i18n)                   | Developer portal content localized if multi-language support is required                                                                       |
| Stage 10 (Release)               | Developer portal content reviewed as part of release readiness; getting started guides validated for accuracy                                  |

## Quality Standards

- **Portal IA:** ≥90% search success rate; navigation task completion ≥95% in usability testing
- **Getting Started:** ≥80% of developers complete the getting started flow on first attempt; time-to-first-call ≤5 minutes
- **Tutorial Completeness:** Tutorial completion rate ≥75%; zero critical gaps reported by developers following the tutorial end-to-end
- **Troubleshooting Effectiveness:** ≥70% of support tickets deflected by troubleshooting docs; mean time to resolution reduced by ≥30%
- **Changelog Quality:** Changelog read rate ≥60%; zero developer complaints about undocumented breaking changes
- **DX Writing Score:** ≥4.3/5 in developer surveys; documentation NPS ≥+40
- **Documentation Freshness:** 100% of developer portal pages reviewed and updated within 90 days of last change
- **Version Alignment:** 100% of documentation pages display correct API version; zero instances of version mismatch between docs and implementation
