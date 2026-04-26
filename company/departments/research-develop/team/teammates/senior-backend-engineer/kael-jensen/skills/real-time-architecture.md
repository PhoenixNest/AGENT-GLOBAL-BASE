---
version: "1.0.0"
---

| Competency                 | Description                                                                       | Quality Criteria                                                                                                                                        |
| -------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| WebSocket Architecture     | Handshake protocol, frame structure, heartbeat/ping-pong, reconnection logic      | Implements RFC 6455-compliant WebSocket server; handles connection lifecycle (open, message, close, error); implements exponential backoff reconnection |
| SSE vs WebSockets          | Decision criteria based on communication pattern                                  | Selects SSE for server-push-only scenarios; selects WebSockets for bidirectional; understands HTTP/2 multiplexing implications                          |
| GraphQL Subscriptions      | Subscription resolution, event filtering, connection management                   | Implements subscriptions with pub/sub backend; handles subscription lifecycle; filters events per-client                                                |
| Message Queuing            | Redis Pub/Sub, Kafka consumer patterns, fan-out strategies                        | Designs pub/sub topology for real-time event distribution; handles message ordering and delivery guarantees                                             |
| Connection Pool Management | Connection limits, memory per connection, idle timeout, graceful shutdown         | Calculates connection capacity per instance; implements connection lifecycle management; handles graceful drain on shutdown                             |
| Horizontal Scaling         | Sticky sessions, shared pub/sub, connection affinity, load balancer configuration | Scales WebSocket servers horizontally with shared message bus; configures load balancer for connection upgrade support                                  |

## Execution Guidance

### WebSocket vs SSE Decision Matrix

| Requirement                 | WebSocket              | SSE              | HTTP/2 Server Push | gRPC Streaming      |
| --------------------------- | ---------------------- | ---------------- | ------------------ | ------------------- |
| Bidirectional communication | ✅ Yes                 | ❌ Server-only   | ❌ Server-only     | ✅ Yes              |
| Binary data                 | ✅ Yes                 | ❌ Text-only     | ❌ Text-only       | ✅ Yes              |
| Auto-reconnect              | ❌ Manual              | ✅ Built-in      | N/A                | ❌ Manual           |
| HTTP proxy compatible       | ❌ Upgrade required    | ✅ Standard HTTP | ✅ Standard HTTP   | ❌ Requires HTTP/2  |
| Browser support             | ✅ All modern          | ✅ All modern    | ⚠️ Limited         | ❌ Requires library |
| Implementation complexity   | Medium                 | Low              | High               | Medium              |
| Server resource usage       | High (persistent conn) | Medium           | Low                | High                |

**Rule of thumb:**

- Client needs to send messages to server → **WebSocket**
- Server-only push (notifications, live updates) → **SSE**
- GraphQL client → **GraphQL Subscription** (WebSocket transport)
- Internal service-to-service → **gRPC streaming**

### WebSocket Server Implementation (Go)

```go
type WebSocketServer struct {
    upgrader    websocket.Upgrader
    connections *ConnectionManager
    pubsub      *RedisPubSub
    logger      *zap.Logger
}

type ConnectionManager struct {
    mu          sync.RWMutex
    connections map[string]*Connection  // userID → Connection
    byRoom      map[string]map[string]*Connection  // roomID → userID → Connection
}

type Connection struct {
    UserID    string
    Conn      *websocket.Conn
    Send      chan []byte
    LastPong  time.Time
    Room      string
}

func (s *WebSocketServer) HandleWebSocket(w http.ResponseWriter, r *http.Request) {
    userID := GetUserIDFromQuery(r)
    room := GetRoomFromQuery(r)

    conn, err := s.upgrader.Upgrade(w, r, nil)
    if err != nil {
        s.logger.Error("WebSocket upgrade failed", zap.Error(err))
        return
    }

    connection := &Connection{
        UserID:   userID,
        Conn:     conn,
        Send:     make(chan []byte, 256),
        LastPong: time.Now(),
        Room:     room,
    }

    s.connections.Add(connection)
    defer s.connections.Remove(connection)

    // Subscribe to room events
    sub, err := s.pubsub.Subscribe(r.Context(), fmt.Sprintf("room:%s", room))
    if err != nil {
        s.logger.Error("Pub/Sub subscribe failed", zap.Error(err))
        return
    }
    defer sub.Close()

    // Start read/write goroutines
    go connection.writePump(s.logger)
    go connection.readPump(s.logger, s.connections)

    // Forward pub/sub messages to client
    for {
        select {
        case msg := <-sub.Messages():
            connection.Send <- msg.Data
        case <-r.Context().Done():
            return
        }
    }
}

// Write pump: sends messages to client, handles ping/pong
func (c *Connection) writePump(logger *zap.Logger) {
    ticker := time.NewTicker(30 * time.Second)
    defer ticker.Stop()

    for {
        select {
        case message, ok := <-c.Send:
            c.Conn.SetWriteDeadline(time.Now().Add(10 * time.Second))
            if !ok {
                c.Conn.WriteMessage(websocket.CloseMessage, []byte{})
                return
            }

            w, err := c.Conn.NextWriter(websocket.TextMessage)
            if err != nil {
                return
            }
            w.Write(message)

            // Batch pending messages
            n := len(c.Send)
            for i := 0; i < n; i++ {
                w.Write([]byte{'\n'})
                w.Write(<-c.Send)
            }

            if err := w.Close(); err != nil {
                return
            }

        case <-ticker.C:
            c.Conn.SetWriteDeadline(time.Now().Add(10 * time.Second))
            if err := c.Conn.WriteMessage(websocket.PingMessage, nil); err != nil {
                return
            }
        }
    }
}

// Read pump: receives messages from client
func (c *Connection) readPump(logger *zap.Logger, cm *ConnectionManager) {
    defer func() {
        cm.Remove(c)
        c.Conn.Close()
    }()

    c.Conn.SetReadLimit(512 * 1024) // 512KB max message
    c.Conn.SetReadDeadline(time.Now().Add(60 * time.Second))
    c.Conn.SetPongHandler(func(string) error {
        c.Conn.SetReadDeadline(time.Now().Add(60 * time.Second))
        c.LastPong = time.Now()
        return nil
    })

    for {
        _, message, err := c.Conn.ReadMessage()
        if err != nil {
            if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseNormalClosure) {
                logger.Error("WebSocket read error", zap.Error(err))
            }
            break
        }

        // Process message (e.g., chat message, presence update)
        c.handleMessage(message)
    }
}
```

