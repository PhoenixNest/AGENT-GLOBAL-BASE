---
name: testing-qa-mobile-mobile-unit-testing
description: 'Testing Qa skill: Mobile Unit Testing'
---

# Mobile Unit Testing

## Overview

Unit testing is the foundation of the mobile test pyramid. This skill provides detailed guidance for writing effective unit tests across Android (Kotlin), iOS (Swift), and cross-platform (KMP/Flutter) codebases.

### Scope and Purpose

**Unit tests verify that individual functions, methods, or classes produce correct outputs for given inputs, in isolation from external dependencies.**

| Aspect              | Description                                            |
| ------------------- | ------------------------------------------------------ |
| **Scope**           | Single class, function, or module boundary             |
| **Dependencies**    | All external dependencies replaced with test doubles   |
| **Execution**       | Milliseconds per test, no I/O, no network, no database |
| **Determinism**     | Same inputs always produce same outputs                |
| **Coverage Target** | >= 80% branch coverage, >= 90% line coverage           |

### What Makes a Good Unit Test?

```
A Good Unit Test is:
├── FAST     — Executes in < 100ms
├── ISOLATED — No shared state, no order dependency
├── REPEATABLE — Same result every time, every machine
├── SELF-VALIDATING — Pass or fail, no manual inspection
├── TIMELY   — Written before or alongside production code
└── CLEAR    — Intent is obvious from reading the test name
```

### Coverage Targets

| Metric                 | Minimum Target | Rationale                                           |
| ---------------------- | -------------- | --------------------------------------------------- |
| Line Coverage          | 90%            | Most lines should be exercised                      |
| Branch Coverage        | 80%            | All if/else, when/switch paths tested               |
| Function Coverage      | 95%            | Almost every function should have at least one test |
| Critical Path Coverage | 100%           | Business logic, security, payments — no exceptions  |

**What NOT to cover:**

- Generated code (data classes, simple getters)
- Framework delegation (lifecycle methods that just call super)
- Third-party library code
- UI rendering (use dedicated UI testing tools)
- Simple property accessors

---

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

## iOS Unit Testing

### Testing Stack

| Component      | Framework                             | Purpose                               |
| -------------- | ------------------------------------- | ------------------------------------- |
| Test Framework | XCTest                                | Traditional test framework            |
| Test Framework | Swift Testing                         | Modern Swift-native testing (iOS 18+) |
| Mocking        | Manual (protocols) or Cuckoo          | Dependency injection                  |
| Assertions     | XCTestAssertions / Swift Expectations | Test assertions                       |
| Async Testing  | XCTest async/await                    | Testing async/await code              |
| Code Coverage  | Xcode Coverage                        | Built-in coverage reporting           |

### Project Structure

```
App/
├── App/                    # Production code
│   ├── Data/
│   │   ├── Repository/
│   │   ├── Local/
│   │   └── Remote/
│   ├── Domain/
│   │   ├── Model/
│   │   └── UseCase/
│   └── Presentation/
│       ├── ViewModel/
│       └── Views/
└── AppTests/               # Unit tests
    ├── Data/
    │   └── Repository/
    │       └── UserRepositoryTests.swift
    └── Domain/
        └── UseCase/
            └── LoginUseCaseTests.swift
```

### XCTest Test Patterns

**Basic Test Structure:**

