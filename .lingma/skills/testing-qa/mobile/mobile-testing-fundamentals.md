---
name: mobile-testing-fundamentals
description: This skill provides foundational knowledge for mobile testing across all platforms in the company's pipeline. It establishes the principles, strategies.
---

# Mobile Testing Fundamentals

## Overview

This skill provides foundational knowledge for mobile testing across all platforms in the company's pipeline. It establishes the principles, strategies, and practices that underpin comprehensive mobile quality assurance, serving as the basis for more specialized testing skills (unit testing, integration testing, E2E testing, etc.).

Mobile application testing is inherently more complex than web testing due to:

- **Platform fragmentation** — multiple OS versions, device form factors, screen densities
- **Network variability** — cellular, Wi-Fi, offline transitions, flaky connectivity
- **Hardware diversity** — cameras, GPS, biometrics, sensors, NFC, Bluetooth
- **App lifecycle management** — backgrounding, foregrounding, process death, memory pressure
- **App store constraints** — review processes, binary size limits, privacy manifests

### The Mobile Test Pyramid

```
                    ┌─────────────┐
                    │   Manual    │        ← Exploratory, usability, ad-hoc
                    │  Testing    │
                ┌───┴─────────────┴───┐
                │    E2E / UI Tests   │    ← Few (slow, brittle, expensive)
            ┌───┴─────────────────────┴───┐
            │    Integration Tests        │  ← Some (network, DB, platform APIs)
        ┌───┴─────────────────────────────┴───┐
        │         Unit Tests                  │  ← Many (fast, cheap, reliable)
        └─────────────────────────────────────┘
```

| Layer             | Scope                 | Execution Speed | Maintenance Cost | Recommended % |
| ----------------- | --------------------- | --------------- | ---------------- | ------------- |
| Unit Tests        | Single class/function | Milliseconds    | Low              | 60–70%        |
| Integration Tests | Module interactions   | Seconds         | Medium           | 20–30%        |
| E2E / UI Tests    | Full user flows       | Minutes         | High             | 5–10%         |
| Manual Testing    | Exploratory, UX       | Variable        | Very High        | 1–5%          |

**Principle:** Push tests as far down the pyramid as possible. A unit test that validates business logic is preferable to an E2E test that does the same — faster execution, clearer failure signals, lower flakiness.

---

## Test Types

### 1. Unit Tests

Unit tests verify individual functions, methods, or classes in isolation. They are the foundation of the test pyramid.

**Characteristics:**

- Execute in milliseconds
- No external dependencies (databases, networks, file systems)
- Deterministic — same inputs always produce same outputs
- Run on developer machines without special setup

**What to test:**

- Business logic and calculations
- Data transformations and mappings
- Validation rules
- State machine transitions
- Error handling paths

**What NOT to unit test:**

- Framework code (Google/Apple already test their frameworks)
- Simple getters/setters
- Third-party library behavior
- UI rendering (use dedicated UI testing tools)

### 2. Integration Tests

Integration tests verify that multiple components work together correctly.

**Characteristics:**

- May use test doubles for some dependencies
- Test real interactions between modules
- Slower than unit tests but faster than UI tests
- May require test infrastructure (test database, mock server)

**What to test:**

- Repository ↔ Data source interactions
- ViewModel ↔ Repository data flows
- Network client ↔ API endpoint communication
- Database ↔ DAO/Repository layer
- Platform API integrations (location, camera, notifications)

**Example — Android Repository Integration Test:**

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
@RunWith(AndroidJUnit4::class)
class UserRepositoryIntegrationTest {

    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    private lateinit var db: AppDatabase
    private lateinit var userDao: UserDao
    private lateinit var repository: UserRepository
    private lateinit var apiService: FakeUserService

