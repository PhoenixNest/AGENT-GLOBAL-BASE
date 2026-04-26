---
name: testing-qa-mobile-device-farm-management
description: Device farm management for mobile testing — Firebase Test Lab, AWS Device Farm, BrowserStack, Sauce Labs configuration, device matrix selection, real device vs emulator strategy, and device farm cost optimization. Owned by Rachel Kim (Test Automation Lead). Use during Stage 4 (Implementation Plan) for device farm strategy and Stage 7 (Testing) for device farm test execution. Trigger: device farm management, Firebase Test Lab, AWS Device Farm, BrowserStack, Sauce Labs, device matrix, real device testing, emulator strategy.
prerequisites:
  - testing-qa-overview

version: "1.0.0"
---

# Device Farm Management — Cloud Testing Infrastructure

**Category:** Mobile Test Infrastructure — Device Management
**Owner:** SDET Mobile #2 (Tobias Weber)

## Overview

This skill covers the operation, optimization, and management of cloud-based device farms for mobile test execution. It encompasses AWS Device Farm, Firebase Test Lab, and BrowserStack — the three primary platforms for scalable mobile testing across real devices. Device farm management ensures that automated test suites execute reliably across the target device matrix, with comprehensive result aggregation, screenshot/video capture, and automated flaky test detection.

Effective device farm management directly impacts Stage 7 test throughput and Stage 8 integrity verification confidence. A well-managed device farm provides the statistical confidence that a release candidate will perform correctly for end users across the fragmentation landscape of Android and iOS devices.

## Competency Dimensions

| Dimension                             | Description                                                                                                                                                            | Proficiency Indicators                                                                                                                                                                                                                                                                                     |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AWS Device Farm**                   | Project configuration, device pool creation, test scheduling, Appium/Espresso/XCTest integration, result analysis, artifact download, pricing optimization             | Device pools configured by OS version, manufacturer, form factor; test runs scheduled via CLI (`aws devicefarm schedule-run`); artifacts (screenshots, logs, videos) downloaded programmatically; reserved device minutes purchased for cost optimization; results parsed from Device Farm's JSON report   |
| **Firebase Test Lab**                 | Test matrix configuration, Robo test execution, instrumentation test runs, Game Loop test (if applicable), results via Firebase Console / gcloud CLI, shard management | Test matrices defined with `--device` flags for multi-device parallelism; sharding configured via `--numUniformShards`; Robo tests run on every major UI change; results aggregated via `gcloud firebase test android models list`; Flank used for advanced sharding and cost optimization                 |
| **BrowserStack App Automate**         | App upload, test capability configuration, parallel test execution, session inspection, debug artifacts (logs, screenshots, videos), network logs, team management     | Capabilities set via `browserstack.appium` driver config; parallel sessions managed via `maxInstances`; session URLs captured for defect reports; network logs enabled for API interaction debugging; team access scoped by role; Automate API used for programmatic test scheduling                       |
| **Test Scheduling & Orchestration**   | CI-triggered test runs, cron-based regression schedules, test distribution across platforms, priority queue management, resource allocation                            | Tests triggered on PR merge (smoke suite), nightly (full regression), weekly (extended device matrix); priority queues ensure P0/P1-related tests run first; resource allocation optimized to minimize queue wait time; scheduling respects device availability windows                                    |
| **Results Aggregation & Reporting**   | JUnit XML parsing, cross-platform result normalization, trend analysis, pass-rate dashboards, defect auto-filing, SLA monitoring                                       | Results from all platforms normalized to JUnit XML; aggregated dashboard shows pass rate by device, OS, test suite; trend analysis flags degrading tests; auto-filing creates defects for new failures with attached artifacts; SLA monitoring alerts on test completion delays                            |
| **Screenshot & Video Capture**        | Automatic capture on failure, manual capture checkpoints, video recording for full session, screenshot diff comparison, artifact retention policy                      | Screenshots captured on every assertion failure; video recording enabled for all sessions; manual checkpoints at critical journey steps; screenshot diff detects visual regressions; artifacts retained for 90 days in cloud storage; attached to defect reports automatically                             |
| **Flaky Test Detection & Management** | Statistical flake analysis, retry-based detection, quarantine workflow, root cause categorization, reintegration criteria                                              | Flake detection via statistical analysis (test fails intermittently across same code); retry count configurable per test; quarantined tests tracked in dedicated dashboard; root causes categorized as: timing, state, network, platform, infrastructure; reintegration requires 50 consecutive clean runs |

