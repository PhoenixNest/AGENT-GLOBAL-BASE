---
name: studio-production-agile-production
description: Agile production management for game development — sprint planning, Scrum execution, milestone tracking, risk management, and cross-functional team coordination. Owned by James Mitchell (Producer). Use during Studio Pipeline Stages 4–10 for production management and sprint execution. Trigger: agile production, sprint planning, Scrum, milestone tracking, risk management, Jira, velocity tracking, game production.
version: "1.0.0"
---

# Agile Production

**Skill Owner:** James Mitchell (Producer)
**Applies To:** Sprint Planning, Agile/Scrum Execution, Milestone Tracking, Risk Management

## Tools & Frameworks

| Tool/Framework | Version Context | Usage                                        |
| -------------- | --------------- | -------------------------------------------- |
| Jira           | Latest (Cloud)  | Sprint planning, backlog management          |
| Confluence     | Latest          | Documentation, meeting notes, retrospectives |
| Miro           | Latest          | Sprint planning boards, retrospectives       |
| Slack          | Latest          | Daily standups, team communication           |
| Google Sheets  | Latest          | Burndown charts, velocity tracking           |
| Unity DevOps   | Latest          | Build tracking, release management           |

## Real-World Production Scenarios

### Scenario 1: Setting Up Agile Process for a New Game Studio

**Context:** New team with no existing process.
**Process:**

1. Define sprint cadence: 2-week sprints with Monday planning, Friday review
2. Set up Jira: project boards, issue types, workflows, custom fields for game dev
3. Establish ceremonies: daily standup (15 min), sprint planning (2 hours), sprint review (1 hour), retrospective (1 hour)
4. Define team capacity: account for holidays, meetings, and non-project work
5. Create backlog: epics → features → user stories → tasks with story point estimation
6. Track velocity: measure completed story points per sprint, adjust capacity accordingly
7. Results: predictable sprint delivery, 25% cycle time reduction

### Scenario 2: Managing a Cross-Functional Game Development Team

**Context:** Team of 15-20 across engineering, art, design, and QA.
**Process:**

1. Define cross-functional sprint goals: each sprint delivers a vertical slice of functionality
2. Coordinate dependencies: engineering blocks → art blocks → QA blocks
3. Manage risks: identify blockers early, escalate to Studio Director when needed
4. Track milestones: Gantt chart with critical path, weekly progress updates
5. Run playtests: schedule regular playtests with target audience, collect feedback
6. Results: on-time delivery of vertical slice, predictable milestone progression

## Trade-Off Analysis

| Decision          | Option A                   | Option B                   | Trade-Off                                                                                                         |
| ----------------- | -------------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Sprint Length     | 1-week sprints             | 2-week sprints             | 1-week = faster feedback but more overhead; 2-week = more stable but slower iteration                             |
| Estimation Method | Story points               | Time-based estimates       | Story points = relative, team-consistent; Time = absolute but varies by individual                                |
| Scope Management  | Fixed scope, flexible time | Fixed time, flexible scope | Fixed scope = predictable deliverables but risk of delays; Fixed time = predictable schedule but scope may be cut |

## Measurable Quality Standards

| Standard                   | Target                          | Measurement Method                |
| -------------------------- | ------------------------------- | --------------------------------- |
| Sprint Completion Rate     | ≥ 90% of committed story points | Jira sprint reports               |
| Velocity Stability         | ± 15% variation                 | Velocity tracking over 5+ sprints |
| Cycle Time                 | ≤ 5 days per story              | Jira cycle time report            |
| Milestone On-Time Delivery | ≥ 95%                           | Gantt chart tracking              |
| Team Satisfaction          | ≥ 4.0/5.0                       | Sprint retrospective surveys      |

## Industry Best Practice References

- **Scrum Guide 2020** — Official Scrum framework
- **Playdemic Agile Process** — Industry-standard game development Agile
- **Atlassian Agile Best Practices** — Jira/Confluence best practices
- **"Agile Game Development with Scrum" by Clinton Keith** — Game-specific Agile guide
