---
name: security-architecture-cicd-pipeline-access
description: CI/CD pipeline access control — RBAC for pipeline runners, environment protection rules, branch protection policies, secure artifact storage, and audit logging for mobile build pipelines. Owned by Yuki Matsuda (Security Engineer). Use during Stage 4 (Implementation Plan) for access control design and Stage 6 (Code Review) for access policy compliance. Trigger: pipeline access control, RBAC CI/CD, environment protection, branch protection, secure artifact storage, pipeline audit logging, runner access management.
prerequisites:
  - security-architecture-cicd-secrets-scan

version: "1.0.0"
---

# CI/CD Pipeline Access Control

**Category:** DevOps Security — Access Control
**Owner:** Security Engineer — Yuki Matsuda

## Overview

Implement access control for CI/CD pipelines covering RBAC for runners, environment protection rules, branch protection policies, secure artifact storage, and comprehensive audit logging.

## Competency Dimensions

| Dimension               | Description                                        | Proficiency Indicators                                                                                          |
| ----------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Pipeline RBAC           | Role-based access control for CI/CD operations     | Runners have minimal permissions; environment-specific access; no runner can access production without approval |
| Environment Protection  | GitHub environment rules with approval gates       | Production deployments require manual approval; environment-scoped secrets; deployment history tracked          |
| Branch Protection       | Branch policies preventing unauthorized changes    | Main branch requires 2+ approvals, status checks, signed commits; force-push disabled                           |
| Secure Artifact Storage | Encrypted storage with access-controlled downloads | Artifacts encrypted at rest; download requires authentication; retention policies enforced                      |

## Execution Guidance

### 1. Environment Protection Rules

```yaml
# GitHub environment configuration
environments:
  production:
    protection_rules:
      required_reviewers: 2
      wait_timer: 0
    variables:
      DEPLOY_TARGET: "production"
    secrets:
      # Scoped to production environment only
      - KEYSTORE_B64
      - FIREBASE_SA_KEY
```

### 2. Branch Protection Policy

```yaml
# Required branch protection rules
branch_protection:
  main:
    required_pull_request_reviews:
      required_approving_review_count: 2
      dismiss_stale_reviews: true
      require_code_owner_reviews: true
    required_status_checks:
      strict: true
      contexts: [security-sast, security-dependencies, unit-tests]
    enforce_admins: true
    restrictions: null
    required_signatures: true
    allow_force_pushes: false
    allow_deletions: false
```

### 3. Artifact Storage Security

```yaml
jobs:
  store-artifact:
    runs-on: ubuntu-latest
    steps:
      - name: Upload Encrypted Artifact
        run: |
          # Encrypt artifact before upload
          openssl enc -aes-256-gcm -salt -pbkdf2 \
            -in app-release.apk -out app-release.apk.enc \
            -pass env:ARTIFACT_KEY
        env:
          ARTIFACT_KEY: ${{ secrets.ARTIFACT_ENCRYPTION_KEY }}

      - uses: actions/upload-artifact@v4
        with:
          name: encrypted-release
          path: app-release.apk.enc
          retention-days: 90
```

## Quality Standards

| Metric                 | Standard                                                                |
| ---------------------- | ----------------------------------------------------------------------- |
| Runner Permissions     | Minimal permissions per job; no runner has write-all access             |
| Environment Protection | Production requires 2+ approvals; secrets scoped to environment         |
| Branch Protection      | Main branch: 2+ approvals, status checks, signed commits, no force-push |
| Artifact Retention     | Release artifacts retained 90 days; encrypted at rest                   |

## Related Skills

- `security-architecture-cicd-secrets-scan` — Secrets scanning and detection
- `security-architecture-cicd-supply-chain` — SLSA attestation and supply chain security
