# Compliance Foundations (SOC 2 Type II + PCI-DSS)

## Module Objectives

After completing this module, the trainee must be able to:

1. Explain the scope and requirements of SOC 2 Type II audits
2. Explain the scope and requirements of PCI-DSS compliance
3. Identify which pipeline security gates map to which compliance controls
4. Prepare evidence and documentation for a compliance audit
5. Understand the difference between operational compliance (SOC 2, PCI-DSS) and product compliance (OWASP MASVS)

## Trainee

| Trainee      | Role        | Deadline | Verification                                                      |
| ------------ | ----------- | -------- | ----------------------------------------------------------------- |
| Thomas Zhang | DevOps Lead | Day 30   | Complete compliance study course + pass written assessment (≥70%) |

## Prerequisites

None required.

## Course Structure

### Session 1: SOC 2 Type II Overview (1.5 hours, led by CSO)

**What is SOC 2?** A Service Organization Control report based on the AICPA Trust Services Criteria. Type II assesses the **operational effectiveness** of controls over a period of time (typically 6–12 months).

**Five Trust Services Criteria:**

| Criteria                 | What It Covers                                               | Pipeline Mapping                                                     |
| ------------------------ | ------------------------------------------------------------ | -------------------------------------------------------------------- |
| **Security**             | Protection against unauthorized access                       | SAST/DAST gates, access controls, MFA, network segmentation          |
| **Availability**         | System uptime and accessibility                              | SLO monitoring, incident response, disaster recovery, load balancing |
| **Processing Integrity** | Data processed completely, validly, accurately               | Input validation, error handling, data reconciliation                |
| **Confidentiality**      | Protection of confidential information                       | Encryption at rest/in transit, access controls, data classification  |
| **Privacy**              | Collection, use, retention, disposal of personal information | Data minimization, consent management, data subject access requests  |

**Key Controls Relevant to DevOps:**

- Change management (all deployments tracked, approved, documented)
- Access control (least privilege, MFA, session management)
- Monitoring and alerting (security events logged, alerts routed to responsible team)
- Backup and recovery (regular backups, tested restoration, documented RTO/RPO)
- Vendor management (third-party risk assessments, dependency scanning)

### Session 2: PCI-DSS Overview (1.5 hours, led by CSO)

**What is PCI-DSS?** Payment Card Industry Data Security Standard — mandatory for any organization that processes, stores, or transmits payment card data.

**12 Requirements:**

| #   | Requirement                                                          | Pipeline Mapping                                             |
| --- | -------------------------------------------------------------------- | ------------------------------------------------------------ |
| 1   | Install and maintain network security controls                       | WAF, network segmentation, firewall rules                    |
| 2   | Apply secure configurations to all system components                 | Hardened base images, IaC scanning (Checkov, tfsec)          |
| 3   | Protect stored account data                                          | Encryption at rest (AES-256), tokenization, key rotation     |
| 4   | Protect cardholder data with strong cryptography during transmission | TLS 1.2+ in transit, certificate pinning                     |
| 5   | Protect all systems from malware                                     | Endpoint protection, container scanning (Trivy)              |
| 6   | Develop and maintain secure systems and software                     | SAST/DAST, code review, patch management                     |
| 7   | Restrict access to cardholder data                                   | RBAC, least privilege, access reviews                        |
| 8   | Identify users and authenticate access to system components          | MFA, unique user IDs, session management                     |
| 9   | Restrict physical access to cardholder data                          | N/A for cloud infrastructure (AWS handles physical)          |
| 10  | Log and monitor all access to system components and cardholder data  | SIEM, audit logging, log retention                           |
| 11  | Test security of systems and processes regularly                     | Penetration testing, vulnerability scanning, DAST            |
| 12  | Maintain information security policy                                 | Security policies, incident response plans, training records |

### Session 3: Compliance-to-Pipeline Mapping (1 hour, led by CSO)

**Exercise:** Map each existing CI/CD security gate to its corresponding compliance control(s):

| Pipeline Gate              | SOC 2 Criteria          | PCI-DSS Requirement          |
| -------------------------- | ----------------------- | ---------------------------- |
| SAST (Semgrep)             | Security (CC6.1)        | Req 6 (secure systems)       |
| DAST (OWASP ZAP)           | Security (CC6.1, CC7.1) | Req 6, Req 11 (testing)      |
| Container Scanning (Trivy) | Security (CC6.1)        | Req 5 (malware protection)   |
| Dependency Scanning        | Security (CC6.1, CC8.1) | Req 6 (patch management)     |
| IaC Scanning (Checkov)     | Security (CC6.1)        | Req 2 (secure configs)       |
| SBOM Generation            | Security (CC6.1)        | Req 6 (inventory management) |
| Access Control Audit       | Security (CC6.1, CC6.6) | Req 7, 8 (access control)    |

### Session 4: Self-Directed Study (2 hours, trainee works independently)

Trainee studies:

- SOC 2 Type II audit process (what auditors look for, common findings, preparation checklist)
- PCI-DSS Self-Assessment Questionnaire (SAQ) types and applicability
- Company's existing compliance documentation (Security Coordination Charter, RACI matrices)

### Session 5: Written Assessment (1 hour, led by CSO)

**Format:** 10 short-answer questions covering SOC 2, PCI-DSS, and pipeline mapping.

**Sample Questions:**

1. What are the five Trust Services Criteria in SOC 2?
2. Which PCI-DSS requirement maps to our container scanning (Trivy) pipeline gate?
3. Explain the difference between SOC 2 Type I and Type II.
4. A new microservice processes payment card data. What PCI-DSS requirements apply?
5. Which pipeline gates provide evidence for SOC 2 Security criteria?

## Verification Method

**Deliverable:** Written assessment with 10 questions

## Pass/Fail Criteria

**PASS:** ≥7 of 10 questions answered correctly (≥70%).

**FAIL:** <7 of 10. One revision cycle allowed (re-study incorrect topics, re-take assessment with different questions). Second failure = position reopened for recruitment.

**Deadline:** Day 30 of probationary period. No extensions.

## Resources

- SOC 2 Trust Services Criteria: https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report
- PCI-DSS Quick Reference Guide: https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Quick%20Reference%20Guide/2024/PCI-DSS-v4_0_Quick-Reference-Guide.pdf
- Company Security Coordination Charter: `company/departments/human-resources/recruitment-plans/engineering-fy2026-q2/security-coordination-charter/README.md`
