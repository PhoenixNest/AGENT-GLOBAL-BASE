# Configuration Management

## Configuration Management

### Environment-Based Configuration

```go
// internal/config/config.go
package config

import (
    "fmt"
    "os"
    "strconv"
    "time"
)

type Config struct {
    Server   ServerConfig
    Database DatabaseConfig
    GRPC     GRPCConfig
    Tracing  TracingConfig
}

type ServerConfig struct {
    Port         int
    ReadTimeout  time.Duration
    WriteTimeout time.Duration
}

type DatabaseConfig struct {
    Host            string
    Port            int
    User            string
    Password        string // Injected via secret management
    Database        string
    MaxOpenConns    int
    MaxIdleConns    int
    ConnMaxLifetime time.Duration
}

type GRPCConfig struct {
    Port             int
    MaxRecvMsgSize   int
    MaxSendMsgSize   int
    KeepaliveTime    time.Duration
}

type TracingConfig struct {
    Enabled       bool
    Endpoint      string
    SampleRate    float64
}

func Load() (*Config, error) {
    cfg := &Config{
        Server: ServerConfig{
            Port:         getEnvInt("SERVER_PORT", 8080),
            ReadTimeout:  getEnvDuration("SERVER_READ_TIMEOUT", 5*time.Second),
            WriteTimeout: getEnvDuration("SERVER_WRITE_TIMEOUT", 10*time.Second),
        },
        Database: DatabaseConfig{
            Host:            getEnv("DB_HOST", "localhost"),
            Port:            getEnvInt("DB_PORT", 5432),
            User:            getEnv("DB_USER", "postgres"),
            Password:        getEnv("DB_PASSWORD", ""),
            Database:        getEnv("DB_NAME", "orders"),
            MaxOpenConns:    getEnvInt("DB_MAX_OPEN_CONNS", 25),
            MaxIdleConns:    getEnvInt("DB_MAX_IDLE_CONNS", 5),
            ConnMaxLifetime: getEnvDuration("DB_CONN_MAX_LIFETIME", 5*time.Minute),
        },
        GRPC: GRPCConfig{
            Port:           getEnvInt("GRPC_PORT", 50051),
            MaxRecvMsgSize: getEnvInt("GRPC_MAX_RECV_MSG_SIZE", 4*1024*1024),
            MaxSendMsgSize: getEnvInt("GRPC_MAX_SEND_MSG_SIZE", 4*1024*1024),
            KeepaliveTime:  getEnvDuration("GRPC_KEEPALIVE_TIME", 10*time.Second),
        },
        Tracing: TracingConfig{
            Enabled:    getEnvBool("TRACING_ENABLED", true),
            Endpoint:   getEnv("TRACING_ENDPOINT", "otel-collector:4317"),
            SampleRate: getEnvFloat64("TRACING_SAMPLE_RATE", 0.1),
        },
    }

    return cfg, cfg.Validate()
}

func (c *Config) Validate() error {
    if c.Database.Password == "" {
        return fmt.Errorf("DB_PASSWORD is required")
    }
    if c.Server.Port <= 0 || c.Server.Port > 65535 {
        return fmt.Errorf("SERVER_PORT must be between 1 and 65535")
    }
    return nil
}

// Helper functions
func getEnv(key, fallback string) string {
    if v := os.Getenv(key); v != "" {
        return v
    }
    return fallback
}

func getEnvInt(key string, fallback int) int {
    if v := os.Getenv(key); v != "" {
        if n, err := strconv.Atoi(v); err == nil {
            return n
        }
    }
    return fallback
}

func getEnvBool(key string, fallback bool) bool {
    if v := os.Getenv(key); v != "" {
        if b, err := strconv.ParseBool(v); err == nil {
            return b
        }
    }
    return fallback
}

func getEnvDuration(key string, fallback time.Duration) time.Duration {
    if v := os.Getenv(key); v != "" {
        if d, err := time.ParseDuration(v); err == nil {
            return d
        }
    }
    return fallback
}

func getEnvFloat64(key string, fallback float64) float64 {
    if v := os.Getenv(key); v != "" {
        if f, err := strconv.ParseFloat(v, 64); err == nil {
            return f
        }
    }
    return fallback
}
```

### Kubernetes Secret Injection

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: order-service-secrets
  namespace: production
type: Opaque
data:
  db-password: <base64-encoded-password>
  api-key: <base64-encoded-api-key>
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  template:
    spec:
      containers:
        - name: order-service
          env:
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: order-service-secrets
                  key: db-password
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: order-service-secrets
                  key: api-key
```

---
