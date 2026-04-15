---
name: visual-regression-testing
description: Visual regression testing detects unintended UI changes by comparing screenshots of the application under test against a known-good baseline ("golden master").
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

## Pixel Diff Analysis

### Threshold Configuration

Pixel diff thresholds determine what constitutes a meaningful visual change versus acceptable rendering variance.

**Threshold Levels:**

| Threshold | Pixel Change Tolerance | Use Case                           | False Positive Rate | False Negative Risk   |
| --------- | ---------------------- | ---------------------------------- | ------------------- | --------------------- |
| Strict    | 0.00% - 0.05%          | Pixel-perfect brand UI, typography | Low                 | High (font rendering) |
| Normal    | 0.05% - 0.5%           | General UI components              | Medium              | Low                   |
| Relaxed   | 0.5% - 2.0%            | Canvas/WebGL content, animations   | High                | Very Low              |

**Recommended Configuration:**

```yaml
visual-regression:
  thresholds:
    default: 0.1% # 0.1% pixel difference tolerance
    strict: 0.02% # For brand-critical screens
    relaxed: 1.0% # For dynamic content areas
  comparison:
    method: pixelmatch # Algorithm: pixelmatch, resemble, odiff
    alpha: 0.1 # Opacity of diff overlay
    threshold: 0.1 # Per-pixel sensitivity (0-1)
    includeAA: false # Ignore anti-aliasing differences
    ignoreAntialiasing: true # Reduce false positives from font rendering
  output:
    diff-format: png
    diff-color: ff0066 # Magenta diff highlights
```

### Ignore Regions

Define regions of the screenshot that should be excluded from comparison due to expected variance.

**Ignore Region Types:**

| Region Type            | Examples                             | Ignore Strategy                       |
| ---------------------- | ------------------------------------ | ------------------------------------- |
| Dynamic content        | Timestamps, user avatars, live feeds | Full region exclusion via coordinates |
| Animations             | Loading spinners, transitions        | Exclude animated elements             |
| System UI              | Status bar, navigation bar           | Exclude platform-specific chrome      |
| Third-party content    | Ads, embedded maps                   | Exclude external iframes              |
| User-generated content | Comments, posts                      | Mask content area                     |

**Region Definition (Rectangle-based):**

```json
{
  "ignoreRegions": [
    {
      "name": "status-bar",
      "coordinates": { "x": 0, "y": 0, "width": 1080, "height": 80 }
    },
    {
      "name": "timestamp-area",
      "selector": ".message-timestamp"
    },
    {
      "name": "scrollable-content",
      "selector": ".feed-list",
      "mode": "ignore-all"
    }
  ]
}
```

**Selector-based vs. Coordinate-based Regions:**

| Approach              | Advantages                             | Disadvantages             | Best For                        |
| --------------------- | -------------------------------------- | ------------------------- | ------------------------------- |
| CSS/XPath selectors   | Responsive to layout changes           | Requires accessible DOM   | Web, React Native with test IDs |
| Coordinate rectangles | Precise, tool-agnostic                 | Breaks on layout changes  | Mobile native screens           |
| AI-powered masking    | Automatic detection of dynamic content | Requires ML model, slower | Complex dynamic screens         |

### False Positive Reduction

False positives erode team trust in visual regression gating. Minimize them systematically.

**Common False Positive Causes and Mitigations:**

| Cause                             | Mitigation                                             | Expected Reduction |
| --------------------------------- | ------------------------------------------------------ | ------------------ |
| Anti-aliasing differences         | `ignoreAntialiasing: true`                             | 40-60% reduction   |
| Sub-pixel rendering variance      | Increase threshold to 0.1%                             | 20-30% reduction   |
| Font rendering across OS versions | Ignore text rendering regions or use relaxed threshold | 30-50% reduction   |
| Shadow/glow rendering differences | Use structural similarity (SSIM) comparison            | 15-25% reduction   |
| Image compression artifacts       | Use lossless PNG for all captures                      | Near 0%            |
| Hardware acceleration differences | Force software rendering in test environment           | 10-20% reduction   |
| Network-dependent assets          | Pre-bundle all assets in test build                    | Near 0%            |

