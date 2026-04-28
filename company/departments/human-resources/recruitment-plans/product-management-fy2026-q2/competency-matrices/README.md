# VP Product — Competency Matrices

**Document Type:** Role-Specific Competency Matrices
**Version:** 1.0
**Date:** April 19, 2026
**Owner:** CPO (Marcus Tran-Yoshida) — primary. CHRO (Dr. Evelyn Hartwell) — process steward.
**Applies To:** VP Product, Web Platforms · VP Product, API & Developer Platforms
**Status:** Approved

---

## What This Document Is For

Selection criteria for the two VP-tier Product Leaders being recruited. This is used by the CHRO, CPO, and the interview panel to evaluate candidates against a shared bar. It is applied during hiring, not during onboarding.

The evaluation uses the company's standard 20-point vetting gate (defined in `vet-candidate.md`). The dimensions below are the product-leadership specialization of that gate: they describe what "5/5 Craft Depth" actually means for a Web Product VP versus an API Product VP, and what "4/5 Leadership Signal" looks like for someone who will report to an opinionated CPO.

---

## Hiring Bar

| Gate               | Requirement                                               |
| ------------------ | --------------------------------------------------------- |
| Total score        | ≥ 16 / 20                                                 |
| Red Flag Scan      | PASS                                                      |
| Cultural alignment | PASS (non-negotiable)                                     |
| Panel consensus    | Unanimous across CPO, CHRO, CTO, CIO (+ CSO for API role) |

A single veto from any Chief Officer on the panel is binding. Scores below the bar are not rounded up; a 15/20 candidate is rejected even if the panel likes them personally.

---

## Universal Dimensions

These are assessed for both roles. They are the floor; a candidate who does not clear these is rejected regardless of domain craft.

### Strategic Judgment

The ability to form an opinion about where a product should go, defend it against pushback from engineering and commercial stakeholders, and change the opinion when the evidence warrants. Assessed by CPO + CHRO.

A 5/5 candidate has killed a product they personally championed, because the data said to. A 4/5 candidate has killed someone else's pet project. A 3/5 candidate has only shipped and has never publicly retired a bet. We do not hire 3/5 on this dimension.

### Customer Empathy

The ability to read a customer transcript or support ticket and name the underlying unmet need — not just the surface complaint. Assessed by CPO.

A 5/5 candidate has a documented practice of talking to customers directly and can tell a story of a decision that changed because of a single customer interview. A 3/5 candidate quotes NPS scores without having spoken to a customer in the last quarter. We do not hire 3/5 on this dimension.

### Commercial Literacy

Comfort with the unit economics of their domain. For Web: CAC, LTV, conversion cohorts, margin per channel. For API: ARR per developer account, rate-limit-tier attach rates, cost-to-serve per call. Assessed by CPO + CHRO.

A 5/5 candidate has been accountable for a revenue or cost line and can describe the tradeoffs they made. A 3/5 candidate has never seen a P&L for their product.

### Storytelling and Stakeholder Influence

The ability to take a complex product trade-off and explain it to a room that includes an engineering lead, a designer, a finance partner, and a skeptical executive — and walk out with alignment. Assessed by CPO + CHRO + CTO.

A 5/5 candidate has run a decision-making meeting where the room was divided at the start and aligned at the end. We test this in the interview with a live structuring exercise.

### Rhythm-of-Business Design

The ability to design and sustain the weekly / quarterly / annual operating cadence for a product area: standups, roadmap reviews, stakeholder syncs, executive briefings, quarterly bet-setting. Assessed by CPO.

A 5/5 candidate has an opinion about why their last company's cadence was wrong and what they would change. A 3/5 candidate defers to whatever cadence exists around them.

### Kill-Criteria Discipline

The willingness to write kill criteria for their own bets and enforce them. This is a specific subset of strategic judgment but worth calling out separately because it is the single most common failure mode of senior product hires. Assessed by CPO.

A 5/5 candidate has a written kill-criteria artifact they can show us from a past role. A 3/5 candidate treats kill criteria as optional.

### Template Stewardship Fluency

