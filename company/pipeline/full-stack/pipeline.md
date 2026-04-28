# Full-Stack Cross-Platform Pipeline

## Overview

The company's full-stack cross-platform development workflow is a ten-stage state machine. At each stage you are required to log the current execution phase and update the workflow's progress. Each stage follows a consistent schema: **Relevant Personnel**, **Artifacts In**, **Artifacts Out**, a designated **Responsible Producer**, explicit **Reviewers**, **Gate Criteria** that must be satisfied before the stage closes, and **Defect Handling** where applicable.

This is a **meta-pipeline** that orchestrates coordinated delivery across web + mobile + backend as a unified product. It is NOT a replacement for individual pipeline specs -- it sits above them.

Each workflow must be assigned to a designated responsible party. Each assigned individual is regarded as a "Subagent"; as the primary "Agent," you must collaborate with these Subagents -- leveraging their respective skill sets -- to successfully complete every task within the workflow.

---

## Defect Severity System (P0-P3)

Applied in Stages 6, 7, and 8. All identified defects must be classified before any remediation begins.

| Level | Definition                              | Release Impact                   |
| ----- | --------------------------------------- | -------------------------------- |
| P0    | App crash / data loss / security breach | Blocks release -- non-negotiable |
| P1    | Core feature broken / major UX failure  | Blocks release -- non-negotiable |
| P2    | Minor feature degraded / cosmetic issue | User decides to fix or defer     |
| P3    | Polish / nice-to-have                   | User decides to fix or defer     |

**Authority rule:** P0/P1 classification is final and cannot be overridden. P2/P3 defects are submitted to the user, who has explicit final authority to skip or defer them.

---

## Progress Sync Protocol

Active from Stage 4 onward.

- Each completed coding task triggers an update to the progress log.
- Any task exceeding its estimated duration by **>20%** triggers an automatic CTO to CPO schedule risk notification.
- The CTO produces weekly progress summaries (status indicators, milestone percentages, risk mitigation plans) for C-suite visibility.

**Full specification:** [`monitoring.md`](monitoring.md) -- Progress Monitoring & Recovery System (mandatory for Stage 4+ projects).

---

## Multi-Platform Strategy Matrix

### Overview

Stage 5 development executes per the **Multi-Platform Strategy Matrix**, which determines track activation based on the **Multi-Platform Strategy ADR** produced at Stage 3. The Stage 1 gate asks "Which platforms?" -- this confirms the **target platform combination**. The **implementation approach** per platform is locked at **Stage 3**.

**Three mutually exclusive scenarios -- a project selects exactly one.**

### Decision Matrix

| Dimension                 | Full Product (web + mobile + API) | Web + API Only (no mobile)  | Mobile + API Only (no web)      |
| ------------------------- | --------------------------------- | --------------------------- | ------------------------------- |
| **Stage 1 Gate**          | All platforms                     | Web + API                   | Mobile + API                    |
| **Stage 3 ADR**           | Multi-platform (all 3)            | Web + backend               | Mobile + backend                |
| **Stage 5 Active Tracks** | FS-WFE + FS-WBE + FS-MOB + FS-INT | FS-WFE + FS-WBE + FS-INT    | FS-MOB + FS-WBE + FS-INT        |
| **Stage 5 Team Size**     | 17-23                             | 9                           | 12-18                           |
| **Stage 6 Tier 1 Review** | All leads cross-review            | Web to Backend              | Mobile to Backend               |
| **Stage 7 Testing**       | All platform tests + parity       | Web + backend E2E           | Mobile + backend E2E            |
| **Stage 10 Submission**   | All platforms simultaneously      | Web deployed + backend live | Mobile submitted + backend live |
| **CI/CD Scope**           | All platform CI/CD + parity       | Web + backend CI            | Mobile + backend CI             |

### Track Activation Protocol

| Scenario                   | FS-WFE (Web Frontend) | FS-WBE (Web Backend) | FS-MOB (Mobile)           | FS-INT (Integration) | Coordinator                        |
| -------------------------- | --------------------- | -------------------- | ------------------------- | -------------------- | ---------------------------------- |
| Full product               | **FULL** (4 eng)      | **FULL** (3 eng)     | Per mobile ADR (7-13 eng) | **FULL** (3 eng)     | Elena Vasquez + Mei-Ling Johansson |
| Web + API only (no mobile) | **FULL** (4 eng)      | **FULL** (3 eng)     | **Dormant**               | **LIGHT** (2 eng)    | Elena Vasquez                      |
| Mobile + API only (no web) | **Dormant**           | **FULL** (3 eng)     | Per mobile ADR (7-13 eng) | **LIGHT** (2 eng)    | Mei-Ling Johansson                 |

