---
name: websocket-scaling
description: Design and scale WebSocket infrastructure for real-time mobile features — connection management, horizontal scaling with Redis pub/sub, heartbeat and reconnection protocols, and graceful degradation for unreliable mobile networks.
version: "1.0.0"
---

# Websocket Scaling

| Competency          | Description                                                            | Quality Criteria                                                                                                      |
| ------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| WebSocket Server    | Implement WebSocket server with connection lifecycle management        | Server handles connect/disconnect/error events; connection registry maintained per user; no memory leak on disconnect |
| Horizontal Scaling  | Scale WebSocket servers horizontally using Redis pub/sub               | Messages delivered to connected clients across all server instances; Redis channel per user/room; fan-out < 50ms p95  |
| Mobile Reconnection | Implement exponential backoff reconnection protocol for mobile clients | Client reconnects on disconnect with jittered exponential backoff (1s, 2s, 4s, max 60s); state resync on reconnection |
| Load Testing        | Load test WebSocket endpoint for concurrent connection capacity        | Tested to 10K concurrent connections per server instance; p99 message delivery latency < 100ms; no message loss       |

## Execution Guidance

### Horizontal Scaling Architecture

```
Mobile Client → Load Balancer (sticky sessions) → WS Server 1
                                                 → WS Server 2
                                                 → WS Server 3
                                                       ↓
                                               Redis Pub/Sub
                                               (cross-server fan-out)
```

When a message targets a user, the server:

1. Checks if the user is connected to this instance → deliver directly
2. If not, publishes to Redis channel `user:{userId}` → all instances deliver to their local connections

### Mobile Heartbeat Protocol

```
Client → Server: PING every 30s
Server → Client: PONG within 5s
If no PONG: client closes and reconnects with backoff
If no PING for 60s: server closes idle connection
```

Configure ALB/NLB idle timeout to 300s (greater than the heartbeat interval) to prevent the load balancer from closing active WebSocket connections.
