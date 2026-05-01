# Mobile Development Pipeline — Delta Overlay

| Field          | Value                                                                                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Pipeline**   | `mobile-development`                                                                                                                                                                |
| **Owner**      | VP Mobile (Marcus Andersson)                                                                                                                                                        |
| **Surfaces**   | Android (Google Play) + iOS (App Store) — selectable per-project via the 5-scenario Strategy Matrix below                                                                           |
| **Effective**  | 2026-04-21                                                                                                                                                                          |
| **Supersedes** | `mobile-development/pipeline.md` (legacy 453-line file; back-compat redirect retained until 2026-07-21).                                                                            |
| **Cross-Refs** | Base: [`company/pipeline/_base/pipeline.md`](company/pipeline/_base/pipeline.md) · Template: [`company/pipeline/_base/delta-template.md`](company/pipeline/_base/delta-template.md) |

> **Reading order.** This delta is consumed _alongside_ [`company/pipeline/_base/pipeline.md`](company/pipeline/_base/pipeline.md), not instead of it. The base defines the universal 12-stage state machine, defect severity, Progress Sync Protocol, gate criteria, and the Release Readiness Checklist. This delta fills the `{{DELTA: …}}` placeholders the base reserves for mobile-specific content. Anything in the base applies; anything contradicted by this delta IS A BUG — escalate to the Software Architect.

---

## 1. Surface / Platform Strategy Matrix

### 1.1 Overview

Stage 5 development executes per the **Platform Strategy Matrix**, which determines track activation based on the **Platform Strategy ADR** produced at Stage 3. The Stage 1 gate asks "Android, iOS, or both?" — this confirms **target platforms** (where the app ships). The **implementation approach** (how the code is structured) is an architecture decision locked at **Stage 3**.

**Five mutually exclusive scenarios — a project selects exactly one.**

### 1.2 Decision Matrix

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

### 1.3 Track Activation Protocol

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

### 1.4 KMP / Flutter — How Track A/B Semantics Change

When the user chooses KMP or Flutter, Tracks A and B do **not** disappear — they shift from "feature implementation" to "platform integration."

| Aspect         | Native (FULL)            | KMP Integration (LIGHT)                      | Flutter Integration (LIGHT)                   |
| -------------- | ------------------------ | -------------------------------------------- | --------------------------------------------- |
| Code ownership | 100% of platform code    | Thin native adapters only                    | Platform channel handlers only                |
| Feature work   | Full implementation      | Integration of shared module                 | Integration of Flutter engine                 |
| Team size      | 7 engineers              | 2 engineers                                  | 2 engineers                                   |
| Freed capacity | N/A                      | 5 engineers reassigned                       | 5 engineers reassigned                        |
| CI/CD          | Full platform pipeline   | Adapter build + shared module integration    | Platform channel build + Flutter build        |
| Testing        | Full platform test suite | Adapter tests + shared module contract tests | Platform channel tests + Flutter widget tests |

### 1.5 Resource Reallocation Protocol

| Scenario               | Freed Resources                                   | Reassignment Options                                              |
| ---------------------- | ------------------------------------------------- | ----------------------------------------------------------------- |
| Android-only           | iOS Lead + 6 eng, Cross-Platform Lead + 2 eng     | Other projects, internal tooling, CI/CD, test automation          |
| iOS-only               | Android Lead + 6 eng, Cross-Platform Lead + 2 eng | Same as above                                                     |
| KMP Cross-Platform     | 5 Android eng, 5 iOS eng (from FULL teams)        | Other projects, platform-specific test suites, SDK migration prep |
| Flutter Cross-Platform | 5 Android eng, 5 iOS eng                          | Same as above                                                     |

### 1.6 Monitoring Adaptation

`PROGRESS.md` must reflect active tracks only. Inactive tracks show "N/A," not "0%". The Progress Sync Protocol must account for reallocated resources — reassigned engineers should not penalize a project's capacity metrics.

