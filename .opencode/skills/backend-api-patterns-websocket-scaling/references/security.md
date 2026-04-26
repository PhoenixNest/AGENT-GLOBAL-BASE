# Security

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