    @Before
    fun setup() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        db = Room.inMemoryDatabaseBuilder(context, AppDatabase::class.java)
            .allowMainThreadQueries()
            .build()
        userDao = db.userDao()
        apiService = FakeUserService()
        repository = UserRepository(userDao, apiService)
    }

    @After
    fun teardown() {
        db.close()
    }

    @Test
    fun `fetchUser syncs from API and returns cached result`() = runTest {
        // Given: API returns a user
        apiService.enqueueUser(UserResponse(id = "1", name = "Alice"))

        // When: Repository fetches user
        val result = repository.fetchUser("1")

        // Then: Result matches API response
        assertThat(result.id).isEqualTo("1")
        assertThat(result.name).isEqualTo("Alice")

        // And: User was cached in database
        val cached = userDao.getUserById("1")
        assertThat(cached).isNotNull()
        assertThat(cached!!.name).isEqualTo("Alice")
    }
}
```

### 3. UI Tests

UI tests verify user interface behavior — that tapping a button performs the expected action and shows the expected result.

**Characteristics:**

- Run on real devices or emulators
- Interact with actual UI components
- Sensitive to timing, animations, and rendering
- Highest maintenance cost in the pyramid

**Platform Tools:**
| Platform | Framework | Language | Execution |
|----------|-----------|----------|-----------|
| Android | Espresso | Kotlin/Java | On-device |
| iOS | XCUITest | Swift | On-device |
| Cross-platform | Maestro | YAML | On-device |
| Cross-platform | Appium | Multi-language | On-device |
| Flutter | Flutter Driver / integration_test | Dart | On-device |
| Compose | Compose Testing | Kotlin | On-device |

### 4. End-to-End (E2E) Tests

E2E tests validate complete user journeys through the application, from UI to backend and back.

**Characteristics:**

- Test real user workflows
- May involve multiple systems (app, backend API, database)
- Slowest and most expensive
- Best reserved for critical path validation only

**Critical paths to cover:**

- User registration and authentication
- Core feature workflow (app's primary value proposition)
- Payment/checkout flow (if applicable)
- Data synchronization
- Offline-to-online transition

**Example — Maestro E2E Test (YAML):**

```yaml
# flows/login-and-sync.yaml
appId: com.company.app
---
- launchApp
- assertVisible: 'Welcome'
- tapOn: 'Sign In'
- tapOn:
    id: 'email_field'
- inputText: 'test@example.com'
- tapOn:
    id: 'password_field'
- inputText: 'SecurePass123!'
- tapOn: 'Login'
- assertVisible: 'Dashboard'
- assertVisible:
    text: 'Hello, Test User'
