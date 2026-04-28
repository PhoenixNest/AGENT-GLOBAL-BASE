# Development Pipeline

## Overview

The company's development workflow is a ten-stage state machine. At each stage you are required to log the current execution phase and update the workflow's progress. Each stage follows a consistent schema: **Relevant Personnel**, **Artifacts In**, **Artifacts Out**, a designated **Responsible Producer**, explicit **Reviewers**, **Gate Criteria** that must be satisfied before the stage closes, and **Defect Handling** where applicable.

Each workflow must be assigned to a designated responsible party. Each assigned individual is regarded as a "Subagent"; as the primary "Agent," you must collaborate with these Subagents — leveraging their respective skill sets — to successfully complete every task within the workflow.

---

## Defect Severity System (P0–P3)

Applied in Stages 6, 7, and 8. All identified defects must be classified before any remediation begins.

| Level | Definition                              | Release Impact                  |
| ----- | --------------------------------------- | ------------------------------- |
| P0    | App crash / data loss / security breach | Blocks release — non-negotiable |
| P1    | Core feature broken / major UX failure  | Blocks release — non-negotiable |
| P2    | Minor feature degraded / cosmetic issue | User decides to fix or defer    |
| P3    | Polish / nice-to-have                   | User decides to fix or defer    |

**Authority rule:** P0/P1 classification is final and cannot be overridden. P2/P3 defects are submitted to the user, who has explicit final authority to skip or defer them.

---

## Progress Sync Protocol

Active from Stage 4 onward.

- Each completed coding task triggers an update to the progress log.
- Any task exceeding its estimated duration by **>20%** triggers an automatic CTO → CPO schedule risk notification.
- The CTO produces weekly progress summaries (status indicators, milestone percentages, risk mitigation plans) for C-suite visibility.

**Full specification:** [`monitoring.md`](monitoring.md) — Progress Monitoring & Recovery System (mandatory for Stage 4+ projects).

---

## Platform Strategy Matrix

### Overview

Stage 5 development executes per the **Platform Strategy Matrix**, which determines track activation based on the **Platform Strategy ADR** produced at Stage 3. The Stage 1 gate asks "Android, iOS, or both?" — this confirms **target platforms** (where the app ships). The **implementation approach** (how the code is structured) is an architecture decision locked at **Stage 3**.

**Five mutually exclusive scenarios — a project selects exactly one.**

### Decision Matrix

| Dimension                 | Android-Only          | iOS-Only                 | Both Native                          | KMP Cross-Platform                                  | Flutter Cross-Platform                                           |
| ------------------------- | --------------------- | ------------------------ | ------------------------------------ | --------------------------------------------------- | ---------------------------------------------------------------- |
| **Stage 1 Gate**          | Android               | iOS                      | Both                                 | Both                                                | Both                                                             |
| **Stage 3 ADR**           | N/A                   | N/A                      | "Native dual-track" ADR              | "KMP shared module" ADR                             | "Flutter single codebase" ADR                                    |
| **Stage 5 Active Tracks** | Track A only          | Track B only             | Track A + Track B                    | Track C (primary) + Tracks A/B (lightweight)        | Track C (primary) + Tracks A/B (platform channels)               |
| **Stage 5 Team Size**     | 7                     | 7                        | 13                                   | 11                                                  | 11                                                               |
| **Stage 6 Tier 1 Review** | Android Lead only     | iOS Lead only            | Android Lead ↔ iOS Lead cross-review | KMP Lead primary; Android/iOS Leads review adapters | Flutter Lead primary; Android/iOS Leads review platform channels |
| **Stage 7 Testing**       | Android only          | iOS only                 | Both platforms separately            | KMP shared (JVM) + platform adapter tests           | Flutter widget + platform channel tests                          |
| **Stage 9 i18n**          | strings.xml only      | Localizable.strings only | Both extracted separately            | KMP key-index.csv → both adapters                   | Flutter ARB → both adapters                                      |
| **Stage 10 Submission**   | Google Play only      | App Store only           | Both stores                          | Both stores                                         | Both stores                                                      |
| **CI/CD Scope**           | Android pipeline only | iOS pipeline only        | Both pipelines                       | KMP multi-target CI + platform-specific CI          | Flutter CI + platform channel CI                                 |

### Track Activation Protocol

