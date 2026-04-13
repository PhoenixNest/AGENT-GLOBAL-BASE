---
name: live-ops-strategy
description: Post-launch content planning, economy design, UA strategy, KPI monitoring, and community management for live game operations. Owns the operational framework for Stage 8 (Soft Launch) and Stage 10 (Live Ops).
---

# Live Ops Strategy

## Role

Live Operations is the revenue engine of any mobile game. This skill covers the strategic framework for post-launch content delivery, virtual economy management, user acquisition optimization, and community engagement — from Soft Launch (Stage 8) through ongoing Live Ops (Stage 10).

## Core Framework: The Three-Dial Economy Model

Every live game economy has three dials that must be monitored and adjusted continuously:

| Dial         | Definition                                      | Key Metrics                                       | Adjustment Frequency                   |
| ------------ | ----------------------------------------------- | ------------------------------------------------- | -------------------------------------- |
| **Sink**     | Where players spend currency (items, upgrades)  | Spend rate, inventory depletion                   | Weekly review, bi-weekly change        |
| **Faucet**   | Where players earn currency (rewards, ads, IAP) | Earn rate, source distribution                    | Weekly review, bi-weekly change        |
| **Velocity** | How fast currency circulates in the economy     | Turnover rate, hoarding index, transaction volume | Real-time monitoring, daily adjustment |

### Instrumentation Requirements

- Real-time economy dashboard updating every 15 minutes during first 4 weeks of any new feature
- Player segmentation by spend tier (whale, dolphin, minnow, F2P) with separate economy tracking per segment
- A/B testing framework for economy changes — no change deployed to 100% of players without validation

## Content Pipeline Management

### Content Cadence

| Content Type        | Frequency     | Lead Time Required | Owner                |
| ------------------- | ------------- | ------------------ | -------------------- |
| Live events         | Bi-weekly     | 4 weeks            | Live Ops Lead        |
| New levels/areas    | Monthly       | 8 weeks            | Level Designer + Art |
| Seasonal content    | Quarterly     | 12 weeks           | Creative Director    |
| Major feature drops | Semi-annually | 16+ weeks          | Studio Director      |

### Content Validation Gate

Before any content ships to live players:

1. Internal playtest by minimum 3 team members outside the content's creation team
2. Economy impact simulation — verify sink/faucet balance remains within ±15% of target
3. Performance profiling — ensure no FPS degradation on lowest-spec target device
4. Localization completeness check — all text extracted and translated for target markets

## KPI Monitoring Framework

### Primary KPIs (daily monitoring)

| KPI           | Target (Casual)  | Alert Threshold | Recovery Action                               |
| ------------- | ---------------- | --------------- | --------------------------------------------- |
| D1 Retention  | ≥ 40%            | < 35%           | Investigate onboarding, review tutorial flow  |
| D7 Retention  | ≥ 18%            | < 14%           | Review mid-game engagement loops              |
| D30 Retention | ≥ 8%             | < 5%            | Evaluate long-term content depth              |
| ARPU          | Market-dependent | > 20% decline   | Review pricing, offers, economy balance       |
| DAU/MAU       | ≥ 25%            | < 20%           | Increase engagement hooks, push notifications |

### Soft Launch KPI Validation (Stage 8)

During soft launch (30–90 days in target region), the following must be validated before global launch commitment:

- D1 retention ≥ 40% in at least 2 of 3 test regions
- D7 retention ≥ 15% in at least 2 of 3 test regions
- Day 7 monetization ≥ $0.50 ARPU in at least 1 test region
- Crash-free sessions ≥ 99.5%
- Average session length ≥ 8 minutes

## UA Strategy Integration

- Coordinate with UA Specialist on creative asset testing — minimum 5 ad creative variants running simultaneously
- Target CPI (Cost Per Install) must align with LTV (Lifetime Value) model: LTV/CPI ratio ≥ 1.5 at Day 30
- Regional UA budgets allocated based on soft launch KPI performance — double down on regions exceeding retention targets
- Organic uplift monitoring: Track ratio of organic-to-paid installs; target ≥ 30% organic by Month 3

## Community Management Principles

- Response SLA: Critical issues (P0/P1 bugs) acknowledged within 2 hours, resolved within 24 hours
- Community feedback loop: Top 5 player-requested features reviewed monthly; at least 1 addressed per quarter
- Transparency: Known issues communicated proactively via in-game mail and social channels within 48 hours of identification
- Sentiment tracking: Weekly social media sentiment analysis; alert on >10% negative sentiment shift

## References

- `studio/casual-games/team/recruitment-plan/recruitment-plan.md` — Master recruitment plan with Live Ops division structure
- `company/pipeline/development/pipeline.md` — Stage 8 (Soft Launch) and Stage 10 (Release Readiness) definitions
- `company/library/topics/testing.md` — Testing standards that apply to live ops regression validation
