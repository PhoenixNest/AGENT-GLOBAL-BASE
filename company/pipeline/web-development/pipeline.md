# Web Application Pipeline

## Overview

The company's web application development workflow is a thirteen-stage state machine (Stages 0–11, with Stage 9.5 between Stage 9 and Stage 10). At each stage you are required to log the current execution phase and update the workflow's progress. Each stage follows a consistent schema: **Relevant Personnel**, **Artifacts In**, **Artifacts Out**, a designated **Responsible Producer**, explicit **Reviewers**, **Gate Criteria** that must be satisfied before the stage closes, and **Defect Handling** where applicable.

Each workflow must be assigned to a designated responsible party. Each assigned individual is regarded as a "Subagent"; as the primary "Agent," you must collaborate with these Subagents — leveraging their respective skill sets — to successfully complete every task within the workflow.

> **Behavioural Constraints:** All agents operating in this pipeline must comply with the forbidden behaviours and required declarations defined in [`company/pipeline/_base/agent-behavioral-constraints.md`](company/_base/agent-behavioral-constraints.md).

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

## Web Strategy Matrix

### Overview

Stage 5 development executes per the **Web Strategy Matrix**, which determines track activation based on the **Web Strategy ADR** produced at Stage 3. The Stage 1 gate asks "What type of web application?" — this confirms the **target delivery model** (PWA, SPA, SSR). The **implementation approach** (SSR vs CSR vs PWA vs hybrid) is an architecture decision locked at **Stage 3**.

**Four mutually exclusive scenarios — a project selects exactly one.**

### Decision Matrix

| Dimension                 | Frontend-Heavy (SPA/Dashboard)  | Backend-Heavy (Data Platform)   | Full-Stack (E-commerce/Social) | Lightweight (Landing Page) |
| ------------------------- | ------------------------------- | ------------------------------- | ------------------------------ | -------------------------- |
| **Stage 1 Gate**          | Web app                         | Web API                         | Web app + API                  | Web app                    |
| **Stage 3 ADR**           | SSR/CSR/PWA decision            | REST/GraphQL decision           | SSR + REST + deployment        | CSR only                   |
| **Stage 5 Active Tracks** | Track W-FE + Track W-FS         | Track W-BE + Track W-FS         | Track W-FE + W-BE + W-FS       | Track W-FE only            |
| **Stage 5 Team Size**     | 8                               | 8                               | 12                             | 4                          |
| **Stage 6 Tier 1 Review** | Frontend ↔ Backend cross-review | Backend ↔ Frontend cross-review | All three leads cross-review   | Frontend Lead only         |
| **Stage 7 Testing**       | FE unit + E2E + perf            | BE unit + contract + load       | Full-stack E2E + all platforms | FE unit + basic E2E        |
| **Stage 10 Submission**   | Vercel deploy + CDN             | API gateway + docs              | Full deployment + docs         | Vercel deploy              |
| **CI/CD Scope**           | Frontend + deploy               | Backend + contract              | Full-stack CI/CD               | Frontend CI only           |

### Track Activation Protocol

| Project Type   | Track W-FE (Web Frontend) | Track W-BE (Web Backend) | Track W-FS (Full-Stack Integration) | Coordinator                      |
| -------------- | ------------------------- | ------------------------ | ----------------------------------- | -------------------------------- |
| Frontend-heavy | **FULL** (4 eng)          | **LIGHT** (2 eng)        | **LIGHT** (2 eng)                   | Elena Vasquez (VP Web & Backend) |
| Backend-heavy  | **LIGHT** (2 eng)         | **FULL** (4 eng)         | **LIGHT** (2 eng)                   | Elena Vasquez (VP Web & Backend) |
| Full-stack     | **FULL** (4 eng)          | **FULL** (4 eng)         | **PRIMARY** (4 eng)                 | Elena Vasquez + Amira Voss       |
| Lightweight    | **LIGHT** (2 eng)         | Dormant                  | **LIGHT** (2 eng)                   | Elena Vasquez (VP Web & Backend) |

