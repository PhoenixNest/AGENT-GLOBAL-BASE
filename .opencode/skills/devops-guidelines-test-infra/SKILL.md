---
name: devops-guidelines-test-infra
description: Test infrastructure for mobile CI/CD — device farm management (Firebase Test Lab, AWS Device Farm, BrowserStack), emulator/simulator orchestration, parallel test execution, flaky test detection, and test result aggregation for Android and iOS automated testing. Owned by Thomas Zhang (DevOps Lead). Use during Stage 4 (Implementation Plan) for test infrastructure design and Stage 7 (Testing) for test execution orchestration. Trigger: test infrastructure, device farm, Firebase Test Lab, AWS Device Farm, BrowserStack, emulator orchestration, parallel tests, flaky test detection, test result aggregation.
prerequisites:
  - devops-guidelines-ci-cd-optimization

version: "1.0.0"
---

# Test Infrastructure

**Category:** Developer Experience (Testing)
**Owner:** Developer Experience Engineer (Zara Okonkwo)

## Overview

Builds and maintains the test infrastructure that enables fast, reliable, and scalable test execution across the organization, covering test runner architecture with discovery and parallelization, test environment provisioning with Docker Compose and testcontainers, flaky test detection with statistical analysis and quarantine mechanisms, and test result aggregation with dashboarding for team visibility.

## Competency Dimensions

| Dimension                     | Description                                                                              | Proficiency Indicators                                                                                                                                             |
| ----------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Test Runner Architecture      | Test discovery, parallelization, reporting, plugin architecture, custom reporters        | Designs test runners that discover and execute tests efficiently; implements parallel execution with proper isolation; creates custom reporters for CI integration |
| Test Environment Provisioning | Docker Compose orchestration, testcontainers, ephemeral environments, cleanup automation | Provisions isolated test environments on demand; manages service dependencies; ensures clean state between test runs                                               |
| Flaky Test Detection          | Statistical analysis, retry mechanisms, quarantine, root cause categorization            | Identifies flaky tests through statistical analysis; implements quarantine for unreliable tests; categorizes flakiness root causes                                 |
| Result Aggregation            | Multi-format result parsing, trend analysis, dashboard creation, alerting                | Aggregates test results from multiple runners; tracks flakiness trends; creates dashboards for team visibility; alerts on test health degradation                  |

## Detection Criteria

- Test fails > 20% and < 80% of the time over last 50 runs
- Statistical confidence > 70%

## Quarantine Actions

1. **Mark as flaky** in test framework (skip by default)
2. **Create tracking issue** with flakiness analysis
3. **Assign to owning team** for investigation
4. **Set SLA**: 2 weeks to fix or delete

## Re-enrollment Criteria

- Test passes 100 consecutive runs in CI
- Root cause identified and fixed
- Code review approval from test infrastructure team

## Quarantine Dashboard

| Test                                  | Flaky Since | Type                  | Owner    | SLA Due    | Status        |
| ------------------------------------- | ----------- | --------------------- | -------- | ---------- | ------------- |
| UserProfileTest.testAvatarUpload      | 2026-03-15  | timing-dependent      | Frontend | 2026-04-12 | Investigating |
| OrderServiceTest.testConcurrentUpdate | 2026-03-20  | race-condition        | Backend  | 2026-04-17 | Fix in PR     |
| PaymentGatewayTest.testTimeout        | 2026-03-25  | performance-sensitive | Payments | 2026-04-22 | Quarantined   |

````

### Test Result Aggregation and Dashboarding

