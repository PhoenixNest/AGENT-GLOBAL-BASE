---
name: compliance-foundations
description: CI/CD compliance foundations — how Thomas Zhang's pipeline enforces OWASP MASVS, GDPR data-handling constraints, PCI DSS scope controls, and SOC 2 audit trail requirements through automated gate controls. Covers the compliance evidence package Thomas produces for Stage 8 (Integrity Verification) and how to coordinate security findings with the CSO (Dr. Sarah Chen) and CIO (Dr. Priya Mehta). Use when adding a new compliance control to the pipeline, when preparing for the Stage 8 security sign-off, or when responding to a compliance audit request.
version: "1.0.0"
---

# Compliance Foundations

## Purpose

Thomas Zhang's CI/CD pipeline is the enforcement layer for the company's compliance obligations. Policies written by the CSO and CIO become reality only when Thomas embeds them as automated pipeline gates. This skill defines the compliance controls Thomas operates, the evidence he produces, and how he coordinates with the security leadership.

## Compliance Frameworks in Scope

| Framework           | Applies To                     | Key CI/CD Obligation                                            | Evidence for Stage 8            |
| ------------------- | ------------------------------ | --------------------------------------------------------------- | ------------------------------- |
| **OWASP MASVS L1**  | All mobile releases            | SAST, dependency scan, storage/network controls verified        | Scan results report             |
| **OWASP MASVS L2**  | Auth and payment features      | Binary protection, anti-tampering, certificate pinning verified | L2 scan report                  |
| **GDPR**            | All features processing EU PII | PII-in-logs scanner, data retention policy enforced in pipeline | Log audit, data-flow doc        |
| **PCI DSS**         | Payment flows                  | No raw PAN in code, TLS enforced, scope isolation               | Tokenization test, network scan |
| **SOC 2 (Type II)** | Infrastructure access controls | IAM audit log, environment change log, RBAC enforcement         | Audit trail export              |

## MASVS Gate Controls (Pipeline)

Thomas implements the MASVS gate as a mandatory check in the CI pipeline on every PR to `main` / `release/*`:

```yaml
# .github/workflows/masvs-gate.yml
name: MASVS L1 Gate
on:
  pull_request:
    branches: [main, release/**]

jobs:
  masvs-l1:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Dependency vulnerability scan (OSV Scanner)
        run: |
          osv-scanner --format json --output dependency-scan.json .
          # Fail on CVSS >= 9.0 (Critical)
          python scripts/check-osv-severity.py dependency-scan.json --fail-on CRITICAL

      - name: SAST scan (Semgrep)
        run: |
          semgrep --config p/owasp-top-ten \
                  --config p/secrets \
                  --config p/mobile-masvs \
                  --json --output semgrep-results.json .
          # Fail on ERROR severity; WARNING is advisory only
          python scripts/check-semgrep.py semgrep-results.json --fail-on error

      - name: Upload compliance artifacts
        uses: actions/upload-artifact@v4
        with:
          name: masvs-l1-evidence
          path: |
            dependency-scan.json
            semgrep-results.json
```

### CVSS Severity Policy

| CVSS Range | Classification       | Pipeline Action                                                |
| ---------- | -------------------- | -------------------------------------------------------------- |
| 9.0–10.0   | Critical             | Block merge immediately; Thomas notifies CSO within 4 hours    |
| 7.0–8.9    | High                 | Block merge; Thomas + CSO decide fix-or-accept within 24 hours |
| 4.0–6.9    | Medium               | Advisory; tracked in security backlog; CSO reviews quarterly   |
| 0.1–3.9    | Low                  | Logged; no blocking action                                     |
| 0.0        | None / Informational | No action                                                      |

## PII-in-Logs Scanner

GDPR requires that PII never appears in application logs. Thomas operates a PII-detection Semgrep rule as part of the SAST pipeline:

```yaml
# semgrep rule: pii-in-logs
rules:
  - id: pii-in-logs
    patterns:
      - pattern: log.*(email|password|ssn|credit_card|phone|address)
      - pattern: logger.*(email|password|ssn|credit_card|phone|address)
      - pattern: console.log(..."$USER_EMAIL"...)
    message: >
      Potential PII in log statement. Remove PII or replace with a non-identifying
      correlation ID before merging.
    severity: ERROR
    languages: [kotlin, java, swift, typescript, python]
```

