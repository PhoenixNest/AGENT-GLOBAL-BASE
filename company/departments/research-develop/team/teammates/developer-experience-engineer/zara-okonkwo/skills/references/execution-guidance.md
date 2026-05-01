---
version: "1.0.0"
---

------------- | --------------------------- | ------------------------- |
| OS (`runner.os`) | Platform-specific builds | Different runner OS |
| Lockfile hash | Dependency versions | Dependencies change |
| Source file hash | Code changes | Source files change |
| Compiler version | Compiler/toolchain updates | Toolchain version changes |
| Config file hash | Build configuration changes | Build config changes |

**Cache warming for common builds:**

```yaml
# Nightly cache warming job
name: Cache Warming
on:
  schedule:
    - cron: "0 2 * * *" # 2 AM daily
  workflow_dispatch:

jobs:
  warm-cache:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Build main branch to populate cache
      - name: Build (populate cache)
        run: |
          ./gradlew assemble
          ./gradlew testClasses

      # Build common feature branches
      - name: Build feature branches
        run: |
          for branch in $(git ls-remote --heads origin | grep 'feature/' | awk '{print $2}'); do
            git fetch origin $branch
            git checkout $branch
            ./gradlew assemble --parallel
          done
```

### Deployment Strategies

**Canary deployment with automated analysis:**

```yaml
# Argo Rollouts — Canary deployment
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: api-canary
spec:
  replicas: 10
  strategy:
    canary:
      steps:
        # Step 1: 10% traffic to canary
        - setWeight: 10
        - pause: { duration: 5m }

        # Step 2: Automated canary analysis
        - analysis:
            templates:
              - templateName: api-canary-analysis
            args:
              - name: service-name
                value: api-canary

        # Step 3: 25% traffic
        - setWeight: 25
        - pause: { duration: 10m }

        # Step 4: Automated analysis again
        - analysis:
            templates:
              - templateName: api-canary-analysis

        # Step 5: 50% traffic
        - setWeight: 50
        - pause: { duration: 15m }

        # Step 6: 100% traffic (full rollout)
        - setWeight: 100

---
# Canary analysis template
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: api-canary-analysis
spec:
  metrics:
    - name: error-rate
      interval: 1m
      successCondition: result[0] < 0.01 # < 1% error rate
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus.monitoring
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}", code=~"5.."}[1m]))
            /
            sum(rate(http_requests_total{service="{{args.service-name}}"}[1m]))

    - name: latency-p99
      interval: 1m
      successCondition: result[0] < 500 # P99 < 500ms
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus.monitoring
          query: |
            histogram_quantile(0.99, 
              sum(rate(http_request_duration_seconds_bucket{service="{{args.service-name}}"}[1m])) 
              by (le))
```

**Rolling update with health checks:**

```yaml
# Kubernetes Deployment — Rolling update
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2 # Max 2 extra pods during update
      maxUnavailable: 1 # Max 1 pod unavailable
  template:
    spec:
      containers:
        - name: api
          image: gcr.io/company/api:v1.3.0
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 3 # 3 failures = not ready
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            failureThreshold: 3
```

### Rollback Automation

```yaml
# Automated rollback on health check failure
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: api
spec:
  strategy:
    canary:
      autoPromotionEnabled: true
      analysis:
        templates:
          - templateName: health-check
        startingStep: 1
        failOnAbort: true  # Abort rollback on analysis failure

  # Rollback trigger: if analysis fails, automatically rollback
  rollbackWindow:
    revisions: 3  # Keep last 3 revisions available for rollback

---
# Rollback analysis template
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: health-check
spec:
  metrics:
    - name: health-check
      interval: 30s
      successCondition: result[0] == 200
      failureLimit: 2  # 2 consecutive failures = rollback
      provider:
        web:
          url: "http://api-canary/healthz"
          timeoutSeconds: 5

# Rollback script (fallback)
#!/bin/bash
# rollback.sh
set -e

CURRENT_REVISION=$(kubectl rollout history deployment/api | tail -1 | awk '{print $1}')
PREVIOUS_REVISION=$((CURRENT_REVISION - 1))

echo "Rolling back from revision $CURRENT_REVISION to $PREVIOUS_REVISION"

# Execute rollback
kubectl rollout undo deployment/api --to-revision=$PREVIOUS_REVISION

# Wait for rollback to complete
kubectl rollout status deployment/api --timeout=300s

# Verify health
HEALTH=$(curl -sf http://api.company.com/healthz || echo "FAILED")
if [ "$HEALTH" != "ok" ]; then
    echo "WARNING: Health check failed after rollback!"
    exit 1
fi

echo "Rollback successful"
```

**Rollback decision matrix:**

| Trigger                            | Action                            | Automation Level    |
| ---------------------------------- | --------------------------------- | ------------------- |
| Health check fails (2 consecutive) | Automatic rollback                | Fully automated     |
| Error rate > 5% for 5 minutes      | Automatic rollback                | Fully automated     |
| P99 latency > 1s for 10 minutes    | Alert + suggested rollback        | Semi-automated      |
| Data corruption detected           | Immediate rollback + data restore | Manual with runbook |
| Business metric drop > 10%         | Alert + investigation             | Manual              |
