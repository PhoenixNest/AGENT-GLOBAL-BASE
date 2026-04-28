# ADR: Observability Strategy

| Field         | Value                                         |
| ------------- | --------------------------------------------- |
| **Status**    | Proposed                                      |
| **Context**   | Stage 3 — Backend API Pipeline (P2)           |
| **Decision**  | OpenTelemetry + Prometheus + Grafana + Jaeger |
| **Date**      | YYYY-MM-DD                                    |
| **Authors**   | CIO (primary), Backend Lead                   |
| **Reviewers** | CTO (technology), CSO (security)              |

---

## Decision

We will implement a **three-pillar observability strategy**:

1. **Distributed Tracing** — OpenTelemetry SDK + Jaeger collector
2. **Structured Logging** — JSON-formatted logs with mandatory fields
3. **Metrics Collection** — Prometheus + Grafana with RED/USE methods

## Rationale

Backend API services require comprehensive observability to diagnose production issues, monitor performance SLAs, and maintain service reliability. Without distributed tracing, structured logging, and metrics collection, incident response times increase exponentially, and performance regressions go undetected until users report them.

This ADR establishes the observability stack for all backend API services, ensuring consistent telemetry across REST, GraphQL, gRPC, and event-driven architectures.

## Implementation Details

### 1. Distributed Tracing (OpenTelemetry)

**Technology:** OpenTelemetry SDK + Jaeger/Zipkin collector

**Implementation:**

- Auto-instrumentation for all HTTP/gRPC requests
- Manual instrumentation for business logic boundaries (auth, payment, data processing)
- Trace propagation via W3C Trace Context headers (`traceparent`, `tracestate`)
- Sample rate: 100% in staging, 10% in production (configurable per endpoint)
- Trace retention: 7 days (staging), 30 days (production)

**Trace Structure:**

```
Root Span: POST /api/v1/users/{id}/orders
├─ Span: Authentication middleware (JWT validation)
├─ Span: Authorization check (RBAC)
├─ Span: Database query (PostgreSQL)
│  └─ Span: Query execution (SELECT * FROM orders WHERE user_id = ?)
├─ Span: Cache lookup (Redis)
└─ Span: Response serialization
```

### 2. Structured Logging

**Standard:** JSON-formatted logs with mandatory fields

**Mandatory Log Fields:**

```json
{
  "timestamp": "2026-04-14T10:30:00Z",
  "level": "INFO|WARN|ERROR|FATAL",
  "service": "order-service",
  "version": "1.2.3",
  "trace_id": "abc123...",
  "span_id": "def456...",
  "request_id": "req_789...",
  "user_id": "usr_001",
  "endpoint": "POST /api/v1/orders",
  "method": "POST",
  "status_code": 201,
  "duration_ms": 45,
  "message": "Order created successfully"
}
```

**Log Levels:**

- **DEBUG:** Detailed diagnostic information (disabled in production)
- **INFO:** Normal operational events (request received, order created)
- **WARN:** Unexpected but handled conditions (rate limit approaching, cache miss)
- **ERROR:** Request failures, database errors, external service timeouts
- **FATAL:** Service crash, unrecoverable state (triggers immediate alert)

**Retention Policy:**

- DEBUG/INFO: 7 days
- WARN: 30 days
- ERROR/FATAL: 90 days (compliance requirement)

### 3. Metrics Collection (Prometheus + Grafana)

**Metrics Categories:**

#### RED Method (Request-centric):

- `http_requests_total{method, endpoint, status_code}` — Request count
- `http_request_duration_seconds{method, endpoint, quantile}` — Latency distribution (p50, p95, p99)
- `http_request_size_bytes{method, endpoint}` — Request payload size
- `http_response_size_bytes{method, endpoint}` — Response payload size

#### USE Method (Resource-centric):

- `node_cpu_usage_percent` — CPU utilization
- `node_memory_usage_bytes` — Memory consumption
- `node_disk_io_time_seconds` — Disk I/O latency
- `postgres_connections_active` — Database connection pool usage
- `redis_connected_clients` — Redis client connections

#### Business Metrics:

- `orders_created_total{payment_method}` — Order volume by payment type
- `authentication_failures_total{reason}` — Auth failure breakdown
- `rate_limit_exceeded_total{endpoint}` — Rate limiting triggers

**Scrape Interval:** 15 seconds  
**Retention:** 90 days (raw metrics), 1 year (aggregated hourly/daily)

---

## SLO Error Budgets

**Service-Level Objectives (SLOs):**

