# Security Coordination Charter

**Document Type:** Security Coordination Charter (RACI)
**Version:** 1.0
**Date:** April 3, 2026
**Authors:** CIO (Dr. Priya Mehta) + CSO (Dr. Sarah Chen)
**Purpose:** Define RACI matrices for security decisions across pipeline stages to prevent security vs. engineering friction at scale.
**Status:** ✅ Approved — RACI Audit In Progress (5 business days)

---

## Scope

This charter governs all security-related decisions across the 10-stage development pipeline for the 57-person engineering organization.

---

## RACI Definitions

| Code  | Meaning                                                  |
| ----- | -------------------------------------------------------- |
| **R** | Responsible — does the work                              |
| **A** | Accountable — owns the decision; one person per activity |
| **C** | Consulted — provides input before decision               |
| **I** | Informed — notified after decision                       |

---

## RACI Matrix by Pipeline Stage

### Stage 1: Requirements → PRD + SRD

| Activity                       | CSO  | CIO | CTO | CPO |
| ------------------------------ | ---- | --- | --- | --- |
| SRD authorship                 | A, R | C   | C   | I   |
| Privacy obligations            | A, R | C   | I   | C   |
| Platform security requirements | A, R | C   | C   | I   |
| Threat modeling (initial)      | A, R | C   | R   | C   |

### Stage 3: UML Engineering Package

| Activity                     | CSO | CIO  | CTO | Security Architect |
| ---------------------------- | --- | ---- | --- | ------------------ |
| Security architecture review | A   | R    | C   | R                  |
| ADR security implications    | C   | A, R | C   | R                  |
| TSD security assessment      | C   | A, R | C   | R                  |
| Cryptographic standards      | A   | C    | C   | R                  |

### Stage 5: Development

| Activity                     | CSO | CTO | Lead Security Engineer | Security Engineers | Security Champions |
| ---------------------------- | --- | --- | ---------------------- | ------------------ | ------------------ |
| Secure coding standards      | A   | C   | R                      | R                  | I                  |
| PR security review           | I   | I   | A                      | R                  | R                  |
| Dependency security scanning | I   | I   | A                      | R                  | I                  |
| Supply chain security        | I   | I   | A                      | R                  | I                  |
| Secrets management           | A   | I   | R                      | R                  | I                  |

### Stage 6: Code Review

| Activity                         | CSO  | CTO | CPO | Security Engineers |
| -------------------------------- | ---- | --- | --- | ------------------ |
| Security code review             | A, R | C   | I   | R                  |
| OWASP MASVS compliance check     | A, R | I   | C   | R                  |
| Penetration testing coordination | A    | I   | R   | R                  |
| Defect classification (security) | A    | C   | C   | R                  |

### Stage 7: Automated Testing

| Activity                       | CSO  | CTO | Test Lead | Security Engineers |
| ------------------------------ | ---- | --- | --------- | ------------------ |
| Security test case inclusion   | A, R | C   | R         | R                  |
| SAST/DAST pipeline integration | I    | C   | I         | R                  |
| Security regression testing    | A    | C   | R         | R                  |

### Stage 8: Integrity Verification

| Activity                        | CSO  | CTO | CPO | Security Engineers |
| ------------------------------- | ---- | --- | --- | ------------------ |
| Security integrity verification | A, R | C   | I   | R                  |
| SRD enforcement verification    | A, R | C   | I   | R                  |
| Anti-tampering verification     | A    | C   | I   | R                  |

### Stage 10: Release Readiness

| Activity                  | CSO  | CTO | CPO | Compliance Analyst |
| ------------------------- | ---- | --- | --- | ------------------ |
| Security release sign-off | A, R | C   | I   | R                  |
| OWASP MASVS final audit   | A    | I   | C   | R                  |
| Compliance documentation  | I    | I   | A   | R                  |

---

## Ongoing Security Activities

| Activity                       | CSO | CIO | CTO | Security Architect | Security Engineers |
| ------------------------------ | --- | --- | --- | ------------------ | ------------------ |
| Vulnerability management       | A   | I   | I   | C                  | R                  |
| Incident response              | A   | C   | C   | C                  | R                  |
| Security training              | A   | I   | C   | R                  | I                  |
| External pen test coordination | A   | I   | I   | C                  | R                  |
| Security tool evaluation       | A   | C   | C   | R                  | I                  |
| Compliance audit (SOC2, GDPR)  | A   | C   | I   | C                  | R                  |

---

## Escalation Protocol

### Security vs. Engineering Disputes

| Level       | Parties                                          | Timeline       |
| ----------- | ------------------------------------------------ | -------------- |
| **Level 1** | Security Champion + Chapter Lead                 | 24 hours       |
| **Level 2** | Lead Security Engineer + VP of relevant division | 48 hours       |
| **Level 3** | CSO + CTO                                        | 72 hours       |
| **Level 4** | User (P0/P1 security defects only)               | Final decision |

### Security Block Authority

| Role                       | Authority                                                      |
| -------------------------- | -------------------------------------------------------------- |
| **CSO**                    | Can block any pipeline stage for security reasons              |
| **Lead Security Engineer** | Can block development for critical vulnerabilities (CVSS 9.0+) |
| **Security Engineers**     | Can block PRs for security violations                          |
| **Security Champions**     | Can flag PRs for security review                               |

---

## Review Cycle

This charter is reviewed:

- Quarterly by CSO + CIO
- After any security incident
- When new pipeline stages are added
- When organizational structure changes

---

## v1.6 Note: CISO Role Transition

This charter originally referenced a standalone CISO role. Per the v1.6 recruitment plan (Option C confirmed), the CISO role has been replaced:

- **CSO (Dr. Sarah Chen)** holds dual CSO/CISO title during the scaling period (until 150 engineers)
- **Lead Security Engineer** (Phase 1 hire) assumes operational "A" and "R" responsibilities previously assigned to CISO in Stage 5 and 7 activities
- All Stage 1, 3, 6, 8, and 10 "A" (Accountable) assignments remain with CSO
- A full RACI audit of all entries is being conducted by CSO + CIO within 5 business days of plan approval
