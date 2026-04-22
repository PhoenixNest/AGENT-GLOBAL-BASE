# Full-Stack Cross-Platform Pipeline — Delta Overlay

| Field          | Value                                                                                                                                                                              |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pipeline**   | `full-stack`                                                                                                                                                                       |
| **Owner**      | VP Web (Julia Thorne) + VP API (Alex Rivera) + Cross-Platform Lead (Mei-Ling Johansson) — meta-pipeline coordinated jointly                                                        |
| **Surfaces**   | Coordinated multi-platform delivery across web + iOS + Android + backend API as a unified product — selectable per-project via the 3-scenario Multi-Platform Strategy Matrix below |
| **Effective**  | 2026-04-21                                                                                                                                                                         |
| **Supersedes** | `full-stack/pipeline.md` (legacy 446-line file; back-compat redirect retained until 2026-07-21).                                                                                   |
| **Cross-Refs** | Base: [`../_base/pipeline.md`](../_base/pipeline.md) · Template: [`../_base/delta-template.md`](../_base/delta-template.md)                                                        |

> **Reading order.** This delta is consumed _alongside_ [`../_base/pipeline.md`](../_base/pipeline.md), not instead of it. The base defines the universal 12-stage state machine, defect severity, Progress Sync Protocol, gate criteria, and the Release Readiness Checklist. This delta fills the `{{DELTA: …}}` placeholders the base reserves for full-stack-cross-platform-specific content — which is _orchestration on top of_ the per-platform deltas (mobile / web / backend), not a replacement for them. Anything in the base applies; anything contradicted by this delta IS A BUG — escalate to the Software Architect.
>
> **Meta-pipeline note.** Full-stack is unique among deltas: it is a **meta-pipeline** that orchestrates coordinated delivery across [`../mobile-development/delta.md`](../mobile-development/delta.md), [`../web-development/delta.md`](../web-development/delta.md), and [`../backend-api/delta.md`](../backend-api/delta.md). It does **not** replace those per-platform deltas — it sits above them and adds cross-platform orchestration concerns (release coordination, parity verification, shared data models, unified auth, design-token pipeline). When a project chooses `full-stack`, it activates this delta **plus** the relevant per-platform deltas in tandem. The base + full-stack delta + per-platform deltas together produce the derived view.

---

## 1. Surface / Multi-Platform Strategy Matrix

### 1.1 Overview

Stage 5 development executes per the **Multi-Platform Strategy Matrix**, which determines track activation based on the **Multi-Platform Strategy ADR** produced at Stage 3. The Stage 1 gate asks "Which platforms?" — this confirms the **target platform combination**. The **implementation approach per platform** is locked at **Stage 3** (and inherits from each per-platform delta).

**Three mutually exclusive scenarios — a project selects exactly one.**

### 1.2 Decision Matrix

| Dimension                 | Full Product (web + mobile + API) | Web + API Only (no mobile)  | Mobile + API Only (no web)      |
| ------------------------- | --------------------------------- | --------------------------- | ------------------------------- |
| **Stage 1 Gate**          | All platforms                     | Web + API                   | Mobile + API                    |
| **Stage 3 ADR**           | Multi-platform (all 3)            | Web + backend               | Mobile + backend                |
| **Stage 5 Active Tracks** | FS-WFE + FS-WBE + FS-MOB + FS-INT | FS-WFE + FS-WBE + FS-INT    | FS-MOB + FS-WBE + FS-INT        |
| **Stage 5 Team Size**     | 17–23                             | 9                           | 12–18                           |
| **Stage 6 Tier 1 Review** | All leads cross-review            | Web ↔ Backend               | Mobile ↔ Backend                |
| **Stage 7 Testing**       | All platform tests + parity       | Web + backend E2E           | Mobile + backend E2E            |
| **Stage 10 Submission**   | All platforms simultaneously      | Web deployed + backend live | Mobile submitted + backend live |
| **CI/CD Scope**           | All platform CI/CD + parity       | Web + backend CI            | Mobile + backend CI             |

### 1.3 Track Activation Protocol

