---
name: testing-qa-mobile-native-mobile-testing
description: 'Testing Qa skill: Native Mobile Testing'
---

# Native Mobile Testing

Platform-specific testing patterns, native debugging, crash analysis, memory leak detection, and ANR investigation on Android and iOS.

---

## 1. Overview

### 1.1 Native vs Cross-Platform Testing

| Dimension    | Native Testing                               | Cross-Platform Testing                  |
| ------------ | -------------------------------------------- | --------------------------------------- |
| **Tooling**  | Espresso, XCUITest                           | Appium, Maestro, Detox                  |
| **Language** | Kotlin (Android), Swift (iOS)                | JavaScript/TypeScript                   |
| **Speed**    | Fast (runs on device/emulator)               | Slower (bridge overhead)                |
| **Depth**    | Full platform API access                     | Limited to exposed bindings             |
| **CI Cost**  | Per-platform runner required                 | Single test suite, multi-platform       |
| **Best For** | Platform-specific features, deep integration | E2E flows, smoke tests across platforms |

### 1.2 Testing Pyramid for Native Mobile

```
                    ┌───────────────┐
                    │    Manual     │  Exploratory, usability
                   ┌┴───────────────┴┐
                  │    E2E / UI      │  XCUITest, Espresso flows
                 ┌┴─────────────────┴┐
                │   Integration       │  ViewModel + Repository
               ┌┴─────────────────────┴┐
              │      Unit Tests         │  Pure Kotlin/Swift logic
             └─────────────────────────┘
```

### 1.3 When to Use Native Testing

- **Platform-specific APIs**: Keychain, Keystore, BiometricPrompt, Haptics
- **Native UI components**: Navigation transitions, sheet presentations, Compose animations
- **Performance-critical paths**: Startup, scroll performance, memory-sensitive screens
- **Accessibility compliance**: VoiceOver/TalkBack testing requires platform-native tools
- **Crash investigation**: Symbolicated crash logs require platform-specific debuggers

---

## 2. Android Native Testing

### 2.1 Espresso Advanced

```kotlin
// Custom ViewAction for RecyclerView
fun clickRecyclerViewItemAt(position: Int): ViewAction {
    return object : ViewAction {
        override fun getConstraints() = isAssignableFrom(RecyclerView::class.java)
        override fun getDescription() = "Click RecyclerView item at position $position"
        override fun perform(uiController: UiController, view: View) {
            val rv = view as RecyclerView
            val viewHolder = rv.findViewHolderForAdapterPosition(position)
                ?: throw AssertionError("No ViewHolder at position $position")
            viewHolder.itemView.performClick()
            uiController.loopMainThreadForAtLeast(100)
        }
    }
}

// Testing Coroutines with MainDispatcherRule
@get:Rule
val mainDispatcherRule = MainDispatcherRule()

@Test
fun `should display user profile after load`() = runTest {
    // Arrange
    val mockRepo = FakeUserRepository()
    val viewModel = UserProfileViewModel(mockRepo)

    // Act
    viewModel.loadUser("user-123")
    advanceUntilIdle()

    // Assert
    assertEquals("John Doe", viewModel.userName.value)
    assertTrue(viewModel.isLoading.value == false)
}

// IdlingResource for async operations
class NetworkIdlingResource(
    private val okHttpClient: OkHttpClient
) : IdlingResource {
    @Volatile private var callback: IdlingResource.ResourceCallback? = null
    @Volatile private var activeCalls = 0

    override fun getName() = "NetworkIdlingResource"
    override fun isIdleNow() = activeCalls == 0

    override fun registerIdleTransitionCallback(callback: IdlingResource.ResourceCallback) {
        this.callback = callback
    }

    private val eventListener = object : EventListener() {
        override fun callStart(call: Call) {
            activeCalls++
        }
        override fun callEnded(call: Call) {
            activeCalls--
            if (activeCalls == 0) callback?.onTransitionToIdle()
        }
    }
}
```

### 2.2 UIAutomator for System UI

