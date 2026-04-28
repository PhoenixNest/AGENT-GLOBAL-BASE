---
name: devops-guidelines-cicd-artifact-signing
description: CI/CD artifact signing — cosign keyless signing with Sigstore, OIDC-bound identities, transparency log (Rekor), signature verification, and multi-platform release signing for Android APK and iOS IPA. Owned by Thomas Zhang (DevOps Lead). Use during Stage 5 (Development) for release pipeline setup and Stage 8 (Integrity Verification) for signature validation. Trigger: artifact signing, cosign, Sigstore, keyless signing, Rekor transparency log, OIDC signing, APK signing, IPA signing, release verification.
prerequisites:
  - devops-guidelines-cicd-secrets-mgmt

version: "1.0.0"
---

# CI/CD Artifact Signing

**Category:** DevOps Security — Artifact Integrity
**Owner:** DevOps Engineer — Yuki Matsuda

## Overview

Implement cryptographic signing of build artifacts within CI/CD using cosign/Sigstore. Covers keyless signing with OIDC identity binding, transparency log entries (Rekor), signature verification workflows, and multi-platform release signing for Android APK and iOS IPA.

## Competency Dimensions

| Dimension        | Description                                   | Proficiency Indicators                                                                                  |
| ---------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Artifact Signing | Cryptographic signing of build artifacts      | All release artifacts signed with cosign; keyless signing with OIDC; signatures verifiable by any party |
| Transparency Log | Sigstore Rekor integration for auditability   | Every signature uploaded to Rekor; transparency log entries verifiable; tamper-evident signing history  |
| Verification     | Signature verification in deployment pipeline | Deployment blocked if signature invalid or missing; certificate identity and OIDC issuer verified       |
| Multi-Platform   | Signing for Android APK and iOS IPA           | Both platforms signed within pipeline; iOS uses Apple code signing + additional cosign signature        |

## Execution Guidance

### 1. Cosign Keyless Signing Pipeline

```yaml
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
      - name: Sign APK with Cosign
        run: |
          cosign sign-blob \
            --oidc-issuer=https://token.actions.githubusercontent.com \
            --output-signature app-release.apk.sig \
            --output-certificate app-release.apk.pem \
            app-release.apk

  verify-signatures:
    needs: [sign-android]
    runs-on: ubuntu-latest
    steps:
      - name: Verify Android Signature
        run: |
          cosign verify-blob \
            --signature app-release.apk.sig \
            --certificate app-release.apk.pem \
            --certificate-identity="https://github.com/our-org/mobile-app/.github/workflows/release-signing.yml@refs/heads/main" \
            --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
            app-release.apk
```

### 2. Verification with Rekor Transparency Log

```bash
cosign verify-blob \
  --signature app-release.apk.sig \
  --certificate app-release.apk.pem \
  --certificate-identity="https://github.com/our-org/mobile-app/.github/workflows/release-signing.yml@refs/heads/main" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com" \
  --rekor-url="https://rekor.sigstore.dev" \
  app-release.apk
```

## Quality Standards

| Metric           | Standard                                                                      |
| ---------------- | ----------------------------------------------------------------------------- |
| Signing Coverage | 100% of release artifacts signed with cosign/Sigstore                         |
| Key Management   | Keyless signing only — no long-lived signing keys in CI/CD                    |
| Verification     | Signatures verified before every deployment; invalid signatures block release |
| Transparency     | All signatures logged to Rekor; entries publicly verifiable                   |

## Related Skills

- `devops-guidelines-cicd-secrets-mgmt` — Vault-based secrets management
- `devops-guidelines-cicd-runner-hardening` — Pipeline isolation and runner security
- `devops-guidelines-cicd-gate-enforcement` — Security gate enforcement in CI/CD
