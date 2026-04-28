---
name: advanced-a11y
description: This skill enables the implementation and validation of WCAG 2.1 AA/AAA compliance across all frontend surfaces.
---

# Advanced Accessibility Engineering

**Category:** Frontend Engineering / Accessibility
**Owner:** Senior Frontend Engineer (Elena Kim)

## Overview

This skill enables the implementation and validation of WCAG 2.1 AA/AAA compliance across all frontend surfaces, going beyond automated tooling to address the nuanced realities of assistive technology users. It covers screen reader optimization (VoiceOver, TalkBack, NVDA, JAWS), keyboard navigation architecture, aria-live region management, focus control patterns, and axe-core automation integration. Accessibility is not a checklist — it is a fundamental quality attribute that determines whether our product is usable by the 1.3 billion people worldwide who experience significant disability. Every component, every interaction, every content update must be accessible by design, not as an afterthought.

## Competency Dimensions

| Dimension                        | Description                                                                                    | Proficiency Indicators                                                                                  |
| -------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **WCAG 2.1 AA/AAA Compliance**   | Deep understanding of all 78 success criteria across A/AA/AAA conformance levels               | Zero AA violations in automated + manual audit; AAA achieved for all Level A/AA criteria where feasible |
| **Screen Reader Optimization**   | VoiceOver (iOS/macOS), TalkBack (Android), NVDA (Windows), JAWS (Windows Windows) testing      | All interactive elements announced correctly; content read in logical order; no silent UI elements      |
| **Keyboard Navigation**          | Complete keyboard operability with visible focus indicators, skip links, and logical tab order | 100% of functionality accessible via keyboard; focus trap in modals; no keyboard traps                  |
| **ARIA & Live Regions**          | Correct ARIA role/state/property usage; aria-live for dynamic content updates                  | Zero ARIA misuse (role/property mismatch); live regions announce appropriately without spam             |
| **Automated Testing**            | axe-core integration, CI gating, custom rule development                                       | axe-core in CI pipeline; custom rules for domain-specific patterns; zero false negatives                |
| **Assistive Technology Testing** | Manual testing with real AT devices; user journey validation                                   | Quarterly AT testing report; issues resolved within 1 sprint of discovery                               |

## Execution Guidance

### WCAG 2.1 Compliance — Beyond the Checklist

**Conformance level strategy:**

- **Target: WCAG 2.1 AA** as the minimum baseline (required by Stage 2 IDS specifications)
- **AAA where feasible** for text content (1.4.8 Visual Presentation, 2.4.9 Link Purpose, 3.1.5 Reading Level)
- **Document deviations** — if AAA is not achievable for a component, document the reason and the compensating control

**Critical AA criteria that commonly fail in SPAs:**

| Criterion                        | Requirement                                                                             | Common Failure Mode                                                        | Remediation                                                                                      |
| -------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **1.3.1 Info and Relationships** | Information/structure conveyed through presentation must be programmatically determined | Div soup — using `<div>` for semantic structure                            | Use semantic HTML: `<nav>`, `<main>`, `<article>`, `<section>`, `<header>`, `<footer>`           |
| **1.3.2 Meaningful Sequence**    | Correct reading order when CSS is disabled                                              | CSS grid/flexbox reorders DOM visually but screen readers follow DOM order | Ensure DOM order matches visual order; use `order` CSS property only for non-critical reordering |
| **2.1.1 Keyboard**               | All functionality operable via keyboard                                                 | Custom widgets (dropdowns, sliders) without keyboard handlers              | Implement full keyboard interaction model per WAI-ARIA Authoring Practices                       |
| **2.4.3 Focus Order**            | Focus navigates in meaningful order                                                     | Modal opens but focus remains on trigger behind the modal                  | Move focus to modal container on open; return focus to trigger on close                          |
| **2.4.7 Focus Visible**          | Keyboard focus indicator always visible                                                 | `outline: none` without alternative focus style                            | Custom focus styles: `:focus-visible { outline: 2px solid; outline-offset: 2px; }`               |
| **3.3.1 Error Identification**   | Input errors identified and described in text                                           | Red border only, no text description                                       | `<span role="alert" id="error-msg">Invalid email format</span>` + `aria-describedby="error-msg"` |
| **4.1.2 Name, Role, Value**      | All UI components have accessible name, role, and current value                         | Custom buttons without aria-label or text content                          | `<button aria-label="Close dialog">✕</button>` or better: use an `<svg>` with `<title>`          |

