---
name: backend-api-patterns-websocket-scaling
description: WebSocket scaling architecture for real-time services — connection lifecycle management, horizontal scaling strategies, message routing patterns, backpressure handling, and production-grade Go implementations with goroutine concurrency. Owned by Dev Malhotra (Backend Chapter Lead). Use during Stage 3 (Architecture) for WebSocket scaling design and Stage 5 (Development) for implementation. Trigger: websocket scaling, connection management, horizontal scaling websocket, message routing, backpressure, goroutine websocket, real-time scaling.
prerequisites:
  - backend-api-patterns-distributed-systems

version: "1.0.0"
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

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`connection-management.md`](references/connection-management.md) — Connection Management
- [`horizontal-scaling.md`](references/horizontal-scaling.md) — Horizontal Scaling
- [`backpressure-handling.md`](references/backpressure-handling.md) — Backpressure Handling
- [`go-implementation:-goroutine-workers.md`](references/go-implementation:-goroutine-workers.md) — Go Implementation: Goroutine Workers
- [`security.md`](references/security.md) — Security
- [`monitoring-&-observability.md`](references/monitoring-&-observability.md) — Monitoring & Observability
- [`stage-5-integration.md`](references/stage-5-integration.md) — Stage 5 Integration
- [`websocket-service-code-review-checklist.md`](references/websocket-service-code-review-checklist.md) — WebSocket Service Code Review Checklist
- [`references.md`](references/references.md) — References
