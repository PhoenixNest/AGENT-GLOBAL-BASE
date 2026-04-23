---
name: security-architecture-cicd-security
description: "Security skill: Cicd Security"
---

# CI/CD Pipeline Security

**Category:** DevOps Security — Pipeline Hardening
**Owner:** DevOps Engineer — Yuki Matsuda

## Overview

Design, implement, and maintain secure CI/CD pipelines that protect the software delivery process from source code commit through production deployment. This skill covers secrets management with HashiCorp Vault, pipeline hardening against supply chain attacks, artifact signing and provenance generation, SBOM integration, supply chain verification, and security gate enforcement. The CI/CD pipeline is the most critical infrastructure component in mobile app development — a compromised pipeline can deliver malicious code to billions of devices. This skill ensures the pipeline itself is a trusted, auditable, and defensible component of the security architecture.

## Competency Dimensions

| Dimension                 | Description                                                              | Proficiency Indicators                                                                                                                                       |
| ------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Secrets Management        | Secure handling of credentials, API keys, and signing materials in CI/CD | Zero hardcoded secrets in pipeline configurations; all secrets managed via Vault with automatic rotation; audit trail for every secret access                |
| Pipeline Hardening        | Protecting CI/CD pipelines from tampering and unauthorized access        | Pipelines run in isolated, ephemeral environments; no persistent runner access; all pipeline changes require code review; zero pipeline compromise incidents |
| Artifact Signing          | Cryptographic signing of build artifacts within CI/CD                    | All release artifacts signed within pipeline using cosign/Sigstore; signature verification enforced in deployment pipeline; keyless signing with OIDC        |
| Supply Chain Verification | Verifying integrity of all pipeline inputs and dependencies              | All actions pinned to SHA; dependencies verified against allowlist; SBOM generated and verified at each stage; SLSA provenance generated                     |
| SBOM Integration          | Embedding SBOM generation into the build pipeline                        | SBOM generated for every build (CycloneDX + SPDX); SBOM scanned for vulnerabilities; SBOM signed and archived                                                |
| Security Gate Enforcement | Implementing automated security checks that block unsafe deployments     | Gates enforce: SAST pass, DAST pass, dependency scan pass, SBOM generated, artifact signed; zero instances of gate bypass in production                      |

## Execution Guidance

### 1. Secrets Management in CI/CD

**Principles:**

1. **Never** store secrets in repository files (including `.env`, `.properties`, `.plist`)
2. **Never** pass secrets through environment variables visible in logs
3. **Always** use dynamic, short-lived credentials where possible
4. **Always** audit secret access with tamper-proof logging
5. **Always** rotate secrets on a defined schedule

**GitHub Actions Secrets + Vault Integration:**

```yaml
# .github/workflows/build-and-sign.yml
name: Build & Sign Release
on:
  push:
    tags: ["v*"]

# CRITICAL: Minimal permissions
permissions:
  id-token: write # For OIDC token generation (keyless signing)
  contents: read # For checkout
  actions: read # For artifact access

jobs:
  build:
    runs-on: ubuntu-latest
    environment: production # Environment protection rules apply
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

      # Authenticate to Vault using OIDC (no static credentials)
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
            secret/data/mobile/firebase service-account-key | FIREBASE_SA_KEY ;
            secret/data/mobile/api-staging-key | API_STAGING_KEY ;

      # Retrieve keystore from Vault (stored as base64-encoded secret)
      - name: Retrieve Signing Keystore
        run: |
          echo "$KEYSTORE_B64" | base64 -d > release-keystore.jks
        env:
          KEYSTORE_B64: ${{ steps.vault.outputs.keystore-b64 }}

      # Build with secrets injected at runtime only
      - name: Build Release APK
        run: |
          ./gradlew :app:assembleRelease \
            -PkeystorePassword="$KEYSTORE_PASSWORD" \
            -PkeyAlias="$KEYSTORE_ALIAS" \
            -PkeyPassword="$KEY_PASSWORD"
        env:
          KEYSTORE_PASSWORD: ${{ steps.vault.outputs.keystore-password }}
          KEYSTORE_ALIAS: ${{ steps.vault.outputs.keystore-alias }}
          KEY_PASSWORD: ${{ steps.vault.outputs.key-password }}

      # Sign with cosign (keyless — uses OIDC identity)
      - name: Sign Artifact
        run: |
          cosign sign-blob \
            --oidc-issuer=https://token.actions.githubusercontent.com \
            --output-signature app-release.apk.sig \
            app/build/outputs/apk/release/app-release.apk

      # Cleanup — ensure secrets are removed from runner filesystem
      - name: Cleanup Secrets
        if: always()
        run: |
          shred -u release-keystore.jks 2>/dev/null || rm -f release-keystore.jks
          rm -f app/build/outputs/apk/release/*.sig
```

