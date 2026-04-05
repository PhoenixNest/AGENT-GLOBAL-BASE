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

## Execution Guidance

### Test Runner Architecture

```typescript
// Custom test runner with parallelization and reporting
// Built on top of Jest/Vitest for extensibility

import { Worker } from "worker_threads";
import { EventEmitter } from "events";
import * as path from "path";

interface TestResult {
  filePath: string;
  testName: string;
  status: "pass" | "fail" | "skip" | "flaky";
  duration: number;
  error?: string;
  retryCount: number;
}

interface TestRunnerConfig {
  testPattern: string;
  maxWorkers: number;
  retryFlakyTests: number;
  quarantineThreshold: number; // Times failed before quarantine
  reporters: ("json" | "junit" | "html" | "console")[];
  setupFiles?: string[];
  teardownFiles?: string[];
}

class ParallelTestRunner extends EventEmitter {
  private config: TestRunnerConfig;
  private results: TestResult[] = [];
  private flakyTestHistory: Map<string, number[]> = new Map();

  constructor(config: TestRunnerConfig) {
    super();
    this.config = config;
  }

  async run(testFiles: string[]): Promise<TestResult[]> {
    // 1. Discover tests in each file
    const testGroups = await this.discoverTests(testFiles);

    // 2. Sort by duration (longest first) for better load balancing
    testGroups.sort((a, b) => b.estimatedDuration - a.estimatedDuration);

    // 3. Distribute across workers
    const workerResults = await this.distributeToWorkers(testGroups);

    // 4. Aggregate results
    this.results = workerResults.flat();

    // 5. Detect flaky tests
    const flakyTests = this.detectFlakyTests();

    // 6. Generate reports
    await this.generateReports(this.results, flakyTests);

    return this.results;
  }

  private async discoverTests(files: string[]): Promise<TestGroup[]> {
    // Parse test files to identify individual tests
    // Estimate duration based on historical data
    return files.map((file) => ({
      file,
      tests: this.parseTestNames(file),
      estimatedDuration: this.getHistoricalDuration(file),
    }));
  }

  private async distributeToWorkers(
    groups: TestGroup[],
  ): Promise<TestResult[][]> {
    const workers: Worker[] = [];
    const results: TestResult[][] = [];

    // Create worker pool
    for (let i = 0; i < this.config.maxWorkers; i++) {
      const worker = new Worker(path.resolve(__dirname, "test-worker.js"), {
        workerData: {
          config: this.config,
          flakyHistory: Object.fromEntries(this.flakyTestHistory),
        },
      });
      workers.push(worker);
    }

    // Distribute test groups using longest-processing-time-first
    const assignments: TestGroup[][] = Array.from(
      { length: workers.length },
      () => [],
    );
    let workerIndex = 0;

    for (const group of groups) {
      assignments[workerIndex].push(group);
      workerIndex = (workerIndex + 1) % workers.length;
    }

    // Execute in parallel
    const promises = workers.map((worker, i) => {
      return new Promise<TestResult[]>((resolve, reject) => {
        worker.on("message", (result: TestResult[]) => resolve(result));
        worker.on("error", reject);
        worker.on("exit", (code) => {
          if (code !== 0)
            reject(new Error(`Worker ${i} exited with code ${code}`));
        });
        worker.postMessage(assignments[i]);
      });
    });

    const allResults = await Promise.all(promises);

    // Cleanup workers
    await Promise.all(workers.map((w) => w.terminate()));

    return allResults;
  }

  private detectFlakyTests(): string[] {
    const flaky: string[] = [];

    for (const [testName, history] of this.flakyTestHistory) {
      if (history.length < 5) continue; // Need minimum samples

      const passRate = history.filter((h) => h === 1).length / history.length;

      // Flaky: passes sometimes, fails sometimes (20-80% pass rate)
      if (passRate > 0.2 && passRate < 0.8) {
        flaky.push(testName);
      }
    }

    return flaky;
  }

  private async generateReports(results: TestResult[], flakyTests: string[]) {
    const summary = {
      total: results.length,
      passed: results.filter((r) => r.status === "pass").length,
      failed: results.filter((r) => r.status === "fail").length,
      flaky: flakyTests.length,
      duration: results.reduce((sum, r) => sum + r.duration, 0),
    };

    for (const reporter of this.config.reporters) {
      switch (reporter) {
        case "json":
          await this.writeJsonReport(results, summary);
          break;
        case "junit":
          await this.writeJunitReport(results, summary);
          break;
        case "html":
          await this.writeHtmlReport(results, summary, flakyTests);
          break;
        case "console":
          this.printConsoleReport(results, summary, flakyTests);
          break;
      }
    }
  }
}

// Test worker (runs in separate thread)
// test-worker.js
import { parentPort, workerData } from "worker_threads";

parentPort!.on("message", async (testGroups: TestGroup[]) => {
  const results: TestResult[] = [];

  for (const group of testGroups) {
    // Provision test environment
    const env = await provisionTestEnvironment();

    try {
      // Run setup files
      for (const setup of workerData.config.setupFiles || []) {
        await import(setup);
      }

      // Run tests with retry for flaky detection
      for (const test of group.tests) {
        let passed = false;
        let retries = 0;
        let error: string | undefined;

        while (retries <= workerData.config.retryFlakyTests) {
          try {
            await runTest(test);
            passed = true;
            break;
          } catch (err: any) {
            error = err.message;
            retries++;
          }
        }

        results.push({
          filePath: group.file,
          testName: test.name,
          status: passed ? "pass" : "fail",
          duration: test.duration,
          error,
          retryCount: retries - 1,
        });
      }
    } finally {
      // Cleanup environment
      await cleanupTestEnvironment(env);
    }
  }

  parentPort!.postMessage(results);
});
```

