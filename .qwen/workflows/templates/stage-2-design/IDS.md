# Interaction Design Specification (IDS)

**Project:** [Project Name]
**Version:** v1
**Author:** CDO (Yuki Tanaka-Chen)
**Date:** YYYY-MM-DD
**Status:** Draft | Under Review | Approved
**Referenced Artifacts:** PRD v1, SRD v1, Web Prototype vN

## Version History

| Version | Date       | Author | Changes                  | Communicated to Platform Leads? |
| ------- | ---------- | ------ | ------------------------ | ------------------------------- |
| v1      | YYYY-MM-DD | [Name] | Initial specification    | ☐ Yes / ☐ No                    |
| v2      | YYYY-MM-DD | [Name] | [Description of changes] | ☐ Yes / ☐ No                    |

> **Change Propagation Protocol:** During Stage 5 development, any IDS revision must be communicated to all active platform track leads within **24 hours**. Platform leads acknowledge receipt and submit an impact assessment within 48 hours. IDS changes that alter implemented components, gestures, or accessibility specifications must trigger a partial Design Fidelity Checkpoint re-run on the affected areas. Version tracking follows the repository's document versioning convention (`ids-v1/`, `ids-v2/`, `VERSIONS.md`).

---

## 1. Design Context

Brief description of the product, its design goals, and the design system/tokens being used.

---

## 2. Platform Design Conventions

| Platform | Design System                    | Navigation Pattern                             | Transition Style                |
| -------- | -------------------------------- | ---------------------------------------------- | ------------------------------- |
| iOS      | Human Interface Guidelines (HIG) | [Navigation controller / Tab bar / etc.]       | [Push / Modal / Sheet]          |
| Android  | Material Design 3                | [Bottom navigation / Navigation drawer / etc.] | [Slide / Shared element / Fade] |

---

## 3. Component Tree

### 3.1 [Screen Name]

```
├─ AppBar
│  ├─ Title
│  ├─ [Action Buttons]
│  └─ [Overflow Menu]
├─ Content Area
│  ├─ [Component 1]
│  ├─ [Component 2]
│  └─ [Component 3]
└─ Bottom Bar (if applicable)
   └─ [CTA / Navigation]
```

---

## 4. Visual Specifications

### 4.1 [Screen Name] — [Platform]

| Property         | Value                           |
| ---------------- | ------------------------------- |
| Background color | [Token reference]               |
| Typography scale | [Type ramp / Text style tokens] |
| Spacing          | [8dp grid / spacing tokens]     |
| Corner radius    | [Component token]               |
| Elevation/Shadow | [Elevation token]               |

### 4.2 [Screen Name] — Accessibility

| Property                   | Value                             |
| -------------------------- | --------------------------------- |
| Screen reader label        | [Label text]                      |
| Contrast ratio             | [Ratio — must meet WCAG 2.1 AA]   |
| Touch target size          | [Minimum 48dp Android / 44pt iOS] |
| Focus order                | [Logical tab/voice order]         |
| Dynamic type support       | [Yes — up to 200%]                |
| Reduced motion alternative | [Description]                     |

---

## 5. Gesture Vocabulary

| Gesture         | Target    | Action   | Platform Convention                |
| --------------- | --------- | -------- | ---------------------------------- |
| Tap             | [Element] | [Action] | [iOS/Android convention or custom] |
| Swipe           | [Element] | [Action] | [Direction, distance]              |
| Long press      | [Element] | [Action] | [Context menu / haptic feedback]   |
| Pull to refresh | [Screen]  | [Action] | [Standard pattern]                 |

---

## 6. State Diagrams

### 6.1 [Feature/Flow Name]

```
[State 1] ──(event)──▶ [State 2] ──(event)──▶ [State 3]
    │                                             │
    │──(error)──▶ [Error State] ◀──(error)────────│
```

---

## 7. Edge Case Matrices

| Scenario               | Android Behavior               | iOS Behavior                   |
| ---------------------- | ------------------------------ | ------------------------------ |
| No network             | [Error screen / offline mode]  | [Error screen / offline mode]  |
| Empty state            | [Placeholder UI]               | [Placeholder UI]               |
| Loading                | [Skeleton / spinner]           | [Skeleton / spinner]           |
| Error                  | [Error message + retry]        | [Error message + retry]        |
| Permission denied      | [Explanation + settings link]  | [Explanation + settings link]  |
| Low storage            | [Graceful degradation / error] | [Graceful degradation / error] |
| Backgrounded during op | [State preserved / resume]     | [State preserved / resume]     |

---

## 8. Animation Specifications

| Animation           | Trigger       | Duration | Easing     | Interruptible? | Platform |
| ------------------- | ------------- | -------- | ---------- | -------------- | -------- |
| [Screen transition] | [User action] | [300ms]  | [ease-out] | ☐ Yes / ☐ No   | Both     |
| [Button feedback]   | [Tap]         | [150ms]  | [linear]   | ☐ Yes / ☐ No   | Both     |

---

## 9. Design Tokens Reference

