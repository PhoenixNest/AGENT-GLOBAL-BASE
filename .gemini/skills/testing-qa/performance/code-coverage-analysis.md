---
name: code-coverage-analysis
description: Code coverage analysis for mobile applications, covering JaCoCo (Android) and Xcode Coverage (iOS) configuration, threshold enforcement, coverage reporting, CI/CD pipeline gate integration, and distinguishing coverage from test quality.
---

# Code Coverage Analysis

## 1. Overview

### Purpose

Code coverage analysis measures the extent to which the source code of a mobile application is executed during automated test runs. It provides quantitative insight into test suite effectiveness, identifies untested code paths, and serves as a **Stage 7 gate criterion** in the development pipeline.

Coverage is **not** a proxy for test quality — high coverage with weak assertions provides false confidence. However, **low coverage is a reliable indicator of risk**. This skill defines how to configure, collect, analyze, and enforce coverage thresholds for Android and iOS platforms.

### Scope

| Dimension    | Coverage                                                                        |
| ------------ | ------------------------------------------------------------------------------- |
| Platforms    | Android (JUnit 5 + Robolectric + Compose), iOS (XCTest + Quick/Nimble)          |
| Test Levels  | Unit tests (primary), Integration tests (secondary)                             |
| Metric Types | Line, branch, function, statement, path coverage                                |
| Enforcement  | CI/CD pipeline gates, PR merge blocking, Stage 7 gate criteria                  |
| Reporting    | JaCoCo HTML/XML reports, Xcov summaries, trend dashboards, PR coverage comments |

### Coverage in the Pipeline

| Stage | Coverage Activity                                                               |
| ----- | ------------------------------------------------------------------------------- |
| 5     | Unit test infrastructure setup — coverage tooling configured per platform       |
| 6     | Code review — coverage trends reviewed alongside defect reports                 |
| 7     | **Gate criterion** — coverage thresholds enforced; failures block stage advance |
| 8     | Integrity verification — coverage completeness validated against UML diagrams   |
| 10    | Release readiness — coverage trends included in readiness report                |

### Relationship to Mobile Unit Testing

This skill operates in conjunction with `mobile-unit-testing.md`. Unit test patterns (coroutine testing, flow testing, reactive state testing) defined in that skill are the **source** of coverage data. Coverage analysis measures the **effectiveness** of those tests.

---

## 2. Coverage Metrics

### Metric Definitions

| Metric                 | Definition                                                                | Example                                                              |
| ---------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Line Coverage**      | Percentage of executable source lines executed at least once during tests | 850 of 1000 lines executed = 85% line coverage                       |
| **Branch Coverage**    | Percentage of control flow branches (if/else, when, switch) taken         | 6 of 8 branches taken = 75% branch coverage                          |
| **Function Coverage**  | Percentage of functions/methods invoked during tests                      | 120 of 150 functions called = 80% function coverage                  |
| **Statement Coverage** | Percentage of individual statements executed                              | Similar to line coverage but counts multi-statement lines separately |
| **Path Coverage**      | Percentage of unique execution paths through the code                     | Most comprehensive but often infeasible for complex code             |

### Metric Limitations

| Metric             | Limitation                                                                                   | Mitigation                                                            |
| ------------------ | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Line Coverage      | Does not verify assertions — a line can be executed with no meaningful test validation       | Combine with mutation testing; review test assertion quality          |
| Branch Coverage    | Does not cover all path combinations — nested conditionals create exponential paths          | Focus on critical paths; use property-based testing for complex logic |
| Function Coverage  | Does not verify all code within a function — entry execution counts as covered               | Use in combination with line/branch coverage                          |
| Statement Coverage | Can be misleading with multi-statement lines — one line may contain multiple logical actions | Prefer line coverage over statement coverage for readability          |
| Path Coverage      | Computationally infeasible for most real-world codebases                                     | Apply selectively to safety-critical modules only                     |

### Recommended Metric Priority

1. **Branch coverage** — primary metric for gating (most meaningful for correctness)
2. **Line coverage** — secondary metric for trending (easiest to interpret)
3. **Function coverage** — tertiary metric for completeness checks
4. **Path coverage** — applied only to safety-critical modules (authentication, payments)

---

## 3. Android Coverage (JaCoCo)

### JaCoCo Configuration

**Root `build.gradle.kts`** — Apply JaCoCo plugin:

