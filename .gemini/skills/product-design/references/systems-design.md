---
name: studio-creative-design-systems-design
description: Game systems design for F2P mobile games — core loop architecture, progression systems, feedback systems, and systemic player engagement design. Owned by Lisa Henderson (Senior Game Designer). Use during Studio Pipeline Stages 1–5 for system architecture and progression balancing. Trigger: system design, core loop, progression system, feedback loop, game systems, F2P mechanics.
version: "1.0.0"
---

# Systems Design

**Skill ID:** systems-design
**Role:** Senior Game Designer
**Seniority:** Senior

## Overview

Game systems design — core loop architecture, progression systems, feedback systems, and systemic player engagement design for F2P mobile games.

## Tools & Frameworks

| Tool                | Proficiency  | Use Case                                   |
| ------------------- | ------------ | ------------------------------------------ |
| Excel/Google Sheets | Expert       | Economy modeling, progression curves       |
| Miro/FigJam         | Expert       | System flow diagrams, relationship mapping |
| Unity               | Intermediate | System prototyping and tuning              |
| Amplitude/Mixpanel  | Intermediate | Data-driven system iteration               |

## Scenarios & Trade-offs

### Scenario 1: Core Loop Design for Casual Puzzle Game

- **Approach:** Design 3-loop system — micro loop (single puzzle, 30s), meta loop (level progression, 30min), macro loop (event participation, 1 week)
- **Trade-off:** Loop complexity vs. accessibility — more loops create depth but may overwhelm casual players
- **Quality Bar:** Each loop is independently understandable; loops reinforce each other; clear progression at every timescale

### Scenario 2: Progression System Balancing

- **Approach:** Model progression curves mathematically, validate with player data, iterate based on retention metrics
- **Trade-off:** Challenge vs. frustration — too easy = boring, too hard = churn
- **Quality Bar:** D1 retention ≥ 40%, D7 ≥ 20%; progression feels meaningful at every milestone

## Quality Standards

- All systems documented with flow diagrams, input/output definitions, and edge cases
- Progression curves mathematically modeled before implementation
- Systems designed with telemetry in mind — every meaningful player action tracked
- System interactions mapped to identify potential exploits or unintended consequences

## Industry References

- Playrix's Gardenscapes progression system design
- King's Candy Crush meta-progression architecture
- F2P mobile game economy design best practices
