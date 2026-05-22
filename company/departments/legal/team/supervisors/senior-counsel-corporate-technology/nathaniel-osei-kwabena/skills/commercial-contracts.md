---
name: commercial-contracts
description: Commercial agreement review, negotiation, and management for the Senior Counsel. Use when reviewing or drafting any commercial agreement (client contracts, vendor agreements, partnership terms, licensing deals, master service agreements), advising on contract negotiation strategy, managing the contract template library, structuring IP ownership in a product development engagement, or responding to a counterparty's proposed redlines.
version: "1.0.0"
---

# Commercial Contracts

## Purpose

Every commercial agreement is a risk allocation document. The negotiation is about deciding who bears which risks — not about winning. The best outcome is a contract that both parties understand, that fairly allocates foreseeable risks, and that does not create time-consuming disputes when something goes wrong. Speed and fairness both matter: a legally perfect contract that takes 45 days to sign costs the business in opportunity.

---

## Contract Review Workflow

### Step 1 — Initial Classification

Identify the agreement type and apply the correct template or review lens (see CLO's `technology-transactions.md` for full classification). At minimum:

| Question                                             | Why It Matters                                                                  |
| ---------------------------------------------------- | ------------------------------------------------------------------------------- |
| Who are the contracting parties?                     | Confirm legal entity names; trading names create enforceability risk            |
| What is the primary obligation?                      | Services / goods / licence / data access / joint venture                        |
| Does the agreement involve personal data processing? | If yes, a Data Processing Agreement (DPA) is likely required                    |
| What jurisdiction governs the agreement?             | Determines which mandatory law overrides apply                                  |
| What is the contract value and term?                 | Determines tier (see tiered review model in CLO's `technology-transactions.md`) |

### Step 2 — Risk Identification Pass

Read the full agreement once without marking. Note the following as you go:

- Unusual or one-sided terms that depart from market standard
- Missing standard protections (no IP indemnity, no limitation of liability, no data return on termination)
- Automatic renewal clauses with short cancellation windows
- Unilateral amendment rights (provider can change terms with 30-day notice)
- Audit rights that are overly broad or invasive
- Dispute resolution that mandates arbitration in an unfavourable jurisdiction

### Step 3 — Structured Redline

Produce redlines in priority order:

| Priority                | Issue Type                                                                                                                     | Standard Position                                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| **P1 — Must resolve**   | Data ownership, IP assignment, unlimited liability, no limitation of liability, no data return on termination                  | Will not sign without resolution                                               |
| **P2 — Should resolve** | One-sided termination, overly broad audit rights, unilateral amendment rights, auto-renewal with < 60 days cancellation notice | Strongly prefer resolution; will escalate to CLO if counterparty refuses       |
| **P3 — Preferred**      | Governing law in unfavourable jurisdiction, warranty scope narrower than desired, SLA below internal standard                  | Raise in negotiation; accept if counterparty holds firm and P1/P2 are resolved |

### Step 4 — Negotiation Strategy

Before entering negotiations, define:

1. **Walk-away points** (P1 issues that cannot be compromised)
2. **Trading chips** (P3 issues that can be conceded to get P2 issues resolved)
3. **Market standard reference** (if counterparty claims a term is standard, verify before accepting)

Document the negotiation outcome in a deal summary that records every deviation from the standard template and who accepted the deviation.

---

## IP Ownership Structuring

When a commercial agreement involves the creation of technology — software, data models, configurations, integrations — establish IP ownership before work begins:

### IP Ownership Matrix

| Work Type                      | Default Legal Position                                            | Company's Preferred Position                                     | Negotiation Approach                                            |
| ------------------------------ | ----------------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------- |
| Custom development for company | Contractor owns unless assigned                                   | Company owns all work product                                    | Require IP assignment clause                                    |
| Platform customisation (SaaS)  | Platform provider owns the platform; company owns its config/data | Company owns its data and configurations; provider owns platform | Standard for SaaS; ensure data portability                      |
| Joint development              | Joint ownership (messy)                                           | Company owns output; provider receives licence back              | Negotiate field-of-use licence back rather than joint ownership |
| Open-source contribution       | Governed by OSS licence                                           | Ensure contribution does not contaminate proprietary code        | Require OSS audit before any contribution to OSS projects       |

### Background IP Carve-Out

Every agreement that involves IP creation must clearly define:

- **Background IP**: IP each party owned before the engagement. Each party retains ownership of its own background IP.
- **Developed IP**: IP created during the engagement. Company should own unless there is a compelling reason otherwise.
- **Third-party IP**: IP owned by neither party (open-source, licensed tools). Both parties must comply with applicable licences.

---

## Contract Template Management

Maintain a tiered contract template library:

| Template                              | Coverage                                          | Review Cycle                    |
| ------------------------------------- | ------------------------------------------------- | ------------------------------- |
| Master Service Agreement (outbound)   | Company as service provider                       | Annual                          |
| Master Service Agreement (inbound)    | Company as customer                               | Annual                          |
| Software Licence Agreement (outbound) | Company licensing its software                    | Annual                          |
| Non-Disclosure Agreement (mutual)     | Pre-engagement confidentiality                    | Annual                          |
| Non-Disclosure Agreement (one-way)    | Company receiving confidential information        | Annual                          |
| Data Processing Agreement             | Any engagement involving personal data processing | Bi-annual (privacy laws change) |
| Consulting / Contractor Agreement     | Individual contractor engagement                  | Annual                          |

For each template, maintain a **deviation log** — a list of pre-approved deviations that do not require escalation. This eliminates repeated discussions on standard counterparty pushback.

---

## Output Standards

- Every contract review must produce a written summary: parties, obligations, key risks identified, recommended redlines, overall recommendation (approve / approve with changes / escalate to CLO).
- Do not approve an agreement with unresolved P1 issues. Escalate to CLO if counterparty will not move on a P1 issue.
- Contract summaries are business documents — write them so a non-lawyer C-suite executive can act on them without re-reading the contract.
- Log every signed agreement in the contract register with: parties, effective date, expiry date, renewal date, DRI, and key obligations.
