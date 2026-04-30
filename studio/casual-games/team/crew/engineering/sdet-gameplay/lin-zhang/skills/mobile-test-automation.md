---
name: mobile-test-automation
description: Mobile game test automation covering device farm management, cross-platform testing, touch input simulation, and platform certification testing.
version: "1.0.0"
---

# Mobile Test Automation

## Overview

This skill covers automated testing for mobile games across iOS and Android platforms, including device farm management, cross-platform test execution, touch input simulation, and platform certification testing.

## Tools & Platforms

| Tool              | Purpose                               |
| ----------------- | ------------------------------------- |
| Appium            | Cross-platform mobile test automation |
| XCUITest          | iOS-specific UI automation            |
| UiAutomator2      | Android-specific UI automation        |
| Firebase Test Lab | Cloud device farm testing             |
| BrowserStack      | Additional device coverage            |

## Core Methodologies

### 1. Device Farm Strategy

| Device Tier        | Devices Covered         | Test Frequency | Purpose                          |
| ------------------ | ----------------------- | -------------- | -------------------------------- |
| Tier 1 (Flagship)  | iPhone 15+, Galaxy S24+ | Every build    | Primary QA, performance baseline |
| Tier 2 (Mid-range) | iPhone 13, Galaxy A54   | Nightly        | Main user base coverage          |
| Tier 3 (Budget)    | Older/low-end devices   | Weekly         | Edge case, accessibility         |

### 2. Touch Input Simulation

| Input Type   | Implementation                 | Test Coverage            |
| ------------ | ------------------------------ | ------------------------ |
| Single tap   | Coordinate-based tap           | UI buttons, menus        |
| Swipe/drag   | Multi-point gesture simulation | Match-3 swaps, scrolling |
| Pinch/zoom   | Multi-touch simulation         | Camera, map zoom         |
| Long press   | Timed touch + hold             | Context menus, power-ups |
| Multi-finger | Simultaneous touch points      | Gesture combos           |

### 3. Visual Regression Testing

- Automated screenshot comparison with perceptual diff (SSIM ≥ 0.95 threshold)
- Platform-specific baseline images maintained per device tier
- False positive reduction: ignore anti-aliasing differences, dynamic elements (particle effects)

## Device vs Bot Responsibility Split

The studio's SDET team separates test _authorship_ from test _execution at scale_. Amir Hassan and Lin Zhang have distinct, non-overlapping ownership areas:

| Dimension             | Amir Hassan (SDET Gameplay #1)                                        | Lin Zhang (SDET Gameplay #2)                                                     |
| --------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Primary ownership** | Test framework architecture — test suite design, bot engine, CI hooks | Device-specific test execution — physical device farm runs, platform parity      |
| **Test authorship**   | Authors the canonical test suite (gameplay, session, economy tests)   | Runs the suite Amir authors across the full Android device matrix                |
| **iOS coverage**      | Not the primary owner                                                 | Owns iOS simulator parity checks — validating test suite runs cleanly on iOS     |
| **Android matrix**    | Designs tests to be device-agnostic                                   | Owns Android-version matrix runs (API 26 through API 35 across 20+ farm devices) |
| **Artifacts owned**   | Test suite source code, framework architecture doc                    | **Device Test Report** — produced after each Stage 6 gate run                    |

### Device Test Report

Lin Zhang produces the **Device Test Report** as the authoritative artifact after each Stage 6 gate run. This report documents:

- Pass/fail results per device model and Android API level
- Any device-specific failures that did not appear in Amir's baseline runs
- iOS simulator parity status (pass / known deviations / blocking failures)
- Thermal or performance anomalies observed during farm execution

The Device Test Report is submitted to Amara Osei (Lead QA Engineer) alongside Amir's test run summary as dual inputs to Stage 6 sign-off.
