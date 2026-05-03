---
name: test-framework-architecture
description: Extensible test framework design for game testing, including fixture management, page-object patterns for game UI, and reporting.
version: "1.0.0"
---

# Test Framework Architecture

## Overview

This skill covers the design of extensible, maintainable test frameworks for game development, following software engineering best practices adapted for game-specific testing needs.

## Architecture Patterns

### 1. Page Object Pattern (adapted for games)

| Pattern     | Game Adaptation  | Example                         |
| ----------- | ---------------- | ------------------------------- |
| Page Object | Screen Object    | `MainMenuScreen`, `LevelScreen` |
| Element     | UI Widget        | `PlayButton`, `SettingsToggle`  |
| Action      | Game Action      | `TapPlay()`, `SelectLevel(3)`   |
| Assertion   | Game State Check | `AssertLevelLoaded(3)`          |

### 2. Fixture Management

| Fixture Type   | Purpose                    | Lifecycle      |
| -------------- | -------------------------- | -------------- |
| Game State     | Reset game to known state  | Per test       |
| Player Profile | Pre-configured player data | Per test class |
| Server Mock    | Mocked backend responses   | Per test suite |
| Device Config  | Device-specific settings   | Per test run   |

### 3. Test Reporting

| Report Type       | Audience        | Content                          | Frequency     |
| ----------------- | --------------- | -------------------------------- | ------------- |
| Build Report      | Engineering     | Pass/fail per test, flaky tests  | Every build   |
| Trend Report      | QA Lead         | Pass rate over time, defect rate | Weekly        |
| Coverage Report   | Engineering+QA  | Code + gameplay coverage         | Weekly        |
| Executive Summary | Studio Director | Quality gate status, risk areas  | Per milestone |

## Collaboration Contracts

### Who Amir Works With at Each Gate

| Collaborator                              | Role in Relation to Amir                                                                                                         |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Amara Osei** (Lead QA Engineer)         | Reviews and approves all test framework architecture decisions; Amir does not merge major framework changes without her sign-off |
| **Sofia Martinez** (Gameplay Engineer #1) | Provides test hooks in gameplay code; Amir coordinates with Sofia to ensure C# gameplay systems expose testable interfaces       |
| **Ryu Tanaka** (Gameplay Engineer #2)     | Provides test hooks for UI scripting and animation systems; Amir validates that UI event hooks are automation-compatible         |

### Handoff Protocol: Amara Osei → Amir → Amara Osei

The standard QA workflow at each Stage 6 gate run follows this three-step handoff:

1. **Amara delivers the test plan** — Amara Osei authors the Stage 6 test plan (scope, priorities, pass/fail criteria) and assigns the automation tracks to Amir.
2. **Amir implements automation** — Amir builds or updates the test suite per the plan, executes it across the device farm (coordinating with Lin Zhang for device matrix runs), and aggregates results.
3. **Amir reports back to Amara** — Amir submits the test run results (pass/fail counts, failure triage, flaky test log) to Amara Osei. Amara reviews results and issues sign-off or raises a remediation request. Amir does not independently declare Stage 6 passed.
