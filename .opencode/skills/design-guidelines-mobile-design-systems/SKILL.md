---
name: design-guidelines-mobile-design-systems
description: Mobile design system creation for iOS and Android — platform-specific component libraries (iOS HIG, Android Material Design), interaction patterns, design tokens, accessibility standards (WCAG 2.1 AA), and design-to-production workflow. Owned by Yuki Tanaka-Chen (CDO). Use during Stage 2 (Prototype) for mobile design system creation and Stage 5 (Development) for design token implementation. Trigger: mobile design system, iOS design system, Android design system, Material Design, HIG components, design tokens mobile.
prerequisites:
  - design-overview

version: "1.0.0"
---

# Mobile Design Systems

## Purpose

Build comprehensive, platform-native design systems that enable consistent, high-quality mobile experiences across iOS and Android while respecting platform conventions and maintaining brand identity.

## When to Use

- Creating a new design system from scratch
- Extending an existing design system with mobile components
- Defining platform-specific interaction patterns
- Establishing design tokens and theming architecture
- Setting accessibility standards for mobile products

## Core Principles

1. **Platform respect over brand dogma** — iOS and Android have distinct interaction paradigms. A great mobile design system adapts to platform conventions rather than forcing a single cross-platform aesthetic.

2. **Component specifications, not just visuals** — Every component needs interaction specs, state definitions, accessibility requirements, and implementation notes — not just pretty Figma frames.

3. **Design tokens as the foundation** — Color, typography, spacing, and motion should be tokenized and platform-specific (iOS uses SF Pro, Android uses Roboto; iOS uses 8pt grid, Android uses 4dp grid).

4. **Accessibility as a requirement, not an afterthought** — Every component must meet WCAG 2.1 AA, support VoiceOver/TalkBack, and define focus states and touch target sizes.

## Design System Structure

### 1. Foundation Layer

**Design Tokens:**

- Colors (semantic tokens: primary, secondary, error, surface, etc.)
- Typography (platform-specific: SF Pro for iOS, Roboto for Android)
- Spacing scale (iOS: 4, 8, 16, 24, 32, 48; Android: 4dp, 8dp, 16dp, 24dp, 32dp)
- Corner radius (iOS: 8, 12, 16; Android: 4dp, 8dp, 16dp)
- Elevation/shadows (iOS: subtle shadows; Android: Material elevation)
- Motion curves (iOS: ease-in-out; Android: Material motion)

**Platform Conventions:**

- iOS: Navigation bars, tab bars, modal sheets, swipe gestures
- Android: App bars, bottom navigation, FABs, Material motion

### 2. Component Library

For each component, document:

**Visual Specifications:**

- Default, hover, pressed, disabled, error states
- Light and dark mode variants
- Responsive behavior across screen sizes

**Interaction Specifications:**

- Tap targets (minimum 44x44pt iOS, 48x48dp Android)
- Gesture support (swipe, long-press, pinch)
- Haptic feedback (iOS: UIImpactFeedbackGenerator; Android: HapticFeedbackConstants)
- Animation timing and curves

**Accessibility Requirements:**

- VoiceOver/TalkBack labels and hints
- Dynamic Type/Font scaling support
- Color contrast ratios (4.5:1 for text, 3:1 for UI elements)
- Focus indicators and keyboard navigation

**Implementation Notes:**

- iOS: UIKit/SwiftUI component mapping
- Android: Jetpack Compose/View system mapping
- Edge cases and error states

### 3. Pattern Library

**Navigation Patterns:**

- iOS: Push navigation, modal presentation, tab switching
- Android: Fragment navigation, bottom sheets, drawer navigation

**Gesture Vocabularies:**

- iOS: Swipe back, pull to refresh, long-press context menus
- Android: Swipe to dismiss, FAB expansion, bottom sheet drag

**Form Patterns:**

- Input validation and error messaging
- Keyboard management and input accessories
- Autofill and password management integration

## Deliverable Format

### Component Specification Template

```
# [Component Name]

## Overview
[1-2 sentence description of purpose]

## Variants
- Default
- [List all variants: sizes, states, platform differences]

## Visual Specs
- iOS: [Figma link, dimensions, spacing]
- Android: [Figma link, dimensions, spacing]

## Interaction Specs
- Tap target: [size]
- Gestures: [supported gestures]
- Haptics: [when to trigger]
- Animation: [duration, curve, properties]

## States
| State | Visual | Interaction | Accessibility |
|-------|--------|-------------|---------------|
| Default | [description] | [behavior] | [label/hint] |
| Pressed | [description] | [behavior] | [label/hint] |
| Disabled | [description] | [behavior] | [label/hint] |
| Error | [description] | [behavior] | [label/hint] |

## Accessibility
- VoiceOver/TalkBack: [label, hint, traits]
- Dynamic Type: [scaling behavior]
- Color contrast: [ratios]
- Focus: [indicator style]

## Implementation Notes
- iOS: [UIKit/SwiftUI code reference]
- Android: [Compose/View code reference]
- Edge cases: [list known issues]

## Usage Guidelines
- When to use: [scenarios]
- When NOT to use: [anti-patterns]
```

## Quality Checklist

Before shipping a design system component:

- [ ] Platform-specific variants defined (iOS ≠ Android)
- [ ] All states documented (default, pressed, disabled, error, loading)
- [ ] Light and dark mode variants
- [ ] Accessibility requirements specified (VoiceOver/TalkBack, Dynamic Type, contrast)
- [ ] Interaction specs complete (tap targets, gestures, haptics, animations)
- [ ] Implementation notes for engineers (UIKit/SwiftUI, Compose/View)
- [ ] Edge cases identified and documented
- [ ] Usage guidelines and anti-patterns listed
- [ ] Figma components match specifications exactly

## Collaboration Protocol

1. **Kickoff with Product and Engineering** — Understand product requirements, technical constraints, and platform capabilities before designing
2. **Draft component specs** — Create visual and interaction specifications with platform-specific variants
3. **Review with Engineering** — Validate implementation feasibility, adjust for technical constraints
4. **Prototype and test** — Build interactive prototypes, run usability tests with accessibility tools enabled
5. **Finalize and document** — Lock specifications, create Figma components, write implementation guides
6. **Ship and iterate** — Monitor adoption, gather feedback, refine based on real-world usage

## Anti-Patterns to Avoid

- **Cross-platform sameness** — Don't force iOS and Android to look identical; respect platform conventions
- **Visual-only specs** — Don't ship Figma files without interaction, accessibility, and implementation notes
- **Accessibility as optional** — Don't treat VoiceOver/TalkBack as "nice to have"; it's a requirement
- **Token-free designs** — Don't hard-code colors and spacing; use semantic tokens
- **Spec-less handoffs** — Don't throw designs over the wall; collaborate with engineers throughout
