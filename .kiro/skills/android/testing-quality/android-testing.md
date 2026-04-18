---
name: android-testing
description: This skill establishes comprehensive Android testing practices covering TDD methodology, unit testing with JUnit 5 and MockK, UI testing with Espresso and Compose Testing.
---

# Android Testing

**Category:** Mobile Engineering — Android Testing
**Owner:** Senior Android Engineer (Sofia Rezende)

## Overview

This skill establishes comprehensive Android testing practices covering TDD methodology, unit testing with JUnit 5 and MockK, UI testing with Espresso and Compose Testing, Robolectric for JVM-based Android framework tests, and test utility architecture. It is foundational to Stage 7 (Automated Testing) where the 100% automated test pass rate target is enforced, and Stage 6 (Code Review) where test coverage and quality are evaluated.

## Competency Dimensions

| Dimension           | Description                                                                                     | Proficiency Indicators                                                                                               |
| ------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| TDD Methodology     | Red-Green-Refactor cycle, test-first design, emergent architecture through testing              | Writes failing test before implementation; test suite drives design decisions; refactoring phase preserves all tests |
| Unit Testing        | JUnit 5, MockK, coroutine testing with TestDispatcher, parameterized tests, assertion libraries | >80% unit test coverage on domain layer; all use cases have unit tests; coroutine tests use controlled dispatchers   |
| UI Testing          | Espresso, Compose Testing, UiAutomator, screenshot testing, flaky test mitigation               | Core user flows covered by UI tests; screenshot tests catch visual regressions; flaky test rate <1%                  |
| Robolectric         | JVM-based Android framework testing, shadow objects, resource loading, manifest simulation      | Tests run on JVM without emulator; Android framework classes properly shadowed; test execution <2s per test          |
| Test Infrastructure | Test fixtures, factories, builders, mock servers, test runners, parallel execution              | Test data generation is declarative; mock server returns deterministic responses; tests run in parallel where safe   |

## Execution Guidance

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
        // Given
        every { cartRepository.getCart() } returns Cart.empty()

        // When
        val result = useCase.execute()

        // Then
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
        if (cart.items.isEmpty()) {
            return Result.failure(ValidationError.EMPTY_CART)
        }
        return Result.success(CheckoutValidation(cart))
    }
}

// STEP 3: REFACTOR — Improve code while keeping tests green
// Extract validation logic, improve naming, remove duplication
// All tests still pass — confidence that refactoring didn't break behavior
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
        // Given
        val user = UserFactory.create(id = "user-123", name = "John Doe")
        val profile = ProfileFactory.createFromUser(user)

        every { userRepository.getUser("user-123") } returns Result.success(user)
        every { profileMapper.toProfile(user) } returns profile

        // When
        val result = useCase.execute("user-123")

        // Then
        assertTrue(result.isSuccess)
        assertEquals(profile, result.getOrNull())

        coVerify(exactly = 1) { userRepository.getUser("user-123") }
        verify(exactly = 1) { profileMapper.toProfile(user) }
    }

    @Test
    fun `given network error, when execute, then returns network error`() = runTest(testDispatcher) {
        // Given
        every { userRepository.getUser(any()) } returns Result.failure(NetworkException())

        // When
        val result = useCase.execute("user-123")

        // Then
        assertTrue(result.isFailure)
        assertIs<NetworkException>(result.exceptionOrNull())
    }

    @Test
    fun `given null user id, when execute, then throws invalid argument`() = runTest(testDispatcher) {
        // When/Then
        assertFailsWith<IllegalArgumentException> {
            useCase.execute("")
        }
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
    ): User {
        return User(
            id = id,
            name = name,
            email = email,
            createdAt = createdAt,
            preferences = UserPreferencesFactory.create()
        )
    }
}

object UserPreferencesFactory {
    fun create(
        theme: Theme = Theme.LIGHT,
        notificationsEnabled: Boolean = true,
        language: String = "en"
    ): UserPreferences {
        return UserPreferences(theme, notificationsEnabled, language)
    }
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
        // Given
        fakeRepository.users = listOf(
            UserFactory.create(id = "1", name = "Alice"),
            UserFactory.create(id = "2", name = "Bob")
        )

        // When
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