The willingness to adopt and steward an existing company standard (Marcus's `prd-authorship.md`) rather than impose their own. Candidates who signal, "my first move would be to redesign the PRD template," are auto-rejected on this dimension regardless of other strengths. Assessed by CPO.

This is explicitly not a test of servility. Strong candidates will absolutely propose refinements — they just propose them as contributions to the standard, not replacements for it.

### Cultural Alignment (Non-Negotiable)

Low ego, high self-esteem, open to being wrong, able to give and receive direct feedback, contributes to psychological safety rather than consumes it. Assessed by CHRO + CPO through behavioral interview plus reference checks.

This is PASS / FAIL. A 20/20 candidate who fails cultural alignment is rejected. This matches the engineering hiring standard and is not negotiable.

---

## Role-Specific Craft Depth: VP Product, Web Platforms

Assessed by CPO + Elena Vasquez (VP of Web & Backend Engineering, R&D) + CDO for the design-partnership dimension.

### Web Product Strategy

Depth in web-native product decisions: PWA vs. SPA vs. SSR as a product-strategy choice (not just an engineering one), browser platform trade-offs, performance budgets as a product constraint. A 5/5 candidate has made each of these calls at least once with consequences.

### Conversion and Growth Mechanics

Funnel design, experimentation frameworks that produce statistically sound results (not just vanity wins), organic growth through SEO / content / referral. A 5/5 candidate has driven a measurable shift in a core funnel metric and can explain the causal chain.

### Web Accessibility Fluency

Treats accessibility as a product decision, not an engineering post-script. Fluent in WCAG 2.1 AA as acceptance criteria from the PRD's first draft. A 5/5 candidate has shipped a product where accessibility was a differentiator.

### Multi-Viewport and Device-Class Design

Desktop, tablet, mobile web — and the product-strategy implications of each. Understands when to unify and when to differentiate. A 5/5 candidate has explicitly chosen a device-class priority and can defend it with data.

### Design Partnership

Can work with the CDO's team on prototype-to-PRD cycles. Reads prototypes the way engineers read code. Doesn't treat design as decoration. Assessed by CDO.

### Web Security Product-Awareness

Understands that cookie consent, DSR (data subject request) workflows, authentication flows, and session management are product-surface decisions with security implications. Does not need to be a CSO, but can co-author an SRD section without the CSO having to hold their hand. Assessed by CSO.

---

## Role-Specific Craft Depth: VP Product, API & Developer Platforms

Assessed by CPO + Dev Malhotra (Backend Chapter Lead, R&D) + CSO for the API-security dimension. Elena Vasquez contributes a scale / infrastructure perspective.

### API-as-Product Strategy

Treats the API schema, versioning, and deprecation lifecycle as product decisions — not implementation details. A 5/5 candidate has personally owned a public or internal-SDK API product with documented developer adoption or revenue, and has navigated at least one deprecation cycle without losing the customer base.

### Developer Experience Craft

Fluent in DX as a first-class discipline: SDK ergonomics, quickstart time, error-message quality, sandbox design, time-to-first-successful-call as a measurable metric. A 5/5 candidate has owned a DX KPI for at least a year.

### Developer Relations Strategy

Treats DevRel as a product discipline, not a marketing function. Has opinions about the right mix of content / community / events / sample apps for the stage of the product. A 5/5 candidate has designed or run a DevRel program.

### API Pricing and Monetization

Fluent in the mechanics of API pricing — free-tier economics, rate-limit tiering as a product lever, usage-based vs. seat-based trade-offs. A 5/5 candidate has designed a pricing model and seen it through to revenue impact.

### API Governance and Lifecycle Management

Versioning policy, deprecation windows (typically 6–12 months for paid endpoints), backward-compatibility discipline. Understands how product decisions at Stage 1 become ADRs at Stage 3 (the CIO's domain) and writes PRDs that enable good ADRs. Assessed by CIO.

### API Security Product-Awareness

Understands that auth patterns, rate limiting, abuse prevention, webhook signature verification, and PII minimization are product-surface decisions. Can co-author an SRD section without the CSO holding their hand. Fluent in OWASP API Top 10. Assessed by CSO.

---

## Scoring Rubric

The 20-point gate is allocated as follows, by category. Individual dimensions are averaged into the category score.

### Web VP

| Category          | Dimensions Contributing                                                           | Max         |
| ----------------- | --------------------------------------------------------------------------------- | ----------- |
| Impact at Scale   | Strategic Judgment · Commercial Literacy · Web Product Strategy                   | 5           |
| Craft Depth       | Conversion/Growth · Web Accessibility · Multi-Viewport Design · Customer Empathy  | 5           |
| Leadership Signal | Storytelling · Rhythm-of-Business · Design Partnership · Kill-Criteria Discipline | 5           |
| Standards Signal  | Template Stewardship · Web Security Product-Awareness                             | 5           |
| Red Flag Scan     | Background · references · employment history · Cultural Alignment                 | PASS / FAIL |
| **Total**         |                                                                                   | **20**      |

### API VP

| Category          | Dimensions Contributing                                                          | Max         |
| ----------------- | -------------------------------------------------------------------------------- | ----------- |
| Impact at Scale   | Strategic Judgment · Commercial Literacy · API-as-Product Strategy · API Pricing | 5           |
| Craft Depth       | Developer Experience · Developer Relations · Customer Empathy                    | 5           |
| Leadership Signal | Storytelling · Rhythm-of-Business · Kill-Criteria Discipline                     | 5           |
| Standards Signal  | Template Stewardship · API Governance · API Security Product-Awareness           | 5           |
| Red Flag Scan     | Background · references · employment history · Cultural Alignment                | PASS / FAIL |
| **Total**         |                                                                                  | **20**      |

Notes:

- A candidate can be strong in Craft Depth and weak in Leadership Signal. We do not hire them. The four category caps force balance.
- A candidate can be 5/5 on Craft Depth and 2/5 on cultural alignment. Cultural alignment is a hard veto. They are not hired.
- Scores are discussed by the panel and recorded by the CHRO in the [`../recruitment-checkpoint.md`](../recruitment-checkpoint.md) on a per-candidate basis.

---

## Selection Protocol

### Stage A — Profile Screen (CHRO)

CHRO reviews inbound candidate profiles against a coarse filter:

- At least 8 years of product management experience with direct product ownership
- At least 3 years managing other product managers
- Demonstrable domain signal (shipped web products with scale, or shipped API products with developer adoption)
- No obvious cultural-misalignment markers from public writing or references

Candidates who clear the screen advance to Stage B.

### Stage B — Domain Interview

A 90-minute conversation with the CPO and the domain counterpart from R&D (Elena Vasquez for Web; Dev Malhotra for API). The conversation tests craft depth through live scenarios, not hypotheticals the candidate has prepared for.

### Stage C — Landscape Exercise

The candidate receives a short brief (half a page) for a real or lightly-fictionalized product opportunity in their domain. They have 5 business days to produce a 3-page Landscape Memo in Marcus's template — not a full PRD, just the Landscape-Memo subset (state of domain, opportunities, risks, proposed first bet).

This is the most load-bearing signal in the process. Marcus reads the memo and scores it qualitatively against his own standard.

### Stage D — Panel Interview

A round of 45-minute conversations with CPO, CTO, CIO, CSO (for API candidates), CDO (for Web candidates), and CHRO. Each panel member evaluates the candidate on their assigned dimensions and records a PASS / FAIL with commentary.

### Stage E — Reference and Back-Channel

CHRO contacts three candidate-supplied references and two independently-sourced back-channel references. Material inconsistencies between the two pools are a FAIL.

### Stage F — Panel Debrief and Offer

The full panel debriefs. Scores are locked. If all category caps are cleared and Cultural Alignment is PASS and Red Flag Scan is PASS, the candidate receives an offer. If any category falls below 4/5 or any Chief Officer vetoes, the candidate is rejected.

### Stage G — Placement

On offer acceptance, the CHRO invokes `recruit-product.md` to produce the `agent/profile.md` artifact. The `skills/` folder is populated during onboarding (not before), per the [`../onboarding-plan/onboarding-plan.md`](../onboarding-plan/onboarding-plan.md) Phase 3 milestones.

---

## Document History

| Version | Date       | Changes                                                                                                      | Status           |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------ | ---------------- |
| 1.0     | 2026-04-18 | Initial competency matrices for VP Product Web + VP Product API. Product-leadership dimensions foregrounded. | Pending Approval |

---

**Next step:** CPO review. Once approved, the CHRO uses this document as the scoring framework for every candidate throughout Stages A–F.
