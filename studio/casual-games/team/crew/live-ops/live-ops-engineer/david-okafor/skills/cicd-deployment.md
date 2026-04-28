---
name: cicd-deployment
description: CI/CD pipeline design, blue-green deployments, feature flag management, and automated rollback for live game operations.
version: "1.0.0"
---

# CI/CD & Deployment

## Overview

This skill covers the design, implementation, and maintenance of CI/CD pipelines for live game content deployment, including zero-downtime deployment strategies, feature flag systems, and automated rollback mechanisms.

## Tools & Platforms

| Tool           | Purpose                                     |
| -------------- | ------------------------------------------- |
| GitHub Actions | CI/CD pipeline orchestration                |
| Kubernetes     | Container orchestration, blue-green deploys |
| LaunchDarkly   | Feature flag management, gradual rollouts   |
| ArgoCD         | GitOps deployment automation                |
| Helm           | Kubernetes package management               |

## Core Methodologies

### 1. Blue-Green Deployment

```
Current (Blue) ──┐                  ┌── Traffic Shift ──→ New (Green)
                 ├── Load Balancer ─┤
New (Green)  ────┘                  └── Health Check ───→ Validate
```

| Phase                | Duration | Criteria                              |
| -------------------- | -------- | ------------------------------------- |
| Deploy to Green      | 5 min    | All pods healthy, no error spikes     |
| Health Check         | 2 min    | Crash rate < 0.1%, latency < 200ms    |
| Traffic Shift        | 1 min    | Shift 100% traffic to Green           |
| Validate             | 10 min   | Monitor KPIs: errors, retention, perf |
| Rollback (if needed) | 2 min    | Automated if thresholds exceeded      |

### 2. Feature Flag Rollout Strategy

| Phase    | Traffic % | Duration | Monitor                      | Auto-Rollback Trigger         |
| -------- | --------- | -------- | ---------------------------- | ----------------------------- |
| Canary   | 1%        | 1 hour   | Crash rate, error rate       | Crash rate > 0.5%             |
| Early    | 5%        | 2 hours  | + D1 retention proxy metrics | Error rate > 2%               |
| Growing  | 25%       | 4 hours  | + Session length             | D1 retention drop > 2pp       |
| Majority | 50%       | 4 hours  | + Monetization metrics       | Revenue drop > 5%             |
| Full     | 100%      | —        | All KPIs                     | Any critical threshold breach |

### 3. Automated Rollback Triggers

| Metric             | Threshold               | Action                            |
| ------------------ | ----------------------- | --------------------------------- |
| Crash rate         | > 0.5% of sessions      | Immediate rollback                |
| Error rate         | > 2% of API calls       | Immediate rollback                |
| D1 retention proxy | Drop > 3pp vs. baseline | Investigate, rollback if persists |
| P95 latency        | > 500ms                 | Investigate, rollback if > 1000ms |
