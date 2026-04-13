---
name: performance-testing
description: Mobile game performance testing including FPS benchmarking, memory profiling, GPU analysis, and thermal stress testing.
---

# Performance Testing

## Overview

This skill covers comprehensive performance testing for mobile games, measuring and optimizing frame rate, memory usage, GPU performance, CPU utilization, and thermal behavior across target device configurations.

## Tools & Platforms

| Tool              | Purpose                                    |
| ----------------- | ------------------------------------------ |
| Xcode Instruments | iOS profiling (Time Profiler, Allocations) |
| Android Profiler  | Android profiling (CPU, Memory, Energy)    |
| RenderDoc         | GPU frame capture, draw call analysis      |
| GameBench         | Real-time performance monitoring           |
| Custom FPS Tool   | Frame time histogram analysis              |

## Performance Targets

| Metric              | Target               | Minimum Acceptable | Measurement Method       |
| ------------------- | -------------------- | ------------------ | ------------------------ |
| Average FPS         | 60 fps               | 30 fps             | Frame time sampling      |
| Frame time variance | < 1% of frame budget | < 5%               | Histogram analysis       |
| Memory (low-end)    | < 500 MB             | < 800 MB           | Instruments/Profiler     |
| Memory (flagship)   | < 1 GB               | < 1.5 GB           | Instruments/Profiler     |
| GPU utilization     | < 80% sustained      | < 95% sustained    | RenderDoc frame analysis |
| Device temperature  | < 42°C sustained     | < 45°C sustained   | Thermal camera/IR sensor |
| App startup time    | < 3 seconds          | < 5 seconds        | Cold start measurement   |

## Testing Cadence

| Test Type        | Frequency     | Device Coverage | Pass Criteria            |
| ---------------- | ------------- | --------------- | ------------------------ |
| FPS benchmark    | Every RC      | Tier 1 + Tier 2 | 60fps avg, < 5% variance |
| Memory profiling | Weekly        | Tier 1 + Tier 3 | Under memory targets     |
| Thermal stress   | Per milestone | Tier 1          | Under temp targets       |
| GPU analysis     | Monthly       | Tier 1          | Under GPU utilization    |
| Startup time     | Every RC      | All tiers       | Under startup targets    |
