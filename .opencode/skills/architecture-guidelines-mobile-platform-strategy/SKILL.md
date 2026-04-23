---
name: architecture-guidelines-mobile-platform-strategy
description: 'Architecture skill: Mobile Platform Strategy'
---

# Mobile Platform Strategy

## Purpose

Own all mobile engineering execution across Android, iOS, and cross-platform teams. Translate the Coding Implementation Plan and UML Engineering Package into platform-specific development plans, enforce architectural coherence across 30+ mobile engineers, and deliver at consumer scale (500M+ MAU, 99.9% crash-free rate, sub-400ms perceived latency).

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

## Quality Standards

- All shared KMP code must have unit test coverage ≥85%
- Platform-specific code must have test coverage ≥75%
- Build time must not exceed 8 minutes for clean build on CI
- Crash-free rate target: ≥99.9% for all production releases
- Feature parity gap must not exceed 1 sprint between platforms
- No platform SDK imports allowed in shared KMP module
