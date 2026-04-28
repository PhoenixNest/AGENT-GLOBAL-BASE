# Game Interaction Design Specification (IDS) Template

> **Audit Condition 2 Remediation:** "Before Stage 2 (Prototype) begins, Marco Bellini must produce a Game IDS template covering animation specs, UI interaction flows, and platform-native meta-UI patterns."
>
> **Status:** ✅ ADDRESSED — This template is authored and frozen as the authoritative IDS structure for all casual game projects under `studio/casual-games/`.
>
> **Author:** Yuki Tanaka-Chen (CDO), with Marco Bellini (Motion/UI Animator), Elena Morozova (UI Visual Artist), Mei Watanabe (Lead Game Designer)
>
> **Version:** 1.0
> **Date:** 2026-04-12
> **Review Status:** CDO-approved, ready for project use

---

## 1. Executive Summary

This document establishes the **Game Interaction Design Specification (IDS) Template** — a standardized framework for documenting all game UI/UX interactions before Stage 2 (Prototype) begins. It was authored in direct response to a CDO audit finding that no game-specific IDS template existed for the casual games studio.

### Purpose

- Provide a **repeatable, project-agnostic IDS structure** that any game team can populate with project-specific content
- Ensure **animation specs, UI interaction flows, and platform-native meta-UI patterns** are defined before prototype development begins
- Serve as the **conformance baseline** for Stage 6 Code Review and Stage 8 Integrity Verification
- Enable **cross-platform consistency** while respecting iOS HIG and Android Material Design conventions

### Scope

This template covers:

- Game canvas interactions (core gameplay UI)
- Meta-UI overlays (settings, store, leaderboards, notifications)
- Animation and motion design specifications
- Gesture vocabulary and input handling
- Edge case handling and responsive behavior
- Accessibility requirements

### Out of Scope

- Backend service architecture (owned by CTO)
- Audio design specifications (owned by Audio Director)
- Marketing/ASO assets (owned by Product Marketing)

---

## 2. IDS Document Structure

Every project-specific IDS must include the following sections. This template provides the structure; project teams fill in the content.

### 2.1 Document Metadata

| Field          | Value                                   |
| -------------- | --------------------------------------- |
| **Project**    | `[Game Title]`                          |
| **Document**   | Game Interaction Design Specification   |
| **Version**    | `v{N}`                                  |
| **Authors**    | `[List of contributing designers]`      |
| **CDO Review** | `[Date]`                                |
| **Status**     | `Draft / In Review / Approved / Frozen` |
| **Stage**      | `2 (Design)`                            |
| **Platform**   | `iOS / Android / Both`                  |

### 2.2 Design Principles

Every game interaction must be evaluated against these principles:

| Principle                  | Description                                                                                                   | Metric                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| **Session Length**         | Core gameplay loops target `[X]` seconds per session with natural pause points                                | Average session duration           |
| **Zero-Tutorial Ideal**    | First-time users achieve core action within `[X]` seconds without explicit tutorial                           | Time-to-first-successful-action    |
| **Juice**                  | Every player input produces visible, satisfying feedback (screen shake, particle burst, sound, haptic)        | Subjective playtest rating ≥ 4/5   |
| **Failure Feel**           | Failure states communicate clearly, feel fair, and invite immediate retry (no dead ends, no blame)            | Retry rate within 3 seconds ≥ 80%  |
| **Progressive Disclosure** | Complexity reveals over time; initial screen shows only essential controls                                    | New-user confusion score ≤ 2/10    |
| **Platform Respect**       | Meta-UI (settings, store, nav) follows platform conventions; game canvas is brand-consistent across platforms | Platform guideline compliance 100% |

### 2.3 Platform Conventions

