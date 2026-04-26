# Android Unit Testing

## Android Unit Testing

### Testing Stack

| Component             | Library                         | Version      | Purpose                  |
| --------------------- | ------------------------------- | ------------ | ------------------------ |
| Test Runner           | JUnit 5 (JUnit Jupiter)         | 5.10+        | Test framework           |
| Assertions            | Truth or AssertJ                | 1.2+ / 3.24+ | Fluent assertions        |
| Mocking               | MockK                           | 1.13+        | Kotlin-native mocking    |
| Android Simulation    | Robolectric                     | 4.11+        | Android framework on JVM |
| Coroutine Testing     | kotlinx-coroutines-test         | 1.8+         | Testing coroutines       |
| Instant Task Executor | androidx.arch.core:core-testing | 2.2+         | LiveData testing         |
| Fake Data             | Kotlin Faker                    | 1.16+        | Synthetic test data      |

### Project Structure

```
app/src/
├── main/                    # Production code
│   ├── kotlin/com/company/app/
│   │   ├── data/
│   │   │   ├── repository/
│   │   │   ├── local/
│   │   │   └── remote/
│   │   ├── domain/
│   │   │   ├── model/
│   │   │   └── usecase/
│   │   └── presentation/
│   │       ├── viewmodel/
│   │       └── ui/
│   └── res/
├── test/                    # JVM unit tests (no Android framework)
│   └── kotlin/com/company/app/
│       ├── data/
│       │   └── repository/
│       │       └── UserRepositoryTest.kt
│       └── domain/
│           └── usecase/
│               └── LoginUseCaseTest.kt
└── testDebugUnitTest/       # Debug-only unit tests
    └── kotlin/
```

**Gradle Configuration:**

```kotlin
// app/build.gradle.kts
dependencies {
    // Test dependencies
    testImplementation(libs.junit.jupiter)
    testImplementation(libs.truth)
    testImplementation(libs.mockk)
    testImplementation(libs.kotlinx.coroutines.test)
    testImplementation(libs.turbine)
    testRuntimeOnly(libs.junit.jupiter.engine)

    // Robolectric for Android framework simulation
    testImplementation(libs.robolectric)

    // Architecture components testing
    testImplementation(libs.arch.core.testing)
}

tasks.withType<Test> {
    useJUnitPlatform()
    maxParallelForks = Runtime.getRuntime().availableProcessors()
    testLogging {
        events("passed", "skipped", "failed")
        showStandardStreams = true
    }
}
```

### JUnit 5 Test Patterns

**Basic Test Structure:**

```kotlin
package com.company.app.domain.usecase

import com.company.app.data.repository.UserRepository
import com.company.app.domain.model.User
import com.company.app.domain.result.Result
import io.kotest.matchers.shouldBe
import io.kotest.matchers.types.shouldBeInstanceOf
import io.mockk.coEvery
import io.mockk.coVerify
import io.mockk.mockk
import kotlinx.coroutines.test.runTest
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Nested
import org.junit.jupiter.api.Test
import org.junit.jupiter.params.ParameterizedTest
import org.junit.jupiter.params.provider.ValueSource

@DisplayName("LoginUseCase")
class LoginUseCaseTest {

    private lateinit var userRepository: UserRepository
    private lateinit var loginUseCase: LoginUseCase

    @BeforeEach
    fun setUp() {
        userRepository = mockk()
        loginUseCase = LoginUseCase(userRepository)
    }

    @Nested
    @DisplayName("Given valid credentials")
    inner class ValidCredentials {

        @Test
        fun `should return success with user when login succeeds`() = runTest {
            // Given
            val email = "alice@example.com"
            val password = "SecurePass123!"
            val expectedUser = User(id = "1", name = "Alice", email = email)
            coEvery { userRepository.login(email, password) } returns
                Result.Success(expectedUser)

            // When
            val result = loginUseCase.execute(email, password)

            // Then
            result.shouldBeInstanceOf<Result.Success>()
            (result as Result.Success).data shouldBe expectedUser
            coVerify(exactly = 1) { userRepository.login(email, password) }
        }
    }

    @Nested
    @DisplayName("Given invalid credentials")
    inner class InvalidCredentials {

        @ParameterizedTest(name = "should fail for empty {0}")
        @ValueSource(strings = ["", "   ", "\t", "\n"])
        fun `should return error for invalid email format`(invalidEmail: String) = runTest {
            // When
            val result = loginUseCase.execute(invalidEmail, "password123")

            // Then
            result.shouldBeInstanceOf<Result.Error>()
        }

        @Test
        fun `should return authentication error when credentials are wrong`() = runTest {
            // Given
            coEvery { userRepository.login("user@test.com", "wrong") } returns
                Result.Error(AuthenticationException("Invalid credentials"))

            // When
            val result = loginUseCase.execute("user@test.com", "wrong")

            // Then
            result.shouldBeInstanceOf<Result.Error>()
            (result as Result.Error).exception.shouldBeInstanceOf<AuthenticationException>()
        }
    }

    @Nested
    @DisplayName("Given network failure")
    inner class NetworkFailure {

        @Test
        fun `should return network error when API is unreachable`() = runTest {
            // Given
            coEvery { userRepository.login(any(), any()) } throws
                java.net.SocketTimeoutException("Connection timed out")

            // When
            val result = loginUseCase.execute("user@test.com", "password")

            // Then
            result.shouldBeInstanceOf<Result.Error>()
        }
    }
}
```

### Mockito vs. MockK

**MockK is preferred for Kotlin codebases** because it handles Kotlin-specific features that Mockito struggles with.

