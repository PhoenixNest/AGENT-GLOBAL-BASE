---
# Backend services per region
apiVersion: cloud.google.com/v1
kind: BackendService
metadata:
  name: api-backend-us
spec:
  protocol: HTTP
  healthChecks:
    - api-health-check
  localityLbPolicy: ROUND_ROBIN
  connectionDraining:
    drainingTimeoutSec: 300
version: "1.0.0"
---

apiVersion: cloud.google.com/v1
kind: BackendService
metadata:
name: api-backend-eu
spec:
protocol: HTTP
healthChecks: - api-health-check
localityLbPolicy: ROUND_ROBIN

---

# URL map with failover

apiVersion: cloud.google.com/v1
kind: URLMap
metadata:
name: api-urlmap
spec:
defaultService: api-backend-us
hostRules: - hosts: - api.company.com
pathMatcher: api-paths
pathMatchers: - name: api-paths
defaultService: api-backend-us
pathRules: - paths: - /api/\*
service: api-backend-us

# Failover: if US region unhealthy, route to EU

# Configured via health check thresholds

apiVersion: cloud.google.com/v1
kind: HealthCheck
metadata:
name: api-health-check
spec:
httpHealthCheck:
requestPath: /healthz
port: 8080
checkIntervalSec: 10
timeoutSec: 5
unhealthyThreshold: 3 # 30 seconds to detect failure
healthyThreshold: 2 # 20 seconds to confirm recovery

````

### Disaster Recovery Runbook

```markdown
# Disaster Recovery Runbook
````
