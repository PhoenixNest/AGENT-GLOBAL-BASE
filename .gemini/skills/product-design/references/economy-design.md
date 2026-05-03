---
name: studio-creative-design-economy-design
description: Virtual economy design, currency balancing, monetization strategy, and live ops economy management for F2P casual games. Owned by Mei Watanabe (Lead Game Designer). Use during Studio Pipeline Stages 1–5 and 10 for economy modeling and live economy tuning. Trigger: economy design, currency balancing, dual currency, economy simulation, live ops economy, economy inflation, IAP strategy.
version: "1.0.0"
---

# Economy Design

**Skill Owner:** Mei Watanabe (Lead Game Designer)
**Applies To:** Virtual Economy Design, Currency Balancing, Monetization Strategy, Live Ops Economy

## Tools & Frameworks

| Tool/Framework      | Version Context | Usage                                      |
| ------------------- | --------------- | ------------------------------------------ |
| Google Sheets       | Latest          | Economy modeling, progression curves       |
| Python + Pandas     | 3.12+ / 2.2+    | Economy simulation, cohort analysis        |
| Amplitude           | Latest          | Player behavior analytics, funnel analysis |
| Unity Remote Config | Latest          | Live economy tuning without app updates    |
| Jupyter Notebooks   | Latest          | Economy balance documentation              |

## Real-World Production Scenarios

### Scenario 1: Designing a Dual-Currency Economy

**Context:** New casual game needs soft and hard currency system.
**Process:**

1. Define currency purposes: soft (earned through gameplay, used for progression), hard (earned slowly or purchased, used for premium items)
2. Model currency flow: sources (level completion, daily rewards, IAP) and sinks (upgrades, boosts, cosmetics)
3. Balance progression: each level's reward should be enough to afford the next level's cost with 10-20% surplus
4. Design IAP strategy: value packs at $0.99, $4.99, $9.99, $19.99, $49.99 with increasing value per dollar
5. Simulate economy: run 10,000 player simulations to identify inflation points, progression walls, and monetization opportunities
6. A/B test economy variants with 10% of players, measure D1/D7 retention and IAP conversion

### Scenario 2: Fixing Economy Inflation in a Live Game

**Context:** Players are hoarding soft currency, progression is too easy, IAP revenue declining.
**Process:**

1. Analyze data: identify currency accumulation rate, average player balance, IAP purchase frequency
2. Identify root cause: reward amounts too high, sink options too limited, progression too flat
3. Design fixes: add new currency sinks (cosmetic items, time-limited events), reduce reward amounts by 15%, add prestige system
4. Roll out changes gradually: 5% → 25% → 100% of players over 2 weeks
5. Monitor: track currency balance, IAP conversion, retention metrics
6. Results: 20% increase in IAP revenue, stable retention, healthier economy

## Trade-Off Analysis

| Decision            | Option A                 | Option B                      | Trade-Off                                                                                                          |
| ------------------- | ------------------------ | ----------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Currency Generosity | Generous (easy to earn)  | Tight (hard to earn)          | Generous = happy players but low IAP; Tight = higher IAP but player frustration risk                               |
| IAP Pricing         | Low prices ($0.99-$4.99) | Premium prices ($4.99-$49.99) | Low = higher conversion but lower ARPPU; Premium = lower conversion but higher ARPPU                               |
| Economy Complexity  | Simple (1-2 currencies)  | Complex (4-5 currencies)      | Simple = easy to understand but limited monetization; Complex = more monetization levers but player confusion risk |

## Measurable Quality Standards

| Standard                        | Target                 | Measurement Method  |
| ------------------------------- | ---------------------- | ------------------- |
| D1 Retention                    | ≥ 45%                  | Analytics dashboard |
| D7 Retention                    | ≥ 20%                  | Analytics dashboard |
| IAP Conversion Rate             | ≥ 3%                   | Analytics dashboard |
| Average Revenue Per Paying User | ≥ $15/month            | Analytics dashboard |
| Economy Balance                 | ≤ 20% currency surplus | Economy simulation  |

## Industry Best Practice References

- **King Economy Design Standards** — Industry-standard F2P economy principles
- **DiGRA 2023: "F2P Economy Design"** — Mei's published paper
- **Game Economy Design: "The Math Behind the Fun"** — Industry-standard economy design guide
- **Joost van Dreunen: "The Business of Video Games"** — F2P monetization strategy