## Execution Guidance

### AWS Device Farm

**1. Project & Device Pool Setup**

```bash
# Create project
aws devicefarm create-project --name "CompanyApp-Mobile-Tests"

# List available devices
aws devicefarm get-device-pool --arn $PROJECT_ARN

# Create device pool (flagship devices)
aws devicefarm create-device-pool \
  --project-arn $PROJECT_ARN \
  --name "Flagship-Android" \
  --rules '[
    {"attribute": "PLATFORM", "operator": "EQUALS", "value": "ANDROID"},
    {"attribute": "FORM_FACTOR", "operator": "EQUALS", "value": "PHONE"},
    {"attribute": "OS_VERSION", "operator": "GREATER_THAN_OR_EQUALS", "value": "13"}
  ]'

# Create iOS device pool
aws devicefarm create-device-pool \
  --project-arn $PROJECT_ARN \
  --name "Flagship-iOS" \
  --rules '[
    {"attribute": "PLATFORM", "operator": "EQUALS", "value": "IOS"},
    {"attribute": "FORM_FACTOR", "operator": "EQUALS", "value": "PHONE"},
    {"attribute": "OS_VERSION", "operator": "GREATER_THAN_OR_EQUALS", "value": "16.0"}
  ]'
```

**2. Schedule Android Instrumentation Test Run**

```bash
# Upload APK
APK_UPLOAD=$(aws devicefarm upload \
  --project-arn $PROJECT_ARN \
  --type ANDROID_APP \
  --name "app-debug.apk")

aws devicefarm upload \
  --arn $APK_UPLOAD_ARN \
  --content-type application/octet-stream \
  --body app/build/outputs/apk/debug/app-debug.apk

# Upload test APK
TEST_UPLOAD=$(aws devicefarm upload \
  --project-arn $PROJECT_ARN \
  --type INSTRUMENTATION_TEST_PACKAGE \
  --name "app-debug-androidTest.apk")

# Schedule run
RUN=$(aws devicefarm schedule-run \
  --project-arn $PROJECT_ARN \
  --name "Android-Regression-$(date +%Y%m%d)" \
  --device-pool-arn $DEVICE_POOL_ARN \
  --test type=INSTRUMENTATION,testPackageArn=$TEST_UPLOAD_ARN \
  --configuration '{"executionTimeoutMinutes": 30, "accountsCleanup": true, "appPackagesCleanup": true}')

# Wait for completion and get results
aws devicefarm get-run --arn $RUN_ARN
```

**3. Download Results & Artifacts**

```bash
# List all artifacts from run
aws devicefarm list-artifacts --arn $RUN_ARN --type SCREENSHOT > screenshots.json

# Download each screenshot
jq -r '.artifacts[].url' screenshots.json | while read url; do
  curl -o "screenshots/$(basename $url)" "$url"
done

# Download logs
aws devicefarm list-artifacts --arn $RUN_ARN --type LOG > logs.json
jq -r '.artifacts[].url' logs.json | while read url; do
  curl -o "logs/$(basename $url)" "$url"
done

# Download video recordings
aws devicefarm list-artifacts --arn $RUN_ARN --type VIDEO > videos.json
jq -r '.artifacts[].url' videos.json | while read url; do
  curl -o "videos/$(basename $url)" "$url"
done
```

### Firebase Test Lab

**1. Multi-Device Test Matrix**