```swift
import XCTest
@testable import App

@MainActor
final class LoginUseCaseTests: XCTestCase {

    var userRepository: MockUserRepository!
    var loginUseCase: LoginUseCase!

    override func setUpWithError() throws {
        try super.setUpWithError()
        userRepository = MockUserRepository()
        loginUseCase = LoginUseCase(repository: userRepository)
    }

    override func tearDownWithError() throws {
        loginUseCase = nil
        userRepository = nil
        try super.tearDownWithError()
    }

    // MARK: - Valid Credentials

    func test_loginWithValidCredentials_returnsSuccess() async {
        // Given
        let email = "alice@example.com"
        let password = "SecurePass123!"
        let expectedUser = User(id: "1", name: "Alice", email: email)
        userRepository.mockedLoginResult = .success(expectedUser)

        // When
        let result = await loginUseCase.execute(email: email, password: password)

        // Then
        switch result {
        case .success(let user):
            XCTAssertEqual(user.id, "1")
            XCTAssertEqual(user.name, "Alice")
            XCTAssertEqual(user.email, email)
        case .failure:
            XCTFail("Expected success but got failure")
        }

        XCTAssertEqual(userRepository.loginCallCount, 1)
        XCTAssertEqual(userRepository.lastLoginEmail, email)
    }

    // MARK: - Invalid Credentials

    func test_loginWithEmptyEmail_returnsValidationError() async {
        // When
        let result = await loginUseCase.execute(email: "", password: "password123")

        // Then
        switch result {
        case .success:
            XCTFail("Expected validation error but got success")
        case .failure(let error):
            XCTAssertTrue(error is ValidationError)
        }
    }

    func test_loginWithWrongPassword_returnsAuthenticationError() async {
        // Given
        userRepository.mockedLoginResult = .failure(
            AuthenticationError.invalidCredentials
        )

        // When
        let result = await loginUseCase.execute(
            email: "user@test.com",
            password: "wrong"
        )

        // Then
        switch result {
        case .success:
            XCTFail("Expected auth error but got success")
        case .failure(let error):
            XCTAssertTrue(error is AuthenticationError)
        }
    }

    // MARK: - Network Failure

    func test_loginWithNetworkFailure_returnsNetworkError() async {
        // Given
        userRepository.mockedLoginResult = .failure(
            NetworkError.connectionTimeout
        )

        // When
        let result = await loginUseCase.execute(
            email: "user@test.com",
            password: "password"
        )

        // Then
        switch result {
        case .success:
            XCTFail("Expected network error but got success")
        case .failure(let error):
            XCTAssertTrue(error is NetworkError)
        }
    }
}
```

### Swift Testing (Modern, iOS 18+)

```swift
import Testing
@testable import App

@Suite("LoginUseCase Tests")
@MainActor
struct LoginUseCaseTests {

    var userRepository: MockUserRepository!
    var loginUseCase: LoginUseCase!

    init() async throws {
        userRepository = MockUserRepository()
        loginUseCase = LoginUseCase(repository: userRepository)
    }

    @Test("Login with valid credentials returns success")
    func loginWithValidCredentials() async {
        let expectedUser = User(id: "1", name: "Alice", email: "alice@example.com")
        userRepository.mockedLoginResult = .success(expectedUser)

        let result = await loginUseCase.execute(
            email: "alice@example.com",
            password: "SecurePass123!"
        )

        switch result {
        case .success(let user):
            #expect(user.id == "1")
            #expect(user.name == "Alice")
            #expect(user.email == "alice@example.com")
        case .failure(let error):
            Issue.record("Expected success but got \(error)")
        }
    }

    @Test("Login with empty email returns validation error")
    @Arguments(["", "   ", "\t", "\n"])
    func loginWithInvalidEmail(email: String) async {
        let result = await loginUseCase.execute(email: email, password: "password123")

        switch result {
        case .success:
            Issue.record("Expected validation error but got success")
        case .failure(let error):
            #expect(error is ValidationError)
        }
    }
}
```

### Dependency Injection Pattern

**Protocol-based DI is the standard for testable Swift code:**