| Scenario                   | FS-WFE (Web Frontend) | FS-WBE (Web Backend) | FS-MOB (Mobile)           | FS-INT (Integration) | Coordinator                        |
| -------------------------- | --------------------- | -------------------- | ------------------------- | -------------------- | ---------------------------------- |
| Full product               | **FULL** (4 eng)      | **FULL** (3 eng)     | Per mobile ADR (7–13 eng) | **FULL** (3 eng)     | Elena Vasquez + Mei-Ling Johansson |
| Web + API only (no mobile) | **FULL** (4 eng)      | **FULL** (3 eng)     | **Dormant**               | **LIGHT** (2 eng)    | Elena Vasquez                      |
| Mobile + API only (no web) | **Dormant**           | **FULL** (3 eng)     | Per mobile ADR (7–13 eng) | **LIGHT** (2 eng)    | Mei-Ling Johansson                 |

**Track semantics:**

| Term        | Definition                                                                                                               |
| ----------- | ------------------------------------------------------------------------------------------------------------------------ |
| **FULL**    | End-to-end feature implementation, testing, and delivery for that platform. Owns complete codebase for that platform.    |
| **LIGHT**   | Integration and adaptation only (e.g., API consumer wiring, platform channel handlers). NOT full feature implementation. |
| **PRIMARY** | Owns the shared integration layer. Coordinates cross-platform contracts, shared data models, and release timing.         |
| **Dormant** | Track lead and engineers are reassigned to technical debt, test automation, cross-training, or other pipeline projects.  |

### 1.4 Resource Reallocation Protocol

| Scenario                   | Freed Resources           | Reassignment Options                                              |
| -------------------------- | ------------------------- | ----------------------------------------------------------------- |
| Full product               | None — all tracks active  | N/A                                                               |
| Web + API only (no mobile) | All mobile eng (7–13 eng) | Other mobile projects, mobile test automation, SDK migration prep |
| Mobile + API only (no web) | All web FE eng (4 eng)    | Other web projects, web test automation, design system updates    |

### 1.5 Monitoring Adaptation

`PROGRESS.md` must reflect active tracks only. Inactive tracks show "N/A," not "0%". The Progress Sync Protocol must account for reallocated resources — reassigned engineers should not penalize a project's capacity metrics.

### 1.6 Per-Scenario CI/CD Blueprint

| CI/CD Component       | Full Product                                                      | Web + API Only                  | Mobile + API Only            |
| --------------------- | ----------------------------------------------------------------- | ------------------------------- | ---------------------------- |
| Web Frontend CI       | ESLint, TSC, Vitest, Playwright                                   | ESLint, TSC, Vitest, Playwright | N/A                          |
| Mobile CI             | Per mobile Platform Strategy                                      | N/A                             | Per mobile Platform Strategy |
| Backend CI/CD         | build, test, contract, load                                       | build, test, contract, load     | build, test, contract, load  |
| Cross-platform E2E CI | Playwright (web) + Maestro/Appium (mobile) against shared staging | N/A                             | N/A                          |
| Parity CI             | Automated comparison of feature coverage across platforms         | N/A                             | N/A                          |
| Integration CI        | Shared API contract tests consumed by all frontend platforms      | Shared API contract tests       | Shared API contract tests    |
| Deployment            | Coordinated — backend first, then web + mobile simultaneously     | Backend first, then web         | Backend first, then mobile   |

---

## 2. Stage 1 — PRD Stewardship (full-stack-specific)

- **PRD steward:** **VP Web (Julia Thorne) + VP API (Alex Rivera) — joint primary**, with **CPO arbitration** for any feature whose scope touches mobile (CPO retains veto on mobile-facing PRD sections, and arbitrates VP-VP deadlocks).
- **Stage 1 surface question (delta-fills the base placeholder):** "Which target platforms?" (web, iOS, Android, API — confirm all combinations upfront). A second confirmation: "Which API consumer types?" (web frontend, mobile apps, third-party integrations) — drives the cross-platform contract security baseline. This delta's gate is _stricter_ than the per-platform deltas because changing platform mix mid-flight is the single most common Stage-1→Stage-3 escape hatch and must be closed at Stage 1.
- **Cross-platform PRD fields (delta-additive over per-platform PRD fields):** per-platform performance SLA targets stated together for comparability (web: LCP/INP/CLS; mobile: cold start, fps, crash-free; backend: P99/uptime); release-coordination preference declared at Stage 1 (staggered vs. simultaneous); cross-platform feature-parity expectations declared (Tier-A features must reach 100% parity; Tier-B features may legitimately diverge per platform constraint).
- **Cross-platform SRD fields (delta-fills the base placeholder):** unified auth flow with cross-platform session management; token revocation propagation across platforms; data synchronization security; API contract security verification across all consuming platforms; per-platform security baselines stated together (iOS ATS, Android Keystore, web CSP/cookies); shared threat model covering cross-platform attack vectors (attacker pivots to weakest platform).

