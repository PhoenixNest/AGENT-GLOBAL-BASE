# Reflection — core-component-00-fy2026-q3 Recruitment Cycle

| Field              | Value                                                                                        |
| ------------------ | -------------------------------------------------------------------------------------------- |
| **Document Type**  | Post-cycle reflection — process retrospective, not a hiring decision record                  |
| **Plan ID**        | `core-component-00-fy2026-q3`                                                                |
| **Authors**        | Dr. Elias Vance (Laboratory Director) + Dr. Evelyn Hartwell (CHRO)                           |
| **Date**           | 2026-07-03                                                                                   |
| **Audience**       | CEO, and any future recruiter running a CC-00 or company-wide cycle                          |
| **Classification** | Internal — Leadership Only                                                                   |
| **Related docs**   | `recruitment-plan.md`, `candidates/*.md`, `phase-summaries/*.md`, `hiring-outcome-report.md` |

---

## Why this document exists

This cycle went through three plan revisions, one director-authored organizational audit, one
independent CHRO governance audit, and one retroactive scoring correction that touched 7 of 11
hires — all in a single day, all on the record. That density of self-correction is a good sign for
this specific cycle. It is not a substitute for fixing the conditions that made so much correction
necessary. This document is those conditions, named plainly, so the next cycle needs fewer of them.

---

## Issue 1 — Deferred risk framed as "future work" undercounts urgency

**What happened:** Dr. Vance's original Composition Assessment (`core-component-00/crew/README.md`)
identified four real structural gaps after the first 4 hires — bus factor, no research-scientist
tier, no safety function, no infra support — then recommended waiting a full quarter before acting
on any of them. The CEO reviewed the same facts and reached a different conclusion: three amendment
cycles later (v1.1 → v1.3), all four gaps were closed in the same expansion, not the next one.

**Root cause:** "This is real but not urgent" is a judgment call, and the person making it was also
the person who would carry the cost of acting on it sooner (more direct reports, more onboarding
load). That's not misconduct — it's an incentive worth naming so it can be checked, not trusted to
self-correct.

**What changed (executed 2026-07-03):** a **Deferral Review** convention is now recorded in
`company/recruitment/README.md` § 2 Conventions — any staffing or composition assessment that
recommends deferring action on a named risk must route to the CEO or CHRO for confirmation before
the deferral is treated as final. `core-component-00/crew/CLAUDE.md` carries a pointer to this
rule, since CC-00's own Composition Assessments are the artifact type that motivated it.
Self-assessed "not urgent" is no longer the last word when the assessor has a stake in the answer.

---

## Issue 2 — Reporting structure defaulted to flat, and flat breaks past ~6 reports

