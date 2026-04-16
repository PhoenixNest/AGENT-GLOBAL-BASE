---
name: cicd-test-integration
description: CI/CD test integration strategy covering automated test pipeline design, gate configuration, test sharding, flaky test detection, coverage enforcement, and reliable feedback loops for mobile application development.
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

## 4. Test Reporting

### JUnit XML Aggregation

All test frameworks should output JUnit XML format for unified aggregation:

```yaml
# Aggregate test results from all shards
jobs:
  aggregate-results:
    needs: [unit-tests]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: all-results/

      - name: Merge JUnit XML
        run: |
          npx junit-merge \
            --input all-results/ \
            --output merged-test-results.xml

      - name: Upload merged results
        uses: actions/upload-artifact@v4
        with:
          name: merged-test-results
          path: merged-test-results.xml
```

### Trend Analysis

Track test metrics over time to identify regressions:

| Metric                 | Warning Threshold   | Fail Threshold      |
| ---------------------- | ------------------- | ------------------- |
| Test pass rate         | <98%                | <95%                |
| Average execution time | +20% over 7-day avg | +50% over 7-day avg |
| New test failures      | >5 new failures     | >20 new failures    |
| Coverage change        | -2% overall         | -5% overall         |
| Flaky test count       | >3 flaky tests      | >10 flaky tests     |

### Dashboard Integration

Pipeline runs should produce structured metrics suitable for dashboard ingestion:

```json
{
  "pipeline_run_id": "run-20260406-001",
  "timestamp": "2026-04-06T10:30:00Z",
  "branch": "main",
  "commit_sha": "abc123",
  "stages": {
    "unit_tests": {
      "status": "passed",
      "duration_seconds": 187,
      "total": 2450,
      "passed": 2450,
      "failed": 0,
      "skipped": 0
    },
    "integration_tests": {
      "status": "passed",
      "duration_seconds": 412,
      "total": 380,
      "passed": 378,
      "failed": 0,
      "skipped": 2
    },
    "e2e_tests": {
      "status": "failed",
      "duration_seconds": 890,
      "total": 85,
      "passed": 83,
      "failed": 2,
      "skipped": 0
    }
  },
  "coverage": { "lines": 87.3, "branches": 82.1, "functions": 91.0 },
  "flaky_tests_detected": 1,
  "gate_result": "failed"
}
```

### Allure Report

Allure provides rich HTML test reports with history, trends, and categorization:

```yaml
jobs:
  publish-allure:
    needs: [aggregate-results]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Generate Allure report
        uses: simple-elf/allure-report-action@v1.7
        with:
          allure_results: all-results/
          allure_report: allure-report/

      - name: Upload Allure report
        uses: actions/upload-artifact@v4
        with:
          name: allure-report
          path: allure-report/
```

---

## 5. Gate Enforcement

Gate criteria are evaluated after test execution. Failure to meet any gate criterion blocks pipeline progression.

### Coverage Thresholds

| Metric                   | Minimum Threshold | Target | Enforced At |
| ------------------------ | ----------------- | ------ | ----------- |
| Line coverage            | 80%               | 90%+   | Stage 7     |
| Branch coverage          | 70%               | 85%+   | Stage 7     |
| Function coverage        | 85%               | 95%+   | Stage 7     |
| New code coverage        | 90%               | 95%+   | Stage 6, 7  |
| Critical module coverage | 95%               | 100%   | Stage 7, 8  |

```yaml
# Coverage gate enforcement
jobs:
  coverage-gate:
    needs: [unit-tests]
    runs-on: ubuntu-latest
    steps:
      - name: Check coverage thresholds
        run: |
          COVERAGE_JSON=$(cat coverage/coverage-summary.json)
          LINE_PCT=$(echo "$COVERAGE_JSON" | jq '.total.lines.pct')
          BRANCH_PCT=$(echo "$COVERAGE_JSON" | jq '.total.branches.pct')

          if (( $(echo "$LINE_PCT < 80" | bc -l) )); then
            echo "::error::Line coverage ${LINE_PCT}% is below 80% threshold"
            exit 1
          fi
          if (( $(echo "$BRANCH_PCT < 70" | bc -l) )); then
            echo "::error::Branch coverage ${BRANCH_PCT}% is below 70% threshold"
            exit 1
          fi
```

### Flakiness Limits

| Metric                              | Warning      | Block Pipeline           |
| ----------------------------------- | ------------ | ------------------------ |
| Flaky test rate                     | >1% of suite | >5% of suite             |
| Consecutive flaky runs on same test | >3 retries   | >10 retries on same test |
| New flaky tests persisted per run   | >1           | >5                       |

### Performance Budgets

