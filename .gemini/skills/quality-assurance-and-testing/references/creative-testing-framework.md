---
name: creative-testing-framework
description: Systematic creative testing methodology for UA campaigns, including test design, kill/scale decisions, and performance tracking.
version: "1.0.0"
---

# Creative Testing Framework

## Overview

This skill defines the systematic approach to creative testing for UA campaigns. The framework ensures that every creative asset is tested, measured, and optimized against clear performance criteria.

## Testing Architecture

### Test Design

| Component            | Standard                                                  |
| -------------------- | --------------------------------------------------------- |
| Concurrent tests     | 50+ active creative tests                                 |
| Test duration        | Minimum 7 days (statistical significance)                 |
| Variants per concept | 3 (hook variation, CTA variation, format variation)       |
| Kill threshold       | CPI > 130% of target for 3+ days                          |
| Scale threshold      | CPI < 80% of target for 3+ days + D1 retention ≥ baseline |

### Kill/Scale Decision Matrix

| CPI vs. Target | D1 Retention | Action                                  |
| -------------- | ------------ | --------------------------------------- |
| < 80%          | ≥ Baseline   | **SCALE** (increase budget 2×)          |
| < 80%          | < Baseline   | **HOLD** (monitor, investigate quality) |
| 80–130%        | Any          | **HOLD** (maintain, gather data)        |
| > 130%         | Any          | **KILL** (pause, analyze learnings)     |

## Creative Production Pipeline

```
Concept Ideation → Script/Storyboard → Production (internal/agency) → QA → Launch → Measure → Iterate
```

| Phase               | Duration | Owner                         |
| ------------------- | -------- | ----------------------------- |
| Concept ideation    | 2 days   | UA Specialist + Creative      |
| Production          | 3–5 days | Creative team / Agency        |
| QA & compliance     | 1 day    | UA Specialist                 |
| Launch              | Day 1    | UA Specialist                 |
| Initial measure     | Days 1–3 | UA Specialist                 |
| Kill/Scale decision | Day 7    | UA Specialist + Live Ops Lead |

## Performance Dashboard Metrics

| Metric           | Frequency | Alert Threshold          |
| ---------------- | --------- | ------------------------ |
| CPI              | Daily     | > 130% of target         |
| D1 Retention     | Weekly    | < 90% of baseline        |
| ROAS (D7)        | Weekly    | < 25%                    |
| Creative fatigue | Weekly    | CTR decline > 30% WoW    |
| Frequency cap    | Daily     | > 3 impressions/user/day |
