---
name: monetization-strategy
description: IAP design, battle pass architecture, limited-time offer strategy, and value proposition optimization for F2P games.
version: "1.0.0"
---

# Monetization Strategy

## Overview

This skill covers the design and optimization of monetization systems in F2P mobile games, focusing on player-friendly monetization that maximizes revenue without compromising player experience.

## IAP Design Principles

| Principle          | Implementation                            | Rationale                         |
| ------------------ | ----------------------------------------- | --------------------------------- |
| Player-first value | Every IAP delivers ≥ 2× perceived value   | Builds trust, encourages spending |
| No paywalls        | All content accessible without spending   | Maintains F2P integrity           |
| Price anchoring    | Strategic pricing tiers ($0.99 to $99.99) | Guides spending decisions         |
| Scarcity & urgency | Limited-time offers, countdown timers     | Drives impulse purchases          |
| Personalization    | Targeted offers based on player behavior  | Increases relevance, conversion   |

## Battle Pass Architecture

| Component     | Design Guideline                        | Impact              |
| ------------- | --------------------------------------- | ------------------- |
| Free track    | 30% of total rewards, meaningful items  | Engagement driver   |
| Premium track | 70% of rewards, exclusive cosmetics     | Conversion driver   |
| Duration      | 28–35 days (aligned with monthly cycle) | Predictable revenue |
| Price         | $9.99–$14.99                            | Accessible premium  |
| Progression   | 50–70 tiers, achievable with 30 min/day | Daily engagement    |

## Offer Strategy

| Offer Type     | Frequency     | Discount Range | Conversion Rate Target |
| -------------- | ------------- | -------------- | ---------------------- |
| Starter pack   | Once/player   | 80–90% off     | 25–35%                 |
| Daily deal     | Daily         | 30–60% off     | 5–10%                  |
| Weekly bundle  | Weekly        | 40–70% off     | 8–15%                  |
| Event special  | Per event     | 50–80% off     | 10–20%                 |
| Comeback offer | Lapsed player | 70–90% off     | 15–25%                 |

## Personalized Offer Design

Generic offers underperform personalized offers by 2–4× in conversion. Kwame designs the offer personalization strategy based on behavioral segments:

| Segment                                   | Trigger                                    | Offer Design                                                      | Why It Works                                                  |
| ----------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------- | ------------------------------------------------------------- |
| **New player (D1–D3)**                    | First session completion                   | Starter pack: high-value, low-price ($0.99–$2.99), one-time only  | Establishes spending habit at lowest psychological barrier    |
| **Engaged F2P (D7+ active, 0 purchases)** | 3rd consecutive coin depletion             | "Power up" bundle: coins + 1 premium item at 70% discount         | Converts at the moment of highest frustration                 |
| **Past purchaser**                        | First purchase anniversary                 | Loyalty offer: 150% value vs. original purchase, same price point | Rewards brand loyalty; re-engages purchasing behavior         |
| **Whale (>$50 LTV)**                      | 30 days since last purchase                | High-value bundle ($19.99–$49.99) with exclusive cosmetic         | High perceived exclusivity; whale segment responds to premium |
| **Lapsed player (14+ days inactive)**     | Re-engagement push notification → app open | Comeback offer: 80% off + 3 free lives                            | Reduces re-engagement friction                                |
| **Progression staller**                   | Player fails same level 5+ times           | "Helping hand" offer: 3 lives + 1 power-up at $1.99               | Targets moment of maximum frustration/intent to spend         |

### Personalization Guard Rails

- Never show a paid offer within 60 seconds of another paid offer
- A player who has declined 3 consecutive offers of the same type is suppressed from that type for 7 days
- No offer uses artificial countdown timers on permanent catalog items — real scarcity only

## Stage 8 — Soft Launch Monetization Assessment

At Stage 8 (Soft Launch), Kwame produces a **Monetization Assessment Report** at Day 14:

```markdown
# Soft Launch Monetization Assessment — Day 14

## Revenue KPIs

| KPI                   | Target            | Actual | Assessment                         |
| --------------------- | ----------------- | ------ | ---------------------------------- |
| IAP conversion (D7)   | 3%                | 2.1%   | Below target — starter pack review |
| ARPPU (D14)           | $12–$18           | $9.40  | Below — avg. IAP price too low     |
| Paying player % (D14) | 4–6%              | 3.2%   | Below — top-of-funnel offer gap    |
| Battle pass uptake    | 15% of active D7+ | 8%     | Below — value perception issue     |

## Root Cause Analysis

[Specific diagnosis: "The starter pack is priced at $2.99 but competitive titles benchmark at $0.99 for the casual puzzle genre. Premium price perception is suppressing first conversion."]

## Recommended Changes

1. Reduce starter pack price from $2.99 to $0.99; compensate by reducing coin quantity 25%
2. Add "first time buyer" IAP banner to the post-level-completion screen (currently only visible in shop)
3. Add 1 exclusive cosmetic to battle pass free track to improve value perception

## Risks of Not Addressing

At current conversion rate, projected D30 ARPU is $0.28 vs. $0.45 target. This creates an $0.17/DAU gap that compounds into a viability issue at scale.
```

## Stage 10 — Live Monetization Operations

In Stage 10, Kwame manages the monetization calendar and evaluates the performance of every live offer:

### Monthly Monetization Calendar

Kwame plans the next month's offers by the 20th of the current month, submitted to Aisha Nkemelu (Live Ops Lead) for scheduling:

```
November Monetization Calendar

Week 1: Thanksgiving Pack — 60% off bundle (historical event: 9% conversion)
Week 2: Standard rotation — daily deals and weekly bundles
Week 3: Black Friday Special — highest-value offer of the year ($9.99 premium bundle, 85% off)
Week 4: Pre-holiday ramp — gift-themed starter pack for new users acquired from holiday UA spend

Rationale: Black Friday historically represents 2.5× normal ARPPU week. Front-load the high-value offer
at peak spending intent rather than spreading across the month.
```

### Offer Postmortem (Mandatory)

After every limited-time offer, Kwame completes a one-page offer postmortem within 5 business days:

```markdown
# Offer Postmortem: Halloween Bundle

Duration: Oct 28–Nov 1 | Price: $4.99

Target conversion: 8% | Actual: 11.2% ✅
Target revenue: $12,000 | Actual: $17,400 ✅
Player satisfaction (post-offer survey): 4.3/5 ✅

Why it worked:

- Cosmetic was genuinely exclusive (no equivalent in base game)
- Offer appeared at end of session (high engagement moment), not on app open (low intent)
- Price point matched "impulse buy" zone for this player segment

Replication for next holiday: [specific elements to carry forward]
```

## Cross-Team Handoffs

| Collaborator                                    | What Kwame Provides                                                    | What Kwame Receives                                             |
| ----------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------- |
| Yuki Tanaka (Data Analyst)                      | A/B test specs for offer variants, conversion attribution requirements | Offer performance dashboards, segment LTV analysis, A/B results |
| Aisha Nkemelu (Live Ops Lead)                   | Monthly monetization calendar, event offer specs                       | Live ops schedule, event participation rates                    |
| David Okafor / Sofia Reyes (Live Ops Engineers) | Offer configuration parameters, personalization rules                  | Offer implementation confirmation, A/B test activation status   |
| Mei Watanabe (Lead Game Designer)               | Monetization changes affecting progression pacing                      | Approval for offers that modify core economy sinks/sources      |

## Quality Standards

- Monthly monetization calendar submitted to Live Ops Lead by the 20th of the preceding month
- Offer postmortem completed within 5 business days of every limited-time offer
- No offer targets a segment that has declined 3+ consecutive offers of the same type
- Soft Launch Monetization Assessment Report delivered at Day 14
- All personalization rules reviewed for dark pattern compliance before implementation (no artificial scarcity on permanent items)
