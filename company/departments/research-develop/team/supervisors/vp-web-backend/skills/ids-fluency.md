---
name: ids-fluency
description: IDS (Interaction Design Specification) comprehension and design-engineering feasibility review — reading CDO deliverables, translating design intent into engineering constraints, surfacing implementation blockers during Stage 2–3 handoff, and maintaining design-engineering fidelity through Stage 5. Use when receiving an IDS from the CDO or when evaluating the engineering feasibility of a design specification.
version: "1.0.0"
---

# IDS Fluency

## Purpose

Read, interpret, and respond to the Interaction Design Specification (IDS) produced by CDO Yuki Tanaka-Chen at Stage 2. Elena Vasquez's role is not to redesign the IDS — that is the CDO's authority — but to identify engineering constraints early, surface implementation blockers before Stage 3 locks the UML package, and ensure the implementation in Stage 5 faithfully reflects the approved design.

## Why This Matters

Design-engineering misalignment is the most expensive defect in the company pipeline. A misunderstood animation spec discovered at Stage 6 Code Review requires UI rework, re-review by the CDO, and a re-run of the Stage 6 process. An IDS question raised at Stage 2 review costs 30 minutes. The same question raised at Stage 6 costs 2 weeks.

## IDS Anatomy — What to Read and Why

A CDO-authored IDS typically contains these sections. Elena reviews each for engineering impact:

| IDS Section                 | What It Contains                                                                     | Elena's Review Focus                                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| **Component Inventory**     | All new UI components with states (default, hover, active, disabled, error, loading) | Are any states non-trivial to implement? (e.g., animated state transitions requiring custom CSS/JS)               |
| **Interaction Flows**       | User journey diagrams, screen transition logic                                       | Does any flow require new API endpoints, real-time data, or complex state management?                             |
| **Responsive Breakpoints**  | Specified at ≥320px, 768px, 1024px, 1440px                                           | Does any layout require server-side rendering for SEO at the mobile breakpoint?                                   |
| **Animation Specs**         | Duration, easing, trigger, exit behavior for all animations                          | Do any animations require GPU-composited layers (`will-change`, `transform`) for performance?                     |
| **Design Tokens**           | Color, spacing, typography, radius, elevation values                                 | Are tokens already in the shared token library, or do new tokens need to be added to the design system?           |
| **Accessibility Notes**     | ARIA roles, focus management, screen reader requirements                             | Does any component require a custom ARIA implementation that has no native HTML equivalent?                       |
| **Performance Constraints** | LCP targets, interaction budgets (INP), animation frame rate targets                 | Are any performance targets tighter than the current baseline? Does achieving them require architectural changes? |

## Stage 2 → Stage 3 Feasibility Review

When Elena receives the IDS at Stage 2 completion, she produces a **Feasibility Review memo** within 3 business days. The memo has exactly two sections:

### 1. Engineering Complexity Flags

Items requiring additional implementation effort or architectural consideration:

```markdown
## Feasibility Review — [Project Name] IDS v[N]

**Reviewed by:** Elena Vasquez (VP Web-Backend)
**IDS version:** [version]
**Date:** YYYY-MM-DD

### Complexity Flags

| Component / Flow      | IDS Requirement                                     | Engineering Note                                                              | Estimated Impact               |
| --------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------ |
| Notification drawer   | Slide-in animation (300ms ease-out) + backdrop blur | `backdrop-filter` has GPU cost; verify on low-end Android WebView             | +0.5 sprint                    |
| Checkout address form | Inline validation with real-time suggestions        | Requires debounced API call to validation service; needs new endpoint         | +1 sprint; API team dependency |
| Dashboard metrics     | D3.js animated charts on first load                 | Chart animation must complete before LCP window; requires preloading strategy | Architecture discussion needed |
```

### 2. Clarification Requests

Specific questions for the CDO before Stage 3 locks the UML:

```markdown
### Clarification Requests (must resolve before Stage 3)

1. **Profile image upload** — the IDS shows a cropping modal on upload. Is the crop client-side only (canvas API), or does the server need to store the original? This determines whether we need a new media upload service.

2. **Empty state illustration** — animated SVG or static? If animated, specify the trigger (on-mount, on-scroll-into-view, looping?). The implementation differs significantly.
```

The CDO responds to clarifications; the responses are logged in the Stage 2 → Stage 3 decision record.

## Design Fidelity at Stage 5 and Stage 6

During Stage 5 (Software Development), Elena ensures the engineering team implements the IDS with fidelity:

- **Design tokens:** Every color, spacing, radius, or elevation value in the IDS must come from the shared token library — no hardcoded hex values in production code. Any discrepancy is flagged in PR review.
- **Animation parity:** Implementations are compared against IDS motion specs using browser dev tools (verify duration and easing match spec). Discrepancies >15% from spec require CDO notification.
- **Responsive review:** Before Stage 6, Elena runs the implementation against all specified breakpoints in Chrome DevTools. Any breakpoint that deviates from the IDS triggers a design review request to the CDO before the code review panel convenes.

## Quality Standards

- Feasibility Review memo delivered within 3 business days of IDS receipt
- Zero architecture-blocking discoveries after Stage 3 technology lock
- Zero hardcoded design values (colors, spacing, typography) in production code — all from shared tokens
- All IDS clarifications resolved and documented before Stage 3 UML sign-off
