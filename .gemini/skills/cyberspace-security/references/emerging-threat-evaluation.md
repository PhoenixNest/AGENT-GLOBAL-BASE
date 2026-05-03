---
name: emerging-threat-evaluation
description: Evaluate security implications of emerging mobile technologies, conduct threat intelligence research, and provide early risk identification for new platforms and capabilities
version: "1.0.0"
---

# Emerging Threat Evaluation

## Purpose

Continuously monitor and evaluate security implications of emerging mobile technologies, identify threats before they become widespread, and provide strategic guidance on adopting new capabilities securely.

## Why This Matters

Identifies security risks 6-12 months before they become mainstream threats. Quarterly threat landscape assessments prevent reactive patching and enable proactive architecture adjustments.

## Emerging Technology Assessment

### 1. Technology Monitoring

**Focus Areas:**

- 5G and edge computing security
- On-device machine learning privacy
- eSIM and digital identity
- Passkeys and passwordless authentication
- Mobile payment innovations (NFC, QR codes)
- AR/VR security considerations
- Cross-device synchronization
- App Clips / Instant Apps security

### 2. Security Evaluation Framework

**Assessment Criteria:**

1. **Attack Surface Analysis** — new entry points and vulnerabilities
2. **Privacy Implications** — data collection and user tracking risks
3. **Platform Maturity** — security feature completeness
4. **Threat Actor Interest** — likelihood of exploitation
5. **Mitigation Availability** — existing security controls

### 3. Threat Intelligence

**Intelligence Sources:**

- CVE databases and security advisories
- Platform security bulletins (Apple, Google)
- Security research publications
- Bug bounty program trends
- Dark web monitoring
- Threat actor TTPs (tactics, techniques, procedures)

**Analysis Output:**

- Quarterly threat landscape reports
- Technology-specific risk assessments
- Early warning alerts for emerging threats
- Competitive security intelligence

## Risk Identification Process

### Phase 1: Technology Discovery

1. Monitor platform announcements (WWDC, Google I/O)
2. Track beta releases and developer previews
3. Review security research papers
4. Engage with security community

### Phase 2: Security Analysis

1. Analyze security model and controls
2. Identify potential vulnerabilities
3. Assess privacy implications
4. Evaluate compliance impact

### Phase 3: Risk Assessment

1. Determine likelihood of exploitation
2. Assess potential business impact
3. Identify mitigation strategies
4. Calculate risk score

### Phase 4: Recommendation

1. Adoption timeline guidance
2. Security requirements definition
3. Implementation best practices
4. Monitoring and validation plan

## Collaboration Points

**With CIO:** Align security evaluation with technology strategy

**With CTO:** Integrate security requirements into architecture decisions

**With Product:** Balance innovation with security risk tolerance

## Key Deliverables

1. **Quarterly Threat Landscape Reports** — emerging threats and trends
2. **Technology Security Assessments** — risk analysis for new capabilities
3. **Early Warning Alerts** — critical threat notifications
4. **Security Adoption Guides** — best practices for new technologies

## When to Use This Skill

Use this skill when:

- The CTO proposes adopting a new mobile technology, SDK, or platform capability in a Stage 3 ADR/TSD
- A new CVSS 9.0+ vulnerability affecting the mobile platform is published
- A major platform update (iOS/Android major version, new hardware capability) is announced
- A peer company announces a security breach involving a technology the company uses or is evaluating
- Quarterly threat landscape review is due

Do **not** wait for the CTO to trigger this skill. The CSO proactively monitors and surfaces assessments — the CTO should receive the threat landscape report before the quarterly ADR review cycle, not after.

## Trigger → Deliverable SLA

| Trigger                                                 | Deliverable                          | SLA                                       |
| ------------------------------------------------------- | ------------------------------------ | ----------------------------------------- |
| CTO proposes new technology in Stage 3 ADR              | Security assessment memo             | 3 business days from ADR draft receipt    |
| CVSS 9.0+ vulnerability published for in-use technology | Early Warning Alert to CTO + CIO     | 4 hours of public disclosure              |
| New iOS/Android major version announced                 | Platform security changelog briefing | 2 weeks before developer preview deadline |
| Quarterly review cycle                                  | Quarterly Threat Landscape Report    | Last business day of each quarter         |
| Peer company breach in relevant technology              | Ad-hoc threat assessment             | 5 business days                           |

## Assessment Report Format

Every Emerging Threat Assessment follows this structure:

```markdown
# Emerging Threat Assessment: [Technology/Threat Name]

**Date:** YYYY-MM-DD
**Assessed by:** Dr. Sarah Chen, CSO
**Trigger:** [What prompted this assessment]
**Urgency:** Critical (4h) | Standard (3 days) | Quarterly (scheduled)

## Executive Summary (3 sentences max)

[What is the threat, what is the business impact, what action is recommended]

## Threat Description

[Technical summary of the threat or technology — 2–4 paragraphs]

## Risk Score

| Dimension                  | Score (1-5) | Rationale |
| -------------------------- | ----------- | --------- |
| Likelihood of exploitation | X           | [reason]  |
| Impact if exploited        | X           | [reason]  |
| Detection difficulty       | X           | [reason]  |
| Mitigation feasibility     | X           | [reason]  |
| **Composite Risk**         | **X.X**     |           |

Risk classification: ≥4.0 = Critical | 3.0–3.9 = High | 2.0–2.9 = Medium | <2.0 = Low

## Affected Systems / Features

[Which company products, features, or infrastructure are affected]

## Recommended Mitigations

1. [Specific, actionable mitigation — who does it, by when]
2. [Second mitigation]
3. [Monitoring recommendation]

## Implementation Guidance

[Architecture notes, code references, configuration changes — specific enough for the CTO to action immediately]

## Adoption Recommendation (for new technology assessments)

[ ] Adopt now — risk acceptable, mitigations implemented
[ ] Adopt after mitigations — specific gates required
[ ] Defer — risk too high until [specific condition]
[ ] Do not adopt — fundamental security incompatibility
```

## Success Metrics

- Identify security risks 6-12 months before mainstream adoption
- Zero security incidents from newly adopted technologies
- 100% of emerging technologies assessed before production use
- All assessments delivered within SLA — tracked in Jira with `security-assessment` label
- Quarterly Threat Landscape Report delivered by last business day of each quarter without exception