| Feature                        | MockK              | Mockito                            |
| ------------------------------ | ------------------ | ---------------------------------- |
| Kotlin coroutines (`coEvery`)  | Native support     | Requires mockito-kotlin wrapper    |
| Object mocking (`mockkObject`) | Native support     | Requires static mocking workaround |
| Extension functions            | Supported          | Not supported                      |
| Default arguments              | Preserved          | Requires explicit setup            |
| Sealed class matching          | `match { }` blocks | Limited support                    |
| Relaxed mocks                  | `relaxed = true`   | `CALLS_REAL_METHODS`               |

```kotlin
// MockK — Kotlin-native
val mockRepo = mockk<UserRepository>()
coEvery { mockRepo.getUser("1") } returns Result.Success(User("1", "Alice"))

// Mockito-Kotlin — Requires wrapper
val mockRepo = mock<UserRepository>()
whenever(mockRepo.getUser("1")).thenReturn(Result.Success(User("1", "Alice")))
```

### Robolectric (Android Framework Simulation)

Use Robolectric when you need to test code that interacts with the Android framework but don't want the overhead of instrumented tests.

```kotlin
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [34])
class SharedPreferencesStorageTest {

    @Test
    fun `should save and retrieve auth token`() {
        val context = ApplicationProvider.getApplicationContext<Application>()
        val storage = SharedPreferencesStorage(context, "test_prefs")

        storage.saveAuthToken("test-token-123")

        assertThat(storage.getAuthToken()).isEqualTo("test-token-123")
    }

    @Test
    fun `should return null when no token saved`() {
        val context = ApplicationProvider.getApplicationContext<Application>()
        val storage = SharedPreferencesStorage(context, "test_prefs")

        assertThat(storage.getAuthToken()).isNull()
    }

    @Test
    fun `should clear token on logout`() {
        val context = ApplicationProvider.getApplicationContext<Application>()
        val storage = SharedPreferencesStorage(context, "test_prefs")
        storage.saveAuthToken("test-token")

        storage.clear()

        assertThat(storage.getAuthToken()).isNull()
    }
}
```

### Coroutine Testing

**kotlinx-coroutines-test** is the standard library for testing coroutine-based code.

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class ViewModelCoroutineTest {

    @get:Rule
    val mainDispatcherRule = StandardTestDispatcherRule()

    private val repository = mockk<UserRepository>()
    private lateinit var viewModel: UserViewModel

    @BeforeEach
    fun setUp() {
        viewModel = UserViewModel(repository)
    }

    @Test
    fun `should emit loading then success when fetch succeeds`() = runTest {
        // Given
        val user = User("1", "Alice")
        coEvery { repository.fetchUser("1") } returns Result.Success(user)

        // When
        viewModel.loadUser("1")

        // Then — use Turbine for Flow assertions
        viewModel.uiState.test {
            awaitItem().shouldBeInstanceOf<UiState.Loading>()
            awaitItem().shouldBeInstanceOf<UiState.Success>()
            cancelAndIgnoreRemainingEvents()
        }
    }

    @Test
    fun `should emit loading then error when fetch fails`() = runTest {
        // Given
        coEvery { repository.fetchUser("1") } returns
            Result.Error(NetworkException("No connection"))

        // When
        viewModel.loadUser("1")

        // Then
        viewModel.uiState.test {
            awaitItem().shouldBeInstanceOf<UiState.Loading>()
            val error = awaitItem() as UiState.Error
            error.message shouldBe "No connection"
            cancelAndIgnoreRemainingEvents()
        }
    }

    @Test
    fun `should debounce rapid search input`() = runTest {
        // Given
        coEvery { repository.searchUsers(any()) } returns
            Result.Success(emptyList())

        // When — emit 5 searches in 100ms
        viewModel.onSearchQueryChanged("a")
        viewModel.onSearchQueryChanged("al")
        viewModel.onSearchQueryChanged("ali")
        viewModel.onSearchQueryChanged("alic")
        viewModel.onSearchQueryChanged("alice")

        // Advance time past debounce window
        advanceTimeBy(500)

        // Then — only last query should trigger API call
        coVerify(exactly = 1) { repository.searchUsers("alice") }
        coVerify(exactly = 0) { repository.searchUsers("a") }
        coVerify(exactly = 0) { repository.searchUsers("al") }
    }
}

// Test dispatcher rule
class StandardTestDispatcherRule(
    val testDispatcher: TestDispatcher = StandardTestDispatcher()
) : TestWatcher() {
    override fun starting(description: Description) {
        Dispatchers.setMain(testDispatcher)
    }
    override fun finished(description: Description) {
        Dispatchers.resetMain()
    }
}
```

### Compose Testing

Compose Testing tests individual Compose UI components in isolation.

```kotlin
@Test
fun `user card displays name and email`() {
    val user = User("1", "Alice Johnson", "alice@example.com")

    composeTestRule.setContent {
        UserCard(user = user)
    }

    composeTestRule.onNodeWithText("Alice Johnson").assertIsDisplayed()
    composeTestRule.onNodeWithText("alice@example.com").assertIsDisplayed()
}

@Test
fun `user card shows avatar when available`() {
    val user = User(
        id = "1",
        name = "Alice",
        avatarUrl = "https://example.com/avatar.jpg"
    )

    composeTestRule.setContent {
        UserCard(user = user)
    }

    composeTestRule.onNodeWithContentDescription("User avatar").assertIsDisplayed()
}

@Test
fun `user card shows placeholder when no avatar`() {
    val user = User("1", "Alice", avatarUrl = null)

    composeTestRule.setContent {
        UserCard(user = user)
    }

    composeTestRule.onNodeWithContentDescription("User avatar").assertDoesNotExist()
    composeTestRule.onNodeWithText("A").assertIsDisplayed() // Initial placeholder
}
```

---
