---
name: architecture-guidelines-cross-platform-architecture
description: Cross-platform mobile architecture for KMP and Flutter — shared-core strategies, API design for mobile clients, offline-first synchronization, cross-platform security patterns, and architecture-to-implementation traceability. Owned by Rafael Okonkwo (Software Architect). Use during Stage 3 (UML Engineering) for cross-platform architecture design and Stage 5 (Development) for layer conformance. Trigger: cross-platform architecture, KMP architecture, Flutter architecture, shared core, offline-first sync, mobile API design.
prerequisites:
  - architecture-overview

version: "1.0.0"
---

# Cross-Platform Architecture

**Category:** Architecture
**Owner:** Senior Software Architect

## Overview

This skill covers mobile cross-platform architecture patterns, shared-core strategies, API design for mobile clients, offline-first synchronization, and architecture-to-implementation traceability. It bridges the gap between system-level design decisions (system-design skill) and platform-specific implementation, providing concrete guidance for Stage 3 architecture packages and conformance verification at Stages 6 and 8.

## Competency Dimensions

| Dimension                  | Description                                                                                                          | Proficiency Indicators                                                                                                                                    |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mobile Pattern Selection   | Choosing among native, cross-platform, hybrid, and PWA with evidence-based trade-off analysis                        | Produces scored comparison matrix for target product; selection is justified by team capability, performance requirements, and time-to-market constraints |
| Platform Layering          | Designing clean boundaries between shared business logic and platform-specific adapters (KMP, Flutter, React Native) | Layer dependency graph has depth ≤ 4; no circular dependencies; each layer has explicit public API and concealed internals                                |
| API Design for Mobile      | Designing APIs optimized for mobile constraints (latency, bandwidth, battery, intermittent connectivity)             | All endpoints support pagination, partial responses, and delta sync; mobile-specific error codes documented; retry-safe by design                         |
| Offline-First Architecture | Local database synchronization with conflict resolution, optimistic UI, and CRDTs                                    | Sync engine handles all conflict scenarios; merge strategy is documented and tested; data consistency guarantees are explicit                             |
| Cross-Platform Security    | Certificate pinning, secure storage, JWT lifecycle, biometric authentication across iOS and Android                  | Security patterns are implemented identically on both platforms; no platform-specific security gaps; OWASP MASVS L2 compliance                            |
| Build System Architecture  | Monorepo structure, shared CI/CD pipelines, feature flag orchestration across platforms                              | Build dependency depth ≤ 4; feature flags synchronized across platforms within 1 hour; reproducible builds                                                |
| Performance Budgets        | Memory limits, background execution constraints, battery optimization per platform                                   | Performance budgets defined and enforced; budget violations caught in CI; platform-specific constraint documentation is current                           |
| Architecture Traceability  | UML-to-code mapping, ADR enforcement, architecture conformance testing                                               | Every UML component maps to a module/package; ADR compliance is verified programmatically; architecture drift is detected before merge                    |

## Pipeline Integration

| Stage                                | Application                                                                                                                                                                                                                                                                                                                        |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 3 (Architecture)**           | Primary application stage. Produce UML component diagrams showing platform layering (shared core, platform adapters, feature modules). Draft ADRs for mobile pattern selection (native vs. KMP vs. Flutter), API protocol choice, offline sync strategy, and security patterns. Define module dependency graph with maximum depth. |
| **Stage 4 (Implementation Plan)**    | Translate architecture into implementation tasks per platform. Define shared module build configuration, CI/CD pipeline setup, performance budget baselines, and feature flag infrastructure. Map each UML component to a code module in the traceability matrix.                                                                  |
| **Stage 5 (Development)**            | Platform leads implement per the architecture package. Shared team builds KMP shared module first (domain + data layers), then platform teams build UI layer. Architecture conformance tests run on every PR. Performance budgets are measured and tracked.                                                                        |
| **Stage 6 (Code Review)**            | Verify implementation conforms to ADRs and UML diagrams. Check module dependency depth ≤ 4. Verify security patterns (certificate pinning, secure storage, JWT rotation) are implemented identically on both platforms. Check offline sync implementation against the conflict resolution strategy defined in ADRs.                |
| **Stage 8 (Integrity Verification)** | Validate offline-first behavior end-to-end: simulate network partition, verify local mutations queue correctly, verify conflict resolution produces correct results. Verify performance budgets are met on target devices. Confirm traceability matrix is complete (every UML component has a code module).                        |
| **Stage 10 (Release Readiness)**     | Confirm cross-platform parity (feature parity, security parity, performance parity between iOS and Android). Verify feature flags are synchronized. Confirm App Store / Google Play requirements are met for both platforms. Sign off on architecture domain.                                                                      |

## Quality Standards

| Standard                               | Measurement                                    | Target                       |
| -------------------------------------- | ---------------------------------------------- | ---------------------------- |
| Module dependency depth                | Maximum path length in dependency graph        | ≤ 4                          |
| Code sharing ratio                     | Lines of shared code / total codebase          | ≥ 60% (KMP), ≥ 85% (Flutter) |
| Architecture conformance               | ADR violations in codebase                     | 0                            |
| Offline sync reliability               | Successful sync after simulated partition      | ≥ 99.5%                      |
| Conflict resolution correctness        | Conflict resolution test pass rate             | 100%                         |
| Certificate pinning coverage           | All API endpoints pinned                       | 100%                         |
| JWT rotation correctness               | Token rotation without data loss               | 100%                         |
| Performance budget compliance          | All metrics within budget in CI                | 100%                         |
| Binary size                            | iOS and Android binary size                    | < 120 MB each                |
| Cold launch time                       | Measured on mid-range device                   | < 2s both platforms          |
| Traceability completeness              | UML components with corresponding code module  | 100%                         |
| ADR-to-code linkage                    | Every ADR has traceable implementation         | 100%                         |
| Cross-platform feature parity          | Features implemented on both platforms         | 100% at release              |
| Architecture conformance test coverage | Module graph tests, interface compliance tests | Run on every PR              |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