```swift
// Production protocol
protocol UserRepositoryProtocol {
    func login(email: String, password: String) async -> Result<User, Error>
    func fetchUser(_ userId: String) async -> Result<User, Error>
}

// Production implementation
class UserRepository: UserRepositoryProtocol {
    private let apiClient: APIClient
    private let database: Database

    init(apiClient: APIClient, database: Database) {
        self.apiClient = apiClient
        self.database = database
    }

    func login(email: String, password: String) async -> Result<User, Error> {
        // Real implementation
    }

    func fetchUser(_ userId: String) async -> Result<User, Error> {
        // Real implementation
    }
}

// Test double
final class MockUserRepository: UserRepositoryProtocol {
    var mockedLoginResult: Result<User, Error>?
    var mockedFetchUserResult: Result<User, Error>?
    var loginCallCount = 0
    var lastLoginEmail: String?

    func login(email: String, password: String) async -> Result<User, Error> {
        loginCallCount += 1
        lastLoginEmail = email
        return mockedLoginResult!
    }

    func fetchUser(_ userId: String) async -> Result<User, Error> {
        return mockedFetchUserResult!
    }
}
```

### Async/Await Testing

```swift
@MainActor
final class ViewModelAsyncTests: XCTestCase {

    var repository: MockUserRepository!
    var viewModel: UserViewModel!

    override func setUp() {
        repository = MockUserRepository()
        viewModel = UserViewModel(repository: repository)
    }

    func test_loadUser_emitsLoadingThenSuccess() async {
        // Given
        let user = User(id: "1", name: "Alice", email: "alice@example.com")
        repository.mockedFetchUserResult = .success(user)

        // When
        let expectation = expectation(description: "State changes")
        expectation.expectedFulfillmentCount = 2

        var states: [UserViewState] = []
        viewModel.$viewState.sink { state in
            states.append(state)
            expectation.fulfill()
        }.store(in: &cancellables)

        viewModel.loadUser("1")

        // Then
        await fulfillment(of: [expectation], timeout: 1.0)

        XCTAssertTrue(states[0] is UserViewState.Loading)
        if case .success(let loadedUser) = states[1] {
            XCTAssertEqual(loadedUser.name, "Alice")
        } else {
            XCTFail("Expected success state")
        }
    }

    func test_loadUser_emitsErrorOnFailure() async {
        // Given
        repository.mockedFetchUserResult = .failure(
            NetworkError.connectionTimeout
        )

        let expectation = expectation(description: "Error state emitted")
        var emittedError: UserViewState?

        viewModel.$viewState.dropFirst().sink { state in
            emittedError = state
            expectation.fulfill()
        }.store(in: &cancellables)

        // When
        viewModel.loadUser("1")

        // Then
        await fulfillment(of: [expectation], timeout: 1.0)

        if case .error(let message) = emittedError {
            XCTAssertFalse(message.isEmpty)
        } else {
            XCTFail("Expected error state")
        }
    }
}
```

---

## Cross-Platform Unit Testing

### KMP Shared Module Testing

KMP (Kotlin Multiplatform) shared modules are tested using JUnit 5 on the JVM because shared business logic has no platform dependencies.

```kotlin
// shared/src/commonTest/kotlin/com/company/app/LoginUseCaseTest.kt
// Runs on JVM via JUnit 5

class LoginUseCaseTest {
    private val repository = FakeUserRepository()
    private val loginUseCase = LoginUseCase(repository)

    @Test
    fun `login with valid credentials returns success`() = runTest {
        val result = loginUseCase.execute("alice@example.com", "password")
        assertTrue(result.isSuccess)
        assertEquals("Alice", result.getOrNull()?.name)
    }

    @Test
    fun `login with invalid email returns error`() = runTest {
        val result = loginUseCase.execute("", "password")
        assertTrue(result.isError)
    }
}

// Fake implementation in commonTest
class FakeUserRepository : UserRepository {
    var shouldSucceed = true
    var loginCallCount = 0

    override suspend fun login(email: String, password: String): Result<User> {
        loginCallCount++
        return if (shouldSucceed) {
            Result.Success(User("1", "Alice", email))
        } else {
            Result.Error(AuthenticationException("Invalid credentials"))
        }
    }
}
```

**Gradle Configuration for KMP Testing:**