**Track semantics:**

| Term        | Definition                                                                                                               |
| ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| **FULL**    | End-to-end feature implementation, testing, and delivery for that platform. Owns complete codebase for that platform.    |
| **LIGHT**   | Integration and adaptation only (e.g., API consumer wiring, platform channel handlers). NOT full feature implementation. |
| **PRIMARY** | Owns the shared integration layer. Coordinates cross-platform contracts, shared data models, and release timing.         |
| **Dormant** | Track lead and engineers are reassigned to technical debt, test automation, cross-training, or other pipeline projects.  |

### Resource Reallocation Protocol

| Scenario                   | Freed Resources           | Reassignment Options                                              |
| -------------------------- | ------------------------- | ----------------------------------------------------------------- |
| Full product               | None -- all tracks active | N/A                                                               |
| Web + API only (no mobile) | All mobile eng (7-13 eng) | Other mobile projects, mobile test automation, SDK migration prep |
| Mobile + API only (no web) | All web FE eng (4 eng)    | Other web projects, web test automation, design system updates    |

### Per-Scenario CI/CD Blueprint

| CI/CD Component       | Full Product                                                      | Web + API Only                  | Mobile + API Only            |
| --------------------- | ----------------------------------------------------------------- | ------------------------------- | ---------------------------- |
| Web Frontend CI       | ESLint, TSC, Vitest, Playwright                                   | ESLint, TSC, Vitest, Playwright | N/A                          |
| Mobile CI             | Per mobile Platform Strategy                                      | N/A                             | Per mobile Platform Strategy |
| Backend CI/CD         | build, test, contract, load                                       | build, test, contract, load     | build, test, contract, load  |
| Cross-platform E2E CI | Playwright (web) + Maestro/Appium (mobile) against shared staging | N/A                             | N/A                          |
| Parity CI             | Automated comparison of feature coverage across platforms         | N/A                             | N/A                          |
| Integration CI        | Shared API contract tests consumed by all frontend platforms      | Shared API contract tests       | Shared API contract tests    |
| Deployment            | Coordinated -- backend first, then web + mobile simultaneously    | Backend first, then web         | Backend first, then mobile   |

### Multi-Platform Strategy ADR Requirements

The mandatory Multi-Platform Strategy ADR at Stage 3 must include **all 16 fields**:

1. **Decision statement** -- Which platforms? (web + iOS + Android? web + Android?)
2. **Web approach** -- SSR vs CSR vs PWA
3. **Mobile approach** -- Native vs KMP vs Flutter
4. **Backend approach** -- Shared API vs per-platform APIs
5. **Rationale** -- Market needs, team skills, time-to-market
6. **Trade-offs** -- Development speed vs. platform parity vs. cost
7. **Team capability assessment** -- All leads available?
8. **Risk analysis** -- Coordination overhead, platform divergence, release timing
9. **TCO projection (24-month)** -- All platforms combined, total estimated cost
10. **Vendor lock-in risk matrix** -- Per-platform + overall
11. **Performance SLA alignment** -- Per-platform thresholds (web: LCP/CLS; mobile: cold start/fps; backend: P99/uptime)
12. **Security mandate** -- Unified auth, data protection, platform-specific hardening
13. **STRIDE threat model** -- Cross-platform attack surface
14. **Track activation mapping** -- All four tracks
15. **Reassignment plan** -- For dormant tracks
16. **Release coordination** -- Which platform launches first? Staggered or simultaneous?

**Ownership:** CTO authors. All platform leads (Frontend, Backend, Mobile) input. CIO reviews for technology conformance. CSO reviews for security conformance. CDO reviews for design quality impact. Once approved at Stage 3 gate, this decision is **locked** -- switching platform combinations requires a full Stage 3 re-entry with ADR re-authorship and Implementation Plan re-baseline.

---

## Stage Definitions

### Stage 1: Requirements to PRD + SRD

**Relevant Personnel:** VP Web (Julia Thorne) + VP API (Alex Rivera) (PRD — primary); CPO (template steward, arbiter for mobile features, final sign-off); CSO (SRD — primary); both VPs (SRD co-authors for their respective surfaces)

