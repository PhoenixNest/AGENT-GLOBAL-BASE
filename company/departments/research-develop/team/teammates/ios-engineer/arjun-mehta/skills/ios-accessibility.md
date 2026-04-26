---
version: "1.0.0"
---

| Competency                | Description                                                                                                | Quality Criteria                                                                                                              |
| ------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| VoiceOver                 | Accessibility labels, hints, traits, notifications, custom actions, rotor items                            | All UI elements have meaningful labels; custom actions for complex interactions; VoiceOver navigation is logical and complete |
| Dynamic Type              | Text scaling,ContentSizeCategory observation, layout adaptation, maximum size testing, custom font scaling | App fully functional at XXXL font size; layouts adapt gracefully; no text truncation or overlap at any size                   |
| Switch Control            | Focus management, focus groups, scan styles, custom gestures, point scanning                               | All interactive elements reachable via Switch Control; logical focus order; custom gestures for complex interactions          |
| Accessibility Identifiers | Systematic naming convention, test-auditable identifiers, consistency across platforms                     | Every interactive element has a11y identifier; identifiers follow naming convention; XCUITests use identifiers exclusively    |
| Audit Tools               | Accessibility Inspector, Accessibility Scanner, automated checks, manual VoiceOver testing                 | Automated a11y checks in CI; manual VoiceOver test script executed per release; audit tool findings tracked and resolved      |

## Navigation

- [ ] Can navigate all screens using swipe gestures
- [ ] Rotor allows navigation by headings, links, and form controls
- [ ] Logical reading order matches visual layout
- [ ] No elements skipped or inaccessible

## Interactive Elements

- [ ] All buttons have meaningful labels (not "Button 1", "Button 2")
- [ ] All form fields have associated labels
- [ ] All images have appropriate descriptions (or marked decorative)
- [ ] Custom actions available for complex interactions

## Dynamic Content

- [ ] State changes announced via accessibility notifications
- [ ] Loading states announced ("Loading...")
- [ ] Error messages announced immediately
- [ ] Success confirmations announced

## Dynamic Type

- [ ] All text readable at XXXL font size
- [ ] No text truncation or overlap
- [ ] Scrolling works for overflow content
- [ ] Touch targets remain usable at large font sizes

## Switch Control

- [ ] All interactive elements reachable via point scanning
- [ ] Logical scan order
- [ ] Custom gestures work with Switch Control

```

## Pipeline Integration

- **Stage 2 (Design):** IDS specifies accessibility requirements (contrast ratios, touch target sizes, VoiceOver labels, Dynamic Type support).
- **Stage 5 (Development):** All UI components built with accessibility from the start. No retrofitting after visual completion.
- **Stage 6 (Code Review):** Accessibility audit: label completeness, touch target sizing, Dynamic Type resilience, semantic structure, identifier coverage.
- **Stage 7 (Automated Testing):** Automated accessibility checks in test suite; manual VoiceOver test script execution.
- **Stage 8 (Integrity Verification):** CDO verifies IDS accessibility specifications are realized. Accessibility Inspector audit with zero critical issues.
- **Stage 10 (Release Readiness):** Accessibility conformance is item 2 on the release checklist (Design — all CDO/IDS specifications realized).

## Quality Standards

- **100%** interactive elements have meaningful accessibility labels
- **100%** interactive elements have minimum 44x44pt touch target
- **100%** text scales correctly at all Dynamic Type sizes (XXS to XXXXL)
- App fully usable at **accessibility font sizes** — no truncation or overlap
- **100%** VoiceOver users can complete all core user flows
- **100%** interactive elements have accessibility identifiers (for XCUITest)
- Custom accessibility actions provided for **complex multi-touch interactions**
- Dynamic content changes announced via **UIAccessibility notifications**
- Decorative images marked with `accessibilityHidden(true)` / `.accessibilityHidden(true)`
- Manual VoiceOver test script **executed and signed off** before every release
- Accessibility defects classified as **P0/P1** (not cosmetic) — they block release
- No information conveyed by **color alone** — always paired with text or icon


---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
```
