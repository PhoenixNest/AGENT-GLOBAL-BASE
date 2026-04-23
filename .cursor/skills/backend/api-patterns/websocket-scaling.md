---
name: websocket-scaling
description: This skill covers the architecture and implementation of scalable WebSocket services for real-time communication, including connection lifecycle management.
---

# WebSocket Scaling Architecture

## Overview

This skill covers the architecture and implementation of scalable WebSocket services for real-time communication, including connection lifecycle management, horizontal scaling strategies, message routing patterns, backpressure handling, and production-grade Go implementations using goroutine-based concurrency models.

### Scope and Use Cases

| Use Case                  | Connection Pattern | Message Pattern          | Scale Target         |
| ------------------------- | ------------------ | ------------------------ | -------------------- |
| Real-time chat            | Many-to-many       | Broadcast + targeted     | 10K-100K concurrent  |
| Live notifications        | One-to-many        | Fan-out                  | 100K-1M concurrent   |
| Collaborative editing     | Many-to-many       | Operational transforms   | 1K-10K concurrent    |
| Live sports/stock updates | One-to-many        | High-frequency broadcast | 100K-500K concurrent |
| IoT device telemetry      | Many-to-one        | Aggregation              | 10K-1M concurrent    |
| Multiplayer gaming        | Many-to-many       | Low-latency sync         | 1K-50K concurrent    |
| Live dashboards           | One-to-many        | Periodic updates         | 10K-100K concurrent  |

### When to Use WebSocket vs Alternatives

| Protocol                 | Direction        | Overhead                   | Best For                        | Not Good For                     |
| ------------------------ | ---------------- | -------------------------- | ------------------------------- | -------------------------------- |
| WebSocket                | Full-duplex      | Low (2-14 bytes/frame)     | Interactive, bidirectional      | Simple polling, firewalls        |
| Server-Sent Events (SSE) | Server-to-client | Low (HTTP/streaming)       | One-way updates, auto-reconnect | Client-to-server messages        |
| gRPC Streaming           | Full-duplex      | Medium (HTTP/2 + protobuf) | Service-to-service, typed       | Browser clients (needs grpc-web) |
| MQTT                     | Pub/Sub          | Very low (2-4 bytes)       | IoT, constrained networks       | Direct browser connections       |
| Long Polling             | Request/Response | High (HTTP per message)    | Legacy compatibility            | High-frequency updates           |

**Decision rule:** Use WebSocket when you need low-latency bidirectional communication with browser clients. Use SSE for server-push-only scenarios. Use gRPC streaming for service-to-service real-time communication.

---

## Connection Management

### WebSocket Handshake

```
Client                          Server
  |                                |
  |--- HTTP GET /ws ------------->|
  |    Upgrade: websocket        |
  |    Connection: Upgrade       |
  |    Sec-WebSocket-Key: dGhl    |
  |    Sec-WebSocket-Version: 13 |
  |                                |
  |<- HTTP 101 Switching --------|
  |   Upgrade: websocket          |
  |   Connection: Upgrade         |
  |   Sec-WebSocket-Accept: s3p   |
  |                                |
  |<==== WebSocket Frame =======> |
  |     (binary or text)          |
```

### Go WebSocket Server with Gorilla

