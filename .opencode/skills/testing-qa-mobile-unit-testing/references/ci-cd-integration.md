# CI/CD Integration

## CI/CD Integration

### Unit Test Pipeline

```
Developer pushes code
    │
    ▼
┌──────────────────────────────────────┐
│ PRE-COMMIT HOOK                      │
│ ├── ktlint / SwiftLint               │
│ └── Quick unit test suite (< 30s)    │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│ PULL REQUEST CI                      │
│ ├── Full unit test suite             │
│ ├── JaCoCo / Xcode coverage report   │
│ ├── Lint + static analysis           │
│ └── Coverage threshold check         │
│                                      │
│ If any step fails → PR blocked       │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│ MERGE TO MAIN                        │
│ ├── Full test suite (re-run)         │
│ ├── Coverage trend analysis          │
│ └── Coverage badge update            │
└──────────────────────────────────────┘
```

### GitHub Actions — Android Unit Tests

```yaml
name: Android Unit Tests

on: [pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          distribution: "temurin"
          java-version: "21"

      - name: Grant execute permission
        run: chmod +x gradlew

      - name: Run unit tests
        run: ./gradlew testDebugUnitTest

      - name: Generate JaCoCo report
        run: ./gradlew jacocoTestReport

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: "**/build/reports/jacoco/"

      - name: Check coverage threshold
        run: ./gradlew jacocoTestCoverageVerification
```

### GitHub Actions — iOS Unit Tests

```yaml
name: iOS Unit Tests

on: [pull_request]

jobs:
  unit-tests:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4

      - name: Run unit tests with coverage
        run: |
          xcodebuild test \
            -workspace App.xcworkspace \
            -scheme App \
            -destination 'platform=iOS Simulator,name=iPhone 15' \
            -enableCodeCoverage YES

      - name: Generate coverage report
        run: |
          slather coverage \
            --input-format profdata \
            --cobertura-xml \
            --output-directory coverage \
            --scheme App \
            App.xcworkspace

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: ios-coverage
          path: coverage/
```

---
