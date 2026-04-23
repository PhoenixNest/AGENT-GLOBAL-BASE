# Backend Observability

**Category:** Backend Engineering
**Owner:** Senior Backend Engineer

## Overview

This skill defines the standards and practices for implementing comprehensive observability across backend services, enabling rapid incident detection, root cause analysis, and performance optimization in production environments. It covers the three pillars of observability—logs, metrics, and traces—with production-grade instrumentation patterns using OpenTelemetry, structured logging, distributed tracing, and SLO-driven alerting strategies.

## Competency Dimensions

| Dimension                | Description                                                                              | Proficiency Indicators                                                                                       |
| ------------------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Instrumentation**      | Embedding observability primitives into application code without performance degradation | Automatic instrumentation coverage >80%; custom spans for all critical paths; <2% overhead on p99 latency    |
| **Log Management**       | Structured log production, aggregation, and querying at scale                            | 100% JSON structured logs; correlation IDs in all log lines; log volume <5GB/service/day at production scale |
| **Metrics Engineering**  | Designing metric collections aligned with business and system health                     | RED/USE method coverage for all services; custom business metrics for critical user journeys                 |
| **Distributed Tracing**  | End-to-end request visibility across service boundaries                                  | W3C Trace Context propagation across all hops; trace completeness >95%; span cardinality optimized           |
| **Alerting & SLOs**      | Defining actionable alerts based on error budgets and burn rates                         | False positive rate <5%; alert-to-action ratio >70%; SLO coverage for all customer-facing services           |
| **Production Debugging** | Safe diagnostic techniques without service restarts or code deploys                      | Dynamic log injection <30s latency; feature-flagged debug endpoints with RBAC controls                       |

## Execution Guidance

### The Three Pillars of Observability

Observability is not monitoring. Monitoring tells you when something is wrong; observability enables you to investigate _why_ without predefining every possible failure mode. The three pillars work in concert:

- **Logs** provide discrete, timestamped event records with rich context
- **Metrics** offer aggregatable, time-series data for trend analysis and alerting
- **Traces** map the complete request journey across service boundaries

Each pillar has distinct strengths and cost profiles. Logs are high-cardinality but expensive at scale. Metrics are cheap and aggregatable but lose individual request context. Traces bridge the gap with per-request latency breakdowns but require careful instrumentation discipline.

### Structured Logging

All log output MUST be structured JSON with a consistent schema. Unstructured text logs are prohibited in production services.

**Required fields in every log line:**

```json
{
  "timestamp": "2026-04-04T08:32:15.123Z",
  "level": "ERROR",
  "service": "order-service",
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "span_id": "b7ad6b7169203331",
  "correlation_id": "corr-abc-123-def-456",
  "message": "Payment gateway timeout",
  "duration_ms": 5023,
  "http.status_code": 504,
  "error.type": "TimeoutError",
  "error.stack": "..."
}
```

**Node.js/TypeScript structured logging configuration (Winston + OpenTelemetry):**

```typescript
import winston from 'winston';
import { trace, context } from '@opentelemetry/api';

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DDTHH:mm:ss.SSSZ' }),
    winston.format((info) => {
      const span = trace.getSpan(context.active());
      if (span) {
        const spanContext = span.spanContext();
        info.trace_id = spanContext.traceId;
        info.span_id = spanContext.spanId;
      }
      return info;
    })(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: process.env.SERVICE_NAME,
    environment: process.env.NODE_ENV,
  },
  transports: [
    new winston.transports.Console({
      level: process.env.LOG_LEVEL || 'info',
    }),
  ],
});

// Usage with correlation ID propagation
export function createRequestLogger(req: Request) {
  const correlationId = req.headers['x-correlation-id'] || crypto.randomUUID();
  return logger.child({ correlation_id: correlationId });
}
```

**Log sampling strategies for cost optimization:**

