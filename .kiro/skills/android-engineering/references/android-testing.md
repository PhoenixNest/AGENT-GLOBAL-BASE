---
name: android_testing
version: "1.0.0"
---

# Android Testing

| Competency              | Description                                                                                                           | Quality Criteria                                                                                                                              |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| TDD Methodology         | Red-Green-Refactor cycle, test-first design, emergent architecture through testing                                    | Writes failing test before implementation; test suite drives design decisions; refactoring phase preserves all tests                          |
| Unit Testing            | JUnit 5, MockK, coroutine testing with TestDispatcher, parameterized tests, assertion libraries                       | >80% unit test coverage on domain layer; all use cases have unit tests; coroutine tests use controlled dispatchers                            |
| UI Testing              | Espresso, Compose Testing, UiAutomator, screenshot testing, flaky test mitigation                                     | Core user flows covered by UI tests; screenshot tests catch visual regressions; flaky test rate <1%                                           |
| Robolectric             | JVM-based Android framework testing, shadow objects, resource loading, manifest simulation                            | Tests run on JVM without emulator; Android framework classes properly shadowed; test execution <2s per test                                   |
| Maestro E2E Testing     | Flow-based mobile UI automation, YAML-based test scripts, cross-platform E2E scenarios, device farm execution         | Critical user journeys covered by Maestro flows; flows run on real devices in CI; E2E suite completes in <20 minutes                          |
| Test Fixtures           | Deterministic test data generation, factory pattern, builders, JSON fixtures, database seeding                        | Test data is reproducible across runs; fixtures cover edge cases (empty lists, null fields, boundary values); factory methods compose cleanly |
| CI Integration          | GitHub Actions test orchestration, artifact management, test result publishing, coverage aggregation, matrix strategy | Tests run on CI in <30 minutes; test results published as actionable reports; coverage reports aggregated across modules                      |
| Parallel Test Execution | Shard-based distribution, module-level parallelism, emulator parallelization, test ordering                           | Full test suite completes in <45 minutes; no test interference between shards; consistent results across parallel runs                        |
| Flaky Test Management   | Flaky test detection, quarantine workflow, root cause analysis, retry strategies, stability metrics                   | Flaky test rate <1%; all flaky tests tracked with ownership; quarantine-to-fix SLA <1 sprint                                                  |
| Test Utilities          | Mock server setup, fake repositories, coroutine test utilities, idling resources, test rules                          | Test utilities are reusable across test classes; mock server returns deterministic responses; coroutine tests use controlled dispatchers      |

---

## Testing Methodology

### TDD — Red-Green-Refactor in Practice

**Example: Testing a use case before implementation:**

```kotlin
// STEP 1: RED — Write the failing test first
class ValidateCheckoutUseCaseTest {

    private val cartRepository = mockk<CartRepository>()
    private val paymentValidator = mockk<PaymentValidator>()
    private lateinit var useCase: ValidateCheckoutUseCase

    @Before
    fun setup() {
        useCase = ValidateCheckoutUseCase(cartRepository, paymentValidator)
    }

    @Test
    fun `given empty cart, when validate, then returns empty cart error`() = runTest {
        every { cartRepository.getCart() } returns Cart.empty()
        val result = useCase.execute()
        assertTrue(result.isFailure)
        assertEquals(ValidationError.EMPTY_CART, result.exceptionOrNull())
    }
}

// STEP 2: GREEN — Implement minimum code to pass
class ValidateCheckoutUseCase(
    private val cartRepository: CartRepository,
    private val paymentValidator: PaymentValidator
) {
    suspend fun execute(): Result<CheckoutValidation> {
        val cart = cartRepository.getCart()
        if (cart.items.isEmpty()) return Result.failure(ValidationError.EMPTY_CART)
        return Result.success(CheckoutValidation(cart))
    }
}

// STEP 3: REFACTOR — Improve code while keeping tests green
```

**TDD discipline rules:**

1. **Never write production code without a failing test.** If you can't write a test, the design is too coupled.
2. **Write the minimum code to pass.** Don't anticipate future requirements — let tests drive complexity.
3. **Refactor ruthlessly after green.** Tests are your safety net — use them to improve code quality.
4. **Test behavior, not implementation.** Tests should survive refactoring that preserves behavior.

### Unit Testing — Domain Layer

**Use case testing with coroutine control:**