```go
// internal/websocket/server.go
package websocket

import (
    "context"
    "log"
    "net/http"
    "sync"
    "time"

    "github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
    ReadBufferSize:  4096,
    WriteBufferSize: 4096,
    CheckOrigin: func(r *http.Request) bool {
        // Production: validate origin against allowlist
        origin := r.Header.Get("Origin")
        return isAllowedOrigin(origin)
    },
    // Enable compression (permessage-deflate)
    EnableCompression: true,
}

type Server struct {
    mu       sync.RWMutex
    clients  map[string]*Client // connection ID -> Client
    register   chan *Client
    unregister chan *Client
    hub        *MessageHub
}

func NewServer(hub *MessageHub) *Server {
    return &Server{
        clients:    make(map[string]*Client),
        register:   make(chan *Client, 256),
        unregister: make(chan *Client, 256),
        hub:        hub,
    }
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Printf("websocket upgrade error: %v", err)
        return
    }

    userID := extractUserID(r) // From JWT/session
    clientID := generateClientID()

    client := NewClient(clientID, userID, conn, s)

    s.register <- client
}

func (s *Server) Run(ctx context.Context) {
    for {
        select {
        case client := <-s.register:
            s.mu.Lock()
            s.clients[client.ID] = client
            s.mu.Unlock()

            log.Printf("client connected: %s (user: %s)", client.ID, client.UserID)

            // Join rooms/channels
            s.hub.JoinUser(client.UserID, client)

        case client := <-s.unregister:
            s.mu.Lock()
            if _, ok := s.clients[client.ID]; ok {
                delete(s.clients, client.ID)
                client.Conn.Close()
            }
            s.mu.Unlock()

            log.Printf("client disconnected: %s (user: %s)", client.ID, client.UserID)

            // Leave all rooms
            s.hub.LeaveUser(client.UserID, client)

        case <-ctx.Done():
            // Graceful shutdown: close all connections
            s.mu.RLock()
            for _, client := range s.clients {
                client.Conn.WriteMessage(websocket.CloseMessage,
                    websocket.FormatCloseMessage(websocket.CloseGoingAway, "server shutdown"))
                client.Conn.Close()
            }
            s.mu.RUnlock()
            return
        }
    }
}
```

### Client Lifecycle with Keepalive

```go
// internal/websocket/client.go
package websocket

import (
    "context"
    "log"
    "sync"
    "time"

    "github.com/gorilla/websocket"
)

const (
    pongWait   = 60 * time.Second  // Max time between pong responses
    pingPeriod = (pongWait * 9) / 10 // Send ping at 90% of pongWait
    writeWait  = 10 * time.Second   // Max time for write operation
)

type Client struct {
    ID     string
    UserID string
    Conn   *websocket.Conn

    server *Server

    // Buffered write channel (backpressure)
    send chan []byte

    // Prevent concurrent writes
    mu sync.Mutex

    // Metrics
    ConnectedAt  time.Time
    MessagesSent int64
    MessagesRecv int64
}

func NewClient(id, userID string, conn *websocket.Conn, server *Server) *Client {
    return &Client{
        ID:      id,
        UserID:  userID,
        Conn:    conn,
        server:  server,
        send:    make(chan []byte, 256), // Buffer 256 messages
    }
}

// ReadPump handles incoming messages
func (c *Client) ReadPump(ctx context.Context) {
    defer func() {
        c.server.unregister <- c
        c.Conn.Close()
    }()

    c.Conn.SetReadLimit(512 * 1024) // 512KB max message
    c.Conn.SetReadDeadline(time.Now().Add(pongWait))
    c.Conn.SetPongHandler(func(appData string) error {
        c.Conn.SetReadDeadline(time.Now().Add(pongWait))
        return nil
    })

    for {
        select {
        case <-ctx.Done():
            return
        default:
            _, message, err := c.Conn.ReadMessage()
            if err != nil {
                if websocket.IsUnexpectedCloseError(err,
                    websocket.CloseGoingAway,
                    websocket.CloseNormalClosure) {
                    log.Printf("unexpected close error: %v", err)
                }
                return
            }

            c.MessagesRecv++

            // Process message (validate, route, etc.)
            if err := c.server.hub.HandleMessage(ctx, c, message); err != nil {
                log.Printf("message handling error for client %s: %v", c.ID, err)
                // Don't disconnect on application errors
            }
        }
    }
}

// WritePump handles outgoing messages
func (c *Client) WritePump(ctx context.Context) {
    ticker := time.NewTicker(pingPeriod)
    defer func() {
        ticker.Stop()
        c.Conn.Close()
    }()

    for {
        select {
        case message, ok := <-c.send:
            if !ok {
                // Channel closed, send close frame
                c.Conn.WriteMessage(websocket.CloseMessage,
                    websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
                return
            }

            c.mu.Lock()
            c.Conn.SetWriteDeadline(time.Now().Add(writeWait))
            err := c.Conn.WriteMessage(websocket.TextMessage, message)
            c.mu.Unlock()

            if err != nil {
                log.Printf("write error for client %s: %v", c.ID, err)
                return
            }

            c.MessagesSent++

        case <-ticker.C:
            c.mu.Lock()
            c.Conn.SetWriteDeadline(time.Now().Add(writeWait))
            err := c.Conn.WriteMessage(websocket.PingMessage, nil)
            c.mu.Unlock()

            if err != nil {
                return
            }

        case <-ctx.Done():
            return
        }
    }
}
```

