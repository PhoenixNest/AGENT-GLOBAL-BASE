---
candidate_name: "Data Analyst"
candidate_id: "G33"
entity_type: "studio"
stage: "stage-4"
division: "live-ops"
role: "data-analyst"
document_type: "Interview Scores"
---

# Stage 4: Interview Simulation & Scored Assessments — Data Analyst (G33)

**Assessment Period:** 2026-04-12 to 2026-04-16
**Candidates Assessed:** 22

---

## Assessment Results — Top Candidate: Yuki Tanaka

### Data Analysis Case Study (48-hour async) — Score: 4.8/5

**Prompt:** Analyze soft-launch player data for a casual match-3 game. Build a cohort decay model, forecast LTV at 90 days, and design an A/B test for a new monetization feature.

**Deliverable Summary:**

- Cohort decay model using Weibull distribution fit to D1–D30 retention data; identified 3 player segments (casual, engaged, whale) with distinct decay curves
- LTV forecast model: hybrid parametric + ML approach achieving 94% accuracy when backtested against historical data; projected D90 LTV of $4.20 per acquired user
- A/B test design for new "bonus pack" IAP offer: power analysis (n=50K per variant), stratified randomization by player segment, 14-day test duration, guardrail metrics defined
- Python code repository with full analysis (pandas, scikit-learn, matplotlib), SQL queries for data extraction, and Tableau dashboard mockup

**Strengths:** Exceptional statistical rigor; production-quality code; clear visualization; actionable recommendations tied to business outcomes.

### Statistical Reasoning Test (90-min timed) — Score: 4.6/5

- Correctly solved 9 of 10 statistical problems (hypothesis testing, Bayesian inference, regression diagnostics, power analysis)
- Identified a Simpson's paradox in the provided dataset that would have led to incorrect business decisions
- Missed one subtle multiple comparison correction issue

### SQL/Python Coding Challenge (90-min sandboxed) — Score: 4.7/5

- SQL: Complex window functions, CTEs, and self-joins executed correctly; optimized query reduced runtime from 45s to 3s
- Python: Clean, well-documented code with proper error handling; used vectorized operations instead of loops
- Produced a cohort retention heatmap and LTV forecast curve as deliverables

### Simulated Panel Interview (45 min) — Score: 4.5/5

| Dimension         | Score | Notes                                                     |
| ----------------- | ----- | --------------------------------------------------------- |
| Impact at Scale   | 5/5   | LTV model used for $2M+ budget allocation at Zynga        |
| Craft Depth       | 5/5   | Deep stats + ML; cohort modeling expertise                |
| Leadership Signal | 3/5   | Mentored 1 junior analyst; no formal leadership           |
| Standards Signal  | 4/5   | Established data quality checks adopted by analytics team |
| Red Flag Scan     | PASS  | Zero flags                                                |

#### Behavioral / Culture Add — Score: 4.1/5

#### Composite Score: 4.620/5 (97th percentile) — **ADVANCE** ✅

---

## Auto-Reject at Stage 4

| Count | Avg Composite | Rejection Reason                      |
| ----- | ------------- | ------------------------------------- |
| 7     | 2.1–3.3       | Composite Score below 80th percentile |

**Pipeline Status:** 15 candidates advance to Stage 5.
