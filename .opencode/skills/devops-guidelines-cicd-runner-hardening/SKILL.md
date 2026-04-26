---
name: devops-guidelines-cicd-runner-hardening
description: CI/CD pipeline hardening — ephemeral runners, OPA/Conftest policy enforcement, action pinning to SHA, minimal permissions, branch protection, and self-hosted runner isolation for mobile build pipelines. Owned by Thomas Zhang (DevOps Lead). Use during Stage 4 (Implementation Plan) for pipeline security design and Stage 6 (Code Review) for policy compliance audit. Trigger: CI/CD pipeline hardening, ephemeral runners, OPA Conftest, action pinning, minimal permissions, branch protection, self-hosted runner security, runner isolation.
prerequisites:
  - devops-guidelines-cicd-secrets-mgmt

version: "1.0.0"
---

# CI/CD Pipeline Hardening

**Category:** DevOps Security — Pipeline Hardening
**Owner:** DevOps Engineer — Yuki Matsuda

## Overview

Harden CI/CD pipelines against tampering and unauthorized access. Covers ephemeral runner configuration, OPA/Conftest policy enforcement, GitHub Actions security hardening, self-hosted runner isolation, and network/filesystem restrictions.

## Competency Dimensions

| Dimension          | Description                                                  | Proficiency Indicators                                                                                       |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Pipeline Hardening | Protecting CI/CD from tampering and unauthorized access      | Pipelines run in isolated ephemeral environments; all changes require code review; zero compromise incidents |
| Action Pinning     | All third-party actions pinned to commit SHA                 | 100% actions pinned; automated PR check blocks unpinned actions; approved actions registry maintained        |
| Runner Isolation   | Self-hosted runners with network and filesystem restrictions | Runners destroyed after each job; iptables restrict outbound; no cross-job data persistence                  |
| Policy Enforcement | OPA/Conftest policies validate pipeline configs              | Policies deny unpinned actions, broad permissions, unmasked secrets; policies run in PR check                |

## Execution Guidance

### 1. GitHub Actions Security Hardening Checklist

| Control                    | Implementation                                   | Verification                         |
| -------------------------- | ------------------------------------------------ | ------------------------------------ |
| **Action pinning**         | All actions pinned to commit SHA                 | Automated check in PR workflow       |
| **Minimal permissions**    | `permissions:` block with least privilege        | Code review + automated policy check |
| **Environment protection** | Production environment with approval gates       | GitHub environment settings          |
| **Ephemeral runners**      | Self-hosted runners destroyed after each job     | Runner lifecycle monitoring          |
| **No secrets in logs**     | `::add-mask::` for all secrets; log scanning     | Automated log scanning               |
| **Branch protection**      | Main branch requires 2+ approvals, status checks | GitHub branch protection rules       |
| **Fork PR restrictions**   | No secret access from fork PRs                   | GitHub default behavior (verify)     |

### 2. OPA/Conftest Pipeline Policy

```rego
package pipeline
import rego.v1

deny_unpinned_actions contains msg if {
    some workflow in input.workflows
    some job in workflow.jobs
    some step in job.steps
    uses := step.uses
    not re_match("@[a-f0-9]{40}$", uses)
    msg := sprintf("Unpinned action: '%s' — pin to commit SHA", [uses])
}

deny_broad_permissions contains msg if {
    some workflow in input.workflows
    workflow.permissions == "write-all"
    msg := sprintf("Workflow uses 'write-all' — use least privilege", [workflow.name])
}
```

### 3. Self-Hosted Runner Hardening

```bash
#!/bin/bash
set -euo pipefail
# 1. Isolated runner user
useradd --system --shell /usr/sbin/nologin --home /opt/actions-runner gh-runner
# 2. Ephemeral runner
echo -e "EPHEMERAL=true\nRUNNER_ALLOW_RUNASROOT=false" > /opt/actions-runner/.env
# 3. Network restrictions (allow only required endpoints)
iptables -A OUTPUT -d api.github.com -j ACCEPT
iptables -A OUTPUT -d vault.company.internal -j ACCEPT
iptables -A OUTPUT -j DROP
# 4. Filesystem restrictions
chmod 700 /opt/actions-runner
chown gh-runner:gh-runner /opt/actions-runner
# 5. Auto cleanup after job
find /opt/actions-runner/_work -mindepth 1 -delete 2>/dev/null
shred -u /tmp/* 2>/dev/null || true
```

## Quality Standards

| Metric             | Standard                                                    |
| ------------------ | ----------------------------------------------------------- |
| Action Pinning     | 100% of CI/CD actions pinned to commit SHA                  |
| Pipeline Isolation | All CI/CD jobs run in ephemeral, isolated environments      |
| Policy Coverage    | All workflows validated by OPA policies before merge        |
| Runner Security    | Self-hosted runners: ephemeral, network-restricted, audited |

## Related Skills

- `devops-guidelines-cicd-secrets-mgmt` — Vault-based secrets management
- `devops-guidelines-cicd-artifact-signing` — Artifact signing with cosign/Sigstore
- `devops-guidelines-cicd-gate-enforcement` — Security gate enforcement in CI/CD
