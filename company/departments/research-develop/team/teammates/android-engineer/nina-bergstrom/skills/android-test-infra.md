# Android Test Infrastructure

**Category:** Mobile Engineering — Android Testing Infrastructure
**Owner:** Android Engineer (Nina Bergström)

## Overview

This skill establishes the testing infrastructure for Android applications covering test fixtures, CI integration, parallel test execution, and flaky test management. It applies to Stage 5 (Development) where test utilities are built alongside production code, Stage 6 (Code Review) where test infrastructure quality is evaluated, and Stage 7 (Automated Testing) where the full test suite execution depends on this infrastructure for reliability and speed.

## Competency Dimensions

| Dimension               | Description                                                                                                           | Proficiency Indicators                                                                                                                        |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Test Fixtures           | Deterministic test data generation, factory pattern, builders, JSON fixtures, database seeding                        | Test data is reproducible across runs; fixtures cover edge cases (empty lists, null fields, boundary values); factory methods compose cleanly |
| CI Integration          | GitHub Actions test orchestration, artifact management, test result publishing, coverage aggregation, matrix strategy | Tests run on CI in <30 minutes; test results published as actionable reports; coverage reports aggregated across modules                      |
| Parallel Test Execution | Shard-based distribution, module-level parallelism, emulator parallelization, test ordering                           | Full test suite completes in <45 minutes; no test interference between shards; consistent results across parallel runs                        |
| Flaky Test Management   | Flaky test detection, quarantine workflow, root cause analysis, retry strategies, stability metrics                   | Flaky test rate <1%; all flaky tests tracked with ownership; quarantine-to-fix SLA <1 sprint                                                  |
| Test Utilities          | Mock server setup, fake repositories, coroutine test utilities, idling resources, test rules                          | Test utilities are reusable across test classes; mock server returns deterministic responses; coroutine tests use controlled dispatchers      |

## Execution Guidance

### Test Factory Pattern — Comprehensive Fixtures

**Factory hierarchy with composition:**

```kotlin
object UserFixtures {
    fun validUser(
        id: String = "user-${randomId()}",
        name: String = "John Doe",
        email: String = "john@example.com",
        age: Int = 30,
        preferences: UserPreferences = UserPreferencesFixtures.defaults()
    ): User {
        return User(id, name, email, age, preferences)
    }

    fun userWithInvalidEmail() = validUser(email = "not-an-email")
    fun userWithLongName() = validUser(name = "A".repeat(256))
    fun userWithSpecialCharacters() = validUser(
        name = "José García Müller",
        email = "jose+test@example.com"
    )
    fun emptyUser() = validUser(name = "", email = "")
    fun userWithNullFields() = validUser(name = "", email = "")
}

object OrderFixtures {
    fun pendingOrder(
        id: String = "order-${randomId()}",
        userId: String = "user-123",
        items: List<OrderItem> = listOf(OrderItemFixtures.singleItem()),
        totalAmount: Long = items.sumOf { it.unitPrice * it.quantity }
    ): Order {
        return Order(
            id = id,
            userId = userId,
            status = OrderStatus.PENDING,
            items = items,
            totalAmount = totalAmount,
            createdAt = Instant.now().toEpochMilli()
        )
    }

    fun completedOrder() = pendingOrder().copy(status = OrderStatus.DELIVERED)
    fun cancelledOrder() = pendingOrder().copy(status = OrderStatus.CANCELLED)
    fun emptyOrder() = pendingOrder(items = emptyList())
    fun orderWithManyItems(count: Int = 100) = pendingOrder(
        items = List(count) { OrderItemFixtures.randomItem() }
    )
}

object OrderItemFixtures {
    fun singleItem(
        id: String = "item-${randomId()}",
        productId: String = "prod-123",
        name: String = "Test Product",
        quantity: Int = 1,
        unitPrice: Long = 999  // $9.99
    ): OrderItem {
        return OrderItem(id, productId, name, quantity, unitPrice)
    }

    fun randomItem(): OrderItem = singleItem(
        productId = "prod-${randomId()}",
        name = "Product ${randomId()}",
        unitPrice = (100L..9999L).random()
    )
}

private fun randomId() = UUID.randomUUID().toString().take(8)
```

**JSON fixture loading for API responses:**

```kotlin
object ApiFixtureLoader {
    inline fun <reified T> loadResponse(fileName: String): T {
        val inputStream = javaClass.classLoader
            ?.getResourceAsStream("api-responses/$fileName")
            ?: throw IllegalArgumentException("Fixture not found: $fileName")

        val json = inputStream.bufferedReader().use { it.readText() }
        return Json.decodeFromString(json)
    }
}

// Usage in tests
@Test
fun `given success response, when fetch orders, then returns mapped orders`() = runTest {
    // Given
    val mockResponse = ApiFixtureLoader.loadResponse<OrderApiResponse>("orders-success.json")
    every { orderApi.getOrders(any()) } returns mockResponse

    // When
    val result = repository.fetchOrders("user-123")

    // Then
    // Assertions...
}
```

