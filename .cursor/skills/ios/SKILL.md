---
name: ios
description: Use for iOS platform development — SwiftUI, Swift Concurrency, The Composable Architecture (TCA), UIKit + Combine, testing, accessibility, performance profiling, and App Store submission. Covers iOS Lead (Seo-Yeon Park) and the iOS engineering team.
---

# iOS

## Overview

iOS platform engineering using modern Swift-based tooling. Owned by the iOS Development Lead (Seo-Yeon Park). All iOS code follows SwiftUI-first with Swift Concurrency, with UIKit + Combine for legacy codebase maintenance.

## Sub-Guidelines

### UI & UX

| Guideline            | File                                                             | Owner            |
| -------------------- | ---------------------------------------------------------------- | ---------------- |
| SwiftUI              | [`ui-ux/swiftui.md`](ui-ux/swiftui.md)                           | Camila Rodriguez |
| UIKit + Combine      | [`ui-ux/uikit-combine.md`](ui-ux/uikit-combine.md)               | Hiroshi Tanaka   |
| WidgetKit Extensions | [`ui-ux/widgetkit-extensions.md`](ui-ux/widgetkit-extensions.md) | Camila Rodriguez |

### Architecture

| Guideline          | File                                                                       | Owner         |
| ------------------ | -------------------------------------------------------------------------- | ------------- |
| Swift Concurrency  | [`architecture/swift-concurrency.md`](architecture/swift-concurrency.md)   | Lars Eriksson |
| TCA Architecture   | [`architecture/tca-architecture.md`](architecture/tca-architecture.md)     | Lars Eriksson |
| UIKit Architecture | [`architecture/uikit-architecture.md`](architecture/uikit-architecture.md) | Lars Eriksson |

### Data & Networking

| Guideline        | File                                                                                                 | Owner          |
| ---------------- | ---------------------------------------------------------------------------------------------------- | -------------- |
| Core Data        | [`data-networking/core-data.md`](data-networking/core-data.md)                                       | Hiroshi Tanaka |
| iOS Networking   | [`data-networking/ios-networking.md`](data-networking/ios-networking.md)                             | Amara Diallo   |
| Combine Reactive | [`data-networking/combine-reactive-programming.md`](data-networking/combine-reactive-programming.md) | Amara Diallo   |

### Testing & Quality

| Guideline         | File                                                                           | Owner       |
| ----------------- | ------------------------------------------------------------------------------ | ----------- |
| iOS Testing       | [`testing-quality/ios-testing.md`](testing-quality/ios-testing.md)             | Arjun Mehta |
| iOS Accessibility | [`testing-quality/ios-accessibility.md`](testing-quality/ios-accessibility.md) | Arjun Mehta |

### Infrastructure

| Guideline          | File                                                                           | Owner         |
| ------------------ | ------------------------------------------------------------------------------ | ------------- |
| iOS Implementation | [`infrastructure/ios-implementation.md`](infrastructure/ios-implementation.md) | Seo-Yeon Park |
| iOS CI/CD          | [`infrastructure/ios-ci-cd.md`](infrastructure/ios-ci-cd.md)                   | Amara Diallo  |
| iOS Performance    | [`infrastructure/ios-performance.md`](infrastructure/ios-performance.md)       | Mei Chen      |
| Core Animation     | [`infrastructure/core-animation.md`](infrastructure/core-animation.md)         | Mei Chen      |