```kotlin
plugins {
    id("jacoco")
}

jacoco {
    toolVersion = "0.8.11"
}
```

**App `build.gradle.kts`** — Enable coverage in test options:

```kotlin
android {
    buildTypes {
        debug {
            isTestCoverageEnabled = true
        }
    }

    testOptions {
        unitTests {
            isIncludeAndroidResources = true  // Required for Robolectric
            isReturnDefaultValues = false     // Fail fast on unmocked calls
        }
    }
}
```

**JaCoCo Report Task** — Generate combined coverage reports:

```kotlin
tasks.register<JacocoReport>("jacocoTestReport") {
    dependsOn("testDebugUnitTest")

    reports {
        xml.required.set(true)   // For CI consumption
        html.required.set(true)  // For human review
        csv.required.set(false)
    }

    val fileFilter = listOf(
        "**/R.class",
        "**/R\$*.class",
        "**/BuildConfig.*",
        "**/Manifest*.*",
        "**/*Test*.*",
        "**/*\$Lambda$*.*",
        "**/*\$Companion$*.*",
        "**/di/**"
    )

    val kotlinTree = fileTree("${project.buildDir}/tmp/kotlin-classes/debug") {
        exclude(fileFilter)
    }
    val javaTree = fileTree("${project.buildDir}/intermediates/javac/debug") {
        exclude(fileFilter)
    }
    val mainSrc = fileTree("${project.projectDir}/src/main/java") {
        exclude(fileFilter)
    }

    sourceDirectories.setFrom(files(mainSrc))
    classDirectories.setFrom(files(kotlinTree, javaTree))
    executionData.setFrom(
        fileTree(project.buildDir) {
            include(
                "outputs/unit_test_code_coverage/debugUnitTest/testDebugUnitTest.exec",
                "outputs/code_coverage/debugAndroidTest/connected/*coverage.ec"
            )
        }
    )
}
```

### Robolectric Coverage

Robolectric runs unit tests on the JVM with shadow implementations of Android framework classes. Coverage data is collected identically to standard JUnit tests — no special configuration is required beyond `isIncludeAndroidResources = true`.

```kotlin
// Coverage for ViewModel with Android dependencies
@RunWith(RobolectricTest::class)
class HomeViewModelTest {

    @Test
    fun `given network success, when load called, then state is loaded`() = runTest {
        val dispatcher = StandardTestDispatcher(testScheduler)
        val viewModel = HomeViewModel(fakeRepository, dispatcher)

        viewModel.load()
        advanceUntilIdle()

        assertThat(viewModel.uiState.value).isInstanceOf(HomeUiState.Loaded::class.java)
    }
}
```

### Compose Coverage

Jetpack Compose UI code requires special handling for coverage because Compose generates synthetic methods and lambdas. The JaCoCo configuration above excludes `**/*\$Lambda$*.*` by default, but Compose coverage can be improved by:

1. **Including Compose-generated classes** — remove `**/*\$Lambda$*.*` from exclusion filter
2. **Using Compose Test Rule** — ensure UI tests drive actual composition:

```kotlin
@get:Rule
val composeTestRule = createComposeRule()

@Test
fun `given user profile, when rendered, then displays name and avatar`() {
    composeTestRule.setContent {
        UserProfileScreen(
            user = TestUserFactory.create(),
            onNavigate = { }
        )
    }

    composeTestRule.onNodeWithText("John Doe").assertIsDisplayed()
}
```

### Coverage Reports

JaCoCo generates two report formats:

| Format | Location                                                         | Purpose                                                          |
| ------ | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| HTML   | `app/build/reports/jacoco/jacocoTestReport/html/index.html`      | Interactive human-readable report with source-level highlighting |
| XML    | `app/build/reports/jacoco/jacocoTestReport/jacocoTestReport.xml` | Machine-parseable for CI integration and threshold enforcement   |

**HTML Report Structure:**

- Package-level coverage summary (line, branch, function percentages)
- Drill-down to class-level coverage
- Source-level highlighting (green = covered, red = uncovered, yellow = partial branch coverage)

---

## 4. iOS Coverage (Xcode + Xcov)

### Xcode Coverage Configuration

**Xcode Build Settings** — Enable code coverage:

```
GCC_INSTRUMENT_PROGRAM_FLOW_ARCS = YES    // Enable gcov instrumentation
CLANG_ENABLE_CODE_COVERAGE = YES          // Enable clang coverage
```

**For Xcode 14+ with Swift Testing:**