```bash
gcloud firebase test android run \
  --type instrumentation \
  --app app/build/outputs/apk/debug/app-debug.apk \
  --test app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk \
  --device model=Pixel6,version=33,locale=en,orientation=portrait \
  --device model=Pixel7,version=34,locale=en,orientation=portrait \
  --device model=GalaxyS23,version=33,locale=en,orientation=portrait \
  --device model=GalaxyS24,version=34,locale=en,orientation=portrait \
  --num-uniform-shards=10 \
  --timeout 20m \
  --results-bucket gs://company-test-results \
  --results-dir android-regression-$(date +%Y%m%d-%H%M%S) \
  --test-targets "notAnnotation com.company.testing.FlakyTest"
```

**2. Flank for Advanced Sharding & Cost Optimization**

`flank.yml`:

```yaml
gcloud:
  type: instrumentation
  app: app/build/outputs/apk/debug/app-debug.apk
  test: app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk
  device:
    - model: Pixel6
      version: 33
      locale: en
      orientation: portrait
    - model: GalaxyS23
      version: 33
      locale: en
      orientation: portrait
  num-test-runs: 3 # Run 3x to detect flakiness
  test-targets-always-run:
    - class com.company.CheckoutFlowTest
  test-targets:
    - class com.company.LoginFlowTest
    - class com.company.SearchFlowTest
  max-test-shards: 20
  timeout-minutes: 15
  output-style: compact
  full-junit-result: true
  results-bucket: gs://company-test-results
```

Execute:

```bash
flank firebase test android run --config flank.yml
```

**3. Robo Test for Exploratory Coverage**

```bash
gcloud firebase test android run \
  --type robo \
  --app app/build/outputs/apk/debug/app-debug.apk \
  --device model=Pixel6,version=33 \
  --timeout 10m \
  --no-auto-google-login \
  --results-bucket gs://company-test-results \
  --results-dir robo-exploratory-$(date +%Y%m%d)
```

Robo tests crawl the app automatically, discovering crashes, rendering issues, and navigation dead-ends without requiring test scripts. Run on every major UI change.

### BrowserStack App Automate

**1. Test Capability Configuration**

```javascript
// wdio.conf.js for BrowserStack
exports.config = {
  user: process.env.BROWSERSTACK_USERNAME,
  key: process.env.BROWSERSTACK_ACCESS_KEY,
  host: "hub-cloud.browserstack.com",
  port: 443,

  capabilities: [
    {
      "bstack:options": {
        projectName: "CompanyApp-Mobile",
        buildName: "Regression-Suite",
        sessionName: "Android-Checkout-Flow",
        debug: true,
        networkLogs: true,
        appiumLogs: true,
        video: true,
        seleniumLogs: true,
        consoleLogs: "verbose",
      },
      platformName: "Android",
      "appium:deviceName": "Google Pixel 7",
      "appium:platformVersion": "13.0",
      "appium:automationName": "uiautomator2",
      "appium:app": process.env.BROWSERSTACK_APP_ID,
    },
  ],

  maxInstances: 5, // Parallel sessions
  services: [
    [
      "browserstack",
      {
        browserstackLocal: false,
      },
    ],
  ],

  reporters: [
    [
      "junit",
      {
        outputDir: "./test-results/browserstack",
        outputFileFormat: function (opts) {
          return `results-${opts.capabilities["bstack:options"].buildName}.xml`;
        },
      },
    ],
  ],
};
```

**2. App Upload via API**

```bash
# Upload app
curl -u "$BROWSERSTACK_USERNAME:$BROWSERSTACK_ACCESS_KEY" \
  -X POST "https://api-cloud.browserstack.com/app-automate/upload" \
  -F "file=@app-debug.apk"

# Response: {"app_url": "bs://a1b2c3d4e5f6..."}
# Store this URL in CI environment variable
```

**3. Session Inspection & Debug**

After test execution, each session has a unique BrowserStack URL:

```
https://automate.browserstack.com/dashboard/v2/sessions/<session-id>
```

The session dashboard provides:

- Full video recording with step-by-step breakdown
- Device logs (logcat for Android, syslog for iOS)
- Appium command log with timing
- Network logs (HTTP requests/responses)
- Screenshots at each assertion
- Performance metrics (CPU, memory, network)

Capture session URLs in test output for defect report attachment:

