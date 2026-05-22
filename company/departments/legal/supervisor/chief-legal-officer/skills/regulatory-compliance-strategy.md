---
name: regulatory-compliance-strategy
description: Multi-jurisdictional regulatory compliance programme for the CLO. Use when the CLO must assess data sovereignty obligations, design a cross-border data transfer mechanism, respond to a regulatory inquiry, advise on market entry legal requirements, or produce a jurisdiction-by-jurisdiction compliance matrix for a product or project. Especially relevant for projects handling government data, transit data, infrastructure data, or sensitive personal data across national borders.
version: "1.0.0"
---

# Regulatory Compliance Strategy

## Purpose

Products that handle personal data, government data, or sensitive infrastructure data across national borders are governed by a patchwork of data sovereignty laws, sector-specific regulations, and government-access frameworks that vary significantly by jurisdiction. A single incorrect assumption — "our cloud provider stores data in Singapore, so Singapore law applies" — can result in a product being illegal to operate in its target market. This skill gives the CLO a systematic approach to identifying, mapping, and satisfying multi-jurisdictional legal obligations before they become blockers.

---

## Phase 1 — Jurisdiction and Data Mapping

Before any compliance analysis, establish the factual foundation:

### Step 1.1 — Data Flow Inventory

For each product or project, produce a data flow inventory:

| Data Element                    | Data Category        | Source Jurisdiction | Processing Location  | Storage Location     | Recipients               | Retention Period |
| ------------------------------- | -------------------- | ------------------- | -------------------- | -------------------- | ------------------------ | ---------------- |
| [e.g., passenger location data] | Personal / Sensitive | [e.g., Japan]       | [e.g., Singapore DC] | [e.g., Singapore DC] | [e.g., transit operator] | [e.g., 90 days]  |

**Data category classifications:**

- **Personal data** — any information relating to an identified or identifiable natural person
- **Sensitive personal data** — health, biometric, financial, location (continuous tracking), political opinion, criminal record
- **Government data** — data owned by or entrusted to a government entity; subject to additional sovereignty obligations
- **Critical infrastructure data** — data related to transport, utilities, communications, or financial systems; often regulated separately from personal data
- **Non-personal data** — aggregated, anonymised, or machine-generated data (verify anonymisation is irreversible)

### Step 1.2 — Applicable Law Matrix

For each data flow, identify every applicable law by jurisdiction:

| Jurisdiction   | Primary Data Law  | Sector Regulation                               | Cross-Border Transfer Mechanism                 | Localisation Requirement?          |
| -------------- | ----------------- | ----------------------------------------------- | ----------------------------------------------- | ---------------------------------- |
| European Union | GDPR              | [NIS2 if infrastructure]                        | SCCs / Adequacy Decision / BCRs                 | No (but transfer conditions apply) |
| Japan          | APPI              | [sector-specific if applicable]                 | Adequacy or Contractual Safeguards              | No                                 |
| South Korea    | PIPA              | [ISMS-P if applicable]                          | Data Transfer Agreement                         | Yes (certain sectors)              |
| Singapore      | PDPA              | [Cybersecurity Act if critical info-comm infra] | Contractual clause or adequacy                  | No                                 |
| China          | PIPL + DSL + CSL  | [MLPS if applicable]                            | SAMR SCC or CAC security assessment             | Yes (above threshold)              |
| Indonesia      | Law 27/2022 (PDP) | [SPBE if government data]                       | Government approval required for sensitive data | Yes (government and sensitive)     |
| India          | DPDP Act 2023     | [CERT-In if applicable]                         | Government whitelist (forthcoming)              | TBD (pending rules)                |

> This matrix is a starting point. Laws change. Before relying on any entry, verify current status from the applicable regulatory authority's official source.

---

## Phase 2 — Compliance Gap Analysis

For each applicable law, assess the company's current compliance status:

### Compliance Assessment Template