### Reconnection Strategies

```javascript
// Client-side reconnection with exponential backoff
class WebSocketClient {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
    this.baseReconnectDelay = 1000; // 1 second
    this.messageQueue = [];
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.reconnectAttempts = 0;
      this.flushMessageQueue();
      console.log('WebSocket connected');
    };

    this.ws.onmessage = (event) => {
      this.handleMessage(JSON.parse(event.data));
    };

    this.ws.onclose = (event) => {
      console.log(`WebSocket closed: ${event.code} ${event.reason}`);
      this.scheduleReconnect();
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    // Exponential backoff with jitter
    const delay = this.baseReconnectDelay * Math.pow(2, this.reconnectAttempts);
    const jitter = Math.random() * 500; // Prevent thundering herd
    const totalDelay = Math.min(delay + jitter, 30000); // Cap at 30s

    console.log(`Reconnecting in ${totalDelay}ms (attempt ${this.reconnectAttempts + 1})`);

    setTimeout(() => {
      this.reconnectAttempts++;
      this.connect();
    }, totalDelay);
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      // Queue message for reconnection
      this.messageQueue.push(message);
      if (this.messageQueue.length > 1000) {
        this.messageQueue.shift(); // Drop oldest
      }
    }
  }

  flushMessageQueue() {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      this.ws.send(JSON.stringify(message));
    }
  }
}
```

---

## Horizontal Scaling

### Architecture Overview

```
                    ┌─────────────────┐
                    │   Load Balancer │
                    │   (nginx/ALB)   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
    ┌─────────▼────┐ ┌──────▼──────┐ ┌─────▼──────┐
    │  WS Server 1 │ │ WS Server 2 │ │ WS Server 3│
    │  (Node A)    │ │ (Node B)    │ │ (Node C)   │
    │  10K conns   │ │ 10K conns   │ │ 10K conns  │
    └───────┬──────┘ └──────┬──────┘ └─────┬──────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
              ┌─────────────▼─────────────┐
              │    Redis Pub/Sub / NATS   │
              │   (Message Broker Layer)  │
              └───────────────────────────┘
                            │
              ┌─────────────▼─────────────┐
              │    Backend Services       │
              │  (gRPC / REST APIs)       │
              └───────────────────────────┘
```

### Sticky Sessions vs Pub/Sub

| Approach        | Pros                        | Cons                                 | When to Use                  |
| --------------- | --------------------------- | ------------------------------------ | ---------------------------- |
| Sticky Sessions | Simple, no broker needed    | Single point of failure, uneven load | Small scale (< 5 servers)    |
| Redis Pub/Sub   | Simple, well-understood     | No message persistence, memory-bound | Medium scale (< 100K conns)  |
| NATS            | High throughput, clustering | Additional infrastructure            | Large scale (100K-1M conns)  |
| Kafka           | Persistent, replayable      | Complex, higher latency              | Event sourcing, audit trails |

### Redis Pub/Sub Message Broker

