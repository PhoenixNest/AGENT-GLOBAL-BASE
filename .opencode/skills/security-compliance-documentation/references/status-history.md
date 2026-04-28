# Status History

## Status History

| Date       | Status      | Updated By     | Notes                         |
| ---------- | ----------- | -------------- | ----------------------------- |
| 2026-03-15 | Open        | Ingrid Solberg | Finding received from auditor |
| 2026-03-20 | In Progress | Dr. Sarah Chen | Tabletop exercise scheduled   |
| [date]     | Complete    | Ingrid Solberg | All validation criteria met   |

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

````

**PBC List Response Template:**

```markdown
# PBC List Response — SOC 2 Type II Audit 2026

**Auditor:** [External Audit Firm]
**Prepared By:** Ingrid Solberg
**Date Submitted:** 2026-09-01
**Response Status:** Complete / Partial / Pending

| PBC Item # | Description            | Status    | Evidence File            | Notes                    |
| ---------- | ---------------------- | --------- | ------------------------ | ------------------------ |
| PBC-001    | Organization chart     | Submitted | EV-ORG-001.pdf           | Updated 2026-08-15       |
| PBC-002    | Security policies      | Submitted | EV-SEC-001.pdf           | All 12 policies included |
| PBC-003    | Risk assessment        | Submitted | EV-RA-001.pdf            | Annual assessment 2026   |
| PBC-004    | Access review evidence | Submitted | EV-CC6.1-01-2026-Q3.json | Automated collection     |
| PBC-005    | Incident response test | Submitted | EV-CC7.2-001.pdf         | Tabletop + drill reports |
| ...        | ...                    | ...       | ...                      | ...                      |

**Submission Summary:**

- Total PBC Items: [XX]
- Submitted: [XX]
- Pending: [XX] (expected by [date])
- Not Applicable: [XX] (justification provided)
````

### 6. Documentation Template Library

**Template Inventory:**

| Template ID    | Template Name              | Purpose                              | Framework |
| -------------- | -------------------------- | ------------------------------------ | --------- |
| TMPL-RA-001    | Risk Assessment            | Comprehensive risk assessment        | All       |
| TMPL-CTL-001   | Control Description        | Individual control documentation     | All       |
| TMPL-GAP-001   | Gap Analysis               | Compliance gap identification        | All       |
| TMPL-REM-001   | Remediation Plan           | Finding remediation tracking         | All       |
| TMPL-EVD-001   | Evidence Package           | Evidence collection documentation    | All       |
| TMPL-PBC-001   | PBC Response               | Auditor information request response | All       |
| TMPL-ROPA-001  | Record of Processing       | GDPR data processing inventory       | GDPR      |
| TMPL-DPIA-001  | Data Protection Impact     | GDPR high-risk processing assessment | GDPR      |
| TMPL-DSR-001   | DSR Response               | Data subject request fulfillment     | GDPR      |
| TMPL-SOA-001   | Statement of Applicability | ISO 27001 control selection          | ISO 27001 |
| TMPL-ROC-001   | Report on Compliance       | PCI DSS compliance report            | PCI DSS   |
| TMPL-MASVS-001 | MASVS Audit Report         | Mobile security compliance audit     | MASVS     |
| TMPL-AUD-001   | Audit Plan                 | Annual audit planning                | All       |
| TMPL-MGMT-001  | Management Response        | Auditor finding response             | All       |
