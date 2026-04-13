# C++ Physics & Platform Integration

**Skill Owner:** Nikolai Petrov | **Version:** 1.0 | **Date:** 2026-04-20

## Description

Low-level C++ programming for game engines, physics system integration (Havok), and platform SDK development (Android Vulkan, iOS Metal).

## Tools & Frameworks

| Tool          | Version | Context                    |
| ------------- | ------- | -------------------------- |
| C++           | 17      | Engine-level programming   |
| Havok Physics | 2023.2  | Physics SDK integration    |
| Android NDK   | r25     | Native Android development |
| Vulkan SDK    | 1.3     | Android graphics API       |

## Production Scenarios

**Scenario 1: Collision Detection Optimization (Wargaming 2024)** — Optimized broad-phase collision detection using spatial hashing. Result: Physics compute time reduced 25%; enabled larger battle scenarios.
**Scenario 2: Vulkan Rendering Path (Wargaming 2024)** — Implemented platform abstraction layer for Android Vulkan rendering. Result: 15% GPU performance improvement on Vulkan-capable devices.

## Trade-offs

- Broad-phase algorithm: Grid vs BVH → grid for dynamic; BVH for static-heavy
- Platform abstraction: #ifdef vs runtime detection → runtime for maintainability

## Quality Standards

- Physics frame budget: ≤ 5ms
- Collision accuracy: ≥ 99.9%
- Platform SDK compatibility: 100% of target devices
- Code coverage: ≥ 75% for engine modules

## References

"Real-Time Collision Detection" (Ericson); Havok documentation; Vulkan programming guide
