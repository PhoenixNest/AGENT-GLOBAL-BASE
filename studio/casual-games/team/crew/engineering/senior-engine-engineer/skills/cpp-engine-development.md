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

## References

"Game Engine Architecture" (Gregory); "C++ Concurrency in Action" (Williams); GDC 2023 "Memory Management in UE5"
