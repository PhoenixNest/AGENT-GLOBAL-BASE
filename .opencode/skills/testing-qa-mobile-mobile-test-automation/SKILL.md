---
name: testing-qa-mobile-mobile-test-automation
description: 'Testing Qa skill: Mobile Test Automation'
---

# Mobile Test Automation

## Overview

Comprehensive mobile test automation architecture spanning unit, integration, E2E, and regression testing across Android, iOS, and cross-platform frameworks. This skill enables a test automation lead to design scalable test frameworks, manage device farms, detect and quarantine flaky tests, and integrate test execution into CI/CD pipelines — ensuring 100% automated test pass rate as required by the Stage 7 gate.

## Competency Dimensions

| Dimension                   | Proficiency Level | Key Capabilities                                                                       |
| --------------------------- | ----------------- | -------------------------------------------------------------------------------------- |
| Test Framework Architecture | Expert            | Multi-layer test strategy (unit, integration, E2E, regression), shared test DSL design |
| Espresso + XCTest + Maestro | Expert            | Platform-native UI testing, cross-platform test orchestration, shared test scenarios   |
| Flaky Test Detection        | Advanced          | Statistical analysis, auto-quarantine, root cause analysis, stabilization strategies   |
| Parallel Test Execution     | Expert            | Test sharding, distributed execution, resource contention management                   |
| Device Farm Management      | Advanced          | Physical + emulator/simulator management, device scheduling, environment provisioning  |
| Test Result Aggregation     | Expert            | Unified reporting, trend analysis, defect correlation, dashboard design                |
| CI/CD Test Pipeline         | Expert            | Gate enforcement, parallel orchestration, artifact publishing, failure triage          |

## Execution Guidance

### Mobile Test Framework Architecture

**Test Pyramid for Mobile:**

```
                    /\
                   /  \    E2E (Maestro) — 10% of tests
                  /____\   Critical user journeys, cross-platform flows
                 /        \
                /__________\  Integration — 20% of tests
               /            \  API contracts, data layer, platform interop
              /______________\
             /                \  Unit — 70% of tests
            /__________________\  Business logic, utilities, view models
```

**Framework Layering:**

1. **Unit Test Layer:** JUnit 5 (Android), XCTest (iOS), Dart `test` (Flutter) — fast, deterministic, no I/O
2. **Integration Test Layer:** Android Instrumentation Tests, iOS XCTestCase with dependencies, Flutter integration tests — tests component interactions
3. **E2E Test Layer:** Maestro for cross-platform scenarios, Espresso (Android), XCUITest (iOS) — full app flows
4. **Regression Test Layer:** Full suite execution on every release candidate; includes all above layers plus performance benchmarks

**Shared Test DSL (Domain-Specific Language):**

- Define test scenarios in a platform-agnostic format (YAML or Gherkin)
- Generate platform-specific test code from shared scenario definitions
- Example shared scenario:
  ```yaml
  scenario: user_login_success
    steps:
      - tap: "#email_field"
      - input_text: "test@example.com"
      - tap: "#password_field"
      - input_text: "SecurePass123!"
      - tap: "#login_button"
      - assert_visible: "#home_screen"
  ```
- Compile to: Espresso (Kotlin), XCUITest (Swift), Maestro (YAML) — all from single source

### Espresso + XCTest + Maestro

**Espresso (Android):**

- Use `@RunWith(AndroidJUnit4::class)` for AndroidX test runner
- Implement Page Object pattern: each screen as a class with element locators and actions
- Use `IdlingResource` for async operations (network calls, database queries)
- Configure test orchestrator (`AndroidJUnitRunner`) for test isolation — each test runs in its own instrumentation instance
- Use `@ScreenshotTest` annotation for automatic screenshot capture on test failure

**XCTest / XCUITest (iOS):**

- Use `XCTestCase` subclasses with `setUp()` and `tearDown()` for test lifecycle
- Implement `XCUIApplication()` launch with custom arguments for test mode (mock network, skip onboarding)
- Use accessibility identifiers (`accessibilityIdentifier`) as primary locators — not XPath
- Implement `expectation(for:timeout:)` for async assertions
- Use `XCUIScreenshot` for automatic failure capture

**Maestro (Cross-Platform E2E):**

- Write flows in YAML — executes on both Android and iOS without modification
- Use `runFlow:` for reusable sub-flows (login, navigation, logout)
- Implement `retry:` for flaky interaction points
- Use `evalScript:` for JavaScript-based assertions when YAML expressions are insufficient
- Run with `maestro test flow.yaml --device <device_id>` for targeted device testing
- Integrate with CI: `maestro test flows/ --format junit --output test-results/`

