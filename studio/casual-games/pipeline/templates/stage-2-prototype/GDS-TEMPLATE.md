# Game Design Specification (GDS) — Template

> **Stage:** 2 — Prototype
> **Producer:** Creative Director (Sakura Ishimori)
> **Kill Gate:** KG-2 — Prototype Validation
> **User Approval:** ✅ Required (as part of Stage 2 package)

The GDS is the detailed design contract for the game. It expands the GDD's concept into actionable specifications for engineers, artists, and audio crew. It is a living document — updated through Stage 5.

---

## Document Control

| Field          | Value               |
| :------------- | :------------------ |
| **Game Title** | [Working title]     |
| **Version**    | v0.2 (Prototype)    |
| **Date**       | YYYY-MM-DD          |
| **Author**     | [Creative Director] |

---

## 1. Core Mechanics — Detailed Specification

### 1.1 [Primary Mechanic Name]

**Description:** [2–3 sentences explaining the mechanic precisely]

**Input:** [What the player does — tap, swipe, hold, etc.]

**Output:** [What happens as a result]

**Feedback:** [Visual / audio / haptic feedback]

**Feel targets:** [e.g. "Snappy response < 50ms; satisfying impact sound; particle burst on success"]

**Edge cases:**

- [Edge case 1 and expected behaviour]
- [Edge case 2 and expected behaviour]

### 1.2 [Secondary Mechanic Name]

[Same structure as above]

---

## 2. Level / Content Specification

### 2.1 Level Structure

| Level Type     | Count (Prototype) | Estimated Count (Full) | Description          |
| :------------- | :---------------: | :--------------------: | :------------------- |
| Tutorial       |         1         |           1            | First-run experience |
| [Level type 1] |        [N]        |          [N]           | [Description]        |
| [Level type 2] |        [N]        |          [N]           | [Description]        |

### 2.2 Difficulty Curve

| Phase      | Levels  | Challenge | New Elements Introduced |
| :--------- | :------ | :-------- | :---------------------- |
| Onboarding | 1–[N]   | Low       | Core mechanic only      |
| Early game | [N]–[N] | Medium    | [Secondary mechanic]    |
| Mid game   | [N]–[N] | High      | [Advanced mechanic]     |
| Late game  | [N]+    | Very high | [Expert mechanic]       |

---

## 3. Economy Design

### 3.1 Currency System

| Currency | Name   | Earned By               | Spent On | Purchasable? |
| :------- | :----- | :---------------------- | :------- | :----------: |
| Soft     | [Name] | Gameplay, daily rewards | [Uses]   |      ☐       |
| Hard     | [Name] | IAP, special rewards    | [Uses]   |      ✅      |

### 3.2 IAP Products (Prototype Stage)

| Product         | Price         | Value      | Notes   |
| :-------------- | :------------ | :--------- | :------ |
| [Starter pack]  | $[X.XX]       | [Contents] | [Notes] |
| [Currency pack] | $[X.XX]       | [Contents] | [Notes] |
| [Battle pass]   | $[X.XX]/month | [Contents] | [Notes] |

### 3.3 Reward Schedule

| Reward         | Trigger     | Frequency | Value                  |
| :------------- | :---------- | :-------- | :--------------------- |
| Daily login    | App open    | Daily     | [Soft currency amount] |
| Level complete | Level clear | Per level | [Soft currency amount] |
| First purchase | IAP         | Once      | [Bonus multiplier]     |

---

## 4. Progression System

| Progression Type | Mechanic      | Reset on Fail? | Long-term driver? |
| :--------------- | :------------ | :------------: | :---------------: |
| [Type 1]         | [Description] |       ☐        |         ☐         |
| [Type 2]         | [Description] |       ☐        |         ☐         |

---

## 5. Social Features

| Feature        | Description   |       Stage        |
| :------------- | :------------ | :----------------: |
| [Leaderboard]  | [Description] | [Stage when built] |
| [Friends list] | [Description] | [Stage when built] |

---

## 6. Audio Design Brief

> Detailed audio spec produced by Audio division in Stage 5.

| Element            | Direction                                     |
| :----------------- | :-------------------------------------------- |
| **Music tone**     | [e.g. Upbeat, loopable, non-intrusive]        |
| **SFX philosophy** | [e.g. Tactile, satisfying, minimal UI sounds] |
| **Adaptive audio** | ☐ Yes / ☐ No                                  |

---

**Produced by:** [Creative Director] on YYYY-MM-DD
**Reviewed by:** [Studio Director] on YYYY-MM-DD