Any `ERROR` from this rule blocks the PR. Thomas reviews suppressions (`# nosemgrep`) monthly and reports them to the CSO.

## SOC 2 Audit Trail

Thomas maintains the infrastructure audit trail required for SOC 2 compliance:

| Audit Evidence                | Source                                      | Retention | Location             |
| ----------------------------- | ------------------------------------------- | --------- | -------------------- |
| CI/CD pipeline execution logs | GitHub Actions                              | 12 months | S3 compliance bucket |
| Environment access logs       | IAM / Cloud provider audit logs             | 24 months | S3 compliance bucket |
| Infrastructure change log     | Terraform state history / GitHub PR history | 36 months | Git + S3             |
| Secrets rotation log          | Vault audit log                             | 24 months | S3 compliance bucket |
| Deployment approval history   | GitHub required reviewers log               | 12 months | GitHub               |

Thomas runs a monthly automated job to verify all logs are being written to the compliance bucket and that none have been tampered with (SHA-256 integrity verification).

## Stage 8 Compliance Evidence Package

For every Stage 8 (Integrity Verification), Thomas produces a **Compliance Evidence Package** and delivers it to the CSO and CIO:

```markdown
# Compliance Evidence Package — [Release Version]

**Date:** YYYY-MM-DD
**Prepared by:** Thomas Zhang, DevOps Lead
**Build SHA:** [commit hash]
**Reviewed by CSO:** [pending / YYYY-MM-DD sign-off]

## MASVS Gate Results

| Scan                     | Last Run | Status  | Findings                                             |
| ------------------------ | -------- | ------- | ---------------------------------------------------- |
| OSV dependency scan      | [date]   | ✅ PASS | 0 Critical, 2 Medium (accepted, tracked in #SEC-123) |
| Semgrep SAST             | [date]   | ✅ PASS | 0 ERROR, 3 WARNING (advisory)                        |
| MASVS L2 (if applicable) | [date]   | ✅ PASS | 0 findings                                           |

## GDPR Controls

- [ ] PII-in-logs scan: PASS (0 violations)
- [ ] Data retention enforcement: PASS (confirmed in staging)
- [ ] DSAR fulfillment endpoint: tested and operational

## PCI DSS Controls (if applicable)

- [ ] No raw PAN in codebase (Semgrep scan): PASS
- [ ] TLS 1.3 enforced on all payment endpoints: PASS
- [ ] Payment scope isolation: PASS

## SOC 2 Audit Trail

- [ ] All audit log streams writing to compliance bucket: PASS
- [ ] Log integrity verification (SHA-256): PASS
- [ ] No unauthorized environment access in trailing 30 days: PASS

## Open Findings

| Finding                  | Severity | Status                        | Owner        |
| ------------------------ | -------- | ----------------------------- | ------------ |
| [CVE-XXXX-XXXX] in lib X | Medium   | Accepted (no patch available) | CSO sign-off |
```

## Coordination with CSO and CIO

| Situation                  | Thomas's Action                                                  | Response SLA               |
| -------------------------- | ---------------------------------------------------------------- | -------------------------- |
| CVSS Critical finding      | Notify CSO + CIO via Slack #security-incidents; block deployment | 4 hours                    |
| CVSS High finding          | File Jira security ticket; tag CSO; notify CIO                   | 24 hours                   |
| Monthly MASVS summary      | Email to CSO + CIO with findings trend                           | First Monday of each month |
| Stage 8 compliance package | Deliver to CSO + CIO at least 48 hours before the review         | 48 hours before Stage 8    |

## Quality Standards

- MASVS L1 gate runs on every PR to main/release branches without exception
- Zero Critical CVSSs accepted in any release build — escalate immediately if found
- SOC 2 audit log integrity verified monthly; any integrity failure is P0
- Stage 8 compliance evidence package delivered 48 hours before review
- All semgrep `# nosemgrep` suppressions reviewed monthly by Thomas and reported to CSO
