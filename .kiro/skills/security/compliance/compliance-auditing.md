---
name: compliance-auditing
description: Comprehensive methodology for planning, executing, and managing compliance audits across multiple regulatory frameworks relevant to mobile application development and operation.
---

# Compliance Auditing

**Category:** Regulatory Compliance & Audit Management
**Owner:** Compliance Analyst — Ingrid Solberg

## Overview

Comprehensive methodology for planning, executing, and managing compliance audits across multiple regulatory frameworks relevant to mobile application development and operation. This skill covers SOC 2 Type II, PCI DSS v4.0, GDPR, and ISO 27001 compliance programs, including audit planning, evidence collection automation, control assessment, gap analysis, remediation tracking, and external auditor coordination. The compliance program ensures that all mobile applications and their supporting infrastructure meet regulatory obligations and industry security standards, enabling market access and customer trust.

## Competency Dimensions

| Dimension           | Description                                                                                     | Proficiency Indicators                                                                                                                                                       |
| ------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SOC 2 Type II       | Trust Service Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy) | Designs and maintains SOC 2 control framework; coordinates annual Type II audit with zero qualified opinions; manages 12-month observation period evidence collection        |
| PCI DSS v4.0        | Payment Card Industry Data Security Standard — latest version                                   | Maps all payment-processing controls to PCI DSS v4.0 requirements; coordinates annual ROC (Report on Compliance) with QSA; manages SAQ completion for applicable scope       |
| GDPR                | General Data Protection Regulation — EU data protection                                         | Maintains Records of Processing Activities (RoPA); coordinates DPO activities; manages data subject request (DSR) fulfillment; ensures cross-border data transfer compliance |
| ISO 27001           | Information Security Management System (ISMS)                                                   | Develops Statement of Applicability (SoA); manages internal audit program; coordinates Stage 1 + Stage 2 certification audits; maintains ISMS documentation                  |
| Audit Planning      | End-to-end audit lifecycle management                                                           | Produces comprehensive audit plans with scope, timeline, resource requirements, and deliverables; achieves zero audit scope creep incidents                                  |
| Evidence Collection | Systematic gathering and organization of compliance evidence                                    | Automates 70%+ of evidence collection; maintains evidence repository with chain of custody; achieves 100% evidence completeness at audit time                                |

## Execution Guidance

### 1. SOC 2 Type II — Control Framework

**Trust Service Categories (TSCs):**

| TSC                            | Relevance                                        | Key Controls                                                                                               |
| ------------------------------ | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| **Security (Common Criteria)** | Mandatory — baseline for all SOC 2               | CC1–CC9: Control environment, risk assessment, control activities, information & communication, monitoring |
| **Availability**               | Required if app offers SLA-guaranteed uptime     | A1.1–A1.3: Capacity management, environmental protections, recovery procedures                             |
| **Processing Integrity**       | Required if app processes financial transactions | PI1.1–PI1.5: Processing completeness, accuracy, timeliness, authorization                                  |
| **Confidentiality**            | Required if app handles confidential data        | C1.1–C1.2: Confidential information identification, encryption, access controls                            |
| **Privacy**                    | Required if app processes personal data          | P1.1–P8.1: Notice, choice, collection, use, retention, disposal, access, disclosure                        |

**SOC 2 Control Mapping — Mobile App Focus:**

