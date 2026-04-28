---
name: company-pipeline
description: The authoritative 10-stage development pipeline for this mobile product company. Use when you need to understand pipeline stage ownership, gate criteria, artifact flows, defect severity rules, or the Progress Sync Protocol. Covers Stages 1–10 end-to-end.
disable-model-invocation: false
---

# Development Pipeline Overview

The company's development workflow is a ten-stage state machine governing the full lifecycle of a mobile product — from raw requirements through to release. Each stage has a designated responsible producer, explicit reviewers, defined artifacts in and out, and gate criteria that must be satisfied before advancing.

---

## Stage Summary

| #   | Stage                                      | Key Output                                                                              | Responsible Producer(s)                       |
| --- | ------------------------------------------ | --------------------------------------------------------------------------------------- | --------------------------------------------- |
| 1   | Requirements → PRD + SRD                   | Product Requirements Document, Security Requirements Document                           | CPO (PRD), CSO (SRD)                          |
| 2   | PRD → Web Prototype + IDS                  | Web prototype (single HTML file), Interaction Design Specification                      | CDO                                           |
| 3   | Prototype → UML Engineering Package        | UML diagrams, Architecture Decision Records (ADRs), Technology Selection Document (TSD) | CTO (UML), CIO (ADRs + TSD)                   |
| 4   | UML → Coding Implementation Plan           | Implementation Plan, Gantt Chart                                                        | CTO                                           |
| 5   | Plan → Software Development                | Development codebase                                                                    | CTO                                           |
| 6   | Development → Code Review                  | Defect Report, Code Review Sign-off                                                     | CTO (panel: CPO, CDO, CTO, CIO, CSO)          |
| 7   | Code Review → Automated Testing            | Automated Test Suite, Test Results Report                                               | CTO + Test Lead                               |
| 8   | Testing → Integrity Verification           | Integrity Verification Sign-off                                                         | CTO (panel: all C-suite + Brand Design + R&D) |
| 9   | Integrity Verification → i18n Engineering  | Localised codebase, Translation Verification Report                                     | CTO-L + R&D                                   |
| 10  | i18n Engineering → Release Readiness Check | Release Readiness Report, Release Decision                                              | CTO (panel) + User                            |

---

## Stage Owner Index

| Agent                                         | Pipeline Stages                                                               |
| --------------------------------------------- | ----------------------------------------------------------------------------- |
| CPO — Marcus Tran-Yoshida                     | 1 (PRD), 6 (reviewer), 8 (reviewer), 10 (sign-off: product)                   |
| CSO — Dr. Sarah Chen                          | 1 (SRD), 6 (security reviewer), 8 (reviewer), 10 (sign-off: security)         |
| CDO — Yuki Tanaka-Chen                        | 2 (prototype + IDS), 6 (design reviewer), 8 (reviewer), 10 (sign-off: design) |
| CTO — Dr. Kenji Nakamura                      | 3 (UML), 4, 5, 6 (convenes panel), 7, 8 (convenes panel), 10 (convenes panel) |
| CIO — Dr. Priya Mehta                         | 3 (ADRs + TSD), 6 (reviewer), 8 (reviewer), 10 (sign-off: architecture)       |
| CTO-L — Dr. Amara Osei-Mensah                 | 9 (translation), 10 (sign-off: localisation)                                  |
| Software Architect — Rafael Okonkwo           | 3 (UML support), 6 (reviewer)                                                 |
| Test Lead — Priscilla Oduya                   | 7 (automated testing), 8 (reviewer)                                           |
| Platform Leads (Android, iOS, Cross-Platform) | 5 (development), 8 (reviewer)                                                 |

---

## Key Conventions

### Defect Severity System (P0–P3)

Applied in Stages 6, 7, and 8.

| Level | Definition                              | Release Impact                  |
| ----- | --------------------------------------- | ------------------------------- |
| P0    | App crash / data loss / security breach | Blocks release — non-negotiable |
| P1    | Core feature broken / major UX failure  | Blocks release — non-negotiable |
| P2    | Minor feature degraded / cosmetic issue | User decides to fix or defer    |
| P3    | Polish / nice-to-have                   | User decides to fix or defer    |

> P0/P1 classification is final and cannot be overridden. The user has explicit final authority on P2/P3 defects.

### Progress Sync Protocol

Active from Stage 4 onward.

- Any task exceeding its estimated duration by **>20%** triggers an automatic CTO → CPO schedule risk notification.
- The CTO produces weekly progress summaries for C-suite visibility.

### Paired Artifacts

The PRD and SRD are archived together at Stage 1 and travel as a unit through all subsequent stages.

### Release Checklist (Stage 10)

| #   | Domain                                              | Sign-off Authority |
| --- | --------------------------------------------------- | ------------------ |
| 1   | Product — all PRD requirements implemented          | CPO                |
| 2   | Design — all CDO/IDS specifications realised        | CDO                |
| 3   | Architecture — all UML/ADR/TSD standards upheld     | CTO + CIO          |
| 4   | Security — SRD enforced, OWASP MASVS compliant      | CSO                |
| 5   | Testing — 100% automated test pass rate             | CTO                |
| 6   | Localisation — all target languages complete        | CTO-L              |
| 7   | Platform — App Store / Google Play requirements met | CTO + CPO          |

---

