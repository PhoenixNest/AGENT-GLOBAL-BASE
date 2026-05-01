# Development Pipeline — Canonical Base

> **Status:** Phase P-1 (universal content extracted from `mobile-development/pipeline.md` as proof-of-pattern).
> **Source of extraction:** `company/pipeline/mobile-development/pipeline.md` v(legacy, 453 lines), the most-elaborated of the four legacy product pipelines.
> **Scope:** universal content. Per-product behaviour lives in the four product overlays — `mobile-development/delta.md`, `web-development/delta.md`, `backend-api/delta.md`, and `full-stack/delta.md`. Read this file alongside the relevant overlay; the overlay fills every `{{DELTA: ...}}` placeholder below.

This file is the **shared base** for every product pipeline (mobile, web, backend API, full-stack). Sections written here are authoritative across all four product types. Sections marked `{{DELTA: …}}` are filled in by each product's `delta.md` overlay (see [`delta-template.md`](./delta-template.md)).

---

## Overview

The company's development workflow is a **10-stage state machine** (post-Step-3 + Step-6 + Step-15 = a **12-stage state machine** including Stage 0 Discovery, Stage 9.5 Dogfood, and Stage 11 Live Operations). At each stage you must log the current execution phase and update the workflow's progress. Each stage follows a consistent schema: **Relevant Personnel**, **Artifacts In**, **Artifacts Out**, a designated **Responsible Producer**, explicit **Reviewers**, **Gate Criteria**, and **Defect Handling** where applicable.

Each workflow must be assigned to a designated responsible party. Each assigned individual is regarded as a "Subagent"; as the primary "Agent," you must collaborate with these Subagents — leveraging their respective skill sets — to successfully complete every task within the workflow.

---

## Defect Severity System (P0–P3) — UNIVERSAL

Applied in Stages 6, 7, and 8. All identified defects must be classified before any remediation begins.

| Level | Definition                              | Release Impact                  |
| ----- | --------------------------------------- | ------------------------------- |
| P0    | App crash / data loss / security breach | Blocks release — non-negotiable |
| P1    | Core feature broken / major UX failure  | Blocks release — non-negotiable |
| P2    | Minor feature degraded / cosmetic issue | User decides to fix or defer    |
| P3    | Polish / nice-to-have                   | User decides to fix or defer    |

**Authority rule:** P0/P1 classification is final and cannot be overridden. P2/P3 defects are submitted to the user, who has explicit final authority to skip or defer them.

---

## Progress Sync Protocol — UNIVERSAL

Active from Stage 4 onward.

- Each completed coding task triggers an update to the progress log.
- Any task exceeding its estimated duration by **>20%** triggers an automatic CTO → CPO schedule risk notification.
- The CTO produces weekly progress summaries (status indicators, milestone percentages, risk mitigation plans) for C-suite visibility.

**Full specification:** see the per-product `monitoring.md` (e.g., [`company/pipeline/mobile-development/monitoring.md`](company/pipeline/mobile-development/monitoring.md)) — Progress Monitoring & Recovery System (mandatory for Stage 4+ projects).

---

## Platform / Architecture Strategy Matrix — DELTA

The strategy matrix is **product-specific** in form (mobile selects among 5 platform scenarios; web selects among rendering strategies; backend selects among API protocols; full-stack composes web + mobile + backend) but **universal in role**: it is always produced at Stage 1 (the user-facing scope question), locked at Stage 3 via the **Platform Strategy ADR** (or its product equivalent), and references how Stage 5 tracks activate.

`{{DELTA: Each product pipeline defines its own strategy matrix, decision matrix, and track activation protocol here.}}`

- **mobile-development/delta.md** — 5-scenario Platform Strategy Matrix (Android-only / iOS-only / Both Native / KMP / Flutter), Track A/B/C activation, KMP/Flutter track-semantic shifts, per-scenario CI/CD blueprint.
- **web-development/delta.md** — Web rendering strategy (SPA / SSR / SSG / hybrid), browser/device matrix, CI build matrix.
- **backend-api/delta.md** — API protocol strategy (REST / GraphQL / gRPC / event-streaming), service decomposition plan, contract testing matrix.
- **full-stack/delta.md** — Composition strategy (web + mobile + backend coordination), shared-contract governance, monorepo vs. polyrepo decision.

**Universal ADR Requirement:** The product-specific Strategy ADR is **versionable + supersedable**. Supersession requires a documented rollback plan and is not a free action — it triggers an Implementation-Plan re-baseline (Stage 4 re-entry minimum). See [`adr-template.md`](./adr-template.md) for the canonical ADR shape.

---

## Stage 0 — Problem Validation (NEW — Step 3) — UNIVERSAL FRAME