**Artifacts In:** Raw product requirements, user research, market analysis

**Artifacts Out:**

- `PRD.md` -- Product Requirements Document (with JTBD, kill criteria, commercial assessment, all target platforms specified upfront)
- `SRD.md` -- Security Requirements Document (unified security requirements across all platforms)

**Reviewers:** CTO, CIO, CSO, CPO, VP Web, VP API

**Gate Criteria:**

1. User has confirmed all target platforms (web, iOS, Android, API)
2. User has confirmed API consumer types (web frontend, mobile apps, third-party integrations)
3. PRD includes per-platform performance SLA targets
4. SRD includes cross-platform security requirements (unified auth with cross-platform session management, per-platform security baselines — iOS ATS, Android Keystore, web CSP/cookies, data synchronization security, API contract security verification across all consuming platforms)
5. User has confirmed no further revisions are required

**Authorship Model Subnote:** Web + API features are VP-led with CPO template review; features that also touch mobile carry CPO veto on the mobile-facing sections; deadlocks escalate to the CPO.

**Defect Handling:** P0/P1 defects block Stage 1 to 2. P2/P3 defects require user decision.

---

### Stage 2: PRD to Cross-Platform Prototype + IDS

**Relevant Personnel:** CDO, VP Web (Julia Thorne), VP API (Alex Rivera)

**Artifacts In:** PRD, SRD (paired artifacts)

**Artifacts Out:**

- Approved cross-platform design package:
  - Web prototype (production-grade HTML/CSS/JS at 3 breakpoints — 375px, 768px, 1440px)
  - Mid-fidelity iOS wireframes (minimum: all critical screens, key user flows, platform-specific navigation patterns)
  - Mid-fidelity Android wireframes (minimum: all critical screens, key user flows, platform-specific navigation patterns)
  - API specification (OpenAPI/Swagger or GraphQL SDL) with sample responses for all endpoints
  - Developer portal low-fidelity prototype (documentation layout, interactive explorer, onboarding flow)
- `IDS.md` -- Cross-Platform Interaction Design Specification (covers all platforms — web, iOS, Android. Design token compatibility matrix: CSS custom properties to iOS UIColor/Android ColorRes mapping. Platform-specific accessibility, animation specs per platform, gesture vocabulary per platform)

**Reviewers:** CTO, CDO, CPO, VP Web (Julia Thorne), VP API (Alex Rivera)

**Gate Criteria:**

1. Web prototype validates functional requirements across all breakpoints with at least one interactive user flow
2. Mid-fidelity mobile wireframes cover all critical screens with platform-specific navigation patterns
3. IDS covers all platforms with design token compatibility matrix (web CSS → iOS → Android mapping)
4. IDS includes platform-specific accessibility specifications (Web: WCAG 2.1 AA + screen reader methodology; iOS: VoiceOver + Dynamic Type + switch access; Android: TalkBack + font scaling)
5. API specification validates (OpenAPI lint passes, GraphQL SDL validates) with interactive mock server or Swagger UI instance
6. CDO confirms design fidelity to PRD requirements across all platforms
7. User has given final confirmation

**Defect Handling:** P0/P1 defects block Stage 2 to 3. P2/P3 defects require user decision.

---

### Stage 3: Prototype to UML Engineering Package

**Relevant Personnel:** CTO (UML), CIO (ADRs, TSD)

**Artifacts In:** PRD, SRD, web prototype, IDS

**Artifacts Out:**

