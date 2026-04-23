---
name: testing-qa-mobile-accessibility-testing-mobile
description: 'Testing Qa skill: Accessibility Testing Mobile'
---

# Mobile Accessibility Testing

## Overview

Mobile accessibility testing ensures that applications are usable by people with diverse abilities, including visual, auditory, motor, and cognitive impairments. This skill covers the systematic verification of accessibility compliance for Android and iOS platforms against internationally recognized standards.

### Regulatory Framework

Accessibility compliance is not optional. The following standards define the baseline requirements:

| Standard          | Scope                                     | Alignment with WCAG         |
| ----------------- | ----------------------------------------- | --------------------------- |
| **WCAG 2.1 AA**   | Web Content Accessibility Guidelines      | Primary reference standard  |
| **Section 508**   | U.S. federal accessibility requirement    | Incorporates WCAG 2.1 AA    |
| **EN 301 549**    | European accessibility requirement        | Harmonized with WCAG 2.1 AA |
| **ADA Title III** | U.S. civil rights — public accommodations | Courts reference WCAG 2.1   |
| **AODA**          | Ontario Accessibility for Ontarians Act   | WCAG 2.0 AA minimum         |

### WCAG 2.1 AA Principles (POUR)

| Principle          | Requirement                                                                        |
| ------------------ | ---------------------------------------------------------------------------------- |
| **Perceivable**    | Information and UI components must be presentable in ways users can perceive       |
| **Operable**       | UI components and navigation must be operable by all users                         |
| **Understandable** | Information and operation of UI must be understandable                             |
| **Robust**         | Content must be robust enough to be interpreted reliably by assistive technologies |

### Mobile-Specific WCAG Success Criteria (AA Level)

| SC Number | Criterion              | Level | Mobile Relevance                                           |
| --------- | ---------------------- | ----- | ---------------------------------------------------------- |
| 1.1.1     | Non-text Content       | A     | All images, icons, and decorative elements need alt text   |
| 1.3.1     | Info and Relationships | A     | Semantic structure, headings, list semantics               |
| 1.3.2     | Meaningful Sequence    | A     | Screen reader reading order must match visual order        |
| 1.3.4     | Orientation            | AA    | Content must not lock to portrait or landscape             |
| 1.3.5     | Identify Input Purpose | A     | Form fields must declare autocomplete semantics            |
| 1.4.1     | Use of Color           | A     | Color must not be the sole means of conveying information  |
| 1.4.3     | Contrast (Minimum)     | AA    | 4.5:1 for normal text, 3:1 for large text                  |
| 1.4.4     | Resize Text            | AA    | Text must scale to 200% without loss of content/function   |
| 1.4.10    | Reflow                 | AA    | Content reflows at 320px width without horizontal scroll   |
| 1.4.11    | Non-text Contrast      | AA    | UI components and graphical objects: 3:1 minimum           |
| 1.4.12    | Text Spacing           | AA    | Line height, paragraph, letter, and word spacing overrides |
| 2.1.1     | Keyboard               | A     | All functionality accessible via external keyboard/switch  |
| 2.2.1     | Timing Adjustable      | A     | Users can adjust or extend time limits                     |
| 2.4.3     | Focus Order            | A     | Focus order preserves meaning and operability              |
| 2.4.7     | Focus Visible          | AA    | Focus indicator must be clearly visible                    |
| 2.5.1     | Pointer Gestures       | A     | No path-based gestures without single-pointer alternative  |
| 2.5.2     | Pointer Cancellation   | A     | Single tap activates, no accidental activation on down     |
| 2.5.3     | Label in Name          | A     | Visible label must be part of the accessibility name       |
| 2.5.7     | Dragging Movements     | AA    | Dragging must have single-pointer alternative (WCAG 2.2)   |
| 3.2.2     | On Input               | A     | Context changes only occur on user-initiated action        |
| 4.1.2     | Name, Role, Value      | A     | All components expose name, role, and state to AT          |
| 4.1.3     | Status Messages        | AA    | Status messages announced to assistive technology          |

### Platform Accessibility APIs

