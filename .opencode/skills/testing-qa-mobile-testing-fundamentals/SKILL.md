---
name: testing-qa-mobile-testing-fundamentals
description: Mobile testing fundamentals — test pyramid architecture, platform-specific testing patterns (iOS/Android), test-driven development for mobile, mocking strategies, and testing lifecycle management for mobile application development. Owned by Priscilla Oduya (Test Lead). Use during Stage 4 (Implementation Plan) for test architecture design and Stage 5 (Development) for testing fundamentals implementation. Trigger: mobile testing fundamentals, test pyramid, platform testing patterns, TDD mobile, mocking strategies, test lifecycle, iOS testing, Android testing.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
---

# Mobile Testing Fundamentals

## Overview

This skill provides foundational knowledge for mobile testing across all platforms in the company's pipeline. It establishes the principles, strategies, and practices that underpin comprehensive mobile quality assurance, serving as the basis for more specialized testing skills (unit testing, integration testing, E2E testing, etc.).

Mobile application testing is inherently more complex than web testing due to:

- **Platform fragmentation** — multiple OS versions, device form factors, screen densities
- **Network variability** — cellular, Wi-Fi, offline transitions, flaky connectivity
- **Hardware diversity** — cameras, GPS, biometrics, sensors, NFC, Bluetooth
- **App lifecycle management** — backgrounding, foregrounding, process death, memory pressure
- **App store constraints** — review processes, binary size limits, privacy manifests

### The Mobile Test Pyramid

```
                    ┌─────────────┐
                    │   Manual    │        ← Exploratory, usability, ad-hoc
                    │  Testing    │
                ┌───┴─────────────┴───┐
                │    E2E / UI Tests   │    ← Few (slow, brittle, expensive)
            ┌───┴─────────────────────┴───┐
            │    Integration Tests        │  ← Some (network, DB, platform APIs)
        ┌───┴─────────────────────────────┴───┐
        │         Unit Tests                  │  ← Many (fast, cheap, reliable)
        └─────────────────────────────────────┘
```

| Layer             | Scope                 | Execution Speed | Maintenance Cost | Recommended % |
| ----------------- | --------------------- | --------------- | ---------------- | ------------- |
| Unit Tests        | Single class/function | Milliseconds    | Low              | 60–70%        |
| Integration Tests | Module interactions   | Seconds         | Medium           | 20–30%        |
| E2E / UI Tests    | Full user flows       | Minutes         | High             | 5–10%         |
| Manual Testing    | Exploratory, UX       | Variable        | Very High        | 1–5%          |

**Principle:** Push tests as far down the pyramid as possible. A unit test that validates business logic is preferable to an E2E test that does the same — faster execution, clearer failure signals, lower flakiness.

---

## Device Coverage Strategy

### Real Devices vs. Emulators/Simulators

| Dimension         | Emulators/Simulators              | Real Devices               |
| ----------------- | --------------------------------- | -------------------------- |
| Speed             | Fast spin-up                      | Physical handling required |
| Cost              | Free                              | Purchase/rent device farm  |
| Accuracy          | Good for logic, poor for hardware | Exact user experience      |
| Sensor Testing    | Simulated (often inaccurate)      | Real sensors               |
| Network Testing   | Throttle simulation               | Real cellular/Wi-Fi        |
| Battery Testing   | Not possible                      | Accurate drain measurement |
| Memory Pressure   | Simulated                         | Real OS behavior           |
| Biometric Testing | Limited support                   | Real fingerprint/Face ID   |

**Strategy:**

```
Development Phase (Local):
  ├── Android Emulator (API 28–35, various form factors)
  └── iOS Simulator (iPhone SE, iPhone 15, iPad)

CI/CD Phase (Automated):
  ├── Emulator/Simulator for unit + integration tests
  └── Device farm for critical E2E smoke tests

Release Phase (Validation):
  ├── Physical device lab for regression suite
  ├── Beta testers for real-world validation
  └── Dogfooding (team uses app daily)
```

### Device Farm Options

| Service                 | Platforms    | Pricing               | Integration             |
| ----------------------- | ------------ | --------------------- | ----------------------- |
| Firebase Test Lab       | Android, iOS | Pay-per-minute        | Gradle plugin, Fastlane |
| AWS Device Farm         | Android, iOS | Pay-per-device-minute | CLI, Fastlane           |
| BrowserStack App Live   | Android, iOS | Subscription          | REST API, Fastlane      |
| Sauce Labs              | Android, iOS | Subscription          | REST API, Fastlane      |
| Bitrise Virtual Devices | Android, iOS | Included in tier      | Native in Bitrise CI    |

### OS Version Matrix

**Android Matrix (per Play Store distribution):**

| Android Version | API Level | Coverage Target                 |
| --------------- | --------- | ------------------------------- |
| Android 10      | 29        | Minimum supported               |
| Android 11      | 30        | Test on emulators               |
| Android 12      | 31        | Test on emulators + device farm |
| Android 13      | 33        | Test on emulators + device farm |
| Android 14      | 34        | Primary test target             |
| Android 15      | 35        | Early testing (beta/stable)     |

**iOS Matrix (per Apple guidelines):**

