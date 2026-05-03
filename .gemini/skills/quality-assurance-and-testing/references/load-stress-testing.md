---
name: load-stress-testing
description: Server load testing and concurrent player simulation for mobile game backend infrastructure.
version: "1.0.0"
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

## Scope Boundary: Client vs Server Load Testing

A clear ownership boundary exists between Priya Subramanian's load testing scope and Priya Nair's (Senior Backend Engineer) backend load testing scope. Overlapping this boundary without coordination creates misleading results and duplicated effort.

### Priya Subramanian — Client-Side Load Testing (Owner)

Priya Subramanian owns all load and stress testing that originates from the game client or simulates client behavior at scale:

| Scenario                                 | Owner             | Detail                                                                                               |
| ---------------------------------------- | ----------------- | ---------------------------------------------------------------------------------------------------- |
| Game loop stress testing                 | Priya Subramanian | Sustained core gameplay loop execution; CPU/GPU/thermal impact on-device                             |
| Concurrent economy transactions (client) | Priya Subramanian | Simulated burst of client-side economy calls (item purchase, reward claim) during live event windows |
| Session stress during live event bursts  | Priya Subramanian | Stress-testing the client session layer when event systems fire at high volume                       |

### Priya Nair — Server-Side Load Testing (Owner)

Server-side capacity and throughput testing is owned by Priya Nair (Senior Backend Engineer), who operates the PlayFab backend:

| Scenario                        | Owner      | Detail                                                             |
| ------------------------------- | ---------- | ------------------------------------------------------------------ |
| PlayFab capacity planning       | Priya Nair | Backend throughput under peak DAU; Cloud Script execution capacity |
| Backend API stress              | Priya Nair | Direct load generation against PlayFab endpoints                   |
| Database / session store limits | Priya Nair | Backend infrastructure ceiling identification                      |

### Handoff: Load Test Findings Memo

When Priya Subramanian's client-side load tests reveal a **server-side bottleneck** (e.g., PlayFab API latency spiking under client burst, economy endpoints timing out during event simulation), she does not attempt to diagnose or fix the server layer. Instead, she produces a **Load Test Findings Memo** and hands it off to Priya Nair. The memo contains:

- Test scenario description and configuration
- Observed client-side symptoms (latency, error rate, timeout patterns)
- Timestamp and reproduction steps
- Hypothesis about whether the bottleneck is server-side (with supporting data

Priya Nair then takes ownership of the investigation and remediation on the backend side.
