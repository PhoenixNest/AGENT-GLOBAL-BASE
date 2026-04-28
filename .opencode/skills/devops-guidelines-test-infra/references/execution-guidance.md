# Execution Guidance

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
```

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

````

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
````

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
```
