# Formation Meeting — Academic Neural Unit 00 (ANU-00)

**Date:** 2026-07-23
**Convened by:** Dr. Elias Vance, Laboratory Director, Core Component 00
**Purpose:** Spearhead the formation of ANU-00 per CEO directive; determine whether additional
personnel need to be recruited.
**Status:** Internal record — outcome reported to the CEO in `formation-report.md` (this folder).
Unedited below per meeting-minutes convention (a record of what was discussed, not a living
document) — see the reader's note immediately following for a later naming collision this
record's own "Phase 1" / "Phase 2" language runs into.

> **Reader's note (added later, does not alter the record below):** the "Phase 1" / "Phase 2"
> labels in this meeting's discussion (2 roles / 3 roles) were superseded the same day by the
> CEO's full-scale override and never executed under those names. A different, unrelated "Phase
> 1" / "Phase 2" (Founding Cohort / Elite Expansion Cohort, 5 roles each) was used later for the
> recruitment cycle that actually ran — see `formation-report.md` §6–§7 and
> `company/recruitment/academic-neural-unit-00-fy2026-q3/recruitment-plan.md`. Don't read this
> page's phase numbers against those.

---

## 1. Attendees

Convened as an advisory session under Dr. Vance's authority (`crew/director/elias-vance/agent/profile.md`).
Attendees drawn from CC-00 crew members whose expertise bears on standing up an independent
academic research function, per `crew/README.md`'s roster and authority table.

| Name                 | Role (CC-00)                           | Role in this meeting                                                                                   |
| -------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Dr. Elias Vance      | Laboratory Director                    | Chair. Incubation lead for ANU-00; CC-00/LLM systems architecture advisor                              |
| Dr. Amara Nwosu-Chen | Staff Research Scientist               | Advisor — independent research origination; only crew member scoped as a PI, not an execution engineer |
| Dr. Idris Farouk     | Staff Research Engineer, MAE Lead (L4) | Advisor — PhD-level research depth; frontier multi-agent/orchestration perspective                     |
| Dr. Tomasz Wieczorek | Staff Safety & Evaluation Engineer     | Advisor — independent evaluation rigor, research-quality auditing                                      |

Module leads (Zhao, Asante, Almeida) and Research Engineer IIs were not convened — their mandate
is CC-00 production-module ownership, which is out of scope for an organizationally independent
academic entity. Ravi Deshmukh (Infrastructure) was not convened at this stage; infrastructure
needs are deferred until ANU-00 has its own staffed lead (see §4).

**Note on authority:** per `crew/README.md`, no CC-00 crew member — including Dr. Vance — holds
recruitment or personnel-evaluation authority. That authority belongs to the CHRO. This meeting's
output is therefore a **recommendation**, not a hiring decision.

---

## 2. Agenda

1. Confirm the CEO's charter and boundary conditions for ANU-00.
2. Define ANU-00's scope, structure, and relationship to CC-00.
3. Assess whether ANU-00 can be incubated with existing CC-00 personnel alone, or whether
   dedicated recruitment is required.
4. If recruitment is required, define prospective role profiles for CEO/CHRO evaluation.
5. Agree on next steps and the reporting artifact for CEO review.

---

## 3. Discussion

### 3.1 Charter and boundary conditions

The CEO's directive was read into the record verbatim:

- ANU-00 has **no direct organizational link** to `core-component-00/`. CC-00 and Dr. Vance serve
  an **incubation role only** — advisory and methodological support during formation, not
  governance, staffing, or line authority over the new entity.
- ANU-00's charter is academic research into frontier fields (computer science, AI, neural
  networks, software engineering) and construction of a knowledge base from that research — a
  broader and more open-ended mandate than CC-00's applied-engineering-and-production-patterns
  charter.

Consensus: the boundary is a **reporting-line and governance** distinction, not a technical-standard
exemption. Any LLM-powered tooling ANU-00 later builds (e.g. its knowledge base) is still bound by
the workspace-wide ASE framework (root `CLAUDE.md` §9) — that obligation is universal, not
CC-00-specific, and does not create an organizational link back to the lab.

