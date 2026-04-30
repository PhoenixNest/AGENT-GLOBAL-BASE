# ADR: Accessibility Strategy

**Project:** [Project Name]
**ADR ID:** ADR-[NNN]
**Status:** Proposed | Accepted | Superseded
**Author:** CDO (Yuki Tanaka-Chen) + CTO (Dr. Kenji Nakamura)
**Date:** YYYY-MM-DD
**Pipeline:** Full-Stack Cross-Platform

---

## Context

The full-stack application spans web, iOS, and Android surfaces. Each platform has distinct accessibility APIs, guidelines, and user expectations. WCAG 2.1 AA compliance is a universal baseline, but platform-specific targets — VoiceOver on iOS, TalkBack on Android, ARIA on web — require dedicated engineering decisions. This ADR locks the accessibility approach for the full project and drives implementation in Stage 5 and testing in Stage 7.

Accessibility is not cosmetic — it is a legal requirement in the EU (EN 301 549), US (ADA Section 508 for public-facing services), and APAC markets. Non-compliance is a P0 release blocker.

---

## Decision

### Universal Baseline (All Platforms)

| Requirement                      | Standard        | Measurement                                | Stage 7 Gate    |
| -------------------------------- | --------------- | ------------------------------------------ | --------------- |
| Colour contrast (normal text)    | WCAG 2.1 §1.4.3 | ≥ 4.5:1 ratio                              | Automated audit |
| Colour contrast (large text)     | WCAG 2.1 §1.4.3 | ≥ 3:1 ratio                                | Automated audit |
| Colour not sole conveyor of info | WCAG 2.1 §1.4.1 | No information conveyed by colour alone    | Manual review   |
| Text resize support              | WCAG 2.1 §1.4.4 | Content readable at 200% zoom without loss | Manual test     |
| No seizure-inducing content      | WCAG 2.1 §2.3   | No content flashes > 3 times/second        | Automated check |
| Skip navigation                  | WCAG 2.1 §2.4.1 | Web: skip-to-content link; Mobile: N/A     | Manual test     |
| Page/screen titles               | WCAG 2.1 §2.4.2 | Every screen has a descriptive title       | Automated audit |
| Focus order                      | WCAG 2.1 §2.4.3 | Logical focus traversal order              | Manual test     |

### Web Surface (Track FS-WFE)

| Requirement                        | Implementation Approach                                      | Tooling                      |
| ---------------------------------- | ------------------------------------------------------------ | ---------------------------- |
| ARIA roles on interactive elements | Native HTML semantics first; ARIA only to supplement         | eslint-plugin-jsx-a11y       |
| Screen reader — announcements      | `aria-live` regions for dynamic content updates              | axe-core, manual VoiceOver   |
| Screen reader — tested platforms   | VoiceOver/Safari (macOS + iOS), NVDA/Firefox (Windows)       | Manual CI-gated gate Stage 7 |
| Keyboard navigation                | Full keyboard operability on all interactive elements        | Playwright keyboard tests    |
| Focus visible indicator            | `:focus-visible` with 2px outline, 3:1 contrast              | Automated + visual review    |
| Reduced motion                     | `prefers-reduced-motion` media query on all animations       | CSS audit + manual test      |
| Responsive text                    | No fixed-px font sizes; all type in rem/clamp                | Automated lint               |
| Form labels                        | All inputs have associated `<label>` or `aria-label`         | axe-core                     |
| Error identification               | Error messages linked to their inputs via `aria-describedby` | axe-core + manual            |

### iOS Surface (Track FS-MOB)

| Requirement           | Implementation Approach                                                                             |
| --------------------- | --------------------------------------------------------------------------------------------------- |
| VoiceOver labels      | `accessibilityLabel` on all interactive elements                                                    |
| VoiceOver hints       | `accessibilityHint` for non-obvious actions                                                         |
| VoiceOver traits      | Correct `accessibilityTraits` (button, link, image, etc.)                                           |
| Dynamic Type          | All text uses `UIFont.preferredFont(forTextStyle:)` with `adjustsFontForContentSizeCategory = true` |
| Minimum touch targets | 44pt × 44pt minimum (HIG requirement)                                                               |
| Reduce Motion         | Respect `UIAccessibility.isReduceMotionEnabled`                                                     |
| Switch Access         | All interactive elements reachable via switch access                                                |
| Grouping              | Related content grouped with `accessibilityElements` or container frames                            |

### Android Surface (Track FS-MOB)

| Requirement           | Implementation Approach                                                       |
| --------------------- | ----------------------------------------------------------------------------- |
| TalkBack labels       | `contentDescription` on all interactive views                                 |
| TalkBack traversal    | `importantForAccessibility` set correctly; logical traversal order            |
| Font scaling          | All text sizes in `sp`; layouts accommodate up to 1.4× scale without overflow |
| Minimum touch targets | 48dp × 48dp minimum                                                           |
| Reduce Motion         | Respect `Settings.System.ANIMATOR_DURATION_SCALE == 0`                        |
| Colour contrast       | Verify at Android OS large font + high contrast settings                      |
| Haptic feedback       | `HapticFeedbackConstants` used for interactive events                         |

---

## Accessibility Testing Protocol (Stage 7)

| Platform         | Automated                     | Manual                                 | Pass Threshold                                     |
| ---------------- | ----------------------------- | -------------------------------------- | -------------------------------------------------- |
| Web              | axe-core (CI + Stage 7)       | VoiceOver/Safari + NVDA/Firefox by CDO | ≥ 95% axe-core pass; zero critical manual findings |
| iOS              | XCTest accessibility APIs     | VoiceOver full flow walkthrough by CDO | Zero critical findings                             |
| Android          | Espresso accessibility checks | TalkBack full flow walkthrough by CDO  | Zero critical findings                             |
| Developer portal | axe-core                      | Screen reader spot-check               | WCAG 2.1 AA ≥ 95%                                  |

**Defect classification:**

| Violation Level              | P-Severity | Release Impact |
| ---------------------------- | ---------- | -------------- |
| Critical (blocks access)     | P0         | Blocks release |
| Serious (impedes access)     | P1         | Blocks release |
| Moderate (frustrates access) | P2         | User decides   |
| Minor (nuisance)             | P3         | User decides   |

---

## Rationale

[Explain key decisions — e.g., why native semantics preferred over ARIA, why axe-core chosen over alternative auditors, platform-specific trade-offs, etc.]

---

## Trade-offs

| Benefit                                                           | Cost                                                         |
| ----------------------------------------------------------------- | ------------------------------------------------------------ |
| Legal compliance across all key markets                           | Moderate development overhead per feature                    |
| Expanded addressable market (≥ 1B users with disability globally) | Manual screen reader testing at each stage gate adds time    |
| Platform-native a11y performs better than workarounds             | Platform-specific implementations require separate codepaths |

---

## Sign-Off

| Role | Name               | Decision   | Date       |
| ---- | ------------------ | ---------- | ---------- |
| CDO  | Yuki Tanaka-Chen   | ☐ Accepted | YYYY-MM-DD |
| CTO  | Dr. Kenji Nakamura | ☐ Accepted | YYYY-MM-DD |
| CIO  | Dr. Priya Mehta    | ☐ Accepted | YYYY-MM-DD |
