# Connection Management

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
      console.log("WebSocket connected");
    };

    this.ws.onmessage = (event) => {
      this.handleMessage(JSON.parse(event.data));
    };

    this.ws.onclose = (event) => {
      console.log(`WebSocket closed: ${event.code} ${event.reason}`);
      this.scheduleReconnect();
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }

  scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error("Max reconnection attempts reached");
      return;
    }

    // Exponential backoff with jitter
    const delay = this.baseReconnectDelay * Math.pow(2, this.reconnectAttempts);
    const jitter = Math.random() * 500; // Prevent thundering herd
    const totalDelay = Math.min(delay + jitter, 30000); // Cap at 30s

    console.log(
      `Reconnecting in ${totalDelay}ms (attempt ${this.reconnectAttempts + 1})`,
    );

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