**Cross-Platform Test Execution Strategy:**
| Test Type | Android | iOS | Cross-Platform |
|-----------|---------|-----|----------------|
| Unit | JUnit 5 | XCTest | Dart `test` |
| Integration | Espresso (no UI) | XCTest (no UI) | Flutter integration |
| UI E2E | Espresso | XCUITest | Maestro |
| Performance | Macrobenchmark | XCTMetric | Flutter devtools |
| Accessibility | Accessibility Scanner | Accessibility Inspector | Manual audit |

### Flaky Test Detection and Auto-Quarantine

**Detection Algorithm:**

1. Track test pass/fail history across the last N runs (N ≥ 30)
2. Calculate flakiness score: `flakiness = (intermittent_failures / total_runs) × 100`
3. Classify:
   - **Stable:** flakiness < 2%
   - **Watch:** flakiness 2–5% (flagged for investigation)
   - **Flaky:** flakiness 5–15% (auto-quarantined)
   - **Critical Flaky:** flakiness > 15% (disabled + ticket created)

**Auto-Quarantine Mechanism:**

- When a test exceeds the flaky threshold, automatically move it to a `quarantined_tests.yaml` registry
- Quarantined tests still run in a separate "flaky suite" — they report but don't block the pipeline
- Generate a quarantine report: test name, flakiness score, last 10 results, suspected cause
- Assign a stabilization owner (usually the test author or feature team)
- SLA: quarantined tests must be fixed or permanently disabled within 5 business days

**Root Cause Analysis for Flaky Tests:**

- **Timing issues:** Add explicit waits, use IdlingResource/expectations instead of `sleep()`
- **Test order dependency:** Ensure test isolation; randomize execution order to detect dependencies
- **Resource contention:** Use unique test data per test run; avoid shared state
- **Environment variability:** Pin test environment versions; use mocks for external services
- **Device-specific behavior:** Run on multiple device configurations; skip tests that are inherently device-specific with clear documentation

### Parallel Test Execution Strategy

**Test Sharding:**

- Split test suite into N shards based on execution time (not test count)
- Use historical execution data to balance shards: each shard should have approximately equal total duration
- Android: `./gradlew connectedAndroidTest -PnumShards=4 -PshardIndex=0`
- iOS: Use `xcodebuild` with test plans that define parallelizable test classes
- Flutter: Use `--total-shards` and `--shard-index` flags

**Distributed Execution:**

- Deploy test runners on separate infrastructure nodes (VMs, containers, or physical devices)
- Use a test orchestrator (GitLab CI parallel jobs, Jenkins parallel stage) to distribute shards
- Aggregate results: each shard publishes JUnit XML; orchestrator merges into unified report
- Handle shard failures: if one shard fails, continue others; report partial results

**Resource Contention Management:**

- Device locking: only one test session per physical device at a time
- Network isolation: each test session uses its own mock server instance
- Database isolation: each test session uses a separate test database (in-memory or schema-scoped)
- Rate limiting: coordinate API mock responses to avoid overwhelming test servers

### Device Farm Management

**Physical Device Farm:**

- Maintain a matrix of devices covering: OS versions (current + 2 previous), screen sizes, manufacturers
- Minimum coverage: 3 Android devices (low-end, mid-range, flagship), 2 iOS devices (current + previous gen)
- Device management tool: STF (Smartphone Test Farm) or proprietary device management API
- Health monitoring: battery level, storage, connectivity, OS version drift alerts

**Emulator/Simulator Management:**

- Pre-provision emulator/simulator images for all target OS versions
- Use headless emulators for CI (no UI rendering overhead)
- Snapshot-based provisioning: restore to clean state before each test session
- Containerize emulators where possible (Docker + Android emulator in container)

**Cloud Device Farms:**

- Firebase Test Lab (Android + iOS): managed device matrix, automated testing, video recording
- AWS Device Farm: physical devices, custom test environments, parallel execution
- BrowserStack/Sauce Labs: broad device coverage, network simulation, live debugging
- Cost optimization: use cloud devices for release validation; use local emulators/simulators for CI

**Device Farm Orchestration:**

```
Test job → request device (OS version, manufacturer, form factor) →
  device scheduler assigns available device →
  provision device (clean state, install app, configure mock network) →
  execute test suite →
  collect results (logs, screenshots, video, performance metrics) →
  release device (reset to clean state) →
  publish results
```

### Test Result Aggregation

**Unified Reporting:**

