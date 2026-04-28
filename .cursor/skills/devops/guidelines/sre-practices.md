---
name: sre-practices
description: Implements Site Reliability Engineering practices including SLO/SLI definition and measurement, error budget policies, incident response lifecycle management.
---

# SRE Practices

**Category:** Site Reliability Engineering
**Owner:** SRE Engineer (Raihan Rahman)

## Overview

Implements Site Reliability Engineering practices including SLO/SLI definition and measurement, error budget policies, incident response lifecycle management, blameless postmortem facilitation, and on-call rotation design. Bridges the gap between development velocity and production reliability through data-driven reliability targets and systematic incident management.

## Competency Dimensions

| Dimension             | Description                                                                                | Proficiency Indicators                                                                                                                   |
| --------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| SLO/SLI Definition    | Service level objectives, service level indicators, error budgets, SLI collection          | Defines measurable SLIs aligned with user experience; sets SLOs based on user expectations; calculates error budgets and burn rates      |
| Error Budget Policies | Budget consumption tracking, burn rate alerts, policy enforcement, feature freeze triggers | Implements multi-window burn rate alerting; triggers feature freeze when budget exhausted; defines recovery procedures                   |
| Incident Response     | Detection, triage, mitigation, resolution, postmortem lifecycle                            | Runs incident response as incident commander; follows structured incident lifecycle; ensures timely communication                        |
| Blameless Postmortems | Root cause analysis, contributing factors, action items, cultural safety                   | Facilitates postmortems focused on systemic factors, not individual blame; produces actionable follow-ups; tracks action item completion |
| On-Call Rotation      | Rotation design, escalation policies, fatigue prevention, compensation                     | Designs sustainable on-call rotations (no more than 1 week per 4); implements tiered escalation; tracks on-call load metrics             |

## Execution Guidance

### SLO/SLI Definition and Measurement

**SLI categories with examples:**

| Category     | SLI                           | Measurement                                           | Example Target |
| ------------ | ----------------------------- | ----------------------------------------------------- | -------------- |
| Availability | % of successful requests      | `(total_requests - failed_requests) / total_requests` | 99.9%          |
| Latency      | % of requests under threshold | `count(request_duration < 200ms) / total_requests`    | 95% < 200ms    |
| Throughput   | Requests per second           | `count(requests) / time_window`                       | > 1000 rps     |
| Correctness  | % of correct results          | `correct_results / total_results`                     | 99.99%         |
| Durability   | % of data not lost            | `(total_data - lost_data) / total_data`               | 99.999999999%  |
| Freshness    | Data age at query time        | `current_time - data_timestamp`                       | < 5 seconds    |

**SLO definition template:**

````markdown
# SLO: API Availability

## Service

API Gateway (all backend services)

## SLI

Availability = (Successful HTTP responses / Total HTTP responses) × 100

Where "successful" = HTTP 2xx, 3xx, 4xx responses (not 5xx)
Excludes: 429 (rate limited), client-caused errors (4xx)

## SLO Target

99.9% over a 30-day rolling window

## Error Budget

0.1% of requests over 30 days = ~43 minutes of allowable downtime

## Measurement

```promql
# Success rate over 30 days
sum(rate(http_requests_total{code=~"2..|3..|4.."}[30d]))
/
sum(rate(http_requests_total[30d]))
* 100
```
````

## Burn Rate Alerting

| Burn Rate | Window  | Severity | Action                                  |
| --------- | ------- | -------- | --------------------------------------- |
| 14.4x     | 1 hour  | Critical | Page on-call, investigate immediately   |
| 6x        | 6 hours | Critical | Page on-call, investigate within 30 min |
| 3x        | 1 day   | Warning  | Ticket, investigate within 4 hours      |
| 1x        | 3 days  | Warning  | Review in next planning cycle           |

````

**Multi-window burn rate alerting (Google SRE approach):**

