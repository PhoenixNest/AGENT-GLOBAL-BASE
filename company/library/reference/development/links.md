# Development Reference Library

Reference resources for the R&D Department and relevant personnel. Organized by platform and domain. Use these materials to stay current with official APIs, patterns, and security standards.

---

## Google Android

- [Kotlin for Android — Getting Started](https://developer.android.com/kotlin/first)
  Official guide for using Kotlin on Android. Entry point for Android development setup and Kotlin language fundamentals.

- [Android API Reference — Packages](https://developer.android.com/reference/packages)
  Comprehensive reference for all Android SDK packages, classes, and methods. The authoritative source for API signatures and behaviour.

- [Android Jetpack Compose — Documentation](https://developer.android.com/develop/ui/compose/documentation)
  Official Compose UI documentation covering layouts, state, theming, animation, and testing. The current standard for Android UI development.

- [Jetpack Compose Architecture Guide](https://developer.android.com/jetpack/compose/architecture)
  Unidirectional Data Flow (UDF) pattern, ViewModel integration, state management, and composable lifecycle. Required reading for Compose-based Android projects.

- [Android Accessibility — Developer Guide](https://developer.android.com/guide/topics/ui/accessibility)
  Semantic modifiers for Compose, touch target requirements, TalkBack testing, Dynamic Type and contrast support. Covers Android 16 accessibility updates.

---

## Apple iOS

- [Swift — Official Language Overview](https://developer.apple.com/swift/)
  Language reference and resources for Swift 6. Ensure code examples use Swift 6 concurrency and the `@Observable` macro (not the older `ObservableObject` / `@Published` patterns).

- [SwiftUI — Framework Documentation](https://developer.apple.com/documentation/swiftui/)
  Primary reference for all SwiftUI views, modifiers, and frameworks. Updated alongside Xcode and iOS releases.

- [SwiftUI — Official Tutorials](https://developer.apple.com/tutorials/swiftui/)
  Curated learning path with tutorials, articles, and sample projects. Targets modern Swift 6 + Xcode 26 patterns.

- [Develop in Swift — Tutorials](https://developer.apple.com/tutorials/develop-in-swift)
  Apple's guided learning path for building apps with Swift and Xcode. Most reliable source for up-to-date best practices.

- [Apple Developer Design Resources](https://developer.apple.com/design/resources/)
  Figma and Sketch templates, SF Pro fonts, SF Symbols library. Also the source for Human Interface Guidelines.

---

## JetBrains Kotlin Multiplatform (KMP)

- [KMP Overview](https://kotlinlang.org/docs/multiplatform/kmp-overview.html)
  Introduction to Kotlin Multiplatform: shared code across Android, iOS, and other targets.

- [KMP Quickstart](https://kotlinlang.org/docs/multiplatform-get-started.html)
  Environment setup (IDE plugins, Android SDK, Xcode), project creation wizard, and troubleshooting. Start here for new KMP projects.

- [Compose Multiplatform — Documentation](https://www.jetbrains.com/compose-multiplatform/)
  Share UI code across Android, iOS, and desktop using Compose. Covers shared ViewModel patterns, Dependency Injection, and architecture for multi-platform projects.

- [KMP Learning Resources](https://kotlinlang.org/docs/multiplatform-resources.html)
  Curated resources by experience level: Beginner (Room, Ktor, SQLDelight), Intermediate (architecture patterns), Advanced (scaling, multi-team), and Library Authors (publishing KMP libraries).

---

## Google Flutter

- [Flutter — Quick Start](https://docs.flutter.dev/install/quick)
  Installation and environment setup for Windows, macOS, Linux, and ChromeOS. Entry point for new Flutter environments.

- [Flutter Widget Catalog](https://docs.flutter.dev/reference/widgets)
  All widgets organized by category and design system (Material 3, Cupertino). Covers Layout, Input, Animation, Assets, and Async widget families.

- [Flutter Cookbook](https://docs.flutter.dev/cookbook)
  Practical recipes for common real-world problems: lists, networking, persistence, navigation, and testing. Use for implementation questions.

- [Flutter API Reference](https://api.flutter.dev/)
  Complete reference documentation for all Flutter framework classes, methods, and libraries. The authoritative source for API signatures.

---

## Security

- [OWASP Mobile Application Security — mas.owasp.org](https://mas.owasp.org/)
  Official hub for mobile application security standards. Contains two primary resources:
  - **MASVS** (Mobile Application Security Verification Standard) — defines security requirements the app must meet
  - **MASTG** (Mobile Application Security Testing Guide) — comprehensive manual for testing those requirements

  > OWASP MAS is a living document updated continuously. Always refer to the official site for current guidance. The v2.0 refactor (2023) introduced MAS Testing Profiles and NIST OSCAL alignment.

- [Android Keystore System](https://developer.android.com/privacy-and-security/keystore)
  Official guide for cryptographic key storage on Android. Required for all sensitive credential handling per the SRD.

- [iOS Security — Keychain Services](https://developer.apple.com/documentation/security/keychain_services)
  Official API reference for iOS Keychain. Required for all sensitive credential and token storage on iOS per the SRD.
