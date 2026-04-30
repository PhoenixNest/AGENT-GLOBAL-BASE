# Cyberspace Security Department

Responsible for technology evaluation, architecture strategy, security requirements, risk assessment, and platform security compliance. The department produces two of the pipeline's foundational documents (SRD at Stage 1, ADRs + TSD at Stage 3) and reviews all subsequent stages for security and architectural integrity.

> Reports to the Chief Security Officer (CSO) and the Chief Information Officer (CIO).

---

## Supervisors

| Name            | Role                            | Seniority | Profile                                                                                                     |
| --------------- | ------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------- |
| Dr. Priya Mehta | Chief Information Officer (CIO) | C-suite   | [`profile.md`](../../departments/cyberspace-security/supervisor/chief-information-officer/agent/profile.md) |
| Dr. Sarah Chen  | Chief Security Officer (CSO)    | C-suite   | [`profile.md`](../../departments/cyberspace-security/supervisor/chief-security-officer/agent/profile.md)    |

**CIO Skills:**

| Skill File                                                                                                                                                       | Purpose                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| [`technology-evaluation.md`](../../departments/cyberspace-security/supervisor/chief-information-officer/skills/technology-evaluation.md)                         | Comparative technology analysis, TCO assessments, vendor lock-in evaluation, migration risk matrices   |
| [`mobile-architecture-strategy.md`](../../departments/cyberspace-security/supervisor/chief-information-officer/skills/mobile-architecture-strategy.md)           | Mobile architecture strategy and platform selection guidance                                           |
| [`technical-selection-documentation.md`](../../departments/cyberspace-security/supervisor/chief-information-officer/skills/technical-selection-documentation.md) | Technology Selection Document (TSD) authorship: explicit recommendations with success/failure criteria |

**CSO Skills:**

| Skill File                                                                                                                                              | Purpose                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`mobile-security-architecture.md`](../../departments/cyberspace-security/supervisor/chief-security-officer/skills/mobile-security-architecture.md)     | Mobile security architecture design for iOS and Android platforms                                                                                     |
| [`application-security-hardening.md`](../../departments/cyberspace-security/supervisor/chief-security-officer/skills/application-security-hardening.md) | Encryption, secure storage, iOS Keychain / Android Keystore, OWASP MASVS compliance                                                                   |
| [`security-risk-assessment.md`](../../departments/cyberspace-security/supervisor/chief-security-officer/skills/security-risk-assessment.md)             | Privacy obligations, data handling constraints, authentication requirements, GDPR/CCPA compliance                                                     |
| [`emerging-threat-evaluation.md`](../../departments/cyberspace-security/supervisor/chief-security-officer/skills/emerging-threat-evaluation.md)         | Threat landscape analysis and proactive security requirement definition                                                                               |
| [`security-requirements-and-srd.md`](../../departments/cyberspace-security/supervisor/chief-security-officer/skills/security-requirements-and-srd.md)   | Stage 1 SRD authorship: data asset inventory, STRIDE threat modelling, SR-NNN requirements with pipeline traceability, compliance obligations mapping |

---

## Team Members

| Name            | Role                   | Pipeline Stages | Skills                                                                    | Profile                                                                                                                   |
| --------------- | ---------------------- | --------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| James Wright    | Lead Security Engineer | 1, 6, 8, 10     | `security-operations`                                                     | [`profile.md`](../../departments/cyberspace-security/team/teammates/lead-security-engineer/james-wright/agent/profile.md) |
| Natalia Petrova | Security Architect     | 1, 3, 6, 8, 10  | `threat-modeling`                                                         | [`profile.md`](../../departments/cyberspace-security/team/teammates/security-architect/natalia-petrova/agent/profile.md)  |
| Sana Khoury     | Security Engineer #1   | 1, 6, 8, 10     | `mobile-penetration-testing`, `owasp-masvs-compliance`                    | [`profile.md`](../../departments/cyberspace-security/team/teammates/security-engineer/sana-khoury/agent/profile.md)       |
| Omar Farouq     | Security Engineer #2   | 1, 6, 8, 10     | `sast-dast-pipeline`, `web-application-security`                          | [`profile.md`](../../departments/cyberspace-security/team/teammates/security-engineer/omar-farouq/agent/profile.md)       |
| Li Wei Chen     | Security Engineer #3   | 1, 6, 8, 10     | `supply-chain-security`, `secure-coding-training`                         | [`profile.md`](../../departments/cyberspace-security/team/teammates/security-engineer/li-wei-chen/agent/profile.md)       |
| Leila Khoury    | DevOps Engineer        | 1, 6, 8, 10     | `aws-monitoring`, `secrets-management`                                    | [`profile.md`](../../departments/cyberspace-security/team/teammates/devops-engineer/leila-khoury/agent/profile.md)        |
| Yuki Matsuda    | DevOps Engineer        | 1, 6, 8, 10     | `cicd-security`, `infrastructure-as-code`                                 | [`profile.md`](../../departments/cyberspace-security/team/teammates/devops-engineer/yuki-matsuda/agent/profile.md)        |
| Ingrid Solberg  | Compliance Analyst     | 1, 6, 8, 10     | `compliance-auditing`, `owasp-masvs-auditing`, `compliance-documentation` | [`profile.md`](../../departments/cyberspace-security/team/teammates/compliance-analyst/ingrid-solberg/agent/profile.md)   |

---

## Pipeline Stages

| Stage                                             | Role                                                                                                                                                                                                                                      |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 1** — Requirements → PRD + SRD            | **CSO: Responsible Producer.** Produces the Security Requirements Document (SRD) covering privacy obligations, data handling, authentication, encryption, and platform-specific security requirements. Reviews PRD alongside CIO and CTO. |
| **Stage 3** — Prototype → UML Engineering Package | **CIO: Responsible Producer** (ADRs + TSD). Produces Architecture Decision Records and Technology Selection Document. CIO and CTO jointly review all deliverables for feasibility.                                                        |
| **Stage 6** — Code Review                         | **Both: Reviewers.** CSO owns the security review criterion: encryption, secure storage (Keychain/Keystore), and OWASP MASVS compliance. CIO reviews architectural conformance.                                                           |
| **Stage 8** — Integrity Verification              | **Both: Reviewers.** Verify that remediation did not silently remove security or architectural requirements.                                                                                                                              |
| **Stage 10** — Release Readiness Check            | **CSO sign-off:** SRD enforced, OWASP MASVS compliant. **CIO sign-off (with CTO):** All UML/ADR/TSD standards upheld.                                                                                                                     |

---

## Key Artifacts Produced

- **Security Requirements Document (SRD)** — Paired with the PRD from Stage 1. Travels with the PRD through all subsequent stages.
- **Architecture Decision Records (ADRs)** — Documents technology choices with rationale, trade-offs, and explicit success/failure criteria.
- **Technology Selection Document (TSD)** — Comparative analysis with TCO assessments, vendor lock-in evaluation, and technology recommendations.

---

## Reference Links

See [`reference/development/links.md`](../reference/development/links.md) for OWASP MASVS, platform security documentation, and development references.

For cross-cutting security guidance, see [`topics/security.md`](../topics/security.md).