```yaml
# Prometheus alerting rules for burn rate
groups:
  - name: slo-burn-rate
    rules:
      # 14.4x burn rate over 1 hour (consumes 2% of monthly budget in 1 hour)
      - alert: APIAvailabilityHighBurn1h
        expr: |
          (
            (1 - (
              sum(rate(http_requests_total{code=~"2..|3..|4.."}[1h]))
              /
              sum(rate(http_requests_total[1h]))
            ))
            /
            (1 - 0.999)  # SLO target
          ) > 14.4
        for: 3m
        labels:
          severity: critical
          team: backend
          slo: api-availability
        annotations:
          summary: "API availability burning budget at 14.4x rate"
          description: "At this rate, monthly error budget will be exhausted in ~2 hours"

      # 6x burn rate over 6 hours
      - alert: APIAvailabilityHighBurn6h
        expr: |
          (
            (1 - (
              sum(rate(http_requests_total{code=~"2..|3..|4.."}[6h]))
              /
              sum(rate(http_requests_total[6h]))
            ))
            /
            (1 - 0.999)
          ) > 6
        for: 15m
        labels:
          severity: critical
          team: backend
          slo: api-availability

      # 3x burn rate over 1 day
      - alert: APIAvailabilityHighBurn1d
        expr: |
          (
            (1 - (
              sum(rate(http_requests_total{code=~"2..|3..|4.."}[1d]))
              /
              sum(rate(http_requests_total[1d]))
            ))
            /
            (1 - 0.999)
          ) > 3
        for: 1h
        labels:
          severity: warning
          team: backend
          slo: api-availability

      # 1x burn rate over 3 days
      - alert: APIAvailabilityHighBurn3d
        expr: |
          (
            (1 - (
              sum(rate(http_requests_total{code=~"2..|3..|4.."}[3d]))
              /
              sum(rate(http_requests_total[3d]))
            ))
            /
            (1 - 0.999)
          ) > 1
        for: 3h
        labels:
          severity: warning
          team: backend
          slo: api-availability
````

### Error Budget Policy

```markdown
# Error Budget Policy

## Budget Status Dashboard

- Current budget remaining: 45%
- Burn rate trend: Stable (0.8x)
- Days until exhaustion (at current rate): 56 days

## Policy Actions by Budget Level

| Budget Remaining | Action                                                       |
| ---------------- | ------------------------------------------------------------ |
| > 50%            | Normal operations                                            |
| 25-50%           | Review recent incidents, identify reliability improvements   |
| 10-25%           | Pause non-critical feature deployments, focus on reliability |
| 5-10%            | Feature freeze — only bug fixes and reliability improvements |
| < 5%             | Emergency reliability sprint, all hands on reliability       |

## Budget Reset

- Rolling 30-day window (budget resets continuously)
- Monthly review: assess budget consumption trends
- Quarterly: recalibrate SLO targets based on user feedback

## Release Governance

When budget < 25%:

- All releases require SRE sign-off
- Canary deployment mandatory (1% → 10% → 50% → 100%)
- Rollback plan required before deployment
- No deployments during peak hours (9 AM - 6 PM)
```

### Incident Response Lifecycle

```
Incident Lifecycle:

DETECTION → TRIAGE → MITIGATION → RESOLUTION → POSTMORTEM
    │          │          │             │             │
    ▼          ▼          ▼             ▼             ▼
 Alert      Assess      Contain       Fix root      Blameless
 fired      severity    impact        cause         analysis
                        Communicate   Verify        Action items
```

**Incident severity levels:**

| Level | Definition                                    | Response Time     | Communication                   | Example                                          |
| ----- | --------------------------------------------- | ----------------- | ------------------------------- | ------------------------------------------------ |
| SEV-0 | Complete outage, data breach                  | 5 minutes         | C-suite, all-hands every 30 min | API completely down, customer data exposed       |
| SEV-1 | Major feature broken, significant user impact | 15 minutes        | Affected users every hour       | Payment processing down, 50% of users affected   |
| SEV-2 | Partial degradation, workaround exists        | 1 hour            | Status page update              | Slow API responses, intermittent errors          |
| SEV-3 | Minor issue, limited user impact              | 4 hours           | Internal notification           | Non-critical feature broken, < 5% users affected |
| SEV-4 | Cosmetic, no user impact                      | Next business day | Internal ticket                 | UI misalignment, typo in error message           |

**Incident commander runbook:**

```markdown
# Incident Commander Runbook

