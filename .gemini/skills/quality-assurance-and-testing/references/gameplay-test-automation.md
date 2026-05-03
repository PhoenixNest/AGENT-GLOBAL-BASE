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

## Studio Context and Device Farm

### Device Farm Setup

The Casual Games Studio operates a physical device farm of 20+ Android devices used for matrix testing across the target device tier spread. Amir's gameplay automation suite is designed to run on this farm as its primary execution environment.

| Farm Component     | Detail                                                                                    |
| ------------------ | ----------------------------------------------------------------------------------------- |
| Device count       | 20+ Android physical devices                                                              |
| Coverage purpose   | Android API level matrix, GPU vendor spread (Qualcomm, Mali, PowerVR), RAM tier coverage  |
| Execution trigger  | Nightly and Stage 6 gate runs                                                             |
| Orchestration tool | Unity Test Runner with Appium for UI-layer test execution where Unity APIs are not enough |

### Automation Suite Integration with Device Farm

Amir's gameplay automation suite runs inside Unity's test runner (EditMode + PlayMode tests) for game-logic-level assertions. For interaction-layer tests (UI flow, session transitions) Appium is used to drive the device externally and Unity Test Runner is used for internal game state validation. The two work together:

```
GitHub Actions CI
  → Build APK (Unity Cloud Build or local Unity build server)
  → Deploy to device farm (20+ Android devices via ADB batch push)
  → Unity Test Runner: core gameplay tests, economy validation
  → Appium: session lifecycle, UI interaction
  → Collect results → TestRail report → Amara Osei review
```

### Casual Game Test Patterns

| Pattern                         | What It Tests                                                    | Tooling                           |
| ------------------------------- | ---------------------------------------------------------------- | --------------------------------- |
| Session lifecycle tests         | App launch → main menu → game entry → session close; state saved | Appium + Unity Test Runner        |
| Core loop regression            | Primary game loop repeatable N times without state drift         | Custom Bot Engine (deterministic) |
| Economy transaction validation  | Currency grant, spend, refund; server-authoritative result check | Unity Test Runner + PlayFab SDK   |
| Session interruption resilience | Backgrounding, incoming calls, resume — state preserved          | Appium device-level signals       |