```kotlin
class GetUserProfileUseCaseTest {

    private val userRepository = mockk<UserRepository>()
    private val profileMapper = mockk<ProfileMapper>()
    private val testDispatcher = UnconfinedTestDispatcher()
    private lateinit var useCase: GetUserProfileUseCase

    @Before
    fun setup() {
        useCase = GetUserProfileUseCase(userRepository, profileMapper, testDispatcher)
    }

    @Test
    fun `given user exists, when execute, then returns mapped profile`() = runTest(testDispatcher) {
        val user = UserFactory.create(id = "user-123", name = "John Doe")
        val profile = ProfileFactory.createFromUser(user)
        every { userRepository.getUser("user-123") } returns Result.success(user)
        every { profileMapper.toProfile(user) } returns profile

        val result = useCase.execute("user-123")

        assertTrue(result.isSuccess)
        assertEquals(profile, result.getOrNull())
        coVerify(exactly = 1) { userRepository.getUser("user-123") }
        verify(exactly = 1) { profileMapper.toProfile(user) }
    }

    @Test
    fun `given network error, when execute, then returns network error`() = runTest(testDispatcher) {
        every { userRepository.getUser(any()) } returns Result.failure(NetworkException())
        val result = useCase.execute("user-123")
        assertTrue(result.isFailure)
        assertIs<NetworkException>(result.exceptionOrNull())
    }

    @Test
    fun `given null user id, when execute, then throws invalid argument`() = runTest(testDispatcher) {
        assertFailsWith<IllegalArgumentException> { useCase.execute("") }
    }
}
```

**Factory pattern for test data:**

```kotlin
object UserFactory {
    fun create(
        id: String = "test-user-id",
        name: String = "Test User",
        email: String = "test@example.com",
        createdAt: Long = 1_000_000L
    ): User = User(id = id, name = name, email = email, createdAt = createdAt,
        preferences = UserPreferencesFactory.create())
}

object UserPreferencesFactory {
    fun create(
        theme: Theme = Theme.LIGHT,
        notificationsEnabled: Boolean = true,
        language: String = "en"
    ): UserPreferences = UserPreferences(theme, notificationsEnabled, language)
}
```

### UI Testing — Compose Testing

```kotlin
class UserListScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    private val fakeRepository = FakeUserRepository()

    @Test
    fun whenUsersLoaded_displaysUserList() {
        fakeRepository.users = listOf(
            UserFactory.create(id = "1", name = "Alice"),
            UserFactory.create(id = "2", name = "Bob")
        )

        composeTestRule.setContent {
            AppTheme {
                UserListScreen(
                    viewModel = UserListViewModel(
                        getUsersUseCase = GetUsersUseCase(fakeRepository),
                        deleteUserUseCase = mockk(relaxed = true)
                    )
                )
            }
        }

        composeTestRule.onNodeWithText("Alice").assertIsDisplayed()
        composeTestRule.onNodeWithText("Bob").assertIsDisplayed()
    }

    @Test
    fun whenLoading_showsLoadingIndicator() {
        val hangingRepository = FakeUserRepository(hangForever = true)
        composeTestRule.setContent {
            AppTheme {
                UserListScreen(
                    viewModel = UserListViewModel(
                        getUsersUseCase = GetUsersUseCase(hangingRepository),
                        deleteUserUseCase = mockk(relaxed = true)
                    )
                )
            }
        }
        composeTestRule.onNodeWithTag("loading_indicator").assertIsDisplayed()
    }
}
```

### Robolectric — JVM-Based Android Tests

```kotlin
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class SharedPreferencesStorageTest {

    private lateinit var storage: SharedPreferencesStorage

    @Before
    fun setup() {
        val context = ApplicationProvider.getApplicationContext<Application>()
        storage = SharedPreferencesStorage(context)
    }

    @Test
    fun `given key exists, when get, then returns value`() {
        storage.save("test_key", "test_value")
        assertEquals("test_value", storage.get("test_key"))
    }

    @Test
    fun `given key does not exist, when get, then returns null`() {
        assertNull(storage.get("nonexistent_key"))
    }
}

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33], application = TestApplication::class, qualifiers = "en-rUS")
class ResourceLoadingTest {

    @Test
    fun `loads string resources correctly`() {
        val context = ApplicationProvider.getApplicationContext<Application>()
        assertEquals("MyApp", context.getString(R.string.app_name))
    }
}
```

### Maestro E2E Testing

Maestro provides a YAML-based E2E automation layer for verifying full user journeys on real devices and emulators — covering the integration between UI, navigation, and backend in a way that unit and Compose tests cannot.

