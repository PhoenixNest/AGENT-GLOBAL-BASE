# Formation Report — Academic Neural Unit 00 (ANU-00)

**To:** CEO
**From:** Dr. Elias Vance, Laboratory Director, Core Component 00 (incubation lead for this
formation only)
**Date:** 2026-07-23
**Status:** ~~For CEO evaluation — User Approval gate, hard stop~~ → **Approved — recruitment
executed (see §6, CEO Decision, 2026-07-23).**
**Supporting record:** `meeting-minutes.md` (this folder), `prospective-hires.md` (this folder)

---

## 1. Charter Recap

Per the CEO's directive, this report addresses:

1. Formation of ANU-00, spearheaded by Dr. Vance and CC-00 advisors.
2. A decision on whether additional personnel are needed, with a prospective-hire list if so.
3. Confirmation that ANU-00 has no direct organizational link to `core-component-00/` — CC-00's
   role is incubation only.

---

## 2. Boundary Statement — ANU-00 and CC-00

This is the load-bearing clarification from the CEO and is restated here explicitly so the
boundary is unambiguous in the CEO's own review record:

- **No governance link.** Dr. Vance and CC-00 hold **no** standing authority over ANU-00 — not
  ASE ratification, not pipeline stage ownership, not personnel authority. CC-00's role ends at
  incubation: providing research-methodology grounding and advisory input while ANU-00 stands
  itself up.
- **No shared reporting line.** ANU-00 personnel will not report into Dr. Vance or any CC-00 crew
  member. ANU-00 needs its own lead (see §4).
- **No folder/document merge.** This formation record lives entirely under
  `academic-neural-unit-00/`. Nothing in `core-component-00/` has been or should be modified to
  represent ANU-00 as part of the CC-00 lab.
- **One universal exception — ASE governance.** Root `CLAUDE.md` §9 makes the Agent Systems
  Engineering framework mandatory for **all** LLM-powered systems in this workspace, not just
  CC-00's. If ANU-00 later builds LLM-powered tooling (e.g., an ingestion pipeline for its
  knowledge base), that tooling is bound by ASE the same way any other workspace system is. This
  is a technical-standard obligation shared workspace-wide, not a governance link back to CC-00 or
  Dr. Vance specifically — flagging it here to avoid it being read as contradicting "no direct
  link."

---

## 3. Proposed Charter for ANU-00

| Element                       | Definition                                                                                                                                                                                                                                                                                                                  |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mission**                   | Conduct primary academic research in frontier computer science, artificial intelligence, neural networks, and software engineering, and build a durable, navigable knowledge base from that research.                                                                                                                       |
| **Type**                      | Independent academic research entity — a fourth co-resident system alongside The Company, The Studio, and CC-00 Lab.                                                                                                                                                                                                        |
| **Scope boundary vs. CC-00**  | CC-00 is applied engineering (production-grade patterns, reference implementations for LLM systems used across the organization). ANU-00 is primary academic research — it is not expected to ship production code, and its output is knowledge (research reports, syntheses, literature reviews), not engineering modules. |
| **Knowledge base convention** | Follows the workspace's existing dated research-archive pattern (`YYYY-MM-DD-<slug>/research-report.md`) already used by `company/telescope/`, `studio/casual-games/telescope/`, and `core-component-00/telescope/` — for consistency of navigation, not as a link to any one of those archives.                            |
| **Governance**                | Subject to workspace-wide ASE for any LLM-powered tooling it builds (§2 above). Not subject to CC-00 ASE ratification authority, Company pipeline stage gates, or Studio pipeline stage gates unless it chooses to consume one of those pipelines for a specific deliverable.                                               |

### 3.1 Refinement — Stage-of-Inquiry Framing (CEO-approved 2026-07-23)

**Approved.** The CEO confirmed this refinement on 2026-07-23. It now stands as part of ANU-00's
charter, alongside (not replacing) the output-type framing in the table above — see the migrate-
vs-task distinction below, which is binding, not aspirational, going forward.

In discussion following this report's original filing, the CEO characterized the CC-00/ANU-00
distinction differently than the output-type framing in the table above: CC-00 was founded to put
theory into practice and implementation; ANU-00 exists to investigate and explore cutting-edge
fields and evaluate new technologies. This is a genuine sharpening, not a restatement — the table
above distinguishes the two orgs **by output type** (production code vs. research reports); the
CEO's framing distinguishes them **by stage of inquiry**:

- **CC-00** takes theory or technique already validated as workable and hardens it into
  production-grade implementation — _post-validation_ work, regardless of how novel the
  underlying idea is.
- **ANU-00** investigates whether a theory or technique is workable or worth pursuing at all —
  _pre-implementation_ work, regardless of which of its four charter fields it falls under.

