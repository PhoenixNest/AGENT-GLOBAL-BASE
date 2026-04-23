---
name: ci-cd-optimization
description: Designs and optimizes continuous integration and delivery pipelines for speed, reliability, and developer feedback, covering pipeline parallelization strategies.
---

# CI/CD Optimization

**Category:** Developer Experience (CI/CD)
**Owner:** Developer Experience Engineer (Zara Okonkwo)

## Overview

Designs and optimizes continuous integration and delivery pipelines for speed, reliability, and developer feedback, covering pipeline parallelization strategies, test sharding by code ownership, artifact caching with remote and content-addressable stores, deployment strategies (canary, blue-green, rolling), and rollback automation with health check verification.

## Competency Dimensions

| Dimension                | Description                                                                                                | Proficiency Indicators                                                                                                                |
| ------------------------ | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Pipeline Parallelization | Stage decomposition, DAG-based execution, resource optimization, dependency management                     | Designs pipelines with maximum safe parallelism; reduces total pipeline time by > 50%; eliminates unnecessary sequential dependencies |
| Test Sharding            | Code ownership-based sharding, affected test detection, dynamic shard allocation, shard result aggregation | Shards tests by changed files; allocates shards dynamically based on test duration; reduces test time by > 60%                        |
| Artifact Caching         | Remote cache configuration, content-addressable storage, cache invalidation, cache warming                 | Achieves > 80% cache hit rate; designs cache keys based on content hashes; implements cache warming for common builds                 |
| Deployment Strategies    | Canary, blue-green, rolling updates, feature flags, traffic shifting                                       | Implements zero-downtime deployments; configures automated canary analysis; designs rollback triggers                                 |
| Rollback Automation      | Health check verification, automated rollback triggers, rollback testing, data migration rollback          | Configures automated rollback on health check failure; tests rollback procedures regularly; handles data migration rollback           |

## Execution Guidance

### Pipeline Parallelization Strategies

**Directed Acyclic Graph (DAG) pipeline design:**

```yaml
# GitLab CI — DAG-based pipeline
stages:
  - validate
  - build
  - test
  - security
  - deploy

# Stage 1: All independent validations (parallel)
lint:
  stage: validate
  script: npm run lint

type-check:
  stage: validate
  script: npm run type-check

spell-check:
  stage: validate
  script: npm run spell-check

# Stage 2: Build (depends on all validations)
build:
  stage: build
  needs: [lint, type-check, spell-check] # DAG: wait for all validations
  script: npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

# Stage 3: Tests (parallel shards)
test-unit-shard-1:
  stage: test
  needs: [build]
  script: npm run test:shard -- --shard=1/4

test-unit-shard-2:
  stage: test
  needs: [build]
  script: npm run test:shard -- --shard=2/4

test-unit-shard-3:
  stage: test
  needs: [build]
  script: npm run test:shard -- --shard=3/4

test-unit-shard-4:
  stage: test
  needs: [build]
  script: npm run test:shard -- --shard=4/4

test-integration:
  stage: test
  needs: [build]
  script: npm run test:integration
  services:
    - postgres:16
    - redis:7

test-e2e:
  stage: test
  needs: [build]
  script: npm run test:e2e

# Stage 4: Security (parallel with test completion)
security-scan:
  stage: security
  needs: [build]
  script: npm run security:scan

dependency-check:
  stage: security
  needs: [build]
  script: npm run dependency:check

# Stage 5: Deploy (depends on ALL tests and security)
deploy-staging:
  stage: deploy
  needs:
    - job: test-unit-shard-1
      optional: false
    - job: test-unit-shard-2
      optional: false
    - job: test-unit-shard-3
      optional: false
    - job: test-unit-shard-4
      optional: false
    - job: test-integration
      optional: false
    - job: test-e2e
      optional: false
    - job: security-scan
      optional: false
    - job: dependency-check
      optional: false
  script: ./deploy.sh staging
  environment: staging

deploy-production:
  stage: deploy
  needs: [deploy-staging]
  script: ./deploy.sh production
  environment: production
  when: manual # Manual approval for production
```

**Pipeline time optimization:**

```
Sequential pipeline (before optimization):
  Lint (2m) → Type-check (1m) → Build (5m) → Unit tests (12m) → Integration (8m) → E2E (10m) → Deploy (3m)
  Total: 41 minutes

Parallelized pipeline (after optimization):
  [Lint (2m), Type-check (1m), Spell-check (1m)] → Build (5m) →
  [Unit shard1 (3m), Unit shard2 (3m), Unit shard3 (3m), Unit shard4 (3m), Integration (8m), E2E (10m), Security (2m)] →
  Deploy (3m)
  Total: 2 + 5 + 10 + 3 = 20 minutes (51% reduction)
```

### Test Sharding by Ownership