### 1.7 Per-Scenario CI/CD Blueprint

| CI/CD Component        | Android-Only | iOS-Only | Both Native | KMP                      | Flutter            |
| ---------------------- | ------------ | -------- | ----------- | ------------------------ | ------------------ |
| Gradle build           | ✅           | ❌       | ✅          | ✅ (Android target)      | ❌                 |
| Xcode build            | ❌           | ✅       | ✅          | ✅ (iOS target)          | ❌                 |
| Detekt                 | ✅           | ❌       | ✅          | ✅ (shared + Android)    | ❌                 |
| SwiftLint              | ❌           | ✅       | ✅          | ❌                       | ❌                 |
| KMP multi-target       | ❌           | ❌       | ❌          | ✅ (JVM + Android + iOS) | ❌                 |
| Flutter build          | ❌           | ❌       | ❌          | ❌                       | ✅ (Android + iOS) |
| Platform channel tests | ❌           | ❌       | ❌          | ❌                       | ✅                 |
| Firebase Test Lab      | ✅           | ❌       | ✅          | ✅ (Android adapter)     | ❌                 |
| Xcode UI tests         | ❌           | ✅       | ✅          | ✅ (iOS adapter)         | ❌                 |

---

## 2. Stage 1 — PRD Stewardship (mobile-specific)

- **PRD steward:** CPO (Marcus Tran-Yoshida).
- **Stage 1 surface question (delta-fills the base placeholder):** "Android, iOS, or both?" The user's answer determines the Strategy Matrix scenario at Stage 3.
- **Mobile-specific PRD fields:** target OS-version floor (e.g., Android 9+ / iOS 16+), target device class (phone / tablet / fold), platform-specific monetization mechanism (IAP, subscription via App Store/Play Billing, ad SDK choice), platform-specific permission posture (camera, location, notifications).
- **Mobile-specific SRD fields (delta-fills the base placeholder):** iOS App Transport Security policy, Android SafetyNet/Play Integrity attestation, Keychain / Keystore key-class declarations, certificate-pinning policy.

---

## 3. Stage 2 — Prototype Variant (mobile-specific)

- **Prototype format (delta-fills the base placeholder):** single HTML file (validates functional requirements + design style; does NOT govern native interaction behaviour).
- **IDS surface coverage:** iOS HIG + Android Material Design — both must be specified for any "Both Native" / KMP / Flutter project. Component trees, gesture vocabularies, state diagrams, edge case matrices, animation specs, design tokens.

---

## 4. Stage 3 — Additional Mandatory ADRs (mobile-specific)

In addition to the universal **String Key Taxonomy ADR** and **Security Architecture ADRs** mandated by the base:

### 4.1 Platform Strategy ADR (mandatory for every mobile project)

The Platform Strategy ADR must include:

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
11. **Track activation mapping** — Explicit reference to which tracks are FULL, LIGHT, or dormant.
12. **Reassignment plan** — If tracks are dormant or light, where do freed engineers go?
13. **Contract versioning (KMP/Flutter only)** — Shared module API contract versioning scheme and notification mechanism.

**Ownership:** CTO authors the ADR. All three platform leads provide input. CIO reviews for technology conformance. CSO reviews for security conformance. The ADR is versionable + supersedable per [`company/pipeline/_base/adr-template.md`](company/pipeline/_base/adr-template.md); supersession requires a documented rollback plan and triggers an Implementation-Plan re-baseline (Stage 4 re-entry minimum).

### 4.2 Mobile-Specific Security ADR Topics

- iOS Keychain access-group strategy.
- Android Keystore key-purpose declarations.
- Certificate-pinning approach (per-host trust anchors, fallback policy on rotation).
- Background-execution sandbox (BGTaskScheduler / WorkManager constraints).

---

## 5. Stage 4 — Pipeline-Specific Plan Sections

### 5.1 Track Activation Mapping (mandatory in every Mobile Coding Implementation Plan)