> **Relevant Personnel:** User (sponsor), CPO (DRI), VP-of-product-area
> **Artifacts In:** Raw problem statement / opportunity hypothesis
> **Artifacts Out:** Problem Validation Memo (1-page maximum) + Discovery Findings + Kill Criteria

**Responsible Producer:** CPO (mobile, web, full-stack) | VP API (backend-only initiatives)

The Problem Validation Memo establishes that the problem is real, valued, and worth solving _before_ PRD authoring begins. It contains:

1. **Customer-discovery evidence:** n ≥ 5 user interviews, observation notes, or analyst data.
2. **Quantitative demand signal:** funnel data, search volume, support-ticket clusters, or competitor adoption rate — at minimum one quantified signal.
3. **Explicit kill criteria:** the conditions under which Stage 1 will NOT be entered (e.g., "if interview-validation rate falls below 60%, terminate").
4. **Scope of validation:** what was NOT tested and remains assumed.

**Universal gate criteria:**

- [ ] Customer-discovery evidence (n ≥ 5) attached.
- [ ] At least one quantitative demand signal documented.
- [ ] Kill criteria explicit and testable.
- [ ] CPO sign-off recorded.

`{{DELTA: any product-specific Stage 0 evidence requirements (e.g., backend pipelines may require an existing-API usage signal in addition to interviews).}}`

---

## Stage 1 — Requirements Conceptualization → PRD + SRD

> **Relevant Personnel:** User, CPO (or relevant VP per product), CIO, CTO, CSO
> **Artifacts In:** Problem Validation Memo (Stage 0 output) + User's raw product requirements + `{{DELTA: target platforms / surface}}`
> **Artifacts Out:** Final PRD + Security Requirements Document (SRD)

**Responsible Producers:** `{{DELTA: PRD authorship by CPO (mobile), VP Web (web), VP API (backend), or joint VP Web + VP API (full-stack)}}` | CSO → SRD

Once a user submits product requirements, you must first inquire about their intended `{{DELTA: target surface — release platforms for mobile (Android / iOS / both); rendering target for web (SPA / SSR / SSG); API protocol for backend; composition scope for full-stack}}`. Upon receiving the user's response, forward the requirements to the PRD steward (CPO or product-specific VP).

The PRD steward leverages their professional expertise to process and coordinate these requirements, ultimately producing a Product Requirements Document (PRD).

Concurrently, the Chief Security Officer (CSO) produces the Security Requirements Document (SRD), identifying: privacy obligations, data handling constraints, authentication requirements, encryption mandates, and `{{DELTA: platform-specific security requirements (mobile: iOS App Transport Security, Android SafetyNet; web: CSP, CORS, CSRF; backend: rate limiting, auth scopes; full-stack: cross-surface CSRF + CORS)}}`. GDPR/CCPA compliance is universal across all product types.

Once the initial drafts of both documents are complete, the PRD steward and CSO must convene the CIO and CTO to review both documents and provide feedback. Feedback is communicated to the user, who determines whether revisions are required. If the user confirms revisions are needed, the loop repeats. Once the user confirms no further revisions are needed, the PRD and SRD are finalized and archived as a paired artifact and travel together through all subsequent stages.

**Universal gate criteria:**

- [ ] User has confirmed `{{DELTA: target platforms / surface}}`.
- [ ] User has confirmed no further revisions are required.
- [ ] PRD and SRD archived as a paired artifact.

`{{DELTA: any additional Stage 1 gate criteria specific to this product type.}}`

---

## Stage 2 — PRD → Web Prototype + Interaction Design Specification

> **Relevant Personnel:** User, CPO/VP, CIO, CTO, CDO, Brand Design Department
> **Artifacts In:** Final PRD, SRD
> **Artifacts Out:** `{{DELTA: Approved web prototype (single HTML file) for mobile/web/full-stack; Approved API contract (OpenAPI/GraphQL schema) for backend}}` + Interaction Design Specification (IDS)

**Responsible Producer:** CDO

Upon receiving the final PRD and SRD, the Chief Design Officer (CDO) analyses the requirements and produces blueprints and interaction design documentation. The CDO mobilises the Brand Design team to generate `{{DELTA: high-quality prototypes — HTML for mobile/web/full-stack, contract specs for backend}}` for user style selection.

Once the user confirms the overall design style, the CDO convenes a review session with the CPO/VP, CIO, and CTO to audit the prototypes against the PRD and SRD. If the prototypes fail to fully cover requirements, the CDO returns them to the Brand Design team for revision. This loop repeats until all four approve.

