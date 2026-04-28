---
name: android-language-core-kotlin-advanced
description: Advanced Kotlin patterns for Android — coroutines and structured concurrency, Kotlin Flow (StateFlow/SharedFlow), Kotlin Multiplatform expect/actual, memory management, sealed hierarchies, and type-safe DSLs. Owned by Tariq Al-Hassan (Senior Android Engineer). Use during Stage 5 (Development) for coroutine-based features and KMP shared modules, Stage 7 (Automated Testing) for coroutine testing. Trigger: kotlin coroutines, structured concurrency, StateFlow, SharedFlow, KMP, kotlin multiplatform, expect actual, memory management, sealed interface, kotlin DSL.
prerequisites:
  - android-language-core-implementation

version: "1.0.0"
---

# Kotlin Advanced

**Category:** Mobile Engineering — Android
**Owner:** Senior Android Engineer (Tariq Al-Hassan)

## Overview

This skill enables production-grade Kotlin development leveraging coroutines, Flow, structured concurrency, and Kotlin Multiplatform (KMP) interoperability. It is critical to Stage 5 (Development) and Stage 7 (Automated Testing) where coroutine correctness, memory management, and shared business logic directly impact application stability, testability, and cross-platform code reuse.

## Competency Dimensions

| Dimension                           | Description                                                                                   | Proficiency Indicators                                                                                                                                  |
| ----------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Coroutines & Structured Concurrency | Deep understanding of coroutine lifecycle, scopes, dispatchers, and cancellation semantics    | Correctly implements `CoroutineScope` hierarchies; zero leaked coroutines in production; proper `supervisorScope` vs `coroutineScope` selection         |
| Kotlin Flow                         | Cold vs hot flow semantics, state management, backpressure handling, and operator composition | Uses `StateFlow`/`SharedFlow` appropriately; implements backpressure with `buffer`/`conflate`/`collectLatest`; zero dropped emissions in critical paths |
| Kotlin Multiplatform (KMP)          | Shared module design, expect/actual patterns, platform-specific implementations               | Designs clean abstraction boundaries; handles platform-specific edge cases; maintains >70% shared code ratio for business logic                         |
| Memory Management & Performance     | Heap analysis, coroutine context leaks, reference cycles in lambda captures                   | Zero memory leaks detected in LeakCanary profiles; proper `WeakReference`/`SoftReference` usage; coroutine contexts released on scope cancellation      |
| Kotlin Type System & DSLs           | Reified generics, inline functions, sealed hierarchies, type-safe builders                    | Leverages sealed interfaces for result types; creates internal DSLs for configuration; zero unnecessary boxing/unboxing in hot paths                    |

## Execution Guidance

### Structured Concurrency Patterns

**Rule 1: Every coroutine must have a parent scope.** Never launch fire-and-forget coroutines from `GlobalScope`. Use `viewModelScope` for UI-layer work, `lifecycleScope` for Activity/Fragment-scoped work, and custom `CoroutineScope` with `SupervisorJob()` for service-layer operations that should survive individual child failures.

```kotlin
// CORRECT: SupervisorJob allows sibling coroutines to survive individual failures
class UserRepository(
    private val api: UserApi,
    private val database: UserDao
) {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    fun syncUsers() = scope.launch {
        // If fetchUsers fails, cacheUsers won't be affected
        // and other sibling launches continue executing
    }
}

// WRONG: GlobalScope leaks coroutines beyond component lifecycle
fun syncUsers() = GlobalScope.launch { ... }
```

**Rule 2: Use `coroutineScope` for parallel decomposition, `supervisorScope` for independent operations.** `coroutineScope` cancels all children on any failure (all-or-nothing). `supervisorScope` isolates failures (best-effort). Choose based on transactional requirements.

```kotlin
// All-or-nothing: if any call fails, all are cancelled
suspend fun loadDashboardData(): Dashboard = coroutineScope {
    val user = async { api.getUser() }
    val orders = async { api.getOrders() }
    val notifications = async { api.getNotifications() }
    Dashboard(user.await(), orders.await(), notifications.await())
}

// Best-effort: individual failures don't affect siblings
suspend fun syncAllData() = supervisorScope {
    launch { try { syncUsers() } catch (e: Exception) { handleSyncError(e) } }
    launch { try { syncOrders() } catch (e: Exception) { handleSyncError(e) } }
    launch { try { syncPreferences() } catch (e: Exception) { handleSyncError(e) } }
}
```

### Flow Architecture Decisions

**StateFlow vs SharedFlow selection matrix:**

| Use Case                                | Recommended Type                                                         | Rationale                                                                  |
| --------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| UI state emission                       | `StateFlow<T>`                                                           | Requires initial value; replay to new collectors                           |
| One-time events (snackbars, navigation) | `SharedFlow<T>(extraBufferCapacity = 1, onBufferOverflow = DROP_OLDEST)` | No replay needed; prevents stale event re-delivery on configuration change |
| Continuous data stream                  | `flow { }` builder (cold)                                                | Lazily executed; new execution per collector                               |
| Multi-collector hot stream              | `SharedFlow` with appropriate `replay`                                   | Shares single upstream subscription                                        |

