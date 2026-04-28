---
name: quality-engineering-strategy
description: Quality engineering strategy at enterprise scale: test pyramid design, quality scorecard with release gate authority, SDET team structure, product risk calibration, flaky test management, and 100% automated test pass rate enforcement across 57 engineers and 5 divisions.
version: "1.0.0"
---

# Quality Engineering Strategy

## Purpose

Own quality strategy, test architecture, and release gate authority for all engineering output across 5 divisions (57 FTEs). The VP of Quality Engineering ensures that quality is engineered into the product — not inspected in after the fact. This means test design happens in parallel with feature design, not after.

## Test Pyramid Architecture

### Layer Definitions and Enforcement

```
                    ┌──────────────────┐
                    │   E2E Tests      │  10% — Full user journeys (Maestro/Cypress)
                    │   (<2 hours)     │  Nightly only. Never block PRs on E2E alone.
                    ├──────────────────┤
                    │ Integration      │  20% — Cross-service contracts, API testing
                    │   (<15 min)      │  Run on merge to main. Block on contract failures.
                    ├──────────────────┤
                    │ Unit Tests       │  70% — Fast, deterministic, isolated
                    │   (<5 min)       │  Run on every PR. Block on any failure.
                    └──────────────────┘
```

### Test Execution Triggers

| Trigger       | Test Suite                                              | Time Budget | Gate Action                                    |
| ------------- | ------------------------------------------------------- | ----------- | ---------------------------------------------- |
| PR opened     | Unit tests on changed modules + 2 levels of dependency  | <5 min      | Block merge on any failure                     |
| PR approved   | Unit + integration tests                                | <12 min     | Block merge on any failure                     |
| Merge to main | Full unit + integration suite                           | <15 min     | Block deployment on any failure                |
| Nightly (2am) | Full E2E on all device/OS combos + performance baseline | <2 hours    | Open P1 if any user journey fails              |
| Pre-release   | Full regression suite + exploratory testing session     | <4 hours    | Block release candidate promotion on any P0/P1 |

### Multi-Platform Test Infrastructure

| Platform             | Test Framework                          | Execution Environment                                              | Device Coverage                                                                             |
| -------------------- | --------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Android              | Espresso + UiAutomator                  | Firebase Test Lab                                                  | 15 physical devices (Pixel 6–8 Pro, Samsung S22–S24, OnePlus 11) + 10 emulators (API 28–34) |
| iOS                  | XCTest/XCUITest                         | AWS Device Farm                                                    | 12 physical devices (iPhone 13–15 Pro, SE 3rd gen) + simulators (iOS 15–17)                 |
| Cross-platform (KMP) | Shared Kotlin tests + platform adapters | CI runners (macOS + Linux)                                         | Shared test suite executed on both Android and iOS runners                                  |
| Web                  | Cypress + Playwright                    | GitHub Actions (headless Chrome, Firefox, Safari via BrowserStack) | Chrome 120+, Firefox 120+, Safari 17+                                                       |
| API                  | Pact contract testing + k6 performance  | CI runners                                                         | All API endpoints with consumer-driven contracts                                            |
| Backend              | Testcontainers + integration tests      | Docker-in-Docker on CI                                             | PostgreSQL 15, Redis 7, Kafka 3.6                                                           |

### Intelligent Test Selection

Not all tests need to run on every PR. Use code coverage mapping to select only affected tests:

```
PR changes: orders-service/src/main/java/com/company/orders/OrderService.java

Affected tests:
  ✅ OrderServiceTest.java (direct — same module)
  ✅ OrderControllerTest.java (depends on OrderService)
  ✅ OrderIntegrationTest.java (depends on OrderController)
  ❌ UserServiceTest.java (no dependency path)
  ❌ AuthE2ETest.cy.js (no dependency path)
```

**Implementation:** Maintain a module dependency graph. On PR open, compute the transitive closure of changed modules. Run tests only in affected modules. This reduces CI time by 40–60% while maintaining coverage guarantees.

### Flaky Test Management

**Definition:** A test is flaky if it passes/fails nondeterministically on unchanged code across 5+ consecutive runs.

**Detection algorithm:**

1. Nightly pipeline runs the full test suite twice on the same commit
2. Flag any test with different pass/fail results between runs
3. Auto-quarantine flagged tests (move to `flaky/` suite, excluded from PR gating)
4. Mandatory root cause analysis within 48 hours

**Common flaky test root causes:**

| Root Cause                                                         | Detection Pattern                                       | Fix                                                                                |
| ------------------------------------------------------------------ | ------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Timing dependency (test assumes response arrives in X ms)          | Test passes on fast CI, fails on slow CI; or vice versa | Replace `sleep()` with event-driven assertions; use mock clock                     |
| Shared mutable state (tests leak state between runs)               | Test order affects results                              | Reset state in `@BeforeEach`/`setUp`; use test containers for isolation            |
| Network dependency (test hits real external service)               | Fails when external service is down or rate-limited     | Mock external services with WireMock/MSW; use contract tests for API compatibility |
| Test data dependency (test assumes specific DB state)              | Passes on clean DB, fails on seeded DB                  | Use factory patterns for test data; never depend on pre-existing data              |
| Asynchronous operation (test checks result before async completes) | Intermittent failures                                   | Use `CountDownLatch`, `CompletableFuture.get(timeout)`, or polling assertions      |

