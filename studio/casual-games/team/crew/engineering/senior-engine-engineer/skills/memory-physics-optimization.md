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

## References

GDC 2023 "Physics Profiling at Epic"; "Real-Time Collision Detection" (Ericson); Havok documentation