**Validation Checklist Before Gate Enforcement:**

1. Run baseline vs. baseline comparison — should yield 0 diffs
2. Seed a known visual change — should be detected
3. Run same build twice on same device — should yield 0 diffs (reproducibility)
4. Test with ignore regions applied — verify dynamic content excluded
5. Verify threshold sensitivity with intentional 0.05% change — should NOT trigger at Normal threshold

---

## Responsive Layout Verification

### Breakpoint Validation

Verify that the UI correctly adapts at defined responsive breakpoints.

**Standard Breakpoint Matrix:**

| Breakpoint Name | Width  | Target Devices                  | Verification Focus                |
| --------------- | ------ | ------------------------------- | --------------------------------- |
| xs              | 320px  | iPhone SE, small Android phones | Content fit, no horizontal scroll |
| sm              | 375px  | iPhone 15, Pixel 7              | Primary mobile layout             |
| md              | 768px  | iPad, small tablets             | Tablet-specific layout            |
| lg              | 1024px | iPad Pro, small desktops        | Multi-column layouts              |
| xl              | 1440px | Desktop monitors                | Full-width layouts                |
| xxl             | 1920px | Large monitors                  | Max-width constraints             |

**Breakpoint Verification Rules:**

| Rule                  | Description                                      | Enforcement                       |
| --------------------- | ------------------------------------------------ | --------------------------------- |
| No horizontal scroll  | Content must fit within viewport width           | Automated scroll detection        |
| Touch target minimum  | 44x44dp on mobile, 48x48dp on Android            | Automated hit-target analysis     |
| Text readability      | No text truncation without ellipsis/tooltip      | Automated text overflow detection |
| Navigation adaptation | Nav pattern changes appropriately at breakpoints | Manual review of nav state        |
| Image scaling         | Images scale proportionally without distortion   | Automated aspect ratio check      |

### Orientation Testing

Verify layout correctness in both portrait and landscape orientations.

| Orientation                    | Platform      | Required Screens        | Notes                                 |
| ------------------------------ | ------------- | ----------------------- | ------------------------------------- |
| Portrait                       | iOS + Android | All user-facing screens | Primary usage mode                    |
| Landscape                      | iOS + Android | All user-facing screens | Media consumption, keyboard scenarios |
| Split-screen (Android)         | Android 7.0+  | Top 5 user journeys     | Multi-window support                  |
| Slide over / Split view (iPad) | iPadOS        | Top 5 user journeys     | iPad multitasking                     |

**Orientation-Specific Checks:**

| Check                    | Portrait                         | Landscape                                 |
| ------------------------ | -------------------------------- | ----------------------------------------- |
| Safe area insets         | Top notch, bottom home indicator | Side notches (if applicable)              |
| Keyboard overlay         | Bottom content not obscured      | Reduced vertical space handled            |
| Image/video aspect ratio | Full width maintained            | Letterboxing/pillarboxing correct         |
| Navigation               | Bottom tab bar or drawer         | Side navigation or compact bar            |
| Scroll direction         | Vertical primary                 | Horizontal may be primary on some screens |

### Dynamic Type Verification

Verify layout integrity when users change system font size settings.

| Setting             | Scale Factor | Platforms     | Risk Level                 |
| ------------------- | ------------ | ------------- | -------------------------- |
| Default             | 1.0x         | iOS + Android | Baseline                   |
| Large               | 1.3x         | iOS + Android | Medium — text overflow     |
| Extra Large         | 1.5x         | iOS + Android | High — layout break        |
| Accessibility (Max) | 2.0x+        | iOS + Android | Critical — reflow required |

**Dynamic Type Test Execution:**