```kotlin
// Testing notification drawer interaction
@Test
fun `should handle notification tap`() {
    val device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())

    // Open notification shade
    device.openNotification()
    device.waitForIdle()

    // Find and tap notification
    val notification = device.findObject(
        UiSelector().textContains("New message")
    )
    notification.click()

    // Verify app opens to correct screen
    val appPackage = InstrumentationRegistry.getTargetContext().packageName
    device.wait(
        Until.hasObject(By.pkg(appPackage).depth(25)),
        5000
    )
}

// Testing multi-app flows
@Test
fun `should return from browser after auth`() {
    val device = UiDevice.getInstance(InstrumentationRegistry.getInstrumentation())

    // Launch browser
    val intent = Intent(Intent.ACTION_VIEW, Uri.parse("https://example.com/auth"))
    context.startActivity(intent)
    device.waitForIdle()

    // Simulate auth callback
    device.pressBack()

    // Verify return to app
    assertTrue(isAppInForeground(targetPackage))
}
```

### 2.3 Accessibility Scanner Integration

```kotlin
// Programmatic accessibility check in tests
@Test
fun `should meet accessibility requirements`() {
    val activity = activityScenarioRule.scenario
    val root = activity.awaitActivity().findViewById<ViewGroup>(android.R.id.content)

    // Check content descriptions
    val viewsWithoutLabels = mutableListOf<String>()
    traverseView(root) { view ->
        if (view.isImportantForAccessibility &&
            view.contentDescription.isNullOrEmpty() &&
            view.text.isNullOrEmpty()
        ) {
            viewsWithoutLabels.add(view.javaClass.simpleName)
        }
    }

    assertTrue(
        "Views missing accessibility labels: $viewsWithoutLabels",
        viewsWithoutLabels.isEmpty()
    )
}
```

### 2.4 Layout Inspector Workflow

```bash
# Capture layout hierarchy for analysis
adb shell uiautomator dump /sdcard/ui.xml
adb pull /sdcard/ui.xml ./layout-dump.xml

# Inspect view hierarchy programmatically
adb shell dumpsys activity top | grep -A 20 "mCurrentFocus"

# Check overdraw (rendering performance)
adb shell setprop debug.hwui.overdraw show
# Then: Settings > Developer options > Debug GPU overdraw
```

---

## 3. iOS Native Testing

### 3.1 XCUITest Advanced

```swift
// Custom XCUIElement query with timeout
extension XCUIApplication {
    func waitForElement(
        _ predicate: String,
        timeout: TimeInterval = 10,
        file: StaticString = #file,
        line: UInt = #line
    ) -> XCUIElement {
        let element = descendants(matching: .any).matching(
            NSPredicate(format: predicate)
        ).firstMatch

        let expectation = XCTNSPredicateExpectation(
            predicate: NSPredicate(format: "exists == true"),
            object: element
        )
        wait(for: [expectation], timeout: timeout)
        return element
    }
}

// Testing SwiftUI with accessibility identifiers
func testUserProfileDisplaysCorrectly() {
    let app = XCUIApplication()
    app.launchArguments = ["--testing"]
    app.launch()

    // Use accessibility identifiers set in SwiftUI
    let nameField = app.staticTexts["user-name-label"]
    XCTAssertTrue(nameField.waitForExistence(timeout: 5))
    XCTAssertEqual(nameField.label, "John Doe")

    // Test navigation
    app.buttons["settings-button"].tap()
    XCTAssertTrue(app.navigationBars["Settings"].waitForExistence(timeout: 3))
}

// Testing with mock server
func testNetworkErrorHandling() {
    // Inject mock URLProtocol
    MockURLProtocol.requestHandler = { request in
        let response = HTTPURLResponse(
            url: request.url!,
            statusCode: 500,
            httpVersion: nil,
            headerFields: nil
        )!
        return (response, Data())
    }

    let app = XCUIApplication()
    app.launch()

    let errorLabel = app.staticTexts["network-error"]
    XCTAssertTrue(errorLabel.waitForExistence(timeout: 5))
    XCTAssertEqual(errorLabel.label, "Unable to connect. Please try again.")
}
```

### 3.2 Accessibility Inspector

```swift
// Programmatic accessibility audit in tests
func testAccessibilityAudit() {
    let app = XCUIApplication()
    app.launch()

    // Run built-in accessibility audit
    let auditIssues = app.performAccessibilityAudit()
    for issue in auditIssues {
        XCTReport.issue(issue.description)
    }
    XCTAssertTrue(auditIssues.isEmpty, "Accessibility audit found issues")
}

// Testing VoiceOver gestures
func testVoiceOverNavigation() {
    // Enable voice over simulation
    let app = XCUIApplication()
    app.launch()

    // Activate first element
    let firstElement = app.buttons.firstMatch
    firstElement.activate()

    // Swipe right (next element)
    app.swipeRight()

    // Verify focus moved
    let focusedElement = app.staticTexts["welcome-text"]
    XCTAssertTrue(focusedElement.hasFocus)
}
```

