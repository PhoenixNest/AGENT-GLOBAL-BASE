# Monitoring & Observability

## Monitoring & Observability

### Prometheus Metrics

```go
// internal/metrics/websocket_metrics.go
package metrics

import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    ActiveConnections = promauto.NewGaugeVec(prometheus.GaugeOpts{
        Name: "websocket_active_connections",
        Help: "Number of active WebSocket connections",
    }, []string{"server"})

    MessagesSent = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "websocket_messages_sent_total",
        Help: "Total number of WebSocket messages sent",
    }, []string{"server"})

    MessagesReceived = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "websocket_messages_received_total",
        Help: "Total number of WebSocket messages received",
    }, []string{"server"})

    ConnectionDuration = promauto.NewHistogramVec(prometheus.HistogramOpts{
        Name:    "websocket_connection_duration_seconds",
        Help:    "Duration of WebSocket connections",
        Buckets: prometheus.ExponentialBuckets(1, 2, 16),
    }, []string{"server"})

    WriteErrors = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "websocket_write_errors_total",
        Help: "Total number of WebSocket write errors",
    }, []string{"server", "error_type"})

    DroppedMessages = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "websocket_dropped_messages_total",
        Help: "Total number of messages dropped due to backpressure",
    }, []string{"server"})

    QueueDepth = promauto.NewGaugeVec(prometheus.GaugeOpts{
        Name: "websocket_queue_depth",
        Help: "Current depth of client send queues",
    }, []string{"server", "percentile"})
)
```

### Key Metrics Dashboard

| Metric                | Alert Threshold   | Action                      |
| --------------------- | ----------------- | --------------------------- |
| Active connections    | > 80% of max      | Scale horizontally          |
| Connection rate       | > 100/s sustained | Check for reconnect storm   |
| Message latency p99   | > 500ms           | Investigate broker lag      |
| Write error rate      | > 1% of sends     | Check network/client health |
| Dropped messages      | > 0.1% of total   | Increase buffer or scale    |
| Queue depth p95       | > 200             | Backpressure issue          |
| Memory per connection | > 50KB            | Optimize buffer sizes       |

---
