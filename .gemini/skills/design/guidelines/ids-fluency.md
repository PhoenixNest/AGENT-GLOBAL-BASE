---
name: ids-fluency
description: This skill ensures all engineers and reviewers can read, interpret, and correctly implement from the Interaction Design Specification (IDS) produced at Stage 2 by the CDO.
---

# Interaction Design Specification Fluency

## Purpose

This skill ensures all engineers and reviewers can read, interpret, and correctly implement from the Interaction Design Specification (IDS) produced at Stage 2 by the CDO. IDS fluency prevents the common failure mode of engineers ignoring or misinterpreting interaction specifications, leading to UX defects at Stage 6 Code Review and Stage 8 Integrity Verification. It is used by the CTO, platform leads, and all engineering personnel.

## Execution Guidance

### 1. IDS Document Structure

The IDS produced by the CDO at Stage 2 contains:

| Section                        | Content                                                  | Engineering Relevance                                                       |
| ------------------------------ | -------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Interaction Flows**          | Step-by-step user journey diagrams and descriptions      | Implement navigation logic and state transitions                            |
| **Component Behaviors**        | Animation specs, timing curves, gesture responses        | Implement UI components with exact motion behavior                          |
| **State Definitions**          | Loading, error, empty, success states for each screen    | Implement all states — not just the happy path                              |
| **Accessibility Requirements** | Screen reader labels, focus order, minimum touch targets | Implement WCAG 2.1 AA compliance per screen                                 |
| **Responsive Breakpoints**     | Layout adaptation rules for different screen sizes       | Implement responsive/adaptive layouts                                       |
| **Design Tokens**              | Color, typography, spacing, elevation values             | Map to platform-specific token systems (Android themes, iOS asset catalogs) |

### 2. Reading an IDS as an Engineer

**Step 1 — Identify affected screens**: Map each IDS screen to your platform's view hierarchy (Android Activities/Fragments/Composables, iOS ViewControllers/SwiftUI Views).

**Step 2 — Extract interaction requirements**: For each screen, note:

- What gestures are supported (tap, swipe, long-press, pull-to-refresh)?
- What animations occur (enter/exit transitions, state change animations)?
- What are the timing specifications (duration, easing curves)?

**Step 3 — Identify all states**: Every screen has at minimum: loading, loaded, error, and empty states. The IDS specifies each one. Implement all of them.

**Step 4 — Map accessibility requirements**: Each IDS element has accessibility metadata. Implement content descriptions, accessibility labels, and focus management.

### 3. IDS-to-Implementation Traceability

Maintain a traceability matrix linking IDS elements to implementation:

```
IDS Element ID → Platform Component → Implementation File → Test Coverage
IDS-SCR-001 → MainActivity.kt → ui/screens/HomeScreen.kt → HomeScreenTest.kt
IDS-ANIM-003 → SharedElementTransition → animations/CardExpandAnimation.kt → (visual test)
```

### 4. Common IDS Misinterpretations to Avoid

- **Ignoring animation specs**: "It works without animation" is a defect. Animation timing and easing curves are requirements.
- **Missing error states**: Engineers often implement only the happy path. The IDS specifies error states for every interaction.
- **Incorrect touch targets**: Minimum 44x44pt (iOS) / 48x48dp (Android). Smaller targets are accessibility defects.
- **Not implementing focus order**: Screen reader navigation follows the IDS focus order. Visual order ≠ focus order.

### 5. IDS Review Checklist (Stage 6 & 8)

When reviewing code against the IDS:

- [ ] All screens in IDS are implemented
- [ ] All interaction flows match IDS specifications
- [ ] All animations have correct duration and easing curves
- [ ] All states (loading, error, empty, success) are implemented
- [ ] All accessibility labels and descriptions are present
- [ ] Touch targets meet minimum size requirements
- [ ] Focus order matches IDS specification
- [ ] Responsive breakpoints match IDS specification

## Reference Materials

- Stage 2 IDS output from CDO
- WCAG 2.1 AA mobile guidelines
- Platform accessibility guidelines (Android Accessibility, iOS VoiceOver)
- Company design token documentation
