---
name: privacy-regulatory-counsel
description: Privacy law analysis and advisory for the Associate Counsel. Use when advising on GDPR, PDPA (Singapore / Thailand), NDPR (Nigeria), POPIA (South Africa), CCPA, or other data protection laws; when assessing data subject rights obligations; when a regulatory inquiry or enforcement action is received; when privacy-by-design requirements need to be embedded in a product specification; or when monitoring legislative changes in jurisdictions where the company operates.
version: "1.0.0"
---

# Privacy Regulatory Counsel

## Purpose

Privacy law is not a checklist — it is a risk framework that must be applied to the specific data flows, processing purposes, and jurisdictional footprint of each product. The goal is not formal compliance (ticking boxes) but genuine protection of data subjects' rights, which in turn protects the company from regulatory sanction and reputational harm. This skill gives the Associate Counsel a structured, law-specific approach to privacy analysis that produces actionable guidance rather than hedged opinions.

---

## Privacy Law Quick-Reference Index

For each jurisdiction where the company processes personal data, apply the applicable law framework:

### GDPR (EU / EEA)

| Key Element            | Requirement                                                                                                                                     |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Lawful basis           | One of 6 bases required for every processing activity (consent, contract, legal obligation, vital interests, public task, legitimate interests) |
| Data subject rights    | Access, rectification, erasure, portability, restriction, objection, right not to be subject to automated decisions                             |
| DPO requirement        | Mandatory if large-scale processing of special categories or systematic monitoring                                                              |
| Breach notification    | Supervisory authority within 72 hours; data subjects if high risk                                                                               |
| Cross-border transfers | Adequacy, SCCs, BCRs, derogations                                                                                                               |
| Maximum penalty        | €20M or 4% of global annual turnover, whichever is higher                                                                                       |

### PDPA — Singapore

| Key Element            | Requirement                                                                                  |
| ---------------------- | -------------------------------------------------------------------------------------------- |
| Consent                | Default basis; legitimate interests available but narrower than GDPR                         |
| Notification           | Purpose must be notified at or before collection                                             |
| Access and correction  | Individuals have access and correction rights                                                |
| Data portability       | Mandatory data portability right under 2021 amendments                                       |
| Cross-border transfers | Comparable protection required (adequacy or contractual obligation)                          |
| Breach notification    | Personal Data Protection Commission (PDPC) within 3 calendar days if significant harm likely |

### NDPR — Nigeria

| Key Element            | Requirement                                                                                   |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| Consent                | Explicit, informed, revocable                                                                 |
| Data minimisation      | Collect only what is necessary                                                                |
| Cross-border transfers | Lawful only if receiving country provides adequate protection or contractual safeguards exist |
| Government data        | Additional restrictions on government-held data                                               |
| Breach notification    | NITDA within 72 hours                                                                         |

### APPI — Japan

| Key Element            | Requirement                                                                        |
| ---------------------- | ---------------------------------------------------------------------------------- |
| Purpose specification  | Processing purpose must be specified and communicated to data subjects             |
| Third-party provision  | Consent required for most third-party sharing; opt-out for indirect transfer       |
| Cross-border transfers | Consent or use of a personal information protection commission-compliant framework |
| Anonymisation          | Strict anonymisation standard before data loses "personal information" status      |

---

## Privacy by Design — Advisory Protocol

When a new product feature or system architecture is proposed, apply the Privacy by Design advisory before any technical specification is finalised:

### Seven Foundational Principles (Applied)

1. **Proactive, not reactive** — Identify privacy risks before design is complete, not after implementation. The cost of a late-stage privacy remediation is 10–20× the cost of designing correctly upfront.

2. **Privacy as the default** — The default setting must be the most privacy-protective. Opt-in for data sharing, not opt-out. Collect the minimum data needed, not the maximum data possible.

3. **Privacy embedded in design** — Privacy is not a bolt-on feature. Data minimisation, purpose limitation, and retention deletion must be expressed in the system architecture — not in a policy document that sits beside the system.

4. **Full functionality** — Privacy and function are not zero-sum. Challenge any design decision that treats them as mutually exclusive.

5. **End-to-end lifecycle security** — Data must be protected from collection through deletion. Design for secure deletion, not just secure storage.

6. **Visibility and transparency** — Individuals must be able to see what data is held about them and how it is used. The privacy notice must be accurate, current, and intelligible.

7. **Respect for user privacy** — When in doubt, design for the interests of data subjects, not the interests of the data controller.

### Privacy Review Output

For each new product feature involving personal data, produce:

```
Privacy Review: [Product/Feature Name]
Date: [YYYY-MM-DD]
Reviewer: [Azalea Nkrumah, Associate Counsel]
Applicable Laws: [List each jurisdiction and applicable law]

Data Collected: [List each data element]
Processing Purpose: [State the specific, legitimate purpose]
Lawful Basis: [Per applicable law — confirm each]
Retention Period: [State specifically — "as long as needed" is not acceptable]
Third-Party Sharing: [Yes/No — if yes, list recipients and legal basis]
Cross-Border Transfer: [Yes/No — if yes, state mechanism]
Data Subject Rights: [How each right is honoured in the product]

Privacy Risks Identified: [List with severity]
Required Design Changes: [Specific changes to embed privacy by design]

Recommendation: [Approve / Approve with mandatory changes / Block pending redesign]
```

---

## Regulatory Monitoring

Maintain a live watch list for jurisdictions where the company operates. For each:

- Track proposed legislation that would affect data processing practices
- Flag enacted laws with a future compliance deadline
- Monitor enforcement actions and guidance from applicable data protection authorities
- Produce a quarterly regulatory change summary for the CLO

---

## Data Subject Rights Management

When a data subject request is received:

| Request Type  | Verification Required?       | Response Deadline (GDPR)   | Internal Process                                           |
| ------------- | ---------------------------- | -------------------------- | ---------------------------------------------------------- |
| Access (SAR)  | Identity verification        | 30 days (extendable to 90) | Route to product DRI for data extract                      |
| Rectification | Identity verification        | 30 days                    | Route to product DRI for data update                       |
| Erasure       | Identity + legitimate ground | 30 days                    | Assess if grounds exist; route to product DRI for deletion |
| Portability   | Identity verification        | 30 days                    | Route to product DRI for structured data export            |
| Objection     | Identity verification        | Without undue delay        | Assess legitimate grounds to continue processing           |

Log every data subject request in the privacy request register with: request type, date received, identity verified, response deadline, response date, outcome.

---

## Output Standards

- Every privacy opinion must identify the specific law, article, and recital (where applicable) relied upon. General references to "GDPR" without article citations are insufficient.
- Privacy by design recommendations must be expressed as technical requirements an engineer can implement — not as legal principles the engineer must interpret.
- When advising that a processing activity is lawful, state the lawful basis specifically. "Legitimate interests" requires a legitimate interests assessment (LIA) to document the balancing test.
