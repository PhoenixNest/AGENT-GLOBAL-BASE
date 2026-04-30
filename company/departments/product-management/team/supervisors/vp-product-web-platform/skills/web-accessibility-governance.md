---
name: web-accessibility-governance
description: Implement and scale WCAG 2.1 AA accessibility standards across the full web product lifecycle — from PRD authorship through Stage 6 code review. Use when defining accessibility requirements, auditing compliance, or establishing governance processes that treat accessibility as a product-quality gate rather than a post-launch correction.
version: "1.0.0"
---

# Web Accessibility Governance

Julia Thorne (VP Web) treats accessibility as a core product quality gate — not a retrofit. This skill defines the standards, processes, and decision frameworks for integrating WCAG 2.1 AA compliance into every phase of the web product lifecycle.

---

## 1. WCAG 2.1 AA — Non-Negotiable Requirements

Every web product surface must satisfy the following baseline before Stage 6 sign-off:

### Perceivable

- **Text Alternatives:** All non-text content (images, icons, charts) must carry meaningful `alt` text. Decorative images use `alt=""`.
- **Color Contrast:** Minimum 4.5:1 for body text; 3:1 for large text (≥18pt regular or ≥14pt bold) and UI components.
- **Captions & Transcripts:** All pre-recorded audio/video must have synchronized captions; live video requires real-time captions.
- **Resize Text:** Content must remain readable and functional at 200% zoom without horizontal scrolling on viewports ≥320px wide.

### Operable

- **Keyboard Navigability:** Every interactive element (links, buttons, form fields, modals, carousels) is reachable and operable via keyboard alone. Focus must never be trapped.
- **Visible Focus Indicators:** All focusable elements carry a high-contrast focus ring (minimum 3:1 contrast ratio against adjacent background). Suppressing `:focus-visible` via CSS is a P1 defect.
- **Skip Navigation:** A "Skip to main content" link is present and is the first focusable element on every page.
- **No Seizure Hazards:** No content flashes more than 3 times per second.
- **Timeouts:** Any session timeout must warn the user at least 20 seconds in advance and allow an extension.

### Understandable

- **Form Error Handling:** Validation errors are identified in text (never by color alone), associated programmatically with the failing field via `aria-describedby`, and suggest a correction where possible.
- **Language Declaration:** The page `<html>` element carries the correct `lang` attribute; language switches within the page use `lang` on the containing element.
- **Consistent Navigation:** Navigation landmarks and labeling remain consistent across pages.

### Robust

- **Valid Semantics:** HTML validates against the W3C spec. ARIA roles, properties, and states are used correctly and never override native HTML semantics unnecessarily.
- **Screen Reader Compatibility:** All interactive flows must be smoke-tested against NVDA (Windows) + Chrome and VoiceOver (macOS/iOS) + Safari before Stage 6.

---

## 2. PRD Authorship — Accessibility Section

Every Web PRD authored by Julia or a PM teammate must include an **Accessibility Specification** block with the following structure:

```markdown
## Accessibility Specification

### Scope

[List all new or modified UI surfaces covered by this PRD.]

### WCAG 2.1 AA Baseline

[Confirm all surfaces meet the §1 non-negotiables.]

### Component-Level Notes

[For any custom components (date pickers, carousels, modals), specify the intended ARIA pattern from the ARIA Authoring Practices Guide.]

### Assistive Technology Smoke Tests

[Specify required screen reader / browser combinations for pre-launch testing.]

### Exclusions & Accepted Risks

[Any deviation from AA requires CPO sign-off and must be logged here with rationale and a remediation timeline.]
```

**PRD Gate:** A PRD without an Accessibility Specification block is incomplete and cannot advance to Stage 2.

---

## 3. Accessibility Audit Methodology

### Automated Scanning (CI/CD Gate)

- **Tooling:** `axe-core` integrated into the Playwright test suite; `Lighthouse` CI with an accessibility score threshold of ≥95.
- **Scope:** Every PR that touches web-facing UI must pass the automated accessibility gate before merge.
- **False Positive Protocol:** Suppressed rules must be documented with a code comment referencing the WCAG criterion, a rationale, and a JIRA ticket for follow-up.

### Manual Audit (Stage 6 Requirement)

Prior to Stage 6 sign-off, a manual audit is conducted for every new or significantly changed user journey:

| Step | Actor        | Action                                                             |
| ---- | ------------ | ------------------------------------------------------------------ |
| 1    | QA / PM      | Walk the journey using keyboard only — no mouse                    |
| 2    | QA / PM      | Walk the journey using NVDA + Chrome                               |
| 3    | QA / PM      | Walk the journey using VoiceOver + Safari (mobile)                 |
| 4    | QA / PM      | Verify all color contrast values using the WebAIM contrast checker |
| 5    | Julia Thorne | Review audit report; escalate any P0/P1 findings to CTO            |

**Accessibility finding severity** maps to the company's defect system:

| Severity | Definition                                             | Stage Impact                      |
| -------- | ------------------------------------------------------ | --------------------------------- |
| P0       | Legal risk (ADA/EAA) or complete screen-reader failure | Blocks Stage 6 sign-off           |
| P1       | Core journey broken for keyboard or AT users           | Blocks Stage 6 sign-off           |
| P2       | Degraded but navigable experience                      | Logged; user decides release gate |
| P3       | Best-practice refinement                               | Backlog; no release impact        |

---

## 4. Accessibility as Market Strategy

When authoring roadmap proposals or Stage 1 PRDs, Julia frames accessibility investments through three lenses:

1. **Regulatory Compliance** — EAA enforcement (EU, effective 2025), ADA Title III case law (US), and AODA (Canada). Non-compliance creates legal exposure that is categorically P0.
2. **Market Expansion** — 1.3 billion people globally live with a disability. Accessible products index higher in search (semantic HTML = SEO) and convert better across all demographics via reduced friction.
3. **Technical Quality Signal** — Accessible code is structurally sound code. Teams that consistently produce accessible output have lower defect rates across all quality dimensions — a DORA metric correlation Julia has documented at two previous companies.

---

## 5. Governance Cadence

| Cadence     | Activity                                                               | Owner       |
| ----------- | ---------------------------------------------------------------------- | ----------- |
| Per PR      | Automated axe-core + Lighthouse gate                                   | CI/CD       |
| Per Stage 6 | Manual audit for all new/changed journeys                              | QA + Julia  |
| Quarterly   | Full-site WCAG audit; update Accessibility Statement                   | Julia       |
| Annually    | Third-party VPAT (Voluntary Product Accessibility Template) assessment | Julia + CPO |

The **Accessibility Statement** (publicly posted) is owned by Julia and reviewed at every quarterly audit. Any deviation from AA status must be disclosed with a planned remediation date.