### Test Environment Provisioning

```yaml
# docker-compose.test.yml — Ephemeral test environment
version: "3.8"

services:
  # PostgreSQL with test data
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
    ports:
      - "5432" # Dynamic port
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test_user"]
      interval: 2s
      timeout: 3s
      retries: 10
    tmpfs:
      - /var/lib/postgresql/data # In-memory for speed

  # Redis for cache testing
  redis:
    image: redis:7-alpine
    ports:
      - "6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 2s
      timeout: 3s
      retries: 5

  # Kafka for event testing
  kafka:
    image: confluentinc/cp-kafka:7.5.0
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      zookeeper:
        condition: service_healthy
    healthcheck:
      test:
        ["CMD-SHELL", "kafka-topics --bootstrap-server localhost:9092 --list"]
      interval: 5s
      timeout: 10s
      retries: 10

  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    healthcheck:
      test: ["CMD-SHELL", "echo ruok | nc localhost 2181"]
      interval: 5s
      timeout: 5s
      retries: 10

  # WireMock for external API mocking
  wiremock:
    image: wiremock/wiremock:2.35.0
    volumes:
      - ./test-data/wiremock:/home/wiremock
    ports:
      - "8089"

  # Test runner
  test-runner:
    build:
      context: .
      dockerfile: Dockerfile.test
    environment:
      DATABASE_URL: postgresql://test_user:test_password@postgres:5432/test_db
      REDIS_URL: redis://redis:6379
      KAFKA_BROKERS: kafka:9092
      EXTERNAL_API_URL: http://wiremock:8080
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      kafka:
        condition: service_healthy
      wiremock:
        condition: service_started
    command: npm run test:ci
```

**Testcontainers for per-test isolation:**

```typescript
// testcontainers setup for integration tests
import {
  PostgreSqlContainer,
  StartedPostgreSqlContainer,
} from "@testcontainers/postgresql";
import { RedisContainer } from "@testcontainers/redis";

describe("UserRepository Integration Tests", () => {
  let postgres: StartedPostgreSqlContainer;
  let db: Database;

  beforeAll(async () => {
    // Start PostgreSQL container
    postgres = await new PostgreSqlContainer("postgres:16-alpine")
      .withDatabase("test_db")
      .withUsername("test_user")
      .withPassword("test_password")
      .withExposedPorts(5432)
      .withStartupTimeout(30_000)
      .start();

    // Connect and run migrations
    const connectionString = postgres.getConnectionUri();
    db = new Database(connectionString);
    await db.migrate();
  }, 60_000);

  afterAll(async () => {
    await postgres.stop();
  });

  beforeEach(async () => {
    // Clean state before each test
    await db.query("TRUNCATE users, orders, order_items CASCADE");
  });

  test("creates user and retrieves by ID", async () => {
    const user = await db.users.create({
      name: "Test User",
      email: "test@example.com",
    });

    expect(user.id).toBeDefined();

    const retrieved = await db.users.findById(user.id);
    expect(retrieved).toEqual(user);
  });

  test("handles duplicate email", async () => {
    await db.users.create({
      name: "User 1",
      email: "dup@example.com",
    });

    await expect(
      db.users.create({
        name: "User 2",
        email: "dup@example.com",
      }),
    ).rejects.toThrow("duplicate key");
  });
});
```

