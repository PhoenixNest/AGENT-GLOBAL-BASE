---
name: wcag-mobile-roadmap
description: This skill provides a roadmap for achieving WCAG 2.1 AA compliance in mobile applications, covering the specific success criteria that apply to mobile platforms.
---

# WCAG 2.1 AA Mobile Compliance Roadmap

## Purpose

This skill provides a roadmap for achieving WCAG 2.1 AA compliance in mobile applications, covering the specific success criteria that apply to mobile platforms, implementation strategies for Android and iOS, and verification methods. It is used by the Accessibility Lead (Jordan Rivera), CDO, platform leads, and the Stage 8 Integrity Verification panel.

## Execution Guidance

### 1. WCAG 2.1 AA — Mobile-Relevant Success Criteria

Not all 50 WCAG 2.1 AA success criteria apply to mobile. The following are the most relevant:

| SC #   | Criterion              | Mobile Implementation                                               |
| ------ | ---------------------- | ------------------------------------------------------------------- |
| 1.1.1  | Non-text Content       | Content descriptions for all images, icons, and custom UI elements  |
| 1.3.1  | Info and Relationships | Semantic UI components, proper heading structure, ARIA labels       |
| 1.3.2  | Meaningful Sequence    | Logical reading order matches visual order                          |
| 1.3.4  | Orientation            | Content does not lock to portrait or landscape (unless essential)   |
| 1.3.5  | Identify Input Purpose | Input fields have autocomplete attributes for common data types     |
| 1.4.1  | Use of Color           | Information is not conveyed by color alone                          |
| 1.4.3  | Contrast (Minimum)     | Text contrast ratio ≥ 4.5:1, large text ≥ 3:1, UI components ≥ 3:1  |
| 1.4.4  | Resize Text            | Text can be scaled to 200% without loss of content or functionality |
| 1.4.10 | Reflow                 | Content reflows at 320px equivalent without horizontal scrolling    |
| 1.4.12 | Text Spacing           | Users can override text spacing without breaking layout             |
| 2.1.1  | Keyboard (Pointer)     | All functionality operable via external keyboard/pointer            |
| 2.4.3  | Focus Order            | Focus order preserves meaning and operability                       |
| 2.4.7  | Focus Visible          | Keyboard focus indicator is visible                                 |
| 2.5.1  | Pointer Gestures       | All multipoint gestures have single-pointer alternatives            |
| 2.5.2  | Pointer Cancellation   | No unintended actions on down-event                                 |
| 2.5.3  | Label in Name          | Visible text matches accessible name                                |
| 2.5.4  | Motion Actuation       | Motion-based input can be disabled; alternative provided            |
| 2.5.5  | Target Size            | Touch targets ≥ 44×44 CSS pixels (AAA, but recommended)             |
| 2.5.7  | Dragging Movements     | Dragging has pointer-based alternative (AA, 2.2)                    |
| 3.2.6  | Consistent Help        | Help mechanisms appear in consistent locations                      |
| 4.1.2  | Name, Role, Value      | All UI components have accessible name and role                     |

### 2. Platform Implementation Guide

**Android**:

```kotlin
// Content descriptions
imageView.contentDescription = getString(R.string.cd_profile_photo)

// Touch target size (minimum 48x48dp)
<Button
    android:layout_width="48dp"
    android:layout_height="48dp"
    android:minWidth="48dp"
    android:minHeight="48dp" />

// Focus order (important in Compose)
ComposeLayout {
    Column {
        Text("Title", modifier = Modifier.semantics { heading() })
        Button(onClick = { /* ... */ },
               modifier = Modifier.semantics { contentDescription = "Submit form" })
    }
}

// Text scaling (use sp, not dp for text)
Text(text = "Hello", fontSize = 16.sp)

// Color contrast (verify with Accessibility Scanner)
// Use Material Theme colors that meet 4.5:1 ratio
```

**iOS**:

```swift
// Content descriptions / accessibility labels
imageView.accessibilityLabel = NSLocalizedString("Profile photo", comment: "")
imageView.isAccessibilityElement = true

// Touch target size (minimum 44x44pt)
Button(action: { /* ... */ }) {
    Image(systemName: "plus")
        .frame(minWidth: 44, minHeight: 44)
}

// Dynamic Type (text scaling)
Text("Hello").font(.body) // Automatically scales with Dynamic Type
// Or custom: Text("Hello").font(.custom("Helvetica", size: 16, relativeTo: .body))

// VoiceOver focus order
VStack {
    Text("Title").accessibilityAddTraits(.isHeader)
    Button("Submit") { /* ... */ }
    // Order in VStack = VoiceOver order
}

// Reduce Motion support
@Environment(\.accessibilityReduceMotion) var reduceMotion
if reduceMotion {
    // Skip animations
} else {
    // Play animations
}
```

### 3. Compliance Verification Process

**Phase 1 — Automated testing (Stage 5)**:

- Run axe-core or platform-equivalent tools in CI pipeline.
- Automated tools catch ~57% of WCAG 2.1 AA violations.
- Fix all automated findings before proceeding to manual testing.

**Phase 2 — Manual testing (Stage 7)**:

- **Screen reader testing**: Navigate every screen using VoiceOver (iOS) and TalkBack (Android).
  - Can you understand every element's purpose from its label?
  - Can you complete every critical task using only the screen reader?
  - Is the reading order logical?
- **Text scaling**: Set device font to largest setting (200%). Verify no content loss, overlap, or truncation.
- **Touch target verification**: Measure all interactive elements with Accessibility Scanner (Android) or Accessibility Inspector (iOS).
- **Color contrast**: Verify all text and UI component contrast ratios.

**Phase 3 — Compliance report (Stage 8)**:

- Produce an accessibility compliance matrix mapping each WCAG 2.1 AA criterion to implementation status (Pass/Fail/Not Applicable).
- Document any known gaps with remediation plans and timelines.
- Include results from both automated and manual testing.

### 4. Common Mobile Accessibility Pitfalls

| Pitfall                                        | WCAG Criterion | Fix                                                     |
| ---------------------------------------------- | -------------- | ------------------------------------------------------- |
| Custom components without accessibility labels | 4.1.2          | Implement accessibility properties on custom components |
| Swipe gestures without alternatives            | 2.5.1          | Add button alternatives for swipe actions               |
| PDF content in app                             | 1.1.1, 1.3.1   | Provide accessible PDF or HTML alternative              |
| Video without captions                         | 1.2.2          | Provide captions for all video content                  |
| Color-only error states                        | 1.4.1          | Add text/icon alongside color change                    |
| Small touch targets                            | 2.5.5          | Increase minimum target to 44x44pt/48x48dp              |
| Fixed text size                                | 1.4.4          | Use scalable fonts (sp on Android, Dynamic Type on iOS) |
| Auto-playing media                             | 1.4.2          | Provide pause/stop controls                             |

### 5. Accessibility in the Design System

The design system (managed by the CDO) must bake accessibility in from the start:

- Every component specification includes accessibility properties (labels, roles, traits).
- Color palette is validated for contrast compliance before use.
- Touch target sizes are enforced in component implementations.
- Animation specifications include "reduce motion" alternatives.
- Typography scale supports Dynamic Type / scalable text.

## Reference Materials

- WCAG 2.1 AA official specification (w3.org/TR/WCAG21)
- W3C WAI — Mobile Accessibility Mapping
- Google Android Accessibility documentation
- Apple iOS Accessibility Programming Guide
- axe-core WCAG testing tool
- Company accessibility testing strategy
