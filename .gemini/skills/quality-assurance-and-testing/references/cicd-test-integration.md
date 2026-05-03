---
name: cicd-test-integration
description: Integrate the full mobile test suite into CI/CD pipelines — configuring parallel test execution, test result reporting, flaky test handling, and gate conditions that block deployment if critical test failures occur.
version: "1.0.0"
---

# CICD Test Integration

| Competency            | Description                                                          | Quality Criteria                                                                                                      |
| --------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Pipeline Design       | Design CI stages for unit, integration, and UI tests with caching    | Test stages run in parallel where possible; Gradle/Xcode caches reduce build time; each stage has a time SLA          |
| Test Result Reporting | Publish test results to CI dashboard with failure details            | JUnit XML reports published; flaky test annotations visible in PR; failures link to logs with sufficient context      |
| Gate Conditions       | Block PR merge and deployment on test failures                       | Unit test failures block PR merge; E2E failures on critical flows block deployment; test results visible in PR status |
| Emulator Management   | Manage Android emulator lifecycle in CI (startup, snapshot, cleanup) | Emulators use snapshots for fast startup (< 30s); emulators terminated after test run; no port conflicts between jobs |

## Execution Guidance

### GitHub Actions Mobile Test Pipeline

```yaml
jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gradle/actions/setup-gradle@v3
      - run: ./gradlew testDebugUnitTest
      - uses: mikepenz/action-junit-report@v4
        with:
          report_paths: "**/TEST-*.xml"

  instrumented-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          script: ./gradlew connectedAndroidTest
```

### Test Stage Time SLAs

| Stage             | Time SLA | Action if Exceeded                     |
| ----------------- | -------- | -------------------------------------- |
| Unit tests        | < 5 min  | Investigate slow tests; add sharding   |
| Integration tests | < 15 min | Add sharding; parallelize modules      |
| UI / E2E tests    | < 30 min | Add device sharding; reduce test scope |