This framing gives a cleaner per-programme test than restating a boundary sentence for each new
role (as `prospective-hires.md` originally did for the software-engineering specialist): ask
whether the question is "does this work / is it worth building" (ANU-00) or "given that it works,
how do we build it reliably" (CC-00) — not which field's vocabulary it happens to use. This
matters concretely for the CEO's separate directive to intensify ANU-00 research in LLMs, ML, AI,
and agent engineering (raised in advisory discussion, not yet a filed decision): "investigate
emergent multi-agent coordination behavior" is ANU-00 under this test even though it uses CC-00's
vocabulary; "harden a coordination pattern into a reusable orchestration module" would be CC-00,
for the same reason.

**Tension this framing surfaces, stated explicitly rather than smoothed over:** a stage-of-inquiry
distinction implies a _pipeline_ — ANU-00 investigates and evaluates, CC-00 implements what clears
the bar — which reads uncomfortably close to the "direct link" the CEO's original ruling in §2
prohibits. This is resolved, not contradicted, by one distinction that must hold going forward:

- **Findings migrating** from ANU-00 into a future CC-00 programme is ordinary research uptake —
  the same way CC-00 might draw on any external published research — and creates no reporting
  line or governance dependency. This is consistent with §2's boundary as originally stated.
- **ANU-00 being tasked** by CC-00, Dr. Vance, or the CEO to de-risk a specific item already on
  CC-00's roadmap, on request, would recreate the direct link §2 prohibits — that is a
  service-provider relationship, not an independent research charter, regardless of how the
  tasking is framed.

**Disposition (executed):** the stage-of-inquiry framing is now the primary per-programme test,
alongside the output-type framing in the table above, which remains true as a description of
typical results. The migrate-vs-task distinction is stated explicitly wherever this charter is
cited, including in Dr. Mokoena's
`academic-neural-unit-00/crew/lead/naledi-mokoena/skills/research-programme-chartering.md`, which
should be updated to reference this test — tracked as a follow-up, not done as part of this
records update.

---

## 4. Recruitment Decision

**Outcome of the internal formation meeting (`meeting-minutes.md`): recruitment is necessary.**

Rationale, in brief (full discussion in `meeting-minutes.md` §3.3):

- ANU-00 cannot be organizationally independent while running on borrowed CC-00 crew capacity —
  doing so would recreate the exact coupling the CEO's "no direct link" clarification is meant to
  prevent.
- CC-00 crew members are each already scoped to a specific module or cross-cutting mandate
  (`core-component-00/crew/README.md`); none has standing capacity or a personnel-authority
  mandate to originate and staff a second organization's research programme. Recruitment and
  personnel evaluation is CHRO authority, not CC-00's, in any case.
- ANU-00 needs a permanent lead of its own — Dr. Vance's involvement here is a one-time incubation
  act, not a standing directorship.

**Recommended approach: phased recruitment**, mirroring the pacing discipline CC-00 itself applied
during its own build-out (`crew/README.md`'s Composition Assessment: avoid headcount added before
a crew has shipped anything together).

> **Naming note:** the two tranches below were superseded by the CEO's ruling in §6 before either
> was executed under this name — they never became the workspace's "Phase 1" / "Phase 2." This
> report deliberately does not use "Phase 1" / "Phase 2" for them, to avoid colliding with the
> unrelated, later, actually-executed recruitment-cycle phases of the same name documented in §7
> and `company/recruitment/academic-neural-unit-00-fy2026-q3/recruitment-plan.md` (the Founding
> Cohort and the Elite Expansion Cohort — 5 roles and 5 roles, not the 2-and-3 split below).

- **Recommended now:** 2 hires. An ANU-00 Lead and one generalist Research Scientist. Sufficient
  to legally/organizationally stand up the entity, ratify its own first research agenda, and
  establish the knowledge-base structure.
- **Flagged, not requested in this report:** 3 further roles (domain Research Scientists for
  AI/neural networks and for software engineering, plus a knowledge-systems engineer), once the
  first 2 hires have a track record to hire against.

Full role profiles: `prospective-hires.md` (this folder).

**Deferral flag (per `company/recruitment/README.md` and `core-component-00/crew/README.md`'s
Deferral Review convention):** deferring the flagged 3-role set as "not now" is this group's own
judgment and is explicitly flagged here for independent CEO/CHRO confirmation before it is treated
as final — consistent with the convention that an assessor recommending deferral of a known need
does not get the last word unassisted.

---

## 5. Requested CEO Actions

This report is presented for evaluation. Requested decisions:

1. **Approve or amend** the ANU-00 charter and CC-00-incubation-only boundary as stated in §2–§3.
2. **Approve, amend, or reject** the initial 2-hire recruitment recommendation in §4 /
   `prospective-hires.md`.
