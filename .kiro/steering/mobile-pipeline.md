---
inclusion: fileMatch
fileMatchPattern: "**/mobile-development/**"
---

# Mobile Development Pipeline — Platform-Specific Rules

**Authority:** AGENTS.md § 4.4 + `company/pipeline/mobile-development/pipeline.md`  
**Applies To:** Android and iOS mobile application development

---

## Mobile Pipeline Overview

The mobile development pipeline follows the standard 13-stage company pipeline with mobile-specific requirements and deliverables.

## Platform Coverage

- **Android** — Kotlin, Jetpack Compose, Material Design 3
- **iOS** — Swift, SwiftUI, Human Interface Guidelines
- **Cross-Platform** — Kotlin Multiplatform (KMP), Flutter (when approved)

## Stage-Specific Mobile Requirements

### Stage 1: Requirements → PRD + SRD

**Mobile-Specific PRD Sections:**

- Platform support (Android, iOS, or both)
- Minimum OS versions (Android API level, iOS version)
- Device form factors (phone, tablet, foldable)
- Offline functionality requirements
- Push notification requirements
- Deep linking and app linking requirements

**Mobile-Specific SRD Sections:**

- Mobile platform security (OWASP MASVS compliance)
- Biometric authentication requirements
- Secure storage (Keychain, Keystore)
- Certificate pinning requirements
- Mobile-specific threat model

### Stage 2: PRD → Web Prototype + IDS

**Mobile Design Requirements:**

- Responsive layouts for multiple screen sizes
- Platform-specific design patterns (Material Design 3 / HIG)
- Touch target sizes (minimum 48dp / 44pt)
- Gesture interactions
- Navigation patterns (bottom nav, tab bar, drawer)
- Dark mode support

### Stage 3: Prototype → UML Engineering Package

**Mobile Architecture Decisions:**

- **ADR Required:** Platform selection (Native, KMP, Flutter)
- **ADR Required:** Architecture pattern (MVVM, MVI, Clean Architecture)
- **ADR Required:** Dependency injection framework
- **ADR Required:** Networking library
- **ADR Required:** Local storage solution
- **TSD Required:** Complete technology stack justification

**Mobile-Specific UML:**

- App architecture diagram
- Navigation flow diagram
- Data flow diagram (local + remote)
- Module dependency graph

### Stage 4: UML → Implementation Plan + Gantt

**Mobile-Specific Tasks:**

- Platform-specific module setup
- Build configuration (Gradle, Xcode project)
- CI/CD pipeline setup (Android: GitHub Actions, iOS: Xcode Cloud)
- Code signing and provisioning profiles
- App store preparation

### Stage 5: Plan → Software Development

**Mobile Development Standards:**

- Follow platform-specific style guides
- Implement proper lifecycle management
- Handle configuration changes (Android)
- Implement proper memory management
- Support accessibility features
- Implement proper error handling

### Stage 6: Development → Arch. & Conformance Review

**Mobile-Specific Review Criteria:**

- Platform design guideline compliance
- Performance benchmarks (startup time, frame rate)
- Battery usage optimization
- Network efficiency
- APK/IPA size optimization
- Accessibility compliance

### Stage 7: Arch. Review → Automated Testing

**Mobile Testing Requirements:**

- Unit tests (minimum 80% coverage)
- UI tests (critical user flows)
- Integration tests (API + local storage)
- Screenshot tests (visual regression)
- Performance tests (startup, memory, battery)
- Accessibility tests

**Testing Frameworks:**

- **Android:** JUnit, Espresso, Robolectric, Compose Testing
- **iOS:** XCTest, XCUITest, Quick/Nimble

### Stage 8: Testing → Integrity Verification

**Mobile-Specific Integrity Checks:**

- OWASP MASVS compliance verification
- ProGuard/R8 obfuscation (Android)
- Code signing verification
- API key security audit
- SSL/TLS certificate validation
- Biometric authentication security

### Stage 9: Integrity Verification → Translation Production

**Mobile Localization:**

- String resources externalized (strings.xml, Localizable.strings)
- RTL layout support
- Locale-specific formatting (dates, numbers, currency)
- Image asset localization
- App store metadata translation

### Stage 10: Translation Production → Release Readiness Check

**Mobile Release Checklist:**

- App store assets prepared (screenshots, descriptions, icons)
- Privacy policy and terms of service links
- App store compliance review
- Beta testing completed (TestFlight, Google Play Beta)
- Crash reporting configured (Firebase Crashlytics)
- Analytics configured

### Stage 11: Live Operations

**Mobile Live Ops:**

- App store monitoring (ratings, reviews)
- Crash rate monitoring (< 1% crash-free sessions)
- Performance monitoring (Firebase Performance, App Center)
- A/B testing and feature flags
- Push notification campaigns
- App store optimization (ASO)

## Mobile-Specific Technology Lock Rules

**Locked at Stage 3:**

- Platform choice (Native Android, Native iOS, KMP, Flutter)
- Architecture pattern (MVVM, MVI, Clean Architecture)
- Dependency injection framework
- Networking library
- Local storage solution
- Navigation library

**Cannot be changed after Stage 3 approval without full re-entry.**

## Mobile-Specific Defect Severity

**P0 (Blocks Release):**

- App crashes on launch
- Data loss or corruption
- Security vulnerability (OWASP MASVS failure)
- Payment processing failure
- Biometric authentication bypass

**P1 (Blocks Release):**

- Core feature non-functional
- Navigation broken
- Critical UI rendering issue
- Offline mode failure
- Push notifications not working

## Platform-Specific Resources

**Android:**

- Material Design 3: https://m3.material.io/
- Android Developer Docs: https://developer.android.com/
- Jetpack Compose: https://developer.android.com/jetpack/compose

**iOS:**

- Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
- iOS Developer Docs: https://developer.apple.com/documentation/
- SwiftUI: https://developer.apple.com/xcode/swiftui/

## Related Steering Files

- `company-pipeline-overview.md` — Core 13-stage pipeline
- `android-development.md` — Android-specific patterns (manual)
- `ios-development.md` — iOS-specific patterns (manual)
- `cross-platform-development.md` — KMP/Flutter patterns (manual)
