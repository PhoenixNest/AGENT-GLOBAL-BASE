# VP Product — First 90 Days Onboarding Plan

**Document Type:** Senior Leadership Onboarding Plan
**Version:** 1.0
**Date:** April 19, 2026
**Owner:** CPO Office (Marcus Tran-Yoshida) — primary sponsor. CHRO Office (Dr. Evelyn Hartwell) — process steward.
**Applies To:** VP Product, Web Platforms · VP Product, API & Developer Platforms
**Status:** Approved

---

## Why This Document Exists

Both new VP-tier Product Leaders arrive having already cleared the 20-point vetting gate. They are hired because they are qualified. The purpose of this document is not to re-qualify them — it is to calibrate them with how Product Management works at this company: Marcus's PRD standard, the 10-stage pipeline, the relationships with R&D / Design / Security / Infrastructure, and the customers we serve.

The right mental model is a **90-day integration**, not a probationary exam. The VP's job is to get their arms around a domain that the CPO office has not previously owned deeply (Web, or API), build relationships that will carry them for years, and produce a credible first roadmap. The company's job is to set them up to succeed.

The plan is structured in three 30-day phases:

| Phase          | Days  | Posture                                                   | Authority                            | Primary Output                                   |
| -------------- | ----- | --------------------------------------------------------- | ------------------------------------ | ------------------------------------------------ |
| **Immerse**    | 1–30  | Listen, learn, meet people                                | Observer / shadow                    | Landscape Memo                                   |
| **Contribute** | 31–60 | Co-own with the CPO; draft and ship work alongside Marcus | Co-author                            | First co-authored PRD shipped to Stage 2         |
| **Lead**       | 61–90 | Own the pipeline's Stage 1; hold the pen                  | Solo author, subject to CPO sign-off | Solo PRD shipped to Stage 2 + Q1 Product Roadmap |