3. **Confirm or override** the flagged 3-role deferral in §4, per the Deferral Review convention.
4. If the initial 2-hire recommendation is approved, **direct CHRO** to open a hiring cycle at
   `company/recruitment/academic-neural-unit-00-fy2026-q3/` under the standard 9-stage recruitment
   pipeline (`company/pipeline/recruitment/pipeline.md`).
5. If desired, direct that the root `CLAUDE.md` repository map (§2, §4) be updated to list ANU-00
   as a fourth co-resident system — not done in this record, since it is a workspace-wide document
   change outside this formation record's scope and appropriately gated by CEO sign-off first.

**This is a hard stop.** No further action — recruitment cycle creation, root document updates, or
ANU-00 operational activity — proceeds until the CEO responds.

---

## 6. CEO Decision (2026-07-23)

**Ruling:** Approved, with the phasing in §4 overridden — **full-scale recruitment**, not a
phased build-out. All 5 identified roles (the initial 2-hire recommendation plus the flagged
3-role set, combined: ANU-00 Lead, generalist Research Scientist, AI/Neural-Networks Research
Scientist, Software-Engineering/CS Research Scientist, Knowledge Systems Engineer) are approved in
a single hiring cohort — this becomes the "Founding Cohort" named in §7 and
`recruitment-plan.md` — so ANU-00 launches as a fully-resourced, comprehensive research
organization from day one rather than growing into one over successive cycles. The flagged 3-role
deferral in §4/§5, for CEO/CHRO confirmation, is **not confirmed — it is overridden.**

**Authorization:** CHRO is authorized to open the hiring cycle immediately under the standard
9-stage recruitment pipeline (`company/pipeline/recruitment/pipeline.md`) and to report final
results upon completion, without a further CEO check-in between requisition and Stage 9 outcome.

**Execution record:** `company/recruitment/academic-neural-unit-00-fy2026-q3/` (recruitment plan,
candidate evaluations, phase summary, hiring outcome report). Hired agent profiles:
`academic-neural-unit-00/crew/`.

**Status update:** This report's status is now **Approved — recruitment executed**, superseding
the "For CEO evaluation" hard-stop status at the top of this document.

---

## 7. Staff Expansion Execution (2026-07-23) — Consolidated Report

This section consolidates everything decided after §6, for the CEO's single-reference record.

**Sequence of events:**

1. The CEO characterized CC-00 and ANU-00 by stage of inquiry rather than output type; Dr.
   Mokoena's group assessed this as a genuine sharpening and drafted a refinement — recorded in §3.1.
2. The CEO **approved** the §3.1 refinement.
3. The CEO directed ANU-00 to intensify research in LLMs, ML, AI, and agent engineering, told Dr.
   Mokoena not to be frugal with headcount, and set a "top Ivy League / leading research
   institution" recruiting standard.
4. Dr. Mokoena proposed 5 roles against that directive (1 L4 Staff Research Scientist anchor + 4
   L3 Research Scientists: Machine Learning Theory, LLM Systems, Applied AI Systems, Agent Systems
   Research), operationalizing the institution standard as **evidentiary caliber**, not
   institutional pedigree — consistent with CHRO's own vetting philosophy.
5. The CEO **delegated full execution authority** for this expansion to Dr. Mokoena — the same
   pattern used for Dr. Vance during CC-00's own Phase 3. As with that precedent, delegated
   execution did not bypass CHRO's pipeline authority: CHRO's office signed every candidate.

**Outcome:** Phase 2 ("Elite Expansion Cohort") executed and closed the same day. All 5 roles
filled, all candidates clearing tier floor (17–19/20), zero conditional approvals. Full detail:
`company/recruitment/academic-neural-unit-00-fy2026-q3/` (`recruitment-plan.md` v1.1,
`candidates/06`–`10`, `phase-summaries/phase-2-summary.md`, `hiring-outcome-report.md`'s Phase 2
addendum — **HIRING OUTCOME: APPROVED**, no open findings).

**Resulting structure:** ANU-00 now has 10 FTEs and 2 organizational layers — Dr. Mokoena (7
direct reports) and Dr. Bhandari (2 direct reports, absorbed as part of a deliberate
span-of-control restructure applied within the same phase, not caught later by audit as happened
at CC-00). Full roster: `academic-neural-unit-00/crew/README.md`.

**Boundary discipline maintained throughout:** every Phase 2 role was scoped and, per its
candidate file, interviewed against the stage-of-inquiry test and the specific CC-00 module it is
adjacent to in vocabulary (Applied AI Systems / LLM Systems vs. CC-00's engineering modules; Agent
Systems Research vs. `multi-agent-engineering/` specifically) — sequencing placed the
highest-boundary-risk role (Agent Systems Research) last, so its non-overlap could be demonstrated
by precedent rather than asserted by charter language alone.