| Sampling Strategy    | Use Case                                    | Implementation                                                                                   |
| -------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Head-based**       | Reduce volume by fixed percentage           | Configure at log shipper (Fluent Bit, Vector) with 10-20% sample rate for INFO/DEBUG             |
| **Tail-based**       | Retain interesting traces, drop normal ones | Use OpenTelemetry Collector tail sampler; keep error traces at 100%, success traces at 5%        |
| **Adaptive**         | Increase sampling during incidents          | Dynamic adjustment via feature flags; when error rate >1%, bump sampling to 50%                  |
| **Log-level gating** | Different retention per severity            | ERROR/CRITICAL: 100% retention, 90-day storage; WARN: 30-day storage; INFO/DEBUG: 7-day, sampled |

### Distributed Tracing with OpenTelemetry

**OpenTelemetry SDK initialization (Node.js/TypeScript):**

```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { W3CTraceContextPropagator } from '@opentelemetry/core';
import { propagation } from '@opentelemetry/api';

// Set global propagator for W3C Trace Context
propagation.setGlobalPropagator(new W3CTraceContextPropagator());

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: process.env.SERVICE_NAME || 'unknown-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: process.env.SERVICE_VERSION || '0.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV || 'development',
    'host.name': process.env.HOSTNAME,
    'k8s.pod.name': process.env.POD_NAME,
    'k8s.namespace.name': process.env.NAMESPACE,
  }),
  spanProcessor: new BatchSpanProcessor(
    new OTLPTraceExporter({
      url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://otel-collector:4318/v1/traces',
      headers: {
        'x-otlp-api-key': process.env.OTEL_API_KEY || '',
      },
    }),
    {
      maxQueueSize: 2048,
      maxExportBatchSize: 512,
      scheduledDelayMillis: 5000,
    }
  ),
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-http': {
        ignoreIncomingRequestHook: (req) => {
          // Exclude health checks from tracing
          return req.url === '/health' || req.url === '/ready';
        },
      },
      '@opentelemetry/instrumentation-pg': {
        enhanceDatabaseStatements: true,
      },
    }),
  ],
  sampler: {
    // Always sample errors, probabilistically sample everything else
    shouldSample: (context, traceId, spanName, spanKind, attributes, links) => {
      const errorRate = getRecentErrorRate();
      if (errorRate > 0.01) return { decision: 2 }; // ALWAYS_ON
      return Math.random() < 0.1 ? { decision: 2 } : { decision: 1 }; // 10% sample rate
    },
  },
});

sdk.start();
```

**Trace context propagation across service boundaries:**

W3C Trace Context is the industry standard for propagating trace information between services. It uses two HTTP headers:

- `traceparent`: Contains version, trace ID, span ID, and trace flags
- `tracestate`: Vendor-specific extensions (optional)

**Outgoing request instrumentation (injecting context):**

```typescript
import { trace, propagation, context } from '@opentelemetry/api';

async function callDownstreamService(url: string, payload: any) {
  const activeSpan = trace.getSpan(context.active());

  // Create child span for this outgoing call
  const childSpan = trace.getTracer('order-service').startSpan('call-payment-gateway', {
    attributes: {
      'http.url': url,
      'http.method': 'POST',
      'payment.amount': payload.amount,
      'payment.currency': payload.currency,
    },
  });

  // Inject trace context into headers
  const headers: Record<string, string> = {};
  propagation.inject(context.active(), headers);

  // Add correlation ID for log aggregation
  headers['x-correlation-id'] = activeSpan?.spanContext().traceId || crypto.randomUUID();

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        ...headers,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    childSpan.setAttributes({
      'http.status_code': response.status,
      'http.response_content_length': response.headers.get('content-length') || '0',
    });

    if (!response.ok) {
      childSpan.recordException(new Error(`HTTP ${response.status}: ${response.statusText}`));
      childSpan.setStatus({ code: 2, message: `HTTP ${response.status}` }); // ERROR
    }

    return response;
  } catch (error) {
    childSpan.recordException(error as Error);
    childSpan.setStatus({ code: 2, message: (error as Error).message });
    throw error;
  } finally {
    childSpan.end();
  }
}
```

**Incoming request instrumentation (extracting context):**