### SSE Implementation

```go
func (s *Server) HandleSSE(w http.ResponseWriter, r *http.Request) {
    userID := GetUserIDFromContext(r.Context())

    // Set SSE headers
    w.Header().Set("Content-Type", "text/event-stream")
    w.Header().Set("Cache-Control", "no-cache")
    w.Header().Set("Connection", "keep-alive")
    w.Header().Set("X-Accel-Buffering", "no") // Disable nginx buffering

    flusher, ok := w.(http.Flusher)
    if !ok {
        http.Error(w, "Streaming not supported", http.StatusInternalServerError)
        return
    }

    // Subscribe to user events
    sub, err := s.pubsub.Subscribe(r.Context(), fmt.Sprintf("user:%s", userID))
    if err != nil {
        http.Error(w, "Subscription failed", http.StatusInternalServerError)
        return
    }
    defer sub.Close()

    // Send initial connection event
    fmt.Fprintf(w, "event: connected\ndata: %s\n\n", time.Now().Format(time.RFC3339))
    flusher.Flush()

    // Heartbeat every 15s (SSE clients detect disconnection via timeout)
    ticker := time.NewTicker(15 * time.Second)
    defer ticker.Stop()

    for {
        select {
        case msg := <-sub.Messages():
            fmt.Fprintf(w, "event: %s\nid: %d\ndata: %s\n\n", msg.Event, msg.ID, msg.Data)
            flusher.Flush()

        case <-ticker.C:
            // SSE comment as heartbeat (colon prefix)
            fmt.Fprintf(w, ": heartbeat %d\n\n", time.Now().Unix())
            flusher.Flush()

        case <-r.Context().Done():
            return
        }
    }
}
```

### GraphQL Subscriptions

```go
// GraphQL subscription resolver with event filtering
type SubscriptionResolver struct {
    pubsub *RedisPubSub
}

func (r *SubscriptionResolver) OrderUpdated(ctx context.Context) (<-chan *Order, error) {
    userID := GetUserIDFromContext(ctx)

    // Create channel for this subscription
    ch := make(chan *Order, 10)

    // Subscribe to user's order events
    sub, err := r.pubsub.Subscribe(ctx, fmt.Sprintf("orders:%s", userID))
    if err != nil {
        return nil, err
    }

    go func() {
        defer sub.Close()
        defer close(ch)

        for {
            select {
            case msg := <-sub.Messages():
                var order Order
                if err := json.Unmarshal(msg.Data, &order); err != nil {
                    continue
                }
                // Filter: only send if user is involved
                if order.UserID == userID || order.AssignedTo == userID {
                    ch <- &order
                }
            case <-ctx.Done():
                return
            }
        }
    }()

    return ch, nil
}
```

### Horizontal Scaling with Shared Pub/Sub

