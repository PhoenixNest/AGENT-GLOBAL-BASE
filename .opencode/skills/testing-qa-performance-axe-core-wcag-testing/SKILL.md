---
name: testing-qa-performance-axe-core-wcag-testing
description: 'Testing Qa skill: Axe Core Wcag Testing'
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
import axe from 'axe-core';

// Run axe with default configuration
const results = await axe.run(document, {
  runOnly: {
    type: 'tag',
    values: ['wcag2a', 'wcag2aa', 'wcag21aa'],
  },
});
```

### Context Configuration

The context parameter determines which parts of the DOM to test. Use include/exclude arrays to target specific regions:

```javascript
const context = {
  include: [['#main-content']],
  exclude: [['#third-party-widget'], ['#skip-nav']],
};

const results = await axe.run(context);
```

### Custom Rule Configuration with axe.configure()

```javascript
axe.configure({
  rules: [
    {
      id: 'custom-heading-level',
      selector: 'h1, h2, h3, h4, h5, h6',
      tags: ['cat.structure', 'best-practice'],
      metadata: {
        description: 'Ensure heading levels increase sequentially',
        help: 'Heading levels should not skip more than one level',
        helpUrl: 'https://dequeuniversity.com/rules/axe/heading-levels',
      },
      any: ['heading-level'],
      all: [],
      none: [],
    },
  ],
  checks: [
    {
      id: 'heading-level',
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
    type: 'tag',
    values: ['wcag2a', 'wcag21aa'],
  },
  // Limit execution time (milliseconds)
  elementRef: true,
  selectors: true,
  // Performance: exclude off-screen elements
  xpath: false,
  absolutePaths: false,
  // Skip performance-heavy rules if needed
  rules: {
    'color-contrast': { enabled: true },
    'duplicate-id': { enabled: true },
    label: { enabled: true },
    // Disable rules that are not relevant to your project
    marquee: { enabled: false },
    blink: { enabled: false },
  },
  // Impact level filtering (critical, serious, moderate, minor)
  resultTypes: ['violations', 'passes', 'incomplete'],
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

## 4. Integration Patterns

### Jest Integration with jest-axe

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['@testing-library/jest-dom', 'jest-axe/extend-expect'],
  transform: {
    '^.+\\.jsx?$': 'babel-jest',
  },
};

// accessibility.test.jsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import MyComponent from './MyComponent';

expect.extend(toHaveNoViolations);

describe('MyComponent accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<MyComponent />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('passes specific WCAG criteria', async () => {
    const { container } = render(<MyComponent />);
    const results = await axe(container, {
      runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa'],
    });
    expect(results).toHaveNoViolations();
  });

  it('has no critical accessibility violations', async () => {
    const { container } = render(<MyComponent />);
    const results = await axe(container);
    const criticalViolations = results.violations.filter(
      (v) => v.impact === 'critical' || v.impact === 'serious'
    );
    expect(criticalViolations).toHaveLength(0);
  });
});
```

### Playwright Integration with axe-playwright

```javascript
// playwright-accessibility.test.js
import { test, expect } from '@playwright/test';
import { injectAxe, checkA11y, getViolations } from 'axe-playwright';