The approved prototypes are presented to the user for final confirmation. Upon confirmation, the CDO produces a separate **Interaction Design Specification (IDS)** covering: component trees, gesture vocabularies, state diagrams, edge case matrices, and `{{DELTA: platform-specific interaction patterns (mobile: iOS HIG + Android Material Design; web: WCAG 2.1 AA mobile-first; backend: API contract semantics; full-stack: cross-surface state coherence)}}`. The IDS clarifies that the prototype validates functional requirements and design style; native interaction behaviour is governed exclusively by the IDS.

The prototype and IDS are archived together.

**Cross-cutting i18n at Stage 2:** Pseudo-localization in prototype; RTL/LTR validation in IDS. See `{{DELTA: cross-cutting i18n requirements per product}}`.

**Universal gate criteria:**

- [ ] CPO/VP, CIO, CTO, and CDO have all approved the prototype.
- [ ] User has given final confirmation.
- [ ] IDS produced and archived alongside the prototype.

---

## Stage 3 — Prototype → UML Engineering Package

> **Relevant Personnel:** User, CTO, CIO, R&D Department
> **Artifacts In:** Final PRD, SRD, Prototype, IDS
> **Artifacts Out:** UML Engineering Package (diagrams + documentation) + Architecture Decision Records (ADRs) + Technology Selection Document (TSD)

**Responsible Producers:** CTO → UML Package | CIO → ADRs + TSD

Upon receipt of the approved prototype and IDS, the CTO coordinates with the CIO and R&D Department to select appropriate technologies, conduct UML modelling, and produce corresponding diagrams (class, sequence, component) and documentation — referencing the PRD, SRD, Prototype, and IDS throughout.

Concurrently, the CIO produces the Architecture Decision Records (ADRs) and Technology Selection Document (TSD): comparative technology analysis, TCO assessments, vendor lock-in evaluation, migration risk matrices, and explicit technology recommendations with success/failure criteria.

**Mandatory ADRs (universal):**

- **String Key Taxonomy ADR** — locks the naming convention for all localised strings (e.g., `{feature}.{screen}.{component}.{property}`). This is a technology decision that locks at Stage 3.
- **Security Architecture ADRs** — crypto standards, secure storage mechanisms, certificate pinning strategy, and `{{DELTA: platform-specific security patterns (mobile: iOS Keychain + Android Keystore; web: localStorage/IndexedDB hardening + CSP; backend: secrets vaulting + KMS; full-stack: cross-surface session governance)}}`.

`{{DELTA: pipeline-specific mandatory ADRs — e.g., Platform Strategy ADR (mobile), Web Rendering ADR (web), API Protocol ADR (backend), Composition ADR (full-stack).}}`

**Decision lock rule (universal):** ADRs and the TSD are **versionable + supersedable**. Supersession requires a documented rollback plan per [`adr-template.md`](./adr-template.md).

The CTO and CIO jointly review all deliverables to ensure the proposed solution is implementable on time and within requirements, and that no technical constraints render current requirements impossible. The full UML Engineering Package (UML docs + ADRs + TSD) is submitted to the user. Upon user approval, all artifacts are archived.

**Universal gate criteria:**

- [ ] CTO and CIO have both approved all deliverables.
- [ ] Solution confirmed technically feasible within current requirements.
- [ ] User has approved the UML Engineering Package.
- [ ] UML Package, ADRs, and TSD archived.

---

## Stage 4 — All Deliverables → Coding Implementation Plan

> **Relevant Personnel:** User, CTO, R&D Department
> **Artifacts In:** All archived deliverables (PRD, SRD, Prototype, IDS, UML Package, ADRs, TSD)
> **Artifacts Out:** Coding Implementation Plan + Gantt Chart

**Responsible Producer:** CTO

The CTO integrates all archived deliverables to produce a Coding Implementation Plan using SPEC techniques and appropriate development methodologies. ADRs and TSD from Stage 3 serve as reference inputs — technology decisions are supersedable only with a documented rollback plan per [`adr-template.md`](./adr-template.md); the plan executes against them.

The plan includes (universal):

- **Technology Decision Registry** — A table listing every ADR and TSD decision from Stage 3, with a compliance checkbox that the CTO must sign. Any deviation requires a new ADR (Stage 3 re-entry, or supersession per Step 14).
- **Phased task decomposition** with explicit personnel assignments.
- **Dependency mapping** organized by layer: data layer → domain layer → presentation layer → `{{DELTA: platform/surface adapter layer (mobile: native adapters; web: client/SSR boundary; backend: external-service adapter; full-stack: cross-surface contract layer)}}`.
- **Gantt chart** for progress tracking with explicit milestones.
- **Progress Sync Protocol** documentation.
- **`key-index.csv` creation** scheduled as a Stage 5 task, operationalizing the String Key Taxonomy ADR from Stage 3.
- **Requirements Traceability Matrix (RTM)** — A mapping of every PRD requirement (REQ-NNN) and SRD requirement (SEC-NNN) to IDS sections, UML elements, implementation tasks, and test cases. **100% RTM coverage is required before Stage 5 begins.**
- **SIS completion reference** — Security Implementation Specification must be completed and CSO-signed before Stage 5 Day 1. Listed as a gate item in the CI/CD Readiness section.
- **Technical-debt allocation rule:** every Stage 5 sprint reserves ≥ 20% capacity for technical debt; the plan declares this allocation explicitly.

