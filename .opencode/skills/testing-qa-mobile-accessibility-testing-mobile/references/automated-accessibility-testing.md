# Automated Accessibility Testing

## Automated Accessibility Testing

Accessibility checks should be integrated into the automated test suite to catch regressions.

### Espresso Accessibility Checks (Android)

```kotlin
import androidx.test.espresso.accessibility.AccessibilityChecks
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.matcher.ViewMatchers.withId
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import androidx.test.ext.junit.runners.AndroidJUnit4

@RunWith(AndroidJUnit4::class)
class AccessibilityTest {

    @Before
    fun setUp() {
        // Enable accessibility checks for all views in the view hierarchy
        AccessibilityChecks.enable().apply {
            // Optionally suppress specific checks
            setSuppressingResultMatcher(
                matchesCheckNames(
                    `is`("SpeakableTextPresentCheck")
                )
            )
        }
    }

    @Test
    fun mainScreen_accessibilityChecks() {
        // Launch the activity and run accessibility checks automatically
        onView(withId(R.id.main_screen)).check(matches(isDisplayed()))
    }

    @Test
    fun allScreens_accessibilityChecks() {
        // Navigate through screens and run checks on each
        onView(withId(R.id.nav_button)).perform(click())
        onView(withId(R.id.second_screen)).check(matches(isDisplayed()))
        // AccessibilityChecks.runChecks() is called automatically on each check
    }
}
```

### XCTest Accessibility Checks (iOS)

```swift
import XCTest

class AccessibilityTests: XCTestCase {

    let app = XCUIApplication()

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app.launch()
    }

    func testMainScreen_allElementsAccessible() {
        // Verify key elements have accessibility labels
        XCTAssertTrue(app.buttons["submit"].exists)
        XCTAssertEqual(app.buttons["submit"].label, "Submit")
        XCTAssertEqual(app.buttons["submit"].accessibilityTraits, .button)

        // Verify text fields have labels
        XCTAssertTrue(app.textFields["email"].exists)
        XCTAssertEqual(app.textFields["email"].label, "Email address")

        // Verify images are properly marked
        let decorativeImage = app.images["decorativeBackground"]
        if decorativeImage.exists {
            XCTAssertTrue(decorativeImage.isAccessibilityElement == false,
                "Decorative images should not be accessibility elements")
        }
    }

    func testNavigation_accessibilityLabels() {
        // Test all navigation elements
        let tabBar = app.tabBars.element
        XCTAssertTrue(tabBar.buttons["home"].exists)
        XCTAssertEqual(tabBar.buttons["home"].label, "Home")
        XCTAssertEqual(tabBar.buttons["home"].accessibilityTraits, .tab)
    }
}
```

### CI/CD Automation Strategy

| Stage             | Tool                      | Action                                              |
| ----------------- | ------------------------- | --------------------------------------------------- |
| Lint/Static Check | Android Lint, SwiftLint   | Fail build on missing accessibility attributes      |
| Unit Test         | Espresso + XCTest         | Run accessibility assertions in test suite          |
| Integration Test  | Maestro/Appium            | Navigate screens with accessibility assertions      |
| Post-Deploy       | Accessibility Scanner API | Run automated screen scans (where API available)    |
| Gate Criteria     | Stage 7 Test Results      | Accessibility checks must pass for Stage 7 sign-off |

---
