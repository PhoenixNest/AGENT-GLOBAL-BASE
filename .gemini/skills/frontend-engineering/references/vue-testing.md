---
version: "1.0.0"
---

# Vue Testing

| Competency                     | Description                                                                     | Quality Criteria                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Vitest Configuration**       | Test runner setup, globals, coverage, mocking, environment configuration        | Zero-config Vitest for Vue; coverage thresholds enforced; MSW integration        |
| **Vue Test Utils**             | Mounting strategies, reactive state testing, event simulation, slot testing     | Tests use `mount`/`shallowMount` appropriately; all reactive states verified     |
| **Component Testing Patterns** | Testing props, emits, slots, composables, async components, Suspense            | Every component tested for default render, props variants, emits, and edge cases |
| **Cypress E2E**                | End-to-end test architecture, network stubbing, custom commands, CI integration | All critical user flows have E2E tests; flaky test rate = 0                      |
| **Visual Regression**          | Pixel-perfect comparison, baseline management, CI integration, diff analysis    | Visual regression CI gate; baseline updates require CDO approval                 |
| **Composable Testing**         | Testing reactive state, side effects, lifecycle hooks, async operations         | All composables have unit tests; reactive state transitions verified             |

## Pipeline Integration

| Pipeline Stage                       | Responsibility                                                        | Deliverable                                    |
| ------------------------------------ | --------------------------------------------------------------------- | ---------------------------------------------- |
| **Stage 2** (Web Prototype + IDS)    | Identify testable behaviors and visual baselines from IDS             | Test requirements in IDS, visual baseline plan |
| **Stage 5** (Development)            | Write unit tests, component tests, E2E tests, visual regression tests | Test suite alongside Vue codebase              |
| **Stage 6** (Code Review)            | Review test quality, coverage, E2E flow completeness                  | Testing section in DEFECT-REPORT.md            |
| **Stage 7** (Automated Testing)      | Execute full test suite; meet coverage thresholds                     | Test results report                            |
| **Stage 8** (Integrity Verification) | Run visual regression against baselines; verify IDS fidelity          | Visual integrity verification report           |

## Quality Standards

| Metric                     | Target                                                  | Enforcement                         |
| -------------------------- | ------------------------------------------------------- | ----------------------------------- |
| **Unit test coverage**     | ≥ 80% lines, ≥ 90% branches                             | CI gate via Vitest coverage         |
| **Component coverage**     | 100% of components have tests                           | Test file audit                     |
| **Composable coverage**    | 100% of composables have tests                          | Test file audit                     |
| **E2E coverage**           | All critical user flows have E2E tests                  | Test audit against user journey map |
| **Visual regression**      | All key screens have visual baselines                   | Visual test audit                   |
| **Flaky test rate**        | Zero flaky tests in CI                                  | CI retry analysis                   |
| **Test execution time**    | Unit tests < 30s, E2E < 5 minutes                       | CI timing metrics                   |
| **MSW coverage**           | 100% of API calls mocked in unit/component tests        | Test audit                          |
| **Reactive state testing** | All reactive state transitions verified                 | Code review                         |
| **Emit testing**           | All component emits have tests                          | Code review                         |
| **Slot testing**           | All slot variants tested                                | Code review                         |
| **Baseline management**    | Visual baselines updated only with CDO approval         | PR review process                   |
| **Error path coverage**    | All error states tested (network, validation, boundary) | Code review; mutation testing       |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
