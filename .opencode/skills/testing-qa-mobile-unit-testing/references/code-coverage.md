# Code Coverage

## Code Coverage

### Android — JaCoCo

```kotlin
// app/build.gradle.kts
plugins {
    id("jacoco")
}

jacoco {
    toolVersion = "0.8.11"
}

tasks.register<JacocoReport>("jacocoTestReport") {
    dependsOn("testDebugUnitTest")

    reports {
        xml.required.set(true)
        html.required.set(true)
        csv.required.set(false)
    }

    val fileFilter = listOf(
        "**/R.class",
        "**/R$*.class",
        "**/BuildConfig.*",
        "**/Manifest*.*",
        "**/*Test*.*",
        "**/databinding/**",
        "**/hilt/**",
        "**/*_Factory.*",
        "**/*_MembersInjector.*"
    )

    val debugTree = fileTree("${buildDir}/tmp/kotlin-classes/debug") {
        exclude(fileFilter)
    }

    val mainSrc = fileTree("src/main/java") {
        exclude(fileFilter)
    }

    sourceDirectories.setFrom(files(mainSrc))
    classDirectories.setFrom(files(debugTree))
    executionData.setFrom(fileTree(buildDir) {
        include("outputs/unit_test_code_coverage/debugUnitTest/*.exec")
    })
}
```

**Coverage Threshold Enforcement:**

```kotlin
tasks.register<JacocoCoverageVerification>("jacocoTestCoverageVerification") {
    dependsOn("testDebugUnitTest")

    violationRules {
        rule {
            limit {
                minimum = "0.80".toBigDecimal() // 80% branch coverage
            }
        }
        limit {
            minimum = "0.90".toBigDecimal() // 90% line coverage
        }
    }
}
```

### iOS — Xcode Coverage

Xcode provides built-in coverage reporting:

```bash
# Run tests with coverage
xcodebuild test \
    -workspace App.xcworkspace \
    -scheme App \
    -destination 'platform=iOS Simulator,name=iPhone 15' \
    -enableCodeCoverage YES

# Generate coverage report with Slather
slather coverage \
    --input-format profdata \
    --cobertura-xml \
    --output-directory coverage \
    --scheme App \
    App.xcworkspace
```

**Coverage Threshold in CI:**

```bash
# Parse coverage and fail if below threshold
coverage=$(slather coverage --simple-output --scheme App App.xcworkspace)
percentage=$(echo "$coverage" | grep -o '[0-9.]*%' | head -1 | tr -d '%')
if (( $(echo "$percentage < 80" | bc -l) )); then
    echo "Coverage $percentage% is below 80% threshold"
    exit 1
fi
```

---
