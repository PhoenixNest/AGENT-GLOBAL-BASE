---
name: devops-guidelines-cicd-secrets-mgmt
description: CI/CD secrets management — HashiCorp Vault integration with OIDC auth, dynamic credentials, secret rotation, and zero-hardcoded-secrets enforcement for mobile build pipelines. Owned by Thomas Zhang (DevOps Lead). Use during Stage 4 (Implementation Plan) for secrets architecture and Stage 5 (Development) for Vault integration. Trigger: CI/CD secrets management, HashiCorp Vault, OIDC auth, dynamic credentials, secret rotation, zero hardcoded secrets, vault policy, JWT auth.
prerequisites:
  - devops-guidelines-ci-cd-optimization

version: "1.0.0"
---

# CI/CD Secrets Management

**Category:** DevOps Security — Secrets Management
**Owner:** DevOps Engineer — Yuki Matsuda

## Overview

Implement secure secrets management for CI/CD pipelines using HashiCorp Vault with OIDC authentication. Covers dynamic short-lived credentials, secret injection at runtime only, audit logging, and automatic rotation. Zero hardcoded secrets in any repository or pipeline configuration.

## Competency Dimensions

| Dimension          | Description                                            | Proficiency Indicators                                                                                     |
| ------------------ | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| Secrets Management | Secure handling of credentials, API keys, signing keys | Zero hardcoded secrets; all secrets via Vault with automatic rotation; audit trail for every secret access |
| OIDC Auth          | JWT-based authentication from CI/CD to Vault           | No static Vault credentials; GitHub Actions OIDC tokens bound to repo/branch; TTL ≤5 minutes               |
| Secret Rotation    | Automated credential rotation on defined schedule      | All CI/CD secrets rotated ≤90 days; rotation transparent to pipeline; zero downtime during rotation        |
| Audit Logging      | Tamper-proof logging of all secret access events       | Every secret read logged with identity, timestamp, and purpose; logs immutable and monitored for anomalies |

## Execution Guidance

### 1. Vault OIDC Integration with GitHub Actions

```yaml
# .github/workflows/build-and-sign.yml
permissions:
  id-token: write
  contents: read
  actions: read

jobs:
  build:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

      - name: Authenticate to Vault
        uses: hashicorp/vault-action@v2.8.0
        with:
          url: https://vault.company.internal
          method: jwt
          role: github-ci-mobile-app
          jwtGithubAudience: https://vault.company.internal
          exportToken: true
          secrets: |
            secret/data/mobile/android signing-keystore-password | KEYSTORE_PASSWORD ;
            secret/data/mobile/android signing-key-alias | KEYSTORE_ALIAS ;
            secret/data/mobile/android signing-key-password | KEY_PASSWORD ;

      - name: Build Release APK
        run: |
          ./gradlew :app:assembleRelease \
            -PkeystorePassword="$KEYSTORE_PASSWORD" \
            -PkeyAlias="$KEYSTORE_ALIAS" \
            -PkeyPassword="$KEY_PASSWORD"

      - name: Cleanup Secrets
        if: always()
        run: shred -u release-keystore.jks 2>/dev/null || rm -f release-keystore.jks
```

### 2. Vault Policy (Least Privilege)

```hcl
path "secret/data/mobile/android" {
  capabilities = ["read"]
  allowed_parameters = {
    "fields" = ["signing-keystore-password", "signing-key-alias", "signing-key-password"]
  }
}
path "secret/data/mobile/production/*" {
  capabilities = ["deny"]
}
```

### 3. JWT Auth Role Configuration

```hcl
vault write auth/jwt/role/github-ci-mobile-app \
  role_type="jwt" \
  bound_audiences="https://vault.company.internal" \
  bound_subject="repo:our-org/mobile-app:ref:refs/heads/main" \
  user_claim="repository" \
  ttl="5m" \
  policies="github-ci-mobile-app"
```

## Principles

1. **Never** store secrets in repository files (`.env`, `.properties`, `.plist`)
2. **Never** pass secrets through environment variables visible in logs
3. **Always** use dynamic, short-lived credentials where possible
4. **Always** audit secret access with tamper-proof logging
5. **Always** rotate secrets on a defined schedule

## Pipeline Integration

| Stage                        | Application                                                               |
| ---------------------------- | ------------------------------------------------------------------------- |
| **Stage 4** (Implementation) | Secrets management strategy documented; Vault roles and policies designed |
| **Stage 5** (Development)    | Vault OIDC integration operational; secrets injected at runtime only      |
| **Stage 6** (Code Review)    | Secrets management verified; zero hardcoded secrets in pipeline configs   |
| **Stage 8** (Integrity)      | Secret access audit trail verified; rotation schedule confirmed           |

## Quality Standards

| Metric            | Standard                                             |
| ----------------- | ---------------------------------------------------- |
| Hardcoded Secrets | Zero in any repository or pipeline configuration     |
| Secret TTL        | ≤5 minutes for CI/CD sessions; ≤90 days for rotation |
| Audit Coverage    | 100% of secret access events logged                  |
| Vault Auth        | OIDC only — no static tokens or approles for CI/CD   |

## Related Skills

- `devops-guidelines-cicd-runner-hardening` — Pipeline isolation and runner security
- `devops-guidelines-cicd-artifact-signing` — Artifact signing with cosign/Sigstore
- `devops-guidelines-cicd-gate-enforcement` — Security gate enforcement in CI/CD