test.describe('Accessibility Tests', () => {
  test('homepage has no critical accessibility violations', async ({ page }) => {
    await page.goto('/');
    await injectAxe(page);

    const violations = await getViolations(page, null, {
      runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa'],
    });

    const criticalViolations = violations.filter(
      (v) => v.impact === 'critical' || v.impact === 'serious'
    );

    // Log all violations for reporting
    if (violations.length > 0) {
      console.log(`Found ${violations.length} accessibility violations:`);
      violations.forEach((v) => {
        console.log(`  [${v.impact}] ${v.id}: ${v.description}`);
        v.nodes.forEach((node) => {
          console.log(`    - ${node.html}`);
        });
      });
    }

    expect(criticalViolations).toHaveLength(0);
  });

  test('form page has accessible labels', async ({ page }) => {
    await page.goto('/form');
    await injectAxe(page);
    await checkA11y(page, null, {
      detailedReport: true,
      detailedReportOptions: { html: true },
    });
  });
});
```

### Cypress Integration with cypress-axe

```javascript
// cypress/e2e/accessibility.cy.js
describe('Accessibility Tests', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.injectAxe();
  });

  it('has no accessibility violations on homepage', () => {
    cy.checkA11y(
      null,
      {
        runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa'],
      },
      (violations) => {
        cy.log(`Found ${violations.length} accessibility violations`);
        violations.forEach((violation) => {
          cy.log(`[${violation.impact}] ${violation.id}: ${violation.description}`);
        });
      },
      true // detailedReport
    );
  });

  it('has no critical violations on form page', () => {
    cy.visit('/form');
    cy.checkA11y('#main-content', { runOnly: ['wcag2a', 'wcag2aa'] }, (violations) => {
      const critical = violations.filter((v) => v.impact === 'critical' || v.impact === 'serious');
      expect(critical).to.have.length(0);
    });
  });

  it('validates accessibility after user interaction', () => {
    cy.get('[data-testid="open-modal"]').click();
    cy.checkA11y('[role="dialog"]', {
      runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa'],
    });
  });
});
```

### CI/CD Pipeline Configuration

```yaml
# .github/workflows/accessibility.yml
name: Accessibility Testing

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  axe-core-a11y:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Serve application
        run: npx serve -s build -l 3000 &
        shell: bash

      - name: Wait for server
        run: npx wait-on http://localhost:3000 -t 30000

      - name: Run axe-core accessibility tests
        run: npx playwright test accessibility
        env:
          CI: true

      - name: Upload accessibility results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: accessibility-results
          path: test-results/accessibility/

      - name: Check for critical violations
        if: failure()
        run: |
          echo "Critical accessibility violations found."
          echo "These must be fixed before merge."
          echo "Review the accessibility-results artifact for details."
          exit 1