```yaml
dynamic-type-tests:
  - name: "text-reflow-small"
    font-scale: 1.3
    expected: "All text readable without truncation"

  - name: "text-reflow-medium"
    font-scale: 1.5
    expected: "Layout reflows; no overlap"

  - name: "text-reflow-large"
    font-scale: 2.0
    expected: "Content remains accessible; scrolling enabled"

  execution:
    platform: [ios, android]
    screens: "all-user-facing"
    capture-mode: "screenshot-per-screen-per-scale"
```

### RTL (Right-to-Left) Layout Verification

Verify correct mirroring of UI for RTL languages (Arabic, Hebrew, Persian, Urdu).

| Element                   | RTL Behavior                         | Verification                                 |
| ------------------------- | ------------------------------------ | -------------------------------------------- |
| Navigation back button    | Flips to right side                  | Screenshot comparison with mirrored baseline |
| Text alignment            | Right-aligned by default             | Verify all body text                         |
| Icons with directionality | Arrow icons flip                     | Chevron, back, forward icons                 |
| Progress indicators       | LTR progress (rightward) even in RTL | Confirm no flip on progress bars             |
| Media playback controls   | Unchanged (LTR)                      | Verify no unwanted mirroring                 |
| Numbers                   | LTR (Western numerals)               | Verify number rendering                      |
| Mixed content (bidi)      | Correct bidirectional rendering      | Test with mixed Arabic/English text          |

**RTL Test Execution:**

```yaml
rtl-tests:
  locales:
    - ar # Arabic
    - he # Hebrew
    - fa # Persian
    - ur # Urdu
  verification:
    - "All layout directions mirrored correctly"
    - "Non-mirgradable elements preserved (media, progress)"
    - "Text truncation handled at RTL boundary"
  baseline: "RTL-specific baselines required (not mirrored LTR)"
```

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

## CI/CD Integration

### Automated Comparison Pipeline

```yaml
# GitHub Actions — Visual Regression Pipeline
name: Visual Regression

on:
  pull_request:
    paths:
      - "src/**"
      - "assets/**"
      - "*.css"
      - "*.scss"
      - "*.xml" # Android layouts
      - "*.swift" # iOS views
      - "*.jet" # Compose layouts

jobs:
  visual-regression:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        viewport:
          - { name: "mobile-sm", width: 320, height: 568 }
          - { name: "mobile-md", width: 375, height: 812 }
          - { name: "tablet", width: 768, height: 1024 }
          - { name: "desktop", width: 1920, height: 1080 }

    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Run visual regression tests
        uses: Percy/cli@v1
        with:
          command: exec -- npm run test:visual
        env:
          PERCY_TOKEN: ${{ secrets.PERCY_TOKEN }}

      - name: Upload test artifacts
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: visual-diffs-${{ matrix.viewport.name }}
          path: test-results/visual-regression/

      - name: Comment PR with diff summary
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const percyBuild = process.env.PERCY_BUILD_URL;
            if (percyBuild) {
              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: `Visual regression results: ${percyBuild}`
              });
            }
```

### Playwright Native Visual Regression

```typescript
// playwright-visual.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/visual",
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: [["html", { outputFolder: "test-results/visual" }]],
  use: {
    baseURL: "http://localhost:3000",
    screenshot: "only-on-failure",
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium-mobile",
      use: {
        ...devices["Pixel 7"],
        hasTouch: true,
        viewport: { width: 393, height: 851 },
      },
    },
    {
      name: "chromium-tablet",
      use: {
        ...devices["iPad Mini"],
        viewport: { width: 768, height: 1024 },
      },
    },
    {
      name: "chromium-desktop",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1920, height: 1080 },
      },
    },
  ],
});

// tests/visual/homepage.visual.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Homepage visual regression", () => {
  test("matches baseline — default state", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveScreenshot("homepage-default.png", {
      maxDiffPixels: 100,
      maxDiffPixelRatio: 0.001, // 0.1% threshold
      threshold: 0.1, // Per-pixel sensitivity
      animations: "disabled",
      mask: [page.locator(".dynamic-timestamp"), page.locator(".user-avatar")],
      omitBackground: false,
      fullPage: true,
    });
  });

  test("matches baseline — dark mode", async ({ page }) => {
    await page.goto("/");
    await page.emulateMedia({ colorScheme: "dark" });
    await expect(page).toHaveScreenshot("homepage-dark.png", {
      maxDiffPixelRatio: 0.001,
      fullPage: true,
    });
  });
});
```

