---
name: economy-design
description: F2P economy design, virtual currency balancing, pricing models, and data-driven economy iteration for mobile games.
version: "1.0.0"
---

# Economy Design

## Overview

This skill covers the design, balancing, and continuous optimization of virtual economies in F2P mobile games, including currency modeling, pricing strategy, and data-driven iteration.

## Core Methodologies

### 1. Currency Architecture

| Currency Type  | Acquisition                  | Consumption               | Design Goal                   |
| -------------- | ---------------------------- | ------------------------- | ----------------------------- |
| Soft Currency  | Level rewards, daily bonuses | Upgrades, boosts          | Engagement loop driver        |
| Hard Currency  | IAP, achievements, events    | Premium items, time skips | Revenue driver                |
| Energy         | Time regen, IAP, friends     | Level attempts            | Session pacing                |
| Event Currency | Event-specific activities    | Event rewards             | Limited-time engagement spike |

### 2. Economy Balancing Process

1. **Design Phase:** Define currency sources and sinks, model expected player accumulation rate
2. **Simulation Phase:** Run Monte Carlo simulation of player behavior (10K+ virtual players)
3. **Playtest Phase:** Internal testing with calibrated difficulty and reward values
4. **Soft Launch Phase:** Real player data analysis, cohort-level economy health monitoring
5. **Live Phase:** Continuous monitoring and adjustment based on real economy data

### 3. Economy Health Metrics

| Metric                  | Target Range          | Alert Threshold      |
| ----------------------- | --------------------- | -------------------- |
| Currency inflation rate | < 5% monthly          | > 10% monthly        |
| Sink/source ratio       | 0.9–1.1 (balanced)    | < 0.8 or > 1.2       |
| IAP conversion rate     | 3–5%                  | < 2% or > 8%         |
| ARPPU                   | $10–$30/month         | < $5 or > $50        |
| Paywall detection       | 0% progression blocks | Any block identified |
