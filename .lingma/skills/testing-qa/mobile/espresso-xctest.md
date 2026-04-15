---
name: espresso-xctest
description: This skill covers production-grade test automation using Espresso (Android) and XCTest/XCUITest (iOS) — the two dominant native UI testing frameworks.
---

# Espresso & XCTest — Native Mobile Test Automation

**Category:** Mobile Test Automation — Native Frameworks
**Owner:** SDET Mobile #1 (Ananya Krishnan)

## Overview

This skill covers production-grade test automation using Espresso (Android) and XCTest/XCUITest (iOS) — the two dominant native UI testing frameworks. It addresses test architecture, synchronization strategies, intent mocking, performance measurement, and parallel execution on device farms. These frameworks form the foundation of the Stage 7 automated test suite for all native mobile features.

Mastery of both frameworks ensures comprehensive test coverage across the platform matrix, enables accurate defect reproduction at the native layer, and provides the test pyramid's integration and E2E layers with deterministic, fast-executing test suites.

## Competency Dimensions

| Dimension                          | Description                                                                                                                                                                                | Proficiency Indicators                                                                                                                                                                                                                                                |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Espresso Test Architecture**     | Composing tests with ViewMatchers, ViewActions, and ViewAssertions; structuring test classes by feature module; managing test dependencies and build variants                              | Tests use fluent matcher compositions (`allOf()`, `anyOf()`, `not()`); custom matchers extend `TypeSafeMatcher<View>`; test classes follow `FeatureNameEspressoTest` naming; build variants include debug manifests with `android:usesCleartextTraffic` for mock APIs |
| **Espresso Synchronization**       | IdlingResource API implementation, OkHttpIdlingResource integration, custom CountingIdlingResource for async operations, handling non-standard async patterns                              | Zero `Thread.sleep()` calls in test code; all async operations bridged via `IdlingResource`; custom idling resources registered in `@Before` and unregistered in `@After`; `EspressoIdlingResource` singleton wraps application-level async counters                  |
| **Espresso Intents & Stubbing**    | `IntentsTestRule` for intent capture/validation, `intending()` for stubbing external activity results, intent matching with `hasAction()`, `hasComponent()`, `hasData()`                   | All external activity launches (camera, contacts, payment SDKs) stubbed via `intending()`; intent verification uses `intended()` with Hamcrest matchers; deep link tests validate intent extras with `hasExtraWithKey()`                                              |
| **XCTest/XCUITest Architecture**   | XCUIApplication launch configuration, XCUIElement query resolution, accessibility identifier strategy, test class organization, shared test fixtures                                       | Every interactive UI element has a unique `accessibilityIdentifier`; queries use descendant matching (`app.tables["list"].cells["row-1"]`); test classes inherit from `XCTestCase` with `setUpWithError()` override; shared fixtures in `TestDataFactory` struct      |
| **XCTest UI Testing Patterns**     | Element state predicates (`exists`, `isHittable`), expectation-based async testing (`XCTNSPredicateExpectation`, `XCTWaiter`), swipe/drag gesture synthesis, keyboard interaction handling | Tests use `wait(for:timeout:)` with `XCTNSPredicateExpectations` instead of `sleep()`; gesture tests verify start/end coordinates; keyboard dismissal uses `app.typeKey("\n", modifierFlags: [])` or tap on coordinate outside keyboard frame                         |
| **XCTest Performance Testing**     | `measure(block:)` for benchmark execution, `XCTClockMetric`, `XCTCPUMetric`, `XCTMemoryMetric`, baseline management, performance regression gates                                          | Performance tests call `measure(metrics: [XCTClockMetric()], block:)`; baselines stored in `.xccovreport`; CI gates fail on >10% regression from baseline; memory tests capture `XCTMemoryMetric` before/after critical user journeys                                 |
| **Parallel Device Farm Execution** | Shard configuration for Firebase Test Lab / AWS Device Farm, test distribution strategy, flaky test isolation, result aggregation                                                          | Test sharding uses `testShards` parameter with `numUniformShards`; shard results merged via `junit-merge` or Firebase's built-in aggregation; flaky tests tagged with `@Flaky` annotation and quarantined in separate shard                                           |

## Execution Guidance

### Espresso — Core Patterns

**1. Standard Test Structure**

