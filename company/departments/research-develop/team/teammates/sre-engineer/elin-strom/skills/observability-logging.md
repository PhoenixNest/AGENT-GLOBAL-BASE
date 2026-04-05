# Observability & Logging

**Category:** Site Reliability Engineering
**Owner:** SRE Engineer (Elin Ström)

## Overview

This skill defines the observability and logging architecture for production systems, covering the ELK Stack (Elasticsearch, Logstash, Kibana), Fluentd log collection, anomaly detection, real-time alerting, and distributed tracing integration. Observability is the foundation of reliable operations — it enables engineers to understand system behavior, detect problems before they impact users, and debug issues efficiently when they occur.

## Competency Dimensions

| Dimension           | Description                                                                                                              | Proficiency Indicators                                                                                    |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| ELK Stack           | Elasticsearch cluster management, Logstash pipeline configuration, Kibana dashboard creation, index lifecycle management | Manages multi-node ELK clusters processing 100GB+/day; dashboards provide actionable operational insights |
| Fluentd             | Log collection, parsing, filtering, buffering, output configuration, Kubernetes integration                              | Collects logs from all services with zero data loss; structured JSON parsing for all log sources          |
| Anomaly Detection   | Statistical anomaly detection, machine learning-based detection, baseline establishment, alert tuning                    | Detects anomalies before they become incidents; false positive rate <5%                                   |
| Real-Time Alerting  | Alert rule design, notification routing, escalation policies, alert correlation, silence management                      | Alerts are actionable and routed to the right person; mean time to detection <1 minute                    |
| Distributed Tracing | Trace collection, span correlation, trace sampling, trace-based alerting, performance bottleneck identification          | End-to-end traces for 100% of requests; trace-log-correlation for debugging                               |

## Execution Guidance

### ELK Stack Architecture

**Deployment Topology:**

```
Log Sources → Fluentd → Kafka → Logstash → Elasticsearch → Kibana
                                             ↓
                                      Index Lifecycle
                                      (Hot → Warm → Cold → Delete)
```

**Elasticsearch Cluster Configuration:**

```yaml
# elasticsearch.yml
cluster.name: production-logging
node.name: es-node-01
node.roles: [master, data, ingest]

path:
  data: /var/lib/elasticsearch
  logs: /var/log/elasticsearch

network.host: 0.0.0.0
http.port: 9200

discovery.seed_hosts: ["es-node-01", "es-node-02", "es-node-03"]
cluster.initial_master_nodes: ["es-node-01", "es-node-02", "es-node-03"]

# Performance tuning
bootstrap.memory_lock: true
thread_pool.write.size: 8
thread_pool.write.queue_size: 500

# Index lifecycle management
xpack.ilm.enabled: true
```

**Index Template:**

```json
{
  "index_patterns": ["logs-*-*"],
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "index.lifecycle.name": "logs-lifecycle-policy",
      "index.lifecycle.rollover_alias": "logs",
      "index.refresh_interval": "5s",
      "index.sort.field": "@timestamp",
      "index.sort.order": "desc"
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "message": { "type": "text", "analyzer": "standard" },
        "level": { "type": "keyword" },
        "service": { "type": "keyword" },
        "trace_id": { "type": "keyword" },
        "span_id": { "type": "keyword" },
        "host": {
          "properties": {
            "name": { "type": "keyword" },
            "ip": { "type": "ip" }
          }
        },
        "http": {
          "properties": {
            "request": {
              "properties": {
                "method": { "type": "keyword" },
                "url": { "type": "keyword" },
                "status_code": { "type": "integer" }
              }
            },
            "response": {
              "properties": {
                "duration_ms": { "type": "float" }
              }
            }
          }
        },
        "error": {
          "properties": {
            "message": { "type": "text" },
            "stack_trace": { "type": "text" },
            "type": { "type": "keyword" }
          }
        }
      }
    }
  }
}
```

**Index Lifecycle Management (ILM):**

