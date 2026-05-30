---
name: axe-core-wcag-testing
description: Automated WCAG 2.1 AA accessibility testing using axe-core — CI/CD integration, Playwright and Cypress rule configuration, suppression governance, Lighthouse CI accessibility gates, and release-blocking criteria for accessibility failures. Use at Stage 7 (Automated Testing) and Stage 8 (Integrity Verification) to enforce accessibility quality gates.
version: "1.0.0"
---

# axe-core WCAG 2.1 AA Test Suite

## Purpose

Enforce WCAG 2.1 AA accessibility compliance through automated testing integrated into the CI/CD pipeline. Accessibility quality is not a CDO concern alone — it is an engineering quality gate that Aisha Patel owns at Stage 7 (Automated Testing) and Stage 8 (Integrity Verification). Any accessibility regression that escapes to production is classified as a P1 defect and blocks the next release.

## Why This Matters

The company's WCAG 2.1 AA commitment (owned by Julia Thorne, VP Web) requires automated gate enforcement in engineering, not only manual audits. Automated testing with axe-core catches approximately 57% of WCAG issues mechanically. The remaining 43% require manual audit (see Julia's `web-accessibility-governance.md`). The automated gate is the engineering organization's responsibility; the manual audit is shared with the CDO and VP Web.

## axe-core Integration Pattern

### Playwright + axe-core (Primary Pattern)

```typescript
// tests/accessibility/a11y.spec.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test.describe("Accessibility — WCAG 2.1 AA", () => {
  test("home page has no WCAG 2.1 AA violations", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test("checkout flow — each step is accessible", async ({ page }) => {
    const steps = ["/checkout/cart", "/checkout/shipping", "/checkout/payment"];
    for (const step of steps) {
      await page.goto(step);
      const results = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
        .analyze();
      expect(results.violations, `Violations on ${step}`).toEqual([]);
    }
  });
});
```

### Cypress + axe-core (Alternative — legacy web pipelines)

```javascript
// cypress/support/commands.js
import "cypress-axe";

// cypress/e2e/accessibility.cy.js
describe("WCAG 2.1 AA — Critical Pages", () => {
  beforeEach(() => {
    cy.injectAxe();
  });

  it("dashboard page passes axe", () => {
    cy.visit("/dashboard");
    cy.checkA11y(null, {
      runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21aa"] },
    });
  });
});
```

## CI/CD Gate Configuration

### Gate Rules

| Gate Level             | Trigger                         | Blocking?                               | Rule                                                   |
| ---------------------- | ------------------------------- | --------------------------------------- | ------------------------------------------------------ |
| PR gate                | Every PR touching web-facing UI | Yes — violations block merge            | Zero new violations vs. main branch baseline           |
| Nightly gate           | Full-site axe scan              | Yes — violations create P1 Jira tickets | Zero total violations in WCAG 2.1 AA ruleset           |
| Release gate (Stage 7) | Pre-release build               | Yes — blocks Stage 8 advancement        | Zero violations AND Lighthouse accessibility score ≥95 |

### Lighthouse CI Integration

```yaml
# .lighthouserc.yml
ci:
  collect:
    url:
      - https://staging.app/
      - https://staging.app/dashboard
      - https://staging.app/checkout
    numberOfRuns: 3
  assert:
    preset: "lighthouse:recommended"
    assertions:
      accessibility:
        minScore: 0.95
        aggregationMethod: pessimistic
  upload:
    target: temporary-public-storage
```

## Suppression Governance

A suppressed violation is a documented exception — it is never silent. Every suppression requires:

```typescript
const results = await new AxeBuilder({ page })
  .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
  .exclude("#third-party-widget") // JIRA-2847: Third-party widget, no source access — remediation Q3 2026
  .analyze();
```

**Suppression registry** (maintained by Aisha in Confluence):

| Suppression ID | Rule Suppressed | Scope           | Justification                           | Owner    | Expiry     |
| -------------- | --------------- | --------------- | --------------------------------------- | -------- | ---------- |
| AXE-001        | color-contrast  | `#legacy-chart` | Legacy charting lib — replacement in Q3 | Elena V. | 2026-09-01 |

Suppressions that exceed their expiry date are automatically escalated to P2 defects and added to the sprint backlog.

## Violation Severity Mapping

axe-core impact levels map to the company's defect classification:

| axe-core Impact | Company Severity | Release Gate Impact               |
| --------------- | ---------------- | --------------------------------- |
| Critical        | P0               | Blocks Stage 7 immediately        |
| Serious         | P1               | Blocks Stage 7                    |
| Moderate        | P2               | Logged; user decides release gate |
| Minor           | P3               | Backlog; no gate impact           |

## Quality Standards

- Zero `critical` or `serious` axe-core violations on all web-facing routes before Stage 7 advancement
- Lighthouse CI accessibility score ≥95 on all audited pages
- Suppression registry reviewed at every Stage 6 Code Review — expired suppressions are P2 defects
- 100% of new web UI routes covered by at least one axe-core test within the same sprint they ship
