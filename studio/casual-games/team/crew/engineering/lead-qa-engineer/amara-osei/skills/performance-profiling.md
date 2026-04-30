---
name: studio-qa-performance-profiling
description: Mobile game performance testing and profiling — FPS validation, memory benchmarking, load time testing, battery drain measurement, and thermal throttling assessment for iOS and Android. Owned by Amara Osei (Lead QA Engineer). Trigger: performance testing, FPS, frame rate, memory test, load time, battery drain, profiling, thermal throttling.
version: "1.0.0"
---

# Performance Profiling

**Skill Owner:** Amara Osei (Lead QA Engineer)
**Applies To:** Performance Testing, FPS Validation, Memory Testing, Battery and Thermal Testing

## Tools & Frameworks

| Tool/Framework            | Version Context | Usage                                             |
| ------------------------- | --------------- | ------------------------------------------------- |
| Unity Profiler            | Built-in        | CPU/GPU/memory frame-level profiling              |
| Android GPU Inspector     | Latest          | GPU workload profiling on Android                 |
| Xcode Instruments         | Latest          | CPU, memory, battery, and thermal profiling (iOS) |
| Firebase Performance      | Latest          | Real-device production performance monitoring     |
| Android Battery Historian | Latest          | Battery drain and wake lock analysis              |
| Custom FPS Counter        | Studio-built    | Overlay for QA test captures during session       |
| Perfetto                  | Latest          | Android system-level tracing for thermal analysis |

## Performance Budget (Studio Baseline)

These targets are set by Dmitri Volkov and enforced by Amara's QA gates at Stage 6 and Stage 7:

| Metric                  | Minimum Spec Target | Target Spec Target | Measurement Device               |
| ----------------------- | ------------------- | ------------------ | -------------------------------- |
| Frame rate (gameplay)   | ≥30fps sustained    | ≥60fps sustained   | Pixel 4a / iPhone 11             |
| Frame rate (UI menus)   | ≥60fps              | ≥60fps             | All devices                      |
| Cold start time         | ≤12 seconds         | ≤8 seconds         | Clean install                    |
| Level load time         | ≤6 seconds          | ≤3 seconds         | After first play (assets cached) |
| Memory usage (peak)     | ≤60% available RAM  | ≤45% available RAM | Unity Memory Profiler            |
| Battery drain           | ≤18% per hour       | ≤12% per hour      | 30-minute active play session    |
| App size (base install) | ≤90MB               | ≤80MB              | Store submission size            |

## Real-World Production Scenarios

### Scenario 1: FPS Regression Investigation

**Context:** Nightly build shows a 15fps regression on minimum spec Android device.
**Process:**

1. Reproduce on physical minimum spec device; confirm regression is consistent
2. Use `git bisect` with the CI build history to identify the commit that introduced the regression
3. Profile the problematic build with Unity Profiler connected to device; capture 5 seconds of the affected game state
4. Identify CPU vs. GPU bound: if "Gfx.WaitForPresent" is high, it's GPU-bound; if it's `Update()` or `BehaviourUpdate`, it's CPU-bound
5. Share profiler capture with Dmitri; engineer who owns the area investigates root cause
6. The regression MUST be resolved before Stage 6 sign-off; it's automatically classified as P1

### Scenario 2: Pre-Launch Performance Sweep

**Context:** Title is entering Stage 7 (Soft Launch Prep); full performance sweep required.
**Process:**

1. Run FPS validation across all game modes (onboarding, core loop, meta loop, shop) on full device matrix
2. Conduct 30-minute sessions to measure battery drain and check for thermal throttling (CPU governor stepping down)
3. Measure cold start and warm start times in Clean Install conditions
4. Test under memory pressure: enable background apps on minimum spec device, then launch the game
5. Validate build size matches the performance budget target
6. Document all results in the **Performance Baseline Report** — this becomes the regression baseline for live ops

### Scenario 3: Memory Pressure Testing

**Context:** Reports of crashes on older Android devices in early access.
**Process:**

1. Enable developer options on minimum spec device; set Background process limit to 0 (simulate memory pressure)
2. Play game for 20 minutes; observe memory trend in Unity Memory Profiler
3. Trigger memory pressure via `adb shell am send-trim-memory <pid> RUNNING_CRITICAL`
4. Verify game responds correctly: it should free non-essential assets and continue running
5. If it crashes, classify as P0; identify the memory allocation spike causing the OOM kill

## Measurable Quality Standards

| Standard                      | Target                      | Measurement Method           |
| ----------------------------- | --------------------------- | ---------------------------- |
| No performance regressions    | 0 between Stage 6 builds    | Automated nightly comparison |
| P0/P1 performance issues open | 0 at Stage 7                | JIRA defect log              |
| Profiling coverage            | All game modes tested       | Performance baseline report  |
| Device matrix coverage        | Min spec + 3 common devices | Test matrix documentation    |