`{{DELTA: pipeline-specific Stage 4 plan sections — Track Activation Mapping (mobile), Service Decomposition Plan (backend), Composition Plan (full-stack), Rendering Strategy Plan (web).}}`

**Universal gate criteria:**

- [ ] Plan covers all requirements in PRD, SRD, IDS, and UML Package.
- [ ] Gantt chart included with explicit milestones.
- [ ] Personnel assignments explicit for all tasks.
- [ ] Progress Sync Protocol documented.
- [ ] RTM created with 100% coverage.
- [ ] SIS completed and CSO-signed referenced in CI/CD Readiness section.
- [ ] Technology Decision Registry shows 100% ADR/TSD compliance.
- [ ] Technical-debt allocation rule (≥ 20%) declared.
- [ ] User has approved the plan.
- [ ] Plan and Gantt chart archived.

---

## Stage 5 — Coding Implementation Plan → Software Development

> **Relevant Personnel:** CTO, R&D Department
> **Artifacts In:** Coding Implementation Plan, Gantt Chart, all prior archived deliverables
> **Artifacts Out:** Development codebase

**Responsible Producer:** CTO

This is the core implementation phase. The CTO oversees and tracks development progress against the Gantt chart, with `{{DELTA: pipeline-specific lead coordinator (mobile: VP Mobile coordinates Track A/B/C; web: Frontend Lead; backend: Backend Lead per service decomposition; full-stack: VP Mobile + Frontend Lead + Backend Lead jointly)}}`.

`{{DELTA: pipeline-specific Stage 5 details — track execution model (mobile: Track A/B/C activation), shared module coordination (KMP/Flutter mobile + full-stack contract layer), SIS scope per platform/surface, design fidelity checkpoint scope.}}`

**Universal mandates:**

- **Security Implementation Specification (SIS):** Before development begins, the security team (Security Architect + Lead Security Engineer) produces a per-track / per-surface SIS translating SRD requirements into concrete code patterns. Signed off by CSO.
- **Design Fidelity Checkpoint (~60% completion):** At approximately 60% completion of the Coding Implementation Plan, the CDO conducts a formal Design Fidelity Checkpoint against the IDS. Remediation thresholds: ≥ 90% pass rate → proceed with documented failures; 70–89% → proceed with remediation plan and CDO re-check at 80%; < 70% → STOP, remediation required, CTO notifies CPO. Results recorded in `DEVELOPMENT-LOG.md`.
- **String Extraction Readiness Check (CTO internal review):** Before advancing to Stage 6, the Internationalization Specialist runs a preliminary scan of the completed codebase to identify hardcoded strings that were not extracted into resource files. Any remaining hardcoded strings are classified as P2 defects (P1 if they affect core user flows). This is not full extraction — it is an audit to ensure Stage 9 extraction does not become a refactoring exercise under release pressure.
- **Progress Sync Protocol:** Any task exceeding its estimated duration by >20% triggers an automatic CTO → CPO schedule risk notification. Per-track / per-surface variance is also tracked — if one track/surface is >20% behind others, the alert fires regardless of overall average.
- **Cross-cutting i18n at Stage 5:** Locale-aware components from first commit; zero-hardcoded-strings rule enforced in CI; pseudo-locale screenshot regression gate.

Upon completion of each coding task, the progress log is updated. Once all coding tasks are complete, the CTO conducts a comprehensive internal review to ensure the project compiles, runs successfully, and is free of known compilation or runtime bugs before advancing to Code Review.

**Universal gate criteria:**

- [ ] All tasks in the Coding Implementation Plan marked complete.
- [ ] CTO internal review passed (no known compilation or runtime bugs).
- [ ] Design Fidelity Checkpoint completed (≥ 90% conformance, or remediation plan attached).
- [ ] String Extraction Readiness Check completed (hardcoded strings classified as defects, none blocking).
- [ ] Progress log current and archived.

`{{DELTA: any additional Stage 5 gate criteria specific to this product type — e.g., Contract Verification Reports at 30%/70% (mobile KMP/Flutter + full-stack); E2E composition tests passing on a mock surface (full-stack); contract drift report against published consumer schemas (backend).}}`

---

## Stage 6 — Development Deliverables → Architecture & Cross-Functional Conformance Review

