# company/recruitment/ — Hiring Cycles & Templates

Active hiring records and reusable templates for The Company's 9-stage recruitment pipeline.
Owned by CHRO — Dr. Evelyn Hartwell and the Human Resources department.

---

## What Lives Here

```
recruitment/
├── template/                          ← Reusable templates for all recruitment artifacts
└── <department>-<fy>-<quarter>/       ← One folder per active/completed hiring cycle
```

---

## Folder Naming Convention

Hiring cycle folders follow this format:

```
<department>-<fiscal-year>-<quarter>/
```

Examples:

```
research-develop-fy2026-q2/
brand-design-fy2026-q3/
```

---

## Recruitment Pipeline

The recruitment process is a **standalone 9-stage pipeline** — it does not use the `_base/` pattern
shared by the four development pipelines. Its canonical specification lives at:

```
company/pipeline/recruitment/pipeline.md
```

**Always read this `pipeline.md` before producing any recruitment artifact.**

| Stage | Name                            |
| ----- | ------------------------------- |
| 1     | Job Requisition                 |
| 2     | Role Definition & JD Authorship |
| 3     | Sourcing Strategy               |
| 4     | Candidate Sourcing              |
| 5     | Application Review & Screening  |
| 6     | Interviews                      |
| 7     | Assessment & Vetting            |
| 8     | Offer & Negotiation             |
| 9     | Onboarding                      |

---

## Templates

Reusable recruitment templates are in `template/`. Use these when creating new cycle folders or
producing stage artifacts. Do not create bespoke document formats — use the templates.

---

## Ownership

| Role                       | Responsibility                                          |
| -------------------------- | ------------------------------------------------------- |
| CHRO — Dr. Evelyn Hartwell | Recruitment pipeline governance, final hiring authority |
| HR Department              | Cycle execution, candidate management, vetting          |

---

## Rules

- Hiring cycle folders are named `<department>-<fy>-<quarter>/` — follow this exactly.
- Use templates from `template/` for all recruitment artifacts.
- Do not conflate the 9-stage recruitment pipeline with the 13-stage development pipelines — they
  are entirely separate processes.
- Vetting rules are defined in `company/pipeline/recruitment/pipeline.md` — follow them exactly;
  do not invent alternative vetting criteria.