| Platform | Accessibility API         | Key Properties                                                                         |
| -------- | ------------------------- | -------------------------------------------------------------------------------------- |
| Android  | Accessibility Framework   | `contentDescription`, `contentDescription`, `isFocusable`, `isClickable`               |
| iOS      | UI Accessibility Protocol | `accessibilityLabel`, `accessibilityHint`, `accessibilityValue`, `accessibilityTraits` |
| Android  | View Properties           | `importantForAccessibility`, `liveRegion`                                              |
| iOS      | UIAccessibility           | `accessibilityIdentifier`, `accessibilityLanguage`, `isAccessibilityElement`           |

---

## Screen Reader Testing

Screen readers are the primary assistive technology for blind and low-vision users. Both TalkBack (Android) and VoiceOver (iOS) must be tested.

### TalkBack Testing (Android)

#### Essential Gestures

| Gesture                       | Action                               | Test Scenario                                     |
| ----------------------------- | ------------------------------------ | ------------------------------------------------- |
| Single tap                    | Focus item (do not activate)         | Verify item receives focus and reads announcement |
| Double tap anywhere on screen | Activate focused item                | Verify activation matches focused element         |
| Swipe right                   | Move focus to next item              | Verify logical navigation order                   |
| Swipe left                    | Move focus to previous item          | Verify reverse navigation order                   |
| Two-finger swipe up           | Open local context menu              | Verify headings, links, controls available        |
| Three-finger swipe up         | Scroll up                            | Verify scrollable content moves                   |
| Three-finger swipe down       | Scroll down                          | Verify scrollable content moves                   |
| Two-finger double tap         | Play/pause (media controls)          | Verify media playback control                     |
| Two-finger triple tap         | Screen curtain toggle (if supported) | Verify screen blackout for low-vision testing     |

#### TalkBack Announcement Verification Checklist

For each interactive element, verify the following:

- [ ] **Name/Label**: Reads meaningful text (not resource IDs like `@string/button_1`)
- [ ] **Role/Type**: Announces element type (button, checkbox, link, heading)
- [ ] **State**: Announces current state (checked, unchecked, selected, expanded)
- [ ] **Value**: For sliders/progress bars, announces current value with context
- [ ] **Hint**: Where needed, announces usage hint (e.g., "Double-tap to activate")
- [ ] **Context**: Grouped elements announce combined context
- [ ] **Heading**: Headings announce "Heading" prefix
- [ ] **Link**: Links announce "Link" suffix
- [ ] **Button**: Buttons announce "Button" suffix
- [ ] **Image/Icon**: Decorative images are hidden (`importantForAccessibility="no"`); informative images have descriptions

#### TalkBack Testing Scenarios

| Scenario                         | Expected Behavior                                         |
| -------------------------------- | --------------------------------------------------------- |
| Navigate through list of items   | Each item announced in visual order; no items skipped     |
| Focus on button                  | "Submit, button, double-tap to activate"                  |
| Focus on checked checkbox        | "Agree to terms, checkbox, checked, double-tap to toggle" |
| Focus on text input field        | "Email address, edit box, double-tap to edit"             |
| Focus on image with description  | "Company logo, image"                                     |
| Focus on decorative icon         | No announcement; focus skips element                      |
| Navigate modal dialog            | Focus trapped within modal; background not reachable      |
| Swipe gesture in scrollable list | Focus moves through items; scroll announced at boundaries |

### VoiceOver Testing (iOS)

#### Essential Gestures

| Gesture                       | Action                       | Test Scenario                                     |
| ----------------------------- | ---------------------------- | ------------------------------------------------- |
| Single tap                    | Focus item (do not activate) | Verify item receives focus and reads announcement |
| Double tap anywhere on screen | Activate focused item        | Verify activation matches focused element         |
| Swipe right                   | Move focus to next item      | Verify logical navigation order                   |
| Swipe left                    | Move focus to previous item  | Verify reverse navigation order                   |
| Three-finger swipe up         | Scroll up                    | Verify scrollable content moves                   |
| Three-finger swipe down       | Scroll down                  | Verify scrollable content moves                   |
| Two-finger tap                | Silence VoiceOver            | Verify VoiceOver can be silenced                  |
| Three-finger double tap       | Toggle screen curtain        | Verify screen blackout for low-vision testing     |
| Rotor gesture                 | Open rotor menu              | Verify headings, links, controls available        |