> **Naming convention:** Stage 6 is **"Architecture & Cross-Functional Conformance Review,"** not "Code Review." Per-PR code review is continuous (CI-enforced, two-reviewer minimum, `CODEOWNERS`). Stage 6 verifies _aggregate_ conformance, not lines of code.
> **Sign-off model:** Stage 6 uses the **DRI-async** model — the named DRI signs off; the cross-functional panel reviews exceptions asynchronously within 24h. Full-panel convene is reserved for explicit escalation triggers (P0/P1 unresolved, scope > X% change, security exception).
> **Relevant Personnel:** CPO/VP, CDO, CTO, CIO, CSO, R&D Department, User
> **Artifacts In:** Development codebase, PRD, SRD, IDS, UML Package, ADRs, TSD
> **Artifacts Out:** Defect Report (if any) + Conformance Sign-off

**Responsible Producer:** CTO (DRI; convenes panel only on escalation triggers)

The conformance review follows a **two-tier process**:

**Tier 1 — Technical Review (Cross-Lead Cross-Review):** Per-PR code review remains continuous and CI-enforced. Stage 6's Tier 1 produces a **written cross-review memo** that aggregates conformance findings against Stage 3 ADRs/TSD. The reviewer pairing is product-specific: `{{DELTA: Tier-1 pairing (mobile: Android Lead ↔ iOS Lead, with Cross-Platform Lead reviewing shared modules; web: Frontend Lead pairs cross-team; backend: Backend Lead pairs across service-team boundaries; full-stack: Frontend Lead ↔ Backend Lead with VP Mobile reviewing mobile surface)}}`. Automated quality gates (SAST, unit tests, linting) must pass before Tier 1 begins.

**ADR/TSD Compliance Enforcement (Three-Layer Defense — UNIVERSAL):**

1. **Lead Attestation** — Each pipeline lead certifies in their cross-review memo that the codebase matches Stage 3 ADRs/TSD. Any deviation is flagged as P1.
2. **Architecture Compliance Audit** — Senior Architect (Dr. Elena Rostova) conducts an independent audit of the codebase against all Stage 3 ADRs. Audit findings are included in the Defect Report.
3. **CI/CD Gates** — Automated checks enforce dependency version pinning (TSD-approved versions match build files), prohibited technology detection, and security ADR compliance (SAST rules derived from Security Architecture ADRs).

**Tier 2 — Strategic Review (DRI sign-off + panel exceptions async):** The CTO is the DRI. Tier 2 verifies four criteria against the codebase:

1. All requirements and specifications in the PRD have been fully implemented.
2. All design requirements in the IDS and prototypes have been accurately reproduced.
3. All requirements in the UML Engineering Package (diagrams, ADRs, TSD) have been fully implemented as prescribed. **All technology choices in the codebase match Stage 3 ADRs/TSD. Any deviation is a P1 defect.**
4. _(CSO-owned)_ All security requirements in the SRD have been implemented: encryption, secure storage, `{{DELTA: platform/surface security standards (mobile: iOS Keychain / Android Keystore + OWASP MASVS; web: CSP + CORS + OWASP ASVS; backend: secrets vault + OWASP API Top 10; full-stack: cross-surface session + OWASP ASVS+MASVS)}}`.

All identified defects are documented with their P0–P3 classification and a precise description of the gap. The Defect Report is submitted to the user. The user reviews: P0/P1 defects are non-negotiable fixes; the user has final authority to skip or defer P2/P3 defects. The CTO assigns specific R&D personnel to remediate all confirmed defects.

**Live Demonstration:** Before sign-off, the CDO conducts a live demo of the running build(s). For mobile, on both platforms; for web, across the supported browser/device matrix; for backend, against a representative consumer client; for full-stack, end-to-end across all surfaces. Any design or interaction defects discovered during the demo are classified as P0–P3 defects and added to the Defect Report.

**Universal gate criteria:**

- [ ] All P0 and P1 defects resolved.
- [ ] User has reviewed the Defect Report and made explicit decisions on all P2/P3 defects.
- [ ] DRI signed off (or full panel signed off on escalation).
- [ ] Conformance Sign-off archived.

---

## Stage 7 — Conformance Review → Automated Testing

> **Relevant Personnel:** CTO, R&D Department, Test Lead
> **Artifacts In:** Conformance-signed-off codebase
> **Artifacts Out:** Automated Test Suite + Test Results Report

**Responsible Producer:** CTO + Test Lead

The CTO designates R&D personnel to develop test cases and execute automated tests targeting a 100% pass rate. Any bugs identified are consolidated into a Bug Report and handed to developers for remediation. After fixes, testers perform regression testing on all affected functionalities. Regression must pass fully before advancing.

**Universal mandates:**