```
CODE_COVERAGE_ENABLED = YES
```

### Xcov Integration

Xcov is a Ruby gem that parses Xcode coverage data and generates human-readable reports. Install and configure:

```ruby
# Gemfile
gem "xcov"
```

```ruby
# Fastlane Fastfile
lane :coverage do
  xcov(
    workspace: "MyApp.xcworkspace",
    scheme: "MyAppTests",
    output_directory: "fastlane/test_output/coverage",
    html_report: true,
    json_report: true,
    minimum_coverage_percentage: 80.0,
    ignore_file_path: "fastlane/.xcovignore"
  )
end
```

### Coverage Merge

For multi-module iOS projects, coverage data must be merged across test targets:

```bash
# Merge coverage data from multiple test runs
xcrun llvm-profdata merge -output merged.profdata *.profraw

# Generate report from merged data
xcrun llvm-cov show \
  -instr-profile=merged.profdata \
  -format=html \
  -output-dir=coverage-report \
  MyApp.app/MyApp
```

### Xcov Ignore File

Use `.xcovignore` to exclude generated code, test helpers, and third-party code:

```
# Generated code
*Generated.swift
*Mocks.swift

# Test utilities
*TestHelper*
*TestFactory*

# Third-party (if not using SPM)
*Pods/*
*Carthage/*

# AppDelegate extension for testing
*+Testing.swift
```

### Coverage Reports

Xcov generates:

| Format   | Location                                  | Purpose                                               |
| -------- | ----------------------------------------- | ----------------------------------------------------- |
| HTML     | `fastlane/test_output/coverage/xcov.html` | Interactive report with file-level coverage breakdown |
| JSON     | `fastlane/test_output/coverage/xcov.json` | Machine-parseable for CI integration                  |
| Markdown | `fastlane/test_output/coverage/xcov.md`   | Summary for PR comments and Slack notifications       |

**Markdown Report Example:**

```
| File                          | Coverage | Lines Covered |
|-------------------------------|----------|---------------|
| HomeViewModel.swift           | 94.2%    | 131/139       |
| NetworkClient.swift           | 87.5%    | 70/80         |
| UserRepository.swift          | 91.0%    | 101/111       |
| **Total**                     | **89.1%**| **302/330**   |
```

---

## 5. Coverage Thresholds

### Team Targets

Per the VP Quality audit, coverage thresholds are a **Stage 7 gate criterion**. The following targets apply:

| Metric            | Android Target | iOS Target | Rationale                                     |
| ----------------- | -------------- | ---------- | --------------------------------------------- |
| Line Coverage     | ≥ 80%          | ≥ 80%      | Baseline for meaningful test suite            |
| Branch Coverage   | ≥ 70%          | ≥ 70%      | Ensures conditional logic is tested           |
| Function Coverage | ≥ 85%          | ≥ 85%      | Ensures all public APIs are exercised         |
| New Code Coverage | ≥ 90%          | ≥ 90%      | Higher bar for new code to prevent regression |

### Module-Level Thresholds

Different modules have different risk profiles and coverage requirements:

| Module Category    | Examples                            | Line Coverage | Branch Coverage | Rationale                                           |
| ------------------ | ----------------------------------- | ------------- | --------------- | --------------------------------------------------- |
| **Critical**       | Authentication, Payments, Security  | ≥ 95%         | ≥ 90%           | High-risk code demands near-complete testing        |
| **Core**           | ViewModels, Repositories, Use Cases | ≥ 85%         | ≥ 75%           | Business logic must be well-covered                 |
| **UI**             | Composables, ViewControllers        | ≥ 70%         | ≥ 60%           | UI code changes frequently; focus on critical paths |
| **Infrastructure** | DI setup, Network config, Logging   | ≥ 60%         | ≥ 50%           | Lower risk; focus on integration testing            |

### CI/CD Coverage Gates

**GitHub Actions (Android):**

```yaml
- name: Run JaCoCo Coverage
  run: ./gradlew jacocoTestReport

- name: Enforce Coverage Thresholds
  uses: madrapps/jacoco-report@v1.6.1
  with:
    paths: ${{ github.workspace }}/app/build/reports/jacoco/jacocoTestReport/jacocoTestReport.xml
    token: ${{ secrets.GITHUB_TOKEN }}
    min-coverage-overall: 80
    min-coverage-changed-files: 90
    title: 'Android Coverage Report'
```

