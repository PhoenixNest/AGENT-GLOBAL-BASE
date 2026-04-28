---
version: "1.0.0"
---

| Competency               | Description                                                                              | Quality Criteria                                                                                             |
| ------------------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Instrumentation**      | Embedding observability primitives into application code without performance degradation | Automatic instrumentation coverage >80%; custom spans for all critical paths; <2% overhead on p99 latency    |
| **Log Management**       | Structured log production, aggregation, and querying at scale                            | 100% JSON structured logs; correlation IDs in all log lines; log volume <5GB/service/day at production scale |
| **Metrics Engineering**  | Designing metric collections aligned with business and system health                     | RED/USE method coverage for all services; custom business metrics for critical user journeys                 |
| **Distributed Tracing**  | End-to-end request visibility across service boundaries                                  | W3C Trace Context propagation across all hops; trace completeness >95%; span cardinality optimized           |
| **Alerting & SLOs**      | Defining actionable alerts based on error budgets and burn rates                         | False positive rate <5%; alert-to-action ratio >70%; SLO coverage for all customer-facing services           |
| **Production Debugging** | Safe diagnostic techniques without service restarts or code deploys                      | Dynamic log injection <30s latency; feature-flagged debug endpoints with RBAC controls                       |

## Pipeline Integration

This skill applies to the following pipeline stages:

| Stage                                 | Application                                                                                                                                 |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 3 (UML Engineering Package)** | Observability architecture decisions captured in ADRs; component diagrams include logging, metrics, and tracing infrastructure              |
| **Stage 4 (Implementation Plan)**     | Observability tasks included in implementation plan with time estimates for instrumentation, dashboard creation, and alert configuration    |
| **Stage 5 (Development)**             | OpenTelemetry SDK integration, structured logging implementation, metric collection, and trace propagation coded into all platform services |
| **Stage 6 (Code Review)**             | Observability code reviewed: span coverage, log structure, metric naming conventions, and alert definitions validated                       |
| **Stage 7 (Automated Testing)**       | Observability tested: metric exporters verified, trace context propagation validated, log structure assertions in unit/integration tests    |
| **Stage 8 (Integrity Verification)**  | End-to-end observability verified: traces flow from edge to database, dashboards render correctly, alerts fire on injected faults           |
| **Stage 10 (Release Readiness)**      | Observability readiness confirmed: all services instrumented, dashboards operational, alerts tested, runbooks documented                    |

## Quality Standards

| Standard                            | Target                                                                  | Measurement                                                    |
| ----------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Structured logging coverage**     | 100% of production log output is JSON                                   | Log shipper parsing success rate ≥99.5%                        |
| **Trace context propagation**       | W3C Trace Context in 100% of inter-service calls                        | Trace completeness (child spans with parent) ≥95%              |
| **RED method coverage**             | All customer-facing HTTP services expose Rate, Errors, Duration metrics | Metric existence check across all service `/metrics` endpoints |
| **SLO definition**                  | Every production service has at least one availability SLO              | SLO registry completeness = 100%                               |
| **Alert runbook coverage**          | 100% of active alerts have documented runbooks                          | Alert-to-runbook mapping audit                                 |
| **False positive rate**             | <5% of alerts are false positives                                       | Alert resolution tracking over rolling 30 days                 |
| **Dashboard freshness**             | All production dashboards refreshed within last 30 days                 | Dashboard last-accessed timestamp audit                        |
| **Observability overhead**          | Instrumentation adds <2% to p99 latency                                 | Load test with/without instrumentation comparison              |
| **Log retention**                   | ERROR/CRITICAL: 90 days; WARN: 30 days; INFO: 7 days                    | Log storage policy enforcement audit                           |
| **Trace sampling rate**             | 100% of errors sampled; 5-10% of successful requests                    | OpenTelemetry Collector sampling configuration                 |
| **Mean Time to Detect (MTTD)**      | <2 minutes for P0/P1 incidents                                          | Incident post-mortem data                                      |
| **Mean Time to Acknowledge (MTTA)** | <5 minutes for critical, <30 minutes for warning                        | On-call response tracking                                      |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
