---
name: compliance-documentation
description: "Produce audit-grade compliance documentation — risk assessments, control descriptions, evidence packages, and remediation plans — that satisfy SOC 2, ISO 27001, PCI DSS, and GDPR auditors on first submission."
version: "1.0.0"
---

| Competency                     | Description                                                                   | Quality Criteria                                                                                                                                                                      |
| ------------------------------ | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Risk Assessment Documentation  | Producing comprehensive, auditable risk assessments                           | Develops risk assessments that satisfy SOC 2, ISO 27001, and PCI DSS requirements; achieves zero documentation-related audit findings; maintains risk register with quarterly updates |
| Control Descriptions           | Writing clear, precise, auditable control documentation                       | Every control description includes: purpose, implementation details, responsible party, evidence source, testing procedure; controls mapped to all applicable framework requirements  |
| Evidence Collection Automation | Designing automated evidence pipelines for compliance                         | 70%+ of evidence collected automatically; evidence linked to controls via unique identifiers; evidence repository structured for auditor self-service                                 |
| Remediation Plans              | Developing actionable, trackable remediation documentation                    | Every remediation plan includes: root cause, corrective action, preventive action, owner, timeline, validation criteria; 100% of plans tracked to closure                             |
| Auditor Communication          | Managing external auditor relationships and information requests              | Provides complete information requests on first submission; zero "evidence not found" findings; audit fieldwork completed within planned timeline                                     |
| Template Design                | Creating reusable documentation templates for consistent compliance artifacts | Maintains template library covering all compliance artifact types; templates enforce consistent structure; new audit programs bootstrapped from templates in ≤1 day                   |

## Execution Guidance

### 1. Risk Assessment Documentation

**Risk Assessment Methodology — NIST SP 800-30 Aligned:**

```markdown
# Risk Assessment — Mobile Banking Application

## 1. System Description

- Application: Mobile Banking App v[X.Y.Z]
- Platforms: Android (minSdk 26+), iOS (15.0+)
- Backend: AWS (us-east-1, eu-west-1)
- Data Types: PII, financial data, authentication credentials, transaction data
- User Base: [X] million active users
- Regulatory Context: FFIEC, PSD2, GDPR, PCI DSS

## 2. Threat Identification

| Threat Agent    | Capability | Motivation                | Attack Vector                                         |
| --------------- | ---------- | ------------------------- | ----------------------------------------------------- |
| Organized Crime | High       | Financial gain            | Account takeover, transaction fraud, ransomware       |
| Nation State    | Very High  | Intelligence gathering    | Supply chain compromise, zero-day exploitation        |
| Insider Threat  | Medium     | Financial gain, espionage | Data exfiltration, credential theft                   |
| Script Kiddie   | Low        | Notoriety                 | Known vulnerability exploitation, credential stuffing |

## 3. Vulnerability Assessment

| Vulnerability               | Source              | Likelihood | Impact | Risk Level |
| --------------------------- | ------------------- | ---------- | ------ | ---------- |
| Insecure data storage       | Pen test finding    | Medium     | High   | High       |
| Missing certificate pinning | Architecture review | Low        | High   | Medium     |
| Outdated dependency         | SAST scan           | Medium     | Medium | Medium     |
| Insufficient logging        | Internal audit      | Medium     | Medium | Medium     |

## 4. Risk Analysis

| Risk ID | Threat + Vulnerability                            | Likelihood | Impact   | Risk Level | Treatment                      |
| ------- | ------------------------------------------------- | ---------- | -------- | ---------- | ------------------------------ |
| R-001   | Account takeover via credential stuffing + no MFA | High       | Critical | Critical   | Mitigate — implement MFA       |
| R-002   | Data breach via insecure storage + device theft   | Medium     | High     | High       | Mitigate — encrypt storage     |
| R-003   | Supply chain compromise via vulnerable dependency | Medium     | High     | High       | Mitigate — dependency scanning |
| R-004   | Fraudulent transactions via API manipulation      | Low        | Critical | High       | Mitigate — transaction signing |

## 5. Risk Treatment Plan

| Risk ID | Treatment | Action Items                                                                                               | Owner            | Target Date | Status      |
| ------- | --------- | ---------------------------------------------------------------------------------------------------------- | ---------------- | ----------- | ----------- |
| R-001   | Mitigate  | 1. Implement MFA enrollment flow<br>2. Add biometric authentication<br>3. Configure risk-based auth        | Product Team     | 2026-05-01  | In Progress |
| R-002   | Mitigate  | 1. Implement SQLCipher<br>2. Clear cache on background<br>3. Verify encryption                             | Android/iOS Lead | 2026-04-20  | In Progress |
| R-003   | Mitigate  | 1. Deploy Snyk scanning<br>2. Establish patch SLAs<br>3. Create dependency allowlist                       | Li Wei Chen      | 2026-04-15  | In Progress |
| R-004   | Mitigate  | 1. Implement transaction signing<br>2. Add transaction confirmation flow<br>3. Configure anomaly detection | Backend Team     | 2026-06-01  | Planned     |

## 6. Residual Risk Assessment

| Risk ID | Residual Likelihood | Residual Impact | Residual Level | Accepted?    |
| ------- | ------------------- | --------------- | -------------- | ------------ |
| R-001   | Low                 | High            | Medium         | Yes — by CSO |
| R-002   | Low                 | Medium          | Low            | Yes — by CSO |
| R-003   | Low                 | Medium          | Low            | Yes — by CSO |
| R-004   | Low                 | High            | Medium         | Yes — by CSO |

## 7. Approval

Prepared by: Ingrid Solberg — Date: [YYYY-MM-DD]
Reviewed by: Dr. Sarah Chen (CSO) — Date: [YYYY-MM-DD]
Approved by: Dr. Kenji Nakamura (CTO) — Date: [YYYY-MM-DD]
```