### 3.3 View Debugger

```bash
# Reveal layout hierarchy
# Use Reveal app or Xcode View Debugger:
# Xcode > Debug > View Debugging > Capture View Hierarchy

# Export view hierarchy for CI analysis
xcrun simctl io booted screenshot screenshot.png

# List all accessibility elements
xcrun simctl spawn booted accessibility list
```

---

## 4. Native Debugging

### 4.1 Logcat Analysis (Android)

```bash
# Filter crashes only
adb logcat -s AndroidRuntime:E

# Filter ANR events
adb logcat -s ActivityManager:I am_anr

# Full crash stack trace with symbols
adb logcat -d > crash-logcat.txt

# Real-time crash monitoring
adb logcat '*:E' | grep -E "(FATAL|CRASH|AndroidRuntime)"

# Extract native crash (SIGSEGV, etc.)
adb logcat -s libc:F DEBUG:F
```

**Logcat Crash Pattern Recognition:**

```
# Java/Kotlin crash
AndroidRuntime: FATAL EXCEPTION: main
Process: com.example.app, PID: 12345
java.lang.NullPointerException
    at com.example.app.ui.MainActivity.onCreate(MainActivity.kt:42)

# Native crash (C/C++ via JNI)
DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
DEBUG   : Build fingerprint: 'google/redfin/redfin:12/SP1A/123456'
DEBUG   : Revision: '0'
DEBUG   : ABI: 'arm64'
DEBUG   : Timestamp: 2026-04-06 10:30:45.123456789+0000
DEBUG   : pid: 12345, tid: 12346, name: Thread-5
DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0

# OutOfMemoryError
AndroidRuntime: FATAL EXCEPTION: main
java.lang.OutOfMemoryError: Failed to allocate a 52428816 byte allocation
    at android.graphics.BitmapFactory.decodeStream(BitmapFactory.java:1)
```

### 4.2 ADB Commands for Debugging

```bash
# Force crash and capture
adb shell am force-stop com.example.app
adb shell am start -n com.example.app/.MainActivity
adb logcat -c && adb logcat > debug.log

# Monitor memory in real-time
adb shell dumpsys meminfo com.example.app

# Check strict mode violations
adb shell setprop debug.strictmode 1

# Simulate low memory condition
adb shell cmd activity trim-memory com.example.app RUNNING_CRITICAL

# Network traffic inspection (proxy)
adb shell settings put global http_proxy 192.168.1.100:8888
adb shell settings put global http_proxy :0  # Clear

# Battery stats
adb shell dumpsys batterystats com.example.app
```

### 4.3 LLDB Debugging (iOS)

```swift
// LLDB commands for iOS debugging
(lldb) po viewController          // Print object description
(lldb) expression -l swift --     // Execute Swift code
(lldb) bt                         // Full backtrace
(lldb) image lookup --address 0x  // Symbolicate address
(lldb) memory read --size 8 0x    // Read memory at address

// Symbolicate crash log
(lldb) symbolicate crash.log MyApp.app.dSYM/

// Set breakpoint on exception
(lldb) breakpoint set -E objc
(lldb) breakpoint set -n "-[UIViewController viewDidLoad]"

// Debug memory issues
(lldb) memory history 0x12345678  // Trace allocation
(lldb) expr (void)MallocStackLoggingEnable()
```

### 4.4 Instruments (iOS)

```bash
# Launch Instruments from CLI
xcrun instruments -t "Leaks" -w <device-uuid> com.example.app

# Time Profiler
xcrun instruments -t "Time Profiler" -w <device-uuid> com.example.app

# Energy Log
xcrun instruments -t "Energy Log" -w <device-uuid> com.example.app

# Automation with JavaScript
xcrun instruments -w <device-uuid> \
    -t "Automation" \
    com.example.app \
    -e UIASCRIPT script.js
```

---

## 5. Memory Leak Detection

### 5.1 Android Profiler