---

## 3. Stage 2 — Prototype Variant (full-stack-specific)

- **Prototype format (delta-fills the base placeholder):** the **cross-platform design package** — web prototype (production-grade HTML/CSS/JS at 3 breakpoints) **+** mid-fidelity iOS wireframes covering all critical screens with platform-specific navigation patterns **+** mid-fidelity Android wireframes covering the same **+** API specification (OpenAPI/Swagger or GraphQL SDL) with sample responses **+** developer-portal low-fidelity prototype (documentation layout, interactive explorer, onboarding flow). All five artifacts are required for the Stage-2 gate to close on a full-product project; per-platform-only scenarios drop the inactive surfaces.
- **IDS surface coverage (delta-additive over per-platform IDS):** the IDS **must** be cross-platform — it covers all active platforms in a single document. **Design Token Compatibility Matrix** mandatory (CSS custom properties → iOS UIColor / Android ColorRes mapping). Per-platform accessibility specifications stated together (web: WCAG 2.1 AA + screen-reader methodology; iOS: VoiceOver + Dynamic Type + switch access; Android: TalkBack + font scaling). Animation specs per platform; gesture vocabulary per platform; cross-platform navigation parity matrix — i.e., for each PRD feature, where each platform's navigation diverges and the rationale.

---

## 4. Stage 3 — Additional Mandatory ADRs (full-stack-specific)

In addition to the universal **String Key Taxonomy ADR** and **Security Architecture ADRs** mandated by the base — and in addition to the per-platform ADRs inherited from each active per-platform delta:

### 4.1 Multi-Platform Strategy ADR (mandatory for every full-stack project) — 16 fields