```

---

## 5. Reporting & Analysis

### axe-core Report Structure

axe-core returns a structured results object:

```javascript
{
  testEngine: {
    name: 'axe-core',
    version: '4.8.4',
  },
  testRunner: { name: 'axe' },
  testEnvironment: {
    orientationAngle: 0,
    orientationType: 'landscape-primary',
    userAgent: 'Mozilla/5.0...',
    windowWidth: 1280,
    windowHeight: 720,
  },
  timestamp: '2026-04-06T10:30:00.000Z',
  url: 'https://example.com',
  toolOptions: { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa'] } },
  passes: [ /* ... */ ],
  violations: [
    {
      id: 'color-contrast',
      impact: 'serious',
      tags: ['cat.color', 'wcag2aa', 'wcag143'],
      description: 'Ensures the contrast between foreground and background colors meets WCAG 2 AA minimum contrast ratio thresholds.',
      help: 'Elements must meet minimum color contrast ratio thresholds',
      helpUrl: 'https://dequeuniversity.com/rules/axe/4.8/color-contrast',
      nodes: [
        {
          any: [],
          all: [],
          none: [
            {
              id: 'color-contrast',
              impact: 'serious',
              message: 'Element has insufficient color contrast of 3.2 (foreground: #777777, background: #ffffff, font size: 10.5pt, font weight: normal). Expected contrast ratio: 4.5:1',
              data: {
                fgColor: '#777777',
                bgColor: '#ffffff',
                contrastRatio: 3.2,
                fontSize: '10.5pt',
                fontWeight: 'normal',
                expectedContrastRatio: '4.5:1',
              },
              relatedNodes: [
                {
                  html: '<p class="body-text">',
                  target: ['.body-text'],
                },
              ],
            },
          ],
          html: '<p class="body-text">Low contrast text</p>',
          target: ['.body-text'],
        },
      ],
    },
  ],
  incomplete: [ /* ... */ ],
  inapplicable: [ /* ... */ ],
}
```

### Violation Categorization by Impact

| Impact Level | WCAG Conformance                  | Release Pipeline Impact     |
| ------------ | --------------------------------- | --------------------------- |
| `critical`   | WCAG A failure                    | P0 — Non-negotiable fix     |
| `serious`    | WCAG AA failure                   | P1 — Non-negotiable fix     |
| `moderate`   | WCAG AAA failure or best practice | P2 — User decides fix/defer |
| `minor`      | Nice-to-have enhancement          | P3 — User decides fix/defer |

### Trend Analysis Script

```javascript
// scripts/a11y-trend-analysis.js
import fs from 'fs';
import path from 'path';

const RESULTS_DIR = './test-results/accessibility';

function analyzeTrends() {
  const files = fs.readdirSync(RESULTS_DIR).sort();
  const trends = [];

  for (const file of files) {
    const data = JSON.parse(fs.readFileSync(path.join(RESULTS_DIR, file), 'utf-8'));
    trends.push({
      date: file.replace('.json', ''),
      violations: data.violations.length,
      critical: data.violations.filter((v) => v.impact === 'critical').length,
      serious: data.violations.filter((v) => v.impact === 'serious').length,
      moderate: data.violations.filter((v) => v.impact === 'moderate').length,
      minor: data.violations.filter((v) => v.impact === 'minor').length,
    });
  }

  console.log('Accessibility Violation Trends:');
  console.log('--------------------------------');
  trends.forEach((t) => {
    console.log(
      `${t.date}: ${t.violations} total (critical: ${t.critical}, serious: ${t.serious}, moderate: ${t.moderate}, minor: ${t.minor})`
    );
  });

  const latest = trends[trends.length - 1];
  const previous = trends[trends.length - 2];

  if (previous) {
    const delta = latest.violations - previous.violations;
    console.log(`\nChange from previous: ${delta > 0 ? '+' : ''}${delta} violations`);
  }

  return trends;
}

analyzeTrends();
```

---

## 6. Framework-Specific Integration

### React: jest-axe and @axe-core/react

```javascript
// jest-axe setup with React Testing Library
import React from 'react';
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import Button from './Button';

expect.extend(toHaveNoViolations);

describe('Button accessibility', () => {
  it('renders with accessible label', async () => {
    const { container } = render(<Button>Submit</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('icon-only button has aria-label', async () => {
    const { container } = render(
      <Button aria-label="Close dialog">
        <CloseIcon />
      </Button>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});

// Runtime accessibility checking during development with @axe-core/react
import { checkA11y } from '@axe-core/react';

// In development mode only
if (process.env.NODE_ENV === 'development') {
  checkA11y();
}
```

### Angular: ngx-axe

```typescript
// app.module.ts
import { NgModule } from '@angular/core';
import { AxeModule } from 'ngx-axe';

@NgModule({
  imports: [
    AxeModule.forRoot({
      runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa'],
      // Exclude specific elements (e.g., third-party iframes)
      exclude: ['.third-party-widget'],
    }),
    // ... other imports
  ],
})
export class AppModule {}

// Component-level testing
import { TestBed } from '@angular/core/testing';
import { axe, toHaveNoViolations } from 'jest-axe';
import { render } from '@testing-library/angular';
import { MyComponent } from './my.component';

expect.extend(toHaveNoViolations);

describe('MyComponent', () => {
  it('should be accessible', async () => {
    const fixture = await render(MyComponent);
    const results = await axe(fixture.container);
    expect(results).toHaveNoViolations();
  });
});
```

### Vue: vue-axe

```javascript
// main.js
import { createApp } from 'vue';
import VueAxe from 'vue-axe';
import App from './App.vue';

const app = createApp(App);

app.use(VueAxe, {
  config: {
    runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa'],
  },
  manual: false, // Auto-inject and run on page load
  clearConsoleOnPass: false,
});

app.mount('#app');

// Component testing with vue-testing-library
import { render } from '@testing-library/vue';
import { axe, toHaveNoViolations } from 'jest-axe';
import MyComponent from './MyComponent.vue';

expect.extend(toHaveNoViolations);

describe('MyComponent accessibility', () => {
  it('has no violations', async () => {
    const { container } = render(MyComponent);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### Static Site Integration

```javascript
// For static sites, use axe-core directly with Puppeteer or Playwright
import { chromium } from 'playwright';
import axe from 'axe-core';

const INJECTED_SCRIPT = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf-8');

async function testPage(url) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(url);

  // Inject axe-core into the page
  await page.evaluate(INJECTED_SCRIPT);

  // Run axe-core and get results
  const results = await page.evaluate(() =>
    axe.run({
      runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa'],
    })
  );

  await browser.close();

  console.log(`Violations found: ${results.violations.length}`);
  results.violations.forEach((violation) => {
    console.log(`  [${violation.impact}] ${violation.id}: ${violation.description}`);
  });

  return results;
}

// Batch test multiple pages
const pages = ['/', '/about', '/contact', '/products'];
for (const page of pages) {
  await testPage(`https://example.com${page}`);
}
```

---

## 7. False Positive Management

### Rule Exclusion Strategies

```javascript
const results = await axe.run(context, {
  rules: {
    // Disable rules that are not applicable to your project
    marquee: { enabled: false },
    blink: { enabled: false },
    // Disable rules handled by third-party libraries
    'aria-allowed-role': { enabled: false },
  },
});
```

### Context-Based Ignoring

```javascript
const results = await axe.run({
  include: [['#main-content']],
  exclude: [
    // Exclude third-party widgets you cannot modify
    ['#google-maps-widget'],
    ['#stripe-payment-form'],
    // Exclude legacy code pending remediation
    ['#legacy-forms'],
  ],
});
```

### Impact Level Filtering

```javascript
function filterByImpact(results, minimumImpact) {
  const impactOrder = {
    minor: 1,
    moderate: 2,
    serious: 3,
    critical: 4,
  };

  const threshold = impactOrder[minimumImpact] || 0;

  return results.violations.filter((violation) => impactOrder[violation.impact] >= threshold);
}

// Only report serious and critical violations
const significantViolations = filterByImpact(results, 'serious');
```

### Team-Specific Rule Tuning by Platform

```javascript
// platform-specific rule configuration
const platformConfig = {
  android: {
    runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice'],
    rules: {
      'heading-order': { enabled: true },
      label: { enabled: true },
      'color-contrast': { enabled: true },
    },
  },
  ios: {
    runOnly: ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice'],
    rules: {
      'aria-allowed-role': { enabled: false }, // iOS uses different patterns
      'heading-order': { enabled: true },
      label: { enabled: true },
    },
  },
};

const config = platformConfig[currentPlatform];
const results = await axe.run(context, config);
```

### Managing Known Issues with Baseline Files

```javascript
// baseline-a11y-violations.json — track known violations pending remediation
{
  "last-updated": "2026-04-01",
  "known-violations": [
    {
      "id": "color-contrast",
      "component": "legacy-header",
      "impact": "moderate",
      "jira-ticket": "A11Y-042",
      "planned-fix": "2026-05-15",
    },
    {
      "id": "aria-required-attr",
      "component": "third-party-calendar",
      "impact": "serious",
      "vendor": "ExternalWidget Inc.",
      "planned-fix": "Waiting for vendor update",
    }
  ]
}

function compareWithBaseline(results, baselinePath) {
  const baseline = JSON.parse(fs.readFileSync(baselinePath, 'utf-8'));
  const newViolations = results.violations.filter((v) => {
    const isKnown = baseline['known-violations'].some(
      (known) => known.id === v.id
    );
    return !isKnown;
  });

  return {
    newViolations,
    knownViolations: results.violations.filter((v) =>
      baseline['known-violations'].some((known) => known.id === v.id)
    ),
  };
}
```

---

## 8. Remediation Guidance

### Missing Labels (WCAG 1.3.1, 3.3.2)

**Violation**: Form inputs without associated labels.

```html
<!-- ❌ BAD: Missing label -->
<input type="text" name="email" placeholder="Enter email" />

<!-- ✅ GOOD: Associated label with for/id -->
<label for="email-input">Email Address</label>
<input type="text" id="email-input" name="email" placeholder="Enter email" />

<!-- ✅ GOOD: Implicit label -->
<label>
  Email Address
  <input type="text" name="email" placeholder="Enter email" />
</label>

<!-- ✅ GOOD: ARIA label (when visible label is not appropriate) -->
<input type="text" name="search" aria-label="Search products" placeholder="Search" />
```

### Insufficient Color Contrast (WCAG 1.4.3)

**Violation**: Text contrast ratio is below 4.5:1 for AA (or 3:1 for large text).

```css
/* ❌ BAD: Contrast ratio 3.2:1 (below 4.5:1 threshold) */
.body-text {
  color: #777777;
  background-color: #ffffff;
}

/* ✅ GOOD: Contrast ratio 5.74:1 (above 4.5:1 threshold) */
.body-text {
  color: #595959;
  background-color: #ffffff;
}

/* ✅ GOOD: Large text (18pt or 14pt bold) requires 3:1 */
.large-heading {
  color: #767676;
  background-color: #ffffff;
  font-size: 1.5rem; /* 24px — qualifies as large text */
  font-weight: 700;
}
```

### ARIA Misconfiguration (WCAG 4.1.2)

**Violation**: ARIA roles used incorrectly or missing required attributes.

```html
<!-- ❌ BAD: button role on non-interactive element without keyboard support -->
<div role="button" onclick="handleClick()">Click me</div>

<!-- ✅ GOOD: Use native <button> element -->
<button type="button" onclick="handleClick()">Click me</button>

<!-- ❌ BAD: aria-labelledby pointing to non-existent element -->
<div aria-labelledby="missing-id">Content</div>

<!-- ✅ GOOD: aria-labelledby points to valid element -->
<h2 id="section-title">Section Title</h2>
<div aria-labelledby="section-title">Content</div>

<!-- ❌ BAD: aria-hidden on focusable element -->
<button aria-hidden="true">Invisible button</button>

<!-- ✅ GOOD: aria-hidden on non-interactive element only -->
<span aria-hidden="true">Decorative icon</span>
<button>
  <span aria-hidden="true">⭐</span>
  <span class="sr-only">Favorite this item</span>
</button>
```

### Empty Interactive Elements (WCAG 2.4.4, 4.1.2)

**Violation**: Buttons or links without accessible names.

```html
<!-- ❌ BAD: Empty button -->
<button type="button"><i class="icon-close"></i></button>

<!-- ✅ GOOD: Button with aria-label -->
<button type="button" aria-label="Close dialog">
  <i class="icon-close" aria-hidden="true"></i>
</button>

<!-- ✅ GOOD: Button with visible text (hidden visually but available to SR) -->
<button type="button">
  <i class="icon-close" aria-hidden="true"></i>
  <span class="sr-only">Close dialog</span>
</button>

<!-- ❌ BAD: Empty link -->
<a href="/details"></a>

<!-- ✅ GOOD: Link with text -->
<a href="/details">View product details</a>
```

### Heading Structure (WCAG 2.4.6, 1.3.1)

**Violation**: Heading levels skipped (e.g., h1 → h3).

```html
<!-- ❌ BAD: Heading level skipped (h1 → h3) -->
<h1>Main Title</h1>
<h3>Subsection</h3>

<!-- ✅ GOOD: Sequential heading levels -->
<h1>Main Title</h1>
<h2>Section Title</h2>
<h3>Subsection Title</h3>
<h4>Sub-subsection Title</h4>
```

### Focus Order (WCAG 2.4.3)

**Violation**: Positive tabindex values creating illogical focus order.

```html
<!-- ❌ BAD: Positive tabindex creates unnatural focus order -->
<input type="text" tabindex="5" />
<input type="text" tabindex="3" />
<input type="text" tabindex="1" />

<!-- ✅ GOOD: Use 0 or -1 for tabindex -->
<input type="text" tabindex="0" />
<!-- Natural DOM order -->
<input type="text" tabindex="0" />
<input type="text" tabindex="-1" />
<!-- Removed from tab order -->

<!-- CSS approach for visual reordering without breaking focus -->
.form-group { display: flex; flex-direction: column; /* Visual order matches DOM order */ }
```

### Duplicate IDs (WCAG 4.1.1)

**Violation**: Multiple elements with the same `id` attribute.

```html
<!-- ❌ BAD: Duplicate IDs -->
<div id="header-nav">...</div>
<div id="header-nav">...</div>

<!-- ✅ GOOD: Unique IDs -->
<div id="header-nav-primary">...</div>
<div id="header-nav-secondary">...</div>

<!-- ✅ GOOD: Use classes for shared styling -->
<div class="header-nav">...</div>
<div class="header-nav">...</div>
```

### Screen Reader Only Text Utility

```css
/* Visually hidden but available to screen readers */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Focusable when using keyboard */
.sr-only-focusable:focus {
  position: static;
  width: auto;
  height: auto;
  margin: 0;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

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

## 10. References

### Related Skills

- `advanced-a11y.md` — Advanced accessibility patterns, ARIA widget implementation, and screen reader testing methodology.
- `accessibility-testing-mobile.md` — Mobile-specific accessibility testing for iOS (VoiceOver) and Android (TalkBack) platforms.
- `wcag-mobile-compliance.md` — WCAG mobile compliance roadmap and platform-specific accessibility guidelines.

### External Resources

| Resource                    | URL                                           | Purpose                                                                         |
| --------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------- |
| axe-core Documentation      | https://github.com/dequelabs/axe-core         | Official axe-core API reference, rule documentation, and configuration guides   |
| Deque University            | https://dequeuniversity.com                   | Comprehensive accessibility training, rule explanations, and remediation guides |
| WCAG 2.1 AA Quick Reference | https://www.w3.org/WAI/WCAG21/quickref/       | Official W3C WCAG 2.1 AA success criteria with techniques and examples          |
| ARIA Authoring Practices    | https://www.w3.org/WAI/ARIA/apg/              | Patterns for accessible custom widgets with code examples                       |
| WebAIM Contrast Checker     | https://webaim.org/resources/contrastchecker/ | Quick contrast ratio calculation tool                                           |
| axe Browser Extension       | https://www.deque.com/axe/browser-extensions/ | Free axe-core browser extension for manual accessibility testing                |
| axe DevTools                | https://www.deque.com/axe/devtools/           | Professional accessibility testing IDE integration                              |

### axe-core Rule Reference

For the complete list of axe-core rules and their WCAG mappings, see the official documentation:
https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md

### WCAG 2.1 AA Conformance Checklist

- [ ] 1.1.1 Non-text Content — All non-text content has text alternatives
- [ ] 1.3.1 Info and Relationships — Information and relationships conveyed through presentation can be programmatically determined
- [ ] 1.3.2 Meaningful Sequence — When the sequence affects meaning, a programmatically determinable reading sequence is available
- [ ] 1.3.4 Orientation — Content does not restrict view to portrait or landscape
- [ ] 1.3.5 Identify Input Purpose — Input purpose can be programmatically determined
- [ ] 1.4.1 Use of Color — Color is not the only visual means of conveying information
- [ ] 1.4.3 Contrast (Minimum) — Text has contrast ratio of at least 4.5:1
- [ ] 1.4.4 Resize Text — Text can be resized up to 200% without assistive technology
- [ ] 1.4.10 Reflow — Content can be presented at 320px width without horizontal scrolling
- [ ] 1.4.11 Non-text Contrast — UI components have contrast ratio of at least 3:1
- [ ] 1.4.12 Text Spacing — No loss of content when text spacing is adjusted
- [ ] 1.4.13 Content on Hover or Focus — Additional content can be dismissed
- [ ] 2.1.1 Keyboard — All functionality operable through keyboard interface
- [ ] 2.1.2 No Keyboard Trap — Focus can be moved away from component using keyboard
- [ ] 2.4.1 Bypass Blocks — Mechanism to bypass repeated content blocks
- [ ] 2.4.2 Page Titled — Web pages have titles describing topic or purpose
- [ ] 2.4.3 Focus Order — Components receive focus in meaningful order
- [ ] 2.4.4 Link Purpose — Purpose of each link can be determined from link text
- [ ] 2.4.5 Multiple Ways — More than one way to locate a web page
- [ ] 2.4.6 Headings and Labels — Headings and labels describe topic or purpose
- [ ] 2.4.7 Focus Visible — Keyboard focus indicator is always visible
- [ ] 3.1.1 Language of Page — Default human language can be programmatically determined
- [ ] 3.1.2 Language of Parts — Human language of each passage can be programmatically determined
- [ ] 3.2.1 On Focus — Receiving focus does not initiate change of context
- [ ] 3.2.2 On Input — Changing setting does not initiate change of context
- [ ] 3.2.3 Consistent Navigation — Navigational mechanisms repeated in same order
- [ ] 3.2.4 Consistent Identification — Components with same functionality identified consistently
- [ ] 3.3.1 Error Identification — Input error detected, error described to user
- [ ] 3.3.2 Labels or Instructions — Labels or instructions provided for content input
- [ ] 3.3.3 Error Suggestion — Input error detected, suggestion provided
- [ ] 3.3.4 Error Prevention — For legal/financial/data entries, submissions are reversible
- [ ] 4.1.1 Parsing — HTML is valid (IDs unique, elements nested correctly)
- [ ] 4.1.2 Name, Role, Value — For all UI components, name and role can be programmatically determined
- [ ] 4.1.3 Status Messages — Status messages can be programmatically determined through role or properties

---

_This skill is maintained by the Testing & QA department. For questions about axe-core configuration or accessibility testing strategy, contact Test Lead Priscilla Oduya or the SDET team._
