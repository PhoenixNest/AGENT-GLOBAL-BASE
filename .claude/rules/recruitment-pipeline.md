---
paths:
  - "**/recruitment/**"
description: Company 9-stage recruitment pipeline rules
---

# Recruitment Pipeline — 9-Stage Process

**Applies To:** All company recruitment activities

---

## Pipeline Overview

| #   | Stage                          | Key Producer | User Approval? |
| --- | ------------------------------ | ------------ | -------------- |
| 1   | Hiring Plan Authorship         | CHRO         | ✅             |
| 2   | Job Description Creation       | CHRO         | ✅             |
| 3   | Candidate Sourcing             | CHRO         | ❌             |
| 4   | Resume Screening               | CHRO         | ❌             |
| 5   | Technical Assessment           | CHRO + Dept  | ❌             |
| 6   | Behavioral Interview           | CHRO + Dept  | ❌             |
| 7   | Final Interview & Vetting      | CHRO + Dept  | ✅             |
| 8   | Offer & Negotiation            | CHRO         | ✅             |
| 9   | Onboarding & Profile Authoring | CHRO         | ✅             |

---

## Cycle Folder Structure

```
company/recruitment/<department>-<fy>-<quarter>/
├── hiring-plan.md
├── job-descriptions/
├── candidates/<candidate-name>/
│   ├── assessment.md
│   ├── interview-notes.md
│   └── vetting-report.md
└── hired/<agent-name>/
    ├── offer-letter.md
    └── profile.md
```

**Naming:** `<department>-<fy>-<quarter>` (e.g., `research-develop-fy2026-q2`)

---

## Recruitment-Specific Rules

- Candidate information is confidential
- Use structured interviews (STAR method)
- Apply consistent evaluation criteria
- Document all hiring decisions
- Total timeline: 8–12 weeks per cycle

---

## Profile Location

Hired agent profile: `company/departments/<dept>/<tier>/<role>/agent/profile.md`

**Templates:** `company/recruitment/template/`
