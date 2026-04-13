---
name: load-stress-testing
description: Server load testing and concurrent player simulation for mobile game backend infrastructure.
---

# Load & Stress Testing

## Overview

This skill covers server-side load testing for mobile game backends, simulating concurrent player behavior to identify bottlenecks, capacity limits, and failure points before production deployment.

## Tools & Platforms

| Tool                    | Purpose                             |
| ----------------------- | ----------------------------------- |
| k6 / Locust             | Load generation, scenario scripting |
| Grafana                 | Real-time load test monitoring      |
| Prometheus              | Server metrics collection           |
| Custom Player Simulator | Game-specific behavior simulation   |

## Load Test Scenarios

| Scenario    | Concurrent Users   | Duration | Purpose                       |
| ----------- | ------------------ | -------- | ----------------------------- |
| Normal load | Expected DAU × 0.3 | 2 hours  | Baseline performance          |
| Peak load   | Expected DAU × 0.8 | 1 hour   | Peak hour simulation          |
| Stress test | Expected DAU × 1.5 | 30 min   | Capacity limit identification |
| Spike test  | 0 → max in 5 min   | 15 min   | Auto-scaling validation       |
| Soak test   | Expected DAU × 0.5 | 24 hours | Memory leak detection         |

## Pass Criteria

| Metric               | Target              | Alert Threshold     |
| -------------------- | ------------------- | ------------------- |
| Response time (p95)  | < 200ms             | > 500ms             |
| Error rate           | < 0.1%              | > 1%                |
| Throughput           | ≥ expected RPS      | < 80% expected      |
| Server CPU           | < 70% average       | > 85% sustained     |
| Server memory        | Stable (no growth)  | > 5% growth/hour    |
| Database connections | < 80% pool capacity | > 90% pool capacity |
