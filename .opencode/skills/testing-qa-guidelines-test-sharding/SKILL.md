---
name: testing-qa-guidelines-test-sharding
description: Test sharding for mobile CI/CD — parallel test execution across multiple devices/emulators, dynamic shard allocation, flaky test isolation, and test result aggregation for Android (Firebase Test Lab) and iOS (Xcode parallel testing). Owned by Rachel Kim (Test Automation Lead). Use during Stage 5 (Development) for test infrastructure setup and Stage 7 (Testing) for parallel test execution optimization. Trigger: test sharding, parallel test execution, dynamic shard allocation, flaky test isolation, Firebase Test Lab, Xcode parallel testing, test result aggregation.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
---

# Test Sharding

## Overview

This skill covers test sharding architecture, parallel test execution, and dynamic shard allocation for large test suites. It is used by Developer Experience engineers and SDETs during Stage 5 (Development) and Stage 7 (Testing) for test infrastructure optimization.

## Why Shard Tests

- Test suites exceeding 30 minutes cannot provide fast feedback to developers.
- Single-runner test execution is a bottleneck for CI throughput.
- Flaky tests compound across large suites, increasing false-negative rates.

## Sharding Strategies

| Strategy | Description                                                   | Balance       | Complexity |
| -------- | ------------------------------------------------------------- | ------------- | ---------- |
| Static   | Pre-define N shards with equal test count                     | Unbalanced    | Simple     |
| Dynamic  | Allocate tests to runners based on historical execution time  | Balanced      | Complex    |
| Hybrid   | Pre-define shards, rebalance based on timing data over 7 days | Near-balanced | Moderate   |

## Shard Allocation Algorithm

**Time-based allocation**:

1. Collect historical execution time for each test (last 30 runs).
2. Sort tests by average execution time (descending).
3. Assign each test to the shard with the lowest total time so far (greedy bin-packing).
4. Target: max shard time within 10% of average shard time.

## Flaky Test Detection and Auto-Quarantine

- Track pass/fail pattern: if test result differs between identical runs, flag as flaky.
- Flakiness score: `flaky_runs / total_runs` over rolling 30-day window.
- Auto-quarantine threshold: flakiness score >5% → move to quarantine suite.

**Quarantine handling**:

- Quarantined tests run in separate pipeline (non-blocking).
- Owner assignment: last committer to the test file or the code under test.
- SLA: quarantined test must be fixed or removed within 5 business days.

## Parallel Test Execution

**Isolation requirements**:

- Each shard runs in isolated environment (container or VM).
- Shared state (databases, caches) must be namespaced per shard.
- Test order randomization within each shard to detect inter-test dependencies.
