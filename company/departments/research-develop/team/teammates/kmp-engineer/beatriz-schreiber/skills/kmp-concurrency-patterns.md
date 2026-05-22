---
name: kmp-concurrency-patterns
description: KMP coroutine and concurrency patterns for multiplatform targets. Use when implementing coroutine-based business logic in shared Kotlin modules, bridging Kotlin coroutines to Swift async/await or callbacks, managing structured concurrency across Android and iOS, designing the ViewModel or UseCase layer in a KMP architecture, or debugging coroutine-related issues on Kotlin/Native iOS.
version: "1.0.0"
---

# KMP Concurrency Patterns

## Purpose

Coroutines are the foundation of KMP's async story on Android, but they require deliberate design to work correctly on iOS. The Kotlin/Native runtime enforces threading constraints differently from the JVM. Understanding the differences — and writing shared Kotlin code that handles them correctly — is the difference between a KMP module that iOS engineers trust and one they work around.

---

## Coroutine Scope Strategy

### Shared ViewModels / UseCases

In shared KMP code, coroutine scopes must be lifecycle-aware. The pattern depends on the architecture layer:

| Layer               | Scope Strategy                                             | iOS Consumer Pattern                                 |
| ------------------- | ---------------------------------------------------------- | ---------------------------------------------------- |
| ViewModel (shared)  | `CoroutineScope(SupervisorJob() + Dispatchers.Main)`       | Swift `Task {}` observing a `StateFlow`              |
| UseCase (shared)    | No scope; accept `CoroutineScope` as parameter from caller | Caller provides scope; cancelled when caller is done |
| Repository (shared) | Internal scope for background work; `Dispatchers.Default`  | —                                                    |
| Network layer       | `Dispatchers.Default`; IO operations via Ktor (suspending) | —                                                    |

### Cancellation

Structured concurrency's cancellation must propagate correctly across platforms. Apply these conventions:

- Always use `SupervisorJob()` at the ViewModel/presenter scope — prevents one child coroutine failure from cancelling all siblings
- Use `viewModelScope.launch` (Android) or the KMP equivalent wrapper (iOS), not `GlobalScope`
- Expose a `cancel()` function on shared ViewModels; call it from `onCleared()` (Android) or `deinit` (Swift)

---

## Swift Async/Await Bridging

Kotlin coroutines do not automatically map to Swift `async` functions in the generated ObjC header. There are two bridging approaches:

### Option A — Manual Callback Wrapper (Simple, Portable)

```kotlin
// Shared code
class UserRepository {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)

    fun fetchUser(id: String, completion: (User?, Error?) -> Unit) {
        scope.launch {
            try {
                val user = api.getUser(id)  // suspend function
                completion(user, null)
            } catch (e: Exception) {
                completion(null, e.toNSError())
            }
        }
    }
}
```

Swift consumer:

```swift
repo.fetchUser(id: "123") { user, error in
    // UI update on main thread (completion called on Main dispatcher)
}
```

### Option B — `kotlinx-coroutines-core` Swift Concurrency Support (Modern)

With `kotlinx.coroutines` 1.6.4+ and Kotlin 1.8+, `suspend` functions are exposed as Swift `async throws` functions automatically when the `kotlin.native.binary.objcExportSuspendFunctionLaunchThreadRestriction=none` opt-in is set.

```kotlin
// Shared code
suspend fun fetchUser(id: String): User = api.getUser(id)
```

Swift consumer:

```swift
let user = try await repo.fetchUser(id: "123")
```

**Choose Option B for new projects** — it produces cleaner Swift code and aligns with Swift's native concurrency model. Choose Option A for compatibility with older iOS targets (< iOS 15) or existing codebases.

---

## `StateFlow` and `SharedFlow` on iOS

Kotlin `StateFlow` and `SharedFlow` are the KMP solution for observable state. Consuming them from Swift requires a wrapper because Swift cannot directly `collect` a `Flow`.

### Pattern: Observable Wrapper (SKIE or manual)

**Using SKIE (recommended):** The SKIE Gradle plugin automatically generates Swift-friendly wrappers for `StateFlow` and `SharedFlow`, making them directly consumable as `AsyncSequence` in Swift. Add SKIE to the KMP module's build.

**Manual wrapper pattern:**

```kotlin
// Shared
class UserViewModel {
    private val _state = MutableStateFlow<UserState>(UserState.Loading)
    val state: StateFlow<UserState> = _state.asStateFlow()

    fun observeState(collector: (UserState) -> Unit): Job =
        CoroutineScope(Dispatchers.Main).launch {
            state.collect { collector(it) }
        }
}
```

Swift:

```swift
let job = viewModel.observeState { state in
    // update UI
}
// Cancel in deinit:
job.cancel(cause: nil)
```

---

## `Dispatchers.Main` on iOS

Kotlin/Native requires a `Main` dispatcher to be provided explicitly on iOS. Ensure the project includes:

```kotlin
// in commonMain or iosMain
implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.x.x")
```

On iOS, `Dispatchers.Main` delegates to `dispatch_get_main_queue()` automatically when the above dependency is present. Verify by running an iOS simulator test that collects a `StateFlow` — if `Main` is missing, the test will throw a `RuntimeException`.

---

## Common Pitfalls

| Pitfall                                         | Symptom                                              | Fix                                                                                     |
| ----------------------------------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------- |
| No `SupervisorJob` at top-level scope           | One failed coroutine cancels all others              | Add `SupervisorJob()` to the CoroutineScope constructor                                 |
| `GlobalScope` usage                             | Memory leaks; coroutines outlive the UI              | Replace with a scoped `CoroutineScope` with a lifecycle-bound cancel                    |
| `Dispatchers.IO` on iOS                         | `IllegalStateException` — no IO dispatcher on Native | Replace with `Dispatchers.Default` in shared code; IO dispatcher is JVM-only            |
| Flow collected on background thread updating UI | Thread checker crash on iOS                          | Ensure flow collection switches to `Dispatchers.Main` before emitting UI-relevant state |
| Missing SKIE or manual wrapper                  | iOS cannot consume `StateFlow`                       | Add SKIE plugin or manual `observeState` wrapper pattern                                |
