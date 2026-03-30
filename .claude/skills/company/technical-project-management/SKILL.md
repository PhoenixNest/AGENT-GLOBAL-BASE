---
name: company-technical-project-management
description: Technical project management — phased delivery methodology, progress oversight, milestone tracking, Gantt chart production, risk management, Progress Sync Protocol, and CTO→CPO schedule risk notifications. Owned by Dr. Kenji Nakamura (CTO).
disable-model-invocation: false
---

# Technical Project Management

## Purpose

Manage technical projects from planning through delivery using phased methodology. Provide visibility into progress, manage risks proactively, and ensure engineering teams deliver on time with quality.

## Phased Delivery Methodology

### Phase 1: Requirements Analysis

**Goal**: Understand what needs to be built and why.

**Activities**: Review product requirements with CPO; identify technical constraints with CIO; clarify success criteria; document assumptions and dependencies; estimate scope.

**Deliverables**: Requirements document, initial effort estimate, risk assessment, go/no-go recommendation.

### Phase 2: Architecture Design

**Goal**: Design the technical solution.

**Deliverables**: Architecture documentation, component specifications, technology selection decisions, design review approval.

### Phase 3: SPEC Authoring

**Goal**: Produce detailed technical specification.

**Deliverables**: Complete SPEC document, task breakdown with estimates, implementation roadmap.

### Phase 4: Implementation Planning

**Goal**: Organize engineering execution.

**Deliverables**: Sprint/milestone plan, team assignments, communication schedule.

### Phase 5: Iterative Delivery

**Goal**: Build and ship incrementally.

**Activities**: Execute in 2-week sprints; daily standups for blockers; weekly progress reviews; continuous integration and testing.

### Phase 6: Retrospective

**Goal**: Learn and improve.

**Deliverables**: Retrospective document, process improvements, updated playbooks.

---

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

## Planned for Next Week
- [ ] [Planned item 1]
- [ ] [Planned item 2]

## Milestone Status
| Milestone | Target Date | Status | Confidence |
|-----------|-------------|--------|------------|
| M1: Architecture Complete | YYYY-MM-DD | ✅ Done | - |
| M2: Backend API Ready | YYYY-MM-DD | 🟡 At Risk | 70% |

## Risks and Issues
| Risk/Issue | Impact | Status | Mitigation |
|------------|--------|--------|------------|
| [Risk 1] | High | Active | [Mitigation] |

## Metrics
- **Velocity**: [N] story points (target: [N])
- **Open bugs**: [N] (P0: [N], P1: [N], P2: [N])

## Blockers
[None | List any blockers requiring executive intervention]
```

### Status Indicators

**🟢 On Track**: Progressing as planned, no intervention needed
**🟡 At Risk**: Potential issues identified, mitigation in progress
**🔴 Blocked**: Critical blocker, requires immediate attention

---

## Progress Sync Protocol

**Active from Stage 4 onward.**

- Each completed coding task triggers an update to the progress log
- Any task exceeding its estimated duration by **>20%** triggers an automatic CTO → CPO schedule risk notification
- The CTO produces weekly progress summaries for C-suite visibility

This is a non-negotiable pipeline rule. If a task is 20% over estimate, the CPO is notified immediately — do not wait for the weekly summary.

---

## Risk Management

### Risk Assessment Matrix

| Likelihood | Impact | Priority | Response |
|------------|--------|----------|----------|
| High | High | P0 | Immediate mitigation required |
| High | Medium | P1 | Mitigation plan within 1 week |
| Medium | High | P1 | Mitigation plan within 1 week |
| High | Low | P2 | Monitor and document |
| Medium | Medium | P2 | Monitor and document |
| Low | High | P2 | Monitor and document |
| Low/Medium | Low | P3 | Accept risk |

### Common Project Risks

**Technical**: Technology choice doesn't scale; third-party dependencies fail; performance requirements not met.

**Team**: Key engineer leaves; skills gap on critical technology; team velocity lower than estimated.

**External**: Product requirements change; platform policy changes (App Store, Play Store); competitive pressure accelerates timeline.

---

## Milestone Planning

Good milestones are SMART: Specific, Measurable, Achievable, Relevant, Time-bound.

**Bad milestone**: "Make progress on backend"
**Good milestone**: "Backend API endpoints deployed to staging with 95% test coverage by May 1"

Track each milestone with: target date, actual date (or current estimate), status, confidence percentage, owner.

---

## Effort Estimation

### Story Points (Fibonacci)

- 1 point: Few hours, trivial
- 2 points: Half day, simple
- 3 points: 1 day, straightforward
- 5 points: 2-3 days, moderate complexity
- 8 points: 1 week, complex
- 13 points: 2 weeks, very complex (consider breaking down)

**Include buffer**: 20-30% for unknowns. Account for meetings, code review, testing. Assume 60-70% productive time.

---

## Quality Gates

Must be met before advancing any stage:

**Code Quality**: Code review approval required; test coverage ≥ 75%; no P0/P1 bugs; linting passes.

**Performance**: API latency < 200ms p95; app launch time < 2 seconds; memory within limits.

**Security**: Security review completed; no critical vulnerabilities; data encryption verified.

**User Experience**: Accessibility compliance; platform guidelines followed; error handling graceful; loading states implemented.

Don't ship if quality gates aren't met.
