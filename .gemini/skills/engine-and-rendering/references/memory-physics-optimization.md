---
name: studio-engineering-memory-physics-optimization
description: Memory management and physics system optimization — custom allocators, GC tuning, fragmentation reduction, collision detection, deterministic sync for mobile games. Owned by Viktor Stahl (Senior Engine Engineer). Use during Studio Pipeline Stages 5–6 for engine-level optimization and Stage 8 (Soft Launch) for performance validation. Trigger: memory optimization, physics optimization, custom allocators, collision detection, deterministic physics, fragmentation.
version: "1.0.0"
---

# Memory & Physics Optimization

**Skill Owner:** Viktor Stahl | **Version:** 1.0 | **Date:** 2026-04-20

## Description

Memory management (custom allocators, GC tuning, fragmentation reduction) and physics system optimization (collision detection, deterministic sync, profiling).

## Tools & Frameworks

| Tool                      | Version | Context                                       |
| ------------------------- | ------- | --------------------------------------------- |
| Custom Pool Allocators    | —       | Designed for UE5; lock-free concurrent access |
| Havok Physics             | 2023.2  | Integration and optimization                  |
| Physics Profiler (custom) | —       | Built for 200+ internal devs at Epic          |
| Intel VTune               | 2024    | CPU profiling; cache analysis                 |

## Production Scenarios

**Scenario 1: Physics Profiler (Epic 2023)** — Built custom physics profiler identifying bottlenecks in collision detection, constraint solving, and rigid body simulation. Result: Used by 200+ devs; average physics optimization improved 30%.
**Scenario 2: Mobile Memory Optimization (Epic 2024)** — Reduced mobile memory footprint by 35% through custom allocators and object lifecycle management. Result: Enabled UE5 games to run on 4GB RAM devices.

## Trade-offs

- Pool allocator vs slab vs general → pool for fixed-size; slab for variable
- Deterministic vs approximate physics → deterministic for multiplayer
- Real-time vs offline profiling → both; real-time for development, offline for deep analysis

## Quality Standards

- Physics frame budget: ≤ 5ms
- Memory fragmentation: ≤ 10%
- Profiler overhead: ≤ 3% frame time
- Physics determinism: bit-exact across platforms

## Mentorship of Nikolai Petrov

Viktor Stahl is the direct supervisor of Nikolai Petrov (Engine Engineer, Mid-Level L1). The following structure governs their working relationship and Nikolai's development toward seniority.

### Task Assignment Model

Viktor assigns Nikolai to **scoped physics subsystem tasks** — implementation work with clearly bounded interfaces and well-defined success criteria. Viktor does not assign Nikolai to open-ended architecture tasks until Nikolai has demonstrated readiness. Current scope: Havok integration maintenance, collision detection optimisation tasks, platform SDK work on Android Vulkan paths.

### Working Cadence

- **Weekly 1:1 (60 minutes):** Viktor reviews Nikolai's code in progress, identifies any correctness or performance issues, and adjusts the task scope if needed.
- **Code review:** Viktor reviews all of Nikolai's code before it enters the main branch. Nikolai does not merge engine-level code without Viktor's explicit approval.

### Escalation

If Nikolai's tasks are delayed **more than 50% beyond their original estimate**, Viktor escalates to Dmitri Volkov (Senior Game Engineer). Viktor does not absorb scope slippage silently — early escalation is the expected protocol.

### Growth Trajectory

Viktor's explicit goal is to ramp Nikolai from Mid-Level (L1) to Senior over **18 months** by progressively increasing the autonomy and complexity of his assignments:

| Phase       | Timeframe    | Task Type                                                                    |
| ----------- | ------------ | ---------------------------------------------------------------------------- |
| Foundation  | Months 1–6   | Scoped implementation tasks with detailed specs; daily feedback loops        |
| Expansion   | Months 7–12  | Subsystem ownership with Viktor's design; Nikolai designs the implementation |
| Senior prep | Months 13–18 | Nikolai proposes design for small subsystem; Viktor reviews and approves     |

Progress against this trajectory is assessed quarterly by Viktor and reported to Dmitri Volkov.

## References

GDC 2023 "Physics Profiling at Epic"; "Real-Time Collision Detection" (Ericson); Havok documentation
