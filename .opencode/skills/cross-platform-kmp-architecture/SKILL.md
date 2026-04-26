---
name: cross-platform-kmp-architecture
description: Kotlin Multiplatform (KMP) architecture — shared module design, expect/actual patterns, Ktor shared networking, SQLDelight database, Kotlin/Native memory model, and cross-platform clean architecture. Owned by Mei-Ling Johansson (Cross-Platform Lead). Use during Stage 3 (UML Engineering) for KMP architecture design and Stage 5 (Development) for KMP shared module implementation. Trigger: KMP architecture, Kotlin Multiplatform, expect/actual, Ktor, SQLDelight, shared module architecture.
prerequisites:
  - cross-platform-overview

version: "1.0.0"
---

# KMP Architecture

**Category:** Mobile Engineering — Cross-Platform Architecture (KMP)
**Owner:** Cross-Platform Engineer (Dmitri Volkov)

## Overview

This skill defines Clean Architecture with Kotlin Multiplatform covering shared domain layer design, platform adapters, dependency injection across platforms, and architectural boundary enforcement. It applies to Stage 5 (Development) where the architectural backbone for cross-platform code is established, Stage 6 (Code Review) where layer compliance and boundary enforcement are audited, and Stage 8 (Integrity Verification) where architectural integrity is verified on both platforms.

## Competency Dimensions

| Dimension                   | Description                                                                                                | Proficiency Indicators                                                                                                                    |
| --------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Clean Architecture with KMP | Layer separation across platform boundaries, dependency inversion, shared domain, platform adapters        | Domain layer in commonMain with zero platform dependencies; platform adapters implement domain interfaces; dependency graph flows inward  |
| Shared Domain Layer         | Pure Kotlin entities, use case interactors, repository interfaces, error hierarchies, validation           | All domain code in commonMain; use cases are testable on JVM; error types are sealed interfaces; validation logic is shared               |
| Platform Adapters           | Adapter pattern for platform-specific implementations, interface contracts, adapter testing                | Each platform implements domain interfaces via adapters; adapters are thin wrappers; adapter behavior tested per platform                 |
| Cross-Platform DI           | Koin module composition, platform-specific module overrides, test module substitution, lazy initialization | DI modules composed per platform; shared modules define core bindings; platform modules override as needed; test modules substitute mocks |
| Boundary Enforcement        | Compile-time checks, source set dependencies, import restrictions, architecture tests                      | Domain layer cannot import platform packages; architecture tests run on CI; import violations caught at compile time                      |

## Pipeline Integration

- **Stage 3 (Architecture):** ADR establishes Clean Architecture with KMP. Layer boundaries, shared domain scope, and platform adapter contracts defined.
- **Stage 4 (Implementation Plan):** Architecture tasks include: shared module setup, domain layer design, platform adapter contracts, DI module composition.
- **Stage 5 (Development):** Primary skill for KMP architecture implementation. All shared domain code, platform adapters, and DI modules.
- **Stage 6 (Code Review):** Architecture review: layer boundary compliance, expect/actual completeness, DI module correctness, platform adapter thinness.
- **Stage 8 (Integrity Verification):** Architecture tests run on both platforms. Shared domain behavior verified to be identical across platforms.

## Quality Standards

- **Zero** platform imports in commonMain/domain — compile-time enforced
- **100%** domain use cases testable on JVM — no platform dependencies
- Repository interfaces defined in domain — **implemented** in platform adapters
- Platform adapters are **thin wrappers** — no business logic in adapters
- DI modules composed per platform — **sharedModule + platformModule** pattern
- Either type used for error handling — **no exceptions** crossing layer boundaries
- All domain entities are **Serializable** — for cross-platform data transfer
- Use cases have **single responsibility** — one use case per file
- Architecture tests run on **CI** — layer violations caught automatically
- Shared module **>70% code sharing** ratio for business logic
- Platform-specific code limited to: UI, storage, networking engine, cryptography

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