```yaml
# Affected test detection — only run tests for changed files
# Using changesets to determine which tests to run

.changeset-rules:
  rules:
    - changes:
        - src/api/**/*
      variables:
        TEST_SCOPE: 'api'
    - changes:
        - src/ui/**/*
      variables:
        TEST_SCOPE: 'ui'
    - changes:
        - src/shared/**/*
      variables:
        TEST_SCOPE: 'all'

# Dynamic test allocation based on historical duration
test-shard:
  stage: test
  parallel:
    matrix:
      - SHARD: [1, 2, 3, 4, 5, 6, 7, 8]
  script:
    # Run tests for this shard
    - npm run test -- --shard=$SHARD/8
    # Upload coverage for this shard
    - npm run coverage:upload -- --shard=$SHARD
  artifacts:
    reports:
      junit: test-results/shard-$SHARD.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/shard-$SHARD/cobertura.xml
```

**Test duration-based shard allocation:**

```python
# test_shard_optimizer.py — Optimize shard allocation based on test duration
import json
from collections import defaultdict

def optimize_shards(test_durations: dict, num_shards: int) -> list[list[str]]:
    """
    Distribute tests across shards to balance total duration.
    Uses longest-processing-time-first (LPT) algorithm.

    Args:
        test_durations: {test_name: duration_seconds}
        num_shards: Number of parallel runners

    Returns:
        List of shards, each containing list of test names
    """
    # Sort tests by duration (longest first)
    sorted_tests = sorted(test_durations.items(), key=lambda x: x[1], reverse=True)

    # Initialize shards
    shards = [[] for _ in range(num_shards)]
    shard_durations = [0.0] * num_shards

    # Greedy assignment: assign each test to the shard with least total duration
    for test_name, duration in sorted_tests:
        min_shard_idx = shard_durations.index(min(shard_durations))
        shards[min_shard_idx].append(test_name)
        shard_durations[min_shard_idx] += duration

    return shards

# Usage: load historical test durations
with open('test-durations.json') as f:
    durations = json.load(f)

shards = optimize_shards(durations, 8)
for i, shard in enumerate(shards):
    total = sum(durations[t] for t in shard)
    print(f"Shard {i+1}: {len(shard)} tests, {total:.1f}s total")
```

### Artifact Caching

**Remote cache configuration (Bazel):**

```python
# .bazelrc
# Remote cache with content-addressable storage
build --remote_cache=grpcs://cache.company.com:9092
build --remote_instance_name=company-monorepo
build --remote_upload_local_results

# Cache authentication
build --google_default_credentials

# Cache optimization
build --remote_download_toplevel
build --experimental_remote_cache_async

# Local fallback cache
build --disk_cache=/tmp/bazel-disk-cache
```

**GitHub Actions cache with content-addressable keys:**

```yaml
# .github/workflows/ci.yml
- name: Cache build artifacts
  uses: actions/cache@v4
  with:
    # Content-addressable key based on lockfile hash
    path: |
      ~/.cache/go-build
      ~/go/pkg/mod
      node_modules/.cache
    key: ${{ runner.os }}-build-${{ hashFiles('**/go.sum', '**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-build-
      ${{ runner.os }}-

- name: Cache test results
  uses: actions/cache@v4
  with:
    path: .test-cache
    key: ${{ runner.os }}-test-${{ hashFiles('**/*.test.ts', 'src/**/*.ts') }}
    restore-keys: |
      ${{ runner.os }}-test-
```

**Cache invalidation strategy:**

| Cache Key Component | Purpose                     | Invalidated When          |
| ------------------- | --------------------------- | ------------------------- |
| OS (`runner.os`)    | Platform-specific builds    | Different runner OS       |
| Lockfile hash       | Dependency versions         | Dependencies change       |
| Source file hash    | Code changes                | Source files change       |
| Compiler version    | Compiler/toolchain updates  | Toolchain version changes |
| Config file hash    | Build configuration changes | Build config changes      |

**Cache warming for common builds:**

```yaml
# Nightly cache warming job
name: Cache Warming
on:
  schedule:
    - cron: '0 2 * * *' # 2 AM daily
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

## Pipeline Integration

**Stage 4 (Implementation Plan):** CI/CD pipeline designed with parallelization. Deployment strategy selected per service. Rollback procedures documented.

**Stage 5 (Development):** Pipeline implemented with test sharding. Artifact caching configured. Deployment automation deployed.

**Stage 6 (Code Review):** Pipeline configuration reviewed for correctness. Cache configuration validated. Rollback procedures tested.

**Stage 7 (Testing):** Pipeline execution time measured. Cache hit rates monitored. Deployment and rollback procedures tested in staging.

**Stage 10 (Release Readiness):** Panel confirms CI/CD pipeline operational, deployment strategy validated, rollback procedures tested.

## Quality Standards

| Metric                    | Target                                     | Measurement            |
| ------------------------- | ------------------------------------------ | ---------------------- |
| Pipeline duration (P95)   | < 15 minutes                               | CI monitoring          |
| Cache hit rate            | > 80%                                      | Cache metrics          |
| Test shard balance        | < 20% variance between shards              | Test timing analysis   |
| Deployment success rate   | > 99%                                      | Deployment tracking    |
| Rollback time             | < 5 minutes                                | Rollback drill timing  |
| Zero-downtime deployments | 100%                                       | Deployment monitoring  |
| Canary analysis accuracy  | > 95% correct promotion/rollback decisions | Canary analysis review |