**Note:** KMP and Flutter are mutually exclusive. Track C's technology stack and team composition change based on the Platform Strategy ADR.

| Platform Strategy      | Track A (Android) | Track B (iOS)     | Track C (Cross-Platform)        | Coordinator                           |
| ---------------------- | ----------------- | ----------------- | ------------------------------- | ------------------------------------- |
| Android-only           | **FULL** (7 eng)  | Dormant           | Dormant                         | Marcus Andersson                      |
| iOS-only               | Dormant           | **FULL** (7 eng)  | Dormant                         | Marcus Andersson                      |
| Both Native            | **FULL** (7 eng)  | **FULL** (7 eng)  | Optional (shared utilities)     | Marcus Andersson                      |
| KMP Cross-Platform     | **LIGHT** (2 eng) | **LIGHT** (2 eng) | **PRIMARY** — KMP shared module | Marcus Andersson + Mei-Ling Johansson |
| Flutter Cross-Platform | **LIGHT** (2 eng) | **LIGHT** (2 eng) | **PRIMARY** — Flutter codebase  | Marcus Andersson + Mei-Ling Johansson |

**Track semantics:**

| Term        | Definition                                                                                                         |
| ----------- | ------------------------------------------------------------------------------------------------------------------ |
| **FULL**    | End-to-end feature implementation, testing, and delivery for that platform.                                        |
| **LIGHT**   | Platform-specific integration only (UI glue, platform APIs, native dependencies). NOT feature implementation.      |
| **PRIMARY** | Owns the shared codebase that produces binaries for multiple platforms.                                            |
| **Dormant** | Track lead and engineers are reassigned to technical debt, test automation, cross-training, or SDK migration prep. |

### KMP/Flutter — How Track A/B Semantics Change

When the user chooses KMP or Flutter, Tracks A and B do **not** disappear — they shift from "feature implementation" to "platform integration."

| Aspect         | Native (FULL)            | KMP Integration (LIGHT)                      | Flutter Integration (LIGHT)                   |
| -------------- | ------------------------ | -------------------------------------------- | --------------------------------------------- |
| Code ownership | 100% of platform code    | Thin native adapters only                    | Platform channel handlers only                |
| Feature work   | Full implementation      | Integration of shared module                 | Integration of Flutter engine                 |
| Team size      | 7 engineers              | 2 engineers                                  | 2 engineers                                   |
| Freed capacity | N/A                      | 5 engineers reassigned                       | 5 engineers reassigned                        |
| CI/CD          | Full platform pipeline   | Adapter build + shared module integration    | Platform channel build + Flutter build        |
| Testing        | Full platform test suite | Adapter tests + shared module contract tests | Platform channel tests + Flutter widget tests |

### Resource Reallocation Protocol

| Scenario               | Freed Resources                                   | Reassignment Options                                              |
| ---------------------- | ------------------------------------------------- | ----------------------------------------------------------------- |
| Android-only           | iOS Lead + 6 eng, Cross-Platform Lead + 2 eng     | Other projects, internal tooling, CI/CD, test automation          |
| iOS-only               | Android Lead + 6 eng, Cross-Platform Lead + 2 eng | Same as above                                                     |
| KMP Cross-Platform     | 5 Android eng, 5 iOS eng (from FULL teams)        | Other projects, platform-specific test suites, SDK migration prep |
| Flutter Cross-Platform | 5 Android eng, 5 iOS eng                          | Same as above                                                     |

### Monitoring Adaptation

`PROGRESS.md` must reflect active tracks only. Inactive tracks show "N/A," not "0%". The Progress Sync Protocol must account for reallocated resources — reassigned engineers should not penalize a project's capacity metrics.

### Per-Scenario CI/CD Blueprint

| CI/CD Component        | Android-Only | iOS-Only | Both Native | KMP                      | Flutter            |
| ---------------------- | ------------ | -------- | ----------- | ------------------------ | ------------------ |
| Gradle build           | ✅           | ❌       | ✅          | ✅ (Android target)      | ❌                 |
| Xcode build            | ❌           | ✅       | ✅          | ✅ (iOS target)          | ❌                 |
| Detekt                 | ✅           | ❌       | ✅          | ✅ (shared + Android)    | ❌                 |
| SwiftLint              | ❌           | ✅       | ✅          | ❌                       |                    |
| KMP multi-target       | ❌           | ❌       | ❌          | ✅ (JVM + Android + iOS) | ❌                 |
| Flutter build          | ❌           | ❌       | ❌          | ❌                       | ✅ (Android + iOS) |
| Platform channel tests | ❌           | ❌       | ❌          | ❌                       | ✅                 |
| Firebase Test Lab      | ✅           | ❌       | ✅          | ✅ (Android adapter)     | ❌                 |
| Xcode UI tests         | ❌           | ✅       | ✅          | ✅ (iOS adapter)         | ❌                 |