**Vault Policy for CI/CD:**

```hcl
# vault-policies/github-ci-mobile-app.hcl
# GitHub Actions CI/CD pipeline — least privilege

# Read-only access to mobile app build secrets
path "secret/data/mobile/android" {
  capabilities = ["read"]
  allowed_parameters = {
    "fields" = ["signing-keystore-password", "signing-key-alias", "signing-key-password"]
  }
}

path "secret/data/mobile/firebase" {
  capabilities = ["read"]
  allowed_parameters = {
    "fields" = ["service-account-key"]
  }
}

path "secret/data/mobile/api-keys" {
  capabilities = ["read"]
  allowed_parameters = {
    "fields" = ["staging-key"]
  }
}

# No access to production secrets (separate pipeline role)
path "secret/data/mobile/production/*" {
  capabilities = ["deny"]
}

# Audit logging is automatic — no policy needed
```

**Vault JWT Auth Role Configuration:**

```hcl
# Configure JWT auth for GitHub Actions
vault write auth/jwt/role/github-ci-mobile-app \
  role_type="jwt" \
  bound_audiences="https://vault.company.internal" \
  bound_subject="repo:our-org/mobile-app:ref:refs/heads/main" \
  bound_claims_type="glob" \
  user_claim="repository" \
  ttl="5m" \
  policies="github-ci-mobile-app"
```

### 2. Pipeline Hardening

**GitHub Actions Security Hardening Checklist:**

| Control                    | Implementation                                   | Verification                         |
| -------------------------- | ------------------------------------------------ | ------------------------------------ |
| **Action pinning**         | All actions pinned to commit SHA                 | Automated check in PR workflow       |
| **Minimal permissions**    | `permissions:` block with least privilege        | Code review + automated policy check |
| **Environment protection** | Production environment with approval gates       | GitHub environment settings          |
| **Ephemeral runners**      | Self-hosted runners destroyed after each job     | Runner lifecycle monitoring          |
| **No secrets in logs**     | `::add-mask::` for all secrets; log scanning     | Automated log scanning               |
| **Branch protection**      | Main branch requires 2+ approvals, status checks | GitHub branch protection rules       |
| **Fork PR restrictions**   | No secret access from fork PRs                   | GitHub default behavior (verify)     |
| **Dependency review**      | All pipeline dependencies reviewed and approved  | Approved actions registry            |

**Pipeline Security Policy (OPA/Conftest):**

```rego
# policy/pipeline-security.rego
package pipeline

import rego.v1

# Deny workflows that use unpinned actions
deny_unpinned_actions contains msg if {
    some workflow in input.workflows
    some job in workflow.jobs
    some step in job.steps
    uses := step.uses
    not re_match("@[a-f0-9]{40}$", uses)
    msg := sprintf("Unpinned action in workflow '%s', job '%s': '%s' — pin to commit SHA", [workflow.name, job.name, uses])
}

# Deny workflows with overly broad permissions
deny_broad_permissions contains msg if {
    some workflow in input.workflows
    workflow.permissions == "write-all"
    msg := sprintf("Workflow '%s' uses 'write-all' permissions — use least privilege", [workflow.name])
}

# Deny workflows that expose secrets in environment variables without masking
deny_unmasked_secrets contains msg if {
    some workflow in input.workflows
    some job in workflow.jobs
    some step in job.steps
    some env_name, env_value in step.env
    re_match("(?i)(password|secret|key|token)", env_name)
    not step.run
    msg := sprintf("Potentially unmasked secret in workflow '%s', job '%s': '%s'", [workflow.name, job.name, env_name])
}

# Require environment protection for production deployments
deny_production_without_protection contains msg if {
    some workflow in input.workflows
    some job in workflow.jobs
    job.environment == "production"
    not job.needs
    msg := sprintf("Production deployment in workflow '%s', job '%s' must have dependencies (approval gates)", [workflow.name, job.name])
}
```

**Self-Hosted Runner Hardening:**