- 100% pass rate target (subject to user-approved P2/P3 deferrals).
- Regression testing on all fixed functionalities required.
- **Flakiness budget:** < 2% non-deterministic test pass-rate variance with auto-quarantine. Tests exceeding the budget are quarantined and tracked as P2 defects.
- **Accessibility (universal):** Automated WCAG 2.1 AA checks on every PR. Accessibility defects classified per impact: critical = P0, serious = P1, moderate = P2, minor = P3.
- **DAST (Dynamic Application Security Testing):** OWASP ZAP (or equivalent) active + passive scan against all reachable surfaces. Zero "High" risk findings (P1); all "Medium" findings resolved or user-deferred (P2).
- **Penetration Testing:** Manual penetration test by Security Engineer covering OWASP `{{DELTA: applicable OWASP track (mobile: Mobile Top 10 + MASVS; web: Top 10 + ASVS; backend: API Top 10; full-stack: Top 10 + API Top 10 + MASVS)}}`. Zero Critical findings (P0); zero High findings unresolved (P1).
- **Performance Benchmarks:** All PRD performance thresholds verified. 100% pass rate required; any failed metric exceeding threshold by >20% is a P1 defect.

`{{DELTA: pipeline-specific Stage 7 testing mandates — Espresso/XCTest/KMP-shared/Flutter-widget (mobile); Playwright/Cypress + Lighthouse (web); contract tests + load tests (backend); composition E2E + cross-surface contract drift tests (full-stack); device/browser/OS coverage matrices.}}`

**Regression testing model — UNIVERSAL frame, DELTA in execution detail:**

| Trigger       | Scope                                                                    | Execution                                         |
| ------------- | ------------------------------------------------------------------------ | ------------------------------------------------- |
| PR opened     | Affected modules + 2 levels of dependency (unit tests)                   | CI — blocks merge                                 |
| Merge to main | Full unit + integration suite                                            | CI — blocks deployment                            |
| Nightly       | Full E2E on `{{DELTA: device/browser/OS matrix}}` + performance baseline | Automated — opens P1 on failure                   |
| Pre-release   | Full regression suite + exploratory testing                              | Manual + automated — blocks RC promotion on P0/P1 |

Bugs discovered during automated testing are classified using the P0–P3 system. P0/P1 bugs block advancement; P2/P3 are submitted to the user for the same skip/defer authority as in Stage 6.

**Universal gate criteria:**

- [ ] 100% of test cases pass (accounting for user-approved P2/P3 deferrals and the flakiness budget).
- [ ] Regression testing on all fixed functionalities passes.
- [ ] Test Results Report archived.

---

## Stage 8 — Automated Testing → Integrity Verification

> **Sign-off model:** Stage 8 uses the **DRI-async** model — DRI signs off; cross-functional panel reviews exceptions asynchronously within 24h. Full-panel convene is reserved for explicit escalation triggers.
> **Relevant Personnel:** CPO/VP, CDO, CTO, CIO, CSO, Brand Design Department, R&D Department, User
> **Artifacts In:** Post-testing codebase, all prior archived deliverables
> **Artifacts Out:** Integrity Verification Sign-off

**Responsible Producer:** CTO (DRI; convenes panel only on escalation triggers)

The review confirms remediation did not silently remove or reduce functionality — the **"Trim-to-Pass" anti-pattern** (KEEP-01). Functionality removal is never a valid remediation strategy.

The review verifies (universal):

- All PRD features remain intact (verified against per-feature Stage 6 baseline).
- All CDO/IDS design specifications accurately realised (IDS Conformance Matrix re-verified ≥ 95%).
- All UML engineering standards upheld.
- All SRD security requirements remain enforced and effective (not just present — correctness verified).
- **Removal, disabling, or weakening of any security control specified in the SRD (encryption, certificate pinning, root/jailbreak detection, obfuscation, authentication flows) is classified as a P0 defect.** Stealthy weakening — e.g., keeping certificate pinning but reducing validation strictness, keeping encryption but using a weaker cipher — is also classified as P0.
- Analytics instrumentation integrity is verified — all PRD-defined metrics must still fire correctly after Stage 7 remediation. Any regressions are treated as P0/P1 defects.

**Universal gate criteria:**

- [ ] No functionality reduced or removed relative to the Stage 6 baseline.
- [ ] DRI signed off (or panel signed off on escalation).
- [ ] Integrity Verification Sign-off archived.

`{{DELTA: any additional Stage 8 product-specific integrity checks (e.g., mobile: per-platform feature parity; full-stack: cross-surface state coherence; backend: contract back-compat; web: SSR vs CSR parity).}}`

---

## Stage 9.5 — Internal Dogfood (NEW — Step 15) — UNIVERSAL

