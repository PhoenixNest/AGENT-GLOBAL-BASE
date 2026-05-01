# Market Tier Criteria — Soft Launch Evaluation

> **Stage:** 8 — Soft Launch
> **Referenced by:** `SOFT-LAUNCH-REPORT.md` §5, `casual-games-pipeline.md` §Kill Gate 5

This document defines the numeric thresholds for each market tier, used at Kill Gate 5 to determine the global launch strategy.

---

## Tier Definitions

### Tier A — Global Priority Launch

All of the following must be met or exceeded:

| Metric              | Threshold |
| :------------------ | :-------: |
| D1 Retention        |  ≥ [40]%  |
| D7 Retention        |  ≥ [20]%  |
| D30 Retention       |  ≥ [10]%  |
| ARPDAU              | ≥ $[0.10] |
| LTV:CAC             |  ≥ [3.0]  |
| Crash-free sessions |  ≥ 99.5%  |

**Strategic response:** Aggressive global launch with full UA spend. Priority markets activated immediately. Live ops team on standby.

---

### Tier B — Standard Global Launch

All core thresholds met (see below), with no Tier A exceedance required:

| Metric              | Threshold |
| :------------------ | :-------: |
| D1 Retention        |  ≥ [30]%  |
| D7 Retention        |  ≥ [15]%  |
| D30 Retention       |  ≥ [7]%   |
| ARPDAU              | ≥ $[0.06] |
| LTV:CAC             |  ≥ [2.0]  |
| Crash-free sessions |  ≥ 99.0%  |

**Strategic response:** Global launch with standard UA spend. Monitor weekly against QBR thresholds. First QBR at 90 days.

---

### Tier C — Targeted Release / Extended Soft Launch

At least 3 of 6 core metrics meet Tier B threshold:

| Scenario                       | Recommended Action                                                 |
| :----------------------------- | :----------------------------------------------------------------- |
| D1/D7 strong; D30/revenue weak | 60-day extension; run A/B test on retention mechanics              |
| Revenue strong; retention weak | Feature update addressing top drop-off point; 30-day re-evaluation |
| All metrics borderline         | Targeted release to 2–3 markets only; build organic evidence       |

**Note:** Extended soft launch carries a $[X,XXX] weekly burn. Studio Director must notify User at the 60-day mark with a go/kill recommendation.

---

### Kill — Project Termination

Any of the following conditions triggers a Kill recommendation:

| Trigger                             |                       Threshold                        |
| :---------------------------------- | :----------------------------------------------------: |
| D1 Retention                        |                < [20]% after iteration                 |
| D7 Retention                        |                 < [8]% after iteration                 |
| LTV:CAC                             | < [1.0] (spending more to acquire than lifetime value) |
| Crash-free sessions                 |         < 98% (unresolvable technical issues)          |
| Budget consumed (soft launch phase) |         > $[X,XXX,XXX] without Tier C metrics          |

**Kill protocol:** Per `kill-gate-report.md` — asset preservation, team reassignment, post-mortem within 5 business days.

---

## Threshold Calibration Notes

These thresholds are the studio's **current defaults**. They must be recalibrated after each completed project based on:

1. Actual market performance vs projected performance
2. Genre-specific industry benchmarks (casual games averages: D1 ~40%, D7 ~20%, D30 ~10%)
3. Studio Director + CPO review at each QBR retrospective

> **Calibration history is recorded in** `studio/casual-games/library/retrospectives/`

---

## Tier Assessment Worksheet

| Metric        | Actual | Tier A threshold | Tier B threshold | Tier (A/B/C/Kill) |
| :------------ | :----: | :--------------: | :--------------: | :---------------: |
| D1 Retention  |        |     ≥ [40]%      |     ≥ [30]%      |                   |
| D7 Retention  |        |     ≥ [20]%      |     ≥ [15]%      |                   |
| D30 Retention |        |     ≥ [10]%      |      ≥ [7]%      |                   |
| ARPDAU        |        |    ≥ $[0.10]     |    ≥ $[0.06]     |                   |
| LTV:CAC       |        |     ≥ [3.0]      |     ≥ [2.0]      |                   |
| Crash-free    |        |     ≥ 99.5%      |     ≥ 99.0%      |                   |

**Overall tier:** [ ] A / [ ] B / [ ] C / [ ] Kill
**Rationale:** [2–3 sentences]