**Track semantics:**

| Term        | Definition                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------- |
| **FULL**    | End-to-end feature implementation, testing, and delivery for that layer. Owns the complete codebase for that layer. |
| **LIGHT**   | Integration and adaptation only (e.g., API client integration, deployment wiring). NOT full feature implementation. |
| **PRIMARY** | Owns the shared integration layer that connects frontend and backend. Coordinates cross-layer contracts.            |
| **Dormant** | Track lead and engineers are reassigned to technical debt, test automation, cross-training, or other projects.      |

### Track W-FE/W-BE — How Semantics Change

When the user chooses a project type that shifts track responsibility:

| Aspect         | FULL Track            | LIGHT Integration Track                        |
| -------------- | --------------------- | ---------------------------------------------- |
| Code ownership | 100% of layer code    | Integration wiring only                        |
| Feature work   | Full implementation   | Integration of other layer's APIs              |
| Team size      | 4 engineers           | 2 engineers                                    |
| Freed capacity | N/A                   | Reassigned to technical debt / test automation |
| CI/CD          | Full layer pipeline   | Integration build + contract verification      |
| Testing        | Full layer test suite | Contract tests + integration tests             |

### Resource Reallocation Protocol

| Scenario       | Freed Resources                      | Reassignment Options                                                   |
| -------------- | ------------------------------------ | ---------------------------------------------------------------------- |
| Frontend-heavy | 2 W-BE eng, 2 W-FS eng               | Other projects, API contract tests, CI/CD hardening                    |
| Backend-heavy  | 2 W-FE eng, 2 W-FS eng               | Other projects, frontend test automation, performance profiling        |
| Full-stack     | None — all tracks active             | N/A                                                                    |
| Lightweight    | 4 W-FE eng, all W-BE eng, 2 W-FS eng | Technical debt, accessibility audit, documentation, SDK migration prep |

### Per-Scenario CI/CD Blueprint

| CI/CD Component    | Frontend-Heavy | Backend-Heavy | Full-Stack | Lightweight |
| ------------------ | -------------- | ------------- | ---------- | ----------- |
| ESLint + TSC       | ✅             | ✅ (BE only)  | ✅         | ✅          |
| Vitest unit tests  | ✅             | ✅ (BE only)  | ✅         | ✅          |
| Playwright E2E     | ✅             | ❌            | ✅         | Basic       |
| Lighthouse CI      | ✅             | ❌            | ✅         | ❌          |
| API contract tests | ✅ (consumer)  | ✅ (provider) | ✅ (both)  | ❌          |
| k6 load tests      | ❌             | ✅            | ✅         | ❌          |
| ZAP DAST           | ✅             | ✅            | ✅         | ✅          |
| Vercel deploy      | ✅             | ❌            | ✅ (FE)    | ✅          |
| API gateway deploy | ❌             | ✅            | ✅ (BE)    | ❌          |

### Web Strategy ADR Requirements

The mandatory Web Strategy ADR at Stage 3 must include **all 14 fields**:

1. **Decision statement** — Which approach: SSR, CSR, PWA, or hybrid?
2. **Rationale** — Why this approach? (SEO needs, performance targets, team skills, time-to-market)
3. **Trade-offs** — What is gained and sacrificed vs. alternatives?
4. **Team capability assessment** — Do we have the right frontend/backend balance?
5. **Risk analysis** — SSR complexity, bundle size, SEO risks, browser compatibility
6. **TCO projection (24-month)** — Hosting costs, CDN, monitoring, total estimated cost
7. **Vendor lock-in risk matrix** — Framework abandonment risk, migration cost, hosting dependency, hosting platform comparison (Vercel vs Netlify vs self-hosted AWS/CloudFront + S3)
8. **Performance SLA alignment** — LCP (<2.5s), INP (<200ms), CLS (<0.1), TTFB (<800ms) — can the chosen approach meet PRD thresholds?
9. **Accessibility mandate** — WCAG 2.1 AA from Stage 2 IDS, tested in Stage 7
10. **STRIDE-based threat model** — XSS, CSRF, injection, session hijacking, supply chain
11. **Track activation mapping** — Explicit reference to which tracks are FULL, LIGHT, or Dormant
12. **Reassignment plan** — If tracks are dormant or light, where do freed engineers go?
13. **SEO strategy** — Meta tags, sitemap, structured data, SSR rendering for crawlers
14. **Browser support matrix** — Which browsers and versions are supported?