### PR Diff Comment Workflow

```yaml
# .github/workflows/visual-regression-comment.yml
name: Visual Regression PR Comment

on:
  workflow_run:
    workflows: ["Visual Regression"]
    types: [completed]

jobs:
  post-comment:
    runs-on: ubuntu-latest
    if: github.event.workflow_run.conclusion == 'success' || github.event.workflow_run.conclusion == 'failure'
    steps:
      - name: Download artifact
        uses: dawidd6/action-download-artifact@v3
        with:
          run_id: ${{ github.event.workflow_run.id }}

      - name: Generate diff summary
        id: summary
        run: |
          if [ -d "visual-diffs" ]; then
            CHANGED=$(ls visual-diffs/ | wc -l)
            echo "changed_screenshots=$CHANGED" >> $GITHUB_OUTPUT
          fi

      - name: Post PR comment
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          number: ${{ github.event.workflow_run.pull_requests[0].number }}
          message: |
            ## Visual Regression Results

            | Metric | Value |
            |--------|-------|
            | Status | ${{ github.event.workflow_run.conclusion }} |
            | Changed Screenshots | ${{ steps.summary.outputs.changed_screenshots }} |

            ${{ github.event.workflow_run.conclusion == 'failure' && '⚠️ Visual differences detected. Review diffs before approving.' || 'No visual differences detected.' }}
```

### Baseline Approval Workflow

**Approval Process (GitLab CI example):**

```yaml
# .gitlab-ci.yml — Visual Regression with Approval Gate
visual-regression:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm run build
    - npm run test:visual -- --compare-with=baseline/${CI_MERGE_REQUEST_TARGET_BRANCH_NAME}
  artifacts:
    when: always
    paths:
      - test-results/visual-regression/
    reports:
      junit: test-results/visual-regression/junit.xml
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      changes:
        - src/**/*
        - assets/**/*
        - "*.css"

update-baseline:
  stage: deploy
  image: node:20
  script:
    - npm ci
    - npm run test:visual -- --update-baseline
    - git add baselines/
    - git commit -m "chore: update visual baselines [skip ci]"
    - git push origin HEAD:$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: manual
      allow_failure: false
      variables: $VISUAL_REGRESSION_APPROVED == "true"
```

**Baseline Update Approval Criteria:**

| Criterion                   | Required?           | Verification                      |
| --------------------------- | ------------------- | --------------------------------- |
| All diffs are intentional   | Yes                 | Reviewer confirms each diff       |
| No unintended layout shifts | Yes                 | Side-by-side comparison review    |
| Accessibility maintained    | Yes                 | Verify focus indicators, contrast |
| Responsive behavior correct | Yes                 | All breakpoints verified          |
| RTL layouts correct         | Yes (if applicable) | RTL baseline captured             |

### Automated Baseline Update Command

```bash
# Update baselines for a specific feature branch
npx playwright test --update-snapshots \
  --grep "visual" \
  --project="chromium-mobile"

# Review changes before committing
git diff baselines/

# Commit with descriptive message
git add baselines/
git commit -m "test(visual): update baselines for feature X

Changes:
- Homepage hero banner: +20px height (design update v3.2)
- Settings screen: new toggle added (intentional)
- Profile page: avatar shape circular -> square (ADR-042)

Approved-by: @design-reviewer
Design-ref: figma://project/abc123/v4.1"
```

---

## Cross-Device Testing

### Device Farm Integration