- Collect JUnit XML from all test frameworks (JUnit, XCTest, Maestro)
- Normalize into a unified schema: test_name, platform, status, duration, error_message, screenshot_url
- Aggregate into a single test report per pipeline run
- Publish to test dashboard with filtering by: platform, test type, date range, severity

**Trend Analysis:**

- Track test execution time trends (alert on >20% increase)
- Track pass rate trends (alert on pass rate <99%)
- Track flaky test count over time (target: zero quarantined tests)
- Track code coverage trends (target: 80%+ line coverage, 70%+ branch coverage)

**Defect Correlation:**

- Link failed tests to known defects (by Jira/Linear ticket ID in test metadata)
- Auto-create defect tickets for new test failures (with logs, screenshots, device info)
- Correlate test failures with code changes (map failing tests to recently modified files)
- Generate "failure cluster" reports: group related failures by root cause

**Dashboard Design:**

- Real-time pipeline status: green/red per stage, per platform
- Historical trends: pass rate, execution time, coverage over time
- Flaky test registry: current quarantined tests, ownership, SLA countdown
- Device health: available/in-use/offline devices, emulator status
- Coverage report: by module, by platform, trending

### CI/CD Test Pipeline Integration

**Pipeline Integration Points:**

```
commit → lint → unit-test (parallel: Android, iOS, Flutter) →
  integration-test (parallel) → build → E2E (Maestro, Espresso, XCUITest in parallel) →
  security-scan → staging-deploy → regression-test (full suite) → release-candidate
```

**Gate Enforcement:**

- Unit test failure: blocks merge — must be fixed before code review
- Integration test failure: blocks merge — must be fixed before code review
- E2E test failure: creates P1 defect; blocks Stage 7 → 8 transition
- Regression test failure: creates P0/P1 defect; blocks Stage 10 release
- Performance regression: >10% degradation in any metric creates P2 defect for user decision

**Artifact Publishing:**

- Test reports: JUnit XML, HTML reports, coverage reports published as pipeline artifacts
- Failure artifacts: screenshots, videos, logs, crash dumps attached to test report
- Coverage reports: publish to coverage service (Codecov, SonarQube) with trend tracking
- SBOM: include test dependencies in SBOM

**Failure Triage Workflow:**

1. Test fails in CI
2. Auto-classify: known flaky (quarantined) vs. new failure
3. If new failure: auto-create defect ticket with all context (logs, screenshots, diff)
4. Notify owning team via Slack/Teams integration
5. Developer investigates, fixes, re-runs test
6. Test passes → defect closed; test still fails → escalated to test lead

## Pipeline Integration

| Pipeline Stage              | Test Automation Activity                                                                |
| --------------------------- | --------------------------------------------------------------------------------------- |
| Stage 3 (Architecture)      | Define test architecture in TSD; select frameworks and tools                            |
| Stage 5 (Development)       | Write unit and integration tests alongside feature development; maintain test framework |
| Stage 6 (Code Review)       | Verify unit test coverage for new code; review test quality                             |
| Stage 7 (Automated Testing) | Execute full test suite; produce Test Results Report; classify defects                  |
| Stage 8 (Integrity)         | Run regression test suite; verify all fixed functionalities pass; no trim-to-pass       |
| Stage 9 (i18n)              | Run l10n regression tests: verify all localized strings render correctly                |
| Stage 10 (Release)          | Final regression pass; validate release candidate against all test suites               |

## Quality Standards

- **Test pass rate:** 100% of non-quarantined tests must pass for Stage 7 gate
- **Code coverage:** Minimum 80% line coverage, 70% branch coverage for all production code
- **E2E coverage:** All PRD-defined user journeys must have at least one E2E test
- **Flaky test rate:** <1% of test suite may be quarantined at any time
- **Parallel execution efficiency:** Test suite wall-clock time must be <30 minutes (full suite)
- **Test execution reliability:** >99% of test runs must complete without infrastructure failures
- **Defect detection rate:** Test suite must catch >95% of defects introduced in each sprint
- **Regression coverage:** 100% of previously fixed defects must have regression tests

## Reference Materials

- Android Testing: https://developer.android.com/training/testing
- iOS Testing: https://developer.apple.com/documentation/xctest
- Maestro Testing: https://maestro.mobile.dev/
- Espresso Testing: https://developer.android.com/training/testing/espresso
- XCUITest: https://developer.apple.com/documentation/xctest/xcuitest
- Firebase Test Lab: https://firebase.google.com/docs/test-lab
- AWS Device Farm: https://aws.amazon.com/device-farm/
- Test Pyramid (Martin Fowler): https://martinfowler.com/articles/practical-test-pyramid.html
- Flaky Tests (Google): https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
