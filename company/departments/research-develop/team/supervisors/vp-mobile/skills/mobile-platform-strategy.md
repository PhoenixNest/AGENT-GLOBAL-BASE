---
name: mobile-platform-strategy
description: Mobile platform strategy for consumer-scale applications: Kotlin Multiplatform architecture, cross-platform code sharing, mobile org scaling, competency matrix design, and delivery planning at 500M+ MAU.
version: "1.0.0"
---

# Mobile Platform Strategy

## Purpose

Own all mobile engineering execution across Android, iOS, and cross-platform teams. Translate the Coding Implementation Plan and UML Engineering Package into platform-specific development plans, enforce architectural coherence across 30+ mobile engineers, and deliver at consumer scale (500M+ MAU, 99.9% crash-free rate, sub-400ms perceived latency).

## Why This Matters

Defines the strategic direction for iOS and Android platforms. Without platform strategy, teams drift toward lowest-common-denominator solutions that fail to leverage platform advantages.

## Kotlin Multiplatform Architecture (Shared-Logic, Native-UI)

### Decision Framework: When to Share vs. Platform-Specific

| Domain                                                        | Recommendation                                  | Rationale                                                                         |
| ------------------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------- |
| Business logic (domain models, use cases, validation)         | **Share via KMP**                               | Zero UI dependency, identical behavior expected across platforms                  |
| Data layer (repository implementations, API clients, caching) | **Share via KMP**                               | Same backend contracts, same serialization logic                                  |
| Persistence (Room → SQLDelight, CoreData → SQLDelight)        | **Share via SQLDelight**                        | Single SQL schema, platform-specific driver                                       |
| Networking (HTTP clients, interceptors, auth)                 | **Share via Ktor**                              | Same API contracts, token refresh logic identical                                 |
| UI components                                                 | **Platform-native** (Jetpack Compose / SwiftUI) | Platform-specific UX expectations, native performance, accessibility              |
| Navigation                                                    | **Platform-native**                             | Different navigation paradigms (back stack vs. navigation stack)                  |
| Platform integrations (notifications, deep links, biometrics) | **Platform-native with shared interface**       | Define expect interface in shared module, provide platform actual implementations |

### Shared Module Architecture

```kotlin
// shared/build.gradle.kts
kotlin {
    androidTarget()
    listOf(iosX64(), iosArm64(), iosSimulatorArm64()).forEach { iosTarget() }

    sourceSets {
        commonMain {
            dependencies {
                implementation(libs.ktor.client.core)
                implementation(libs.ktor.client.contentNegotiation)
                implementation(libs.ktor.serialization.kotlinx.json)
                implementation(libs.kotlinx.coroutines.core)
                implementation(libs.kotlinx.datetime)
                implementation(libs.sqldelight.coroutines)
                implementation(libs.koin.core)
            }
        }
        androidMain {
            dependencies {
                implementation(libs.ktor.client.okhttp)
                implementation(libs.sqldelight.android.driver)
            }
        }
        iosMain {
            dependencies {
                implementation(libs.ktor.client.darwin)
                implementation(libs.sqldelight.native.driver)
            }
        }
    }
}
```

### expect/actual Pattern for Platform Integrations

```kotlin
// commonMain — shared interface
expect class SecureStorage() {
    suspend fun get(key: String): String?
    suspend fun set(key: String, value: String)
    suspend fun delete(key: String)
}

// androidMain — Android Keystore + EncryptedSharedPreferences
actual class SecureStorage actual constructor() {
    private val context = ... // inject via Koin
    actual suspend fun get(key: String): String? = ...
    actual suspend fun set(key: String, value: String) = ...
    actual suspend fun delete(key: String) = ...
}

// iosMain — iOS Keychain
actual class SecureStorage actual constructor() {
    actual suspend fun get(key: String): String? = ...
    actual suspend fun set(key: String, value: String) = ...
    actual suspend fun delete(key: String) = ...
}
```

### Code Sharing Targets

| Phase                | Shared Coverage | Components                                                                     |
| -------------------- | --------------- | ------------------------------------------------------------------------------ |
| Phase 1 (foundation) | 25–30%          | Domain models, use cases, repository interfaces, DTOs, serialization           |
| Phase 2 (data layer) | 35–40%          | Repository implementations, Ktor API client, SQLDelight schema, auth flow      |
| Phase 3 (advanced)   | 40–45%          | Notification logic, analytics, A/B testing, feature flags, experiment tracking |

**Quality gate:** Shared module must have zero platform SDK imports. If a file imports `android.*` or `UIKit`, it belongs in a platform module, not shared.

## Mobile Organization Scaling

### Team Structure (per project)

```
VP of Mobile Engineering
├── Android Chapter Lead
│   ├── Senior Android Engineers (3)
│   └── Android Engineers (3)
├── iOS Chapter Lead
│   ├── Senior iOS Engineers (3)
│   └── iOS Engineers (3)
└── Cross-Platform Chapter Lead
    └── Cross-Platform Engineers (2)
```

### Feature Parity Tracking

Weekly cross-platform sync identifies Android/iOS feature gaps >1 sprint. Tracking mechanism:

| Metric                         | Target       | Alert Threshold                                           |
| ------------------------------ | ------------ | --------------------------------------------------------- |
| Feature parity gap             | 0 sprints    | >1 sprint → escalate to VP                                |
| Bug parity (platform-specific) | <5% of total | >10% → investigate root cause in shared vs. platform code |
| Release cadence alignment      | Same week    | >2 week gap → investigate release pipeline                |

### Competency Matrix Design

Skill bands for mobile engineers:

| Level           | Technical Scope                                                   | Impact Scope                             | Leadership                         |
| --------------- | ----------------------------------------------------------------- | ---------------------------------------- | ---------------------------------- |
| IC1 (Junior)    | Implements assigned features within established patterns          | Single feature, single platform          | Self-managed                       |
| IC2 (Mid)       | Designs solutions for features; chooses appropriate patterns      | Single feature, cross-platform awareness | Mentors IC1                        |
| IC3 (Senior)    | Defines technical direction for feature areas; trade-off analysis | Multiple features, cross-platform        | Tech lead for 2–3 engineers        |
| IC4 (Staff)     | Shapes engineering standards; architecture decisions              | Org-wide (all mobile)                    | Mentors IC3; code review authority |
| IC5 (Principal) | Technology vision; industry-representative expertise              | Company-wide (all engineering)           | Cross-department influence         |

## Delivery Planning at Consumer Scale

### Release Coordination

Staged rollout strategy for all production releases:

| Stage    | Traffic %    | Duration | Success Criteria                               | Auto-Rollback Trigger  |
| -------- | ------------ | -------- | ---------------------------------------------- | ---------------------- |
| Internal | 0% (dogfood) | 2 days   | Zero P0/P1 in internal testing                 | Any P0                 |
| Alpha    | 1%           | 1 day    | Crash-free rate ≥99.9%                         | Crash-free rate <99.9% |
| Beta     | 5%           | 2 days   | Crash-free rate ≥99.95%, no P1 support tickets | Crash-free rate <99.9% |
| Phased   | 25%          | 3 days   | All KPIs stable vs. previous version           | Any regression >5%     |
| Phased   | 50%          | 3 days   | All KPIs stable                                | Any regression >3%     |
| Full     | 100%         | —        | —                                              | —                      |

### Technical Debt Allocation

20% of each sprint capacity reserved for technical debt, measured by:

- **Cyclomatic complexity:** No function >15; module average <8
- **Test coverage:** Shared ≥85%, platform-specific ≥75%
- **Build time:** Clean CI build <8 minutes
- **Crash-free rate:** ≥99.9% for all production releases

## Stage 6 — Code Review Panel Responsibilities

Marcus is a panel member at every Stage 6 Code Review. His review scope is limited to mobile engineering quality; security and product correctness are reviewed by other panel members. Within his scope, any finding Marcus classifies as P0 or P1 blocks advancement from Stage 6.

### Review Checklist — Mobile Engineering

| Area                         | What Marcus Reviews                                                                                      | P0/P1 Trigger                                                      |
| ---------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **KMP boundary integrity**   | Shared module contains no `android.*` or `UIKit` imports                                                 | Any platform import in shared module                               |
| **Architecture adherence**   | Feature implementations follow the agreed KMP layer structure (domain → data → platform-UI)              | Architectural bypass that creates future migration debt            |
| **Test coverage**            | Shared ≥85%, platform-specific ≥75%; critical paths have both unit and integration tests                 | Coverage below P0 thresholds on any released-to-production module  |
| **Performance implications** | Any change affecting cold start, frame rate, memory, or battery; review against Stage 3 performance SLOs | Measurable regression vs. SLO baseline in staging profiling        |
| **Release rollout safety**   | Feature flags correctly gating new behaviour; staged rollout percentage approved                         | Missing flag gate on any first-time feature delivery to 100% users |
| **Feature parity**           | Equivalent behaviour confirmed on both Android and iOS; divergences documented with owner and timeline   | Undocumented divergence with no remediation plan                   |

### Defect Remediation Loop

When Marcus identifies a P0 or P1 during Stage 6, he files a defect in Jira with the full code path, test case, and impact assessment. After remediation, the full Stage 6 review panel convenes again from the beginning — not from defect verification only.

## Stage 8 — Integrity Verification Panel Responsibilities

Marcus signs off on the mobile engineering dimension of Stage 8 Integrity Verification. His sign-off is required before the release candidate can advance to Stage 9 (i18n Engineering).

### Sign-Off Checklist — Mobile Integrity

| Gate                                  | Evidence Required                                                                                                                                   | Marcus's Verdict                             |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| **Crash-free rate**                   | Firebase Crashlytics report from Beta rollout (5%) showing ≥99.95% crash-free session rate                                                          | Block release if below threshold             |
| **Cold start performance**            | Profiling output from CI benchmark suite: Android P50 <400ms, iOS P50 <350ms                                                                        | Block release if above threshold             |
| **Shared module boundary compliance** | CI SAST report confirming zero platform imports in shared module on release build                                                                   | Block if any found                           |
| **MASVS mobile controls active**      | Confirm certificate pinning, Keychain/Keystore storage, and obfuscation active in release build (complement to David Okonkwo's platform-level gate) | Block if inactive                            |
| **Feature parity confirmation**       | Feature parity log signed by Android Chapter Lead and iOS Chapter Lead                                                                              | Block if parity gap >0 undocumented features |
| **No Trim-to-Pass**                   | Confirm no features, security controls, or accessibility requirements were disabled to pass Stage 6 or Stage 7                                      | P0 if any discovered — non-overridable       |

### Escalation Path

Any item Marcus blocks at Stage 8 is escalated to the CTO (Dr. Kenji Nakamura) within 4 hours. Marcus provides a written impact assessment and remediation estimate. The CTO holds final Stage 8 sign-off authority.

## Quality Standards

- All shared KMP code must have unit test coverage ≥85%
- Platform-specific code must have test coverage ≥75%
- Build time must not exceed 8 minutes for clean build on CI
- Crash-free rate target: ≥99.9% for all production releases (≥99.95% at Beta rollout)
- Feature parity gap must not exceed 1 sprint between platforms
- No platform SDK imports allowed in shared KMP module
- Stage 6 defect filings include full code path, test case, and impact assessment — no verbal-only findings
- Stage 8 sign-off memo delivered to CTO within 24 hours of review completion