**Target:** <2% of total test suite quarantined at any time. If quarantined tests exceed 2%, VP Quality halts feature work until flakiness is addressed.

## Quality Scorecard

### Composite Release Readiness Score (0–100)

| Metric                      | Weight | Elite (100 pts)        | Acceptable (70 pts)    | Unacceptable (0 pts) |
| --------------------------- | ------ | ---------------------- | ---------------------- | -------------------- |
| Test coverage               | 30%    | ≥90% line, ≥80% branch | ≥80% line, ≥70% branch | <75% line            |
| Flakiness rate              | 20%    | <0.5%                  | <2%                    | >5%                  |
| Escaped defect rate         | 25%    | <0.1 per release       | <0.5 per release       | >2 per release       |
| MTTR (P1 incidents)         | 15%    | <15 minutes            | <30 minutes            | >2 hours             |
| Release candidate pass rate | 10%    | ≥95% first-pass        | ≥85% first-pass        | <70% first-pass      |

**Score calculation:** Each metric is scored on a 0–100 scale, then weighted and summed. The composite score determines release eligibility.

### Release Gate Authority

| Score     | Action                                                                                                                             |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **≥85**   | Release candidate approved. Proceed to deployment.                                                                                 |
| **75–84** | Release candidate conditionally approved. VP Quality must provide written justification for any risk acceptance. CTO must co-sign. |
| **<75**   | Release candidate rejected. Engineering teams must fix blockers before re-submission.                                              |

**Veto authority:** VP Quality has unilateral authority to block any release regardless of scorecard. Written rationale required. This authority exists to prevent "ship it at all costs" pressure from overriding quality concerns.

**No trim-to-pass:** Removing a feature to make tests pass is never valid remediation. If a test fails, the code is broken — the fix is in the code, not in removing the test.

## SDET Team Structure

### Division of Responsibilities

| Role                              | % of Team | Responsibilities                                                                                                                                 | Tools                                                                  |
| --------------------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| **Test Infrastructure Engineers** | 40%       | Build and maintain test platforms, CI/CD integration, test selection algorithms, device farm management, flaky test detection system             | Testcontainers, Firebase Test Lab, AWS Device Farm, custom test runner |
| **Product QE Specialists**        | 40%       | Own quality for specific product areas (mobile, web, backend); write E2E tests; perform exploratory testing; define acceptance criteria with PMs | Maestro, Cypress, k6, exploratory testing sessions                     |
| **Performance QE Engineers**      | 20%       | Load testing, stress testing, performance regression detection, capacity planning, SLO validation                                                | k6, Gatling, JMeter, custom performance dashboards                     |

### SDET Skill Progression

| Level                | Scope                            | Technical Expectation                                                       |
| -------------------- | -------------------------------- | --------------------------------------------------------------------------- |
| SDET I               | Individual test authoring        | Write reliable, maintainable tests; understand test pyramid                 |
| SDET II              | Test framework design            | Design test DSLs, page object patterns, test data factories                 |
| Senior SDET          | Cross-platform test architecture | Design test strategies spanning Android, iOS, web, API; manage device farms |
| Test Automation Lead | Organization-wide test strategy  | Own test framework architecture, CI integration, quality metrics            |

## Product Risk Calibration

The VP of Quality must calibrate defect severity against **user impact**, not just technical correctness:

| Severity | User Impact                                     | Technical Impact                    | Examples                                                                  | Fix Timeline                    |
| -------- | ----------------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------- | ------------------------------- |
| **P0**   | Data loss, security breach, app crash on launch | System instability, data corruption | Login broken for all users, PII exposed in logs, crash on app open        | Immediate — blocks release      |
| **P1**   | Core feature broken, major UX failure           | Partial system degradation          | Payment processing fails, search returns no results, offline mode broken  | Before release — non-negotiable |
| **P2**   | Minor feature degraded, cosmetic issue          | Non-critical code path affected     | Profile picture not loading on specific device, typo in error message     | User decides — fix or defer     |
| **P3**   | Polish, nice-to-have                            | Code quality concern                | Animation timing slightly off, color contrast below WCAG AA on one screen | User decides — fix or defer     |

**Critical distinction:** A P1 from a user's perspective (can't complete checkout) may be a P3 from a code perspective (CSS issue). Calibrate to **user impact**, not code complexity.

## Quality Standards

- No release may pass with open P0 or P1 defects
- Regression test suite must achieve 100% pass rate before release candidate promotion
- All new features must have automated tests written before feature is marked complete
- Test execution time for full suite must not exceed 2 hours
- Flaky test rate target: <2% of total suite
- No test may be disabled without written justification and tracking ticket
- Test coverage must not decrease between releases (coverage gate enforced in CI)
