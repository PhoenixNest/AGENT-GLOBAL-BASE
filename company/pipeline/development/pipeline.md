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

The plan includes: phased task decomposition, explicit personnel assignments (e.g., UI/UX coding vs. logic coding), dependency mapping, and a Gantt chart for progress tracking. The Progress Sync Protocol is documented within the plan.

The CTO reviews the plan against all archived artifacts to verify accuracy and reasonable task assignment. The plan is submitted to the user for approval and archived upon confirmation.

**Gate Criteria:**

- [ ] Plan covers all requirements in PRD, SRD, IDS, and UML Package.
- [ ] Gantt chart included with explicit milestones.
- [ ] Personnel assignments explicit for all tasks.
- [ ] Progress Sync Protocol documented.
- [ ] User has approved the plan.
- [ ] Plan and Gantt chart archived.

---

## Stage 5: Coding Implementation Plan → Software Development

> **Relevant Personnel:** CTO, R&D Department
> **Artifacts In:** Coding Implementation Plan, Gantt Chart, all prior archived deliverables
> **Artifacts Out:** Development codebase

**Responsible Producer:** CTO

This is the core implementation phase. The CTO oversees and tracks development progress against the Gantt chart. Upon completion of each coding task, the progress log is updated. Any task exceeding its estimated duration by >20% is flagged to the CPO per the Progress Sync Protocol.

Once all coding tasks are complete, the CTO conducts a comprehensive internal review to ensure the project compiles, runs successfully, and is free of known compilation or runtime bugs before advancing to Code Review.

**Gate Criteria:**

- [ ] All tasks in the Coding Implementation Plan marked complete.
- [ ] CTO internal review passed (no known compilation or runtime bugs).
- [ ] Progress log current and archived.

---

## Stage 6: Development Deliverables → Code Review

> **Relevant Personnel:** CPO, CDO, CTO, CIO, CSO, R&D Department, User
> **Artifacts In:** Development codebase, PRD, SRD, IDS, UML Package, ADRs, TSD
> **Artifacts Out:** Defect Report (if any) + Code Review Sign-off

**Responsible Producer:** CTO (convenes review panel)

All key stakeholders (CPO, CDO, CTO, CIO, CSO) conduct a joint review of the codebase against four criteria:

1. All requirements and specifications in the PRD have been fully implemented.
2. All design requirements in the IDS and web prototypes have been accurately reproduced.
3. All requirements in the UML Engineering Package (diagrams, ADRs, TSD) have been fully implemented as prescribed.
4. _(CSO-owned)_ All security requirements in the SRD have been implemented: encryption, secure storage, platform security standards (iOS Keychain / Android Keystore), and OWASP MASVS compliance.

All identified defects are documented with their P0–P3 classification and a precise description of the gap. The Defect Report is submitted to the user. The user reviews: P0/P1 defects are non-negotiable fixes; the user has final authority to skip or defer P2/P3 defects. The CTO assigns specific R&D personnel to remediate all confirmed defects. After remediation, the full review process repeats until all non-deferred defects are resolved and all panel members sign off.

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

The review confirms: all PRD features remain intact; all CDO/IDS design specifications accurately realised; all UML engineering standards upheld; all SRD security requirements remain enforced. Any regressions are treated as P0/P1 defects — functionality removal is never a valid remediation strategy. Once all personnel sign off, the Integrity Verification Sign-off is archived.

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

The R&D Department scans the codebase to identify and extract all hardcoded strings, storing them in platform-appropriate resource files (e.g., `strings.xml` for Android) per platform guidelines. Any additional datasets requiring localisation (e.g., JSON content files) are identified and flagged alongside string resources.

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