**Backpressure handling strategy:**

```kotlin
// High-frequency sensor data — drop intermediate values
sensorFlow
    .conflate()
    .stateIn(viewModelScope, SharingStarted.Lazily, initialSensorState)

// User search queries — cancel previous in-flight request
searchQueryFlow
    .debounce(300)
    .distinctUntilChanged()
    .flatMapLatest { query -> repository.search(query) }
    .collect { results -> updateUi(results) }

// Critical audit events — buffer with bounded capacity
auditEventFlow
    .buffer(capacity = 64, onBufferOverflow = BufferOverflow.SUSPEND)
    .collect { event -> auditLogger.log(event) }
```

### KMP Shared Module Design

**Abstraction boundary principle:** Platform-independent business logic lives in `:shared` module. Platform-specific implementations (database, networking, cryptography) are declared as `expect` in shared and implemented as `actual` in platform modules.

```kotlin
// shared/src/commonMain/kotlin/
expect class SecureStorage() {
    suspend fun put(key: String, value: String)
    suspend fun get(key: String): String?
    suspend fun delete(key: String)
}

// androidMain/kotlin/
actual class SecureStorage actual constructor() {
    private val preferences = EncryptedSharedPreferences(...)
    actual suspend fun put(key: String, value: String) = ...
    actual suspend fun get(key: String): String? = ...
    actual suspend fun delete(key: String) = ...
}

// iosMain/kotlin/
actual class SecureStorage actual constructor() {
    actual suspend fun put(key: String, value: String) = ...
    actual suspend fun get(key: String): String? = ...
    actual suspend fun delete(key: String) = ...
}
```

**Coroutine interop on KMP:** Use `kotlinx-coroutines-core` which provides common coroutine APIs. On iOS, coroutines map to Swift `async/await` via the Kotlin/Native compiler. Always use `Dispatchers.Main.immediate` for UI updates to prevent unnecessary dispatch on already-main-thread callers.

### Memory Management Discipline

**Common leak patterns and prevention:**

1. **Coroutine scope leaks:** Always tie coroutine scope to a lifecycle-bound owner (`ViewModel`, `LifecycleOwner`). Use `lifecycleScope.launchWhenStarted` (deprecated) → migrate to `lifecycleScope.launch { lifecycle.repeatOnLifecycle(Lifecycle.State.STARTED) { ... } }`.

2. **Flow collection leaks:** Cancel flow collection in `onCleared` or use `repeatOnLifecycle`. Never collect flows in `init` blocks without lifecycle awareness.

3. **Lambda capture leaks:** Avoid capturing `this` in long-lived lambdas. Use `weakReferenceOf(this)` for callbacks that outlive the captured object.

4. **Context leaks:** Always specify `CoroutineContext` explicitly. `Dispatchers.Default` for CPU-intensive, `Dispatchers.IO` for blocking I/O, `Dispatchers.Main.immediate` for UI. Never use `Dispatchers.Unconfined` in production.

### Kotlin DSL & Type-Safe Builders

For configuration-heavy modules (e.g., dependency injection, network client setup), use type-safe builders:

```kotlin
fun httpClientConfig(block: HttpClientConfig.() -> Unit): HttpClientConfig {
    return HttpClientConfig().apply(block)
}

class HttpClientConfig {
    var baseUrl: String = ""
    var timeout: Long = 30_000
    val interceptors = mutableListOf<Interceptor>()

    fun interceptor(interceptor: Interceptor) {
        interceptors += interceptor
    }
}

// Usage
val config = httpClientConfig {
    baseUrl = "https://api.example.com"
    timeout = 15_000
    interceptor(AuthInterceptor(tokenProvider))
    interceptor(LoggingInterceptor())
}
```

## Pipeline Integration

- **Stage 5 (Development):** Primary skill applied during Android platform development. All coroutine-based features, KMP shared modules, and Flow-driven state management must follow these patterns.
- **Stage 6 (Code Review):** Code review checklist includes: structured concurrency compliance, proper scope lifecycle binding, Flow backpressure handling, KMP expect/actual completeness.
- **Stage 7 (Automated Testing):** Coroutine test coverage using `TestDispatcher`, `runTest`, and `UnconfinedTestDispatcher`. Flow testing with `Turbine` library for assertion-based stream testing.
- **Stage 8 (Integrity Verification):** Memory leak audit via LeakCanary CI integration; coroutine cancellation verification under lifecycle transitions.

## Quality Standards

- **Zero** `GlobalScope` usages in production code
- **100%** coroutine scopes bound to lifecycle-aware owners
- **>70%** code sharing ratio for business logic in KMP modules
- **<2%** coroutine cancellation exceptions in production crash analytics
- **Zero** Flow collector leaks detected in automated lifecycle transition tests
- **100%** `expect` declarations have corresponding `actual` implementations for all target platforms
- All coroutines use explicit `CoroutineDispatcher` — no implicit dispatching in production code
- Sealed interfaces used for all Result/Error type hierarchies — no nullable error states