**What happened:** The original Phase 3 org design routed all 7 new hires to Dr. Vance directly,
bringing his total direct reports to 11. This wasn't caught until Dr. Vance's own pre-execution
audit — a step that only happened because the CEO explicitly asked for one. It was fixed
(module-paired ICs now report to their lead, dropping Vance's direct span to 7) before any hire
started, so no one operated under the broken structure. But it shipped in the first draft.

**Root cause:** The recruitment plan template has no field that forces a reporting-line sanity
check as headcount scales. Nothing in `recruitment-plan.md`'s template prompts "does span of
control still make sense at this size" — it has to be caught by inspection.

**What changed (executed 2026-07-03):** `company/recruitment/template/recruitment-plan.md` now
requires a **Span-of-Control Check** subsection directly under Division / Org Structure — every
role with more than 5 direct reports in the draft must be listed with a justification or a
restructure applied, and the plan may not move from Draft to Approved with an unresolved row. This
is a template gate, not a reviewer's judgment call — it would have caught this cycle's own error on
the first read.

---

## Issue 3 — "Is this redundant with an existing function" wasn't asked before the req opened

**What happened:** The Infrastructure Engineer role was flagged by Dr. Vance's own audit as
possibly duplicating R&D's existing DevOps Lead and SRE Engineers — a legitimate question that
turned out to have a clean answer (R&D's bench serves the parent company only), but the question
was asked _after_ the role was already scoped and staged for hiring, not before.

**Root cause:** Nothing in the recruitment plan process requires checking for adjacent existing
capability elsewhere in the org before opening a new req. This is a cross-department blind spot,
not a CC-00-specific one — any department could propose a role that duplicates another team's
existing function and nothing in the pipeline would catch it structurally.

**What changed (executed 2026-07-03):** Stage 1 (Role Intake) in
`company/pipeline/recruitment/pipeline.md` now requires an **Adjacent Capability Check** as part
of the intake request — the requesting department head names the departments most likely to have
adjacent capability and states why the new req isn't redundant with them. Not a veto step; a
required, documented check, the same way no-outsourcing compliance is documented rather than
assumed.

---

## Issue 4 — Leadership Signal was scored by inference, not evidence, and it was systemic

**What happened:** All 7 Phase 3 candidates were scored 4/5 on Leadership Signal. None of the
seven write-ups cited the rubric's own signal question ("who did they grow, where are they now").
CHRO's Stage 9 audit caught this as "one dimension is thin." On retroactive correction, 6 of the 7
corrected totals fell below the sum-based tier floor — a materially bigger gap than the original
framing suggested, and CHRO said so plainly in her addendum rather than let the smaller framing
stand.

**Root cause, stated precisely:** `vet-candidate.md` asked scorers to assign a number 1–5 per
dimension but did not require evidence to accompany the number. Without that requirement, scoring
under time pressure defaults to inference from seniority level ("L4, so probably a 4") rather than
interrogation of the actual record. This is a template design flaw, not an individual lapse — it
happened identically across two different interviewers (Dr. Vance and, independently, whoever
each candidate's Stage 6/7 reviewers were) and seven different candidates. A failure mode that
consistent is a process gap, not seven unrelated mistakes.

**Secondary finding, from CHRO's own addendum:** her office's Stage 7 Secondary Officer Review is
supposed to catch exactly this — an unsupported score — and did not, seven times. She named that
as her own office's gap, not only Dr. Vance's.

**What changed (already executed):**

- `vet-candidate.md` now requires cited signal-question evidence for every numeric dimension
  before a score is accepted. "Not established" is now an explicit, acceptable, honest answer —
  the template previously had no way to say that without either inventing evidence or leaving a
  number unjustified.
- Stage 7 Secondary Officer Review now checks for that evidence explicitly, not just that a
  number exists in range.
- All 7 affected files carry a visible, dated amendment — struck-through original score, corrected
  score, and rationale — not a silent rewrite. The audit trail shows what was wrong and what
  changed, which is the entire point of keeping one.

**What this did _not_ do:** reopen any hiring decision. CHRO's ruling (recorded in full in
`hiring-outcome-report.md` and `phase-summaries/phase-3-summary.md`) holds that the sum-floor table
is a screening heuristic, not the pipeline's actual pass/fail logic — every affected candidate
cleared the real gate (dimension-count pass on Impact, Craft, Standards) independent of Leadership.
That distinction between "the floor number" and "the pass logic" is itself worth flagging: **the
two mechanisms can now diverge after a retroactive correction, and nothing in the pipeline
documentation currently says which one governs when they disagree.** This cycle resolved it by
CHRO ruling, once. It should be a documented rule, not a one-time judgment call, before it comes
up again.

---

## Cross-cutting insight: self-review vs. independent review

Every real finding in this cycle came from a review that was _not_ conducted by the person whose
work was being reviewed:

- Dr. Vance's org-design flaw (Issue 2) was caught by an audit the CEO required, not one Dr. Vance
  initiated unprompted for himself.
- The Leadership Signal gap (Issue 4) was caught by CHRO auditing Dr. Vance's interviews — a
  different office, a different rubric-holder.
- CHRO's own Stage 7 gap was caught by her own retroactive review of her own prior sign-off, which
  is the weakest form of independence in this list, and she said so.

The pattern holds: **independent review finds things self-review doesn't, and the more genuinely
independent the reviewer, the more real the finding.** Issue 1's fix (second opinion required on
any "defer this risk" call) and Issue 3's fix (named cross-department check before opening a req)
are both instances of the same principle, now built into the process instead of left as
recommendations — a required field and a routing rule, not something a future reviewer has to
remember to ask for. Future cycles should keep building independent checks in before the fact, not
discover the value of one after the fact.

---

## Summary table

| #   | Issue                                         | Status                                      | Structural fix in place?                                                                                      |
| --- | --------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| 1   | Deferred-risk framing lacked a second opinion | Resolved this cycle (CEO override)          | **Yes** — Deferral Review convention in `company/recruitment/README.md`, cross-referenced in `crew/CLAUDE.md` |
| 2   | Flat reporting structure at 11 direct reports | Fixed pre-execution                         | **Yes** — Span-of-Control Check required in `company/recruitment/template/recruitment-plan.md`                |
| 3   | No redundancy check before opening a req      | Resolved this cycle (CEO clarification)     | **Yes** — Adjacent Capability Check required at Stage 1 in `company/pipeline/recruitment/pipeline.md`         |
| 4   | Leadership Signal scored without evidence     | Corrected retroactively, hires not reopened | **Yes** — `vet-candidate.md` gate change + Stage 7 process change, both live                                  |

All four issues now have a durable fix in the workspace, not just a recommendation on record. This
document's job is done for this cycle — the open item is whether the next cycle that trips one of
these checks proves they actually work in practice, not just on paper.
