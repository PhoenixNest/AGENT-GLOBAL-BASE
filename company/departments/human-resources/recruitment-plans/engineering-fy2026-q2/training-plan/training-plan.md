# Engineering FY2026 Q2 — Probationary Training Plan

**Document Type:** Probationary Training Plan
**Version:** 1.3
**Date:** April 5, 2026
**Owner:** CHRO (Dr. Evelyn Hartwell) + CTO Office (Dr. Kenji Nakamura)
**Contributing Officers (Phase 2):** CTO, CIO, CSO, CDO, Rafael Okonkwo (Software Architect)
**Contributing Officers (Phase 3):** CTO, CSO, CDO, iOS Lead, Android Lead, Cross-Platform Lead, VP Web & Backend, VP Platform Eng, DevEx Lead, DevOps Lead, Test Lead
**Status:** ✅ Complete — All 62 modules passed, 42/42 conditional hires training complete
**Department:** Human Resources — Recruitment Plans

---

## Table of Contents

1. [Policy](#policy)
2. [Trainee Registry — Phase 1](#trainee-registry--phase-1)
3. [Trainee Registry — Phase 2](#trainee-registry--phase-2)
4. [Module Assignments — Phase 1 (A–J)](#module-assignments--phase-1-aj)
5. [Module Assignments — Phase 2 (K–W)](#module-assignments--phase-2-kw)
6. [Module Assignments — Phase 3 Conditional Hires (AA–BF)](#module-assignments--phase-3-conditional-hires-aabf)
7. [At-Risk Conditions](#at-risk-conditions)
8. [Failure Protocol](#failure-protocol)
9. [Curriculum Index](#curriculum-index)
10. [Weekly Check-In Schedule](#weekly-check-in-schedule)
11. [Contributing Officers (Phase 3 Training Reviews)](#contributing-officers-phase-3-training-reviews)
12. [Document History](#document-history)

---

## Policy

### Phase 1: 30-Day Probationary Period

All Phase 1 hires enter a **30-day probationary period** beginning on their first day of employment. During this period, each hire must complete all assigned training modules and receive supervisor approval before formally commencing duties.

### Phase 2: 90-Day Probationary Period

Phase 2 conditional hires enter a **90-day probationary period** reflecting deliverables that require 60–90 days to produce (WCAG compliance roadmaps, mobile-specific ADRs, MASVS certification).

**Phase 2 Duty Commencement:** Conditional hires may begin core responsibilities on Day 1, subject to these restrictions:

| Restriction                                                             | Rationale                                     |
| ----------------------------------------------------------------------- | --------------------------------------------- |
| Cannot author ADRs solo until UML Production Certification passed (P11) | Architectural authority must be earned        |
| Cannot lead platform performance reviews until baseline delivered (P9)  | Must demonstrate measurement competence first |
| Cannot conduct unsupervised mobile pentests until MASVS certified (P13) | Security risk                                 |
| All production decisions require dual sign-off until all conditions met | Risk mitigation                               |

### Phase 3: Conditional Hire Probationary Period

Phase 3 conditional hires enter probationary periods matching their module deadlines (60–90 days). Duty commencement rules mirror Phase 2 — trainees may begin core responsibilities on Day 1 subject to dual sign-off requirements until all modules are passed.

**High-Risk (🔴) modules carry mandatory checkpoint reviews.** Missing a checkpoint triggers immediate CHRO notification and intensified supervision.

### Mandatory Completion Rule

**Failure to complete any assigned training module within the specified probationary period will result in the position being reopened for recruitment.** There are no extensions, no deferrals, and no exceptions. A vacant position is preferable to an untrained hire.

### Duty Commencement Rule (Phase 1)

**An employee may not formally commence their duties until:**

1. All assigned training modules are completed and verified as PASS
2. Their direct supervisor has signed off on training completion
3. The CHRO has recorded the completion in this document

Until all three conditions are met, the employee remains in training status. They may participate in onboarding activities (environment setup, team introductions, documentation review) but **may not make production decisions, approve PRs, or represent the company in external technical forums**.

### Weekly Check-In Requirement

Each responsible officer (training deliverer) must provide a **weekly status update** for each trainee enrolled in their module. Updates are recorded in `progress/tracker.md` and include:

- Session completed (yes/no)
- Trainee progress (on track / at risk / behind)
- Next session scheduled (date)
- Concerns or blockers
- Officer sign-off (initials)

---

## Trainee Registry — Phase 1

| #   | Trainee          | Role                            | Department          | Reports To                   | Assigned Modules                                        | Deadline | Status  |
| --- | ---------------- | ------------------------------- | ------------------- | ---------------------------- | ------------------------------------------------------- | -------- | ------- |
| 1   | Marcus Andersson | VP of Mobile Engineering        | R&D                 | CTO                          | ADR/TSD Governance, i18n Strategy Partnering            | Day 30   | ✅ PASS |
| 2   | Elena Vasquez    | VP of Web & Backend Engineering | R&D                 | CTO                          | ADR/TSD Governance, IDS Fluency                         | Day 30   | ✅ PASS |
| 3   | David Okonkwo    | VP of Platform Engineering      | R&D                 | CTO                          | MASVS Briefing                                          | Day 30   | ✅ PASS |
| 4   | Aisha Patel      | VP of Quality Engineering       | R&D                 | CTO                          | Localization Testing Strategy, Accessibility Automation | Day 30   | ✅ PASS |
| 5   | Thomas Zhang     | DevOps Lead                     | R&D                 | VP of Platform Engineering   | Compliance Foundations, Mobile Scanning Tools           | Day 30   | ✅ PASS |
| 6   | Rachel Kim       | Test Automation Lead            | R&D                 | Test Lead (Priscilla)        | Defect Triage Protocol                                  | Day 30   | ✅ PASS |
| 7   | James Wright     | Lead Security Engineer          | Cyberspace Security | CSO (Dr. Sarah Chen)         | MASVS Mastery (Track A), Mobile Scanning Tools          | Day 30   | ✅ PASS |
| 8   | Natalia Petrova  | Security Architect              | Cyberspace Security | Lead Security Engineer → CSO | MASVS Mastery (Track B), Mobile Threat Modeling         | Day 30   | ✅ PASS |

---

## Trainee Registry — Phase 2

### P9 — Amira Voss — Frontend Chapter Lead

| Field                  | Detail                                                                                                                      |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Department**         | R&D                                                                                                                         |
| **Reports To**         | CTO (Dr. Kenji Nakamura)                                                                                                    |
| **Deadline**           | Day 90                                                                                                                      |
| **Modules**            | P9-M1: Frontend Performance Baseline (30d), P9-M2: WCAG 2.1 AA Mobile Roadmap (60d), P9-M3: Mobile Platform Immersion (90d) |
| **Assessing Officers** | CTO (conditional), CDO (unconditional), CHRO (unconditional)                                                                |
| **Status**             | ✅ PASS                                                                                                                     |

### P11 — Dr. Elena Rostova — Senior Software Architect

| Field                  | Detail                                                                                                                                                                                                                                                                                                                 |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Department**         | R&D                                                                                                                                                                                                                                                                                                                    |
| **Reports To**         | CTO (Dr. Kenji Nakamura)                                                                                                                                                                                                                                                                                               |
| **Deadline**           | Day 90                                                                                                                                                                                                                                                                                                                 |
| **Modules**            | P11-M1: Code Review Participation (90d), P11-M2: 3 Mobile-Specific ADRs (90d), P11-M3: Weekly Architecture Syncs (90d), P11-M4: Mobile Platform Assessment (60d), P11-M5: ADR Template Adaptation (90d), P11-M6: Practice UML + ADR (30d), P11-M7: UML Production Certification (60d), P11-M8: Stage 3 Shadowing (90d) |
| **Assessing Officers** | CTO (conditional), CIO (conditional), Rafael (conditional), CHRO (not documented)                                                                                                                                                                                                                                      |
| **Status**             | ✅ PASS                                                                                                                                                                                                                                                                                                                |

> **CHRO Note (P11):** Dr. Rostova carries the highest conditional load — 8 conditions from 3 assessing officers. If any module fails, the entire candidacy is reviewed. No partial passes.

### P13 — Omar Farouq — Security Engineer #2

| Field                  | Detail                                                                        |
| ---------------------- | ----------------------------------------------------------------------------- |
| **Department**         | Cyberspace Security                                                           |
| **Reports To**         | CSO (Dr. Sarah Chen)                                                          |
| **Deadline**           | Day 90                                                                        |
| **Modules**            | P13-M1: MASVS Certification (90d), P13-M2: Supervised Mobile Pentesting (90d) |
| **Assessing Officers** | CSO (conditional), James Wright (unconditional), CHRO (not documented)        |
| **Status**             | ✅ PASS                                                                       |

---

## Module Assignments — Phase 1 (A–J)

### Module A: MASVS Mastery — James Wright (Track A), Natalia Petrova (Track B), David Okonkwo (Track C)

| Field            | Detail                                       |
| ---------------- | -------------------------------------------- |
| **Delivered by** | CSO (Dr. Sarah Chen)                         |
| **Trainee**      | James Wright, Natalia Petrova, David Okonkwo |
| **Deadline**     | 30 days                                      |
| **Risk**         | 🔴 High                                      |
| **Curriculum**   | `curricula/masvs-mastery.md`                 |

| Track                  | Trainee         | Scope                                       | Sessions       | Verification                                                          | Pass Bar                                       |
| ---------------------- | --------------- | ------------------------------------------- | -------------- | --------------------------------------------------------------------- | ---------------------------------------------- |
| A — Full Mastery       | James Wright    | All V1–V8, MobSF, Frida, mobile audit       | 4 weeks        | Practical audit (40%) + written exam (35%) + deliverables (25%)       | ≥80% exam, ≥75% audit, 100% critical knowledge |
| B — Framework Review   | Natalia Petrova | Taxonomy, STRIDE mapping, 3 threat models   | 4 weeks        | Threat models (45%) + gap analysis (30%) + integration playbook (25%) | ≥80% across all deliverables                   |
| C — Executive Briefing | David Okonkwo   | MASVS overview + platform gate implications | 1 session (2h) | 10-question comprehension check                                       | ≥70%                                           |

> **Weekly Gate (all tracks):** CSO reviews trainee progress each Friday. Failed gate equals one remediation attempt. Second failure equals training failed and position reopened.

---

### Module B: ADR/TSD Governance — Marcus Andersson, Elena Vasquez, Natalia Petrova

| Field            | Detail                                           |
| ---------------- | ------------------------------------------------ |
| **Delivered by** | CIO (Dr. Priya Mehta) + CTO (Dr. Kenji Nakamura) |
| **Trainee**      | Marcus Andersson, Elena Vasquez, Natalia Petrova |
| **Deadline**     | 30 days                                          |
| **Risk**         | 🟡 Medium                                        |
| **Curriculum**   | `curricula/adr-tsd-governance.md`                |

| Trainee          | Sessions        | Verification                                   | Pass Bar                                              |
| ---------------- | --------------- | ---------------------------------------------- | ----------------------------------------------------- |
| Marcus Andersson | 5 sessions (9h) | Produce 1 compliant ADR independently          | All 7 checklist criteria met on 1st or 2nd submission |
| Elena Vasquez    | 5 sessions (9h) | Produce 1 compliant ADR independently          | All 7 checklist criteria met on 1st or 2nd submission |
| Natalia Petrova  | 5 sessions (9h) | Produce 1 ADR covering non-security dimensions | All 7 checklist criteria met on 1st or 2nd submission |

---

### Module C: IDS Fluency — Elena Vasquez

| Field            | Detail                     |
| ---------------- | -------------------------- |
| **Delivered by** | CDO (Yuki Tanaka-Chen)     |
| **Trainee**      | Elena Vasquez              |
| **Deadline**     | 30 days                    |
| **Risk**         | 🟡 Medium                  |
| **Curriculum**   | `curricula/ids-fluency.md` |

| Trainee       | Sessions        | Verification                                                            | Pass Bar                                              |
| ------------- | --------------- | ----------------------------------------------------------------------- | ----------------------------------------------------- |
| Elena Vasquez | 5 sessions (9h) | Conduct 1 design-engineering feasibility review rated acceptable by CDO | All 7 checklist criteria met on 1st or 2nd submission |

---

### Module D: Defect Triage Protocol — Rachel Kim

| Field            | Detail                                |
| ---------------- | ------------------------------------- |
| **Delivered by** | Test Lead (Priscilla Oduya)           |
| **Trainee**      | Rachel Kim                            |
| **Deadline**     | 30 days                               |
| **Risk**         | 🟡 Medium                             |
| **Curriculum**   | `curricula/defect-triage-protocol.md` |

| Trainee    | Sessions        | Verification                                   | Pass Bar                                                  |
| ---------- | --------------- | ---------------------------------------------- | --------------------------------------------------------- |
| Rachel Kim | 5 sessions (6h) | Classify 10 sample defects using decision tree | ≥8 of 10 classifications match Test Lead's classification |

---

### Module E: Compliance Foundations — Thomas Zhang

| Field            | Detail                                |
| ---------------- | ------------------------------------- |
| **Delivered by** | CSO (Dr. Sarah Chen)                  |
| **Trainee**      | Thomas Zhang                          |
| **Deadline**     | 30 days                               |
| **Risk**         | 🟡 Medium                             |
| **Curriculum**   | `curricula/compliance-foundations.md` |

| Trainee      | Sessions        | Verification                      | Pass Bar                |
| ------------ | --------------- | --------------------------------- | ----------------------- |
| Thomas Zhang | 5 sessions (7h) | Written assessment (10 questions) | ≥7 of 10 correct (≥70%) |

---

### Module F: i18n Strategy Partnering — Marcus Andersson

| Field            | Detail                        |
| ---------------- | ----------------------------- |
| **Delivered by** | CTO-L (Dr. Amara Osei-Mensah) |
| **Trainee**      | Marcus Andersson              |
| **Deadline**     | 30 days                       |
| **Risk**         | 🟢 Low                        |
| **Curriculum**   | Ongoing pairing               |

| Trainee          | Scope                                                              | Verification                                                                   | Pass Bar                      |
| ---------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ----------------------------- |
| Marcus Andersson | Strategic i18n awareness; paired with platform lead during Stage 9 | CTO-L confirms strategic i18n decisions informed by platform-level engineering | CTO-L sign-off during Stage 9 |

---

### Module G: Mobile Scanning Tools — James Wright, Thomas Zhang

| Field            | Detail                                                     |
| ---------------- | ---------------------------------------------------------- |
| **Delivered by** | CSO (Dr. Sarah Chen)                                       |
| **Trainee**      | James Wright, Thomas Zhang                                 |
| **Deadline**     | 30 days                                                    |
| **Risk**         | 🟡 Medium                                                  |
| **Curriculum**   | Part of `curricula/masvs-mastery.md` (practical component) |

| Trainee      | Scope                                         | Verification                                                    | Pass Bar                                |
| ------------ | --------------------------------------------- | --------------------------------------------------------------- | --------------------------------------- |
| James Wright | MobSF scan execution + Frida runtime analysis | Practical exercise: perform security audit on sample mobile app | CSO sign-off on audit findings          |
| Thomas Zhang | MobSF scan execution + result interpretation  | Run MobSF on sample app; interpret results in writing           | CSO sign-off on interpretation accuracy |

---

### Module H: Mobile Threat Modeling — Natalia Petrova

| Field            | Detail                                         |
| ---------------- | ---------------------------------------------- |
| **Delivered by** | CSO (Dr. Sarah Chen)                           |
| **Trainee**      | Natalia Petrova                                |
| **Deadline**     | 30 days                                        |
| **Risk**         | 🟡 Medium                                      |
| **Curriculum**   | Part of `curricula/masvs-mastery.md` (Track B) |

| Trainee         | Scope                                                 | Verification                   | Pass Bar                      |
| --------------- | ----------------------------------------------------- | ------------------------------ | ----------------------------- |
| Natalia Petrova | STRIDE adapted for mobile scenarios (3 threat models) | Produce 3 mobile threat models | CSO sign-off on model quality |

---

### Module I: Accessibility Test Automation — Aisha Patel

| Field            | Detail                         |
| ---------------- | ------------------------------ |
| **Delivered by** | CDO (Yuki Tanaka-Chen) + CTO-L |
| **Trainee**      | Aisha Patel                    |
| **Deadline**     | 30 days                        |
| **Risk**         | 🟡 Medium                      |
| **Curriculum**   | Guided study                   |

| Trainee     | Scope                                                       | Verification                                       | Pass Bar                                |
| ----------- | ----------------------------------------------------------- | -------------------------------------------------- | --------------------------------------- |
| Aisha Patel | axe-core WCAG test suite design + a11y automation baselines | Implement axe-core WCAG 2.1 AA test suite baseline | CDO sign-off on test suite completeness |

---

### Module J: Localization Testing Strategy — Aisha Patel

| Field            | Detail                        |
| ---------------- | ----------------------------- |
| **Delivered by** | CTO-L (Dr. Amara Osei-Mensah) |
| **Trainee**      | Aisha Patel                   |
| **Deadline**     | 30 days                       |
| **Risk**         | 🟡 Medium                     |
| **Curriculum**   | Guided study                  |

| Trainee     | Scope                                                        | Verification                                                                                                                | Pass Bar                                |
| ----------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| Aisha Patel | Localization testing strategy document (not full test suite) | Produce strategy doc covering: pseudo-localization validation, l10n asset verification, cross-platform string parity checks | CTO-L sign-off on strategy completeness |

---

## Module Assignments — Phase 2 (K–W)

### Module K: Frontend Performance Baseline — Amira Voss

| Field            | Detail                                       |
| ---------------- | -------------------------------------------- |
| **Delivered by** | CTO (Dr. Kenji Nakamura)                     |
| **Trainee**      | Amira Voss                                   |
| **Deadline**     | 30 days                                      |
| **Risk**         | 🔴 High                                      |
| **Curriculum**   | `curricula/frontend-performance-baseline.md` |

| Module | Scope                                                                                                                            | Success Criteria                                                                                      | Pass/Fail                                      |
| ------ | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| K-M1   | Establish Lighthouse baseline for Web, iOS WKWebView, Android WebView (6 metrics: LCP, FID, CLS, TTI, bundle size, JS exec time) | All 3 targets covered; all 6 metrics measured; target scores defined with justification; CTO sign-off | PASS = Report accepted; FAIL = Report rejected |

> **Checkpoint structure:**
>
> | Checkpoint | Day | Requirement                                         | Consequence of Miss              |
> | ---------- | --- | --------------------------------------------------- | -------------------------------- |
> | CP1        | 10  | Tooling configured and baseline measurement running | CTO provides direct intervention |
> | CP2        | 20  | Draft report with all 6 metrics for all 3 targets   | CTO pairs on remaining analysis  |
> | Final      | 30  | Final report signed off by CTO                      | Module pass/fail decision        |

---

### Module L: WCAG 2.1 AA Compliance Roadmap for Mobile — Amira Voss

| Field            | Detail                                               |
| ---------------- | ---------------------------------------------------- |
| **Delivered by** | CDO (Yuki Tanaka-Chen) with technical input from CTO |
| **Trainee**      | Amira Voss                                           |
| **Deadline**     | 60 days                                              |
| **Risk**         | 🔴 High                                              |
| **Curriculum**   | `curricula/wcag-mobile-roadmap.md`                   |

| Module | Scope                                                                                                                                                                  | Success Criteria                                                                                                                                                                                              | Pass/Fail                                                                                                      |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| L-M1   | WCAG 2.1 AA compliance roadmap for iOS (VoiceOver, Dynamic Type, Switch Control) and Android (TalkBack, accessibility services) with automated testing pipeline design | Gap analysis covers 38+ WCAG criteria; pipeline design includes tool selection, CI/CD integration, pass/fail thresholds; remediation roadmap is P0–P3 prioritized and platform-specific; CDO and CTO sign-off | PASS = Both CDO and CTO sign off; FAIL = Either officer rejects, or gap analysis misses >5 applicable criteria |

---

### Module M: Mobile Platform Immersion — iOS & Android Pairing — Amira Voss

| Field            | Detail                                                                           |
| ---------------- | -------------------------------------------------------------------------------- |
| **Delivered by** | iOS Lead (Seo-yeon Park) + Android Lead (Kofi Asante-Mensah), coordinated by CTO |
| **Trainee**      | Amira Voss                                                                       |
| **Deadline**     | 90 days                                                                          |
| **Risk**         | 🟡 Medium                                                                        |
| **Curriculum**   | On-demand                                                                        |

| Module | Scope                                                                                                                                  | Success Criteria                                                                                                                                                                                                                                                        | Pass/Fail                                                                                                                                                                       |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| M-M1   | 90-day structured pairing: SwiftUI/UIKit, Jetpack Compose/XML, platform build systems, deployment pipelines, platform review processes | Minimum 16 sessions completed (8 each platform); synthesis document covers UI pattern mapping, performance constraint mapping, accessibility pattern mapping, deployment constraint mapping; both platform leads confirm engagement; CTO sign-off on synthesis document | PASS = 16+ sessions, all 4 mapping areas covered, both leads confirm, CTO signs off; FAIL = Fewer than 16 sessions, any mapping area missing, or any officer withholds sign-off |

---

### Modules N–U: Dr. Elena Rostova — 8 Modules

| Module | Name                                              | Deadline | Risk      | Scope                                                                                                                                     | Success Criteria                                                                                                                                                                                                          | Pass/Fail                                                                                                                                                 |
| ------ | ------------------------------------------------- | -------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| N      | Code Review Participation                         | 90d      | 🔴 High   | ≥20% hands-on PR review participation across all platform PRs                                                                             | Participation rate ≥20%; CTO quality audit of 5 random reviews — each must identify ≥1 substantive issue or approve with valid justification; no missed P0/P1 defects                                                     | PASS = Rate ≥20% and quality audit passes; FAIL = Rate <20%, quality failure, or missed P0/P1                                                             |
| O      | Mobile-Specific ADR Production (3 ADRs)           | 90d      | 🔴 High   | (a) iOS/Android platform layering, (b) shared business logic partitioning (KMP vs. native), (c) offline-first data synchronization        | All 3 ADRs produced and CTO-signed; each ADR meets 7-criteria checklist with ≥1 UML diagram; Rafael pre-approves each ADR                                                                                                 | PASS = All 3 CTO-signed and Rafael-pre-approved; FAIL = Any ADR rejected by CTO after Rafael review, or any ADR missing required criteria                 |
| P      | Weekly Architecture Syncs with Platform Leads     | 90d      | 🟡 Medium | Weekly 1-hour syncs with both platform leads; 1-page weekly summary shared with CTO, CIO, Rafael                                          | Minimum 11 of 12 syncs attended; weekly summaries produced for every session; CTO confirms active architectural leadership; both leads confirm substantive contributions                                                  | PASS = 11+ syncs, 11+ summaries, positive confirmation from CTO and both leads; FAIL = Fewer than 11 syncs, or any officer confirms passive participation |
| Q      | Mobile Platform Architecture Assessment           | 60d      | 🔴 High   | ATS, iOS/Android background execution limits, battery optimization, platform-specific networking stack behaviors                          | All 5 domains covered with constraint description, architectural impact, recommended mitigation, trade-off analysis; CIO sign-off; assessment is actionable for Stage 3 decisions                                         | PASS = All 5 domains covered and CIO sign-off; FAIL = Any domain missing or CIO rejects                                                                   |
| R      | ADR Template Adaptation for Mobile-First Projects | 90d      | 🟡 Medium | Adapt standard ADR template for mobile-first: platform constraints, offline capability, cross-platform sharing, store review requirements | Adapted template includes all standard ADR fields plus mobile-specific extensions; Rafael confirms usability; CIO confirms alignment with TSD standards; template added to company library                                | PASS = Both Rafael and CIO approve; FAIL = Either rejects, or template cannot be applied without significant modification                                 |
| S      | Practice UML + ADR — Mobile Platform Immersion    | 30d      | 🔴 High   | Practice UML class diagram and ADR for offline-first data synchronization (certification exercise)                                        | UML class diagram covers all required components with correct relationships, multiplicities, visibility; ADR follows 7-criteria standard with UML embedded; Rafael confirms zero-ambiguity standard                       | PASS = Rafael signs off on zero-ambiguity; FAIL = Rafael rejects after remediation, or delivered after first Stage 3 engagement                           |
| T      | UML Production Certification                      | 60d      | 🔴 High   | Produce sequence diagram AND component diagram in PlantUML/Mermaid meeting zero-ambiguity standard                                        | Sequence diagram covers 4 paths (happy, offline, conflict, error); component diagram shows all components with boundaries, responsibilities, contracts; both diagrams syntactically valid; Rafael confirms zero-ambiguity | PASS = Rafael certifies both diagrams; FAIL = Rafael rejects after remediation                                                                            |
| U      | Stage 3 Shadowing Program                         | 90d      | 🟡 Medium | Shadow 2 full Stage 3 cycles with Rafael as co-author (Cycle 1: 30/70, Cycle 2: 60/40)                                                    | Both cycles completed with Elena as named co-author; Rafael's assessments show improvement from Cycle 1 to 2; CTO confirms readiness for independent ownership; no architectural defects traced to Elena                  | PASS = Both cycles complete, Rafael confirms improvement, CTO confirms readiness; FAIL = Either cycle incomplete, or CTO/Rafael confirms not ready        |

> **Dependencies:** P11-M6 (Module S) is prerequisite for P11-M2 (Module O) and P11-M7 (Module T). Failure triggers candidacy review. P11-M7 requires P11-M6 pass before certification scenario can begin.

---

### Module V: OWASP MASVS Certification — Omar Farouq

| Field            | Detail                                              |
| ---------------- | --------------------------------------------------- |
| **Delivered by** | CSO (Dr. Sarah Chen) with support from James Wright |
| **Trainee**      | Omar Farouq                                         |
| **Deadline**     | 90 days                                             |
| **Risk**         | 🔴 High                                             |
| **Curriculum**   | `curricula/masvs-mastery.md` (Phase 2 variant)      |

| Module | Scope                                                                           | Success Criteria                                                                                                                                                                 | Pass/Fail                                                                                        |
| ------ | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| V-M1   | OWASP MASVS certification: MASVS-L1, L2, R — V1–V8 (all 8 verification domains) | Written exam ≥80% (80/100); can classify any MASVS requirement into L1/L2/R without reference; produces validated quick-reference card; 10+ of 12 weekly study sessions attended | PASS = Exam ≥80%, card validated, 10+ sessions; FAIL = Exam <80%, <10 sessions, or card rejected |

---

### Module W: Supervised Mobile Application Penetration Testing — Omar Farouq

| Field            | Detail                                               |
| ---------------- | ---------------------------------------------------- |
| **Delivered by** | CSO (Dr. Sarah Chen) with James Wright               |
| **Trainee**      | Omar Farouq                                          |
| **Deadline**     | 90 days                                              |
| **Risk**         | 🔴 High                                              |
| **Curriculum**   | Embedded in `curricula/masvs-mastery.md` (practical) |

| Module | Scope                                                                                   | Success Criteria                                                                                                                                       | Pass/Fail                                                                                                                                |
| ------ | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| W-M1   | Supervised mobile pentests on iOS and Android using MobSF, Frida, Burp Suite, objection | Penetration test reports for both platforms; ≥80% vulnerability detection rate on each; CSO and James both sign off on report quality and presentation | PASS = Both reports, ≥80% detection on both, both officers sign off; FAIL = Either report rejected, or detection <80% on either platform |

> **Dependency:** Requires P13-M1 (Module V — MASVS exam) pass before pentest begins. If exam not passed by Day 70, pentest timeline compresses to 20 days.

---

## Module Assignments — Phase 3 Conditional Hires (AA–BF)

### Module AA: Jetpack Compose Ramp-up — Tariq Al-Hassan

| Field            | Detail                            |
| ---------------- | --------------------------------- |
| **Delivered by** | Android Lead (Kofi Asante-Mensah) |
| **Trainee**      | Tariq Al-Hassan                   |
| **Deadline**     | 60 days                           |
| **Risk**         | 🟡 Medium                         |
| **Curriculum**   | On-demand                         |

| Module | Scope                                                                                             | Success Criteria                                                                                                  | Pass/Fail                                                                                                                                |
| ------ | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| AA-M1  | Compose declarative UI, state management, recomposition, XML interop, M3 theming, Compose testing | Migration of medium-complexity XML screen to Compose accepted; style guide approved; PR review passes quality bar | PASS = Migration accepted, style guide approved, PR review passes; FAIL = Migration rejected, style guide incomplete, or PR review fails |

---

### Module AB: KMP Architecture Training — Priya Narayanan

| Field            | Detail                                   |
| ---------------- | ---------------------------------------- |
| **Delivered by** | Cross-Platform Lead (Mei-Ling Johansson) |
| **Trainee**      | Priya Narayanan                          |
| **Deadline**     | 90 days                                  |
| **Risk**         | 🟡 Medium                                |
| **Curriculum**   | On-demand                                |

| Module | Scope                                                                   | Success Criteria                                                               | Pass/Fail                                                                                                   |
| ------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| AB-M1  | KMP shared modules, expect/actual, Koin DI, coroutines across platforms | Module compiles on both platforms; platform interop tests pass; lead signs off | PASS = Compiles, tests pass, lead signs off; FAIL = Compilation failure, test failure, or sign-off withheld |

---

### Module AC: KMP Architecture Training — Sofia Rezende

| Field            | Detail                                   |
| ---------------- | ---------------------------------------- |
| **Delivered by** | Cross-Platform Lead (Mei-Ling Johansson) |
| **Trainee**      | Sofia Rezende                            |
| **Deadline**     | 90 days                                  |
| **Risk**         | 🟢 Low                                   |
| **Curriculum**   | On-demand                                |

| Module | Scope                                                                                                          | Success Criteria                                                               | Pass/Fail                                                                                                   |
| ------ | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| AC-M1  | KMP shared modules, expect/actual, Koin DI, coroutines across platforms — plus advanced Ktor and serialization | Module compiles on both platforms; platform interop tests pass; lead signs off | PASS = Compiles, tests pass, lead signs off; FAIL = Compilation failure, test failure, or sign-off withheld |

---

### Module AD: UIKit Architecture Review — Lars Eriksson

| Field            | Detail                   |
| ---------------- | ------------------------ |
| **Delivered by** | iOS Lead (Seo-yeon Park) |
| **Trainee**      | Lars Eriksson            |
| **Deadline**     | 60 days                  |
| **Risk**         | 🟢 Low                   |
| **Curriculum**   | On-demand                |

| Module | Scope                                                                        | Success Criteria                                           | Pass/Fail                                                                                               |
| ------ | ---------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| AD-M1  | UIKit patterns review — custom views, Auto Layout, animations, accessibility | Documentation accurate; UIKit-to-SwiftUI bridge functional | PASS = Documentation accurate and bridge functional; FAIL = Documentation gaps or bridge non-functional |

---

### Module AE: SwiftUI Declarative UI Ramp-up — Mei Chen

| Field            | Detail                   |
| ---------------- | ------------------------ |
| **Delivered by** | iOS Lead (Seo-yeon Park) |
| **Trainee**      | Mei Chen                 |
| **Deadline**     | 90 days                  |
| **Risk**         | 🟡 Medium                |
| **Curriculum**   | On-demand                |

| Module | Scope                                                                                                                  | Success Criteria                                                                            | Pass/Fail                                                                                                                          |
| ------ | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| AE-M1  | SwiftUI production proficiency — layout, state management, NavigationStack, custom modifiers, animation, UIKit interop | Screen meets specification; state flow correct; custom component approved for design system | PASS = Screen meets spec, state flow correct, component approved; FAIL = Screen fails spec, state incorrect, or component rejected |

---

### Module AF: Combine Reactive Programming — Amara Diallo

| Field            | Detail                   |
| ---------------- | ------------------------ |
| **Delivered by** | iOS Lead (Seo-yeon Park) |
| **Trainee**      | Amara Diallo             |
| **Deadline**     | 90 days                  |
| **Risk**         | 🟡 Medium                |
| **Curriculum**   | On-demand                |

| Module | Scope                                                                                                 | Success Criteria                                          | Pass/Fail                                                                                                                        |
| ------ | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| AF-M1  | Combine — publishers, subscribers, operators, error handling, Combine/UIKit bridging, Combine testing | Reactive flow correct; test coverage ≥80%; lead signs off | PASS = Reactive flow correct, coverage ≥80%, lead signs off; FAIL = Reactive flow incorrect, coverage <80%, or sign-off withheld |

---

### Module AG: SwiftUI Declarative UI Ramp-up — Hiroshi Tanaka

| Field            | Detail                   |
| ---------------- | ------------------------ |
| **Delivered by** | iOS Lead (Seo-yeon Park) |
| **Trainee**      | Hiroshi Tanaka           |
| **Deadline**     | 90 days                  |
| **Risk**         | 🔴 High                  |
| **Curriculum**   | On-demand                |

| Module | Scope                                                                                                                                               | Success Criteria                                                                            | Pass/Fail                                                                                                                          |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| AG-M1  | SwiftUI production proficiency — layout, state management, NavigationStack, custom modifiers, animation, UIKit interop (score 12/20 — highest risk) | Screen meets specification; state flow correct; custom component approved for design system | PASS = Screen meets spec, state flow correct, component approved; FAIL = Screen fails spec, state incorrect, or component rejected |

> **Checkpoint structure:**
>
> | Checkpoint | Day | Requirement                                              | Consequence of Miss        |
> | ---------- | --- | -------------------------------------------------------- | -------------------------- |
> | CP1        | 30  | Basic layout and state exercises completed               | Bi-weekly reviews mandated |
> | CP2        | 60  | Multi-screen flow implemented independently              | Intensified pairing        |
> | Final      | 90  | All deliverables accepted and component in design system | Module pass/fail decision  |

---

### Module AH: SwiftUI Declarative UI Ramp-up — Arjun Mehta

| Field            | Detail                   |
| ---------------- | ------------------------ |
| **Delivered by** | iOS Lead (Seo-yeon Park) |
| **Trainee**      | Arjun Mehta              |
| **Deadline**     | 90 days                  |
| **Risk**         | 🔴 High                  |
| **Curriculum**   | On-demand                |

| Module | Scope                                                                                                                                | Success Criteria                                                                            | Pass/Fail                                                                                                                          |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| AH-M1  | SwiftUI production proficiency — layout, state management, NavigationStack, custom modifiers, animation, UIKit interop (score 12/20) | Screen meets specification; state flow correct; custom component approved for design system | PASS = Screen meets spec, state flow correct, component approved; FAIL = Screen fails spec, state incorrect, or component rejected |

> **Checkpoint structure:**
>
> | Checkpoint | Day | Requirement                                              | Consequence of Miss        |
> | ---------- | --- | -------------------------------------------------------- | -------------------------- |
> | CP1        | 30  | Basic layout and state exercises completed               | Bi-weekly reviews mandated |
> | CP2        | 60  | Multi-screen flow implemented independently              | Intensified pairing        |
> | Final      | 90  | All deliverables accepted and component in design system | Module pass/fail decision  |

---

### Module AI: Swift Language Familiarization — Dmitri Volkov

| Field            | Detail                                         |
| ---------------- | ---------------------------------------------- |
| **Delivered by** | iOS Lead (Seo-yeon Park) + Cross-Platform Lead |
| **Trainee**      | Dmitri Volkov                                  |
| **Deadline**     | 90 days                                        |
| **Risk**         | 🟢 Low                                         |
| **Curriculum**   | On-demand                                      |

| Module | Scope                                                                                           | Success Criteria                                                              | Pass/Fail                                                                                                                 |
| ------ | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| AI-M1  | Swift proficiency — optionals, generics, protocols, async/await, actors, property wrappers, SPM | Swift module interfacing with KMP compiles; 3 iOS PR reviews meet quality bar | PASS = Module compiles and PR reviews meet quality bar; FAIL = Module fails compilation or PR review quality insufficient |

---

### Module AJ: KMP Architecture Training — Fatima Al-Zahra

| Field            | Detail                                   |
| ---------------- | ---------------------------------------- |
| **Delivered by** | Cross-Platform Lead (Mei-Ling Johansson) |
| **Trainee**      | Fatima Al-Zahra                          |
| **Deadline**     | 90 days                                  |
| **Risk**         | 🟡 Medium                                |
| **Curriculum**   | On-demand                                |

| Module | Scope                                                                                                  | Success Criteria                                                               | Pass/Fail                                                                                                   |
| ------ | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| AJ-M1  | KMP shared modules, expect/actual, Koin DI, coroutines across platforms — with Day 45 milestone review | Module compiles on both platforms; platform interop tests pass; lead signs off | PASS = Compiles, tests pass, lead signs off; FAIL = Compilation failure, test failure, or sign-off withheld |

> **Milestone:** Day 45 milestone review to assess progress and adjust pacing if needed.

---

### Module AK: PWA Engineering — Elena Kim

| Field            | Detail                                    |
| ---------------- | ----------------------------------------- |
| **Delivered by** | CDO (Yuki Tanaka-Chen) + VP Web & Backend |
| **Trainee**      | Elena Kim                                 |
| **Deadline**     | 90 days                                   |
| **Risk**         | 🟢 Low                                    |
| **Curriculum**   | On-demand                                 |

| Module | Scope                                                                                                         | Success Criteria                                        | Pass/Fail                                                                                                 |
| ------ | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| AK-M1  | PWA — service workers, cache strategies, web app manifests, offline-first, push notifications, Lighthouse PWA | Lighthouse PWA score ≥90; deployment checklist approved | PASS = Lighthouse PWA score ≥90 and checklist approved; FAIL = Lighthouse score <90 or checklist rejected |

---

### Module AL: SSR/Next.js Training — Rafael Santos

| Field            | Detail                           |
| ---------------- | -------------------------------- |
| **Delivered by** | VP Web & Backend (Elena Vasquez) |
| **Trainee**      | Rafael Santos                    |
| **Deadline**     | 90 days                          |
| **Risk**         | 🟡 Medium                        |
| **Curriculum**   | On-demand                        |

| Module | Scope                                                                                      | Success Criteria                                                            | Pass/Fail                                                                                                                 |
| ------ | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| AL-M1  | Next.js SSR/SSG/ISR, React Server Components, data fetching, Edge runtime, SSR performance | SSR functional; performance report shows improvement or justified trade-off | PASS = SSR functional and report shows improvement or justified trade-off; FAIL = SSR non-functional or report inadequate |

---

### Module AM: CQRS Architecture Deep-Dive — Viktor Horváth

| Field            | Detail                           |
| ---------------- | -------------------------------- |
| **Delivered by** | VP Web & Backend (Elena Vasquez) |
| **Trainee**      | Viktor Horváth                   |
| **Deadline**     | 60 days                          |
| **Risk**         | 🟡 Medium                        |
| **Curriculum**   | On-demand                        |

| Module | Scope                                                                                                   | Success Criteria                               | Pass/Fail                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------- |
| AM-M1  | CQRS — command/query separation, event sourcing integration, read/write splitting, eventual consistency | Design sound; trade-off analysis comprehensive | PASS = Design sound and analysis comprehensive; FAIL = Design flawed or analysis superficial |

---

### Module AN: Database Sharding Hands-On — Aisha Mohammed

| Field            | Detail                           |
| ---------------- | -------------------------------- |
| **Delivered by** | VP Web & Backend (Elena Vasquez) |
| **Trainee**      | Aisha Mohammed                   |
| **Deadline**     | 60 days                          |
| **Risk**         | 🟡 Medium                        |
| **Curriculum**   | On-demand                        |

| Module | Scope                                                                           | Success Criteria                                               | Pass/Fail                                                                     |
| ------ | ------------------------------------------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| AN-M1  | Sharding — strategies, shard keys, cross-shard queries, rebalancing, monitoring | Proof of concept correct; shard key selection guide actionable | PASS = PoC correct and guide actionable; FAIL = PoC fails or guide incomplete |

---

### Module AO: WebSocket Scaling Architecture — Kael Jensen

| Field            | Detail                           |
| ---------------- | -------------------------------- |
| **Delivered by** | VP Web & Backend (Elena Vasquez) |
| **Trainee**      | Kael Jensen                      |
| **Deadline**     | 60 days                          |
| **Risk**         | 🟡 Medium                        |
| **Curriculum**   | On-demand                        |

| Module | Scope                                                                                                   | Success Criteria                                           | Pass/Fail                                                                                           |
| ------ | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| AO-M1  | WebSocket scaling — connection management, message brokers, sticky sessions, reconnection, backpressure | Architecture meets target connections; load test validates | PASS = Architecture meets targets and load test validates; FAIL = Target not met or load test fails |

---

### Module AP: Go Microservices Development — Omar Hassan

| Field            | Detail                   |
| ---------------- | ------------------------ |
| **Delivered by** | CTO (Dr. Kenji Nakamura) |
| **Trainee**      | Omar Hassan              |
| **Deadline**     | 90 days                  |
| **Risk**         | 🔴 High                  |
| **Curriculum**   | On-demand                |

| Module | Scope                                                                                    | Success Criteria                                                              | Pass/Fail                                                                                                                                 |
| ------ | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| AP-M1  | Go production — syntax, goroutines, channels, HTTP server, gRPC, error handling, testing | Microservice functional; tests pass; test coverage ≥80%; code meets standards | PASS = Microservice functional, tests pass, code meets standards; FAIL = Microservice non-functional, tests fail, or code below standards |

> **Checkpoint structure:**
>
> | Checkpoint | Day | Requirement                                         | Consequence of Miss                     |
> | ---------- | --- | --------------------------------------------------- | --------------------------------------- |
> | CP1        | 30  | Go syntax and concurrency fundamentals demonstrated | Daily check-ins and intensified support |
> | CP2        | 60  | gRPC service functional and unit tests ≥50%         | CTO pairs on remaining work             |
> | Final      | 90  | Microservice production-ready and ≥80% coverage     | Module pass/fail decision               |

---

### Module AQ: PostgreSQL Performance Optimization — Ingrid Nilsen

| Field            | Detail                           |
| ---------------- | -------------------------------- |
| **Delivered by** | VP Web & Backend (Elena Vasquez) |
| **Trainee**      | Ingrid Nilsen                    |
| **Deadline**     | 90 days                          |
| **Risk**         | 🔴 High                          |
| **Curriculum**   | On-demand                        |

| Module | Scope                                                                                               | Success Criteria                                       | Pass/Fail                                                                                                         |
| ------ | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| AQ-M1  | PostgreSQL optimization — EXPLAIN ANALYZE, index strategies, PgBouncer, partitioning, vacuum tuning | ≥8 of 10 queries optimized with measurable improvement | PASS = ≥8 of 10 optimized with measurable improvement; FAIL = Fewer than 8 optimized or no measurable improvement |

> **Checkpoint structure:**
>
> | Checkpoint | Day | Requirement                                        | Consequence of Miss       |
> | ---------- | --- | -------------------------------------------------- | ------------------------- |
> | CP1        | 30  | EXPLAIN ANALYZE proficiency and 3 queries analyzed | VP pairs on analysis      |
> | CP2        | 60  | 7 of 10 queries analyzed with implementation plan  | Intensified review cycle  |
> | Final      | 90  | ≥8 of 10 optimized with measurable improvement     | Module pass/fail decision |

---

### Module AR: AWS Architecture Foundations — Thabo Mokoena

| Field            | Detail                          |
| ---------------- | ------------------------------- |
| **Delivered by** | VP Platform Eng (David Okonkwo) |
| **Trainee**      | Thabo Mokoena                   |
| **Deadline**     | 90 days                         |
| **Risk**         | 🔴 High                         |
| **Curriculum**   | On-demand                       |

| Module | Scope                                                                                             | Success Criteria                                         | Pass/Fail                                                                                                       |
| ------ | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| AR-M1  | AWS — EC2, ECS/EKS, RDS, S3, CloudFront, IAM, VPC, Lambda, CloudWatch, Well-Architected Framework | 3-tier deployment successful; cost estimation reasonable | PASS = Deployment successful and cost estimation reasonable; FAIL = Deployment fails or estimation unreasonable |

> **Checkpoint structure:**
>
> | Checkpoint | Day | Requirement                                  | Consequence of Miss           |
> | ---------- | --- | -------------------------------------------- | ----------------------------- |
> | CP1        | 30  | Core services (EC2, S3, IAM, VPC) configured | David provides guided session |
> | CP2        | 60  | 3-tier app deployed in sandbox               | David reviews architecture    |
> | Final      | 90  | Full deployment and cost estimation complete | Module pass/fail decision     |

---

### Module AS: Docker Orchestration — Nina Petrova

| Field            | Detail                          |
| ---------------- | ------------------------------- |
| **Delivered by** | VP Platform Eng (David Okonkwo) |
| **Trainee**      | Nina Petrova                    |
| **Deadline**     | 60 days                         |
| **Risk**         | 🟡 Medium                       |
| **Curriculum**   | On-demand                       |

| Module | Scope                                                                                     | Success Criteria                               | Pass/Fail                                                                                              |
| ------ | ----------------------------------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| AS-M1  | Docker Compose, container networking, volumes, multi-stage builds, resource limits, CI/CD | All services start; image size reduced by ≥20% | PASS = All services start and image size reduced ≥20%; FAIL = Services fail to start or reduction <20% |

---

### Module AT: Angular Signals Migration — Diego Morales

| Field            | Detail                 |
| ---------------- | ---------------------- |
| **Delivered by** | CDO (Yuki Tanaka-Chen) |
| **Trainee**      | Diego Morales          |
| **Deadline**     | 60 days                |
| **Risk**         | 🟡 Medium              |
| **Curriculum**   | On-demand              |

| Module | Scope                                                                                          | Success Criteria                                        | Pass/Fail                                                                                                |
| ------ | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| AT-M1  | Angular Signals — signal-based state management, computed signals, effects, migration strategy | All 3 components functional; migration guide actionable | PASS = All 3 components functional and guide actionable; FAIL = Any component broken or guide inadequate |

---

### Module AU: WebAuthn & Biometric Auth — Sora Kim

| Field            | Detail                                  |
| ---------------- | --------------------------------------- |
| **Delivered by** | CSO (Dr. Sarah Chen) + VP Web & Backend |
| **Trainee**      | Sora Kim                                |
| **Deadline**     | 90 days                                 |
| **Risk**         | 🔴 High                                 |
| **Curriculum**   | On-demand                               |

| Module | Scope                                                                                                                | Success Criteria                                                         | Pass/Fail                                                                                                                    |
| ------ | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| AU-M1  | WebAuthn/FIDO2 — passkeys, authenticator types, attestation, biometric auth, fallback flows, credential threat model | Authentication functional; CSO review passes; integration guide complete | PASS = Authentication functional, CSO review passes, guide complete; FAIL = Non-functional, CSO rejects, or guide incomplete |

> **Checkpoint structure:**
>
> | Checkpoint | Day | Requirement                                           | Consequence of Miss             |
> | ---------- | --- | ----------------------------------------------------- | ------------------------------- |
> | CP1        | 30  | WebAuthn fundamentals and attestation understood      | CSO provides intensive briefing |
> | CP2        | 60  | Registration flow implemented and tested              | VP pairs on backend integration |
> | Final      | 90  | Full auth flow, CSO review passed, and guide complete | Module pass/fail decision       |

---

### Module AV: Multi-Tenant Data Isolation Architecture — Marcus Wright

| Field            | Detail                 |
| ---------------- | ---------------------- |
| **Delivered by** | VP Web & Backend + CSO |
| **Trainee**      | Marcus Wright          |
| **Deadline**     | 90 days                |
| **Risk**         | 🔴 High                |
| **Curriculum**   | On-demand              |

| Module | Scope                                                                                                            | Success Criteria                                                              | Pass/Fail                                                                                                           |
| ------ | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| AV-M1  | Multi-tenant isolation — schema-per-tenant, row-level security, tenant context propagation, data leak prevention | Prevents cross-tenant leaks; isolation tests pass; CSO security review passes | PASS = Prevents cross-tenant leaks, tests pass, CSO review passes; FAIL = Leak detected, tests fail, or CSO rejects |

> **Checkpoint structure:**
>
> | Checkpoint | Day | Requirement                                            | Consequence of Miss         |
> | ---------- | --- | ------------------------------------------------------ | --------------------------- |
> | CP1        | 30  | Architecture design reviewed by VP and CSO             | Redesign required           |
> | CP2        | 60  | Context propagation implemented and unit tests pass    | VP pairs on isolation logic |
> | Final      | 90  | Full isolation verified and CSO security review passed | Module pass/fail decision   |

---

### Module AW: GCP Multi-Region Architecture — Raihan Rahman

| Field            | Detail                          |
| ---------------- | ------------------------------- |
| **Delivered by** | VP Platform Eng (David Okonkwo) |
| **Trainee**      | Raihan Rahman                   |
| **Deadline**     | 60 days                         |
| **Risk**         | 🟡 Medium                       |
| **Curriculum**   | On-demand                       |

| Module | Scope                                                                                                          | Success Criteria                             | Pass/Fail                                                                                         |
| ------ | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| AW-M1  | GCP multi-region — load balancing, Cloud DNS, global VPC, cross-region replication, disaster recovery, RTO/RPO | Meets RTO/RPO targets; DR runbook actionable | PASS = Meets RTO/RPO targets and runbook actionable; FAIL = RTO/RPO not met or runbook inadequate |

---

### Module AX: Container Runtime Security — Elin Ström

| Field            | Detail               |
| ---------------- | -------------------- |
| **Delivered by** | CSO (Dr. Sarah Chen) |
| **Trainee**      | Elin Ström           |
| **Deadline**     | 60 days              |
| **Risk**         | 🟡 Medium            |
| **Curriculum**   | On-demand            |

| Module | Scope                                                                                                                                      | Success Criteria                                                                          | Pass/Fail                                                                                                                      |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| AX-M1  | Container security — image scanning (Trivy/Grype), runtime detection (Falco), image signing (cosign), SLSA, seccomp, K8s security contexts | Scanning pipeline operational; threat rules fire correctly; hardening guide comprehensive | PASS = Pipeline operational, rules fire correctly, guide comprehensive; FAIL = Pipeline fails, rules miss, or guide incomplete |

---

### Module AY: Bazel Build System Migration Study — Kai Nakamura

| Field            | Detail       |
| ---------------- | ------------ |
| **Delivered by** | DevEx Lead   |
| **Trainee**      | Kai Nakamura |
| **Deadline**     | 60 days      |
| **Risk**         | 🟡 Medium    |
| **Curriculum**   | On-demand    |

| Module | Scope                                                                                                           | Success Criteria                                   | Pass/Fail                                                                                         |
| ------ | --------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| AY-M1  | Bazel — BUILD syntax, WORKSPACE, Kotlin/Java/Swift rules, hermetic builds, remote execution, migration strategy | Study comprehensive; migration estimate defensible | PASS = Study comprehensive and estimate defensible; FAIL = Study has gaps or estimate unjustified |

---

### Module AZ: Test Sharding Architecture — Zara Okonkwo

| Field            | Detail                      |
| ---------------- | --------------------------- |
| **Delivered by** | Test Lead (Priscilla Oduya) |
| **Trainee**      | Zara Okonkwo                |
| **Deadline**     | 60 days                     |
| **Risk**         | 🟡 Medium                   |
| **Curriculum**   | On-demand                   |

| Module | Scope                                                                                                                    | Success Criteria                                         | Pass/Fail                                                                     |
| ------ | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------- | ----------------------------------------------------------------------------- |
| AZ-M1  | Test sharding — distribution strategies, flaky test detection, parallel execution, result aggregation, CI/CD integration | Reduces execution time by ≥30%; proof of concept correct | PASS = Reduces time ≥30% and PoC correct; FAIL = Reduction <30% or PoC flawed |

---

### Module BA: Kubernetes at Scale — Yuki Tanaka

| Field            | Detail                          |
| ---------------- | ------------------------------- |
| **Delivered by** | VP Platform Eng (David Okonkwo) |
| **Trainee**      | Yuki Tanaka                     |
| **Deadline**     | 90 days                         |
| **Risk**         | 🟡 Medium                       |
| **Curriculum**   | On-demand                       |

| Module | Scope                                                                                                                                         | Success Criteria                                                                             | Pass/Fail                                                                                             |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| BA-M1  | K8s operations — cluster architecture, autoscaling (HPA/VPA), resource quotas, network policies, Istio, Prometheus/Grafana, incident response | Autoscaling validated; IR runbook actionable; chaos experiment demonstrates correct failover | PASS = Autoscaling validated, runbook actionable, chaos experiment passes; FAIL = Any criterion unmet |

---

### Module BB: Network Security Fundamentals — Leila Nasser

| Field            | Detail               |
| ---------------- | -------------------- |
| **Delivered by** | CSO (Dr. Sarah Chen) |
| **Trainee**      | Leila Nasser         |
| **Deadline**     | 90 days              |
| **Risk**         | 🔴 High              |
| **Curriculum**   | On-demand            |

| Module | Scope                                                                                                     | Success Criteria                                                                                 | Pass/Fail                                                                                                                                 |
| ------ | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| BB-M1  | Network security — OSI model, TLS/mTLS, network segmentation, firewalls, DDoS mitigation, WAF, zero-trust | Identifies ≥80% vulnerabilities; WAF configured correctly; fundamentals course verified complete | PASS = ≥80% vulnerabilities identified, WAF correct, course verified; FAIL = <80% identification, WAF misconfigured, or course incomplete |

> **Checkpoint structure:**
>
> | Checkpoint | Day | Requirement                                              | Consequence of Miss               |
> | ---------- | --- | -------------------------------------------------------- | --------------------------------- |
> | CP1        | 30  | Fundamentals course ≥50% complete                        | CSO provides guided study session |
> | CP2        | 60  | Network security assessment draft complete               | CSO reviews and provides feedback |
> | Final      | 90  | Course complete, WAF configured, and assessment approved | Module pass/fail decision         |

---

### Module BC: Unit Test Architecture — Ananya Krishnan

| Field            | Detail                      |
| ---------------- | --------------------------- |
| **Delivered by** | Test Lead (Priscilla Oduya) |
| **Trainee**      | Ananya Krishnan             |
| **Deadline**     | 60 days                     |
| **Risk**         | 🟡 Medium                   |
| **Curriculum**   | On-demand                   |

| Module | Scope                                                                                                                                 | Success Criteria                                    | Pass/Fail                                                                                                             |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| BC-M1  | Unit test architecture — test pyramid, mock/stub patterns, test data management, test isolation, flaky test detection, CI integration | Architecture sound; tests consistent; coverage ≥80% | PASS = Architecture sound, tests consistent, coverage ≥80%; FAIL = Architecture flawed, tests flaky, or coverage <80% |

---

### Module BD: CI/CD Test Integration — Tobias Weber

| Field            | Detail                  |
| ---------------- | ----------------------- |
| **Delivered by** | Test Lead + DevOps Lead |
| **Trainee**      | Tobias Weber            |
| **Deadline**     | 90 days                 |
| **Risk**         | 🔴 High                 |
| **Curriculum**   | On-demand               |

| Module | Scope                                                                                                                   | Success Criteria                                                                | Pass/Fail                                                                                                                                |
| ------ | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| BD-M1  | CI/CD test pipeline — test triggering, parallel execution, result reporting, flaky quarantine, environment provisioning | Pipeline operational; tests trigger correctly; troubleshooting guide actionable | PASS = Pipeline operational, tests trigger correctly, guide actionable; FAIL = Pipeline fails, tests do not trigger, or guide inadequate |

> **Note:** Runs parallel with Module BE.
>
> **Checkpoint structure:**
>
> | Checkpoint | Day | Requirement                                           | Consequence of Miss       |
> | ---------- | --- | ----------------------------------------------------- | ------------------------- |
> | CP1        | 30  | Pipeline design approved by Test Lead and DevOps Lead | Redesign required         |
> | CP2        | 60  | Auto-triggering functional and reporting operational  | Joint officer pairing     |
> | Final      | 90  | Full pipeline and troubleshooting guide complete      | Module pass/fail decision |

---

### Module BE: Native Mobile Test Frameworks — Espresso & XCTest — Tobias Weber

| Field            | Detail                              |
| ---------------- | ----------------------------------- |
| **Delivered by** | Test Lead + Android Lead + iOS Lead |
| **Trainee**      | Tobias Weber                        |
| **Deadline**     | 90 days                             |
| **Risk**         | 🔴 High                             |
| **Curriculum**   | On-demand                           |

| Module | Scope                                                                                                                 | Success Criteria                                                                         | Pass/Fail                                                                                                                                 |
| ------ | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| BE-M1  | Espresso (ViewMatchers, Intents, IdlingResource) and XCTest (XCUIElement, performance testing, screenshot comparison) | All 10+ tests pass reliably; both platform leads approve; comparison guide comprehensive | PASS = All 10+ tests pass reliably, both leads approve, guide comprehensive; FAIL = Tests flaky, either lead rejects, or guide inadequate |

> **Note:** Runs parallel with Module BD.

---

### Module BF: Mobile Testing Fundamentals — Priya Sharma

| Field            | Detail                   |
| ---------------- | ------------------------ |
| **Delivered by** | Test Lead + Android Lead |
| **Trainee**      | Priya Sharma             |
| **Deadline**     | 60 days                  |
| **Risk**         | 🟡 Medium                |
| **Curriculum**   | On-demand                |

| Module | Scope                                                                                                                                              | Success Criteria                                                      | Pass/Fail                                                                                                                                              |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| BF-M1  | Mobile testing — mobile vs web differences, device matrix, emulator vs real device, network condition simulation, mobile perf testing, mobile a11y | Strategy comprehensive; tests cover critical paths; sign-off obtained | PASS = Strategy comprehensive, tests cover critical paths, sign-off obtained; FAIL = Strategy has gaps, critical paths uncovered, or sign-off withheld |

---

## At-Risk Conditions

### Phase 1 At-Risk Conditions

| #   | Trainee         | Module                                          | Rationale                                                                              | Mitigation                                                                                                                                             | Risk      |
| --- | --------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- |
| 1   | James Wright    | MASVS Mastery (Track A) + Mobile Scanning Tools | 60-day timeline is aggressive for full MASVS mastery across all 8 verification domains | CSO commits to 2x/week sessions; practical exam on Day 28                                                                                              | 🔴 High   |
| 2   | Natalia Petrova | CI/CD Security KT with Thomas Zhang             | Reassigned from original 60-day timeline                                               | **Reassigned:** CSO provides CI/CD security overview directly. Thomas KT becomes optional enrichment                                                   | 🟡 Medium |
| 3   | Aisha Patel     | Localization Testing + Accessibility Automation | 90-day timeline for full test suite design and implementation is too aggressive        | **Scope reduced:** Strategy document only (not full test suite). CTO-L provides template, reviews within 14 days                                       | 🔴 High   |
| 4   | Elena Vasquez   | Nominate Frontend Implementation Lead           | 60-day deadline conflicts with IDS fluency and ADR governance completion               | **Deferred:** Complete IDS fluency and ADR governance in 30 days; nomination deferred to Day 60 (Phase 2 dependency). Does not block duty commencement | 🟡 Medium |

### Phase 2 At-Risk Conditions

| #   | Trainee                 | Module                                          | Rationale                                                                                      | Mitigation                                                                                                            | Risk    |
| --- | ----------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------- |
| 5   | Amira Voss (P9)         | P9-M1: Frontend Performance Baseline            | 30-day deadline for 3-platform baseline is aggressive; web-first background                    | CTO provides tooling Day 1; weekly check-ins; if behind at Day 15, platform lead assists                              | 🔴 High |
| 6   | Amira Voss (P9)         | P9-M2: WCAG 2.1 AA Mobile Roadmap               | Large surface area; requires cross-platform CI/CD knowledge                                    | CDO provides Instagram audit framework; structured milestones (gap analysis Day 30, pipeline Day 45, roadmap Day 60)  | 🔴 High |
| 7   | Dr. Elena Rostova (P11) | P11-M1: Code Review Participation               | ≥20% rate depends on PR volume — low volume blocks threshold, high volume risks quality        | CTO monitors PR volume weekly; assigns historical PRs if insufficient, caps load if excessive                         | 🔴 High |
| 8   | Dr. Elena Rostova (P11) | P11-M2: Mobile-Specific ADR Production          | 3 ADRs in 90 days alongside 7 other modules is significant load                                | Rafael provides template and 60+ reference ADRs Day 1; sequenced delivery (Day 30/60/90) distributes workload         | 🔴 High |
| 9   | Dr. Elena Rostova (P11) | P11-M4: Mobile Platform Architecture Assessment | Non-mobile-native background; deep platform knowledge required                                 | CIO provides Stripe mobile SDK documentation as baseline; 2-hour deep-dive at Day 30 to identify gaps                 | 🔴 High |
| 10  | Dr. Elena Rostova (P11) | P11-M6: Practice UML + ADR                      | Gate to Stage 3 authorship — failure blocks core function; zero-ambiguity standard unforgiving | Rafael provides scenario brief Day 1; UML standards walkthrough Week 1; one remediation attempt                       | 🔴 High |
| 11  | Dr. Elena Rostova (P11) | P11-M7: UML Production Certification            | Zero-ambiguity bar from Airbnb is extremely high; failure blocks solo Stage 3 authorship       | Rafael provides standards document Day 1; distinct scenario from P11-M6; one remediation with coaching                | 🔴 High |
| 12  | Omar Farouq (P13)       | P13-M1: MASVS Certification                     | 8 verification domains across 3 levels; ≥80% exam is high bar                                  | James conducts weekly study sessions; CSO practice exams at Day 30/60; if below 70% at Day 60, intensifies to 2x/week | 🔴 High |
| 13  | Omar Farouq (P13)       | P13-M2: Supervised Mobile Pentesting            | ≥80% detection rate on both platforms; steep tooling learning curve (Frida, objection, MobSF)  | CSO provides targets Day 1; James provides tooling tutorials Weeks 1–3; mid-point review Day 45                       | 🔴 High |

### Phase 3 At-Risk Conditions

| #   | Trainee         | Module                                       | Rationale                                                                                    | Mitigation                                                                                           | Risk      |
| --- | --------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | --------- |
| 14  | Hiroshi Tanaka  | AG: SwiftUI Declarative UI Ramp-up           | Score 12/20 — highest risk SwiftUI module; 90-day deadline with checkpoint dependency        | Day 30/60/90 checkpoints enforced; bi-weekly reviews from iOS Lead; CP1 miss triggers daily pairing  | 🔴 High   |
| 15  | Arjun Mehta     | AH: SwiftUI Declarative UI Ramp-up           | Score 12/20 — identical risk profile to Hiroshi; parallel execution compounds iOS Lead load  | Staggered sessions with Hiroshi; Day 30/60/90 checkpoints; CP1 miss triggers intensified pairing     | 🔴 High   |
| 16  | Omar Hassan     | AP: Go Microservices Development             | Non-Go background; 90 days to production-level proficiency with ≥80% test coverage           | CTO provides reference services Day 1; Day 30/60/90 checkpoints; CP1 miss triggers daily check-ins   | 🔴 High   |
| 17  | Ingrid Nilsen   | AQ: PostgreSQL Performance Optimization      | Deep database internals required; ≥8/10 queries optimized with measurable improvement        | VP provides slow query log Day 1; Day 30/60/90 checkpoints; pairs on analysis if CP1 missed          | 🔴 High   |
| 18  | Thabo Mokoena   | AR: AWS Architecture Foundations             | Broad AWS surface area (9+ services); 3-tier deployment and cost estimation in 90 days       | David provides sandbox Day 1; Day 30/60/90 checkpoints; guided session if CP1 missed                 | 🔴 High   |
| 19  | Sora Kim        | AU: WebAuthn & Biometric Auth                | Security-critical module; CSO and VP dual delivery; credential threat model complexity       | Day 30/60/90 checkpoints; CSO intensive briefing if CP1 missed; VP pairs on backend if CP2 delayed   | 🔴 High   |
| 20  | Marcus Wright   | AV: Multi-Tenant Data Isolation Architecture | Zero-tolerance for data leaks; dual sign-off (VP and CSO); architectural complexity          | Day 30/60/90 checkpoints; redesign required if CP1 fails; VP pairs on isolation logic if CP2 delayed | 🔴 High   |
| 21  | Leila Nasser    | BB: Network Security Fundamentals            | Fundamentals course and WAF configuration and assessment in 90 days; non-security background | Day 30/60/90 checkpoints; CSO guided study if CP1 behind; feedback loop on assessment draft at CP2   | 🔴 High   |
| 22  | Tobias Weber    | BD: CI/CD Test Integration                   | Dual-delivery (Test Lead and DevOps Lead); pipeline design, implementation, and guide in 90d | Day 30/60/90 checkpoints; redesign if CP1 fails; joint officer pairing if CP2 delayed                | 🔴 High   |
| 23  | Tobias Weber    | BE: Native Mobile Test Frameworks            | Two frameworks (Espresso and XCTest) with dual platform lead reviews; parallel with BD       | Kofi and Seo-yeon staggered review sessions; 10+ tests must pass reliably; comparison guide required | 🔴 High   |
| 24  | Tariq Al-Hassan | AA: Jetpack Compose Ramp-up                  | 60-day XML-to-Compose migration deadline; medium complexity screen                           | Kofi provides production examples Day 1; weekly pairing sessions                                     | 🟡 Medium |
| 25  | Priya Narayanan | AB: KMP Architecture Training                | 90-day cross-platform compilation and interop tests; new KMP paradigm                        | Mei-Ling provides architecture docs Day 1; mid-point review at Day 45                                | 🟡 Medium |
| 26  | Fatima Al-Zahra | AJ: KMP Architecture Training                | Same as AB with Day 45 milestone review; timeline risk if milestone missed                   | Day 45 milestone review enforced; if missed, pacing adjustment required                              | 🟡 Medium |
| 27  | Rafael Santos   | AL: SSR/Next.js Training                     | CSR-to-SSR conversion and performance report; trade-off justification required               | VP provides architecture docs Day 1; Day 45 progress check                                           | 🟡 Medium |
| 28  | Viktor Horváth  | AM: CQRS Architecture Deep-Dive              | CQRS design and trade-off analysis; architectural complexity                                 | VP provides reference architecture Day 1; Day 30 design review                                       | 🟡 Medium |
| 29  | Aisha Mohammed  | AN: Database Sharding Hands-On               | PoC and shard key guide in 60 days; practical complexity                                     | VP provides test environment Day 1; Day 30 PoC review                                                | 🟡 Medium |
| 30  | Kael Jensen     | AO: WebSocket Scaling Architecture           | Scaled architecture design and load test in 60 days; performance targets must be met         | VP provides current architecture Day 1; Day 30 design review                                         | 🟡 Medium |
| 31  | Nina Petrova    | AS: Docker Orchestration                     | 5+ service Compose and Dockerfile optimization in 60 days                                    | David provides microservice architecture Day 1; Day 30 Compose review                                | 🟡 Medium |
| 32  | Diego Morales   | AT: Angular Signals Migration                | 3 component migration and guide in 60 days; migration strategy complexity                    | CDO provides architecture docs Day 1; Day 30 migration review                                        | 🟡 Medium |
| 33  | Raihan Rahman   | AW: GCP Multi-Region Architecture            | Multi-region design and DR runbook in 60 days; RTO/RPO targets must be met                   | David provides architecture Day 1; Day 30 design review                                              | 🟡 Medium |
| 34  | Elin Ström      | AX: Container Runtime Security               | Scanning pipeline and threat rules and hardening guide in 60 days                            | CSO provides baseline Day 1; Day 30 pipeline review                                                  | 🟡 Medium |
| 35  | Kai Nakamura    | AY: Bazel Build System Migration Study       | Comprehensive migration study and defensible estimate in 60 days                             | DevEx Lead provides build docs Day 1; Day 30 research review                                         | 🟡 Medium |
| 36  | Zara Okonkwo    | AZ: Test Sharding Architecture               | ≥30% execution time reduction and PoC in 60 days                                             | Priscilla provides pipeline docs Day 1; Day 30 strategy review                                       | 🟡 Medium |
| 37  | Yuki Tanaka     | BA: Kubernetes at Scale                      | Autoscaling and IR runbook and chaos experiment in 90 days                                   | David provides architecture Day 1; Day 45 autoscaling review                                         | 🟡 Medium |
| 38  | Ananya Krishnan | BC: Unit Test Architecture                   | Architecture design and ≥80% coverage suite in 60 days                                       | Priscilla provides docs Day 1; Day 30 architecture review                                            | 🟡 Medium |
| 39  | Priya Sharma    | BF: Mobile Testing Fundamentals              | Test strategy and critical path tests in 60 days; mobile testing unfamiliarity               | Priscilla and Kofi provide docs Day 1; Day 30 strategy review                                        | 🟡 Medium |

### Cross-Module Dependencies (Phase 2)

| Dependent Module           | Depends On                   | Consequence of Failure                                      |
| -------------------------- | ---------------------------- | ----------------------------------------------------------- |
| P11-M2 (Mobile ADRs)       | P11-M6 (Practice UML+ADR)    | If P11-M6 fails, candidacy review triggered                 |
| P11-M7 (UML Certification) | P11-M6 (Practice UML+ADR)    | If P11-M6 fails, candidacy review triggered                 |
| P13-M2 (Mobile Pentesting) | P13-M1 (MASVS Certification) | If exam not passed by Day 70, pentest compressed to 20 days |

### Cross-Module Dependencies (Phase 3)

| Dependent Module            | Depends On                  | Consequence of Failure                                          |
| --------------------------- | --------------------------- | --------------------------------------------------------------- |
| BD (CI/CD Test Integration) | BE (Native Mobile Testing)  | Parallel execution — if BE delayed, BD timeline may extend      |
| BE (Native Mobile Testing)  | BD (CI/CD Test Integration) | Parallel execution — shared trainee (Tobias Weber) creates load |
| AG/AH (SwiftUI Ramp-up)     | —                           | Both trainees share iOS Lead — session scheduling conflict risk |

---

## Failure Protocol

If a trainee fails to complete any assigned module by the specified deadline:

1. **Day of deadline:** Responsible officer confirms failure and documents the specific module(s) not completed
2. **Day of deadline:** CHRO notifies the trainee, their supervisor, and the CTO of the failure
3. **Day +1:** CHRO initiates recruitment reopening for the position
4. **Day +1:** Trainee's access to production systems is suspended
5. **Day +1–7:** CHRO reviews lessons learned — was the condition unrealistic? Was the delivery inadequate? Was the trainee's capability misassessed?
6. **Day +7:** CHRO updates this training plan with lessons learned to prevent recurrence
7. **Day +7:** Recruitment for the position resumes via the standard CHRO recruitment process

**No exceptions.** This protocol applies to all Phase 1, Phase 2, and Phase 3 hires equally.

---

## Curriculum Index

| Module                                 | Curriculum File                                      | Delivered By             | Trainees                                            |
| -------------------------------------- | ---------------------------------------------------- | ------------------------ | --------------------------------------------------- |
| **A: MASVS Mastery**                   | `curricula/masvs-mastery.md`                         | CSO                      | James (Track A), Natalia (Track B), David (Track C) |
| **B: ADR/TSD Governance**              | `curricula/adr-tsd-governance.md`                    | CIO + CTO                | Marcus, Elena, Natalia                              |
| **C: IDS Fluency**                     | `curricula/ids-fluency.md`                           | CDO                      | Elena                                               |
| **D: Defect Triage Protocol**          | `curricula/defect-triage-protocol.md`                | Test Lead                | Rachel                                              |
| **E: Compliance Foundations**          | `curricula/compliance-foundations.md`                | CSO                      | Thomas                                              |
| **F: i18n Strategy Partnering**        | Ongoing pairing (no curriculum file)                 | CTO-L                    | Marcus                                              |
| **G: Mobile Scanning Tools**           | Embedded in `curricula/masvs-mastery.md`             | CSO                      | James, Thomas                                       |
| **H: Mobile Threat Modeling**          | Embedded in `curricula/masvs-mastery.md`             | CSO                      | Natalia                                             |
| **I: Accessibility Test Automation**   | Guided study (no curriculum file)                    | CDO + CTO-L              | Aisha                                               |
| **J: Localization Testing Strategy**   | Guided study (no curriculum file)                    | CTO-L                    | Aisha                                               |
| **K: Frontend Performance Baseline**   | `curricula/frontend-performance-baseline.md`         | CTO                      | Amira Voss (P9)                                     |
| **L: WCAG 2.1 AA Mobile Roadmap**      | `curricula/wcag-mobile-roadmap.md`                   | CDO                      | Amira Voss (P9)                                     |
| **M: Mobile Platform Immersion**       | Ongoing pairing (no curriculum file)                 | iOS Lead + Android Lead  | Amira Voss (P9)                                     |
| **N: Code Review Participation**       | Tracking metric (no curriculum file)                 | CTO                      | Dr. Elena Rostova (P11)                             |
| **O: Mobile-Specific ADRs**            | Embedded in `curricula/adr-tsd-governance.md`        | CTO + Rafael             | Dr. Elena Rostova (P11)                             |
| **P: Weekly Architecture Syncs**       | Tracking metric (no curriculum file)                 | CTO (coordinating)       | Dr. Elena Rostova (P11)                             |
| **Q: Mobile Platform Assessment**      | `curricula/mobile-platform-assessment.md`            | CIO                      | Dr. Elena Rostova (P11)                             |
| **R: ADR Template Adaptation**         | `curricula/adr-template-mobile.md`                   | CIO + Rafael             | Dr. Elena Rostova (P11)                             |
| **S: Practice UML + ADR**              | `curricula/uml-production-certification.md`          | Rafael                   | Dr. Elena Rostova (P11)                             |
| **T: UML Production Certification**    | `curricula/uml-production-certification.md`          | Rafael                   | Dr. Elena Rostova (P11)                             |
| **U: Stage 3 Shadowing**               | Ongoing pairing (no curriculum file)                 | Rafael + CTO             | Dr. Elena Rostova (P11)                             |
| **V: MASVS Certification (Phase 2)**   | `curricula/masvs-mastery.md` (Phase 2 variant)       | CSO + James Wright       | Omar Farouq (P13)                                   |
| **W: Supervised Mobile Pentesting**    | Embedded in `curricula/masvs-mastery.md` (practical) | CSO + James Wright       | Omar Farouq (P13)                                   |
| **AA: Jetpack Compose Ramp-up**        | On-demand (Android Lead)                             | Android Lead             | Tariq Al-Hassan                                     |
| **AB: KMP Architecture Training**      | On-demand (Cross-Platform Lead)                      | Cross-Platform Lead      | Priya Narayanan                                     |
| **AC: KMP Architecture Training**      | On-demand (Cross-Platform Lead)                      | Cross-Platform Lead      | Sofia Rezende                                       |
| **AD: UIKit Architecture Review**      | On-demand (iOS Lead)                                 | iOS Lead                 | Lars Eriksson                                       |
| **AE: SwiftUI Declarative UI**         | On-demand (iOS Lead)                                 | iOS Lead                 | Mei Chen                                            |
| **AF: Combine Reactive Programming**   | On-demand (iOS Lead)                                 | iOS Lead                 | Amara Diallo                                        |
| **AG: SwiftUI Declarative UI**         | On-demand (iOS Lead)                                 | iOS Lead                 | Hiroshi Tanaka                                      |
| **AH: SwiftUI Declarative UI**         | On-demand (iOS Lead)                                 | iOS Lead                 | Arjun Mehta                                         |
| **AI: Swift Language Familiarization** | On-demand (iOS Lead + Cross-Platform Lead)           | iOS Lead + X-Platform    | Dmitri Volkov                                       |
| **AJ: KMP Architecture Training**      | On-demand (Cross-Platform Lead)                      | Cross-Platform Lead      | Fatima Al-Zahra                                     |
| **AK: PWA Engineering**                | On-demand (CDO + VP Web & Backend)                   | CDO + VP Web & Backend   | Elena Kim                                           |
| **AL: SSR/Next.js Training**           | On-demand (VP Web & Backend)                         | VP Web & Backend         | Rafael Santos                                       |
| **AM: CQRS Architecture Deep-Dive**    | On-demand (VP Web & Backend)                         | VP Web & Backend         | Viktor Horváth                                      |
| **AN: Database Sharding Hands-On**     | On-demand (VP Web & Backend)                         | VP Web & Backend         | Aisha Mohammed                                      |
| **AO: WebSocket Scaling Arch.**        | On-demand (VP Web & Backend)                         | VP Web & Backend         | Kael Jensen                                         |
| **AP: Go Microservices Development**   | On-demand (CTO)                                      | CTO                      | Omar Hassan                                         |
| **AQ: PostgreSQL Performance Opt.**    | On-demand (VP Web & Backend)                         | VP Web & Backend         | Ingrid Nilsen                                       |
| **AR: AWS Architecture Foundations**   | On-demand (VP Platform Eng)                          | VP Platform Eng          | Thabo Mokoena                                       |
| **AS: Docker Orchestration**           | On-demand (VP Platform Eng)                          | VP Platform Eng          | Nina Petrova                                        |
| **AT: Angular Signals Migration**      | On-demand (CDO)                                      | CDO                      | Diego Morales                                       |
| **AU: WebAuthn & Biometric Auth**      | On-demand (CSO + VP Web & Backend)                   | CSO + VP Web & Backend   | Sora Kim                                            |
| **AV: Multi-Tenant Data Isolation**    | On-demand (VP Web & Backend + CSO)                   | VP Web & Backend + CSO   | Marcus Wright                                       |
| **AW: GCP Multi-Region Arch.**         | On-demand (VP Platform Eng)                          | VP Platform Eng          | Raihan Rahman                                       |
| **AX: Container Runtime Security**     | On-demand (CSO)                                      | CSO                      | Elin Ström                                          |
| **AY: Bazel Build System Migration**   | On-demand (DevEx Lead)                               | DevEx Lead               | Kai Nakamura                                        |
| **AZ: Test Sharding Architecture**     | On-demand (Test Lead)                                | Test Lead                | Zara Okonkwo                                        |
| **BA: Kubernetes at Scale**            | On-demand (VP Platform Eng)                          | VP Platform Eng          | Yuki Tanaka                                         |
| **BB: Network Security Fundamentals**  | On-demand (CSO)                                      | CSO                      | Leila Nasser                                        |
| **BC: Unit Test Architecture**         | On-demand (Test Lead)                                | Test Lead                | Ananya Krishnan                                     |
| **BD: CI/CD Test Integration**         | On-demand (Test Lead + DevOps Lead)                  | Test Lead + DevOps Lead  | Tobias Weber                                        |
| **BE: Native Mobile Test Frameworks**  | On-demand (Test Lead + Android Lead + iOS Lead)      | Test + Android + iOS     | Tobias Weber                                        |
| **BF: Mobile Testing Fundamentals**    | On-demand (Test Lead + Android Lead)                 | Test Lead + Android Lead | Priya Sharma                                        |

---

## Weekly Check-In Schedule

### Phase 1

| Day       | Responsible Officer | Trainees                      | Check-In Format                         |
| --------- | ------------------- | ----------------------------- | --------------------------------------- |
| Monday    | CSO                 | James, Natalia, David, Thomas | Written update in `progress/tracker.md` |
| Tuesday   | CIO + CTO           | Marcus, Elena, Natalia        | Written update in `progress/tracker.md` |
| Wednesday | CDO                 | Elena, Aisha                  | Written update in `progress/tracker.md` |
| Thursday  | Test Lead           | Rachel                        | Written update in `progress/tracker.md` |
| Friday    | CTO-L               | Marcus, Aisha                 | Written update in `progress/tracker.md` |

### Phase 2

| Day       | Responsible Officer | Trainees                                 | Check-In Format                         |
| --------- | ------------------- | ---------------------------------------- | --------------------------------------- |
| Monday    | CTO                 | Amira Voss (P9), Dr. Elena Rostova (P11) | Written update in `progress/tracker.md` |
| Tuesday   | CIO                 | Dr. Elena Rostova (P11)                  | Written update in `progress/tracker.md` |
| Wednesday | CDO                 | Amira Voss (P9)                          | Written update in `progress/tracker.md` |
| Thursday  | Rafael Okonkwo      | Dr. Elena Rostova (P11)                  | Written update in `progress/tracker.md` |
| Friday    | CSO                 | Omar Farouq (P13)                        | Written update in `progress/tracker.md` |

### Phase 3

| Day       | Responsible Officer      | Trainees                                                                                                           | Check-In Format                         |
| --------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------- |
| Monday    | CTO                      | Omar Hassan (AP)                                                                                                   | Written update in `progress/tracker.md` |
| Tuesday   | iOS Lead (Seo-yeon Park) | Lars Eriksson (AD), Mei Chen (AE), Amara Diallo (AF), Hiroshi Tanaka (AG), Arjun Mehta (AH)                        | Written update in `progress/tracker.md` |
| Wednesday | Android Lead (Kofi)      | Tariq Al-Hassan (AA)                                                                                               | Written update in `progress/tracker.md` |
| Wednesday | CSO                      | Sora Kim (AU), Marcus Wright (AV), Elin Ström (AX), Leila Nasser (BB)                                              | Written update in `progress/tracker.md` |
| Thursday  | Cross-Platform Lead      | Priya Narayanan (AB), Sofia Rezende (AC), Dmitri Volkov (AI), Fatima Al-Zahra (AJ)                                 | Written update in `progress/tracker.md` |
| Thursday  | Test Lead                | Zara Okonkwo (AZ), Ananya Krishnan (BC), Tobias Weber (BD, BE), Priya Sharma (BF)                                  | Written update in `progress/tracker.md` |
| Friday    | VP Web & Backend         | Elena Kim (AK), Rafael Santos (AL), Viktor Horváth (AM), Aisha Mohammed (AN), Kael Jensen (AO), Ingrid Nilsen (AQ) | Written update in `progress/tracker.md` |
| Friday    | VP Platform Eng          | Thabo Mokoena (AR), Nina Petrova (AS), Raihan Rahman (AW), Yuki Tanaka (BA)                                        | Written update in `progress/tracker.md` |

**Check-in content (per trainee):**

- Module(s) in progress: [list]
- Session completed this week: [yes/no — which session/module]
- Progress status: [on track / at risk / behind]
- Next session scheduled: [date]
- Concerns or blockers: [free text]
- Officer sign-off: [initials]

> **Note:** Modules with checkpoint structures (AG, AH, AP, AQ, AR, AU, AV, BB, BD) require checkpoint status reporting in addition to standard weekly check-in content.

---

## Contributing Officers (Phase 3 Training Reviews)

The following 9 officers conducted post-training skill reviews for all 42 conditional hires:

| #   | Officer                                  | Role                            | Reviews Conducted                   |
| --- | ---------------------------------------- | ------------------------------- | ----------------------------------- |
| 1   | CTO (Dr. Kenji Nakamura)                 | Chief Technology Officer        | 30 trainees (Phase 2 + Phase 3 R&D) |
| 2   | CDO (Yuki Tanaka-Chen)                   | Chief Design Officer            | 3 trainees                          |
| 3   | CSO (Dr. Sarah Chen)                     | Chief Security Officer          | 5 trainees                          |
| 4   | Test Lead (Priscilla Oduya)              | Test Lead                       | 4 trainees                          |
| 5   | CTO-L (Dr. Amara Osei-Mensah)            | Chief Translation Officer       | 1 trainee                           |
| 6   | CIO (Dr. Priya Mehta)                    | Chief Information Officer       | 3 trainees                          |
| 7   | Android Lead (Kofi Asante-Mensah)        | Android Development Lead        | 1 trainee                           |
| 8   | iOS Lead (Seo-yeon Park)                 | iOS Development Lead            | 5 trainees                          |
| 9   | Cross-Platform Lead (Mei-Ling Johansson) | Cross-Platform Development Lead | 4 trainees                          |

**Total reviews conducted:** 56 (some trainees reviewed by multiple officers) across 42 unique trainees. All reviews resulted in PASS. Full review details are in `progress/chief-officer-skill-reviews.md`.

---

## Document History

| Version | Date       | Author      | Changes                                                                                                                                                                                                                                                                                         | Status                                 |
| ------- | ---------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| 1.0     | 2026-04-03 | CHRO Office | Initial training plan — 8 trainees, 10 modules, 30-day probationary period                                                                                                                                                                                                                      | ⏳ Pending Activation                  |
| 1.1     | 2026-04-04 | CHRO Office | Phase 2 conditional training consolidated — 3 additional trainees, 13 modules (K–W), 90-day probationary; Phase 1/Phase 2 sections separated; readability reform                                                                                                                                | ⏳ Active Phase 1, Pending Phase 2     |
| 1.2     | 2026-04-04 | CHRO Office | Phase 3 conditional hires added — 32 modules (AA–BF) across Mobile, Frontend, Backend, Full-Stack, Platform, QA; At-Risk table extended (#14–39); Curriculum Index expanded; Weekly Check-In Schedule expanded with Phase 3 officers                                                            | ⏳ Active Phase 1, Pending Phase 2 & 3 |
| 1.3     | 2026-04-05 | CHRO Office | All 62 modules passed across 42 trainees. All phases complete. Status updated to ✅ Complete. Phase 3 Training Reviews section added with 9 reviewing officers. All trainee registry statuses updated to ✅ PASS. Full readability reform: all 62 modules standardized to compact table format. | ✅ Complete                            |

---

**Completion Date:** April 5, 2026
**Review Cycle:** Weekly check-ins completed; full plan review at Day 30 (Phase 1), Day 60 (Phase 2 milestone), Day 90 (Phase 2 completion), Day 30/60/90 (Phase 3 milestones per module).
