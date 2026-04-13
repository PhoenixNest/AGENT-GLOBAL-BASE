# Mobile Pipeline Optimization Plan

**Date:** April 8, 2026
**Author:** Lead Agent (Orchestrator)
**Context:** Post-recruitment optimization — 55 FTEs fully staffed, mobile-first (Android/iOS)
**Status:** C-Suite Panel Evaluation Complete — Unanimous Conditional Approve (8/8)

---

## Table of Contents

- [Part I: Core Recommendations](#part-i-core-recommendations) — 10 optimization recommendations
- [Part II: Platform Strategy Matrix](#part-ii-platform-strategy-matrix) — Conditional platform activation
- [Part III: Pipeline Overview Gaps](#part-iii-pipeline-overview-gaps) — 11 documentation gaps
- [Part IV: C-Suite Panel Evaluation](#part-iv-c-suite-panel-evaluation) — 8 officer reviews, 59 conditions
- [Appendix A: Personnel Reference](#appendix-a-personnel-reference) — Team assignments
- [Appendix B: Cross-Cutting Themes](#appendix-b-cross-cutting-themes) — Recurring patterns
- [Appendix C: Implementation Notes](#appendix-c-implementation-notes) — Approval requirements

---

## Part I: Core Recommendations

### Rec 1: Stage 5 Parallel Construction — Formalize It

| Aspect           | Detail                                                                                                                                 |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Problem**      | Stage 5 ("CTO oversees development") is the most mobile-relevant but least specified. The `MAXIMIZE` directive exists only in QWEN.md. |
| **Solution**     | Split into three parallel tracks with explicit ownership:                                                                              |
|                  | **Track A (Android):** Kofi Asante-Mensah → 6 engineers                                                                                |
|                  | **Track B (iOS):** Seo-Yeon Park → 6 engineers                                                                                         |
|                  | **Track C (Cross-Platform):** Mei-Ling Johansson → 2 engineers                                                                         |
| **Coordination** | Shared module coordination protocol + Stage 5 integration checkpoint (cross-platform parity verification)                              |

### Rec 2: Platform Leads in Stage 6 Code Review

| Aspect       | Detail                                                                                         |
| ------------ | ---------------------------------------------------------------------------------------------- |
| **Problem**  | Platform Leads absent from Stage 6 review panel. Only C-suite reviews — lacks technical depth. |
| **Solution** | Two-tier review:                                                                               |
|              | **Tier 1 (Technical):** Platform Leads cross-review each other's code (Android ↔ iOS)          |
|              | **Tier 2 (Strategic):** C-suite reviews Tier 1 findings + PRD/IDS/SRD conformance              |
| **Note**     | Tier 1 is advisory; C-suite retains gate authority.                                            |

### Rec 3: Per-Platform Monitoring Enhancement

| Aspect       | Detail                                                                                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Problem**  | Monitoring system has zero platform breakdown. Cannot distinguish Android 80% / iOS 40%.                                                                      |
| **Solution** | Extend `PROGRESS.md` with per-platform progress table and `platform_breakdown` in checkpoint JSON. Progress Sync Protocol (>20% variance) fires per-platform. |

### Rec 4: Mobile Testing Strategy — Platform-Specific Mandates

| Aspect       | Detail                                                                                                     |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| **Problem**  | Testing requirements are platform-agnostic. No device matrix, UI automation, or store compliance mandates. |
| **Solution** | Stage 7 must include:                                                                                      |
|              | **Android:** Espresso instrumented tests + Play Pre-Launch Report                                          |
|              | **iOS:** XCTest UI tests on 2 iOS versions (current + previous)                                            |
|              | **Cross-Platform:** KMP shared module unit tests (100%) / Flutter widget tests                             |
|              | **Integration:** At least one E2E flow per platform                                                        |

### Rec 5: Cross-Platform Integration Verification

| Aspect       | Detail                                                                                                                   |
| ------------ | ------------------------------------------------------------------------------------------------------------------------ |
| **Problem**  | No mechanism to verify KMP shared modules work with both Android/iOS consumers, or Flutter platform channels are tested. |
| **Solution** | Stage 5.5 coordination artifacts:                                                                                        |
|              | **KMP:** Contract Verification Report (shared API matches both consumers)                                                |
|              | **Flutter:** Platform Channel Audit (all Flutter→Native channels have implementations)                                   |
| **Owner**    | Cross-Platform Lead with sign-off from Android + iOS Leads                                                               |

### Rec 6: Leverage VP-Tier Talent — Strategic Reassignments

| Person                                       | Role                            | Assignment                                                                            |
| -------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------------- |
| **Marcus Andersson** (VP Mobile, 19/20)      | Stage 5 coordinator             | Orchestrates parallel construction across all three platform leads                    |
| **Aisha Patel** (VP Quality, 19/20)          | Stage 7 test architecture owner | Test strategy design, not just execution                                              |
| **David Okonkwo** (VP Platform, 19/20)       | CI/CD mobile pipeline owner     | Build signing, provisioning profiles, Play Console/TestFlight automation              |
| **Dr. Elena Rostova** (Sr. Architect, 18/20) | Architecture compliance         | Reviews ADRs for mobile conformance _(Note: CIO recommends role expansion — see H10)_ |
| **Thomas Zhang** (DevOps Lead, 15/20)        | Mobile SAST/DAST implementation | Android Lint security checks, iOS static analysis, dependency scanning                |

### Rec 7: Buddy System for Lower-Vetting-Score Hires

Seven hires scored 12/20 — structured support required:

| Hire                       | Score | Buddy                   | Checkpoint               |
| -------------------------- | ----- | ----------------------- | ------------------------ |
| Hiroshi Tanaka (iOS)       | 12/20 | Lars Eriksson (17/20)   | Day 30/60/90 SwiftUI     |
| Yuna Park (Frontend)       | 12/20 | Elena Kim (18/20)       | Day 30 React             |
| Omar Hassan (Backend)      | 12/20 | Viktor Horvath (15/20)  | Day 30 API design        |
| Ingrid Nilsen (Backend)    | 12/20 | Aisha Mohammed (15/20)  | Day 30 FastAPI           |
| Thabo Mokoena (Backend)    | 12/20 | Kael Jensen (15/20)     | Day 30 real-time systems |
| Marcus Wright (Full-Stack) | 12/20 | Nina Petrova (15/20)    | Day 30 full-stack flow   |
| Tobias Weber (SDET)        | 12/20 | Ananya Krishnan (15/20) | Day 30 test framework    |

### Rec 8: CI/CD Mobile Pipeline

Must-haves before Stage 5:

| Component       | Details                                                                     |
| --------------- | --------------------------------------------------------------------------- |
| **Android CI**  | Gradle build per PR, Detekt, unit tests, Firebase Test Lab instrumentation  |
| **iOS CI**      | Xcode build per PR, SwiftLint, unit tests, Xcode UI tests on macOS runner   |
| **KMP CI**      | Shared module builds on JVM + Android + iOS targets, tests on all platforms |
| **i18n CI**     | String key naming enforcement, `key-index.csv` parity check                 |
| **Security CI** | SAST, dependency scanning, secrets detection (gitleaks)                     |

### Rec 9: String Key Naming — Tomas Dvoracek as Central Authority

| Aspect          | Detail                                                                                                                                                 |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Standard**    | `{feature}.{screen}.{component}.{property}` dot-notation                                                                                               |
| **Timing**      | Taxonomy defined during Stage 3 (architecture), `key-index.csv` created during Stage 4 _(Note: CIO and CTO-L recommend Stage 3 for taxonomy — see C9)_ |
| **Enforcement** | CI/CD gate (Thomas Zhang) enforces after 2-week grace period                                                                                           |

### Rec 10: Technical Debt Allocation — 15-20% Sprint Capacity (Per-Project Variable)

With 18 mobile engineers, reserving 15-20% = ~3 FTEs per sprint for:

- Refactoring platform-specific code
- SDK version updates (Android API level, iOS SDK)
- Performance profiling and optimization
- Ongoing accessibility compliance monitoring and edge case remediation _(not retrofitting — accessibility is a first-class Stage 2/7 requirement per C6)_
- Security debt (minimum 5% of total sprint capacity): crypto library updates, vulnerability patching, obfuscation improvements, certificate pin rotation, SAST finding remediation

**Calibration:** 15-20% is a starting heuristic, not a fixed percentage. Calibrate per project complexity: greenfield 20%, mature 15%, inherited up to 30%. Technical debt work items are tracked in the same system as feature work and reported in PROGRESS.md.

---

## Part II: Platform Strategy Matrix

### Problem Statement

Recommendations 1–5 assume all three tracks are active simultaneously. In reality, users may request Android-only, iOS-only, both native, KMP, or Flutter. The pipeline's Stage 1 gate asks "Android, iOS, or both?" — this confirms **target platforms** (where the app ships), not **implementation approach** (how the code is structured). The latter is an architecture decision at **Stage 3**.

**Five mutually exclusive scenarios — a project selects exactly one.**

### Matrix

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

| Term        | Definition                                                                                                    |
| ----------- | ------------------------------------------------------------------------------------------------------------- |
| **FULL**    | End-to-end feature implementation, testing, and delivery for that platform                                    |
| **LIGHT**   | Platform-specific integration only (UI glue, platform APIs, native dependencies). NOT feature implementation. |
| **PRIMARY** | Owns the shared codebase that produces binaries for multiple platforms                                        |
| **Dormant** | Track lead and engineers are reassigned to other projects or internal tooling                                 |

### KMP/Flutter — How Track A/B Semantics Change

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
| SwiftLint              | ❌           | ✅       | ✅          | ❌                       | ❌                 |
| KMP multi-target       | ❌           | ❌       | ❌          | ✅ (JVM + Android + iOS) | ❌                 |
| Flutter build          | ❌           | ❌       | ❌          | ❌                       | ✅ (Android + iOS) |
| Platform channel tests | ❌           | ❌       | ❌          | ❌                       | ✅                 |
| Firebase Test Lab      | ✅           | ❌       | ✅          | ✅ (Android adapter)     | ❌                 |
| Xcode UI tests         | ❌           | ✅       | ✅          | ✅ (iOS adapter)         | ❌                 |

### Platform Strategy ADR Requirements

The mandatory Platform Strategy ADR at Stage 3 must include **all 13 fields**:

1. **Decision statement** — Which approach: native dual-track, KMP, or Flutter? KMP and Flutter are mutually exclusive — select exactly one.
2. **Rationale** — Why this approach? (team skills, time-to-market, code sharing targets, performance)
3. **Trade-offs** — What is gained and sacrificed vs. alternatives?
4. **Team capability assessment** — Do we have the right people?
5. **Risk analysis** — What could go wrong? (KMP iOS target maturity, Flutter package ecosystem, native API limits)
6. **TCO projection (24-month)** — Engineering headcount, SDK update cost, platform-specific feature cost, total estimated cost.
7. **Vendor lock-in risk matrix** — Framework abandonment risk, migration cost if switching to native, open-source dependency risk, exit strategy.
8. **Performance SLA alignment** — Cold start, frame rate, memory, network payload — can the chosen approach meet PRD thresholds?
9. **Store & compliance implications** — App Store Review Guidelines compatibility, Google Play Developer Policy compatibility, in-app purchase requirements, background execution permissions, IAP revenue share tier (15% small business vs. 30% standard).
10. **STRIDE-based threat model** — Authored by Security Architect, reviewed by CSO. Platform-specific attack surface notes (KMP C interop, Flutter Dart VM, native dual-implementation).
11. **Track activation mapping** — Explicit reference to which tracks are FULL, LIGHT, or dormant per track.
12. **Reassignment plan** — If tracks are dormant or light, where do freed engineers go?
13. **Contract versioning (KMP/Flutter only)** — Shared module API contract versioning scheme and notification mechanism.
14. **Design risk assessment** — Cross-platform UI divergence risk, custom widget native parity, design token compatibility, platform-specific accessibility availability.

**Ownership:** CTO authors the ADR. All three platform leads provide input. CIO reviews for technology conformance. CSO reviews for security conformance. CDO reviews for design quality impact. Once approved at Stage 3 gate, this decision is **locked** — switching between strategies requires a full stage rollback (Stage 3 re-entry, ADR re-authorship, Implementation Plan re-baseline).

---

## Part III: Pipeline Overview Gaps

**Source:** Systematic comparison of `company/library/overview/pipeline.md` against `company/pipeline/mobile-development/pipeline.md`.

### 🔴 Critical — Execution would be incorrect without these

| #   | Gap                                           | Full Spec Says                                                                                                                    | Overview Says                                    |
| --- | --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| 1   | **No user approval gate indicator**           | Each stage states whether user approval is required (Stages 1→2, 2→3, 3→4, 4→5, 6→7, 7→8, 10 require user; 5→6, 8→9, 9→10 do not) | No indication of which stages need user approval |
| 2   | **Stage 4 technology decision lock**          | "ADRs and TSD from Stage 3 serve as reference inputs — **technology decisions are locked**"                                       | No mention of the lock                           |
| 3   | **Stage 8 "trim-to-pass" anti-pattern guard** | "Functionality removal is **never a valid remediation strategy**" — the PRIMARY purpose of Stage 8                                | Only lists panel composition                     |

### 🟠 High — Important context missing

| #   | Gap                                    | Full Spec Says                                                                                                 | Overview Says                                  |
| --- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| 4   | **Stage 6's 4 review criteria**        | Panel reviews: (1) PRD implemented, (2) IDS reproduced, (3) UML/ADR/TSD implemented, (4) SRD security enforced | Only lists panel members                       |
| 5   | **Stage 7 regression testing mandate** | "Regression testing on **all affected functionalities**. Must pass fully before advancing"                     | No mention                                     |
| 6   | **Stage 9 responsibility split**       | CPO/CDO/CTO review **structure only**. Translation accuracy is **CTO-L's sole responsibility**                 | Groups "CTO-L + R&D" together — no distinction |
| 7   | **No artifact input column**           | Each stage has explicit "Artifacts In"                                                                         | Summary table only shows "Key Output"          |

### 🟡 Medium — Completeness gaps

| #   | Gap                                | Full Spec Says                                                                                            | Overview Says                                  |
| --- | ---------------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| 8   | **Stage 5 CTO internal review**    | "CTO conducts comprehensive internal review to ensure project compiles, runs, is bug-free" before Stage 6 | No mention                                     |
| 9   | **Stage 6 remediation loop**       | "CTO assigns R&D to remediate. Full review repeats until all panel sign off"                              | No mention of re-review cycle                  |
| 10  | **Security team below CSO absent** | James Wright, Natalia Petrova, and 4 engineers actively support Stage 1/6/8                               | Stage Owner Index only lists "CSO"             |
| 11  | **Three-layer monitoring system**  | PROGRESS.md + session logs + checkpoint JSON                                                              | References monitoring.md but doesn't summarize |

---

## Part IV: C-Suite Panel Evaluation

**Date:** April 8, 2026 | **Convened by:** Lead Agent (Orchestrator) | **Panel:** 8 officers

### Verdict: Unanimous Conditional Approve (8/8)

| Officer                       | Verdict             | Conditions | Critical |
| ----------------------------- | ------------------- | ---------- | -------- |
| Dr. Kenji Nakamura (CTO)      | Conditional Approve | 9          | 2        |
| Marcus Tran-Yoshida (CPO)     | Conditional Approve | 6          | 3        |
| Dr. Sarah Chen (CSO)          | Conditional Approve | 10         | 4        |
| Yuki Tanaka-Chen (CDO)        | Conditional Approve | 6          | 3        |
| Dr. Priya Mehta (CIO)         | Conditional Approve | 7          | 3        |
| Dr. Amara Osei-Mensah (CTO-L) | Conditional Approve | 6          | 1        |
| Marcus Andersson (VP Mobile)  | Conditional Approve | 6          | 2        |
| Aisha Patel (VP Quality)      | Conditional Approve | 9          | 3        |

**Total: 59 conditions — 18 Critical, 14 High, 18 Medium, 9 resolved inline.**

---

### Critical Conditions (9 items — cross-officer consensus)

| #      | Condition                                                                                                                                                                 | Raised By                 | Owner               |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- | ------------------- |
| **C1** | **KMP capacity gap** — Plan assumes 6 KMP engineers; actual roster has 3. Revise to 5 (Mei-Ling + Dmitri + Fatima + Priya N. + Sofia R.). Timeline adjusted by ~1 sprint. | CTO, VP Mobile, CIO       | CTO                 |
| **C2** | **Platform Strategy ADR expanded** — Add TCO (24-month), Vendor Lock-In Risk Matrix, Performance SLA, Store/Compliance implications.                                      | CIO, CTO, CPO             | CIO                 |
| **C3** | **Security Implementation Specification (SIS)** per platform track before Stage 5. Authored by Natalia Petrova + James Wright, signed off by CSO.                         | CSO                       | CSO                 |
| **C4** | **CI/CD security expanded** — Add Semgrep, CodeQL, OWASP ZAP, CycloneDX SBOM, cosign signing, HashiCorp Vault, pipeline hardening.                                        | CSO, CTO, CIO             | CSO + DevOps        |
| **C5** | **Test Architecture Document (TAD)** as Stage 4 deliverable. Device farms (Firebase Test Lab + AWS Device Farm) provisioned before Stage 5.                               | VP Quality, CTO, CPO      | VP Quality + DevOps |
| **C6** | **Accessibility as Stage 7 mandate, NOT tech debt** — WCAG 2.1 AA in IDS from Stage 2, tested in Stage 7. Rec 10 reworded.                                                | CDO, CPO, CSO, VP Quality | CDO + VP Quality    |
| **C7** | **User approval gate indicator** in pipeline overview — every stage shows "User Approval Required: Yes/No."                                                               | CTO, CPO                  | CTO                 |
| **C8** | **Stage 8 "trim-to-pass" anti-pattern explicit** — security control removal/disabling/weakening = P0 defect.                                                              | CTO, CSO                  | CTO + CSO           |
| **C9** | **String key taxonomy moved to Stage 3 (ADR)** — naming convention is a technology decision that locks at Stage 3. `key-index.csv` operationalized in Stage 4.            | CIO, CTO-L                | CIO                 |

---

### High-Priority Conditions (14 items)

| #   | Condition                                                                                                                                          | Raised By      | Owner                   |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | ----------------------- |
| H1  | **Track A/B "LIGHT" exclusion criteria** — explicitly define what is NOT in scope for thin native adapters.                                        | CTO            | CTO                     |
| H2  | **Stage 6 Tier 1 is advisory only** — C-suite retains gate authority. Automated quality gates mandatory before Tier 1.                             | CTO, CSO       | CTO                     |
| H3  | **Stage 5.5 checkpoint split** — 30% contract verification + 70% integration verification.                                                         | VP Mobile, CTO | VP Mobile               |
| H4  | **CI/CD architecture during Stage 3** — not Stage 4. Hard gate before Stage 5.                                                                     | CTO, VP Mobile | CTO + DevOps            |
| H5  | **Platform Strategy ADR switch = full stage rollback** — not just P0 risk.                                                                         | CTO            | CTO                     |
| H6  | **Tier 1 cross-review produces written memo** — becomes part of Stage 6 Defect Report.                                                             | CPO            | CTO                     |
| H7  | **Stage 5 Design Fidelity Checkpoint** — mandatory design review at ~60% Stage 5 completion.                                                       | CDO            | CDO                     |
| H8  | **IDS timeline aligned with Platform Strategy ADR** — surface platform strategy at Stage 1 as option, or produce platform-agnostic IDS at Stage 2. | CDO, CIO       | CDO                     |
| H9  | **ADR enforcement: three-layer defense** — Platform Lead attestation + Elena Rostova audits + CI/CD gates.                                         | CIO            | CIO + CTO               |
| H10 | **Elena Rostova: Architecture Compliance Analyst** (Stages 3–6) — not "Stage 3/4 reviewer."                                                        | CIO            | CIO                     |
| H11 | **Translation progress tracking** in per-platform monitoring — TM leverage %, post-editing %, linguistic QA pass rate per language.                | CTO-L          | CTO-L + DevOps          |
| H12 | **Stage Owner Index expanded** — show full security team hierarchy with stage-specific responsibilities.                                           | CSO            | CTO + CSO               |
| H13 | **Security debt allocation** — minimum 5% sprint capacity for security debt.                                                                       | CSO            | CSO + CTO               |
| H14 | **Tobias Weber buddy system starts Week 1 of Stage 5** — paired test code review with Ananya for 90 days.                                          | VP Quality     | VP Quality + Rachel Kim |

---

### Medium-Priority Conditions (18 items)

| #   | Condition                                                                                                                                 | Raised By           | Owner                       |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | --------------------------- |
| M1  | **Tech debt allocation is per-project variable** — 15-20% is starting heuristic, calibrated per project.                                  | CTO                 | CTO                         |
| M2  | **PROGRESS.md includes dependency graph** — shows "what blocks what" per track.                                                           | VP Mobile, CTO, CPO | VP Mobile                   |
| M3  | **Dormant-track reassignment defined** as tech debt + test automation + cross-training + SDK migration prep.                              | VP Mobile           | VP Mobile                   |
| M4  | **Mei-Ling as co-coordinator** for KMP/Flutter projects with Track C internal delivery authority.                                         | VP Mobile           | VP Mobile                   |
| M5  | **String key naming: CTO recommends Stage 4** for implementation detail. _(Conflict with C9 — CIO/CTO-L say Stage 3. Resolution needed.)_ | CTO                 | CTO                         |
| M6  | **Stage 5 CTO internal review** added to pipeline overview.                                                                               | CTO                 | CTO                         |
| M7  | **Stage 6 remediation loop** added to pipeline overview.                                                                                  | CTO                 | CTO                         |
| M8  | **Three-layer monitoring system** summarized in pipeline overview.                                                                        | CTO                 | CTO                         |
| M9  | **Live demo at Stage 6** — CDO interacts with running builds on both platforms.                                                           | CDO                 | CDO                         |
| M10 | **Design Fidelity Test Checklist** in Stage 7 — manual protocol authored by CDO.                                                          | CDO                 | CDO                         |
| M11 | **IDS versioning and change propagation protocol** for parallel tracks during Stage 5.                                                    | CDO                 | CDO                         |
| M12 | **Platform-specific translation style guides** for KMP `key-index.csv` and Flutter ARB.                                                   | CTO-L               | CTO-L                       |
| M13 | **Cross-Platform String Parity Report** added to Stage 5.5 checkpoint.                                                                    | CTO-L               | CTO-L + Cross-Platform Lead |
| M14 | **`key-index.csv` maintenance ownership** during Stage 5 — Tomas owns, CI/CD enforces, VP Mobile coordinates.                             | CTO-L               | CTO                         |
| M15 | **CI/CD i18n gate extended** — placeholder integrity, empty value detection, truncation risk (>40% length increase).                      | CTO-L               | DevOps + Tomas Dvoracek     |
| M16 | **`translation_status` column** in `key-index.csv` — extracted → tm_analyzed → translated → post_edited → validated.                      | CTO-L               | Tomas Dvoracek              |
| M17 | **Quarterly Technology Radar** for continuous technology evaluation.                                                                      | CIO                 | CIO                         |
| M18 | **Performance benchmarks** per platform — cold start (<2s), frame rate (60fps), memory (<150MB).                                          | VP Quality, CPO     | VP Quality                  |

---

### Cross-Cutting Themes

| Theme                                      | Officers                       | Required Action                                                                                                                                     |
| ------------------------------------------ | ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Security under-represented**             | CSO, CTO, CIO                  | Security team absent from narrative; add to Implementation Notes; mandate STRIDE threat modeling in Platform Strategy ADR                           |
| **Accessibility misclassified**            | CDO, CPO, CSO, VP Quality      | All four independently flagged Rec 10's "tech debt" as unacceptable. Reclassify as Stage 2/7 requirement.                                           |
| **String key placement conflict**          | CIO (S3), CTO-L (S3), CTO (S4) | Resolution: taxonomy definition at Stage 3, `key-index.csv` operationalization at Stage 4.                                                          |
| **KMP capacity gap**                       | CTO, VP Mobile, CIO            | Plan assumes 6; actual is 3. Revise to 5 with borrowed staff; adjust timeline ~1 sprint.                                                            |
| **Monitoring needs dependency graph**      | VP Mobile, CTO, CPO            | Percentages alone insufficient. Must show blocking relationships.                                                                                   |
| **CI/CD must start in Stage 3**            | CTO, VP Mobile, VP Quality     | Architecture and prototype during Stage 3; operational by Stage 5 Day 1.                                                                            |
| **Stage 2 IDS vs. Stage 3 ADR sequencing** | CDO, CIO                       | IDS produced before platform strategy known. Flutter IDS cannot match native IDS. Surface option at Stage 1 or produce platform-agnostic IDS first. |

---

## Appendix A: Personnel Reference

### VP-Tier

| Name             | Role                         | Vetting | Pipeline Ownership                        |
| ---------------- | ---------------------------- | ------- | ----------------------------------------- |
| Marcus Andersson | VP Mobile Engineering        | 19/20   | Stage 5 coordinator (all platform tracks) |
| Elena Vasquez    | VP Web & Backend Engineering | 19/20   | Stage 5 web/backend track                 |
| David Okonkwo    | VP Platform Engineering      | 19/20   | CI/CD mobile pipeline owner               |
| Aisha Patel      | VP Quality Engineering       | 19/20   | Stage 7 test architecture owner           |

### Platform Leads

| Name               | Role                | Team Size   | Pipeline Stages |
| ------------------ | ------------------- | ----------- | --------------- |
| Kofi Asante-Mensah | Android Lead        | 6 engineers | 5, 8            |
| Seo-Yeon Park      | iOS Lead            | 6 engineers | 5, 8            |
| Mei-Ling Johansson | Cross-Platform Lead | 2 engineers | 5, 8            |

### Security Team

| Name            | Role                   | Reports To   | Key Training                        |
| --------------- | ---------------------- | ------------ | ----------------------------------- |
| James Wright    | Lead Security Engineer | CSO          | MASVS Mastery (30d, High risk)      |
| Natalia Petrova | Security Architect     | CSO          | Mobile Threat Modeling, ADR/TSD     |
| Sana Khoury     | Security Engineer #1   | James Wright | Mobile pen testing                  |
| Omar Farouq     | Security Engineer #2   | James Wright | MASVS + Pentesting (90d, High risk) |
| Li Wei Chen     | Security Engineer #3   | James Wright | Supply chain security               |
| Ingrid Solberg  | Compliance Analyst     | James Wright | SOC 2, GDPR, ISO 27001              |

### Testing Team

| Name            | Role                 | Reports To  | Platform Focus              |
| --------------- | -------------------- | ----------- | --------------------------- |
| Priscilla Oduya | Test Lead            | CTO         | Integration + regression    |
| Rachel Kim      | Test Automation Lead | Aisha Patel | Test framework architecture |
| Ananya Krishnan | SDET Mobile #1       | Rachel Kim  | Android test automation     |
| Tobias Weber    | SDET Mobile #2       | Rachel Kim  | iOS test automation         |
| Priya Sharma    | SDET Web/Backend #1  | Rachel Kim  | API contract tests          |

---

## Appendix B: Cross-Cutting Themes

Seven recurring patterns identified across multiple independent officer evaluations. See [Cross-Cutting Themes table](#cross-cutting-themes) in Part IV for details.

---

## Appendix C: Implementation Notes

These recommendations are **advisory** — they do not modify the pipeline specification itself. Implementation requires:

1. **CTO approval** — Stage 5 coordinator, two-tier code review, per-platform monitoring
2. **VP Mobile acceptance** — Stage 5 coordination role
3. **Platform Lead buy-in** — cross-review in Stage 6, integration checkpoint
4. **DevOps Lead execution** — CI/CD mobile pipeline setup
5. **VP Quality ownership** — Stage 7 test architecture
6. **CSO approval** — SIS, CI/CD security expansion, Stage Owner Index expansion
7. **CIO alignment** — Platform Strategy ADR template, ADR enforcement, string key taxonomy
8. **CDO integration** — Design Fidelity Checkpoint, IDS timeline alignment, accessibility-first IDS

All recommendations are **incremental** — none require pipeline stage renumbering or gate authority changes.

---

## Officer Evaluation Status

| Officer                       | Evaluation  | Status              |
| ----------------------------- | ----------- | ------------------- |
| Dr. Kenji Nakamura (CTO)      | ✅ Complete | Pending user review |
| Marcus Tran-Yoshida (CPO)     | ✅ Complete | Pending user review |
| Dr. Sarah Chen (CSO)          | ✅ Complete | Pending user review |
| Yuki Tanaka-Chen (CDO)        | ✅ Complete | Pending user review |
| Dr. Priya Mehta (CIO)         | ✅ Complete | Pending user review |
| Dr. Amara Osei-Mensah (CTO-L) | ✅ Complete | Pending user review |
| Marcus Andersson (VP Mobile)  | ✅ Complete | Pending user review |
| Aisha Patel (VP Quality)      | ✅ Complete | Pending user review |

---

_Document created: April 8, 2026_
_Last updated: April 8, 2026 (C-Suite Panel Evaluation added)_
_Status: Pending user review and implementation decisions_
