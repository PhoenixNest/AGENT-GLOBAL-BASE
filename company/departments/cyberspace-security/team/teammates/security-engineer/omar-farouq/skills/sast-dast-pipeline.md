# SAST/DAST Pipeline Engineering

**Category:** Application Security — CI/CD Integration
**Owner:** Security Engineer #2 — Omar Farouq (SAST/DAST Pipeline Specialist)

## Overview

Design, implement, and maintain automated static and dynamic application security testing (SAST/DAST) pipelines integrated into the software development lifecycle. This skill covers SAST tool configuration (Semgrep, CodeQL), DAST automation (OWASP ZAP, Nuclei), dependency scanning (Snyk, Dependabot), CI/CD quality gate enforcement, false positive management, and security metrics reporting. The objective is to shift security left by catching vulnerabilities at the earliest possible stage while maintaining developer velocity through intelligent triage and automated remediation guidance.

## Competency Dimensions

| Dimension                 | Description                                                 | Proficiency Indicators                                                                                                                                                        |
| ------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SAST Engine Configuration | Tuning static analysis tools for high signal-to-noise ratio | Writes custom Semgrep rules with <3% false positive rate; configures CodeQL for mobile-specific query packs; achieves 80%+ true positive rate on known vulnerability datasets |
| DAST Automation           | Orchestrating dynamic scanning against mobile API backends  | Configures OWASP ZAP automation framework with authenticated scanning; achieves 95%+ endpoint coverage; integrates Nuclei templates for CVE-specific testing                  |
| Dependency Scanning       | Managing software supply chain vulnerability detection      | Configures Snyk with custom ignore rules and SLA-based alerting; achieves 100% transitive dependency coverage; automates PR-based vulnerability remediation                   |
| CI/CD Integration         | Embedding security gates into build pipelines               | Implements non-blocking (advisory) and blocking (gate) scan stages; pipeline adds <5 minutes to build time; gate failures provide actionable remediation guidance             |
| False Positive Management | Systematic reduction of noise in security tooling           | Maintains <5% false positive rate across all SAST/DAST tools; implements baseline suppression with expiration; tracks FP trends with monthly reduction targets                |
| Quality Gate Design       | Defining pass/fail criteria for automated security checks   | Designs gates that block P0/P1 vulnerabilities while allowing P2/P3 with documented exceptions; gate logic maps to defect severity classification system                      |

## Execution Guidance

### 1. SAST Pipeline — Semgrep Custom Rules

**Why Semgrep:** Semgrep provides fast, language-aware static analysis with an intuitive rule syntax. It excels at detecting insecure patterns in mobile application code (Kotlin, Swift, Java, Objective-C, Dart) and supports custom rule packs tailored to company security standards.

**Semgrep Rule Architecture:**

```yaml
# rules/mobile-security/insecure-crypto.yml
rules:
  - id: insecure-aes-ecb-mode
    pattern: |
      Cipher.getInstance("AES/ECB/...")
    message: >
      AES in ECB mode is cryptographically insecure — identical plaintext blocks
      produce identical ciphertext blocks, enabling pattern analysis. Use
      AES-GCM or AES-CBC with random IV instead.
    severity: ERROR
    languages: [java, kotlin]
    metadata:
      owasp: MASVS V3.1.1
      cwe: CWE-327: Use of a Broken or Risky Cryptographic Algorithm
      confidence: HIGH
      impact: HIGH
      remediation: |
        Replace with: Cipher.getInstance("AES/GCM/NoPadding")
        Ensure IV is generated via SecureRandom and never reused.

  - id: hardcoded-api-key
    patterns:
      - pattern-either:
          - pattern: |
              $KEY = "AIza..."
          - pattern: |
              String $KEY = "sk-..."
          - pattern: |
              let $KEY = "xoxb-..."
      - pattern-not: |
          $KEY = ""
      - pattern-not: |
          $KEY = "YOUR_KEY_HERE"
    message: >
      Hardcoded API key detected. API keys must be loaded from secure
      configuration (BuildConfig, encrypted SharedPreferences, or remote
      configuration with certificate pinning).
    severity: ERROR
    languages: [java, kotlin, swift]
    metadata:
      owasp: MASVS V7.1.4
      cwe: CWE-798: Use of Hard-coded Credentials
      confidence: HIGH
      impact: CRITICAL

  - id: insecure-webview-javascript
    pattern-either:
      - pattern: |
          $WEBVIEW.getSettings().setJavaScriptEnabled(true)
      - pattern: |
          $WEBVIEW.getSettings().setAllowFileAccess(true)
      - pattern: |
          $WEBVIEW.addJavascriptInterface(...)
    message: >
      WebView JavaScript enabled without security controls. If JavaScript
      is required, ensure: (1) setAllowFileAccess(false), (2) no
      addJavascriptInterface() with sensitive objects, (3) URL loading
      validated against allowlist.
    severity: WARNING
    languages: [java, kotlin]
    metadata:
      owasp: MASVS V6.1.5
      cwe: CWE-749: Exposed Dangerous Method or Function
      confidence: MEDIUM
      impact: HIGH
```

