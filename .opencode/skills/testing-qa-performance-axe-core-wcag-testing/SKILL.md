---
name: testing-qa-performance-axe-core-wcag-testing
description: axe-core WCAG accessibility testing — automated accessibility scanning for web and mobile, WCAG 2.1 AA rule validation, ARIA attribute verification, color contrast analysis, and accessibility defect reporting. Owned by Aisha Patel (VP Quality). Use during Stage 7 (Testing) for automated accessibility audit and Stage 10 (Release Readiness) for WCAG compliance sign-off. Trigger: axe-core testing, WCAG accessibility, automated a11y scanning, WCAG 2.1 AA, ARIA verification, color contrast, accessibility defects.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
---

# axe-core WCAG 2.1 AA Automated Accessibility Testing

## 1. Overview

### Purpose and Scope

axe-core is an open-source accessibility testing engine developed by Deque Systems. It performs automated accessibility checks against web content and mobile applications, identifying violations of WCAG 2.1 AA criteria. axe-core is the industry standard for automated accessibility testing and integrates with Jest, Playwright, Cypress, and custom test runners.

### What axe-core Detects (30–40% of Issues)

axe-core's automated engine catches approximately 30–40% of all accessibility issues. These are issues that can be detected programmatically:

- Missing or empty `alt` attributes on images
- Insufficient color contrast ratios
- Missing form input labels
- Invalid ARIA attribute usage
- Missing heading hierarchy
- Missing language attributes
- Duplicate IDs
- Missing document titles
- Empty interactive elements (buttons, links)
- Focus management issues

### What Requires Manual Testing (60–70% of Issues)

The remaining 60–70% of accessibility issues require human judgment or assistive technology testing:

- Keyboard navigation flow and logical tab order
- Screen reader compatibility and announcements
- Cognitive accessibility and content clarity
- Focus trap behavior in modals
- Meaningful alternative text (not just presence)
- Logical reading order
- Complex widget interaction patterns
- Video/audio captioning accuracy

### Relationship to Pipeline Stages

In the 10-stage development pipeline, axe-core testing is executed during:

- **Stage 7 (Automated Testing)**: axe-core tests run as part of the automated test suite. Results feed into the `TEST-RESULTS-REPORT.md`.
- **Stage 8 (Integrity Verification)**: Accessibility violations are classified using the P0–P3 defect severity system. P0/P1 accessibility defects (e.g., complete keyboard inaccessibility, screen reader blocking) are non-negotiable release blockers.

---

## 2. axe-core Configuration

### Basic Configuration

```javascript
import axe from "axe-core";

// Run axe with default configuration
const results = await axe.run(document, {
  runOnly: {
    type: "tag",
    values: ["wcag2a", "wcag2aa", "wcag21aa"],
  },
});
```

### Context Configuration

The context parameter determines which parts of the DOM to test. Use include/exclude arrays to target specific regions:

```javascript
const context = {
  include: [["#main-content"]],
  exclude: [["#third-party-widget"], ["#skip-nav"]],
};

const results = await axe.run(context);
```

### Custom Rule Configuration with axe.configure()

```javascript
axe.configure({
  rules: [
    {
      id: "custom-heading-level",
      selector: "h1, h2, h3, h4, h5, h6",
      tags: ["cat.structure", "best-practice"],
      metadata: {
        description: "Ensure heading levels increase sequentially",
        help: "Heading levels should not skip more than one level",
        helpUrl: "https://dequeuniversity.com/rules/axe/heading-levels",
      },
      any: ["heading-level"],
      all: [],
      none: [],
    },
  ],
  checks: [
    {
      id: "heading-level",
      evaluate: function (node) {
        const level = parseInt(node.tagName.charAt(1));
        const parentLevel = this.data?.parentLevel || 0;
        return level <= parentLevel + 1;
      },
    },
  ],
});
```

### Performance Tuning