### Screen Reader Optimization

**Screen reader behavior patterns** — understand how each AT interprets your markup:

**Announcement order** (screen readers follow this sequence):

```
1. Page/region landmark (if entering a new landmark)
2. Element role (button, link, heading, etc.)
3. Accessible name (text content, aria-label, or aria-labelledby)
4. State (pressed, expanded, checked, disabled)
5. Value (for sliders, progress bars, etc.)
6. Description (aria-describedby — if present)
```

**Common screen reader pitfalls and fixes:**

```tsx
// ❌ PROBLEM: Screen reader announces "div" with no role
<div onClick={handleClick} tabIndex={0}>Click me</div>

// ✅ FIX: Use semantic element or explicit role
<button onClick={handleClick}>Click me</button>
// OR if div is structurally necessary:
<div role="button" onClick={handleClick} tabIndex={0}
     onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') handleClick(); }}>
  Click me
</div>

// ❌ PROBLEM: Icon-only button with no accessible name
<button><TrashIcon /></button>

// ✅ FIX: Provide accessible name
<button aria-label="Delete item"><TrashIcon aria-hidden="true" /></button>

// ❌ PROBLEM: Heading levels skip (h1 → h3)
<h1>Page Title</h1>
<h3>Section Title</h3>

// ✅ FIX: Maintain sequential heading hierarchy
<h1>Page Title</h1>
<h2>Section Title</h2>

// ❌ PROBLEM: Image with decorative icon announced
<svg class="icon"><path d="..."/></svg>

// ✅ FIX: Mark decorative images as such
<svg aria-hidden="true" focusable="false"><path d="..."/></svg>
// OR if the icon conveys meaning:
<svg role="img" aria-label="Warning"><path d="..."/></svg>
```

**Screen reader testing protocol:**

| Platform | Screen Reader   | Test Method                          | Key Commands                                                            |
| -------- | --------------- | ------------------------------------ | ----------------------------------------------------------------------- |
| iOS      | VoiceOver       | iPhone/iPad with VoiceOver enabled   | Swipe right/left, double-tap to activate, two-finger swipe to read all  |
| Android  | TalkBack        | Android device with TalkBack enabled | Swipe right/left, double-tap to activate, two-finger swipe to read all  |
| macOS    | VoiceOver       | Mac with VoiceOver enabled           | VO + Right/Left arrow, VO + Space to activate, VO + U for rotor         |
| Windows  | NVDA (free)     | Windows with NVDA installed          | Tab/Shift+Tab, Enter/Space to activate, Insert + Down Arrow to read all |
| Windows  | JAWS (licensed) | Windows with JAWS installed          | Tab/Shift+Tab, Enter/Space to activate, Insert + Down Arrow to read all |

**Testing checklist per component:**