### Flaky Test Detection

```python
# flaky_test_detector.py — Statistical analysis of test results
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta

class FlakyTestDetector:
    def __init__(self, test_results: pd.DataFrame):
        """
        test_results columns:
          - test_name: Full test name
          - timestamp: Test execution time
          - status: pass/fail
          - duration_ms: Test duration
          - build_id: Build identifier
          - runner: Test runner identifier
          - retry_count: Number of retries
        """
        self.data = test_results

    def detect_flaky_tests(self, min_runs: int = 20) -> pd.DataFrame:
        """
        Detect flaky tests using statistical analysis.
        A test is flaky if its pass rate is significantly different from
        both 0% and 100%.
        """
        # Aggregate by test name
        test_stats = self.data.groupby('test_name').agg(
            total_runs=('status', 'count'),
            pass_count=('status', lambda x: (x == 'pass').sum()),
            fail_count=('status', lambda x: (x == 'fail').sum()),
            avg_duration=('duration_ms', 'mean'),
            max_duration=('duration_ms', 'max'),
            retry_rate=('retry_count', lambda x: (x > 0).mean()),
        )

        # Filter tests with minimum runs
        test_stats = test_stats[test_stats['total_runs'] >= min_runs]

        # Calculate pass rate
        test_stats['pass_rate'] = test_stats['pass_count'] / test_stats['total_runs']

        # Flaky detection: pass rate between 20% and 80%
        # (excluding tests that always pass or always fail)
        flaky = test_stats[
            (test_stats['pass_rate'] > 0.20) &
            (test_stats['pass_rate'] < 0.80)
        ].copy()

        # Confidence score (higher = more confident it's flaky)
        # Using binomial confidence interval
        flaky['confidence'] = flaky.apply(
            lambda row: self._flaky_confidence(
                row['pass_count'], row['total_runs']
            ),
            axis=1
        )

        # Categorize flakiness type
        flaky['flaky_type'] = flaky.apply(self._categorize_flakiness, axis=1)

        return flaky.sort_values('confidence', ascending=False)

    def _flaky_confidence(self, passes: int, total: int) -> float:
        """Calculate confidence that a test is flaky (not just random noise)."""
        if total < 10:
            return 0.0

        # Use Wilson score interval
        p = passes / total
        n = total
        z = 1.96  # 95% confidence

        denominator = 1 + z**2 / n
        center = (p + z**2 / (2 * n)) / denominator
        spread = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denominator

        # Confidence is highest when pass rate is ~50%
        # and decreases as it approaches 0% or 100%
        distance_from_extremes = min(
            abs(center - 0),
            abs(center - 1)
        )

        # Narrow interval = high confidence
        interval_width = 2 * spread
        confidence = distance_from_extremes * (1 - interval_width)

        return max(0, min(1, confidence))

    def _categorize_flakiness(self, row: pd.Series) -> str:
        """Categorize the type of flakiness."""
        if row['retry_rate'] > 0.5:
            return 'timing-dependent'
        elif row['max_duration'] > row['avg_duration'] * 5:
            return 'performance-sensitive'
        elif row['pass_rate'] > 0.5:
            return 'occasionally-failing'
        else:
            return 'occasionally-passing'

    def quarantine_recommendations(self) -> list:
        """Generate quarantine recommendations for flaky tests."""
        flaky = self.detect_flaky_tests()

        recommendations = []
        for test_name, row in flaky.iterrows():
            recommendations.append({
                'test': test_name,
                'action': 'quarantine' if row['confidence'] > 0.7 else 'monitor',
                'reason': f"Pass rate: {row['pass_rate']:.1%}, "
                         f"Type: {row['flaky_type']}, "
                         f"Confidence: {row['confidence']:.1%}",
                'investigation': self._suggest_investigation(row['flaky_type']),
            })

        return recommendations

    def _suggest_investigation(self, flaky_type: str) -> str:
        suggestions = {
            'timing-dependent': 'Check for race conditions, async operations, sleep dependencies',
            'performance-sensitive': 'Check for resource contention, GC pauses, network latency',
            'occasionally-failing': 'Check for shared state, environment dependencies, data ordering',
            'occasionally-passing': 'Check for test logic errors, assertion issues, cleanup problems',
        }
        return suggestions.get(flaky_type, 'Investigate test and environment')
```

**Flaky test quarantine workflow:**

```markdown
# Flaky Test Quarantine Process

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
```

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
```

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