### Platform Strategy ADR Requirements

The mandatory Platform Strategy ADR at Stage 3 must include:

1. **Decision statement** — Which approach: native dual-track, KMP, or Flutter? KMP and Flutter are mutually exclusive — select exactly one.
2. **Rationale** — Why this approach? (team skills, time-to-market, code sharing targets, performance)
3. **Trade-offs** — What is gained and sacrificed vs. alternatives?
4. **Team capability assessment** — Do we have the right people?
5. **Risk analysis** — What could go wrong? (KMP iOS target maturity, Flutter package ecosystem, native API limits)
6. **TCO projection (24-month)** — Engineering headcount, SDK update cost, platform-specific feature cost, total estimated cost.
7. **Vendor lock-in risk matrix** — Framework abandonment risk, migration cost if switching to native, open-source dependency risk, exit strategy.
8. **Performance SLA alignment** — Cold start, frame rate, memory, network payload — can the chosen approach meet PRD thresholds?
9. **Store & compliance implications** — App Store Review Guidelines compatibility, Google Play Developer Policy compatibility, in-app purchase requirements, background execution permissions.
10. **STRIDE-based threat model** — Authored by Security Architect, reviewed by CSO. Platform-specific attack surface notes (KMP C interop, Flutter Dart VM, native dual-implementation).
11. **Track activation mapping** — Explicit reference to which tracks are FULL, LIGHT, or dormant per track.
12. **Reassignment plan** — If tracks are dormant or light, where do freed engineers go?
13. **Contract versioning (KMP/Flutter only)** — Shared module API contract versioning scheme and notification mechanism.

**Ownership:** CTO authors the ADR. All three platform leads provide input. CIO reviews for technology conformance. CSO reviews for security conformance. Once approved at Stage 3 gate, this decision is **locked** — switching between strategies requires a full stage rollback (Stage 3 re-entry, ADR re-authorship, Implementation Plan re-baseline).

---

## Stage 1: Requirements Conceptualization → PRD + SRD

> **Relevant Personnel:** User, CPO, CIO, CTO, CSO
> **Artifacts In:** User's raw product requirements + target platform(s) (Android / iOS)
> **Artifacts Out:** Final PRD + Security Requirements Document (SRD)

**Responsible Producers:** CPO → PRD | CSO → SRD

Once a user submits product requirements, you must first inquire about their intended release platforms (Android, iOS, or both). Upon receiving the user's response, forward the requirements to the Chief Product Officer (CPO). The CPO leverages their professional expertise to process and coordinate these requirements, ultimately producing a Product Requirements Document (PRD).

Concurrently, the Chief Security Officer (CSO) produces the Security Requirements Document (SRD), identifying: privacy obligations, data handling constraints, authentication requirements, encryption mandates, and platform-specific security requirements (iOS App Transport Security, Android SafetyNet, GDPR/CCPA compliance).

Once the initial drafts of both documents are complete, the CPO and CSO must convene the CIO and CTO to review both documents and provide feedback. Feedback is communicated to the user, who determines whether revisions are required.

If the user confirms revisions are needed, the CPO and CSO repeat the process, re-engaging the CIO and CTO to review the updated documents. Once the user confirms no further revisions are needed, the CPO produces a final optimised PRD and the CSO finalises the SRD. Both documents are archived as a paired artifact and travel together through all subsequent stages.

**Gate Criteria:**

- [ ] User has confirmed target platform(s).
- [ ] User has confirmed no further revisions are required.
- [ ] PRD and SRD archived as a paired artifact.

---

## Stage 2: PRD → Web Prototype + Interaction Design Specification

> **Relevant Personnel:** User, CPO, CIO, CTO, CDO, Brand Design Department
> **Artifacts In:** Final PRD, SRD
> **Artifacts Out:** Approved web prototype (single HTML file) + Interaction Design Specification (IDS)

