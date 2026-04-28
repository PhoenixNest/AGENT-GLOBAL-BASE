---
name: security-architecture-cicd-supply-chain
description: CI/CD supply chain security — SLSA provenance generation, signed commits with GPG/Sigstore, SBOM generation (CycloneDX + SPDX), dependency allowlisting, and supply chain verification for mobile build pipelines. Owned by Yuki Matsuda (Security Engineer). Use during Stage 4 (Implementation Plan) for supply chain architecture and Stage 8 (Integrity Verification) for provenance validation. Trigger: SLSA provenance, supply chain attestation, signed commits, GPG signing, SBOM generation, CycloneDX, SPDX, dependency allowlisting, supply chain verification.
prerequisites:
  - security-architecture-cicd-secrets-scan

version: "1.0.0"
---

# CI/CD Supply Chain Security

**Category:** DevOps Security — Supply Chain
**Owner:** Security Engineer — Yuki Matsuda

## Overview

Implement supply chain security for mobile CI/CD pipelines. Covers SLSA provenance generation, signed commits, SBOM generation (CycloneDX + SPDX), dependency allowlisting, and supply chain verification at each pipeline stage.

## Competency Dimensions

| Dimension               | Description                                      | Proficiency Indicators                                                                                         |
| ----------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| SLSA Provenance         | Generating build provenance per SLSA framework   | SLSA Level 3 provenance generated for every build; provenance verifiable by any party; stored with artifacts   |
| Signed Commits          | GPG/Sigstore signing of all source code commits  | 100% of commits signed; branch protection requires signed commits; unsigned commits blocked by CI              |
| SBOM Generation         | Software Bill of Materials for every build       | CycloneDX + SPDX SBOMs generated; SBOMs scanned for vulnerabilities; SBOMs signed and archived                 |
| Dependency Allowlisting | Verifying all dependencies against approved list | All dependencies verified against allowlist; unauthorized dependencies block build; allowlist reviewed monthly |

## Execution Guidance

### 1. SLSA Provenance Generation

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

      - name: Generate SLSA Provenance
        uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v1.9.0
        with:
          compile-generator: true
          upload-assets: true
```

### 2. SBOM Generation (CycloneDX + SPDX)

```yaml
- name: Generate CycloneDX SBOM
  run: |
    ./gradlew :app:cyclonedxBom
    # Output: app/build/reports/bom.json

- name: Generate SPDX SBOM
  uses: CycloneDX/gh-node-module-generatebom@v1
  with:
    path: ./app
    output: sbom-spdx.json
```

### 3. Signed Commit Enforcement

```yaml
# GitHub branch protection rule
branch_protection:
  require_signed_commits: true
  # All commits to main must be GPG or Sigstore signed
```

## Quality Standards

| Metric                  | Standard                                                            |
| ----------------------- | ------------------------------------------------------------------- |
| SLSA Level              | Level 3 provenance for all release builds                           |
| Commit Signing          | 100% of commits to main branch signed                               |
| SBOM Coverage           | SBOM generated for every build; covers all direct + transitive deps |
| Dependency Verification | All dependencies verified against allowlist before build            |

## Related Skills

- `security-architecture-cicd-secrets-scan` — Secrets scanning and detection
- `security-architecture-cicd-pipeline-access` — Pipeline access control and RBAC
