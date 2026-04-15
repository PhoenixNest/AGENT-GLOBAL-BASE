# ADR: Observability Strategy (Cross-Platform)

| Field         | Value                                                               |
| ------------- | ------------------------------------------------------------------- |
| **Status**    | Proposed                                                            |
| **Context**   | Stage 3 — Full-Stack Cross-Platform Pipeline (P3)                   |
| **Decision**  | OpenTelemetry across all platforms + per-platform SLO error budgets |
| **Date**      | YYYY-MM-DD                                                          |
| **Authors**   | CIO (primary), Backend Lead, Mobile Lead, Frontend Lead             |
| **Reviewers** | CTO (technology), CSO (security)                                    |

---

## Decision

We will implement **unified distributed tracing using OpenTelemetry** across web, iOS, Android, and backend with W3C Trace Context propagation, per-platform SLO error budgets, and cross-platform correlation dashboards.

## Rationale

Full-stack cross-platform products generate telemetry across web browsers, iOS devices, Android devices, and backend services. Without unified observability, diagnosing issues that span multiple platforms (e.g., slow API response affecting mobile cold start) becomes impossible. This ADR extends the Backend API Pipeline's `ADR-OBSERVABILITY.md` with cross-platform tracing, per-platform SLO error budgets, and trace correlation strategies.

### 1. Unified Distributed Tracing: OpenTelemetry Across All Platforms

**Technology Stack:**

- **Backend:** OpenTelemetry SDK (Java/Go/Node.js)
- **Web:** OpenTelemetry JavaScript SDK (auto-instrumentation for fetch/XHR)
- **iOS:** OpenTelemetry Swift SDK (manual instrumentation for URLSession)
- **Android:** OpenTelemetry Kotlin SDK (manual instrumentation for OkHttp/Retrofit)
- **Collector:** OpenTelemetry Collector (centralized trace aggregation)
- **Backend:** Jaeger (trace visualization) or Zipkin (lightweight alternative)

**Trace Propagation:**
All platforms use W3C Trace Context headers to maintain trace continuity:

```
Mobile App → Backend API → Database
traceparent: 00-abc123def456-789ghi012jkl-01
             ^  ^           ^          ^
             |  |           |          |
          version trace_id  span_id   flags
```

**Cross-Platform Trace Example:**

```
Root Span: User completes checkout flow
├─ Span: iOS app - "Checkout button tapped" (mobile)
│  ├─ Span: iOS app - "Validate cart" (mobile)
│  └─ Span: iOS app - "POST /api/v1/orders" (network call)
│     └─ Span: Backend API - "POST /api/v1/orders" (server)
│        ├─ Span: Backend - "Authenticate user" (auth middleware)
│        ├─ Span: Backend - "Query database" (PostgreSQL)
│        └─ Span: Backend - "Send confirmation email" (external service)
└─ Span: iOS app - "Display order confirmation" (mobile UI)
```

**Sampling Strategy:**

- **Production:** 10% default, 100% for errors, 100% for critical user journeys (checkout, login)
- **Staging:** 100% sampling (full visibility for debugging)
- **Per-endpoint override:** Critical APIs (payment, auth) always 100% sampled

---

### 2. Structured Logging: Per-Platform Standards

**Common Fields (All Platforms):**

```json
{
  "timestamp": "2026-04-14T10:30:00Z",
  "level": "INFO|WARN|ERROR|FATAL",
  "service": "checkout-service",
  "version": "1.2.3",
  "trace_id": "abc123...",
  "span_id": "def456...",
  "platform": "ios|android|web|backend",
  "user_id": "usr_001",
  "session_id": "sess_789..."
}
```

**Platform-Specific Fields:**

| Platform | Additional Fields                                       |
| -------- | ------------------------------------------------------- |
| Web      | `browser`, `browser_version`, `url`, `referrer`         |
| iOS      | `ios_version`, `device_model`, `app_version`            |
| Android  | `android_version`, `device_manufacturer`, `app_version` |
| Backend  | `endpoint`, `method`, `status_code`, `duration_ms`      |

**Log Aggregation:**

- **Backend:** Loki (lightweight, Prometheus-compatible)
- **Mobile:** Firebase Crashlytics (crash reports) + custom event logging to backend
- **Web:** Sentry (error tracking) + custom events to backend

**Retention Policy:**

- Errors/Fatal: 90 days (compliance requirement)
- Warnings: 30 days
- Info/Debug: 7 days

---

### 3. Metrics Collection: Per-Platform SLO Error Budgets

**Backend SLOs (from Backend ADR-OBSERVABILITY):**

- Availability: 99.9% (43m 49s downtime/month)
- P99 Latency: <200ms (critical APIs), <500ms (standard APIs)
- Error Rate: <0.1%

**Web SLOs (from Web Pipeline):**

- LCP (Largest Contentful Paint): <2.5s
- CLS (Cumulative Layout Shift): <0.1
- TTI (Time to Interactive): <3.8s
- TTFB (Time to First Byte): <800ms

**Mobile SLOs (from Mobile Pipeline):**

- Cold Start: <2s (iOS), <2.5s (Android)
- Frame Rate: ≥60fps (scrolling, animations)
- Memory Usage: <150MB (iOS), <200MB (Android)
- Network Payload: <500KB per screen load

**Error Budget Burn Rate Alerts:**

| Platform | Fast Burn (>14.4x)        | Slow Burn (>1x)            |
| -------- | ------------------------- | -------------------------- |
| Backend  | Page on-call engineer     | Slack notification to team |
| Web      | Alert frontend lead       | Dashboard warning          |
| Mobile   | Alert mobile chapter lead | Weekly report              |

