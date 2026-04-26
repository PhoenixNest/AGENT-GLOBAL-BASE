# Service Discovery

## Service Discovery

### Consul-Based Service Discovery

```go
// internal/discovery/consul.go
package discovery

import (
    "fmt"
    "log"
    "net"
    "strconv"

    consul "github.com/hashicorp/consul/api"
)

type ConsulDiscovery struct {
    client *consul.Client
    serviceID string
}

func NewConsulDiscovery(config *consul.Config, serviceName string) (*ConsulDiscovery, error) {
    client, err := consul.NewClient(config)
    if err != nil {
        return nil, fmt.Errorf("consul client error: %w", err)
    }

    return &ConsulDiscovery{
        client:    client,
        serviceID: serviceName,
    }, nil
}

func (d *ConsulDiscovery) Register(name string, port int, tags []string) error {
    registration := &consul.AgentServiceRegistration{
        ID:      fmt.Sprintf("%s-%s", name, generateID()),
        Name:    name,
        Port:    port,
        Tags:    tags,
        Check: &consul.AgentServiceCheck{
            GRPC:                           fmt.Sprintf("localhost:%d", port),
            GRPCUseTLS:                    false,
            Timeout:                       "3s",
            Interval:                      "10s",
            DeregisterCriticalServiceAfter: "90s",
        },
    }

    return d.client.Agent().ServiceRegister(registration)
}

func (d *ConsulDiscovery) Discover(serviceName string) ([]ServiceInstance, error) {
    entries, _, err := d.client.Health().Service(serviceName, "", true, nil)
    if err != nil {
        return nil, fmt.Errorf("service discovery error: %w", err)
    }

    var instances []ServiceInstance
    for _, entry := range entries {
        instances = append(instances, ServiceInstance{
            ID:      entry.Service.ID,
            Address: entry.Service.Address,
            Port:    entry.Service.Port,
            Tags:    entry.Service.Tags,
        })
    }

    return instances, nil
}
```

### Kubernetes DNS Discovery

```yaml
# k8s/order-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service
  namespace: production
spec:
  selector:
    app: order-service
  ports:
    - name: grpc
      port: 50051
      targetPort: 50051
    - name: http
      port: 8080
      targetPort: 8080
  type: ClusterIP
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
        - name: order-service
          image: registry.company.com/order-service:v1.2.3
          ports:
            - containerPort: 50051
              name: grpc
            - containerPort: 8080
              name: http
          readinessProbe:
            grpc:
              port: 50051
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            grpc:
              port: 50051
            initialDelaySeconds: 15
            periodSeconds: 20
          env:
            - name: PAYMENT_SERVICE_ADDR
              value: "payment-service.production.svc.cluster.local:50052"
            - name: USER_SERVICE_ADDR
              value: "user-service.production.svc.cluster.local:50053"
```

### API Gateway Routing

```yaml
# k8s/gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: api-gateway
  namespace: production
spec:
  gatewayClassName: istio
  listeners:
    - name: grpc
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs:
          - name: gateway-tls-cert
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: order-routing
  namespace: production
spec:
  parentRefs:
    - name: api-gateway
  hostnames:
    - "api.company.com"
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /order.v1.OrderService
      backendRefs:
        - name: order-service
          port: 50051
    - matches:
        - path:
            type: PathPrefix
            value: /payment.v1.PaymentService
      backendRefs:
        - name: payment-service
          port: 50052
```

---