**Semgrep CI Integration (GitHub Actions):**

```yaml
# .github/workflows/security-sast.yml
name: Security — SAST (Semgrep)
on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    container:
      image: returntocorp/semgrep
    steps:
      - uses: actions/checkout@v4

      - name: Run Semgrep Scan
        run: |
          semgrep ci \
            --config ./security/rules/mobile-security/ \
            --config p/owasp-top-ten \
            --config p/cwe-top-25 \
            --json --output semgrep-results.json \
            --baseline-ref origin/main

      - name: Evaluate Quality Gate
        run: |
          ERRORS=$(jq '[.results[] | select(.extra.severity == "ERROR")] | length' semgrep-results.json)
          if [ "$ERRORS" -gt 0 ]; then
            echo "❌ SAST gate failed: $ERRORS ERROR-level findings"
            jq '.results[] | select(.extra.severity == "ERROR") | {rule: .check_id, file: .path, line: .start.line, message: .extra.message}' semgrep-results.json
            exit 1
          fi
          echo "✅ SAST gate passed"

      - name: Upload SARIF to GitHub
        if: always()
        run: |
          semgrep convert semgrep-results.json --format sarif --output semgrep.sarif
        # Upload via GitHub API to Security tab

      - name: Comment on PR
        if: failure()
        uses: marocchino/sticky-pull-request-comment@v2
        with:
          header: semgrep-findings
          path: semgrep-results.json
          recreate: true
```

**Custom Rule Development Process:**

