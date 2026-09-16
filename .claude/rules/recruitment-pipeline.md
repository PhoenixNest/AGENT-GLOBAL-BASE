---
paths:
  - "**/recruitment/**"
description: Company 9-stage recruitment pipeline rules
---

# Recruitment Pipeline — 9-Stage Process

**Applies To:** All company recruitment activities

---

## Pipeline Overview

Canonical source: `company/pipeline/recruitment/pipeline.md`. Where this summary and that file
disagree, `pipeline.md` governs.

| #   | Stage                                      | Key Producer                                                    | User Approval? |
| --- | ------------------------------------------ | --------------------------------------------------------------- | -------------- |
| 1   | Role Intake → Position Specification       | System (automated)                                              | ❌             |
| 2   | Sourcing → Candidate Pipeline              | System (automated)                                              | ❌             |
| 3   | Automated Screening → Assessment Battery   | System (automated)                                              | ❌             |
| 4   | Interview Simulation → Scored Assessments  | System; L3+ human engineering panel (CTO or Software Architect) | ❌             |
| 5   | Elite Vetting Gate → Pass/Fail Decision    | System (automated)                                              | ❌             |
| 6   | Background Verification → Clearance Status | System (automated)                                              | ❌             |
| 7   | Offer Generation → Package Extended        | System (automated)                                              | ❌             |
| 8   | **Hiring Outcome Report → User Review**    | CHRO → User                                                     | ✅             |
| 9   | Onboarding → 90-Day Checkpoint             | System (automated)                                              | ❌             |

**Stage 8 is the only gate in this pipeline requiring human approval.** Stages 1–7 run without
human involvement. **Stage 9 begins only after user approval at Stage 8** — no onboarding activity,
including profile authorship, occurs before that sign-off.

**L3+ engineering roles** are assessed at Stage 4 by a human engineering panel conducted by the CTO
or the Software Architect. The hiring manager may sit in as a second voice, never as the only
technical interviewer.

---

## Cycle Folder Structure

```
company/recruitment/<department>-<fy>-<quarter>/
├── recruitment-plan.md          ← the cycle's plan; versioned in its own history table
├── candidates/                  ← one flat file per candidate, hired and rejected alike
│   └── NN-<lastname>-<firstname>.md
├── phase-summaries/             ← one per hiring phase, filed at phase close
│   └── phase-N-summary.md
└── hiring-outcome-report.md     ← Stage 8 deliverable for user review
```

A cycle may add further records where the round produced them — a secondary review such as
`cto-interview-review.md`, or a `reflection.md`. Candidate numbering is continuous across the whole
cycle, not restarted per phase or per role.

Hired-agent profiles are **not** written into the cycle folder — see Profile Location below.

**Naming:** `<department>-<fy>-<quarter>` (e.g., `research-develop-fy2026-q2`). An entity that is
not a Company department uses its own name in the same shape (e.g.,
`behavior-control-unit-00-fy2026-q3`).

---

## Recruitment-Specific Rules

- Candidate information is confidential
- Use structured interviews (STAR method)
- Apply consistent evaluation criteria
- Document all hiring decisions
- Total timeline: 8–12 weeks per cycle

---

## Profile Location

A hired agent's profile is written at Stage 9, after Stage 8 sign-off, into the folder of the
organisation that hired them — never into the recruitment cycle folder. Three shapes are in use:

| Hired into                                        | Path                                                                                                                   |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| A Company department — C-suite or department head | `company/departments/<dept>/supervisor/<role>/agent/profile.md`                                                        |
| A Company department — team member                | `company/departments/<dept>/team/<tier>/<role>/<name>/agent/profile.md` where `<tier>` is `supervisors` or `teammates` |
| An independent entity (CC-00, ANU-00, BCU-00)     | `<entity>/crew/<function>/<first-last>/agent/profile.md`                                                               |

Skill files sit alongside the profile as `skills/<skill-name>.md`, adjacent to the `agent/` folder.

**Templates:** `company/recruitment/template/` — `recruitment-plan.md`, `candidate-evaluation.md`,
`phase-summary.md`.