## Immediate Actions (First 5 minutes)

1. [ ] Acknowledge alert, create incident channel (#incident-YYYYMMDD-HHmm)
2. [ ] Assign roles: Incident Commander, Communications Lead, Tech Lead
3. [ ] Assess severity using severity matrix
4. [ ] Notify stakeholders based on severity level

## Triage (5-15 minutes)

1. [ ] Identify affected service(s) and user impact
2. [ ] Check recent deployments (last 2 hours)
3. [ ] Review dashboards for anomalies
4. [ ] Formulate hypothesis for root cause

## Mitigation (15-60 minutes)

1. [ ] Implement containment (rollback, feature flag disable, traffic shift)
2. [ ] Verify mitigation effectiveness
3. [ ] If mitigation fails, try next hypothesis
4. [ ] Communicate status to stakeholders every 30 minutes

## Resolution (60+ minutes)

1. [ ] Confirm issue is resolved
2. [ ] Monitor for recurrence (30-minute observation period)
3. [ ] Declare incident resolved
4. [ ] Schedule postmortem within 48 hours

## Communication Template

**Initial:** "We are investigating reports of [issue] affecting [scope]. ETA for next update: [time]."
**Update:** "Update: [what we found], [what we're doing], [impact]. Next update: [time]."
**Resolved:** "Resolved: [issue] has been resolved. [Root cause summary]. Postmortem will follow."
```

### Blameless Postmortem

```markdown
# Postmortem: [Incident Title]

## Metadata

| Field                  | Value                     |
| ---------------------- | ------------------------- |
| **Date**               | YYYY-MM-DD                |
| **Severity**           | SEV-1                     |
| **Duration**           | 2 hours 15 minutes        |
| **Incident Commander** | [Name]                    |
| **Author**             | [Name]                    |
| **Status**             | Draft / Review / Complete |

## Summary

[2-3 paragraph summary of what happened, impact, and resolution.]

## Impact

- **Duration:** 2h 15m (14:32 - 16:47 UTC)
- **Users affected:** ~15,000 (30% of active users)
- **Revenue impact:** ~$12,000 in failed transactions
- **SLO impact:** Consumed 18% of monthly error budget

## Timeline

| Time (UTC) | Event                                                          |
| ---------- | -------------------------------------------------------------- |
| 14:32      | Alert fired: API availability dropped to 94%                   |
| 14:35      | On-call engineer acknowledged, created incident channel        |
| 14:42      | Root cause identified: Database connection pool exhaustion     |
| 14:50      | Mitigation attempted: Restarted application pods (ineffective) |
| 15:15      | Correct mitigation: Increased PgBouncer pool size              |
| 15:20      | Recovery began, availability improved to 98%                   |
| 16:00      | Full recovery confirmed                                        |
| 16:47      | Incident declared resolved                                     |

## Root Cause Analysis

### Direct Cause

PgBouncer connection pool size (50) was insufficient for the increased traffic from a new feature launch, causing connection timeouts.

### Contributing Factors

1. **Capacity planning gap:** Load testing was done with baseline traffic, not accounting for feature launch spike
2. **Monitoring gap:** No alert on connection pool utilization (only on errors)
3. **Configuration drift:** Pool size was not adjusted when new services were added
4. **Deployment process:** New feature deployed without capacity review

### Five Whys

1. **Why did the API become unavailable?** — Database connections timed out.
2. **Why did connections time out?** — PgBouncer pool was exhausted (all 50 connections in use).
3. **Why was the pool exhausted?** — New feature increased database connections by 3x.
4. **Why wasn't the pool sized for the increased load?** — Capacity review was not part of the deployment checklist.
5. **Why wasn't capacity review required?** — The deployment process doesn't mandate capacity review for features that increase database load.

## Action Items

| ID  | Action                                                 | Owner        | Priority | Due Date | Status |
| --- | ------------------------------------------------------ | ------------ | -------- | -------- | ------ |
| A1  | Add PgBouncer pool utilization alert (> 80%)           | SRE          | High     | 1 week   | Open   |
| A2  | Update deployment checklist to include capacity review | Engineering  | High     | 2 weeks  | Open   |
| A3  | Increase PgBouncer pool size to 150                    | SRE          | High     | 1 day    | Done   |
| A4  | Load test with 3x baseline traffic                     | Test Lead    | Medium   | 2 weeks  | Open   |
| A5  | Document connection pool sizing formula                | Backend Lead | Medium   | 1 week   | Open   |

## Lessons Learned

- **What went well:** Quick detection (< 3 min), effective incident command, clear communication
- **What needs improvement:** Capacity planning process, monitoring coverage, deployment checklist
- **Where we got lucky:** Issue occurred during business hours when full team was available
```

### On-Call Rotation Design

```markdown
# On-Call Rotation Policy

## Rotation Structure

- **Primary on-call:** 1 week rotation, 4-week cycle (1 week on, 3 weeks off)
- **Secondary on-call:** Backup, escalates from primary if no response in 10 min
- **Tertiary (manager):** Escalates from secondary if unresolved in 1 hour

## Schedule

- Rotation starts Monday 9:00 AM local time
- Handoff meeting: 15-minute sync between outgoing and incoming
- Documentation: Incoming reviews open incidents, recent changes, known issues

## Alert Fatigue Prevention

- **Alert budget:** Max 5 pages per on-call shift (otherwise review alert configuration)
- **Alert quality review:** Weekly review of all pages, eliminate false positives
- **Actionable alerts only:** Every page must require immediate human action
- **Info alerts go to Slack, not PagerDuty**

## Escalation Policy

| Time   | Action                               |
| ------ | ------------------------------------ |
| 0 min  | Primary on-call notified (PagerDuty) |
| 10 min | Secondary on-call notified           |
| 30 min | Engineering manager notified         |
| 60 min | CTO notified (for SEV-0/SEV-1)       |

## Compensation

- On-call allowance: $500/week
- Incident response (> 1 hour, off-hours): Comp time 1:1
- SEV-0 response: Additional $200 bonus
```

## Pipeline Integration

**Stage 1 (Requirements):** SLO requirements derived from PRD user experience expectations. Error budget allocation considered in product roadmap planning.

**Stage 3 (Architecture):** Component diagrams show monitoring and alerting infrastructure. ADR required for SLO targets and monitoring tool selection.

**Stage 5 (Development):** All services instrumented with SLI collection. Health check endpoints implemented. Structured logging for incident investigation.

**Stage 7 (Testing):** Load testing validates SLO targets. Chaos testing validates incident response procedures. Alert testing validates monitoring coverage.

**Stage 10 (Release Readiness):** Panel confirms SLO monitoring operational, error budget policies defined, on-call rotation staffed, incident runbooks documented.

## Quality Standards

| Metric                         | Target                                 | Measurement          |
| ------------------------------ | -------------------------------------- | -------------------- |
| SLO coverage                   | 100% of user-facing services have SLOs | SLO inventory        |
| Alert accuracy                 | > 95% of pages are actionable          | Alert review         |
| Incident response time (SEV-1) | < 15 minutes                           | Incident tracking    |
| MTTR (SEV-1)                   | < 2 hours                              | Incident tracking    |
| Postmortem completion          | 100% of SEV-0/SEV-1 within 48 hours    | Postmortem tracker   |
| Action item completion         | > 90% completed by due date            | Postmortem follow-up |
| On-call page budget            | < 5 pages per shift                    | PagerDuty metrics    |
| Error budget consumption       | < 25% per rolling 30 days              | SLO dashboard        |
