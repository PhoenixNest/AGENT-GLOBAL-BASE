---
version: "1.0.0"
---

| Competency          | Description                                                                                                              | Quality Criteria                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| ELK Stack           | Elasticsearch cluster management, Logstash pipeline configuration, Kibana dashboard creation, index lifecycle management | Manages multi-node ELK clusters processing 100GB+/day; dashboards provide actionable operational insights |
| Fluentd             | Log collection, parsing, filtering, buffering, output configuration, Kubernetes integration                              | Collects logs from all services with zero data loss; structured JSON parsing for all log sources          |
| Anomaly Detection   | Statistical anomaly detection, machine learning-based detection, baseline establishment, alert tuning                    | Detects anomalies before they become incidents; false positive rate <5%                                   |
| Real-Time Alerting  | Alert rule design, notification routing, escalation policies, alert correlation, silence management                      | Alerts are actionable and routed to the right person; mean time to detection <1 minute                    |
| Distributed Tracing | Trace collection, span correlation, trace sampling, trace-based alerting, performance bottleneck identification          | End-to-end traces for 100% of requests; trace-log-correlation for debugging                               |

## Pipeline Integration

| Pipeline Stage                   | Application                                                                           |
| -------------------------------- | ------------------------------------------------------------------------------------- |
| Stage 3 (Architecture)           | Observability architecture decisions; log format standardization; tracing strategy    |
| Stage 5 (Development)            | Structured logging implementation; trace context propagation; metric instrumentation  |
| Stage 6 (Code Review)            | Logging completeness review; trace propagation verification; error logging quality    |
| Stage 7 (Testing)                | Log output validation; alert rule testing; anomaly detection baseline establishment   |
| Stage 8 (Integrity Verification) | Observability completeness audit; dashboard verification; alert routing testing       |
| Stage 10 (Release Readiness)     | Monitoring dashboard sign-off; alert configuration verification; runbook completeness |

## Quality Standards

| Metric                       | Target                                            | Measurement             |
| ---------------------------- | ------------------------------------------------- | ----------------------- |
| Log coverage                 | 100% of services emit structured logs             | Log ingestion audit     |
| Trace completeness           | >99% of requests have complete traces             | Trace span analysis     |
| Log ingestion latency        | <10 seconds from emission to searchable           | Log ingestion timing    |
| Anomaly detection accuracy   | >90% true positive rate, <5% false positive rate  | Alert accuracy analysis |
| Alert actionability          | 100% of alerts have runbooks                      | Runbook audit           |
| Dashboard coverage           | All critical services have operational dashboards | Dashboard inventory     |
| Elasticsearch cluster health | Green status; <75% disk utilization               | Cluster health API      |
| Log retention compliance     | 30 days hot, 90 days warm/cold                    | ILM policy compliance   |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
