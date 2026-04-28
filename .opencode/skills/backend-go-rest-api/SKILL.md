---
name: backend-go-rest-api
description: Go REST API development — idiomatic HTTP handler chains, composable middleware, structured error handling, context propagation for cancellation/timeouts, and structured logging with zap/zerolog. Owned by Dev Malhotra (Backend Chapter Lead). Use during Stage 5 (Development) for Go API implementation and Stage 6 (Code Review) for Go pattern validation. Trigger: go rest api, golang http handler, go middleware, context propagation, structured logging go, go error handling.
prerequisites:
  - backend-overview

version: "1.0.0"
---

# Go REST API Development

**Category:** Backend Development (Go)
**Owner:** Backend Engineer (Omar Hassan)

## Overview

Builds production-grade REST APIs in Go using idiomatic patterns including HTTP handler chains, composable middleware, structured error handling, context propagation for cancellation and timeouts, and structured logging with zap or zerolog. Emphasizes Go's philosophy of simplicity, explicit error handling, and standard library preference.

## Competency Dimensions

| Dimension           | Description                                                                      | Proficiency Indicators                                                                                                                                                       |
| ------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HTTP Handlers       | Handler functions, ServeMux routing, method dispatch, request/response lifecycle | Writes handlers following `func(w http.ResponseWriter, r *http.Request)` signature; uses `http.ServeMux` (Go 1.22+) for routing; separates handler logic from business logic |
| Middleware Chains   | Handler wrapping, context enrichment, authentication, logging, recovery          | Composes middleware using functional wrapping; ensures middleware order is correct (recovery → logging → auth → handler); propagates context through chain                   |
| Error Handling      | Sentinel errors, error wrapping, HTTP error responses, custom error types        | Uses `%w` for error wrapping; defines sentinel errors for comparison; maps errors to appropriate HTTP status codes; never panics in handlers                                 |
| Context Propagation | Cancellation, deadlines, values in context, timeout patterns                     | Passes context as first parameter to all I/O functions; sets appropriate timeouts; handles cancellation signals; never ignores context.Done()                                |
| Structured Logging  | zap/zerolog configuration, log levels, field enrichment, correlation IDs         | Uses structured (JSON) logging in production; includes request ID in all log entries; avoids logging sensitive data; uses sampling for high-volume logs                      |

## Execution Guidance

### HTTP Handler Architecture

**Go 1.22+ ServeMux with method routing:**

```go
func NewRouter(userHandler *UserHandler) *http.ServeMux {
    mux := http.NewServeMux()

    // Go 1.22+ supports method+path routing
    mux.HandleFunc("GET /users", userHandler.ListUsers)
    mux.HandleFunc("POST /users", userHandler.CreateUser)
    mux.HandleFunc("GET /users/{id}", userHandler.GetUser)
    mux.HandleFunc("PUT /users/{id}", userHandler.UpdateUser)
    mux.HandleFunc("DELETE /users/{id}", userHandler.DeleteUser)

    return mux
}

// Handler with dependency injection
type UserHandler struct {
    service *UserService
    logger  *zap.Logger
}

func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    // Extract path parameter
    userID := r.PathValue("id")
    if userID == "" {
        WriteError(w, http.StatusBadRequest, "missing_user_id", "User ID is required")
        return
    }

    // Use context from request (includes cancellation)
    ctx := r.Context()

    user, err := h.service.GetUser(ctx, userID)
    if err != nil {
        h.handleServiceError(w, err)
        return
    }

    WriteJSON(w, http.StatusOK, UserResponse{
        ID:    user.ID,
        Name:  user.Name,
        Email: user.Email,
    })
}
```

**JSON response helpers:**

```go
func WriteJSON(w http.ResponseWriter, status int, data interface{}) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)

    encoder := json.NewEncoder(w)
    encoder.SetEscapeHTML(false) // Don't escape < > & in JSON
    if err := encoder.Encode(data); err != nil {
        // Too late to change status code, log error
        log.Printf("failed to encode response: %v", err)
    }
}

func WriteError(w http.ResponseWriter, status int, code string, message string) {
    WriteJSON(w, status, ErrorResponse{
        Code:    code,
        Message: message,
        Status:  status,
    })
}
```

### Middleware Chain

**Middleware composition with correct ordering:**

