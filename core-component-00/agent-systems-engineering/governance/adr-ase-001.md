# ADR-ASE-001 — Ratify Agent Systems Engineering as the Mandatory Governing Framework

| Field              | Value                                              |
| ------------------ | -------------------------------------------------- |
| **ADR ID**         | ADR-ASE-001                                        |
| **Status**         | Ratified                                           |
| **Date**           | 2026-04-28                                         |
| **Governing Body** | Core Component 00 Laboratory                       |
| **Authority**      | Dr. Elias Vance, Laboratory Director               |
| **Applies To**     | All LLM-powered systems built in this organisation |
| **Supersedes**     | None (inaugural decision)                          |

---

## Context

This organisation builds LLM-powered systems across four company development pipelines
(Mobile, Web, Backend API, Full-Stack), a creative studio pipeline, and internal tooling.
As of April 2026, no unified engineering standard governs how these systems are designed
and evaluated.

In the absence of a governing standard, teams independently implement LLM integrations
with the following recurring failure modes observed across projects:

| Failure Mode                    | Root Cause                                           | Observed Consequence                                       |
| ------------------------------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| Silent context overflow         | No token budget monitoring (missing Harness Layer)   | Long sessions degrade without user-visible error           |
| Hallucination under load        | No retrieval pipeline (missing RAG Layer)            | Parametric knowledge exhausted; model fabricates facts     |
| Inconsistent agent behaviour    | No structured identity design (missing Prompt Layer) | Same agent produces different outputs for identical inputs |
| Cascading failure on tool error | No error boundary (missing Harness Layer)            | Tool timeout propagates as unhandled exception to user     |
| Agent context mismatch          | No handoff protocol (missing Context Layer)          | Subagents lack decisions made by orchestrators             |

These failures share a common cause: **each engineering concern (prompts, context,
execution, knowledge) is addressed in isolation without integration design**. A system
that passes functional testing can fail in production because the layers do not compose
correctly even if each layer is individually adequate.

The emerging field of Agent Systems Engineering (ASE) addresses this gap. ASE is the
convergence of four foundational engineering disciplines — Prompt, Context, Harness, and
RAG Engineering — into a unified architecture discipline that governs how they compose.

The theoretical basis is documented in:
[_Agent Systems Engineering: The Convergence of Four Disciplines_](../CONCEPTS.md)

---

## Decision

**Agent Systems Engineering is ratified as the mandatory governing framework for all
LLM-powered systems built in this organisation.**

| Clause                        | Mandate                                                                                                                                                                                                                                                                                              |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1 — Four-layer coverage**   | Every LLM-powered system must address Prompt Engineering (Layer 1), Context Engineering (Layer 2), Harness Engineering (Layer 3), and RAG / Memory (Layer 4) before it is considered production-ready. Layer 4 may be intentionally absent with documented rationale; Layers 1–3 are non-negotiable. |
| **2 — Multi-Agent (Layer 5)** | Additionally required when a system involves more than one coordinated LLM agent. Governs swarm topology, task decomposition, context handoff, and parallel execution safety.                                                                                                                        |
| **3 — Compliance Standard**   | `compliance-standard.md` defines per-layer requirements. Maintained by CC-00 and updated as requirements evolve.                                                                                                                                                                                     |
| **4 — Mandatory audit**       | ASE Compliance Audits are required before production deployment, conducted using `director/skills/ase-compliance-audit.md`. Systems with P0 or P1 gaps may not enter production.                                                                                                                     |
| **5 — Governing authority**   | The CC-00 laboratory (Director: Dr. Elias Vance) holds authority over interpretation of the standard, architectural exceptions, and evolution of compliance requirements.                                                                                                                            |

---

## Rationale

### Why mandate all four layers?

Each layer addresses a failure mode that cannot be detected by functional testing alone:

| Layer       | Why it cannot be skipped                                                                                                  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------- |
| 1 — Prompt  | Unstructured prompts produce consistent outputs in testing but degrade under input variation in production                |
| 2 — Context | Context issues manifest only across long sessions or multi-agent handoffs, not in unit tests                              |
| 3 — Harness | Timeout, rate-limit, and token overflow failures are infrastructure conditions absent in test environments                |
| 4 — RAG     | Knowledge staleness and hallucination cannot be detected until the domain knowledge required is not in parametric weights |

### Why is this a cross-organisational mandate rather than a team-level guideline?

Inconsistent implementation creates inter-team incompatibilities. When Team A builds a
context-engineered orchestrator that hands off to Team B's unengineered subagent, the
handoff fails at the boundary — not within either team's system individually. The
mandate creates a shared contract that makes inter-team integration safe.

### Why CC-00 as the governing authority?

CC-00 is the organisation's centralised LLM engineering laboratory. Its five modules
are the reference implementations that the compliance standard points to. Having the
same team own both the standard and the reference implementations ensures that the
standard is always achievable and that the implementations always satisfy the standard.

---

## Consequences

| Stakeholder               | Obligations                                                                                                                                                                                                                                                                                                                       |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **All development teams** | Design LLM integrations against the ASE Compliance Standard from the outset — not retrofitted after functional development. Pre-production ASE audits are a hard gate, not a recommendation. Build against CC-00 patterns; do not create parallel implementations of harness, context, or RAG functionality without CC-00 review. |
| **CC-00 laboratory**      | Keep the Compliance Standard current as engineering modules evolve. Maintain `ase-compliance-audit.md` as the primary audit instrument. Remain available to consult on architectural exceptions and edge cases.                                                                                                                   |
| **Company pipelines**     | ASE compliance is a mandatory input to Stage 3 (_Prototype → UML Engineering Package_) of all four development pipelines for any LLM-powered feature.                                                                                                                                                                             |
| **Studio pipelines**      | ASE compliance is required before Stage 5 (_Full Production_) of the Casual Games Studio pipeline for any agent-powered feature.                                                                                                                                                                                                  |

---

## Exceptions

Architectural exceptions to this decision (e.g., a system where Layer 3 — Harness — is
demonstrably unnecessary) must be:

1. Documented in writing with technical rationale.
2. Reviewed and approved by the CC-00 Laboratory Director.
3. Recorded as an addendum to this ADR.

No exception overrides the requirement to audit; the audit documents the intentional
absence.

---

## Amendments

| Date       | Change               | Authority              |
| ---------- | -------------------- | ---------------------- |
| 2026-04-28 | Initial ratification | Dr. Elias Vance, CC-00 |