| Metric                      | Target   | Error Budget (Monthly) | Alert Threshold |
| --------------------------- | -------- | ---------------------- | --------------- |
| Availability                | 99.9%    | 43m 49s downtime       | 99.8%           |
| P99 Latency (critical APIs) | <200ms   | 14h 24m >200ms         | 250ms           |
| P99 Latency (standard APIs) | <500ms   | 35h 60m >500ms         | 600ms           |
| Error Rate                  | <0.1%    | 43m 49s error time     | 0.2%            |
| Throughput                  | >10k rps | N/A                    | <8k rps         |

**Error Budget Burn Rate Alerts:**

- **Fast burn (>14.4x):** Page on-call engineer immediately (implies <2 hours to exhaust monthly budget)
- **Slow burn (>1x):** Notify team via Slack (implies <30 days to exhaust monthly budget)

---

## Alternatives Considered

### Alternative 1: Proprietary APM (DataDog/New Relic)

**Pros:** Turnkey solution, built-in dashboards, anomaly detection  
**Cons:** Vendor lock-in, $15-30/host/month cost, data egress fees  
**Rejected because:** Open-source stack provides equivalent functionality at 1/10th cost with full data ownership.

### Alternative 2: ELK Stack (Elasticsearch + Logstash + Kibana)

**Pros:** Powerful log aggregation, flexible querying  
**Cons:** High resource overhead (Elasticsearch requires 8GB+ RAM per node), complex scaling  
**Rejected because:** Prometheus + Grafana + Loki (log aggregation) is lighter-weight and better suited for our scale (<100 services).

### Alternative 3: No Distributed Tracing

**Pros:** Simpler architecture, lower overhead  
**Cons:** Impossible to debug cross-service latency, blind spots in microservice communication  
**Rejected because:** Violates SRD requirement for "full request lifecycle visibility."

---

## Consequences

### Positive

- **Incident MTTR reduced by 60%** — Traces pinpoint exact failure point in <5 minutes vs. 30+ minutes of log grepping
- **Performance regression detection** — Automated alerts when P99 latency exceeds SLO thresholds
- **Capacity planning** — Historical metrics inform infrastructure scaling decisions
- **Compliance audit trail** — Structured logs provide immutable record of all API requests (GDPR Article 30)

### Negative

- **Operational overhead** — Team must maintain Prometheus, Grafana, Jaeger clusters (~4 hours/week)
- **Storage costs** — 90-day metric retention + 30-day trace retention requires ~500GB storage/month
- **Learning curve** — Engineers must understand OpenTelemetry instrumentation patterns (2-week ramp-up)

### Risks & Mitigations

| Risk                          | Likelihood | Impact | Mitigation                                                                   |
| ----------------------------- | ---------- | ------ | ---------------------------------------------------------------------------- |
| Trace sampling misses bugs    | Medium     | High   | 100% sampling for error traces, configurable per-endpoint                    |
| Metrics cardinality explosion | Medium     | Medium | Enforce label limits (max 10 labels/metric), reject high-cardinality metrics |
| Grafana dashboard sprawl      | High       | Low    | Dashboard governance policy (max 5 dashboards/service, quarterly review)     |

---

## Implementation Plan

**Phase 1 (Week 1-2):** Infrastructure setup

- Deploy Prometheus + Grafana + Jaeger on Kubernetes
- Configure scrape targets, alerting rules, retention policies
- Create baseline dashboards (RED method, USE method)

**Phase 2 (Week 3-4):** SDK integration

- Add OpenTelemetry SDK to all backend services
- Instrument critical endpoints (auth, payment, data processing)
- Enable trace propagation headers

**Phase 3 (Week 5-6):** Logging standardization

- Migrate all services to JSON structured logging
- Add mandatory fields (trace_id, span_id, request_id)
- Configure log aggregation (Loki or CloudWatch Logs)

**Phase 4 (Week 7-8):** SLO definition & alerting

- Define SLOs per service tier (critical/standard/internal)
- Configure error budget burn rate alerts
- Train on-call engineers on dashboard interpretation

---

## Compliance Alignment

- **GDPR Article 30:** Structured logs provide processing activity records
- **SOC 2 Type II:** Audit trail of all API access (who, what, when)
- **PCI-DSS Requirement 10:** Log all access to cardholder data
- **SRD Section 4.2:** "Full request lifecycle visibility from ingress to egress"

---

## References

- [OpenTelemetry Specification](https://opentelemetry.io/docs/)
- [Google SRE Workbook: SLOs](https://sre.google/workbook/implementing-slos/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- SRD.md Section 4.2 (Observability Requirements)