#### VoiceOver Announcement Verification Checklist

For each interactive element, verify the following:

- [ ] **accessibilityLabel**: Reads meaningful text
- [ ] **accessibilityTraits**: Announces element type (Button, Link, Image, Static Text)
- [ ] **accessibilityValue**: For controls, announces current value
- [ ] **accessibilityHint**: Where needed, provides usage guidance
- [ ] **isAccessibilityElement**: Set to true for interactive, false for decorative
- [ ] **accessibilityGroup**: Grouped elements combine into single announcement
- [ ] **accessibilityTraits includes .notEnabled**: Disabled controls announce state

#### VoiceOver Testing Scenarios

| Scenario                    | Expected Behavior                                        |
| --------------------------- | -------------------------------------------------------- |
| Navigate through table rows | Each row announced with label, detail, and traits        |
| Focus on button             | "Submit, Button"                                         |
| Focus on selected tab       | "Home, Tab, selected, double-tap to activate"            |
| Focus on text field         | "Password, Secure text field, double-tap to edit"        |
| Focus on switch control     | "Notifications, Toggle button, on, double-tap to toggle" |
| Navigate grouped elements   | Combined announcement for logical groups                 |
| Navigate collection view    | Items announced in order; "collection, X items"          |
| Dismiss modal               | Focus returns to triggering element                      |

### Cross-Platform Screen Reader Comparison

| Aspect               | Android (TalkBack)                  | iOS (VoiceOver)                   |
| -------------------- | ----------------------------------- | --------------------------------- |
| Activation gesture   | Double tap anywhere                 | Double tap anywhere               |
| Focus navigation     | Swipe left/right                    | Swipe left/right                  |
| Context menu         | Local context (two-finger swipe up) | Rotor (two-finger rotate)         |
| Screen curtain       | Two-finger triple tap (if enabled)  | Three-finger double tap           |
| Silence announcement | Two-finger tap (brief)              | Two-finger tap                    |
| Custom labels        | `contentDescription` on View        | `accessibilityLabel` on UIView    |
| Hidden elements      | `importantForAccessibility="no"`    | `isAccessibilityElement = false`  |
| Grouped elements     | AccessibilityDelegate               | `accessibilityElements` array     |
| Live regions         | `liveRegion` on View                | `UIAccessibilityPostNotification` |

---

## Touch Target Testing

Touch targets must be large enough and well-spaced enough for users with motor impairments to activate reliably.

### Minimum Touch Target Sizes

| Platform | Minimum Size   | Recommendation                      | Rationale                                                    |
| -------- | -------------- | ----------------------------------- | ------------------------------------------------------------ |
| iOS      | 44 x 44 pt     | Apple HIG                           | Human Interface Guidelines minimum for all tappable elements |
| Android  | 48 x 48 dp     | Material Design 3                   | Material Design accessibility guidelines                     |
| WCAG 2.1 | 24 x 24 CSS px | Target Size (SC 2.5.8, WCAG 2.2 AA) | Absolute minimum; 44pt/48dp preferred for mobile             |

### Touch Target Spacing

| Criterion                         | Requirement                                        | Measurement Method                         |
| --------------------------------- | -------------------------------------------------- | ------------------------------------------ |
| WCAG 2.5.5 Target Size (Enhanced) | 44 x 44 CSS px minimum, or equivalent spacing      | Measure center-to-center distance          |
| WCAG 2.5.8 Target Size (Minimum)  | 24 x 24 CSS px minimum                             | Visual bounding box of interactive element |
| Material Design                   | 8dp minimum spacing between adjacent touch targets | Measure gap between target bounding boxes  |
| Apple HIG                         | Adjacent targets should not overlap                | Verify no overlapping hit areas            |

### Touch Target Testing Procedure

1. **Enable layout bounds** (Android: Developer Options > Show layout bounds; iOS: no equivalent, use view hierarchy debugger)
2. **Measure each interactive element's touch target** — not just the visual icon size, but the clickable area
3. **Verify minimum size** — each target meets platform minimum (44pt iOS, 48dp Android)
4. **Verify spacing** — adjacent targets have adequate gap (8dp minimum per Material)
5. **Check for overlapping targets** — no two interactive elements share hit area
6. **Test with motor impairment simulation** — use larger touch area or switch device

