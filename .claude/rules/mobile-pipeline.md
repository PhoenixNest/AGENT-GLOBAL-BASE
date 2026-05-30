---
paths:
  - "**/mobile-development/**"
description: Mobile development pipeline platform-specific rules
---

# Mobile Development Pipeline — Platform-Specific Rules

**Applies To:** Android and iOS mobile application development

---

## Platform Coverage

- **Android** — Kotlin, Jetpack Compose, Material Design 3
- **iOS** — Swift, SwiftUI, Human Interface Guidelines
- **Cross-Platform** — Kotlin Multiplatform (KMP), Flutter (when approved)

---

## Stage-Specific Mobile Requirements

### Stage 1 — PRD + SRD

Mobile PRD: platform support, minimum OS versions, device form factors, offline/push/deep linking requirements.

Mobile SRD: OWASP MASVS compliance, biometric auth, secure storage, certificate pinning, threat model.

### Stage 2 — Prototype + IDS

Responsive layouts, platform-specific design (Material Design 3 / HIG), touch targets (48dp / 44pt), dark mode.

### Stage 3 — UML Engineering Package

**ADRs required:** Platform selection, architecture pattern (MVVM/MVI/Clean), DI framework, networking library, local storage.

### Stage 7 — Automated Testing

- Unit tests: minimum 80% coverage
- UI tests: critical flows
- Frameworks: JUnit/Espresso (Android), XCTest/XCUITest (iOS)

### Stage 8 — Integrity Verification

OWASP MASVS compliance, ProGuard/R8 obfuscation, code signing, API key security audit, SSL/TLS validation.

---

## Mobile P0 Defects (Block Release)

- App crashes on launch
- Data loss or corruption
- Security vulnerability (OWASP MASVS failure)
- Payment processing failure
- Biometric authentication bypass

---

## Mobile Technology Lock (Stage 3)

Locked: platform choice, architecture pattern, DI framework, networking library, local storage, navigation library.