**Ownership:** CTO authors the ADR. Frontend Lead + Backend Lead provide input. CIO reviews for technology conformance. CSO reviews for security conformance. CDO reviews for design quality impact. Once approved at Stage 3 gate, this decision is **locked** — switching between strategies requires a full stage rollback (Stage 3 re-entry, ADR re-authorship, Implementation Plan re-baseline).

### Deployment & Compliance Implications

The Web Strategy ADR must also address:

- **Deployment platform compliance:** Vercel/Netlify terms, AWS region selection, data residency requirements
- **Cookie & privacy compliance:** GDPR cookie consent, CCPA data handling, third-party script governance
- **IAP/monetization implications:** Stripe/Payment gateway integration, revenue share (if applicable), tax compliance

---

## Stage Definitions

### Stage 1: Requirements → PRD + SRD

**Relevant Personnel:** CPO (PRD), CSO (SRD)

**Artifacts In:** Raw product requirements, user research, market analysis

**Artifacts Out:**

- `PRD.md` — Product Requirements Document (with JTBD, kill criteria, commercial assessment, locale formatting)
- `SRD.md` — Security Requirements Document (expanded: XSS prevention, CSRF protection, CSP requirements, OAuth 2.0 session security, data residency, GDPR compliance)

**Reviewers:** CTO, CIO, CSO, CPO

**Gate Criteria:**

1. User has confirmed target delivery model (SPA, SSR, PWA, or hybrid)
2. User has confirmed target browsers (Chrome, Firefox, Safari, Edge)
3. PRD includes performance SLA targets (LCP, CLS, TTFB, TTI)
4. SRD includes web-specific security requirements (XSS, CSRF, CSP)
5. User has confirmed no further revisions are required

**Defect Handling:** P0/P1 defects block Stage 1→2. P2/P3 defects require user decision.

---

### Stage 2: PRD → Web Prototype + IDS

**Relevant Personnel:** CDO, VP Web (Julia Thorne)

**Artifacts In:** PRD, SRD (paired artifacts)

**Artifacts Out:**

- Approved web prototype (production-grade HTML/CSS/JS, not just mock — serves as design validation AND initial frontend scaffold)
- `IDS.md` — Interaction Design Specification (with responsive breakpoints, accessibility specs, text expansion tolerance, RTL considerations, animation specs)

**Reviewers:** CTO, CDO, CPO, VP Web (Julia Thorne)

**Gate Criteria:**

1. Prototype validates functional requirements across all target breakpoints (mobile 375px, tablet 768px, desktop 1440px)
2. IDS includes responsive design specifications for all breakpoints
3. IDS includes WCAG 2.1 AA compliance targets
4. CDO confirms design fidelity to PRD requirements
5. User has given final confirmation

**Defect Handling:** P0/P1 defects block Stage 2→3. P2/P3 defects require user decision.

---

### Stage 3: Web Prototype → UML Engineering Package

**Relevant Personnel:** CTO (UML), CIO (ADRs, TSD)

**Artifacts In:** PRD, SRD, web prototype, IDS

**Artifacts Out:**

