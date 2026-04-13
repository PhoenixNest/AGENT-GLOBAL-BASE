---
name: f2p-economy-design
description: Virtual economy balancing, monetization loop design, currency sink/source modeling, and inflation risk management for free-to-play mobile games.
---

# F2P Economy Design

## Overview

This skill covers the design, balancing, and continuous optimization of virtual economies in F2P mobile games. It includes currency modeling, monetization loop architecture, inflation risk assessment, and pricing strategy.

## Tools & Frameworks

| Tool/Framework           | Purpose                                  | Proficiency Level |
| ------------------------ | ---------------------------------------- | ----------------- |
| Excel / Google Sheets    | Economy modeling, simulation             | Expert            |
| Python (pandas, numpy)   | Large-scale economy data analysis        | Advanced          |
| SQL                      | Player economy data extraction           | Advanced          |
| R                        | Statistical modeling of economy behavior | Intermediate      |
| Economy simulation tools | Virtual economy stress testing           | Advanced          |

## Core Methodologies

### 1. Currency Sink/Source Modeling

| Currency Type | Primary Sources                      | Primary Sinks                       | Balance Target                |
| ------------- | ------------------------------------ | ----------------------------------- | ----------------------------- |
| Soft Currency | Level completion, daily rewards, ads | Upgrades, boosts, event entry       | Net neutral per week          |
| Hard Currency | IAP, achievement rewards, events     | Premium items, time skips, gacha    | Controlled inflation (<5%/mo) |
| Energy        | Time-based regen, IAP, friends       | Level attempts, event participation | Slight deficit (IAP driver)   |

### 2. Inflation Risk Assessment

- **Monthly currency flow analysis:** Track total currency generated vs. consumed
- **Player segment analysis:** Monitor currency accumulation by player tier (whales, dolphins, minnows, F2P)
- **Inflation threshold:** > 10% monthly currency accumulation in any segment triggers corrective action
- **Corrective measures:** Introduce new sinks, adjust source rates, implement currency decay mechanics

### 3. Monetization Loop Architecture

```
Player Engagement → Resource Earning → Consumption Need → IAP Consideration
       ↑                                                    |
       └───────────── Value Delivery ←──────────────────────┘
```

**Key Principles:**

- Every IAP offer must deliver perceived value ≥ 2× price paid
- F2P progression must be viable (no paywalls that block progress)
- Premium currency pricing follows psychological price points ($0.99, $4.99, $9.99, $19.99, $49.99, $99.99)

## Scenario: Economy Rebalancing

**Situation:** Month 2 of soft launch shows 12% soft currency inflation in mid-tier players, reducing IAP conversion by 8%.

**Approach:**

1. **Diagnose:** Identify source of excess currency (event rewards too generous? level completion payouts inflated?)
2. **Model:** Simulate corrective measures (reduce event rewards by 15%, add new sink: cosmetic shop)
3. **Test:** A/B test corrected economy against baseline for 14 days
4. **Deploy:** Roll out winning variant; monitor inflation rate for 30 days post-deployment

**Trade-offs:**

- Reducing rewards risks player dissatisfaction; must communicate changes transparently
- Adding sinks must feel like value addition, not punishment
- Economy changes affect all player segments differently; segment-specific analysis required

## Quality Standards

- Economy model updated monthly with actual player data
- Inflation rate monitored weekly; alerts trigger at > 5% monthly accumulation
- All economy changes A/B tested before full deployment
- Player segment economy health reviewed quarterly
- Pricing strategy benchmarked against top 10 grossing games monthly

## Industry References

- Joost van Dreunen, "The Business of Games" (economy design principles)
- GDC: "Free-to-Play Economy Design" (various speakers)
- Playnomics: "F2P Economy Benchmarks" (industry data)
- DeltaDNA: "Player Economy Analytics" (methodology)
- Internal Playrix Economy Design Guide (Nkemelu's framework)
