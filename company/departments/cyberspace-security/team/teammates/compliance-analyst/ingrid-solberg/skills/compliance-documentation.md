# Compliance Documentation

**Category:** Compliance Documentation & Risk Management
**Owner:** Compliance Analyst — Ingrid Solberg

## Overview

Systematic methodology for creating, maintaining, and managing compliance documentation across all regulatory frameworks applicable to the company's mobile application products. This skill covers risk assessment documentation, control descriptions, evidence collection automation, remediation plan development, external auditor communication protocols, and standardized documentation templates. High-quality compliance documentation is the foundation of successful audits — it demonstrates to regulators and auditors that the organization operates a mature, controlled, and continuously monitored security program. Poor documentation is the single most common cause of audit findings, even when technical controls are properly implemented.

## Competency Dimensions

| Dimension | Description | Proficiency Indicators |
|-----------|-------------|----------------------|
| Risk Assessment Documentation | Producing comprehensive, auditable risk assessments | Develops risk assessments that satisfy SOC 2, ISO 27001, and PCI DSS requirements; achieves zero documentation-related audit findings; maintains risk register with quarterly updates |
| Control Descriptions | Writing clear, precise, auditable control documentation | Every control description includes: purpose, implementation details, responsible party, evidence source, testing procedure; controls mapped to all applicable framework requirements |
| Evidence Collection Automation | Designing automated evidence pipelines for compliance | 70%+ of evidence collected automatically; evidence linked to controls via unique identifiers; evidence repository structured for auditor self-service |
| Remediation Plans | Developing actionable, trackable remediation documentation | Every remediation plan includes: root cause, corrective action, preventive action, owner, timeline, validation criteria; 100% of plans tracked to closure |
| Auditor Communication | Managing external auditor relationships and information requests | Provides complete information requests on first submission; zero "evidence not found" findings; audit fieldwork completed within planned timeline |
| Template Design | Creating reusable documentation templates for consistent compliance artifacts | Maintains template library covering all compliance artifact types; templates enforce consistent structure; new audit programs bootstrapped from templates in ≤1 day |

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
| Threat Agent | Capability | Motivation | Attack Vector |
|-------------|-----------|------------|---------------|
| Organized Crime | High | Financial gain | Account takeover, transaction fraud, ransomware |
| Nation State | Very High | Intelligence gathering | Supply chain compromise, zero-day exploitation |
| Insider Threat | Medium | Financial gain, espionage | Data exfiltration, credential theft |
| Script Kiddie | Low | Notoriety | Known vulnerability exploitation, credential stuffing |

## 3. Vulnerability Assessment
| Vulnerability | Source | Likelihood | Impact | Risk Level |
|--------------|--------|------------|--------|------------|
| Insecure data storage | Pen test finding | Medium | High | High |
| Missing certificate pinning | Architecture review | Low | High | Medium |
| Outdated dependency | SAST scan | Medium | Medium | Medium |
| Insufficient logging | Internal audit | Medium | Medium | Medium |

## 4. Risk Analysis
| Risk ID | Threat + Vulnerability | Likelihood | Impact | Risk Level | Treatment |
|---------|----------------------|------------|--------|------------|-----------|
| R-001 | Account takeover via credential stuffing + no MFA | High | Critical | Critical | Mitigate — implement MFA |
| R-002 | Data breach via insecure storage + device theft | Medium | High | High | Mitigate — encrypt storage |
| R-003 | Supply chain compromise via vulnerable dependency | Medium | High | High | Mitigate — dependency scanning |
| R-004 | Fraudulent transactions via API manipulation | Low | Critical | High | Mitigate — transaction signing |

## 5. Risk Treatment Plan
| Risk ID | Treatment | Action Items | Owner | Target Date | Status |
|---------|-----------|-------------|-------|-------------|--------|
| R-001 | Mitigate | 1. Implement MFA enrollment flow<br>2. Add biometric authentication<br>3. Configure risk-based auth | Product Team | 2026-05-01 | In Progress |
| R-002 | Mitigate | 1. Implement SQLCipher<br>2. Clear cache on background<br>3. Verify encryption | Android/iOS Lead | 2026-04-20 | In Progress |
| R-003 | Mitigate | 1. Deploy Snyk scanning<br>2. Establish patch SLAs<br>3. Create dependency allowlist | Li Wei Chen | 2026-04-15 | In Progress |
| R-004 | Mitigate | 1. Implement transaction signing<br>2. Add transaction confirmation flow<br>3. Configure anomaly detection | Backend Team | 2026-06-01 | Planned |