- UML diagrams (class, sequence, component, activity)
- 6 mandatory ADRs:
  - `ADR-WEB-STRATEGY.md` — SSR vs CSR vs PWA vs hybrid (14 fields + compliance implications)
  - `ADR-SECURITY-CRYPTO.md` — Cryptography (Web Crypto API, HTTPS, encrypted storage)
  - `ADR-SECURITY-WEB-PATTERNS.md` — XSS prevention, CSRF tokens, CSP, CORS, OAuth 2.0 session security
  - `ADR-SECURITY-WEB-STORAGE.md` — Cookie security (HttpOnly, Secure, SameSite), localStorage/sessionStorage encryption, IndexedDB security
  - `ADR-STRING-KEY-TAXONOMY.md` — String key naming convention, `key-index.csv` operationalization
  - `ADR-SECURITY-WEB-PLATFORM-PATTERNS.md` — Web-specific security patterns: URL routing security (server-side route guards, auth-required deep links), service worker integrity (scope restriction, cache integrity, update strategy), push notification security (VAPID auth, subscription management), PWA security (manifest integrity, install prompt security, origin trials), open redirect prevention, clickjacking protection (X-Frame-Options + frame-ancestors), prototype pollution prevention, Web Share API security, File API sanitization, third-party iframe sandboxing, security headers (X-Content-Type-Options, Referrer-Policy, Permissions-Policy, HSTS)
- `TSD.md` — Technology Selection Document (with Technology Radar, weighted scorecard, vendor risk scoring)

**Reviewers:** CTO, CIO, CPO

**Gate Criteria:**

1. All 6 ADRs authored, reviewed, and approved
2. TSD includes weighted scorecard with at least 2 alternatives per technology decision
3. UML diagrams cover data layer → domain layer → presentation layer → platform adapter layer
4. Web Strategy ADR locked (no changes without Stage 3 re-entry)
5. User has approved the UML Engineering Package

**Defect Handling:** P0/P1 defects block Stage 3→4. P2/P3 defects require user decision.

---

### Stage 4: UML → Coding Implementation Plan

**Relevant Personnel:** CTO

**Artifacts In:** PRD, SRD, UML package, ADRs, TSD

**Artifacts Out:**

- `IMPLEMENTATION-PLAN.md` — Implementation Plan (with task breakdown, dependencies, estimates)
- `RTM.md` — Requirements Traceability Matrix (PRD/SRD → implementation mapping)
- `TEST-ARCHITECTURE-DOCUMENT.md` — Test Architecture Document (unit, integration, E2E, contract, performance, accessibility)
- `GANTT.md` — Gantt Chart (with critical path, milestones, resource allocation)

**Reviewers:** CTO, CPO

**Gate Criteria:**

1. Implementation Plan covers all 3 tracks (W-FE, W-BE, W-FS) with explicit task assignments
2. RTM traces 100% of PRD requirements to implementation tasks
3. Test Architecture Document covers all test types with tools, standards, and coverage targets
4. `key-index.csv` task defined (string extraction preparation)
5. Database migration strategy defined with rollback procedure and zero-downtime migration plan
6. SIS (Security Implementation Specification) completed and CSO-signed, referenced in CI/CD readiness section
7. Progress Sync Protocol thresholds defined (baseline estimates for >20% variance detection)
8. VP Engineering confirms buddy pairings established for all 12/20-score engineers assigned to this project's tracks (see `buddy-system-assignments.md`).
9. User has approved the plan

**Defect Handling:** P0/P1 defects block Stage 4→5. P2/P3 defects require user decision.

---

### Stage 4.1: Security Implementation Specification (SIS)

Before **Stage 5** begins, the security team produces a web-specific SIS:

- **Author:** Security team (Natalia Petrova + James Wright), signed off by CSO
- **Timing:** Completed during **Stage 4**, referenced in CI/CD readiness gate before **Stage 5** Day 1
- **Content:** Translates SRD requirements into web-specific code patterns — XSS prevention (React auto-escaping, DOMPurify for rich content), CSRF token implementation (double-submit cookie pattern), CSP header configuration (strict-dynamic, nonce-based), OAuth 2.0 session security (PKCE, short-lived tokens), dependency vulnerability response, third-party script supply chain governance (SRI hashes, subresource integrity), URL routing security, service worker integrity, push notification security, PWA security, open redirect prevention, clickjacking protection, prototype pollution prevention, security headers (X-Content-Type-Options, Referrer-Policy, Permissions-Policy, HSTS)
- **Gate Criterion:** "SIS completed and CSO-signed" is a **Stage 4**→**Stage 5** gate criterion

---

### Stage 5: Plan → Software Development

**Relevant Personnel:** CTO (oversees), Elena Vasquez (VP Web & Backend — coordinates), Amira Voss (Track W-FE), Dev Malhotra (Track W-BE), Elena Vasquez (Track W-FS)

**Artifacts In:** Implementation Plan, Gantt Chart, RTM, TAD, SIS, ADRs, TSD

**Artifacts Out:**

- Development codebase (web frontend + web backend + integration layer)
- Contract Verification Reports (30% and 70% milestones — API contract parity between frontend and backend)
- String Extraction Readiness audit (Internationalization Specialist audits codebase for hardcoded strings)
- `DEVELOPMENT-LOG.md` — Per-track development logs with phase completions, variance tracking, CTO weekly summaries

**Reviewers:** CTO (internal review only — no panel)

**Gate Criteria:**

1. All Implementation Plan tasks marked complete across all active tracks
2. Design Fidelity Checkpoint passed at ~60% completion (≥90% pass rate → proceed; 70–89% → proceed with remediation plan; <70% → STOP, CTO notifies CPO)
3. String Extraction Readiness audit completed — remaining hardcoded strings ≤5%, classified as P2 (P1 if core user flow affected)
4. Contract Verification Reports produced at 30% and 70% milestones
5. CTO internal review checklist completed:
   - All TypeScript/JavaScript builds pass with zero errors
   - Application runs without errors on staging environment
   - No P0/P1 defects in bug tracker
   - Design Fidelity Checkpoint completed
   - String Extraction Readiness completed
   - API contract parity verified (API-CONTRACT-PARITY-REPORT.md produced)
   - SIS requirements implemented and verified
   - `DEVELOPMENT-LOG.md` current

**Progress Sync Protocol:** Active — any task >20% over estimate triggers CTO → CPO notification.

**Buddy System Tracking:** For any 12/20-score engineers assigned to this project, buddy pairings are tracked in `PROGRESS.md` session logs and checkpoint JSON buddy progress field. 30/60/90-day checkpoints conducted per `buddy-system-assignments.md` protocol.

**Technical Debt Allocation:** 15–20% sprint capacity reserved (calibrated per project: greenfield 20%, mature 15%, inherited up to 30%). Security debt minimum: 5% of total sprint capacity.

---

### Stage 6: Development → Code Review

**Relevant Personnel:** CTO (convenes panel)

**Artifacts In:** Development codebase, Contract Verification Reports, String Extraction Readiness audit, DEVELOPMENT-LOG.md

**Artifacts Out:**

- `DEFECT-REPORT.md` — Defect Report with Architecture Compliance Audit, IDS Conformance Matrix, pre-Tier 1 automated quality gates
- `SIGNOFF.md` — Code Review Sign-off (with Live Demonstration results)

**Reviewers:** CTO (convenes), CPO, CDO, CIO, CSO, Frontend Lead (Amira Voss), Backend Lead (Dev Malhotra), VP Web (Julia Thorne) (advisor)

**Gate Criteria:**