```typescript
import { trace, propagation, context } from '@opentelemetry/api';
import { TraceFlags } from '@opentelemetry/api';

function createSpanFromIncomingRequest(req: Request, tracerName: string) {
  const tracer = trace.getTracer(tracerName);

  // Extract parent context from headers
  const parentContext = propagation.extract(context.active(), {
    traceparent: req.headers.get('traceparent') || '',
    tracestate: req.headers.get('tracestate') || '',
    'x-correlation-id': req.headers.get('x-correlation-id') || '',
  });

  // Parse traceparent header manually for validation
  const traceparent = req.headers.get('traceparent');
  let parentSpanId: string | undefined;
  let traceId: string | undefined;

  if (traceparent) {
    const parts = traceparent.split('-');
    if (parts.length === 4) {
      traceId = parts[1];
      parentSpanId = parts[2];
    }
  }

  // Create span with explicit parent
  return tracer.startSpan(
    `${req.method} ${req.url.pathname}`,
    {
      kind: 1, // SERVER
      attributes: {
        'http.method': req.method,
        'http.url': req.url.toString(),
        'http.user_agent': req.headers.get('user-agent'),
        'http.client_ip': req.headers.get('x-forwarded-for'),
        'http.request_content_length': req.headers.get('content-length'),
        'service.name': process.env.SERVICE_NAME,
      },
    },
    parentContext
  );
}
```

### Metrics Collection

**RED Method (Request-oriented services):**

| Metric       | Description                  | Prometheus Name                 | Type      |
| ------------ | ---------------------------- | ------------------------------- | --------- |
| **Rate**     | Requests per second          | `http_requests_total`           | Counter   |
| **Errors**   | Failed requests per second   | `http_errors_total`             | Counter   |
| **Duration** | Request latency distribution | `http_request_duration_seconds` | Histogram |

**USE Method (Resource-oriented systems):**

| Metric          | Description              | Prometheus Name                            | Type    |
| --------------- | ------------------------ | ------------------------------------------ | ------- |
| **Utilization** | % time resource was busy | `node_cpu_utilization_ratio`               | Gauge   |
| **Saturation**  | Queue depth / wait time  | `node_load1`, `node_disk_io_time_weighted` | Gauge   |
| **Errors**      | Error count              | `node_disk_errors_total`                   | Counter |

**Prometheus/Grafana Agent metrics configuration:**

```yaml
metrics:
  global:
    scrape_interval: 15s
    evaluation_interval: 15s

  scrape_configs:
    - job_name: 'node-exporter'
      static_configs:
        - targets: ['node-exporter:9100']
          labels:
            cluster: 'production'

    - job_name: 'application'
      metrics_path: '/metrics'
      static_configs:
        - targets: ['order-service:3000', 'payment-service:3001']
          labels:
            cluster: 'production'

    - job_name: 'otel-collector'
      static_configs:
        - targets: ['otel-collector:8888']

  # Recording rules for RED method
  rules:
    - record: job:http_requests:rate5m
      expr: rate(http_requests_total[5m])
    - record: job:http_errors:rate5m
      expr: rate(http_errors_total[5m])
    - record: job:http_error_rate:ratio5m
      expr: job:http_errors:rate5m / job:http_requests:rate5m
    - record: job:http_request_duration:p50
      expr: histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))
    - record: job:http_request_duration:p95
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
    - record: job:http_request_duration:p99
      expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

### SLO-Based Alerting Strategy

**Define SLOs before alerts. Alerts should fire when error budget burn rate exceeds thresholds.**

| Service            | SLO Target | Error Budget   | Measurement Window |
| ------------------ | ---------- | -------------- | ------------------ |
| API Availability   | 99.9%      | 43.8 min/month | 28 days            |
| API Latency (p95)  | <500ms     | N/A            | Rolling 5 min      |
| Payment Processing | 99.95%     | 21.9 min/month | 28 days            |
| Order Creation     | 99.9%      | 43.8 min/month | 28 days            |

**Multi-window, multi-burn-rate alerting (Google SRE methodology):**

```yaml
groups:
  - name: slo-burn-rate-alerts
    rules:
      # Page: 14.4x burn rate over 5 min (exhausts budget in 2 days)
      - alert: SLOErrorBudgetBurnRateCritical
        expr: |
          (
            (1 - (rate(http_requests_total{code=~"5.."}[5m]) / rate(http_requests_total[5m]))) / (1 - 0.999)
          ) > 14.4
        for: 5m
        labels:
          severity: critical
          team: backend-oncall
        annotations:
          summary: 'Error budget burn rate is {{ $value }}x (critical)'
          description: 'Service {{ $labels.service }} is burning error budget at {{ $value }}x normal rate. Page immediately.'
          runbook_url: 'https://runbooks.internal/slo-burn-critical'

      # Page: 6x burn rate over 30 min (exhausts budget in 5 days)
      - alert: SLOErrorBudgetBurnRateHigh
        expr: |
          (
            (1 - (rate(http_requests_total{code=~"5.."}[30m]) / rate(http_requests_total[30m]))) / (1 - 0.999)
          ) > 6
        for: 30m
        labels:
          severity: warning
          team: backend-oncall
        annotations:
          summary: 'Error budget burn rate is {{ $value }}x (high)'
          description: 'Service {{ $labels.service }} is burning error budget at {{ $value }}x normal rate. Investigate within 1 hour.'

      # Page: 1x burn rate over 6 hours (exhausts budget in 30 days)
      - alert: SLOErrorBudgetBurnRateSustained
        expr: |
          (
            (1 - (rate(http_requests_total{code=~"5.."}[6h]) / rate(http_requests_total[6h]))) / (1 - 0.999)
          ) > 1
        for: 6h
        labels:
          severity: warning
          team: backend-oncall
        annotations:
          summary: 'Error budget burn rate is {{ $value }}x (sustained)'
          description: 'Service {{ $labels.service }} is burning error budget at {{ $value }}x normal rate over 6 hours. Review during business hours.'
