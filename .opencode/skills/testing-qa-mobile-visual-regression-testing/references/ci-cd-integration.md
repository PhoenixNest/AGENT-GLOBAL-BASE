# CI/CD Integration

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
