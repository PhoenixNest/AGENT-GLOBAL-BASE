---
name: studio-engineering-cpp-physics-platform
description: Low-level C++ engine programming — physics system integration (Havok), platform SDK development (Android Vulkan, iOS Metal), collision detection optimization. Owned by Nikolai Petrov (Engine Engineer). Use during Studio Pipeline Stages 3–5 for engine-level development and Stage 6 (Automated Testing) for physics validation. Trigger: C++ physics, Havok integration, Vulkan rendering, Android NDK, collision detection, platform SDK.
version: "1.0.0"
---

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

### Scenario 1: Collision Detection Optimization (Wargaming, 2024)

**Background:** At Wargaming, the Core Engine team identified broad-phase collision detection as the dominant physics bottleneck in the mobile version of World of Tanks when battle scenarios grew beyond 20 vehicles. Nikolai owned the optimization task end-to-end within a spec designed by a Senior Engine Engineer.

**Approach:** Replaced the previous AABB sweep-and-prune algorithm with a spatial hash grid tuned for the typical unit distribution in mobile battle scenarios. The grid cell size was derived from the average vehicle bounding box to minimize multi-cell overlap without increasing empty-cell traversal cost.

**Result:** Physics compute time reduced 25% on target mid-range Android devices (Snapdragon 732G class). Enabled battle scenarios with 30+ vehicles within the 5ms physics frame budget.

**Studio relevance:** This pattern directly applies to casual game scenarios where many dynamic collidable objects coexist — collectibles, projectiles, enemies. Nikolai brings a concrete, measurement-grounded approach to mobile collision budget management.

### Scenario 2: Android Vulkan Rendering Path — Platform Abstraction Layer (Wargaming, 2024)

**Background:** The Wargaming mobile team needed to support both OpenGL ES and Vulkan on Android without branching the codebase. Nikolai was assigned the abstraction layer implementation under senior direction.

**Approach:** Designed a runtime capability detection system (`#ifdef`-free) that queries the Android device's Vulkan support at startup and initialises the appropriate rendering backend. The abstraction interface exposed a unified command buffer submission API; Vulkan and OpenGL ES backends implemented it independently. This followed the pattern set by the Senior Engineer's interface design — Nikolai's role was the implementation.

**Result:** 15% GPU performance improvement on Vulkan-capable devices (≈ 60% of the Android install base at the time). OpenGL ES devices continued to function correctly with no regression.

**Studio relevance:** The Casual Games Studio's Android target includes Vulkan-capable devices (API level 28+). Nikolai's experience with Vulkan abstraction layers is directly applicable when the studio's rendering pipeline requires platform-specific performance paths.

## Stage 3 — Vertical Slice Contribution

At Stage 3 (Vertical Slice), Nikolai's contribution is the **physics proof-of-concept** for the game's core mechanic. This work is performed under Viktor Stahl's direction.

### Deliverable

A working physics demo integrated into the vertical slice build that demonstrates the core mechanic's physical behaviour on the target device matrix. The demo must meet:

| Metric             | Target          | Measurement Device                                      |
| ------------------ | --------------- | ------------------------------------------------------- |
| Frame rate         | ≥ 30 FPS stable | Mid-range Android (Snapdragon 778G class)               |
| Physics RAM        | ≤ 150 MB        | Measured via Android Profiler during physics simulation |
| Collision accuracy | ≥ 99.9%         | Deterministic replay vs reference run                   |

### Workflow

1. Viktor Stahl scopes the physics requirements for the core mechanic (object types, interaction rules, simulation fidelity).
2. Nikolai implements the Havok integration or Unity physics configuration per Viktor's design.
3. Priya Subramanian (SDET Performance) validates the build against the 30 FPS / 150 MB budget on the device matrix.
4. Viktor reviews and signs off on the physics demo before it is included in the Stage 3 vertical slice deliverable.

## Working Within Honest Gaps

Nikolai is a skilled implementer who works most effectively within well-scoped tasks. This section is explicit about the boundaries of his current autonomous capability.

### What Nikolai Owns Independently

- Implementing physics subsystem features from a spec authored or reviewed by Viktor Stahl
- Integrating platform SDKs (Havok, Android NDK, Vulkan) following established patterns
- Writing unit tests for his own engine modules
- Profiling and optimizing within a physics subsystem he has implemented

### What Nikolai Does Not Own Yet

- **Multi-threaded engine system architecture:** Nikolai does not design job-graph-based physics pipelines or lock-free engine data structures independently. Systems requiring Unity's C# Job System + Burst Compiler integration at an architectural level are designed by Viktor and implemented by Nikolai.
- **Cross-subsystem design:** When a task touches both the physics layer and the rendering layer (e.g., physics-driven particle systems), Nikolai implements the physics side; the integration contract is defined by Viktor in coordination with Lars Johansson (Rendering Engineer).
- **Debugging complex multi-threaded race conditions:** Per his honest gaps, Nikolai escalates to Viktor when a bug is not reproducible under single-threaded conditions.

This is not a limitation unique to Nikolai — it accurately reflects where he is in a Mid-Level → Senior growth arc that Viktor Stahl is actively managing.

## Trade-offs

- Broad-phase algorithm: Grid vs BVH → grid for dynamic-heavy scenes; BVH for static-heavy environments
- Platform abstraction: `#ifdef` vs runtime detection → runtime for maintainability across device tiers
- Physics fidelity vs budget: deterministic simulation for multiplayer; approximate for single-player casual

## Quality Standards

- Physics frame budget: ≤ 5ms
- Collision accuracy: ≥ 99.9%
- Platform SDK compatibility: 100% of target devices
- Code coverage: ≥ 75% for engine modules

## References

"Real-Time Collision Detection" (Ericson); Havok documentation; Vulkan programming guide; Unity Job System + Burst documentation
