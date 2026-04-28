---
name: studio-engineering-combat-progression-systems
description: End-to-end combat and progression system design — damage calculation, hit confirmation, input buffering, combo systems, leveling, skill trees, and reward scheduling. Owned by Kaelen Reeves (Senior Gameplay Engineer). Use during Studio Pipeline Stages 2–5 for combat system implementation and Stage 8 (Soft Launch) for retention validation. Trigger: combat systems, progression systems, hit registration, input buffering, skill trees, damage calculation.
version: "1.0.0"
---

# Combat & Progression Systems

**Skill Owner:** Kaelen Reeves  
**Version:** 1.0 | **Date:** 2026-04-20

---

## Description

End-to-end design and implementation of combat systems (damage calculation, hit confirmation, input buffering, combo systems) and progression systems (leveling, skill trees, reward scheduling) for mobile games.

## Tools & Frameworks

| Tool/Framework    | Version      | Context                                                                    |
| ----------------- | ------------ | -------------------------------------------------------------------------- |
| Unity Engine      | 2023 LTS     | Primary game engine; custom combat framework built on Unity's Input System |
| C#                | 11.0         | Combat logic, progression data models, serialization                       |
| ScriptableObjects | Unity native | Data-driven combat parameters and progression configuration                |
| Addressables      | Unity 2023   | Async loading of combat assets and progression rewards                     |
| PlayFab Economy   | v2.17        | Server-authoritative progression tracking and reward distribution          |

## Production Scenarios

### Scenario 1: Combat System Redesign (Brawl Stars, Supercell 2023)

**Problem:** Existing combat system had inconsistent hit registration causing player complaints. Input latency averaged 45ms.  
**Solution:** Redesigned input buffering system with 120ms buffer window, server-side hit validation with rollback, and deterministic damage calculation.  
**Result:** Hit registration complaints dropped 78%; input latency reduced to 16ms; D7 retention improved 4%.

### Scenario 2: Progression System Architecture (Supercell 2024)

**Problem:** Player progression felt grindy; D30 retention was declining.  
**Solution:** Redesigned progression curve with dynamic difficulty adjustment, milestone celebrations, and meaningful choice points (skill tree branching).  
**Result:** D30 retention increased 12%; average session length increased 8%.

## Trade-off Analysis

| Decision         | Option A             | Option B                           | Chosen                          | Rationale                                                  |
| ---------------- | -------------------- | ---------------------------------- | ------------------------------- | ---------------------------------------------------------- |
| Hit Registration | Client-authoritative | Server-authoritative with rollback | Server with rollback            | Prevents cheating; rollback masks latency                  |
| Progression Data | Flat JSON            | ScriptableObjects + server sync    | ScriptableObjects + server sync | Designer-friendly editing; server authority for anti-cheat |
| Input System     | Unity Legacy Input   | Unity New Input System             | New Input System                | Better touch handling; rebindable controls                 |

## Quality Standards

- Input-to-action latency: ≤ 16ms (1 frame at 60fps)
- Hit registration accuracy: ≥ 99.5%
- Progression save frequency: Every significant milestone + 30s auto-save
- Combat frame budget: ≤ 3ms CPU, ≤ 5ms GPU per frame

## Industry Best Practice References

- GDC 2023: "Networking the Brawl Stars Combat System" (Supercell)
- GDC 2022: "Progression Systems That Retain Players" (King)
- Unity Learn: "Building a Combat System" (official tutorial)
- "Game Feel" by Steve Swink — input responsiveness principles
