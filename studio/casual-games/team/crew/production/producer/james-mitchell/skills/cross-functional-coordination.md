---
name: studio-production-cross-functional-coordination
description: Cross-functional coordination for multi-discipline game production teams — dependency management, blocker resolution, stakeholder communication, and sprint facilitation across engineering, art, design, audio, and live-ops disciplines. Owned by James Mitchell (Producer). Trigger: cross-functional coordination, inter-team dependency, stakeholder communication, blocker resolution, sprint facilitation.
version: "1.0.0"
---

# Cross-Functional Coordination

**Skill Owner:** James Mitchell (Producer)
**Applies To:** All Studio Disciplines, Stage 1–10 Cross-Team Dependencies

## Dependency Mapping

At the start of each sprint, James produces a **dependency map** — a visual board (Confluence page or Jira Epic link view) showing which stories are blocked on deliverables from other disciplines:

```
Design (Mei)          Art (Renaud)         Audio (Hiroshi)       Engineering (Dmitri)
   │                      │                      │                      │
   │ GDD section          │ Asset X               │ SFX set Y           │ API Z
   │ approved? ──────────►│ (need spec first)     │ (need level first)  │ (need schema first)
   │                      │                       │                      │
   └──────────────────────┴───────────────────────┴──────────────────────►
                                  Sprint Goal
```

Any dependency with no clear owner or unclear handoff date gets a **BLOCKED** status and same-day attention from James.

## Standing Meeting Cadence

| Meeting              | Cadence       | Attendees                                        | Purpose                                           |
| -------------------- | ------------- | ------------------------------------------------ | ------------------------------------------------- |
| Daily standup        | Every day     | All disciplines (10 min max)                     | Surface blockers; status in 3 sentences each      |
| Sprint planning      | Every 2 weeks | All leads + James Okonkwo (EP)                   | Commit to sprint goal; assign stories             |
| Sprint review        | Every 2 weeks | All leads + Studio Director (milestone stages)   | Demo completed work; confirm stage gate readiness |
| Sprint retrospective | Every 2 weeks | All leads + Producer                             | Improve process; action items with owners         |
| Stakeholder update   | Weekly        | James Okonkwo (EP) + Studio Director (milestone) | Milestone progress; risk summary                  |

## Blocker Resolution Protocol

A **blocker** is any dependency that stops a team member from completing a sprint story:

1. Team member flags blocker in standup and adds `BLOCKED` label to Jira ticket within same hour
2. James triages within 2 hours: is the blocker resolvable within the sprint?
   - **Yes:** James coordinates the resolution directly, scheduling a 30-min call with the two parties involved
   - **No:** James escalates to Dmitri (technical) or Renaud/Mei (creative) and updates the sprint plan
3. If the blocker threatens the sprint goal, James notifies James Okonkwo (EP) before the end of the business day
4. All resolved blockers are documented in the sprint log with: root cause, resolution, and prevention action

## Communication Standards

| Stakeholder        | Channel    | Frequency      | Format                                                 |
| ------------------ | ---------- | -------------- | ------------------------------------------------------ |
| Engineering team   | Jira       | Real-time      | Story status updates; blocker flags                    |
| All disciplines    | Slack      | Daily          | Standup summary; action items                          |
| Executive Producer | Confluence | Weekly         | 1-page status report: progress, risks, next milestones |
| Studio Director    | 1:1        | At stage gates | Gate readiness briefing                                |

## Real-World Production Scenario

### Scenario: Cascading Dependency Failure

**Context:** Art team is blocked on an environment asset waiting for the final level design spec (Mei). Design team is blocked on design spec pending a technical feasibility answer from engineering (Dmitri). Dmitri's team is in the middle of a critical bug fix sprint and unavailable for spec work.

**Process:**

1. James maps the dependency chain in a 15-minute session: Design → Art → Level Integration
2. Identifies the root constraint: Engineering is the critical path bottleneck
3. Negotiates with Dmitri: can a 2-hour feasibility spike be carved out without jeopardizing the bug fix sprint?
4. If yes: spike is added to sprint; dependency unblocked
5. If no: James escalates to James Okonkwo; options are (a) delay the level's sprint entry, or (b) bring in contract support
6. Art team is given interim work (non-blocked assets) to maintain velocity during the resolution window
7. Full resolution and root cause documented in Confluence

## Measurable Quality Standards

| Standard                         | Target                         | Measurement Method      |
| -------------------------------- | ------------------------------ | ----------------------- |
| Blocker resolution time          | ≤1 business day                | Jira BLOCKED ticket age |
| Sprint goal achievement rate     | ≥80% of committed stories      | Jira sprint report      |
| Cross-discipline dependency gaps | 0 undocumented at sprint start | Dependency map review   |
| Stakeholder update cadence       | 100% weekly on time            | Confluence page history |
