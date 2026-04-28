---
name: hr-recruiting-guidelines-recruit-data
description: "Recruits data science, ML, and analytics roles — Data Analyst, Data Scientist, ML Engineer, Staff Data Scientist, ML Research Scientist, Head of Data, VP Data, CDAO — using seniority rubrics calibrated to production ML systems, novel research, and data org leadership, with interview simulation protocols and elite vetting. Owned by Dr. Evelyn Hartwell (CHRO). Use when recruiting for data science, machine learning, analytics, MLOps, or AI research roles. Trigger: recruit data, hire data scientist, hire ML engineer, recruit analytics, data recruitment, ML recruitment, CDAO, head of data."
prerequisites:
  - hr-recruiting-overview

version: "1.0.0"
---

# Data & ML Recruitment Skill

## Roles Covered

Data Analyst, Data Scientist, ML Engineer, Staff Data Scientist, ML Research Scientist,
Head of Data, VP Data, Chief Data & AI Officer (CDAO).

## Seniority Rubric

| Criterion       | Analyst                | Data Scientist                  | Senior DS                           | Staff DS                      | ML Engineer                   | ML Research Scientist                                  | Head of Data                | VP Data                      | CDAO                        |
| --------------- | ---------------------- | ------------------------------- | ----------------------------------- | ----------------------------- | ----------------------------- | ------------------------------------------------------ | --------------------------- | ---------------------------- | --------------------------- |
| Scope           | Reporting & dashboards | Predictive modeling             | Cross-team DS projects              | Org-wide data strategy        | Production ML systems         | Cross-org ML research                                  | Data org + strategy         | Business unit data           | Company data vision         |
| Technical depth | SQL + BI tools         | Python/R, statistics, ML basics | Advanced ML, experimentation design | ML platform, infrastructure   | MLOps, model serving at scale | Novel ML research, publication-grade work              | Data architecture           | Data strategy                | AI/data governance          |
| Research depth  | None required          | Applied research                | Novel approaches within domain      | Published or patented methods | Production-scale ML research  | Original research, published or patent-pending methods | N/A                         | N/A                          | Industry thought leadership |
| Influence       | Analytics team         | Cross-functional                | Business decisions                  | Org metric culture            | Engineering + science         | Engineering + science + exec                           | Exec data decisions         | Board-level                  | Regulatory + market         |
| Track record    | Dashboards used daily  | Model in production             | Multiple models driving revenue     | Org-wide ML platform          | High-traffic inference system | Published models or papers with production adoption    | Data org built from scratch | Company revenue through data | Industry AI leadership      |

## Interview Simulation Protocol

1. **Identity block** — name, title, company, YOE, education (PhD/MS/BS relevant at senior levels)

2. **Data/ML track record** (3 bullets)
   - Format: "[Built / deployed / designed] [model/system/framework] at [company], achieving [quantified outcome]"
   - Example: "Deployed a real-time fraud detection model at PayPal serving 400K transactions/minute, reducing chargebacks by $18M annually with < 0.3% false positive rate"
   - Note: three achievement bullets are required in the candidate profile — one per major model, system, or research contribution

3. **Technical strengths** (2–3 with concrete examples)
   - Must reference specific algorithms, frameworks, architectures, or data systems — not generic "machine learning"

4. **Honest gaps** (1–2)
   - Example: "Deep expertise in NLP and recommender systems; limited production experience with computer vision or robotics"

5. **Seniority score** — apply rubric, assign level

6. **Vetting result** — apply `vet-candidate.md`, paste full scoring output

7. **Placement recommendation** — tier, directory name, rationale

## Output Contract

After user confirms placement:

1. Create `team/[tier]/[role-name]/agent/profile.md`
   (where `[tier]` is `supervisors` for C-suite/VP/Director/Principal or `teammates` for Staff/Senior IC and below)
2. Create at least one `team/[tier]/[role-name]/skills/[skill-name].md` (e.g., `ml-modeling.md`, `data-strategy.md`, `experimentation-design.md`)
3. Confirm: "Recruited and placed: [Name], [Title] → team/[tier]/[role-name]/"