**Risk Assessment Schedule:**

| Assessment Type                   | Frequency   | Trigger                          | Audience                    |
| --------------------------------- | ----------- | -------------------------------- | --------------------------- |
| Comprehensive Risk Assessment     | Annual      | Scheduled                        | C-suite, Board              |
| Feature-Specific Risk Assessment  | Per feature | New feature with security impact | Product team, CSO           |
| Technology Change Risk Assessment | Per change  | New technology adoption          | Engineering, CSO            |
| Threat Model Update               | Quarterly   | Scheduled or significant change  | Engineering, CSO            |
| Incident-Driven Risk Assessment   | As needed   | Security incident                | CSO, incident response team |

### 2. Control Description Framework

**Standard Control Description Template:**

```markdown
# Control: CC6.1 — Logical Access Security

## Control Information

| Field            | Value                                                               |
| ---------------- | ------------------------------------------------------------------- |
| Control ID       | CC6.1                                                               |
| Control Name     | Logical Access Security Software, Infrastructure, and Architectures |
| Framework        | SOC 2 Type II — Common Criteria                                     |
| Category         | Security                                                            |
| Owner            | Dr. Priya Mehta (CIO)                                               |
| Implementer      | Leila Khoury (DevOps)                                               |
| Review Frequency | Quarterly                                                           |
| Last Review      | 2026-03-15                                                          |
| Next Review      | 2026-06-15                                                          |

## Control Description

The entity implements logical access security software, infrastructure, and
architectures to protect systems and data from unauthorized access. Access to
production systems is restricted to automated CI/CD pipelines; no direct human
access to production databases or servers is permitted.

## Implementation Details

### Access Control Mechanisms

1. **Source Code Repositories**: GitHub with SSO (Okta) + MFA enforcement
   - Repository access granted via team membership in Okta
   - Branch protection rules require 2+ approvals for main branch
   - CODEOWNERS file enforces review by designated team members

2. **Cloud Infrastructure**: AWS IAM with least-privilege policies
   - Production access via CI/CD pipeline roles only
   - Developer access limited to staging and development environments
   - All privileged actions logged via CloudTrail

3. **CI/CD Pipeline**: GitHub Actions with OIDC to AWS
   - Pipeline assumes IAM role with least-privilege permissions
   - No long-lived AWS credentials stored in repository
   - Deployment approvals required for production

### Monitoring & Detection

- AWS GuardDuty monitors for anomalous access patterns
- CloudTrail logs all API actions (retained 365 days)
- Access reviews conducted quarterly by CIO office
- Automated alerts on privileged access attempts

## Evidence Sources

| Evidence ID | Description               | Source         | Frequency | Automation   |
| ----------- | ------------------------- | -------------- | --------- | ------------ |
| EV-CC6.1-01 | GitHub access list export | GitHub API     | Quarterly | ✅ Automated |
| EV-CC6.1-02 | AWS IAM policy review     | AWS Console    | Quarterly | ✅ Automated |
| EV-CC6.1-03 | MFA enforcement report    | Okta Admin     | Quarterly | ✅ Automated |
| EV-CC6.1-04 | CloudTrail log sample     | AWS CloudTrail | Monthly   | ✅ Automated |
| EV-CC6.1-05 | Access review sign-off    | Confluence     | Quarterly | ❌ Manual    |

## Testing Procedure

1. Verify MFA is enforced for all GitHub accounts (Okta policy)
2. Verify branch protection rules are active on all production repositories
3. Verify no IAM users with direct production access exist
4. Verify CI/CD pipeline uses OIDC (not access keys) for AWS authentication
5. Sample 5 CloudTrail log entries for privileged actions

## Related Controls

- CC6.2: Registration and authorization
- CC6.6: Access removal
- CC6.7: Authentication
- PCI DSS Req 7: Restrict access by need-to-know
- ISO 27001 A.8.2: Access rights

## Finding Information

| Field             | Value                                  |
| ----------------- | -------------------------------------- |
| Finding ID        | AUD-2026-001                           |
| Framework         | SOC 2 Type II                          |
| Control ID        | CC7.2                                  |
| Finding Title     | Insufficient incident response testing |
| Severity          | Major                                  |
| Identified By     | External Auditor — [Firm Name]         |
| Date Identified   | 2026-03-15                             |
| Remediation Owner | Dr. Sarah Chen (CSO)                   |
| Target Completion | 2026-05-15                             |

## Root Cause Analysis

The organization had documented incident response procedures but had not
conducted a tabletop exercise or live drill in the past 12 months. This
gap was identified during the SOC 2 Type II fieldwork when the auditor
requested evidence of incident response testing.

Root cause: Incident response testing was scheduled quarterly but was
deprioritized due to product delivery pressures. No escalation mechanism
existed to ensure testing occurred.

## Corrective Action

1. **Conduct tabletop exercise** (Target: 2026-04-01)
   - Scenario: Mobile app data breach affecting 100K users
   - Participants: CSO, CTO, CPO, Legal, Comms
   - Duration: 2 hours
   - Output: After-action report with improvement items

2. **Conduct live drill** (Target: 2026-04-15)
   - Scenario: Automated detection of anomalous API access patterns
   - Participants: Security team, on-call engineers, DevOps
   - Duration: 1 hour (during business hours)
   - Output: Drill report with timeline and effectiveness metrics

3. **Update incident response plan** (Target: 2026-04-30)
   - Incorporate lessons learned from tabletop and drill
   - Add mobile-specific incident scenarios
   - Update contact lists and escalation procedures

## Preventive Action

1. **Automate testing reminders**: Configure calendar reminders with escalation
   to CSO if testing not completed within 30 days of scheduled date
2. **Include testing in OKRs**: Add incident response testing as quarterly OKR
   for security team with measurable completion criteria
3. **Executive dashboard**: Add incident response testing status to monthly
   C-suite security dashboard

## Validation Criteria

- [ ] Tabletop exercise completed with after-action report
- [ ] Live drill completed with drill report
- [ ] Incident response plan updated and approved by CSO
- [ ] Automated reminders configured and tested
- [ ] Incident response testing added to quarterly OKRs
- [ ] Dashboard updated to show testing status

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`change-history.md`](references/change-history.md) — Change History
- [`evidence-collection.md`](references/evidence-collection.md) — Evidence Collection
- [`status-history.md`](references/status-history.md) — Status History
- [`pipeline-integration.md`](references/pipeline-integration.md) — Pipeline Integration
- [`quality-standards.md`](references/quality-standards.md) — Quality Standards
```