**Nothing further requires CEO action on this thread** unless the CEO wants to revisit any
individual decision above — this section is the closing record, not a new request.

---

## 8. Documentation Hygiene Pass (2026-07-23) — For CEO Sign-Off

**Status: hard stop.** Work is complete; presented here for final CEO sign-off per this report's
own stage-gate convention (root `CLAUDE.md` §1). No further edits are made pending that sign-off.

Following §7's expansion, a documentation review found and corrected three ambiguity issues in
how recruitment-cycle terminology had leaked into permanent identity/reference documents. None of
the underlying decisions in §1–§7 changed — this is a records-hygiene pass only.

### 8.1 What was found and fixed

1. **Bare recruitment-phase labels in `crew/README.md`.** The directory tree and Roster table
   tagged individual crew members `(Phase 1)` / `(Phase 2)` — a recruitment-pipeline sequencing
   label, not a fact about current org structure. Fixed by relabeling to the formal cohort names,
   then — per a direct CEO request the same day — **removed entirely**, since the tags indicated
   neither hierarchy position nor organizational tier and duplicated information already canonical
   in each profile's `recruitment-phase` frontmatter and
   `company/recruitment/academic-neural-unit-00-fy2026-q3/`. `crew/README.md` now describes
   current structure only (role, level, reporting line); hiring history is not repeated there.
2. **A genuine naming collision, not just cosmetic ambiguity.** `formation-report.md` §4 and
   `prospective-hires.md` used "Phase 1" / "Phase 2" for the _original, superseded_ recommendation
   (2 hires / 3 hires, never executed under that name) — a different scheme from the _actually
   executed_ "Phase 1" / "Phase 2" in `recruitment-plan.md` (Founding Cohort / Elite Expansion
   Cohort, 5 roles each). Fixed: §4/§5/§6 above reworded the superseded recommendation without
   "Phase" labels; `prospective-hires.md` and `meeting-minutes.md` (left otherwise unedited, per
   meeting-minutes being a historical record) each got an explicit collision-warning note.
3. **Folder-tree comments in the top-level `academic-neural-unit-00/README.md`** were updated to
   match both fixes above, for consistency across the two roster-facing documents.

### 8.2 Files changed in this pass

- `academic-neural-unit-00/crew/README.md`
- `academic-neural-unit-00/README.md`
- `academic-neural-unit-00/formation/2026-07-23-formation-meeting/formation-report.md` (this file,
  §4–§6 reworded)
- `academic-neural-unit-00/formation/2026-07-23-formation-meeting/prospective-hires.md`
  (collision-warning note added)
- `academic-neural-unit-00/formation/2026-07-23-formation-meeting/meeting-minutes.md`
  (reader's note added; discussion record itself unedited)

**Not touched, deliberately:** `company/recruitment/academic-neural-unit-00-fy2026-q3/` and every
individual crew member's `profile.md` — both already use one consistent, correctly-scoped "Phase
1"/"Phase 2" vocabulary with no collision risk, so no change was needed there.

**Requesting:** final CEO sign-off that this closes the ANU-00 formation and expansion thread with
no outstanding documentation-quality issues.

---

## 9. Final Review (2026-07-23) — Establishment and Recruitment Confirmed

Per the CEO's request, the two relevant heads — Dr. Naledi Mokoena (ANU-00 Lead) and Dr. Evelyn
Hartwell (CHRO) — independently verified the underlying records (not restated prior claims) and
jointly confirmed: **establishment complete, recruitment complete (10/10 roles, no open
findings).** Full review, including each reviewer's own verification method and findings:
`final-review.md` (this folder).

One item is named as a deliberate deferral, not a gap: the root `CLAUDE.md` repository map does
not yet list ANU-00 as a fourth co-resident system (§5, item 5), pending explicit CEO direction.

**This is the closing status for the entire ANU-00 formation and expansion thread, awaiting CEO
final sign-off per `final-review.md`'s joint recommendation.**

---

## 10. Repository Map Updated (2026-07-23) — §5 Item 5 Resolved

The CEO gave explicit direction to close the one item §9 flagged as deferred (not missing). Root
`CLAUDE.md` §2 and §4 now list ANU-00 as the fourth architecturally independent, co-resident
system, alongside The Company, The Studio, and the CC-00 Lab — with its incubated-not-governed
relationship to CC-00 stated inline, consistent with §2's boundary statement above. No CLAUDE.md
exists yet for `academic-neural-unit-00/` itself, so the repository map does not add a
`[→ CLAUDE.md]` marker for it, unlike the other three systems; the map points to
`academic-neural-unit-00/README.md` instead.

**With this, every item raised across §1–§9 is either resolved or explicitly and knowingly
deferred (none remain open by omission). The ANU-00 formation and expansion thread is closed.**
