---
name: testing-qa-mobile-visual-regression-testing
description: Visual regression testing for mobile apps — pixel-perfect UI comparison, screenshot diffing, cross-device visual validation, Percy/Applitools integration, and design fidelity verification against IDS specifications. Owned by Priya Sharma (SDET). Use during Stage 6 (Code Review) for visual baseline establishment and Stage 8 (Integrity Verification) for design fidelity re-verification. Trigger: visual regression testing, screenshot diffing, pixel comparison, Percy, Applitools, cross-device visual testing, design fidelity, IDS verification.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
---

# Visual Regression Testing

## Overview

Visual regression testing detects unintended UI changes by comparing screenshots of the application under test against a known-good baseline ("golden master"). Unlike functional testing which validates behavior, visual regression testing validates _appearance_ — pixel-level fidelity to the expected visual state.

### When to Use

| Scenario                      | Visual Regression Applicable? | Rationale                                     |
| ----------------------------- | ----------------------------- | --------------------------------------------- |
| CSS/style changes             | Yes                           | Directly impacts rendered output              |
| Component refactor            | Yes                           | Layout shifts may not be caught by unit tests |
| Dependency upgrades (UI libs) | Yes                           | Library updates may change default styles     |
| Responsive breakpoint changes | Yes                           | Layout at specific widths must be verified    |
| Localization/i18n changes     | Yes                           | Text expansion may break layouts              |
| Backend-only changes          | No                            | No expected visual impact                     |
| Test-only changes             | No                            | No production code changes                    |

### Pipeline Integration Points

| Pipeline Stage                   | Visual Regression Activity                                    |
| -------------------------------- | ------------------------------------------------------------- |
| Stage 7 — Automated Testing      | Execute visual regression suite; generate diff reports        |
| Stage 8 — Integrity Verification | Verify no unauthorized visual deviations from approved design |
| Stage 9 — i18n Engineering       | Verify localized UI renders correctly in all target languages |
| Stage 10 — Release Readiness     | Final visual sign-off against design specification            |

### Key Metrics

| Metric                  | Target                       | Enforcement                                      |
| ----------------------- | ---------------------------- | ------------------------------------------------ |
| Baseline coverage       | 100% of user-facing screens  | Tracked in visual test manifest                  |
| False positive rate     | < 2%                         | Achieved via threshold tuning and ignore regions |
| Review turnaround       | < 24 hours for new baselines | Enforced by CI/CD SLA                            |
| Diff detection accuracy | > 95% true positives         | Validated through seeded regression tests        |

---

## Screenshot Capture Strategies

### Golden Master Baseline

The golden master is the authoritative reference screenshot set against which all future captures are compared.

**Baseline Creation Workflow:**

1. Deploy the approved build to a stable test environment
2. Execute visual test suite with `update-baseline` flag
3. Review each captured screenshot for visual correctness
4. Commit baseline images to version-controlled baseline repository
5. Tag baseline with corresponding git SHA and build version

**Baseline Storage Structure:**

```
baselines/
├── android/
│   ├── pixel-7-api-33/
│   │   ├── home-screen.png
│   │   ├── settings-screen.png
│   │   └── login-screen.png
│   └── galaxy-s23-api-33/
│       ├── home-screen.png
│       └── settings-screen.png
├── ios/
│   ├── iphone-15-ios-17/
│   │   ├── home-screen.png
│   │   └── settings-screen.png
│   └── ipad-air-ios-17/
│       └── home-screen.png
└── web/
    ├── chrome-1920x1080/
    │   └── dashboard.png
    └── safari-375x812/
        └── dashboard.png
```

**Baseline Update Rules:**

| Rule               | Description                                      |
| ------------------ | ------------------------------------------------ |
| Atomic updates     | Update baselines for a single feature/PR only    |
| Review required    | Every new baseline must be reviewed and approved |
| Changelog entry    | Document what changed and why                    |
| No blanket updates | Never update all baselines in a single commit    |

### Device Matrix Capture

Capture screenshots across a representative matrix of devices, OS versions, and screen densities.

**Minimum Device Matrix for Mobile:**