| Metric                  | Budget                            | Enforced At |
| ----------------------- | --------------------------------- | ----------- |
| App cold start          | <2 seconds (Android), <1.5s (iOS) | Stage 8     |
| Screen render time      | <16ms (60fps)                     | Stage 8     |
| API response time (p95) | <500ms                            | Stage 7     |
| APK/IPA size            | <100MB (Android), <200MB (iOS)    | Stage 8     |
| Memory usage (peak)     | <256MB                            | Stage 8     |

### Failure Handling Protocol

| Failure Scenario                     | Action                         | Notification                            |
| ------------------------------------ | ------------------------------ | --------------------------------------- |
| Unit test failure                    | Block PR merge                 | PR comment + Slack #test-failures       |
| Integration test failure             | Block PR merge                 | PR comment + Slack #test-failures       |
| E2E flaky failure (first occurrence) | Log + allow merge with warning | PR comment                              |
| E2E flaky failure (>3 occurrences)   | Quarantine test                | Slack #flaky-tests + issue auto-created |
| Coverage regression                  | Block merge to main            | PR comment                              |
| Performance budget exceeded          | Block Stage 8 progression      | CTO notification                        |

---

## 6. Flaky Test Management

### Detection

Flaky tests are detected by running the same test multiple times and observing inconsistent results:

```yaml
# Flaky test detection job
jobs:
  flaky-test-scan:
    runs-on: ubuntu-latest
    schedule:
      - cron: "0 2 * * *" # Run daily at 2 AM
    steps:
      - name: Run tests 10x
        run: |
          for i in {1..10}; do
            ./scripts/test-unit.sh --json > results-run-${i}.json
          done
          ./scripts/detect-flaky.sh results-run-*.json > flaky-report.json

      - name: Upload flaky report
        uses: actions/upload-artifact@v4
        with:
          name: flaky-report
          path: flaky-report.json
```

### Quarantine Process

When a test is confirmed flaky (>3 inconsistent results in 10 runs):

1. **Tag the test** with `@flaky` or equivalent annotation
2. **Exclude from gate calculations** — flaky tests do not block pipelines
3. **Auto-create an issue** in the tracking system, with flaky test details
4. **Assign to owning team** for remediation within 2 sprints
5. **Monitor in quarantine** — run flaky tests in a separate nightly job

```yaml
# Quarantined test execution (separate from gate-enforced tests)
jobs:
  quarantined-tests:
    runs-on: ubuntu-latest
    schedule:
      - cron: "0 3 * * *"
    steps:
      - name: Run quarantined tests
        run: ./scripts/test-quarantined.sh
        continue-on-error: true

      - name: Report flaky status
        run: ./scripts/flaky-status.sh
```

### Auto-Retry Policy

| Context           | Max Retries | Behavior                                   |
| ----------------- | ----------- | ------------------------------------------ |
| PR pipeline       | 1           | Retry once; if still fails, block merge    |
| Nightly build     | 3           | Retry up to 3 times; log results           |
| Release candidate | 0           | No retries — failures must be investigated |
| Quarantined tests | 5           | High retry count for detection accuracy    |

### Remediation Workflow

```
Flaky test detected
       |
       v
Classify: Infrastructure vs. Test code vs. Product code
       |
       ├── Infrastructure → File with DevOps (race condition, timing, resource contention)
       ├── Test code → File with Test Lead (assertion ordering, cleanup, test data)
       └── Product code → File with platform team (non-determinism, threading, state management)
       |
       v
Quarantine + auto-create issue
       |
       v
Assign owner + 2-sprint SLA
       |
       v
Fix verified → Remove quarantine tag → Re-enable in pipeline
```

---

## 7. Device Farm Integration

Mobile applications must be tested on real devices, not just emulators/simulators. Device farms provide access to diverse hardware and OS combinations.

### AWS Device Farm

```yaml
jobs:
  aws-device-farm:
    needs: [build-android, build-ios]
    runs-on: ubuntu-latest
    steps:
      - name: Upload to Device Farm
        run: |
          aws devicefarm create-upload \
            --project-arn "${DEVICE_FARM_PROJECT_ARN}" \
            --name "app-${GITHUB_SHA}.apk" \
            --type ANDROID_APP \
            --content build/outputs/apk/release/app-release.apk

      - name: Schedule test run
        run: |
          aws devicefarm schedule-run \
            --project-arn "${DEVICE_FARM_PROJECT_ARN}" \
            --device-pool-arn "${DEVICE_POOL_ARN}" \
            --test type=APPIUM_JAVA_TESTJUNIT,testSpecArn=${TEST_SPEC_ARN} \
            --name "run-${GITHUB_SHA}"

      - name: Wait for results
        run: |
          aws devicefarm wait run-complete \
            --arn "${RUN_ARN}" \
            --max-attempts 60 --delay 60

      - name: Download results
        run: |
          aws devicefarm list-artifacts \
            --arn "${RUN_ARN}" \
            --type RESULT
```

