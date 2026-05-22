---
name: data-protection-compliance
description: Data Protection Impact Assessment (DPIA), cross-border data transfer mechanism selection, and privacy compliance documentation for the Associate Counsel. Use when conducting a DPIA for a new product or processing activity, selecting and documenting a cross-border data transfer mechanism, assessing data residency requirements, maintaining the Record of Processing Activities (RoPA), responding to a data breach, or producing privacy compliance documentation for a pipeline stage gate.
version: "1.0.0"
---

# Data Protection Compliance

## Purpose

Data protection compliance is not a legal exercise run at the end of a project — it is a continuous technical and legal process that must be embedded in product development from design through operation. The DPIA and transfer mechanism selection are the two highest-leverage compliance tools: get these right before build and most post-launch remediation disappears.

---

## Data Protection Impact Assessment (DPIA) Methodology

A DPIA is required under GDPR (and required or strongly recommended under many other jurisdictions' laws) whenever processing is likely to result in a high risk to individuals' rights and freedoms. Apply the DPIA methodology to all new products and to significant changes to existing products.

### Step 1 — DPIA Necessity Screening

A DPIA is mandatory (GDPR) when processing involves:

- Systematic profiling with legal or significant effect
- Processing of special category data at scale
- Systematic monitoring of publicly accessible areas
- Use of new technologies with unknown privacy implications
- Processing that may prevent individuals from exercising rights or accessing services
- Innovative use of data matching or combining datasets
- Processing of children's data at scale

If any of the above applies, proceed to full DPIA. If uncertain, conduct a DPIA anyway — a completed DPIA that was not strictly required has no legal downside; a missing DPIA that was required is a compliance failure.

### Step 2 — DPIA Structure

```
DPIA Report
===========
Project/Feature Name:   [Name]
DPIA Reference:         [DPIA-YYYY-NNN]
Date:                   [YYYY-MM-DD]
Lead:                   [Azalea Nkrumah, Associate Counsel]
Status:                 [Draft / Under Review / Approved / Approved with Conditions]

SECTION 1 — DESCRIPTION OF PROCESSING
---------------------------------------
1.1 Nature of processing:
    [What data is collected, how it is collected, what processing operations are performed]

1.2 Scope:
    [Volume of data subjects, frequency, geographic scope]

1.3 Context:
    [Relationship with data subjects, reasonable expectations, vulnerability of data subjects]

1.4 Purpose:
    [Specific, explicit, legitimate purposes — one sentence per purpose]

1.5 Lawful basis:
    [Per applicable law — cite article and confirm conditions met]

SECTION 2 — NECESSITY AND PROPORTIONALITY
-------------------------------------------
2.1 Is the processing necessary for the stated purpose?
    [Yes / No / Partially — with analysis]

2.2 Could the purpose be achieved with less data or less invasive processing?
    [If yes, state the less invasive alternative and why it was not chosen]

2.3 Data minimisation measures:
    [Technical measures that limit data to what is strictly necessary]

2.4 Retention policy:
    [Specific retention period per data category — "as long as needed" is not acceptable]

SECTION 3 — RISK IDENTIFICATION AND ASSESSMENT
------------------------------------------------
[For each risk identified:]

Risk ID:        [R-NNN]
Description:    [What could go wrong — specific harm to data subjects]
Likelihood:     [High / Medium / Low + rationale]
Severity:       [High / Medium / Low + rationale]
Risk Rating:    [High / Medium / Low — combine likelihood × severity]
Mitigation:     [Technical or organisational measure to reduce likelihood or severity]
Residual Risk:  [Risk remaining after mitigation — High / Medium / Low]

SECTION 4 — MEASURES TO ADDRESS RISK
---------------------------------------
[Technical measures]
[Organisational measures]
[Contractual measures with third parties]

SECTION 5 — CROSS-BORDER TRANSFER ASSESSMENT
----------------------------------------------
[If processing involves cross-border data transfers — see Section below]

SECTION 6 — CONSULTATION
--------------------------
6.1 DPO consulted: [Yes / No / N/A]
6.2 Processor consultation: [Yes / No / N/A]
6.3 Data subject consultation: [Yes / No / Rationale if No]

SECTION 7 — CONCLUSION AND APPROVAL
--------------------------------------
Overall residual risk: [High / Medium / Low]
Recommendation: [Approve / Approve with conditions / Do not proceed]
Conditions (if any): [Specific conditions to be met before launch]
Approved by: [CLO sign-off required if residual risk is High]
Date of next review: [YYYY-MM-DD — reassess on any material change to processing]
```

---

## Cross-Border Data Transfer Mechanism Selection

When personal data flows from one jurisdiction to another, a valid transfer mechanism is required. Select the appropriate mechanism based on the transfer pair:

### Transfer Mechanism Decision Matrix

| From → To                                             | Adequate?       | Primary Mechanism                                          | Fallback Mechanism          |
| ----------------------------------------------------- | --------------- | ---------------------------------------------------------- | --------------------------- |
| EU → Adequate country (UK post-adequacy, Japan, etc.) | Yes             | Adequacy decision                                          | N/A                         |
| EU → Non-adequate country (most of world)             | No              | Standard Contractual Clauses (SCCs)                        | BCRs (for intra-group only) |
| Singapore → Countries with comparable protection      | Yes (whitelist) | No mechanism needed                                        | —                           |
| Singapore → Countries without comparable protection   | No              | Contractual obligations                                    | —                           |
| Nigeria → Countries with adequate protection          | Yes (whitelist) | No mechanism needed                                        | —                           |
| Nigeria → Countries without adequate protection       | No              | Contractual safeguards + NITDA approval for sensitive data | —                           |
| Japan → Countries with appropriate handling           | Varies          | Contractual obligations or individual consent              | —                           |
| Any → China                                           | No              | SAMR SCCs + (for large-scale) CAC security assessment      | —                           |

### SCC Implementation Checklist (GDPR)

When SCCs are the transfer mechanism:

- [ ] Correct module selected (C2C, C2P, P2C, P2P)
- [ ] Transfer impact assessment (TIA) completed for destination country
- [ ] If destination country has problematic laws: supplementary measures documented
- [ ] SCCs signed before any data transfer commences
- [ ] SCCs stored in contract register
- [ ] RoPA updated to reference SCCs

---

## Record of Processing Activities (RoPA)

Maintain the organisation's RoPA — required under GDPR Art. 30 and equivalent requirements under other privacy laws. Each entry:

| Field                    | Content                                       |
| ------------------------ | --------------------------------------------- |
| Processing activity name | [Descriptive name of the processing activity] |
| Controller / Processor   | [Company's role — controller or processor]    |
| Purpose                  | [Specific purpose]                            |
| Data categories          | [List each category]                          |
| Data subjects            | [Customers / employees / partners / etc.]     |
| Recipients               | [Internal teams + external third parties]     |
| Cross-border transfers   | [Yes/No — if yes, mechanism]                  |
| Retention period         | [Specific period per data category]           |
| Security measures        | [Technical and organisational]                |
| Lawful basis             | [Per applicable law]                          |
| DPIA reference           | [If applicable]                               |

Update the RoPA within 30 days of any new processing activity or material change to an existing activity.

---

## Data Breach Response Protocol

When a potential data breach is identified:

1. **Containment** (first 4 hours) — Notify CLO immediately. Contain the breach if possible (revoke access, isolate system). Do not delete evidence.

2. **Assessment** (first 24 hours) — Determine: what data was affected, how many data subjects, likelihood of harm, cause of breach. Complete breach assessment form.

3. **Notification decision** (before 72-hour GDPR clock) — If breach likely results in risk to data subjects' rights, notify the supervisory authority. If likely results in high risk, also notify affected data subjects.

4. **Regulatory notification** — Draft notification to supervisory authority using the authority's prescribed form. Include: nature of breach, categories and approximate number of data subjects and records, contact point, likely consequences, measures taken or proposed.

5. **Documentation** — Document every breach regardless of notification obligation. The documentation must be comprehensive enough to demonstrate compliance to a regulator.

---

## Output Standards

- Every DPIA must reach a clear conclusion: approve, approve with conditions, or do not proceed. A DPIA that identifies risks without reaching a conclusion is incomplete.
- Cross-border transfer mechanisms must be implemented before data flows — not documented retrospectively.
- Breach response timelines are not negotiable: the 72-hour GDPR notification clock runs from when the organisation becomes aware of the breach, not when the legal team finishes its assessment. Escalate immediately.