**Responsible Producer:** CDO

Upon receiving the final PRD and SRD from the CPO, the Chief Design Officer (CDO) analyses the requirements and produces blueprints and interaction design documentation. The CDO mobilises the Brand Design team to generate high-quality web prototypes for user style selection.

Once the user confirms the overall design style, the CDO convenes a review session with the CPO, CIO, and CTO to audit the prototypes against the PRD and SRD. If the prototypes fail to fully cover requirements, the CDO returns them to the Brand Design team for revision. This loop repeats until all four approve.

The approved prototypes are presented to the user for final confirmation. Upon confirmation, the CDO produces a separate **Interaction Design Specification (IDS)** covering: component trees, gesture vocabularies, state diagrams, edge case matrices, and platform-specific interaction patterns (iOS HIG, Android Material Design). The IDS clarifies that the web prototype validates functional requirements and design style; native mobile interaction behaviour is governed exclusively by the IDS.

The web prototype (HTML file) and IDS are archived together.

**Gate Criteria:**

- [ ] CPO, CIO, CTO, and CDO have all approved the prototype.
- [ ] User has given final confirmation.
- [ ] IDS produced and archived alongside the HTML prototype.

---

## Stage 3: Web Prototype → UML Engineering Package

> **Relevant Personnel:** User, CTO, CIO, R&D Department
> **Artifacts In:** Final PRD, SRD, Web Prototype, IDS
> **Artifacts Out:** UML Engineering Package (diagrams + documentation) + Architecture Decision Records (ADRs) + Technology Selection Document (TSD)

**Responsible Producers:** CTO → UML Package | CIO → ADRs + TSD

Upon receipt of the approved prototype and IDS, the CTO coordinates with the CIO and R&D Department to select appropriate technologies, conduct UML modelling, and produce corresponding diagrams (class, sequence, component) and documentation — referencing the PRD, SRD, Web Prototype, and IDS throughout.

Concurrently, the CIO produces the Architecture Decision Records (ADRs) and Technology Selection Document (TSD): comparative technology analysis, TCO assessments, vendor lock-in evaluation, migration risk matrices, and explicit technology recommendations with success/failure criteria.

**Mandatory ADRs at Stage 3:**

- **Platform Strategy ADR** — Documents the implementation approach (native dual-track, KMP cross-platform, or Flutter cross-platform). KMP and Flutter are mutually exclusive — exactly one must be selected if cross-platform is chosen. The ADR must include: decision statement, rationale, trade-offs, TCO (24-month projection), vendor lock-in risk matrix, performance SLA alignment, store/compliance implications, team capability assessment, STRIDE-based threat model (authored by Security Architect, reviewed by CSO), track activation mapping (FULL/LIGHT/PRIMARY/Dormant per track), and reassignment plan for dormant tracks.
- **String Key Taxonomy ADR** — Documents the naming convention for all localised strings (e.g., `{feature}.{screen}.{component}.{property}`). This is a technology decision that locks at Stage 3 alongside the Platform Strategy ADR.
- **Security Architecture ADRs** — Crypto standards, secure storage mechanisms, certificate pinning strategy, and platform-specific security patterns (iOS Keychain, Android Keystore).

**Technology decisions are locked upon Stage 3 gate approval.** ADRs and the TSD are not revisable during Stage 4 (Implementation Planning) or Stage 5 (Development). Any deviation requires a new ADR, which constitutes a Stage 3 re-entry.

The CTO and CIO jointly review all deliverables to ensure the proposed solution is implementable on time and within requirements, and that no technical constraints render current requirements impossible. The full UML Engineering Package (UML docs + ADRs + TSD) is submitted to the user. Upon user approval, all artifacts are archived.

**Gate Criteria:**

- [ ] CTO and CIO have both approved all deliverables.
- [ ] Solution confirmed technically feasible within current requirements.
- [ ] User has approved the UML Engineering Package.
- [ ] UML Package, ADRs, and TSD archived.

---

## Stage 4: All Deliverables → Coding Implementation Plan

> **Relevant Personnel:** User, CTO, R&D Department
> **Artifacts In:** All archived deliverables (PRD, SRD, Web Prototype, IDS, UML Package, ADRs, TSD)
> **Artifacts Out:** Coding Implementation Plan + Gantt Chart

**Responsible Producer:** CTO

