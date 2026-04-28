---
name: testing-qa-strategy-cicd-test-integration
description: CI/CD test integration for mobile pipelines — test execution triggers, quality gate configuration, test result publishing, flaky test quarantine, pipeline test orchestration, and test failure notification for GitHub Actions, GitLab CI, and Bitrise. Owned by Tobias Weber (SDET). Use during Stage 4 (Implementation Plan) for test pipeline design and Stage 5 (Development) for CI/CD test integration. Trigger: CI/CD test integration, test execution triggers, quality gates, test result publishing, flaky test quarantine, pipeline orchestration, GitHub Actions testing.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
---

# CI/CD Test Integration

## 1. Overview

### Why CI/CD Test Integration Matters

CI/CD test integration is the backbone of a reliable, fast, and safe software delivery pipeline. It ensures that every code change is validated through automated gates before reaching production. Poor test integration leads to broken releases, manual firefighting, and eroded team confidence.

Well-integrated test pipelines provide:

- **Fast feedback** — developers learn about failures within minutes of committing code.
- **Consistent quality gates** — every change must meet the same objective standards.
- **Defect containment** — bugs are caught at the earliest possible stage, where fix cost is lowest.
- **Audit trail** — every test run is recorded with results, coverage, and metrics.
- **Release confidence** — passing the full pipeline is evidence that the release is ready.

### Pipeline Test Stages

| Phase                     | Pipeline Position        | Test Types                                       | Typical Timeout |
| ------------------------- | ------------------------ | ------------------------------------------------ | --------------- |
| Phase 1: Fast Feedback    | PR trigger, before merge | Linting, static analysis, unit tests             | 5-10 min        |
| Phase 2: Integration      | After Phase 1 passes     | Integration tests, API contract tests            | 15-20 min       |
| Phase 3: Quality Gates    | After Phase 2 passes     | Coverage checks, security scans, flaky detection | 10 min          |
| Phase 4: Device/E2E       | Main branch only         | Device farm tests, E2E suites                    | 30-45 min       |
| Phase 5: Gate Enforcement | After all phases         | Threshold evaluation, merge decision             | 5 min           |

### Pipeline Stage Alignment

| Pipeline Stage                   | Test Integration Responsibility | Key Output                                         |
| -------------------------------- | ------------------------------- | -------------------------------------------------- |
| Stage 5 (Development)            | CTO + Platform Leads            | Unit tests pass on every platform build            |
| Stage 6 (Code Review)            | CTO Panel + CSO                 | SAST/DAST scans clean, no critical vulnerabilities |
| Stage 7 (Automated Testing)      | CTO + Test Lead                 | Full test suite results, TEST-RESULTS-REPORT.md    |
| Stage 8 (Integrity Verification) | CTO Panel                       | Performance budgets met, regression tests pass     |
| Stage 10 (Release Readiness)     | CTO Panel + User                | Release smoke tests pass on RC artifact            |

---

## 2. Pipeline Architecture

### Parallel Execution

Modern CI pipelines should maximize parallelism to minimize wall-clock feedback time. The goal is to keep Phase 1 under 5 minutes for any PR.

```yaml
# .github/workflows/test-pipeline.yml
name: Test Pipeline
on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  # Phase 1: Fast feedback — runs first, fails fast
  lint-and-static-analysis:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - name: Run linters
        run: ./scripts/lint.sh
      - name: Run static analysis
        run: ./scripts/static-analysis.sh

  unit-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - name: Run unit tests (shard ${{ matrix.shard }})
        run: ./scripts/test-unit.sh --shard ${{ matrix.shard }} --total-shards 4
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: unit-test-results-shard-${{ matrix.shard }}
          path: build/test-results/unit/*.xml

  # Phase 2: Integration tests — only if Phase 1 passes
  integration-tests:
    needs: [lint-and-static-analysis, unit-tests]
    runs-on: ubuntu-latest
    timeout-minutes: 15
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - name: Run integration tests
        run: ./scripts/test-integration.sh
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
```

### Sharding Strategy

Sharding distributes tests across multiple parallel runners. The goal is to keep each shard under the target time budget.

| Shard Count | Target Time Per Shard | Total Wall Clock |
| ----------- | --------------------- | ---------------- |
| 1 shard     | <30 min               | <30 min          |
| 2 shards    | <15 min               | <15 min          |
| 4 shards    | <7.5 min              | <7.5 min         |
| 8 shards    | <3.75 min             | <3.75 min        |

Sharding should be **dynamic** when possible — test runners should report execution time so the sharding algorithm can rebalance for optimal distribution across runs.

