# Pipeline Stage 1 Authority Transfer

**Document Type:** Authority Transfer Specification
**Version:** 1.0
**Date:** April 19, 2026
**Owner:** CPO (Marcus Tran-Yoshida). Co-signed by CTO (Dr. Kenji Nakamura).
**Applies To:** Mobile · Web · Backend API · Full-Stack Cross-Platform pipelines
**Status:** Approved · Execution deferred until each VP clears their Day 90 gate

---

## Purpose

When each new VP-tier Product Leader completes their 90-day onboarding and the CPO authorizes full commencement, Stage 1 PRD authority for their pipeline transfers from the CPO to the VP. This document specifies:

1. What authority transfers, and to whom.
2. What authority the CPO retains.
3. How decisions get made when the two VPs disagree, or when a pipeline spans more than one VP's domain.
4. How the transfer is announced to the rest of the organization.
5. What text changes in the four `pipeline.md` files (appendix — this is the mechanical part; the primary content of this document is what precedes it).

The transfer is not administrative; it is the point at which the three-person Product Management division begins operating at its intended capacity. Getting the authority and the escalation paths right is what prevents the first quarter from descending into ownership disputes.

---

## Where We Are Today

All four pipelines list the CPO as the sole Stage 1 PRD owner. The company has expanded well past the point where one person — however talented — can author PRDs with native-domain depth across Mobile, Web, API, and Full-Stack. Marcus's craft is mobile; the other three pipelines have been receiving PRDs that are technically complete per his template but structurally missing domain-specific content (web conversion mechanics, API governance, developer experience, etc.). The two new VPs are the fix.

---

## The New Authority Model

### Who Owns Stage 1 After the Transfer

| Pipeline    | Stage 1 Owner (post-transfer)             | Template Steward | Security Co-Author                                                                 |
| ----------- | ----------------------------------------- | ---------------- | ---------------------------------------------------------------------------------- |
| Mobile      | CPO (Marcus) — **unchanged**              | CPO              | CSO                                                                                |
| Web         | **VP Product, Web Platforms**             | CPO              | CSO (SRD primary); VP Web co-authors product-surface security criteria             |
| Backend API | **VP Product, API & Developer Platforms** | CPO              | CSO (SRD primary); VP API co-authors auth / rate-limit / abuse-prevention criteria |
| Full-Stack  | **VP Web + VP API jointly**               | CPO              | CSO (SRD primary); both VPs co-author their respective surfaces                    |

### What the CPO Retains

The CPO retains three distinct pieces of authority that do not transfer:

1. **Template stewardship.** Marcus owns `prd-authorship.md` as a company-wide standard. VPs contribute domain-specific extensions (Section 5) but do not rewrite the template. Changes to Sections 1–4 or 6–8 require CPO sign-off.
2. **Final PRD sign-off on all pipelines.** VPs are the primary authors for Web and API; Marcus remains the Accountable Approver under a Responsible/Accountable split. A PRD does not advance to Stage 2 without the CPO's signature.
3. **Arbitration authority for cross-pipeline features.** When a Full-Stack feature touches Mobile, or when the two VPs deadlock on a joint PRD, the CPO resolves.

This is the "template steward + final approver" model. The VPs own the production of Stage 1 artifacts; the CPO owns the standard against which they're judged.

### Why This Shape

A single pipeline needs a single primary author. Joint authorship across three people (CPO + 2 VPs) on Web or API would produce blurry accountability and slower cycles. At the same time, the CPO cannot cede the standard — the value of Marcus's PRD template is precisely that it is a standard; fragmenting into three templates would undo what has been built.

Full-Stack is the exception because the feature itself spans two domains. There is no non-blurry way to assign a Full-Stack PRD to a single VP. The joint model, with the CPO as arbiter when mobile enters the picture, is the least-bad solution.

---

## Decision Rights Matrix

For every Stage 1 PRD question that could arise, this table specifies who decides. If there is ambiguity in practice, the fallback is whichever row applies most specifically.

| Question                                            | Decides                        |
| --------------------------------------------------- | ------------------------------ |
| "Is the problem statement framed correctly?"        | VP (for their pipeline)        |
| "Is the scope right?"                               | VP (for their pipeline)        |
| "Do the kill criteria meet the template standard?"  | CPO (steward of the standard)  |
| "Does Section 5 cover the domain adequately?"       | VP (for their pipeline)        |
| "Does the PRD conform to the template?"             | CPO (steward)                  |
| "Should this PRD advance to Stage 2?"               | CPO (final sign-off)           |
| "Who owns the web surface of a Full-Stack PRD?"     | VP Web                         |
| "Who owns the API surface of a Full-Stack PRD?"     | VP API                         |
| "Who owns the mobile surface of a Full-Stack PRD?"  | CPO                            |
| "Full-Stack PRD deadlock between VP Web and VP API" | CPO (arbiter)                  |
| "SRD criteria for Web/API product surface"          | CSO (final); VPs co-author     |
| "Whether the PRD feeds Stage 3 well enough"         | CIO (veto-level concern if no) |
| "Whether the PRD design-handoff is clear enough"    | CDO (veto-level concern if no) |
| "Whether the PRD is safe to ship"                   | CSO (veto-level concern if no) |
| "Whether to kill an in-flight bet"                  | VP (proposes); CPO (confirms)  |
| "Whether to amend this authority model itself"      | CPO (proposes); CTO co-signs   |