```yaml
# soc2-controls.yml
CC6: Logical and Physical Access Controls
  CC6.1: Logical access security software, infrastructure, and architectures
    - Mobile: MDM enrollment required for all development devices
    - Mobile: Code repository access via SSO + MFA
    - Mobile: Production environment access restricted to CI/CD pipeline
    - Evidence: Access logs, MFA enrollment reports, CI/CD pipeline configs

  CC6.2: Prior to issuing system access, registration and authorization
    - Mobile: Developer onboarding includes security training (SEC-101)
    - Mobile: Access reviews conducted quarterly
    - Evidence: Training completion records, access review sign-offs

  CC6.6: System access is removed/modified upon role change or termination
    - Mobile: Offboarding checklist includes repository access revocation
    - Mobile: Automated access revocation via SCIM provisioning
    - Evidence: Offboarding logs, SCIM sync reports

CC7: System Operations
  CC7.1: Monitoring for anomalies and security events
    - Mobile: SAST/DAST pipeline monitoring (Omar Farouq)
    - Mobile: AWS GuardDuty + Security Hub alerts (Leila Khoury)
    - Mobile: Penetration testing results (Sana Khoury)
    - Evidence: Security monitoring dashboards, alert response logs

  CC7.2: Incident detection and response
    - Mobile: Security incident runbook
    - Mobile: Incident response team with defined roles
    - Evidence: Incident reports, post-incident reviews, drill results

CC8: Change Management
  CC8.1: Changes are authorized, tested, and documented
    - Mobile: All changes go through 10-stage pipeline
    - Mobile: Code review required for all PRs
    - Mobile: Automated testing with 100% pass rate gate
    - Evidence: Pipeline execution logs, code review records, test results

  CC8.2: Changes are monitored for completeness and accuracy
    - Mobile: Deployment monitoring with rollback capability
    - Mobile: Post-deployment verification checks
    - Evidence: Deployment logs, monitoring alerts, rollback records
```

**SOC 2 Type II Audit Timeline:**

| Phase                    | Duration    | Activities                                                             | Deliverables                                   |
| ------------------------ | ----------- | ---------------------------------------------------------------------- | ---------------------------------------------- |
| **Readiness Assessment** | 4–6 weeks   | Gap analysis, control design review, evidence gap identification       | Readiness report, remediation plan             |
| **Remediation**          | 8–12 weeks  | Implement missing controls, collect evidence, update documentation     | Updated control framework, evidence repository |
| **Observation Period**   | 6–12 months | Controls operating in production; evidence continuously collected      | Evidence packages, monitoring reports          |
| **Fieldwork**            | 4–6 weeks   | Auditor tests controls, requests additional evidence, interviews staff | Auditor working papers, management responses   |
| **Report Issuance**      | 2–4 weeks   | Auditor drafts report, management reviews, final report issued         | SOC 2 Type II report                           |

### 2. PCI DSS v4.0 — Payment Card Compliance

**PCI DSS v4.0 Key Changes from v3.2.1:**

1. **Customized approach**: Organizations can define their own control implementation methods (in addition to defined approach)
2. **Continuous security**: Emphasis on ongoing security rather than point-in-time compliance
3. **Role-based access**: Stricter requirements for role-based access control
4. **MFA everywhere**: MFA required for all access to cardholder data environment (CDE)
5. **Targeted risk analysis**: Required for many requirements where not previously mandated

**PCI DSS v4.0 Requirements — Mobile Payment App Mapping:**

| Req #  | Requirement                        | Mobile App Implementation                       | Evidence                                 |
| ------ | ---------------------------------- | ----------------------------------------------- | ---------------------------------------- |
| **1**  | Firewall and network security      | WAF rules, VPC security groups, NSG rules       | Firewall configs, network diagrams       |
| **2**  | Secure configurations              | Hardened baselines for all systems              | Config audit reports                     |
| **3**  | Protect stored account data        | Tokenization — no PAN stored in app or backend  | Data flow diagrams, tokenization proof   |
| **4**  | Protect cardholder data in transit | TLS 1.2+ with certificate pinning               | TLS configs, pinning implementation      |
| **5**  | Protect against malware            | EDR on all servers; mobile app integrity checks | EDR reports, integrity verification      |
| **6**  | Secure development                 | SAST/DAST pipeline; secure coding training      | Pipeline results, training records       |
| **7**  | Restrict access by need-to-know    | RBAC; least privilege; quarterly access reviews | Access logs, review sign-offs            |
| **8**  | Identify and authenticate access   | MFA for all CDE access; unique IDs              | MFA logs, identity management reports    |
| **9**  | Restrict physical access           | Data center access controls; device encryption  | Physical access logs, encryption configs |
| **10** | Log and monitor all access         | SIEM integration; log retention ≥1 year         | SIEM reports, log samples                |
| **11** | Test security regularly            | Pen testing quarterly; ASV scans quarterly      | Pen test reports, ASV scan results       |
| **12** | Maintain security policy           | Documented security policies; annual review     | Policy documents, review records         |

**Mobile-Specific PCI Considerations:**