- UML diagrams (class, sequence, component, activity) -- covering all platforms
- 13 mandatory ADRs:
  - `ADR-MULTI-PLATFORM-STRATEGY.md` -- Which platforms, per-platform strategy, release coordination (16 fields, including shared state synchronization)
  - `ADR-API-STRATEGY.md` -- REST vs GraphQL vs gRPC decision, data consistency model, API versioning strategy, deprecation policy, developer experience (inherited from Backend API pipeline, adapted for cross-platform context)
  - `ADR-OBSERVABILITY.md` -- Distributed tracing across all platforms (OpenTelemetry), structured logging standards, metrics collection (Prometheus/Grafana), per-platform SLO error budgets, cross-platform trace correlation
  - `ADR-DATABASE.md` -- SQL vs NoSQL selection, migration tooling (Flyway/golang-migrate/Prisma), connection pooling strategy (PgBouncer/HikariCP), read replica strategy, database as shared state across all platforms
  - `ADR-FEATURE-FLAGS.md` -- Cross-platform feature flag governance: unified flag strategy (LaunchDarkly/Unleash), per-platform flag synchronization, kill switch protocol, staggered rollout coordination, environment parity (dev/staging/prod flags must match across platforms)
  - `ADR-API-CLIENT-GENERATION.md` -- Shared API client generation strategy: OpenAPI Generator vs Swagger Codegen vs manual, client SDK consistency enforcement across web/iOS/Android, version synchronization, breaking change detection
  - `ADR-DESIGN-TOKEN-PIPELINE.md` -- Design token pipeline: token generation tool (Style Dictionary/Figma Tokens/custom), versioning, drift detection across platforms, design-to-code synchronization, per-platform token mapping (CSS custom properties → iOS UIColor/Android ColorRes)
  - `ADR-SECURITY-CRYPTO.md` -- Cryptography (per-platform: Web Crypto API, iOS CryptoKit/Keychain, Android Keystore)
  - `ADR-SECURITY-WEB-PATTERNS.md` -- Web-specific: XSS prevention, CSRF tokens, CSP, CORS, OAuth 2.0 session security, SRI hashes
  - `ADR-SECURITY-MOBILE-PATTERNS.md` -- Mobile-specific: Certificate pinning, secure storage (Keychain/Keystore), root/jailbreak detection, App Attest/Play Integrity
  - `ADR-SECURITY-CROSS-PLATFORM.md` -- Unified auth flow with cross-platform session management, token revocation propagation, cross-platform data protection, platform-specific hardening
  - `ADR-STRING-KEY-TAXONOMY.md` -- String key naming convention, unified across all platforms
  - `ADR-ACCESSIBILITY.md` -- Per-platform accessibility: Web WCAG 2.1 AA + screen reader methodology, iOS VoiceOver + Dynamic Type, Android TalkBack + font scaling, developer portal WCAG 2.1 AA
- `TSD.md` -- Technology Selection Document (all-platform tech stack, cross-platform integration decisions: shared API client generation, cross-platform E2E orchestration, unified design token pipeline)

**Reviewers:** CTO, CIO, CPO

**Gate Criteria:**

1. All 13 ADRs + TSD authored, reviewed, and approved
2. TSD covers all platform technology selections + cross-platform integration decisions
3. UML diagrams cover all platform layers + shared data model
4. Multi-Platform Strategy ADR locked (no changes without Stage 3 re-entry)
5. Per-platform security ADRs define platform-specific baselines (iOS ATS, Android Keystore, web CSP/cookies)
6. Accessibility ADR defines per-platform WCAG 2.1 AA + platform-specific targets
7. User has approved the UML Engineering Package

**Defect Handling:** P0/P1 defects block Stage 3 to 4. P2/P3 defects require user decision.

---

### Stage 4: UML to Coding Implementation Plan

**Relevant Personnel:** CTO

**Artifacts In:** PRD, SRD, UML package, ADRs, TSD

**Artifacts Out:**

- `IMPLEMENTATION-PLAN.md` -- Cross-platform Implementation Plan (shared data models, API contracts, auth flow)
- `RTM.md` -- Requirements Traceability Matrix (per-platform)
- `TEST-ARCHITECTURE-DOCUMENT.md` -- All platform test suites + cross-platform E2E flows
- `GANTT.md` -- Gantt Chart (with critical path across all platforms)

**Reviewers:** CTO, CPO

**Gate Criteria:**

1. Implementation Plan covers all active tracks (FS-WFE, FS-WBE, FS-MOB, FS-INT) with explicit task assignments
2. RTM traces 100% of PRD requirements to per-platform implementation tasks
3. Test Architecture Document covers all platform test suites + cross-platform E2E
4. Release coordination plan defined (staggered vs simultaneous launch) with per-platform go/no-go authority and rollback procedure
5. Database migration strategy defined with rollback procedure and zero-downtime migration plan
6. SIS (Security Implementation Specification) completed and CSO-signed — covers per-platform security patterns, cross-platform auth session management, shared backend security controls
7. Progress Sync Protocol thresholds defined (baseline estimates for >20% variance detection)
8. VP Engineering confirms buddy pairings established for all 12/20-score engineers assigned to this project's tracks (see `buddy-system-assignments.md`).
9. User has approved the plan

