---
name: agile-production
description: Agile production coordination for game development, including sprint planning, task tracking, meeting facilitation, and Jira workflow management.
version: "1.0.0"
---

# Agile Production

## Overview

This skill covers agile production coordination for game development teams, adapting Scrum and Kanban methodologies to the creative and iterative nature of game development.

## Tools & Platforms

| Tool             | Purpose                                      |
| ---------------- | -------------------------------------------- |
| Jira             | Sprint planning, task tracking, backlog mgmt |
| Confluence       | Documentation, meeting notes, wikis          |
| Google Workspace | Status reports, stakeholder communication    |
| Miro             | Sprint retrospectives, brainstorming         |

## Sprint Cadence

| Event           | Duration   | Frequency     | Purpose                              |
| --------------- | ---------- | ------------- | ------------------------------------ |
| Sprint Planning | 2 hours    | Every 2 weeks | Commit to sprint goals, assign tasks |
| Daily Standup   | 15 minutes | Daily         | Sync on progress, surface blockers   |
| Sprint Review   | 1 hour     | Every 2 weeks | Demo completed work, gather feedback |
| Retrospective   | 1 hour     | Every 2 weeks | Process improvement, team health     |

## Task Prioritization Framework

| Priority | Criteria                                  | Response Time |
| -------- | ----------------------------------------- | ------------- |
| P0       | Blocks release, critical bug, showstopper | Same day      |
| P1       | Blocks feature development, major scope   | This sprint   |
| P2       | Important but not blocking                | Next sprint   |
| P3       | Nice-to-have, polish                      | Backlog       |

## Key Metrics

| Metric             | Target                 | Measurement                 |
| ------------------ | ---------------------- | --------------------------- |
| Sprint completion  | ≥ 85%                  | Completed / committed       |
| Velocity stability | ± 15% sprint-to-sprint | Story points delivered      |
| Blocker resolution | < 2 days avg           | Time from flagged to clear  |
| Meeting efficiency | ≤ scheduled time       | Actual vs. planned duration |

## Game-Development Sprint Structure

Casual game development sprints have unique characteristics compared to product or enterprise engineering sprints. Lena adapts standard Scrum to account for these realities:

### Discipline-Specific Velocity Calibration

Art, engineering, design, and audio all have different task granularity. Lena maintains separate velocity baselines per discipline:

| Discipline  | Typical Task Unit                                     | Story Points  | Notes                                                     |
| ----------- | ----------------------------------------------------- | ------------- | --------------------------------------------------------- |
| Engineering | Feature implementation, bug fix                       | 1–8           | Well-defined scope; points map reliably to days           |
| Art         | Asset delivery (concept, model, texture, integration) | 2–5 per asset | High variability based on asset complexity                |
| Design      | Mechanic spec, level design, playtest                 | 3–8           | Design tasks often generate more design work after review |
| Audio       | Composition, SFX design, integration                  | 3–8           | Blocked by engineering integration readiness              |

Lena tracks velocity by discipline so capacity planning accurately reflects the real constraint — usually Art or Engineering during full production.

### Pipeline Stage → Sprint Mapping

Each studio pipeline stage spans multiple sprints. Lena maps the current stage to sprint goals:

| Pipeline Stage                | Sprint Focus                                     | Lena's Role                                                                                  |
| ----------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| Stage 2 (Prototype)           | Core mechanic playable; art placeholder only     | Track eng + design sprint; escalate art delays that would block prototype demo               |
| Stage 3 (Vertical Slice)      | Feature-complete slice; shippable visual quality | Cross-discipline dependency tracking critical; art and engineering must sync weekly          |
| Stage 4 (Production Planning) | Gantt finalized; team allocated                  | Supports EP in translating plan into sprint structure; initializes Jira epic/story hierarchy |
| Stage 5 (Full Production)     | Feature development; content production          | Full sprint cadence; weekly burndown to EP; flag velocity deviations weekly                  |
| Stage 6 (Automated Testing)   | Bug triage; test suite completion                | Manage bug backlog in Jira; track P0/P1 resolution daily; coordinate retests                 |
| Stage 7–8 (Soft Launch)       | Monitor, tune, communicate                       | Daily KPI check with EP; support data-driven tuning sprint                                   |

### Sprint Planning Anti-Patterns

Lena proactively prevents these common failure modes:

| Anti-Pattern                                  | Detection                                                               | Response                                                                |
| --------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Over-commitment (team commits >110% capacity) | Sprint planning produces more points than last sprint's velocity allows | Remove lowest-priority items; protect 20% buffer for unplanned work     |
| Vague art tasks ("work on character")         | No clear Definition of Done in the story                                | Reject story at planning; ask artist to define the specific deliverable |
| Undisclosed cross-team dependency             | Story needs input from another discipline but dependency not noted      | Add dependency label in Jira; flag in next cross-discipline sync        |
| "It's almost done" persistence                | Same story in "In Progress" for 3+ days without movement                | Daily check-in with assignee; escalate to EP if blocked for >2 days     |

## Production Runbook

Common situations and how Lena handles them:

### Situation: Milestone at Risk (>20% overrun signal)

Per AGENTS.md §8.4, any task or sprint exceeding its estimate by >20% triggers notification to the Studio Director and user.

1. Lena detects the signal (velocity drop, accumulated blockers, or explicit team feedback) at the sprint review
2. Within 24 hours, Lena prepares a **1-page milestone risk brief** for the Executive Producer (James Okonkwo):
   ```
   Milestone Risk Brief — [Stage X, Sprint N]
   Trigger: [velocity at X points/sprint vs. Y committed; N sprints remain; shortfall = Z points]
   Root cause: [specific — e.g., "art blocked on concept approval for 2 sprints"]
   Options:
   1. Reduce scope: [list features that could defer]
   2. Add resource: [what type, estimated cost]
   3. Extend timeline: [by how many weeks]
   Lena's recommendation: [Option N — brief rationale]
   ```
3. EP reviews and presents options to Studio Director. Studio Director decides and notifies user if schedule impact exceeds the >20% threshold.

### Situation: Cross-Discipline Dependency Blocked

When Engineering finishes a feature but Art is not ready to integrate, or Design changes a spec mid-sprint:

1. Detect: Lena monitors the Jira dependency map; any story where "blocked-by" status changes is flagged in the daily standup
2. Escalate: If blocked for >2 days, Lena schedules a 30-minute sync between the two discipline leads
3. Resolve: Both leads agree on a resolution path and updated ETA; Lena documents in the Jira story and the sprint standup notes
4. If unresolved after sync: Escalate to EP for cross-discipline arbitration

## Quality Standards

- Sprint planning produces a sprint backlog that fits within 90% of the team's trailing velocity
- Every Jira story has a Definition of Done before entering a sprint
- Blockers flagged and assigned an owner within 24 hours of detection
- Milestone risk brief delivered to EP within 24 hours of detecting a >20% overrun signal
- Sprint retrospective action items documented in Confluence and tracked to resolution