**GitHub Actions (iOS):**

```yaml
- name: Run Tests with Coverage
  run: |
    xcodebuild test \
      -workspace MyApp.xcworkspace \
      -scheme MyAppTests \
      -destination 'platform=iOS Simulator,name=iPhone 15' \
      -enableCodeCoverage YES

- name: Generate Coverage Report
  run: bundle exec fastlane coverage

- name: Enforce Coverage Threshold
  run: |
    COVERAGE=$(cat fastlane/test_output/coverage/xcov.json | jq '.coverage')
    if (( $(echo "$COVERAGE < 80.0" | bc -l) )); then
      echo "Coverage $COVERAGE% below threshold 80%"
      exit 1
    fi
```

**PR Gate Enforcement:**

Coverage gates block PR merges when thresholds are not met. The gate check runs as a required status check:

| Check                      | Threshold | Blocking |
| -------------------------- | --------- | -------- |
| Overall line coverage      | ≥ 80%     | Yes      |
| Overall branch coverage    | ≥ 70%     | Yes      |
| New/changed code coverage  | ≥ 90%     | Yes      |
| Module-specific thresholds | Per table | Yes      |

---

## 6. Coverage Analysis

### Uncovered Code Identification

**Step 1: Generate coverage report** — Run the full unit test suite with coverage enabled.

**Step 2: Identify uncovered files** — Filter the report for files below module thresholds:

```bash
# Android — parse JaCoCo XML for files below threshold
xmllint --xpath '//package/class[(@linecoverage < 0.80)]' jacocoTestReport.xml

# iOS — parse Xcov JSON for files below threshold
jq '.files[] | select(.coverage < 80)' xcov.json
```

**Step 3: Categorize uncovered code** — Not all uncovered code requires tests:

| Category             | Action                                  | Example                                  |
| -------------------- | --------------------------------------- | ---------------------------------------- |
| Dead code            | Remove — code is no longer reachable    | Legacy feature flags, deprecated methods |
| Generated code       | Exclude — auto-generated, no test value | Data class copy methods, enum ordinal    |
| Error handling paths | Test — simulate failure conditions      | Network timeout, database corruption     |
| Edge cases           | Test — boundary conditions              | Empty lists, null inputs, max values     |
| Platform-specific    | Test on appropriate platform only       | Android intents, iOS deeplinks           |

### Critical Path Coverage

Critical paths are execution flows that must be covered for core functionality to work correctly. Identify critical paths from:

1. **UML sequence diagrams** (Stage 3 artifacts) — each interaction represents a test scenario
2. **User journey maps** — primary user flows (login, checkout, content consumption)
3. **Risk assessments** (SRD, Stage 1) — security-sensitive flows

**Critical Path Coverage Matrix:**

| Critical Path         | UML Reference | Test Class         | Branch Coverage | Status |
| --------------------- | ------------- | ------------------ | --------------- | ------ |
| User authentication   | SEQ-001       | AuthViewModelTest  | 94%             | ✅     |
| Payment processing    | SEQ-004       | PaymentUseCaseTest | 91%             | ✅     |
| Content sync          | SEQ-007       | SyncRepositoryTest | 78%             | ⚠️     |
| Offline mode fallback | SEQ-009       | OfflineCacheTest   | 65%             | ❌     |

### Risk-Based Prioritization

When coverage gaps exist, prioritize test authoring by risk:

| Priority | Criteria                                              | Action                                      |
| -------- | ----------------------------------------------------- | ------------------------------------------- |
| P0       | Uncovered critical path + production incident history | Write tests immediately, block release      |
| P1       | Uncovered critical path + no incident history         | Write tests within current sprint           |
| P2       | Uncovered non-critical path + complex logic           | Schedule test authoring                     |
| P3       | Uncovered non-critical path + simple logic            | Consider removal or exclusion from coverage |

---

## 7. Coverage Trends

### Historical Tracking

Coverage should be tracked over time to identify trends and regressions. Store coverage data per build:

```json
{
  "build_number": 1247,
  "timestamp": "2026-04-05T14:30:00Z",
  "platform": "android",
  "module": "app",
  "line_coverage": 87.3,
  "branch_coverage": 73.1,
  "function_coverage": 89.5,
  "new_code_line_coverage": 92.0,
  "new_code_branch_coverage": 81.0
}
```

Store these records in a time-series database or simple JSON log for trend analysis.

### Coverage Regression Detection