**Example Maestro flow (`flows/login.yaml`):**

```yaml
appId: com.example.app
---
- launchApp
- tapOn: "Sign In"
- inputText:
    text: "user@example.com"
    id: "email_field"
- inputText:
    text: "password123"
    id: "password_field"
- tapOn: "Login"
- assertVisible: "Home"
- assertVisible: "Welcome back"
```

**Running Maestro flows in CI:**

```yaml
# .github/workflows/maestro-e2e.yml
- name: Run Maestro E2E tests
  run: maestro test flows/
  env:
    MAESTRO_DRIVER: emulator
```

**Maestro conventions:**

- One `.yaml` file per user journey (login, checkout, profile edit)
- Use `id:` selectors for stable element targeting — not text content where possible
- Combine `assertVisible` + `assertNotVisible` to verify state transitions
- Flows must complete in <60 seconds each; flag slow flows for investigation

### Flaky Test Mitigation

| Cause                        | Fix                                                   |
| ---------------------------- | ----------------------------------------------------- |
| Timing-dependent assertions  | Use `composeTestRule.waitUntil()` or `IdlingResource` |
| Shared mutable state         | Create fresh test fixtures per test                   |
| Network timing variability   | Use MockWebServer with deterministic responses        |
| Threading race conditions    | Use `TestDispatcher` with controlled execution        |
| External system dependencies | Mock all external dependencies                        |

```kotlin
// CORRECT: Deterministic timing
@Test
fun whenUserClicks_seeConfirmation() {
    composeTestRule.setContent { /* ... */ }
    composeTestRule.onNodeWithText("Submit").performClick()
    composeTestRule.waitUntil(timeoutMillis = 1_000) {
        composeTestRule.onAllNodesWithText("Success").fetchSemanticsNodes().isNotEmpty()
    }
    composeTestRule.onNodeWithText("Success").assertIsDisplayed()
}

// WRONG: Arbitrary sleep (flaky)
// Thread.sleep(500)  ← Never use this
```

---

## Test Infrastructure

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
    ): User = User(id, name, email, age, preferences)

    fun userWithInvalidEmail() = validUser(email = "not-an-email")
    fun userWithLongName() = validUser(name = "A".repeat(256))
    fun userWithSpecialCharacters() = validUser(name = "José García Müller", email = "jose+test@example.com")
    fun emptyUser() = validUser(name = "", email = "")
}

object OrderFixtures {
    fun pendingOrder(
        id: String = "order-${randomId()}",
        userId: String = "user-123",
        items: List<OrderItem> = listOf(OrderItemFixtures.singleItem()),
        totalAmount: Long = items.sumOf { it.unitPrice * it.quantity }
    ): Order = Order(id = id, userId = userId, status = OrderStatus.PENDING, items = items,
        totalAmount = totalAmount, createdAt = Instant.now().toEpochMilli())

    fun completedOrder() = pendingOrder().copy(status = OrderStatus.DELIVERED)
    fun cancelledOrder() = pendingOrder().copy(status = OrderStatus.CANCELLED)
    fun emptyOrder() = pendingOrder(items = emptyList())
    fun orderWithManyItems(count: Int = 100) = pendingOrder(items = List(count) { OrderItemFixtures.randomItem() })
}

object OrderItemFixtures {
    fun singleItem(
        id: String = "item-${randomId()}",
        productId: String = "prod-123",
        name: String = "Test Product",
        quantity: Int = 1,
        unitPrice: Long = 999
    ): OrderItem = OrderItem(id, productId, name, quantity, unitPrice)

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
        return Json.decodeFromString(inputStream.bufferedReader().use { it.readText() })
    }
}
```

**Database seeding for instrumented tests:**

```kotlin
class DatabaseTestRule(private val context: Context) : TestWatcher() {

    lateinit var database: AppDatabase
        private set