```kotlin
kotlin {
    sourceSets {
        val commonTest by getting {
            dependencies {
                implementation(kotlin("test"))
                implementation(libs.kotlinx.coroutines.test)
                implementation(libs.turbine)
            }
        }
        val jvmTest by getting {
            dependencies {
                implementation(libs.junit.jupiter)
            }
        }
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

### Flutter Widget Testing

Flutter's `flutter_test` package provides widget-level unit testing.

```dart
// test/user_card_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:app/presentation/widgets/user_card.dart';
import 'package:app/domain/models/user.dart';

void main() {
  group('UserCard Widget Tests', () {
    testWidgets('displays user name and email', (WidgetTester tester) async {
      // Given
      final user = User(
        id: '1',
        name: 'Alice Johnson',
        email: 'alice@example.com',
      );

      // When
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(user: user),
          ),
        ),
      );

      // Then
      expect(find.text('Alice Johnson'), findsOneWidget);
      expect(find.text('alice@example.com'), findsOneWidget);
    });

    testWidgets('shows avatar when available', (WidgetTester tester) async {
      // Given
      final user = User(
        id: '1',
        name: 'Alice',
        email: 'alice@example.com',
        avatarUrl: 'https://example.com/avatar.jpg',
      );

      // When
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(user: user),
          ),
        ),
      );

      // Then
      expect(find.byType(CircleAvatar), findsOneWidget);
    });

    testWidgets('shows initial placeholder when no avatar', (WidgetTester tester) async {
      // Given
      final user = User(
        id: '1',
        name: 'Alice Johnson',
        email: 'alice@example.com',
        avatarUrl: null,
      );

      // When
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(user: user),
          ),
        ),
      );

      // Then
      expect(find.byType(CircleAvatar), findsNothing);
      expect(find.text('A'), findsOneWidget); // First initial
    });

    testWidgets('triggers onTap callback', (WidgetTester tester) async {
      // Given
      final user = User(id: '1', name: 'Alice', email: 'alice@example.com');
      var tapped = false;

      // When
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(
              user: user,
              onTap: () => tapped = true,
            ),
          ),
        ),
      );

      await tester.tap(find.byType(UserCard));
      await tester.pump();

      // Then
      expect(tapped, isTrue);
    });
  });
}
```

**Running Flutter Tests:**

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/user_card_test.dart

# Run with coverage
flutter test --coverage

# View coverage report
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

---

## ViewModel Testing

ViewModel testing is a critical pattern in MVVM architecture. The ViewModel translates user actions into state changes and exposes them via StateFlow/Combine.

### Android ViewModel Testing

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class UserViewModelTest {

    @get:Rule
    val mainDispatcherRule = StandardTestDispatcherRule()

    private val userRepository = mockk<UserRepository>()
    private lateinit var viewModel: UserViewModel

    @BeforeEach
    fun setUp() {
        viewModel = UserViewModel(userRepository)
    }

    @Test
    fun `initial state is loading`() = runTest {
        // No API call yet — state should be initial
        viewModel.uiState.value.shouldBeInstanceOf<UiState.Initial>()
    }

    @Test
    fun `loadUser emits loading then success`() = runTest {
        // Given
        val user = User("1", "Alice", "alice@example.com")
        coEvery { userRepository.fetchUser("1") } returns Result.Success(user)

        // When
        viewModel.loadUser("1")

        // Then — collect flow
        val states = mutableListOf<UiState>()
        val job = launch {
            viewModel.uiState.toList(states)
        }

        advanceUntilIdle()
        job.cancel()

        states shouldHaveSize 2
        states[0].shouldBeInstanceOf<UiState.Loading>()
        (states[1] as UiState.Success).user shouldBe user
    }

    @Test
    fun `loadUser emits loading then error on failure`() = runTest {
        // Given
        coEvery { userRepository.fetchUser("1") } returns
            Result.Error(NetworkException("No connection"))

        // When
        viewModel.loadUser("1")

        // Then
        val states = mutableListOf<UiState>()
        val job = launch {
            viewModel.uiState.toList(states)
        }

        advanceUntilIdle()
        job.cancel()

        states shouldHaveSize 2
        states[0].shouldBeInstanceOf<UiState.Loading>()
        (states[1] as UiState.Error).message shouldBe "No connection"
    }

    @Test
    fun `refreshUser does not emit loading when data exists`() = runTest {
        // Given — user already loaded
        val user = User("1", "Alice", "alice@example.com")
        coEvery { userRepository.fetchUser("1") } returns Result.Success(user)
        viewModel.loadUser("1")
        advanceUntilIdle()

        // Mock refresh result
        val refreshedUser = user.copy(name = "Alice Updated")
        coEvery { userRepository.fetchUser("1") } returns Result.Success(refreshedUser)

        // When
        viewModel.refreshUser()

        // Then — should NOT go through loading state on refresh
        val states = mutableListOf<UiState>()
        val job = launch {
            viewModel.uiState.toList(states)
        }

        advanceUntilIdle()
        job.cancel()

        // First state is the existing success, then refresh success
        states.last().shouldBeInstanceOf<UiState.Success>()
        (states.last() as UiState.Success).user.name shouldBe "Alice Updated"
    }
}
```