The Multi-Platform Strategy ADR **supersedes per-platform Strategy ADRs** for full-stack projects (it absorbs each per-platform Strategy ADR's choice and adds cross-platform coordination):

1. **Decision statement** — Which platforms? (web + iOS + Android? web + Android only? etc.)
2. **Web approach** — SSR vs. CSR vs. PWA (inherits from web delta)
3. **Mobile approach** — Native vs. KMP vs. Flutter (inherits from mobile delta)
4. **Backend approach** — Shared API vs. per-platform APIs (inherits from backend delta)
5. **Rationale** — Market needs, team skills, time-to-market.
6. **Trade-offs** — Development speed vs. platform parity vs. cost.
7. **Team capability assessment** — All leads available?
8. **Risk analysis** — Coordination overhead, platform divergence, release timing.
9. **TCO projection (24-month)** — All platforms combined; total estimated cost.
10. **Vendor lock-in risk matrix** — Per-platform + overall.
11. **Performance SLA alignment** — Per-platform thresholds (web: LCP/CLS; mobile: cold start/fps; backend: P99/uptime).
12. **Security mandate** — Unified auth, data protection, platform-specific hardening.
13. **STRIDE threat model** — Cross-platform attack surface (attacker-pivots-to-weakest-platform model).
14. **Track activation mapping** — All four tracks (FS-WFE, FS-WBE, FS-MOB, FS-INT).
15. **Reassignment plan** — For dormant tracks.
16. **Release coordination** — Which platform launches first? Staggered or simultaneous?

**Ownership:** CTO authors. All platform leads (Frontend, Backend, Mobile) provide input. CIO reviews for technology conformance. CSO reviews for security conformance. CDO reviews for design quality impact. The ADR is versionable + supersedable per [`../_base/adr-template.md`](../_base/adr-template.md); supersession requires a documented rollback plan and triggers an Implementation-Plan re-baseline (Stage 4 re-entry minimum).

### 4.2 Cross-Platform Coordination ADRs (full-stack-specific, beyond per-platform canon)

- `ADR-FEATURE-FLAGS.md` — Cross-platform feature-flag governance: unified flag strategy (LaunchDarkly / Unleash), per-platform flag synchronization, kill-switch protocol, staggered-rollout coordination, environment parity (dev/staging/prod flags must match across platforms).
- `ADR-API-CLIENT-GENERATION.md` — Shared API-client generation strategy: OpenAPI Generator vs. Swagger Codegen vs. manual; client-SDK consistency enforcement across web/iOS/Android; version synchronization; breaking-change detection.
- `ADR-DESIGN-TOKEN-PIPELINE.md` — Design-token pipeline: token generation tool (Style Dictionary / Figma Tokens / custom); versioning; drift detection across platforms; design-to-code synchronization; per-platform token mapping (CSS custom properties → iOS UIColor / Android ColorRes).
- `ADR-SECURITY-CROSS-PLATFORM.md` — Unified auth flow with cross-platform session management; token revocation propagation; cross-platform data protection; platform-specific hardening matrix (so the weakest platform cannot be used as a pivot).

The per-platform security ADRs (`ADR-SECURITY-WEB-PATTERNS.md`, `ADR-SECURITY-MOBILE-PATTERNS.md`, `ADR-SECURITY-WEB-STORAGE.md`, `ADR-SECURITY-MOBILE-STORAGE.md`) remain mandatory and are inherited from each active per-platform delta. The cross-platform ADR sits **above** them and resolves any platform-vs-platform inconsistency.

---

## 5. Stage 4 — Pipeline-Specific Plan Sections

### 5.1 Cross-Platform Implementation Plan (mandatory)

The Implementation Plan covers all active tracks (FS-WFE, FS-WBE, FS-MOB, FS-INT) with explicit task assignments per track. Shared data models, API contracts, and unified-auth flow are first-class plan sections. Inactive tracks per scenario are explicitly marked dormant in the plan (not omitted — visibility is required so reassignment-plan auditing is auditable).

### 5.2 Release Coordination Plan (mandatory at Stage 4)

Defines staggered vs. simultaneous launch (per Multi-Platform Strategy ADR field 16); per-platform go/no-go authority; rollback procedure; cross-platform smoke-test ordering post-deploy; and the abort criteria for partial releases (e.g., backend-live-but-mobile-rejected scenario).

### 5.3 Cross-Platform RTM (mandatory)

The Requirements Traceability Matrix is **per-platform per-requirement** — every PRD requirement must have a row per active platform showing which Implementation Plan task implements it on that platform, or an explicit "N/A — not in scope on this platform" entry signed off by the CPO.

### 5.4 Cross-Platform Test Architecture Document (mandatory)

The TAD covers all platform test suites **plus** cross-platform E2E flows **plus** parity tests. Cross-platform E2E orchestration tooling (Playwright for web, Maestro/Appium for mobile, against a shared staging backend) is named in the TAD.

### 5.5 Cross-Platform SIS (mandatory) — full-stack-specific patterns

Translates SRD into cross-platform code patterns — (1) Web: XSS, CSRF, CSP, cookie security, SRI; (2) Mobile: certificate pinning, secure storage, root/jailbreak detection, App Attest / Play Integrity; (3) Backend: rate limiting, input validation, authZ, encrypted DB at rest, TLS 1.3; (4) **Cross-platform** (full-stack-only): unified auth flow with cross-platform session management; token-revocation propagation across platforms; data-synchronization security guarantees; API contract security verification across all consuming platforms; shared threat model covering cross-platform attack vectors.

---

## 6. Stage 5 — Track Execution Model (full-stack-specific)

**Lead coordinator:** **VP Web (Julia Thorne) + VP API (Alex Rivera)** for product / web + backend integration; **VP W&B (Elena Vasquez)** for cross-track engineering coordination of FS-WFE / FS-WBE / FS-INT; **Cross-Platform Lead (Mei-Ling Johansson)** for FS-MOB track coordination per the Mobile Platform Strategy ADR.

**Track execution:**

- **Track FS-WFE (Web Frontend):** inherits engineering execution from [`../web-development/delta.md`](../web-development/delta.md) Track W-FE. FULL for full-product and web+API; dormant for mobile+API.
- **Track FS-WBE (Web Backend):** inherits engineering execution from [`../backend-api/delta.md`](../backend-api/delta.md) Track B-API + B-DATA. FULL for all three full-stack scenarios.
- **Track FS-MOB (Mobile):** inherits engineering execution from [`../mobile-development/delta.md`](../mobile-development/delta.md) (its own Mobile Platform Strategy Matrix applies underneath this delta). FULL for full-product and mobile+API; dormant for web+API.
- **Track FS-INT (Integration — full-stack-only):** Led by VP W&B (Elena Vasquez). PRIMARY in all full-stack scenarios. Owns the shared API client / design-token pipeline / shared-state synchronization layer that wires the platforms together. **This track does not exist in any per-platform delta — it is the irreducible additive scope of the full-stack meta-pipeline.**

**Cross-platform contract verification:** The **Cross-Platform Contract Report** (`CROSS-PLATFORM-CONTRACT-REPORT.md`) is the full-stack-specific equivalent of the per-platform Pact contract reports — API parity is verified across **all** consuming platforms (web frontend, iOS, Android, third-party integrations). Produced at 30% and 70% milestones.

**Unified String Extraction Readiness audit:** unlike per-platform deltas, full-stack runs a **single unified key-index.csv** spanning all platforms. The audit verifies cross-platform string parity — every translatable string used on more than one platform shares one key.

**Design Fidelity Checkpoint scope:** the checkpoint runs **per platform in parallel** at ~60% completion. ≥ 90% pass on **all platforms** to proceed. 70–89% on **any** platform with a documented remediation plan. < 70% on **any** platform STOPS — CTO notifies CPO.

**Additional Full-Stack Stage-5 gate criteria (delta-fills the base placeholder):**

- [ ] Cross-Platform Contract Report (`CROSS-PLATFORM-CONTRACT-REPORT.md`) produced — API parity verified across all platforms.
- [ ] String Extraction Readiness audit completed — unified `key-index.csv` parity verified across platforms; remaining hardcoded strings ≤ 5% per platform.
- [ ] Design Fidelity Checkpoint passed at ~60% per platform per the thresholds above.

---

## 7. Stage 6 — Tier-1 Review Model (full-stack-specific)

**Tier-1 cross-review pairing (delta-fills the base placeholder):**

- **Full product:** **all platform leads cross-review** — Frontend Lead, Backend Lead, Mobile Lead each review the other two's boundaries; VP Web + VP API serve as advisors.
- **Web + API only:** Frontend Lead ↔ Backend Lead cross-review.
- **Mobile + API only:** Mobile Lead ↔ Backend Lead cross-review.

**Live Demonstration scope (delta-fills the base placeholder):** **Cross-Platform Live Demonstration** — CDO interacts with critical user flows on **each** active platform (web on staging; iOS on simulator/device; Android on emulator/device). For every PRD feature, the same scenario is exercised on each platform and behavior is compared side-by-side. Responsive / adaptive check at all breakpoints and screen sizes. Per-platform live accessibility test (web: keyboard + screen reader; iOS: VoiceOver; Android: TalkBack).

**Cross-Platform Conformance Matrix (mandatory at Stage 6):** ≥ 95% feature parity across platforms is the gate. Per-feature deviation requires either (a) a Tier-B feature classification from Stage 1, or (b) an architecture-compliance memo from Dr. Elena Rostova explaining why platform divergence is structural and not avoidable.

**Three-Layer Defense for ADR/TSD compliance (delta-additive):**

- **Layer 1:** all platform leads attest their implementations conform to locked Stage-3 ADRs and TSD selections.
- **Layer 2:** Dr. Elena Rostova conducts an independent **cross-platform** audit of ADR/TSD compliance and produces a written audit memo.
- **Layer 3:** CI/CD gates passed per platform — dependency version pinning, prohibited-technology detection, security ADR compliance.

---

## 8. Stage 7 — Platform-Specific Testing Mandates (full-stack-specific)

Delta-fills the base's `{{DELTA: pipeline-specific Stage 7 testing mandates}}`. The full-stack delta does **not** re-state per-platform test mandates — those are inherited from the active per-platform deltas. It **adds** the following cross-platform-only mandates:

- **Cross-platform E2E tests:** the same critical user journey is executed on web (Playwright) **and** mobile (Maestro/Appium) against a shared staging backend. Stage-7 gate: 100% pass.
- **Parity test:** automated comparison of feature coverage and behavioral equivalence across platforms. Stage-7 gate: ≥ 95% parity.
- **Pact contract tests:** 100% endpoint coverage from each consumer (web, iOS, Android) against the backend provider.
- **Cross-platform performance comparison:** per-platform SLAs are tested independently per per-platform delta; full-stack adds a comparative report so any platform that regresses far below another for the same flow is flagged.
- **OWASP penetration-testing track (delta-fills the base placeholder):** OWASP WSTG (web) **+** MASVS (mobile) **+** OWASP API Security Top 10 (backend) — all three must pass with zero critical/high findings. **Cross-platform pen test addition:** an attacker scenario where a token issued via the weakest platform is used to attack the strongest platform; failure is **P0**.
- **DAST:** OWASP ZAP per platform; aggregated cross-platform ZAP report at Stage 7.
- **Cross-platform accessibility audit:** WCAG 2.1 AA ≥ 95% on all platforms (web: axe-core + screen reader; iOS: VoiceOver manual; Android: TalkBack manual; backend: developer-portal screen-reader test).

**Regression testing model — cross-platform matrix (delta-fills the base placeholder):**

| Trigger     | Full-stack-specific scope                                                                                                                             |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Per-PR      | Per-platform per-PR per the relevant per-platform delta + shared API contract verification.                                                           |
| Nightly E2E | Per-platform nightly suites + cross-platform E2E (Playwright web + Maestro/Appium mobile against shared staging) + parity test + cross-platform DAST. |

---

## 9. Stage 8 — Additional Integrity Checks (full-stack-specific)

Delta-fills the base placeholder for additional Stage-8 product-specific integrity checks:

- **Stealthy weakening — cross-platform watch-list:** in addition to the per-platform watch-lists (inherited from each per-platform delta), a full-stack project also flags **inconsistent auth enforcement across platforms** and **weaker security on one platform vs. others** (because attackers pivot to the weakest platform). Any such cross-platform divergence since Stage 6 is classified as **P0 defect**.
- **Cross-platform parity re-verification:** parity ≥ 95% must be maintained — Stage-8 re-runs the parity test against the Stage-6 baseline; any regression is a **P1 defect** until parity is restored. **Functionality removal is never a valid remediation.**
- **Per-feature PRD checklist:** every PRD requirement verified as implemented and tested on all in-scope platforms (per-platform "N/A — not in scope" rows from the Stage-4 RTM are honored only if CPO-signed).
- **Analytics-integrity verification:** all PRD-mandated analytics events firing correctly on **all** platforms (per-platform analytics drift is a P1 defect).

---

## 10. Stage 10 — Additional Release Criteria (full-stack-specific)

Delta-fills the base placeholder for additional Stage-10 product-specific release criteria. The full-stack release checklist is the **superset** of the per-platform release checklists, _plus_ the following cross-platform-only items:

- **Release coordination strategy validated** per Multi-Platform Strategy ADR field 16 — staggered (backend → web → mobile) **or** simultaneous (all platforms). Per-platform go/no-go confirmed independently. Rollback procedure tested cross-platform.
- **Per-platform deployment sub-checklists confirmed:**
  - **Web:** Vercel deploy + CDN + DNS + SSL verified (per [`../web-development/delta.md`](../web-development/delta.md)).
  - **Mobile:** App Store + Google Play submitted + listings verified (per [`../mobile-development/delta.md`](../mobile-development/delta.md)).
  - **Backend:** API gateway live + sandbox verified + status page live (per [`../backend-api/delta.md`](../backend-api/delta.md)).
- **Parity ≥ 95% confirmed across all platforms** at the moment of release.
- **Unified analytics live on all platforms** — events firing through the same instrumentation pipeline; cross-platform cohort analysis viable on Day 1.
- **Cross-platform smoke tests post-deploy:** within 5 minutes of release, the cross-platform E2E smoke suite runs against production; on failure, automatic per-platform rollback per the Stage-4 release-coordination plan.

---

## 11. Stage 11 — Live Ops Mandates (full-stack-specific)

Delta-fills the base placeholder for product-specific live-ops mandates:

- **Per-platform SLOs apply** as stated in each per-platform delta (web Vitals; mobile crash-free / cold start / fps; backend P99 / uptime / error rate).
- **Cross-platform parity SLO:** 7-day rolling parity ≥ 95%; any platform that drifts opens a P1 ticket.
- **Cross-platform release-cadence policy:** new features ship on every platform within the same release window unless explicitly deferred per Tier-B classification at Stage 1.
- **Token-revocation propagation SLO:** when a session is revoked (logout, password change, security event), revocation must propagate to all consuming platforms within 60 seconds. Beyond 60s = P1 incident.
- **Cross-platform incident escalation:** any incident affecting two or more platforms simultaneously auto-escalates to the C-suite (CTO + CPO + CSO) within 15 minutes of detection.

---

## 12. Cross-Cutting i18n Requirements

i18n is a continuous concern from Stage 2 onward. Full-stack-specific application is **unification** — every per-platform i18n requirement is in scope, plus the cross-platform unification:

| Stage   | Full-stack i18n requirement                                                                                                                                                                                                                                                                                                           |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 1 | PRD declares target locales **once**; locale list locked **across all platforms**; per-platform locale-availability differences (e.g., a locale supported on web but not mobile) called out explicitly with rationale.                                                                                                                |
| Stage 2 | Pseudo-localized strings injected into web prototype + mid-fi mobile wireframes annotated with text-expansion tolerance; cross-platform IDS includes RTL layout mirroring rules per platform; design-token compatibility verified across locales.                                                                                     |
| Stage 3 | String Key Taxonomy ADR uses the canonical `{feature}.{screen}.{component}.{property}` shape; **single unified `key-index.csv`** is the canonical source for all platforms; per-platform string registries (Localizable.strings / strings.xml / messages.json) are generated from the unified registry, never authored independently. |
| Stage 5 | Locale-aware components from first commit on every platform. Zero-hardcoded-strings rule enforced by CI on every PR per platform. Per-platform locale-resolution APIs honored (web `Intl`; iOS `Locale`; Android `Locale`). Unified key-index.csv parity verified weekly.                                                             |
| Stage 7 | Per-platform pseudo-locale screenshot regression + cross-platform parity test verifying the same string key renders correctly on every platform.                                                                                                                                                                                      |
| Stage 9 | Translation accuracy only. CTO-L issues unified Translation Verification Report (BLEU ≥ 0.80 per language; placeholder integrity verified across all platforms; cross-platform string parity verified).                                                                                                                               |

---

## 13. Document Version History

| Version | Date           | Author                                                                      | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------- | -------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0.1     | April 21, 2026 | Software Architect + VP Web + VP API + Cross-Platform Lead + VP W&B (joint) | Initial overlay. Full-stack cross-platform-specific content (3-scenario Multi-Platform Strategy Matrix, Tracks FS-WFE / FS-WBE / FS-MOB / FS-INT activation, Multi-Platform Strategy ADR 16-field requirement, cross-platform coordination ADRs, full-stack-specific Stage 1/2/3/4/5/6/7/8/10/11 sections, unified i18n table) extracted from the legacy `full-stack/pipeline.md` (446 lines). Pairs with [`../_base/pipeline.md`](../_base/pipeline.md) **and** the three per-platform deltas (mobile / web / backend) to produce a derived view equivalent to the legacy file. Full-stack is unique among deltas — it is a **meta-pipeline** that orchestrates per-platform deltas; this delta defines only the additive cross-platform orchestration scope (Track FS-INT, Multi-Platform Strategy ADR, Cross-Platform Contract Report, Cross-Platform Live Demonstration, Cross-Platform Conformance Matrix, parity tests, release coordination, cross-platform stealthy-weakening watch-list, unified i18n key-index.csv). |
