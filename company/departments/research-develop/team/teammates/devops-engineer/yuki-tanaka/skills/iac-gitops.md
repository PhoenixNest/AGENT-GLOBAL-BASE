---
name: iac-gitops
description: Apply GitOps principles to Infrastructure as Code — enforcing that all infrastructure changes flow through git PRs with automated plan review, no manual console changes, and environment promotion gated on CI validation.
version: "1.0.0"
---

# IAC Gitops

| Competency            | Description                                                            | Quality Criteria                                                                                        |
| --------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Terraform GitOps      | All Terraform changes via PRs with automated plan in CI                | `terraform plan` output posted to every PR; no `terraform apply` from local machines in production      |
| Environment Promotion | Promote infra changes staging → production via git branch/tag strategy | Staging applies on merge to `main`; production applies on version tag; no hotfix applies without a PR   |
| Drift Detection       | Detect and alert when infrastructure drifts from the Terraform state   | `terraform plan` scheduled nightly; drift detected → alert in Slack + create GitHub Issue automatically |
| State Management      | Manage Terraform remote state with locking and versioning              | State in S3 with DynamoDB locking; state files separated per environment; no local state in production  |

## Execution Guidance

### GitOps Workflow

```
feature branch → PR → terraform plan (CI) → review → merge to main
                                                          ↓
                                                   staging apply (auto)
                                                          ↓
                                                   version tag (manual)
                                                          ↓
                                                  production apply (auto)
```

### PR Checklist for Infrastructure Changes

- [ ] `terraform fmt` applied (enforced by CI)
- [ ] `terraform validate` passes
- [ ] `terraform plan` output reviewed — no unexpected deletions
- [ ] `tfsec` / `checkov` security scan passes
- [ ] Estimated cost delta reviewed (Infracost comment on PR)
- [ ] Change communicated to affected team leads before merge to main
