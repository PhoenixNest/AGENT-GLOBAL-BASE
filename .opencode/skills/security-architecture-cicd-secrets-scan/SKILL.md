---
name: security-architecture-cicd-secrets-scan
description: CI/CD secrets scanning — git-secrets, truffleHog, pre-commit hooks, secret detection patterns, and automated secret leak prevention for mobile codebases. Owned by Yuki Matsuda (Security Engineer). Use during Stage 4 (Implementation Plan) for secrets scanning strategy and Stage 5 (Development) for pre-commit hook deployment. Trigger: secrets scanning, git-secrets, truffleHog, pre-commit hooks, secret detection, secret leak prevention, credential scanning, git history scan.
prerequisites:
  - security-overview

version: "1.0.0"
---

# CI/CD Secrets Scanning

**Category:** DevOps Security — Secret Detection
**Owner:** Security Engineer — Yuki Matsuda

## Overview

Implement automated secrets scanning across repositories and CI/CD pipelines. Covers git-secrets, truffleHog, pre-commit hooks, secret detection patterns, and automated remediation workflows for leaked credentials.

## Competency Dimensions

| Dimension         | Description                                         | Proficiency Indicators                                                                                      |
| ----------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Secrets Scanning  | Detecting hardcoded secrets in code and git history | git-secrets and truffleHog configured; pre-commit hooks block secret commits; <1% false positive rate       |
| Pattern Detection | Custom regex and entropy-based detection rules      | Detects API keys, tokens, passwords, certificates, private keys; patterns tuned per language/framework      |
| Pre-commit Hooks  | Blocking secret commits before they reach remote    | Pre-commit hooks installed on all developer machines; CI double-checks; bypass requires security approval   |
| Remediation       | Automated response to detected secret leaks         | Detected secrets trigger immediate rotation; affected commits identified; developers notified automatically |

## Execution Guidance

### 1. Pre-Commit Hook Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
        args: ["--verbose", "--redact"]

  - repo: https://github.com/trufflesecurity/trufflehog
    rev: v3.55.0
    hooks:
      - id: trufflehog
        args: ["--no-update", "--only-verified"]
```

### 2. CI Secrets Scan

```yaml
jobs:
  secrets-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
        with:
          fetch-depth: 0 # Full history for git scan

      - name: Run TruffleHog
        run: |
          docker run --rm -v "$(pwd):/workdir" trufflesecurity/trufflehog:latest \
            git file:///workdir --only-verified --fail --json > trufflehog-results.json

      - name: Evaluate Gate
        run: |
          FINDINGS=$(jq 'length' trufflehog-results.json)
          [ "$FINDINGS" -gt 0 ] && { echo "❌ Secrets detected: $FINDINGS findings"; exit 1; }
          echo "✅ No secrets detected"
```

### 3. Git History Scan

```bash
# Scan entire git history for leaked secrets
trufflehog git https://github.com/org/repo --only-verified --json > history-scan.json
# Rotate any confirmed secrets immediately
```

## Quality Standards

| Metric              | Standard                                                    |
| ------------------- | ----------------------------------------------------------- |
| Scan Coverage       | 100% of commits scanned; full git history audited quarterly |
| False Positive Rate | <1% for verified secret detection                           |
| Hook Enforcement    | Pre-commit hooks on all developer machines; CI double-check |
| Remediation SLA     | Confirmed secrets rotated within 1 hour of detection        |

## Related Skills

- `security-architecture-cicd-supply-chain` — SLSA attestation and supply chain security
- `security-architecture-cicd-pipeline-access` — Pipeline access control and RBAC