```go
// internal/broker/redis_broker.go
package broker

import (
    "context"
    "encoding/json"
    "fmt"
    "log"

    "github.com/redis/go-redis/v9"
)

type RedisBroker struct {
    pubsub *redis.PubSub
    client *redis.Client
    channels map[string][]chan Message
    mu       sync.RWMutex
}

type Message struct {
    Type      string          `json:"type"`
    UserID    string          `json:"user_id,omitempty"`
    RoomID    string          `json:"room_id,omitempty"`
    Data      json.RawMessage `json:"data"`
    SenderID  string          `json:"sender_id,omitempty"`
}

func NewRedisBroker(addr string) (*RedisBroker, error) {
    client := redis.NewClient(&redis.Options{
        Addr:     addr,
        Password: "", // From env
        DB:       0,
        PoolSize: 10,
    })

    if err := client.Ping(context.Background()).Err(); err != nil {
        return nil, fmt.Errorf("redis connection failed: %w", err)
    }

    broker := &RedisBroker{
        client:   client,
        channels: make(map[string][]chan Message),
    }

    // Start listening
    go broker.listen()

    return broker, nil
}

func (b *RedisBroker) Publish(ctx context.Context, channel string, msg Message) error {
    data, err := json.Marshal(msg)
    if err != nil {
        return err
    }

    return b.client.Publish(ctx, channel, data).Err()
}

func (b *RedisBroker) Subscribe(channel string, ch chan Message) {
    b.mu.Lock()
    defer b.mu.Unlock()

    b.channels[channel] = append(b.channels[channel], ch)
}

func (b *RedisBroker) Unsubscribe(channel string, ch chan Message) {
    b.mu.Lock()
    defer b.mu.Unlock()

    channels := b.channels[channel]
    for i, c := range channels {
        if c == ch {
            b.channels[channel] = append(channels[:i], channels[i+1:]...)
            break
        }
    }

    if len(b.channels[channel]) == 0 {
        delete(b.channels, channel)
    }
}

func (b *RedisBroker) listen() {
    ctx := context.Background()

    // Subscribe to all channels
    var channelNames []string
    for name := range b.channels {
        channelNames = append(channelNames, name)
    }

    if len(channelNames) > 0 {
        b.pubsub = b.client.Subscribe(ctx, channelNames...)
        defer b.pubsub.Close()

        ch := b.pubsub.Channel()
        for msg := range ch {
            var message Message
            if err := json.Unmarshal([]byte(msg.Payload), &message); err != nil {
                log.Printf("failed to unmarshal message: %v", err)
                continue
            }

            b.mu.RLock()
            for _, ch := range b.channels[msg.Channel] {
                select {
                case ch <- message:
                default:
                    // Channel full, skip (backpressure)
                }
            }
            b.mu.RUnlock()
        }
    }
}
```

### NATS-Based Message Broker (High Scale)

```go
// internal/broker/nats_broker.go
package broker

import (
    "context"
    "encoding/json"
    "log"

    "github.com/nats-io/nats.go"
)

type NATSBroker struct {
    conn *nats.Conn
    js   nats.JetStreamContext
}

func NewNATSBroker(url string) (*NATSBroker, error) {
    conn, err := nats.Connect(url,
        nats.MaxReconnects(-1),
        nats.ReconnectWait(time.Second),
        nats.Name("ws-broker"),
    )
    if err != nil {
        return nil, err
    }

    js, err := conn.JetStream()
    if err != nil {
        return nil, err
    }

    return &NATSBroker{conn: conn, js: js}, nil
}

func (b *NATSBroker) Publish(ctx context.Context, subject string, msg Message) error {
    data, err := json.Marshal(msg)
    if err != nil {
        return err
    }

    _, err = b.js.Publish(subject, data)
    return err
}

func (b *NATSBroker) Subscribe(subject, queueGroup string, handler func(Message)) error {
    _, err := b.js.QueueSubscribe(subject, queueGroup, func(msg *nats.Msg) {
        var message Message
        if err := json.Unmarshal(msg.Data, &message); err != nil {
            log.Printf("nats unmarshal error: %v", err)
            return
        }
        handler(message)
    })
    return err
}
```