The Track Activation Mapping is an explicit reference to the Platform Strategy ADR and activation of the corresponding track configuration (FULL/LIGHT/PRIMARY/Dormant per track per §1.3 above). Personnel assignments must reflect the active tracks.

### 5.2 Mobile-Specific Adapter Layer

The base mandates a "platform/surface adapter layer" in dependency mapping. For mobile, this is the **native adapter layer**: iOS-specific Swift/Objective-C wrappers around shared/cross-platform code, and Android-specific Kotlin/Java wrappers around the same.

---

## 6. Stage 5 — Track Execution Model (mobile-specific)

**Lead coordinator:** **VP Mobile (Marcus Andersson)** coordinates across all active platform tracks.

**Track execution:**

- **Track A (Android):** Led by Android Chapter Lead (Kofi Asante-Mensah). Executes per Platform Strategy ADR — FULL for native Android, LIGHT for KMP/Flutter integration.
- **Track B (iOS):** Led by iOS Chapter Lead (Seo-Yeon Park). Executes per Platform Strategy ADR — FULL for native iOS, LIGHT for KMP/Flutter integration.
- **Track C (Cross-Platform):** Led by Cross-Platform Chapter Lead (Mei-Ling Johansson). PRIMARY for KMP/Flutter projects. Co-coordinates with VP Mobile for cross-platform projects.

**Shared module coordination (KMP/Flutter only):** the shared module's public API contract must be defined before platform integration tracks begin implementation. Contract verification occurs at 30% and 70% completion milestones (the **Contract Verification Report**).

**SIS scope:** per-track SIS (Track A SIS, Track B SIS, Track C SIS as applicable), each translating SRD into platform-specific code patterns; CSO sign-off mandatory before Stage 5 Day 1.

**Design Fidelity Checkpoint scope:** Platform Leads present working builds of the active tracks for side-by-side comparison with IDS specifications on each platform. For KMP/Flutter, the cross-platform build is demonstrated on at least one Android device + one iOS device.

**Additional Mobile Stage-5 gate criteria (delta-fills the base placeholder):**

- [ ] Contract Verification Reports produced at 30% and 70% milestones (KMP/Flutter only).

---

## 7. Stage 6 — Tier-1 Review Model (mobile-specific)

**Tier-1 cross-review pairing (delta-fills the base placeholder):**

- **Native dual-track:** Android Lead ↔ iOS Lead cross-review. Each Lead reviews the other's platform code.
- **KMP:** Cross-Platform Lead reviews the shared module; Android/iOS Leads review native adapters.
- **Flutter:** Cross-Platform Lead reviews the Flutter codebase; Android/iOS Leads review platform channels.

**Live Demonstration scope:** the CDO demonstrates running builds on **both platforms** (Native dual-track, KMP, Flutter) or the single active platform (Android-only / iOS-only).

**Mobile-specific security mandate (delta-fills the base placeholder):** OWASP MASVS Level 2+ compliance (per KEEP-07).

---

## 8. Stage 7 — Platform-Specific Testing Mandates (mobile-specific)

Delta-fills the base's `{{DELTA: pipeline-specific Stage 7 testing mandates}}`:

- **Android:** Espresso instrumented tests, Play Pre-Launch Report (minimum device profiles per Platform Strategy).
- **iOS:** XCTest UI tests on current + previous iOS version.
- **KMP Cross-Platform:** Shared module unit tests (100% coverage) + platform adapter contract tests for both Android and iOS targets.
- **Flutter Cross-Platform:** Flutter widget tests + platform channel tests for every Flutter→Native bridge.
- **Integration:** At least one E2E flow per active platform (login → core feature → logout).
- **Accessibility (mobile-specific tools):** axe-core (web prototype), Espresso accessibility assertions (Android), XCTest accessibility checks (iOS). Severity classification follows the universal rule in the base.
- **OWASP penetration-testing track (delta-fills the base placeholder):** Manual penetration test by Security Engineer (Sana Khoury) covering OWASP Mobile Top 10 + MASVS assessment categories (AUTH, STORAGE, CRYPTO, NETWORK, PLATFORM, RESILIENCE).
- **Performance Benchmarks (mobile-specific metrics):** cold start, warm start, frame rate, memory usage, network payload — all measured per platform per active scenario.

