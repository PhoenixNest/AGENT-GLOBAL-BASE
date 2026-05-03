---
name: studio-engineering-ai-behavior-programming
description: AI behavior system design and implementation — behavior trees, utility AI, finite state machines, navigation/pathfinding optimization for mobile games. Owned by Kaelen Reeves (Senior Gameplay Engineer). Use during Studio Pipeline Stages 2–5 for AI system development and Stage 6 (Automated Testing) for AI behavior validation. Trigger: AI behavior, behavior trees, utility AI, pathfinding, NavMesh, enemy AI.
version: "1.0.0"
---

# AI Behavior Programming

**Skill Owner:** Kaelen Reeves
**Version:** 1.0 | **Date:** 2026-04-20

---

## Description

Design and implementation of AI behavior systems for mobile games including behavior trees, utility AI, finite state machines, and navigation/pathfinding optimization.

## Tools & Frameworks

| Tool/Framework                   | Version  | Context                                                 |
| -------------------------------- | -------- | ------------------------------------------------------- |
| Unity Behavior Designer          | 1.6.x    | Visual behavior tree editor; extended with custom nodes |
| Unity NavMesh                    | 2023 LTS | Runtime navmesh baking; dynamic obstacle avoidance      |
| C#                               | 11.0     | AI logic, utility scoring, state machine implementation |
| Unity AI Utilities (open-source) | 2024     | Contributed pathfinding optimization module             |

## Production Scenarios

### Scenario 1: Boss AI Behavior Tree (Brawl Stars, Supercell 2023)

**Problem:** Boss AI felt predictable and exploitable by players.  
**Solution:** Implemented hierarchical behavior tree with utility-based leaf selection; added randomness with weighted decision trees; integrated perception system for player awareness.  
**Result:** Boss fight win rate stabilized at 35% (target); player engagement with boss mode increased 28%.

### Scenario 2: Pathfinding Optimization (Supercell 2024)

**Problem:** Pathfinding consumed 12% of CPU budget on crowded maps.  
**Solution:** Implemented hierarchical pathfinding with caching; reduced recalculation frequency; used flow fields for group movement.  
**Result:** Pathfinding CPU reduced from 12% to 3%; server compute savings $1.8M/yr.

## Trade-off Analysis

| Decision          | Option A      | Option B                  | Chosen                        | Rationale                                        |
| ----------------- | ------------- | ------------------------- | ----------------------------- | ------------------------------------------------ |
| AI Architecture   | Behavior Tree | Utility AI                | Hybrid (BT + utility leaves)  | BT for structure; utility for flexibility        |
| Pathfinding       | A\* per unit  | Flow field + caching      | Flow field + hierarchical A\* | Better for groups; caching reduces recalculation |
| Perception System | Raycasting    | Trigger zones + LOS cache | Trigger zones + cache         | Lower CPU cost; sufficient accuracy for mobile   |

## Quality Standards

- AI decision latency: ≤ 1 frame (16ms at 60fps)
- Pathfinding CPU budget: ≤ 3% of total frame time
- Behavior tree depth: ≤ 5 levels (maintainability)
- Utility function evaluation: ≤ 0.5ms per AI agent

## Industry Best Practice References

- "Behavior Trees in Game AI" (GDC 2021, Bungie)
- "Utility AI: Theory and Practice" (GDC 2022, EA)
- "Hierarchical Pathfinding in Real-Time Games" (AI Game Programming Wisdom)
- Unity ML-Agents documentation (for hybrid AI/ML approaches)
