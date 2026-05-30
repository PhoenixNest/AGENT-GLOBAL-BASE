---
name: kmp-concurrency-patterns
description: Implement correct coroutine and concurrency patterns for Kotlin Multiplatform — including Kotlin/Native GC-aware structured concurrency, Swift async/await bridging, and StateFlow/SharedFlow consumption across platforms.
version: "1.0.0"
---

# KMP Concurrency Patterns

| Competency                | Description                                                              | Quality Criteria                                                                                            |
| ------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| Structured Concurrency    | Use `SupervisorJob`, `CoroutineScope`, and cancellation correctly in KMP | No leaked coroutines; `SupervisorJob` used in long-lived scopes; scopes tied to component lifecycle         |
| StateFlow iOS Consumption | Bridge `StateFlow`/`SharedFlow` to Swift for idiomatic iOS consumption   | No memory leaks on iOS; `collect` wrapped in a helper that respects iOS lifecycle                           |
| Swift async/await Bridge  | Wrap Kotlin coroutines for consumption from Swift async/await            | SKIE or manual wrapper; no callback hell; Swift-side `async` functions cancel cleanly                       |
| Platform Dispatchers      | Use correct dispatchers on each platform target                          | `Dispatchers.Main` used only for UI; `Dispatchers.Default` for CPU-bound; `Dispatchers.IO` for Android only |

## Execution Guidance

### StateFlow → Swift Wrapper Pattern

```kotlin
// commonMain — define the flow
class ProfileViewModel : ViewModel() {
    private val _state = MutableStateFlow<ProfileState>(ProfileState.Loading)
    val state: StateFlow<ProfileState> = _state.asStateFlow()
}

// iosMain — wrap for Swift consumption
fun <T> StateFlow<T>.asCommonFlow(): CommonFlow<T> = CommonFlow(this)

class CommonFlow<T>(private val origin: StateFlow<T>) {
    fun watch(block: (T) -> Unit): Closeable {
        val job = Job()
        CoroutineScope(Dispatchers.Main + job).launch {
            origin.collect(block)
        }
        return object : Closeable {
            override fun close() = job.cancel()
        }
    }
}
```

### Swift Consumption

```swift
// Swift — consume the flow
let closeable = viewModel.state.watch { state in
    DispatchQueue.main.async {
        self.updateUI(state: state)
    }
}

// Cancel when view disappears
override func viewWillDisappear(_ animated: Bool) {
    super.viewWillDisappear(animated)
    closeable.close()
}
```

### Concurrency Anti-Patterns to Avoid

| Anti-Pattern                          | Problem                                             | Correct Approach                                  |
| ------------------------------------- | --------------------------------------------------- | ------------------------------------------------- |
| `GlobalScope.launch` in shared code   | No lifecycle management; leaks on all platforms     | Use a scoped `CoroutineScope` tied to a component |
| `runBlocking` on iOS main thread      | Blocks the UI thread; crashes on strict main thread | Use callbacks or SKIE async bridge                |
| Sharing mutable `List` across threads | Kotlin/Native GC concurrent mutation issue          | Use `ConcurrentMutableList` or `StateFlow`        |
| `Dispatchers.IO` in `commonMain`      | Not available on iOS; compile error                 | Use `Dispatchers.Default` in shared code          |
