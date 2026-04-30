---
name: studio-creative-design-playtesting
description: Playtest facilitation and data-driven level tuning — test design, player observation, data collection, and iterative level improvement. Owned by Marcus Thompson (Level Designer). Use during Studio Pipeline Stages 2–6 for playtest execution and level tuning. Trigger: playtesting, level tuning, player testing, telemetry analysis, completion rate, playtest protocol, data-driven design.
version: "1.0.0"
---

# Playtesting

**Skill ID:** playtesting
**Role:** Level Designer
**Seniority:** Senior

## Overview

Playtest facilitation and data-driven level tuning — test design, player observation, data collection, and iterative level improvement.

## Tools & Frameworks

| Tool                | Proficiency | Use Case                                     |
| ------------------- | ----------- | -------------------------------------------- |
| Unity Remote        | Expert      | Real-time playtesting on target devices      |
| Analytics platforms | Expert      | Player behavior tracking, heatmap generation |
| Survey tools        | Advanced    | Player feedback collection                   |
| Video analysis      | Advanced    | Session recording and review                 |

## Scenarios & Trade-offs

### Scenario 1: Level Tuning Framework

- **Approach:** Structured playtesting pipeline — internal test (day 1), small external test (day 3), data analysis (day 5), iteration (day 7)
- **Trade-off:** Speed vs. thoroughness — faster tuning risks missing issues, slower tuning delays production
- **Quality Bar:** Each level tested with ≥ 50 players before approval; completion rate within target range (60–80%)

### Scenario 2: Identifying Level Design Issues from Data

- **Approach:** Analyze telemetry data (completion rate, retry count, exit points, time spent) to identify problematic levels and specific pain points
- **Trade-off:** Data-driven vs. intuition — data shows what's happening but not always why
- **Quality Bar:** Problematic levels identified within 48 hours of data availability; iteration reduces churn by ≥ 20%

## Quality Standards

- Playtest protocol documented and consistently followed
- Sample size: ≥ 50 players per level for quantitative data
- Qualitative feedback collected through surveys and observation
- Data analysis turnaround: ≤ 48 hours from test completion
- Iteration cycle: identify → hypothesize → implement → retest

## Mentorship and Knowledge Sharing

Marcus is the most senior level designer at the studio outside of the Lead Game Designer (Mei Watanabe). While he does not have direct reports, he is responsible for maintaining the studio's level design craft standards and onboarding any future level designers who join.

### Mentorship Responsibilities

| Activity                       | Who                                               | Cadence                              | Marcus's Role                                                                      |
| ------------------------------ | ------------------------------------------------- | ------------------------------------ | ---------------------------------------------------------------------------------- |
| Level design onboarding        | New level designers                               | During first month                   | Pair-work on first 3 levels; daily feedback sessions                               |
| Playtesting technique training | Any IC who facilitates playtests                  | On request                           | Walk through the playtest protocol; observe their first session and debrief        |
| Level design doc review        | Any designer producing level design documentation | Per PR/submission                    | Structured written feedback within 48 hours                                        |
| Level design post-mortems      | Whole studio                                      | After every Stage 3 (Vertical Slice) | Facilitates the level design post-mortem session; documents findings in Confluence |

### Knowledge Documentation

Marcus owns and maintains two studio-level documents:

1. **Level Design Principles Doc** — the studio's canonical reference for what makes a good casual game level. Updated after every new project's Stage 3. Lives at `studio/casual-games/projects/<game>/level-design-principles.md`.
2. **Playtest Protocol** — the documented playtest facilitation process used across all projects. Lives at `studio/casual-games/library/topics/playtesting-protocol.md`. Updated whenever the protocol improves based on experience.

### Level Design Feedback Standards

When giving feedback on another designer's level, Marcus uses the **Specific-Objective-Actionable** format:

- **Specific:** Cite the exact level section or mechanic (not "the middle section is confusing")
- **Objective:** Ground the feedback in player data or design principles (not "I don't like this")
- **Actionable:** Provide a concrete direction, not just a critique ("reduce the obstacle density in the 3rd row by 30% and measure completion rate improvement")

## Industry References

- King's playtesting framework (40% tuning time reduction)
- Playtest best practices from GDC talks
- Data-driven level design methodology