The CTO integrates all archived deliverables to produce a Coding Implementation Plan using SPEC techniques and appropriate development methodologies. ADRs and TSD from Stage 3 serve as reference inputs — technology decisions are locked; the plan executes against them.

The plan includes:

- **Track Activation Mapping** — Explicit reference to the Platform Strategy ADR and activation of the corresponding track configuration (FULL/LIGHT/PRIMARY/Dormant per track). Personnel assignments must reflect the active tracks.
- **Technology Decision Registry** — A table listing every ADR and TSD decision from Stage 3, with a compliance checkbox that the CTO must sign. Any deviation requires a new ADR (Stage 3 re-entry).
- **Phased task decomposition** with explicit personnel assignments (e.g., UI/UX coding vs. logic coding).
- **Dependency mapping** including cross-track dependencies organized by layer: data layer → domain layer → presentation layer → platform adapter layer.
- **Gantt chart** for progress tracking with explicit milestones.
- **Progress Sync Protocol** documentation.
- **`key-index.csv` creation** scheduled as a Stage 5 task, operationalizing the String Key Taxonomy ADR from Stage 3.
- **Requirements Traceability Matrix (RTM)** — A mapping of every PRD requirement (REQ-NNN) and SRD requirement (SEC-NNN) to IDS sections, UML elements, implementation tasks, and test cases. 100% RTM coverage is required before Stage 5 begins.
- **SIS completion reference** — Security Implementation Specification must be completed and CSO-signed before Stage 5 Day 1. Listed as a gate item in the CI/CD Readiness section.

The CTO reviews the plan against all archived artifacts to verify accuracy and reasonable task assignment. The plan is submitted to the user for approval and archived upon confirmation.

**Gate Criteria:**

- [ ] Plan covers all requirements in PRD, SRD, IDS, and UML Package.
- [ ] Gantt chart included with explicit milestones.
- [ ] Personnel assignments explicit for all tasks.
- [ ] Progress Sync Protocol documented.
- [ ] Requirements Traceability Matrix (RTM) created with 100% coverage.
- [ ] SIS completed and CSO-signed referenced in CI/CD Readiness section.
- [ ] Technology Decision Registry shows 100% ADR/TSD compliance (any deviation triggers Stage 3 re-entry).
- [ ] User has approved the plan.
- [ ] Plan and Gantt chart archived.

---

## Stage 5: Coding Implementation Plan → Software Development

> **Relevant Personnel:** CTO, R&D Department
> **Artifacts In:** Coding Implementation Plan, Gantt Chart, all prior archived deliverables
> **Artifacts Out:** Development codebase

**Responsible Producer:** CTO

This is the core implementation phase. The CTO oversees and tracks development progress against the Gantt chart, with **VP Mobile (Marcus Andersson) coordinating across all active platform tracks**.

**Track execution:**

- **Track A (Android):** Led by Android Chapter Lead (Kofi Asante-Mensah). Executes per Platform Strategy ADR — FULL for native Android, LIGHT for KMP/Flutter integration.
- **Track B (iOS):** Led by iOS Chapter Lead (Seo-Yeon Park). Executes per Platform Strategy ADR — FULL for native iOS, LIGHT for KMP/Flutter integration.
- **Track C (Cross-Platform):** Led by Cross-Platform Chapter Lead (Mei-Ling Johansson). PRIMARY for KMP/Flutter projects. Co-coordinates with VP Mobile for cross-platform projects.

**Shared module coordination:** For KMP/Flutter projects, the shared module's public API contract must be defined before platform integration tracks begin implementation. Contract verification occurs at 30% and 70% completion milestones.

**Security Implementation Specification (SIS):** Before development begins, the security team (Security Architect + Lead Security Engineer) produces a platform-specific SIS for each active track, translating SRD requirements into concrete, platform-specific code patterns. Signed off by CSO.

**Design Fidelity Checkpoint (~60% completion):** At approximately 60% completion of the Coding Implementation Plan, the CDO conducts a formal Design Fidelity Checkpoint against the IDS. Platform Leads present working builds for side-by-side comparison with IDS specifications (component trees, gesture vocabularies, state diagrams, edge case UIs, accessibility baseline, animation specs, design tokens). Remediation thresholds: ≥ 90% pass rate → proceed with documented failures; 70–89% → proceed with remediation plan and CDO re-check at 80%; < 70% → STOP, remediation required, CTO notifies CPO. Results recorded in `DEVELOPMENT-LOG.md`.

