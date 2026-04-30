# ADR: Web Application Observability

**Project:** [Project Name]
**ADR ID:** ADR-[NNN]
**Status:** Proposed | Accepted | Superseded
**Author:** CTO (Dr. Kenji Nakamura) + CIO (Dr. Priya Mehta)
**Date:** YYYY-MM-DD
**Pipeline:** Web Application

---

## Context

The web application requires an observability strategy covering frontend performance, backend API health, error tracking, and real-user monitoring. Without a defined observability architecture, teams make ad-hoc tool choices, creating monitoring gaps and alert fatigue. This ADR is a mandatory Stage 3 deliverable for all web projects and locks the observability stack before implementation begins.

PRD performance SLAs (LCP < 2.5s, INP < 200ms, CLS < 0.1, TTFB < 800ms) cannot be reliably verified at Stage 7 without the monitoring infrastructure defined here.

---

## Decision

### 1. Real User Monitoring (RUM) — Frontend

| Decision                    | Detail                                                              |
| --------------------------- | ------------------------------------------------------------------- |
| **RUM provider**            | [Vercel Web Analytics / Sentry Performance / Datadog RUM / Custom]  |
| **Core Web Vitals tracked** | LCP, INP, CLS, TTFB, FCP — all pages                                |
| **Session sampling rate**   | [100% for errors; 10% for performance — adjust for traffic volume]  |
| **User session replay**     | [Enabled / Disabled — PII masking required if enabled]              |
| **Custom metrics**          | [Application-specific metrics from PRD §6 Performance Requirements] |

### 2. Error Tracking

| Decision                    | Detail                                                          |
| --------------------------- | --------------------------------------------------------------- |
| **Error tracking provider** | [Sentry / Datadog / Rollbar]                                    |
| **Source maps**             | Uploaded to error tracking provider per deploy (non-public)     |
| **Release tracking**        | Each deploy tagged with version; regression detection active    |
| **User impact grouping**    | Errors grouped by impacted user count for triage prioritisation |
| **PII scrubbing**           | All user-identifying data stripped before upload                |
| **Alert routing**           | P0/P1 errors → on-call PagerDuty; P2/P3 → team Slack channel    |

### 3. Backend API Observability

| Signal                     | Tooling                          | Retention | Alerting Threshold            |
| -------------------------- | -------------------------------- | --------- | ----------------------------- |
| Request latency (P50/P99)  | [Prometheus + Grafana / Datadog] | 30 days   | P99 > [X] ms → Sev2 alert     |
| Error rate (5xx)           | Same                             | 30 days   | > 0.5% → Sev2; > 1% → Sev1    |
| Throughput (RPS)           | Same                             | 30 days   | > [N] RPS → capacity alert    |
| Database query latency     | APM trace sampling               | 7 days    | P99 > [X] ms → DB team alert  |
| External dependency health | HTTP health checks every 30s     | 7 days    | 2 consecutive failures → Sev2 |

### 4. Structured Logging

| Decision            | Detail                                                                       |
| ------------------- | ---------------------------------------------------------------------------- |
| **Log format**      | JSON structured logging — no unstructured text                               |
| **Required fields** | `timestamp`, `level`, `service`, `trace_id`, `span_id`, `message`            |
| **Log levels used** | `ERROR`, `WARN`, `INFO`, `DEBUG` (DEBUG disabled in production)              |
| **PII in logs**     | Prohibited — SAST rule enforced; no user IDs, emails, tokens in log messages |
| **Log aggregation** | [Elasticsearch + Kibana / Datadog Logs / CloudWatch Logs]                    |
| **Retention**       | ERROR/WARN: 90 days; INFO: 30 days; DEBUG: 7 days (dev/staging only)         |

### 5. Distributed Tracing (if applicable)

| Decision              | Detail                                                             |
| --------------------- | ------------------------------------------------------------------ |
| **Required**          | [Yes — if backend API spans multiple services; No — if monolithic] |
| **Standard**          | OpenTelemetry (vendor-neutral)                                     |
| **Trace propagation** | W3C Trace Context header (`traceparent`)                           |
| **Sampling rate**     | [1% of requests in production; 100% on error]                      |
| **Backend**           | [Jaeger / Zipkin / Datadog APM / Honeycomb]                        |

### 6. Alerting and Incident Response

| Severity  | Trigger Condition                                   | Channel           | Responder | SLA     |
| --------- | --------------------------------------------------- | ----------------- | --------- | ------- |
| Sev1 (P0) | Error rate > 1% OR P99 latency > 5s for > 2 min     | PagerDuty         | On-call   | 5 min   |
| Sev2 (P1) | Error rate > 0.5% OR Core Web Vital regressed > 20% | Slack #incidents  | Team      | 30 min  |
| Sev3 (P2) | Any metric outside SLA for > 15 min                 | Slack #monitoring | Team      | 4 hours |

Full incident response procedure: `company/pipeline/_base/incident-response.md`

### 7. Performance Budgets (CI-Enforced)

| Metric                       | Budget        | CI Action on Breach  |
| ---------------------------- | ------------- | -------------------- |
| LCP                          | < 2.5s        | Block PR merge       |
| INP                          | < 200ms       | Block PR merge       |
| CLS                          | < 0.1         | Block PR merge       |
| JS bundle size (initial)     | < 200 KB gzip | Block PR merge       |
| Total page weight (initial)  | < 1 MB        | Warn                 |
| Lighthouse Performance score | ≥ 90          | Warn (block at < 80) |

**Tooling:** Lighthouse CI in GitHub Actions; `lighthouse-budget.json` committed to repository.

### 8. Synthetic Monitoring

| Check                                   | Frequency | Locations    | Alert                     |
| --------------------------------------- | --------- | ------------ | ------------------------- |
| Homepage availability                   | 1 min     | [3+ regions] | On failure                |
| Critical user flow (login + key action) | 5 min     | [3+ regions] | On failure                |
| API health endpoint                     | 30 s      | [3+ regions] | On 2 consecutive failures |

---

## Rationale

[Explain key tool choices — e.g., why OpenTelemetry over vendor-specific, why Sentry over alternatives, why Prometheus/Grafana over managed APM, etc.]

---

## Trade-offs

| Benefit                                             | Cost                                             |
| --------------------------------------------------- | ------------------------------------------------ |
| Real-time visibility into user-impacting issues     | Additional complexity and per-event/seat cost    |
| Structured logging enables fast querying            | Discipline required from all developers          |
| CI-enforced performance budgets prevents regression | Build time addition (~2–3 min for Lighthouse CI) |

---

## Compliance Implications

- GDPR Article 25 (Data Protection by Design): RUM session replay requires PII masking configuration
- SOC 2 Type II: Log retention and access controls required

---

## Sign-Off

| Role | Name               | Decision   | Date       |
| ---- | ------------------ | ---------- | ---------- |
| CTO  | Dr. Kenji Nakamura | ☐ Accepted | YYYY-MM-DD |
| CIO  | Dr. Priya Mehta    | ☐ Accepted | YYYY-MM-DD |
| CSO  | Dr. Sarah Chen     | ☐ Accepted | YYYY-MM-DD |