> **Stage scope:** Mandatory employee Beta channel between Stage 8 and Stage 9. Bug telemetry mandatory; minimum 5 business days. See [`dogfood-telemetry-template.md`](./dogfood-telemetry-template.md) for the canonical telemetry-report shape.
> **Relevant Personnel:** VP Quality (DRI), CTO, CPO, CDO, CSO
> **Artifacts In:** Integrity-verified codebase
> **Artifacts Out:** Dogfood Telemetry Report

**Responsible Producer:** VP Quality

**Universal gate criteria:**

- [ ] 5 business days minimum of internal dogfood usage.
- [ ] Bug telemetry collected and triaged.
- [ ] Zero unresolved Sev1 (P0) defects in telemetry.
- [ ] Dogfood Telemetry Report archived.

---

## Stage 9 — Integrity Verification → Translation Production

> **Naming convention:** Stage 9 is **"Translation Production,"** not "Internationalization Engineering." i18n is a continuous concern from Stage 2 onward (see `{{DELTA: cross-cutting i18n requirements per product}}`); Stage 9's scope is translation accuracy by linguists.
> **Relevant Personnel:** CTO-L (Chief Translation Officer) + Translation Team, CPO/VP, CDO, CTO, R&D
> **Artifacts In:** Integrity-verified + dogfood-validated codebase, PRD (language requirements section)
> **Artifacts Out:** Translated codebase + Translation Verification Report

**Responsible Producer:** CTO-L

The CTO-L and Translation Team take ownership of all extracted strings and datasets, producing translations into all user-specified languages (e.g., English, Chinese, Japanese, Korean, French) governed by the **Language Translation Module**.

**Universal mandates:**

- The String Key Taxonomy ADR from Stage 3 governs key shape; resource files conform to the platform-specific format `{{DELTA: resource format — strings.xml + Localizable.strings + key-index.csv (mobile); ICU/i18next + key-index.csv (web); locale-keyed enums (backend errors); union of mobile + web (full-stack)}}`.
- The CPO/VP, CDO, and CTO conduct a **structural completeness review**: i18n engineering already complete (under Step 2 cross-cutting); Stage 9 verifies translation _accuracy_ across all target languages.
- The CTO-L issues a Translation Verification Report confirming accuracy across all target languages.

**Universal gate criteria:**

- [ ] Translation produced for all target languages.
- [ ] CPO/VP, CDO, CTO structural completeness review passed (i18n engineering already complete).
- [ ] CTO-L Translation Verification Report issued and archived.

---

## Stage 10 — Translation Production → Release Readiness Check

> **Sign-off model:** Stage 10 uses the **DRI-async** model — DRI signs off; full panel reviews exceptions asynchronously. Full-panel convene is reserved for explicit escalation triggers.
> **Relevant Personnel:** CPO/VP, CDO, CTO, CIO, CSO, CTO-L, VP Platform, VP Quality, User
> **Artifacts In:** All archived deliverables from all prior stages
> **Artifacts Out:** Release Readiness Report + Release Decision

**Responsible Producer:** CTO (DRI; convenes panel only on escalation triggers)

A final holistic gate ensuring the product meets all release standards before shipping. Each panel member (or DRI delegate) reviews their domain checklist item(s) and issues sign-off. Any open item blocks release until resolved.

### Release Readiness Checklist — Final Form (Plan §8.5) — UNIVERSAL

| #   | Domain             | Criteria                                                               | Sign-off Authority |
| --- | ------------------ | ---------------------------------------------------------------------- | ------------------ |
| 1   | Product            | All PRD requirements implemented and verified                          | CPO/VP             |
| 2   | Design             | All CDO/IDS specifications accurately realised                         | CDO                |
| 3   | Architecture       | All UML/ADR/TSD standards upheld                                       | CTO + CIO          |
| 4   | Security           | All SRD requirements enforced; OWASP MASVS/ASVS compliant              | CSO                |
| 5   | Testing            | 100% automated test pass rate (with flakiness budget per Step 13)      | CTO + Test Lead    |
| 6   | Localisation       | All target languages complete and verified                             | CTO-L              |
| 7   | Platform           | App Store / Google Play / web hosting / API publishing reqs met        | CTO + CPO/VP       |
| 8   | Performance        | TTI / startup / frame budget met                                       | CTO + VP Platform  |
| 9   | Accessibility      | WCAG 2.1 AA verified, no Level-AA failures                             | CDO                |
| 10  | Privacy            | Data minimization, no PII in logs, consent flows correct               | CSO + (future) GC  |
| 11  | Dogfood            | Stage 9.5 internal beta complete, no Sev1 telemetry                    | VP Quality         |
| 12  | Live Ops Readiness | Sev ladder + on-call + error budget defined per `incident-response.md` | VP Platform + CSO  |