| Domain          | iOS (Human Interface Guidelines)                     | Android (Material Design 3)                  |
| --------------- | ---------------------------------------------------- | -------------------------------------------- |
| **Navigation**  | Tab bar (bottom), navigation bar (top), back gesture | Navigation drawer or bottom nav, system back |
| **Typography**  | SF Pro (system font), Dynamic Type support           | Roboto / Google Sans, scalable text          |
| **Color**       | System semantic colors, Dark Mode native             | Material color roles, Dark theme native      |
| **Iconography** | SF Symbols (preferred)                               | Material Icons (preferred)                   |
| **Haptics**     | Core Haptics (custom patterns)                       | Haptic Feedback Manager (standard patterns)  |
| **Gestures**    | Swipe from left edge = back                          | System gesture navigation (Android 10+)      |
| **Status Bar**  | Status bar visible, content respects safe area       | Edge-to-edge, content behind status/nav bars |
| **Dialogs**     | UIKit UIAlertController style                        | Material AlertDialog style                   |

### 2.4 Accessibility Requirements

| Category            | Requirement                                                                                     | Standard    |
| ------------------- | ----------------------------------------------------------------------------------------------- | ----------- |
| **Colorblind Mode** | All critical information conveyed through shape/pattern + color; colorblind-safe palette        | WCAG 2.1 AA |
| **Motor**           | Tap targets ≥ 44×44pt (iOS) / 48×48dp (Android); no time-critical gestures without alternatives | WCAG 2.1 AA |
| **Cognitive**       | Clear visual hierarchy; consistent interaction patterns; no ambiguous states                    | WCAG 2.1 AA |
| **Screen Reader**   | All interactive elements have VoiceOver/TalkBack labels; logical focus order                    | WCAG 2.1 AA |
| **Reduced Motion**  | All animations have reduced-motion alternative (skip or simplify)                               | WCAG 2.1 AA |
| **Text Scaling**    | UI supports Dynamic Type (iOS) / scalable text (Android) up to 200% without layout break        | WCAG 2.1 AA |

---

## 3. Component Specification Template

Every UI component in the game must be documented using this template. Duplicate this section for each component.

### Component: `[Component Name]`

#### 3.1 Purpose

> What does this component do? Where does it appear? What user need does it serve?

#### 3.2 States

| State    | Description             | Visual Treatment | Trigger                         |
| -------- | ----------------------- | ---------------- | ------------------------------- |
| Default  | Resting state           |                  | Component rendered              |
| Hover    | Pointer/focus hover     |                  | Pointer enters bounds (iPad)    |
| Pressed  | Active touch state      |                  | Finger down on component        |
| Disabled | Non-interactive state   |                  | Condition not met               |
| Loading  | Async operation pending |                  | Network/data request in flight  |
| Error    | Operation failed        |                  | Request error / validation fail |
| Success  | Operation completed     |                  | Request success                 |

#### 3.3 Visual Specification

| Property      | Value                                  |
| ------------- | -------------------------------------- |
| Dimensions    | `[Width] × [Height]` (pt/dp)           |
| Corner Radius | `[X]` pt/dp                            |
| Typography    | `[Font Family] [Weight] [Size]`        |
| Color (Light) | `[Hex / Token Name]`                   |
| Color (Dark)  | `[Hex / Token Name]`                   |
| Iconography   | `[SF Symbol / Material Icon name]`     |
| Elevation     | `[Shadow spec / elevation value]`      |
| Spacing       | `[Internal padding, external margins]` |

#### 3.4 Interaction Specification

| Property        | Value                                      |
| --------------- | ------------------------------------------ |
| Tap Target Size | `≥ 44×44pt (iOS) / ≥ 48×48dp (Android)`    |
| Gesture         | `[Tap / Long Press / Swipe / Pinch]`       |
| Haptic Feedback | `[Core Haptics pattern / Material haptic]` |
| Keyboard Nav    | `[Focusable? Arrow key behavior]`          |
| Screen Reader   | `[VoiceOver/TalkBack label text]`          |

#### 3.5 Animation Specification

| Property          | Value                                    |
| ----------------- | ---------------------------------------- |
| Entry Animation   | `[Name] — [Duration] — [Easing]`         |
| Exit Animation    | `[Name] — [Duration] — [Easing]`         |
| State Transitions | `[From → To] — [Duration] — [Easing]`    |
| Keyframes         | `[If complex, reference animation file]` |

#### 3.6 Performance Budget

