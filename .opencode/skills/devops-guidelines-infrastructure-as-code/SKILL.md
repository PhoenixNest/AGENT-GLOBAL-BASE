---
name: devops-guidelines-infrastructure-as-code
description: Infrastructure as Code for mobile development environments — Terraform modules for CI/CD runners, device farm provisioning, test environment automation, and ephemeral preview environments for mobile app builds. Owned by Thomas Zhang (DevOps Lead). Use during Stage 4 (Implementation Plan) for environment automation design and Stage 5 (Development) for IaC module implementation. Trigger: infrastructure as code, Terraform modules, CI/CD runners, device farm, test environment automation, ephemeral environments, mobile preview environments.
prerequisites:
  - devops-overview

version: "1.0.0"
---

# Infrastructure as Code (IaC) Security

**Category:** DevOps — Infrastructure Architecture & Policy
**Owner:** DevOps Engineer — Yuki Matsuda

## Overview

Design, implement, and maintain secure Infrastructure as Code (IaC) using Terraform, implementing module architecture best practices, state management security, drift detection, policy-as-code with OPA/Sentinel, and GitOps workflows. This skill ensures that all cloud infrastructure supporting mobile applications (API backends, databases, CI/CD runners, monitoring systems) is defined, versioned, reviewed, and deployed through a secure, auditable infrastructure pipeline. Infrastructure security is foundational — no amount of application-level security can compensate for misconfigured cloud infrastructure.

## Competency Dimensions

| Dimension                     | Description                                                                         | Proficiency Indicators                                                                                                                                                           |
| ----------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Terraform Module Architecture | Designing reusable, composable, secure Terraform modules                            | Creates modules with input validation, output documentation, version pinning, and security defaults; modules used across 3+ projects without modification                        |
| State Management              | Secure handling of Terraform state files containing sensitive data                  | State stored in encrypted remote backend with access controls; state file never committed to repository; state locking prevents concurrent modifications                         |
| Drift Detection               | Identifying and remediating configuration drift between IaC and live infrastructure | Automated drift detection runs daily; drift alerts within 1 hour; 100% of drift incidents investigated and remediated within 24 hours                                            |
| Policy-as-Code (OPA/Sentinel) | Enforcing infrastructure security policies through automated checks                 | Writes Sentinel/OPA policies that prevent 100% of common misconfigurations (open S3, unencrypted RDS, public-facing databases); policies tested against known-bad configurations |
| GitOps Workflows              | Managing infrastructure changes through Git-based approval workflows                | All infrastructure changes via PR; requires 2+ approvals; automated plan preview in PR comments; zero manual infrastructure changes                                              |
| IaC Security Scanning         | Automated security analysis of Terraform configurations                             | Integrates tfsec/checkov into CI pipeline; blocks deployment of non-compliant infrastructure; maintains custom rules for company-specific security requirements                  |

## Infrastructure Change Request

### Description

[What is changing and why?]

### Affected Resources

- [ ] VPC/Networking
- [ ] Compute (EC2/ECS/Lambda)
- [ ] Database (RDS/DynamoDB)
- [ ] Storage (S3/EFS)
- [ ] IAM/Roles/Policies
- [ ] CI/CD Pipeline
- [ ] Monitoring/Logging
- [ ] Other: [specify]

### Environment

- [ ] Development
- [ ] Staging
- [ ] Production

### Security Impact

- [ ] New IAM permissions
- [ ] Network changes (security groups, NACLs)
- [ ] Encryption changes
- [ ] Public exposure changes
- [ ] Secrets/credentials changes
- [ ] No security impact

### Terraform Plan Summary

```

# Paste terraform plan output here (resources to add/change/destroy)

```

### Rollback Plan

[How to revert this change if needed?]

### Testing

- [ ] terraform fmt -check passes
- [ ] terraform validate passes
- [ ] tfsec scan passes
- [ ] conftest policy check passes
- [ ] Manual review of plan output

```

## Pipeline Integration

| Pipeline Stage                    | Application                                                                                                                   |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Stage 3** (Architecture)        | Infrastructure architecture designed; Terraform module structure defined; security requirements for infrastructure documented |
| **Stage 4** (Implementation Plan) | IaC implementation plan includes module development, policy-as-code creation, and GitOps workflow setup                       |
| **Stage 5** (Development)         | Infrastructure provisioned via Terraform; drift detection active; policy checks enforced on all changes                       |
| **Stage 6** (Code Review)         | Terraform configuration reviewed for security; policy check results included in review                                        |
| **Stage 10** (Release Readiness)  | Infrastructure security posture confirmed; drift detection current; all policy checks passing                                 |

## Quality Standards

| Metric                 | Standard                                                                                  |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| **IaC Coverage**       | 100% of infrastructure defined in Terraform; no manual infrastructure changes             |
| **Policy Enforcement** | 100% of Terraform changes pass policy checks before merge                                 |
| **State Security**     | Zero state file exposure incidents; state access limited to CI/CD pipeline role           |
| **Drift Detection**    | Drift detected within 6 hours; 100% of drift incidents investigated within 24 hours       |
| **Module Quality**     | All modules pass tfsec with zero critical/high findings; all modules documented           |
| **GitOps Compliance**  | 100% of infrastructure changes via Git PR workflow; zero manual `terraform apply`         |
| **Encryption**         | 100% of storage resources encrypted at rest; 100% of network traffic encrypted in transit |
| **Access Control**     | All infrastructure access via IAM roles; no long-lived access keys                        |


---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
```
