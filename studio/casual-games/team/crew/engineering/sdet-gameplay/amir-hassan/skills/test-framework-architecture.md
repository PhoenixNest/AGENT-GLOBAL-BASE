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
