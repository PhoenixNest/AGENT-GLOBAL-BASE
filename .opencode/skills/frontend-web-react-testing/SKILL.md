---
name: frontend-web-react-testing
description: React testing discipline — component unit testing, integration testing, custom hook validation, E2E user flow verification, async operations, API mocking, and accessibility validation. Owned by Amira Voss (Frontend Chapter Lead). Use during Stage 7 (Automated Testing) for React test infrastructure and Stage 6 (Code Review) for test quality review. Trigger: react testing, react testing library, component testing, hook testing, e2e react, api mocking, accessibility testing.
prerequisites:
  - frontend-web-overview

version: "1.0.0"
---

# React Testing

**Category:** Frontend Testing
**Owner:** Senior Frontend Engineer

## Overview

Comprehensive React testing discipline covering component unit testing, integration testing, custom hook validation, and end-to-end user flow verification. Emphasizes testing user behavior over implementation details, with production-grade patterns for async operations, API mocking, accessibility validation, and visual regression detection.

## Competency Dimensions

| Dimension                         | Description                                                               | Proficiency Indicators                                                                                                    |
| --------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **React Testing Library Mastery** | Querying, user-event simulation, and debugging RTL patterns               | Uses `getByRole` as primary query; never uses `getByTestId` without justification; writes tests that mirror user behavior |
| **Async Component Testing**       | Testing loading states, race conditions, error boundaries, and Suspense   | Correctly awaits `findBy*` queries; handles `waitFor` timeouts; tests Suspense fallbacks                                  |
| **Custom Hook Testing**           | Isolating and testing hook logic with `@testing-library/react-hooks`      | Uses `renderHook` with custom wrapper; tests all hook return paths including error states                                 |
| **API Mocking (MSW)**             | Service worker–based network interception for realistic integration tests | Configures MSW handlers at test setup; uses runtime handlers for per-test overrides; tests error responses                |
| **Context & Provider Testing**    | Testing components that depend on React Context, Redux, or Zustand        | Creates reusable test wrappers; isolates provider behavior from component logic                                           |
| **Snapshot Testing Discipline**   | Knowing when snapshots add value vs. when they create maintenance debt    | Uses snapshots for stable UI contracts only; never snapshots large component trees without intent                         |
| **Accessibility Testing**         | Automated a11y assertion integration with axe-core                        | Every component test includes `expect(container).toBeAccessible()`; tests keyboard navigation                             |
| **Visual Regression Testing**     | Pixel-diff detection with Storybook + Chromatic/Percy                     | Catches unintended visual changes; approves intentional design updates with design team sign-off                          |
| **CI Integration**                | Jest/Vitest configuration, coverage thresholds, parallel execution        | Tests run in <30s for full suite; coverage gates block merge; flaky test quarantine process                               |

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                           |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 5 — Development**            | Tests are written alongside component development (TDD/ATDD). Platform Lead ensures all new components have corresponding test files. |
| **Stage 6 — Code Review**            | Test coverage and quality are reviewed. Defect Report includes missing tests for critical paths as P2 defects.                        |
| **Stage 7 — Automated Testing**      | Full test suite execution. This skill defines the test architecture that Stage 7 runs. Test Lead validates test suite completeness.   |
| **Stage 8 — Integrity Verification** | Accessibility test results verified. Visual regression baselines confirmed. Test coverage thresholds enforced.                        |
| **Stage 10 — Release Readiness**     | Test results contribute to Item 5 (100% automated test pass rate). Any P0/P1 test failures block release.                             |

## Quality Standards

| Standard                                   | Metric                                    | Enforcement                                               |
| ------------------------------------------ | ----------------------------------------- | --------------------------------------------------------- |
| **Test Pass Rate**                         | 100%                                      | CI blocks merge on any failure                            |
| **Function Coverage**                      | ≥90%                                      | Vitest/Jest threshold gates                               |
| **Branch Coverage**                        | ≥80%                                      | Coverage report reviewed at Stage 6                       |
| **Flaky Test Rate**                        | <1%                                       | Monitored in CI; quarantined immediately                  |
| **Accessibility**                          | 0 axe-core violations                     | Every component test includes a11y assertion              |
| **Visual Regression**                      | 0 unapproved diffs                        | Chromatic/Percy blocks PR on unexpected changes           |
| **Test Execution Time**                    | <30s (full suite)                         | CI performance monitoring; parallelization required       |
| **No `getByTestId` Without Justification** | Documented exceptions only                | Code review check                                         |
| **No `any` in Test Files**                 | TypeScript strict mode                    | ESLint `@typescript-eslint/no-explicit-any` in test files |
| **Every Error Path Tested**                | All catch blocks and error states covered | Branch coverage metric                                    |

**Defect Classification for Test Failures:**

| Scenario                                          | Severity | Rationale                                                  |
| ------------------------------------------------- | -------- | ---------------------------------------------------------- |
| Test passes locally but fails in CI               | P1       | Indicates environment-dependent behavior — production risk |
| Missing tests for critical user flow              | P2       | Gap in safety net, but not a broken feature                |
| Flaky test (>5% failure rate)                     | P1       | Erodes trust in test suite; blocks reliable CI             |
| Coverage below threshold                          | P2       | Technical debt, not a functional defect                    |
| Accessibility violations in production components | P0       | Legal/compliance risk; blocks release                      |
| Snapshot update without design team approval      | P1       | Potential unapproved visual regression                     |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