### Load Balancer Configuration

```nginx
# nginx.conf — WebSocket-aware load balancing
upstream websocket_backend {
    # IP hash for sticky sessions (alternative: least_conn)
    ip_hash;

    server ws-server-1:8080;
    server ws-server-2:8080;
    server ws-server-3:8080;
}

server {
    listen 443 ssl;
    server_name ws.company.com;

    location /ws {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;

        # WebSocket upgrade headers
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Client identification
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts (longer for WebSocket)
        proxy_read_timeout 86400s;    # 24 hours
        proxy_send_timeout 86400s;
        proxy_connect_timeout 10s;

        # Buffering off for real-time
        proxy_buffering off;
    }
}
```

---

## Message Routing

### Hub Architecture with Rooms

```go
// internal/websocket/hub.go
package websocket

import (
    "context"
    "encoding/json"
    "sync"
)

type MessageHub struct {
    broker MessageBroker

    // Room-based routing
    mu    sync.RWMutex
    rooms map[string]map[string]*Client // room_id -> client_id -> Client

    // User-to-client mapping (users can have multiple clients)
    userMu   sync.RWMutex
    userClients map[string]map[string]*Client // user_id -> client_id -> Client
}

func NewMessageHub(broker MessageBroker) *MessageHub {
    return &MessageHub{
        broker:      broker,
        rooms:       make(map[string]map[string]*Client),
        userClients: make(map[string]map[string]*Client),
    }
}

func (h *MessageHub) JoinRoom(roomID string, client *Client) {
    h.mu.Lock()
    defer h.mu.Unlock()

    if _, ok := h.rooms[roomID]; !ok {
        h.rooms[roomID] = make(map[string]*Client)
    }
    h.rooms[roomID][client.ID] = client

    // Subscribe to room messages from broker
    ch := make(chan Message, 256)
    h.broker.Subscribe(roomID, ch)
    go h.forwardRoomMessages(roomID, ch)
}

func (h *MessageHub) LeaveRoom(roomID string, client *Client) {
    h.mu.Lock()
    defer h.mu.Unlock()

    if room, ok := h.rooms[roomID]; ok {
        delete(room, client.ID)
        if len(room) == 0 {
            delete(h.rooms, roomID)
        }
    }
}

func (h *MessageHub) JoinUser(userID string, client *Client) {
    h.userMu.Lock()
    defer h.userMu.Unlock()

    if _, ok := h.userClients[userID]; !ok {
        h.userClients[userID] = make(map[string]*Client)
    }
    h.userClients[userID][client.ID] = client

    // Subscribe to user-specific messages
    ch := make(chan Message, 256)
    h.broker.Subscribe("user:"+userID, ch)
    go h.forwardUserMessages(userID, ch)
}

func (h *MessageHub) LeaveUser(userID string, client *Client) {
    h.userMu.Lock()
    defer h.userMu.Unlock()

    if clients, ok := h.userClients[userID]; ok {
        delete(clients, client.ID)
        if len(clients) == 0 {
            delete(h.userClients, userID)
        }
    }
}

// Broadcast to all clients in a room (fan-out)
func (h *MessageHub) BroadcastToRoom(ctx context.Context, roomID string, msg Message, excludeClientID string) error {
    // Publish to broker for cross-node delivery
    if err := h.broker.Publish(ctx, roomID, msg); err != nil {
        return err
    }

    // Deliver to local clients in the room
    h.mu.RLock()
    defer h.mu.RUnlock()

    if room, ok := h.rooms[roomID]; ok {
        data, _ := json.Marshal(msg)
        for clientID, client := range room {
            if clientID == excludeClientID {
                continue
            }
            select {
            case client.send <- data:
            default:
                // Client send buffer full, skip
            }
        }
    }

    return nil
}

// Send to specific user across all their devices
func (h *MessageHub) SendToUser(ctx context.Context, userID string, msg Message) error {
    data, _ := json.Marshal(msg)

    h.userMu.RLock()
    defer h.userMu.RUnlock()

    if clients, ok := h.userClients[userID]; ok {
        for _, client := range clients {
            select {
            case client.send <- data:
            default:
                // Client send buffer full, skip
            }
        }
    }

    return nil
}

func (h *MessageHub) HandleMessage(ctx context.Context, client *Client, rawMessage []byte) error {
    var msg Message
    if err := json.Unmarshal(rawMessage, &msg); err != nil {
        return err
    }

    msg.SenderID = client.UserID

    switch msg.Type {
    case "chat_message":
        // Route to room
        return h.BroadcastToRoom(ctx, msg.RoomID, msg, client.ID)

    case "direct_message":
        // Route to specific user
        return h.SendToUser(ctx, msg.UserID, msg)

    case "typing_indicator":
        // Broadcast typing to room (excluding sender)
        return h.BroadcastToRoom(ctx, msg.RoomID, msg, client.ID)

    case "presence_update":
        // Broadcast presence to all connected users
        return h.broadcastPresence(ctx, client)

    default:
        return fmt.Errorf("unknown message type: %s", msg.Type)
    }
}
```

