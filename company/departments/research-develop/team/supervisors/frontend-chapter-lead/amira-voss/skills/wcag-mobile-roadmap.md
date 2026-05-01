---
name: wcag-mobile-roadmap
description: WCAG 2.1 AA mobile web roadmap — accessibility audit methodology, remediation prioritization, assistive-technology test matrix (VoiceOver, TalkBack, switch access), the mobile-web-specific accessibility patterns (touch target sizing, focus management, reduced motion), and the Stage 6 accessibility review process. Use when planning accessibility work for a mobile web product, when reviewing an accessibility audit report, or when enforcing the accessibility gate at Stage 6.
version: "1.0.0"
---

# WCAG 2.1 AA Mobile Web Roadmap

## Purpose

Define Amira Voss's approach to accessibility for the company's mobile web products. The company targets WCAG 2.1 AA compliance for all web releases. This skill covers the mobile-specific accessibility patterns and testing methodology that go beyond the desktop-centric guidance in most WCAG documentation — mobile web has unique constraints (touch, viewport, orientation, network) that require explicit engineering standards.

## Mobile-Specific Accessibility Requirements

Standard WCAG 2.1 AA covers content and interaction; mobile web adds platform-specific requirements:

| Requirement           | Standard                                   | Mobile-Web Specific                                                                                       |
| --------------------- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **Touch target size** | 44×44pt minimum (WCAG 2.5.5)               | Minimum 44×44 CSS pixels; no target smaller than 24×24 with at least 24px spacing from other targets      |
| **Color contrast**    | 4.5:1 text, 3:1 large text                 | Same targets, tested in both light and dark mode                                                          |
| **Focus management**  | Visible focus indicators                   | Focus traps in modals; return focus to trigger on modal close; no focus loss on route change (SPA)        |
| **Reduced motion**    | `prefers-reduced-motion` media query       | Disable all parallax, auto-play animations, and transitions; never disable navigation animations entirely |
| **Orientation lock**  | WCAG 1.3.4: no lock unless essential       | Default to both orientations; if landscape-only, document the exception                                   |
| **Reflow**            | WCAG 1.4.10: no horizontal scroll at 320px | All content reflowable at 320px viewport; no sticky elements blocking the full-screen viewport            |
| **Text resize**       | Content readable at 200% zoom              | Test with browser text zoom (not viewport zoom) at 200% — no content cutoff or overlap                    |

## Assistive Technology Test Matrix

Before every Stage 6 (Code Review) submission for any user-facing feature, the following test matrix is completed:

| AT + Platform                             | Critical User Flows                      | Tester                |
| ----------------------------------------- | ---------------------------------------- | --------------------- |
| VoiceOver + Safari (iOS 17+)              | Onboarding, core action, form submission | Amira or delegated QA |
| TalkBack + Chrome (Android 12+)           | Onboarding, core action, form submission | Amira or delegated QA |
| Keyboard-only navigation (desktop Chrome) | All modal flows, dropdowns, date pickers | Any engineer          |
| Switch access (iOS)                       | Critical path only                       | Amira (spot-check)    |
| Windows High Contrast Mode                | All screens                              | Any engineer          |

**Test minimum:** All P0/P1 AT failures block merge. Amira records AT test results in Confluence under the feature's accessibility tracking page.

## axe-core Integration

Automated accessibility scanning (owned by VP Quality Aisha Patel — see `axe-core-wcag-testing.md`) catches ~30-40% of WCAG violations. Amira's manual matrix covers the rest. Integration point:

```typescript
// Amira defines the axe-core configuration for web products
const wcagConfig = {
  runOnly: {
    type: "tag",
    values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"],
  },
  rules: {
    // Mobile-specific rule overrides documented in the skill
    "color-contrast": { enabled: true },
    "target-size": { enabled: true }, // WCAG 2.5.5
  },
};
```

## Remediation Prioritization

When an audit produces a list of findings, Amira prioritizes them using impact-effort scoring:

| Priority | Criteria                                                 | Example                                                                   | Timeline                                                         |
| -------- | -------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **P0**   | Completely blocks AT users from a critical flow          | Form submit button has no accessible name — VoiceOver users cannot submit | Fix before Stage 6 approval                                      |
| **P1**   | Severely degrades AT experience on core feature          | Focus lost after modal close — keyboard users must navigate from page top | Fix before Stage 6 approval                                      |
| **P2**   | Non-critical flow inaccessible or significantly degraded | Help tooltip not announced by VoiceOver                                   | Fix within 2 sprints                                             |
| **P3**   | Best-practice violation; AT users can work around        | Color contrast 4.2:1 (below 4.5:1) on a non-primary action                | Track in accessibility backlog; fix at next refactor opportunity |

## Mobile Accessibility Pattern Library

Amira maintains a set of validated, accessible code patterns for common mobile web components:

### Modal / Bottom Sheet

```typescript
// Accessible modal: traps focus, announces to AT, returns focus on close
export function AccessibleModal({ isOpen, onClose, title, children }) {
  const firstFocusableRef = useRef(null);
  const previousFocusRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement;
      firstFocusableRef.current?.focus();
    } else {
      previousFocusRef.current?.focus();
    }
  }, [isOpen]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      // Focus trap implemented via onKeyDown intercepting Tab/Shift+Tab
    >
      <h2 id="modal-title">{title}</h2>
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  );
}
```

### Navigation Route Change (SPA)

```typescript
// Announce route changes to screen reader users — no native browser announcement in SPA
export function RouteAnnouncer() {
  const [announcement, setAnnouncement] = useState("");
  const location = useLocation();

  useEffect(() => {
    const pageTitle = document.title || "New page";
    setAnnouncement(`Navigated to ${pageTitle}`);
  }, [location]);

  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only" // visually hidden
    >
      {announcement}
    </div>
  );
}
```

## Stage 6 Accessibility Review

Amira reviews every PR touching UI components before Stage 6 approval:

| Review Check            | Tool                                      | Pass Criteria                                                   |
| ----------------------- | ----------------------------------------- | --------------------------------------------------------------- |
| axe-core scan           | CI (Playwright + axe)                     | Zero critical/serious violations                                |
| Keyboard navigation     | Manual                                    | All interactive elements reachable by Tab; visible focus on all |
| Touch target sizes      | DevTools emulator                         | All targets ≥ 44×44 CSS px                                      |
| AT test (VoiceOver iOS) | Manual                                    | All P0/P1 user flows navigable                                  |
| Color contrast          | axe-core + manual for complex backgrounds | All text meets 4.5:1 (3:1 for large)                            |

## Quality Standards

- Zero WCAG 2.1 AA P0/P1 violations in any production release
- AT test matrix completed for every feature PR that modifies UI components
- Accessibility tracking page in Confluence updated for every feature before Stage 6 approval
- axe-core scan integrated in CI with zero-violation gate on critical/serious severity
- Mobile accessibility pattern library reviewed and updated annually
