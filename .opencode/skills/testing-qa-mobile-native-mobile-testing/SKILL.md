---
name: testing-qa-mobile-native-mobile-testing
description: Native mobile testing patterns — platform-specific test architecture for iOS (Swift Testing, XCTest) and Android (JUnit 5, Espresso), native component testing, platform API mocking, and device-specific test considerations. Owned by Tobias Weber (SDET). Use during Stage 5 (Development) for native test implementation and Stage 7 (Testing) for platform-specific test execution. Trigger: native mobile testing, Swift Testing, XCTest, JUnit 5, Espresso, platform component testing, native API mocking, device-specific tests.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
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

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`3.-ios-native-testing.md`](references/3.-ios-native-testing.md) — 3. iOS Native Testing
- [`4.-native-debugging.md`](references/4.-native-debugging.md) — 4. Native Debugging
- [`5.-memory-leak-detection.md`](references/5.-memory-leak-detection.md) — 5. Memory Leak Detection
- [`6.-anr---freeze-investigation.md`](references/6.-anr---freeze-investigation.md) — 6. ANR / Freeze Investigation
- [`7.-performance-profiling.md`](references/7.-performance-profiling.md) — 7. Performance Profiling
- [`8.-ci-cd-integration.md`](references/8.-ci-cd-integration.md) — 8. CI/CD Integration
- [`10.-references.md`](references/10.-references.md) — 10. References