```
Jurisdiction:     [Country / Region]
Applicable Law:   [Law name and version]
Assessment Date:  [YYYY-MM-DD]
Assessor:         [CLO / Senior Counsel / External Counsel]

Obligations Identified:
1. [Obligation] — Status: [Compliant / Gap / Unknown]
   Gap Detail: [What is missing or unverified]
   Remediation: [Concrete action + owner + deadline]

2. [Obligation] — Status: [Compliant / Gap / Unknown]
   ...

Overall Status: [Green — compliant | Yellow — remediable gaps | Red — blocking issue]
External Counsel Required: [Yes / No] — [If yes, why]
```

**Common obligations to assess:**

- **Lawful basis for processing** — Is there a valid lawful basis (consent, legitimate interest, legal obligation, etc.) for every data processing activity?
- **Data subject rights** — Can the company honour access, rectification, erasure, portability, and objection requests within the legally required timeframe?
- **Cross-border transfer mechanism** — Is every cross-border data transfer covered by a valid transfer mechanism (SCCs, adequacy decision, binding corporate rules, consent)?
- **Data localisation** — Where required, is the data physically stored within the mandated jurisdiction?
- **Retention limits** — Does the company delete data when the legally mandated retention period expires?
- **Breach notification** — Does the company have a process to notify regulators within 72 hours (GDPR) or the applicable local window?
- **Data Protection Officer** — Is a DPO required by applicable law? If so, is one appointed?
- **Privacy by design** — Are data minimisation and purpose limitation embedded in the product architecture?

---

## Phase 3 — Remediation and Risk Acceptance

Classify each gap and route accordingly:

| Gap Severity | Definition                                                                | Response                                                                                            |
| ------------ | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **Blocking** | Cannot legally operate the product in this jurisdiction without resolving | Escalate to CLO + CTO + CPO. Do not launch until resolved.                                          |
| **High**     | Significant regulatory risk; likely sanction if discovered                | Resolve before launch; document risk-acceptance decision if business requires launch with known gap |
| **Medium**   | Remediable gap; low immediate risk but non-compliant                      | Remediate within 30 days post-launch; owner and deadline required                                   |
| **Low**      | Best-practice gap; no specific legal obligation breached                  | Add to compliance backlog; review quarterly                                                         |

For any gap the business chooses to accept (i.e., launch with known non-compliance), the CLO must produce a written Risk Acceptance Memo countersigned by the relevant C-suite DRI. The memo states: the gap, the applicable law, the probability of regulatory action, the estimated maximum penalty, the business rationale for accepting the risk, and the intended remediation timeline.

---

## Phase 4 — Government Data and Critical Infrastructure — Special Obligations

When a project involves government data or critical infrastructure (transit systems, utilities, communications):

1. **Confirm applicable sector regulation** — Most jurisdictions have specific sector laws governing critical infrastructure data that sit above general data protection law. Identify and map them explicitly.

2. **Assess government ownership claims** — Some jurisdictions treat data generated by or about government infrastructure as government-owned, regardless of who collected it. Confirm whether the government client retains ownership of data the company collects on their behalf.

3. **Map law-enforcement access obligations** — Governments frequently require that operators of critical infrastructure cooperate with law-enforcement access requests. Confirm the specific obligations (warrant required? administrative order? national security letter equivalent?) and ensure the company's legal team can respond appropriately.

4. **Security certification** — Critical infrastructure operators are often required to hold specific security certifications (ISO 27001, national equivalents). Confirm whether any certification is required and whether the company holds it.

5. **Data residency mandate** — Government data related to critical infrastructure is among the highest-risk categories for mandatory localisation. Verify the specific storage requirement before agreeing to any cross-border data architecture.

---

## Output Standards

- Every jurisdiction assessment must cite the specific law, regulation, or guidance document reviewed — not just the law's name but the article, section, or official guidance relied upon.
- Never characterise data as "anonymised" without reviewing the specific anonymisation technique against the applicable legal standard (GDPR Recital 26, or equivalent). Aggregation alone is frequently insufficient.
- When recommending external counsel, name the jurisdiction and the specific practice area required. "Get local counsel" is not actionable.
- Compliance matrices must include a version date and a review cadence. Laws change — an undated matrix is a liability, not an asset.
