---
name: studio-engineering-engineering-leadership
description: Engineering team leadership for game studios — hiring bar, sprint collaboration, technical mentorship, cross-functional communication, and engineering culture. Owned by Dmitri Volkov (Senior Game Engineer). Trigger: engineering team, tech lead, sprint planning, mentorship, engineering culture, team management, hiring technical staff.
version: "1.0.0"
---

# Engineering Leadership

**Skill Owner:** Dmitri Volkov (Senior Game Engineer)
**Applies To:** Team Leadership, Sprint Execution, Technical Mentorship, Cross-Functional Collaboration

## Real-World Production Scenarios

### Scenario 1: Onboarding a New Engineer to the Studio

**Context:** Senior Gameplay Engineer joins mid-production during Stage 5.
**Process:**

1. First week: pair the new engineer with an existing engineer on a bounded, well-specified task (a single feature or bugfix)
2. Share the architecture doc and system diagram for the area they'll own
3. Conduct a 1:1 code review on their first PR — focus on studio patterns, not just correctness
4. By end of week 2, the engineer should be closing tasks independently and attending sprint ceremonies
5. By end of week 4, they should be proposing solutions to technical problems, not just implementing specified ones

### Scenario 2: Running a Sprint Planning Session

**Context:** Two-week sprint; mixed team of engineers, a QA lead (Amara), and a producer (James Mitchell).
**Process:**

1. Before planning: review backlog in Jira; ensure all stories are estimated with T-shirt sizes (S/M/L/XL); anything XL must be split
2. Opening: Producer presents sprint goal aligned to the current pipeline stage and Gantt milestones
3. Engineering reviews capacity: identify who is on support rotation, who has PTO, who is ramping
4. Pull stories into sprint until capacity is 80% committed (20% buffer for bug fixes and blockers)
5. Flag technical risk immediately — if a story requires a new system, it gets a spike task added to the sprint to de-risk it
6. Close with a verbal sprint goal the whole team can repeat back without notes

### Scenario 3: Handling an Engineering Blocker Escalation

**Context:** A gameplay engineer is blocked for >1 day on an integration issue with the backend team.
**Process:**

1. Dmitri conducts a 30-minute "unblocking session" with the blocked engineer
2. If unresolvable at the engineering level, escalate synchronously to the relevant lead (Backend Lead or Senior Backend Engineer)
3. If the blocker will impact the sprint goal, notify the Producer (James Mitchell) within the same day — never let a blocker slip silently past a sprint day boundary
4. Document the root cause and resolution in the sprint retrospective as a process improvement item

## Engineering Culture Standards

| Principle                 | What It Means in Practice                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| Psychological safety      | Engineers voice concerns in retros without attribution. No "shoot the messenger" responses to bad news.  |
| Technical decision-making | Architecture decisions documented in ADRs; no significant design choices made verbally without a record. |
| Knowledge sharing         | Every major system has an author responsible for a 20-minute "tech talk" before Stage 5 begins.          |
| Failure culture           | Post-mortems are blameless. The goal is systemic improvement, not individual accountability.             |
| Mentorship obligation     | All L3+ engineers are expected to mentor at least one L1/L2 engineer per cycle.                          |

## Measurable Quality Standards

| Standard                      | Target                             | Measurement Method        |
| ----------------------------- | ---------------------------------- | ------------------------- |
| Sprint velocity variance      | ≤15% between sprints               | Jira velocity chart       |
| Blocker resolution time       | ≤1 business day                    | Jira blocker ticket aging |
| Code review turnaround        | ≤24 hours from PR open             | GitHub PR metrics         |
| Production bug rate reduction | ≥30% vs. previous project baseline | Post-launch defect log    |
| Engineering team satisfaction | ≥4.2/5 in quarterly survey         | Anonymous team survey     |

## Industry Best Practice References

- **"An Elegant Puzzle" — Will Larson** — Engineering management patterns for leads
- **"The Pragmatic Programmer"** — Engineering craft standards Dmitri reinforces in code review
- **GDC Vault — Engineering Track** — Game-specific engineering leadership patterns