### Touch Target Audit Checklist

- [ ] All buttons meet minimum touch target size (44x44pt iOS / 48x48dp Android)
- [ ] All list items have adequate touch target height
- [ ] All navigation tabs meet minimum target size
- [ ] All form field labels are tappable (expand hit area to label)
- [ ] Icons have adequate touch target (visual icon may be smaller, but hit area meets minimum)
- [ ] Adjacent targets have minimum 8dp/pt spacing
- [ ] No overlapping touch targets
- [ ] Small icon buttons (close, menu, back) have expanded hit areas
- [ ] Inline links in text have adequate line-height for touch targeting
- [ ] Gesture-based controls have single-pointer alternative (WCAG 2.5.1)

### Common Touch Target Defects

| Defect                                     | Severity | Fix Strategy                                              |
| ------------------------------------------ | -------- | --------------------------------------------------------- |
| Icon button with 24x24dp target            | P1       | Add padding/minimum width to expand to 48x48dp            |
| Two buttons with overlapping hit areas     | P1       | Increase spacing between buttons; reduce hit area padding |
| Inline links too close in paragraph text   | P2       | Increase line-height; add touch padding to links          |
| Small close icon (X) on modal dialog       | P1       | Expand touch area beyond visual icon to 44x44pt minimum   |
| List item tap requires precision           | P2       | Increase row height; add touch padding to entire row      |
| Swipe-only control with no tap alternative | P1       | Add single-tap or double-tap alternative                  |

---

## Color and Contrast Testing

Color and contrast testing ensures that text and UI elements are perceivable by users with low vision and various forms of color blindness.

### Contrast Ratio Requirements

| Content Type                             | Minimum Ratio | WCAG SC   | Notes                                                   |
| ---------------------------------------- | ------------- | --------- | ------------------------------------------------------- |
| Normal text (less than 18pt/14pt bold)   | 4.5 : 1       | 1.4.3 AA  | Most body text falls in this category                   |
| Large text (18pt+ or 14pt+ bold)         | 3 : 1         | 1.4.3 AA  | Headers, titles, and prominent labels                   |
| UI components and graphical objects      | 3 : 1         | 1.4.11 AA | Borders, icons, form field boundaries, chart elements   |
| Incidental/inactive elements             | Exempt        | 1.4.3     | Disabled text, decorative elements, logotypes           |
| Active user interface components (focus) | 3 : 1         | 2.4.7 AA  | Focus indicator must be visible against all backgrounds |

### Contrast Testing Procedure

1. **Identify all text elements** in the application (body text, headers, labels, buttons, links)
2. **Identify all UI components** that require contrast (icons, borders, form field outlines, dividers)
3. **Measure foreground/background color values** — use hex codes from design system or inspect rendered colors
4. **Calculate contrast ratio** — use a contrast checker tool (e.g., WebAIM, Colour Contrast Analyser)
5. **Compare against requirements** — 4.5:1 for normal text, 3:1 for large text and UI components
6. **Test on actual device screens** — calibrated display, not design tool color values
7. **Test in various lighting conditions** — indoor, outdoor, low-light

### Color Blindness Testing

Simulate the following types of color vision deficiency:

| Type              | Prevalence   | Affected Colors       | Testing Approach                                                         |
| ----------------- | ------------ | --------------------- | ------------------------------------------------------------------------ |
| **Protanopia**    | 1% of men    | Red weakness          | Use color blindness simulator; verify red elements still distinguishable |
| **Deuteranopia**  | 5% of men    | Green weakness        | Most common CVD; verify green elements distinguishable from background   |
| **Tritanopia**    | 0.01% of men | Blue weakness         | Verify blue/yellow distinctions                                          |
| **Achromatopsia** | 0.003%       | Total color blindness | Test in grayscale mode; all info must be perceivable                     |

### Color Information Testing Checklist

- [ ] Color is NOT the sole means of conveying information (WCAG 1.4.1)
- [ ] Error states use icon + color + text (not color alone)
- [ ] Required form fields indicated by asterisk or text (not red color alone)
- [ ] Success states use icon + color + text
- [ ] Charts/graphs use patterns, labels, or textures in addition to color
- [ ] Links are visually distinguishable from surrounding text (underline or other indicator)
- [ ] Status indicators combine color with icon/text/shape
- [ ] Form validation messages are perceivable without relying on color