```javascript
const results = await axe.run(context, {
  // Restrict which rules run
  runOnly: {
    type: "tag",
    values: ["wcag2a", "wcag21aa"],
  },
  // Limit execution time (milliseconds)
  elementRef: true,
  selectors: true,
  // Performance: exclude off-screen elements
  xpath: false,
  absolutePaths: false,
  // Skip performance-heavy rules if needed
  rules: {
    "color-contrast": { enabled: true },
    "duplicate-id": { enabled: true },
    label: { enabled: true },
    // Disable rules that are not relevant to your project
    marquee: { enabled: false },
    blink: { enabled: false },
  },
  // Impact level filtering (critical, serious, moderate, minor)
  resultTypes: ["violations", "passes", "incomplete"],
});
```

---

## 3. WCAG 2.1 AA Rule Coverage

### Automated Rules (axe-core detects these)

| WCAG Criterion               | axe-core Rule ID        | What It Checks                                    |
| ---------------------------- | ----------------------- | ------------------------------------------------- |
| 1.1.1 Non-text Content       | `image-alt`             | All images have `alt` attributes                  |
| 1.3.1 Info and Relationships | `label`                 | Form inputs have associated labels                |
| 1.3.1 Info and Relationships | `aria-required-attr`    | ARIA roles have required attributes               |
| 1.3.1 Info and Relationships | `aria-roles`            | ARIA roles are valid                              |
| 1.3.1 Info and Relationships | `list`                  | Lists are structured correctly                    |
| 1.3.4 Orientation            | `css-orientation-lock`  | No orientation lock via CSS                       |
| 1.3.5 Identify Input Purpose | `input-button-name`     | Input buttons have accessible names               |
| 1.4.1 Use of Color           | `color-contrast`        | Text has sufficient contrast ratio (4.5:1 for AA) |
| 1.4.3 Contrast (Minimum)     | `color-contrast`        | Same as above                                     |
| 1.4.4 Resize Text            | `meta-viewport`         | Viewport allows text scaling                      |
| 1.4.10 Reflow                | `meta-viewport`         | Viewport allows content reflow at 320px           |
| 1.4.11 Non-text Contrast     | `color-contrast`        | UI components have 3:1 contrast                   |
| 2.1.1 Keyboard               | `keyboard`              | Interactive elements are keyboard accessible      |
| 2.4.1 Bypass Blocks          | `bypass`                | Page has skip navigation mechanism                |
| 2.4.2 Page Titled            | `document-title`        | Document has a `<title>` element                  |
| 2.4.3 Focus Order            | `tabindex`              | No positive tabindex values                       |
| 2.4.4 Link Purpose           | `link-name`             | Links have accessible names                       |
| 2.4.5 Multiple Ways          | `meta-refresh`          | No auto-refresh without warning                   |
| 2.4.6 Headings and Labels    | `empty-heading`         | Headings are not empty                            |
| 2.4.6 Headings and Labels    | `heading-order`         | Heading levels are sequential                     |
| 3.3.2 Labels or Instructions | `label-title-only`      | Labels are not title-only                         |
| 4.1.1 Parsing                | `duplicate-id`          | No duplicate IDs                                  |
| 4.1.2 Name, Role, Value      | `aria-allowed-role`     | ARIA roles are used on correct elements           |
| 4.1.2 Name, Role, Value      | `aria-hidden-focus`     | Hidden elements are not focusable                 |
| 4.1.2 Name, Role, Value      | `aria-input-field-name` | ARIA input fields have accessible names           |

### Manual Review Rules (requires human testing)

| WCAG Criterion             | Manual Test                          | axe-core Support                                        |
| -------------------------- | ------------------------------------ | ------------------------------------------------------- |
| 1.1.1 Non-text Content     | Alternative text quality             | `alt` presence checked, quality requires human review   |
| 2.1.2 No Keyboard Trap     | Keyboard navigation flow             | No automated check for focus traps                      |
| 2.4.7 Focus Visible        | Visual focus indicator visibility    | Detected but quality requires human review              |
| 3.1.1 Language of Page     | Correct language identification      | `html[lang]` checked, correctness requires human review |
| 3.2.1 On Focus             | No unexpected context changes        | Requires human testing                                  |
| 3.3.1 Error Identification | Error messages are clear             | Requires human review                                   |
| 3.3.3 Error Suggestion     | Error messages provide solutions     | Requires human review                                   |
| 4.1.3 Status Messages      | ARIA live regions announce correctly | Partially detected; screen reader testing required      |