**Regression testing model — device/browser/OS matrix (delta-fills the base placeholder):**

| Trigger     | Mobile-specific scope                                                                           |
| ----------- | ----------------------------------------------------------------------------------------------- |
| Nightly E2E | Full E2E on minimum device matrix (Pixel 6 + Pixel 8 + Galaxy S22 + iPhone 13 + iPhone 15 mini) |

---

## 9. Stage 8 — Additional Integrity Checks (mobile-specific)

Delta-fills the base placeholder for additional Stage-8 product-specific integrity checks:

- **Per-platform feature parity** — for "Both Native" / KMP / Flutter scenarios, every PRD feature must be verified to behave identically on Android and iOS. Drift is a P1 defect.

---

## 10. Stage 10 — Additional Release Criteria (mobile-specific)

Delta-fills the base placeholder for additional Stage-10 product-specific release criteria:

- **Store submission package complete:** App Store screenshots (every required device class), Play listing assets, age rating questionnaires, in-app purchase declarations, privacy nutrition labels.
- **Google Play Pre-Launch Report green** for the release-candidate build.
- **App Store TestFlight build distributed to internal QA** and crash-free for 48 hours minimum.

---

## 11. Stage 11 — Live Ops Mandates (mobile-specific)

Delta-fills the base placeholder for product-specific live-ops mandates:

- **Crash-rate SLO per platform:** Android crash-free users ≥ 99.5%; iOS crash-free users ≥ 99.7% (rolling 7-day windows).
- **Store-rejection escalation playbook:** documented chain — VP Mobile → CTO → CPO → CEO; max 24h to first response.
- **Per-platform release-candidate hold rules:** if Play Console pre-launch detects a crash regression, the rollout is paused automatically; the on-call DRI re-enables only after triage.

---

## 12. Cross-Cutting i18n Requirements

i18n is a continuous concern from Stage 2 onward. Mobile-specific application:

| Stage   | Mobile i18n requirement                                                                                                                                                                                |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Stage 1 | PRD declares target locales explicitly; locale list locked.                                                                                                                                            |
| Stage 2 | Pseudo-localized strings injected into the HTML prototype; IDS includes RTL layout mirroring rules for Arabic/Hebrew if in scope.                                                                      |
| Stage 3 | String Key Taxonomy ADR uses the canonical `{feature}.{screen}.{component}.{property}` shape; KMP projects also lock the `key-index.csv` cross-platform parity scheme.                                 |
| Stage 5 | Locale-aware components from first commit. Zero-hardcoded-strings rule enforced by CI on every PR; `strings.xml` (Android), `Localizable.strings` (iOS), `key-index.csv` (KMP) maintained in lockstep. |
| Stage 7 | Pseudo-locale screenshot regression on every PR. Locale-coverage tests on the nightly E2E job.                                                                                                         |
| Stage 9 | Translation accuracy only (i18n engineering already complete). CTO-L issues Translation Verification Report.                                                                                           |

---

## 13. Document Version History

| Version | Date           | Author                         | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------- | -------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.1     | April 21, 2026 | Software Architect + VP Mobile | Initial overlay. Mobile-specific content (5-scenario Strategy Matrix, Track A/B/C activation, KMP/Flutter semantics, per-scenario CI/CD blueprint, Mobile-specific Stage-1/2/3/4/5/6/7/8/10/11 sections, cross-cutting i18n table) extracted from the legacy `mobile-development/pipeline.md` (453 lines). Pairs with [`company/pipeline/_base/pipeline.md`](company/pipeline/_base/pipeline.md) to produce a derived view equivalent to the legacy file. |
