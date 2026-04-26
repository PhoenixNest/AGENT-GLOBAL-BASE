---
name: security-compliance-supply-chain-security
description: Supply chain security for mobile development — SBOM generation, dependency vulnerability scanning, third-party SDK risk assessment, build provenance verification, and software supply chain attack prevention for mobile app dependencies. Owned by Li Wei Chen (Security Engineer). Use during Stage 3 (UML Engineering) for dependency risk assessment and Stage 6 (Code Review) for supply chain verification. Trigger: supply chain security, SBOM, dependency scanning, SDK risk assessment, build provenance, supply chain attack prevention, mobile dependencies, third-party risk.
prerequisites:
  - security-overview

version: "1.0.0"
---

# Supply Chain Security

**Category:** Software Supply Chain & Build Security
**Owner:** Security Engineer #3 — Li Wei Chen (Supply Chain Security Specialist)

## Overview

Comprehensive methodology for securing the software supply chain from source code through build, signing, and distribution. This skill covers Software Bill of Materials (SBOM) generation using CycloneDX and SPDX standards, artifact signing with cosign and Sigstore, CI/CD pipeline hardening using the SLSA (Supply-chain Levels for Software Artifacts) framework, GitHub Actions marketplace vetting, and dependency verification. For mobile applications, supply chain security is critical — a compromised dependency or tampered build can affect billions of devices. This skill ensures end-to-end integrity of every artifact that ships to users.

## Competency Dimensions

| Dimension                       | Description                                                                      | Proficiency Indicators                                                                                                                                                           |
| ------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SBOM Generation & Management    | Creating and maintaining machine-readable inventories of all software components | Generates CycloneDX and SPDX SBOMs for every build; achieves 100% dependency coverage (direct + transitive); integrates SBOM generation into CI/CD with zero build-time overhead |
| Artifact Signing & Verification | Cryptographic signing of build artifacts using Sigstore/cosign                   | Signs all release artifacts (APK, AAB, IPA) with cosign; implements Sigstore keyless signing with OIDC; verifies signatures in distribution pipeline                             |
| SLSA Framework Implementation   | Implementing supply chain security levels per SLSA specification                 | Achieves SLSA Level 3 for all build pipelines; implements provenance generation; enforces hermetic builds; documents SLSA compliance for auditors                                |
| CI/CD Action Vetting            | Evaluating and approving third-party CI/CD actions and plugins                   | Vets all GitHub Actions before use; maintains approved actions registry; pins actions to commit SHA; monitors for action compromise via Dependabot                               |
| Dependency Verification         | Ensuring all dependencies are authentic and untampered                           | Implements dependency lock files; verifies checksums; monitors for typosquatting; implements allowlist-based dependency approval                                                 |
| Build Pipeline Hardening        | Securing the build environment against tampering                                 | Implements isolated build runners; enforces least-privilege access; secures build secrets; implements build reproducibility checks                                               |

## Execution Guidance

### 1. SBOM Generation — CycloneDX & SPDX

**Why Both Formats:** CycloneDX is optimized for security use cases (vulnerability mapping, component analysis), while SPDX is required for license compliance and some regulatory frameworks. Generate both for comprehensive coverage.

**CycloneDX SBOM Generation:**

```bash
# Android — Gradle CycloneDX plugin
# Add to build.gradle:
plugins {
    id 'org.cyclonedx.bom' version '1.10.0'
}

cyclonedxBom {
    includeConfigs = ["releaseRuntimeClasspath"]
    skipConfigs = ["debugRuntimeClasspath", "testRuntimeClasspath"]
    projectType = "application"
    schemaVersion = "1.5"
    destination = file("build/reports")
    outputName = "bom-cyclonedx"
    outputFormat = "all"  // JSON + XML
    includeBomSerialNumber = true
    includeMetadataResolution = true
}

# Generate SBOM
./gradlew :app:bom --configuration releaseRuntimeClasspath

# iOS — using CycloneDX CocoaPods plugin
pod install --repo-update
cyclonedx-cocoapods generate --output bom-cyclonedx.json

# Universal — syft (multi-format SBOM tool)
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
syft platforms/android/code/app/build/outputs/apk/release/app-release.apk \
  -o cyclonedx-json=bom-android-cyclonedx.json \
  -o spdx-json=bom-android-spdx.json
```

**SBOM Content Requirements:**
Every SBOM must include:

- Component name, version, and type (library, framework, application)
- Supplier information (vendor, maintainer)
- Licenses (SPDX license identifier)
- Hashes (SHA-256 minimum)
- External references (purl — Package URL, CPE)
- Dependency graph (parent-child relationships)
- Vulnerability data (linked CVE entries if available)

**SBOM Analysis & Vulnerability Mapping:**

```bash
# Analyze CycloneDX SBOM with grype
grype sbom:bom-cyclonedx.json --fail-on high --output table

# Generate vulnerability report
grype sbom:bom-cyclonedx.json -o json > vulnerability-report.json

# Check against known vulnerabilities
dependency-check --scan bom-cyclonedx.json --format HTML --out dc-report/
```

**SBOM Integration into CI/CD:**

```yaml
# .github/workflows/sbom-generation.yml
name: Security — SBOM Generation
on:
  push:
    branches: [main]
    tags: ["v*"]

jobs:
  generate-sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate Android SBOM
        run: |
          ./gradlew :app:bom
          cp app/build/reports/bom-cyclonedx.json sbom-android-cyclonedx.json
          cp app/build/reports/bom-cyclonedx.xml sbom-android-cyclonedx.xml

      - name: Generate iOS SBOM
        run: |
          brew install cyclonedx/cyclonedx-cli/cyclonedx
          cyclonedx-cocoapods generate --output sbom-ios-cyclonedx.json

      - name: Sign SBOMs
        run: |
          cosign sign-blob --yes \
            --output-signature sbom-android-cyclonedx.json.sig \
            --output-certificate sbom-android-cyclonedx.json.pem \
            sbom-android-cyclonedx.json
          cosign sign-blob --yes \
            --output-signature sbom-ios-cyclonedx.json.sig \
            --output-certificate sbom-ios-cyclonedx.json.pem \
            sbom-ios-cyclonedx.json

      - name: Upload SBOMs
        uses: actions/upload-artifact@v4
        with:
          name: sboms
          path: sbom-*

      - name: Vulnerability Scan
        uses: anchore/scan-action@v3
        with:
          sbom: sbom-android-cyclonedx.json
          fail-build: true
          severity-cutoff: high
```

### 2. Artifact Signing — cosign & Sigstore

**Keyless Signing with Sigstore (Recommended):**

Sigstore's keyless signing uses short-lived certificates bound to OIDC identities, eliminating the need for long-lived signing keys. This is the preferred approach for all release artifacts.

```bash
# Install cosign
brew install sigstore/tap/cosign

# Sign Android APK
cosign sign-blob \
  --output-signature app-release.apk.sig \
  --output-certificate app-release.apk.pem \
  app-release.apk

# Sign with OIDC identity (keyless — recommended for CI/CD)
cosign sign-blob \
  --oidc-issuer=https://token.actions.githubusercontent.com \
  --output-signature app-release.apk.sig \
  --output-certificate app-release.apk.pem \
  app-release.apk

# Verify signature
cosign verify-blob \
  --signature app-release.apk.sig \
  --certificate app-release.apk.pem \
  --certificate-identity=https://github.com/our-org/our-repo/.github/workflows/release.yml@refs/heads/main \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  app-release.apk
```

**Container Image Signing (for backend services):**

```bash
# Sign container image
cosign sign --yes \
  ghcr.io/our-org/mobile-api-backend:v1.2.3

# Verify container image
cosign verify \
  --certificate-identity=https://github.com/our-org/api-repo/.github/workflows/build.yml@refs/heads/main \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  ghcr.io/our-org/mobile-api-backend:v1.2.3
```

**Android App Signing (Standard + Transparency):**

```bash
# Standard APK signing (apksigner)
apksigner sign \
  --ks release-keystore.jks \
  --ks-key-alias release-key \
  --out app-release-signed.apk \
  app-release-unsigned.apk

# Verify APK signature
apksigner verify --verbose app-release-signed.apk

# Additional cosign signature for transparency log
cosign sign-blob \
  --oidc-issuer=https://token.actions.githubusercontent.com \
  --output-signature app-release-signed.apk.cosign.sig \
  app-release-signed.apk
```

**iOS App Signing:**

iOS uses Apple's code signing infrastructure. Ensure:

- Distribution certificates are stored in secure keychain (not committed to repo)
- Provisioning profiles are regenerated automatically (CI/CD integration with App Store Connect API)
- `codesign` verification passes before distribution