### Selective Test Execution

Not all tests need to run on every commit. Use file-change-based selection to accelerate feedback:

| Change Pattern                    | Tests to Run                     |
| --------------------------------- | -------------------------------- |
| Only `docs/` changed              | Skip all tests                   |
| Only `platforms/android/` changed | Android unit + integration tests |
| Only `platforms/ios/` changed     | iOS unit + integration tests     |
| Only `platforms/flutter/` changed | Flutter unit + widget tests      |
| Shared module changed             | All platform tests               |
| Pipeline config changed           | All tests + smoke suite          |

```yaml
# Selective execution example
jobs:
  determine-changes:
    runs-on: ubuntu-latest
    outputs:
      android: ${{ steps.filter.outputs.android }}
      ios: ${{ steps.filter.outputs.ios }}
      shared: ${{ steps.filter.outputs.shared }}
    steps:
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            android:
              - 'platforms/android/**'
              - 'shared/**'
            ios:
              - 'platforms/ios/**'
              - 'shared/**'
            shared:
              - 'shared/**'
              - 'api/**'
```

### Caching Strategy

Cache aggressively to reduce pipeline execution time:

| Cache Target           | Key Pattern                                     | TTL      |
| ---------------------- | ----------------------------------------------- | -------- |
| Gradle dependencies    | `gradle-${{ hashFiles('**/*.gradle*') }}`       | 7 days   |
| CocoaPods              | `cocoapods-${{ hashFiles('**/Podfile.lock') }}` | 7 days   |
| npm/yarn               | `npm-${{ hashFiles('**/package-lock.json') }}`  | 7 days   |
| Compiled test fixtures | `test-fixtures-${{ github.sha }}`               | 24 hours |
| Build cache            | `build-${{ github.sha }}`                       | 24 hours |

---

## 3. Test Environments

### Ephemeral Environments

Every PR should have an isolated test environment that mirrors production as closely as possible.

```yaml
# Ephemeral environment provisioning
jobs:
  provision-environment:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy ephemeral preview
        run: |
          ENV_NAME="pr-${{ github.event.pull_request.number }}"
          ./scripts/deploy-ephemeral.sh "$ENV_NAME"
          echo "ENV_URL=https://${ENV_NAME}.preview.example.com" >> $GITHUB_ENV

      - name: Seed test data
        run: ./scripts/seed-database.sh "$ENV_URL"

      - name: Run tests smoke tests
        run: ./scripts/smoke-tests.sh "$ENV_URL"

  teardown-environment:
    needs: [provision-environment]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Teardown ephemeral environment
        run: |
          ENV_NAME="pr-${{ github.event.pull_request.number }}"
          ./scripts/teardown-ephemeral.sh "$ENV_NAME"
```

### Database Management Strategies

| Strategy                   | Use Case          | Pros                       | Cons                                |
| -------------------------- | ----------------- | -------------------------- | ----------------------------------- |
| Transactional rollback     | Unit tests        | Fast, isolated, repeatable | Not suitable for integration tests  |
| Fresh schema migration     | Integration tests | Clean state every run      | Slow on large schemas               |
| Containerized DB with seed | E2E tests         | Production-like            | Resource-intensive                  |
| In-memory DB (H2, SQLite)  | Fast unit tests   | Zero infrastructure        | Dialect differences from production |

### Mock Services

External dependencies must be mocked or stubbed in CI:

| Service Type                  | Mock Strategy    | Tool                                |
| ----------------------------- | ---------------- | ----------------------------------- |
| REST APIs                     | WireMock stubs   | WireMock                            |
| GraphQL                       | Mocked resolvers | Apollo Mock Provider                |
| Push notifications (FCM/APNS) | Fake push server | Mock push server                    |
| Payment gateways              | Sandbox mode     | Stripe test mode, Braintree sandbox |
| Analytics                     | No-op collector  | Disabled in test builds             |

---

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`4.-test-reporting.md`](references/4.-test-reporting.md) — 4. Test Reporting
- [`5.-gate-enforcement.md`](references/5.-gate-enforcement.md) — 5. Gate Enforcement
- [`6.-flaky-test-management.md`](references/6.-flaky-test-management.md) — 6. Flaky Test Management
- [`7.-device-farm-integration.md`](references/7.-device-farm-integration.md) — 7. Device Farm Integration
- [`8.-security-testing.md`](references/8.-security-testing.md) — 8. Security Testing
- [`9.-stage-5+-integration.md`](references/9.-stage-5+-integration.md) — 9. Stage 5+ Integration
- [`10.-references.md`](references/10.-references.md) — 10. References
