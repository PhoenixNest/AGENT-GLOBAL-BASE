# Competency Bars — Quarterly Configuration

> **Owner:** All Chief Officers
> **Frequency:** Once per calendar quarter
> **Purpose:** Per-role-family minimum thresholds for each assessment dimension

---

## Universal Elite Bar (All Role Families)

| Dimension         | Threshold                   | Auto-Reject If            |
| ----------------- | --------------------------- | ------------------------- |
| Impact at Scale   | ≥ 4 on 20-pt scale          | < 4 on 3+ dimensions      |
| Craft Depth       | ≥ 4                         | < 4                       |
| Leadership Signal | ≥ 4 (supervisor) / ≥ 3 (IC) | Below tier threshold      |
| Standards Signal  | ≥ 4                         | < 4                       |
| Red Flag Scan     | PASS (zero flags)           | Any single flag triggered |

## Role-Family Competency Thresholds

| Role Family | Percentile Required | Auto-Reject If |
| ----------- | ------------------- | -------------- |
| Engineering | ≥ 80th              | < 60th         |
| Product     | ≥ 80th              | < 60th         |
| Design      | ≥ 80th              | < 60th         |
| Security    | ≥ 85th              | < 60th         |
| Translation | ≥ 80th              | < 60th         |
| Data/ML     | ≥ 80th              | < 60th         |
| Business    | ≥ 80th              | < 60th         |

## Tiered Engineering Assessment Thresholds

| Tier           | Model                          | Pass Threshold               | Auto-Reject If                |
| -------------- | ------------------------------ | ---------------------------- | ----------------------------- |
| L0–L1 (Junior) | Fully automated                | ≥ 80th percentile            | < 60th percentile             |
| L2 (Mid)       | Automated filter + code review | ≥ 80th + code review ≥ 3.5/5 | < 60th OR code review ≤ 2.0/5 |
| L3+ (Senior)   | Automated filter + human panel | ≥ 80th + human panel pass    | < 60th OR human panel fail    |

## Platform-Specific Competency Minimums

| Competency                       | Applies To         | L1 Min | L2 Min | L3+ Min | Auto-Reject |
| -------------------------------- | ------------------ | ------ | ------ | ------- | ----------- |
| iOS HIG Fluency                  | iOS roles          | 3      | 3.5    | 4       | ≤ 2         |
| Android Material & Fragmentation | Android roles      | 3      | 3.5    | 4       | ≤ 2         |
| Paywall Experimentation Rigor    | Monetization roles | 3      | 3.5    | 4       | ≤ 2         |
| App Store / Play Store Dynamics  | Production roles   | 3      | 3.5    | 4       | ≤ 2         |
| Device Fragmentation Trade-Offs  | Cross-platform     | 3      | 3.5    | 4       | ≤ 2         |
| OWASP MASVS Competency           | Security roles     | 80%    | 80%    | 85%     | < 60%       |
| Threat Modeling Proficiency      | Security roles     | 3.5/5  | 3.5/5  | 4/5     | ≤ 2.0/5     |
| Vulnerability Identification     | Security roles     | 4 of 6 | 4 of 6 | 5 of 6  | ≤ 2 of 6    |
| Incident Response                | Security roles     | 3.5/5  | 3.5/5  | 4/5     | ≤ 2.0/5     |

---

**Configured By:** [Chief Officer names]
**Quarter:** [Qn YYYY]
**Effective:** [Start date of next quarter]
**Audit Hash:** [SHA-256]