```bash
# Verify iOS code signature
codesign --verify --verbose=4 MyApp.app

# Check entitlements
codesign --display --entitlements :- MyApp.app

# Verify provisioning profile
security cms -D -i embedded.mobileprovision
```

### 3. SLSA Framework Implementation

**SLSA Level Requirements:**

| Requirement        | SLSA L1            | SLSA L2                  | SLSA L3                    | SLSA L4                  |
| ------------------ | ------------------ | ------------------------ | -------------------------- | ------------------------ |
| **Build Process**  | Scripted build     | Version-controlled build | Hermetic build             | Two-person review        |
| **Provenance**     | Available          | Authenticated            | Non-falsifiable            | Tamper-resistant         |
| **Source**         | Version-controlled | Verified history         | Verified branch protection | Verified hermetic source |
| **Build Platform** | Same service       | Same service             | Isolated build             | Isolated + verified      |

**Target: SLSA Level 3 for all mobile app builds.**

**SLSA L3 Implementation — GitHub Actions:**

```yaml
# .github/workflows/slsa-build.yml
name: Security — SLSA L3 Build
on:
  push:
    tags: ["v*"]

permissions:
  id-token: write # For keyless signing
  contents: read
  actions: read

jobs:
  slsa-build:
    runs-on: ubuntu-latest
    # SLSA L3 requires isolated, ephemeral build environment
    container:
      image: our-registry.example.com/android-build:latest
      options: --network=none # Hermetic build — no network after deps fetched

    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # Pinned to SHA (SLSA requirement)

      # Pre-fetched dependencies (network allowed)
      - name: Fetch Dependencies
        run: |
          ./gradlew dependencies --configuration releaseRuntimeClasspath

      # Build phase (network disabled — hermetic)
      - name: Build APK
        run: |
          ./gradlew :app:assembleRelease

      # Generate SLSA Provenance
      - name: Generate Provenance
        uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v1.10.0
        with:
          upload-assets: true
          artifact-path: app/build/outputs/apk/release/app-release.apk

      # Sign with keyless cosign
      - name: Sign Artifact
        run: |
          cosign sign-blob \
            --oidc-issuer=https://token.actions.githubusercontent.com \
            --output-signature app-release.apk.sig \
            app/build/outputs/apk/release/app-release.apk
```

**SLSA Provenance Verification:**

```bash
# Verify SLSA provenance
slsa-verifier verify-artifact \
  --provenance-path provenance.intoto.jsonl \
  --source-uri github.com/our-org/mobile-app \
  --source-tag v1.2.3 \
  app-release.apk
```

### 4. CI/CD Action Vetting Process

**Every GitHub Action must pass vetting before use:**

**Vetting Checklist:**

1. [ ] **Source verification**: Action source code is publicly auditable
2. [ ] **Author reputation**: Published by trusted organization or individual with verified identity
3. [ ] **Version pinning**: Pinned to specific commit SHA (not `@v2` or `@main`)
4. [ ] **Permission analysis**: Minimum required permissions identified and documented
5. [ ] **Dependency review**: Action's dependencies checked for known vulnerabilities
6. [ ] **Update monitoring**: Dependabot or equivalent configured for action updates
7. [ ] **Alternative assessment**: No safer alternative available

**Approved Actions Registry:**

```yaml
# .github/approved-actions.yml
# Maintained by Li Wei Chen — Supply Chain Security
actions:
  actions/checkout:
    sha: b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.7
    approved-by: li-wei-chen
    approved-date: 2026-03-15
    last-reviewed: 2026-03-15
    permissions: [contents]
    risk-level: low

  actions/upload-artifact:
    sha: 65465776419d6a896ff3000970e7d35117509b68 # v4.3.0
    approved-by: li-wei-chen
    approved-date: 2026-03-15
    last-reviewed: 2026-03-15
    permissions: [actions]
    risk-level: low

  anchore/scan-action:
    sha: 334813936482935266612031e241a33f950c8f08 # v3.3.0
    approved-by: li-wei-chen
    approved-date: 2026-03-20
    last-reviewed: 2026-03-20
    permissions: [security-events, contents]
    risk-level: medium
    notes: Requires security-events permission for SARIF upload
```

**Action Vetting Automation:**

