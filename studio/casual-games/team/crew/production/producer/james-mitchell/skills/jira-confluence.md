---
name: studio-production-jira-confluence
description: Jira and Confluence setup, configuration, and maintenance standards for casual game studio production — sprint board configuration, backlog hygiene, milestone tracking, and documentation standards. Owned by James Mitchell (Producer). Trigger: Jira, Confluence, backlog, sprint board, production tooling, task tracking, documentation standards.
version: "1.0.0"
---

# Jira / Confluence Production Tooling

**Skill Owner:** James Mitchell (Producer)
**Applies To:** Sprint Planning, Backlog Management, Production Documentation, Studio Operations

## Jira Project Configuration

### Issue Hierarchy

```
Epic           ← Feature or milestone (e.g., "Season Pass System")
  │
  └─► Story    ← User-facing deliverable (e.g., "Player can purchase Season Pass")
        │
        └─► Task / Sub-task    ← Technical breakdown (e.g., "Implement IAP receipt validation")
              │
              └─► Bug         ← Defect found during QA or production
```

### Required Custom Fields (Studio Standard)

| Field                | Values                                               | Purpose                                       |
| -------------------- | ---------------------------------------------------- | --------------------------------------------- |
| Discipline           | Engineering / Art / Design / Audio / QA / Production | Filter by team in sprint board views          |
| Pipeline Stage       | Stage 1–10                                           | Track which gate this story belongs to        |
| Severity (bugs only) | P0 / P1 / P2 / P3                                    | Aligns to studio defect classification system |
| Blocked By           | Link to blocking issue                               | Surface cross-functional dependencies         |
| Estimate             | XS / S / M / L / XL                                  | T-shirt sizing for sprint capacity planning   |

### Sprint Board Configuration

- **Board type:** Scrum
- **Sprint length:** 2 weeks
- **Columns:** Backlog → To Do → In Progress → In Review → Done
- **Definition of Done:** Story is code-complete, tested by Amara's QA (if applicable), reviewed by Dmitri (if engineering), and accepted by the owner lead

### Backlog Hygiene Rules

1. No story enters the sprint without: a description, acceptance criteria, a discipline tag, and a T-shirt estimate
2. Stories estimated XL must be split before sprint commitment
3. All stories older than 4 sprints without activity are reviewed for relevance and either actioned or archived
4. The backlog is groomed for the next sprint at the mid-point of the current sprint (sprint grooming session)

## Confluence Documentation Standards

### Space Structure

```
Casual Games Studio (Confluence Space)
├── Project: [Game Name]
│   ├── Game Design Document (GDD)
│   ├── Technical Design Documents (TDDs)
│   ├── Art Style Guide
│   ├── Sprint Logs (one page per sprint — auto-created from template)
│   ├── Risk Register
│   ├── Post-Mortems
│   └── Decision Log (ADR-style entries for production decisions)
├── Processes
│   ├── Onboarding Guide
│   ├── Release Checklist
│   └── Pipeline Stage Gate Criteria
└── Templates
    ├── Sprint Log Template
    ├── Risk Register Template
    └── Post-Mortem Template
```

### Documentation Quality Standards

| Principle             | Standard                                                                                                                    |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Every decision logged | Any decision that affects scope, schedule, or design is logged in the Decision Log within 24 hours of being made            |
| Sprint log            | Every sprint has a log page created at sprint start; updated at review with: goal achieved? blockers encountered? velocity? |
| Post-mortems          | Every stage gate review that surfaces a High/Critical risk triggers a post-mortem within 48 hours                           |
| Templates used        | All standing document types use Confluence templates; no ad-hoc formats                                                     |

## Measurable Quality Standards

| Standard                      | Target                                        | Measurement Method            |
| ----------------------------- | --------------------------------------------- | ----------------------------- |
| Backlog groomed before sprint | 100% of stories estimated                     | Jira sprint entry check       |
| Sprint log created on time    | By end of Day 1 of each sprint                | Confluence page creation date |
| Decision log coverage         | 100% of scope/schedule changes                | Decision log review           |
| Jira hygiene                  | 0 stories in "To Do" >3 days without progress | Jira aging report             |