- tapOn: 'Sync'
- assertVisible: 'Last synced: Just now'
- assertVisible: 'All data up to date'
```

### 5. Accessibility Testing

Accessibility testing ensures the app is usable by people with diverse abilities — visual, auditory, motor, cognitive.

**Compliance Standard:** WCAG 2.1 AA (company standard per LINGMA.md)

**Key Areas:**

| Category            | Check                                     | Platform Tool                                        |
| ------------------- | ----------------------------------------- | ---------------------------------------------------- |
| Content Description | All interactive elements have labels      | Accessibility Scanner, Xcode Accessibility Inspector |
| Color Contrast      | Minimum 4.5:1 for normal text             | Contrast analyzers, Lighthouse                       |
| Touch Target Size   | Minimum 44x44pt (iOS) / 48x48dp (Android) | Layout Inspector, Reveal                             |
| Dynamic Type        | Text scales with system font size         | Developer settings → Font size                       |
| VoiceOver/TalkBack  | Screen reader navigates logically         | VoiceOver, TalkBack                                  |
| Focus Order         | Logical tab/focus order                   | Keyboard navigation testing                          |
| Reduced Motion      | Animations respect system setting         | Developer settings → Reduce motion                   |

**Android — Espresso Accessibility Check:**

```kotlin
@Test
fun `login screen meets accessibility standards`() {
    // Navigate to login screen
    onView(withId(R.id.nav_login)).perform(click())

    // Run accessibility checks using Accessibility Test Framework
    val result = AccessibilityChecks.validate()
    // Suppress known, acceptable issues
    result.suppressionResult.suppressedResults.forEach {
        // Log but don't fail on minor issues
        Log.d("A11y", "Suppressed: ${it.viewHierarchyEntry}")
    }
    // Assert no unsuppressed issues remain
    assertThat(result.suppressionResult.unsuppressedResults).isEmpty()
}
```

**iOS — XCTest Accessibility:**

```swift
func testLoginScreenAccessibility() throws {
    let app = XCUIApplication()
    app.launch()

    let emailField = app.textFields["Email"]
    XCTAssertTrue(emailField.exists, "Email field must exist")
    XCTAssertEqual(
        emailField.label,
        "Email Address",
        "Email field must have descriptive label for VoiceOver"
    )
    XCTAssertEqual(
        emailField.accessibilityTraits,
        .staticText,
        "Email field should be identified as text input"
    )

    let loginButton = app.buttons["Login"]
    XCTAssertTrue(loginButton.isAccessibilityElement, "Login button must be accessibility element")
    XCTAssertEqual(
        loginButton.accessibilityLabel,
        "Sign in to your account",
        "Login button must have descriptive label"
    )
}
```

### 6. Performance Testing

Performance testing ensures the app meets responsiveness and resource usage targets.

**Key Metrics:**

| Metric                 | Target               | Measurement                                  |
| ---------------------- | -------------------- | -------------------------------------------- |
| App Launch Time (cold) | < 2 seconds          | Android Baseline Profiles, Xcode Instruments |
| Time to Interactive    | < 3 seconds          | Custom instrumentation                       |
| Frame Rate             | 60 fps (jank-free)   | Systrace, Xcode Core Animation               |
| Memory Usage           | < 200 MB typical     | Android Profiler, Xcode Memory Graph         |
| Network Payload        | < 1 MB per request   | Network profiler, Charles Proxy              |
| Battery Impact         | < 2% per hour active | Battery Historian, Xcode Energy Log          |
| APK/IPA Size           | < 50 MB download     | APK Analyzer, Xcode Report Navigator         |

**Android — Macrobenchmark for Startup:**

```kotlin
@RunWith(AndroidJUnit4::class)
class AppStartupBenchmark {
    @get:Rule
    val benchmarkRule = MacrobenchmarkRule()

    @Test
    fun startup() = benchmarkRule.measureRepeated(
        packageName = "com.company.app",
        metrics = listOf(StartupTimingMetric()),
        iterations = 5,
        startupMode = StartupMode.COLD,
        setupBlock = {
            pressHome()
            startActivityAndWait()
        }
    ) {
        // Measure time from tap to fully drawn UI
        val startupTiming = metrics[StartupTimingMetric::class.java]
        assertThat(startupTiming).isNotNull()
        assertThat(startupTiming.durationNs)
            .isLessThan(TimeUnit.SECONDS.toNanos(2))
    }
}
```

**iOS — XCTMeasure for Performance:**

```swift
func testTableViewScrollPerformance() {
    let app = XCUIApplication()
    app.launch()

    let tableView = app.tables["MainList"]
    let measureOptions = XCTMeasureOptions.default
    measureOptions.iterationCount = 5

    measure(metrics: [XCTOSSignpostMetric.scrollDecelerationMetric],
            options: measureOptions) {
        tableView.swipeUp(velocity: .fast)
        tableView.swipeDown(velocity: .fast)
    }
}
```

### 7. Security Testing

Security testing identifies vulnerabilities that could expose user data or compromise the app.

**Compliance Standard:** OWASP MASVS (company standard per LINGMA.md)

**Key Areas:**

| MASVS Category   | Focus                 | Testing Approach                                                           |
| ---------------- | --------------------- | -------------------------------------------------------------------------- |
| MASVS-STORAGE    | Data at rest          | Verify encryption, check SharedPreferences/UserDefaults for sensitive data |
| MASVS-CRYPTO     | Cryptography          | Validate key management, algorithm strength                                |
| MASVS-AUTH       | Authentication        | Test brute force protection, session management                            |
| MASVS-NETWORK    | Network communication | Verify TLS, certificate pinning                                            |
| MASVS-PLATFORM   | Platform interaction  | Verify deep link validation, intent filtering                              |
| MASVS-RESILIENCE | Anti-tampering        | Verify root/jailbreak detection, obfuscation                               |

---

## Device Coverage Strategy

### Real Devices vs. Emulators/Simulators

| Dimension         | Emulators/Simulators              | Real Devices               |
| ----------------- | --------------------------------- | -------------------------- |
| Speed             | Fast spin-up                      | Physical handling required |
| Cost              | Free                              | Purchase/rent device farm  |
| Accuracy          | Good for logic, poor for hardware | Exact user experience      |
| Sensor Testing    | Simulated (often inaccurate)      | Real sensors               |
| Network Testing   | Throttle simulation               | Real cellular/Wi-Fi        |
| Battery Testing   | Not possible                      | Accurate drain measurement |
| Memory Pressure   | Simulated                         | Real OS behavior           |
| Biometric Testing | Limited support                   | Real fingerprint/Face ID   |

**Strategy:**

```
Development Phase (Local):
  ├── Android Emulator (API 28–35, various form factors)
  └── iOS Simulator (iPhone SE, iPhone 15, iPad)