| Platform | Device                        | OS Version          | Screen Density | Rationale                  |
| -------- | ----------------------------- | ------------------- | -------------- | -------------------------- |
| Android  | Pixel 7                       | API 33 (Android 13) | 420 dpi        | Reference Android device   |
| Android  | Samsung Galaxy S23            | API 33 (Android 13) | 450 dpi        | OEM skin variation         |
| Android  | Low-end device (e.g., Moto G) | API 30 (Android 11) | 280 dpi        | Minimum supported version  |
| iOS      | iPhone 15                     | iOS 17              | 460 dpi        | Reference iOS device       |
| iOS      | iPhone SE (3rd gen)           | iOS 17              | 326 dpi        | Small screen / notchless   |
| iOS      | iPad Air                      | iPadOS 17           | 264 dpi        | Tablet layout verification |

**Capture Timing:**

| Event             | Capture Trigger                          |
| ----------------- | ---------------------------------------- |
| Baseline creation | After design sign-off (Stage 2 approval) |
| Pre-merge         | Every PR targeting UI changes            |
| Post-merge        | Nightly regression on main branch        |
| Release candidate | Full matrix before Stage 10 sign-off     |

### State-Based Capture

UI must be captured in multiple interaction states, not just the default rendered view.

**Required States Per Screen:**

| State         | Description                           | Example                       |
| ------------- | ------------------------------------- | ----------------------------- |
| Default       | Initial load with no user interaction | Empty list view               |
| Loading       | Skeleton/progress indicator visible   | Spinner during API call       |
| Populated     | Full data loaded                      | List with 20+ items           |
| Error         | Error state displayed                 | Network failure message       |
| Empty         | No data available                     | "No results found"            |
| Interaction   | Active user gesture                   | Button pressed, menu expanded |
| Edge cases    | Extreme content length                | Very long text, large images  |
| Accessibility | With screen reader focus indicators   | Highlighted focus ring        |

**State Transition Capture Strategy:**

```
Screen A (Default)
  ├── User taps button → Capture During Interaction
  │   ├── Loading state appears → Capture
  │   └── Result state → Capture
  └── Error occurs → Capture Error State

Each transition point is a screenshot opportunity.
Automate via deterministic state seeding (mock data, fixed clocks).
```

**Deterministic State Seeding:**

| Technique                     | Purpose                          | Implementation                                      |
| ----------------------------- | -------------------------------- | --------------------------------------------------- |
| Mock API responses            | Consistent data across captures  | Return fixed JSON fixtures                          |
| Time freezing                 | Eliminate time-dependent UI      | Freeze `Date.now()` to fixed value                  |
| Font scaling override         | Prevent dynamic type variation   | Force specific font size setting                    |
| Locale forcing                | Consistent text direction/length | Force `en-US` for baseline, test locales separately |
| Network throttling simulation | Consistent loading states        | Mock network delay in test harness                  |

---

## Tool Selection

### Comparison Matrix

| Tool           | Type         | Platform Support                            | Pricing             | Open Source | CI/CD Integration                 | AI Features         | Baseline Storage   |
| -------------- | ------------ | ------------------------------------------- | ------------------- | ----------- | --------------------------------- | ------------------- | ------------------ |
| **Percy**      | SaaS         | Web, React, Vue, Ember, Cypress, Playwright | Paid (tiered)       | No          | Native (GitHub, GitLab, CircleCI) | No                  | Cloud-hosted       |
| **Applitools** | SaaS + SDK   | Web, Mobile Native, Desktop, PDF            | Paid (enterprise)   | No          | Native (all major CI)             | Eyes AI (visual AI) | Cloud-hosted       |
| **BackstopJS** | CLI + Engine | Web (Puppeteer/Playwright)                  | Free                | Yes         | Manual config required            | No                  | Local/remote       |
| **Chromatic**  | SaaS         | Storybook (React, Vue, Angular)             | Paid (free for OSS) | Partial     | Native (GitHub Actions)           | No                  | Cloud-hosted       |
| **Playwright** | Framework    | Web, Android, iOS                           | Free                | Yes         | Native                            | No                  | Local/CI artifacts |
| **Maestro**    | Framework    | Mobile Native (Android, iOS)                | Free (cloud paid)   | Partial     | Native (CI + Cloud)               | Maestro Cloud       | Local/Cloud        |

### Detailed Tool Evaluation

**Percy (BrowserStack):**

| Aspect             | Rating                                                              | Notes                                       |
| ------------------ | ------------------------------------------------------------------- | ------------------------------------------- |
| Setup complexity   | Low                                                                 | SDK integration + CI config                 |
| Diff accuracy      | High                                                                | DOM snapshot approach reduces noise         |
| Review workflow    | Excellent                                                           | In-browser diff review with comment/approve |
| Team collaboration | Excellent                                                           | Role-based permissions, team review         |
| Best for           | Teams wanting managed visual regression with minimal infrastructure |