1. Three-Layer Defense for ADR/TSD compliance passed:
   - **Layer 1:** Frontend Lead + Backend Lead attest implementations conform to locked Stage 3 ADRs and TSD technology selections
   - **Layer 2:** Dr. Elena Rostova conducts independent Architecture Compliance Audit, produces written audit memo
   - **Layer 3:** CI/CD gates passed — dependency version pinning, prohibited technology detection, security ADR compliance (CSP headers, XSS patterns)
2. Live Demonstration completed — CDO interacts with running web application on 3 target browsers (Chrome, Firefox, Safari), verifies responsive layout at 3 breakpoints, spot-checks Lighthouse scores; live accessibility testing performed — keyboard navigation exercised on all critical flows, screen reader announcements verified on at least one critical flow (VoiceOver on Safari or NVDA on Firefox), focus management tested on modals and dropdowns
3. IDS Conformance Matrix ≥ 95% — no "Not Implemented" items
4. Architecture Compliance Audit findings addressed or deferred with user approval
5. Pre-Tier 1 automated quality gates passed — ESLint, TSC, Vitest unit tests, Playwright component tests

**Defect Handling:** P0/P1 defects block Stage 6→7. P2/P3 defects submitted to user for fix/defer decision. CTO assigns R&D to remediate. Full review repeats until all panel sign off.

---

### Stage 7: Code Review → Automated Testing

**Relevant Personnel:** CTO (designates R&D personnel), Test Lead (Priscilla Oduya), Test Automation Lead (Rachel Kim)

**Artifacts In:** Code Review Sign-off, Defect Report (with user decisions on P2/P3)

**Artifacts Out:**

- Automated Test Suite (unit, E2E, contract, performance, accessibility, security)
- `TEST-RESULTS-REPORT.md` — Test Results Report (with DAST, performance benchmarks, Design Fidelity Test Checklist)

**Reviewers:** CTO, Test Lead

**Gate Criteria:**

1. 100% automated test pass rate achieved
2. DAST (OWASP ZAP) passed — zero critical/high findings
3. Manual penetration testing (OWASP Web Security Testing Guide — WSTG) passed — zero critical/high findings (reflected/stored/DOM-based XSS, CSRF, SQL injection, IDOR, authentication bypass, session fixation, privilege escalation, open redirect, clickjacking)
4. Performance benchmarks passed — LCP <2.5s, CLS <0.1, TTFB <800ms, TTI <3.8s
5. Accessibility audit passed — WCAG 2.1 AA ≥ 95% (axe-core + manual screen reader test on critical flows using VoiceOver on Safari and NVDA on Firefox)
6. API contract tests passed — 100% endpoint coverage
7. E2E tests passed — all critical user flows (login, checkout, key interactions)
8. Design Fidelity Test Checklist passed — manual protocol authored by CDO
9. Regression testing passed — all Stage 6+ fixed functionalities verified

**Defect Handling:** P0/P1 defects block Stage 7→8. P2/P3 defects submitted to user for fix/defer decision.

---

### Stage 8: Automated Testing → Integrity Verification

**Relevant Personnel:** CTO (convenes panel)

**Artifacts In:** Test Results Report, Defect Report (with user decisions on P2/P3)

**Artifacts Out:**

- Integrity Verification Sign-off reports from each panel member (CPO, CDO, CIO, CSO, Frontend Lead, Backend Lead)

**Reviewers:** CTO (convenes), CPO, CDO, CIO, CSO, Frontend Lead, Backend Lead, VP Web (Julia Thorne) (co-reviewer)

**Gate Criteria:**

1. Stage 6 baseline re-verification — all Stage 6 defects confirmed fixed, no regression
2. Per-feature PRD checklist — each PRD requirement verified as implemented and tested
3. Stealthy weakening detection — no security controls weakened/removed/disabled since Stage 6 (e.g., weaker cipher, relaxed CSP, removed CSRF protection, removed HSTS, downgraded TLS version, weakened cookie SameSite attribute, disabled Subresource Integrity, relaxed CORS policy). Any such change is classified as **P0 defect**.
4. IDS Conformance Matrix re-verified — ≥95% pass rate maintained
5. Analytics integrity verified — all analytics events firing correctly

