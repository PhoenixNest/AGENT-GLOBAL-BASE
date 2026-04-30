---
name: economy-design
description: F2P economy design, virtual currency balancing, pricing models, and data-driven economy iteration for mobile games.
version: "1.0.0"
---

# Economy Design

## Overview

This skill covers the design, balancing, and continuous optimization of virtual economies in F2P mobile games, including currency modeling, pricing strategy, and data-driven iteration.

## Core Methodologies

### 1. Currency Architecture

| Currency Type  | Acquisition                  | Consumption               | Design Goal                   |
| -------------- | ---------------------------- | ------------------------- | ----------------------------- |
| Soft Currency  | Level rewards, daily bonuses | Upgrades, boosts          | Engagement loop driver        |
| Hard Currency  | IAP, achievements, events    | Premium items, time skips | Revenue driver                |
| Energy         | Time regen, IAP, friends     | Level attempts            | Session pacing                |
| Event Currency | Event-specific activities    | Event rewards             | Limited-time engagement spike |

### 2. Economy Balancing Process

1. **Design Phase:** Define currency sources and sinks, model expected player accumulation rate
2. **Simulation Phase:** Run Monte Carlo simulation of player behavior (10K+ virtual players)
3. **Playtest Phase:** Internal testing with calibrated difficulty and reward values
4. **Soft Launch Phase:** Real player data analysis, cohort-level economy health monitoring
5. **Live Phase:** Continuous monitoring and adjustment based on real economy data

### 3. Economy Health Metrics

| Metric                  | Target Range          | Alert Threshold      |
| ----------------------- | --------------------- | -------------------- |
| Currency inflation rate | < 5% monthly          | > 10% monthly        |
| Sink/source ratio       | 0.9–1.1 (balanced)    | < 0.8 or > 1.2       |
| IAP conversion rate     | 3–5%                  | < 2% or > 8%         |
| ARPPU                   | $10–$30/month         | < $5 or > $50        |
| Paywall detection       | 0% progression blocks | Any block identified |

## Stage 8 — Soft Launch Economy Validation

At Stage 8 (Soft Launch), Kwame monitors the economy in real markets with real players. The soft launch economy assessment is completed within 14 days of soft launch:

### What to Measure and How to Respond

| Signal                          | Good                                     | Investigate        | Act Immediately                                                 |
| ------------------------------- | ---------------------------------------- | ------------------ | --------------------------------------------------------------- |
| D7 coin balance (median player) | Within ±15% of simulation                | ±15–30% deviation  | >30% deviation — rebalance sources/sinks this sprint            |
| IAP conversion D7               | 2–4%                                     | <1.5% or >5%       | <1% — audit starter pack value and first-session experience     |
| Progression block rate          | <5% of players stuck on any single level | 5–10% stuck        | >10% stuck — Kwame files P1 with level design team to rebalance |
| Economy inflation sign          | Sink/source ratio 0.9–1.1                | 0.8–0.9 or 1.1–1.2 | Outside 0.8/1.2 — Kwame proposes tuning change within 48h       |

### Soft Launch Economy Report

Kwame produces a **Soft Launch Economy Report** at Day 7 and Day 14. Structure:

```markdown
# Soft Launch Economy Report — Day [7 / 14]

**Game:** [Name] **Build:** [Version] **Date:** [YYYY-MM-DD]
**Prepared by:** Kwame Asante, Economy Designer

## Key Metrics vs. Projection

| Metric                   | Projected | Actual | Variance | Assessment                    |
| ------------------------ | --------- | ------ | -------- | ----------------------------- |
| D7 coin balance (median) | 2,400     | 2,100  | -12.5%   | Within range                  |
| IAP conversion rate      | 3.2%      | 2.1%   | -34%     | Below threshold — investigate |
| Sink/source ratio        | 1.0       | 1.18   | +18%     | Warning — soft inflation      |

## Root Cause Analysis (for any metric outside range)

[Specific diagnosis — not "players are spending less," but "the Level 12–15 difficulty spike is preventing progression, reducing the incentive to earn/spend"]

## Recommended Actions

1. [Specific tuning action — what to change, by how much, expected impact]
2. [Second action]

## Risks if Not Addressed

[What will happen to D30 retention/revenue if actions are not taken]
```

## Stage 10 — Live Ops Economy Management

