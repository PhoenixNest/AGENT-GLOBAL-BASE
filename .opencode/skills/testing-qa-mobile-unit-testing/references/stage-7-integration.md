# Stage 7 Integration

## Stage 7 Integration

### Stage 7 in the 10-Stage Pipeline

Stage 7 (Automated Testing) validates that the codebase meets quality standards through comprehensive automated testing.

**Input from Stage 6:**

- Code-signed codebase with all P0/P1 defects from code review remediated
- Defect Report with user decisions on P2/P3 defects
- Code Review Sign-off

**What Stage 7 Adds:**

- Comprehensive test suite (unit, integration, E2E)
- Code coverage measurement
- Performance benchmarking
- Accessibility audit
- Test Results Report

**Output to Stage 8:**

- Test Suite
- Test Results Report (pass/fail rates, coverage metrics, benchmarks)
- Updated Defect Report (new defects found during testing)

### Unit Testing's Role in Stage 7

| Activity                      | Responsibility | Tool                             |
| ----------------------------- | -------------- | -------------------------------- |
| Unit test suite execution     | Platform Leads | Gradle test / xcodebuild test    |
| Coverage report generation    | Platform Leads | JaCoCo / Slather                 |
| Coverage threshold validation | CTO            | CI pipeline gate                 |
| Integration test execution    | Test Lead      | Gradle connectedAndroidTest      |
| E2E smoke test execution      | Test Lead      | Maestro / Appium                 |
| Accessibility audit           | Test Lead      | Accessibility Scanner / XCUITest |
| Performance benchmarking      | Platform Leads | Macrobenchmark / XCTMeasure      |

### Unit Test Quality Gate

```
┌─────────────────────────────────────────────────────────────────┐
│ UNIT TEST QUALITY GATE (Stage 7)                                │
│                                                                 │
│ Criterion                    │ Target        │ Verification     │
│ ────────────────────────────│───────────────│────────────────── │
│ Unit test pass rate          │ 100%          │ CI test results  │
│ Branch coverage              │ >= 80%        │ JaCoCo / Slather │
│ Line coverage                │ >= 90%        │ JaCoCo / Slather │
│ No flaky tests               │ 0 confirmed   │ CI retry analysis│
│ Critical path coverage       │ 100%          │ Manual audit     │
│ Test execution time          │ < 5 minutes   │ CI timing        │
│ Test isolation               │ No order dep. │ Shuffle test run │
└─────────────────────────────────────────────────────────────────┘

If any criterion fails:
  1. Platform Lead investigates and fixes
  2. Re-run tests
  3. Re-gate only the failed criterion
```

---
