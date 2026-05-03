---
name: technical-project-management
description: Technical project management with phased delivery methodology, progress oversight, and milestone tracking. Use when the user needs to manage software projects, create project plans, track progress, manage risks, produce status reports, or oversee engineering execution. Trigger when user mentions "project management", "progress tracking", "milestone planning", "status report", or needs to manage technical project delivery.
version: "1.0.0"
---

# Technical Project Management

## Purpose

Manage technical projects from planning through delivery using phased methodology. Provide visibility into progress, manage risks proactively, and ensure engineering teams deliver on time with quality.

## Why This Matters

Tracks progress, manages risks, and ensures on-time delivery. Without project management, teams lose visibility into schedule variance and miss Stage gate deadlines.

## When to Use This Skill

Use this skill when:

- A new project needs planning and execution oversight
- Engineering work requires progress tracking and reporting
- Multiple teams need coordination
- Stakeholders need visibility into technical progress
- Projects are at risk and need intervention
- Periodic status reporting is required

## Phased Delivery Methodology

### Phase 1: Requirements Analysis

**Goal**: Understand what needs to be built and why.

**Activities**:

- Review product requirements with CPO
- Identify technical constraints with CIO
- Clarify success criteria and acceptance conditions
- Document assumptions and dependencies
- Estimate scope and effort

**Deliverables**:

- Requirements document
- Initial effort estimate
- Risk assessment
- Go/no-go recommendation

**Duration**: 1-2 weeks for most projects

### Phase 2: Architecture Design

**Goal**: Design the technical solution.

**Activities**:

- Design system architecture
- Create UML diagrams
- Write architecture decision records
- Identify technology choices
- Plan data models and APIs

**Deliverables**:

- Architecture documentation
- Component specifications
- Technology selection decisions
- Design review approval

**Duration**: 2-4 weeks depending on complexity

### Phase 3: SPEC Authoring

**Goal**: Produce detailed technical specification.

**Activities**:

- Write comprehensive SPEC document
- Break down into implementation tasks
- Create phased rollout plan
- Define success metrics
- Plan monitoring and rollback

**Deliverables**:

- Complete SPEC document
- Task breakdown with estimates
- Implementation roadmap
- SPEC review approval

**Duration**: 1-3 weeks

### Phase 4: Implementation Planning

**Goal**: Organize engineering execution.

**Activities**:

- Assign tasks to engineers
- Set up project tracking
- Establish communication cadence
- Configure development environment
- Plan testing strategy

**Deliverables**:

- Sprint/milestone plan
- Team assignments
- Communication schedule
- Development environment ready

**Duration**: 1 week

### Phase 5: Iterative Delivery

**Goal**: Build and ship incrementally.

**Activities**:

- Execute in 2-week sprints
- Daily standups for blockers
- Weekly progress reviews
- Continuous integration and testing
- Incremental releases

**Deliverables**:

- Working software each sprint
- Progress reports
- Updated risk register
- Demo to stakeholders

**Duration**: 4-16 weeks depending on scope

### Phase 6: Retrospective

**Goal**: Learn and improve.

**Activities**:

- Review what went well
- Identify what to improve
- Document lessons learned
- Update processes and templates
- Celebrate wins

**Deliverables**:

- Retrospective document
- Process improvements
- Updated playbooks

**Duration**: 1 week

## Progress Tracking and Reporting

### Weekly Status Report Template

```markdown
# Project Status Report: [Project Name]

**Week of**: [Date]
**Status**: 🟢 On Track | 🟡 At Risk | 🔴 Blocked

## Executive Summary

[2-3 sentences: current state, key accomplishments, major concerns]

## Progress This Week

- ✅ [Completed item 1]
- ✅ [Completed item 2]
- ✅ [Completed item 3]

## Planned for Next Week

- [ ] [Planned item 1]
- [ ] [Planned item 2]
- [ ] [Planned item 3]

## Milestone Status

| Milestone                 | Target Date | Status      | Confidence |
| ------------------------- | ----------- | ----------- | ---------- |
| M1: Architecture Complete | 2026-04-15  | ✅ Done     | -          |
| M2: Backend API Ready     | 2026-05-01  | 🟡 At Risk  | 70%        |
| M3: iOS App Beta          | 2026-05-15  | 🟢 On Track | 85%        |
| M4: Production Launch     | 2026-06-01  | 🟢 On Track | 80%        |

## Risks and Issues

| Risk/Issue                  | Impact | Status    | Mitigation                          |
| --------------------------- | ------ | --------- | ----------------------------------- |
| Third-party API instability | High   | Active    | Implementing retry logic + fallback |
| iOS developer on leave      | Medium | Mitigated | Reassigned tasks to team            |

## Metrics

- **Velocity**: 32 story points (target: 30)
- **Code coverage**: 78% (target: 75%)
- **Open bugs**: 12 (P0: 0, P1: 3, P2: 9)
- **Tech debt**: 8 items (3 scheduled for next sprint)

## Blockers

[None | List any blockers requiring executive intervention]

## Asks

[Any decisions or resources needed from stakeholders]
```