**Automated Regression Check:**

```python
# coverage_regression_check.py
import json
import sys

def check_regression(current: dict, baseline: dict, threshold: float = 2.0) -> list:
    """Detect coverage regressions exceeding threshold percentage points."""
    regressions = []
    for metric in ["line_coverage", "branch_coverage", "function_coverage"]:
        delta = current[metric] - baseline[metric]
        if delta < -threshold:
            regressions.append({
                "metric": metric,
                "baseline": baseline[metric],
                "current": current[metric],
                "delta": round(delta, 2)
            })
    return regressions

# Load data
current = json.load(open("coverage-current.json"))
baseline = json.load(open("coverage-baseline.json"))

regressions = check_regression(current, baseline)
if regressions:
    print("COVERAGE REGRESSION DETECTED:")
    for r in regressions:
        print(f"  {r['metric']}: {r['baseline']}% → {r['current']}% (Δ{r['delta']}pp)")
    sys.exit(1)
else:
    print("No coverage regression detected.")
    sys.exit(0)
```

**Regression Threshold:** A drop of **>2 percentage points** in any coverage metric triggers a regression alert. This is configurable per module.

### Coverage Improvement Strategies

| Strategy                      | Description                                                                  | Impact                                  |
| ----------------------------- | ---------------------------------------------------------------------------- | --------------------------------------- |
| **Test-first mandate**        | Require tests before implementation (TDD)                                    | Prevents coverage debt accumulation     |
| **Coverage gate on new code** | Enforce ≥90% coverage on changed files only                                  | Ensures new code is well-tested         |
| **Weekly coverage review**    | Review coverage trends in team retro                                         | Identifies regressions early            |
| **Coverage champions**        | Assign coverage ownership per module                                         | Accountability for coverage maintenance |
| **Automated test generation** | Use tools like Diffblue Cover (Android) to generate tests for uncovered code | Accelerates coverage improvement        |

**Coverage Debt Backlog:** Track uncovered code as technical debt items:

| Module        | Current Coverage | Target | Gap  | Effort Estimate | Priority |
| ------------- | ---------------- | ------ | ---- | --------------- | -------- |
| AuthModule    | 72%              | 95%    | 23pp | 3 story points  | P0       |
| PaymentModule | 81%              | 95%    | 14pp | 5 story points  | P0       |
| UIModule      | 64%              | 70%    | 6pp  | 2 story points  | P2       |
| NetworkModule | 76%              | 85%    | 9pp  | 3 story points  | P1       |

---

## 8. Coverage Quality

### Line Coverage vs. Meaningful Coverage

High line coverage does not guarantee test quality. A test that invokes a method without assertions contributes to coverage but provides no verification value.

**Indicators of Meaningful Coverage:**

| Indicator                      | Good Sign                              | Bad Sign                           |
| ------------------------------ | -------------------------------------- | ---------------------------------- |
| Assertions per test            | ≥ 2 assertions per test method         | 0–1 assertions per test method     |
| Test method size               | 10–20 lines (focused)                  | 50+ lines (testing too much)       |
| Test naming                    | Describes behavior (`given/when/then`) | Generic (`testMethod1`, `test2`)   |
| Mock usage                     | Minimal, only for external deps        | Excessive, mocking own code        |
| Coverage delta vs. defect rate | High coverage → low defect escape      | High coverage → high defect escape |

**Mutation Testing for Coverage Quality:**

Mutation testing introduces small faults (mutations) into the code and verifies that tests detect them. A high mutation score indicates meaningful coverage.

| Tool        | Platform | Description                            |
| ----------- | -------- | -------------------------------------- |
| Pitest      | Android  | Java/Kotlin mutation testing framework |
| SwiftMutant | iOS      | Swift mutation testing (experimental)  |

**Pitest Configuration (Android):**

```kotlin
plugins {
    id("info.solidsoft.pitest") version "1.15.0"
}

pitest {
    targetClasses.set(listOf("com.example.*"))
    outputFormats.set(listOf("HTML", "XML"))
    mutationThreshold.set(80)     // Minimum mutation score percentage
    coverageThreshold.set(80)     // Minimum line coverage percentage
    threads.set(4)
}
```

**Mutation Score Interpretation:**

