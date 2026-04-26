---
name: ios-testing-quality-ios-testing
description: "iOS testing with XCTest and XCUITest — unit testing, UI automation, snapshot testing, protocol-based mocking, test parallelization, and flaky test quarantine. Owned by Seo-Yeon Park (iOS Lead). Use during Stage 7 (Automated Testing) for test suite development and Stage 6 (Code Review) for test coverage evaluation. Trigger: xctest, xcuitest, snapshot testing, ios testing, unit test, ui test, mocking, test parallelization, flaky test, xcodebuild test, test plan."
prerequisites:
  - ios-infrastructure-ios-implementation

version: "1.0.0"
---

# iOS Testing

**Category:** Mobile Engineering — iOS Testing
**Owner:** iOS Engineer (Arjun Mehta)

## Overview

This skill establishes comprehensive iOS testing practices covering XCTest framework, XCUITest for UI automation, snapshot testing for visual regression, mocking strategies, and test parallelization. It is foundational to Stage 7 (Automated Testing) where the 100% automated test pass rate target is enforced, and Stage 6 (Code Review) where test coverage and quality are evaluated.

## Competency Dimensions

| Dimension            | Description                                                                                                  | Proficiency Indicators                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| XCTest Framework     | Test lifecycle, async/await test support, expectations, performance testing, test suites                     | All test types covered (unit, integration, performance); async tests use native async/await; performance tests have baselines |
| XCUITest             | UI element queries, interaction recording, accessibility-based queries, launch arguments, screenshot capture | UI tests use accessibility identifiers; launch arguments configure test environment; screenshots captured on failure          |
| Snapshot Testing     | Image comparison, tolerance configuration, device-specific snapshots, dark mode snapshots, CI integration    | Snapshot tests catch visual regressions; tolerance set appropriately per device; dark/light mode snapshots maintained         |
| Mocking              | Protocol-based mocks, mock generators, stub responses, call verification, async mock support                 | All dependencies mockable via protocol; mock behavior configurable per test; call verification for side effects               |
| Test Parallelization | Test plan parallelization, device sharding, test prioritization, flaky test isolation, CI integration        | Tests run in parallel on CI; flaky tests quarantined; test execution time <30 minutes for full suite                          |

## Pipeline Integration

- **Stage 5 (Development):** TDD practiced during development. Unit tests and mock implementations built alongside production code.
- **Stage 6 (Code Review):** Test coverage reviewed: domain layer >80%, presentation >60%, data layer >70%. Test quality assessed.
- **Stage 7 (Automated Testing):** Primary stage for this skill. Full test suite execution: unit tests, UI tests, snapshot tests. Target: 100% pass rate.
- **Stage 8 (Integrity Verification):** Regression test suite executed on all fixed functionalities. Snapshot tests verify no visual regressions.

## Quality Standards

- **>80%** unit test coverage on domain layer
- **>60%** test coverage on presentation layer
- **>70%** test coverage on data layer
- **100%** of public ViewModel methods have unit tests
- **100%** of core user flows have XCUITest coverage
- Snapshot tests cover **all screen states** (loading, loaded, error, empty)
- Snapshot tests cover **light and dark mode**
- Snapshot tests cover **all supported device sizes**
- **Zero** flaky tests in CI — flaky tests quarantined with JIRA tracking
- All XCUITests use **accessibility identifiers** — not raw text queries
- Screenshot captured and attached on **every UI test failure**
- Full test suite completes in **<30 minutes** on CI with parallelization
- Performance tests have **established baselines** — regression flagged automatically

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