### 3.2 Scope and structure

Agreed scope: ANU-00 conducts primary academic research (not production engineering) in the
CEO-specified frontier fields, and maintains a dated research-archive knowledge base following the
workspace's existing `telescope/`-style convention (`YYYY-MM-DD-<slug>/research-report.md`), so
that its output is navigable the same way as other departments' research archives (see root
`CLAUDE.md` §4, `telescope/README.md`).

Agreed structural principle: ANU-00 must have **its own permanent lead**, distinct from Dr. Vance.
Dr. Vance chairing this formation meeting is a one-time incubation act, not a standing directorship
— consistent with the CEO's "no direct link" clarification and with Dr. Vance's own documented
"Honest Gaps" (`elias-vance/agent/profile.md`: does not own product requirements, does not recruit
personnel, and his authority is scoped to CC-00's five-module stack and ASE, not to unrelated
academic domains).

### 3.3 Recruitment assessment

The group evaluated whether ANU-00 could launch without dedicated headcount (e.g., run as a
part-time extension of CC-00 crew effort). Rejected: this would recreate exactly the situation the
CEO's "no direct link" clarification is meant to avoid — an academic entity that is CC-00 in
substance, run by CC-00 people, regardless of its label. CC-00 crew members are also each scoped to
their own module/cross-cutting mandate (`crew/README.md` §Authority Scope) and have no standing
capacity to originate and staff a second organization's research programme.

**Decision: recruitment is necessary.** ANU-00 cannot be meaningfully formed as an independent
entity without at least a dedicated lead and initial research capacity of its own.

Applying the lab's own precedent for pacing new headcount (`crew/README.md`'s Composition
Assessment: "adding headcount before [a] crew has shipped anything together would be premature
scaling, not rigor") the group agreed on a **phased build-out**, not a full roster in one cycle:

- **Phase 1 (recommended now):** an ANU-00 Lead and one generalist Research Scientist — enough to
  stand up the entity, ratify its own initial research agenda, and establish the knowledge-base
  structure.
- **Phase 2 (flagged, not requested now):** additional domain-specific Research Scientists
  (neural networks / AI, software engineering) and a dedicated knowledge-systems engineer, once
  Phase 1 has a track record to hire against.

Per `crew/README.md`'s Deferral Review convention, deferring the Phase 2 roles to a later cycle is
flagged here explicitly for CEO/CHRO confirmation rather than treated as this group's own final
word — see `formation-report.md` §5.

Full role profiles for Phase 1 (and the flagged Phase 2 roles) are in `prospective-hires.md`.

### 3.4 Next steps

1. Report this outcome to the CEO for evaluation (`formation-report.md`).
2. If the CEO approves Phase 1 recruitment, CHRO opens a hiring cycle under the standard 9-stage
   recruitment pipeline (`company/pipeline/recruitment/pipeline.md`), folder
   `company/recruitment/academic-neural-unit-00-fy2026-q3/` per
   `company/recruitment/CLAUDE.md`'s naming convention.
3. Dr. Vance's incubation involvement ends, or steps back to a purely advisory footing, once an
   ANU-00 Lead is onboarded.

---

## 4. Decisions Recorded

| #   | Decision                                                                                                                                        | Owner of follow-through           |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| 1   | ANU-00 is organizationally independent of CC-00; CC-00's role is incubation-only                                                                | Dr. Vance (during formation)      |
| 2   | ANU-00 requires dedicated recruitment; it cannot launch on CC-00 crew capacity alone                                                            | CEO (approval) → CHRO (execution) |
| 3   | Recruitment is phased: Phase 1 = Lead + 1 Research Scientist now; Phase 2 = 3 further roles, flagged and deferred pending CEO/CHRO confirmation | CEO / CHRO                        |
| 4   | ASE governance applies to any future ANU-00 LLM tooling regardless of organizational independence                                               | ANU-00 Lead (once hired)          |

This meeting's outcome is reported for CEO evaluation in `formation-report.md`.
