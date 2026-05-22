---
name: kmp-ios-integration
description: Design and implement Kotlin/Native iOS integration for KMP shared modules — including Swift-compatible API surfaces, XCFramework distribution, Kotlin/Native GC model management, and iOS-side integration testing.
version: "1.0.0"
---

# KMP iOS Integration

| Competency               | Description                                                          | Quality Criteria                                                                                        |
| ------------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Swift API Surface Design | Design the Objective-C/Swift-compatible API surface for KMP modules  | All public APIs use `@ObjCName`; no Kotlin generics exposed directly; Swift consumers use idiomatic API |
| Kotlin/Native GC Model   | Manage memory and threading for Kotlin/Native on iOS                 | No `@Throws` on every function; correct `Dispatchers.Main` usage; GC migration complete                 |
| XCFramework Distribution | Build and distribute KMP modules as XCFramework via CocoaPods or SPM | Multi-arch build (arm64 device + x86_64/arm64 simulator); integration time ≤ 3 hours for consumers      |
| iOS-Side Testing         | Write and maintain iOS integration tests for KMP shared modules      | `iosTest` source set populated; XCTest wrapper exercising Swift API surface; no hidden memory issues    |

## Execution Guidance

### Swift API Surface Design Rules

```kotlin
// BAD: Exposes Kotlin-style generic — not idiomatic in Swift
fun <T> fetchData(id: String): Flow<T>

// GOOD: Use @ObjCName and concrete types
@ObjCName("fetchUserData")
fun fetchUserData(id: String): Flow<UserState>

// BAD: suspend function without wrapper
suspend fun loadProfile(): Profile

// GOOD: Wrap suspend in Swift-friendly callback bridge
fun loadProfile(onResult: (Profile?, Throwable?) -> Unit) {
    scope.launch {
        runCatching { loadProfileInternal() }
            .onSuccess { onResult(it, null) }
            .onFailure { onResult(null, it) }
    }
}
```

### Kotlin/Native Threading Rules

| Rule                                                 | Rationale                                                   |
| ---------------------------------------------------- | ----------------------------------------------------------- |
| All UI callbacks must dispatch to `Dispatchers.Main` | iOS UI must update on the main thread                       |
| `StateFlow` must be collected via `iosMain` helper   | Direct Swift coroutine collection requires SKIE or wrapper  |
| Do not share mutable state without `@Immutable`      | Kotlin/Native GC model requires careful threading           |
| `SupervisorJob` scope in `iosMain`                   | Prevents one child failure from cancelling the entire scope |

### XCFramework Build Pipeline

```gradle
// shared/build.gradle.kts
kotlin {
    iosArm64()
    iosX64()
    iosSimulatorArm64()
}

tasks.register<FatFrameworkTask>("buildXCFramework") {
    from(
        kotlin.targets.withType<KotlinNativeTarget>()
            .filter { it.konanTarget.family == Family.IOS }
            .map { it.binaries.getFramework("RELEASE") }
    )
    destinationDir = buildDir.resolve("xcframework")
}
```
