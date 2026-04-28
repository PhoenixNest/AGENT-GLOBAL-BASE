# CI/CD Integration

## CI/CD Integration

### Pipeline Integration

Tests must integrate at multiple points in the CI/CD pipeline:

```
Developer commits code
    │
    ▼
┌──────────────────────────────────────┐
│ PRE-COMMIT (local)                   │
│ ├── Lint (ktlint, SwiftLint)         │
│ ├── Unit tests (fast subset)         │
│ └── Type checking                    │
│ Duration: < 30 seconds               │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│ CI — PULL REQUEST                    │
│ ├── Full unit test suite             │
│ ├── Integration tests                │
│ ├── Lint + static analysis           │
│ ├── Build verification               │
│ └── Code coverage report             │
│ Duration: < 10 minutes               │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│ CI — MERGE TO MAIN                   │
│ ├── Full test suite                  │
│ ├── UI tests (emulator/simulator)    │
│ ├── E2E smoke tests (device farm)    │
│ ├── Performance baseline check       │
│ └── Accessibility audit              │
│ Duration: < 30 minutes               │
└──────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────┐
│ RELEASE CANDIDATE                    │
│ ├── Full regression suite            │
│ ├── Device farm validation           │
│ ├── Performance benchmarking         │
│ ├── Security scan                    │
│ └── Beta distribution                │
│ Duration: < 2 hours                  │
└──────────────────────────────────────┘
```

### GitHub Actions Example

```yaml
# .github/workflows/mobile-tests.yml
name: Mobile Tests

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  android-unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          distribution: "temurin"
          java-version: "21"
      - name: Run Android unit tests
        run: ./gradlew testDebugUnitTest
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: android-test-results
          path: "**/build/test-results/test*/"
      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: android-coverage
          path: "**/build/reports/jacoco/"

  ios-unit-tests:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Run iOS unit tests
        run: |
          xcodebuild test \
            -workspace App.xcworkspace \
            -scheme App \
            -destination 'platform=iOS Simulator,name=iPhone 15,OS=latest' \
            -resultBundlePath TestResults

  maestro-e2e:
    runs-on: ubuntu-latest
    needs: [android-unit-tests, ios-unit-tests]
    steps:
      - uses: actions/checkout@v4
      - name: Build APK
        run: ./gradlew assembleDebug
      - name: Run Maestro tests
        uses: mobile-dev-inc/action-maestro-cloud@v1
        with:
          api-key: ${{ secrets.MAESTRO_API_KEY }}
          app-file: app/build/outputs/apk/debug/app-debug.apk
          project-id: ${{ secrets.MAESTRO_PROJECT_ID }}
```

### Fastlane Integration

```ruby
# fastlane/Fastfile
default_platform(:android)

platform :android do
  lane :test do
    gradle(task: "testDebugUnitTest")
    jacoco(
      execution_data: "app/build/outputs/unit_test_code_coverage/debugUnitTest/testDebugUnitTest.exec"
    )
  end

  lane :ui_test do
    gradle(task: "connectedDebugAndroidTest")
  end

  lane :full_test do
    test
    ui_test
    maestro(
      flow_path: "maestro/flows/"
    )
  end
end

platform :ios do
  lane :test do
    scan(
      scheme: "App",
      devices: ["iPhone 15"],
      output_directory: "fastlane/test_output",
      output_types: "html,junit"
    )
  end
end
```

---
