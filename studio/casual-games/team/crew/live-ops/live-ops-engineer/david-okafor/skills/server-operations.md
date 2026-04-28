---
name: server-operations
description: Server infrastructure management, Kubernetes operations, monitoring, and incident response for live game services.
version: "1.0.0"
---

# Server Operations

## Overview

This skill covers the management and operation of live game server infrastructure, including Kubernetes cluster management, cloud infrastructure (AWS/GCP), monitoring and alerting, and incident response procedures.

## Tools & Platforms

| Tool                 | Purpose                                |
| -------------------- | -------------------------------------- |
| Kubernetes (EKS/GKE) | Container orchestration, auto-scaling  |
| AWS / GCP            | Cloud infrastructure, managed services |
| Prometheus           | Metrics collection, alerting           |
| Grafana              | Dashboard visualization                |
| PagerDuty            | On-call rotation, incident escalation  |
| ELK Stack            | Log aggregation, search, analysis      |

## Core Methodologies

### 1. Uptime Management

| Target | Allowed Downtime/Year | Strategy                       |
| ------ | --------------------- | ------------------------------ |
| 99.9%  | 8.76 hours            | Blue-green deploys, redundancy |
| 99.95% | 4.38 hours            | Multi-AZ, automated failover   |
| 99.99% | 52.6 minutes          | Multi-region, active-active    |

### 2. Incident Response

| Severity | Definition              | Response Time | Resolution Target | Escalation          |
| -------- | ----------------------- | ------------- | ----------------- | ------------------- |
| P0       | Complete service outage | 5 minutes     | 1 hour            | Live Ops Lead + CTO |
| P1       | Core feature broken     | 15 minutes    | 4 hours           | Live Ops Lead       |
| P2       | Minor feature degraded  | 1 hour        | 24 hours          | —                   |
| P3       | Cosmetic / nice-to-have | 4 hours       | 1 week            | —                   |

### 3. Monitoring Dashboard

| Dashboard         | Key Metrics                         | Alert Threshold      |
| ----------------- | ----------------------------------- | -------------------- |
| Service Health    | Uptime, error rate, response time   | Error rate > 1%      |
| Player Experience | Session success rate, login time    | Login time > 5s      |
| Infrastructure    | CPU, memory, disk, network I/O      | CPU > 80% for 10 min |
| Deployment        | Deploy success rate, rollback count | Rollback rate > 5%   |