| Service           | Device Coverage               | Integration Method        | Cost Model              | Best For                      |
| ----------------- | ----------------------------- | ------------------------- | ----------------------- | ----------------------------- |
| AWS Device Farm   | 200+ real Android/iOS devices | AWS CLI, API              | Pay per device-minute   | Comprehensive device coverage |
| Firebase Test Lab | 50+ real + virtual devices    | gcloud CLI, Gradle plugin | Free tier + pay per use | Android-first teams           |
| BrowserStack      | 3000+ devices/browsers        | REST API, SDKs            | Subscription            | Cross-browser + mobile        |
| Sauce Labs        | 1000+ real + emulated devices | REST API, W3C WebDriver   | Subscription            | Enterprise teams              |
| LambdaTest        | 3000+ browsers/devices        | REST API, Selenium        | Subscription            | Budget-conscious teams        |

### OS Matrix Coverage

| Platform | OS Versions to Test                   | Rationale                         |
| -------- | ------------------------------------- | --------------------------------- |
| Android  | API 33 (13), API 31 (12), API 30 (11) | Current + 2 previous major        |
| Android  | API 28 (9)                            | Minimum supported (if applicable) |
| iOS      | iOS 17, iOS 16                        | Current + 1 previous major        |
| iOS      | iOS 15                                | Minimum supported (if applicable) |

**Browser/Device Coverage Matrix:**

| Browser          | Mobile                 | Tablet             | Desktop      |
| ---------------- | ---------------------- | ------------------ | ------------ |
| Chrome           | Pixel 7, Galaxy S23    | iPad, Galaxy Tab   | Chrome 120+  |
| Safari           | iPhone 15, iPhone SE   | iPad Air, iPad Pro | Safari 17+   |
| Firefox          | —                      | —                  | Firefox 120+ |
| Edge             | —                      | —                  | Edge 120+    |
| Samsung Internet | Galaxy S23, Galaxy A54 | Galaxy Tab S9      | —            |

### Coverage Prioritization

| Priority       | Devices/Browsers                                 | Coverage Goal   | Execution Frequency |
| -------------- | ------------------------------------------------ | --------------- | ------------------- |
| P0 — Critical  | Primary device per platform (Pixel 7, iPhone 15) | 100% of screens | Every PR            |
| P1 — Important | Secondary devices (tablet, small phone, old OS)  | 90% of screens  | Nightly             |
| P2 — Extended  | Edge cases (old browser, foldable, fold/unfold)  | 75% of screens  | Weekly              |
| P3 — Complete  | Full device farm matrix                          | 100% of matrix  | Pre-release only    |

---

## Performance Considerations

### Storage Optimization

| Strategy                          | Impact                           | Implementation                            |
| --------------------------------- | -------------------------------- | ----------------------------------------- |
| Lossless PNG compression          | 40-60% size reduction            | `pngcrush`, `optipng`, `pngquant`         |
| Deduplicate identical screenshots | 10-30% storage savings           | Hash-based deduplication (SHA-256)        |
| Compress baselines on cloud       | 50-70% cost reduction            | S3 Intelligent-Tiering, GCS Nearline      |
| Prune old baselines               | Ongoing storage management       | Retain last 10 versions per screen/device |
| Differential storage              | 80-90% reduction vs. full images | Store only diffs + metadata               |

**Storage Estimation Formula:**

```
Total Storage = (Number of screens) x (Number of device configs)
              x (Average screenshot size) x (Number of versions retained)

Example:
  50 screens x 6 device configs x 500 KB x 10 versions = 1.5 GB

With deduplication (20% savings) + compression (50% savings):
  1.5 GB x 0.8 x 0.5 = 600 MB
```

### Diff Computation Time

| Factor                | Impact                            | Mitigation                                   |
| --------------------- | --------------------------------- | -------------------------------------------- |
| Number of screenshots | Linear scaling                    | Parallelize across workers                   |
| Image resolution      | Quadratic scaling (W x H)         | Downscale before comparison for initial pass |
| Comparison algorithm  | O(n) where n = pixel count        | Use SIMD-optimized libraries (odiff)         |
| Threshold calculation | Additional pass over diff regions | Pre-compute ignore regions                   |

**Performance Benchmarks (per 100 screenshot pairs):**

