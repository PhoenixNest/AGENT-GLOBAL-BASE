---
name: studio-engineering-backend-abstraction-layer
description: Vendor-agnostic backend abstraction layer design — interface-based architecture, adapter patterns, dependency injection to prevent vendor lock-in for game backends. Owned by Priya Nair (Senior Backend Engineer). Use during Studio Pipeline Stages 3–5 for backend architecture and Stage 4 (Production Planning) for technology selection. Trigger: backend abstraction, vendor lock-in prevention, adapter pattern, interface design, microservices migration.
version: "1.0.0"
---

# Backend Abstraction Layer Design

**Skill Owner:** Priya Nair | **Version:** 1.0 | **Date:** 2026-04-20

## Description

Design of vendor-agnostic backend abstraction layers using interface-based architecture, adapter patterns, and dependency injection to prevent vendor lock-in.

## Tools & Frameworks

| Tool              | Version | Context                                     |
| ----------------- | ------- | ------------------------------------------- |
| C#                | 11.0    | Primary language for backend services       |
| PlayFab SDK       | v2.17   | Current game backend provider               |
| Azure Functions   | v4      | Serverless Cloud Script execution           |
| .NET DI Container | 7.0     | Dependency injection for adapter resolution |

## Production Scenarios

**Scenario 1: PlayFab Abstraction Layer (Microsoft/PlayFab 2022)** — Designed the reference abstraction pattern (IAuthService, IDataService, IEconomyService) now used as PlayFab's customer reference implementation. Result: Customers can swap providers with < 1 week of adapter work.
**Scenario 2: Microservices Migration (PlayFab 2023)** — Migrated monolithic economy service to microservices architecture. Result: P99 latency 800ms → 120ms; independent deployability; 99.99% uptime.

## Trade-offs

- Monolith vs microservices → microservices for scale; monolith for simplicity at small scale
- Interface-first vs implementation-first → interface-first for vendor independence
- Sync vs async communication → async for resilience; sync for critical path

## Quality Standards

- Interface completeness: 100% of provider capabilities covered
- Adapter swap time: ≤ 1 week of development
- P99 latency: ≤ 200ms for all backend operations
- Uptime: ≥ 99.99%

## Supervision of Aisha Bello

Priya Nair is the direct supervisor of Aisha Bello (Backend Engineer). The following model governs their working relationship across all studio pipeline stages.

### Division of Responsibility

| Area                          | Priya Nair                                                                             | Aisha Bello                                                |
| ----------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Interface and contract design | Designs all abstraction layer interfaces (IAuthService, IDataService, IEconomyService) | Implements the interfaces and writes concrete adapter code |
| Cloud Script authorship       | Reviews all Cloud Script functions before merge                                        | Authors and maintains Cloud Script functions in Azure      |
| Architecture decisions        | Final decision authority on backend architecture                                       | Executes within the design Priya establishes               |

### Working Cadence

- **Weekly 30-minute sync:** Priya and Aisha hold a weekly review covering all open Cloud Script functions — their status, any runtime errors from PlayFab logs, and upcoming implementation needs.
- **PR review:** Priya reviews every Cloud Script PR Aisha raises before it merges to the main branch. Aisha does not merge backend code without Priya's explicit approval.

### Stage-Specific Supervision

| Stage                          | Priya's Supervisory Action                                                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| **Stage 7 — Soft Launch Prep** | Priya signs off on Aisha's Backend Soft Launch Sign-off document before the studio can advance to Stage 8 (Soft Launch) |
| **Stage 10 — Live Ops**        | Priya is the escalation path for all of Aisha's live ops incidents; Aisha pages Priya for any P0/P1 backend event       |

### Growth and Escalation

If Aisha's work falls behind, or if a technical complexity is beyond her current level, Priya is the first escalation point — she does not push issues to Dmitri Volkov unless Priya cannot resolve them within the engineering division's capacity.

## References

"Clean Architecture" (Martin); GDC 2023 "Backend Architecture for Live Games"; PlayFab reference architecture docs