| Token            | Android              | iOS                | Value       |
| ---------------- | -------------------- | ------------------ | ----------- |
| color.primary    | @color/primary       | AssetColor.primary | [#HEX]      |
| spacing.md       | 16dp                 | 16pt               | [16]        |
| typography.body1 | TextAppearance.Body1 | UIFont.body        | [font/size] |

---

## 10. Accessibility Specifications (WCAG 2.1 AA)

Every component defined above must meet the following accessibility specifications.

### 10.1 Screen Reader Labels

| Component / Screen   | VoiceOver (iOS) Label & Hint                   | TalkBack (Android) Label & Hint                |
| -------------------- | ---------------------------------------------- | ---------------------------------------------- |
| [Primary CTA button] | "[Label] — [Hint]"                             | "[Label] — [Hint]"                             |
| [Form field]         | "[Field name], edit text. [Hint]. Double-tap." | "[Field name], edit text. [Hint]. Double-tap." |
| [Icon button]        | "[Action name], button"                        | "[Action name], button"                        |

### 10.2 Touch Target Minimums

| Component            | Android Target | iOS Target | Meets Minimum? |
| -------------------- | -------------- | ---------- | -------------- |
| [Primary CTA button] | 48×48dp        | 44×44pt    | ☐ Yes / ☐ No   |
| [Icon button]        | 48×48dp        | 44×44pt    | ☐ Yes / ☐ No   |
| [Tab bar item]       | 48×48dp        | 44×44pt    | ☐ Yes / ☐ No   |

### 10.3 Contrast Ratios

All color combinations must meet:

- **Normal text (< 18pt / 14pt bold):** 4.5:1 minimum
- **Large text (≥ 18pt / 14pt bold):** 3:1 minimum
- **UI components & graphical objects:** 3:1 minimum

| Element Pair           | Foreground | Background | Ratio | Passes AA? |
| ---------------------- | ---------- | ---------- | ----- | ---------- |
| [Body text on surface] | [#HEX]     | [#HEX]     | X.X:1 | ☐ Yes      |

### 10.4 Focus Order

Screen reader focus must follow logical reading order (top-to-bottom, grouped by section):

```
[Screen/Flow name]
1. [Element 1: e.g., Screen title]
2. [Element 2: e.g., First form field]
3. [Element 3: e.g., Submit button]
4. [Element 4: e.g., Cancel link]
```

### 10.5 Dynamic Type Support

All text must support up to 200% font scaling without layout breakage:

| iOS Text Style    | Android TextAppearance  | Base Size | 200% Size | Layout Behavior     |
| ----------------- | ----------------------- | --------- | --------- | ------------------- |
| UIFont.body       | TextAppearance.Body     | 17pt      | 34pt      | [Scrolls / Reflows] |
| UIFont.largeTitle | TextAppearance.Headline | 34pt      | 68pt      | [Scrolls / Reflows] |

### 10.6 Reduced Motion Alternatives

When user enables Reduce Motion (iOS) or Remove Animations (Android):

| Original Animation       | Reduced Motion Alternative       |
| ------------------------ | -------------------------------- |
| [Slide transition 300ms] | [Cross-fade 150ms or instant]    |
| [Parallax scroll effect] | [Static background, no parallax] |

---

## 11. Internationalization Design Considerations

### 11.1 Text Expansion Tolerance

All layouts must accommodate text expansion from English source to target languages:

| Language Family  | Expansion Rate | Affected Components                        |
| ---------------- | -------------- | ------------------------------------------ |
| Germanic (DE)    | +25% to +35%   | Buttons, nav titles, form labels, dialogs  |
| Romance (FR, ES) | +20% to +30%   | Buttons, nav titles, form labels, dialogs  |
| CJK (ZH, JA, KO) | −30% to −40%   | May compress; verify minimum touch targets |

#### Component-Specific Thresholds

| Component            | Max Expansion               | Design Strategy                              |
| -------------------- | --------------------------- | -------------------------------------------- |
| Navigation bar title | +30% (iOS) / +35% (Android) | Truncate with ellipsis; full text in tooltip |
| Button labels        | +35%                        | Allow 2-line wrap; minimum 48dp height       |
| Form field labels    | +30%                        | Stack above field (not inline)               |
| Dialog body text     | +45%                        | Scrollable content area                      |
| Tab bar labels       | +25%                        | Icon-only fallback if text overflows         |

#### Verification Method

- Overlay translated strings (worst-case: German for expansion, CJK for compression) on all screen mockups
- Verify no truncation, overlap, or layout breakage at design level
- Document any exceptions in edge case matrix

### 11.2 RTL Layout Considerations

If RTL languages (Arabic, Hebrew, Persian) are targeted per PRD §8:

| Rule                  | Detail                                                                         |
| --------------------- | ------------------------------------------------------------------------------ |
| Mirroring             | All horizontal layouts mirror: nav, tabs, carousels, lists                     |
| Icon directionality   | Directional icons flip (back arrows, progress, timelines)                      |
| Non-directional icons | Icons with no inherent direction do NOT flip (settings gear, search magnifier) |
| Text alignment        | Right-aligned by default; numbers remain LTR                                   |
| Punctuation           | Bidirectional text handled per Unicode Bidi Algorithm                          |
| Touch gestures        | Swipe directions mirror (swipe-left becomes swipe-right)                       |

#### RTL Component Audit

| Screen     | Mirrored? | Directional Icons Updated? | Text Alignment Verified? | Notes |
| ---------- | --------- | -------------------------- | ------------------------ | ----- |
| [Screen 1] | ☐ Yes/No  | ☐ Yes/No                   | ☐ Yes/No                 |       |
| [Screen 2] | ☐ Yes/No  | ☐ Yes/No                   | ☐ Yes/No                 |       |

---

_Approved by CDO (Yuki Tanaka-Chen) on YYYY-MM-DD_
_Archived alongside: Web Prototype vN_