---

## Escalation and Deadlock Resolution

The escalation path is short by design. A longer path produces decision latency that erodes product velocity.

1. **Within pipeline:** VP owns. No escalation required for within-pipeline decisions. If the VP wants the CPO's input as a sounding board, that's a normal conversation, not an escalation.
2. **Full-Stack disagreement between VPs:** The two VPs attempt resolution directly. Most Full-Stack disagreements are not fundamental and resolve in a 30-minute conversation. If unresolved within 48 hours of surfacing, it escalates.
3. **Escalated Full-Stack disagreement:** The CPO holds an arbitration session. 60 minutes, both VPs present their position, CPO decides. Decision is recorded in the PRD as a dated note with reasoning.
4. **Cross-functional disagreement (PRD vs. SRD, PRD vs. architecture, PRD vs. design):** Handled at the Stage 2/3 review meetings per existing pipeline process. VPs represent Product; CSO / CIO / CDO represent their functions. CTO chairs.
5. **Strategic or commercial disputes that exceed the VP's decision rights:** Escalated to the CPO. If the CPO and the VP cannot align, the VP implements the CPO's call and the disagreement is recorded. This is the "disagree and commit" rule.

---

## Stakeholder Communication

Before the transfer takes effect, the following stakeholders receive explicit notice. This is not a formality — it is how the company avoids the scenario where a VP walks into a Stage 2 meeting and the CDO doesn't know they have new authority.

| Audience                                                         | Communicator      | Medium                      | Content                                                                                                                                            |
| ---------------------------------------------------------------- | ----------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| R&D leadership (CTO, Elena Vasquez, Dev Malhotra, chapter leads) | CTO + CPO jointly | Meeting + written follow-up | New Stage 1 ownership per pipeline; who to bring PRD questions to going forward; the weekly sync cadence each VP has established during onboarding |
| Design (CDO + team)                                              | CDO + CPO jointly | Meeting                     | Stage 1 → Stage 2 handoff now comes from the VP, not the CPO, for Web and API pipelines; Mobile unchanged                                          |
| Security (CSO + team)                                            | CSO + CPO jointly | Meeting                     | SRD co-authorship partner per pipeline; VPs are the PRD counterpart for Web / API product-surface security topics                                  |
| Infrastructure / DevOps (CIO, Thomas Zhang)                      | CIO               | Written memo                | How API pricing and rate-limit decisions now flow through VP API; how web performance budgets flow through VP Web                                  |
| Data / Analytics (if applicable)                                 | CPO               | Written memo                | Dashboards and cohorts each VP now owns                                                                                                            |
| Executive team + User                                            | CPO               | Written memo                | Summary of transfer, rationale, what changes externally (nothing) and what changes internally (everything about who holds the Stage 1 pen)         |

All stakeholder communications happen in a single week (the "transfer week"), sequenced after each VP clears Day 90 and before the `pipeline.md` files are amended. The transfer is not real until the stakeholders know it is real.

---

## Execution Gates

The transfer for each VP executes when — and only when — the following are true for that VP:

| Gate                                                                                                           | Status     | Who Confirms                |
| -------------------------------------------------------------------------------------------------------------- | ---------- | --------------------------- |
| VP has cleared the Day 90 review with "Full commencement" outcome                                              | ⏳ Pending | CPO                         |
| VP has shipped their solo PRD to Stage 2                                                                       | ⏳ Pending | CPO                         |
| VP has finalized their `skills/` domain-strategy file (`web-product-strategy.md` or `api-product-strategy.md`) | ⏳ Pending | VP + CPO                    |
| The revised `prd-authorship.md` with Web / API extensions is merged                                            | ⏳ Pending | CPO                         |
| R&D counterpart (Elena Vasquez for Web VP; Dev Malhotra for API VP) has a functioning weekly sync with the VP  | ⏳ Pending | CHRO (via reverse check-in) |
| Stakeholder communications have been delivered                                                                 | ⏳ Pending | CPO + CTO                   |

