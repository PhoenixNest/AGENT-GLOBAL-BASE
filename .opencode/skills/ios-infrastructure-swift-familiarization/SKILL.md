---
name: ios-infrastructure-swift-familiarization
description: "Swift language fundamentals for cross-platform engineers transitioning to iOS — value vs reference types, optionals, async/await, actors, app lifecycle, and KMP interoperability. Owned by Seo-Yeon Park (iOS Lead). Use when onboarding KMP/Flutter engineers to iOS codebase or reading Swift adapter code. Trigger: swift basics, swift fundamentals, swift language, optionals, value types, reference types, swift for kotlin, swift for flutter, kmp ios adapter, expect actual."
prerequisites:
  - ios-overview

version: "1.0.0"
---

# Swift Familiarization

## Overview

This skill provides Swift language fundamentals, concurrency patterns, and iOS platform awareness for engineers coming from other languages or cross-platform frameworks (KMP, Flutter). It enables KMP engineers to understand iOS platform-specific implementations, read Swift code in shared module adapters, and participate effectively in cross-platform architecture decisions.

## Swift Language Fundamentals

**Core syntax**:

```swift
// Value types (structs) — preferred for data models
struct User {
    let id: UUID
    var name: String
    let email: String
}

// Reference types (classes) — for identity and shared state
class UserService {
    static let shared = UserService()
    private init() {}
    private var cache: [UUID: User] = [:]
}

// Optionals — Swift's null safety
let optionalValue: String? = nil
if let value = optionalValue {
    print(value)
}
let defaultValue = optionalValue ?? "default"
```

## Swift Concurrency

**async/await**:

```swift
func fetchUserData(userId: UUID) async throws -> User {
    async let user = userRepository.fetch(id: userId)
    async let preferences = prefsRepository.fetch(userId: userId)
    let (u, p) = try await (user, preferences)
    return User(data: u, preferences: p)
}
```

**Actors for thread safety**:

```swift
actor Cache {
    private var storage: [String: Any] = [:]
    func get(_ key: String) -> Any? { storage[key] }
    func set(_ key: String, value: Any) { storage[key] = value }
}
```

## iOS Platform Awareness

**App lifecycle**: `UIApplicationDelegate` for launch/background/termination, `UISceneDelegate` for multi-window.

**Platform conventions**: NavigationStack (iOS 16+), Human Interface Guidelines, dynamic type, Dark Mode, accessibility.

**Interoperability with KMP**: KMP shared code exposed via Kotlin/Native Swift bindings, expect/actual pattern for platform-specific behavior, coroutines to Swift async/await mapping.

## Common Pitfalls

- **Strong reference cycles**: Use `[weak self]` in closures capturing self.
- **Main thread violations**: UI updates must be on main thread — use `@MainActor`.
- **Optional force-unwrap**: Avoid `!` — use `if let`, `guard let`, or `??`.
- **Equatable/Hashable**: Implement for custom types used in Sets or Dictionary keys.
