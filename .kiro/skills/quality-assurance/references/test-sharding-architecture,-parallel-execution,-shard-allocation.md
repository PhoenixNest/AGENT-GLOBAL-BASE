---
name: test-sharding
description: Design and implement test sharding strategies across Android (Emulator API sharding), iOS (xctest-runner sharding), and backend (pytest-xdist) to reduce CI test execution time to under 15 minutes for the full test suite.
version: "1.0.0"
---

# Test Sharding

| Competency            | Description                                                  | Quality Criteria                                                                                                        |
| --------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Android Test Sharding | Distribute Android instrumented tests across emulator matrix | Tests sharded by module; emulator matrix covers min SDK + target SDK; no single shard exceeds 8 minutes wall-clock time |
| iOS Test Sharding     | Distribute XCTest suite across parallel simulators           | Tests divided into balanced shards; parallel simulator execution configured in Xcode CI scheme; flaky tests quarantined |
| Backend Test Sharding | Configure pytest-xdist for parallel backend test execution   | `pytest-n auto` configured with proper resource isolation; database fixtures use per-worker schemas; no race conditions |
| Flaky Test Management | Detect, quarantine, and remediate flaky tests                | Flaky tests quarantined within 24 hours of detection; root cause identified within 1 sprint; quarantine time ≤ 2 weeks  |

## Execution Guidance

### Android Emulator Sharding (GitHub Actions)

```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - name: Run Android tests (shard ${{ matrix.shard }} of 4)
    run: |
      ./gradlew connectedAndroidTest \
        -PtestShard=${{ matrix.shard }} \
        -PtotalShards=4
```

Module-level sharding strategy: assign each Gradle module to a shard based on historical execution time (use Gradle Enterprise build scan data).

### Flaky Test Quarantine Process

1. Test fails non-deterministically in ≥ 2 CI runs within one week → flagged as flaky.
2. Add `@Flaky` annotation and move to `flaky-quarantine` CI job (runs but doesn't block).
3. Assign owner to investigate root cause within the current sprint.
4. Fix or permanently skip (with documented justification) within 2 weeks — no silent disabling.