### Firebase Test Lab

```yaml
jobs:
  firebase-test-lab:
    needs: [build-android]
    runs-on: ubuntu-latest
    steps:
      - name: Run in Firebase Test Lab
        run: |
          gcloud firebase test android run \
            --type instrumentation \
            --app build/outputs/apk/release/app-release.apk \
            --test build/outputs/apk/androidTest/app-debug-androidTest.apk \
            --device model=redfin,version=31,locale=en,orientation=portrait \
            --device model=shiba,version=34,locale=en,orientation=portrait \
            --timeout 30m \
            --results-bucket "gs://${FIREBASE_RESULTS_BUCKET}"

      - name: Parse results
        run: ./scripts/parse-firebase-results.sh
```

### BrowserStack (Web Frontend)

```yaml
jobs:
  browserstack-e2e:
    needs: [deploy-preview]
    runs-on: ubuntu-latest
    steps:
      - name: Run BrowserStack tests
        run: |
          npx browserstack-cypress run \
            --sync \
            --specs "cypress/e2e/**/*.cy.js" \
            --config-file browserstack.json
```

### Cost Optimization

| Strategy                             | Savings             | Implementation                        |
| ------------------------------------ | ------------------- | ------------------------------------- |
| Run device tests only on main merges | ~60% reduction      | `if: github.ref == 'refs/heads/main'` |
| Selective device matrix              | ~40% reduction      | Test only affected OS versions        |
| Parallel device provisioning         | ~50% time reduction | Request all devices simultaneously    |
| Result caching for unchanged modules | ~30% reduction      | Skip tests for unchanged app modules  |
| Spot/preemptible instances           | ~70% cost reduction | Use spot VMs for non-critical runs    |

---

## 8. Security Testing

Security tests run as part of the CI/CD pipeline, not as a separate manual process.

### SAST (Static Application Security Testing)

```yaml
jobs:
  sast-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run CodeQL analysis
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: "/language:${{ matrix.language }}"
```

### DAST (Dynamic Application Security Testing)

```yaml
jobs:
  dast-scan:
    needs: [deploy-preview]
    runs-on: ubuntu-latest
    steps:
      - name: Run OWASP ZAP scan
        uses: zaproxy/action-full-scan@v0.8.0
        with:
          target: ${{ env.ENV_URL }}
          rules_file_name: .github/zap/rules.tsv
          allow_issue_writing: true
          fail_action: true
```

### Dependency Scanning

| Tool                   | Language              | Pipeline Stage       |
| ---------------------- | --------------------- | -------------------- |
| Dependabot             | All                   | Stage 5 (continuous) |
| npm audit              | JavaScript/TypeScript | Stage 5              |
| Safety / pip-audit     | Python                | Stage 5              |
| GoSec                  | Go                    | Stage 5              |
| OWASP Dependency-Check | All (transitive)      | Stage 7              |

### Container Scanning

```yaml
jobs:
  container-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Build image
        run: docker build -t app:${GITHUB_SHA} .

      - name: Run Trivy scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: app:${GITHUB_SHA}
          format: sarif
          output: trivy-results.sarif
          severity: CRITICAL,HIGH
          exit-code: 1
```

### Security Gate Criteria

| Check              | Threshold                     | Action on Failure                   |
| ------------------ | ----------------------------- | ----------------------------------- |
| Critical CVEs      | 0 allowed                     | Block pipeline                      |
| High CVEs          | 0 allowed                     | Block pipeline                      |
| Medium CVEs        | <5 with documented exceptions | Block with user override            |
| Secrets detected   | 0 allowed                     | Block pipeline + rotate credentials |
| License violations | 0 allowed                     | Block pipeline                      |

---

## 9. Stage 5+ Integration

### Full Pipeline Example