    override fun starting(description: Description) {
        database = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java)
            .allowMainThreadQueries()
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

```kotlin
// build.gradle.kts — module level
tasks.withType<Test> {
    maxParallelForks = (Runtime.getRuntime().availableProcessors() / 2).coerceAtLeast(1)
    useJUnitPlatform()

    if (System.getenv("CI") == "true") {
        failFast = true
    }

    testLogging {
        events("passed", "skipped", "failed")
        showStandardStreams = true
        exceptionFormat = org.gradle.api.tasks.testing.logging.TestExceptionFormat.FULL
    }
}

android {
    defaultConfig {
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        testInstrumentationRunnerArguments["numShards"] = "4"
    }
}
```

**Sharded instrumented test execution:**

```bash
#!/bin/bash
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

```kotlin
@Retention(AnnotationRetention.RUNTIME)
@Target(AnnotationTarget.FUNCTION)
annotation class FlakyTest(val reason: String, val maxRetries: Int = 3)

class FlakyTestExtension : InvocationInterceptor {
    override fun interceptTestMethod(
        invocation: InvocationInterceptor.Invocation<Void>,
        invocationContext: ReflectiveInvocationContext<Method>,
        extensionContext: ExtensionContext
    ) {
        val annotation = invocationContext.testMethod
            .flatMap { it.getAnnotation(FlakyTest::class.java).stream() }
            .findFirst().orElse(null) ?: return invocation.proceed()

        var lastException: Throwable? = null
        repeat(annotation.maxRetries) { attempt ->
            try {
                invocation.proceed()
                return
            } catch (e: Throwable) {
                lastException = e
                println("Flaky test retry ${attempt + 1}/${annotation.maxRetries}: ${e.message}")
                Thread.sleep(1000)
            }
        }
        throw lastException!!
    }
}
```

**Flaky test tracking:**

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

### Test Rules & Utilities

```kotlin
// Main dispatcher override rule
class MainDispatcherRule(
    private val testDispatcher: TestDispatcher = UnconfinedTestDispatcher()
) : TestWatcher() {
    override fun starting(description: Description) { Dispatchers.setMain(testDispatcher) }
    override fun finished(description: Description) { Dispatchers.resetMain() }
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

// Mock API server
class MockApiServer {
    private val server = MockWebServer()

    fun start() = server.start()
    fun shutdown() = server.shutdown()
    fun baseUrl(): String = server.url("/").toString()

    fun enqueueResponse(
        fileName: String,
        responseCode: Int = 200,
        headers: Map<String, String> = emptyMap()
    ) {
        val inputStream = javaClass.classLoader?.getResourceAsStream("api-responses/$fileName")
        val body = inputStream?.bufferedReader()?.use { it.readText() } ?: ""
        val mockResponse = MockResponse().setResponseCode(responseCode).setBody(body)
        headers.forEach { (key, value) -> mockResponse.setHeader(key, value) }
        server.enqueue(mockResponse)
    }

    fun takeRequest(): RecordedRequest = server.takeRequest(5, TimeUnit.SECONDS)
        ?: throw AssertionError("No request received")
}
```

---

## Pipeline Integration

- **Stage 4 (Implementation Plan):** Test infrastructure tasks included in implementation plan: fixture creation, CI pipeline setup, test rule development, flaky test monitoring, Maestro flow design.
- **Stage 5 (Development):** TDD practiced during development. Unit tests written alongside production code. Test utilities and factories built incrementally.
- **Stage 6 (Code Review):** Test coverage reviewed: domain layer >80%, presentation layer >60%, data layer >70%. Test quality assessed (meaningful assertions, no false positives). CI pipeline efficiency reviewed.
- **Stage 7 (Automated Testing):** Primary stage for this skill. Full test suite execution: unit tests (JVM), instrumented tests (emulator), Maestro E2E flows. Target: 100% pass rate.
- **Stage 8 (Integrity Verification):** Regression test suite executed on all fixed functionalities. Test suite completeness verified against PRD requirements via traceability matrix.

## Quality Standards

- **>80%** unit test coverage on domain layer (use cases, entities, validators)
- **>60%** test coverage on presentation layer (ViewModels, mappers)
- **>70%** test coverage on data layer (repositories, mappers, API clients)
- **100%** of public use case methods have unit tests
- **100%** of core user flows have UI test coverage (happy path + error paths)
- **Zero** flaky tests in CI — flaky tests quarantined and fixed within 1 sprint
- All coroutine tests use `TestDispatcher` — no `Thread.sleep()` in test code
- Test fixtures use factory pattern — no inline test data construction
- MockWebServer used for all network-dependent tests — no real network calls in tests
- Test execution time **<30 seconds** for full unit test suite on CI
- Full test suite (unit + instrumented + E2E) completes in **<45 minutes** on CI
- Screenshot tests cover all screen variants (light/dark theme, different locales)
- Accessibility checks included in UI test assertions (Stage 8 requirement)
- Coverage reports uploaded to Codecov with **fail-on-decrease** threshold
- Database tests use **in-memory Room** — no file system dependencies