```yaml
# runner-setup.sh — Hardened self-hosted runner configuration
#!/bin/bash
set -euo pipefail

# 1. Create isolated runner user
useradd --system --shell /usr/sbin/nologin --home /opt/actions-runner gh-runner

# 2. Configure ephemeral runner (destroyed after each job)
cat > /opt/actions-runner/.env << EOF
EPHEMERAL=true
RUNNER_ALLOW_RUNASROOT=false
EOF

# 3. Network restrictions — runner can only access specific endpoints
iptables -A OUTPUT -d api.github.com -j ACCEPT
iptables -A OUTPUT -d vault.company.internal -j ACCEPT
iptables -A OUTPUT -d artifacts.company.internal -j ACCEPT
iptables -A OUTPUT -d registry.company.internal -j ACCEPT
iptables -A OUTPUT -j DROP

# 4. Filesystem restrictions — no access to other users' data
chmod 700 /opt/actions-runner
chown gh-runner:gh-runner /opt/actions-runner

# 5. Audit logging
auditctl -w /opt/actions-runner/ -p wa -k actions_runner

# 6. Automatic cleanup after job
cat > /opt/actions-runner/cleanup.sh << 'EOF'
#!/bin/bash
# Remove all files created during job execution
find /opt/actions-runner/_work -mindepth 1 -delete 2>/dev/null
# Clear environment variables
env -i bash -c 'unset $(env | cut -d= -f1)'
# Shred any temporary files
shred -u /tmp/* 2>/dev/null || true
EOF
chmod +x /opt/actions-runner/cleanup.sh
```

### 3. Artifact Signing in CI/CD

**Cosign Keyless Signing Pipeline:**

```yaml
# .github/workflows/release-signing.yml
name: Release — Sign & Verify
on:
  push:
    tags: ["v*"]

permissions:
  id-token: write
  contents: read
  packages: write

jobs:
  sign-android:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

      - name: Download APK
        uses: actions/download-artifact@v4
        with:
          name: app-release-apk

      # Keyless signing — identity bound to GitHub Actions workflow
      - name: Sign APK with Cosign
        run: |
          cosign sign-blob \
            --oidc-issuer=https://token.actions.githubusercontent.com \
            --output-signature app-release.apk.sig \
            --output-certificate app-release.apk.pem \
            app-release.apk

      # Upload signed artifact + signature + certificate
      - name: Upload Signed Release
        uses: actions/upload-artifact@v4
        with:
          name: signed-release-android
          path: |
            app-release.apk
            app-release.apk.sig
            app-release.apk.pem

  sign-ios:
    runs-on: macos-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Download IPA
        uses: actions/download-artifact@v4
        with:
          name: app-release-ipa

      # iOS uses Apple's code signing + additional cosign signature
      - name: Sign IPA with Cosign
        run: |
          cosign sign-blob \
            --oidc-issuer=https://token.actions.githubusercontent.com \
            --output-signature app-release.ipa.sig \
            --output-certificate app-release.ipa.pem \
            app-release.ipa

      - name: Upload Signed Release
        uses: actions/upload-artifact@v4
        with:
          name: signed-release-ios
          path: |
            app-release.ipa
            app-release.ipa.sig
            app-release.ipa.pem

  verify-signatures:
    needs: [sign-android, sign-ios]
    runs-on: ubuntu-latest
    steps:
      - name: Download Signed Artifacts
        uses: actions/download-artifact@v4

      - name: Verify Android Signature
        run: |
          cosign verify-blob \
            --signature signed-release-android/app-release.apk.sig \
            --certificate signed-release-android/app-release.apk.pem \
            --certificate-identity="https://github.com/our-org/mobile-app/.github/workflows/release-signing.yml@refs/heads/main" \
            --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
            signed-release-android/app-release.apk

      - name: Verify iOS Signature
        run: |
          cosign verify-blob \
            --signature signed-release-ios/app-release.ipa.sig \
            --certificate signed-release-ios/app-release.ipa.pem \
            --certificate-identity="https://github.com/our-org/mobile-app/.github/workflows/release-signing.yml@refs/heads/main" \
            --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
            signed-release-ios/app-release.ipa

      - name: Upload to Sigstore Rekor (Transparency Log)
        run: |
          # Cosign keyless signing automatically uploads to Rekor
          # Verify the transparency log entry exists
          cosign verify-blob \
            --signature signed-release-android/app-release.apk.sig \
            --certificate signed-release-android/app-release.apk.pem \
            --certificate-identity="https://github.com/our-org/mobile-app/.github/workflows/release-signing.yml@refs/heads/main" \
            --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
            --rekor-url="https://rekor.sigstore.dev" \
            signed-release-android/app-release.apk
```

### 4. Security Gate Enforcement

**Multi-Stage Security Gate:**

