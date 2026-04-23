---
name: company-security-risk-assessment
description: Security risk assessment and compliance for mobile apps — threat modelling (STRIDE), penetration testing oversight, OWASP MASVS evaluation, PCI-DSS, GDPR/CCPA, security architecture reviews, P0–P3 defect classification for security findings. Owned by Dr. Sarah Chen (CSO).
disable-model-invocation: false
---

# Security Risk Assessment & Compliance

## Purpose

Establish systematic security risk assessment processes, conduct threat modeling, oversee penetration testing, and ensure compliance with mobile security standards and regulatory requirements.

## Core Assessment Framework

### 1. Threat Modeling

**STRIDE Methodology:**

- **S**poofing — identity verification weaknesses
- **T**ampering — data integrity vulnerabilities
- **R**epudiation — audit trail gaps
- **I**nformation Disclosure — data leakage risks
- **D**enial of Service — availability threats
- **E**levation of Privilege — authorization bypasses

**Process:**

1. Map data flows and trust boundaries
2. Identify assets and entry points
3. Enumerate threats per component
4. Assess likelihood and impact
5. Prioritize mitigation strategies

### 2. Risk Scoring

**CVSS v3.1 Framework:**

- Base Score: exploitability + impact
- Temporal Score: exploit maturity + remediation level
- Environmental Score: business context

**Risk Matrix:**

- Critical (9.0-10.0): immediate action required
- High (7.0-8.9): fix within 7 days
- Medium (4.0-6.9): fix within 30 days
- Low (0.1-3.9): fix in next release

**Pipeline mapping:** Security vulnerabilities map to P0–P3 severity — a security breach is always P0, a minor security gap is P2/P3 (user decides).

### 3. Penetration Testing Oversight

**Testing Scope:** Static analysis (SAST); dynamic analysis (DAST); manual penetration testing; API security testing; network security assessment.

**Vendor Management:** Define testing scope and rules of engagement; review tester credentials; monitor testing progress; validate findings; track remediation.

## Compliance Standards

### OWASP MASVS (Mobile Application Security Verification Standard)

**Level 1 (Standard Security):** Basic security controls; industry best practices; suitable for most apps.

**Level 2 (Defense in Depth):** Advanced security controls; threat modeling required; for apps handling sensitive data.

**Verification Categories:**

- V1: Architecture, Design and Threat Modeling
- V2: Data Storage and Privacy
- V3: Cryptography
- V4: Authentication and Session Management
- V5: Network Communication
- V6: Platform Interaction
- V7: Code Quality and Build Settings
- V8: Resilience Against Reverse Engineering

### PCI Mobile Payment Security

Requirements: Secure transmission of payment data; secure storage prohibition; strong cryptography; secure authentication; regular security testing.

### Regulatory Compliance

**GDPR (EU):** Data protection by design; privacy impact assessments; breach notification requirements; user consent management.

**CCPA (California):** Consumer data rights; opt-out mechanisms; data inventory and mapping.

## Security Review Process

### Pre-Launch Security Review

**Phase 1: Documentation Review** — security architecture document, threat model, data flow diagrams, privacy impact assessment.

**Phase 2: Code Review** — security-critical code paths, cryptographic implementations, authentication/authorization logic, data handling practices.

**Phase 3: Testing** — automated security scanning, manual penetration testing, compliance verification, performance impact assessment.

**Phase 4: Sign-off** — risk acceptance documentation, remediation plan for known issues, launch approval criteria.

## Key Deliverables

1. **Threat Model Documents** — STRIDE analysis with mitigation strategies
2. **Penetration Test Reports** — findings, risk scores, remediation guidance
3. **Compliance Audit Reports** — OWASP MASVS/PCI-DSS assessment results
4. **Security Review Sign-off** — launch approval with risk documentation

## Success Metrics

- 100% of features undergo security review before launch
- All critical/high vulnerabilities remediated before production
- Zero compliance violations in audits
- <30 day average time to remediate medium-risk findings