## 6. Residual Risk Assessment
| Risk ID | Residual Likelihood | Residual Impact | Residual Level | Accepted? |
|---------|-------------------|-----------------|----------------|-----------|
| R-001 | Low | High | Medium | Yes — by CSO |
| R-002 | Low | Medium | Low | Yes — by CSO |
| R-003 | Low | Medium | Low | Yes — by CSO |
| R-004 | Low | High | Medium | Yes — by CSO |

## 7. Approval
Prepared by: Ingrid Solberg — Date: [YYYY-MM-DD]
Reviewed by: Dr. Sarah Chen (CSO) — Date: [YYYY-MM-DD]
Approved by: Dr. Kenji Nakamura (CTO) — Date: [YYYY-MM-DD]
```

**Risk Assessment Schedule:**

| Assessment Type | Frequency | Trigger | Audience |
|-----------------|-----------|---------|----------|
| Comprehensive Risk Assessment | Annual | Scheduled | C-suite, Board |
| Feature-Specific Risk Assessment | Per feature | New feature with security impact | Product team, CSO |
| Technology Change Risk Assessment | Per change | New technology adoption | Engineering, CSO |
| Threat Model Update | Quarterly | Scheduled or significant change | Engineering, CSO |
| Incident-Driven Risk Assessment | As needed | Security incident | CSO, incident response team |

### 2. Control Description Framework

**Standard Control Description Template:**

```markdown
# Control: CC6.1 — Logical Access Security

## Control Information
| Field | Value |
|-------|-------|
| Control ID | CC6.1 |
| Control Name | Logical Access Security Software, Infrastructure, and Architectures |
| Framework | SOC 2 Type II — Common Criteria |
| Category | Security |
| Owner | Dr. Priya Mehta (CIO) |
| Implementer | Leila Khoury (DevOps) |
| Review Frequency | Quarterly |
| Last Review | 2026-03-15 |
| Next Review | 2026-06-15 |

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
| Evidence ID | Description | Source | Frequency | Automation |
|-------------|-------------|--------|-----------|------------|
| EV-CC6.1-01 | GitHub access list export | GitHub API | Quarterly | ✅ Automated |
| EV-CC6.1-02 | AWS IAM policy review | AWS Console | Quarterly | ✅ Automated |
| EV-CC6.1-03 | MFA enforcement report | Okta Admin | Quarterly | ✅ Automated |
| EV-CC6.1-04 | CloudTrail log sample | AWS CloudTrail | Monthly | ✅ Automated |
| EV-CC6.1-05 | Access review sign-off | Confluence | Quarterly | ❌ Manual |

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

## Change History
| Date | Change | Changed By |
|------|--------|-----------|
| 2026-03-15 | Quarterly review — no changes needed | Ingrid Solberg |
| 2025-12-15 | Updated to reflect OIDC migration | Ingrid Solberg |
| 2025-09-01 | Initial control documentation | Ingrid Solberg |
```

### 3. Evidence Collection Automation

**Evidence Collection Pipeline Architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Evidence Sources                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐│
│  │ GitHub   │ │ AWS      │ │ Okta     │ │ SAST/DAST        ││
│  │ API      │ │ CloudTrail│ │ Admin   │ │ Pipeline         ││
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────────┬─────────┘│
│       │             │             │                │          │
└───────┼─────────────┼─────────────┼────────────────┼──────────┘
        │             │             │                │
        ▼             ▼             ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│              Evidence Collection Layer                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Lambda Functions (scheduled & event-driven)          │   │
│  │  • github-access-export.py                            │   │
│  │  • cloudtrail-log-aggregator.py                       │   │
│  │  • okta-mfa-report.py                                 │   │
│  │  • sast-results-export.py                             │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│              Evidence Storage Layer                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  S3 Bucket: compliance-evidence-prod                  │   │
│  │  ├── SOC2/                                           │   │
│  │  │   ├── CC6/                                        │   │
│  │  │   │   ├── 2026-03/                                │   │
│  │  │   │   │   ├── EV-CC6.1-01-2026-03.json           │   │
│  │  │   │   │   └── EV-CC6.1-01-2026-03.sha256         │   │
│  │  │   │   └── ...                                     │   │
│  │  │   └── ...                                         │   │
│  │  ├── PCI-DSS/                                        │   │
│  │  ├── GDPR/                                           │   │
│  │  └── ISO27001/                                       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│              Evidence Index & Retrieval                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  DynamoDB: evidence-index                            │   │
│  │  • Evidence ID                                       │   │
│  │  • Control ID mapping                                │   │
│  │  • Collection date                                   │   │
│  │  • S3 location                                       │   │
│  │  • Integrity hash (SHA-256)                          │   │
│  │  • Retention expiry                                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Evidence Collection Script Template:**

```python
#!/usr/bin/env python3
"""
Evidence Collection Script — GitHub Access Export
Collects: EV-CC6.1-01 — GitHub access list export
Frequency: Quarterly
"""