### iOS ViewModel Testing

```swift
@MainActor
final class UserViewModelTests: XCTestCase {

    var repository: MockUserRepository!
    var viewModel: UserViewModel!
    var cancellables = Set<AnyCancellable>()

    override func setUp() {
        repository = MockUserRepository()
        viewModel = UserViewModel(repository: repository)
    }

    func test_initialStateIsIdle() {
        XCTAssertTrue(viewModel.viewState is UserViewState.Idle)
    }

    func test_loadUser_emitsLoadingThenSuccess() async {
        // Given
        let user = User(id: "1", name: "Alice", email: "alice@example.com")
        repository.mockedFetchUserResult = .success(user)

        // Collect states
        let expectation = XCTestExpectation(description: "States emitted")
        expectation.expectedFulfillmentCount = 2

        var states: [UserViewState] = []
        viewModel.$viewState.sink { state in
            states.append(state)
            expectation.fulfill()
        }.store(in: &cancellables)

        // When
        viewModel.loadUser("1")

        // Then
        await fulfillment(of: [expectation], timeout: 1.0)

        XCTAssertTrue(states[0] is UserViewState.Loading)
        if case .success(let loadedUser) = states[1] {
            XCTAssertEqual(loadedUser.name, "Alice")
        }
    }

    func test_loadUser_deduplicatesConcurrentCalls() async {
        // Given
        repository.mockedFetchUserResult = .success(
            User(id: "1", name: "Alice", email: "alice@example.com")
        )

        // When — fire 3 concurrent loads
        async let result1 = viewModel.loadUser("1")
        async let result2 = viewModel.loadUser("1")
        async let result3 = viewModel.loadUser("1")

        _ = await (result1, result2, result3)

        // Then — only 1 API call should be made
        XCTAssertEqual(repository.fetchUserCallCount, 1)
    }
}
```

---

## Repository Testing

