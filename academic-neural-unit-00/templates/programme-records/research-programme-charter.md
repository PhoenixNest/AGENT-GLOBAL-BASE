# Research Programme Charter — [Programme Title]

<!-- Copy this file to academic-neural-unit-00/knowledge-base/YYYY-MM-DD-<slug>/charter.md at the
     moment a programme is chartered — per research-programme-chartering.md step 6, the dated entry
     is opened at charter time, BEFORE findings exist, so the programme is discoverable from the
     moment it starts. Do not fill this in inside templates/ itself.

     This is a point-in-time record. A charter that changes materially is re-chartered as a new
     file with a pointer back to this one — never edited in place. -->

**Programme slug:** [`YYYY-MM-DD-<slug>` — must match the knowledge-base folder name]
**Charter date:** [YYYY-MM-DD]
**Originated by:** [Name, ANU-00 role]
**Status:** [Proposed / Ratified / Declined — see §8]

---

## 1. Origination

<!-- Per research-programme-chartering.md § When to Use, a question enters chartering from exactly
     one of the origins below. This field exists to keep origination inside ANU-00. If the true
     origin is not on this list, STOP and escalate to Dr. Mokoena before filling anything else in —
     see the boundary note under §4. -->

| Valid origin                                              | This programme? |
| --------------------------------------------------------- | --------------- |
| Dr. Mokoena (ANU-00 Lead)                                 | [ ]             |
| An ANU-00 Research Scientist                              | [ ]             |
| Surfaced by the knowledge base's own literature synthesis | [ ]             |
| Pre-screened by Dr. Bhandari for the Foundational AI pod  | [ ]             |

**Origination note:** [One or two sentences — what prompted the question.]

---

## 2. Research Question

<!-- Step 1. One sentence. It must be answerable by primary academic research — literature
     synthesis, theoretical analysis, or original investigation. If it takes a paragraph, it is not
     yet scoped enough to charter. -->

> [The research question, in one sentence.]

**Charter field(s):** [One or more of: computer science · artificial intelligence · neural
networks · software engineering. A question outside all four is outside ANU-00's charter entirely.]

**Answerable by:** [Literature synthesis / theoretical analysis / original investigation]

---

## 3. Falsifiability Condition

<!-- Step 2, and the single most-cited discipline across this crew's skill files (Baek §1,
     Okonkwo §1, Roldán §1, Dubois §1, Fujimori §1, Tan §1). A programme without a falsifiable
     failure condition is NOT chartered — it is logged in open-question-log.md as an open question
     for later refinement instead. Leaving this section blank is not an option that produces a
     valid charter; it is the signal to route elsewhere. -->

**What result would prove the working hypothesis wrong:**

[State the specific result, observation, or bound that would disprove the hypothesis.]

**Domain-specific scoping required before this counts as falsifiable** — fill in the row matching
this programme's primary domain, delete the rest:

| Primary domain                           | Additional scoping required                                                                     | Source                                       |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------- |
| Neural networks / AI systems             | [Stated disproof condition, not merely a direction of inquiry]                                  | `neural-systems-research-design.md` §1       |
| Machine learning theory                  | [Explicit assumption set + regime of applicability]                                             | `learning-theory-research-design.md` §1      |
| Software engineering / CS                | [Explicit metric AND population — "what is measured, over what population"]                     | `software-engineering-research-design.md` §1 |
| LLM systems                              | [Specific conditions, prompting setup, and what counts as the capability failing to hold]       | `llm-behavior-evaluation-design.md` §1       |
| Applied AI feasibility                   | [The stated cost/benefit bar for "worth pursuing" — set before evaluating, not concluded after] | `applied-ai-feasibility-research.md` §1      |
| Agent coordination / emergence           | [Specific agent population, environment, and observation criteria]                              | `agent-coordination-theory-research.md` §1   |
| Cross-field (two or more charter fields) | [Decomposition into per-field sub-claims — do not synthesize before decomposing]                | `cross-domain-literature-synthesis.md` §1    |

---

## 4. Boundary Check — Stage of Inquiry

<!-- Step 3, applying the CEO-approved charter refinement (formation-report.md §3.1). Judge by
     STAGE OF INQUIRY, not by which field's vocabulary the question uses. This section is mandatory
     on every charter — not only on ones that look like they might blur. -->

**Stage of inquiry:**

- [ ] **Pre-implementation** — "does this work / is it worth pursuing" → ANU-00's charter
- [ ] **Post-validation** — "given that it works, how do we build it reliably" → CC-00's charter;
      this question is not ANU-00 scope

