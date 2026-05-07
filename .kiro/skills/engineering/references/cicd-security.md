---
name: cicd-security
description: Harden CI/CD pipelines against supply-chain attacks and secrets exposure — implementing OIDC-based cloud auth, secret scanning, dependency audits, and signed artifact provenance — meeting SLSA Level 2 requirements for all company release pipelines.
version: "1.0.0"
---

# CICD Security

| Competency          | Description                                                        | Quality Criteria                                                                                                         |
| ------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| OIDC Cloud Auth     | Replace long-lived IAM credentials with GitHub Actions OIDC tokens | Zero long-lived AWS credentials in GitHub Secrets; all AWS interactions use `aws-actions/configure-aws-credentials` OIDC |
| Secret Scanning     | Scan repositories and CI logs for accidentally committed secrets   | `gitleaks` or `truffleHog` runs in pre-commit and CI; PR merge blocked if secrets detected                               |
| Dependency Auditing | Audit third-party dependencies for known CVEs in every CI run      | `npm audit`, `gradle dependencyCheckAnalyze`, or `trivy` runs on every PR; Critical CVEs block merge                     |
| Artifact Provenance | Sign and verify build artifacts with SLSA provenance attestation   | Docker images signed with Cosign; SBOM generated per build; provenance attestation stored in registry                    |

## Execution Guidance

### OIDC Setup for AWS (GitHub Actions)

```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::ACCOUNT:role/GitHubActionsRole
      aws-region: ap-southeast-1
```

The IAM role trust policy must restrict to the specific repository and branch:

```json
{
  "Condition": {
    "StringEquals": {
      "token.actions.githubusercontent.com:sub": "repo:org/repo:ref:refs/heads/main"
    }
  }
}
```

### SLSA Level 2 Checklist

- [ ] Build runs on hosted CI (not self-hosted runners without hardening)
- [ ] Source code version included in build provenance
- [ ] Build script (`Makefile`/`build.gradle`) is not modifiable during build
- [ ] Artifact hash (SHA-256) recorded and verifiable post-build
