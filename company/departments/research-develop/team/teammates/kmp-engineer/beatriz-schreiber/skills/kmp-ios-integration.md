---
name: kmp-ios-integration
description: Kotlin/Native iOS integration for KMP shared modules. Use when designing the Swift-compatible API surface of a KMP module, packaging and distributing KMP XCFrameworks via CocoaPods or Swift Package Manager, resolving Kotlin/Native memory model issues on iOS, writing iOS-side tests for shared modules, or advising on best practices for making KMP code feel idiomatic to Swift and iOS consumers.
version: "1.0.0"
---

# KMP iOS Integration

## Purpose

KMP's greatest value — sharing business logic across Android and iOS — is realised only if the iOS integration is correct. A poorly designed Swift API surface forces iOS engineers to write idiomatic Swift wrappers around every KMP module, erasing the sharing benefit. A Kotlin/Native memory issue crashes the iOS app in ways that are invisible in Android unit tests. This skill ensures that KMP shared modules integrate correctly, safely, and idiomatically with iOS.

---

## Swift API Surface Design

### Naming and Visibility

Kotlin names do not map cleanly to Swift without annotation. Apply these rules to every KMP module's public API:

| Scenario                          | Kotlin                       | Swift-Friendly Annotation             | Result in Swift                         |
| --------------------------------- | ---------------------------- | ------------------------------------- | --------------------------------------- |
| Class with Kotlin name            | `class UserRepository`       | None needed                           | `UserRepository` (fine)                 |
| Function with Kotlin convention   | `fun getUserById(id: Long)`  | `@ObjCName("getUserById")` if needed  | Predictable Swift name                  |
| Property clash with Swift keyword | `val `description`: String`  | Avoid or rename                       | Swift `description` is ambiguous        |
| Generic class                     | `class Result<T>`            | Limited — generics are erased in ObjC | Use sealed class hierarchy instead      |
| Extension function                | `fun List<User>.filter(...)` | Not accessible directly               | Wrap in companion or top-level function |

**Key principle:** Design the KMP public API with the iOS consumer in mind from the start. It is far cheaper to add `@ObjCName` annotations and avoid generics upfront than to discover the Swift API is unusable after Android implementation is complete.

### Sealed Classes vs. Enums

Prefer Kotlin sealed classes over enums when the iOS consumer needs associated values (equivalent to Swift enums with associated values). KMP sealed classes map to Swift as a class hierarchy, which Swift engineers can use with `switch` statements.

```kotlin
// Good: sealed class for state machine
sealed class NetworkState {
    object Loading : NetworkState()
    data class Success(val data: String) : NetworkState()
    data class Error(val message: String) : NetworkState()
}
```

On Swift:

```swift
switch state {
case is NetworkState.Loading: ...
case let success as NetworkState.Success: ...
case let error as NetworkState.Error: ...
}
```

---

## XCFramework Distribution

### Build Pipeline

Produce multi-architecture XCFrameworks using the `XCFramework` Gradle task. The pipeline must produce:

- `arm64` for physical iOS device
- `x86_64` and `arm64` for iOS simulator (for Rosetta and Apple Silicon macs respectively)

```kotlin
// build.gradle.kts (shared module)
kotlin {
    val xcFramework = XCFramework("SharedKit")
    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach {
        it.binaries.framework {
            baseName = "SharedKit"
            xcFramework.add(this)
        }
    }
}
```

Run `./gradlew assembleSharedKitXCFramework` to produce the fat XCFramework.

### Distribution Options

| Method                          | When to Use                                             | Key Steps                                                                                         |
| ------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Swift Package Manager (SPM)** | Preferred for new projects; clean dependency management | Create `Package.swift` referencing the XCFramework; publish to a git tag; consumers add via Xcode |
| **CocoaPods**                   | Required if the iOS project already uses CocoaPods      | Create `.podspec`; publish to CocoaPods Trunk or private spec repo                                |
| **Manual XCFramework**          | Small teams, rapid prototyping                          | Drag XCFramework into Xcode project; link binary with libraries                                   |

---

## Kotlin/Native Memory Model

### Current Model (Kotlin 1.9+)

The new Kotlin/Native memory model (enabled by default since 1.7.20) uses a garbage collector compatible with object sharing across threads. Under the new model:

- Objects can be shared between threads without freezing
- The `freeze()` API is a no-op and deprecated
- Coroutines work correctly across threads without the `newSuspendedCoroutine` workarounds

### Common iOS Memory Issues (Post-New-MM)

Even under the new model, watch for:

1. **Retain cycles with ObjC/Swift closures** — Kotlin lambdas passed to Swift as closures can create retain cycles. Prefer weak references or redesign the API to avoid closure capture of the Kotlin object.

2. **Main thread enforcement** — iOS UI-touching code must run on the main thread. KMP coroutines should use `Dispatchers.Main` for any result that triggers UI updates. Verify `Dispatchers.Main` is correctly provided via `kotlinx-coroutines-core` on iOS.

3. **Autoreleasepool** — Long-running Kotlin loops on iOS that allocate many ObjC objects should wrap the loop body in `autoreleasepool {}` to prevent memory pressure buildup.

---

## iOS-Side Testing for KMP Modules

### `iosTest` Source Set

Write `kotlin.test`-based tests in the `iosTest` source set. These run natively on iOS simulators via the Kotlin/Native test runner. This catches:

- Memory model issues invisible to JVM tests
- Missing `Dispatchers.Main` provider
- Retain cycle or leak issues

### XCTest Integration

For testing the Swift API surface (what the iOS app actually uses), write XCTest tests that exercise the Swift-facing API of the KMP module. This verifies:

- Naming is as expected by iOS consumers
- Coroutine-to-callback bridging works
- Sealed class hierarchies are usable in Swift switch statements
- Error handling surfaces Kotlin exceptions as expected NSError objects

---

## Output Standards

- Every KMP module must have an `iosTest` source set with tests covering the primary business logic paths before shipping.
- XCFramework builds must be verified on both device (`arm64`) and simulator targets before declaring a release ready.
- Any Swift API surface change must be reviewed by an iOS engineer (Seo-Yeon Park or iOS team) before merging.
