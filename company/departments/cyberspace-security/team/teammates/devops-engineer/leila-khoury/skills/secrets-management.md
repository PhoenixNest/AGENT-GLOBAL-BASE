---
version: "1.0.0"
---

----------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| HashiCorp Vault Architecture | Designing and operating Vault clusters for production workloads | Deploys Vault in HA mode with auto-unseal; achieves 99.99% uptime; implements disaster recovery replication; manages Raft storage backend |
| Dynamic Credentials | Configuring Vault to generate short-lived, on-demand credentials | Dynamic credentials for 100% of database and cloud service access; credentials expire within 1 hour; zero static credentials in production |
| Secret Rotation | Automated rotation of all managed secrets | 100% of secrets rotated on defined schedule (≤90 days for static, ≤1 hour for dynamic); rotation failures alert within 5 minutes |
| Access Policies | Fine-grained ACL and RBAC policies for secret access | Every secret access governed by least-privilege policy; policies version-controlled; access reviewed quarterly |
| Audit Logging | Comprehensive, tamper-proof audit trail for all Vault operations | 100% of Vault operations logged (auth, access, policy changes); logs shipped to SIEM; log integrity verified |
| Kubernetes Secrets Management | Integrating Vault with Kubernetes for pod-level secret injection | Vault Agent Injector deployed; secrets injected as environment variables or volumes; no Kubernetes Secrets for sensitive data |
| CI/CD Integration | Securely providing secrets to CI/CD pipelines | CI/CD pipelines authenticate via OIDC (no static tokens); secrets scoped to specific workflows; secret access logged and monitored |

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                                  |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 3** (Architecture)           | Secrets management architecture designed; Vault integration points identified; dynamic credential strategy defined                           |
| **Stage 4** (Implementation Plan)    | Vault deployment plan included; secret rotation schedule defined; CI/CD integration approach documented                                      |
| **Stage 5** (Development)            | Vault operational; all application secrets managed via Vault; dynamic credentials for database access; CI/CD pipelines authenticate via OIDC |
| **Stage 6** (Code Review)            | Secrets management reviewed; no hardcoded secrets in codebase; Vault access policies verified                                                |
| **Stage 8** (Integrity Verification) | Vault audit logs reviewed; secret rotation verified; all credentials confirmed as dynamic or properly rotated                                |
| **Stage 10** (Release Readiness)     | Secrets management posture confirmed; zero static secrets in production; audit trail complete                                                |

## Quality Standards

| Metric                     | Standard                                                                                               |
| -------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Secret Coverage**        | 100% of production secrets managed via Vault; zero hardcoded secrets in codebase or configurations     |
| **Dynamic Credentials**    | 100% of database and cloud service credentials are dynamic; TTL ≤1 hour for database, ≤4 hours for AWS |
| **Secret Rotation**        | 100% of static secrets rotated ≤90 days; 100% of dynamic credentials rotated on TTL expiry             |
| **Access Control**         | Every secret access governed by least-privilege ACL policy; policies reviewed quarterly                |
| **Audit Logging**          | 100% of Vault operations logged; logs shipped to SIEM within 5 minutes; log integrity verified         |
| **Vault Availability**     | 99.99% uptime for Vault cluster; HA with 3 nodes; automated disaster recovery                          |
| **CI/CD Integration**      | 100% of CI/CD pipelines authenticate via OIDC; no static tokens for Vault access                       |
| **Kubernetes Integration** | 100% of Kubernetes secrets injected via Vault Agent; no Kubernetes Secret objects for sensitive data   |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