```go
func BuildMiddlewareChain(
    handler http.Handler,
    logger *zap.Logger,
    auth *Authenticator,
    tracer *otel.Tracer,
) http.Handler {
    // Order matters — applied bottom to top:
    // handler → recovery → tracing → logging → auth → CORS → rate-limit
    chain := handler
    chain = RateLimitMiddleware(chain)
    chain = CORSMiddleware(chain)
    chain = AuthMiddleware(chain, auth)
    chain = LoggingMiddleware(chain, logger)
    chain = TracingMiddleware(chain, tracer)
    chain = RecoveryMiddleware(chain, logger)
    return chain
}

// Authentication middleware
func AuthMiddleware(next http.Handler, auth *Authenticator) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Skip auth for health check and public endpoints
        if isPublicEndpoint(r.URL.Path) {
            next.ServeHTTP(w, r)
            return
        }

        token := extractBearerToken(r)
        if token == "" {
            WriteError(w, http.StatusUnauthorized, "missing_token", "Authorization token required")
            return
        }

        claims, err := auth.VerifyToken(r.Context(), token)
        if err != nil {
            WriteError(w, http.StatusUnauthorized, "invalid_token", "Invalid or expired token")
            return
        }

        // Enrich context with user info
        ctx := context.WithValue(r.Context(), ContextKeyUserID, claims.UserID)
        ctx = context.WithValue(ctx, ContextKeyUserRole, claims.Role)

        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// Request ID middleware for correlation
func RequestIDMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        requestID := r.Header.Get("X-Request-ID")
        if requestID == "" {
            requestID = uuid.New().String()
        }

        // Add to response headers
        w.Header().Set("X-Request-ID", requestID)

        // Add to context
        ctx := context.WithValue(r.Context(), ContextKeyRequestID, requestID)

        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

// Recovery middleware — catch panics and return 500
func RecoveryMiddleware(next http.Handler, logger *zap.Logger) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if rec := recover(); rec != nil {
                stack := debug.Stack()
                logger.Error("panic recovered",
                    zap.Any("panic", rec),
                    zap.String("stack", string(stack)),
                    zap.String("path", r.URL.Path),
                )
                WriteError(w, http.StatusInternalServerError, "internal_error", "An internal error occurred")
            }
        }()
        next.ServeHTTP(w, r)
    })
}
```

### Error Handling Patterns

```go
// Sentinel errors for comparison
var (
    ErrNotFound     = errors.New("resource not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrDuplicate    = errors.New("duplicate resource")
    ErrInvalidInput = errors.New("invalid input")
)

// Domain errors with additional context
type DomainError struct {
    Code    string
    Message string
    Err     error
    Status  int
}

func (e *DomainError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("%s: %v", e.Message, e.Err)
    }
    return e.Message
}

func (e *DomainError) Unwrap() error {
    return e.Err
}

// Map domain errors to HTTP responses
func (h *UserHandler) handleServiceError(w http.ResponseWriter, err error) {
    h.logger.Error("service error", zap.Error(err))

    var domainErr *DomainError
    switch {
    case errors.Is(err, ErrNotFound):
        WriteError(w, http.StatusNotFound, "not_found", "User not found")
    case errors.Is(err, ErrDuplicate):
        WriteError(w, http.StatusConflict, "duplicate", "User already exists")
    case errors.Is(err, ErrInvalidInput):
        WriteError(w, http.StatusBadRequest, "validation_error", err.Error())
    case errors.As(err, &domainErr):
        WriteError(w, domainErr.Status, domainErr.Code, domainErr.Message)
    default:
        WriteError(w, http.StatusInternalServerError, "internal_error", "An internal error occurred")
    }
}

// Service layer error wrapping
func (s *UserService) GetUser(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.GetByID(ctx, id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, fmt.Errorf("get user %s: %w", id, ErrNotFound)
        }
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}
```

### Context Propagation

