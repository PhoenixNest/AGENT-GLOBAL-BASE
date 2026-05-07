---
name: production-management
description: Production planning, schedule management, resource allocation, Agile/Scrum execution, and cross-team dependency management across Stages 4, 5, 6, 7, and 9 of the game development pipeline.
version: "1.0.0"
---

# Production Management

## Role

The Executive Producer translates creative vision into executable production plans. This skill covers end-to-end production management — from Production Planning (Stage 4) through Global Launch Readiness (Stage 9) — ensuring the studio delivers quality game content on schedule and within budget.

## Pipeline Stage Ownership

| Stage | Name                    | Responsibility                                                                                        |
| ----- | ----------------------- | ----------------------------------------------------------------------------------------------------- |
| 4     | Production Planning     | Owns the production plan, Gantt chart, resource allocation, and technical architecture coordination   |
| 5     | Full Production         | Tracks development progress, manages capacity allocation, resolves cross-team blockers                |
| 6     | Automated Testing       | Coordinates testing schedule, ensures test environment readiness, tracks defect resolution            |
| 7     | Soft Launch Prep        | Manages analytics instrumentation schedule, store asset production, localization handoff coordination |
| 9     | Global Launch Readiness | Owns the launch readiness checklist, coordinates final go/no-go preparation across all divisions      |

## Execution Guidance

### Production Planning (Stage 4)

The Production Plan must include:

1. **Detailed task breakdown** — Every deliverable from the GDD decomposed into tasks with estimates
2. **Gantt chart** — Visual timeline with dependencies, milestones, and critical path identified
3. **Resource allocation** — Each team member assigned to specific tasks with capacity percentages
4. **Risk register** — Top 10 schedule risks with probability, impact, and mitigation plans
5. **Budget forecast** — Monthly burn rate projection with contingency allocation

### Capacity Allocation Model (60/25/15)

| Bucket                | Allocation | Purpose                                                    | Management Approach                                 |
| --------------------- | ---------- | ---------------------------------------------------------- | --------------------------------------------------- |
| **Core Production**   | 60%        | Committed roadmap — planned features, content, systems     | Locked 2 sprints ahead, changes require EP approval |
| **Live Ops**          | 25%        | Ongoing live game costs — bugs, events, community response | Flexible, managed week-to-week                      |
| **Innovation Buffer** | 15%        | Unallocated capacity for opportunities and emergencies     | Held by EP, re-allocated as needed                  |

**Key Rule:** The innovation buffer exists so the studio doesn't have to choose between "ship late" and "cut scope" every time something unexpected happens. Never commit the buffer to the roadmap.

### Dependency Mapping Matrix

Every sprint, maintain a dependency map across all teams:

| From Team   | Deliverable      | To Team     | Required By | Status | Owner          |
| ----------- | ---------------- | ----------- | ----------- | ------ | -------------- |
| Art         | Character models | Animation   | Sprint 14   | 🟢     | Art Director   |
| Design      | Level layouts    | Engineering | Sprint 15   | 🟡     | Level Designer |
| Engineering | API endpoints    | QA          | Sprint 16   | 🔴     | Backend Lead   |

**Status colors:**

- 🟢 Green — On track, no risk
- 🟡 Yellow — At risk (estimate may slip, quality concern)
- 🔴 Red — Blocked (cannot proceed without resolution)

**Monday dependency review:** Walk through all red and yellow items with relevant leads. Assign single owner to every dependency. Escalate to Studio Director if red dependency cannot be resolved within 48 hours.

### Agile/Scrum Execution

| Ceremony             | Frequency | Duration | Participants   | Purpose                                    |
| -------------------- | --------- | -------- | -------------- | ------------------------------------------ |
| Sprint Planning      | Bi-weekly | 90 min   | All teams      | Commit to next sprint deliverables         |
| Daily Standup        | Daily     | 15 min   | Per discipline | Blocker identification, progress sync      |
| Sprint Review        | Bi-weekly | 60 min   | All studio     | Demo completed work, gather feedback       |
| Sprint Retrospective | Bi-weekly | 45 min   | Per discipline | Process improvement identification         |
| Cross-Team Sync      | Bi-weekly | 45 min   | Team leads     | Dependency review, cross-team coordination |

### Progress Tracking

- **Weekly status report** to Studio Director: Completed tasks, upcoming milestones, risks, budget status
- **Schedule variance tracking:** Any task exceeding estimated duration by >20% triggers Progress Sync Protocol notification to Studio Director and User
- **Burndown charts** per team — reviewed at every sprint review
- **Critical path monitoring** — any delay on critical path is immediately escalated

### Cross-Team Coordination

- **Communication cadence:** Daily standups within disciplines, bi-weekly cross-discipline syncs, monthly all-studio playtests
- **Escalation path:** Team member → Team Lead → Executive Producer → Studio Director → User
- **Conflict resolution:** Use "trade-off visibility" approach — present options with consequences, let decision-makers choose with full information
- **Meeting hygiene:** Every meeting has an agenda, timebox, and action items. No meetings without all three.

## References

- `company/pipeline/mobile-development/pipeline.md` — Parent company pipeline definitions
- `company/pipeline/mobile-development/monitoring.md` — Progress Monitoring & Recovery System