- [ ] Component is reachable via screen reader navigation
- [ ] Role is announced correctly (button, link, heading, etc.)
- [ ] Accessible name is meaningful and matches visual label
- [ ] State changes are announced (expanded/collapsed, checked/unchecked)
- [ ] Dynamic content updates are announced (via aria-live or focus management)
- [ ] Component is operable via screen reader gestures (activate, dismiss, navigate)
- [ ] No silent elements (everything visible has an accessible equivalent)
- [ ] No redundant announcements (don't repeat information already in context)

### Keyboard Navigation Architecture

**Complete keyboard interaction model** — every interactive component must support:

| Key                | Action                                     | Applies To                                       |
| ------------------ | ------------------------------------------ | ------------------------------------------------ |
| `Tab`              | Move focus to next interactive element     | All interactive elements                         |
| `Shift + Tab`      | Move focus to previous interactive element | All interactive elements                         |
| `Enter`            | Activate/confirm                           | Buttons, links, form submissions, selected items |
| `Space`            | Toggle/activate                            | Buttons, checkboxes, toggles, selected items     |
| `Escape`           | Close/dismiss                              | Modals, dropdowns, tooltips, menus               |
| `Arrow Up/Down`    | Navigate list items                        | Lists, menus, comboboxes, radio groups           |
| `Arrow Left/Right` | Navigate tabs, sliders                     | Tab lists, sliders, carousels                    |
| `Home`             | Jump to first item                         | Lists, menus, tab lists                          |
| `End`              | Jump to last item                          | Lists, menus, tab lists                          |

**Focus management patterns:**

```tsx
// Modal focus trap — prevent focus from leaving the modal
function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      // Store current focus to restore later
      previousFocusRef.current = document.activeElement as HTMLElement;
      // Move focus into modal
      modalRef.current?.focus();
      // Trap focus
      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          onClose();
          return;
        }
        if (e.key !== 'Tab') return;

        const focusable = modalRef.current?.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (!focusable?.length) return;

        const first = focusable[0] as HTMLElement;
        const last = focusable[focusable.length - 1] as HTMLElement;

        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      };

      document.addEventListener('keydown', handleKeyDown);
      return () => document.removeEventListener('keydown', handleKeyDown);
    }
  }, [isOpen, onClose]);

  useEffect(() => {
    // Restore focus when modal closes
    if (!isOpen && previousFocusRef.current) {
      previousFocusRef.current.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div role="dialog" aria-modal="true" aria-labelledby="modal-title" ref={modalRef} tabIndex={-1}>
      <h2 id="modal-title">Modal Title</h2>
      {children}
    </div>
  );
}
```

**Skip navigation link** — mandatory for pages with repeated navigation:

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<style>
  .skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    padding: 8px 16px;
    background: #000;
    color: #fff;
    z-index: 100;
    transition: top 0.2s;
  }
  .skip-link:focus {
    top: 0;
  }
</style>
```

### ARIA Live Regions — Dynamic Content Announcements

**Live region strategy** — announce dynamic content changes without stealing focus:

```tsx
// Toast/notification announcement
function ToastAnnouncer({ message }: { message: string }) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only" // Visually hidden but announced by SR
    >
      {message}
    </div>
  );
}

// Loading state announcement
function LoadingAnnouncer({ isLoading, label }: { isLoading: boolean; label: string }) {
  return (
    <div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
      {isLoading ? `${label} is loading` : `${label} has finished loading`}
    </div>
  );
}