```kotlin
// LeakCanary integration (automatic)
// build.gradle.kts
debugImplementation("com.squareup.leakcanary:leakcanary-android:2.14")

// Manual heap dump analysis
class MemoryTestRule : TestRule {
    override fun apply(base: Statement, description: Description): Statement {
        return object : Statement() {
            override fun evaluate() {
                val runtime = Runtime.getRuntime()
                val beforeHeap = runtime.totalMemory() - runtime.freeMemory()

                base.evaluate()

                // Force GC and check for leaks
                System.gc()
                Runtime.getRuntime().gc()
                Thread.sleep(1000)

                val afterHeap = runtime.totalMemory() - runtime.freeMemory()
                val delta = afterHeap - beforeHeap

                if (delta > 10 * 1024 * 1024) { // 10MB threshold
                    println("WARNING: Possible memory leak, delta: ${delta / 1024 / 1024}MB")
                }
            }
        }
    }
}

// Detecting Bitmap leaks
fun checkBitmapLeaks(context: Context) {
    val bitmap = BitmapFactory.decodeResource(context.resources, R.drawable.large_image)
    // CRITICAL: Always recycle bitmaps when done
    bitmap.recycle()
}

// Activity/Fragment leak detection
@Test
fun `activity should not leak on rotation`() {
    val scenario = ActivityScenario.launch(MainActivity::class.java)

    // Rotate multiple times
    repeat(5) {
        scenario.recreate()
    }

    // LeakCanary will automatically detect leaks
    // Check for any pending leak reports
    Thread.sleep(2000) // Give LeakCanary time to analyze
}
```

### 5.2 iOS Instruments - Leaks

```swift
// Testing for retain cycles
final class ViewModelTests: XCTestCase {
    func testViewModelReleasesOnDismiss() {
        weak var weakViewModel: DetailViewModel?

        autoreleasepool {
            let nav = UINavigationController()
            let vm = DetailViewModel()
            weakViewModel = vm

            let vc = DetailViewController(viewModel: vm)
            nav.pushViewController(vc, animated: false)
            nav.popViewController(animated: false)
        }

        // Force cleanup
        RunLoop.current.run(until: Date())

        XCTAssertNil(weakViewModel, "ViewModel should be deallocated")
    }
}

// Detecting capture list issues
class NotificationObserver {
    private var cancellables = Set<AnyCancellable>()

    deinit {
        print("NotificationObserver deinitialized") // Should be called
    }

    func startObserving() {
        // WRONG: Creates retain cycle
        // NotificationCenter.default.publisher(for: .userDidLogin)
        //     .sink { [self] _ in handleLogin() }

        // CORRECT: Weak capture
        NotificationCenter.default.publisher(for: .userDidLogin)
            .sink { [weak self] _ in self?.handleLogin() }
            .store(in: &cancellables)
    }
}
```

### Memory Leak Debugging Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    MEMORY LEAK INVESTIGATION                │
└─────────────────────────────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       ┌─────────────┐          ┌──────────────┐
       │   Android   │          │     iOS      │
       └──────┬──────┘          └──────┬───────┘
              │                        │
    ┌─────────┴─────────┐   ┌─────────┴──────────┐
    ▼                   ▼   ▼                    ▼
┌─────────┐      ┌──────────┐  ┌──────────┐  ┌──────────┐
│LeakCanary│      │Profiler  │  │Instruments│  │Xcode Mem │
│  (auto)  │      │(manual)  │  │ Leaks    │  │ Debugger │
└────┬─────┘      └────┬─────┘  └────┬─────┘  └────┬─────┘
     │                 │              │              │
     ▼                 ▼              ▼              ▼
┌──────────────────────────────────────────────────────────┐
│              Identify leak source:                       │
│  • Retain cycles (closures, delegates)                  │
│  • Uncancelled coroutines/subscriptions                 │
│  • Static references to Context/Views                   │
│  • Bitmap/cache not released                            │
│  • Observer not removed                                 │
└──────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │     Fix + Retest       │
              │  (verify no leak after │
              │   5+ lifecycle cycles) │
              └────────────────────────┘
```

---

## 6. ANR / Freeze Investigation

### 6.1 ANR Traces (Android)

```bash
# Pull ANR traces from device
adb pull /data/anr/traces.txt ./anr-traces.txt