### Contrast Audit Results Template

| Element             | Foreground | Background | Ratio  | Required | Pass/Fail | Notes          |
| ------------------- | ---------- | ---------- | ------ | -------- | --------- | -------------- |
| Body text           | #1A1A1A    | #FFFFFF    | 18.4:1 | 4.5:1    | PASS      |                |
| Secondary text      | #757575    | #FFFFFF    | 4.6:1  | 4.5:1    | PASS      | Borderline     |
| Disabled text       | #BDBDBD    | #FFFFFF    | 2.1:1  | Exempt   | N/A       | Disabled state |
| Primary button text | #FFFFFF    | #1976D2    | 4.5:1  | 4.5:1    | PASS      | Exact minimum  |
| Icon (inactive tab) | #9E9E9E    | #FFFFFF    | 2.9:1  | 3:1      | FAIL      | P2 defect      |
| Error message text  | #D32F2F    | #FFFFFF    | 5.4:1  | 4.5:1    | PASS      |                |
| Focus indicator     | #1976D2    | #FFFFFF    | 4.5:1  | 3:1      | PASS      |                |

---

## Dynamic Type Testing

Dynamic type (font scaling) testing ensures that the application remains usable when users increase or decrease the system font size.

### Platform Font Scaling

| Platform | Feature                  | Scaling Range   | Access Path                                         |
| -------- | ------------------------ | --------------- | --------------------------------------------------- |
| Android  | Display Size + Font Size | 0.85x to 2.0x+  | Settings > Accessibility > Font size / Display size |
| iOS      | Dynamic Type             | 0.5x to 5.0x+   | Settings > Accessibility > Display & Text Size      |
| Android  | Bold Text                | Weight increase | Settings > Accessibility > Bold text                |
| iOS      | Bold Text                | Weight increase | Settings > Accessibility > Display & Text Size      |

### Dynamic Type Testing Procedure

1. **Set system font size to maximum** (200%+ on Android, largest on iOS)
2. **Navigate through every screen** in the application
3. **Verify the following for each screen:**
   - [ ] All text remains readable at maximum scale
   - [ ] No text is clipped or truncated
   - [ ] No text overlaps with other elements
   - [ ] Content reflows vertically (no horizontal scrolling required)
   - [ ] All interactive elements remain accessible and tappable
   - [ ] Modal dialogs adapt to larger text
   - [ ] Navigation bars and toolbars accommodate larger text
   - [ ] Bottom navigation/tab bars remain usable
   - [ ] Forms remain usable with enlarged labels and input text
   - [ ] Images with embedded text remain legible or have alternatives
   - [ ] Lists adapt row height for larger content

### Text Spacing Requirements (WCAG 1.4.12)

When users override text spacing, the following must be supported without loss of content or functionality:

| Property          | Override Value  | Requirement                          |
| ----------------- | --------------- | ------------------------------------ |
| Line height       | 1.5x font size  | Lines must not overlap or clip       |
| Paragraph spacing | 2x font size    | Paragraphs must be visually distinct |
| Letter spacing    | 0.12x font size | Characters must not overlap          |
| Word spacing      | 0.16x font size | Words must not overlap               |

### Dynamic Type Defect Classification

| Defect                                          | Severity | Rationale                                          |
| ----------------------------------------------- | -------- | -------------------------------------------------- |
| Text clipped/truncated at 200% font size        | P1       | Content not perceivable; violates WCAG 1.4.4       |
| Horizontal scrolling required at 200%           | P1       | Layout does not reflow; violates WCAG 1.4.10       |
| Interactive elements unreachable at 200%        | P1       | Functionality lost; violates WCAG 1.4.4            |
| Text overlaps other elements at 200%            | P2       | Content perceivable but degraded; borderline P1    |
| Layout looks awkward but all content accessible | P3       | Cosmetic issue; all content and function preserved |
| Minor icon alignment shift at maximum font size | P3       | Cosmetic polish; no content or function loss       |

---