**String Extraction Readiness Check (CTO internal review):** Before advancing to Stage 6, the Internationalization Specialist runs a preliminary scan of the completed codebase to identify hardcoded strings that were not extracted into resource files. Any remaining hardcoded strings are classified as P2 defects (P1 if they affect core user flows). This is not full extraction — it is an audit to ensure Stage 9 extraction does not become a refactoring exercise under release pressure.

**Progress Sync Protocol:** Any task exceeding its estimated duration by >20% triggers an automatic CTO → CPO schedule risk notification. Per-platform variance is tracked — if one platform is >20% behind others, the alert fires regardless of overall average.

**Contract verification (KMP/Flutter only):** For KMP/Flutter projects, the Contract Verification Report is produced at 30% and 70% completion milestones. The Cross-Platform Lead verifies that the shared module's public API contract correctly serves both platform consumers. Blocking issues must be resolved before the next checkpoint.

Upon completion of each coding task, the progress log is updated. Once all coding tasks are complete, the CTO conducts a comprehensive internal review to ensure the project compiles, runs successfully, and is free of known compilation or runtime bugs before advancing to Code Review.

**Gate Criteria:**

- [ ] All tasks in the Coding Implementation Plan marked complete.
- [ ] CTO internal review passed (no known compilation or runtime bugs).
- [ ] Design Fidelity Checkpoint completed (≥ 90% conformance, or remediation plan attached).
- [ ] String Extraction Readiness Check completed (hardcoded strings classified as defects, none blocking).
- [ ] Contract Verification Reports produced at 30% and 70% milestones (KMP/Flutter only).
- [ ] Progress log current and archived.

---

## Stage 6: Development Deliverables → Code Review

> **Relevant Personnel:** CPO, CDO, CTO, CIO, CSO, R&D Department, User
> **Artifacts In:** Development codebase, PRD, SRD, IDS, UML Package, ADRs, TSD
> **Artifacts Out:** Defect Report (if any) + Code Review Sign-off

**Responsible Producer:** CTO (convenes review panel)

The code review follows a **two-tier process**:

**Tier 1 — Technical Review (Platform Leads):** Platform Leads cross-review each other's code. The Android Lead reviews iOS code and vice versa. For KMP/Flutter projects, the Cross-Platform Lead reviews the shared module while Android/iOS Leads review native adapters or platform channels. Tier 1 produces a **written cross-review memo** that becomes part of the Defect Report. Automated quality gates (SAST, unit tests, linting) must pass before Tier 1 begins.

**ADR/TSD Compliance Enforcement (Three-Layer Defense):**

1. **Platform Lead Attestation** — Each Platform Lead certifies in their cross-review memo that the codebase matches Stage 3 ADRs/TSD. Any deviation is flagged as P1.
2. **Architecture Compliance Audit** — Senior Architect (Dr. Elena Rostova) conducts an independent audit of the codebase against all Stage 3 ADRs. Audit findings are included in the Defect Report.
3. **CI/CD Gates** — Automated checks enforce dependency version pinning (TSD-approved versions match build files), prohibited technology detection (e.g., disallowed crypto libraries), and security ADR compliance (SAST rules derived from Security Architecture ADRs).

**Tier 2 — Strategic Review (C-Suite Panel):** CPO, CDO, CTO, CIO, and CSO review the codebase against four criteria:

1. All requirements and specifications in the PRD have been fully implemented.
2. All design requirements in the IDS and web prototypes have been accurately reproduced.
3. All requirements in the UML Engineering Package (diagrams, ADRs, TSD) have been fully implemented as prescribed. **All technology choices in the codebase match Stage 3 ADRs/TSD. Any deviation is a P1 defect.**
4. _(CSO-owned)_ All security requirements in the SRD have been implemented: encryption, secure storage, platform security standards (iOS Keychain / Android Keystore), and OWASP MASVS compliance.

All identified defects are documented with their P0–P3 classification and a precise description of the gap. The Defect Report is submitted to the user. The user reviews: P0/P1 defects are non-negotiable fixes; the user has final authority to skip or defer P2/P3 defects. The CTO assigns specific R&D personnel to remediate all confirmed defects. After remediation, the full review process repeats until all non-deferred defects are resolved and all panel members sign off.

