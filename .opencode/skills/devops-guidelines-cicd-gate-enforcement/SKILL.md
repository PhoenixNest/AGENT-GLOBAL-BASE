---
name: devops-guidelines-cicd-gate-enforcement
description: CI/CD security gate enforcement — multi-stage deployment gates for SAST, DAST, dependency scanning, SBOM, and artifact signing with automated pass/fail evaluation and escalation. Owned by Thomas Zhang (DevOps Lead). Use during Stage 4 (Implementation Plan) for gate design and Stage 6 (Code Review) for gate effectiveness validation. Trigger: security gate enforcement, deployment gate, SAST gate, DAST gate, dependency gate, SBOM gate, signing gate, quality gate, gate evaluation.
prerequisites:
  - devops-guidelines-cicd-runner-hardening

version: "1.0.0"
---

# CI/CD Security Gate Enforcement

**Category:** DevOps Security — Gate Enforcement
**Owner:** DevOps Engineer — Yuki Matsuda

## Overview

Implement automated security gates that block unsafe deployments. Covers multi-stage gate evaluation (SAST, DAST, dependency scanning, SBOM, artifact signing), pass/fail criteria, escalation paths, and gate reliability monitoring.

## Competency Dimensions

| Dimension        | Description                                      | Proficiency Indicators                                                                                       |
| ---------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Gate Design      | Defining pass/fail criteria for security checks  | Gates block P0/P1 vulnerabilities; P2/P3 allowed with documented exceptions; criteria map to defect severity |
| Gate Enforcement | Automated evaluation blocking unsafe deployments | All 5 gates (SAST, DAST, Dependency, SBOM, Signing) must pass; zero gate bypasses in production              |
| Escalation       | Notification and escalation on gate failures     | P0/P1 failures notify CTO + CSO immediately; gate failure details provided with remediation guidance         |
| Gate Reliability | Ensuring gates cannot be circumvented            | Zero instances of security gate bypass; gate logic version-controlled; gate changes require security review  |

## Execution Guidance

### 1. Multi-Stage Security Gate

```yaml
jobs:
  security-gate:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      # Gate 1: SAST Results
      - name: Check SAST Gate
        run: |
          ERRORS=$(jq '[.results[] | select(.extra.severity == "ERROR")] | length' semgrep-results.json)
          [ "$ERRORS" -gt 0 ] && { echo "❌ Gate 1 FAILED: $ERRORS SAST errors"; exit 1; }
          echo "✅ Gate 1 PASSED: SAST clean"

      # Gate 2: Dependency Scan
      - name: Check Dependency Gate
        run: |
          CRITICAL=$(jq '[.vulnerabilities[] | select(.severity == "critical")] | length' snyk-results.json)
          [ "$CRITICAL" -gt 0 ] && { echo "❌ Gate 2 FAILED: $CRITICAL critical vulns"; exit 1; }
          echo "✅ Gate 2 PASSED: No critical dependency vulnerabilities"

      # Gate 3: SBOM Generated
      - name: Check SBOM Gate
        run: |
          [ -f bom-cyclonedx.json ] && echo "✅ Gate 3 PASSED: SBOM generated" || { echo "❌ Gate 3 FAILED"; exit 1; }

      # Gate 4: Artifact Signed
      - name: Check Signing Gate
        run: |
          [ -f "*.sig" ] && [ -f "*.pem" ] && echo "✅ Gate 4 PASSED: Artifact signed" || { echo "❌ Gate 4 FAILED"; exit 1; }

      # Gate 5: DAST Results
      - name: Check DAST Gate
        run: |
          HIGH=$(jq '.alertCounts.risk["High"] // 0' zap-summary.json)
          [ "$HIGH" -gt 0 ] && { echo "❌ Gate 5 FAILED: $HIGH high-risk DAST alerts"; exit 1; }
          echo "✅ Gate 5 PASSED: No high-risk DAST alerts"
```

### 2. Gate Logic by Severity

| Severity      | Gate Action             | SLA                    | Escalation           |
| ------------- | ----------------------- | ---------------------- | -------------------- |
| P0 (Critical) | Block merge/release     | Immediate fix required | Notifies CTO + CSO   |
| P1 (High)     | Block merge/release     | Fix within 24 hours    | Notifies team lead   |
| P2 (Medium)   | Advisory (non-blocking) | Fix within sprint      | Weekly report to CSO |
| P3 (Low)      | Advisory (non-blocking) | Fix when convenient    | Monthly trend report |

## Quality Standards

| Metric           | Standard                                                     |
| ---------------- | ------------------------------------------------------------ |
| Gate Coverage    | All 5 gates (SAST, DAST, Dependency, SBOM, Signing) enforced |
| Gate Reliability | Zero instances of security gate bypass in production         |
| Gate Performance | Gate evaluation adds ≤2 minutes to pipeline                  |
| Escalation       | P0/P1 failures notify CTO + CSO within 5 minutes             |

## Related Skills

- `devops-guidelines-cicd-secrets-mgmt` — Vault-based secrets management
- `devops-guidelines-cicd-runner-hardening` — Pipeline isolation and runner security
- `devops-guidelines-cicd-artifact-signing` — Artifact signing with cosign/Sigstore