```go
// All I/O functions accept context as first parameter
func (r *UserRepository) GetByID(ctx context.Context, id string) (*User, error) {
    // Context carries cancellation and timeout
    query := "SELECT id, name, email, role, created_at FROM users WHERE id = $1"

    row := r.db.QueryRowContext(ctx, query, id)

    var user User
    err := row.Scan(&user.ID, &user.Name, &user.Email, &user.Role, &user.CreatedAt)
    return &user, err
}

// HTTP client with timeout via context
func (c *ExternalClient) FetchData(ctx context.Context, url string) ([]byte, error) {
    // Create request with context
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, fmt.Errorf("create request: %w", err)
    }

    resp, err := c.client.Do(req)
    if err != nil {
        // Check if context was cancelled
        if ctx.Err() != nil {
            return nil, fmt.Errorf("request cancelled: %w", ctx.Err())
        }
        return nil, fmt.Errorf("HTTP request: %w", err)
    }
    defer resp.Body.Close()

    return io.ReadAll(resp.Body)
}

// Timeout pattern at handler level
func (h *Handler) WithTimeout(timeout time.Duration) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            ctx, cancel := context.WithTimeout(r.Context(), timeout)
            defer cancel()

            // Check if context already cancelled
            select {
            case <-ctx.Done():
                WriteError(w, http.StatusGatewayTimeout, "timeout", "Request timed out")
                return
            default:
            }

            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}

// Fan-out with context cancellation
func (s *Service) FetchMultiple(ctx context.Context, ids []string) ([]*Result, error) {
    // Create error group with context
    g, ctx := errgroup.WithContext(ctx)

    results := make([]*Result, len(ids))
    for i, id := range ids {
        i, id := i, id // Capture loop variables
        g.Go(func() error {
            // Each goroutine inherits the parent context
            result, err := s.fetchOne(ctx, id)
            if err != nil {
                return err
            }
            results[i] = result
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, fmt.Errorf("fetch multiple: %w", err)
    }

    return results, nil
}
```

### Structured Logging

**zap logger configuration:**

```go
func NewLogger(env string) (*zap.Logger, error) {
    var config zap.Config

    if env == "production" {
        config = zap.NewProductionConfig()
        config.Level = zap.NewAtomicLevelAt(zap.InfoLevel)
        // Sampling: 100 first, then 1 per 100
        config.Sampling = &zap.SamplingConfig{
            Initial:    100,
            Thereafter: 100,
        }
    } else {
        config = zap.NewDevelopmentConfig()
        config.Level = zap.NewAtomicLevelAt(zap.DebugLevel)
        config.EncoderConfig.EncodeLevel = zapcore.CapitalColorLevelEncoder
    }

    logger, err := config.Build()
    if err != nil {
        return nil, err
    }

    return logger, nil
}

// Usage in handler — always include request context
func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
    logger := h.logger.With(
        zap.String("request_id", GetRequestID(r.Context())),
        zap.String("method", r.Method),
        zap.String("path", r.URL.Path),
    )

    logger.Info("creating user")

    // ... business logic ...

    if err != nil {
        logger.Error("failed to create user",
            zap.Error(err),
            zap.String("email", req.Email),
        )
        h.handleServiceError(w, err)
        return
    }

    logger.Info("user created successfully",
        zap.String("user_id", user.ID),
    )
}
```

**zerolog alternative (zero-allocation JSON logging):**

```go
// zerolog — faster than zap for high-throughput scenarios
func NewZeroLogger() zerolog.Logger {
    return zerolog.New(os.Stdout).
        With().
        Timestamp().
        Caller().
        Logger()
}

// Usage
logger.Info().
    Str("request_id", requestID).
    Str("user_id", userID).
    Str("action", "create_user").
    Msg("User created")

// Structured fields are type-safe
logger.Error().
    Err(err).
    Int("status_code", 500).
    Str("path", r.URL.Path).
    Msg("Request failed")
```

## Pipeline Integration

**Stage 5 (Development):** All HTTP handlers follow established patterns. Middleware chain correctly ordered. Context propagated to all I/O calls. Structured logging on all handlers.

**Stage 6 (Code Review):** Review handler error handling completeness. Verify context propagation in all database and external API calls. Check middleware ordering. Validate logging includes request correlation IDs.

**Stage 7 (Testing):** Handler tests validate all error paths. Context cancellation tests verify timeout behavior. Logging tests verify structured output format.

## Quality Standards

| Metric              | Target                               | Measurement                   |
| ------------------- | ------------------------------------ | ----------------------------- |
| Context propagation | 100% of I/O calls use context        | Code review + static analysis |
| Error wrapping      | 100% of errors wrapped with `%w`     | Code review                   |
| Structured logging  | 100% of handlers log with request ID | Log audit                     |
| Panic recovery      | 100% handlers protected              | Code review                   |
| Response time (p95) | < 200ms (excluding DB)               | Application metrics           |
| Test coverage       | > 80% for handler layer              | go test -cover                |
| Lint compliance     | 0 golangci-lint violations           | CI pipeline                   |
