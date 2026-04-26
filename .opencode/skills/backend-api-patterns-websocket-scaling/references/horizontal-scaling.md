# Horizontal Scaling

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
