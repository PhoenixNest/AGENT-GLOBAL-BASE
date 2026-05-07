---
inclusion: fileMatch
fileMatchPattern: "**/recruitment/**"
---

# Recruitment Pipeline — 9-Stage Process

**Authority:** AGENTS.md § 4.6 + `company/pipeline/recruitment/pipeline.md`  
**Applies To:** All company recruitment activities

---

## Recruitment Pipeline Overview

The recruitment pipeline is a **standalone 9-stage process** (Stages 1-9) that does NOT follow the base+delta pattern used by development pipelines.

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

## Recruitment Cycle Conventions

### Cycle Folder Structure

```
company/recruitment/<department>-<fy>-<quarter>/
├── hiring-plan.md
├── job-descriptions/
├── candidates/
│   ├── <candidate-name>/
│   │   ├── resume.pdf
│   │   ├── assessment.md
│   │   ├── interview-notes.md
│   │   └── vetting-report.md
└── hired/
    └── <agent-name>/
        ├── offer-letter.md
        └── profile.md
```

### Naming Convention

- **Format:** `<department>-<fy>-<quarter>`
- **Example:** `research-develop-fy2026-q2`
- **FY:** Fiscal year (e.g., `fy2026`)
- **Quarter:** `q1`, `q2`, `q3`, `q4`

## Stage-Specific Requirements

### Stage 1: Hiring Plan Authorship

**Deliverable:** `hiring-plan.md`

**Required Sections:**

- Department and team context
- Roles to be filled (title, seniority, count)
- Hiring rationale and business justification
- Timeline and urgency
- Budget allocation
- Success criteria

**User Approval Required:** ✅

### Stage 2: Job Description Creation

**Deliverable:** `job-descriptions/<role>.md`

**Required Sections:**

- Role title and seniority level
- Department and reporting structure
- Responsibilities and key deliverables
- Required qualifications (education, experience, skills)
- Preferred qualifications
- Compensation range
- Benefits and perks

**User Approval Required:** ✅

### Stage 3: Candidate Sourcing

**Activities:**

- Post job descriptions to job boards
- Reach out to professional networks
- Engage with recruitment agencies
- Source from internal referrals
- Build candidate pipeline

**Deliverable:** Candidate pool (minimum 10 candidates per role)

### Stage 4: Resume Screening

**Activities:**

- Review resumes against job requirements
- Assess qualifications and experience
- Identify top candidates (top 30%)
- Document screening decisions

**Deliverable:** Shortlist of candidates for assessment

### Stage 5: Technical Assessment

**Activities:**

- Conduct role-specific technical assessment
- Evaluate technical skills and knowledge
- Assess problem-solving abilities
- Document assessment results

**Assessment Types by Role:**

- **Engineering:** Coding challenge, system design
- **Design:** Portfolio review, design challenge
- **Product:** Case study, product sense questions
- **Data:** SQL/Python assessment, analytics case study
- **Translation:** Translation sample, linguistic assessment

**Deliverable:** `candidates/<name>/assessment.md`

### Stage 6: Behavioral Interview

**Activities:**

- Conduct behavioral interview
- Assess cultural fit and values alignment
- Evaluate communication skills
- Assess collaboration and teamwork
- Document interview notes

**Interview Framework:**

- STAR method (Situation, Task, Action, Result)
- Company values alignment
- Team collaboration scenarios
- Conflict resolution examples

**Deliverable:** `candidates/<name>/interview-notes.md`

### Stage 7: Final Interview & Vetting

**Activities:**

- Conduct final interview with department leadership
- Comprehensive candidate vetting
- Reference checks
- Background verification
- Final hiring decision

**Vetting Criteria:**

- Technical competency (from Stage 5)
- Behavioral fit (from Stage 6)
- Reference feedback
- Background check results
- Salary expectations alignment

**Deliverable:** `candidates/<name>/vetting-report.md`

**User Approval Required:** ✅

### Stage 8: Offer & Negotiation

**Activities:**

- Prepare offer letter
- Present offer to candidate
- Negotiate terms (salary, benefits, start date)
- Finalize offer acceptance
- Document offer details

**Deliverable:** `hired/<agent-name>/offer-letter.md`

**User Approval Required:** ✅

### Stage 9: Onboarding & Profile Authoring

**Activities:**

- Create agent profile document
- Assign agent ID
- Define role and responsibilities
- Document skills and expertise
- Set up workspace access
- Complete onboarding checklist

**Deliverable:** `hired/<agent-name>/profile.md`

**Profile Location:** `company/departments/<dept>/<tier>/<role>/agent/profile.md`

**User Approval Required:** ✅

## Recruitment-Specific Rules

### 1. Candidate Privacy

- Candidate information is confidential
- Resume and assessment data must be secured
- Interview notes are for internal use only
- Comply with data protection regulations

### 2. Bias Mitigation

- Use structured interviews
- Apply consistent evaluation criteria
- Document all hiring decisions
- Ensure diverse candidate pools

### 3. Timeline Expectations

- **Stage 1-2:** 1-2 weeks
- **Stage 3-4:** 2-3 weeks
- **Stage 5-6:** 1-2 weeks per candidate
- **Stage 7:** 1 week
- **Stage 8:** 1-2 weeks
- **Stage 9:** 1 week

**Total:** 8-12 weeks per hiring cycle

### 4. Candidate Experience

- Provide timely feedback
- Maintain professional communication
- Respect candidate time
- Offer constructive feedback to rejected candidates

## Role-Specific Vetting Skills

The CHRO has specialized vetting skills for different role categories:

- `recruit-business.md` — Business roles (Product, Strategy)
- `recruit-data.md` — Data roles (Analytics, Data Science)
- `recruit-design.md` — Design roles (UI/UX, Visual Design)
- `recruit-engineering.md` — Engineering roles (Mobile, Backend, Frontend)
- `recruit-product.md` — Product roles (PM, PO)
- `recruit-translation.md` — Translation roles (Linguists, i18n Engineers)

## Templates

All recruitment templates are located at:

```
company/recruitment/template/
├── hiring-plan-template.md
├── job-description-template.md
├── assessment-template.md
├── interview-notes-template.md
├── vetting-report-template.md
└── offer-letter-template.md
```

## Related Steering Files

- `recruitment.md` — Recruitment domain skill (manual)
- `company-pipeline-overview.md` — Company pipeline overview (for context)

## Related Skills

- `.kiro/skills/recruitment/` — Recruitment domain skills
  - `vet-candidate.md`
  - `placement-and-profile-authoring.md`
  - `recruit-business.md`
  - `recruit-data.md`
  - `recruit-design.md`
  - `recruit-engineering.md`
  - `recruit-product.md`
  - `recruit-translation.md`