**Cross-Platform Correlation Dashboard:**
Grafana dashboard showing:

- Backend P99 latency vs. mobile cold start time (correlation analysis)
- Web LCP vs. API TTFB (identify if backend slowness impacts web performance)
- Error rate by platform (detect platform-specific regressions)

---

### 4. Per-Platform SLO Error Budget Allocation

**Monthly Error Budget Distribution:**

| Platform | Availability Budget   | Latency Budget            | Error Rate Budget |
| -------- | --------------------- | ------------------------- | ----------------- |
| Backend  | 43m 49s downtime      | 14h 24m >200ms (critical) | 43m 49s errors    |
| Web      | N/A (SPA resilience)  | 2h 55m LCP >2.5s          | 1h 26m JS errors  |
| iOS      | N/A (offline support) | 1h 26m cold start >2s     | 43m crashes       |
| Android  | N/A (offline support) | 2h 8m cold start >2.5s    | 43m crashes       |

**Budget Exhaustion Policy:**

- **>50% budget consumed:** Freeze feature deployments, focus on reliability
- **>75% budget consumed:** Emergency incident review, rollback recent changes
- **100% budget exhausted:** All-hands reliability sprint, no new features until budget resets

---

## Alternatives Considered

### Alternative 1: Platform-Specific Observability Silos

**Pros:** Simpler per-platform setup, team autonomy  
**Cons:** Impossible to diagnose cross-platform issues, duplicated effort, inconsistent metrics  
**Rejected because:** Violates principle of "unified product experience"; mobile perf issues caused by backend slowness go undetected.

### Alternative 2: Commercial APM Suite (DataDog/New Relic)

**Pros:** Turnkey solution, built-in cross-platform dashboards, anomaly detection  
**Cons:** $30-50/host/month cost ($15k+/month at scale), vendor lock-in, data egress fees  
**Rejected because:** Open-source stack provides equivalent functionality at 1/10th cost with full data ownership.

### Alternative 3: No Mobile Instrumentation

**Pros:** Lower overhead, simpler backend-only monitoring  
**Cons:** Blind spots in mobile user experience, crashes go undetected until App Store reviews  
**Rejected because:** Mobile represents 60%+ of user base; SRD requires "full request lifecycle visibility from client to server."

---

## Consequences

### Positive

- **End-to-end visibility** — Trace user journey from mobile tap → API call → database query → response rendering
- **Cross-platform correlation** — Identify if backend latency spike causes mobile cold start regression
- **Unified alerting** — Single Grafana dashboard shows health across all platforms
- **Compliance audit trail** — Structured logs provide immutable record of all user actions (GDPR Article 30)

### Negative

- **Instrumentation overhead** — Engineers must add manual spans for business logic (~10% development time)
- **Storage costs** — Cross-platform traces require ~1TB storage/month (vs. 500GB backend-only)
- **Complexity** — Team must understand OpenTelemetry SDKs for 4 platforms (learning curve: 2-3 weeks)

### Risks & Mitigations

| Risk                                      | Likelihood | Impact   | Mitigation                                                                                               |
| ----------------------------------------- | ---------- | -------- | -------------------------------------------------------------------------------------------------------- |
| Trace context lost at platform boundaries | Medium     | High     | Enforce W3C Trace Context header propagation in CI gate, integration tests verify trace continuity       |
| Mobile SDK increases app size             | Medium     | Medium   | OpenTelemetry SDK adds ~200KB (iOS), ~150KB (Android); acceptable within bundle budget                   |
| Metric cardinality explosion              | High       | Medium   | Enforce label limits (max 10 labels/metric), reject high-cardinality metrics in collector                |
| Privacy concerns (PII in logs)            | Low        | Critical | Automated PII scrubbing (regex patterns for emails, phone numbers, credit cards), GDPR compliance review |

---

## Implementation Plan

**Phase 1 (Week 1-2):** Backend tracing foundation

- Deploy OpenTelemetry Collector + Jaeger
- Instrument backend services with auto-instrumentation
- Configure trace sampling (10% production, 100% staging)

**Phase 2 (Week 3-4):** Mobile SDK integration

- Add OpenTelemetry Swift SDK to iOS app
- Add OpenTelemetry Kotlin SDK to Android app
- Instrument critical user journeys (login, checkout, search)
- Implement trace propagation headers (W3C Trace Context)

**Phase 3 (Week 5-6):** Web instrumentation

- Add OpenTelemetry JavaScript SDK to web app
- Auto-instrument fetch/XHR requests
- Configure trace propagation from browser to backend

**Phase 4 (Week 7-8):** Cross-platform dashboards

- Build Grafana dashboard correlating backend P99 vs. mobile cold start
- Configure per-platform SLO error budget alerts
- Train teams on trace interpretation, dashboard usage

---

## Compliance Alignment

- **GDPR Article 30:** Structured logs provide processing activity records across all platforms
- **SOC 2 Type II:** Audit trail of all user actions (web clicks, mobile taps, API calls)
- **PCI-DSS Requirement 10:** Log all access to cardholder data (backend + mobile payment flows)
- **SRD Section 7.2:** "Distributed tracing across all platforms with trace correlation"

---

## References

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [W3C Trace Context Specification](https://www.w3.org/TR/trace-context/)
- [Google SRE Workbook: SLOs](https://sre.google/workbook/implementing-slos/)
- [Mobile Performance Monitoring Best Practices](https://developer.apple.com/documentation/os/logging)
- SRD.md Section 7.2 (Cross-Platform Observability Requirements)

---

**Lock-down:** Once approved at Stage 3 gate, this decision is locked — switching between strategies requires a full Stage 3 re-entry with ADR re-authorship and Implementation Plan re-baseline.
