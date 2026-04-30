---
name: studio-creative-design-economy-monetization
description: Virtual economy design and monetization strategy for F2P mobile games — currency flows, sink/source balancing, IAP design, and monetization ethics. Covers Stage 10 (Live Ops) live event economy design and monthly economy health review with Data Analyst. Owned by Lisa Henderson (Senior Game Designer). Trigger: economy design, monetization, IAP, currency balancing, virtual economy, live event economy, Stage 10 economy support.
version: "1.0.0"
---

# Economy & Monetization

**Skill ID:** economy-monetization
**Role:** Senior Game Designer
**Seniority:** Senior

## Overview

Virtual economy design and monetization strategy for F2P mobile games — currency flows, sink/source balancing, IAP design, and monetization ethics.

## Tools & Frameworks

| Tool                | Proficiency  | Use Case                                     |
| ------------------- | ------------ | -------------------------------------------- |
| Excel/Google Sheets | Expert       | Economy modeling, simulation                 |
| Python              | Intermediate | Economy simulation, data analysis            |
| Amplitude           | Advanced     | Monetization analytics                       |
| Unity IAP           | Intermediate | In-app purchase implementation understanding |

## Scenarios & Trade-offs

### Scenario 1: Dual Currency Economy Design

- **Approach:** Soft currency (earned through gameplay) + hard currency (purchased or earned sparingly); clear conversion rules; sink mechanisms for both
- **Trade-off:** Monetization pressure vs. F2P viability — too aggressive = player churn, too lenient = no revenue
- **Quality Bar:** F2P players can progress meaningfully; paying players get convenience and acceleration; economy remains stable over 12+ months

### Scenario 2: IAP Offer Design

- **Approach:** Tiered pricing ($0.99–$99.99); value perception optimized; limited-time offers for urgency; personalized offers based on player behavior
- **Trade-off:** Revenue optimization vs. player trust — aggressive monetization can damage long-term retention
- **Quality Bar:** Conversion rate ≥ 3%; ARPDAU increases without D7 retention decrease; player satisfaction scores maintained

## Stage 10 — Live Ops Economy Design Support

Lisa's profile includes Stage 10 (Live Ops) because economy design does not end at launch. She provides ongoing design support to the Live Ops team:

### Live Event Economy Design

Each live event requires Lisa to design the event-specific economy: event currency sources, event shop contents, premium offer placement, and the relationship between the event economy and the base game economy.

**Event economy checklist:**

- Does the event currency have a time-limited sink (event shop clears at end)? If currency persists, document carry-over policy.
- Does the event premium offer follow the same ethical standards as base IAP (no artificial scarcity, no pay-to-win)?
- Has the event economy been reviewed by Kwame Asante (Economy Designer) for inflation risk?
- Does the event reward cadence preserve the base game's D7 and D30 retention curves (no cannibalization)?

### Monthly Economy Health Review

Working with Yuki Tanaka (Data Analyst), Lisa reviews economy KPIs monthly:

| KPI                                 | Target                                | Lisa's Action Threshold                            |
| ----------------------------------- | ------------------------------------- | -------------------------------------------------- |
| Coin sink/source ratio              | 0.9–1.1 (balanced)                    | >1.2 or <0.8 → tuning proposal within 5 days       |
| IAP conversion rate                 | ≥3% MAU                               | <2% → re-evaluate offer mix and entry price points |
| Premium currency earn rate (F2P)    | 50–100 gems/week at median engagement | >150 → risk of IAP cannibalization                 |
| Player-reported economy frustration | <5% of support tickets                | >10% → economy pain point investigation            |

### Live Ops Tuning Requests

When Live Ops (Aisha Nkemelu) requests an economy parameter change (drop rate, pricing, currency amount), Lisa reviews the change against the economy model before it is implemented:

```
Tuning Request: Reduce Level 20 coin reward from 500 to 350
Lisa's review:
- Impact on daily coin income for median player: -15%
- Impact on inflation: positive (reduces coin surplus)
- Risk: affects "almost made it" spending moments at this level
- Recommendation: Approve with 3-day post-change monitoring; revert if D1 retention drops >1%
```

## Quality Standards

- Economy model documented with all currency sources and sinks
- Inflation control mechanisms designed and tested
- IAP pricing tested across target markets (regional pricing)
- Monetization design reviewed for ethical compliance (no dark patterns)
- Economy simulation run for 12-month projection before launch
- All live event economy designs reviewed by Kwame Asante before implementation
- Monthly economy health review completed with Data Analyst by the 5th of each month

## Industry References

- Playrix's economy design for Gardenscapes (18% ARPDAU increase)
- King's monetization strategy for Candy Crush franchise
- F2P economy design ethics guidelines