### Fan-Out Pattern

```
┌─────────────┐
│   Publisher │
│  (Service)  │
└──────┬──────┘
       │
       ▼
┌──────────────┐
│    Broker    │
│ (Redis/NATS) │
└──────┬───────┘
       │
       ├────────────┬────────────┬────────────┐
       ▼            ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Server 1 │ │ Server 2 │ │ Server 3 │ │ Server N │
│  (5K)    │ │  (5K)    │ │  (5K)    │ │  (5K)    │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

### Fan-In Pattern

```
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Client 1 │ │ Client 2 │ │ Client N │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │             │
     └────────────┼─────────────┘
                  ▼
         ┌───────────────┐
         │  WS Server    │
         │ (Aggregator)  │
         └───────┬───────┘
                 │
                 ▼
         ┌───────────────┐
         │  Kafka/NATS   │
         │  (Sink)       │
         └───────────────┘
```

---

## Backpressure Handling

### Rate Limiting

```go
// internal/ratelimit/rate_limiter.go
package ratelimit

import (
    "sync"
    "time"
)

type TokenBucket struct {
    mu         sync.Mutex
    tokens     float64
    maxTokens  float64
    refillRate float64 // tokens per second
    lastRefill time.Time
}

func NewTokenBucket(maxTokens float64, refillRate float64) *TokenBucket {
    return &TokenBucket{
        tokens:     maxTokens,
        maxTokens:  maxTokens,
        refillRate: refillRate,
        lastRefill: time.Now(),
    }
}

func (tb *TokenBucket) Allow() bool {
    tb.mu.Lock()
    defer tb.mu.Unlock()

    now := time.Now()
    elapsed := now.Sub(tb.lastRefill).Seconds()
    tb.tokens = min(tb.maxTokens, tb.tokens+elapsed*tb.refillRate)
    tb.lastRefill = now

    if tb.tokens >= 1 {
        tb.tokens--
        return true
    }
    return false
}

// Per-client rate limiter registry
type ClientRateLimiter struct {
    mu       sync.RWMutex
    limiters map[string]*TokenBucket
    maxTokens float64
    refillRate float64
}

func NewClientRateLimiter(maxTokens, refillRate float64) *ClientRateLimiter {
    return &ClientRateLimiter{
        limiters:  make(map[string]*TokenBucket),
        maxTokens: maxTokens,
        refillRate: refillRate,
    }
}

func (rl *ClientRateLimiter) Allow(clientID string) bool {
    rl.mu.RLock()
    limiter, ok := rl.limiters[clientID]
    rl.mu.RUnlock()

    if !ok {
        rl.mu.Lock()
        limiter = NewTokenBucket(rl.maxTokens, rl.refillRate)
        rl.limiters[clientID] = limiter
        rl.mu.Unlock()
    }

    return limiter.Allow()
}
```

### Message Queuing with Consumer Lag Monitoring

```go
// internal/websocket/backpressure.go
package websocket