| iOS Version | Minimum Devices | Coverage Target                 |
| ----------- | --------------- | ------------------------------- |
| iOS 16      | iPhone 8 Plus   | Minimum supported               |
| iOS 17      | iPhone 12+      | Test on simulator + device farm |
| iOS 18      | iPhone 15+      | Primary test target             |

**Rule:** Support current OS + 2 previous versions minimum. Test on minimum supported version + latest version + one intermediate.

---

## Cross-Platform Testing

### Framework Comparison

| Framework            | Platform            | Best For                                 | Limitations                            |
| -------------------- | ------------------- | ---------------------------------------- | -------------------------------------- |
| **Espresso**         | Android             | Native UI testing, fast on-device        | Android only, requires Kotlin/Java     |
| **XCUITest**         | iOS                 | Native UI testing, integrated with Xcode | iOS only, requires Swift/Obj-C         |
| **Compose Testing**  | Android             | Compose UI testing                       | Compose only, Android only             |
| **Swift UI Testing** | iOS                 | SwiftUI preview testing                  | SwiftUI only, iOS 16+                  |
| **Maestro**          | Android + iOS       | Cross-platform E2E, YAML-based           | Limited logic in YAML, no unit testing |
| **Appium**           | Android + iOS + Web | Cross-platform, multi-language           | Slower, more setup, flakier            |
| **Detox**            | React Native        | RN E2E testing                           | RN only, complex setup                 |
| **integration_test** | Flutter             | Flutter E2E testing                      | Flutter only                           |
| **flutter_test**     | Flutter             | Flutter widget/unit testing              | Flutter only                           |

### Choosing the Right Tool

```
Test Need                          → Recommended Tool
─────────────────────────────────────────────────────
Android unit test                  → JUnit 5 + Mockito + Robolectric
Android Compose UI test            → Compose Testing
Android View system UI test        → Espresso
iOS unit test                      → XCTest + Swift Testing
iOS SwiftUI test                   → XCUITest
Cross-platform E2E flow            → Maestro (preferred) or Appium
KMP shared module test             → JUnit 5 (runs on JVM)
Flutter widget test                → flutter_test
Flutter integration test           → integration_test
Accessibility audit                → Espresso A11y + XCUITest A11y
Performance benchmark              → Macrobenchmark (Android) / XCTMeasure (iOS)
```

### Cross-Platform E2E with Maestro

Maestro is the recommended cross-platform E2E testing tool because:

- Single YAML file defines tests for both Android and iOS
- Fast execution (no WebDriver overhead like Appium)
- Built-in error handling and retries
- Easy CI/CD integration
- Hot reload during development

```yaml
# flows/complete-purchase.yaml
appId: com.company.app
name: Complete Purchase Flow
tags:
  - smoke
  - purchase
---
- launchApp
- runFlow: login.yaml
- tapOn: "Products"
- tapOn:
    id: "product_card_1"
- tapOn: "Add to Cart"
- assertVisible:
    id: "cart_badge"
    text: "1"
- tapOn:
    id: "cart_button"
- assertVisible: "Cart"
- assertVisible:
    id: "item_name"
    text: "Test Product"
- tapOn: "Checkout"
- tapOn: "Confirm Purchase"
- assertVisible: "Purchase Successful"
- assertVisible:
    text: "Order confirmed"
- tapOn: "Back to Home"
- assertVisible: "Dashboard"
```

**Running Maestro Tests:**

```bash
# Run all tests
maestro test flows/

# Run specific test
maestro test flows/complete-purchase.yaml

# Run against specific device
maestro test flows/ --device-id "Pixel 7"

# Generate test from recording
maestro record flows/
```

---

## Defect Reporting

### Defect Severity Classification

All defects must be classified using the P0–P3 system per company pipeline rules:

| Level  | Definition                              | Release Impact                  | Example                                      |
| ------ | --------------------------------------- | ------------------------------- | -------------------------------------------- |
| **P0** | App crash / data loss / security breach | Blocks release — non-negotiable | App crashes on launch, user data exposed     |
| **P1** | Core feature broken / major UX failure  | Blocks release — non-negotiable | Login fails, checkout broken                 |
| **P2** | Minor feature degraded / cosmetic issue | User decides to fix or defer    | Wrong icon, minor alignment issue            |
| **P3** | Polish / nice-to-have                   | User decides to fix or defer    | Typo in error message, slight color mismatch |

### Defect Report Structure

```markdown
# Defect Report — [Project Name]

## Defect Summary

| ID    | Title                                | Severity | Status | Assigned To  |
| ----- | ------------------------------------ | -------- | ------ | ------------ |
| D-001 | App crashes on deep link navigation  | P0       | Open   | Android Lead |
| D-002 | Login button misaligned on iPhone SE | P2       | Open   | iOS Lead     |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`test-types.md`](references/test-types.md) — Test Types
- [`test-data-management.md`](references/test-data-management.md) — Test Data Management
- [`flaky-test-prevention.md`](references/flaky-test-prevention.md) — Flaky Test Prevention
- [`ci-cd-integration.md`](references/ci-cd-integration.md) — CI/CD Integration
- [`defect-details.md`](references/defect-details.md) — Defect Details
- [`quality-gates.md`](references/quality-gates.md) — Quality Gates
- [`stage-7-integration.md`](references/stage-7-integration.md) — Stage 7 Integration
- [`references.md`](references/references.md) — References
```