## Accessibility Scanner Tools

Automated and semi-automated tools identify accessibility issues that may be missed during manual testing.

### Android Accessibility Scanner

| Feature                    | Description                                           |
| -------------------------- | ----------------------------------------------------- |
| Touch target size          | Flags elements below 48x48dp minimum                  |
| Contrast                   | Measures foreground/background contrast ratio         |
| Content labeling           | Identifies images/buttons without contentDescription  |
| Clickable element labeling | Flags clickable elements missing contentDescription   |
| Implementation             | Install from Play Store; overlay scans current screen |

#### Using Android Accessibility Scanner

1. Install Android Accessibility Scanner from Google Play Store
2. Enable the service in Settings > Accessibility > Android Accessibility Scanner
3. Navigate to the screen to test in the target application
4. Tap the scanner floating action button
5. Review reported issues — tap each suggestion for details
6. Document findings in the accessibility audit report

### iOS Accessibility Inspector

| Feature             | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| Element inspection  | Hover over elements to see accessibility properties          |
| Traits verification | Verify label, traits, value, and hints                       |
| Color contrast      | Built-in contrast checker                                    |
| Smart invert        | Test inverted color rendering                                |
| Implementation      | Built into Xcode > Developer Tools > Accessibility Inspector |

#### Using iOS Accessibility Inspector

1. Launch Xcode > Developer Tools > Accessibility Inspector
2. Select the running application or device
3. Use the inspection pointer to hover over elements
4. Review accessibility properties: label, traits, value, hints
5. Use the contrast checker to verify color ratios
6. Document findings in the accessibility audit report

### Automated Audit Checklist

| Tool                          | Platform | Checks Performed                                         | Limitations                                     |
| ----------------------------- | -------- | -------------------------------------------------------- | ----------------------------------------------- |
| Android Accessibility Scanner | Android  | Touch target, contrast, content labels, clickable labels | Does not check reading order, logical structure |
| iOS Accessibility Inspector   | iOS      | Element properties, contrast, traits                     | Manual inspection required; not batch scanning  |
| Lint (accessibility checks)   | Android  | Missing contentDescription, labelFor, autofill hints     | Static analysis only; no runtime checking       |
| SwiftLint + SwiftLint rules   | iOS      | accessibilityLabel presence, trait checks                | Static analysis only; no runtime checking       |
| Espresso accessibility checks | Android  | Programmatic verification during automated tests         | Requires writing test code                      |
| XCTest accessibility checks   | iOS      | Programmatic verification during automated tests         | Requires writing test code                      |

### Scanner Findings Template

```markdown
## Accessibility Scanner Findings — [Screen Name]

**Date:** YYYY-MM-DD
**Tool:** [Android Accessibility Scanner / iOS Accessibility Inspector]
**Platform:** [Android / iOS] [Version]

| #   | Issue Type    | Element        | Detail                      | Severity | Status |
| --- | ------------- | -------------- | --------------------------- | -------- | ------ |
| 1   | Touch Target  | Close Icon     | 32x32dp, below 48dp minimum | P1       | Open   |
| 2   | Content Label | Settings Icon  | Missing contentDescription  | P1       | Open   |
| 3   | Contrast      | Secondary Text | 3.8:1, below 4.5:1 minimum  | P2       | Open   |
```

---

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

## Defect Classification for Accessibility

Accessibility defects are classified using the P0–P3 severity system aligned with the company's defect classification standard.

### Accessibility Defect Severity Table

| Level  | Definition                  | Accessibility Impact                                                                                | Release Impact                  | Examples                                                                                                                                                                                                                            |
| ------ | --------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **P0** | Complete barrier to access  | Core functionality entirely inaccessible to screen reader users or users with specific disabilities | Blocks release — non-negotiable | - Entire screen has no accessibility labels<br>- Form submission impossible without vision<br>- Security vulnerability exposing user data via accessibility API                                                                     |
| **P1** | Major accessibility barrier | Significant functionality degraded or confusing; workarounds exist but are non-trivial              | Blocks release — non-negotiable | - Touch targets below minimum size on critical buttons<br>- Contrast ratio below 3:1 on primary action buttons<br>- Screen reader navigation order makes screen unusable<br>- Dynamic type causes text clipping on critical content |
| **P2** | Minor accessibility barrier | Some functionality degraded but usable with effort                                                  | User decides to fix or defer    | - Secondary text contrast slightly below 4.5:1 (e.g., 4.0:1)<br>- Missing accessibility hints on non-critical elements<br>- Minor layout shift at maximum dynamic type that does not block access                                   |
| **P3** | Polish / enhancement        | Improves experience but does not block access                                                       | User decides to fix or defer    | - Accessibility announcement could be more descriptive<br>- Focus indicator could be more visible (but meets minimum)<br>- Minor inconsistency in announcement format                                                               |