The two VPs do not need to transfer simultaneously. If one clears Day 90 and the other needs a 30-day extension, the transfer proceeds for the first VP and waits for the second. Half a transfer is still better than none.

Full-Stack joint authorship cannot activate until both VPs have transferred. During any period where one VP has transferred and the other has not, the CPO remains the Full-Stack author.

---

## If the Transfer Needs to Reverse

Rarely, a VP will clear Day 90 and then fail to operate well at Stage 1 in practice — domain judgment is fine, but the stakeholder relationships don't hold, or the solo PRDs degrade over the first quarter. In that case:

1. The CPO raises the concern with the VP directly. Coaching, course correction, a clear two-quarter window.
2. If not resolved by the end of that window, the CPO and CHRO conduct a structured review with the VP.
3. The outcome is one of: continued course correction with a clearer plan; reassignment to a different role; or mutual decision to part.
4. If the outcome requires the VP to leave, Stage 1 authority reverts to the CPO for that pipeline, and the CHRO reopens the recruitment.

Reverting authority is not a re-amendment of `pipeline.md`. It's a personnel change. The pipeline document continues to list "VP Product, Web Platforms" as the authority; the occupant of that role changes.

---

## What Changes for Stages 2–10

Stage 1 is the authority transfer. Stages 2–10 have smaller adjustments:

| Stage                            | Change                                                                                                                                                                                                |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 2 (Design)                 | CDO handoff partner is the VP for Web / API; CPO for Mobile.                                                                                                                                          |
| Stage 3 (Architecture)           | CIO's ADR process receives PRDs with richer domain-specific content. Stage 3 review panel unchanged; VPs may attend as product representatives for their pipeline.                                    |
| Stage 6 (Code Review)            | The 5-officer panel is unchanged. VPs attend as advisors for code in their pipeline; they do not hold veto authority.                                                                                 |
| Stage 8 (Integrity Verification) | VPs co-review with the CPO for their pipeline. A product-level integrity concern (e.g., DX regression for API, accessibility regression for Web) flagged by the VP has the same weight as a CPO flag. |
| Stage 10 (Release Readiness)     | VPs co-sign release readiness for their pipeline. Final authority remains with the CPO; VP input is influential, not binding.                                                                         |

These are evolutions of existing stage semantics, not new stages. Nothing about the pipeline structure changes.

---

## Appendix — Text Changes to `pipeline.md` Files

The mechanical edits to the four pipeline definitions. This is the least important part of the authority transfer — it is simply the documentation following the decisions above.

### Mobile (`company/pipeline/mobile/pipeline.md`)

No change.

### Web (`company/pipeline/web-development/pipeline.md`)

Stage 1 "Relevant Personnel" is updated to replace:

> CPO (PRD), CSO (SRD), Security Engineer, Compliance Analyst

with:

> VP Product, Web Platforms (PRD — primary); CPO (template steward, final sign-off); CSO (SRD — primary); VP Product, Web Platforms (SRD co-author for product-surface security criteria); Security Engineer (SRD technical); Compliance Analyst (SRD compliance).

If the Web Strategy Matrix section lists an authority for Stage 1, update it to show VP Web as Principal and CPO as Steward.

### Backend API (`company/pipeline/backend-api/pipeline.md`)

Stage 1 "Relevant Personnel" is updated analogously, with VP Product, API & Developer Platforms as primary PRD author, CPO as template steward and final sign-off, and VP API as SRD co-author for auth / rate-limit / abuse-prevention criteria.

If the API Strategy Matrix section lists an authority for Stage 1, update it to show VP API as Principal and CPO as Steward.

### Full-Stack (`company/pipeline/full-stack/pipeline.md`)

Stage 1 "Relevant Personnel" is updated to list joint primary authorship between the two VPs, with the CPO as template steward, arbiter for mobile-touching features, and final sign-off. Both VPs are SRD co-authors for their respective surfaces.

Add a clarifying subnote on the Full-Stack authorship model: web+API features are VP-led with CPO template review; features that also touch mobile carry CPO veto on the mobile-facing sections; deadlocks escalate to the CPO.

### How the edits are applied

When the execution gates above are met, the CTO office edits the three `pipeline.md` files in a single commit with the message `docs(pipeline): transfer Stage 1 authority to VP-tier Product Leaders`. The CTO also updates `AGENTS.md` to reflect the new VP-tier Product Officers. The `company/pipeline/README.md` is updated if it currently references Stage 1 owners at the index level.

---

## Document History

| Version | Date       | Changes                                                                                                                                                 | Status           |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| 1.0     | 2026-04-18 | Initial authority transfer specification: decision rights, escalation paths, stakeholder communication plan, execution gates, and text-change appendix. | Pending Approval |

---

**Next step:** CPO + CTO joint review. Execution deferred until the first VP clears their Day 90 gate.
