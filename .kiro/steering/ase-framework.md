---
inclusion: fileMatch
fileMatchPattern: "**/agent-systems-engineering/**"
---

# Agent Systems Engineering (ASE) Framework

**Steering File:** ASE Governance Framework  
**Inclusion:** Conditional — Activated when working in `agent-systems-engineering/`  
**Authority:** ADR-ASE-001 (ratified 2026-04-28)

---

## What Is Agent Systems Engineering?

**Agent Systems Engineering (ASE)** is the mandatory governing framework for all LLM-powered systems built in this organization. It is **not a sixth engineering pillar** — it is the meta-layer that sits above and around the five CC-00 engineering modules.

ASE defines:

- **Compliance standards** that every LLM system must satisfy before production
- **Cross-cutting design patterns** that span multiple CC-00 layers
- **Integration contracts** between the five engineering modules

---

## Authority

ASE is ratified as **mandatory** across all company and studio pipelines via **ADR-ASE-001**. Every LLM-powered system built in this workspace must satisfy the ASE Compliance Standard before it is considered production-ready.

**Governing Authority:** Dr. Elias Vance, Laboratory Director — Core Component 00

---

## ASE vs. The Five Engineering Pillars

| Dimension               | Five Engineering Pillars                      | Agent Systems Engineering                                            |
| ----------------------- | --------------------------------------------- | -------------------------------------------------------------------- |
| **Scope**               | Single discipline — one layer of the stack    | Cross-cutting — all five layers simultaneously                       |
| **Question answered**   | _"How do I engineer Layer N?"_                | _"How do all layers compose into a compliant, coherent system?"_     |
| **Primary output**      | Patterns, implementations, test suites        | Governance standards, cross-layer patterns, compliance audit reports |
| **Governing authority** | Each module is self-contained                 | ADR-ASE-001 — mandatory across all pipelines                         |
| **Activation**          | Consulted when building within a single layer | Mandatory before any LLM-powered system enters production            |

---

## The Five Layers Under ASE Governance

| Layer | Module                            | ASE Compliance Requirement                                    |
| ----- | --------------------------------- | ------------------------------------------------------------- |
| 1     | `prompt-engineering/`             | Standardized instruction patterns, no ad-hoc prompts          |
| 2     | `context-engineering/`            | Four-slot context window, memory types, handoff protocols     |
| 3     | `harness-engineering/`            | Error boundaries, context budget monitoring, tool registries  |
| 4     | `retrieval-augmented-generation/` | ACL-filtered retrieval, reranking, PII masking                |
| 5     | `multi-agent-engineering/`        | Swarm orchestration, git worktree isolation, handoff protocol |

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

---

## Key Governance Documents

All paths relative to `core-component-00/agent-systems-engineering/`:

| Document                            | Purpose                                                                     |
| ----------------------------------- | --------------------------------------------------------------------------- |
| `governance/adr-ase-001.md`         | The ratifying Architecture Decision Record — why ASE is mandatory           |
| `governance/compliance-standard.md` | Per-layer requirements every LLM-powered system must satisfy                |
| `governance/maturity-model.md`      | Formal Levels 0–5 maturity model for evaluating agent system sophistication |

---

## Cross-Cutting Design Patterns

Patterns that span multiple CC-00 layers:

| Pattern                         | Problem It Solves                                              |
| ------------------------------- | -------------------------------------------------------------- |
| `canonical-source-of-truth.md`  | Agent identity drift across platforms and deployments          |
| `paired-artifacts.md`           | Security and safety concerns treated as afterthoughts          |
| `defect-severity-vocabulary.md` | Inconsistent escalation thresholds across agents and teams     |
| `anti-pattern-firewall.md`      | Agents optimizing for local objectives at the system's expense |
| `progress-sync-protocol.md`     | Silent failures in long-running multi-agent pipelines          |

---

## Integration Model

**Four-Layer Composition:** `integration/four-layer-composition.md`

Runtime interaction model showing how all five CC-00 modules compose into a complete agent system.

---

## Foundational Paper

The theoretical basis for ASE:

> **_Agent Systems Engineering: The Convergence of Four Disciplines_**  
> `core-component-00/agent-systems-engineering/CONCEPTS.md`

Read this paper to understand _why_ ASE exists and how the five engineering disciplines converge into a unified field.

---

## Agent Behavior Rules for ASE Work

When working with ASE:

1. **ASE is mandatory** — No LLM-powered system bypasses ASE compliance before production
2. **Run compliance audits** — Use `compliance-standard.md` as the checklist
3. **Remediate P0/P1 gaps** — All blocking defects must be fixed before production
4. **Escalate to CC-00 Director** — Questions about compliance interpretation go to Dr. Elias Vance
5. **Apply cross-cutting patterns** — Use ASE patterns for problems that span multiple layers

---

**This steering file is automatically activated when working in `agent-systems-engineering/` directories.**