**Applitools Eyes:**

| Aspect             | Rating                                                   | Notes                                              |
| ------------------ | -------------------------------------------------------- | -------------------------------------------------- |
| Setup complexity   | Medium                                                   | SDK per platform + Eyes server config              |
| Diff accuracy      | Very High                                                | AI-powered visual matching reduces false positives |
| Review workflow    | Excellent                                                | Ultrafast Test Grid, batch analysis                |
| Team collaboration | Excellent                                                | Enterprise-grade with audit trails                 |
| Best for           | Enterprise teams with budget for best-in-class visual AI |

**BackstopJS:**

| Aspect             | Rating                                                      | Notes                                             |
| ------------------ | ----------------------------------------------------------- | ------------------------------------------------- |
| Setup complexity   | Medium                                                      | Requires config file + Puppeteer/Playwright setup |
| Diff accuracy      | Medium-High                                                 | Depends on pixelmatch configuration               |
| Review workflow    | Basic                                                       | CLI output + HTML report                          |
| Team collaboration | Basic                                                       | Self-hosted, no built-in team features            |
| Best for           | Budget-conscious teams comfortable with self-hosted tooling |

**Chromatic:**

| Aspect             | Rating                                                  | Notes                                      |
| ------------------ | ------------------------------------------------------- | ------------------------------------------ |
| Setup complexity   | Low                                                     | Storybook addon + CI integration           |
| Diff accuracy      | High                                                    | Component-level isolation reduces noise    |
| Review workflow    | Excellent                                               | GitHub PR integration with inline comments |
| Team collaboration | Excellent                                               | Built for component teams                  |
| Best for           | Teams already using Storybook for component development |

**Playwright (Native):**

| Aspect             | Rating                                                    | Notes                                                          |
| ------------------ | --------------------------------------------------------- | -------------------------------------------------------------- |
| Setup complexity   | Medium                                                    | Requires custom visual comparison logic or third-party service |
| Diff accuracy      | Configurable                                              | Use `toHaveScreenshot()` with pixelmatch backend               |
| Review workflow    | Basic                                                     | Built-in diff output; enhance with Percy/Applitools            |
| Team collaboration | Depends on setup                                          | Requires CI integration for team workflow                      |
| Best for           | Teams wanting framework flexibility and no vendor lock-in |

### Selection Decision Tree

```
Is the team using Storybook?
  ├── Yes → Chromatic
  └── No →
      Has dedicated visual testing budget?
        ├── Yes ($$$) → Applitools Eyes (AI-powered, most accurate)
        ├── Yes ($$) → Percy (managed, good UX, broad support)
        └── No (free/open-source) →
            Testing web only?
              ├── Yes → BackstopJS or Playwright toHaveScreenshot
              └── No (mobile native) →
                  Playwright for mobile web
                  + Maestro for native screens
                  + custom pixel comparison
```

---

## Failed Comparisons

| Screen          | Device    | Diff % | Severity | Status   |
| --------------- | --------- | ------ | -------- | -------- |
| Homepage hero   | Pixel 7   | 3.2%   | P1       | Open     |
| Settings toggle | iPhone 15 | 0.08%  | P3       | Deferred |
| ...             | ...       | ...    | ...      | ...      |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`pixel-diff-analysis.md`](references/pixel-diff-analysis.md) — Pixel Diff Analysis
- [`responsive-layout-verification.md`](references/responsive-layout-verification.md) — Responsive Layout Verification
- [`ci-cd-integration.md`](references/ci-cd-integration.md) — CI/CD Integration
- [`cross-device-testing.md`](references/cross-device-testing.md) — Cross-Device Testing
- [`performance-considerations.md`](references/performance-considerations.md) — Performance Considerations
- [`stage-7-8-integration.md`](references/stage-7-8-integration.md) — Stage 7/8 Integration
- [`summary.md`](references/summary.md) — Summary
- [`classification-summary.md`](references/classification-summary.md) — Classification Summary
- [`panel-assessment.md`](references/panel-assessment.md) — Panel Assessment
- [`unresolved-visual-defects.md`](references/unresolved-visual-defects.md) — Unresolved Visual Defects
- [`overall-verdict.md`](references/overall-verdict.md) — Overall Verdict
- [`references.md`](references/references.md) — References