import json
import hashlib
import boto3
import requests
from datetime import datetime
import os

def collect_github_access():
    """Export GitHub organization member and repository access data."""
    
    # Configuration
    org = os.environ['GITHUB_ORG']
    token = os.environ['GITHUB_TOKEN']
    bucket = os.environ['EVIDENCE_BUCKET']
    
    # Collect organization members
    members = []
    page = 1
    while True:
        resp = requests.get(
            f'https://api.github.com/orgs/{org}/members',
            headers={'Authorization': f'token {token}'},
            params={'page': page, 'per_page': 100}
        )
        if not resp.json():
            break
        members.extend(resp.json())
        page += 1
    
    # Collect repository access
    repos = []
    for member in members:
        member_repos = requests.get(
            f'https://api.github.com/orgs/{org}/repos',
            headers={'Authorization': f'token {token}'}
        ).json()
        repos.append({
            'login': member['login'],
            'repo_count': len(member_repos),
            'repos': [r['name'] for r in member_repos]
        })
    
    # Build evidence package
    evidence = {
        'evidence_id': 'EV-CC6.1-01',
        'control_id': 'CC6.1',
        'collection_date': datetime.utcnow().isoformat(),
        'collected_by': 'evidence-collection-lambda',
        'framework': 'SOC2',
        'data': {
            'organization': org,
            'total_members': len(members),
            'members': members,
            'repository_access': repos
        }
    }
    
    # Calculate integrity hash
    data_json = json.dumps(evidence['data'], sort_keys=True).encode()
    evidence['integrity_hash'] = hashlib.sha256(data_json).hexdigest()
    
    # Upload to S3
    s3 = boto3.client('s3')
    month = datetime.utcnow().strftime('%Y-%m')
    key = f"SOC2/CC6/{month}/EV-CC6.1-01-{month}.json"
    
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(evidence, indent=2),
        ServerSideEncryption='aws:kms'
    )
    
    # Update evidence index (DynamoDB)
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(
        TableName='evidence-index',
        Item={
            'evidence_id': {'S': 'EV-CC6.1-01'},
            'collection_date': {'S': evidence['collection_date']},
            's3_location': {'S': f's3://{bucket}/{key}'},
            'integrity_hash': {'S': evidence['integrity_hash']},
            'retention_expiry': {'S': '2029-12-31'},
            'status': {'S': 'collected'}
        }
    )
    
    return evidence

if __name__ == '__main__':
    collect_github_access()
    print("Evidence collected and stored successfully.")
```

### 4. Remediation Plan Documentation

**Remediation Plan Template:**

```markdown
# Remediation Plan — [Finding Title]

## Finding Information
| Field | Value |
|-------|-------|
| Finding ID | AUD-2026-001 |
| Framework | SOC 2 Type II |
| Control ID | CC7.2 |
| Finding Title | Insufficient incident response testing |
| Severity | Major |
| Identified By | External Auditor — [Firm Name] |
| Date Identified | 2026-03-15 |
| Remediation Owner | Dr. Sarah Chen (CSO) |
| Target Completion | 2026-05-15 |

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

## Evidence Collection
| Evidence Item | Description | Expected Date |
|--------------|-------------|---------------|
| EV-AUD-001-01 | Tabletop exercise after-action report | 2026-04-01 |
| EV-AUD-001-02 | Live drill report with timeline | 2026-04-15 |
| EV-AUD-001-03 | Updated incident response plan | 2026-04-30 |
| EV-AUD-001-04 | Calendar reminder configuration | 2026-04-30 |
| EV-AUD-001-05 | Q2 OKR documentation | 2026-04-30 |

## Status History
| Date | Status | Updated By | Notes |
|------|--------|-----------|-------|
| 2026-03-15 | Open | Ingrid Solberg | Finding received from auditor |
| 2026-03-20 | In Progress | Dr. Sarah Chen | Tabletop exercise scheduled |
| [date] | Complete | Ingrid Solberg | All validation criteria met |
```

### 5. Auditor Communication Protocol

**Information Request Response Process:**

```
Auditor submits Information Request (PBC List — Provided By Client)
    │
    ▼
Ingrid Solberg reviews request for completeness and clarity
    ├── If unclear: Request clarification from auditor (within 24 hours)
    └── If clear: Proceed to evidence retrieval
    │
    ▼
