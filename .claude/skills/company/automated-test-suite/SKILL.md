---
name: company-automated-test-suite
description: Automated test suite design and execution for iOS and Android — unit, integration, and E2E test layers; test pyramid standards; XCTest, XCUITest, Espresso, UiAutomator, Maestro, Detox; regression testing gates; 100% pass rate target. Owned by Priscilla Oduya (Test Lead).
disable-model-invocation: false
---

# Automated Test Suite

## Purpose

Design, implement, and execute a comprehensive automated test suite for the project's iOS and Android codebases. The suite must achieve a 100% pass rate (accounting for user-approved P2/P3 deferrals) before Stage 7 closes. All failing tests block Stage 7 advancement until resolved or explicitly deferred by the user via the P0–P3 protocol.

## Test Pyramid

Every project uses a three-layer test pyramid:

```
        /‾‾‾‾‾‾‾‾‾‾\
       /  E2E Tests  \     ← 10–15% of test count
      /‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
     / Integration Tests \ ← 20–30% of test count
    /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
   /     Unit Tests        \← 60–70% of test count
  /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
```

### Layer 1: Unit Tests

- **Scope:** Individual functions, classes, use cases, view models — no network, no database, no UI
- **Coverage target:** 100% of domain layer (use cases, domain models); ≥80% of data layer (repositories, mappers)
- **Tools:** JUnit 5 + MockK (Android); XCTest + Swift Testing (iOS); kotlin.test (KMP shared)
- **Run time target:** Full suite completes in < 2 minutes

### Layer 2: Integration Tests

- **Scope:** Module boundaries — repository + database, repository + API (with mock server), ViewModel + use case
- **Coverage target:** All repository implementations; all API integration points
- **Tools:** Robolectric (Android); XCTest with in-memory stores (iOS); WireMock for API mocking
- **Run time target:** Full suite completes in < 10 minutes

### Layer 3: E2E Tests (UI Automation)

- **Scope:** Full user flows on real or emulated devices — from app launch to flow completion
- **Coverage target:** All primary user flows from PRD; all critical error paths
- **Tools:** Maestro (cross-platform, preferred for speed); Espresso/UiAutomator (Android complex flows); XCUITest (iOS flows requiring platform-native gestures)
- **Run time target:** Full suite completes in < 30 minutes on CI

## Test Case Design

For each test case, document:

```
Test ID:     TC-{NNN}
Layer:       [Unit | Integration | E2E]
Platform:    [Android | iOS | Both]
PRD Ref:     [PRD section and requirement number]
Description: [One sentence — what user behaviour or system behaviour is being verified]
Setup:       [Preconditions and test data]
Steps:       [Numbered steps]
Expected:    [Exact expected result]
Severity:    [P0 | P1 | P2 | P3] — what severity is this if it fails?
```

## Regression Testing Protocol

After any bug fix:

1. Re-run the full test suite for the affected module
2. Re-run all E2E tests for flows that touch the modified code path
3. Regression passes when: all previously passing tests still pass AND the bug-fix test now passes
4. No regression is acceptable — a test that passed before the fix must still pass after

## Bug Report Format

When tests fail, produce a Bug Report:

```
Bug ID:       BUG-{NNN}
Test ID:      TC-{NNN}
Severity:     P0 | P1 | P2 | P3
Platform:     Android | iOS | Both
Description:  [What failed — specific, no vague language]
Steps to reproduce: [Exact steps]
Expected:     [What should happen]
Actual:       [What happened instead]
Stack trace:  [If available]
Assigned to:  [Platform lead responsible for this code area]
```

## Test Results Report

Upon suite completion, produce the Test Results Report:

```markdown
# Test Results Report — {Project Name} — {Date}

## Summary

- Total test cases: {N}
- Passed: {N}
- Failed: {N}
- Skipped / Deferred (user-approved P2/P3): {N}

## Coverage

- Unit layer: {N} tests, {N}% pass rate
- Integration layer: {N} tests, {N}% pass rate
- E2E layer: {N} tests, {N}% pass rate

## Defects Identified

[Table of all BUG-{NNN} entries with severity, status, and assigned engineer]

## Regression Results

[Confirmation that all previously passing tests still pass after bug fixes]

## Stage 7 Gate Status

[ ] 100% pass rate achieved (or all failures are user-approved P2/P3 deferrals)
[ ] Regression testing passed for all fixed functionalities
[ ] Report archived
```