CI/CD Phase (Automated):
  ├── Emulator/Simulator for unit + integration tests
  └── Device farm for critical E2E smoke tests

Release Phase (Validation):
  ├── Physical device lab for regression suite
  ├── Beta testers for real-world validation
  └── Dogfooding (team uses app daily)
```

### Device Farm Options

| Service                 | Platforms    | Pricing               | Integration             |
| ----------------------- | ------------ | --------------------- | ----------------------- |
| Firebase Test Lab       | Android, iOS | Pay-per-minute        | Gradle plugin, Fastlane |
| AWS Device Farm         | Android, iOS | Pay-per-device-minute | CLI, Fastlane           |
| BrowserStack App Live   | Android, iOS | Subscription          | REST API, Fastlane      |
| Sauce Labs              | Android, iOS | Subscription          | REST API, Fastlane      |
| Bitrise Virtual Devices | Android, iOS | Included in tier      | Native in Bitrise CI    |

### OS Version Matrix

**Android Matrix (per Play Store distribution):**

| Android Version | API Level | Coverage Target                 |
| --------------- | --------- | ------------------------------- |
| Android 10      | 29        | Minimum supported               |
| Android 11      | 30        | Test on emulators               |
| Android 12      | 31        | Test on emulators + device farm |
| Android 13      | 33        | Test on emulators + device farm |
| Android 14      | 34        | Primary test target             |
| Android 15      | 35        | Early testing (beta/stable)     |

**iOS Matrix (per Apple guidelines):**

| iOS Version | Minimum Devices | Coverage Target                 |
| ----------- | --------------- | ------------------------------- |
| iOS 16      | iPhone 8 Plus   | Minimum supported               |
| iOS 17      | iPhone 12+      | Test on simulator + device farm |
| iOS 18      | iPhone 15+      | Primary test target             |

**Rule:** Support current OS + 2 previous versions minimum. Test on minimum supported version + latest version + one intermediate.

---

## Test Data Management

### Principles

| Principle          | Description                                    |
| ------------------ | ---------------------------------------------- |
| **Deterministic**  | Same test data produces same results every run |
| **Isolated**       | Tests don't share or mutate shared state       |
| **Self-contained** | Tests create and clean up their own data       |
| **Representative** | Test data reflects production scenarios        |

### Strategies

**1. Factory Methods (Recommended for Unit Tests):**

```kotlin
// Kotlin — Test Data Factory
object UserTestDataFactory {
    fun validUser(
        id: String = "user-123",
        name: String = "Alice Johnson",
        email: String = "alice@example.com"
    ): User = User(id = id, name = name, email = email)

    fun userWithLongName() = validUser(
        name = "Christopher Alexander Montgomery-Smythe III",
        email = "long.name@example.com"
    )

    fun userWithSpecialCharacters() = validUser(
        name = "José García-O'Brien",
        email = "jose@example.com"
    )

    fun minimalUser() = validUser(
        name = "A",
        email = "a@b.co"
    )
}
```

```swift
// Swift — Test Data Factory
enum UserTestDataFactory {
    static func validUser(
        id: String = "user-123",
        name: String = "Alice Johnson",
        email: String = "alice@example.com"
    ) -> User {
        User(id: id, name: name, email: email)
    }

