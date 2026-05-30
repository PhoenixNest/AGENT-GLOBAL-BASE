---
name: studio-design-systems-design
description: Multi-layered game systems design for casual mobile games — progression systems, meta-game loops, collection systems, and interlocking reward structures that create long-term player engagement. Owned by Mei Watanabe (Lead Game Designer). Trigger: systems design, progression system, meta loop, game systems, collection system, reward design, game architecture.
version: "1.0.0"
---

# Systems Design

**Skill Owner:** Mei Watanabe (Lead Game Designer)
**Applies To:** Core Loop Architecture, Progression Systems, Meta-Game Design, Reward Structures

## System Categories

### 1. Progression Systems

The player's sense of forward momentum across sessions. Well-designed progression answers: "Why should I return tomorrow?"

**Design Layers:**

- **Micro-progression (within session):** Stars earned per level, XP accumulating toward a level-up
- **Macro-progression (across sessions):** Season pass tier advancement, chapter unlock
- **Meta-progression (persistent):** Base building, collection completion, leaderboard rank

**Calibration principles:**

- Ensure the player feels progression within the **first 3 minutes of every session** (micro-progression must be immediate)
- The macro-progression arc should take 4–6 weeks for engaged players to complete
- Meta-progression should never fully complete — there is always a next goal visible

### 2. Collection Systems

Collections are pull mechanics that drive daily engagement and spending:

| Component         | Design Requirement                                                             |
| ----------------- | ------------------------------------------------------------------------------ |
| Pity system       | Required for any RNG-gated collection: guaranteed drop within N attempts       |
| Completion reward | Completing a collection triggers a satisfying reward and reveals the next set  |
| Partial display   | Show locked/silhouetted items at all times — creates visible, achievable goals |
| Scarcity mechanic | Time-limited sets create urgency; permanent sets drive completion motivation   |

### 3. Meta-Game Loop

The meta-game is the layer above the core gameplay loop that gives meaning to winning individual rounds:

```
Core Loop (play a level)
    │
    ▼
Currency earned
    │
    ▼
Spend currency (upgrades / cosmetics / gacha)
    │
    ▼
Character / base power increases
    │
    ▼
New content unlocks or harder levels become accessible
    │
    ▼
Player returns for next session ◄────────────────────────────────┐
                                                                  │
                        Periodic events / seasons reinforce cycle ┘
```

## Real-World Production Scenarios

### Scenario 1: Designing the Progression System for a New Title

**Context:** Stage 1 (Concept), authoring the GDD's progression chapter.
**Process:**

1. Define the player journey arc: casual player (D1–D7), engaged player (D7–D30), highly engaged player (D30+)
2. Map one system per arc phase: onboarding tutorial system → chapter progression → meta-base building
3. For each system: define the reward cadence (how frequently does the player feel rewarded?), the grind ratio (effort to reward ratio), and the failure state (what happens when the player fails to progress?)
4. Present the system map to Sakura Ishimori (Creative Director) and Kwame Asante (Economy Designer) for alignment before writing the detailed GDD section
5. Validate assumptions with Yuki Tanaka (Data Analyst) using comparable title data

### Scenario 2: Diagnosing a Retention Drop at D7

**Context:** A/B test data (Yuki Tanaka) shows D7 retention is 3pp below the target (18% vs. 21%).
**Process:**

1. Review the D7 session data: where do players drop off in the core loop? Is it at a difficulty spike, a paywall, or a meta-game dead end?
2. Identify which system is responsible for the D7 experience: typically the end of the tutorial arc and the beginning of the meta-game loop
3. Propose 3 design hypotheses for A/B testing: (a) reduce the grind ratio on the meta-game, (b) introduce a timed event at D5–D7, (c) add a social mechanic (invites, leaderboards)
4. Each hypothesis becomes a separate A/B test card (Yuki Tanaka runs the statistical design)
5. Do not implement more than 2 concurrent A/B tests on the same system — confounds the analysis

## Measurable Quality Standards

| Standard                   | Target                 | Measurement Method            |
| -------------------------- | ---------------------- | ----------------------------- |
| D7 retention               | ≥20% (genre benchmark) | Cohort analysis (Yuki Tanaka) |
| D30 retention              | ≥8% (genre benchmark)  | Cohort analysis (Yuki Tanaka) |
| Average session length     | ≥12 minutes            | Analytics pipeline            |
| Sessions per DAU per day   | ≥2.5                   | Analytics pipeline            |
| Collection completion rate | ≥60% among D30 players | Analytics pipeline            |

## Industry Best Practice References

- **GDC 2025: "Designing for D30 Retention in Match-3"** — Mei Watanabe (speaker)
- **DiGRA 2023: F2P Economy Design paper** — Mei Watanabe (author)
- **"The Art of Game Design" — Jesse Schell** — Foundational systems thinking reference
- **King / Zynga progression patterns** — Industry benchmark for casual game systems
