# Flaky Test Prevention

## Flaky Test Prevention

Flaky tests — tests that sometimes pass and sometimes fail without code changes — erode confidence in the test suite and waste developer time.

### Common Causes of Flakiness

| Cause                  | Symptom                          | Fix                                                                       |
| ---------------------- | -------------------------------- | ------------------------------------------------------------------------- |
| Timing/race conditions | Test passes locally, fails in CI | Use proper synchronization (CountDownLatch, semaphores, async assertions) |
| Shared mutable state   | Test order matters               | Isolate test state, reset between tests                                   |
| Network dependency     | Fails on slow/absent network     | Mock network layer, use MockWebServer                                     |
| Animation timing       | Element not found                | Disable animations in tests, use IdlingResource                           |
| Hard-coded waits       | Brittle, slow                    | Use polling assertions, explicit waits                                    |
| External service calls | Rate limits, downtime            | Stub external dependencies                                                |
| Database state leakage | Tests pollute each other         | Use in-memory DB, transactions with rollback                              |

### Flaky Test Prevention Patterns

**Pattern 1: Polling Assertions (instead of Thread.sleep):**

```kotlin
// BAD — hard-coded wait
@Test
fun `bad approach`() {
    launchActivity()
    Thread.sleep(3000) // Hope the data loads in 3 seconds
    onView(withId(R.id.name)).check(matches(withText("Alice")))
}

// GOOD — polling assertion
@Test
fun `good approach`() {
    launchActivity()
    onView(withId(R.id.name))
        .withTimeout(5, TimeUnit.SECONDS)
        .check(matches(withText("Alice")))
}

// Kotlin extension for polling
fun ViewInteraction.withTimeout(
    timeout: Long,
    unit: TimeUnit
): ViewInteraction {
    val endTime = System.currentTimeMillis() + unit.toMillis(timeout)
    while (System.currentTimeMillis() < endTime) {
        try {
            check(matches(anything()))
            return this
        } catch (e: Throwable) {
            Thread.sleep(100)
        }
    }
    return this
}
```

**Pattern 2: Test Isolation with Transaction Rollback:**

```kotlin
// Android — Room with transaction rollback
@RunWith(AndroidJUnit4::class)
class IsolatedDatabaseTest {
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    private lateinit var db: AppDatabase

    @Before
    fun setup() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        db = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java)
            .allowMainThreadQueries()
            .build()
    }

    @After
    fun teardown() {
        db.close() // Fresh DB for every test
    }

    @Test
    fun `test with clean database`() {
        // This test starts with an empty database
        // No state leakage from previous tests
    }
}
```

**Pattern 3: IdlingResource for Async Operations:**

```kotlin
// Android — Espresso IdlingResource
class AsyncOperationIdlingResource : IdlingResource {
    @Volatile
    var isIdleNow: Boolean = true
        private set
    private var callback: IdlingResource.ResourceCallback? = null

    fun setIdle(idle: Boolean) {
        isIdleNow = idle
        if (idle) {
            callback?.onTransitionToIdle()
        }
    }

    override fun getName() = this::class.java.name

    override fun registerIdleTransitionCallback(callback: IdlingResource.ResourceCallback?) {
        this.callback = callback
    }
}

// Usage in ViewModel
class MyViewModel(
    private val repository: Repository,
    val idlingResource: AsyncOperationIdlingResource
) : ViewModel() {
    fun loadData() {
        idlingResource.setIdle(false)
        viewModelScope.launch {
            val data = repository.fetchData()
            _uiState.value = UiState.Success(data)
            idlingResource.setIdle(true)
        }
    }
}
```

**Pattern 4: Retry Flaky Tests (temporary mitigation, not a fix):**

```kotlin
// JUnit 5 extension for retrying flaky tests
@ExtendWith(RetryOnFailureExtension::class)
@RetryOnFailure(times = 3)
@Test
fun `potentially flaky test`() {
    // This test will retry up to 3 times before failing
    // NOTE: Use only as temporary mitigation — fix the root cause
}
```

### Flaky Test Detection

| Tool                  | Platform       | How It Works                                     |
| --------------------- | -------------- | ------------------------------------------------ |
| CI retry              | Any            | Run test N times in CI; fails if any run differs |
| Bazel --runs_per_test | Android        | Built-in flakiness detection                     |
| Xcode test repetition | iOS            | Built-in test repetition                         |
| Maestro retry         | Cross-platform | Retry failed flows                               |

---