---

## 9. Stage 7/8 Integration

### Stage 7: Automated Testing Execution

axe-core accessibility tests are executed as part of the Stage 7 automated test suite. The Test Lead (Priscilla Oduya) ensures that:

1. **axe-core tests are included in the test suite** alongside unit, integration, and e2e tests.
2. **Results are captured in `TEST-RESULTS-REPORT.md`** with violation counts by severity.
3. **Accessibility defects are classified** using the P0–P3 severity system.

**Defect Classification for Accessibility Violations:**

| axe-core Impact | Pipeline Severity | Examples                                                                  |
| --------------- | ----------------- | ------------------------------------------------------------------------- |
| `critical`      | P0                | Complete keyboard inaccessibility, screen reader blocking errors          |
| `serious`       | P1                | Missing form labels, insufficient contrast on critical text, invalid ARIA |
| `moderate`      | P2                | Heading structure issues, missing skip navigation                         |
| `minor`         | P3                | Best practice violations, minor semantic improvements                     |

**Stage 7 Gate Criteria for axe-core:**

- All P0/P1 accessibility violations must be remediated.
- P2/P3 violations are presented to the user for fix/defer decision.
- axe-core test suite must pass with zero `critical` and `serious` violations.

### Stage 8: Integrity Verification

During Stage 8 Integrity Verification, the CTO panel (including the CSO) reviews accessibility compliance as part of the overall integrity check:

1. **Accessibility compliance is verified** against the SRD (Stage 1 Security Requirements Document) which includes WCAG 2.1 AA as a baseline.
2. **Regression testing** is run on all previously fixed accessibility defects.
3. **The "trim-to-pass" anti-pattern is guarded against** — removing functionality to avoid fixing accessibility defects is never valid remediation.

**Accessibility Gate Criteria (Stage 8):**

```markdown
## Accessibility Integrity Checklist

- [ ] All P0/P1 accessibility defects from Stage 6/7 are resolved
- [ ] axe-core test suite passes with zero critical/serious violations
- [ ] Manual accessibility testing completed for remaining 60-70% of WCAG criteria
- [ ] Screen reader testing performed on iOS (VoiceOver) and Android (TalkBack)
- [ ] Keyboard navigation tested across all user flows
- [ ] Color contrast verified for all text and UI components
- [ ] ARIA attributes validated across all interactive components
- [ ] Focus management verified in all modal/dialog flows
```

### Remediation SLA

| Severity      | Remediation Timeline                   | Re-testing Requirement                  |
| ------------- | -------------------------------------- | --------------------------------------- |
| P0 (critical) | Immediate — blocks all downstream work | Re-test within same session             |
| P1 (serious)  | Before Stage 7 completion              | Re-test before Stage 7 gate sign-off    |
| P2 (moderate) | User decision — fix now or defer       | If fixed, re-test in Stage 7 regression |
| P3 (minor)    | User decision — fix now or defer       | If fixed, re-test in Stage 7 regression |

---

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`4.-integration-patterns.md`](references/4.-integration-patterns.md) — 4. Integration Patterns
- [`5.-reporting-&-analysis.md`](references/5.-reporting-&-analysis.md) — 5. Reporting & Analysis
- [`6.-framework-specific-integration.md`](references/6.-framework-specific-integration.md) — 6. Framework-Specific Integration
- [`7.-false-positive-management.md`](references/7.-false-positive-management.md) — 7. False Positive Management
- [`8.-remediation-guidance.md`](references/8.-remediation-guidance.md) — 8. Remediation Guidance
- [`10.-references.md`](references/10.-references.md) — 10. References
