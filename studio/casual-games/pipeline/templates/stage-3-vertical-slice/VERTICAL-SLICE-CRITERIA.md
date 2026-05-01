# Vertical Slice Completion Criteria — Stage 3

> **Stage:** 3 — Vertical Slice
> **Producer:** Studio Director (Dr. Marcus Vogel)
> **Kill Gate:** KG-3 — Vertical Slice
> **User Approval:** ✅ Required before advancing to Stage 4

---

## What Is the Vertical Slice?

The vertical slice is a **polished, playable section of the game** representing the final quality bar. It must demonstrate the complete art style, core mechanics, economy, audio, and UX — at a level that could appear in a shipping product. It is the definitive proof that the team can execute the full vision.

---

## Completeness Checklist

### Core Mechanics

- [ ] All primary mechanics playable end-to-end
- [ ] All secondary mechanics present (may be unpolished)
- [ ] Core loop executes 3+ times without interruption
- [ ] No placeholder mechanics — all mechanics are intended-final implementations

### Art and Visual Quality

- [ ] Final art style established and consistent across all vertical slice content
- [ ] Character(s) final design implemented
- [ ] Environment/background at final quality
- [ ] VFX for primary mechanic complete
- [ ] UI meets IDS specification (visual conformance ≥ 90%)

### Audio

- [ ] Background music (final or near-final) present
- [ ] Core mechanic SFX implemented
- [ ] UI SFX implemented
- [ ] No placeholder audio assets (temp music/SFX that won't ship)

### Economy and Progression

- [ ] At least one IAP product functional (test environment)
- [ ] Soft currency earn/spend loop complete
- [ ] At least 10 levels of content (or equivalent session depth)
- [ ] Difficulty curve validates against playtest targets

### Technical Quality

- [ ] Builds without errors on all target platforms
- [ ] Runs at ≥ 30 fps on minimum-spec target device
- [ ] Cold start < [X] seconds
- [ ] Memory usage within target budget
- [ ] ADR-GAME-ARCHITECTURE.md architecture decisions implemented correctly
- [ ] TSD technology stack implemented with approved versions

---

## Kill Gate 3 — Playtest Metrics

### Playtest Setup

| Field                                | Value         |
| :----------------------------------- | :------------ |
| **Number of participants**           | [Minimum: 20] |
| **Target audience match**            | ☐ Yes / ☐ No  |
| **Session duration per participant** | [X minutes]   |

### Metric Targets

| Metric                                   | Threshold | Actual | Pass? |
| :--------------------------------------- | :-------: | :----: | :---: |
| D1 Retention (simulated)                 |  ≥ [X]%   |        |   ☐   |
| D7 Retention (simulated)                 |  ≥ [X]%   |        |   ☐   |
| Fun factor score (1–5)                   |  ≥ [X.X]  |        |   ☐   |
| Visual quality rating (1–5)              |  ≥ [X.X]  |        |   ☐   |
| Would pay for this game (% yes)          |  ≥ [X]%   |        |   ☐   |
| Core loop clarity (% no tutorial needed) |  ≥ [X]%   |        |   ☐   |

---

## Architecture Lock Confirmation

By completing Kill Gate 3, the following are **locked**:

| Document                 | Locked | Approver               |
| :----------------------- | :----: | :--------------------- |
| ADR-GAME-ARCHITECTURE.md |   ☐    | Studio Director + User |
| TSD.md                   |   ☐    | Studio Director + User |
| Third-party SDK list     |   ☐    | CSO                    |

> Any architecture change after KG-3 requires a new ADR and full Stage 3 re-entry.

---

## Kill Gate 3 Decision

| Field                              | Value                                      |
| :--------------------------------- | :----------------------------------------- |
| **All checklist items complete?**  | ☐ Yes / ☐ No (list incomplete items below) |
| **All metric thresholds met?**     | ☐ Yes / ☐ No                               |
| **Studio Director recommendation** | ☐ Proceed / ☐ Iterate + Relaunch / ☐ Kill  |
| **Rationale**                      | [2–3 sentences]                            |

**Incomplete items (if any):**

- [ ] [Item]
- [ ] [Item]

---

**Produced by:** [Studio Director] on YYYY-MM-DD
**Awaiting User (CEO) decision.**