# ANR types and their signatures
# 1. KeyDispatchTimeout (5s) - Input event not processed
# 2. BroadcastTimeout (10s) - BroadcastReceiver.onReceive too long
# 3. ServiceTimeout (20s) - Service lifecycle method too long

# Identify ANR-causing thread
grep -A 50 "DALVIK THREADS" anr-traces.txt | head -60

# Look for blocked state
# |  "main" prio=5 tid=1 Blocked
# |    at com.example.app.MainActivity.onSomething(MainActivity.kt:42)
# |    - waiting to lock <0x12345678> (a java.lang.Object)
```

### 6.2 StrictMode Configuration

```kotlin
// Enable StrictMode in debug builds
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        if (BuildConfig.DEBUG) {
            StrictMode.setThreadPolicy(
                StrictMode.ThreadPolicy.Builder()
                    .detectAll()
                    .penaltyLog()
                    .penaltyDeath() // Crashes on violation (testing only)
                    .build()
            )

            StrictMode.setVmPolicy(
                StrictMode.VmPolicy.Builder()
                    .detectLeakedSqlLiteObjects()
                    .detectLeakedClosableObjects()
                    .detectActivityLeaks()
                    .penaltyLog()
                    .penaltyDeath()
                    .build()
            )
        }
    }
}

// StrictMode violations to watch for:
// - DiskReadOnMainThread
// - DiskWriteOnMainThread
// - NetworkOnMainThread
// - LeakedClosableObjects
// - LeakedRegistrationObjects
// - LeakedSqliteObjects
```

### 6.3 Watchdog Timeout (iOS)

```swift
// iOS watchdog timeouts
// - Launch: 20 seconds (background), 5 seconds (foreground)
// - Resume: 10 seconds
// - Suspend: 10 seconds
// - Terminate: 5 seconds

// Detecting main thread blocking
class MainThreadChecker {
    private var heartbeatTimer: Timer?
    private var lastHeartbeat: Date = Date()

    func startMonitoring() {
        heartbeatTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            self.lastHeartbeat = Date()
        }
    }

    func checkForBlocking() {
        let timeSinceHeartbeat = Date().timeIntervalSince(lastHeartbeat)
        if timeSinceHeartbeat > 5.0 {
            print("WARNING: Main thread may be blocked for \(timeSinceHeartbeat)s")
        }
    }
}

// Testing freeze conditions
func testScrollViewDoesNotFreeze() {
    let app = XCUIApplication()
    app.launch()

    let scrollView = app.scrollViews.firstMatch

    // Measure scroll responsiveness
    measure(metrics: [XCTOSSignpostMetric.scrollDecelerationMetric]) {
        scrollView.swipeUp()
        scrollView.swipeDown()
    }
}
```

### ANR Investigation Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                      ANR INVESTIGATION                      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │   Reproduce ANR on     │
              │   physical device      │
              └───────────┬────────────┘
                          │
              ┌───────────┴────────────┐
              ▼                        ▼
     ┌────────────────┐      ┌─────────────────┐
     │ Check traces.txt│      │ Check logcat for│
     │ (main thread   │      │ StrictMode       │
     │  state)         │      │ violations       │
     └───────┬────────┘      └────────┬────────┘
             │                        │
             └───────────┬────────────┘
                         ▼
              ┌────────────────────────┐
              │   Common causes:       │
              │   1. DB query on main  │
              │   2. Network on main   │
              │   3. Large bitmap decode│
              │   4. Lock contention   │
              │   5. Heavy Compose     │
              │      recomposition     │
              └───────────┬────────────┘
                          ▼
              ┌────────────────────────┐
              │   Fix: Move to         │
              │   background thread    │
              │   (Coroutine/Dispatch) │
              └───────────┬────────────┘
                          ▼
              ┌────────────────────────┐
              │   Verify: StrictMode   │
              │   passes, no ANR in    │
              │   100+ interactions    │
              └────────────────────────┘
```

---

## 7. Performance Profiling

### 7.1 Startup Time Measurement

```kotlin
// Android - Measured startup
@Test
fun `cold start should be under 2 seconds`() {
    val context = InstrumentationRegistry.getInstrumentation().targetContext
    val packageManager = context.packageManager
    val intent = packageManager.getLaunchIntentForPackage(context.packageName)!!

    val startTime = System.currentTimeMillis()
    ActivityScenario.launch<MainActivity>(intent)
    val endTime = System.currentTimeMillis()

    val startupTime = endTime - startTime
    assertTrue("Cold start took ${startupTime}ms (limit: 2000ms)", startupTime < 2000)
}

// Android - Baseline Profiles
// app/build.gradle.kts
baselineProfile {
    mergeIntoMain = true
    saveInSrc = true
    from("com.example.app.benchmark.BaselineProfileGenerator")
}
```

