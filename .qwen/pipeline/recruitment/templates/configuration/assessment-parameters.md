# Assessment Parameters — Quarterly Configuration

> **Owner:** All Chief Officers
> **Frequency:** Once per calendar quarter

---

## Scoring Weights by Role Family

### Engineering

| Component                    | Weight    | Pass          | Auto-Reject                    |
| ---------------------------- | --------- | ------------- | ------------------------------ |
| Coding Challenge             | 30%       | ≥ 80th pctile | < 60th pctile                  |
| System Design                | 25%       | ≥ 4/5         | < 3/5                          |
| Panel Interview              | 25%       | ≥ 80th pctile | < 60th pctile                  |
| Behavioral / Culture Add     | 15%       | ≥ 4/5         | < 3/5                          |
| Engineering Taste (modifier) | ±0.3/−0.5 | N/A           | Mentorship ≤ 2 → No Hire (L3+) |

### Product

| Component                    | Weight | Pass          | Auto-Reject   |
| ---------------------------- | ------ | ------------- | ------------- |
| Product Case Study           | 30%    | ≥ 80th pctile | < 60th pctile |
| Product Sense Interview      | 30%    | ≥ 80th pctile | < 60th pctile |
| Metrics/Analytical Reasoning | 20%    | ≥ 4/5         | < 3/5         |
| Behavioral / Culture Add     | 20%    | ≥ 4/5         | < 3/5         |

### Design

| Component                        | Weight | Pass          | Auto-Reject   |
| -------------------------------- | ------ | ------------- | ------------- |
| Phase 1: Problem Framing         | 7.5%   | ≥ 3.5/5       | < 2.5/5       |
| Phase 2: Exploration + Rationale | 7.5%   | ≥ 3.5/5       | < 2.5/5       |
| Phase 3: Final Deliverable       | 10%    | ≥ 3.5/5       | < 2.5/5       |
| Panel Interview                  | 30%    | ≥ 80th pctile | < 60th pctile |
| Behavioral / Culture Add         | 15%    | ≥ 4/5         | < 3/5         |

### Security

| Component          | Weight | Pass       | Auto-Reject     |
| ------------------ | ------ | ---------- | --------------- |
| OWASP MASVS Exam   | 25%    | ≥ 80%      | < 60%           |
| Threat Modeling    | 25%    | ≥ 3.5/5    | ≤ 2.0/5         |
| Vulnerability ID   | 25%    | ≥ 4 of 6   | ≤ 2 of 6        |
| Incident Response  | 15%    | ≥ 3.5/5    | ≤ 2.0/5         |
| Security-First Bar | 10%    | All 3 pass | Any single fail |

### Translation

| Component                | Pass     | Auto-Reject |
| ------------------------ | -------- | ----------- |
| BLEU/TER                 | ≥ 0.80   | < 0.60      |
| Transcreation Challenge  | ≥ 75/100 | < 60/100    |
| Localization Engineering | ≥ 80%    | < 60%       |

### Data/ML

| Component                  | Weight | Pass          | Auto-Reject   |
| -------------------------- | ------ | ------------- | ------------- |
| Statistical Reasoning Test | 35%    | ≥ 80th pctile | < 60th pctile |
| ML System Design Prompt    | 35%    | ≥ 4/5         | < 3/5         |
| Data Pipeline Challenge    | 30%    | ≥ 4/5         | < 3/5         |

### Business

| Component                     | Weight | Pass          | Auto-Reject   |
| ----------------------------- | ------ | ------------- | ------------- |
| Case Study Analysis           | 35%    | ≥ 80th pctile | < 60th pctile |
| Financial Modeling Test       | 25%    | ≥ 4/5         | < 3/5         |
| Strategic Reasoning Interview | 25%    | ≥ 80th pctile | < 60th pctile |
| Behavioral / Culture Add      | 15%    | ≥ 4/5         | < 3/5         |

## Universal Auto-Reject Triggers

| Trigger                                         | Action                                                  |
| ----------------------------------------------- | ------------------------------------------------------- |
| Red Flag Scan = FAIL                            | Immediate rejection                                     |
| AI-likeness score ≥ 0.72                        | Quarantine; confirmed = disqualification + 12-month ban |
| Plagiarism similarity ≥ 0.85                    | Human review; confirmed = disqualification              |
| Assessment compromise (p < 0.01 vs. known keys) | **R1**: assessment invalidated; all re-assessed         |

---

**Configured By:** All Chief Officers
**Quarter:** [Qn YYYY]
**Audit Hash:** [SHA-256]