1. Identify recurring vulnerability patterns from pen test findings (Sana Khoury's reports)
2. Write Semgrep rule with `pattern`, `message`, `severity`, and `metadata`
3. Test against known-vulnerable code samples (positive test) and clean code samples (negative test)
4. Run against entire codebase; analyze false positive rate
5. If FP rate >5%, refine rule patterns or add `pattern-not` exclusions
6. Commit rule to `security/rules/mobile-security/` with documentation
7. Add to CI pipeline configuration

### 2. SAST Pipeline — CodeQL for Deep Analysis

**CodeQL Configuration for Mobile:**

```yaml
# .github/codeql/codeql-config.yml
name: 'Mobile Security CodeQL'
queries:
  - uses: security-extended
  - uses: security-and-quality
  - uses: ./security/codeql-queries/mobile-specific.ql
paths:
  - platforms/android/code/
  - platforms/ios/code/
paths-ignore:
  - '**/test/**'
  - '**/build/**'
  - '**/.gradle/**'
  - 'Pods/'
  - '.build/'
```

**Key CodeQL Query Packs for Mobile:**

- `java/android/insecure-storage.ql` — Detects plaintext storage of sensitive data
- `java/android/insecure-network.ql` — Detects missing TLS configuration
- `swift/ios/keychain-misuse.ql` — Detects incorrect Keychain access group usage
- `swift/ios/insecure-nsuserdefaults.ql` — Detects sensitive data in UserDefaults

### 3. DAST Pipeline — OWASP ZAP Automation

**ZAP Automation Framework Configuration:**

```yaml
# zap-automation.yaml
env:
  contexts:
    - name: 'Mobile API Backend'
      urls:
        - 'https://api-staging.example.com'
      authentication:
        method: 'json'
        parameters:
          loginUrl: 'https://api-staging.example.com/auth/login'
          loginRequest: |
            {"username": "{{ZAP_AUTH_USER}}", "password": "{{ZAP_AUTH_PASS}}"}
        verification:
          method: 'response'
          loggedInIndicator: "\\Q\"access_token\"\\E"
          loggedOutIndicator: "\\Q\"unauthorized\"\\E"
      users:
        - name: 'Test User'
          credentials:
            username: 'zap-test-user@example.com'
            password: '${ZAP_TEST_PASSWORD}'

jobs:
  - type: 'spider'
    name: 'API Spider'
    parameters:
      maxDuration: 15
      url: 'https://api-staging.example.com'

  - type: 'spiderAjax'
    name: 'AJAX Spider'
    parameters:
      maxDuration: 20

  - type: 'activeScan'
    name: 'Active Security Scan'
    parameters:
      policy: 'API-scan'
      maxRuleDurationInMins: 10

  - type: 'passiveScan'
    name: 'Passive Security Scan'

  - type: 'report'
    name: 'HTML Report'
    parameters:
      template: 'traditional-html'
      reportFile: 'zap-report.html'

  - type: 'outputSummary'
    name: 'Quality Gate'
    parameters:
      format: 'JSON'
      summaryFile: 'zap-summary.json'
      failOnHigh: true
      failOnMedium: true
```

**ZAP CI Integration:**

```yaml
# .github/workflows/security-dast.yml
name: Security — DAST (OWASP ZAP)
on:
  schedule:
    - cron: '0 2 * * 1-5'  # Weekdays at 2 AM
  workflow_dispatch:
    inputs:
      target_env:
        description: 'Target environment'
        required: true
        default: 'staging'
        type: choice
        options: [staging, pre-production]

jobs:
  zap-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout ZAP Config
        uses: actions/checkout@v4

      - name: OWASP ZAP Full Scan
        uses: zaproxy/action-full-scan@v0.12.0
        with:
          target: 'https://api-${{ github.event.inputs.target_env || 'staging' }}.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a -j'
          allow_issue_writing: false
          fail_action: true
          artifact_name: 'zap-results'

      - name: Evaluate DAST Gate
        run: |
          # Parse ZAP results for risk levels
          HIGH=$(jq '[.site[].alerts[] | select(.riskcode == "3")] | length' zap-results.json)
          MEDIUM=$(jq '[.site[].alerts[] | select(.riskcode == "2")] | length' zap-results.json)
          if [ "$HIGH" -gt 0 ] || [ "$MEDIUM" -gt 0 ]; then
            echo "❌ DAST gate failed: $HIGH High, $MEDIUM Medium risk alerts"
            exit 1
          fi
          echo "✅ DAST gate passed"
        env:
          ZAP_TEST_PASSWORD: ${{ secrets.ZAP_TEST_PASSWORD }}
```

### 4. Dependency Scanning — Snyk Integration

**Snyk CI Configuration:**

```yaml
# .github/workflows/security-dependencies.yml
name: Security — Dependency Scanning (Snyk)
on:
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 6 * * *' # Daily at 6 AM

jobs:
  snyk-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Snyk Gradle Scan
        uses: snyk/actions/gradle@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: >
            --severity-threshold=high
            --json-file-output=snyk-android-results.json
            --fail-on=all

      - name: Snyk Monitor (SBOM generation)
        uses: snyk/actions/gradle@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          command: monitor
          args: --project-name=mobile-app-android

  snyk-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Snyk CocoaPods Scan
        uses: snyk/actions/cocoapods@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: >
            --severity-threshold=high
            --json-file-output=snyk-ios-results.json
            --fail-on=all

  snyk-gate:
    needs: [snyk-android, snyk-ios]
    runs-on: ubuntu-latest
    steps:
      - name: Download Results
        uses: actions/download-artifact@v4

      - name: Evaluate Dependency Gate
        run: |
          CRITICAL=$(jq '[.vulnerabilities[] | select(.severity == "critical")] | length' snyk-android-results.json snyk-ios-results.json 2>/dev/null || echo 0)
          HIGH=$(jq '[.vulnerabilities[] | select(.severity == "high")] | length' snyk-android-results.json snyk-ios-results.json 2>/dev/null || echo 0)
          if [ "$CRITICAL" -gt 0 ]; then
            echo "❌ Dependency gate failed: $CRITICAL critical vulnerabilities"
            exit 1
          fi
          if [ "$HIGH" -gt 3 ]; then
            echo "❌ Dependency gate failed: $HIGH high vulnerabilities (threshold: 3)"
            exit 1
          fi
          echo "✅ Dependency gate passed ($HIGH high vulns, within threshold)"
```

**Snyk Ignore Policy (snyk-policy.yml):**

```yaml
# .snyk-policy.yml
# Accepted vulnerabilities with documented justification and expiration
ignore:
  SNYK-JAVA-ORGAPACHELOGGINGLOG4J-123456:
    - reason: >
        log4j is only used in test scope; not included in production APK.
        Verified via `./gradlew app:dependencies --configuration releaseRuntimeClasspath`
      expires: 2027-01-01
      created: 2026-04-01
      reason-type: not-vulnerable
```

### 5. False Positive Management System

**Baseline Suppression Workflow:**

1. **Initial Baseline**: On first SAST/DAST pipeline run, generate baseline of all findings
2. **Triage**: Security engineer reviews each finding — True Positive (TP), False Positive (FP), or Accepted Risk (AR)
3. **Suppression**: FP findings added to suppression file with justification and expiration date
4. **Monitoring**: Suppressed findings re-evaluated monthly; expired suppressions trigger re-scan
5. **Trend Analysis**: Monthly report on FP rate, TP rate, and suppression aging

**Suppression File Format:**

```yaml
# .security-suppressions.yml
suppressions:
  - rule: insecure-webview-javascript
    file: platforms/android/code/app/src/main/java/com/example/HelpActivity.kt
    justification: >
      WebView loads only local HTML from assets/ folder (no network content).
      JavaScript is required for interactive help content. Risk accepted as
      no external URL loading is possible.
    expires: 2026-10-01
    status: accepted-risk
    approved-by: omar-farouq
    review-date: 2026-07-01

  - rule: semgrep/insecure-random
    file: platforms/android/code/app/src/test/java/.../RandomTest.kt
    justification: 'Test code only — not included in production build'
    expires: 2027-01-01
    status: false-positive
    approved-by: omar-farouq
```

**FP Rate Monitoring Dashboard Metrics:**

| Metric               | Target    | Alert Threshold               |
| -------------------- | --------- | ----------------------------- |
| Overall FP Rate      | <5%       | >8% triggers rule review      |
| New FP Rate (30-day) | <3%       | >5% triggers immediate review |
| Suppression Aging    | <90 days  | >60 days triggers reminder    |
| TP Detection Rate    | >85%      | <80% triggers gap analysis    |
| Mean Time to Triage  | <24 hours | >48 hours escalates to CSO    |

### 6. Quality Gate Design

**Gate Logic by Severity:**

| Severity      | Gate Action             | SLA                    | Escalation           |
| ------------- | ----------------------- | ---------------------- | -------------------- |
| P0 (Critical) | Block merge/release     | Immediate fix required | Notifies CTO + CSO   |
| P1 (High)     | Block merge/release     | Fix within 24 hours    | Notifies team lead   |
| P2 (Medium)   | Advisory (non-blocking) | Fix within sprint      | Weekly report to CSO |
| P3 (Low)      | Advisory (non-blocking) | Fix when convenient    | Monthly trend report |

**Gate Configuration:**

```yaml
# .github/security-gate.yml
gate:
  blocking:
    severity: [critical, high]
    types: [sast, dast, dependency]
    exceptions: [] # No exceptions for P0/P1

  advisory:
    severity: [medium, low]
    types: [sast, dast, dependency]
    report_to: [cs-office, team-leads]
    frequency: weekly

  metrics:
    track:
      - total_findings_by_severity
      - mean_time_to_remediate
      - false_positive_rate
      - coverage_percentage
    dashboard: security-dashboard.example.com
    alert_channels: [slack-security, email-cso]
```

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                                                         |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 4** (Implementation Plan)    | SAST/DAST pipeline configuration is part of the implementation plan; tool selection and rule configuration must be documented before Stage 5 begins                 |
| **Stage 5** (Development)            | SAST runs on every PR; DAST runs nightly against staging environment; dependency scanning runs on every dependency change; findings flow to developers in real-time |
| **Stage 6** (Code Review)            | SAST/DAST results are aggregated into the Defect Report; quality gate pass/fail status is a gate criterion for Stage 6 → Stage 7 progression                        |
| **Stage 7** (Automated Testing)      | DAST results complement automated test results; security test coverage is tracked alongside functional test coverage                                                |
| **Stage 8** (Integrity Verification) | SAST/DAST pipeline re-runs on the release candidate build; verifies no new vulnerabilities introduced during remediation                                            |
| **Stage 10** (Release Readiness)     | Security gate status report is provided to CSO for release checklist item #4; all P0/P1 findings must be resolved or formally accepted                              |

## Quality Standards

| Metric                   | Standard                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------ |
| **SAST Coverage**        | ≥80% of production code scanned by at least one SAST engine; new code must pass 100% |
| **DAST Coverage**        | ≥95% of API endpoints covered by authenticated DAST scanning                         |
| **Dependency Scanning**  | 100% of direct and transitive dependencies scanned on every change                   |
| **False Positive Rate**  | <5% across all automated scanning tools (measured monthly)                           |
| **Pipeline Performance** | Security scanning adds ≤5 minutes to PR build time; ≤30 minutes for nightly DAST     |
| **Gate Reliability**     | Zero instances of P0/P1 vulnerabilities passing through quality gates                |
| **Remediation SLA**      | P0 findings remediated within 24 hours; P1 within 48 hours; P2 within current sprint |
| **Reporting**            | Weekly security metrics report to CSO; monthly trend analysis to C-suite             |