**Defect Handling:** P0/P1 defects block Stage 4 to 5. P2/P3 defects require user decision.

---

### Stage 4.1: Security Implementation Specification (SIS) — Cross-Platform

Before **Stage 5** begins, the security team produces a full-stack-specific SIS:

- **Author:** Security team (Natalia Petrova + James Wright), signed off by CSO
- **Timing:** Completed during **Stage 4**, referenced in CI/CD readiness gate before **Stage 5** Day 1
- **Content:** Translates SRD requirements into cross-platform code patterns — (1) Web: XSS prevention, CSRF tokens, CSP, cookie security, SRI; (2) Mobile: certificate pinning, secure storage (Keychain/Keystore), root/jailbreak detection, App Attest/Play Integrity; (3) Backend: rate limiting, input validation, authZ, encrypted DB at rest, TLS 1.3; (4) Cross-platform: unified auth flow with cross-platform session management, token revocation propagation across platforms, data synchronization security guarantees, API contract security verification across all consuming platforms, shared threat model covering cross-platform attack vectors
- **Gate Criterion:** "SIS completed and CSO-signed" is a **Stage 4**→**Stage 5** gate criterion

---

### Stage 5: Plan to Software Development

**Relevant Personnel:** CTO (oversees), Elena Vasquez (VP Web & Backend -- coordinates web + backend tracks), Mei-Ling Johansson (Cross-Platform Lead -- coordinates mobile track per Platform Strategy ADR)

**Artifacts In:** Implementation Plan, Gantt Chart, RTM, TAD, SIS, ADRs, TSD

**Artifacts Out:**

- Development codebase (web frontend + web backend + mobile + integration layer)
- Contract Verification Reports (CROSS-PLATFORM-CONTRACT-REPORT.md -- API parity across all platforms)
- String Extraction Readiness audit (unified audit across all platforms via single key-index.csv)
- `DEVELOPMENT-LOG.md` -- Per-track development logs

**Reviewers:** CTO (internal review only -- no panel)

**Gate Criteria:**

1. All Implementation Plan tasks marked complete across all active tracks
2. Design Fidelity Checkpoint passed at ~60% completion across all platforms (greater than or equal to 90% pass rate on all platforms to proceed; 70-89% on any platform with documented remediation plan; less than 70% on any platform to STOP, CTO notifies CPO)
3. String Extraction Readiness audit completed -- unified key-index.csv parity verified, remaining hardcoded strings less than or equal to 5%
4. Cross-Platform Contract Report produced -- API parity verified across all platforms
5. CTO internal review checklist completed:
   - All platform builds pass with zero errors
   - All platforms run without errors on their respective environments
   - No P0/P1 defects in bug tracker
   - Design Fidelity Checkpoint completed across all platforms
   - String Extraction Readiness completed across all platforms
   - Cross-platform contract verification (CROSS-PLATFORM-CONTRACT-REPORT.md produced)
   - SIS requirements implemented and verified across all platforms
   - `DEVELOPMENT-LOG.md` current for all tracks

**Progress Sync Protocol:** Active -- any task >20% over estimate triggers CTO to CPO notification.

**Buddy System Tracking:** For any 12/20-score engineers assigned to this project, buddy pairings are tracked in `PROGRESS.md` session logs and checkpoint JSON buddy progress field. 30/60/90-day checkpoints conducted per `buddy-system-assignments.md` protocol.

**Technical Debt Allocation:** 15-20% sprint capacity reserved (calibrated per project: greenfield 20%, mature 15%, inherited up to 30%). Security debt minimum: 5% of total sprint capacity across all platforms.

---

### Stage 6: Development to Code Review

**Relevant Personnel:** CTO (convenes panel)

**Artifacts In:** Development codebase, Cross-Platform Contract Report, String Extraction Readiness audit, DEVELOPMENT-LOG.md

**Artifacts Out:**

- `DEFECT-REPORT.md` -- Defect Report with Architecture Compliance Audit, Cross-Platform Conformance Matrix, per-platform pre-Tier 1 automated quality gates
- `SIGNOFF.md` -- Code Review Sign-off (with Cross-Platform Live Demonstration results)

**Reviewers:** CTO (convenes), CPO, CDO, CIO, CSO, Frontend Lead, Backend Lead, Mobile Lead, VP Web (Julia Thorne) (advisor), VP API (Alex Rivera) (advisor)

