---
name: studio-engineering-cpp-engine-development
description: Low-level C++ game engine development — memory management, custom allocators, lock-free data structures, engine architecture for mobile game engines. Owned by Viktor Stahl (Senior Engine Engineer). Use during Studio Pipeline Stages 3–5 for engine-level development and Stage 6 (Automated Testing) for engine validation. Trigger: C++ engine development, custom allocators, lock-free structures, memory management, engine architecture.
version: "1.0.0"
---

# C++ Engine Development

**Skill Owner:** Viktor Stahl | **Version:** 1.0 | **Date:** 2026-04-20

## Description

Low-level C++ game engine development including memory management, custom allocators, lock-free data structures, and engine architecture.

## Tools & Frameworks

| Tool          | Version | Context                                                 |
| ------------- | ------- | ------------------------------------------------------- |
| C++           | 20      | Modern C++ for engine development; concepts, coroutines |
| Unreal Engine | 5.2+    | Engine source contributor; memory management subsystem  |
| CMake         | 3.26    | Build system configuration                              |
| LLVM/Clang    | 16      | Static analysis; sanitizers (ASan, TSan, MSan)          |

## Production Scenarios

**Scenario 1: UE5 Memory Management (Epic 2023)** — Redesigned memory allocation strategy reducing fragmentation by 45%. Implemented custom pool allocators for frequently allocated/deallocated game objects. Result: 45% fragmentation reduction; 15% overall memory savings.
**Scenario 2: Deterministic Physics Sync (Epic 2024)** — Built lock-free physics synchronization for cross-platform mobile multiplayer. Result: Enabled Fortnite Mobile cross-platform play; zero physics desync reports.

## Trade-offs

- Standard allocator vs custom → custom for hot paths; standard for cold paths
- Mutex-based vs lock-free → lock-free for performance-critical paths
- Monolithic engine vs modular → modular for team parallelism

## Quality Standards

- Memory fragmentation: ≤ 10%
- Allocator overhead: ≤ 2% of frame time
- Lock-free structure correctness: verified by TSan + formal proof
- Cache hit rate: ≥ 95% for hot data

## Unity 6 LTS Integration Context

Viktor's C++ background does not disappear in a Unity studio — it manifests through Unity's native interop layer. This section defines how his low-level C++ expertise applies specifically to the Casual Games Studio's Unity 6.3 LTS environment.

### Native Plugin Development

Viktor authors and maintains C++ native plugins that Unity's managed C# layer calls via P/Invoke. Studio use cases:

| Plugin Purpose                  | Platform | Detail                                                                                                                                             |
| ------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| iOS Metal performance path      | iOS      | Custom Metal command buffer management for render-critical operations, bypassing Unity's abstraction overhead                                      |
| Android Vulkan performance path | Android  | Vulkan pipeline state caching and explicit synchronization, reducing driver overhead                                                               |
| Custom memory allocators        | Both     | Pool allocators exposed to Unity via native plugin interface; used for frequently instantiated game objects (projectiles, particles, collectibles) |

### Burst Compiler Review

Unity's Burst compiler translates a subset of C# (HPC#) into optimized native code. Viktor reviews Burst-compiled jobs for:

- Correct use of `NativeArray`, `NativeList`, and other Burst-compatible data structures
- Absence of managed allocations inside Burst jobs (which cause Burst to fall back to slower code paths)
- Vectorization-friendly data layouts (SoA vs AoS)
- Correctness under Unity's job system threading model

Viktor's review is the final gate before Burst-compiled systems enter the main branch.

### IL2CPP Build Pipeline Management

Viktor owns the IL2CPP build pipeline for iOS and Android release builds:

- Configuring IL2CPP code generation settings (Full Generic Sharing, incremental build)
- Diagnosing IL2CPP-specific runtime issues (e.g., managed-to-native marshalling overhead, stripped code causing `MissingMethodException`)
- Working with the Unity linker configuration (`link.xml`) to prevent necessary code from being stripped

### The Bridge Role

Viktor is the go-to engineer when Unity's managed C# abstractions hit performance ceilings. When a gameplay engineer identifies a performance bottleneck that cannot be solved within C#, they escalate to Viktor. Viktor evaluates whether a native plugin, Burst job, or IL2CPP configuration change is the appropriate solution.

## References

"Game Engine Architecture" (Gregory); "C++ Concurrency in Action" (Williams); GDC 2023 "Memory Management in UE5"
