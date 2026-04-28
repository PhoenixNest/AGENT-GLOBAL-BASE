---
name: frontend-web-react-testing-advanced
description: Advanced React testing patterns — React Testing Library user-centric methodology, Mock Service Worker for network-level API mocking, multi-component integration testing, and Stage 7 test infrastructure. Owned by Amira Voss (Frontend Chapter Lead). Use during Stage 7 (Automated Testing) for advanced test patterns and Stage 6 (Code Review) for test architecture review. Trigger: advanced react testing, msw, mock service worker, integration testing react, react testing patterns, user-centric testing.
prerequisites:
  - frontend-web-react-testing

version: "1.0.0"
---

# Advanced React Testing

**Category:** Frontend Engineering / Testing
**Owner:** Frontend Engineer (Yuna Park)

## Overview

This skill establishes the React testing discipline that ensures component correctness, integration reliability, and user experience quality across all frontend deliverables. It covers React Testing Library's user-centric testing philosophy, component testing patterns that test behavior over implementation, Mock Service Worker for API mocking at the network level, integration testing for multi-component workflows, and the testing infrastructure needed to support the Stage 7 Automated Testing gate. Tests are written from the user's perspective — if a test can't distinguish between a correct and incorrect implementation based on observable behavior, it's testing the wrong thing.

## Competency Dimensions

| Dimension                             | Description                                                                             | Proficiency Indicators                                                                              |
| ------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **React Testing Library Mastery**     | User-centric queries, event simulation, async testing, accessibility assertions         | Zero implementation-detail tests (no testing state variables, refs, or internal methods)            |
| **Component Testing Patterns**        | Testing props, state transitions, side effects, error boundaries, Suspense boundaries   | Every component has tests covering default render, props variants, error states, and loading states |
| **Mock Service Worker**               | Network-level API mocking, request matching, response handlers, MSW lifecycle           | All API interactions mocked at network level; zero fetch/axios mocking                              |
| **Integration Testing**               | Multi-component workflows, form submissions, navigation flows, state transitions        | End-to-end user flows tested with real component tree, not isolated mocks                           |
| **Test Infrastructure**               | Jest/Vitest configuration, custom render functions, test utilities, coverage thresholds | Shared test utilities in `test-utils.tsx`; coverage thresholds enforced in CI                       |
| **Testing Anti-patterns Recognition** | Identifying and eliminating shallow testing, implementation coupling, flaky tests       | Zero tests that break on refactoring; zero tests that pass for wrong reasons                        |

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                     | Deliverable                          |
| ------------------------------------ | ------------------------------------------------------------------ | ------------------------------------ |
| **Stage 2** (Web Prototype + IDS)    | Identify testable behaviors from IDS specifications                | Test requirements in IDS             |
| **Stage 3** (Architecture)           | Define testing architecture; register ADRs for test tool selection | Testing ADRs                         |
| **Stage 5** (Development)            | Write component tests, integration tests, MSW handlers             | Test suite alongside production code |
| **Stage 6** (Code Review)            | Review test quality, coverage, anti-patterns                       | Testing section in DEFECT-REPORT.md  |
| **Stage 7** (Automated Testing)      | Execute full test suite; meet coverage thresholds; fix defects     | Test results report                  |
| **Stage 8** (Integrity Verification) | Verify tests cover all IDS-specified behaviors                     | Test integrity verification          |
| **Stage 10** (Release Readiness)     | Confirm testing sign-off (Item 5: "100% automated test pass rate") | Testing compliance contribution      |

## Quality Standards

| Metric                        | Target                                                                      | Enforcement                                |
| ----------------------------- | --------------------------------------------------------------------------- | ------------------------------------------ |
| **Test coverage**             | ≥ 80% lines, ≥ 90% branches                                                 | CI gate via Istanbul/Vitest coverage       |
| **Component coverage**        | 100% of components have at least one test                                   | Test file audit                            |
| **RTL query discipline**      | 100% of queries use role/label/text (zero getByTestId unless documented)    | Code review; eslint rule                   |
| **No implementation testing** | Zero tests that access component state, refs, or internal methods           | Code review                                |
| **MSW coverage**              | 100% of API calls mocked at network level                                   | Test audit; zero fetch/axios mocks         |
| **Integration test coverage** | All critical user flows have integration tests                              | Test audit against user journey map        |
| **Flaky test rate**           | Zero flaky tests in CI                                                      | CI retry analysis; flaky tests quarantined |
| **Test execution time**       | Full test suite completes in < 60 seconds                                   | CI timing metrics                          |
| **Accessibility testing**     | All component tests include accessibility assertions                        | RTL `jest-axe` integration                 |
| **Error path coverage**       | All error states tested (network errors, validation errors, boundary cases) | Code review; mutation testing              |
| **Custom render usage**       | All tests use shared `render` function with providers                       | Code review                                |
| **Test readability**          | Tests follow AAA pattern (Arrange, Act, Assert)                             | Code review                                |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