Evidence retrieved from automated evidence repository
    ├── If evidence exists: Package and submit (within 48 hours)
    └── If evidence missing: Initiate evidence collection (within 24 hours)
    │
    ▼
Evidence package reviewed for quality
    ├── Completeness: All requested items included
    ├── Accuracy: Evidence matches control description
    ├── Currency: Evidence is from the audit period
    └── Integrity: Evidence has not been modified
    │
    ▼
Evidence submitted to auditor via secure portal
    ├── Transmittal letter listing all items submitted
    ├── Evidence index with file names and descriptions
    └── Contact information for follow-up questions
    │
    ▼
Auditor reviews and provides feedback
    ├── If accepted: Item marked as satisfied
    └── If additional information requested: Repeat process
    │
    ▼
All PBC items satisfied → Fieldwork complete
```

**PBC List Response Template:**

```markdown
# PBC List Response — SOC 2 Type II Audit 2026

**Auditor:** [External Audit Firm]
**Prepared By:** Ingrid Solberg
**Date Submitted:** 2026-09-01
**Response Status:** Complete / Partial / Pending

| PBC Item # | Description | Status | Evidence File | Notes |
|------------|-------------|--------|---------------|-------|
| PBC-001 | Organization chart | Submitted | EV-ORG-001.pdf | Updated 2026-08-15 |
| PBC-002 | Security policies | Submitted | EV-SEC-001.pdf | All 12 policies included |
| PBC-003 | Risk assessment | Submitted | EV-RA-001.pdf | Annual assessment 2026 |
| PBC-004 | Access review evidence | Submitted | EV-CC6.1-01-2026-Q3.json | Automated collection |
| PBC-005 | Incident response test | Submitted | EV-CC7.2-001.pdf | Tabletop + drill reports |
| ... | ... | ... | ... | ... |

**Submission Summary:**
- Total PBC Items: [XX]
- Submitted: [XX]
- Pending: [XX] (expected by [date])
- Not Applicable: [XX] (justification provided)
```

### 6. Documentation Template Library

**Template Inventory:**

| Template ID | Template Name | Purpose | Framework |
|-------------|--------------|---------|-----------|
| TMPL-RA-001 | Risk Assessment | Comprehensive risk assessment | All |
| TMPL-CTL-001 | Control Description | Individual control documentation | All |
| TMPL-GAP-001 | Gap Analysis | Compliance gap identification | All |
| TMPL-REM-001 | Remediation Plan | Finding remediation tracking | All |
| TMPL-EVD-001 | Evidence Package | Evidence collection documentation | All |
| TMPL-PBC-001 | PBC Response | Auditor information request response | All |
| TMPL-ROPA-001 | Record of Processing | GDPR data processing inventory | GDPR |
| TMPL-DPIA-001 | Data Protection Impact | GDPR high-risk processing assessment | GDPR |
| TMPL-DSR-001 | DSR Response | Data subject request fulfillment | GDPR |
| TMPL-SOA-001 | Statement of Applicability | ISO 27001 control selection | ISO 27001 |
| TMPL-ROC-001 | Report on Compliance | PCI DSS compliance report | PCI DSS |
| TMPL-MASVS-001 | MASVS Audit Report | Mobile security compliance audit | MASVS |
| TMPL-AUD-001 | Audit Plan | Annual audit planning | All |
| TMPL-MGMT-001 | Management Response | Auditor finding response | All |

## Pipeline Integration

| Pipeline Stage | Application |
|----------------|-------------|
| **Stage 1** (SRD) | Risk assessment documentation created for the project; compliance requirements documented based on app scope and data classification |
| **Stage 6** (Code Review) | Code review findings documented with compliance framework mapping; remediation plans created for compliance-related findings |
| **Stage 8** (Integrity Verification) | Evidence collected for compliance-relevant controls; remediation plans updated for previously identified gaps |
| **Stage 10** (Release Readiness) | Compliance documentation package assembled for release decision; confirms all applicable compliance requirements are met with documented evidence |

## Quality Standards

| Metric | Standard |
|--------|----------|
| **Documentation Completeness** | 100% of required compliance artifacts created and maintained |
| **Evidence Availability** | 100% of evidence available within 48 hours of request; zero "evidence not found" during audits |
| **Documentation Accuracy** | Zero documentation errors identified by external auditors |
| **Template Usage** | 100% of compliance artifacts created using approved templates |
| **Remediation Tracking** | 100% of remediation plans tracked to closure with evidence |
| **Auditor Satisfaction** | External auditor rates documentation quality ≥4.5/5.0 |
| **Automation Rate** | ≥70% of evidence collected automatically |
| **Review Currency** | All control descriptions reviewed within scheduled review period |
