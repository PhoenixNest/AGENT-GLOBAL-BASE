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