**One-sentence justification:** [Why this question sits at the stage ticked above.]

**By-name check** — required for software-engineering and agent-coordination programmes, and good
practice for all (`software-engineering-research-design.md` §2, `agent-coordination-theory-research.md` §2):

[State by name which CC-00 module or mandate this question is being checked against — e.g.
`core-component-00/engineering/multi-agent-engineering/` — and why it does not belong there. If the
distinction is not obvious, escalate to Dr. Mokoena before proceeding rather than guessing.]

**Migrate-vs-task attestation** (binding, `formation-report.md` §2 and §3.1):

- [ ] This programme originated inside ANU-00 (see §1) and was **not** requested by CC-00, Dr.
      Vance, or the CEO as de-risking work for a specific item already on CC-00's roadmap.

<!-- If that box cannot be ticked, do not charter this programme. Tasking of that kind recreates
     the direct link the CEO's ruling prohibits — decline or escalate to the CEO instead. A finding
     that later migrates into a CC-00 initiative is ordinary research uptake and needs no special
     ratification; being handed the assignment up front is the thing that does not. -->

---

## 5. Governing Design Skill

<!-- Which crew member's research-design skill governs execution. This is not the same as ownership
     (§6) — a programme owned by one researcher may still be governed by another's rules where it
     crosses into their specialty. -->

**Governing skill file:** [`crew/.../skills/<skill>.md`]

**Named additional requirements this skill imposes on the final report:**

- [e.g. "Report effect sizes and confidence, not only significance" — `software-engineering-research-design.md` §4]
- [e.g. "Report emergence conditions, including under what conditions it does not emerge" — `agent-coordination-theory-research.md` §4]
- [e.g. "Plain-language summary required in addition to the technical treatment" — `neural-systems-research-design.md` §4]

---

## 6. Ownership

<!-- Step 4. Cross-field programmes may name a primary owner plus a contributor from an adjacent
     specialty. Depth gaps get routed to a specialist for review before publishing — never
     published shallow (cross-domain-literature-synthesis.md §3). -->

| Role                               | Name   | Basis                                      |
| ---------------------------------- | ------ | ------------------------------------------ |
| Primary owner                      | [Name] | [Domain fit]                               |
| Named contributor (if cross-field) | [Name] | [Which sub-claim they cover, and why]      |
| Specialist reviewer (if depth gap) | [Name] | [Which sub-claim exceeds generalist depth] |

**Overlap resolved before assignment?** [State how, if this question sat at a boundary between two
specialties — e.g. Baek/Okonkwo per `learning-theory-research-design.md` §2, or Dubois/Tan per
`foundational-ai-research-coordination.md` §2. Resolve ownership before either researcher invests
significant time.]

---

## 7. Tooling Needs — Scoped Out, Not Absorbed

<!-- Step 3's tail: if answering the question requires building production tooling, scope ONLY the
     research component here and record the tooling need as a referral, not as ANU-00 scope. A
     one-off harness built to observe behavior is fine; a reusable framework is not
     (agent-coordination-theory-research.md §3). -->

- [ ] No tooling beyond one-off, non-reusable instrumentation is required.
- [ ] Tooling need identified → filed as `referral-note.md`, path: [`...`]

---

## 8. Ratification

<!-- Step 5. Non-delegable — programme direction is the Lead's core mandate per her Assigned Role.
     Dr. Bhandari pre-screens for her pod but does not approve (foundational-ai-research-coordination.md §3). -->

| Field                   | Value                                                                 |
| ----------------------- | --------------------------------------------------------------------- |
| Ratified by             | Dr. Naledi Mokoena, ANU-00 Lead                                       |
| Date                    | [YYYY-MM-DD]                                                          |
| Decision                | [Ratified / Declined / Returned for scoping]                          |
| If declined or returned | [Reason, and where it went instead — normally `open-question-log.md`] |

---

## 9. Archive Entry

**Knowledge-base path:** `academic-neural-unit-00/knowledge-base/[YYYY-MM-DD-<slug>]/`
**Report file:** `research-report.md` — [Opened at charter time / Not yet opened]

**Taxonomy category:** [Category. If this programme does not fit the current taxonomy cleanly,
resolve the taxonomy gap first with Tobias Lindqvist rather than ingesting under a forced-fit
category — `knowledge-base-ingestion-architecture.md` §1.]