```javascript
afterTest: function (test, context, { error, result, duration, passed, retries }) {
  if (!passed) {
    const sessionUrl = context.browser.capabilities['bstack:options'].session_url;
    console.error(`Failed test: ${test.title}`);
    console.error(`BrowserStack session: ${sessionUrl}`);
    console.error(`Error: ${error.message}`);
  }
}
```

### Test Scheduling Strategy

| Schedule                   | Suite                                                    | Device Coverage                                    | Trigger               |
| -------------------------- | -------------------------------------------------------- | -------------------------------------------------- | --------------------- |
| **PR Smoke**               | Critical user journeys (login, checkout, core feature)   | 2 devices (1 Android flagship, 1 iOS flagship)     | On every PR to `main` |
| **Nightly Regression**     | Full test suite (unit + integration + E2E)               | 4 devices (2 Android, 2 iOS across OS versions)    | Daily at 02:00 UTC    |
| **Weekly Extended Matrix** | Full regression + exploratory Robo tests                 | 12 devices (6 Android, 6 iOS — full device matrix) | Saturday 00:00 UTC    |
| **Pre-Release**            | Full regression + performance tests + Robo + visual diff | 20+ devices (all supported devices)                | Before Stage 8 gate   |
| **On-Demand**              | Specific test class or feature suite                     | Configurable                                       | Manual trigger via CI |

### Results Aggregation Pipeline

```bash
#!/bin/bash
# aggregate-results.sh — Merge JUnit XML from all platforms

RESULTS_DIR="./test-results"
OUTPUT_DIR="./test-results/aggregated"

mkdir -p $OUTPUT_DIR

# Merge Android results (Firebase + AWS Device Farm)
find $RESULTS_DIR -name "*android*.xml" -exec cat {} + > $OUTPUT_DIR/android-merged.xml

# Merge iOS results
find $RESULTS_DIR -name "*ios*.xml" -exec cat {} + > $OUTPUT_DIR/ios-merged.xml

# Generate summary report
REPORT_FILE="$OUTPUT_DIR/test-summary-$(date +%Y%m%d).md"

cat > $REPORT_FILE << EOF
# Test Results Summary — $(date +%Y-%m-%d)

## Android
| Metric | Value |
|--------|-------|
| Total Tests | $(grep -c 'testcase' $OUTPUT_DIR/android-merged.xml) |
| Passed | $(grep -c 'testcase' $OUTPUT_DIR/android-merged.xml | xargs -I{} echo {} | awk '{print $1 - failures}') |
| Failed | $(grep -c 'failure' $OUTPUT_DIR/android-merged.xml || echo 0) |
| Skipped | $(grep -c 'skipped' $OUTPUT_DIR/android-merged.xml || echo 0) |
| Duration | $(grep 'time=' $OUTPUT_DIR/android-merged.xml | awk -F'"' '{sum+=$2} END {print sum "s"}') |

## iOS
| Metric | Value |
|--------|-------|
| Total Tests | $(grep -c 'testcase' $OUTPUT_DIR/ios-merged.xml) |
| Passed | $(grep -c 'testcase' $OUTPUT_DIR/ios-merged.xml | xargs -I{} echo {} | awk '{print $1 - failures}') |
| Failed | $(grep -c 'failure' $OUTPUT_DIR/ios-merged.xml || echo 0) |
| Skipped | $(grep -c 'skipped' $OUTPUT_DIR/ios-merged.xml || echo 0) |
| Duration | $(grep 'time=' $OUTPUT_DIR/ios-merged.xml | awk -F'"' '{sum+=$2} END {print sum "s"}') |

## Failed Tests
$(grep -B2 'failure' $OUTPUT_DIR/android-merged.xml | grep 'name=' | sed 's/.*name="\([^"]*\)".*/- Android: \1/')
$(grep -B2 'failure' $OUTPUT_DIR/ios-merged.xml | grep 'name=' | sed 's/.*name="\([^"]*\)".*/- iOS: \1/')
EOF

echo "Report generated: $REPORT_FILE"
```

### Flaky Test Detection — Statistical Analysis