        // Then
        composeTestRule.onNodeWithText("Alice").assertIsDisplayed()
        composeTestRule.onNodeWithText("Bob").assertIsDisplayed()
    }

    @Test
    fun whenDeleteUser_tapped_removeUserFromList() {
        // Given
        val deletedUserIds = mutableListOf<String>()
        val deleteUserUseCase = mockk<DeleteUserUseCase>(relaxed = true) {
            coEvery { execute(any()) } answers {
                deletedUserIds.add(firstArg())
                Result.success(Unit)
            }
        }

        composeTestRule.setContent {
            AppTheme {
                UserListScreen(
                    viewModel = UserListViewModel(
                        getUsersUseCase = GetUsersUseCase(FakeUserRepository(listOf(
                            UserFactory.create(id = "1", name = "Alice")
                        ))),
                        deleteUserUseCase = deleteUserUseCase
                    )
                )
            }
        }

        // When
        composeTestRule.onNodeWithContentDescription("Delete Alice").performClick()

        // Then
        composeTestRule.waitForIdle()
        assertEquals(listOf("1"), deletedUserIds)
    }

    @Test
    fun whenLoading_showsLoadingIndicator() {
        // Given: repository that never completes (simulates loading)
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

        // Then
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
        // Given
        storage.save("test_key", "test_value")

        // When
        val result = storage.get("test_key")

        // Then
        assertEquals("test_value", result)
    }

    @Test
    fun `given key does not exist, when get, then returns null`() {
        // When
        val result = storage.get("nonexistent_key")

        // Then
        assertNull(result)
    }

    @Test
    fun `when delete, then key is removed`() {
        // Given
        storage.save("test_key", "test_value")

        // When
        storage.delete("test_key")

        // Then
        assertNull(storage.get("test_key"))
    }
}
```

**Robolectric configuration for resource loading:**

```kotlin
@RunWith(RobolectricTestRunner::class)
@Config(
    sdk = [33],
    application = TestApplication::class,
    qualifiers = "en-rUS"
)
class ResourceLoadingTest {

    @Test
    fun `loads string resources correctly`() {
        val context = ApplicationProvider.getApplicationContext<Application>()
        val appName = context.getString(R.string.app_name)
        assertEquals("MyApp", appName)
    }

    @Test
    fun `loads drawable resources correctly`() {
        val context = ApplicationProvider.getApplicationContext<Application>()
        val drawable = ContextCompat.getDrawable(context, R.drawable.ic_launcher)
        assertNotNull(drawable)
    }
}
```

### Test Infrastructure — Mock Server

```kotlin
class MockApiServer {

    private val server = MockWebServer()

    fun start() {
        server.start()
    }

    fun shutdown() {
        server.shutdown()
    }

    fun baseUrl(): String = server.url("/").toString()

    fun enqueueResponse(
        fileName: String,
        responseCode: Int = 200,
        headers: Map<String, String> = emptyMap()
    ) {
        val inputStream = javaClass.classLoader?.getResourceAsStream("api-responses/$fileName")
        val body = inputStream?.bufferedReader()?.use { it.readText() } ?: ""

        val mockResponse = MockResponse()
            .setResponseCode(responseCode)
            .setBody(body)

        headers.forEach { (key, value) ->
            mockResponse.setHeader(key, value)
        }

        server.enqueue(mockResponse)
    }

    fun takeRequest(): RecordedRequest = server.takeRequest(5, TimeUnit.SECONDS)
        ?: throw AssertionError("No request received")
}

// Test fixture JSON files in src/test/resources/api-responses/
// user-success.json, user-not-found.json, server-error.json, etc.
```

### Flaky Test Mitigation

**Common causes and fixes:**

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

    // Wait for state change with timeout
    composeTestRule.waitUntil(timeoutMillis = 1_000) {
        composeTestRule.onAllNodesWithText("Success").fetchSemanticsNodes().isNotEmpty()
    }

    composeTestRule.onNodeWithText("Success").assertIsDisplayed()
}

// WRONG: Arbitrary sleep (flaky)
@Test
fun whenUserClicks_seeConfirmation_flaky() {
    composeTestRule.onNodeWithText("Submit").performClick()
    Thread.sleep(500)  // ❌ May be too short or too long
    composeTestRule.onNodeWithText("Success").assertIsDisplayed()
}
```

## Pipeline Integration

- **Stage 5 (Development):** TDD practiced during development. Unit tests written alongside production code. Test utilities and factories built incrementally.
- **Stage 6 (Code Review):** Test coverage reviewed: domain layer >80%, presentation layer >60%, data layer >70%. Test quality assessed (meaningful assertions, no false positives).
- **Stage 7 (Automated Testing):** Primary stage for this skill. Full test suite execution: unit tests (JVM), instrumented tests (emulator), screenshot tests. Target: 100% pass rate.
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
- Screenshot tests cover all screen variants (light/dark theme, different locales)
- Accessibility checks included in UI test assertions (Stage 8 requirement)