**Live Demonstration:** Before panel sign-off, the CDO conducts a live demo of the running builds on both platforms, interacting with the app as an end user would. Any design or interaction defects discovered during the demo are classified as P0–P3 defects and added to the Defect Report.

**Gate Criteria:**

- [ ] All P0 and P1 defects resolved.
- [ ] User has reviewed the Defect Report and made explicit decisions on all P2/P3 defects.
- [ ] CPO, CDO, CTO, CIO, and CSO have all signed off.
- [ ] Code Review Sign-off archived.

---

## Stage 7: Code Review → Automated Testing

> **Relevant Personnel:** CTO, R&D Department
> **Artifacts In:** Code Review sign-off codebase
> **Artifacts Out:** Automated Test Suite + Test Results Report

**Responsible Producer:** CTO

The CTO designates R&D personnel to develop test cases and execute automated tests targeting a 100% pass rate. Any bugs identified are consolidated into a Bug Report and handed to developers for remediation. After fixes, testers perform regression testing on all affected functionalities. Regression must pass fully before advancing.

**Platform-specific testing mandates:**

- **Android:** Espresso instrumented tests, Play Pre-Launch Report (minimum device profiles per Platform Strategy).
- **iOS:** XCTest UI tests on current + previous iOS version.
- **KMP Cross-Platform:** Shared module unit tests (100% coverage) + platform adapter contract tests for both Android and iOS targets.
- **Flutter Cross-Platform:** Flutter widget tests + platform channel tests for every Flutter→Native bridge.
- **Integration:** At least one E2E flow per platform (login → core feature → logout).
- **Accessibility:** Automated WCAG 2.1 AA checks on every PR (axe-core, Espresso accessibility assertions, XCTest accessibility checks). Accessibility defects classified per impact: critical = P0, serious = P1, moderate = P2, minor = P3.
- **DAST (Dynamic Application Security Testing):** OWASP ZAP (or equivalent) active + passive scan against all API endpoints reachable from the mobile app. Zero "High" risk findings (P1); all "Medium" findings resolved or user-deferred (P2).
- **Penetration Testing:** Manual penetration test by Security Engineer (Sana Khoury) covering OWASP Mobile Top 10 + MASVS assessment categories (AUTH, STORAGE, CRYPTO, NETWORK, PLATFORM, RESILIENCE). Zero Critical findings (P0); zero High findings unresolved (P1).
- **Performance Benchmarks:** All PRD performance thresholds verified (cold start, warm start, frame rate, memory usage, network payload). 100% pass rate required; any failed metric exceeding threshold by >20% is a P1 defect.

**Regression testing model:**

| Trigger       | Scope                                                   | Execution                                         |
| ------------- | ------------------------------------------------------- | ------------------------------------------------- |
| PR opened     | Affected modules + 2 levels of dependency (unit tests)  | CI — blocks merge                                 |
| Merge to main | Full unit + integration suite                           | CI — blocks deployment                            |
| Nightly       | Full E2E on all device/OS combos + performance baseline | Automated — opens P1 on failure                   |
| Pre-release   | Full regression suite + exploratory testing             | Manual + automated — blocks RC promotion on P0/P1 |

Bugs discovered during automated testing are classified using the P0–P3 system. P0/P1 bugs block advancement; P2/P3 are submitted to the user for the same skip/defer authority as in Stage 6.

**Gate Criteria:**

- [ ] 100% of test cases pass (accounting for user-approved P2/P3 deferrals).
- [ ] Regression testing on all fixed functionalities passes with no failures.
- [ ] Test Results Report archived.

---

## Stage 8: Automated Testing → Integrity Verification

> **Relevant Personnel:** CPO, CDO, CTO, CIO, CSO, Brand Design Department, R&D Department, User
> **Artifacts In:** Post-testing codebase, all prior archived deliverables
> **Artifacts Out:** Integrity Verification Sign-off

**Responsible Producer:** CTO (convenes review panel)

All key personnel (CPO, CDO, CTO, CIO, CSO, Brand Design, R&D) review the post-testing codebase against the full artifact set to verify that the remediation process did not silently remove or reduce functionality to achieve passing tests — the "fixing code by trimming the product" anti-pattern.