```yaml
# .github/workflows/full-pipeline.yml
name: Full Pipeline
on:
  pull_request:
    branches: [main]
  push:
    branches: [main, develop]

permissions:
  contents: read
  checks: write
  pull-requests: write

jobs:
  # === PHASE 1: Fast Feedback (<5 min) ===
  phase1-fast-feedback:
    strategy:
      matrix:
        job: [lint, type-check, unit-tests]
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@v4
      - name: Run ${{ matrix.job }}
        run: ./scripts/${{ matrix.job }}.sh

  # === PHASE 2: Integration (<15 min) ===
  phase2-integration:
    needs: phase1-fast-feedback
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
    steps:
      - uses: actions/checkout@v4
      - name: Run integration tests
        run: ./scripts/test-integration.sh

  # === PHASE 3: Quality Gates ===
  phase3-quality-gates:
    needs: phase2-integration
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Check coverage thresholds
        run: ./scripts/check-coverage.sh
      - name: Check for new flaky tests
        run: ./scripts/check-flaky.sh
      - name: Security scan (SAST)
        uses: github/codeql-action/analyze@v3

  # === PHASE 4: Device Testing (main only) ===
  phase4-device-testing:
    needs: phase3-quality-gates
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 45
    steps:
      - name: Run device farm tests
        run: ./scripts/device-farm.sh

  # === PHASE 5: Gate Enforcement ===
  phase5-gate-enforcement:
    needs: [phase3-quality-gates, phase4-device-testing]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Evaluate gate criteria
        run: |
          ALL_PASSED=true

          if [ "${{ needs.phase3-quality-gates.result }}" != "success" ]; then
            echo "::error::Quality gate failed"
            ALL_PASSED=false
          fi

          if [ "${{ github.ref }}" = "refs/heads/main" ] && \
             [ "${{ needs.phase4-device-testing.result }}" != "success" ]; then
            echo "::error::Device testing failed on main"
            ALL_PASSED=false
          fi

          if [ "$ALL_PASSED" = "false" ]; then
            echo "::error::Pipeline gate FAILED — merge blocked"
            exit 1
          fi

          echo "All gates passed — merge permitted"
```

### Gate Criteria Summary by Pipeline Stage

| Stage    | Gate Criteria                          | Enforcement Mechanism         |
| -------- | -------------------------------------- | ----------------------------- |
| Stage 5  | Unit tests pass on every commit        | PR status check (required)    |
| Stage 6  | No new critical SAST findings          | CodeQL analysis               |
| Stage 7  | 100% test pass rate (P0/P1 tests)      | Test result aggregation       |
| Stage 7  | Coverage meets minimum thresholds      | Coverage gate job             |
| Stage 7  | No new flaky tests (>3)                | Flaky detection scan          |
| Stage 8  | Performance budgets met                | Performance test job          |
| Stage 8  | Security scans clean (0 critical/high) | SAST + DAST + dependency scan |
| Stage 10 | Release candidate smoke tests pass     | Smoke test on RC artifact     |

### Escalation Protocol

| Scenario                     | Escalation Path            | Timeline        |
| ---------------------------- | -------------------------- | --------------- |
| Pipeline blocked >4 hours    | CTO notification           | Immediate       |
| Security vulnerability found | CSO + CTO                  | Immediate       |
| Flaky test rate >10%         | Test Lead + platform leads | Within 24 hours |
| Coverage regression >5%      | CTO + team supervisor      | Within 1 sprint |
| Device farm failures >20%    | Platform leads + DevOps    | Within 24 hours |
| Performance budget exceeded  | CTO + platform leads       | Within 1 sprint |

---

## 10. References

### Related Skills

| Skill                  | Location                         | Relevance                            |
| ---------------------- | -------------------------------- | ------------------------------------ |
| Testing QA Overview    | `.gemini/skills/testing-qa/`     | Parent skill category                |
| Android Testing        | `.gemini/skills/android/`        | Platform-specific test configuration |
| iOS Testing            | `.gemini/skills/ios/`            | Platform-specific test configuration |
| Cross-Platform Testing | `.gemini/skills/cross-platform/` | KMP/Flutter test strategies          |
| Frontend Web Testing   | `.gemini/skills/frontend-web/`   | Web E2E and component tests          |
| Backend Testing        | `.gemini/skills/backend/`        | API and integration tests            |
| Security               | `.gemini/skills/security/`       | SAST/DAST integration                |
| DevOps                 | `.gemini/skills/devops/`         | Pipeline infrastructure and CI/CD    |
| Shared                 | `.gemini/skills/shared/`         | Cross-cutting TDD practices          |

### Pipeline Document References

| Document               | Location                                            | Purpose                         |
| ---------------------- | --------------------------------------------------- | ------------------------------- |
| Pipeline Definition    | `.gemini/pipeline/mobile-development/pipeline.md`   | 10-stage pipeline specification |
| Monitoring System      | `company/pipeline/mobile-development/monitoring.md` | Progress tracking and recovery  |
| Defect Severity System | `GEMINI.md`                                         | P0-P3 defect classification     |

### External Resources

| Resource                     | URL                                                        | Purpose                       |
| ---------------------------- | ---------------------------------------------------------- | ----------------------------- |
| GitHub Actions Documentation | https://docs.github.com/actions                            | CI/CD pipeline reference      |
| OWASP CI/CD Security         | https://owasp.org/www-project-top-10-ci-cd-security-risks/ | CI/CD security best practices |
| Allure Framework             | https://docs.qameta.io/allure/                             | Test reporting dashboard      |
| Firebase Test Lab            | https://firebase.google.com/docs/test-lab                  | Mobile device testing         |
| AWS Device Farm              | https://aws.amazon.com/device-farm/                        | Real device testing           |
| BrowserStack                 | https://www.browserstack.com/                              | Cross-browser testing         |