| Property         | Value                                   |
| ---------------- | --------------------------------------- |
| Frame Budget     | `≤ 16.67ms (60fps) / ≤ 33.33ms (30fps)` |
| GPU Target       | `[Adreno 6xx / Mali-G7x / Apple A13+]`  |
| Low-End Fallback | `[Simplified rendering path]`           |
| Memory Budget    | `[X] MB for this component`             |

#### 3.7 Accessibility Notes

- **VoiceOver/TalkBack Label:** `[Descriptive label text]`
- **Reduced Motion Alternative:** `[What happens when Reduce Motion is enabled]`
- **Colorblind Consideration:** `[How critical info is conveyed without color alone]`

---

## 4. Animation Specification Template

Every animation in the game must be documented using this template. Duplicate this section for each animation.

### Animation: `[Animation Name]`

#### 4.1 Trigger

> What event initiates this animation? (e.g., "Player taps play button", "Level complete", "Purchase confirmed")

#### 4.2 Timing Tokens

Use the following design tokens for all animation durations. Do not use arbitrary values.

| Token             | Duration | Use Case                                         |
| ----------------- | -------- | ------------------------------------------------ |
| `anim-fast`       | 100ms    | Micro-interactions, button press, toggle         |
| `anim-base`       | 200ms    | Standard transitions, state changes              |
| `anim-slow`       | 300ms    | Complex transitions, screen changes              |
| `anim-deliberate` | 500ms    | Hero animations, level transitions, celebrations |

#### 4.3 Easing Tokens