### P0 Accessibility Defects (Non-Negotiable — Always Block Release)

| #   | Defect Description                                  | WCAG SC |
| --- | --------------------------------------------------- | ------- |
| 1   | Screen cannot be navigated via screen reader at all | 4.1.2   |
| 2   | Form submission requires vision                     | 1.1.1   |
| 3   | Critical action has no accessibility label          | 4.1.2   |
| 4   | Modal dialog does not trap focus                    | 2.4.3   |
| 5   | CAPTCHA with no accessible alternative              | 1.1.1   |

### P1 Accessibility Defects (Non-Negotiable — Always Block Release)

| #   | Defect Description                                                       | WCAG SC |
| --- | ------------------------------------------------------------------------ | ------- |
| 1   | Touch targets below 44x44pt (iOS) / 48x48dp (Android) on primary actions | 2.5.8   |
| 2   | Contrast ratio below 3:1 for UI components                               | 1.4.11  |
| 3   | Contrast ratio below 4.5:1 for body text                                 | 1.4.3   |
| 4   | Screen reader reading order is illogical/confusing                       | 1.3.2   |
| 5   | Text clipped or truncated at 200% font scaling                           | 1.4.4   |
| 6   | Color is the sole means of conveying critical information                | 1.4.1   |
| 7   | Gesture-only control with no single-pointer alternative                  | 2.5.1   |

### P2 Accessibility Defects (User Decides)

| #   | Defect Description                                                         | WCAG SC |
| --- | -------------------------------------------------------------------------- | ------- |
| 1   | Contrast ratio slightly below threshold (4.0:1 vs 4.5:1) on secondary text | 1.4.3   |
| 2   | Missing accessibility hints on non-critical elements                       | 4.1.2   |
| 3   | Minor layout issues at maximum dynamic type                                | 1.4.4   |
| 4   | Inconsistent announcement format across screens                            | 4.1.2   |
| 5   | Focus indicator meets minimum but could be more visible                    | 2.4.7   |

### P3 Accessibility Defects (User Decides)

| #   | Defect Description                                   | WCAG SC |
| --- | ---------------------------------------------------- | ------- |
| 1   | Accessibility announcement could be more descriptive | N/A     |
| 2   | Minor inconsistency in trait reporting               | N/A     |
| 3   | Polish improvement for VoiceOver/TalkBack experience | N/A     |

---

## Stage 7 and Stage 8 Integration

Accessibility testing is a required component of Stage 7 (Automated Testing) and Stage 8 (Integrity Verification).

### Stage 7 — Automated Testing Requirements

| Requirement                    | Description                                                                |
| ------------------------------ | -------------------------------------------------------------------------- |
| Automated accessibility checks | Espresso and XCTest accessibility checks must pass in the test suite       |
| Screen reader manual testing   | TalkBack and VoiceOver testing completed on all user-facing screens        |
| Contrast audit                 | All text and UI elements measured and documented                           |
| Touch target audit             | All interactive elements verified against platform minimums                |
| Dynamic type testing           | Application tested at 200%+ font scaling on all screens                    |
| Defect reporting               | All accessibility defects classified (P0–P3) and included in Defect Report |
| Automated check pass rate      | 100% of automated accessibility checks must pass for Stage 7 sign-off      |

### Stage 8 — Integrity Verification

| Panel Member | Accessibility Verification Responsibility                        |
| ------------ | ---------------------------------------------------------------- |
| CTO          | Confirm all automated accessibility checks pass                  |
| CSO          | Verify accessibility does not introduce security vulnerabilities |
| CDO          | Confirm design specifications meet accessibility requirements    |
| CPO          | Confirm PRD accessibility requirements are satisfied             |

