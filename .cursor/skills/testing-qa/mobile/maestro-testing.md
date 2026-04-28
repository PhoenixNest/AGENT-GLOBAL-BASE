---
name: maestro-testing
description: Maestro is a modern cross-platform mobile UI testing framework that uses YAML flow definitions to describe user interactions.
---

# Maestro — Cross-Platform Mobile Test Automation

**Category:** Mobile Test Automation — Cross-Platform Frameworks
**Owner:** SDET Mobile #1 (Ananya Krishnan)

## Overview

Maestro is a modern cross-platform mobile UI testing framework that uses YAML flow definitions to describe user interactions. It provides a unified testing language for Android and iOS, supports conditional logic, data-driven testing, and integrates natively with CI/CD pipelines. Unlike Appium, Maestro operates as a gray-box tool with built-in synchronization, eliminating the flaky wait patterns that plague traditional cross-platform test frameworks.

This skill covers Maestro flow authoring, advanced conditional logic, data-driven test patterns, visual testing assertions, and CI/CD pipeline integration. Maestro complements the native Espresso/XCTest suites by providing a single-source test definition that runs identically on both platforms, reducing maintenance overhead for feature parity validation.

## Competency Dimensions

| Dimension                            | Description                                                                                                                                                                               | Proficiency Indicators                                                                                                                                                                                                                           |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Flow Definition Syntax**           | YAML structure, `appId`, `onFlowStart/onFlowComplete` hooks, `commands` sequence, element selectors (`id`, `text`, `containsText`, `accessibilityText`), sub-flow inclusion via `runFlow` | Flows use semantic selectors (preferring `id` over `text`); complex journeys split into sub-flows via `runFlow: {file: login.yaml}`; environment variables parameterize `appId` per build variant; hooks handle test data setup/teardown         |
| **Conditional Logic & Control Flow** | `when` conditions, `retry` blocks, `assert` statements, `loop` constructs, dynamic element handling, platform-specific branching with `${MAESTRO_PLATFORM}`                               | Tests branch on `when: {visible: element}` with `then/else` blocks; retry wraps flaky network-dependent assertions; loops iterate over list items with index variables; platform branching uses `${MAESTRO_PLATFORM}` in conditional expressions |
| **Data-Driven Testing**              | External CSV/JSON data injection, `evalScript` for dynamic data generation, environment variable substitution, parameterized flow execution                                               | Data files stored in `testdata/` directory; `evalScript` generates UUIDs, timestamps, and random strings; flows parameterized via `--env` flag in CI; test matrices run same flow with multiple credential sets                                  |
| **Visual Testing Assertions**        | `assertNoChanges` for screen stability, screenshot capture, pixel comparison with tolerance thresholds, visual regression detection                                                       | `assertNoChanges` used after animations complete; screenshots captured at key journey checkpoints; pixel diff tolerance set to 0.5% for cross-platform rendering differences; visual regressions filed as P2 defects                             |
| **CI/CD Integration**                | GitHub Actions / GitLab CI / Bitrise pipelines, Maestro Cloud execution, emulator/simulator provisioning, test result reporting, artifact upload                                          | Pipeline provisions emulator via `android-emulator-runner` or `revolutio/setup-maestro`; Maestro CLI runs `maestro test flow.yaml`; results uploaded as JUnit XML; screenshots/artifacts attached to CI run; Slack notification on failure       |
| **Debugging & Diagnostics**          | `maestro hierarchy` for element inspection, `maestro record` for video capture, `maestro logcat` / `maestro syslog` for device logs, interactive REPL (`maestro studio`)                  | Debug sessions start with `maestro hierarchy` to verify element selectors; `maestro studio` used for exploratory test authoring; recordings captured for all failed flows; device logs collected and archived alongside test results             |

## Execution Guidance

### Flow Definition — Core Syntax

**1. Standard Login Flow**

```yaml
appId: com.company.app
---
- launchApp:
    appId: ${APP_ID}
    clearState: true
    stopApp: true

- runFlow:
    when:
      visible: 'Allow notifications'
    file: dismiss-notification-prompt.yaml

- tapOn:
    id: 'emailField'
- inputText: ${EMAIL}
- tapOn:
    id: 'passwordField'
- inputText: ${PASSWORD}
- tapOn:
    id: 'loginButton'

- assertVisible:
    id: 'homeScreenTitle'
- assertVisible:
    text: 'Welcome back'
- assertNoChanges:
    timeout: 2000

- runFlow:
    file: verify-navigation-menu.yaml
```

**2. Sub-Flow Composition**

