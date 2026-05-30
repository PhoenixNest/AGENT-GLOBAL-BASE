---
name: studio-creative-design-game-design-vision
description: Game design vision and GDD authorship — core loop design, game design direction, economy balancing, and analytics instrumentation for casual games. Owned by Mei Watanabe (Lead Game Designer). Use during Studio Pipeline Stages 0–4 for game concept definition and design direction. Trigger: game design vision, GDD, core loop, game direction, design leadership, game concept.
version: "1.0.0"
---

# Game Design Vision

**Skill Owner:** Mei Watanabe (Lead Game Designer)
**Applies To:** GDD Authorship, Core Loop Design, Game Design Direction

## Tools & Frameworks

| Tool/Framework       | Version Context | Usage                                     |
| -------------------- | --------------- | ----------------------------------------- |
| Confluence           | Latest          | GDD documentation, design specs           |
| Miro                 | Latest          | Core loop mapping, system design diagrams |
| Figma                | Latest          | UI/UX wireframing for game screens        |
| Unity                | 2024 LTS+       | Prototype validation, playtesting         |
| Google Sheets        | Latest          | Economy balancing, progression curves     |
| Amplitude / Mixpanel | Latest          | Player behavior analytics                 |

## Real-World Production Scenarios

### Scenario 1: Authoring a GDD for a New Casual Game

**Context:** Stage 1 (Concept) — Define the complete game design before prototyping.
**Process:**

1. Define core game loop: Action → Reward → Progression → Unlock → Repeat
2. Design progression systems: level-based, collection-based, meta-base building
3. Design economy: soft currency (earned through gameplay), hard currency (earned or purchased), energy system
4. Define success criteria: D1 retention target 45%, D7 target 20%, D30 target 8%
5. Specify analytics instrumentation: event tracking for every player action
6. Document all systems with clear rules, edge cases, and failure states
7. Review with Creative Director, Engineering Lead, and Producer for feasibility

### Scenario 2: Redesigning an Existing Game's Economy

**Context:** Live game needs economy rebalancing to improve retention.
**Process:**

1. Analyze player data: identify drop-off points, currency hoarding patterns, IAP conversion rates
2. Identify economy imbalances: too much soft currency inflation, hard currency too expensive, progression wall too steep
3. Design new economy: adjust currency sinks/sources, reprice IAPs, smooth progression curve
4. A/B test new economy with 10% of player base
5. Measure results: D1 +12%, D7 +8%, IAP conversion +5%
6. Roll out to 100% of players

## Trade-Off Analysis

| Decision              | Option A                         | Option B                                    | Trade-Off                                                                                               |
| --------------------- | -------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Progression Speed     | Fast progression (quick rewards) | Slow progression (longer engagement)        | Fast = higher D1 but lower D30; Slow = lower D1 but higher D30                                          |
| Monetization Approach | Cosmetic IAPs only               | Pay-for-progression + cosmetics             | Cosmetic = fair but lower revenue; Pay-for-progress = higher revenue but player frustration risk        |
| Complexity            | Simple core loop (match-3)       | Complex meta-game (base building + match-3) | Simple = broader audience but shorter lifespan; Complex = deeper engagement but higher development cost |

## Measurable Quality Standards

| Standard              | Target                                         | Measurement Method             |
| --------------------- | ---------------------------------------------- | ------------------------------ |
| GDD Completeness      | 100% of systems documented                     | GDD review checklist           |
| Design Feasibility    | ≥ 90% of designs implementable within timeline | Engineering feasibility review |
| Player Retention (D1) | ≥ 45%                                          | Analytics dashboard            |
| Player Retention (D7) | ≥ 20%                                          | Analytics dashboard            |
| IAP Conversion Rate   | ≥ 3%                                           | Analytics dashboard            |

## Industry Best Practice References

- **King Design Review Process** — Data-driven design decisions with metrics backing
- **GDC 2025: "Designing for D30 Retention in Match-3"** — Mei's own talk
- **DiGRA 2023: "F2P Economy Design"** — Published paper on economy design principles
- **Game Design Patterns: "Core Loop Design"** — Industry-standard core loop framework