```typescript
// Test result aggregator — combines results from multiple runners
interface TestSuiteResult {
  runner: string;
  timestamp: string;
  build_id: string;
  total: number;
  passed: number;
  failed: number;
  skipped: number;
  flaky: number;
  duration_ms: number;
  tests: TestResult[];
}

class TestResultDashboard {
  private results: TestSuiteResult[] = [];

  async aggregate(runners: string[]): Promise<TestSuiteResult> {
    const suiteResults = await Promise.all(
      runners.map((r) => this.fetchResults(r)),
    );

    return {
      runner: "aggregated",
      timestamp: new Date().toISOString(),
      build_id: suiteResults[0].build_id,
      total: suiteResults.reduce((sum, r) => sum + r.total, 0),
      passed: suiteResults.reduce((sum, r) => sum + r.passed, 0),
      failed: suiteResults.reduce((sum, r) => sum + r.failed, 0),
      skipped: suiteResults.reduce((sum, r) => sum + r.skipped, 0),
      flaky: suiteResults.reduce((sum, r) => sum + r.flaky, 0),
      duration_ms: Math.max(...suiteResults.map((r) => r.duration_ms)),
      tests: suiteResults.flatMap((r) => r.tests),
    };
  }

  generateTrendReport(days: number = 30): TrendReport {
    const recent = this.results.filter(
      (r) => new Date(r.timestamp) > new Date(Date.now() - days * 86400000),
    );

    const daily = recent.reduce(
      (acc, r) => {
        const day = r.timestamp.slice(0, 10);
        if (!acc[day]) acc[day] = { total: 0, passed: 0, failed: 0, flaky: 0 };
        acc[day].total += r.total;
        acc[day].passed += r.passed;
        acc[day].failed += r.failed;
        acc[day].flaky += r.flaky;
        return acc;
      },
      {} as Record<string, any>,
    );

    return {
      period_days: days,
      daily_data: daily,
      pass_rate_trend: this.calculateTrend(daily, "pass_rate"),
      flaky_count_trend: this.calculateTrend(daily, "flaky_count"),
      duration_trend: this.calculateTrend(daily, "duration"),
    };
  }

  generateHealthScore(): number {
    const recent = this.results.slice(-100);

    const passRate =
      recent.reduce((s, r) => s + r.passed / r.total, 0) / recent.length;
    const flakyRate =
      recent.reduce((s, r) => s + r.flaky / r.total, 0) / recent.length;
    const avgDuration =
      recent.reduce((s, r) => s + r.duration_ms, 0) / recent.length;

    // Health score: 0-100
    // Weighted: 50% pass rate, 30% flaky rate, 20% duration
    const passScore = passRate * 100;
    const flakyScore = Math.max(0, 100 - flakyRate * 500); // 20% flaky = 0 score
    const durationScore = Math.max(0, 100 - (avgDuration / 60000) * 10); // 10 min = 0 score

    return Math.round(passScore * 0.5 + flakyScore * 0.3 + durationScore * 0.2);
  }
}
````

**Dashboard metrics:**

| Metric                  | Description                        | Alert Threshold |
| ----------------------- | ---------------------------------- | --------------- |
| Pass rate               | % of tests passing                 | < 95%           |
| Flaky test count        | Tests with inconsistent results    | > 10            |
| Test duration (P95)     | 95th percentile test time          | > 5 minutes     |
| Test coverage           | Code coverage percentage           | < 80%           |
| Quarantined tests       | Tests skipped due to flakiness     | > 5% of total   |
| Test health score       | Composite score (0-100)            | < 70            |
| Time to fix flaky tests | Average time from detection to fix | > 2 weeks       |

## Pipeline Integration

**Stage 5 (Development):** Test infrastructure provisioned. Test runners configured with parallelization. Flaky detection system operational.

**Stage 6 (Code Review):** Review validates that new tests work within test infrastructure. Test environment dependencies documented.

**Stage 7 (Testing):** Full test suite executed through test infrastructure. Flaky detection analysis run. Test results aggregated and reported.

**Stage 8 (Integrity Verification):** Panel reviews test infrastructure health score. Quarantined test list reviewed. Test environment reproducibility validated.

## Quality Standards

| Metric                               | Target                                      | Measurement              |
| ------------------------------------ | ------------------------------------------- | ------------------------ |
| Test runner parallelism              | > 80% CPU utilization during test execution | Resource monitoring      |
| Test environment provisioning time   | < 2 minutes                                 | Startup timing           |
| Flaky test detection accuracy        | > 90% true positive rate                    | Detection audit          |
| Flaky test quarantine rate           | < 5% of total tests                         | Quarantine dashboard     |
| Test result aggregation completeness | 100% of test runs reported                  | Aggregation audit        |
| Test health score                    | > 80/100                                    | Dashboard metric         |
| Test environment cleanup             | 100% cleanup after test run                 | Resource leak monitoring |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
