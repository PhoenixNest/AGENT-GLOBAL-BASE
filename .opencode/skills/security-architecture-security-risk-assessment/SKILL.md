---
name: security-architecture-security-risk-assessment
description: Security risk assessment for mobile apps — threat modelling (STRIDE), penetration testing oversight, OWASP MASVS evaluation, PCI-DSS, GDPR/CCPA, security architecture reviews, P0–P3 defect classification for security findings. Owned by Dr. Sarah Chen (CSO). Use during Stage 1 (Requirements) for SRD risk assessment and Stage 6 (Code Review) for security defect classification. Trigger: security risk assessment, STRIDE, penetration testing, MASVS evaluation, PCI-DSS, GDPR, CCPA, security architecture review, P0 P1 P2 P3 classification.
prerequisites:
  - security-overview

version: "1.0.0"
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

### 3. Penetration Testing Oversight

**Testing Scope:**

- Static analysis (SAST)
- Dynamic analysis (DAST)
- Manual penetration testing
- API security testing
- Network security assessment

**Vendor Management:**

- Define testing scope and rules of engagement
- Review tester credentials
- Monitor testing progress
- Validate findings
- Track remediation

## Compliance Standards

### OWASP MASVS (Mobile Application Security Verification Standard)

**Level 1 (Standard Security):**

- Basic security controls
- Industry best practices
- Suitable for most apps

**Level 2 (Defense in Depth):**

- Advanced security controls
- Threat modeling required
- For apps handling sensitive data

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

**Requirements:**

- Secure transmission of payment data
- Secure storage prohibition
- Strong cryptography
- Secure authentication
- Regular security testing

### Regulatory Compliance

**GDPR (EU):**

- Data protection by design
- Privacy impact assessments
- Breach notification requirements
- User consent management

**CCPA (California):**

- Consumer data rights
- Opt-out mechanisms
- Data inventory and mapping

## Security Review Process

### Pre-Launch Security Review

**Phase 1: Documentation Review**

- Security architecture document
- Threat model
- Data flow diagrams
- Privacy impact assessment

**Phase 2: Code Review**

- Security-critical code paths
- Cryptographic implementations
- Authentication/authorization logic
- Data handling practices

**Phase 3: Testing**

- Automated security scanning
- Manual penetration testing
- Compliance verification
- Performance impact assessment

**Phase 4: Sign-off**

- Risk acceptance documentation
- Remediation plan for known issues
- Launch approval criteria

## Collaboration Framework

**With CTO:** Integrate security reviews into development lifecycle

**With CIO:** Align security standards with technology strategy

**With Legal/Compliance:** Ensure regulatory compliance

**With Product:** Balance security requirements with user experience

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