```swift
// iOS - Measured startup
func testColdStartupTime() {
    let app = XCUIApplication()
    app.launchArguments = ["--cold-start"]

    let start = CFAbsoluteTimeGetCurrent()
    app.launch()

    let firstScreen = app.staticTexts["home-screen"]
    XCTAssertTrue(firstScreen.waitForExistence(timeout: 2.0))

    let elapsed = CFAbsoluteTimeGetCurrent() - start
    XCTAssertLessThan(elapsed, 2.0, "Cold start should be under 2 seconds")
}
```

### 7.2 Frame Rate Monitoring

```kotlin
// Android - FrameCallback for dropped frames
class FrameRateMonitor {
    private var droppedFrames = 0
    private var totalFrames = 0

    private val frameCallback = object : Choreographer.FrameCallback {
        override fun doFrame(frameTimeNanos: Long) {
            totalFrames++
            val jitterNanos = System.nanoTime() - frameTimeNanos
            if (jitterNanos > 16_666_667) { // 60fps threshold
                droppedFrames++
            }
            Choreographer.getInstance().postFrameCallback(this)
        }
    }

    fun start() = Choreographer.getInstance().postFrameCallback(frameCallback)
    fun stop() { /* remove callback */ }
    fun getDroppedFramePercentage() = if (totalFrames > 0) droppedFrames.toDouble() / totalFrames else 0.0
}

// Compose-specific: Report draw frames
@Test
fun `compose list should maintain 60fps`() {
    composeTestRule.setContent {
        LazyColumn {
            items(100) { Text("Item $it") }
        }
    }

    val monitor = FrameRateMonitor()
    monitor.start()

    composeTestRule.onRoot().performTouchInput { swipeUp() }
    composeTestRule.waitForIdle()

    monitor.stop()
    assertTrue(monitor.getDroppedFramePercentage() < 0.1, "Dropped frames > 10%")
}
```

### 7.3 Battery Impact

```kotlin
// Android - Battery Historian
adb shell dumpsys batterystats --reset
# Run app through test scenario
adb shell dumpsys batterystats com.example.app > battery-stats.txt
# Upload to Battery Historian: https://github.com/google/battery-historian
```

```swift
// iOS - Energy impact in tests
func testEnergyImpact() {
    let app = XCUIApplication()
    app.launch()

    // Run energy-intensive scenario
    measure(metrics: [XCTOSSignpostMetric.lifecycle]) {
        performEnergyIntensiveFlow(app)
    }
}
```

### 7.4 Network Performance

```kotlin
// Android - OkHttp Profiling Interceptor
class PerformanceInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val startTime = System.nanoTime()
        val response = chain.proceed(chain.request())
        val elapsed = System.nanoTime() - startTime

        val request = chain.request()
        Log.d("NetworkPerf", "${request.method} ${request.url} - ${elapsed / 1_000_000}ms")

        if (elapsed > 500_000_000) { // > 500ms warning
            Log.w("NetworkPerf", "SLOW REQUEST: ${request.url} took ${elapsed / 1_000_000}ms")
        }

        return response
    }
}
```

---

## 8. CI/CD Integration

### 8.1 Android CI Configuration

```yaml
# GitHub Actions - Android
- name: Run Instrumented Tests
  uses: reactivecircus/android-emulator-runner@v2
  with:
    api-level: 34
    target: google_apis
    arch: x86_64
    script: ./gradlew connectedAndroidTest

- name: Run Unit Tests
  run: ./gradlew testDebugUnitTest

- name: Upload Test Results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: '**/build/outputs/androidTest-results/'
```

### 8.2 iOS CI Configuration

```yaml
# GitHub Actions - iOS
- name: Run iOS Tests
  run: |
    xcodebuild test \
      -project MyApp.xcodeproj \
      -scheme MyApp \
      -destination 'platform=iOS Simulator,name=iPhone 15,OS=17.4' \
      -resultBundlePath TestResults \
      ONLY_ACTIVE_ARCH=YES

- name: Upload Test Results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: ios-test-results
    path: TestResults/
```