| Tool                     | Resolution | Time               | Method               |
| ------------------------ | ---------- | ------------------ | -------------------- |
| pixelmatch               | 1920x1080  | ~8 seconds         | CPU, single-threaded |
| pixelmatch (worker pool) | 1920x1080  | ~2 seconds         | CPU, 4 workers       |
| odiff                    | 1920x1080  | ~1 second          | Rust, SIMD           |
| resemble.js              | 1920x1080  | ~12 seconds        | CPU, JavaScript      |
| Applitools AI            | 1920x1080  | ~3 seconds (cloud) | Cloud GPU, AI model  |

### Baseline Management at Scale

| Challenge                       | Solution                        | Tool Support                                  |
| ------------------------------- | ------------------------------- | --------------------------------------------- |
| Baseline drift over time        | Periodic full baseline review   | Percy batch review, Applitools batch analysis |
| Branch-specific baselines       | Per-branch baseline isolation   | Percy branch testing, BackstopJS `--config`   |
| Merge conflict on binary images | Store baselines in LFS or cloud | Git LFS, Percy cloud storage                  |
| Baseline versioning             | Tag baselines with git SHA      | Automated tagging in CI                       |
| Cross-platform baseline sync    | Unified baseline manifest       | Custom manifest JSON                          |

---

## Stage 7/8 Integration

### Stage 7 — Automated Testing Integration

Visual regression tests are part of the automated test suite executed in Stage 7.

| Stage 7 Requirement  | Visual Regression Contribution                                   |
| -------------------- | ---------------------------------------------------------------- |
| Test Suite execution | Visual regression tests run alongside unit/integration/e2e tests |
| Defect detection     | Visual diffs classified as P0-P3 defects                         |
| Results reporting    | Visual diff report included in TEST-RESULTS-REPORT.md            |
| 100% pass target     | Visual tests must pass (zero unauthorized diffs)                 |

**Visual Regression Defect Classification:**

| Visual Defect                           | Severity | Rationale                    |
| --------------------------------------- | -------- | ---------------------------- |
| Screen completely broken (blank/crash)  | P0       | Core feature non-functional  |
| Major layout broken, content unreadable | P1       | Major UX failure             |
| Minor element misalignment (5-10px)     | P2       | Cosmetic issue, user decides |
| Color shade difference (imperceptible)  | P3       | Polish issue, user decides   |
| Text truncation in RTL layout           | P1       | Core accessibility failure   |
| Button too small on specific device     | P2       | Minor UX degradation         |

**Stage 7 Visual Regression Report Format:**

```markdown
# Visual Regression Report — Stage 7

## Summary

| Metric                      | Value |
| --------------------------- | ----- |
| Total screenshots compared  | 342   |
| Passed                      | 335   |
| Failed (unauthorized diffs) | 7     |
| New baselines (approved)    | 12    |
| False positives             | 2     |

## Failed Comparisons

| Screen          | Device    | Diff % | Severity | Status   |
| --------------- | --------- | ------ | -------- | -------- |
| Homepage hero   | Pixel 7   | 3.2%   | P1       | Open     |
| Settings toggle | iPhone 15 | 0.08%  | P3       | Deferred |
| ...             | ...       | ...    | ...      | ...      |

## Classification Summary

| Severity | Count | Action        |
| -------- | ----- | ------------- |
| P0       | 0     | —             |
| P1       | 1     | Fix required  |
| P2       | 4     | User decision |
| P3       | 2     | User decision |
```

### Stage 8 — Integrity Verification Integration

Stage 8 verifies that the delivered product matches the approved design specification. Visual regression provides the quantitative evidence.

| Stage 8 Requirement      | Visual Regression Contribution                                       |
| ------------------------ | -------------------------------------------------------------------- |
| Design fidelity check    | Compare current screenshots against Stage 2 design prototype renders |
| Panel review evidence    | Visual diff report presented to CTO panel (CDO, CPO, CSO, CTO-L)     |
| No unauthorized changes  | Zero diffs outside approved change list                              |
| Accessibility compliance | Dynamic type, RTL, and contrast screenshots verified                 |

