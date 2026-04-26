# WebSocket Service Code Review Checklist

## WebSocket Service Code Review Checklist

### Connection Management

- [ ] Ping/pong heartbeat implemented (interval < 60s)
- [ ] Reconnection handled client-side with exponential backoff
- [ ] Connection limits enforced (per-user, per-IP, global)
- [ ] Graceful shutdown closes all connections cleanly

### Message Handling

- [ ] Message size limits enforced (prevent memory exhaustion)
- [ ] Input validation on all incoming messages
- [ ] Concurrent write prevention (mutex or single writer)
- [ ] Buffered send channels with appropriate capacity

### Scaling

- [ ] Pub/Sub broker for cross-node message delivery
- [ ] Room membership tracked across nodes
- [ ] No single-node state dependencies (or replicated)
- [ ] Load balancer configured for WebSocket (upgrade headers)

### Backpressure

- [ ] Send buffer overflow handled (drop or reject, not block)
- [ ] Per-client rate limiting implemented
- [ ] Dropped messages counted and alerted
- [ ] Adaptive behavior for overloaded clients

### Security

- [ ] TLS termination at edge (load balancer)
- [ ] JWT/auth validation before upgrade
- [ ] Origin validation (prevent CSRF)
- [ ] DoS protection (rate limits, connection limits)

### Observability

- [ ] Active connections metric exported
- [ ] Message throughput (sent/recv) tracked
- [ ] Write error rate monitored
- [ ] Connection duration histogram

```

### Defect Classification

| Scenario                                     | Severity | Rationale              |
| -------------------------------------------- | -------- | ---------------------- |
| No connection limit (memory exhaustion)      | P0       | DoS vulnerability      |
| Missing authentication on WebSocket endpoint | P0       | Security breach        |
| No graceful shutdown (data loss)             | P1       | Deployment reliability |
| Missing heartbeat (zombie connections)       | P1       | Resource leak          |
| No rate limiting (abuse potential)           | P2       | Security hardening     |
| Missing metrics (observability gap)          | P2       | Operational risk       |
| No backpressure (message drops silently)     | P3       | Quality of service     |

---
```
