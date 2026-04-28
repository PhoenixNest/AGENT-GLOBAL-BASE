---
name: studio-engineering-gameplay-scripting-testing
description: C# gameplay scripting for Unity — feature implementation workflows, debugging techniques, unit testing for gameplay systems, tournament matchmaking. Owned by Sofia Martinez (Gameplay Engineer). Use during Studio Pipeline Stages 2–5 for gameplay feature development and Stage 6 (Automated Testing) for gameplay unit testing. Trigger: gameplay scripting, C# Unity, unit testing, feature implementation, matchmaking, gameplay debugging.
version: "1.0.0"
---

# Gameplay Scripting & Testing

**Skill Owner:** Sofia Martinez | **Version:** 1.0 | **Date:** 2026-04-20

## Description

C# gameplay scripting for Unity, feature implementation workflows, debugging techniques, and unit testing for gameplay systems.

## Tools & Frameworks

| Tool                 | Version  | Context                                  |
| -------------------- | -------- | ---------------------------------------- |
| Unity                | 2023 LTS | Primary game engine                      |
| C#                   | 11.0     | Gameplay scripting language              |
| NUnit                | 3.13     | Unit testing framework                   |
| Unity Test Framework | 2023 LTS | Integration testing in Unity             |
| Git                  | 2.40     | Version control; feature branch workflow |

## Production Scenarios

**Scenario 1: Tournament Matchmaking (Playdemic 2024)** — Implemented tournament matchmaking logic for Golf Clash handling 100K+ concurrent players. Result: Match find time < 15s; fair skill-based matching.
**Scenario 2: Gameplay Unit Testing Framework (Playdemic 2024)** — Introduced unit testing for gameplay systems. Result: Gameplay bug count reduced 40%; regression catch rate 85%.

## Trade-offs

- Manual vs automated testing → automated for core systems; manual for feel
- TDD vs test-after → test-after for rapid prototyping; TDD for stable systems

## Quality Standards

- Unit test coverage: ≥ 80% for gameplay logic
- PR first-pass acceptance: ≥ 95%
- Bug fix turnaround: ≤ 2 days for P1 bugs
- Code review participation: ≥ 2 reviews/week

## References

Unity Testing documentation; "Unit Testing Principles" (Vershyn); Playdemic engineering blog