```json
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_size": "50gb",
            "max_age": "1d"
          },
          "set_priority": { "priority": 100 }
        }
      },
      "warm": {
        "min_age": "2d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 },
          "set_priority": { "priority": 50 }
        }
      },
      "cold": {
        "min_age": "7d",
        "actions": {
          "set_priority": { "priority": 0 },
          "freeze": {}
        }
      },
      "delete": {
        "min_age": "30d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

### Fluentd Configuration

**Fluentd for Kubernetes:**

```xml
# fluent.conf

# Source: Collect logs from Kubernetes pods
<source>
  @type tail
  path /var/log/containers/*.log
  pos_file /var/log/fluentd-containers.log.pos
  tag kubernetes.*
  read_from_head true

  <parse>
    @type json
    time_key time
    time_format %Y-%m-%dT%H:%M:%S.%NZ
  </parse>
</source>

# Filter: Enrich with Kubernetes metadata
<filter kubernetes.**>
  @type kubernetes_metadata
  @id filter_kube_metadata
  skip_labels false
  skip_container_metadata false
  skip_namespace_metadata false
</filter>

# Filter: Parse structured application logs
<filter kubernetes.var.log.containers.**order-service**.log>
  @type parser
  key_name log
  reserve_data true
  <parse>
    @type json
  </parse>
</filter>

# Filter: Add environment labels
<filter **>
  @type record_transformer
  <record>
    environment production
    cluster us-central1
  </record>
</filter>

# Filter: Remove noisy fields
<filter **>
  @type grep
  <exclude>
    key $.kubernetes.container_name
    pattern ^kube-.*$
  </exclude>
</filter>

# Match: Buffer and send to Elasticsearch
<match kubernetes.**>
  @type elasticsearch
  host elasticsearch.production.svc
  port 9200
  logstash_format true
  logstash_prefix logs
  logstash_dateformat %Y.%m.%d

  <buffer tag, time>
    @type file
    path /var/log/fluentd/buffer
    timekey 5m
    timekey_wait 1m
    chunk_limit_size 8m
    queue_limit_length 256
    retry_max_interval 30
    retry_forever false
    overflow_action block
  </buffer>
</match>

# Match: Route error logs to separate index for alerting
<match **>
  @type copy
  <store>
    @type elasticsearch
    host elasticsearch.production.svc
    logstash_format true
    logstash_prefix errors
    <buffer>
      @type file
      path /var/log/fluentd/error-buffer
    </buffer>
  </store>
  <store>
    @type relabel
    @label @ALERT
  </store>
</match>

<label @ALERT>
  <match **>
    @type copy
    <store>
      @type http
      endpoint https://alerting.company.com/api/v1/alerts
      <format>
        @type json
      </format>
      <buffer>
        flush_interval 10s
      </buffer>
    </store>
  </match>
</label>
```

**Log Format Standard:**

```json
{
  "@timestamp": "2026-04-04T14:32:15.123Z",
  "level": "ERROR",
  "message": "Database connection failed",
  "service": "order-service",
  "version": "2.3.1",
  "environment": "production",
  "trace_id": "abc-123-def-456",
  "span_id": "span-789",
  "host": {
    "name": "order-service-abc123",
    "ip": "10.0.1.15"
  },
  "http": {
    "request": {
      "method": "POST",
      "url": "/api/v1/orders",
      "headers": {
        "user_agent": "Mozilla/5.0..."
      }
    },
    "response": {
      "status_code": 500,
      "duration_ms": 2345
    }
  },
  "error": {
    "message": "connection refused",
    "type": "ConnectionError",
    "stack_trace": "..."
  },
  "db": {
    "query": "SELECT * FROM orders WHERE id = $1",
    "duration_ms": 5000,
    "rows_affected": 0
  }
}
```

### Anomaly Detection

**Statistical Anomaly Detection:**

```python
# anomaly_detector.py
import numpy as np
from scipy import stats
from datetime import datetime, timedelta

class AnomalyDetector:
    def __init__(self, lookback_hours=24, sensitivity=3.0):
        self.lookback = timedelta(hours=lookback_hours)
        self.sensitivity = sensitivity  # Standard deviations

    def detect_anomaly(self, metric_name, current_value, historical_data):
        """
        Detect if current value is anomalous compared to historical baseline.
        Uses z-score method for normally distributed metrics.
        """
        if len(historical_data) < 30:
            return False, "Insufficient historical data"

        mean = np.mean(historical_data)
        std = np.std(historical_data)

        if std == 0:
            # No variation — any change is anomalous
            is_anomaly = current_value != mean
        else:
            z_score = abs(current_value - mean) / std
            is_anomaly = z_score > self.sensitivity

        return is_anomaly, {
            "mean": mean,
            "std": std,
            "z_score": z_score if std > 0 else float('inf'),
            "threshold": self.sensitivity,
        }

    def detect_rate_anomaly(self, current_rate, historical_rates):
        """Detect anomalies in event rates using Poisson distribution."""
        if len(historical_rates) < 30:
            return False

        mean_rate = np.mean(historical_rates)
        if mean_rate == 0:
            return current_rate > 0

        # Poisson probability of observing current_rate or more extreme
        p_value = 1 - stats.poisson.cdf(current_rate, mean_rate)

        return p_value < 0.001  # 0.1% significance level
```

**Machine Learning-Based Detection (Elastic ML):**

```json
// Elasticsearch ML job definition
{
  "job_id": "order-service-error-rate-anomaly",
  "analysis_config": {
    "bucket_span": "5m",
    "detectors": [
      {
        "function": "count",
        "field_name": "level",
        "partition_field_name": "service",
        "over_field_name": "host.name"
      }
    ],
    "influencers": ["service", "level"]
  },
  "analysis_limits": {
    "model_memory_limit": "512mb"
  },
  "data_description": {
    "time_field": "@timestamp",
    "time_format": "epoch_ms"
  }
}
```

**Baseline Establishment:**

```yaml
# Baseline configuration per metric
baselines:
  order_api_error_rate:
    calculation_window: 7_days
    update_frequency: daily
    seasonality:
      - period: 24h # Daily pattern
      - period: 168h # Weekly pattern
    exclusion_periods:
      - "deployment windows"
      - "known maintenance"
    alert_threshold: "3 sigma from baseline"

  order_api_latency_p95:
    calculation_window: 14_days
    update_frequency: daily
    seasonality:
      - period: 24h
    alert_threshold: "2 sigma from baseline"

  order_api_throughput:
    calculation_window: 7_days
    update_frequency: daily
    seasonality:
      - period: 24h
      - period: 168h
    alert_threshold: "50% deviation from baseline"
```

### Real-Time Alerting

**Alert Rule Design:**

```yaml
# alert-rules.yaml
groups:
  - name: order-service-alerts
    rules:
      # Error rate alert
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{service="order-service",status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{service="order-service"}[5m]))
          > 0.05
        for: 2m
        labels:
          severity: critical
          team: backend
          service: order-service
        annotations:
          summary: "Order API error rate > 5%"
          description: "Error rate is {{ $value | humanizePercentage }} for the last 5 minutes"
          runbook: "https://runbooks.company.com/order-service/high-error-rate"
          dashboard: "https://grafana.company.com/d/order-service"

      # Latency alert
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, 
            sum(rate(http_request_duration_seconds_bucket{service="order-service"}[5m])) 
            by (le))
          > 0.5
        for: 5m
        labels:
          severity: warning
          team: backend
        annotations:
          summary: "Order API p95 latency > 500ms"
          description: "p95 latency is {{ $value }}s"

      # Throughput anomaly
      - alert: ThroughputDrop
        expr: |
          sum(rate(http_requests_total{service="order-service"}[5m]))
          <
          sum(rate(http_requests_total{service="order-service"}[5m] offset 1w)) * 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Order API throughput dropped >50% vs last week"

      # Database connection pool
      - alert: DatabaseConnectionPoolExhaustion
        expr: |
          db_connection_pool_active{service="order-service"}
          /
          db_connection_pool_max{service="order-service"}
          > 0.9
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool >90% full"
```

**Alert Routing:**

```yaml
# alertmanager.yml
route:
  receiver: default-slack
  group_by: ["service", "alertname"]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: critical
      receiver: pagerduty-critical
      continue: true
    - match:
        severity: warning
      receiver: slack-warnings
    - match:
        team: backend
      receiver: backend-slack

receivers:
  - name: default-slack
    slack_configs:
      - channel: "#alerts"
        send_resolved: true
        title: "{{ .GroupLabels.alertname }}"
        text: "{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}"

  - name: pagerduty-critical
    pagerduty_configs:
      - service_key: "<pagerduty-service-key>"
        severity: "critical"

  - name: slack-warnings
    slack_configs:
      - channel: "#alerts-warnings"
        send_resolved: true

  - name: backend-slack
    slack_configs:
      - channel: "#backend-alerts"
        send_resolved: true
        title: "[Backend] {{ .GroupLabels.alertname }}"
```

**Alert Deduplication and Correlation:**

```python
# alert_correlator.py
from collections import defaultdict
from datetime import datetime, timedelta

class AlertCorrelator:
    def __init__(self, window_minutes=15):
        self.window = timedelta(minutes=window_minutes)
        self.active_incidents = defaultdict(list)

    def correlate(self, alerts):
        """Group related alerts into incidents."""
        incidents = []

        # Group by service and time window
        by_service = defaultdict(list)
        for alert in alerts:
            by_service[alert['service']].append(alert)

        for service, service_alerts in by_service.items():
            # Sort by time
            service_alerts.sort(key=lambda a: a['timestamp'])

            # Group alerts within window
            current_incident = [service_alerts[0]]
            for alert in service_alerts[1:]:
                if alert['timestamp'] - current_incident[0]['timestamp'] <= self.window:
                    current_incident.append(alert)
                else:
                    incidents.append(self.create_incident(current_incident))
                    current_incident = [alert]

            if current_incident:
                incidents.append(self.create_incident(current_incident))

        return incidents

    def create_incident(self, alerts):
        """Create a correlated incident from grouped alerts."""
        return {
            'id': f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'service': alerts[0]['service'],
            'start_time': alerts[0]['timestamp'],
            'alert_count': len(alerts),
            'alerts': alerts,
            'severity': max(a['severity'] for a in alerts),
            'summary': f"{len(alerts)} alerts for {alerts[0]['service']}",
        }
```

### Distributed Tracing Integration

**Trace-Log Correlation:**

```python
# Structured logging with trace context
import logging
import json

class TraceLogger:
    def __init__(self, logger):
        self.logger = logger

    def log(self, level, message, extra=None):
        log_entry = {
            "message": message,
            "level": level,
            "trace_id": get_current_trace_id(),  # From request context
            "span_id": get_current_span_id(),
            "service": "order-service",
        }
        if extra:
            log_entry.update(extra)

        getattr(self.logger, level.lower())(json.dumps(log_entry))

# Usage in handler
logger = TraceLogger(logging.getLogger(__name__))

def handle_request(request):
    logger.info("Processing request", extra={
        "http.request.method": request.method,
        "http.request.url": request.url,
    })

    try:
        result = process_order(request)
        logger.info("Request completed", extra={
            "http.response.status_code": 200,
            "http.response.duration_ms": result.duration_ms,
        })
    except Exception as e:
        logger.error("Request failed", extra={
            "error.type": type(e).__name__,
            "error.message": str(e),
            "http.response.status_code": 500,
        })
        raise
```

**Kibana Dashboard for Tracing:**

```json
{
  "title": "Order Service — Trace Analysis",
  "panels": [
    {
      "title": "Trace Duration Distribution",
      "type": "histogram",
      "query": {
        "query_string": { "query": "service:order-service" }
      },
      "field": "trace.duration_ms"
    },
    {
      "title": "Error Traces",
      "type": "table",
      "query": {
        "query_string": { "query": "service:order-service AND error:true" }
      },
      "columns": ["trace_id", "timestamp", "span.name", "error.message"]
    },
    {
      "title": "Slowest Traces (p99)",
      "type": "table",
      "query": {
        "query_string": { "query": "service:order-service" }
      },
      "sort": { "trace.duration_ms": "desc" },
      "size": 10
    }
  ]
}
```

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
