---
candidate_name: 'Ops Engineer'
entity_type: 'studio'
stage: 'stage-4'
division: 'live-ops'
role: 'live-ops-engineer'
document_type: 'Interview Scores'
---

# Stage 4: Interview Simulation & Scored Assessments — Live Ops Engineer #1 (G30)

**Assessment Period:** 2026-04-12 to 2026-04-16
**Candidates Assessed:** 20

---

## Assessment Results — Top Candidate: David Okafor

### Live Ops Technical Case Study (48-hour async) — Score: 4.6/5

**Prompt:** Design a zero-downtime content deployment pipeline for a casual game with 5M DAU, including rollback strategy, analytics instrumentation, and incident response plan.

**Deliverable Summary:**

- Blue-green deployment architecture with automated health checks and traffic shifting
- Feature flag system (LaunchDarkly-style) for gradual rollout: 1% → 5% → 25% → 50% → 100%
- Automated rollback triggers: crash rate > 0.5%, error rate > 2%, D1 retention drop > 3pp
- Analytics instrumentation plan: 15 key events tracked (deploy start/complete, player sessions post-deploy, error rates, performance metrics)
- Incident response runbook with 4 severity levels and escalation paths

### Coding Challenge (90-min sandboxed) — Score: 4.5/5

- Implemented a rate-limited API endpoint with proper error handling, retry logic, and circuit breaker pattern
- Clean, well-tested code with 95% test coverage
- Optimized database queries using connection pooling and prepared statements

### System Design (60-min async) — Score: 4.4/5

- Designed real-time analytics pipeline: game client → event ingestion (Kafka) → stream processing (Flink) → dashboard (Grafana)
- Addressed scalability (horizontal partitioning by player ID), fault tolerance (exactly-once processing), and cost optimization

### Simulated Panel Interview (45 min) — Score: 4.5/5

| Dimension         | Score | Notes                                                    |
| ----------------- | ----- | -------------------------------------------------------- |
| Impact at Scale   | 5/5   | Zero-downtime deploys for 5M DAU game at Playdemic       |
| Craft Depth       | 4/5   | Deep CI/CD, server ops; growing in analytics engineering |
| Leadership Signal | 4/5   | Led incident response team; mentored 2 junior engineers  |
| Standards Signal  | 4/5   | Instituted deploy checklist adopted by all teams         |
| Red Flag Scan     | PASS  | Zero flags                                               |

#### Behavioral / Culture Add — Score: 4.0/5

#### Composite Score: 4.510/5 (95th percentile) — **ADVANCE** ✅

---

## Auto-Reject at Stage 4: 6 candidates below 80th percentile. 14 advance to Stage 5.