1. **Point of Interaction (POI)**: If the mobile app accepts card data directly (not via redirect to payment processor), the app itself is a POI device and must comply with PTS (PIN Transaction Security) requirements
2. **SDK Compliance**: If using third-party payment SDKs (Stripe, Braintree), verify the SDK is PCI-compliant and obtain their AOC (Attestation of Compliance)
3. **SAQ Selection**: Mobile apps that redirect to payment processors typically qualify for SAQ A; apps that handle card data directly require SAQ D or full ROC

### 3. GDPR — Data Protection Compliance

**GDPR Compliance Checklist for Mobile Apps:**

| Article        | Requirement                                                     | Implementation                                              | Evidence                                    |
| -------------- | --------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------- |
| **Art. 5**     | Data processing principles (lawfulness, fairness, transparency) | Privacy policy; data minimization in app design             | Privacy policy, data inventory              |
| **Art. 6**     | Lawful basis for processing                                     | Consent management platform; legitimate interest assessment | Consent records, LIA documentation          |
| **Art. 7**     | Conditions for consent                                          | Granular consent; easy withdrawal; no pre-ticked boxes      | Consent UI screenshots, withdrawal flow     |
| **Art. 12-14** | Transparent information                                         | Layered privacy notice; just-in-time notices                | Privacy notice designs, in-app notices      |
| **Art. 15-22** | Data subject rights                                             | DSR portal; automated data export/deletion                  | DSR fulfillment logs, export/deletion tools |
| **Art. 25**    | Data protection by design and default                           | Privacy impact assessments; data minimization               | DPIA reports, design review records         |
| **Art. 30**    | Records of processing activities                                | RoPA maintained and updated                                 | RoPA document                               |
| **Art. 32**    | Security of processing                                          | Encryption, access controls, incident response              | Security controls documentation             |
| **Art. 33-34** | Breach notification                                             | 72-hour notification process; DPA contact list              | Breach notification procedure               |
| **Art. 35**    | Data protection impact assessment                               | DPIA for high-risk processing                               | Completed DPIAs                             |
| **Art. 44-49** | International data transfers                                    | SCCs; adequacy decisions; transfer impact assessments       | Transfer documentation, TIAs                |

**Data Subject Request (DSR) Fulfillment Process:**

```
User submits DSR (access, rectification, erasure, portability)
    │
    ▼
DSR Portal receives and logs request (Day 0)
    │
    ▼
Compliance team validates identity (Day 1-2)
    │
    ▼
Request routed to relevant teams:
    ├── Engineering: Data extraction/deletion from databases
    ├── Analytics: Data removal from analytics platforms
    ├── Marketing: Data removal from CRM/marketing tools
    └── Support: Data removal from ticketing systems
    │
    ▼
Data compiled/removed; quality check performed (Day 7-14)
    │
    ▼
Response delivered to user in requested format (Day 14-21)
    │
    ▼
Request logged as fulfilled; evidence retained (Day 28-30)
```

**SLA: 30 calendar days from request receipt (GDPR Article 12(3))**

### 4. ISO 27001 — ISMS Management

**ISO 27001:2022 Annex A Controls — Mobile App Relevance:**

| Annex A Theme          | Controls               | Mobile App Relevance                                                                                                   |
| ---------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **A.5 Organizational** | 5.1–5.37 (37 controls) | Policies, roles, responsibilities, threat intelligence, supplier security                                              |
| **A.6 People**         | 6.1–6.8 (8 controls)   | Screening, terms of employment, awareness training, disciplinary process                                               |
| **A.7 Physical**       | 7.1–7.14 (14 controls) | Secure areas, equipment security, clearing desk, remote working                                                        |
| **A.8 Technological**  | 8.1–8.34 (34 controls) | Access control, cryptography, operations security, communications security, system acquisition, supplier relationships |

**Key Technological Controls (A.8) for Mobile Apps:**