**Database seeding for instrumented tests:**

```kotlin
class DatabaseTestRule(
    private val context: Context
) : TestWatcher() {

    lateinit var database: AppDatabase
        private set

    override fun starting(description: Description) {
        database = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java)
            .allowMainThreadQueries() // Safe for tests
            .build()
    }

    override fun finished(description: Description) {
        database.close()
    }

    fun seedWithTestData() {
        database.userDao().upsert(UserFixtures.validUser())
        database.userDao().upsert(UserFixtures.validUser(id = "user-456", name = "Jane Doe"))
        database.orderDao().upsert(OrderFixtures.pendingOrder(userId = "user-123"))
        database.orderDao().upsert(OrderFixtures.completedOrder(userId = "user-456"))
    }
}
```

### CI Integration — Test Orchestration

**GitHub Actions with test result publishing:**

```yaml
# .github/workflows/android-test-suite.yml
name: Android Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 45

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: "zulu"
          java-version: "17"

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Run unit tests
        run: ./gradlew testDebugUnitTest --parallel

      - name: Upload unit test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: unit-test-results
          path: "**/build/test-results/testDebugUnitTest/*.xml"

      - name: Run instrumented tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 33
          arch: x86_64
          profile: Nexus 6
          script: ./gradlew connectedDebugAndroidTest

      - name: Upload instrumented test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: instrumented-test-results
          path: "**/build/outputs/androidTest-results/"

      - name: Publish test results
        if: always()
        uses: EnricoMi/publish-unit-test-result-action@v2
        with:
          files: |
            **/build/test-results/**/*.xml
            **/build/outputs/androidTest-results/**/*.xml

      - name: Generate coverage report
        run: ./gradlew jacocoTestReport

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          files: "**/build/reports/jacoco/jacoco.xml"
          fail_ci_if_error: true
```

### Parallel Test Execution

**Gradle configuration for parallelism:**

```kotlin
// build.gradle.kts — module level
tasks.withType<Test> {
    // Enable parallel test execution within a module
    maxParallelForks = (Runtime.getRuntime().availableProcessors() / 2).coerceAtLeast(1)

    // Use JUnit 5 platform
    useJUnitPlatform()

    // Fail on first failure (fail fast in CI)
    if (System.getenv("CI") == "true") {
        failFast = true
    }

    // Test logging
    testLogging {
        events("passed", "skipped", "failed")
        showStandardStreams = true
        exceptionFormat = org.gradle.api.tasks.testing.logging.TestExceptionFormat.FULL
    }
}

// Instrumented test sharding
android {
    defaultConfig {
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        // Enable sharding for parallel emulator execution
        testInstrumentationRunnerArguments["numShards"] = "4"
    }
}
```

**Sharded instrumented test execution:**

```bash
#!/bin/bash
# run-sharded-tests.sh
NUM_SHARDS=4

for shard in $(seq 0 $((NUM_SHARDS - 1))); do
  adb shell am instrument -w \
    -e numShards $NUM_SHARDS \
    -e shardIndex $shard \
    com.example.app.test/androidx.test.runner.AndroidJUnitRunner &
done

wait
```

### Flaky Test Management

**Detection and quarantine workflow:**

```kotlin
// Retry annotation for known-flaky tests during investigation
@Retention(AnnotationRetention.RUNTIME)
@Target(AnnotationTarget.FUNCTION)
annotation class FlakyTest(val reason: String, val maxRetries: Int = 3)

// JUnit 5 extension for automatic retry
class FlakyTestExtension : InvocationInterceptor {
    override fun interceptTestMethod(
        invocation: InvocationInterceptor.Invocation<Void>,
        invocationContext: ReflectiveInvocationContext<Method>,
        extensionContext: ExtensionContext
    ) {
        val annotation = invocationContext.testMethod
            .flatMap { it.getAnnotation(FlakyTest::class.java).stream() }
            .findFirst()
            .orElse(null) ?: return invocation.proceed()

        var lastException: Throwable? = null
        repeat(annotation.maxRetries) { attempt ->
            try {
                invocation.proceed()
                return  // Test passed
            } catch (e: Throwable) {
                lastException = e
                println("Flaky test retry ${attempt + 1}/${annotation.maxRetries}: ${e.message}")
                Thread.sleep(1000) // Brief pause between retries
            }
        }
        throw lastException!!
    }
}

// Usage
@ExtendWith(FlakyTestExtension::class)
class FlakyTests {

    @FlakyTest(reason = "Network timing variability on CI", maxRetries = 3)
    @Test
    fun whenFetchData_thenReturnsResults() {
        // This test may fail due to CI network timing
        // Quarantined until root cause is fixed
    }
}
```