```kotlin
@RunWith(AndroidJUnit4::class)
@LargeTest
class CheckoutFlowEspressoTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    @Before
    fun registerIdlingResources() {
        IdlingRegistry.getInstance().register(EspressoIdlingResource.countingIdlingResource)
    }

    @After
    fun unregisterIdlingResources() {
        IdlingRegistry.getInstance().unregister(EspressoIdlingResource.countingIdlingResource)
    }

    @Test
    fun completePurchase_validCard_confirmsOrder() {
        // Navigate to checkout
        onView(withId(R.id.cart_button)).perform(click())
        onView(withId(R.id.checkout_button)).perform(click())

        // Fill payment form
        onView(withId(R.id.card_number_input)).perform(typeText("4111111111111111"), closeSoftKeyboard())
        onView(withId(R.id.expiry_input)).perform(typeText("12/28"), closeSoftKeyboard())
        onView(withId(R.id.cvv_input)).perform(typeText("123"), closeSoftKeyboard())

        // Submit and verify
        onView(withId(R.id.pay_button)).perform(click())
        onView(withId(R.id.order_confirmation)).check(matches(isDisplayed()))
        onView(withId(R.id.order_confirmation)).check(matches(withText(containsString("Order confirmed"))))
    }
}
```

**2. Custom ViewMatcher for Complex Assertions**

```kotlin
fun withRecyclerViewItemText(recyclerViewId: Int, position: Int, expectedText: String): Matcher<View> {
    return object : TypeSafeMatcher<View>() {
        override fun describeTo(description: Description) {
            description.appendText("RecyclerView item at position $position with text: $expectedText")
        }

        override fun matchesSafely(view: View): Boolean {
            if (view.id != recyclerViewId) return false
            val recyclerView = view as RecyclerView
            val viewHolder = recyclerView.findViewHolderForAdapterPosition(position) ?: return false
            val itemView = viewHolder.itemView
            val textView = itemView.findViewById<TextView>(R.id.item_title) ?: return false
            return textView.text.toString() == expectedText
        }
    }
}
```

**3. Intent Stubbing for External Activities**

```kotlin
@get:Rule
val intentsRule = IntentsTestRule(MainActivity::class.java)

@Test
fun cameraLaunch_returnsCapturedImage() {
    // Stub the camera intent result
    val resultData = Intent().apply {
        putExtra("data", createTestBitmap())
    }
    intending(hasAction(MediaStore.ACTION_IMAGE_CAPTURE)).respondWith(
        Instrumentation.ActivityResult(Activity.RESULT_OK, resultData)
    )

    // Trigger camera
    onView(withId(R.id.camera_button)).perform(click())

    // Verify image was received
    onView(withId(R.id.preview_image)).check(matches(isDisplayed()))
    intended(hasAction(MediaStore.ACTION_IMAGE_CAPTURE))
}
```

**4. IdlingResource for Network Calls**

```kotlin
object EspressoIdlingResource {
    private const val RESOURCE = "network_call"

    @JvmField
    val countingIdlingResource = CountingIdlingResource(RESOURCE)

    fun increment() { countingIdlingResource.increment() }
    fun decrement() { countingIdlingResource.decrement() }

    init {
        check(!countingIdlingResource.isIdleNow) { "Should not be idle at init" }
    }
}

// In your Retrofit/OkHttp interceptor:
class IdlingResourceInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        EspressoIdlingResource.increment()
        return try {
            chain.proceed(chain.request())
        } finally {
            EspressoIdlingResource.decrement()
        }
    }
}
```

### XCTest/XCUITest — Core Patterns

**1. Standard Test Structure**

```swift
class CheckoutFlowXCTest: XCTestCase {

    var app: XCUIApplication!

    override func setUpWithError() throws {
        try super.setUpWithError()
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["--ui-testing-mode"]
        app.launchEnvironment["MOCK_API"] = "true"
        app.launch()
    }

    func testCompletePurchase_validCard_confirmsOrder() {
        // Navigate to checkout
        app.buttons["cartButton"].tap()
        app.buttons["checkoutButton"].tap()

        // Fill payment form
        let cardField = app.textFields["cardNumberField"]
        cardField.tap()
        cardField.typeText("4111111111111111")

        app.textFields["expiryField"].tap()
        app.textFields["expiryField"].typeText("12/28")

        app.textFields["cvvField"].tap()
        app.textFields["cvvField"].typeText("123")

        // Submit and verify
        app.buttons["payButton"].tap()

        let confirmation = app.staticTexts["orderConfirmation"]
        let exists = NSPredicate(format: "exists == true")
        expectation(for: exists, evaluatedWith: confirmation, handler: nil)
        waitForExpectations(timeout: 10.0)

        XCTAssertTrue(confirmation.label.contains("Order confirmed"))
    }
}
```

**2. Accessibility Identifier Convention**

Every interactive element MUST have an `accessibilityIdentifier` set in production code (not `accessibilityLabel`, which is for VoiceOver):