The review confirms: all PRD features remain intact (verified against per-feature Stage 6 baseline); all CDO/IDS design specifications accurately realised (IDS Conformance Matrix re-verified ≥ 95%); all UML engineering standards upheld; all SRD security requirements remain enforced and effective (not just present — correctness verified). **Removal, disabling, or weakening of any security control specified in the SRD (encryption, certificate pinning, root/jailbreak detection, obfuscation, authentication flows) is classified as a P0 defect. Stealthy weakening — e.g., keeping certificate pinning but reducing validation strictness, keeping encryption but using a weaker cipher — is also classified as P0.** Functionality removal is never a valid remediation strategy. Analytics instrumentation integrity is verified — all PRD-defined metrics must still fire correctly after Stage 7 remediation. Any regressions are treated as P0/P1 defects. Once all personnel sign off, the Integrity Verification Sign-off is archived.

**Gate Criteria:**

- [ ] No functionality reduced or removed relative to the Stage 6 Code Review baseline.
- [ ] All panel members (CPO, CDO, CTO, CIO, CSO, Brand Design, R&D) signed off.
- [ ] Integrity Verification Sign-off archived.

---

## Stage 9: Integrity Verification → Internationalization Engineering

> **Relevant Personnel:** CTO-L (Chief Translation Officer) + Translation Team, CPO, CDO, CTO, R&D Department
> **Artifacts In:** Integrity-verified codebase, PRD (language requirements section)
> **Artifacts Out:** Localised codebase + Translation Verification Report

**Responsible Producer:** CTO-L (Chief Translation Officer)

The R&D Department scans the codebase to identify and extract all hardcoded strings, storing them in platform-appropriate resource files (e.g., `strings.xml` for Android, `Localizable.strings` for iOS) per platform guidelines and the String Key Taxonomy ADR from Stage 3. For KMP projects, the `key-index.csv` serves as the cross-platform string parity source. Any additional datasets requiring localisation (e.g., JSON content files) are identified and flagged alongside string resources.

The CTO-L and Translation Team take ownership of all extracted strings and datasets, producing translations into all user-specified languages (e.g., English, Chinese, Japanese, Korean, French) governed by the **Language Translation Module**.

The CPO, CDO, and CTO conduct a **structural completeness review**: verifying all hardcoded strings have been extracted, all resource files correctly structured, and no UI component contains untranslated text. This review covers structure only — translation accuracy is the sole responsibility of the CTO-L. The CTO-L issues a Translation Verification Report confirming accuracy across all target languages. All artifacts are archived.

**Gate Criteria:**

- [ ] Zero hardcoded strings remain in the codebase.
- [ ] All resource files and datasets updated for all target languages.
- [ ] CPO, CDO, CTO structural completeness review passed.
- [ ] CTO-L Translation Verification Report issued and archived.

---

## Stage 10: Internationalization Engineering → Release Readiness Check

> **Relevant Personnel:** CPO, CDO, CTO, CIO, CSO, CTO-L, User
> **Artifacts In:** All archived deliverables from all prior stages
> **Artifacts Out:** Release Readiness Report + Release Decision

**Responsible Producer:** CTO (convenes final panel)

A final holistic gate ensuring the product meets all release standards before shipping. Each panel member reviews their domain checklist item(s) and issues sign-off. Any open item blocks release until resolved.

**7-Item Release Checklist:**

| #   | Domain       | Criteria                                             | Sign-off Authority |
| --- | ------------ | ---------------------------------------------------- | ------------------ |
| 1   | Product      | All PRD requirements implemented and verified        | CPO                |
| 2   | Design       | All CDO/IDS specifications accurately realised       | CDO                |
| 3   | Architecture | All UML/ADR/TSD standards upheld                     | CTO + CIO          |
| 4   | Security     | All SRD requirements enforced; OWASP MASVS compliant | CSO                |
| 5   | Testing      | 100% automated test pass rate achieved               | CTO                |
| 6   | Localisation | All target languages complete and verified           | CTO-L              |
| 7   | Platform     | App Store / Google Play submission requirements met  | CTO + CPO          |

The completed Release Readiness Report is submitted to the user. The user makes the final release decision.

**Gate Criteria:**

- [ ] All seven checklist items signed off by the responsible party.
- [ ] Release Readiness Report submitted to user.
- [ ] User has issued the final release decision.
- [ ] Release Readiness Report archived.