| Score  | Interpretation                                                | Action                                      |
| ------ | ------------------------------------------------------------- | ------------------------------------------- |
| ≥ 80%  | Strong test suite — tests detect most mutations               | Maintain current practices                  |
| 60–79% | Moderate — some mutations survive                             | Review surviving mutations, add assertions  |
| < 60%  | Weak — many mutations survive, tests provide false confidence | Significant test quality improvement needed |

### Test Effectiveness Metrics

Beyond coverage, measure test effectiveness:

| Metric                  | Definition                                         | Target       |
| ----------------------- | -------------------------------------------------- | ------------ |
| **Defect escape rate**  | Defects found in production vs. pre-release        | < 5%         |
| **Test flake rate**     | Percentage of tests with non-deterministic results | < 1%         |
| **Mean time to detect** | Time from defect introduction to detection         | < 24 hours   |
| **Test execution time** | Total time for full test suite                     | < 10 minutes |
| **Assertion density**   | Assertions per line of production code             | ≥ 1.5        |

---

## 9. Reporting

### Coverage Dashboards

Coverage dashboards provide at-a-glance visibility into coverage health across teams, modules, and sprints.

**Dashboard Components:**

| Widget                 | Data Source             | Refresh    | Audience          |
| ---------------------- | ----------------------- | ---------- | ----------------- |
| Overall coverage trend | JaCoCo/Xcov historical  | Per build  | Engineering leads |
| Coverage by module     | JaCoCo/Xcov per-module  | Per build  | Module owners     |
| Coverage by team       | Module-to-team mapping  | Per sprint | VP Quality        |
| Regression alerts      | Regression check script | Real-time  | All developers    |
| Coverage debt backlog  | Manual tracking         | Per sprint | Product owners    |

**Example Dashboard (Grafana/Prometheus):**

```
┌─────────────────────────────────────────────────────────────┐
│                    COVERAGE DASHBOARD                       │
├─────────────────────────────────────────────────────────────┤
│  Overall: ████████████████████░░░░  82.3%  (▲ 1.2pp)       │
│  Branch:  ████████████████░░░░░░░░  71.1%  (▲ 0.8pp)       │
│  New Code:██████████████████████░░  91.5%  (▼ 0.3pp) ⚠️     │
├─────────────────────────────────────────────────────────────┤
│  MODULE BREAKDOWN                                           │
│  AuthModule      ████████████████████████████  94%  ✅       │
│  PaymentModule   ████████████████████████░░░░  81%  ⚠️       │
│  UIModule        ████████████████░░░░░░░░░░░░  64%  ❌       │
│  NetworkModule   ██████████████████████░░░░░░  76%  ⚠️       │
├─────────────────────────────────────────────────────────────┤
│  TREND (Last 10 builds)                                     │
│  80% ┤    ╭──╮                                              │
│  78% ┤  ╭╯    ╰──╮  ╭──╮                                   │
│  76% ┤╭╯          ╰──╯  ╰──╮  ╭──╮                          │
│  74% ┤                      ╰──╯  ╰────                     │
│      └───────────────────────────────                        │
│       B1020 B1030 B1040 B1050 B1060 B1070                   │
└─────────────────────────────────────────────────────────────┘
```

### Coverage Badges

Add coverage badges to README files for public visibility:

```markdown
![Android Coverage](https://img.shields.io/badge/coverage-87%25-brightgreen)
![iOS Coverage](https://img.shields.io/badge/coverage-82%25-yellow)
![Branch Coverage](https://img.shields.io/badge/branch-73%25-orange)
```

### PR Coverage Comments

Configure CI to comment on PRs with coverage impact:

```
## 📊 Coverage Report

| Metric             | Before  | After   | Delta  |
|--------------------|---------|---------|--------|
| Line Coverage      | 85.2%   | 86.1%   | +0.9pp |
| Branch Coverage    | 72.0%   | 73.5%   | +1.5pp |
| Function Coverage  | 88.0%   | 88.3%   | +0.3pp |

### Changed Files Coverage

| File                  | Coverage |
|-----------------------|----------|
| HomeViewModel.kt      | 92% ✅   |
| AuthRepository.kt     | 88% ✅   |
| PaymentUseCase.kt     | 71% ⚠️   |

⚠️ PaymentUseCase.kt is below the 90% new code threshold.
```

### Coverage Trends in Stage 7 Report

The Stage 7 Test Results Report includes a coverage section:

```markdown
## Coverage Summary

| Platform | Line Coverage | Branch Coverage | Function Coverage | New Code Coverage |
| -------- | ------------- | --------------- | ----------------- | ----------------- |
| Android  | 87.3%         | 73.1%           | 89.5%             | 92.0%             |
| iOS      | 84.1%         | 71.8%           | 86.2%             | 88.5%             |

### Coverage Gate Status

| Criterion                | Threshold | Android | iOS   | Status     |
| ------------------------ | --------- | ------- | ----- | ---------- |
| Overall line coverage    | ≥ 80%     | 87.3%   | 84.1% | ✅ PASS    |
| Overall branch coverage  | ≥ 70%     | 73.1%   | 71.8% | ✅ PASS    |
| New code coverage        | ≥ 90%     | 92.0%   | 88.5% | ⚠️ iOS     |
| Critical module coverage | ≥ 95%     | 94.2%   | 95.1% | ⚠️ Android |

### Regression Analysis

No coverage regressions detected (>2pp drop) in this build.
```

---

## 10. Stage 7 Integration

### Role in the Pipeline

Stage 7 (Automated Testing) is where coverage analysis is executed and enforced as a **gate criterion**. The Test Lead coordinates with SDET Mobile (Ananya Krishnan) to ensure coverage thresholds are met before advancing to Stage 8.

### Stage 7 Coverage Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    STAGE 7 COVERAGE FLOW                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Test Suite Execution                                    │
│     └─ Run all unit tests with coverage enabled             │
│        ├─ Android: ./gradlew jacocoTestReport               │
│        └─ iOS: xcodebuild test -enableCodeCoverage YES      │
│                                                             │
│  2. Coverage Report Generation                              │
│     └─ Generate JaCoCo (Android) and Xcov (iOS) reports     │
│        ├─ HTML reports for human review                     │
│        └─ XML/JSON reports for CI processing                │
│                                                             │
│  3. Threshold Enforcement                                   │
│     └─ Compare coverage against thresholds                  │
│        ├─ Overall thresholds (line ≥ 80%, branch ≥ 70%)     │
│        ├─ Module thresholds (per risk category)             │
│        └─ New code thresholds (≥ 90%)                       │
│                                                             │
│  4. Regression Check                                        │
│     └─ Compare against previous build coverage              │
│        └─ Alert if any metric drops > 2pp                   │
│                                                             │
│  5. Stage 7 Report Compilation                              │
│     └─ Compile TEST-RESULTS-REPORT.md with coverage section  │
│        ├─ Coverage summary table                            │
│        ├─ Coverage gate status                              │
│        └─ Regression analysis                               │
│                                                             │
│  6. Gate Review                                             │
│     └─ Coverage gate results presented to user              │
│        ├─ If all thresholds met → advance to Stage 8        │
│        └─ If any threshold failed → remediate and re-run    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Coverage Gate Criteria

| Criterion                       | Threshold  | Failure Action                           |
| ------------------------------- | ---------- | ---------------------------------------- |
| Overall line coverage (Android) | ≥ 80%      | Identify gaps, write tests, re-run       |
| Overall line coverage (iOS)     | ≥ 80%      | Identify gaps, write tests, re-run       |
| Overall branch coverage         | ≥ 70%      | Add branch tests, re-run                 |
| New code line coverage          | ≥ 90%      | Author tests for changed files, re-run   |
| Critical module coverage        | ≥ 95%      | Prioritize critical path tests, re-run   |
| Coverage regression             | < 2pp drop | Investigate root cause, restore coverage |

### Gate Failure Remediation

When coverage gates fail, follow this remediation process:

| Step | Action                                         | Owner         | Timeline |
| ---- | ---------------------------------------------- | ------------- | -------- |
| 1    | Identify uncovered files below threshold       | SDET Mobile   | Same day |
| 2    | Categorize gaps (dead code vs. missing tests)  | SDET Mobile   | Same day |
| 3    | Remove dead code or update coverage exclusions | Platform Lead | 1 day    |
| 4    | Author tests for missing coverage              | Platform Lead | 1–3 days |
| 5    | Re-run test suite with coverage                | SDET Mobile   | Same day |
| 6    | Verify thresholds met                          | SDET Mobile   | Same day |
| 7    | Update Stage 7 report                          | Test Lead     | Same day |

### Coverage Sign-off

Coverage sign-off is part of the Stage 7 gate approval:

```markdown
## Stage 7 Coverage Sign-off

| Signatory          | Role        | Signature | Date       |
| ------------------ | ----------- | --------- | ---------- |
| Ananya Krishnan    | SDET Mobile | ✅        | 2026-04-05 |
| Priscilla Oduya    | Test Lead   | ✅        | 2026-04-05 |
| Dr. Kenji Nakamura | CTO         | ✅        | 2026-04-06 |

**Coverage Gate Status: PASS**

- Android line coverage: 87.3% (threshold: 80%) ✅
- iOS line coverage: 84.1% (threshold: 80%) ✅
- Branch coverage: 72.5% average (threshold: 70%) ✅
- New code coverage: 90.3% average (threshold: 90%) ✅
- No coverage regressions detected ✅
```

### Escalation Protocol

If coverage gates cannot be met within the sprint timeline:

| Escalation Level | Condition                        | Action                                      |
| ---------------- | -------------------------------- | ------------------------------------------- |
| Level 1          | Single module below threshold    | Module owner assigns coverage sprint task   |
| Level 2          | Multiple modules below threshold | Test Lead coordinates cross-team effort     |
| Level 3          | Critical module below threshold  | CTO notified, Stage 7 blocked until fixed   |
| Level 4          | Coverage regression > 5pp        | Immediate investigation, potential rollback |

**Note:** Coverage gates are **non-negotiable** for Stage 7 advancement. The "trim-to-pass" anti-pattern (removing functionality to improve coverage ratios) is explicitly prohibited per pipeline rules.

---

## Appendix A: Coverage Tool Quick Reference

| Task                            | Android Command                                 | iOS Command                                    |
| ------------------------------- | ----------------------------------------------- | ---------------------------------------------- |
| Run tests with coverage         | `./gradlew testDebugUnitTest jacocoTestReport`  | `xcodebuild test -enableCodeCoverage YES`      |
| Generate coverage report        | `./gradlew jacocoTestReport`                    | `bundle exec fastlane coverage`                |
| View HTML report                | Open `build/reports/jacoco/.../html/index.html` | Open `fastlane/test_output/coverage/xcov.html` |
| Parse for CI                    | Parse `jacocoTestReport.xml`                    | Parse `xcov.json`                              |
| Merge multi-module coverage     | `./gradlew jacocoMergeReports` (custom task)    | `xcrun llvm-profdata merge`                    |
| Check coverage programmatically | Parse XML with XPath or JaCoCo CLI              | Parse JSON with jq                             |

## Appendix B: Coverage Exclusions Best Practices

Exclude code that cannot or should not be tested:

| Exclusion Category    | Pattern                              | Rationale                                   |
| --------------------- | ------------------------------------ | ------------------------------------------- |
| Generated code        | `*Generated.swift`, `*$$Result.java` | Auto-generated, changes with each build     |
| Data classes / models | `data class User(...)`               | Compiler-generated methods are not testable |
| DI setup              | `*Module.kt`, `*Component.java`      | Framework wiring, tested via integration    |
| BuildConfig           | `BuildConfig.*`                      | Auto-generated build metadata               |
| R class / resources   | `R.class`, `R$*.class`               | Android resource identifiers                |
| Test utilities        | `*TestHelper*`, `*TestFactory*`      | Test code should not count toward coverage  |
| Main entry points     | `MainActivity`, `AppDelegate`        | Tested via E2E, not unit tests              |

**Important:** Exclusions must be reviewed and approved by the Test Lead. Do not exclude production code to artificially inflate coverage numbers — this is a pipeline violation.

## Appendix C: Coverage Anti-Patterns

| Anti-Pattern             | Description                                    | Why It's Bad                                | Prevention                           |
| ------------------------ | ---------------------------------------------- | ------------------------------------------- | ------------------------------------ |
| **Coverage chasing**     | Writing tests solely to hit coverage targets   | Tests may lack meaningful assertions        | Mutation testing, code review        |
| **Trim-to-pass**         | Removing uncovered code to improve ratios      | Functionality loss disguised as improvement | Pipeline rule: explicitly prohibited |
| **Exclusion abuse**      | Excluding production code from coverage        | Artificially inflates coverage numbers      | Test Lead approval required          |
| **Test interdependence** | Tests that depend on execution order           | Flake-prone, unreliable coverage data       | AAA pattern, isolated tests          |
| **Over-mocking**         | Mocking all dependencies, testing nothing real | High coverage, low confidence               | Use fakes for complex dependencies   |
| **Coverage silos**       | Teams only covering their own modules          | Integration gaps between modules            | Cross-module coverage targets        |