import (
    "sync/atomic"
    "time"
)

type BackpressureMonitor struct {
    // Per-client metrics
    droppedMessages atomic.Int64
    queueDepth      atomic.Int64
    lastMessageTime atomic.Int64
}

func (b *BackpressureMonitor) RecordEnqueue() {
    b.queueDepth.Add(1)
    b.lastMessageTime.Store(time.Now().UnixNano())
}

func (b *BackpressureMonitor) RecordDequeue() {
    b.queueDepth.Add(-1)
}

func (b *BackpressureMonitor) RecordDrop() {
    b.droppedMessages.Add(1)
}

func (b *BackpressureMonitor) GetQueueDepth() int64 {
    return b.queueDepth.Load()
}

func (b *BackpressureMonitor) GetDroppedMessages() int64 {
    return b.droppedMessages.Load()
}

// Check if client is healthy
func (b *BackpressureMonitor) IsHealthy() bool {
    depth := b.GetQueueDepth()
    dropped := b.GetDroppedMessages()

    // Unhealthy if queue depth > 500 or dropped > 100
    return depth < 500 && dropped < 100
}

// Adaptive message dropping
func (c *Client) SendWithBackpressure(data []byte) bool {
    if !c.backpressure.IsHealthy() {
        // Adaptive: reduce message frequency for unhealthy clients
        c.backpressure.RecordDrop()
        return false
    }

    select {
    case c.send <- data:
        c.backpressure.RecordEnqueue()
        return true
    default:
        c.backpressure.RecordDrop()
        return false
    }
}
```

---

## Go Implementation: Goroutine Workers

### Connection Pool with Worker Goroutines

```go
// internal/websocket/worker_pool.go
package websocket

import (
    "context"
    "log"
    "sync"
)

type WorkerPool struct {
    workers   int
    tasks     chan func()
    wg        sync.WaitGroup
    ctx       context.Context
    cancel    context.CancelFunc
}

func NewWorkerPool(workers int) *WorkerPool {
    ctx, cancel := context.WithCancel(context.Background())
    pool := &WorkerPool{
        workers: workers,
        tasks:   make(chan func(), 10000),
        ctx:     ctx,
        cancel:  cancel,
    }

    // Start workers
    for i := 0; i < workers; i++ {
        pool.wg.Add(1)
        go pool.worker(i)
    }

    return pool
}

func (p *WorkerPool) worker(id int) {
    defer p.wg.Done()

    for {
        select {
        case task := <-p.tasks:
            task()
        case <-p.ctx.Done():
            return
        }
    }
}

func (p *WorkerPool) Submit(task func()) bool {
    select {
    case p.tasks <- task:
        return true
    case <-p.ctx.Done():
        return false
    default:
        // Pool full, reject
        return false
    }
}

func (p *WorkerPool) Stop() {
    p.cancel()
    p.wg.Wait()
}

// Usage: Process messages through worker pool
func (h *MessageHub) HandleMessageAsync(ctx context.Context, client *Client, rawMessage []byte) {
    h.workerPool.Submit(func() {
        if err := h.HandleMessage(ctx, client, rawMessage); err != nil {
            log.Printf("async message handling error: %v", err)
        }
    })
}
```

### Graceful Shutdown

```go
// cmd/server/main.go
package main

import (
    "context"
    "log"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    server := NewServer()

    // HTTP server for WebSocket
    httpServer := &http.Server{
        Addr:    ":8080",
        Handler: server,
    }

    // Graceful shutdown on SIGTERM/SIGINT
    ctx, stop := signal.NotifyContext(context.Background(),
        syscall.SIGINT, syscall.SIGTERM)
    defer stop()

    go func() {
        log.Printf("HTTP server starting on :8080")
        if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("HTTP server error: %v", err)
        }
    }()

    // Wait for shutdown signal
    <-ctx.Done()
    log.Println("shutdown signal received")

    // Shutdown HTTP server (stops accepting new connections)
    shutdownCtx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    // Close all WebSocket connections
    server.GracefulShutdown(shutdownCtx)

    if err := httpServer.Shutdown(shutdownCtx); err != nil {
        log.Fatalf("HTTP server shutdown error: %v", err)
    }

    log.Println("server stopped gracefully")
}
```

---

## Security

### TLS Termination and Authentication

```go
// internal/websocket/auth.go
package websocket