### Status Indicators

**🟢 On Track**: Progressing as planned, no intervention needed
**🟡 At Risk**: Potential issues identified, mitigation in progress
**🔴 Blocked**: Critical blocker, requires immediate attention

Use these consistently so stakeholders can quickly assess health.

## Risk Management

### Risk Assessment Matrix

| Likelihood | Impact | Priority | Response                      |
| ---------- | ------ | -------- | ----------------------------- |
| High       | High   | P0       | Immediate mitigation required |
| High       | Medium | P1       | Mitigation plan within 1 week |
| Medium     | High   | P1       | Mitigation plan within 1 week |
| High       | Low    | P2       | Monitor and document          |
| Medium     | Medium | P2       | Monitor and document          |
| Low        | High   | P2       | Monitor and document          |
| Medium     | Low    | P3       | Accept risk                   |
| Low        | Medium | P3       | Accept risk                   |
| Low        | Low    | P3       | Accept risk                   |

### Common Project Risks

**Technical Risks**:

- Technology choice doesn't scale
- Third-party dependencies fail
- Performance requirements not met
- Security vulnerabilities discovered

**Team Risks**:

- Key engineer leaves
- Skills gap on critical technology
- Team velocity lower than estimated
- Burnout from sustained overtime

**External Risks**:

- Product requirements change
- Platform policy changes (App Store, Play Store)
- Competitive pressure accelerates timeline
- Budget cuts or resource constraints

**Mitigation Strategies**:

- Build proof-of-concepts early
- Have backup plans for critical dependencies
- Cross-train team members
- Maintain buffer in estimates
- Communicate risks early and often

## Milestone Planning

### Milestone Definition

Good milestones are:

- **Specific**: Clear deliverable, not vague progress
- **Measurable**: Objective completion criteria
- **Achievable**: Realistic given resources
- **Relevant**: Meaningful progress toward goal
- **Time-bound**: Specific target date

**Bad milestone**: "Make progress on backend"
**Good milestone**: "Backend API endpoints deployed to staging with 95% test coverage by May 1"

### Milestone Tracking

Track each milestone with:

- **Target date**: When we plan to complete
- **Actual date**: When we actually completed (or current estimate)
- **Status**: Not started, In progress, At risk, Blocked, Complete
- **Confidence**: Percentage confidence we'll hit target
- **Owner**: Who is accountable for delivery

Update confidence weekly based on progress and risks.

## Team Communication Cadence

### Daily Standups (15 minutes)

- What did you complete yesterday?
- What will you work on today?
- Any blockers?

Keep it brief. Detailed discussions happen offline.

### Weekly Progress Review (30 minutes)

- Review milestone progress
- Discuss risks and mitigation
- Adjust plans if needed
- Celebrate wins

### Bi-weekly Sprint Planning (1-2 hours)

- Review completed work
- Plan next sprint tasks
- Estimate effort
- Commit to sprint goal

### Monthly Stakeholder Review (1 hour)

- Demo working software
- Review overall progress
- Discuss strategic decisions
- Align on priorities

## Effort Estimation

### Estimation Techniques

**Story Points**: Relative sizing (Fibonacci: 1, 2, 3, 5, 8, 13)

- 1 point: Few hours, trivial
- 2 points: Half day, simple
- 3 points: 1 day, straightforward
- 5 points: 2-3 days, moderate complexity
- 8 points: 1 week, complex
- 13 points: 2 weeks, very complex (consider breaking down)

**T-Shirt Sizing**: XS, S, M, L, XL for rough estimates

**Person-Weeks**: Actual time estimates

- Include buffer for unknowns (20-30%)
- Account for meetings, code review, testing
- Assume 60-70% productive time

### Velocity Tracking

Measure team velocity over time:

- Track story points completed per sprint
- Calculate rolling average over 3-4 sprints
- Use for future planning
- Adjust estimates based on actual velocity

## Managing Delays and Scope Changes

### When Projects Fall Behind

1. **Diagnose the cause**:
   - Underestimated complexity?
   - Unexpected technical challenges?
   - Team capacity issues?
   - Scope creep?

2. **Evaluate options**:
   - Add resources (rarely effective)
   - Reduce scope (often best option)
   - Extend timeline
   - Accept technical debt (with plan to address)

3. **Communicate transparently**:
   - Explain situation to stakeholders
   - Present options with trade-offs
   - Get alignment on path forward
   - Update plans and expectations

### Scope Change Process

When requirements change mid-project:

1. **Document the change**: What's different and why?
2. **Assess impact**: How does this affect timeline, resources, risk?
3. **Present options**: Continue as-is, adjust scope, extend timeline
4. **Get approval**: Stakeholder decision required
5. **Update plans**: Revise SPEC, milestones, estimates
6. **Communicate**: Inform team and stakeholders

## Quality Gates

Define quality criteria that must be met:

**Code Quality**:

- Code review approval required
- Test coverage ≥ 75%
- No P0/P1 bugs
- Linting and static analysis pass

**Performance**:

- API latency < 200ms p95
- App launch time < 2 seconds
- Memory usage within limits
- Battery drain acceptable

**Security**:

- Security review completed
- No critical vulnerabilities
- Data encryption verified
- Authentication tested

**User Experience**:

- Accessibility compliance
- Platform guidelines followed
- Error handling graceful
- Loading states implemented

Don't ship if quality gates aren't met.

## Tools and Practices

**Project Tracking**: Jira, Linear, GitHub Projects, Asana
**Documentation**: Confluence, Notion, Google Docs
**Communication**: Slack, Teams, Discord
**Version Control**: Git with feature branches
**CI/CD**: GitHub Actions, CircleCI, Jenkins
**Monitoring**: Datadog, New Relic, Sentry

## Company Pipeline Stage Ownership

The CTO owns or co-owns every stage from Stage 3 through Stage 10 (excluding Stage 9 — i18n). Each stage has specific deliverables the CTO must produce or sign off on before the pipeline can advance.

### Stage 3 — Prototype → UML Engineering Package

**CTO produces:** Architecture Decision Records (ADRs), UML diagrams (class, sequence, component, deployment), Technology Selection Document (TSD). All are locked on user approval; any post-Stage 3 technology change requires a new ADR and full Stage 3 re-entry.

### Stage 4 — UML → Implementation Plan + Gantt

**CTO produces:** Phased coding implementation plan, Gantt chart with milestones, team assignments, sprint allocation. Must include the three mandatory progress-monitoring files in the project folder: `progress.md`, `session-log.md`, and `checkpoint.json`. Any estimate overrun >20% triggers a CTO → CPO schedule risk notification.

### Stage 5 — Software Development

**CTO oversees:** All engineering execution. Weekly progress reports to C-suite. The `progress.md` is updated after every session, `session-log.md` maintains a timestamped audit trail, and `checkpoint.json` reflects the latest milestone completion state.

### Stage 6 — Code Review

**CTO chairs the review panel.** The full panel includes CTO + CDO + CPO + CIO + CSO + VP Web + VP API. Dr. Nakamura's role:

| Review Dimension             | What the CTO Reviews                                                                                                 |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Architecture adherence**   | Does the implementation match the Stage 3 UML package? Any divergences are P1 unless an ADR was filed and approved.  |
| **Specification fidelity**   | Does the implementation fulfill every SPEC requirement? Missing requirements are P1.                                 |
| **Code quality**             | Complexity, test coverage, naming, pattern adherence across all platform layers                                      |
| **Cross-platform coherence** | Android, iOS, and shared layers are internally consistent; VP Mobile's findings are incorporated                     |
| **Security**                 | Coordinates with CIO review; any MASVS or OWASP finding not already flagged by CIO is escalated                      |
| **Trim-to-Pass detection**   | Confirms no feature or security control was disabled to achieve a passing review — this is a P0 defect if discovered |

**Remediation rule:** After any P0/P1 finding and remediation, the full panel reconvenes from the beginning. Dr. Nakamura ensures this rule is enforced — no partial re-reviews.

### Stage 7 — Automated Testing

**CTO co-owns with Test Lead (Priscilla Oduya).** Dr. Nakamura reviews the test plan and results, signs off that coverage thresholds are met, and that any failing tests are either remediated (P0/P1) or accepted with documented rationale (P2/P3). He does not run tests himself — that is Priscilla Oduya's execution domain.

### Stage 8 — Integrity Verification

**CTO holds final technical sign-off authority.** The Integrity Verification panel includes all C-suite. Dr. Nakamura's sign-off confirms:

| Gate                              | CTO Confirmation                                                                               |
| --------------------------------- | ---------------------------------------------------------------------------------------------- |
| All Stage 6 defects remediated    | Zero open P0/P1 items in the defect tracker                                                    |
| All Stage 7 automated tests green | Test suite passes on the release candidate build                                               |
| Architecture integrity            | The shipped system matches the Stage 3 UML package or has an approved ADR for every divergence |
| Trim-to-Pass scan                 | Confirm final confirmation that no feature or security control was removed to reach this stage |
| Performance SLOs met              | All CTO-specified performance targets confirmed in staging profiling data                      |

After all C-suite sign-offs are received, Dr. Nakamura delivers a written **Integrity Confirmation Memo** to the user summarizing the release candidate state and recommending advancement to Stage 9.

### Stage 10 — Release Readiness Check

**CTO co-signs the final Release Readiness Checklist** alongside the user. Confirms that all technical gates across Stages 6–9 are green, production infrastructure is ready, and rollback procedures are tested and documented.

## Output Format

When managing projects, produce:

1. **Project plan** with phases, milestones, and estimates
2. **Weekly status reports** with progress, risks, and metrics
3. **Risk register** tracking and mitigating project risks
4. **Milestone tracker** showing progress toward goals
5. **Retrospective documents** capturing lessons learned
6. **Stage gate deliverables** as specified per pipeline stage above

Keep documentation concise and actionable. Stakeholders should be able to understand project health in under 5 minutes.