```yaml
# .github/workflows/security-gate.yml
name: Security — Deployment Gate
on:
  workflow_call:
    inputs:
      artifact_name:
        required: true
        type: string
      environment:
        required: true
        type: string

jobs:
  security-gate:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Download Artifact
        uses: actions/download-artifact@v4
        with:
          name: ${{ inputs.artifact_name }}

      # Gate 1: SAST Results
      - name: Check SAST Gate
        run: |
          if [ -f semgrep-results.json ]; then
            ERRORS=$(jq '[.results[] | select(.extra.severity == "ERROR")] | length' semgrep-results.json)
            if [ "$ERRORS" -gt 0 ]; then
              echo "❌ Gate 1 FAILED: $ERRORS SAST errors"
              exit 1
            fi
            echo "✅ Gate 1 PASSED: SAST clean"
          else
            echo "⚠️ Gate 1 SKIPPED: No SAST results found"
          fi

      # Gate 2: Dependency Scan Results
      - name: Check Dependency Gate
        run: |
          if [ -f snyk-results.json ]; then
            CRITICAL=$(jq '[.vulnerabilities[] | select(.severity == "critical")] | length' snyk-results.json)
            HIGH=$(jq '[.vulnerabilities[] | select(.severity == "high")] | length' snyk-results.json)
            if [ "$CRITICAL" -gt 0 ]; then
              echo "❌ Gate 2 FAILED: $CRITICAL critical dependency vulnerabilities"
              exit 1
            fi
            echo "✅ Gate 2 PASSED: No critical dependency vulnerabilities"
          else
            echo "⚠️ Gate 2 SKIPPED: No dependency scan results"
          fi

      # Gate 3: SBOM Generated
      - name: Check SBOM Gate
        run: |
          if [ -f bom-cyclonedx.json ]; then
            COMPONENTS=$(jq '.components | length' bom-cyclonedx.json)
            echo "✅ Gate 3 PASSED: SBOM generated with $COMPONENTS components"
          else
            echo "❌ Gate 3 FAILED: SBOM not generated"
            exit 1
          fi

      # Gate 4: Artifact Signed
      - name: Check Signing Gate
        run: |
          if [ -f "*.sig" ] && [ -f "*.pem" ]; then
            echo "✅ Gate 4 PASSED: Artifact signed with cosign"
          else
            echo "❌ Gate 4 FAILED: Artifact not signed"
            exit 1
          fi

      # Gate 5: DAST Results (for API backends)
      - name: Check DAST Gate
        run: |
          if [ -f zap-summary.json ]; then
            HIGH=$(jq '.alertCounts.risk["High"] // 0' zap-summary.json)
            if [ "$HIGH" -gt 0 ]; then
              echo "❌ Gate 5 FAILED: $HIGH high-risk DAST alerts"
              exit 1
            fi
            echo "✅ Gate 5 PASSED: No high-risk DAST alerts"
          else
            echo "⚠️ Gate 5 SKIPPED: No DAST results (pipeline-specific scan not configured)"
          fi

      - name: Gate Summary
        if: success()
        run: |
          echo "🎉 All security gates passed — deployment authorized"
          echo "Environment: ${{ inputs.environment }}"
          echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                         |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 4** (Implementation Plan)    | CI/CD pipeline architecture designed with security controls; secrets management strategy documented; security gate criteria defined |
| **Stage 5** (Development)            | CI/CD pipeline operational with security gates; SAST/DAST/dependency scanning running on every PR; secrets managed via Vault        |
| **Stage 6** (Code Review)            | Pipeline security configuration reviewed; secrets management verified; gate effectiveness validated                                 |
| **Stage 8** (Integrity Verification) | Pipeline provenance verified; artifact signatures validated; SBOM completeness confirmed                                            |
| **Stage 10** (Release Readiness)     | CI/CD security gate results provided to CTO panel; confirms all security checks passed before release                               |

## Quality Standards

| Metric                 | Standard                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| **Secrets Management** | Zero hardcoded secrets in any repository or pipeline configuration                        |
| **Pipeline Isolation** | All CI/CD jobs run in ephemeral, isolated environments                                    |
| **Artifact Signing**   | 100% of release artifacts signed with cosign/Sigstore; signatures verifiable by any party |
| **Security Gates**     | All 5 gates (SAST, DAST, Dependency, SBOM, Signing) must pass before deployment           |
| **Action Pinning**     | 100% of CI/CD actions pinned to commit SHA                                                |
| **Secret Rotation**    | All CI/CD secrets rotated on ≤90-day schedule                                             |
| **Audit Trail**        | 100% of pipeline executions logged with artifact hashes, signatures, and gate results     |
| **Gate Reliability**   | Zero instances of security gate bypass in production                                      |