### Accessibility Gate Criteria Summary

| Stage | Accessibility Gate Criteria                                                            | Sign-off        |
| ----- | -------------------------------------------------------------------------------------- | --------------- |
| 7     | All automated accessibility checks pass; all manual tests documented; defects reported | CTO + Test Lead |
| 8     | No P0/P1 accessibility defects outstanding; P2/P3 presented to user for decision       | CTO Panel       |
| 10    | Accessibility verified as part of full release checklist; platform requirements met    | CTO + User      |

### Platform-Specific Accessibility Requirements

| Platform | Requirement                                      | Standard                                             |
| -------- | ------------------------------------------------ | ---------------------------------------------------- |
| Android  | Play Store accessibility compliance              | Google Play Developer Policy (accessibility section) |
| iOS      | App Store Review Guideline 5.1.1 (Accessibility) | Apple App Store Review Guidelines                    |
| Both     | WCAG 2.1 AA equivalent for mobile                | Industry best practice; referenced in regulations    |

---

## Accessibility Audit Checklist

### Pre-Audit Preparation

- [ ] Identify all screens/screens flows to audit
- [ ] Prepare test devices (Android with TalkBack, iOS with VoiceOver)
- [ ] Install accessibility scanner tools
- [ ] Prepare contrast checking tools
- [ ] Prepare font scaling test scenarios
- [ ] Prepare color blindness simulation tools

### Screen Reader Audit

- [ ] All screens navigable via TalkBack
- [ ] All screens navigable via VoiceOver
- [ ] All interactive elements have meaningful labels
- [ ] Reading order is logical and matches visual order
- [ ] All element roles/types are correctly announced
- [ ] State changes are announced (checked/unchecked, expanded/collapsed)
- [ ] Focus management is correct on modal/dialog open/close
- [ ] Images have appropriate descriptions or are hidden
- [ ] Status messages are announced
- [ ] No dead ends or focus traps (except intentional modal traps)

### Touch Target Audit

- [ ] All touch targets meet minimum size (44x44pt iOS / 48x48dp Android)
- [ ] No overlapping touch targets
- [ ] Adequate spacing between adjacent targets
- [ ] All small icon buttons have expanded hit areas

### Contrast Audit

- [ ] All normal text meets 4.5:1 contrast ratio
- [ ] All large text meets 3:1 contrast ratio
- [ ] All UI components meet 3:1 contrast ratio
- [ ] Focus indicators are visible against all backgrounds
- [ ] Color is not the sole means of conveying information

### Dynamic Type Audit

- [ ] All text readable at maximum font scaling
- [ ] No text clipped or truncated
- [ ] No horizontal scrolling at 200% font size
- [ ] All interactive elements accessible at maximum font scaling
- [ ] Layout adapts gracefully

### Automated Testing

- [ ] Espresso accessibility checks integrated and passing
- [ ] XCTest accessibility checks integrated and passing
- [ ] Lint checks configured for accessibility
- [ ] CI/CD pipeline includes accessibility checks

---

## References

| Document                             | Source                                                                      |
| ------------------------------------ | --------------------------------------------------------------------------- |
| WCAG 2.1 Guidelines                  | https://www.w3.org/TR/WCAG21/                                               |
| WCAG 2.2 Guidelines                  | https://www.w3.org/TR/WCAG22/                                               |
| Understanding WCAG 2.1               | https://www.w3.org/WAI/WCAG21/Understanding/                                |
| Mobile Accessibility                 | https://www.w3.org/WAI/standards-guidelines/mobile/                         |
| Apple Accessibility Guidelines       | https://developer.apple.com/design/human-interface-guidelines/accessibility |
| Google Material Design Accessibility | https://m3.material.io/foundations/accessible-design                        |
| Android Accessibility Documentation  | https://developer.android.com/guide/topics/ui/accessibility                 |
| iOS Accessibility Documentation      | https://developer.apple.com/accessibility/                                  |
| Section 508 Standards                | https://www.section508.gov/                                                 |
| EN 301 549 Standard                  | https://www.etsi.org/deliver/etsi_en/301500_301599/301549/                  |