**Flaky test tracking spreadsheet:**

| Test Name                            | Flake Rate | First Detected | Owner | Root Cause                    | Fix Target Sprint | Status      |
| ------------------------------------ | ---------- | -------------- | ----- | ----------------------------- | ----------------- | ----------- |
| `OrderSyncTest.syncsOnNetworkChange` | 12%        | 2026-03-15     | Nina  | Race condition in WorkManager | Sprint 14         | In Progress |
| `UserProfileTest.loadsAvatar`        | 3%         | 2026-03-20     | Jan   | Image loading timeout         | Sprint 14         | Fixed       |

**Flaky test prevention checklist:**

- [ ] No `Thread.sleep()` — use `TestDispatcher` or `IdlingResource`
- [ ] No shared mutable state between tests — fresh fixtures per test
- [ ] No real network calls — MockWebServer for all HTTP
- [ ] No timing-dependent assertions — use `waitUntil` with timeout
- [ ] No external system dependencies — mock/fake all external services
- [ ] Tests are order-independent — no test depends on another test's side effects
- [ ] Deterministic random values — use seeded random for test data

### Test Rules — Reusable Infrastructure

```kotlin
// Main dispatcher override rule
class MainDispatcherRule(
    private val testDispatcher: TestDispatcher = UnconfinedTestDispatcher()
) : TestWatcher() {
    override fun starting(description: Description) {
        Dispatchers.setMain(testDispatcher)
    }

    override fun finished(description: Description) {
        Dispatchers.resetMain()
    }
}

// Usage in ViewModel tests
class UserListViewModelTest {

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    private val repository = FakeUserRepository()
    private lateinit var viewModel: UserListViewModel

    @Before
    fun setup() {
        viewModel = UserListViewModel(
            getUsersUseCase = GetUsersUseCase(repository),
            deleteUserUseCase = mockk(relaxed = true)
        )
    }

    @Test
    fun `when users loaded, state emits user list`() = runTest {
        repository.users = listOf(
            UserFixtures.validUser(id = "1", name = "Alice"),
            UserFixtures.validUser(id = "2", name = "Bob")
        )

        viewModel.sendIntent(UserListIntent.LoadUsers)

        val state = viewModel.uiState.first { it.users.isNotEmpty() }
        assertEquals(2, state.users.size)
    }
}

// Fake repository for testing
class FakeUserRepository : UserRepository {
    var users: List<User> = emptyList()
    var shouldFail: Boolean = false
    var failureException: Exception = NetworkException()

    override fun observeUser(userId: String): Flow<User> = flow {
        users.find { it.id == userId }?.let { emit(it) }
    }

    override suspend fun getUser(id: String): Result<User> {
        if (shouldFail) return Result.failure(failureException)
        return users.find { it.id == id }
            ?.let { Result.success(it) }
            ?: Result.failure(UserNotFoundException(id))
    }

    override suspend fun updateUser(user: User): Result<Unit> {
        if (shouldFail) return Result.failure(failureException)
        users = users.map { if (it.id == user.id) user else it }
        return Result.success(Unit)
    }
}
```

## Pipeline Integration

- **Stage 4 (Implementation Plan):** Test infrastructure tasks included in implementation plan: fixture creation, CI pipeline setup, test rule development, flaky test monitoring.
- **Stage 5 (Development):** Test utilities built alongside production code. Factories and fakes created as features are developed.
- **Stage 6 (Code Review):** Test infrastructure quality reviewed: fixture completeness, test determinism, CI pipeline efficiency, flaky test count.
- **Stage 7 (Automated Testing):** Primary stage for this skill. Full test suite execution with parallelism, coverage reporting, and flaky test quarantine.
- **Stage 8 (Integrity Verification):** Regression test suite uses same infrastructure. Test results compared against baseline to detect regressions.

## Quality Standards

- Full test suite (unit + instrumented) completes in **<45 minutes** on CI
- Flaky test rate **<1%** (measured over rolling 30-day window)
- All flaky tests have **tracked ownership** and fix target within 1 sprint
- Test fixtures cover **edge cases**: empty collections, null fields, boundary values, special characters
- **Zero** `Thread.sleep()` in test code — use controlled dispatchers or idling resources
- **100%** tests are order-independent — no test depends on another test's execution
- Coverage reports uploaded to Codecov with **fail-on-decrease** threshold
- Test results published as CI artifacts with **pass/fail/skip counts**
- MockWebServer used for all network tests — **zero** real network calls in test suite
- Database tests use **in-memory Room** — no file system dependencies
- CI fails fast on first test failure in PR context (not on main/develop)