**Gate Criteria:**

1. Three-Layer Defense for ADR/TSD compliance passed:
   - **Layer 1:** All platform leads attest their implementations conform to locked Stage 3 ADRs and TSD technology selections
   - **Layer 2:** Dr. Elena Rostova conducts independent cross-platform audit of ADR/TSD compliance, produces written audit memo
   - **Layer 3:** CI/CD gates passed per platform -- dependency version pinning, prohibited technology detection, security ADR compliance
2. Cross-Platform Live Demonstration completed -- CDO interacts with critical user flows on each platform (web on staging, iOS on simulator/device, Android on emulator/device), verifying feature parity; responsive/adaptive check at all breakpoints and screen sizes; same feature exercised on each platform, behavior compared
3. Cross-Platform Conformance Matrix greater than or equal to 95% -- feature parity greater than or equal to 95% across platforms
4. Architecture Compliance Audit findings addressed or deferred with user approval
5. Pre-Tier 1 automated quality gates passed per platform

**Defect Handling:** P0/P1 defects block Stage 6 to 7. P2/P3 defects submitted to user for fix/defer decision.

---

### Stage 7: Code Review to Automated Testing

**Relevant Personnel:** CTO (designates R&D personnel), Test Lead (Priscilla Oduya), Test Automation Lead (Rachel Kim)

**Artifacts In:** Code Review Sign-off, Defect Report (with user decisions on P2/P3)

**Artifacts Out:**

- Automated Test Suite (mobile + web + backend + cross-platform E2E + parity tests)
- `TEST-RESULTS-REPORT.md` -- Test Results Report (with DAST per platform, per-platform performance benchmarks, Design Fidelity Test Checklist)

**Reviewers:** CTO, Test Lead

**Gate Criteria:**

1. 100% automated test pass rate achieved across all platforms
2. DAST (OWASP ZAP) passed -- zero critical/high findings on web + backend; MASVS mobile pen test passed; manual web pen testing (OWASP WSTG) passed -- zero critical/high; manual API pen testing (OWASP API Security Top 10) passed -- zero critical/high
3. Performance benchmarks passed -- per-platform SLAs met (web: LCP/CLS; mobile: cold start/fps; backend: P99/uptime)
4. API contract tests passed -- 100% endpoint coverage across all consumers (Pact)
5. Cross-platform E2E tests passed -- same user journey verified on web + mobile
6. Parity test passed -- feature parity greater than or equal to 95% across platforms
7. Accessibility audit passed -- all platforms meet WCAG 2.1 AA ≥ 95% (web: axe-core + screen reader; iOS: VoiceOver manual test; Android: TalkBack manual test; backend: developer portal screen reader test)
8. Regression testing passed -- all Stage 6+ fixed functionalities verified per platform

**Defect Handling:** P0/P1 defects block Stage 7 to 8. P2/P3 defects submitted to user for fix/defer decision.

---

### Stage 8: Automated Testing to Integrity Verification

**Relevant Personnel:** CTO (convenes panel)

**Artifacts In:** Test Results Report, Defect Report (with user decisions on P2/P3)

**Artifacts Out:**

- Integrity Verification Sign-off reports from each panel member (CPO, CDO, CIO, CSO, all platform leads)

**Reviewers:** CTO (convenes), CPO, CDO, CIO, CSO, Brand Design, all platform leads, VP Web (Julia Thorne), VP API (Alex Rivera)

**Gate Criteria:**

1. Stage 6 baseline re-verification -- all Stage 6 defects confirmed fixed, no regression on any platform
2. Per-feature PRD checklist -- each PRD requirement verified as implemented and tested on all target platforms
3. Cross-platform parity re-verification -- feature parity greater than or equal to 95% maintained across all platforms
4. Stealthy weakening detection -- no security controls weakened/removed/disabled on any platform since Stage 6. Platform-specific examples: (Web) relaxed CSP, removed CSRF, weakened cookies, downgraded TLS; (Mobile) removed certificate pinning, disabled root/jailbreak detection, weakened Keychain/Keystore encryption; (Backend) removed rate limiting, relaxed authZ, expanded CORS, disabled audit logging; (Cross-platform) inconsistent auth enforcement across platforms, weaker security on one platform vs. others (attacker pivots to weakest platform). Any such change is classified as **P0 defect**.
5. Analytics integrity verified -- all analytics events firing correctly on all platforms

