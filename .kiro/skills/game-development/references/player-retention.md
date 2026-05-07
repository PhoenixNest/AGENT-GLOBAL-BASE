---
name: studio-design-player-retention
description: D1/D7/D30 retention design for casual mobile games — reward scheduling, habit loop mechanics, push notification strategy, re-engagement systems, and data-informed retention optimization. Owned by Mei Watanabe (Lead Game Designer). Trigger: retention, D1 D7 D30, player retention, churn, re-engagement, push notifications, habit loop, reward schedule.
version: "1.0.0"
---

# Player Retention

**Skill Owner:** Mei Watanabe (Lead Game Designer)
**Applies To:** Retention Design, Reward Scheduling, Re-Engagement Mechanics, Stage 1–5 Design Deliverables

## Retention Benchmarks (Casual Mobile Games)

| Metric        | Soft Launch Gate | Global Launch Target | Industry Average |
| ------------- | ---------------- | -------------------- | ---------------- |
| D1 Retention  | ≥40%             | ≥45%                 | 35–40%           |
| D7 Retention  | ≥20%             | ≥22%                 | 15–20%           |
| D30 Retention | ≥8%              | ≥10%                 | 6–8%             |

These targets are reviewed against comparable titles by Yuki Tanaka (Data Analyst) before each gate. Titles failing the soft launch gate do not advance to Stage 9 (Global Launch Readiness) without Studio Director sign-off.

## Retention Mechanics Framework

### 1. Habit Loop Design (B.J. Fogg — Motivation × Ability × Prompt)

Every session trigger must align with the player's current habit formation phase:

| Phase (Days) | Player Motivation | Design Priority                                                                                          |
| ------------ | ----------------- | -------------------------------------------------------------------------------------------------------- |
| D1–D3        | Novelty           | Tutorial minimizes friction; first reward in <2 minutes; strong onboarding hook                          |
| D3–D7        | Commitment        | Daily login streak begins; first meta-progression milestone visible; social comparison introduced        |
| D7–D30       | Routine           | Session schedule reinforcement; weekly events; Guild/friend activity feed                                |
| D30+         | Identity          | Player identity systems (avatar, base, title); long-term goals (seasonal content, collection completion) |

### 2. Daily Login Reward System

**Design requirements:**

- The D1–D7 reward arc must be front-loaded with high-perceived-value rewards to establish the habit
- A "streak protection" mechanic is required: players who miss 1 day receive their streak reward for free within the next 24 hours. This reduces D7 churn significantly.
- The reward calendar must always show the next 7 days — players must know what they're working toward
- Never lock the calendar behind a paywall — it's a retention driver, not a monetization surface

### 3. Push Notification Strategy

Push notifications are the primary re-engagement tool but are irreversible if misused (uninstall risk).

| Trigger                                                          | Message Type | Max Frequency    |
| ---------------------------------------------------------------- | ------------ | ---------------- |
| Energy refilled (if applicable)                                  | Functional   | 2× per day max   |
| Daily reward available                                           | Functional   | 1× per day       |
| Time-limited event starting                                      | Urgency      | Event start only |
| Personalized milestone ("You're 3 stars from the next chapter!") | Progress     | 1× per week max  |
| Friend activity ("Ana just surpassed your score!")               | Social       | 1× per day max   |

**Never send:** More than 2 push notifications per day. Do not send notifications during local nighttime hours (22:00–08:00 in user's timezone).

### 4. Re-Engagement Systems (Players Churned after D7)

For players who have not opened the game in 3+ days:

1. **Win-back notification:** personalized to the player's last action ("Your base needs you!" / "A new chapter is waiting")
2. **Win-back offer:** one-time re-engagement gift (soft currency, energy refill) available for 48 hours after opening the win-back notification — no purchase required
3. **Re-onboarding:** if the player has been absent ≥14 days, offer a brief "what's new" recap before resuming play

## Real-World Production Scenario

### Scenario: D7 Retention Drop Identified at Soft Launch

**Context:** Soft launch data (Yuki Tanaka) shows D7 retention at 16% — below the 20% gate.
**Process:**

1. Pull the funnel data: where in the D4–D7 experience do players drop off?
2. Common diagnosis: "meta-game desert" — the tutorial ends, the core loop becomes repetitive, and the meta-game hasn't introduced a new hook yet
3. Design intervention: introduce a "D5 event" — a limited-time challenge with a unique reward that expires at D8. This creates urgency to return and establishes the events loop
4. Run A/B test: 50% players get the D5 event; 50% control. Test for 2 weeks (Yuki Tanaka runs the statistical design)
5. If D7 retention lifts ≥2pp with p < 0.05, ship globally

## Measurable Quality Standards

| Standard                       | Target at Soft Launch  | Measurement Method            |
| ------------------------------ | ---------------------- | ----------------------------- |
| D1 retention                   | ≥40%                   | Cohort analysis (Yuki Tanaka) |
| D7 retention                   | ≥20%                   | Cohort analysis (Yuki Tanaka) |
| D30 retention                  | ≥8%                    | Cohort analysis (Yuki Tanaka) |
| Push notification opt-out rate | ≤30%                   | Analytics pipeline            |
| Day-5 event participation      | ≥60% of active players | Event analytics               |

## Industry Best Practice References

- **GDC 2025: "Designing for D30 Retention in Match-3"** — Mei Watanabe (speaker)
- **"Hooked" — Nir Eyal** — Habit loop formation framework
- **King retention design patterns** — Mei's prior methodology
- **AppsFlyer Mobile Benchmarks Report** — Industry D1/D7/D30 benchmarks
