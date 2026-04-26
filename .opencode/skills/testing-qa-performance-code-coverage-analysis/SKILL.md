---
name: testing-qa-performance-code-coverage-analysis
description: Code coverage analysis for mobile projects — JaCoCo (Android), Xcode coverage (iOS), kover (KMP), coverage threshold enforcement, coverage trend tracking, and minimum coverage gate configuration for CI/CD pipelines. Owned by Ananya Krishnan (SDET). Use during Stage 5 (Development) for coverage instrumentation and Stage 7 (Testing) for coverage gate enforcement. Trigger: code coverage analysis, JaCoCo, Xcode coverage, kover, coverage thresholds, coverage trends, coverage gates, mobile test coverage.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
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

## 📊 Coverage Report

| Metric            | Before | After | Delta  |
| ----------------- | ------ | ----- | ------ |
| Line Coverage     | 85.2%  | 86.1% | +0.9pp |
| Branch Coverage   | 72.0%  | 73.5% | +1.5pp |
| Function Coverage | 88.0%  | 88.3% | +0.3pp |

### Changed Files Coverage

| File              | Coverage |
| ----------------- | -------- |
| HomeViewModel.kt  | 92% ✅   |
| AuthRepository.kt | 88% ✅   |
| PaymentUseCase.kt | 71% ⚠️   |

⚠️ PaymentUseCase.kt is below the 90% new code threshold.

````

### Coverage Trends in Stage 7 Report

The Stage 7 Test Results Report includes a coverage section:

```markdown

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`4.-ios-coverage-(xcode-+-xcov).md`](references/4.-ios-coverage-(xcode-+-xcov).md) — 4. iOS Coverage (Xcode + Xcov)
- [`5.-coverage-thresholds.md`](references/5.-coverage-thresholds.md) — 5. Coverage Thresholds
- [`6.-coverage-analysis.md`](references/6.-coverage-analysis.md) — 6. Coverage Analysis
- [`7.-coverage-trends.md`](references/7.-coverage-trends.md) — 7. Coverage Trends
- [`8.-coverage-quality.md`](references/8.-coverage-quality.md) — 8. Coverage Quality
- [`9.-reporting.md`](references/9.-reporting.md) — 9. Reporting
- [`coverage-summary.md`](references/coverage-summary.md) — Coverage Summary
- [`10.-stage-7-integration.md`](references/10.-stage-7-integration.md) — 10. Stage 7 Integration
- [`stage-7-coverage-sign-off.md`](references/stage-7-coverage-sign-off.md) — Stage 7 Coverage Sign-off
- [`appendix-a:-coverage-tool-quick-reference.md`](references/appendix-a:-coverage-tool-quick-reference.md) — Appendix A: Coverage Tool Quick Reference
- [`appendix-b:-coverage-exclusions-best-practices.md`](references/appendix-b:-coverage-exclusions-best-practices.md) — Appendix B: Coverage Exclusions Best Practices
- [`appendix-c:-coverage-anti-patterns.md`](references/appendix-c:-coverage-anti-patterns.md) — Appendix C: Coverage Anti-Patterns
````