## Full Pipeline (Stages 1–10)

### Stage 1: Requirements → PRD + SRD

**Relevant Personnel:** User, CPO, CIO, CTO, CSO | **Responsible:** CPO → PRD; CSO → SRD

Inquire about target platforms first. CPO produces PRD; CSO concurrently produces SRD. Both convene CIO and CTO for review. User confirms until satisfied. Both documents archived as a paired artifact.

**Gate Criteria:** [ ] Platform confirmed [ ] No further revisions [ ] PRD + SRD archived as paired artifact

---

### Stage 2: PRD → Web Prototype + IDS

**Relevant Personnel:** User, CPO, CIO, CTO, CDO, Brand Design | **Responsible:** CDO

CDO produces prototypes for user style selection. CPO/CIO/CTO audit. Loop until all approve. User confirms. CDO produces IDS (component trees, gesture vocabularies, state diagrams, edge case matrices, platform-specific patterns).

**Gate Criteria:** [ ] CPO, CIO, CTO, CDO all approved [ ] User confirmed [ ] IDS archived with prototype

---

### Stage 3: Web Prototype → UML Engineering Package

**Relevant Personnel:** User, CTO, CIO, R&D | **Responsible:** CTO → UML; CIO → ADRs + TSD

CTO produces UML diagrams (class, sequence, component). CIO produces ADRs + TSD. Jointly reviewed. Submitted to user for approval.

**Gate Criteria:** [ ] CTO + CIO approved [ ] Technically feasible [ ] User approved [ ] All artifacts archived

---

### Stage 4: All Deliverables → Coding Implementation Plan

**Relevant Personnel:** User, CTO, R&D | **Responsible:** CTO

Phased task decomposition, personnel assignments, dependency mapping, Gantt chart. Progress Sync Protocol documented. Submitted for user approval.

**Gate Criteria:** [ ] Covers all PRD/SRD/IDS/UML requirements [ ] Gantt chart included [ ] Personnel assigned [ ] Progress Sync documented [ ] User approved

---

### Stage 5: Plan → Software Development

**Relevant Personnel:** CTO, R&D | **Responsible:** CTO

Core implementation. CTO tracks against Gantt. Tasks >20% over estimate flagged to CPO. Internal review before advancing.

**Gate Criteria:** [ ] All tasks complete [ ] CTO internal review passed [ ] Progress log archived

---

### Stage 6: Development → Code Review

**Relevant Personnel:** CPO, CDO, CTO, CIO, CSO, R&D, User | **Responsible:** CTO (convenes panel)

Panel reviews against PRD, IDS, UML/ADR/TSD, and SRD (CSO-owned). All defects classified P0–P3. User reviews; P0/P1 non-negotiable; user decides P2/P3. Loop until all sign off.

**Gate Criteria:** [ ] All P0/P1 resolved [ ] User decided all P2/P3 [ ] CPO, CDO, CTO, CIO, CSO signed off

---

### Stage 7: Code Review → Automated Testing

**Relevant Personnel:** CTO, R&D | **Responsible:** CTO

100% pass rate target. P0/P1 block advancement; P2/P3 to user. Regression testing mandatory after fixes.

**Gate Criteria:** [ ] 100% pass rate (or user-approved deferrals) [ ] Regression testing passed [ ] Test Results Report archived

---

### Stage 8: Testing → Integrity Verification

**Relevant Personnel:** CPO, CDO, CTO, CIO, CSO, Brand Design, R&D, User | **Responsible:** CTO (convenes panel)

All personnel verify no functionality was removed to achieve passing tests. Anti-"trim-to-pass" guard. Any regression = P0/P1.

**Gate Criteria:** [ ] No functionality reduced vs Stage 6 baseline [ ] All panel members signed off

---

### Stage 9: Integrity Verification → i18n Engineering

**Relevant Personnel:** CTO-L, Translation Team, CPO, CDO, CTO, R&D | **Responsible:** CTO-L

R&D extracts all hardcoded strings into `strings.xml` / `Localizable.strings`. CTO-L governs translation via Language Translation Module. CPO/CDO/CTO structural completeness review. CTO-L issues Translation Verification Report.

**Gate Criteria:** [ ] Zero hardcoded strings [ ] All languages complete [ ] Structural review passed [ ] Translation Verification Report archived

---

### Stage 10: i18n Engineering → Release Readiness Check

**Relevant Personnel:** CPO, CDO, CTO, CIO, CSO, CTO-L, User | **Responsible:** CTO (convenes final panel)

Seven-item checklist — all must be signed off before user issues release decision.

| #   | Domain                                             | Sign-off Authority |
| --- | -------------------------------------------------- | ------------------ |
| 1   | Product: all PRD requirements implemented          | CPO                |
| 2   | Design: all CDO/IDS specifications realised        | CDO                |
| 3   | Architecture: all UML/ADR/TSD standards upheld     | CTO + CIO          |
| 4   | Security: SRD enforced, OWASP MASVS compliant      | CSO                |
| 5   | Testing: 100% automated test pass rate             | CTO                |
| 6   | Localisation: all target languages complete        | CTO-L              |
| 7   | Platform: App Store / Google Play requirements met | CTO + CPO          |

**Gate Criteria:** [ ] All 7 items signed off [ ] Report submitted to user [ ] User issued final release decision
