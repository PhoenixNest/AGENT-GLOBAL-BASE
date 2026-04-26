# Deployment Patterns

## Deployment Patterns

### Blue-Green Deployment

```yaml
# k8s/blue-green.yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service-active
spec:
  selector:
    app: order-service
    track: active
  ports:
    - port: 50051
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
      track: active
  template:
    metadata:
      labels:
        app: order-service
        track: active
    spec:
      containers:
        - name: order-service
          image: registry.company.com/order-service:v1.2.3
---
# Green deployment (new version, not receiving traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
      track: preview
  template:
    metadata:
      labels:
        app: order-service
        track: preview
    spec:
      containers:
        - name: order-service
          image: registry.company.com/order-service:v1.3.0
```

**Switch traffic:**

```bash
kubectl patch service order-service-active \
  -p '{"spec":{"selector":{"track":"preview"}}}'
```

### Canary Deployment

```yaml
# k8s/canary.yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
  ports:
    - port: 50051
---
# Stable version (90% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
        version: stable
    spec:
      containers:
        - name: order-service
          image: registry.company.com/order-service:v1.2.3
---
# Canary version (10% traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
        version: canary
    spec:
      containers:
        - name: order-service
          image: registry.company.com/order-service:v1.3.0
```

### Feature Flags

```go
// internal/featureflags/flags.go
package featureflags

import (
    "context"
    "sync"
)

type FeatureFlags struct {
    mu     sync.RWMutex
    flags  map[string]bool
    watchers []func(flag string, enabled bool)
}

func NewFeatureFlags() *FeatureFlags {
    return &FeatureFlags{
        flags: make(map[string]bool),
    }
}

func (ff *FeatureFlags) IsEnabled(flag string) bool {
    ff.mu.RLock()
    defer ff.mu.RUnlock()
    return ff.flags[flag]
}

func (ff *FeatureFlags) Set(flag string, enabled bool) {
    ff.mu.Lock()
    ff.flags[flag] = enabled
    ff.mu.Unlock()

    // Notify watchers
    for _, w := range ff.watchers {
        w(flag, enabled)
    }
}

// Usage in handler
func (h *OrderHandler) CreateOrder(ctx context.Context, req *pb.CreateOrderRequest) (*pb.CreateOrderResponse, error) {
    if h.flags.IsEnabled("new-payment-flow") {
        return h.createOrderWithNewPaymentFlow(ctx, req)
    }
    return h.createOrderWithLegacyPaymentFlow(ctx, req)
}
```

---