```yaml
# .github/workflows/action-vetting.yml
name: Security — Action Vetting
on:
  pull_request:
    paths: [".github/workflows/**"]

jobs:
  check-approved-actions:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Verify All Actions Are Approved and Pinned
        run: |
          # Extract all action references from workflow files
          grep -rh 'uses:' .github/workflows/ | \
            grep -v '^#' | \
            sed 's/.*uses: //' | \
            while read action; do
              # Check if action is in approved registry
              if ! grep -q "$(echo $action | cut -d@ -f1)" .github/approved-actions.yml; then
                echo "❌ Unapproved action: $action"
                exit 1
              fi
              # Check if action is pinned to SHA
              if echo "$action" | grep -qE '@(main|master|v[0-9]+)$'; then
                echo "❌ Action not pinned to SHA: $action"
                exit 1
              fi
            done
          echo "✅ All actions approved and pinned"
```

### 5. Dependency Verification

**Typosquatting Detection:**

```bash
# Using squaremo/gh-action-dependency-review
# Check for newly added dependencies that resemble existing ones

# Custom typosquatting check
python3 check-typosquatting.py requirements.txt
# Checks against known package names for similarity

# npm audit for typosquatting
npm audit --json | jq '.advisories[] | select(.module_name | test("^[a-z]{1,2}[0-9]+$"))'
```

**Dependency Lock File Enforcement:**

```yaml
# .github/workflows/dependency-lock.yml
name: Security — Dependency Lock Verification
on:
  pull_request:
    paths: ["**/build.gradle", "**/Podfile", "**/pubspec.yaml"]

jobs:
  verify-lock:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Verify Gradle Lock
        run: |
          ./gradlew :app:dependencies --write-locks
          git diff --exit-code -- '**/*.lockfile' || \
            (echo "❌ Dependency lock file out of date" && exit 1)

      - name: Verify Podfile.lock
        run: |
          pod install --repo-update
          git diff --exit-code -- Podfile.lock || \
            (echo "❌ Podfile.lock out of date" && exit 1)
```

**Dependency Allowlist:**

```yaml
# .security/dependency-allowlist.yml
# New dependencies must be added to this list and approved
allowed:
  android:
    - androidx.core:core-ktx:1.12.0
    - com.squareup.retrofit2:retrofit:2.9.0
    - com.squareup.okhttp3:okhttp:4.12.0
    - com.google.crypto.tink:tink-android:1.12.0

  ios:
    - Alamofire: 5.8.1
    - KeychainAccess: 4.2.2
    - CryptoSwift: 1.7.1

  process:
    new-dependency-approval:
      - security-review-required: true
      - sbom-update-required: true
      - approved-by: li-wei-chen
      - sla: 48 hours
```

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                    |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| **Stage 1** (SRD)                    | Defines supply chain security requirements: SBOM mandate, signing requirements, SLSA level targets                             |
| **Stage 4** (Implementation Plan)    | CI/CD pipeline design includes supply chain security controls; action vetting process documented                               |
| **Stage 5** (Development)            | SBOM generated on every build; dependencies monitored continuously; action vetting enforced                                    |
| **Stage 6** (Code Review)            | Supply chain security review: SBOM completeness, signature verification, provenance validation                                 |
| **Stage 8** (Integrity Verification) | Verifies all artifacts are signed and verifiable; validates SLSA provenance; confirms SBOM accuracy                            |
| **Stage 10** (Release Readiness)     | Provides supply chain security sign-off: all artifacts signed, SBOMs generated, provenance verified, SLSA compliance confirmed |

## Quality Standards

| Metric                      | Standard                                                                                             |
| --------------------------- | ---------------------------------------------------------------------------------------------------- |
| **SBOM Coverage**           | 100% of production dependencies (direct + transitive) included in SBOM                               |
| **Artifact Signing**        | 100% of release artifacts signed with cosign/Sigstore; signature verifiable by any party             |
| **SLSA Compliance**         | SLSA Level 3 achieved for all production builds                                                      |
| **Action Vetting**          | 100% of CI/CD actions approved, pinned to SHA, and monitored for updates                             |
| **Dependency Verification** | Zero typosquatting incidents; all dependencies match approved allowlist or have documented exception |
| **Build Hermeticity**       | Build reproducibility verified — identical source produces byte-identical artifacts                  |
| **Provenance**              | Every release artifact has non-falsifiable SLSA provenance attestation                               |