```

**Alert quality checklist:**

- [ ] Every alert has a documented runbook
- [ ] Alert fires for actionable conditions only (no "FYI" alerts)
- [ ] Alert includes sufficient context for first responder (service, environment, error rate, recent changes)
- [ ] False positive rate <5% over rolling 30 days
- [ ] Mean time to acknowledge (MTTA) <5 min for critical, <30 min for warning
- [ ] Mean time to resolution (MTTR) tracked and trending downward

### Log Aggregation Architecture

**ELK Stack (Elasticsearch, Logstash, Kibana):**

Best suited for teams requiring full-text search, complex analytics, and mature Kibana visualizations. Elasticsearch is resource-intensive but offers unmatched query flexibility.

```
Application → Fluent Bit (log shipper) → Kafka (buffer) → Logstash (processing) → Elasticsearch → Kibana
```

**Grafana Loki:**

Best suited for teams already using Grafana/Prometheus. Loki indexes only labels (not full text), making it 5-10x more storage-efficient than ELK. Query with LogQL, which is syntactically similar to PromQL.

```
Application → Promtail (log shipper) → Loki → Grafana (query + visualize)
```

**Comparison matrix:**

| Criterion           | ELK Stack                | Grafana Loki            |
| ------------------- | ------------------------ | ----------------------- |
| Indexing            | Full-text index          | Labels only             |
| Storage cost        | High (3-5x raw log size) | Low (1-2x raw log size) |
| Query flexibility   | Excellent (Lucene)       | Good (LogQL)            |
| Grafana integration | Via plugin               | Native                  |
| Learning curve      | Steep                    | Moderate                |
| Scale ceiling       | 100+ TB with tuning      | 50+ TB out of box       |

**Recommendation:** Use Loki for greenfield projects with existing Grafana/Prometheus investments. Use ELK when full-text search on unstructured logs is a hard requirement.

### Distributed Tracing Backends

| Backend         | Type                              | Best For                                             | Cost                              |
| --------------- | --------------------------------- | ---------------------------------------------------- | --------------------------------- |
| **Jaeger**      | Open-source, CNCF                 | On-premises, self-managed, high-volume               | Infrastructure cost only          |
| **Zipkin**      | Open-source, CNCF                 | Simple deployments, Twitter ecosystem                | Infrastructure cost only          |
| **Honeycomb**   | SaaS (Observability-as-a-Service) | High-cardinality analysis, BubbleUp, derived columns | Per-event pricing (~$0.003/event) |
| **Datadog APM** | SaaS                              | Teams already using Datadog for infra monitoring     | Per-host + per-span pricing       |
| **New Relic**   | SaaS                              | Full-stack observability (APM + infra + logs + RUM)  | Per-user + data ingestion         |

**Jaeger deployment (docker-compose for development):**

```yaml
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:1.56
    ports:
      - '16686:16686' # UI
      - '4317:4317' # OTLP gRPC
      - '4318:4318' # OTLP HTTP
      - '5775:5775/udp' # Zipkin compat
    environment:
      - COLLECTOR_OTLP_ENABLED=true
      - LOG_LEVEL=debug
      - SPAN_STORAGE_TYPE=memory
