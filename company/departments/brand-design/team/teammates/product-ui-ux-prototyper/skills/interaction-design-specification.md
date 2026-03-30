---
name: interaction-design-specification
description: Authorship of the Interaction Design Specification (IDS) — the governing document for native mobile interaction behaviour. Covers component trees, gesture vocabularies, state diagrams, edge case matrices, and platform-specific interaction patterns for iOS HIG and Android Material Design 3.
---

# Interaction Design Specification (IDS)

## Purpose

The IDS is the governing document for native mobile interaction behaviour. It is produced after the web prototype is approved and user confirmation is received. The web prototype validates functional requirements and design style; the IDS governs how those interactions are implemented natively on iOS and Android.

The IDS is delivered to the R&D Department and the CTO alongside the approved web prototype HTML file.

## IDS Structure

### 1. Component Tree

For every screen in the prototype:

- List all UI components in hierarchical order (screen → section → component → sub-component)
- Annotate each component with: component type, platform variant (iOS / Android / shared), and data source

### 2. Gesture Vocabulary

For every interactive component:

| Gesture | Platform | Component | Behaviour | Animation |
|---|---|---|---|---|
| Tap | iOS + Android | [component name] | [what happens] | [duration, easing] |
| Swipe left | iOS | [component name] | [what happens] | [duration, easing] |
| Long press | Android | [component name] | [what happens] | [duration, easing] |
| Pinch | iOS + Android | [component name] | [what happens] | [duration, easing] |

Document every gesture. No gesture left undocumented.

### 3. State Diagrams

For every component with multiple states:

- List all states: default, loading, error, empty, success, disabled, focused, pressed
- Define transition trigger (user action or system event) for each state change
- Define transition animation (type, duration, easing) for each state change
- Define edge conditions: what happens if state changes mid-transition?

### 4. Edge Case Matrix

For every user flow:

| Flow | Happy Path | Edge Case | Expected Behaviour | Error Handling |
|---|---|---|---|---|
| [flow name] | [normal input] | [edge input] | [expected] | [error state] |

Cover at minimum: no network, partial data, empty states, maximum data (truncation), concurrent actions, interruption (phone call, background).

### 5. Platform-Specific Interaction Patterns

#### iOS (Human Interface Guidelines)

- Navigation: specify navigation stack depth, swipe-back gesture regions, modal vs push presentation
- Bottom sheets: detent heights, dismissal gestures, keyboard avoidance
- Dynamic Type: minimum/maximum text sizes for all text elements
- Safe areas: insets respected on all screens
- App Store interaction constraints: no custom back button override, no hiding system chrome without justification

#### Android (Material Design 3)

- Navigation: bottom nav bar vs navigation rail threshold, predictive back gesture handling
- Adaptive layouts: compact / medium / expanded breakpoint behaviour
- Elevation and tonal colour: surface tint levels for overlapping surfaces
- Motion: specify Material motion system tokens (emphasized, emphasized decelerate, emphasized accelerate, standard)
- Google Play interaction constraints: back gesture always dismisses, no custom gesture conflicts with system gestures

### 6. Accessibility Annotations

For every interactive component:

- VoiceOver (iOS) and TalkBack (Android) label
- Minimum touch target size (44×44pt iOS, 48×48dp Android)
- Focus order for keyboard/switch navigation
- Colour contrast ratio (WCAG 2.1 AA minimum: 4.5:1 text, 3:1 UI components)

## Delivery

The completed IDS is delivered as a markdown document alongside the approved prototype HTML file. Both artifacts are archived together before handoff to R&D.

File name: `IDS-v{n}-{product-slug}.md`