// Error announcement (assertive = interrupts current speech)
function ErrorAnnouncer({ error }: { error: string | null }) {
  if (!error) return null;
  return (
    <div role="alert" aria-live="assertive" aria-atomic="true" className="sr-only">
      {error}
    </div>
  );
}
```

**Live region guidelines:**

| Attribute     | Value           | Behavior                                             | Use Case                                       |
| ------------- | --------------- | ---------------------------------------------------- | ---------------------------------------------- |
| `aria-live`   | `polite`        | Announces when screen reader is idle                 | Status updates, loading states, search results |
| `aria-live`   | `assertive`     | Interrupts current announcement                      | Errors, warnings, time-sensitive alerts        |
| `aria-live`   | `off` (default) | No announcement                                      | —                                              |
| `aria-atomic` | `true`          | Announces entire region content                      | Single-message notifications                   |
| `aria-atomic` | `false`         | Announces only changed content                       | Live logs, chat messages                       |
| `role`        | `status`        | Implicit `aria-live="polite"`                        | Non-critical status information                |
| `role`        | `alert`         | Implicit `aria-live="assertive"`                     | Errors, warnings                               |
| `role`        | `log`           | Implicit `aria-live="polite"`, `aria-atomic="false"` | Chat logs, activity feeds                      |
| `role`        | `timer`         | Announces timer changes                              | Countdown timers, elapsed time                 |

**Common live region mistakes:**

- **Over-announcing:** updating a live region on every keystroke in a search box → debounce announcements or announce only final results
- **Under-announcing:** form validation errors that appear visually but aren't announced → use `role="alert"` with `aria-live="assertive"`
- **Empty regions:** rendering an empty live region → screen readers may announce nothing or announce stale content; remove the element entirely when there's nothing to announce
- **Focus stealing:** moving focus to announce content → use live regions instead; only move focus when the user explicitly navigates to new content

### axe-core Automation Integration

**CI pipeline integration:**

```js
// jest.config.js — axe-core integration with Jest
import { configureAxe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

const axe = configureAxe({
  rules: {
    // Override rule severity for specific patterns
    'color-contrast': { enabled: true },
    label: { enabled: true },
    'link-name': { enabled: true },
    'image-alt': { enabled: true },
    // Custom rule for domain-specific patterns
    'custom-focus-visible': {
      selector: 'button, [role="button"], [role="link"], a, input, select, textarea',
      tags: ['cat.keyboard'],
      none: ['custom-focus-visible-check'],
    },
  },
});

// Test every rendered component
test('Button component has no accessibility violations', async () => {
  const { container } = render(<Button>Click me</Button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

**axe-core in Storybook:**

```js
// .storybook/preview.js
export const parameters = {
  a11y: {
    config: {
      rules: [
        { id: 'color-contrast', enabled: true },
        { id: 'label', enabled: true },
      ],
    },
    options: {
      checks: { 'color-contrast': { shadowDOM: true } },
    },
  },
};
```

**Automated + manual testing split:**

| Testing Method                       | Catches                                                                                          | Misses                                                                                    | Frequency                         |
| ------------------------------------ | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | --------------------------------- |
| **axe-core (automated)**             | ~30-40% of WCAG issues: missing labels, color contrast, ARIA attribute errors, heading hierarchy | Logical flow, meaningful alt text, keyboard interaction quality, screen reader experience | Every PR (CI)                     |
| **Keyboard-only testing**            | Tab order, focus visibility, focus traps, keyboard interaction completeness                      | Screen reader announcements, voice control compatibility                                  | Every component before Stage 6    |
| **Screen reader testing**            | Announcement quality, reading order, live region behavior, component operability                 | Color contrast, text sizing                                                               | Quarterly + every major component |
| **User testing with disabled users** | Real-world usability, workflow barriers, assistive technology edge cases                         | —                                                                                         | At least once per release cycle   |

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                                             | Deliverable                                                  |
| ------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
| **Stage 2** (Web Prototype + IDS)    | Validate prototype against WCAG 2.1 AA; identify accessibility risks in IDS patterns       | Accessibility audit of prototype, accessibility notes in IDS |
| **Stage 3** (Architecture)           | Define accessibility architecture in UML; register ADRs for focus management patterns      | Accessibility ADRs                                           |
| **Stage 5** (Development)            | Implement accessible components; integrate axe-core into CI; conduct screen reader testing | Accessible codebase with automated a11y tests                |
| **Stage 6** (Code Review)            | Accessibility-focused code review: ARIA usage, keyboard navigation, focus management       | Accessibility section in DEFECT-REPORT.md                    |
| **Stage 8** (Integrity Verification) | Verify WCAG 2.1 AA compliance across all shipped components; run full a11y audit suite     | Accessibility integrity verification report                  |
| **Stage 10** (Release Readiness)     | Contribute to design sign-off (Item 2) confirming IDS accessibility requirements met       | Accessibility compliance sign-off                            |

## Quality Standards

| Metric                          | Target                                                                           | Enforcement                                          |
| ------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **WCAG 2.1 AA compliance**      | 100% of success criteria met                                                     | axe-core CI + manual audit; zero AA violations       |
| **axe-core automated tests**    | ≥ 30% of WCAG criteria covered automatically                                     | CI blocks on new violations                          |
| **Keyboard operability**        | 100% of functionality accessible via keyboard                                    | Manual keyboard testing checklist per component      |
| **Focus management**            | Zero orphaned focus, zero focus traps                                            | Modal/dropdown focus trap tests                      |
| **Screen reader compatibility** | VoiceOver + NVDA pass rate ≥ 95%                                                 | Quarterly AT testing report                          |
| **Color contrast**              | 4.5:1 for normal text, 3:1 for large text (AA); 7:1 / 4.5:1 (AAA where feasible) | axe-core `color-contrast` rule + manual verification |
| **Live region quality**         | Dynamic content announced within 2 seconds, no spam                              | Manual screen reader testing                         |
| **Skip navigation**             | Present on all pages with > 100 lines of content                                 | Manual audit                                         |
| **Form accessibility**          | 100% of inputs have visible labels + programmatic labels                         | axe-core `label` rule + manual audit                 |
| **Image accessibility**         | 100% of images have alt text or aria-hidden                                      | axe-core `image-alt` rule                            |
| **ARIA correctness**            | Zero ARIA role/property/state mismatches                                         | axe-core `aria-*` rules + manual review              |
| **Accessibility debt**          | Zero known a11y defects older than 2 sprints                                     | Defect tracking with a11y tag                        |
