---
candidate_name: 'Ops Engineer'
entity_type: 'studio'
stage: 'stage-4'
division: 'live-ops'
role: 'live-ops-engineer'
document_type: 'Interview Scores'
---

# Stage 4: Interview Simulation & Scored Assessments — Live Ops Engineer #2 (G31)

**Assessment Period:** 2026-04-12 to 2026-04-16

---

## Assessment Results — Top Candidate: Sofia Reyes

### Technical Case Study (48-hour) — Score: 4.5/5

**Prompt:** Design an A/B testing infrastructure for a live game with 5M DAU, including feature flag integration, data pipeline, and real-time monitoring.

**Deliverable Summary:**

- A/B test platform design with randomization service (consistent bucketing via consistent hashing), experiment management dashboard, and statistical analysis engine
- Data pipeline: game client events → Kafka → Flink stream processing → ClickHouse for real-time queries → S3 for batch analysis
- Feature flag integration: LaunchDarkly-style system with experiment-aware flag evaluation (flags can be scoped to experiment variants)
- Real-time monitoring dashboard: experiment enrollment rates, variant balance check, guardrail metrics (crash rate, latency)
- Player segmentation engine: ML-based clustering (K-means on behavioral features) with automated segment assignment for targeted experiments

**Strengths:** Comprehensive architecture; strong data pipeline design; practical feature flag + experiment integration; excellent player segmentation approach.

### Coding Challenge (90-min) — Score: 4.4/5

- Implemented consistent hashing algorithm for A/B test bucket assignment with even distribution across variants
- Built data pipeline consumer in Python with exactly-once processing guarantees
- Clean code with comprehensive tests (92% coverage)

### System Design (60-min) — Score: 4.3/5

- Designed player segmentation pipeline with real-time feature computation and periodic model retraining
- Addressed data freshness (streaming vs. batch trade-offs), model drift detection, and segment stability

### Simulated Panel Interview (45 min) — Score: 4.4/5

| Dimension         | Score | Notes                                                |
| ----------------- | ----- | ---------------------------------------------------- |
| Impact at Scale   | 5/5   | Built A/B testing platform serving 3M DAU at Scopely |
| Craft Depth       | 4/5   | Deep A/B testing + data pipelines; growing in ML ops |
| Leadership Signal | 4/5   | Led data platform team of 4; mentored 2 analysts     |
| Standards Signal  | 4/5   | Established experiment documentation standard        |
| Red Flag Scan     | PASS  | Zero flags                                           |

#### Behavioral / Culture Add — Score: 4.1/5

#### Composite Score: 4.440/5 (93rd percentile) — **ADVANCE** ✅

---

## Auto-Reject at Stage 4: 5 candidates below 80th percentile. 14 advance to Stage 5.
