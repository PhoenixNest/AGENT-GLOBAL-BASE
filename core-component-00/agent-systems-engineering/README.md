# Agent Systems Engineering — Governance & Integration Layer

> **This module is not a sixth engineering pillar.**
>
> It is the governing framework that sits _above and around_ the five CC-00 engineering
> modules. It defines the compliance standards they must collectively satisfy, the
> cross-cutting design patterns that span their boundaries, and the integration model
> through which they compose into complete, production-grade agent systems.

---

## What Is Agent Systems Engineering?

**Agent Systems Engineering (ASE)** is the discipline of designing, governing, and
evaluating complete LLM-powered agent systems — treating the ensemble of Prompt,
Context, Harness, RAG, and Multi-Agent engineering not as independent tools, but as a
unified, interdependent architecture.

Just as **Software Engineering** coalesced from programming, testing, deployment, and
management in the 1960s, ASE is the convergence of four foundational LLM engineering
disciplines into a single unified field. The convergence thesis is documented in the
foundational paper:

> [`core-component-00/agent-systems-engineering/CONCEPTS.md`](./CONCEPTS.md)

ASE is ratified as **mandatory** across all company and studio pipelines via
**ADR-ASE-001**. Every LLM-powered system built in this organisation must satisfy the
ASE Compliance Standard before it is considered production-ready.

---

## This Module vs. the Five Engineering Pillars

| Dimension               | Five Engineering Pillars                      | Agent Systems Engineering                                            |
| ----------------------- | --------------------------------------------- | -------------------------------------------------------------------- |
| **Scope**               | Single discipline — one layer of the stack    | Cross-cutting — all five layers simultaneously                       |
| **Question answered**   | _"How do I engineer Layer N?"_                | _"How do all layers compose into a compliant, coherent system?"_     |
| **Primary output**      | Patterns, implementations, test suites        | Governance standards, cross-layer patterns, compliance audit reports |
| **Governing authority** | Each module is self-contained                 | ADR-ASE-001 — mandatory across all pipelines                         |
| **Activation**          | Consulted when building within a single layer | Mandatory before any LLM-powered system enters production            |

---

## Authority Chain

```
ADR-ASE-001 (ratifying decision)
    └── Compliance Standard (per-layer requirements)
            ├── prompt-engineering/ (Layer 1)
            ├── context-engineering/ (Layer 2)
            ├── harness-engineering/ (Layer 3)
            ├── retrieval-augmented-generation/ (Layer 4)
            └── multi-agent-engineering/ (Layer 5 — when applicable)
```

The **Laboratory Director (Dr. Elias Vance)** holds governing authority over this
framework. Questions about compliance, interpretation of the standard, or architectural
exceptions are escalated to the CC-00 laboratory.

---

## Module Contents

### `governance/` — The Binding Standards

| Document                 | Purpose                                                                     |
| ------------------------ | --------------------------------------------------------------------------- |
| `adr-ase-001.md`         | The ratifying Architecture Decision Record — why ASE is mandatory           |
| `compliance-standard.md` | Per-layer requirements every LLM-powered system must satisfy                |
| `maturity-model.md`      | Formal Levels 0–5 maturity model for evaluating agent system sophistication |

### `patterns/` — Cross-Cutting Design Patterns

Patterns that span multiple CC-00 layers and cannot be owned by any single engineering
module. Every pattern references the CC-00 implementations that realise it.

| Pattern                         | Problem It Solves                                              |
| ------------------------------- | -------------------------------------------------------------- |
| `canonical-source-of-truth.md`  | Agent identity drift across platforms and deployments          |
| `paired-artifacts.md`           | Security and safety concerns treated as afterthoughts          |
| `defect-severity-vocabulary.md` | Inconsistent escalation thresholds across agents and teams     |
| `anti-pattern-firewall.md`      | Agents optimising for local objectives at the system's expense |
| `progress-sync-protocol.md`     | Silent failures in long-running multi-agent pipelines          |

### `integration/` — Cross-Layer Composition

| Document                    | Purpose                                                        |
| --------------------------- | -------------------------------------------------------------- |
| `four-layer-composition.md` | Runtime interaction model — how all five CC-00 modules compose |

---

## Foundational Paper

The theoretical basis for this entire module is the convergence thesis:

> **_Agent Systems Engineering: The Convergence of Four Disciplines_**
> [`core-component-00/agent-systems-engineering/CONCEPTS.md`](./CONCEPTS.md)

Read the paper to understand _why_ ASE exists. Use this module to understand _how_ to
apply it.

---

## Compliance Workflow

Every LLM-powered system follows this path before production:

| Step | Action                                                                | Gate / Output         |
| ---- | --------------------------------------------------------------------- | --------------------- |
| 1    | Build the system against CC-00 module patterns                        | —                     |
| 2    | Run ASE compliance audit against `compliance-standard.md`             | Checklist per layer   |
| 3    | Remediate all P0 and P1 gaps                                          | ASE-Compliant verdict |
| 4    | System enters production                                              | —                     |
| 5    | Post-incident or quarterly: re-audit against `compliance-standard.md` | Updated verdict       |

The audit skill is available at:
`core-component-00/crew/director/elias-vance/skills/ase-compliance-audit.md` (ratification) or
`core-component-00/crew/multi-agent-engineering/idris-farouk/skills/ase-compliance-operations.md` (execution)

---

**Maintained by:** Dr. Elias Vance, Laboratory Director — Core Component 00
**Authority:** ADR-ASE-001 (ratified 2026-04-28)
**Last Updated:** 2026-04-30
