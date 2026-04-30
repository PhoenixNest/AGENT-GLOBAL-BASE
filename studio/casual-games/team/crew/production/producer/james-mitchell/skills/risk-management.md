---
name: studio-production-risk-management
description: Production risk identification and mitigation for casual game development — risk registers, probability/impact assessment, escalation protocols, and contingency planning across engineering, art, design, and audio disciplines. Owned by James Mitchell (Producer). Trigger: risk management, production risk, risk register, contingency planning, escalation, schedule risk.
version: "1.0.0"
---

# Risk Management

**Skill Owner:** James Mitchell (Producer)
**Applies To:** All Studio Pipeline Stages (1–10), Schedule and Scope Risk

## Risk Register Format

Every active project maintains a risk register in Confluence, reviewed at the start of each sprint. Format:

| ID    | Risk               | Category                                      | Probability | Impact | Score | Mitigation | Owner  | Status                    |
| ----- | ------------------ | --------------------------------------------- | ----------- | ------ | ----- | ---------- | ------ | ------------------------- |
| R-001 | [Risk description] | Engineering / Art / Design / Audio / External | H/M/L       | H/M/L  | H/M/L | [Action]   | [Name] | Open / Mitigated / Closed |

**Score matrix:** H×H = Critical · H×M or M×H = High · M×M = Medium · L×any = Low

## Risk Categories and Common Triggers

### Engineering Risks

| Risk                                         | Trigger Signals                           | Default Mitigation                                                      |
| -------------------------------------------- | ----------------------------------------- | ----------------------------------------------------------------------- |
| Core system complexity underestimated        | Spike task overruns estimate by >50%      | Escalate to Dmitri; re-estimate; adjust sprint goal                     |
| Third-party SDK instability                  | SDK update causes build failures in CI    | Pin SDK version; schedule upgrade sprint separately                     |
| Performance budget breach                    | Nightly profiling shows regression >10fps | P1 defect; engineer owns fix before next sprint review                  |
| Backend API not ready for client integration | Backend estimate slips >3 days            | James coordinates with Backend Lead; James Okonkwo escalated if >1 week |

### Art and Design Risks

| Risk                      | Trigger Signals                                      | Default Mitigation                                     |
| ------------------------- | ---------------------------------------------------- | ------------------------------------------------------ |
| Art pipeline bottleneck   | Artist capacity <80% of sprint commitment            | Identify blocked assets; escalate to Renaud Leclercq   |
| Design churn post-Stage 3 | GDD amendments requested after art production starts | Scope change request process; CD sign-off required     |
| Missing asset on schedule | Asset not in repository 5 days before feature freeze | Blocker flag in Jira; daily check-in with Art Director |

### External / Market Risks

| Risk                                          | Trigger Signals                       | Default Mitigation                                                          |
| --------------------------------------------- | ------------------------------------- | --------------------------------------------------------------------------- |
| Platform policy change (App Store/Play Store) | Policy announcement during production | James monitors developer.apple.com / Android Policy Blog; weekly scan       |
| Soft launch market underperformance           | D1 retention <30% in Stage 8          | Escalate to Executive Producer; hold Stage 9 advancement pending root cause |

## Escalation Protocol

| Situation                                         | Escalation Path                            | Timeframe          |
| ------------------------------------------------- | ------------------------------------------ | ------------------ |
| Risk score escalates from Medium to High          | James → James Okonkwo (EP)                 | Same business day  |
| Risk becomes a live blocker (sprint goal at risk) | James → Dmitri + James Okonkwo             | Immediate          |
| Risk threatens stage gate advancement             | James → Dr. Marcus Vogel (Studio Director) | Before gate review |
| Risk involves external vendor or platform         | James → James Okonkwo + Studio Director    | Within 24 hours    |

## Real-World Production Scenario

### Scenario: Schedule Risk from Feature Complexity

**Context:** An engineering spike on a new social feature reveals the implementation is 3× the original estimate, threatening the Stage 5 milestone.
**Process:**

1. James updates the risk register the same day the spike result is known (no silent slips)
2. Facilitates a scope decision meeting with Dmitri (engineering) and Mei Watanabe (design) within 24 hours:
   - Option A: Reduce scope to MVP (cut social feature to async only)
   - Option B: Extend sprint and compress adjacent milestone by pushing a lower-priority feature
   - Option C: Escalate to Executive Producer for resourcing decision
3. Documents the decision with rationale in Confluence sprint log
4. Updates the Gantt chart and communicates the change to the Studio Director

## Measurable Quality Standards

| Standard                          | Target                               | Measurement Method              |
| --------------------------------- | ------------------------------------ | ------------------------------- |
| Risk register updated             | Every sprint start                   | Confluence last-modified date   |
| Escalation compliance             | 100% within defined timeframe        | Jira ticket creation timestamps |
| Critical risks with no mitigation | 0                                    | Risk register review            |
| Post-mortem coverage              | 100% of High risks that materialized | Post-mortem log                 |