    static func userWithLongName() -> User {
        validUser(name: "Christopher Alexander Montgomery-Smythe III")
    }

    static func userWithSpecialCharacters() -> User {
        validUser(name: "José García-O'Brien")
    }

    static func minimalUser() -> User {
        validUser(name: "A", email: "a@b.co")
    }
}
```

**2. Fixture Files (Recommended for Integration/E2E):**

```json
// tests/fixtures/user-response.json
{
  "id": "user-123",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "avatar_url": "https://example.com/avatar.jpg",
  "created_at": "2024-01-15T10:30:00Z"
}
```

```kotlin
// Loading fixtures in Kotlin tests
inline fun <reified T> loadFixture(fileName: String): T {
    val json = javaClass.classLoader!!
        .getResource("fixtures/$fileName")!!
        .readText()
    return Json.decodeFromString(json)
}

@Test
fun `parse user response from API`() {
    val response: UserResponse = loadFixture("user-response.json")
    val user = response.toDomainModel()
    assertThat(user.name).isEqualTo("Alice Johnson")
}
```

**3. Mock Servers (Recommended for API Integration):**

```kotlin
// Kotlin — MockWebServer for API testing
@OptIn(ExperimentalCoroutinesApi::class)
class ApiServiceTest {
    private val mockServer = MockWebServer()
    private lateinit var apiService: ApiService

