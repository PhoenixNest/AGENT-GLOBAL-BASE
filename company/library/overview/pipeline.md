# Development Pipeline Overview

The company's development workflow is a ten-stage state machine governing the full lifecycle of a mobile product — from raw requirements through to release. Each stage has a designated responsible producer, explicit reviewers, defined artifacts in and out, and gate criteria that must be satisfied before advancing.

> **Full definition:** [`pipeline/development/pipeline.md`](../../pipeline/development/pipeline.md)

---

## Stage Summary

| # | Stage | Key Output | Responsible Producer(s) |
| --- | --- | --- | --- |
| 1 | Requirements → PRD + SRD | Product Requirements Document, Security Requirements Document | CPO (PRD), CSO (SRD) |
| 2 | PRD → Web Prototype + IDS | Web prototype (single HTML file), Interaction Design Specification | CDO |
| 3 | Prototype → UML Engineering Package | UML diagrams, Architecture Decision Records (ADRs), Technology Selection Document (TSD) | CTO (UML), CIO (ADRs + TSD) |
| 4 | UML → Coding Implementation Plan | Implementation Plan, Gantt Chart | CTO |
| 5 | Plan → Software Development | Development codebase | CTO |
| 6 | Development → Code Review | Defect Report, Code Review Sign-off | CTO (panel: CPO, CDO, CTO, CIO, CSO) |
| 7 | Code Review → Automated Testing | Automated Test Suite, Test Results Report | CTO + Test Lead |
| 8 | Testing → Integrity Verification | Integrity Verification Sign-off | CTO (panel: all C-suite + Brand Design + R&D) |
| 9 | Integrity Verification → i18n Engineering | Localised codebase, Translation Verification Report | CTO-L + R&D |
| 10 | i18n Engineering → Release Readiness Check | Release Readiness Report, Release Decision | CTO (panel) + User |

---

## Stage Owner Index

| Agent | Pipeline Stages |
| --- | --- |
| CPO — Marcus Tran-Yoshida | 1 (PRD), 6 (reviewer), 8 (reviewer), 10 (sign-off: product) |
| CSO — Dr. Sarah Chen | 1 (SRD), 6 (security reviewer), 8 (reviewer), 10 (sign-off: security) |
| CDO — Yuki Tanaka-Chen | 2 (prototype + IDS), 6 (design reviewer), 8 (reviewer), 10 (sign-off: design) |
| CTO — Dr. Kenji Nakamura | 3 (UML), 4, 5, 6 (convenes panel), 7, 8 (convenes panel), 10 (convenes panel) |
| CIO — Dr. Priya Mehta | 3 (ADRs + TSD), 6 (reviewer), 8 (reviewer), 10 (sign-off: architecture) |
| CTO-L — Dr. Amara Osei-Mensah | 9 (translation), 10 (sign-off: localisation) |
| Software Architect — Rafael Okonkwo | 3 (UML support), 6 (reviewer) |
| Test Lead — Priscilla Oduya | 7 (automated testing), 8 (reviewer) |
| Platform Leads (Android, iOS, Cross-Platform) | 5 (development), 8 (reviewer) |
| Internationalization Specialist — Tomas Dvoracek | 9 (string extraction) |
| Linguist Team | 9 (translation) |

---

## Key Conventions

### Defect Severity System (P0–P3)

Applied in Stages 6, 7, and 8.

| Level | Definition | Release Impact |
| --- | --- | --- |
| P0 | App crash / data loss / security breach | Blocks release — non-negotiable |
| P1 | Core feature broken / major UX failure | Blocks release — non-negotiable |
| P2 | Minor feature degraded / cosmetic issue | User decides to fix or defer |
| P3 | Polish / nice-to-have | User decides to fix or defer |

> P0/P1 classification is final and cannot be overridden. The user has explicit final authority on P2/P3 defects.

### Progress Sync Protocol

Active from Stage 4 onward.

- Any task exceeding its estimated duration by **>20%** triggers an automatic CTO → CPO schedule risk notification.
- The CTO produces weekly progress summaries for C-suite visibility.

### Paired Artifacts

The PRD and SRD are archived together at Stage 1 and travel as a unit through all subsequent stages.

### Release Checklist (Stage 10)

| # | Domain | Sign-off Authority |
| --- | --- | --- |
| 1 | Product — all PRD requirements implemented | CPO |
| 2 | Design — all CDO/IDS specifications realised | CDO |
| 3 | Architecture — all UML/ADR/TSD standards upheld | CTO + CIO |
| 4 | Security — SRD enforced, OWASP MASVS compliant | CSO |
| 5 | Testing — 100% automated test pass rate | CTO |
| 6 | Localisation — all target languages complete | CTO-L |
| 7 | Platform — App Store / Google Play requirements met | CTO + CPO |

See [`topics/testing.md`](../topics/testing.md), [`topics/security.md`](../topics/security.md), and [`topics/localization.md`](../topics/localization.md) for cross-cutting detail on these domains.
