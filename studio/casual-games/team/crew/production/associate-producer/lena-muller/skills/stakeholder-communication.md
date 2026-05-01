---
name: stakeholder-communication
description: Status reporting, risk communication, and cross-team coordination for game production stakeholders.
version: "1.0.0"
---

# Stakeholder Communication

## Overview

This skill covers effective communication with game development stakeholders across all levels — from individual contributors to studio leadership — ensuring transparency, alignment, and timely escalation of issues.

## Communication Matrix

| Audience           | Channel        | Frequency     | Content                              |
| ------------------ | -------------- | ------------- | ------------------------------------ |
| Team members       | Daily standup  | Daily         | Progress, blockers, next steps       |
| Discipline leads   | Lead sync      | Weekly        | Cross-team dependencies, risks       |
| Producer           | 1:1            | Weekly        | Sprint health, resource needs        |
| Studio leadership  | Status report  | Bi-weekly     | Milestone progress, budget, risks    |
| Publisher/External | Review meeting | Per milestone | Deliverable status, launch readiness |

## Status Report Template

```
PROJECT STATUS REPORT — [Date]
=============================
Overall Status: 🟢 On Track / 🟡 At Risk / 🔴 Off Track

KEY ACCOMPLISHMENTS (this period):
- [Completed items with measurable outcomes]

UPCOMING PRIORITIES (next period):
- [Planned work with dependencies noted]

BLOCKERS & RISKS:
- [Blocker]: Description, owner, ETA for resolution
- [Risk]: Description, probability, impact, mitigation plan

METRICS:
- Sprint completion: X%
- Open blockers: X
- Open risks: X
- Budget burn: X% of planned
```

## Risk Communication Protocol

| Risk Level | Probability × Impact | Notification             | Action                    |
| ---------- | -------------------- | ------------------------ | ------------------------- |
| Low        | 1–3                  | Documented in risk log   | Monitor                   |
| Medium     | 4–6                  | Weekly status report     | Mitigation plan required  |
| High       | 8–12                 | Immediate escalation     | Contingency plan required |
| Critical   | 15–25                | Studio Director notified | Emergency response        |

## Communicating Bad News

The most critical stakeholder communication skill is delivering bad news early, clearly, and with options. Lena follows the **Problem–Impact–Options–Ask** structure:

```
PROBLEM: [What is happening, stated factually — no hedging]
Example: "Art velocity has been 40% below plan for 3 consecutive sprints."

IMPACT: [What happens if nothing changes — specific and quantified]
Example: "At current pace, we will miss the Stage 3 gate by 3 weeks."

OPTIONS: [2–3 concrete paths forward — not just "we need to figure this out"]
Example:
  Option A: Reduce scope — defer the boss character art to Stage 5. Saves 2 sprints.
  Option B: Add contract artist — brings in 1 freelance concept artist for 4 weeks.
  Option C: Extend Stage 3 — accept the 3-week slip; no scope change.

ASK: [What decision is needed from this stakeholder, by when]
Example: "Please decide by end-of-week which option to pursue so we can replanning
in the next sprint planning session."
```

**Rule:** Never communicate a problem without options. Bringing a problem without a path forward forces the stakeholder to do the analysis work Lena should have done.

## Pipeline Stage Communication Responsibilities

Lena supports the EP in communications at each pipeline stage. Her specific responsibilities:

| Stage                         | Lena's Communication Responsibilities                                                                             |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Stage 2 (Prototype)           | Weekly progress note to EP; flag any core mechanic uncertainties before prototype demo                            |
| Stage 3 (Vertical Slice)      | Cross-discipline dependency report to EP weekly; attend user review with EP and take notes                        |
| Stage 4 (Production Planning) | Distribute production plan to all discipline leads; confirm receipt and acknowledge; log any lead concerns        |
| Stage 5 (Full Production)     | Weekly burndown report to EP; daily P0/P1 bug status during crunch periods                                        |
| Stage 6 (Automated Testing)   | Bug triage communication to discipline leads (who owns which fix, by when); daily test results distribution       |
| Stage 7 (Soft Launch Prep)    | Soft launch checklist status to EP; external stakeholder (publisher) communications drafted by Lena, signed by EP |
| Stage 8 (Soft Launch)         | Daily KPI distribution to studio leadership; weekly soft launch status report to EP                               |

## Documentation Standards

Lena owns the production documentation trail — the record that proves decisions were made, communicated, and tracked:

| Document                               | Owner                          | Where                                | Update Frequency                     |
| -------------------------------------- | ------------------------------ | ------------------------------------ | ------------------------------------ |
| Sprint notes (planning, review, retro) | Lena                           | Confluence — Production Sprint Notes | After every ceremony                 |
| Blocker log                            | Lena                           | Jira — Production blockers filter    | Daily during active sprints          |
| Risk register                          | Lena (updates) + EP (owns)     | Confluence — Risk Register           | Weekly or on new risk identification |
| Milestone status (progress.md)         | Lena (writes) + EP (signs off) | Project folder — `progress.md`       | After every sprint review            |

The `progress.md`, `session-log.md`, and `checkpoint.json` files required by the studio pipeline Progress Sync Protocol are Lena's direct responsibility to keep current. The EP reviews and approves, but the daily operational maintenance is Lena's.

## Quality Standards

- Bad news communicated with Problem–Impact–Options–Ask format every time — no raw problem dumps
- Status report delivered before the scheduled stakeholder review, never after
- All meeting notes published to Confluence within 24 hours of the meeting
- `progress.md` updated within 4 hours of every sprint review
- Blocker log reviewed and updated daily during Stage 5 and Stage 6