Reusable authentication sub-flow (`login.yaml`):

```yaml
appId: ${APP_ID}
---
- tapOn:
    id: 'emailField'
- inputText: ${EMAIL}
- tapOn:
    id: 'passwordField'
- inputText: ${PASSWORD}
- tapOn:
    id: 'loginButton'
- assertVisible:
    id: 'homeScreenTitle'
```

Parent flow includes it:

```yaml
appId: ${APP_ID}
---
- launchApp
- runFlow:
    file: login.yaml
    env:
      EMAIL: ${EMAIL}
      PASSWORD: ${PASSWORD}

- tapOn:
    id: 'settingsButton'
- assertVisible:
    id: 'settingsScreen'
```

**3. Conditional Logic with Platform Branching**

```yaml
appId: ${APP_ID}
---
- launchApp

# Handle platform-specific permission dialogs
- when:
    visible: 'Allow while using the app'
  then:
    - tapOn: 'Allow while using the app'
  else:
    - when:
        visible: 'Allow'
      then:
        - tapOn: 'Allow'

# Platform-specific navigation patterns
- runScript: |
    if (maestro.env.MAESTRO_PLATFORM === "iOS") {
      maestro.tapOn({id: "iosBackButton"})
    } else {
      maestro.tapOn({id: "androidBackButton"})
    }

- assertVisible:
    id: 'previousScreen'
```

**4. Data-Driven Test with External CSV**

CSV file (`testdata/checkout-scenarios.csv`):

```csv
scenario_name,card_number,expected_result
valid_visa,4111111111111111,order_confirmed
valid_mastercard,5500000000000004,order_confirmed
expired_card,4000000000000002,card_expired_error
insufficient_funds,4000000000000069,payment_declined_error
invalid_cvv,4000000000000010,cvv_invalid_error
```

Flow (`checkout-data-driven.yaml`):

```yaml
appId: ${APP_ID}
---
- launchApp:
    clearState: true

- runFlow:
    file: login.yaml

# Navigate to checkout with test product
- tapOn:
    id: 'productCard'
- tapOn:
    id: 'addToCartButton'
- tapOn:
    id: 'cartButton'
- tapOn:
    id: 'checkoutButton'

# Fill payment with data-driven values
- tapOn:
    id: 'cardNumberField'
- inputText: ${card_number}
- tapOn:
    id: 'payButton'

# Assert expected result
- when:
    visible:
      id: 'orderConfirmation'
  then:
    - assertVisible:
        id: 'orderConfirmation'
    - assertVisible:
        text: ${expected_result}
  else:
    - assertVisible:
        id: 'errorBanner'
    - assertVisible:
        text: ${expected_result}
```

CI execution:

```bash
maestro test checkout-data-driven.yaml \
  --env APP_ID=com.company.app \
  --env EMAIL=test@company.com \
  --env PASSWORD=SecurePass123! \
  --csv testdata/checkout-scenarios.csv
```

**5. evalScript for Dynamic Data**

```yaml
appId: ${APP_ID}
---
- launchApp:
    clearState: true

# Generate unique test user data
- runScript: |
    const timestamp = Date.now()
    const uuid = crypto.randomUUID()
    maestro.env.UNIQUE_EMAIL = `testuser_${timestamp}@company.com`
    maestro.env.UNIQUE_USERNAME = `user_${uuid.substring(0, 8)}`
    maestro.env.ORDER_REF = `ORD-${timestamp}`

- tapOn:
    id: 'signUpButton'
- inputText: ${UNIQUE_EMAIL}
- inputText: ${UNIQUE_USERNAME}
- tapOn:
    id: 'createAccountButton'

- assertVisible:
    id: 'welcomeScreen'
- assertVisible:
    text: ${UNIQUE_USERNAME}
```

**6. Visual Testing & Screenshot Capture**

```yaml
appId: ${APP_ID}
---
- launchApp

# Capture baseline screenshots at key checkpoints
- tapOn:
    id: 'homeButton'
- assertVisible:
    id: 'homeScreenTitle'
- assertNoChanges:
    timeout: 3000
- takeScreenshot: 'home-screen.png'

# Navigate and verify visual state
- tapOn:
    id: 'productCatalog'
- assertVisible:
    id: 'productGrid'
- assertNoChanges:
    timeout: 2000
- takeScreenshot: 'product-catalog.png'
# Visual regression: compare against baseline
# In CI: maestro test flow.yaml --format junit
# Baseline comparison handled by CI pipeline with pixel-diff tool
```

### CI/CD Integration — GitHub Actions

