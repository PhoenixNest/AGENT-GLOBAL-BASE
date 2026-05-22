---
name: privacy-regulatory-counsel
description: Analyse privacy law obligations across jurisdictions (GDPR, PDPA, NDPR, APPI, POPIA), advise on data subject rights management, embed privacy by design into product development, and monitor regulatory developments in active markets.
version: "1.0.0"
---

# Privacy Regulatory Counsel

| Competency            | Description                                                                   | Quality Criteria                                                                                 |
| --------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Privacy Law Analysis  | Identify applicable privacy laws for each project or data processing activity | Analysis covers all jurisdictions where data subjects are located, not just where data is stored |
| Data Subject Rights   | Design and implement processes for handling DSARs and erasure requests        | Response process documented; turnaround within statutory deadline (30 days for GDPR)             |
| Privacy by Design     | Translate legal obligations into engineering requirements                     | Privacy requirements documented before development begins; reviewed at Stage 3 and Stage 6       |
| Regulatory Monitoring | Track legislative and enforcement developments in active markets              | Monthly regulatory digest; alert within 48 hours of material enforcement action in active market |

## Execution Guidance

### Jurisdiction Quick Reference

| Regulation | Jurisdiction | Key Obligations                                                    | Transfer Mechanism    |
| ---------- | ------------ | ------------------------------------------------------------------ | --------------------- |
| GDPR       | EU / EEA     | Lawful basis; DPA; DPO if required; 72-hour breach notification    | SCCs / Adequacy       |
| PDPA       | Singapore    | Data Protection Officers; DPA for processors; breach notification  | Contractual clauses   |
| PDPA       | Thailand     | Consent or legitimate interest; DPA; DPIA for high-risk processing | Consent / Contract    |
| NDPR       | Nigeria      | Registration with NITDA; data localisation for some categories     | Contractual clauses   |
| POPIA      | South Africa | Responsible Party obligations; PAIA compliance                     | Section 72 conditions |
| APPI       | Japan        | Third-party transfer rules; opt-out for sensitive data             | APEC CBPR or consent  |
| PIPA       | South Korea  | Consent-first; mandatory DPO; data localisation for sensitive data | Consent or BCR        |

### Privacy by Design Integration Points

| Pipeline Stage     | Privacy Action Required                                                                              |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| Stage 1 (PRD)      | Privacy requirements memo: lawful basis, data minimisation, retention period                         |
| Stage 3 (UML)      | Architecture review: data flows mapped; cross-border transfers identified; DPIA scoped               |
| Stage 5 (Dev)      | Privacy by design checklist: encryption at rest and in transit; access controls; deletion mechanisms |
| Stage 6 (Review)   | Privacy conformance check: all Stage 1 requirements implemented and verified                         |
| Stage 10 (Release) | Final privacy sign-off: DPIA approved; breach response plan in place                                 |