```

### Error Tracking with Sentry

**Sentry SDK initialization (Node.js):**

```typescript
import * as Sentry from '@sentry/node';
import { nodeProfilingIntegration } from '@sentry/profiling-node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  release: `${process.env.SERVICE_NAME}@${process.env.SERVICE_VERSION}`,
  integrations: [
    // Enable HTTP/Auto tracing
    Sentry.httpIntegration(),
    Sentry.expressIntegration(),
    // Profiling for performance analysis
    nodeProfilingIntegration(),
  ],
  // Performance monitoring
  tracesSampleRate: 0.1,
  // Sampling rate for profiles (relative to tracesSampleRate)
  profilesSampleRate: 1.0,
  // Capture unhandled promise rejections
  captureUnhandledRejections: true,
  // Breadcrumbs for context
  maxBreadcrumbs: 100,
  // Attach stack traces to all messages
  attachStacktrace: true,
  beforeSend(event) {
    // Filter out sensitive data
    if (event.request?.headers) {
      delete event.request.headers['authorization'];
      delete event.request.headers['cookie'];
    }
    // Filter known noise (e.g., client-side abort errors)
    if (event.exception?.values?.[0]?.value?.includes('AbortError')) {
      return null;
    }
    return event;
  },
});

// Custom error context
function reportError(error: Error, context?: Record<string, any>) {
  Sentry.withScope((scope) => {
    scope.setTags({
      'error.category': context?.category || 'unhandled',
      'error.source': context?.source || 'unknown',
    });
    scope.setExtras(context || {});
    scope.setUser({
      id: context?.userId,
      email: context?.userEmail,
    });
    Sentry.captureException(error);
  });
}
```

### Dashboard Design with Grafana

**Grafana dashboard JSON for API Service Health (RED Method):**

```json
{
  "dashboard": {
    "id": null,
    "uid": "api-service-health",
    "title": "API Service Health — RED Method",
    "tags": ["backend", "api", "red-method", "slo"],
    "timezone": "browser",
    "time": { "from": "now-6h", "to": "now" },
    "refresh": "30s",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate (RPS)",
        "type": "timeseries",
        "gridPos": { "h": 8, "w": 12, "x": 0, "y": 0 },
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{service=\"$service\"}[5m])) by (status_code)",
            "legendFormat": "{{status_code}}",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "reqps",
            "thresholds": {
              "steps": [
                { "color": "green", "value": null },
                { "color": "yellow", "value": 500 },
                { "color": "red", "value": 1000 }
              ]
            }
          }
        }
      },
      {
        "id": 2,
        "title": "Error Rate (%)",
        "type": "timeseries",
        "gridPos": { "h": 8, "w": 12, "x": 12, "y": 0 },
        "targets": [
          {
            "expr": "sum(rate(http_errors_total{service=\"$service\"}[5m])) / sum(rate(http_requests_total{service=\"$service\"}[5m])) * 100",
            "legendFormat": "Error Rate",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "steps": [
                { "color": "green", "value": null },
                { "color": "yellow", "value": 0.1 },
                { "color": "red", "value": 1.0 }
              ]
            },
            "links": [
              {
                "title": "View in Jaeger",
                "url": "http://jaeger.internal/search?service=${service}&lookback=1h",
                "targetBlank": true
              }
            ]
          }
        },
        "alert": {
          "name": "High Error Rate",
          "condition": "A",
          "evaluator": { "params": [1], "type": "gt" },
          "frequency": "1m",
          "handler": 1,
          "notifications": [{ "uid": "backend-oncall-pagerduty" }]
        }
      },
      {
        "id": 3,
        "title": "Latency Percentiles (p50, p95, p99)",
        "type": "timeseries",
        "gridPos": { "h": 8, "w": 24, "x": 0, "y": 8 },
        "targets": [
          {
            "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{service=\"$service\"}[5m]))",
            "legendFormat": "p50",
            "refId": "A"
          },
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{service=\"$service\"}[5m]))",
            "legendFormat": "p95",
            "refId": "B"
          },
          {
            "expr": "histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{service=\"$service\"}[5m]))",
            "legendFormat": "p99",
            "refId": "C"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "s",
            "thresholds": {
              "steps": [
                { "color": "green", "value": null },
                { "color": "yellow", "value": 0.3 },
                { "color": "red", "value": 0.5 }
              ]
            }
          }
        }
      },
      {
        "id": 4,
        "title": "SLO Error Budget Remaining",
        "type": "stat",
        "gridPos": { "h": 4, "w": 6, "x": 0, "y": 16 },
        "targets": [
          {
            "expr": "1 - (sum(increase(http_errors_total{service=\"$service\"}[28d])) / sum(increase(http_requests_total{service=\"$service\"}[28d]))) / (1 - 0.999)",
            "legendFormat": "Budget Remaining",
            "refId": "A"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "thresholds": {
              "steps": [
                { "color": "red", "value": null },
                { "color": "yellow", "value": 0.25 },
                { "color": "green", "value": 0.5 }
              ]
            }
          }
        }
      }
    ],
    "templating": {
      "list": [
        {
          "name": "service",
          "type": "query",
          "query": "label_values(http_requests_total, service)",
          "current": { "text": "order-service", "value": "order-service" },
          "refresh": 2,
          "sort": 1
        }
      ]
    }
  }
}
```

### Production Debugging Techniques

**Dynamic log injection without restarts:**

Implement a runtime debug endpoint that temporarily increases log verbosity for specific traces, requests, or users. This MUST be protected by authentication and automatically time-boxed.

```typescript
import { Router } from 'express';
import { FeatureFlags } from '../config/feature-flags';

