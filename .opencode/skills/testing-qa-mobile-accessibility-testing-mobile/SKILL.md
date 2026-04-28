---
name: testing-qa-mobile-accessibility-testing-mobile
description: Mobile accessibility testing — WCAG 2.1 AA compliance for iOS and Android, VoiceOver/TalkBack screen reader testing, Dynamic Type/font scaling validation, color contrast analysis, and accessibility defect classification (P0–P3). Owned by Priscilla Oduya (Test Lead). Use during Stage 7 (Testing) for accessibility audit execution and Stage 10 (Release Readiness) for accessibility compliance sign-off. Trigger: accessibility testing, WCAG 2.1 AA, VoiceOver, TalkBack, screen reader testing, Dynamic Type, font scaling, color contrast, mobile accessibility.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
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


---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`color-and-contrast-testing.md`](references/color-and-contrast-testing.md) — Color and Contrast Testing
- [`dynamic-type-testing.md`](references/dynamic-type-testing.md) — Dynamic Type Testing
- [`accessibility-scanner-tools.md`](references/accessibility-scanner-tools.md) — Accessibility Scanner Tools
- [`automated-accessibility-testing.md`](references/automated-accessibility-testing.md) — Automated Accessibility Testing
- [`defect-classification-for-accessibility.md`](references/defect-classification-for-accessibility.md) — Defect Classification for Accessibility
- [`stage-7-and-stage-8-integration.md`](references/stage-7-and-stage-8-integration.md) — Stage 7 and Stage 8 Integration
- [`accessibility-audit-checklist.md`](references/accessibility-audit-checklist.md) — Accessibility Audit Checklist
- [`references.md`](references/references.md) — References
```