```swift
// Production code:
cartButton.accessibilityIdentifier = "cartButton"
checkoutButton.accessibilityIdentifier = "checkoutButton"
cardNumberField.accessibilityIdentifier = "cardNumberField"
orderConfirmation.accessibilityIdentifier = "orderConfirmation"

// Test code queries:
app.buttons["cartButton"]       // Exact match on accessibilityIdentifier
app.textFields["cardNumberField"]
app.staticTexts["orderConfirmation"]
```

**3. Performance Test with Baseline**

```swift
func testLaunchPerformance() throws {
    let app = XCUIApplication()
    let metrics: [XCTMetric] = [
        XCTClockMetric(),
        XCTCPUMetric(),
        XCTMemoryMetric()
    ]
    measure(metrics: metrics, block: {
        app.launch()
        let loaded = app.tables["mainTable"]
        let exists = NSPredicate(format: "exists == true")
        let expectation = XCTNSPredicateExpectation(predicate: exists, object: loaded)
        wait(for: [expectation], timeout: 5.0)
    })
}
```

The `.xctestrun` file stores baseline values. CI compares new runs against baseline; >10% regression triggers a P1 defect.

**4. Handling Scrollable Lists**

```swift
func testScrollToLastItem_inLongList() {
    let table = app.tables["productList"]
    let lastItem = table.cells.element(boundBy: 99)  // Last item by index

    // Scroll until element exists
    while !lastItem.exists {
        table.swipeUp()
    }
    lastItem.tap()

    XCTAssertTrue(app.staticTexts["productDetailTitle"].exists)
}
```

### Device Farm Parallel Execution

**Firebase Test Lab (Android):**

```bash
gcloud firebase test android run \
  --type instrumentation \
  --app app/build/outputs/apk/debug/app-debug.apk \
  --test app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk \
  --device model=Pixel6,version=33,locale=en,orientation=portrait \
  --device model=GalaxyS23,version=33,locale=en,orientation=portrait \
  --test-runner-arguments numUniformShards=8 \
  --timeout 15m \
  --results-bucket gs://my-project-test-results \
  --results-dir $(date +%Y%m%d-%H%M%S)
```

**Xcode Cloud / xcodebuild for iOS parallel testing:**

```bash
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyAppUITests \
  -destination 'platform=iOS Simulator,name=iPhone 15,OS=17.0' \
  -destination 'platform=iOS Simulator,name=iPhone 14,OS=16.4' \
  -parallel-testing-enabled YES \
  -parallel-testing-worker-count 4 \
  -test-iterations 3 \
  -retry-tests-on-failure \
  resultBundlePath: TestResults.xcresult
```

**Flaky Test Quarantine Strategy:**

Tag known-flaky tests and exclude them from the primary shard:

```kotlin
// Android — custom annotation
@Retention(AnnotationRetention.RUNTIME)
@Target(AnnotationTarget.FUNCTION)
annotation class FlakyTest

// In build.gradle:
android {
    defaultConfig {
        testInstrumentationRunnerArgument "notAnnotation", "com.company.testing.FlakyTest"
    }
}

// Swift — test plan exclusion
// In .xctestplan: exclude tests with trait "flaky" from primary test target
```

## Pipeline Integration

| Stage                                | Application                                                                                                                        |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 5** (Development)            | Write native test scaffolding alongside feature code; ensure `accessibilityIdentifier` conventions are enforced in production code |
| **Stage 6** (Code Review)            | Review test code for anti-patterns: `Thread.sleep()`, hardcoded waits, missing IdlingResource, ambiguous XCUIElement queries       |
| **Stage 7** (Automated Testing)      | **Primary ownership** — execute Espresso and XCTest suites, manage device farm sharding, aggregate results, classify defects       |
| **Stage 8** (Integrity Verification) | Regression test suite runs against fixed defects; verify no functionality reduced (Stage 8 anti-pattern guard)                     |

## Quality Standards

| Metric                              | Target                          | Measurement                                                          |
| ----------------------------------- | ------------------------------- | -------------------------------------------------------------------- |
| Espresso test flake rate            | < 2% per 100 runs               | Measured via CI retry analysis over 30 days                          |
| XCTest execution time (full suite)  | < 25 minutes on single device   | `xcrun xcresulttool` duration extraction                             |
| IdlingResource coverage             | 100% of async operations        | Code review gate — no `Thread.sleep()` or `sleep()` allowed          |
| Accessibility identifier coverage   | 100% of interactive elements    | Automated lint check in CI (`accessibilityIdentifier` presence scan) |
| Device farm parallel shard success  | > 98% shard completion rate     | Firebase Test Lab / AWS Device Farm dashboard                        |
| Performance test baseline deviation | < 10% from established baseline | XCTest `measure()` baseline comparison; >10% = P1 defect             |
| Test code review turnaround         | < 4 hours                       | Tracked via PR metadata in Stage 6                                   |