| Control ID | Control Name                            | Implementation                                                        |
| ---------- | --------------------------------------- | --------------------------------------------------------------------- |
| A.8.1      | User endpoint devices                   | MDM for all developer devices; BYOD policy with security requirements |
| A.8.6      | Capacity management                     | Infrastructure monitoring; auto-scaling; capacity planning            |
| A.8.7      | Protection against malware              | EDR on all servers; mobile app integrity verification                 |
| A.8.8      | Management of technical vulnerabilities | Automated vulnerability scanning; patch management SLAs               |
| A.8.9      | Configuration management                | IaC (Terraform); configuration drift detection                        |
| A.8.10     | Information deletion                    | Data retention policies; automated deletion workflows                 |
| A.8.11     | Data masking                            | PII masking in non-production environments                            |
| A.8.12     | Data leakage prevention                 | DLP controls for source code repositories; secret scanning            |
| A.8.15     | Logging                                 | Centralized logging; log integrity protection                         |
| A.8.16     | Monitoring activities                   | SIEM; alerting; security dashboards                                   |
| A.8.20     | Network security                        | Network segmentation; WAF; DDoS protection                            |
| A.8.21     | Security of network services            | TLS; certificate management; DNS security                             |
| A.8.23     | Web filtering                           | URL filtering for corporate networks                                  |
| A.8.24     | Use of cryptography                     | AES-256; RSA-2048+; TLS 1.2+; key management                          |

**Statement of Applicability (SoA) Template:**

```yaml
# soa-mobile-app.yml
statement_of_applicability:
  standard: 'ISO/IEC 27001:2022'
  organization: 'Mobile Product Company'
  scope: 'Mobile application development and operation'
  version: '1.0'
  date: '2026-04-01'

  controls:
    - control_id: A.8.24
      control_name: Use of cryptography
      status: applicable
      implementation: AES-256-GCM for data at rest; TLS 1.3 for data in transit;
        RSA-4096 for key exchange; keys managed via AWS KMS with automatic rotation
      justification: Required for protection of user data and payment information
      auditor_notes: Verified — encryption implementation reviewed by CSO

    - control_id: A.8.11
      control_name: Data masking
      status: applicable
      implementation: PII masked in staging and development environments using
        deterministic anonymization; production data never copied to non-production
      justification: Required for GDPR compliance and data protection
      auditor_notes: Verified — sampled 50 records, all properly masked
```

### 5. Audit Planning & Evidence Collection

**Annual Audit Calendar:**

| Audit                     | Frequency           | Typical Month      | Lead                       | Duration            |
| ------------------------- | ------------------- | ------------------ | -------------------------- | ------------------- |
| SOC 2 Type II             | Annual (continuous) | Fieldwork: October | Ingrid Solberg             | 4–6 weeks fieldwork |
| PCI DSS ROC               | Annual              | August             | Ingrid Solberg + QSA       | 6–8 weeks           |
| ISO 27001 Surveillance    | Annual              | March              | Ingrid Solberg + Registrar | 3–5 days on-site    |
| ISO 27001 Recertification | Triennial           | Year 3             | Ingrid Solberg + Registrar | 5–10 days           |
| GDPR Compliance Review    | Annual              | June               | Ingrid Solberg + DPO       | 2–3 weeks           |
| OWASP MASVS Assessment    | Per release         | Each Stage 6/8     | Sana Khoury                | 5 business days     |
| Internal Audit            | Quarterly           | Jan, Apr, Jul, Oct | Ingrid Solberg             | 1–2 weeks           |

**Evidence Collection Automation:**

```yaml
# evidence-collection-automation.yml
automated_evidence:
  - control: CC7.1 (Monitoring)
    source: AWS CloudWatch + GuardDuty
    collection: Daily export of security alerts and response actions
    format: JSON → evidence-repository/CC7.1/YYYY-MM/
    tool: Lambda function + S3 lifecycle policy

  - control: CC8.1 (Change Management)
    source: GitHub Actions pipeline logs
    collection: On each pipeline execution, archive gate results
    format: JSON → evidence-repository/CC8.1/YYYY-MM/
    tool: GitHub Actions artifact export

  - control: PCI DSS Req 6 (Secure Development)
    source: SAST/DAST pipeline results
    collection: On each scan, archive results with timestamps
    format: SARIF + JSON → evidence-repository/PCI-DSS-6/YYYY-MM/
    tool: CI/CD pipeline integration

  - control: PCI DSS Req 10 (Logging)
    source: SIEM (Splunk/Datadog)
    collection: Weekly export of audit logs
    format: CSV → evidence-repository/PCI-DSS-10/YYYY-MM/
    tool: SIEM scheduled search + export

  - control: ISO 27001 A.8.15 (Logging)
    source: Application logs
    collection: Daily aggregation and integrity verification
    format: Compressed + signed → evidence-repository/A8.15/YYYY-MM/
    tool: Log aggregation pipeline

manual_evidence:
  - control: SOC 2 CC1.2 (Board oversight)
    collection: Quarterly board meeting minutes (security section)
    responsible: Ingrid Solberg
    frequency: Quarterly

  - control: ISO 27001 A.6.3 (Awareness training)
    collection: Training completion reports
    responsible: Li Wei Chen
    frequency: Quarterly
```

