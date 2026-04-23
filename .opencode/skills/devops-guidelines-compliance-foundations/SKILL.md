---
name: devops-guidelines-compliance-foundations
description: "Devops skill: Compliance Foundations"
---

# Compliance Foundations

## Overview

This skill covers compliance framework fundamentals, audit readiness processes, and regulatory alignment for engineering organizations. It includes SOC 2 Type II, ISO 27001, GDPR, and PCI DSS compliance preparation, evidence collection automation, and audit lifecycle management. It is used by DevOps leads and compliance analysts during Stage 1 (Requirements) and Stage 8 (Integrity Verification).

## Compliance Framework Overview

| Framework     | Scope                           | Audit Frequency                      | Key Controls                                                           |
| ------------- | ------------------------------- | ------------------------------------ | ---------------------------------------------------------------------- |
| SOC 2 Type II | Service organization controls   | Annual (6-12 month observation)      | Security, Availability, Processing Integrity, Confidentiality, Privacy |
| ISO 27001     | Information security management | Annual (certification every 3 years) | 114 controls across 14 domains                                         |
| GDPR          | EU personal data processing     | Ongoing (DPA enforcement)            | Lawful basis, data minimization, breach notification (72h)             |
| PCI DSS       | Payment card data handling      | Annual (QSA assessment)              | 12 requirements, 4 levels by transaction volume                        |

## Audit Readiness Process

**Continuous evidence collection**:

- Infrastructure: Terraform state files, security group configs, encryption settings.
- Access: IAM policies, MFA enforcement, privileged access reviews (quarterly).
- Change management: PR records, approval workflows, deployment logs.
- Incident response: Incident tickets, postmortems, remediation tracking.

**Automated evidence pipeline**:

```
Infrastructure (Terraform) → Evidence collector → Evidence store → Auditor portal
CloudTrail logs ────────────→
CI/CD pipeline ─────────────→
HR system (access reviews) ─→
```

## Regulatory Alignment

**GDPR compliance engineering**:

- Data mapping: automated discovery of PII in databases and file stores.
- Consent management: explicit opt-in tracking, withdrawal mechanisms.
- Data subject requests: automated data export and deletion pipelines.
- Data retention: automated purging based on defined retention schedules.

## Compliance Monitoring

- Compliance dashboard: real-time status of all control objectives.
- Control failure alerting: immediate notification when a control fails.
- Quarterly self-assessments: internal review before external audit.