**Defect Handling:** P0/P1 defects block Stage 8 to 9. Functionality removal is **never** valid remediation. Platform divergence (features differ) is classified as P1 until parity restored.

---

### Stage 9: Integrity to i18n Engineering

**Relevant Personnel:** CTO-L (leads), Internationalization Specialist (Tomas Dvoracek), Translation Team

**Artifacts In:** Integrity Verification Sign-off, codebase

**Artifacts Out:**

- Localised codebase (all platforms, all target languages)
- `TRANSLATION-VERIFICATION-REPORT.md` -- Translation Verification Report (with BLEU/TER scores, unified string extraction from all platforms)

**Reviewers:** CTO-L, CTO

**Gate Criteria:**

1. All target languages translated across all platforms
2. BLEU score greater than or equal to 0.80 for all languages
3. Unified string extraction via single key-index.csv verified
4. Cross-platform string parity report produced -- all platforms have matching string coverage
5. Accessibility labels localized across all platforms

**Defect Handling:** P0/P1 defects block Stage 9 to 10. P2/P3 defects deferred to post-release if CTO-L approves.

---

### Stage 10: i18n to Release Readiness Check

**Relevant Personnel:** CTO (convenes panel), CPO, VP Product, Web Platforms (Julia Thorne), VP Product, API & Developer Platforms (Alex Rivera), CDO, CSO, CTO-L, **User** (final decision)

**Artifacts In:** Localised codebase, Translation Verification Report, all prior stage artifacts

**Artifacts Out:**

- `RELEASE-CHECKLIST.md` -- Release Readiness Report (7-item checklist with per-platform sub-checklists)
- Release Decision (approved / conditional / rejected)

**Reviewers:** CTO (convenes), CPO, VP Web (Julia Thorne), VP API (Alex Rivera), CDO, CSO, CTO-L + **User**

**Release Checklist (7 Items):**

| #   | Domain                                                                      | Sign-off Authority | Key Sub-Checks                                                                                                                                                                                                                                                                                                                                                                   |
| --- | --------------------------------------------------------------------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Product -- all PRD requirements implemented                                 | CPO + VPs          | Analytics firing on all platforms, IAP configured, kill condition monitoring active                                                                                                                                                                                                                                                                                              |
| 2   | Design -- all CDO/IDS specifications accurately realised                    | CDO                | Cross-platform conformance greater than or equal to 95%, design token compatibility verified, WCAG 2.1 AA met on all platforms, platform-specific accessibility met                                                                                                                                                                                                              |
| 3   | Architecture -- all UML/ADR/TSD standards upheld                            | CTO + CIO          | Technology Decision Registry 100% compliant per platform, no ADR deviations                                                                                                                                                                                                                                                                                                      |
| 4   | Security -- SRD enforced, all platform security controls effective          | CSO                | All security controls present AND effective on all platforms, cross-platform auth parity verified, stealthy weakening verified absent                                                                                                                                                                                                                                            |
| 5   | Testing -- 100% automated test pass rate achieved                           | CTO                | DAST passed per platform, per-platform performance benchmarks passed, cross-platform parity greater than or equal to 95%                                                                                                                                                                                                                                                         |
| 6   | Localisation -- all platforms, all languages complete                       | CTO-L              | BLEU greater than or equal to 0.80, cross-platform string parity verified, accessibility labels localized on all platforms                                                                                                                                                                                                                                                       |
| 7   | Deployment -- all platforms ready per Multi-Platform Strategy ADR field #16 | CTO + CPO          | Release coordination strategy validated (staggered: backend → web → mobile OR simultaneous: all platforms). Per-platform go/no-go confirmed. Rollback procedure tested. Web: Vercel deploy + CDN + DNS + SSL verified. Mobile: App Store + Google Play submitted + listings verified. Backend: API gateway live + sandbox verified. Parity ≥ 95% confirmed across all platforms. |

**Gate Criteria:**

1. All 7 checklist items signed off (per-platform)
2. User has issued the final release decision

**Defect Handling:** P0/P1 defects block release on any platform. P2/P3 defects -- user has explicit final authority to fix before release or defer to post-launch.

---

**Monitoring system:** `monitoring.md` -- Full-Stack Cross-Platform Pipeline monitoring system (three-layer: PROGRESS.md, session logs, checkpoint JSON).