`{{DELTA: any additional Stage 10 product-specific release criteria — e.g., mobile: store submission package (App Store screenshots, Play listing assets, age rating); web: CDN cache invalidation; backend: API versioning + deprecation notice; full-stack: cross-surface release coordination plan.}}`

**Universal gate criteria:**

- [ ] All twelve checklist items signed off.
- [ ] Release Readiness Report submitted to user.
- [ ] User has issued the final release decision.
- [ ] Release Readiness Report archived.

---

## Stage 11 — Live Operations (NEW — Step 6) — UNIVERSAL FRAME

> **Stage scope:** Stage 11 is **continuous** — it begins at release and never closes for the lifetime of the product. The full operating model lives at [`incident-response.md`](./incident-response.md).
> **Relevant Personnel:** VP Platform (DRI), CSO, CTO, CPO/VP, Test Lead, On-Call Rotation
> **Artifacts In:** Released product
> **Artifacts Out:** Quarterly Business Review (QBR) reports, postmortem reports, error budget reports

**Responsible Producer:** VP Platform + CSO

**Universal mandates:**

- Sev1 / Sev2 / Sev3 incident ladder defined.
- On-call rotation staffed and documented.
- Blameless postmortem template + cadence defined per [`incident-response.md`](./incident-response.md).
- Error budget per quarter defined and tracked.
- QBR cadence defined.
- **Rollback authority chain explicitly named:** the on-call DRI has rollback authority without convening C-suite; the chain of escalation is documented in [`incident-response.md`](./incident-response.md).

`{{DELTA: any additional Stage 11 product-specific live-ops mandates — e.g., mobile: store-rejection escalation playbook + crash-rate SLO per platform; web: CDN failover + WAF rule cadence; backend: capacity scaling triggers + dependency-failure runbooks; full-stack: cross-surface incident coordination.}}`

---

## Appendix — Universal vs. Delta Section Index

| Section                                   | Universal? | Delta-required?                                    |
| ----------------------------------------- | ---------- | -------------------------------------------------- |
| Defect Severity (P0–P3)                   | ✅         | —                                                  |
| Progress Sync Protocol                    | ✅         | —                                                  |
| Platform / Architecture Strategy Matrix   | —          | ✅                                                 |
| Stage 0 Problem Validation                | ✅ (frame) | ✅ (additional product-specific evidence)          |
| Stage 1 PRD authorship                    | ✅ (frame) | ✅ (PRD steward identity, surface-specific fields) |
| Stage 2 prototype + IDS                   | ✅ (frame) | ✅ (prototype format varies by surface)            |
| Stage 3 Mandatory ADRs                    | ✅ (frame) | ✅ (additional product-specific ADRs)              |
| Stage 4 Coding Implementation Plan        | ✅ (frame) | ✅ (track / service / rendering plan)              |
| Stage 5 Development                       | ✅ (frame) | ✅ (track execution, platform leads)               |
| Stage 6 Architecture & Conformance Review | ✅ (frame) | ✅ (tier-1 review pairing, security mandates)      |
| Stage 7 Automated Testing                 | ✅ (frame) | ✅ (platform-specific testing mandates)            |
| Stage 8 Integrity Verification            | ✅         | ✅ (additional product-specific checks)            |
| Stage 9.5 Dogfood                         | ✅         | —                                                  |
| Stage 9 Translation Production            | ✅ (frame) | ✅ (resource file format)                          |
| Stage 10 Release Readiness                | ✅         | ✅ (additional product-specific release criteria)  |
| Stage 11 Live Operations                  | ✅ (frame) | ✅ (product-specific live-ops mandates)            |

---

## Document Version History

| Version | Date           | Author             | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------- | -------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.1     | April 21, 2026 | Software Architect | Initial **skeleton** authored. Universal sections sketched; `{{DELTA}}` placeholders reserved for per-product overlays.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 0.2     | April 21, 2026 | Software Architect | **Phase P-1 (mobile extraction).** Skeleton replaced with universal content extracted from `mobile-development/pipeline.md` (legacy, 453 lines). Universal sections (Defect Severity, Progress Sync, Stage 0/1/2/3/4/5/6/7/8/9.5/9/10/11 frames, Release Readiness Checklist 12 rows) populated with real prose/tables. `{{DELTA}}` markers retained only where content is genuinely product-specific (Strategy Matrix, surface-specific ADRs, Tier-1 reviewer pairing, platform-specific testing mandates, resource file format, additional release criteria, live-ops mandates). Mobile-only proof-of-pattern overlay sits in [`company/pipeline/mobile-development/delta.md`](company/pipeline/mobile-development/delta.md). Web/backend/full-stack pending P-3. |