**Defect Handling:** P0/P1 defects block Stage 8→9. Functionality removal is **never** valid remediation.

---

### Stage 9: Integrity → i18n Engineering

**Relevant Personnel:** CTO-L (leads), Internationalization Specialist (Tomas Dvoracek), Translation Team

**Artifacts In:** Integrity Verification Sign-off, codebase

**Artifacts Out:**

- Localised codebase (all target languages complete)
- `TRANSLATION-VERIFICATION-REPORT.md` — Translation Verification Report (with BLEU/TER scores, platform-specific style guides)

**Reviewers:** CTO-L, CTO

**Gate Criteria:**

1. All target languages translated (EN, ZH, JA, KO, FR at minimum)
2. BLEU score ≥ 0.80 for all languages
3. `key-index.csv` parity verified — all strings extracted into platform resource files
4. Placeholder integrity verified — no broken interpolation
5. Text expansion tolerance verified — no truncation >40% length increase
6. Accessibility labels localized — all ARIA labels, alt text, screen reader content translated
7. Commercial copy localized — marketing text, legal disclaimers, terms of service

**Defect Handling:** P0/P1 defects block Stage 9→10. P2/P3 defects deferred to post-release if CTO-L approves.

---

### Stage 10: i18n → Release Readiness Check

**Relevant Personnel:** CTO (convenes panel), CPO, CDO, CSO, CTO-L, VP Web (Julia Thorne), **User** (final decision)

**Artifacts In:** Localised codebase, Translation Verification Report, all prior stage artifacts

**Artifacts Out:**

- `RELEASE-CHECKLIST.md` — Release Readiness Report (7-item checklist with sub-checklists)
- Release Decision (approved / conditional / rejected)

**Reviewers:** CTO (convenes), CPO, CDO, CSO, CTO-L, VP Web (Julia Thorne) + **User**

**Release Checklist (7 Items):**

| #   | Domain                                                   | Sign-off Authority          | Key Sub-Checks                                                                                                                                                |
| --- | -------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Product — all PRD requirements implemented               | CPO + VP Web (Julia Thorne) | Analytics firing, IAP configured, kill condition monitoring active, post-launch dashboard ready                                                               |
| 2   | Design — all CDO/IDS specifications accurately realised  | CDO                         | IDS Conformance Matrix ≥ 95%, zero "Not Implemented" items, WCAG 2.1 AA met, responsive breakpoints respected, design tokens correct, animation specs matched |
| 3   | Architecture — all UML/ADR/TSD standards upheld          | CTO + CIO                   | Technology Decision Registry 100% compliant, no ADR deviations                                                                                                |
| 4   | Security — SRD enforced, web security controls effective | CSO                         | All security controls present AND effective (XSS prevention, CSRF protection, CSP headers, OAuth 2.0 session integrity), stealthy weakening verified absent   |
| 5   | Testing — 100% automated test pass rate achieved         | CTO                         | DAST passed, performance benchmarks passed, Design Fidelity Test Checklist passed                                                                             |
| 6   | Localisation — all target languages complete             | CTO-L                       | BLEU ≥ 0.80, accessibility labels verified, commercial copy localized, locale variants distinct                                                               |
| 7   | Deployment — Vercel/AWS deployment verified              | CTO + CPO                   | CDN configured, DNS pointing, domain verified, analytics firing, SEO validated, monitoring dashboards live                                                    |

**Gate Criteria:**

1. All 7 checklist items signed off
2. User has issued the final release decision

**Defect Handling:** P0/P1 defects block release. P2/P3 defects — user has explicit final authority to fix before release or defer to post-launch.

---

**Monitoring system:** `monitoring.md` — Web Application Pipeline monitoring system (three-layer: PROGRESS.md, session logs, checkpoint JSON).
