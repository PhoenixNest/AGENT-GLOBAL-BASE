# Test Types

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
- assertVisible: "Welcome"
- tapOn: "Sign In"
- tapOn:
    id: "email_field"
- inputText: "test@example.com"
- tapOn:
    id: "password_field"
- inputText: "SecurePass123!"
- tapOn: "Login"
- assertVisible: "Dashboard"
- assertVisible:
    text: "Hello, Test User"
- tapOn: "Sync"
- assertVisible: "Last synced: Just now"
- assertVisible: "All data up to date"
```

### 5. Accessibility Testing

Accessibility testing ensures the app is usable by people with diverse abilities — visual, auditory, motor, cognitive.

**Compliance Standard:** WCAG 2.1 AA (company standard per AGENTS.md)

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

**Compliance Standard:** OWASP MASVS (company standard per AGENTS.md)

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