**Evidence Repository Structure:**

```
evidence-repository/
├── SOC2/
│   ├── CC1/
│   ├── CC2/
│   ├── ...
│   └── CC9/
├── PCI-DSS/
│   ├── Req1/
│   ├── Req2/
│   ├── ...
│   └── Req12/
├── GDPR/
│   ├── Art5-7/
│   ├── Art12-22/
│   └── Art25-49/
├── ISO27001/
│   ├── A5/
│   ├── A6/
│   ├── A7/
│   └── A8/
└── INDEX.md  # Master evidence index with metadata
```

### 6. Remediation Tracking

**Remediation Workflow:**

```
Audit Finding Identified
    │
    ▼
Finding logged in remediation tracker
    ├── Severity: Critical / Major / Minor / Observation
    ├── Root cause analysis required? (Critical/Major: Yes)
    ├── Remediation owner assigned
    └── Target remediation date set
    │
    ▼
Remediation plan developed
    ├── Immediate containment (if applicable)
    ├── Root cause analysis
    ├── Corrective action
    ├── Preventive action
    └── Validation criteria
    │
    ▼
Remediation implemented
    ├── Evidence of implementation collected
    └── Validation testing performed
    │
    ▼
Remediation validated
    ├── Validated by: Compliance team (Ingrid Solberg)
    ├── Evidence: Test results, screenshots, logs
    └── Status: Closed / Reopened
    │
    ▼
Lessons learned documented
    ├── Root cause added to risk register
    ├── Preventive measures applied to similar systems
    └── Process improvements implemented
```

**Remediation SLA by Severity:**

| Severity        | Definition                                            | Remediation SLA  | Escalation                 |
| --------------- | ----------------------------------------------------- | ---------------- | -------------------------- |
| **Critical**    | Control completely absent; regulatory breach possible | 30 days          | Immediate CSO notification |
| **Major**       | Control partially implemented; significant gap        | 60 days          | CSO + CTO notification     |
| **Minor**       | Control implemented but documentation incomplete      | 90 days          | Team lead notification     |
| **Observation** | Improvement opportunity; no compliance impact         | Next audit cycle | Noted for follow-up        |

## Pipeline Integration

| Pipeline Stage                       | Application                                                                                                                                                            |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 1** (SRD)                    | Identifies regulatory compliance requirements that drive security requirements; defines which frameworks apply based on app scope (payment processing, EU users, etc.) |
| **Stage 6** (Code Review)            | Provides compliance perspective on code review findings; ensures security controls map to applicable compliance framework requirements                                 |
| **Stage 8** (Integrity Verification) | Verifies that compliance-relevant controls are functioning as designed; provides evidence for compliance framework requirements                                        |
| **Stage 10** (Release Readiness)     | Confirms that all applicable compliance framework requirements are met; provides compliance sign-off to CSO for release checklist                                      |

## Quality Standards

| Metric                     | Standard                                                                                                   |
| -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Audit Readiness**        | Evidence repository is audit-ready at all times; zero "evidence not found" findings during external audits |
| **Finding Remediation**    | 100% of Critical findings remediated within 30 days; 100% of Major findings within 60 days                 |
| **External Audit Results** | Zero qualified opinions on SOC 2 Type II reports; zero non-conformities on ISO 27001 surveillance audits   |
| **PCI DSS Compliance**     | Annual ROC with zero non-compliant requirements; quarterly ASV scans with zero high/critical findings      |
| **GDPR Compliance**        | 100% of DSRs fulfilled within 30-day SLA; zero regulatory fines or enforcement actions                     |
| **Evidence Automation**    | ≥70% of compliance evidence collected automatically                                                        |
| **Audit Efficiency**       | External audit fieldwork completed within planned timeline; zero scope extensions                          |