| Token         | Curve                          | Use Case                               |
| ------------- | ------------------------------ | -------------------------------------- |
| `ease-in`     | `cubic-bezier(0.4, 0, 1, 1)`   | Elements entering scene (accelerating) |
| `ease-out`    | `cubic-bezier(0, 0, 0.2, 1)`   | Elements exiting scene (decelerating)  |
| `ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Bidirectional transitions              |
| `spring`      | `stiffness: 300, damping: 25`  | Playful, bouncy interactions (juice)   |

#### 4.4 State Transition

| Property    | Value                      |
| ----------- | -------------------------- |
| Start State | `[Describe initial state]` |
| End State   | `[Describe final state]`   |
| Duration    | `[Token name] = [X]ms`     |
| Easing      | `[Token name]`             |

#### 4.5 Keyframes (if applicable)

| Frame | Time (ms) | Property     | Value                  |
| ----- | --------- | ------------ | ---------------------- |
| 0     | 0         | `[property]` | `[start value]`        |
| 1     | `[X]`     | `[property]` | `[intermediate value]` |
| 2     | `[Y]`     | `[property]` | `[end value]`          |

> For complex animations, attach a Lottie file, After Effects composition, or video reference.

#### 4.6 Performance Budget

| Property          | Value                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| Target Frame Rate | `60fps` (game canvas), `60fps` (meta-UI)                                                         |
| Low-End Fallback  | `[e.g., reduce particle count by 50%, skip intermediate keyframes, use opacity-only transition]` |
| GPU Constraints   | `[e.g., no overdraw > 3x, max 50k triangles per frame]`                                          |

#### 4.7 Accessibility Notes

- **Reduced Motion:** When `prefers-reduced-motion` / Accessibility → Reduce Motion is enabled:
  - `[ ]` Skip animation entirely (instant state change)
  - `[ ]` Simplify animation (opacity fade only, no motion)
  - `[ ]` Reduce duration to ≤ 100ms
- **Seizure Safety:** No flashing content > 3 flashes/second (WCAG 2.3.1)

---

## 5. Platform-Native Meta-UI Patterns

The following meta-UI screens must follow platform-specific conventions. The game canvas itself is **identical** across platforms for brand consistency.

### 5.1 Game Canvas

| Property    | iOS                      | Android                  | Notes                                                                 |
| ----------- | ------------------------ | ------------------------ | --------------------------------------------------------------------- |
| Rendering   | Identical                | Identical                | Core gameplay visuals are platform-agnostic                           |
| Safe Area   | Respect                  | Respect                  | UI elements must not overlap notches, camera cutouts, or gesture bars |
| Orientation | `[Portrait / Landscape]` | `[Portrait / Landscape]` | Lock orientation per PRD                                              |

### 5.2 Settings Menu

| Property     | iOS                                 | Android                  |
| ------------ | ----------------------------------- | ------------------------ |
| Presentation | Modal sheet (UIKit)                 | Bottom sheet (Material)  |
| Navigation   | List with disclosure indicators     | List with trailing icons |
| Toggles      | iOS-style UISwitch                  | Material Switch          |
| Sliders      | iOS-style UISlider                  | Material Slider          |
| Dismissal    | Swipe down / tap outside / Done btn | Swipe down / system back |
| Hierarchy    | Grouped sections with headers       | Categories with dividers |

### 5.3 Store / In-App Purchase

| Property      | iOS                                 | Android                                  |
| ------------- | ----------------------------------- | ---------------------------------------- |
| Presentation  | Tab or modal                        | Tab or bottom sheet                      |
| Product Cards | Scrollable cards with price badge   | Scrollable cards with Material elevation |
| Purchase Flow | Native StoreKit 2 sheet             | Native Google Play Billing dialog        |
| Confirmation  | Success animation + receipt         | Success animation + receipt              |
| Restore       | "Restore Purchases" button (bottom) | "Restore Purchases" button (bottom)      |
| Compliance    | Apple Review Guidelines §3.1.1      | Google Play Policies §3                  |

### 5.4 Leaderboards

| Property        | iOS                                     | Android                                |
| --------------- | --------------------------------------- | -------------------------------------- |
| Presentation    | Full-screen list or Game Center overlay | Full-screen list or Play Games overlay |
| Ranking Display | Player rank highlighted, scrollable     | Player rank highlighted, scrollable    |
| Social          | Friend filtering (Game Center)          | Friend filtering (Play Games)          |
| Refresh         | Pull-to-refresh                         | Pull-to-refresh                        |
| Empty State     | "No scores yet — play to compete!"      | "No scores yet — play to compete!"     |

### 5.5 Notifications

| Property   | iOS                                      | Android                                  |
| ---------- | ---------------------------------------- | ---------------------------------------- |
| In-App     | Banner toast (top), auto-dismiss 3s      | Snackbar (bottom), auto-dismiss 4s       |
| Push       | UNUserNotificationCenter                 | Firebase Cloud Messaging                 |
| Permission | System prompt (timing: after value demo) | System prompt (timing: after value demo) |
| Badge      | App icon badge count                     | Not supported (use notification)         |

---

## 6. Gesture Vocabulary

All game interactions must use this standardized gesture vocabulary.

### 6.1 Tap

| Property      | Value                                                       |
| ------------- | ----------------------------------------------------------- |
| **Purpose**   | Primary interaction — select, confirm, activate             |
| **Target**    | ≥ 44×44pt (iOS) / ≥ 48×48dp (Android)                       |
| **Feedback**  | Visual (pressed state) + haptic (light tap)                 |
| **Timeout**   | 100ms debounce between taps                                 |
| **Edge Case** | Tap on overlapping elements: topmost element receives event |

### 6.2 Long Press

| Property      | Value                                           |
| ------------- | ----------------------------------------------- |
| **Purpose**   | Context menu, preview, drag initiation          |
| **Duration**  | 500ms before activation                         |
| **Feedback**  | Visual (scale up 1.05x) + haptic (medium)       |
| **Cancel**    | Finger drag > 10pt cancels long press           |
| **Edge Case** | Long press on non-interactive area: no response |

### 6.3 Swipe

| Property      | Value                                              |
| ------------- | -------------------------------------------------- |
| **Purpose**   | Navigation (horizontal), card dismissal (vertical) |
| **Threshold** | ≥ 50pt horizontal / ≥ 80pt vertical to activate    |
| **Velocity**  | ≥ 0.5 pt/ms for intent recognition                 |
| **Feedback**  | Animated follow + snap to state                    |
| **Edge Case** | Swipe during animation: queue or ignore            |

### 6.4 Pinch (if applicable)

| Property      | Value                                   |
| ------------- | --------------------------------------- |
| **Purpose**   | Zoom (map, board, detail view)          |
| **Range**     | `[Min scale] × to [Max scale] ×`        |
| **Feedback**  | Continuous scale + haptic at boundaries |
| **Edge Case** | Pinch on non-zoomable area: no response |

### 6.5 Edge Swipe (Android)

| Property      | Value                                                              |
| ------------- | ------------------------------------------------------------------ |
| **Purpose**   | System back navigation                                             |
| **Priority**  | System gesture > game gesture                                      |
| **Behavior**  | Game must not intercept edge swipe from left/right edge            |
| **Edge Case** | Game canvas edge interactions: add 16dp dead zone from screen edge |

---

## 7. Edge Case Matrix

Every edge case must be handled with a defined UI state and recovery path.

| Edge Case                        | UI State                                                      | Recovery Path                                                    | Animation                     | Data Handling                |
| -------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------- | ---------------------------- |
| **Offline**                      | Banner: "No internet connection"                              | Auto-reconnect when available                                    | Fade-in banner (200ms)        | Queue actions locally        |
| **Slow Network**                 | Skeleton loaders + timeout indicator                          | Timeout after 15s → retry dialog                                 | Skeleton shimmer animation    | Partial data display         |
| **Interrupted IAP**              | "Purchase in progress" overlay                                | Resume on foreground / retry button                              | Loading spinner               | Transaction state persisted  |
| **Interrupted Data Sync**        | Toast: "Sync paused — will resume"                            | Resume on foreground                                             | Toast slide-in (300ms)        | Checksum validation          |
| **App Backgrounded**             | Game auto-pauses on `applicationWillResignActive` / `onPause` | Resume from pause on foreground                                  | Pause overlay fade-in (200ms) | Save game state immediately  |
| **App Foregrounded**             | Check for updates, validate session                           | If session expired → re-auth                                     | Transition from pause overlay | Validate cached data         |
| **Low Storage**                  | Warning: "Low storage — some features limited"                | Clear cache button provided                                      | Warning dialog (Material/iOS) | Aggressive cache eviction    |
| **Low Battery**                  | No special UI (respect OS battery saver)                      | If OS throttles: reduce particles, skip non-essential animations | N/A                           | Reduce GPU workload          |
| **Memory Warning**               | Release non-essential assets                                  | Reload on demand                                                 | Brief loading indicator       | Asset reference counting     |
| **OS Update / Version Mismatch** | "Update required" screen with store link                      | Deep link to App Store / Play Store                              | Fade-in screen (300ms)        | Block gameplay until updated |

---

## 8. Responsive Breakpoints

| Breakpoint   | Width Range          | Target Devices                   | Layout Adjustments                                                   |
| ------------ | -------------------- | -------------------------------- | -------------------------------------------------------------------- |
| **Phone**    | 320–480pt            | iPhone SE–15 Pro, Android phones | Single-column, bottom nav, compact cards                             |
| **Tablet**   | 600–840pt            | iPad mini–Pro, Android tablets   | Two-column layouts, side nav option, larger tap targets              |
| **Foldable** | Dual-screen (varies) | Surface Duo, Galaxy Fold         | Span-aware layouts, hinge avoidance zones, continuity across screens |

### 8.1 Design Token Scaling

| Token          | Phone | Tablet | Foldable (spanned) |
| -------------- | ----- | ------ | ------------------ |
| `spacing-xs`   | 4pt   | 6pt    | 6pt                |
| `spacing-sm`   | 8pt   | 12pt   | 12pt               |
| `spacing-md`   | 16pt  | 24pt   | 24pt               |
| `spacing-lg`   | 24pt  | 32pt   | 32pt               |
| `spacing-xl`   | 32pt  | 48pt   | 48pt               |
| `font-body`    | 16pt  | 18pt   | 18pt               |
| `font-heading` | 24pt  | 32pt   | 32pt               |

### 8.2 Hinge / Fold Considerations

- **Avoid placing interactive elements** within 24px of the hinge/fold line
- **Test readability** on both sides of the fold
- **Posture modes**: Support tabletop (game canvas on top half, controls on bottom) and book (continuous scroll across screens)

---

## 9. IDS Conformance Checklist

This checklist must be completed for every project IDS before it advances to Stage 2 Gate Review.

### 9.1 Document Completeness

| #   | Item                                                        | Pass | Fail | N/A | Notes |
| --- | ----------------------------------------------------------- | :--: | :--: | :-: | ----- |
| 1   | Document metadata complete (version, authors, date, status) |      |      |     |       |
| 2   | Design principles defined with measurable metrics           |      |      |     |       |
| 3   | Platform conventions documented for both iOS and Android    |      |      |     |       |
| 4   | Accessibility requirements aligned to WCAG 2.1 AA           |      |      |     |       |

### 9.2 Component Specifications

| #   | Item                                                             | Pass | Fail | N/A | Notes |
| --- | ---------------------------------------------------------------- | :--: | :--: | :-: | ----- |
| 5   | All UI components documented using component spec template       |      |      |     |       |
| 6   | Each component defines all 7 required states                     |      |      |     |       |
| 7   | Visual specs include dimensions, typography, color, iconography  |      |      |     |       |
| 8   | Interaction specs include tap target size and gesture vocabulary |      |      |     |       |
| 9   | Animation specs reference duration and easing tokens             |      |      |     |       |
| 10  | Performance budget defined per component                         |      |      |     |       |
| 11  | Accessibility notes present for every component                  |      |      |     |       |

### 9.3 Animation Specifications

| #   | Item                                                        | Pass | Fail | N/A | Notes |
| --- | ----------------------------------------------------------- | :--: | :--: | :-: | ----- |
| 12  | All animations documented using animation spec template     |      |      |     |       |
| 13  | Duration uses design tokens only (100/200/300/500ms)        |      |      |     |       |
| 14  | Easing uses design tokens only (ease-in/out/in-out, spring) |      |      |     |       |
| 15  | Start and end states defined for every animation            |      |      |     |       |
| 16  | Keyframes documented for complex animations                 |      |      |     |       |
| 17  | Performance budget defined (60fps target, low-end fallback) |      |      |     |       |
| 18  | Reduced-motion alternatives defined for every animation     |      |      |     |       |

### 9.4 Platform-Native Meta-UI

| #   | Item                                                         | Pass | Fail | N/A | Notes |
| --- | ------------------------------------------------------------ | :--: | :--: | :-: | ----- |
| 19  | Game canvas rendering identical across platforms             |      |      |     |       |
| 20  | Settings menu follows iOS HIG / Material 3 per platform      |      |      |     |       |
| 21  | Store/IAP follows platform-native purchase flows             |      |      |     |       |
| 22  | Leaderboards follow platform conventions                     |      |      |     |       |
| 23  | Notifications follow platform patterns                       |      |      |     |       |
| 24  | Safe areas respected (notches, camera cutouts, gesture bars) |      |      |     |       |

### 9.5 Gesture Vocabulary

| #   | Item                                                        | Pass | Fail | N/A | Notes |
| --- | ----------------------------------------------------------- | :--: | :--: | :-: | ----- |
| 25  | Tap targets meet minimum size (44pt iOS / 48dp Android)     |      |      |     |       |
| 26  | Long press duration defined (500ms)                         |      |      |     |       |
| 27  | Swipe thresholds and velocity defined                       |      |      |     |       |
| 28  | Pinch range defined (if applicable)                         |      |      |     |       |
| 29  | Edge swipe dead zone defined for Android                    |      |      |     |       |
| 30  | Gesture conflicts resolved (no overlapping gesture targets) |      |      |     |       |

### 9.6 Edge Cases

| #   | Item                                             | Pass | Fail | N/A | Notes |
| --- | ------------------------------------------------ | :--: | :--: | :-: | ----- |
| 31  | Offline state handling defined                   |      |      |     |       |
| 32  | Slow network state handling defined              |      |      |     |       |
| 33  | Interrupted transaction recovery defined         |      |      |     |       |
| 34  | App backgrounding/foregrounding behavior defined |      |      |     |       |
| 35  | Low storage state handling defined               |      |      |     |       |
| 36  | Low battery state handling defined               |      |      |     |       |
| 37  | Memory warning handling defined                  |      |      |     |       |
| 38  | OS update / version mismatch handling defined    |      |      |     |       |

### 9.7 Responsive Design

| #   | Item                                             | Pass | Fail | N/A | Notes |
| --- | ------------------------------------------------ | :--: | :--: | :-: | ----- |
| 39  | Phone breakpoint (320–480pt) layout defined      |      |      |     |       |
| 40  | Tablet breakpoint (600–840pt) layout defined     |      |      |     |       |
| 41  | Foldable / dual-screen considerations documented |      |      |     |       |
| 42  | Design token scaling table present               |      |      |     |       |
| 43  | Hinge/fold avoidance zones defined               |      |      |     |       |

### 9.8 Accessibility

| #   | Item                                                           | Pass | Fail | N/A | Notes |
| --- | -------------------------------------------------------------- | :--: | :--: | :-: | ----- |
| 44  | Colorblind mode specified (no color-only information)          |      |      |     |       |
| 45  | Motor accessibility (tap target size, alternative gestures)    |      |      |     |       |
| 46  | Cognitive accessibility (clear hierarchy, consistent patterns) |      |      |     |       |
| 47  | Screen reader labels defined for all interactive elements      |      |      |     |       |
| 48  | Reduced-motion alternatives defined for all animations         |      |      |     |       |
| 49  | Text scaling support (up to 200% without layout break)         |      |      |     |       |
| 50  | WCAG 2.1 AA conformance verified                               |      |      |     |       |

### 9.9 Determination

| Result          | Criteria                                                               |
| --------------- | ---------------------------------------------------------------------- |
| **PASS**        | ≥ 95% Pass, zero Fail items, all accessibility items (44–50) Pass      |
| **CONDITIONAL** | 80–94% Pass, zero accessibility Fails, remediation plan required       |
| **FAIL**        | < 80% Pass, OR any accessibility Fail → STOP, remediate before Stage 2 |

### 9.10 Sign-Off

| Role                   | Name             | Signature | Date | Vote |
| ---------------------- | ---------------- | --------- | ---- | ---- |
| **CDO**                | Yuki Tanaka-Chen |           |      |      |
| **Art Director**       | Renaud Leclercq  |           |      |      |
| **Lead Game Designer** | Mei Watanabe     |           |      |      |
| **Motion/UI Animator** | Marco Bellini    |           |      |      |

---

## 10. Authoring Responsibility

The following roles are responsible for authoring specific sections of each project IDS:

| Section                    | Responsible Author                 | Reviewer               |
| -------------------------- | ---------------------------------- | ---------------------- |
| Design Principles          | Mei Watanabe (Lead Game Designer)  | Yuki Tanaka-Chen (CDO) |
| Platform Conventions       | Yuki Tanaka-Chen (CDO)             | Platform Leads         |
| Accessibility Requirements | Yuki Tanaka-Chen (CDO)             | CDO Accessibility Lead |
| Component Specifications   | Elena Morozova (UI Visual Artist)  | Marco Bellini          |
| Animation Specifications   | Marco Bellini (Motion/UI Animator) | Elena Morozova         |
| Platform-Native Meta-UI    | Yuki Tanaka-Chen (CDO)             | Platform Leads         |
| Gesture Vocabulary         | Mei Watanabe (Lead Game Designer)  | Marco Bellini          |
| Edge Case Matrix           | Marco Bellini (Motion/UI Animator) | Dmitri Volkov          |
| Responsive Breakpoints     | Elena Morozova (UI Visual Artist)  | Marco Bellini          |
| IDS Conformance Review     | Yuki Tanaka-Chen (CDO)             | Full creative team     |

### 10.1 Authoring Timeline

| Milestone                      | Deadline             | Owner              |
| ------------------------------ | -------------------- | ------------------ |
| IDS template structure drafted | Before Stage 2 start | Marco Bellini      |
| Component specs populated      | Stage 2, Week 1      | Elena Morozova     |
| Animation specs populated      | Stage 2, Week 1–2    | Marco Bellini      |
| Meta-UI patterns documented    | Stage 2, Week 1      | Yuki Tanaka-Chen   |
| IDS completeness review        | Stage 2, Week 2      | Yuki Tanaka-Chen   |
| IDS conformance sign-off       | Stage 2 Gate Review  | Full creative team |

---

_Document End — Game IDS Template v1.0 — Studio Casual Games Design Department_