```
Architecture for horizontally scaled real-time connections:

  Client A ──WS──┐                    ┌──WS── Client B
                 │                    │
          ┌──────▼──────┐      ┌──────▼──────┐
          │  WS Server 1│      │  WS Server 2│
          │  (conn: A)  │      │  (conn: B)  │
          └──────┬──────┘      └──────┬──────┘
                 │                    │
                 └────┬──────────┬────┘
                      │          │
               ┌──────▼──────────▼──────┐
               │    Redis Pub/Sub       │
               │  (shared message bus)  │
               └──────┬──────────┬──────┘
                      │          │
               ┌──────▼──────┐  ┌▼────────────┐
               │  Kafka      │  │  Event      │
               │  (durability│  │  Sources    │
               │   + replay) │  │             │
               └─────────────┘  └─────────────┘

Key: Each WS server subscribes to Redis channels for rooms/users
     it has connections for. Messages published to Redis fan out
     to all servers, but only servers with relevant connections
     forward to clients.
```

**Load balancer configuration (nginx):**

```nginx
upstream websocket_servers {
    least_conn;
    server ws-1:8080;
    server ws-2:8080;
    server ws-3:8080;
}

server {
    listen 443 ssl;

    location /ws {
        proxy_pass http://websocket_servers;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket timeout settings
        proxy_read_timeout 86400s;    # 24 hours
        proxy_send_timeout 86400s;

        # Buffer settings (disable for streaming)
        proxy_buffering off;
    }

    location /sse {
        proxy_pass http://websocket_servers;
        proxy_http_version 1.1;
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400s;
        chunked_transfer_encoding off;
    }
}
```

### Connection Capacity Planning

```
Memory per WebSocket connection:
  Connection struct:     ~512 bytes
  Send channel buffer:   ~256 * 1KB = 256KB
  Goroutine stack:       ~2KB (initial)
  TCP buffer:            ~128KB (kernel)
  TLS overhead:          ~30KB
  ──────────────────────────────
  Total per connection:  ~430KB

Connections per 4GB instance:
  Available memory:      3GB (after OS + app overhead)
  Connections:           3GB / 430KB ≈ 7,000 connections

Target: 50,000 concurrent connections
  Instances needed:      50,000 / 7,000 ≈ 8 instances
  With headroom (30%):   11 instances
```

### Graceful Shutdown

```go
func (s *WebSocketServer) GracefulShutdown(timeout time.Duration) {
    // 1. Stop accepting new connections
    s.isShuttingDown = true

    // 2. Send close frame to all connected clients
    s.connections.BroadcastClose(websocket.CloseGoingAway, "Server shutting down")

    // 3. Wait for clients to disconnect (up to timeout)
    deadline := time.After(timeout)
    ticker := time.NewTicker(500 * time.Millisecond)
    defer ticker.Stop()

    for {
        select {
        case <-deadline:
            // Force close remaining connections
            s.connections.ForceClose()
            return
        case <-ticker.C:
            if s.connections.Count() == 0 {
                return
            }
        }
    }
}
```

## Pipeline Integration

**Stage 3 (Architecture):** Component diagrams must show real-time communication topology, pub/sub infrastructure, and load balancer configuration. ADR required for WebSocket vs SSE vs GraphQL Subscriptions selection.

**Stage 4 (Implementation Plan):** Real-time infrastructure (Redis Pub/Sub, Kafka) is deployment dependency. Connection capacity planning must inform infrastructure sizing.

**Stage 5 (Development):** WebSocket/SSE handlers implemented with connection lifecycle management. Horizontal scaling tested with multiple server instances. Graceful shutdown implemented.

**Stage 6 (Code Review):** Review connection leak prevention (defer cleanup). Validate heartbeat/ping-pong implementation. Check memory usage per connection. Verify horizontal scaling correctness.

**Stage 7 (Testing):** Load tests validate connection capacity. Failover tests validate reconnection behavior. Message delivery tests validate pub/sub fan-out correctness.

**Stage 8 (Integrity Verification):** Panel verifies real-time architecture matches design, connection limits are within capacity, message delivery is reliable, and graceful shutdown works correctly.

## Quality Standards

| Metric                           | Target                      | Measurement                 |
| -------------------------------- | --------------------------- | --------------------------- |
| Connection capacity per instance | As planned (within 10%)     | Memory profiling under load |
| Message delivery latency (p95)   | < 100ms                     | Distributed tracing         |
| Reconnection time                | < 3 seconds                 | Client-side monitoring      |
| Connection leak rate             | 0 connections leaked        | Connection count monitoring |
| Heartbeat reliability            | 100% (no false disconnects) | Heartbeat success rate      |
| Horizontal scaling efficiency    | Linear to 90%               | Multi-instance load test    |
| Graceful shutdown time           | < 30 seconds                | Shutdown timing measurement |
| Message ordering guarantee       | 100% within stream          | Message sequence validation |
