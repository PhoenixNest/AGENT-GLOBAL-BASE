---
name: live-ops-strategy
description: End-to-end live operations strategy including content roadmap design, seasonal event architecture, KPI management, and A/B testing for F2P mobile games.
version: "1.0.0"
---

# Live Ops Strategy

## Overview

This skill covers the design, execution, and optimization of post-launch content strategy for F2P mobile games. It encompasses content roadmap planning, seasonal event architecture, KPI target setting, and A/B testing frameworks.

## Tools & Frameworks

| Tool/Framework          | Purpose                                       | Proficiency Level |
| ----------------------- | --------------------------------------------- | ----------------- |
| Event Impact Matrix     | Prioritize seasonal content by KPI impact     | Expert            |
| Amplitude / Firebase    | Player behavior analytics, funnel analysis    | Expert            |
| Optimizely / Split.io   | A/B test design and statistical analysis      | Expert            |
| Tableau / Looker        | KPI dashboard creation and monitoring         | Advanced          |
| Jira / Confluence       | Content pipeline management and documentation | Advanced          |
| Discord / Sprout Social | Community engagement and sentiment tracking   | Advanced          |

## Core Methodologies

### 1. 3-Tier Event Architecture

| Tier             | Frequency | Duration   | Primary KPI      | Design Focus                                 |
| ---------------- | --------- | ---------- | ---------------- | -------------------------------------------- |
| Weekly Challenge | 7 days    | 5–7 days   | D7 retention     | Low-friction engagement, repeatable          |
| Monthly Event    | 30 days   | 10–14 days | ARPU, conversion | Themed content, premium rewards              |
| Quarterly Mega   | 90 days   | 21–30 days | Re-engagement    | Major content drops, lapsed player targeting |

### 2. A/B Testing Framework

- **Experimental Design:** Power analysis (α = 0.05, β = 0.20) before test launch
- **Concurrent Tests:** Maximum 4 simultaneous experiments to avoid interaction effects
- **Statistical Rigor:** Minimum 14-day test duration; sequential analysis only with alpha spending functions
- **Decision Criteria:** Pre-defined success metrics; no p-hacking or early stopping without correction

### 3. KPI Target Setting

| KPI             | Baseline | Target (90 days) | Measurement Method          |
| --------------- | -------- | ---------------- | --------------------------- |
| D1 Retention    | 42%      | 45%              | Cohort analysis (Firebase)  |
| D7 Retention    | 18%      | 22%              | Cohort analysis (Amplitude) |
| D30 Retention   | 8%       | 11%              | Cohort analysis (Amplitude) |
| ARPU            | $0.18    | $0.23            | Revenue / DAU (daily)       |
| Conversion Rate | 3.2%     | 4.0%             | Payers / DAU (daily)        |

## Scenario: Seasonal Event Launch

**Situation:** Launch a "Summer Festival" seasonal event for a match-3 game with 5M DAU.

**Approach:**

1. **Pre-Event (T-30 days):** Define KPI targets, design reward structure, set up A/B test (event duration: 7 vs 10 days), prepare community teaser campaign
2. **Launch (T-0):** Deploy event content, activate push notifications, begin community engagement push
3. **Mid-Event (T+5 days):** Review real-time KPIs, adjust difficulty if engagement drops below threshold, run mid-event community AMA
4. **Post-Event (T+14 days):** Conduct 48-hour post-mortem using Event Impact Scorecard, compare pre/post KPIs, document lessons learned

**Trade-offs:**

- Longer events increase total engagement but risk player fatigue
- Higher reward tiers boost short-term monetization but may devalue currency long-term
- Aggressive push notifications increase DAU but risk opt-out rates

## Quality Standards

- All events must have pre-defined KPI targets before launch
- Post-mortem completed within 48 hours of event conclusion
- A/B test results documented and shared with full team
- Community sentiment monitored daily during active events
- Economy impact modeled before event launch (currency sink/source analysis)

## Industry References

- Playrix Live Ops Playbook (internal framework)
- GDC 2024: "Designing Seasonal Events That Drive Retention" (Nkemelu)
- Gamasutra: "The Event Impact Matrix: A Data-Driven Approach to Content Prioritization"
- Deconstructor of Fun: "Match-3 Live Ops Deep Dive" (industry analysis)
- Supercell Framework: "Player-Centric Event Design" (public talks)