const debugRouter = Router();

// Protected by admin RBAC middleware
debugRouter.post('/debug/enable', async (req, res) => {
  const { traceId, userId, durationMinutes } = req.body;

  if (durationMinutes > 30) {
    return res.status(400).json({ error: 'Maximum debug duration is 30 minutes' });
  }

  // Set feature flag with TTL
  await FeatureFlags.set('debug.trace.enabled', true, {
    trace_id: traceId,
    user_id: userId,
    expires_at: Date.now() + durationMinutes * 60 * 1000,
    enabled_by: req.user.email,
  });

  res.json({
    message: `Debug mode enabled for ${durationMinutes} minutes`,
    expires_at: new Date(Date.now() + durationMinutes * 60 * 1000).toISOString(),
  });
});

// Auto-expiry check (runs every 60s)
setInterval(async () => {
  const flags = await FeatureFlags.getAll('debug.trace.enabled');
  for (const flag of flags) {
    if (Date.now() > flag.expires_at) {
      await FeatureFlags.delete(flag.key);
      logger.info(`Debug mode auto-disabled: expired flag for trace ${flag.trace_id}`);
    }
  }
}, 60000);
```

**Feature flags for debug mode:**

Debug capabilities MUST be gated behind feature flags with the following properties:

- **Role-based access control:** Only engineers with `backend-oncall` or `engineering-admin` roles can enable
- **Time-boxed:** Maximum 30 minutes per activation; auto-expiry enforced
- **Audit-logged:** Every enable/disable action logged with actor identity, timestamp, and scope
- **Scoped:** Debug mode can target specific traces, users, or endpoints—not blanket service-wide
- **Non-impacting:** Debug mode MUST NOT alter production behavior (no request blocking, no added latency beyond log serialization)

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
