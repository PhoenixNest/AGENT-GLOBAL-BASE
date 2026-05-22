---
name: technology-transactions
description: Technology agreement review and negotiation for the CLO. Use when the CLO must review, draft, or negotiate technology contracts including SaaS agreements, software licensing, API access agreements, cloud infrastructure contracts, IP assignments, NDAs, government procurement contracts, or data processing agreements. Also use when advising on vendor legal framework strategy, evaluating contract risk, or structuring IP ownership in a technology development engagement.
version: "1.0.0"
---

# Technology Transactions

## Purpose

Technology agreements are not generic commercial contracts — they carry platform lock-in risk, IP ownership ambiguity, data handling obligations, and export control exposure that standard contract templates miss. This skill gives the CLO a structured, technology-literate approach to reviewing and negotiating agreements that govern the company's most critical technical dependencies and commercial relationships.

---

## Agreement Type Classification

Before reviewing any agreement, classify it to apply the right review lens:

| Agreement Type                  | Core Legal Risk                                                      | CLO Priority Focus                                                    |
| ------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------- |
| SaaS / Platform agreement       | Lock-in, data portability, uptime SLA, data ownership on termination | Termination data return, IP in customer data, liability cap           |
| Software licence                | Scope of permitted use, sublicence rights, audit rights              | Field-of-use restrictions, open-source contamination                  |
| API access agreement            | Rate limits, data use by provider, change-of-terms unilateralism     | Provider's right to use company data, 30-day change notice clauses    |
| Cloud infrastructure (IaaS)     | Availability SLA, data residency, government access                  | Jurisdiction of processing, law enforcement access clauses            |
| IP assignment                   | Full vs. partial transfer, moral rights, background IP carve-outs    | Background IP retained by assignor, representations on ownership      |
| NDA                             | One-way vs. mutual, residuals clause, return/destruction obligations | Residuals clauses that nullify confidentiality, perpetual injunctions |
| Government procurement          | Security requirements, national content, data sovereignty mandates   | Data localisation obligations, security clearance requirements        |
| Data Processing Agreement (DPA) | GDPR/PDPA compliance, sub-processor chain, breach notification       | Sub-processor approval mechanism, breach notification timeline        |

---

## Standard Contract Review Checklist

Apply to every agreement before advising the business:

### Commercial Terms

- [ ] Parties correctly identified (legal entity names, not trading names)
- [ ] Term and renewal: auto-renewal with adequate notice period for cancellation
- [ ] Pricing: fixed vs. variable; indexation triggers documented
- [ ] Payment terms: consistent with company's cash-flow management

### IP and Data

- [ ] Ownership of work product: company owns deliverables, not contractor
- [ ] Licence back: if contractor retains ownership, company has perpetual, irrevocable licence
- [ ] Background IP: clearly defined and carved out from any assignment
- [ ] Company data: provider has no right to use, analyse, or train models on company data
- [ ] Data return on termination: format, timeline, deletion confirmation requirement

### Liability and Indemnification

- [ ] Liability cap: adequate relative to contract value and potential harm
- [ ] Carve-outs from cap: data breach, gross negligence, IP infringement, wilful misconduct
- [ ] Indemnification: mutual for third-party IP claims; unilateral for data breaches caused by provider
- [ ] Insurance: provider carries adequate professional indemnity and cyber insurance

### Data Residency and Jurisdiction

- [ ] Processing jurisdiction: stated explicitly
- [ ] Transfer restrictions: compliant with applicable data-transfer law (GDPR SCCs, PDPA mechanisms, etc.)
- [ ] Law enforcement access: provider must notify company before disclosing data unless legally prohibited
- [ ] Governing law and jurisdiction: identified, and appropriate for company's risk tolerance

### Termination

- [ ] Termination for convenience: right exists, notice period is commercially reasonable (30–90 days)
- [ ] Termination for cause: specific triggers defined (not just "material breach" without cure mechanism)
- [ ] Post-termination data handling: clear obligations on provider, with timeline
- [ ] Survival clauses: identify which clauses survive termination (IP, confidentiality, dispute resolution)

---

## Government Procurement — Special Protocol

Government contracts require additional scrutiny beyond standard commercial terms. Apply these steps:

1. **Data sovereignty check** — Identify every data element the government contract requires the company to collect, process, or store. Map each element against the jurisdiction's data localisation laws. Flag any element that must be stored in-country for legal review of the technical architecture.

2. **Security requirements** — Government contracts frequently incorporate security standards by reference (ISO 27001, NIST CSF, local equivalents). Confirm the company can meet every referenced standard before signing.

3. **Audit rights** — Government clients often retain broad audit rights. Confirm the audit scope is defined (what systems, what data, how much notice) and that company's confidential information held by the government client is protected.

4. **Subcontractor approval** — Many government contracts require pre-approval of subcontractors. Identify the company's critical subcontractors early and include them in the contract schedule.

5. **Termination for convenience by government** — Government clients often have unilateral termination-for-convenience rights. Ensure compensation for work completed and committed costs is clear.

---

## Vendor Legal Framework

For recurring vendor relationships, apply a tiered model:

| Tier                 | Annual Spend                   | Review Level                                  | Time Budget     |
| -------------------- | ------------------------------ | --------------------------------------------- | --------------- |
| Tier 1 — Strategic   | > $500K or critical dependency | Full CLO review                               | 5 business days |
| Tier 2 — Significant | $50K–$500K                     | Senior Counsel review with CLO sign-off       | 3 business days |
| Tier 3 — Standard    | < $50K, standard SaaS          | Pre-approved template with self-certification | 1 business day  |
| Tier 4 — Low-risk    | < $10K, no data processing     | Purchasing approval only, no legal review     | Same day        |

Maintain a vendor contract register with expiry dates, renewal trigger dates, and DRI for each Tier 1 and Tier 2 agreement.

---

## Output Standards

- Produce a **contract review memo** for every Tier 1 agreement: issue identified, clause reference, risk rating (Critical/High/Medium/Low), recommended redline, business context.
- Never approve a contract with open data-residency ambiguity for a project that handles personal data of residents in a jurisdiction with active data localisation laws.
- When a counterparty's standard terms are unacceptable on a critical clause, propose a specific redline — do not simply say "this clause is unacceptable." The business needs a negotiable position, not a veto.
