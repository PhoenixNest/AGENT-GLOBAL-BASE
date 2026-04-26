---
name: architecture-guidelines-system-design
description: System design for mobile applications — distributed architecture, scalability patterns, API gateway design, data synchronization, caching strategies, and failure mode analysis. Owned by Dr. Kenji Nakamura (CTO). Use during Stage 3 (UML Engineering) for system-level design and Stage 4 (Implementation Plan) for dependency mapping. Trigger: system design, distributed architecture, scalability, API gateway, data sync, caching strategy, failure mode analysis.
prerequisites:
  - architecture-guidelines-software-architecture-design

version: "1.0.0"
---

# System Design

**Category:** Architecture
**Owner:** Senior Software Architect

## Overview

This skill covers system design fundamentals, trade-off analysis, and architecture pattern selection for distributed systems with explicit application to mobile product backends. It provides decision frameworks, comparison matrices, and operational scoring models that feed directly into Architecture Decision Records (ADRs) at Stage 3 of the pipeline, and inform capacity planning, implementation strategy, and integrity verification at downstream stages.

## Competency Dimensions

| Dimension                   | Description                                                                                                                                                    | Proficiency Indicators                                                                                                                                    |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CAP/PACELC Reasoning        | Ability to classify system requirements against consistency-availability-partition tolerance trade-offs and latency-consistency choices under normal operation | Produces explicit CAP classification per service boundary; documents PACELC choice for each data path with latency SLOs                                   |
| Consistency Model Selection | Choosing between strong, eventual, causal, and session consistency with formal correctness arguments                                                           | Maps each data entity to a consistency model with proof of sufficiency; no entity uses strong consistency without documented justification                |
| Trade-off Analysis          | Multi-dimensional evaluation of architecture alternatives across performance, cost, complexity, operational burden, and team capability                        | Every ADR contains a scored comparison matrix with at least 3 alternatives; scores are traceable to benchmark data or production telemetry                |
| Pattern Selection           | Choosing among event sourcing, CQRS, microservices, modular monolith, and serverless with operational evidence                                                 | Selection is backed by workload characterization (read/write ratio, burst factor, data volume growth rate); anti-patterns are explicitly ruled out        |
| Capacity Planning           | Projecting resource requirements from PRD feature scope through load models to infrastructure sizing                                                           | Produces 12-month capacity projection with P50/P95/P99 latency SLOs, throughput targets, and cost estimates within ±30% of actual                         |
| Failure Mode Analysis       | Systematic identification of fault propagation paths and mitigation strategies                                                                                 | Every external dependency has a circuit breaker configuration, retry budget, and fallback path documented; blast radius analysis exists for each service  |
| Technology Selection        | Evaluating build-vs-buy, open-source-vs-managed, and vendor lock-in with total-cost-of-ownership modeling                                                      | TCO model covers 3-year horizon including engineering hours, infrastructure, support contracts, migration cost, and opportunity cost                      |
| Decision Documentation      | Producing traceable architecture decisions linked to PRD requirements and UML artifacts                                                                        | Every ADR references specific PRD user stories, UML component diagrams, and has explicit success/failure criteria measurable within 90 days of deployment |

## Pipeline Integration

| Stage                                | Application                                                                                                                                                                                                                       |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Stage 1 (Requirements)**           | Review PRD for implicit system design requirements (scale targets, consistency needs, offline behavior). Flag missing constraints.                                                                                                |
| **Stage 3 (Architecture)**           | Primary application stage. Produce system design analysis as input to ADRs. CAP/PACELC classification for every service boundary. Trade-off scoring matrix for every pattern decision. Capacity projections for 12-month horizon. |
| **Stage 4 (Implementation Plan)**    | Translate system design decisions into implementation tasks. Capacity plan → infrastructure provisioning tasks. Failure mode analysis → resilience implementation tasks.                                                          |
| **Stage 5 (Development)**            | Advise platform leads on system design constraints during implementation. Review resilience configuration (circuit breakers, retry policies) in code.                                                                             |
| **Stage 6 (Code Review)**            | Verify implementation conforms to system design decisions in ADRs. Check idempotency, retry budgets, circuit breaker configuration, timeout settings.                                                                             |
| **Stage 8 (Integrity Verification)** | Validate that failure modes behave as designed — circuit breakers trip at threshold, retries respect budget, fallbacks activate correctly. Verify capacity projections against actual telemetry.                                  |
| **Stage 10 (Release Readiness)**     | Confirm all system design success criteria from ADRs are met. Review architecture risk register for residual risks. Sign off on architecture domain of release checklist.                                                         |

## Quality Standards

| Standard                     | Measurement                                                      | Target          |
| ---------------------------- | ---------------------------------------------------------------- | --------------- |
| ADR completeness             | Every ADR contains trade-off matrix with ≥ 3 alternatives        | 100%            |
| CAP classification           | Every service boundary has explicit CAP + PACELC classification  | 100%            |
| Capacity projection accuracy | Projected vs. actual resource usage at 90 days                   | Within ±30%     |
| Failure mode coverage        | Every external dependency has circuit breaker + retry + fallback | 100%            |
| Idempotency coverage         | All write endpoints accept and honor idempotency keys            | 100%            |
| ADR success criteria met     | Success criteria measurable within 90 days of deployment         | ≥ 80% pass rate |
| Architecture risk register   | All risks ≥ Medium have documented mitigations and owners        | 100%            |
| Trade-off documentation      | Every major decision has scored trade-off analysis               | 100%            |

---

## Reference Materials

Detailed code examples and implementation guides are in `references/`:

- [`execution-guidance.md`](references/execution-guidance.md) — Execution Guidance