    @BeforeEach
    fun setup() {
        apiService = Retrofit.Builder()
            .baseUrl(mockServer.url("/"))
            .addConverterFactory(MoshiConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }

    @AfterEach
    fun teardown() {
        mockServer.shutdown()
    }

    @Test
    fun `fetchUser returns parsed user`() = runTest {
        val jsonResponse = loadJsonResource("user-response.json")
        mockServer.enqueue(
            MockResponse()
                .setResponseCode(200)
                .setBody(jsonResponse)
        )

        val user = apiService.fetchUser("user-123")

        assertThat(user.name).isEqualTo("Alice Johnson")
        val request = mockServer.takeRequest()
        assertThat(request.path).isEqualTo("/api/users/user-123")
    }
}
```

### Sensitive Data Handling

**NEVER commit production data or credentials to test fixtures.**

| Rule                                             | Enforcement               |
| ------------------------------------------------ | ------------------------- |
| No real passwords, tokens, API keys in test code | Pre-commit hooks, CI lint |
| No production database dumps in fixtures         | Repository policy         |
| Use synthetic data generators for large datasets | Faker libraries           |
| Mask PII in test logs                            | Log sanitization          |

```kotlin
// Use Faker for synthetic test data
val faker = Faker()
val testUser = User(
    name = faker.name().fullName(),
    email = faker.internet().emailAddress(),
    phone = faker.phoneNumber().cellPhone()
)
```

---

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

## Cross-Platform Testing

### Framework Comparison

| Framework            | Platform            | Best For                                 | Limitations                            |
| -------------------- | ------------------- | ---------------------------------------- | -------------------------------------- |
| **Espresso**         | Android             | Native UI testing, fast on-device        | Android only, requires Kotlin/Java     |
| **XCUITest**         | iOS                 | Native UI testing, integrated with Xcode | iOS only, requires Swift/Obj-C         |
| **Compose Testing**  | Android             | Compose UI testing                       | Compose only, Android only             |
| **Swift UI Testing** | iOS                 | SwiftUI preview testing                  | SwiftUI only, iOS 16+                  |
| **Maestro**          | Android + iOS       | Cross-platform E2E, YAML-based           | Limited logic in YAML, no unit testing |
| **Appium**           | Android + iOS + Web | Cross-platform, multi-language           | Slower, more setup, flakier            |
| **Detox**            | React Native        | RN E2E testing                           | RN only, complex setup                 |
| **integration_test** | Flutter             | Flutter E2E testing                      | Flutter only                           |
| **flutter_test**     | Flutter             | Flutter widget/unit testing              | Flutter only                           |

### Choosing the Right Tool

```
Test Need                          → Recommended Tool
─────────────────────────────────────────────────────
Android unit test                  → JUnit 5 + Mockito + Robolectric
Android Compose UI test            → Compose Testing
Android View system UI test        → Espresso
iOS unit test                      → XCTest + Swift Testing
iOS SwiftUI test                   → XCUITest
Cross-platform E2E flow            → Maestro (preferred) or Appium
KMP shared module test             → JUnit 5 (runs on JVM)
Flutter widget test                → flutter_test
Flutter integration test           → integration_test
Accessibility audit                → Espresso A11y + XCUITest A11y
Performance benchmark              → Macrobenchmark (Android) / XCTMeasure (iOS)
```

### Cross-Platform E2E with Maestro

Maestro is the recommended cross-platform E2E testing tool because:

- Single YAML file defines tests for both Android and iOS
- Fast execution (no WebDriver overhead like Appium)
- Built-in error handling and retries
- Easy CI/CD integration
- Hot reload during development

```yaml
# flows/complete-purchase.yaml
appId: com.company.app
name: Complete Purchase Flow
tags:
  - smoke
  - purchase
---
- launchApp
- runFlow: login.yaml
- tapOn: 'Products'
- tapOn:
    id: 'product_card_1'
- tapOn: 'Add to Cart'
- assertVisible:
    id: 'cart_badge'
    text: '1'
- tapOn:
    id: 'cart_button'
- assertVisible: 'Cart'
- assertVisible:
    id: 'item_name'
    text: 'Test Product'
- tapOn: 'Checkout'
- tapOn: 'Confirm Purchase'
- assertVisible: 'Purchase Successful'
- assertVisible:
    text: 'Order confirmed'
- tapOn: 'Back to Home'
- assertVisible: 'Dashboard'
```

**Running Maestro Tests:**

```bash
# Run all tests
maestro test flows/

# Run specific test
maestro test flows/complete-purchase.yaml

# Run against specific device
maestro test flows/ --device-id "Pixel 7"

# Generate test from recording
maestro record flows/
```

---

## CI/CD Integration

### Pipeline Integration

Tests must integrate at multiple points in the CI/CD pipeline:

```
Developer commits code
    │
    ▼
┌──────────────────────────────────────┐
│ PRE-COMMIT (local)                   │
│ ├── Lint (ktlint, SwiftLint)         │
│ ├── Unit tests (fast subset)         │
│ └── Type checking                    │
│ Duration: < 30 seconds               │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│ CI — PULL REQUEST                    │
│ ├── Full unit test suite             │
│ ├── Integration tests                │
│ ├── Lint + static analysis           │
│ ├── Build verification               │
│ └── Code coverage report             │
│ Duration: < 10 minutes               │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│ CI — MERGE TO MAIN                   │
│ ├── Full test suite                  │
│ ├── UI tests (emulator/simulator)    │
│ ├── E2E smoke tests (device farm)    │
│ ├── Performance baseline check       │
│ └── Accessibility audit              │
│ Duration: < 30 minutes               │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│ RELEASE CANDIDATE                    │
│ ├── Full regression suite            │
│ ├── Device farm validation           │
│ ├── Performance benchmarking         │
│ ├── Security scan                    │
│ └── Beta distribution                │
│ Duration: < 2 hours                  │
└──────────────────────────────────────┘
```

### GitHub Actions Example

```yaml
# .github/workflows/mobile-tests.yml
name: Mobile Tests

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  android-unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
      - name: Run Android unit tests
        run: ./gradlew testDebugUnitTest
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: android-test-results
          path: '**/build/test-results/test*/'
      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: android-coverage
          path: '**/build/reports/jacoco/'

  ios-unit-tests:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Run iOS unit tests
        run: |
          xcodebuild test \
            -workspace App.xcworkspace \
            -scheme App \
            -destination 'platform=iOS Simulator,name=iPhone 15,OS=latest' \
            -resultBundlePath TestResults