```yaml
name: Maestro E2E Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  maestro-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        platform: [android, ios]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Maestro
        uses: mobile-dev-inc/setup-maestro@v1

      - name: Start Android Emulator
        if: matrix.platform == 'android'
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          arch: x86_64
          profile: pixel_6
          script: |
            maestro test flows/checkout-flow.yaml \
              --env APP_ID=com.company.app \
              --env EMAIL=ci@test.com \
              --env PASSWORD=Test1234! \
              --format junit \
              --output test-results/maestro-android.xml

      - name: Run iOS Tests (macOS runner)
        if: matrix.platform == 'ios'
        run: |
          xcrun simctl boot "iPhone 15" || true
          maestro test flows/checkout-flow.yaml \
            --env APP_ID=com.company.app.test \
            --env EMAIL=ci@test.com \
            --env PASSWORD=Test1234! \
            --format junit \
            --output test-results/maestro-ios.xml

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: maestro-results-${{ matrix.platform }}
          path: test-results/

      - name: Upload Screenshots
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: maestro-screenshots-${{ matrix.platform }}
          path: ~/.maestro/screenshots/

      - name: Notify on Failure
        if: failure()
        run: |
          curl -X POST $SLACK_WEBHOOK \
            -H 'Content-Type: application/json' \
            -d "{\"text\": \"Maestro E2E tests failed on ${{ matrix.platform }}. Check artifacts for screenshots and logs.\"}"
```

### Maestro Studio — Interactive Test Authoring

Maestro Studio provides a browser-based IDE for exploratory test creation:

```bash
maestro studio
```

This opens `http://localhost:9999` with:

- Live device screen mirror
- Element hierarchy inspector
- Action recorder (tap, scroll, input)
- Flow editor with YAML preview
- Test execution controls

**Workflow:**

1. Launch Maestro Studio with app running on emulator/simulator
2. Navigate through the app manually
3. Maestro records each action as YAML
4. Edit the generated flow in the IDE
5. Add assertions, conditional logic, and data injection
6. Save and export as `.yaml` file to `flows/` directory

### Debugging Failed Flows

**1. Element Hierarchy Inspection**

```bash
maestro hierarchy
```

Outputs the full UI tree with element properties (`id`, `text`, `bounds`, `enabled`, `visible`). Use this to verify selectors when tests fail with "element not found."

**2. Video Recording for Failure Analysis**

```bash
maestro test flow.yaml --record
```

Captures the entire test execution as an MP4. Video is saved to `~/.maestro/recordings/`. Attach to defect reports in Stage 7.

**3. Device Log Collection**

```bash
# Android
maestro logcat > logs/android-logcat.log

# iOS
maestro syslog > logs/ios-syslog.log
```

Filter logs by your app's package name to isolate relevant stack traces.

## Pipeline Integration

| Stage                                | Application                                                                                                                                                              |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Stage 5** (Development)            | Author Maestro flows alongside cross-platform feature development; validate flows against debug builds on emulators                                                      |
| **Stage 6** (Code Review)            | Review flow definitions for selector stability, proper use of `id` over `text`, adequate assertion coverage                                                              |
| **Stage 7** (Automated Testing)      | **Primary ownership** — execute Maestro E2E suites in CI, manage data-driven test matrices, aggregate cross-platform results, classify visual regression defects         |
| **Stage 8** (Integrity Verification) | Re-run full Maestro suite against post-fix builds; verify critical user journeys remain intact; compare screenshots against baseline to detect unintended visual changes |

## Quality Standards

| Metric                         | Target                                                     | Measurement                                                                                    |
| ------------------------------ | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Maestro flow flake rate        | < 3% per 100 runs                                          | CI retry analysis; flows exceeding threshold quarantined                                       |
| Cross-platform parity coverage | 100% of critical user journeys on both Android and iOS     | Traced to PRD requirements; each critical journey has a Maestro flow running on both platforms |
| Selector stability (id-based)  | > 95% of element selectors use `id` or `accessibilityText` | Automated flow lint; `text`-based selectors flagged for review                                 |
| CI execution time (full suite) | < 45 minutes for both platforms combined                   | Measured from CI pipeline start to result aggregation                                          |
| Visual regression detection    | All pixel diffs > 0.5% flagged and reviewed                | Automated screenshot comparison in CI pipeline                                                 |
| Data-driven scenario coverage  | 100% of edge-case scenarios from PRD covered               | Traceability matrix maps PRD test scenarios to Maestro CSV data rows                           |
| Screenshot artifact retention  | 90 days for all failed flow runs                           | CI artifact retention policy; archived to cloud storage                                        |