Repository tests verify that the data layer correctly coordinates between data sources (API, database, cache).

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class UserRepositoryTest {

    @get:Rule
    val mainDispatcherRule = StandardTestDispatcherRule()

    private val apiService = mockk<ApiService>()
    private val database = mockk<AppDatabase>()
    private val userDao = mockk<UserDao>()
    private lateinit var repository: UserRepository

    @BeforeEach
    fun setUp() {
        every { database.userDao() } returns userDao
        repository = UserRepository(apiService, database)
    }

    @Test
    fun `fetchUser returns cached user when available`() = runTest {
        // Given
        val cachedUser = User("1", "Alice (cached)")
        coEvery { userDao.getUserById("1") } returns cachedUser

        // When
        val result = repository.fetchUser("1")

        // Then
        (result as Result.Success).data.name shouldBe "Alice (cached)"
        coVerify(exactly = 0) { apiService.getUser(any()) } // No API call for cached data
    }

    @Test
    fun `fetchUser calls API when no cache and updates database`() = runTest {
        // Given
        coEvery { userDao.getUserById("1") } returns null
        val apiUser = UserResponse("1", "Alice (API)", "alice@example.com")
        coEvery { apiService.getUser("1") } returns apiUser
        coEvery { userDao.insertUser(any()) } returns Unit

        // When
        val result = repository.fetchUser("1")

        // Then
        (result as Result.Success).data.name shouldBe "Alice (API)"
        coVerify { apiService.getUser("1") }
        coVerify { userDao.insertUser(match { it.id == "1" }) }
    }

    @Test
    fun `fetchUser returns error when API fails and no cache`() = runTest {
        // Given
        coEvery { userDao.getUserById("1") } returns null
        coEvery { apiService.getUser("1") } throws
            java.net.SocketTimeoutException("Timeout")

        // When
        val result = repository.fetchUser("1")

        // Then
        result.shouldBeInstanceOf<Result.Error>()
    }
}
```

---

## Test Doubles

### Types of Test Doubles

| Type      | Purpose                             | When to Use                                                   |
| --------- | ----------------------------------- | ------------------------------------------------------------- |
| **Stub**  | Returns canned responses            | When you need to control input to the SUT                     |
| **Mock**  | Records and verifies interactions   | When you need to verify the SUT called dependencies correctly |
| **Fake**  | Working implementation (simplified) | When you need real behavior without external systems          |
| **Spy**   | Wraps real object, records calls    | When you need partial mocking                                 |
| **Dummy** | Placeholder, never used             | When API requires a parameter you don't care about            |

### Test Double Implementation

```kotlin
// Stub — Returns canned data
class StubUserService : UserService {
    override suspend fun getUser(id: String): User = User(id, "Stub User")
    override suspend fun login(email: String, password: String): AuthToken = "stub-token"
}

// Mock — Records calls and returns configurable responses (MockK)
val mockUserService = mockk<UserService> {
    coEvery { getUser("1") } returns User("1", "Mock User")
    coEvery { login(any(), any()) } returns "mock-token"
}

// Fake — Simplified working implementation
class FakeUserService : UserService {
    private val users = mutableMapOf<String, User>()
    var loginAttempts = 0

    override suspend fun getUser(id: String): User {
        return users[id] ?: throw UserNotFoundException(id)
    }

    override suspend fun login(email: String, password: String): AuthToken {
        loginAttempts++
        if (password == "correct-password") return "valid-token"
        throw AuthenticationException("Invalid credentials")
    }

    fun addUser(user: User) { users[user.id] = user }
}
```

---

## Code Coverage

### Android — JaCoCo

```kotlin
// app/build.gradle.kts
plugins {
    id("jacoco")
}

jacoco {
    toolVersion = "0.8.11"
}

tasks.register<JacocoReport>("jacocoTestReport") {
    dependsOn("testDebugUnitTest")

    reports {
        xml.required.set(true)
        html.required.set(true)
        csv.required.set(false)
    }

    val fileFilter = listOf(
        "**/R.class",
        "**/R$*.class",
        "**/BuildConfig.*",
        "**/Manifest*.*",
        "**/*Test*.*",
        "**/databinding/**",
        "**/hilt/**",
        "**/*_Factory.*",
        "**/*_MembersInjector.*"
    )

    val debugTree = fileTree("${buildDir}/tmp/kotlin-classes/debug") {
        exclude(fileFilter)
    }

    val mainSrc = fileTree("src/main/java") {
        exclude(fileFilter)
    }

    sourceDirectories.setFrom(files(mainSrc))
    classDirectories.setFrom(files(debugTree))
    executionData.setFrom(fileTree(buildDir) {
        include("outputs/unit_test_code_coverage/debugUnitTest/*.exec")
    })
}
```

**Coverage Threshold Enforcement:**

```kotlin
tasks.register<JacocoCoverageVerification>("jacocoTestCoverageVerification") {
    dependsOn("testDebugUnitTest")

    violationRules {
        rule {
            limit {
                minimum = "0.80".toBigDecimal() // 80% branch coverage
            }
        }
        limit {
            minimum = "0.90".toBigDecimal() // 90% line coverage
        }
    }
}
```

### iOS — Xcode Coverage

Xcode provides built-in coverage reporting:

```bash
# Run tests with coverage
xcodebuild test \
    -workspace App.xcworkspace \
    -scheme App \
    -destination 'platform=iOS Simulator,name=iPhone 15' \
    -enableCodeCoverage YES

