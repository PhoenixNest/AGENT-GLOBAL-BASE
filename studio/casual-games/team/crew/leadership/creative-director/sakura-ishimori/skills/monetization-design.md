---
name: monetization-design
description: Player-centric F2P monetization strategy, IAP design, event pass systems, and engagement loop design that serves player motivation rather than exploiting frustration.
---

# Monetization Design

## Role

Monetization in F2P games is not about extracting money — it's about creating value that players voluntarily purchase. This skill covers the strategic framework for designing monetization systems that enhance rather than degrade the player experience, driving sustainable revenue while maintaining player trust and engagement.

## Core Philosophy: Monetization as Player Service

Every monetization touchpoint must serve one of three player motivations (Self-Determination Theory):

| Motivation      | What Players Buy                        | Design Principle                                | Anti-Pattern to Avoid                           |
| --------------- | --------------------------------------- | ----------------------------------------------- | ----------------------------------------------- |
| **Competence**  | Boosters, power-ups, skill accelerators | Help players overcome genuine skill barriers    | Pay-to-win mechanics that invalidate skill      |
| **Autonomy**    | Cosmetics, decorations, customization   | Give players meaningful self-expression choices | Cosmetic items that confer gameplay advantage   |
| **Relatedness** | Team gifts, social items, co-op content | Strengthen player-to-player connections         | Social pressure to spend (guilt-trip mechanics) |

## IAP Design Framework

### Value Proposition Design

Every IAP item must pass the "genuine value" test:

1. **Desirability**: Do players want this item? (Measured by wishlist/add-to-cart rate)
2. **Fairness**: Is the price proportional to the value delivered? (Measured by refund rate — target < 1%)
3. **Optionality**: Can players enjoy the full game without purchasing this item? (Measured by F2P retention vs. paying player retention — target < 5% gap)

### Pricing Strategy

| Item Type            | Price Range (USD) | Purchase Frequency Target | Design Notes                                      |
| -------------------- | ----------------- | ------------------------- | ------------------------------------------------- |
| Starter pack         | $0.99 – $4.99     | One-time (first 7 days)   | High perceived value, limited-time urgency        |
| Booster bundle       | $1.99 – $9.99     | 1–2 per week per payer    | Scales with player progression                    |
| Event pass           | $4.99 – $14.99    | Per event (bi-weekly)     | Seasonal content, exclusive rewards               |
| Cosmetic item        | $0.99 – $4.99     | 1–3 per month per payer   | Visual customization, no gameplay impact          |
| Monthly subscription | $4.99 – $9.99     | Monthly                   | Recurring value: daily rewards, exclusive content |

### Event Pass System Design

The event pass is the highest-performing monetization mechanic in casual games when designed correctly:

**Structure:**

- 30–50 tiers of rewards over a 14-day event period
- Free track: 40% of rewards available to all players (engagement driver)
- Premium track: 60% of rewards for pass purchasers ($4.99–$14.99)
- Premium-exclusive items must be genuinely desirable, not filler

**Design Principles:**

- Progression should feel achievable: Average player completes 60–70% of free track, 40–50% of premium track
- Reward pacing: Small rewards every 2–3 tiers, major rewards every 8–10 tiers
- The final premium reward should be a "crown jewel" that players see from the start and work toward
- Pass purchase rate target: 8–12% of MAU for casual games

## Engagement Loop Design

### Session Structure

| Session Phase | Duration    | Purpose                              | Monetization Touchpoint                      |
| ------------- | ----------- | ------------------------------------ | -------------------------------------------- |
| Warm-up       | 1–2 minutes | Re-engage player, daily reward claim | Daily login reward, streak bonus             |
| Core loop     | 3–8 minutes | Primary gameplay                     | Post-level offer (lost) or celebration (won) |
| Extension     | 1–3 minutes | Additional engagement                | Event progress, team contribution            |
| Cool-down     | 30 seconds  | Session closure                      | Next session preview, limited-time offer     |

### Retention-Driven Monetization

| Retention Metric | Monetization Connection                               | Design Action                                         |
| ---------------- | ----------------------------------------------------- | ----------------------------------------------------- |
| D1 Retention     | First-time player experience sets spending foundation | No monetization in first session; focus on engagement |
| D7 Retention     | Players who return 7 days have established habit      | Introduce starter pack at Day 3–4                     |
| D30 Retention    | Long-term players have emotional investment           | Event pass becomes primary monetization driver        |
| Day 90+          | Veteran players need novelty                          | Limited-time cosmetics, prestige systems              |

## Anti-Patterns (Never Use)

| Anti-Pattern                   | Why It Fails                                      | Alternative                                             |
| ------------------------------ | ------------------------------------------------- | ------------------------------------------------------- |
| Pay-to-win mechanics           | Destroys skill-based engagement, drives F2P churn | Cosmetic-only or convenience-only purchases             |
| Energy systems with short caps | Artificially limits engagement, feels punitive    | Longer energy caps, generous refill mechanics           |
| Pop-up offers every session    | Creates ad fatigue, degrades experience           | Contextual offers triggered by player behavior          |
| Time-gated progression         | Players feel blocked, not challenged              | Skill-gated progression with optional assist purchases  |
| Social pressure to spend       | Creates guilt, damages community trust            | Social rewards that benefit the group, not pressure     |
| Opaque pricing                 | Players can't evaluate value, lose trust          | Clear item descriptions, comparison tools, fair pricing |

## Analytics & Optimization

### Monetization KPIs (weekly review)

| KPI                | Target (Casual) | Alert Threshold | Action                                     |
| ------------------ | --------------- | --------------- | ------------------------------------------ |
| Conversion rate    | 3–5%            | < 2%            | Review IAP value propositions, pricing     |
| ARPPU              | $15–$25/month   | < $10           | Review premium item desirability           |
| ARPU               | $0.50–$1.50/day | < $0.30         | Review overall monetization balance        |
| Pass purchase rate | 8–12% of MAU    | < 5%            | Review event pass reward quality           |
| Refund rate        | < 1%            | > 2%            | Investigate item quality or pricing issues |

### A/B Testing Framework

- Test one monetization variable at a time (price, item, timing, presentation)
- Minimum sample size: 1,000 players per variant for statistical significance
- Test duration: Minimum 7 days to capture weekly engagement patterns
- Success metric: Revenue uplift without retention degradation (D7 and D30 must not drop > 3%)

## References

- `studio/casual-games/team/recruitment-plan/recruitment-plan.md` — Master recruitment plan
- `company/pipeline/development/pipeline.md` — Pipeline stages that include monetization design (Stage 1, 5, 8, 10)
- `company/library/topics/testing.md` — Testing standards for monetization feature validation
