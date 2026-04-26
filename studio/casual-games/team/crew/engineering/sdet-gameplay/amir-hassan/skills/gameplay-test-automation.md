---
name: gameplay-test-automation
description: Bot-driven gameplay testing, regression test automation, and CI/CD integration for game development.
version: "1.0.0"
---

# Gameplay Test Automation

## Overview

This skill covers the design and implementation of automated gameplay testing systems using AI-driven bots, scripted test scenarios, and CI/CD integration for continuous quality assurance.

## Tools & Frameworks

| Tool                 | Purpose                                |
| -------------------- | -------------------------------------- |
| Unity Test Framework | Unit and integration testing for Unity |
| Custom Bot Engine    | AI-driven gameplay simulation          |
| GitHub Actions       | CI/CD test execution orchestration     |
| TestRail             | Test case management and reporting     |
| ADB / XCUITest       | Mobile device automation               |

## Core Methodologies

### 1. Bot-Driven Testing Architecture

```
Test Orchestrator → Bot Controller → Game Instance → Result Collector → Report Generator
                         ↓
                    Behavior Tree / State Machine
                         ↓
                    Input Generator (deterministic + randomized)
```

| Bot Type        | Purpose                             | Coverage         |
| --------------- | ----------------------------------- | ---------------- |
| Navigation Bot  | Pathfinding, level traversal        | Map completeness |
| Combat Bot      | Attack patterns, enemy AI testing   | Combat system    |
| Progression Bot | Level completion, unlock testing    | Game progression |
| Chaos Bot       | Randomized input, edge case hunting | Crash detection  |

### 2. Regression Test Suite

| Test Category     | Frequency    | Execution Time | Automation Target |
| ----------------- | ------------ | -------------- | ----------------- |
| Smoke tests       | Every commit | < 5 minutes    | 100%              |
| Core gameplay     | Every PR     | < 30 minutes   | 90%               |
| Full regression   | Nightly      | < 4 hours      | 85%               |
| Platform-specific | Weekly       | < 8 hours      | 80%               |

### 3. CI/CD Integration

| Pipeline Stage    | Trigger        | Test Suite      | Gate Criteria              |
| ----------------- | -------------- | --------------- | -------------------------- |
| Pre-merge         | PR opened      | Smoke tests     | 100% pass                  |
| Post-merge        | Code merged    | Core gameplay   | ≥ 95% pass                 |
| Nightly           | Scheduled      | Full regression | ≥ 90% pass                 |
| Release candidate | Manual trigger | Full + platform | 100% pass (P0), ≥ 95% (P1) |