# Generate coverage report with Slather
slather coverage \
    --input-format profdata \
    --cobertura-xml \
    --output-directory coverage \
    --scheme App \
    App.xcworkspace
```

**Coverage Threshold in CI:**

```bash
# Parse coverage and fail if below threshold
coverage=$(slather coverage --simple-output --scheme App App.xcworkspace)
percentage=$(echo "$coverage" | grep -o '[0-9.]*%' | head -1 | tr -d '%')
if (( $(echo "$percentage < 80" | bc -l) )); then
    echo "Coverage $percentage% is below 80% threshold"
    exit 1
fi
```

---

## CI/CD Integration

### Unit Test Pipeline

```
Developer pushes code
    │
    ▼
┌──────────────────────────────────────┐
│ PRE-COMMIT HOOK                      │
│ ├── ktlint / SwiftLint               │
│ └── Quick unit test suite (< 30s)    │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│ PULL REQUEST CI                      │
│ ├── Full unit test suite             │
│ ├── JaCoCo / Xcode coverage report   │
│ ├── Lint + static analysis           │
│ └── Coverage threshold check         │
│                                      │
│ If any step fails → PR blocked       │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│ MERGE TO MAIN                        │
│ ├── Full test suite (re-run)         │
│ ├── Coverage trend analysis          │
│ └── Coverage badge update            │
└──────────────────────────────────────┘
```

### GitHub Actions — Android Unit Tests

```yaml
name: Android Unit Tests