```python
#!/usr/bin/env python3
"""
flake_detector.py — Analyze test results across multiple runs to identify flaky tests.

A test is classified as flaky if:
- It has both pass and fail results across identical code (same commit)
- Flake rate > 10% (fails between 10% and 90% of runs)
- Not consistently failing (that would be a real bug, not flake)
"""

import json
import sys
from collections import defaultdict

def analyze_flake_rate(results_file, threshold=0.10):
    """Analyze JUnit XML results for flaky test detection."""
    # Parse results (simplified — use junitparser in production)
    test_results = defaultdict(lambda: {'pass': 0, 'fail': 0, 'total': 0})

    # In production: parse JUnit XML with junitparser library
    # For each test case entry:
    #   test_results[full_class_name + "." + test_name]['pass'] += 1  # or 'fail'
    #   test_results[...]['total'] += 1

    flaky_tests = []
    for test_name, counts in test_results.items():
        if counts['total'] < 5:
            continue  # Insufficient data

        fail_rate = counts['fail'] / counts['total']
        if threshold < fail_rate < 0.90:
            flaky_tests.append({
                'test': test_name,
                'total_runs': counts['total'],
                'failures': counts['fail'],
                'flake_rate': round(fail_rate * 100, 1),
                'classification': 'FLAKY'
            })

    return sorted(flaky_tests, key=lambda x: x['flake_rate'], reverse=True)

if __name__ == '__main__':
    results_file = sys.argv[1] if len(sys.argv) > 1 else 'test-results/aggregated/'
    flaky = analyze_flake_rate(results_file)

    print(f"Found {len(flaky)} flaky tests:")
    for test in flaky:
        print(f"  [{test['flake_rate']}% flake] {test['test']} "
              f"({test['failures']}/{test['total_runs']} runs failed)")
```

**Quarantine Workflow:**

1. Flake detector runs nightly against aggregated results
2. Tests exceeding 10% flake rate flagged in dashboard
3. SDET reviews flagged tests within 24 hours
4. Root cause identified and categorized:
   - **Timing**: Replace implicit waits with explicit synchronization
   - **State**: Add proper test isolation/reset
   - **Network**: Mock external dependencies
   - **Platform**: File platform-specific defect
   - **Infrastructure**: Report to device farm provider
5. Test moved to `quarantine/` directory
6. Fix developed and verified with 50 consecutive clean runs
7. Test returned to main suite

## Pipeline Integration

| Stage                                | Application                                                                                                                                                                                                             |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 5** (Development)            | Provision device farm credentials in CI; configure initial device pools; validate test execution on at least 1 device per platform                                                                                      |
| **Stage 7** (Automated Testing)      | **Primary ownership** — execute full test suite across device matrix; aggregate results from all platforms; capture screenshots/videos for failed tests; run flaky test detection analysis; produce Test Results Report |
| **Stage 8** (Integrity Verification) | Re-run full regression suite on pre-release device matrix; verify all previously failing tests now pass; confirm no new flaky tests introduced                                                                          |

## Quality Standards

| Metric                            | Target                                                      | Measurement                                                            |
| --------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------- |
| Device matrix coverage            | 100% of PRD-specified devices/OS versions                   | Traced to PRD platform requirements; gap = P1 defect                   |
| Test completion SLA (nightly)     | Full suite completes within 60 minutes                      | Measured from CI trigger to final result aggregation                   |
| Flaky test quarantine SLA         | Identified within 24 hours, resolved within 5 business days | Tracked via quarantine dashboard                                       |
| Screenshot/video capture rate     | 100% of failed test executions                              | Verified by CI artifact presence check                                 |
| Results aggregation accuracy      | 100% of device results merged into unified report           | Automated validation: sum of per-device test counts = aggregated total |
| Device farm cost efficiency       | < 15% waste on idle device time                             | Measured via provider billing dashboard; optimize via shard tuning     |
| Artifact retention                | 90 days for all test artifacts                              | Cloud storage lifecycle policy; verified monthly                       |
| Flaky test rate (post-quarantine) | < 3% of total test suite                                    | Measured weekly; sustained > 5% triggers process review                |