During Stage 10 (Live Ops), Kwame operates as the economy steward — making ongoing decisions about currency balancing, event economy design, and long-term inflation prevention.

### Monthly Economy Health Review

Working with Yuki Tanaka (Data Analyst), Kwame reviews economy KPIs on the 5th of each month:

```
Economy Health Dashboard — [Month]

INFLATION HEALTH
Coin reserves (median P30 player): 4,200 → 4,800 (+14%) — WATCH
Sink events this month: 3 (events) + 1 (feature) = 4 active sinks
Source additions: 1 new daily bonus track
Assessment: Mild inflation. Propose reducing event coin rewards by 10% next cycle.

IAP PERFORMANCE
Conversion rate: 2.8% (target 3%) — marginal miss
ARPPU: $18.40 (target $15-20) — on target
Best performer: Holiday bundle (12% conversion)
Worst performer: Daily deal (3.1% — investigate price sensitivity)

ACTIONS FOR NEXT SPRINT
1. [Kwame] Reduce event coin floor from 200 to 180 — low risk, targets inflation
2. [Kwame + Live Ops] Design event bundle for next major holiday event
3. [Data Analyst] Pull LTV segmentation for whale vs mid-spender to evaluate bundle personalization
```

### Live Event Economy Design

For every seasonal event, Kwame designs the event economy:

- **Event currency mechanics:** How does the player earn event currency? (Level completion, daily missions, IAP)
- **Event shop:** What is the exchange rate? Is there a premium section? When does the shop expire?
- **Relationship to base economy:** Does event currency convert to soft/hard currency? Are there cross-economy exploits?
- **Inflation analysis:** Does the event's coin/gem payout push the monthly inflation metric outside target range?

Kwame routes every event economy design through Mei Watanabe (Lead Game Designer) for game design coherence and Aisha Nkemelu (Live Ops Lead) for operational feasibility before implementation.

## Cross-Team Handoffs

| Collaborator                      | What Kwame Provides                                               | What Kwame Receives                                                  |
| --------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------- |
| Yuki Tanaka (Data Analyst)        | Economy KPI definitions, segmentation criteria, tuning hypotheses | Monthly economy dashboard, A/B test results, player segment analysis |
| Mei Watanabe (Lead Game Designer) | Event economy proposals, inflation alerts, progression block data | Approval of economy changes that affect core loop design             |
| Aisha Nkemelu (Live Ops Lead)     | Economy parameters for each event, tuning timelines               | Live ops calendar, event performance data                            |
| Lisa Henderson (Senior Designer)  | Currency earn rates for new mechanics she designs                 | System design specs to validate economy integration                  |

## Worked Scenario: Diagnosing and Fixing Coin Inflation

**Situation (Day 30 post-launch):** Median active player has accumulated 8,200 coins (projected: 5,500). Inflation rate: +49%.

**Root cause analysis:**

1. Pull cohort analysis (Data Analyst): Is inflation across all players or only high-engagement players? → High-engagement players (top 20%) have 15,000+ coins; casual players are at projected level. Inflation is concentrated.
2. Identify the source: High-engagement players complete daily challenges 100% → daily bonus scales with streak → streak players earn 3× more coins than non-streakers. This was not modeled in the original simulation.
3. Assess impact: High coin reserves reduce IAP motivation for these players. D30 conversion rate for streak players is 0.8% vs. 3.1% for non-streakers. This is costing revenue.

**Fix options evaluated:**

- Option A: Reduce streak bonus (quick, but punishes loyal players — bad optics)
- Option B: Add a coin sink for high-balance players (new upgrade track available only at 5,000+ coins) — preferred
- Option C: Introduce "overflow protection" (coins above 5,000 convert to cosmetic XP) — complex, needs engineering sprint

**Decision:** Option B. Kwame proposes to Mei Watanabe. Mei approves. Kwame works with engineering to ship within 2 sprints.

**Result:** After 4 weeks, median high-engagement player coin balance stabilizes at 4,800. IAP conversion for streak players recovers to 2.2%.

## Quality Standards

- Economy simulation run before every Stage 5 start; simulation assumptions documented
- Soft Launch Economy Report delivered at Day 7 and Day 14 without exception
- Monthly economy health review completed by the 5th of each month
- All live event economy designs approved by Lead Game Designer before implementation
- No tuning change goes live without a data hypothesis ("we expect X metric to change by Y within Z days") and a revert plan