  maestro-e2e:
    runs-on: ubuntu-latest
    needs: [android-unit-tests, ios-unit-tests]
    steps:
      - uses: actions/checkout@v4
      - name: Build APK
        run: ./gradlew assembleDebug
      - name: Run Maestro tests
        uses: mobile-dev-inc/action-maestro-cloud@v1
        with:
          api-key: ${{ secrets.MAESTRO_API_KEY }}
          app-file: app/build/outputs/apk/debug/app-debug.apk
          project-id: ${{ secrets.MAESTRO_PROJECT_ID }}
```

### Fastlane Integration

```ruby
# fastlane/Fastfile
default_platform(:android)

platform :android do
  lane :test do
    gradle(task: "testDebugUnitTest")
    jacoco(
      execution_data: "app/build/outputs/unit_test_code_coverage/debugUnitTest/testDebugUnitTest.exec"
    )
  end

  lane :ui_test do
    gradle(task: "connectedDebugAndroidTest")
  end

  lane :full_test do
    test
    ui_test
    maestro(
      flow_path: "maestro/flows/"
    )
  end
end

platform :ios do
  lane :test do
    scan(
      scheme: "App",
      devices: ["iPhone 15"],
      output_directory: "fastlane/test_output",
      output_types: "html,junit"
    )
  end
end
```

---

## Defect Reporting

### Defect Severity Classification

All defects must be classified using the P0–P3 system per company pipeline rules:

| Level  | Definition                              | Release Impact                  | Example                                      |
| ------ | --------------------------------------- | ------------------------------- | -------------------------------------------- |
| **P0** | App crash / data loss / security breach | Blocks release — non-negotiable | App crashes on launch, user data exposed     |
| **P1** | Core feature broken / major UX failure  | Blocks release — non-negotiable | Login fails, checkout broken                 |
| **P2** | Minor feature degraded / cosmetic issue | User decides to fix or defer    | Wrong icon, minor alignment issue            |
| **P3** | Polish / nice-to-have                   | User decides to fix or defer    | Typo in error message, slight color mismatch |

### Defect Report Structure

```markdown
# Defect Report — [Project Name]

## Defect Summary

| ID    | Title                                | Severity | Status | Assigned To  |
| ----- | ------------------------------------ | -------- | ------ | ------------ |
| D-001 | App crashes on deep link navigation  | P0       | Open   | Android Lead |
| D-002 | Login button misaligned on iPhone SE | P2       | Open   | iOS Lead     |

## Defect Details

### D-001: App crashes on deep link navigation

**Severity:** P0
**Platform:** Android
**Reproduction Rate:** 100%
**Steps to Reproduce:**

1. Install app v2.1.0
2. Open link `myapp://product/123` from external app
3. App crashes immediately

**Expected:** App opens Product detail screen
**Actual:** App crashes with NullPointerException

**Stack Trace:**
```

java.lang.NullPointerException: Product ID is null
at com.company.app.ProductDetailActivity.onCreate(ProductDetailActivity.kt:45)

```

**Device:** Pixel 7, Android 14
**Priority:** Immediate fix required for release
```

---

## Quality Gates

### Gate Criteria for Stage 7 (Automated Testing)

| Criterion                  | Target                     | Verification                   |
| -------------------------- | -------------------------- | ------------------------------ |
| Unit test pass rate        | 100%                       | CI test results                |
| Integration test pass rate | 100%                       | CI test results                |
| E2E smoke test pass rate   | 100%                       | Device farm results            |
| Code coverage (unit tests) | >= 80% branch, >= 90% line | JaCoCo / Xcode coverage report |
| No P0/P1 defects           | Zero open                  | Defect report review           |
| Accessibility compliance   | WCAG 2.1 AA                | A11y audit report              |
| Performance baseline met   | Per ADR targets            | Benchmark results              |
| Security scan passed       | OWASP MASVS                | CSO security audit             |

### Gate Review Process

```
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 7 GATE REVIEW                                             │
│ Panel: CTO, Test Lead, CSO                                      │
│                                                                 │
│ Step 1: Test Lead presents Test Results Report                  │
│ Step 2: CTO reviews coverage metrics                            │
│ Step 3: CSO reviews security test results                       │
│ Step 4: Panel classifies any defects (P0–P3)                    │
│ Step 5: USER reviews defect report, decides on P2/P3            │
│ Step 6: If no P0/P1 and user approves P2/P3 → advance           │
│ Step 7: If P0/P1 found → remediate and re-test                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Stage 7 Integration

### Stage 7 in the 10-Stage Pipeline

Stage 7 (Automated Testing) sits between Stage 6 (Code Review) and Stage 8 (Integrity Verification).

**Input from Stage 6:**

- Code-signed codebase with all P0/P1 defects remediated
- Defect Report with user decisions on P2/P3 defects
- Code Review Sign-off

**Output to Stage 8:**

- Test Suite (unit, integration, E2E, accessibility, performance)
- Test Results Report (pass/fail rates, coverage metrics)
- Updated Defect Report (new defects found during testing)

**Responsible Producers:** CTO (oversees) + Test Lead (executes)

### Stage 7 Workflow

```
Stage 6 Sign-off received
    │
    ▼
┌──────────────────────────────────┐
│ 1. Test Lead reviews codebase    │
│    and identifies test scope     │
└──────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────┐
│ 2. Build/extend test suite       │
│    - Unit tests (platform leads) │
│    - Integration tests           │
│    - E2E smoke tests             │
│    - Accessibility tests         │
│    - Performance tests           │
└──────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────┐
│ 3. Execute full test suite       │
│    - CI pipeline (automated)     │
│    - Device farm (E2E)           │
│    - Manual accessibility audit  │
└──────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────┐
│ 4. Compile Test Results Report   │
│    - Pass/fail rates per suite   │
│    - Coverage metrics            │
│    - Performance benchmarks      │
│    - Defect list (new defects)   │
└──────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────┐
│ 5. Gate Review (CTO, Test Lead,  │
│    CSO + User for P2/P3)         │
└──────────────────────────────────┘
    │
    ├── All pass + no P0/P1 → Advance to Stage 8
    └── P0/P1 found → Remediate → Re-test → Re-gate
```

### Regression Testing Protocol

When defects are fixed during Stage 7:

1. **Fix the defect** in the codebase
2. **Run the failing test** to verify it now passes
3. **Run regression suite** on all related functionality
4. **Update Defect Report** with resolution status
5. **Do NOT re-gate** unless the fix introduces new defects

---

## References

### Official Documentation

- [Android Testing Documentation](https://developer.android.com/training/testing)
- [iOS Testing with XCTest](https://developer.apple.com/documentation/xctest)
- [Swift Testing Framework](https://developer.apple.com/documentation/testing)
- [Flutter Testing](https://docs.flutter.dev/cookbook/testing)
- [Maestro Documentation](https://maestro.mobile.dev/)
- [Appium Documentation](https://appium.io/)

### Frameworks & Libraries

| Category      | Android                           | iOS                                 | Cross-Platform              |
| ------------- | --------------------------------- | ----------------------------------- | --------------------------- |
| Unit Testing  | JUnit 5, Truth, Mockito           | XCTest, Swift Testing, Quick/Nimble | KMP: JUnit 5, Flutter: test |
| UI Testing    | Espresso, Compose Testing         | XCUITest, SwiftUI Testing           | Maestro, Appium             |
| Mocking       | MockK, Mockito                    | Cuckoo, Sourcery                    | Depends on platform         |
| Async Testing | kotlinx-coroutines-test           | XCTest async/await                  | Platform-specific           |
| Coverage      | JaCoCo                            | Xcode Coverage, Slather             | Platform-specific           |
| CI            | GitHub Actions, Bitrise, CircleCI | Xcode Cloud, Bitrise, CircleCI      | GitHub Actions, Bitrise     |

### Company Standards

- OWASP MASVS — Security testing baseline
- WCAG 2.1 AA — Accessibility compliance target
- Company Defect Severity System — P0/P1/P2/P3 classification
- 10-Stage Development Pipeline — Stage 7 specification

### Further Reading

- "Mobile Test Automation with Espresso and XCUITest"
- "Test-Driven Development for Mobile Apps"
- "Continuous Testing in CI/CD Pipelines"
- "Accessibility Testing for Mobile Applications"