on: [pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'

      - name: Grant execute permission
        run: chmod +x gradlew

      - name: Run unit tests
        run: ./gradlew testDebugUnitTest

      - name: Generate JaCoCo report
        run: ./gradlew jacocoTestReport

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: '**/build/reports/jacoco/'

      - name: Check coverage threshold
        run: ./gradlew jacocoTestCoverageVerification
```

### GitHub Actions — iOS Unit Tests

```yaml
name: iOS Unit Tests

on: [pull_request]

jobs:
  unit-tests:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4

      - name: Run unit tests with coverage
        run: |
          xcodebuild test \
            -workspace App.xcworkspace \
            -scheme App \
            -destination 'platform=iOS Simulator,name=iPhone 15' \
            -enableCodeCoverage YES

      - name: Generate coverage report
        run: |
          slather coverage \
            --input-format profdata \
            --cobertura-xml \
            --output-directory coverage \
            --scheme App \
            App.xcworkspace

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: ios-coverage
          path: coverage/
```

---

## Stage 7 Integration

### Stage 7 in the 10-Stage Pipeline

Stage 7 (Automated Testing) validates that the codebase meets quality standards through comprehensive automated testing.

**Input from Stage 6:**

- Code-signed codebase with all P0/P1 defects from code review remediated
- Defect Report with user decisions on P2/P3 defects
- Code Review Sign-off

**What Stage 7 Adds:**

- Comprehensive test suite (unit, integration, E2E)
- Code coverage measurement
- Performance benchmarking
- Accessibility audit
- Test Results Report

**Output to Stage 8:**

- Test Suite
- Test Results Report (pass/fail rates, coverage metrics, benchmarks)
- Updated Defect Report (new defects found during testing)

### Unit Testing's Role in Stage 7

| Activity                      | Responsibility | Tool                             |
| ----------------------------- | -------------- | -------------------------------- |
| Unit test suite execution     | Platform Leads | Gradle test / xcodebuild test    |
| Coverage report generation    | Platform Leads | JaCoCo / Slather                 |
| Coverage threshold validation | CTO            | CI pipeline gate                 |
| Integration test execution    | Test Lead      | Gradle connectedAndroidTest      |
| E2E smoke test execution      | Test Lead      | Maestro / Appium                 |
| Accessibility audit           | Test Lead      | Accessibility Scanner / XCUITest |
| Performance benchmarking      | Platform Leads | Macrobenchmark / XCTMeasure      |

### Unit Test Quality Gate

```
┌─────────────────────────────────────────────────────────────────┐
│ UNIT TEST QUALITY GATE (Stage 7)                                │
│                                                                 │
│ Criterion                    │ Target        │ Verification     │
│ ────────────────────────────│───────────────│────────────────── │
│ Unit test pass rate          │ 100%          │ CI test results  │
│ Branch coverage              │ >= 80%        │ JaCoCo / Slather │
│ Line coverage                │ >= 90%        │ JaCoCo / Slather │
│ No flaky tests               │ 0 confirmed   │ CI retry analysis│
│ Critical path coverage       │ 100%          │ Manual audit     │
│ Test execution time          │ < 5 minutes   │ CI timing        │
│ Test isolation               │ No order dep. │ Shuffle test run │
└─────────────────────────────────────────────────────────────────┘

If any criterion fails:
  1. Platform Lead investigates and fixes
  2. Re-run tests
  3. Re-gate only the failed criterion
```

---

## References

### Official Documentation

- [Android Testing Documentation](https://developer.android.com/training/testing)
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [MockK Documentation](https://mockk.io/)
- [Robolectric Documentation](https://robolectric.org/)
- [kotlinx-coroutines-test](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/)
- [Turbine (Flow Testing)](https://github.com/cashapp/turbine)
- [XCTest Documentation](https://developer.apple.com/documentation/xctest)
- [Swift Testing Documentation](https://developer.apple.com/documentation/testing)
- [Flutter Testing Cookbook](https://docs.flutter.dev/cookbook/testing)

### Libraries and Tools

| Category           | Android                          | iOS                        | Cross-Platform               |
| ------------------ | -------------------------------- | -------------------------- | ---------------------------- |
| Framework          | JUnit 5                          | XCTest, Swift Testing      | JUnit 5 (KMP), flutter_test  |
| Assertions         | Truth, Kotest                    | XCTestAssertions, #expect  | Truth, expect                |
| Mocking            | MockK                            | Manual (protocols), Cuckoo | Manual, MockK (KMP)          |
| Coroutines/Async   | kotlinx-coroutines-test, Turbine | XCTest async/await         | kotlinx-coroutines-test      |
| Android Simulation | Robolectric                      | N/A                        | N/A                          |
| Coverage           | JaCoCo                           | Xcode Coverage, Slather    | JaCoCo (KMP), lcov (Flutter) |
| Test Data          | Kotlin Faker                     | Manual factories           | Faker libraries              |

### Company Standards

- Stage 7 Pipeline Specification — `.opencode/pipeline/mobile-development/pipeline.md`
- Defect Severity System — P0/P1/P2/P3 classification
- Code Coverage Standards — 80% branch / 90% line coverage minimum
- OWASP MASVS — Security testing requirements
- WCAG 2.1 AA — Accessibility compliance targets

### Further Reading

- "Test-Driven Development by Example" — Kent Beck
- "Unit Testing Principles, Practices, and Patterns" — Vladimir Khorikov
- "Effective Testing with XCTest" — iOS-specific deep dive
- "Kotlin Coroutines: Testing" — Official Kotlin documentation
- "Clean Architecture" — Robert C. Martin (repository and use case patterns)