import (
    "context"
    "net/http"
    "strings"

    "github.com/golang-jwt/jwt/v5"
)

func AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Extract token from query param or cookie
        tokenStr := r.URL.Query().Get("token")
        if tokenStr == "" {
            // Try Authorization header
            authHeader := r.Header.Get("Authorization")
            if strings.HasPrefix(authHeader, "Bearer ") {
                tokenStr = strings.TrimPrefix(authHeader, "Bearer ")
            }
        }

        if tokenStr == "" {
            http.Error(w, "unauthorized", http.StatusUnauthorized)
            return
        }

        // Validate JWT
        token, err := jwt.Parse(tokenStr, func(token *jwt.Token) (interface{}, error) {
            return jwtSigningKey, nil
        })
        if err != nil || !token.Valid {
            http.Error(w, "invalid token", http.StatusUnauthorized)
            return
        }

        // Attach user info to context
        claims := token.Claims.(jwt.MapClaims)
        userID := claims["sub"].(string)
        ctx := context.WithValue(r.Context(), "userID", userID)

        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

### DoS Protection

```yaml
# nginx — WebSocket DoS protection
limit_req_zone $binary_remote_addr zone=ws_limit:10m rate=10r/s;
limit_conn_zone $binary_remote_addr zone=ws_conn:10m;

server {
    location /ws {
        # Connection limit per IP
        limit_conn ws_conn 5;

        # Rate limit (handshake requests)
        limit_req zone=ws_limit burst=20 nodelay;

        # Max request body size
        client_max_body_size 1k;

        proxy_pass http://websocket_backend;
        # ... rest of WebSocket config
    }
}
```

---

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

## Stage 5 Integration

### WebSocket Development in Stage 5

During Stage 5 (Development), WebSocket services are developed by platform leads following the Coding Implementation Plan. Key considerations:

**Development tracking:**

- WebSocket server code goes in `platforms/<platform>/code/services/websocket-server/`
- Each service has its own `DEVELOPMENT-LOG.md` tracking milestones
- CTO oversees development; no user approval needed during Stage 5

**Implementation phases:**

1. Core WebSocket server (handshake, read/write pumps)
2. Connection management (register, unregister, heartbeat)
3. Message hub (rooms, routing, fan-out)
4. Broker integration (Redis/NATS for horizontal scaling)
5. Backpressure handling (rate limiting, adaptive dropping)
6. Security (authentication, TLS, DoS protection)
7. Observability (metrics, logging, tracing)
8. Graceful shutdown

### Code Review Checklist (Stage 6)

```markdown
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

## References

### Related Skills

- `backend/go-microservices` — Go microservice architecture patterns
- `backend/go-api-design` — REST API design patterns
- `backend/graphql` — GraphQL for real-time subscriptions
- `devops/kubernetes` — Container orchestration for WebSocket pods
- `security/service-security` — WebSocket security considerations
- `testing-qa/load-testing` — Performance testing for real-time systems

### External Resources

- [Gorilla WebSocket Documentation](https://pkg.go.dev/github.com/gorilla/websocket)
- [RFC 6455: The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455)
- [NATS Documentation](https://docs.nats.io/)
- [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/)
- [Scaling WebSocket (Ably)](https://ably.com/topics/websocket-scaling)
- [WebSocket Load Testing](https://github.com/hashrocket/ws)
- [Prometheus Go Client](https://pkg.go.dev/github.com/prometheus/client_golang/prometheus)