### 8.3 Test Sharding

```bash
# Android - Shard across emulators
./gradlew connectedAndroidTest \
  -Pandroid.testInstrumentationRunnerArguments.numShards=4 \
  -Pandroid.testInstrumentationRunnerArguments.shardIndex=0

# iOS - Parallel test execution
xcodebuild test \
  -parallel-testing-enabled YES \
  -parallel-testing-worker-count 4 \
  -maximum-concurrent-test-simulator-threads 4
```

---

## 9. Stage 7 / Stage 8 Integration

### 9.1 Stage 7 — Automated Testing

Native mobile tests are part of the Stage 7 test suite. The Test Lead (`priscilla-oduya`) coordinates with platform leads to ensure:

| Artifact                   | Location                                                           |
| -------------------------- | ------------------------------------------------------------------ |
| Android instrumented tests | `company/project/<project>/platforms/android/app/src/androidTest/` |
| iOS XCUITests              | `company/project/<project>/platforms/ios/UITests/`                 |
| Test results report        | `company/project/<project>/testing/results/`                       |
| Defects                    | `company/project/<project>/testing/defects/`                       |

**Stage 7 Gate Criteria for Native:**

- All instrumented tests pass on minimum supported OS versions
- Accessibility audit passes (no critical violations)
- Performance thresholds met (startup < 2s, no ANRs in 100 interactions)
- Memory leak checks pass (LeakCanary/Instruments clean)

### 9.2 Stage 8 — Integrity Verification

During Stage 8 integrity review, native mobile artifacts undergo:

| Check                                          | Responsible    |
| ---------------------------------------------- | -------------- |
| All Stage 7 defects remediated                 | Test Lead      |
| No regression in native functionality          | Platform Leads |
| OWASP MASVS compliance (security testing)      | CSO            |
| Accessibility compliance (WCAG 2.1 AA / MASVS) | CDO            |
| Platform-specific requirements met             | Platform Leads |

### 9.3 Defect Classification for Native Issues

| Issue                           | Severity | Rationale                      |
| ------------------------------- | -------- | ------------------------------ |
| App crash on launch             | P0       | Non-negotiable release blocker |
| ANR on core screen (>5s freeze) | P0       | Core UX failure                |
| Memory leak causing OOM         | P1       | Data loss risk                 |
| VoiceOver/TalkBack broken       | P1       | Accessibility failure          |
| Dropped frames on animation     | P2       | Minor UX degradation           |
| Slightly slow cold start (2-3s) | P2       | User decides fix/defer         |
| Minor layout misalignment       | P3       | Cosmetic                       |

---

## 10. References

### 10.1 Official Documentation

| Resource        | URL                                                         |
| --------------- | ----------------------------------------------------------- |
| Android Testing | https://developer.android.com/training/testing              |
| Espresso        | https://developer.android.com/training/testing/espresso     |
| UIAutomator     | https://developer.android.com/training/testing/ui-automator |
| XCUITest        | https://developer.apple.com/documentation/xctest            |
| Instruments     | https://developer.apple.com/documentation/instruments       |
| LLDB            | https://lldb.llvm.org/                                      |
| LeakCanary      | https://square.github.io/leakcanary/                        |
| OWASP MASVS     | https://mas.owasp.org/                                      |

### 10.2 Related Skills

| Skill            | Location                                    |
| ---------------- | ------------------------------------------- |
| `android`        | `.opencode/skills/android-overview/`        |
| `ios`            | `.opencode/skills/ios-overview/`            |
| `cross-platform` | `.opencode/skills/cross-platform-overview/` |
| `testing-qa`     | `.opencode/skills/testing-qa-overview/`     |
| `security`       | `.opencode/skills/security-overview/`       |

### 10.3 Pipeline References

| Document                        | Path                                                |
| ------------------------------- | --------------------------------------------------- |
| Pipeline Definition             | `.opencode/pipeline/mobile-development/pipeline.md` |
| Stage 7: Automated Testing      | Stage 7 in pipeline                                 |
| Stage 8: Integrity Verification | Stage 8 in pipeline                                 |
| Monitoring System               | `company/pipeline/mobile-development/monitoring.md` |

---

_Last updated: 2026-04-06_