Pipeline Stage 1 authority transfers at the end of Day 90, gated on the outcomes of a 90-day review conversation. There are three outcomes — full commencement, course correction with an extension, or a mutual decision to part — described in the [90-Day Review](#day-90--review--decision-gate) section. There is no mechanical "fail a module, fire the hire" protocol. Senior leadership is evaluated on judgment and outcomes, not checklist completions.

---

## Principles

1. **Calibration, not re-qualification.** The VP already passed vetting. Onboarding is about learning the system well enough to lead inside it.
2. **Domain-first immersion.** The Web VP spends their first weeks in web. The API VP spends their first weeks in API. Mobile exposure is deliberate but secondary.
3. **Relationships are the deliverable.** The VP's ability to run Stage 1 depends on trust with R&D, Design, Security, Infrastructure, and CPO. The first 30 days budget time for 1:1s accordingly.
4. **Coach, don't grade.** Check-ins are conversations: what's working, what isn't, how to adjust. No rubric scores, no points, no curriculum passes.
5. **Kill-criteria are sacred.** Marcus's PRD template includes kill criteria as a non-optional section. VPs inherit this discipline on Day 1 — killing weak bets is a product-leadership skill, not an engineering-process artifact.
6. **Quiet authority.** The VP does not lead Stage 1 externally until Day 90. Until then, the CPO is publicly the Stage 1 owner and the VP is internally the rising owner. This protects the VP from being judged on work before they've had time to learn the system.

---

## Phase 1 — Immerse (Days 1–30)

**Theme:** _What is this place? Who runs what? What do our customers actually need?_

### Day 1 — Orientation

Owned by CPO + CHRO. One day, face-to-face (or video) with Marcus.

- Welcome + company context (mission, four active pipelines, why PM is expanding)
- Marcus's product philosophy + why the PRD template looks the way it does
- The 10-stage pipeline, walked through at a high level with a real shipped product as the example
- Scope of authority during the first 90 days (observer → co-author → lead)
- Introduction to the CHRO process steward and the weekly check-in rhythm
- Tour of the repo, documents, access provisioning

**Deliverable:** None. Listen.

### Week 1 — Get the Data In Front of You

The first week is about getting raw customer and product signal directly into the VP's hands, not about meetings.

- **Customer voice intake.** For VP Web: read the last 90 days of support tickets for web surfaces; read the last two quarterly NPS reports; read exit-interview summaries for churned customers. For VP API: same set, filtered to developer customers; read the last 90 days of developer forum threads, Stack Overflow tags, and GitHub issues on the SDK repos.
- **Dashboard access.** Provisioned to the relevant analytics stack (GA4 + Amplitude for Web; internal API analytics + Grafana for API). By end of Week 1 the VP can pull their domain's core metrics without help.
- **Portfolio read-out.** The VP reads every PRD shipped, in-flight, and killed for their pipeline in the last 12 months. Marcus writes a one-paragraph context note next to each killed PRD explaining why it was killed.
- **Competitive intel briefing.** CPO-led, 2 hours, covering the top 5 competitors for each domain and what we believe they're good at and bad at.

No stakeholder meetings this week beyond Marcus + CHRO. The VP needs to form their own priors before being shaped by stakeholder narratives.

### Week 2 — Meet the Customers, Meet the Partners

- **Customer interviews.** Minimum 3 for each VP. Real customers, booked by the product-ops function or directly by Marcus. 45-minute sessions. The VP takes notes and shares raw transcripts with the CPO.
- **R&D partnership introductions.**
  - VP Web: 1:1 with **Elena Vasquez** (VP of Web & Backend Engineering, R&D) + 1:1 with **Amira Voss** (Frontend Chapter Lead). The Elena relationship is the most important in the company for VP Web.
  - VP API: 1:1 with **Dev Malhotra** (Backend Chapter Lead, R&D) + 1:1 with **Elena Vasquez** (Dev's direct supervisor) + 1:1 with **Thomas Zhang** (DevOps Lead — relevant because API rate limits and scale are an infrastructure concern). The Dev Malhotra relationship is the most important in the company for VP API.
- **C-suite 1:1s.** 30–45 minutes each with CDO (Yuki Tanaka-Chen), CSO (Dr. Sarah Chen), CIO (Dr. Priya Mehta), CTO (Dr. Kenji Nakamura). Get their unvarnished read on what's working and what isn't in the current product model.
- **Design partnership introduction.** Shadow one CDO-led Stage 2 session to see how the PRD → prototype handoff happens today.

### Week 3 — Go Deep on the PRD Template

- **Template deep-dive with Marcus.** Four 90-minute sessions across the week. Marcus walks through three of his own PRDs — one shipped, one killed, one in-flight — and explains every section. The VP asks questions.
- **First PRD fragment.** The VP drafts one section of a real upcoming PRD for their pipeline — not the whole PRD, just one section. Marcus reads it, discusses what works and what needs adjustment. This is coaching, not grading.
- **Kill-criteria workshop.** One 90-minute session with Marcus specifically on how to write kill criteria that actually get used. This is the hardest part of the template to learn and the most consequential.

### Week 4 — Form a Point of View

- **Landscape Memo.** The VP writes a 3–5 page memo to the CPO answering four questions:
  1. What did I find? (the state of the domain as the VP now understands it)
  2. What are the top 3 opportunities worth pursuing over the next 2 quarters?
  3. What are the top 3 risks we are exposed to?
  4. What would I propose as my first quarterly bet?

  The memo is the primary deliverable of Phase 1. It replaces any rubric-based exam. It is assessed qualitatively by the CPO and forms the backbone of the 30-day check-in conversation.

- **30-day check-in conversation.** 90 minutes, CPO + VP + CHRO. Discussion of the Landscape Memo, the VP's read on the stakeholder ecosystem, and any calibration needed. No score. The output is a written shared note captured by the CHRO recording the main takeaways and any agreed adjustments to Phase 2.

### Phase 1 Commitments (What the Company Owes the VP)

- Calendar protection: no more than 40% of the VP's time is in meetings during Immerse. The rest is reading and thinking.
- Marcus is available for at least 3 hours per week of pairing during Phase 1.
- Access to every PRD, dashboard, and customer signal is provisioned by Day 3.
- No Stage 1 external responsibility. The VP is not expected to represent the company externally in their domain until Phase 3.

---

## Phase 2 — Contribute (Days 31–60)

**Theme:** _Co-own, co-draft, co-ship. Build credibility with R&D and Design through real work._

### Co-Authored PRD

Each VP picks one real upcoming Stage 1 PRD for their pipeline and co-authors it with Marcus. Marcus holds the pen for Sections 1–4 and 6–8; the VP holds the pen for Section 5 (platform-specific constraints) and the domain-specific parts of the Metrics and Launch Sequencing sections. They review each other's sections. Marcus signs off as the formal author; the VP's name appears as co-author.

This is the primary instrument of Phase 2. It is not a test. It is a real PRD that goes through Stage 2 → Stage 3 → downstream normally.

### R&D Partnership Rhythm

By end of Phase 2 the VP has established:

- A recurring weekly 30-minute sync with their R&D counterpart
  - VP Web ↔ Elena Vasquez
  - VP API ↔ Dev Malhotra (and a biweekly 30-minute sync with Elena and Thomas Zhang)
- A shared backlog visible to both sides
- An agreed working definition of "what PRD readiness looks like" for their domain (this flows into the domain-specific PRD template extension drafted in Phase 3)

### Stage 2 and Stage 3 Participation

- Attend the CDO-led Stage 2 prototype review for the co-authored PRD. The VP doesn't drive; they observe and contribute domain context.
- Attend the Stage 3 architecture review (CTO + CIO + Software Architect) where the PRD serves as input. Again, observe; contribute when the architect needs clarification on product intent.

### Stage 6 Observation

The VP attends one Stage 6 code review panel as an observer, for code in their pipeline. This is the first exposure to how the 5-officer panel actually operates. No participation at this stage — just presence.

### Domain-Specific PRD Template Extension (Draft)

The VP begins drafting Section 5 extensions for their domain. These live in their `skills/` folder as a working document, not yet finalized:

- VP Web: `skills/web-product-strategy.md` (draft state)
- VP API: `skills/api-product-strategy.md` (draft state)

Marcus reviews the draft and discusses trade-offs. The final version ships in Phase 3.

### 60-Day Check-In Conversation

90 minutes, CPO + VP + CHRO. The conversation covers:

- How did the co-authored PRD go? What did the VP learn? What did Marcus learn about the VP?
- Have the R&D relationships taken root? Any friction the CHRO should help resolve?
- Does the VP's Landscape Memo still hold up 30 days later, or has the thinking evolved?
- Is the VP on track to hold the pen solo in Phase 3? What's still in the way?

The output is a shared written note. If anything material is off-track, adjustments are made now — not at Day 90 when they become harder to address.

---

## Phase 3 — Lead (Days 61–90)

**Theme:** _Hold the pen. Earn the pipeline._

### Solo-Authored PRD

Each VP authors one Stage 1 PRD for their pipeline solo. Marcus is a reviewer and signatory; he does not co-author. The VP runs the PRD cycle end-to-end — intake from product-ops or stakeholders, framing, scoping, drafting, iteration, Stage 2 handoff.

### Q1 Product Roadmap

The VP presents a Q1 roadmap for their pipeline to Marcus and, at the end of Phase 3, to the C-suite panel (CPO + CTO + CIO + CSO + CDO). The roadmap includes:

- Proposed bets for Q1
- Kill criteria for each bet
- Metrics to watch
- Dependencies on R&D / Design / Security / Infra
- Anti-bets (things we explicitly are not doing)

The roadmap presentation is the VP's first piece of external-facing product leadership. It is also the most honest readout of whether the VP has learned the pipeline.

### Domain-Specific PRD Template Extension (Final)

The VP finalizes and merges their Section 5 extension skill file:

- VP Web: `skills/web-product-strategy.md` (merged, referenced by PRD template)
- VP API: `skills/api-product-strategy.md` (merged, referenced by PRD template)

Marcus integrates these into a revised `prd-authorship.md` that now explicitly supports Mobile / Web / API extensions. The revised template is the artifact that unlocks the pipeline amendments (see companion [`../pipeline-amendments/README.md`](../pipeline-amendments/README.md)).

### Stage 6 Participation

The VP participates in the Stage 6 code review panel as an advisor for code in their pipeline — still without veto authority, but contributing domain perspective to the CPO.

### Full-Stack Co-Authorship

The two VPs jointly scope one Full-Stack PRD as a dry run for the Full-Stack authorship model. Marcus observes but does not arbitrate unless asked. The purpose is to test whether the two VPs can work as genuine co-owners before the Full-Stack pipeline is formally transferred.

---

## Day 90 — Review + Decision Gate

A structured review conversation. 2 hours. CPO + VP + CHRO + CTO.

The conversation covers:

- The solo PRD: Marcus's read on quality, completeness, readiness. CTO's read on how it fed Stage 3.
- The Q1 roadmap: is it credible? Are the bets the right bets?
- The PRD template extension skill: does it hold up as a company-standard extension?
- Stakeholder signal: CHRO has conducted reverse-check-ins with Elena Vasquez / Dev Malhotra / CDO / CSO about the VP. What are they saying?
- The VP's own self-assessment: what still feels unresolved?

There are three outcomes:

| Outcome                           | Trigger                                                                                                   | Consequence                                                                                                                                                                                    |
| --------------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Full commencement**             | The solo PRD, roadmap, and stakeholder signal are all strong.                                             | Pipeline amendments execute (see [`../pipeline-amendments/README.md`](../pipeline-amendments/README.md)). VP takes Stage 1 authority for their pipeline and the relevant Full-Stack slice.     |
| **Course correction + extension** | One or two dimensions are not yet ready but the trajectory is clearly positive.                           | 30- or 60-day extension with an explicit, short list of what needs to change. Pipeline amendments deferred until extension review passes. CPO retains Stage 1 authority during the extension.  |
| **Mutual decision to part**       | Multiple dimensions are misaligned — especially if cultural/stakeholder signal is poor and not improving. | Handled as a mature leadership transition, not a termination. Severance per company policy. CHRO reopens the recruitment for the role. Pipeline amendments are not executed for that pipeline. |

A "course correction + extension" is the most likely outcome for at least one of the two hires. That's not a failure; it's a realistic reflection of what it takes to absorb a new product domain inside an opinionated PRD tradition.

---

## Sponsors and Cadence

### Sponsors

| Role                     | Sponsor                                                        | Responsibility                                                                                              |
| ------------------------ | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Primary                  | **CPO (Marcus Tran-Yoshida)**                                  | Template teaching, co-authoring, sign-off decisions. Primary 1:1 partner for the VP throughout the 90 days. |
| Process steward          | **CHRO (Dr. Evelyn Hartwell)**                                 | Runs check-ins, collects stakeholder signal, surfaces friction, owns the written record of each check-in.   |
| Pipeline context         | **CTO (Dr. Kenji Nakamura)**                                   | One hour in Week 1 on pipeline lifecycle; reviewer at Day 90.                                               |
| Design partnership       | **CDO (Yuki Tanaka-Chen)**                                     | Stage 2 shadow session in Week 2. Ongoing availability as partnership forms.                                |
| Security partnership     | **CSO (Dr. Sarah Chen)**                                       | One 1:1 in Week 2; SRD co-authorship on co-authored PRD in Phase 2.                                         |
| Architecture partnership | **CIO (Dr. Priya Mehta)**                                      | One 1:1 in Week 2; Stage 3 review observation during Phase 2.                                               |
| R&D counterpart          | **Elena Vasquez** (for VP Web) · **Dev Malhotra** (for VP API) | Weekly sync from Week 2 onward. Most important operational relationship.                                    |

### Weekly Cadence

| Cadence             | Participants                  | Length     | Purpose                                                                         |
| ------------------- | ----------------------------- | ---------- | ------------------------------------------------------------------------------- |
| Weekly 1:1          | CPO + VP                      | 30–45 min  | Pairing, questions, work-in-progress review                                     |
| Weekly check-in     | CHRO + VP                     | 20 min     | Process, stakeholder signal, things the VP might not raise with Marcus directly |
| Weekly R&D sync     | VP + R&D counterpart          | 30 min     | Backlog, PRD readiness, upcoming dependencies                                   |
| 30/60/90 day review | CPO + VP + CHRO (+ CTO at 90) | 90–120 min | Phase gate conversation                                                         |

---

## What We Don't Do

To be explicit about the design choices in this plan:

- **We don't grade with rubrics.** The Landscape Memo, co-authored PRD, and solo PRD are discussed qualitatively. Marcus's sign-off is the signal, not a score.
- **We don't have mandatory curriculum files authored by Chief Officers.** Each sponsor contributes to a single shared `onboarding-resources.md` (optional follow-up artifact) as they see fit. There is no requirement that the CSO or CIO produce a dedicated curriculum for two hires.
- **We don't use "PASS/FAIL" gates.** Check-ins are conversations with three possible outcomes (proceed, course-correct, part ways). Phase gates are calibration points, not exams.
- **We don't have an adversarial appeal protocol.** If the VP disagrees with a check-in outcome, they raise it with the CHRO in the normal course of business. The CHRO is the process steward; they will mediate.
- **We don't require the VP to pass a test on engineering artifacts.** The VP needs fluency with what an ADR, SRD, and UML diagram are for so they write PRDs that feed them. They don't need to match the CIO's architectural judgment. A 90-minute briefing from the CIO suffices.
- **We don't expect the VP to shadow mobile PRDs extensively.** One shadow session in Phase 1 for context is enough. The VP's domain is Web or API; that's where their time should go.

---

## Progress Record

The CHRO maintains a short running record of each check-in in `progress/tracker.md` (created when onboarding begins). Each entry includes:

- Date and participants
- Phase and day count
- Main topics discussed
- Agreed actions / adjustments
- Any escalation flags

This is a lightweight record, not a compliance artifact. Its purpose is to give the CPO and CHRO continuity between check-ins and to document the 90-day trajectory in case the outcome is a course correction or mutual part.

---

## Relationship to Other Documents

- The [`../product-management-fy2026-q2.md`](../product-management-fy2026-q2.md) master plan references this document for the onboarding summary.
- The [`../pipeline-amendments/README.md`](../pipeline-amendments/README.md) pipeline amendments are gated on the Day 90 outcome being "Full commencement."
- The [`../competency-matrices/README.md`](../competency-matrices/README.md) competency matrices govern selection (pre-hire), not onboarding (post-hire). They are not re-applied during this plan.

---

## Document History

| Version | Date       | Changes                                                                                                       | Status           |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------- | ---------------- |
| 1.0     | 2026-04-18 | Initial 90-day onboarding plan for two VP-tier Product Leaders. Phased Immerse / Contribute / Lead structure. | Pending Approval |

---

**Next step:** CPO review. Once the CPO is comfortable with the shape of the 90 days and the cadence of sponsorship, this plan is ready to activate on each VP's first day.