**Stage 8 Visual Verification Checklist:**

| Check                         | Responsible Panel Member | Verification Method                     |
| ----------------------------- | ------------------------ | --------------------------------------- |
| Visual match to design spec   | CDO                      | Screenshot vs. IDS comparison           |
| PRD requirements met visually | CPO                      | Screen-by-screen PRD checklist          |
| Security UI intact            | CSO                      | Permission dialogs, security indicators |
| Localization rendering        | CTO-L                    | RTL, text expansion screenshots         |
| Architecture compliance       | CTO/CIO                  | Component structure matches UML         |

**Stage 8 Integrity Sign-off for Visual Regression:**

```markdown
# Visual Integrity Verification — Stage 8 Sign-off

## Panel Assessment

| Panel Member          | Assessment                                  | Sign-off     |
| --------------------- | ------------------------------------------- | ------------ |
| CDO (Design Fidelity) | All screens match IDS within tolerance      | [ ] Approved |
| CPO (PRD Alignment)   | All PRD requirements visually verified      | [ ] Approved |
| CSO (Security UI)     | All security indicators present and correct | [ ] Approved |
| CTO-L (Localization)  | All target languages render correctly       | [ ] Approved |

## Unresolved Visual Defects

| Defect                | Severity | Panel Decision |
| --------------------- | -------- | -------------- |
| [None — all resolved] | —        | —              |

## Overall Verdict

[ ] PASS — Visual integrity verified, no unauthorized changes
[ ] FAIL — Unauthorized visual changes detected
```

---

## References

### Tool Documentation

| Tool       | Documentation URL                          | Key Pages                       |
| ---------- | ------------------------------------------ | ------------------------------- |
| Percy      | https://docs.browserstack.com/docs/percy   | Visual Testing, CI Integration  |
| Applitools | https://applitools.com/docs                | Eyes SDK, Ultrafast Test Grid   |
| BackstopJS | https://github.com/garris/BackstopJS       | Configuration, Scenarios        |
| Chromatic  | https://www.chromatic.com/docs             | Storybook Integration, GitHub   |
| Playwright | https://playwright.dev/docs/test-snapshots | toHaveScreenshot, Configuration |
| Maestro    | https://maestro.mobile.dev                 | Visual testing, Cloud           |

### Related Skills

| Skill                            | Category     | Relevance                                |
| -------------------------------- | ------------ | ---------------------------------------- |
| testing-qa/unit-testing          | Testing QA   | Foundation for test automation           |
| testing-qa/e2e-testing           | Testing QA   | Complementary to visual regression       |
| testing-qa/accessibility-testing | Testing QA   | Overlapping viewport/dynamic type checks |
| android/testing                  | Android      | Native Android visual testing            |
| ios/testing                      | iOS          | Native iOS visual testing                |
| frontend-web/testing             | Frontend Web | Web screenshot strategies                |
| shared/wcag-compliance           | Shared       | Accessibility visual requirements        |

### Standards and Specifications

| Standard                   | Description                          | Relevance                                 |
| -------------------------- | ------------------------------------ | ----------------------------------------- |
| WCAG 2.1 AA                | Web Content Accessibility Guidelines | Dynamic type, contrast, focus indicators  |
| Material Design 3          | Google design system                 | Android visual baseline reference         |
| Human Interface Guidelines | Apple design system                  | iOS visual baseline reference             |
| OWASP MASVS                | Mobile App Security Verification     | Security UI visual verification (Stage 8) |

### Pipeline References

| Document              | Location                                                    | Relevance                      |
| --------------------- | ----------------------------------------------------------- | ------------------------------ |
| Stage 7 Specification | `.lingma/pipeline/mobile-development/pipeline.md`           | Test execution requirements    |
| Stage 8 Specification | `.lingma/pipeline/mobile-development/pipeline.md`           | Integrity verification process |
| Defect Classification | `LINGMA.md`                                                 | P0-P3 severity system          |
| Test Lead Profile     | `company/departments/research-develop/.../priscilla-oduya/` | Stage 7 ownership              |
