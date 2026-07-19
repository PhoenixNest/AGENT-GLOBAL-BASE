# Core Component 00 — LLM Engineering Laboratory

> _Approved for formal laboratory conversion — 2026-04-28_
>
> The canonical knowledge base and production framework for building reliable, production-grade LLM-powered systems. Every team building with large language models in this organisation starts here.

---

## Laboratory Profile

| Field              | Detail                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------ |
| **Designation**    | Core Component 00 (CC-00)                                                                                    |
| **Classification** | Applied LLM Research Laboratory                                                                              |
| **Status**         | CEO-approved · Formally chartered · Active                                                                   |
| **Founded**        | 2026-04-28                                                                                                   |
| **Director**       | Dr. Elias Vance — _see [Agent Profile](./crew/director/elias-vance/agent/profile.md)_                        |
| **Crew**           | 11 crew FTEs across 3 phases (FY2026 Q3) — _see [Roster](./crew/README.md)_                                  |
| **Research Scope** | Prompt Engineering · Context Engineering · Harness Engineering · Retrieval Systems · Multi-Agent Engineering |
| **Output Format**  | Production frameworks · Executable implementations · Peer-reviewed documentation                             |

---

## Organizational Chart

Personnel structure as of FY2026 Q3 — Dr. Vance plus 11 crew hired across three phases (4
module-owning Research Engineers, then a Research Scientist, Safety & Evaluation Engineer,
Infrastructure Engineer, and 4 paired Research Engineer IIs). Total headcount 12. Full profiles:
[`crew/README.md`](./crew/README.md).

```
User (CEO)
 │
 └── Dr. Elias Vance — Laboratory Director (L5)
      │    owns: ASE governance · cross-module architecture · engineering/prompt-engineering/ (direct)
      │
      ├── Dr. Idris Farouk — Staff Research Engineer, MAE Lead (L4)
      │    owns: engineering/multi-agent-engineering/ (lead) · ASE audit execution
      │    │
      │    └── Amina Yusuf — Senior Research Engineer II (L3)
      │         owns: engineering/multi-agent-engineering/ (fleet resilience, isolation)
      │
      ├── Mei-Ling Zhao — Senior Research Engineer (L3)
      │    owns: engineering/context-engineering/ (lead)
      │    │
      │    └── Hana Kobayashi — Senior Research Engineer II (L3)
      │         owns: engineering/context-engineering/ (memory scaling, concurrent-access safety)
      │
      ├── Kwame Asante — Senior Research Engineer (L3)
      │    owns: engineering/harness-engineering/ (lead)
      │    │
      │    └── Connor O'Malley — Senior Research Engineer II (L3)
      │         owns: engineering/harness-engineering/ (fault injection, recovery validation)
      │
      ├── Sofia Almeida — Senior Research Engineer (L3)
      │    owns: retrieval-augmented-generation/ (lead)
      │    │
      │    └── Diego Fontán — Senior Research Engineer II (L3)
      │         owns: retrieval-augmented-generation/ (index scaling, re-embedding ops)
      │
      ├── Dr. Amara Nwosu-Chen — Staff Research Scientist (L4)
      │    owns: cross-cutting — independent research origination
      │
      ├── Dr. Tomasz Wieczorek — Staff Safety & Evaluation Engineer (L4)
      │    owns: cross-cutting — independent adversarial evaluation & audit verification
      │
      └── Ravi Deshmukh — Infrastructure Engineer (L3)
           owns: cross-cutting — dev environment, dependency management, CI-for-research
```

| Level | Headcount | Role(s)                                                                                                 |
| ----- | --------- | ------------------------------------------------------------------------------------------------------- |
| L5    | 1         | Laboratory Director                                                                                     |
| L4    | 3         | Staff Research Engineer (MAE Lead) · Staff Research Scientist · Staff Safety & Evaluation Engineer      |
| L3    | 8         | Senior Research Engineer (×3 module leads) · Senior Research Engineer II (×4) · Infrastructure Engineer |

Dr. Vance's direct-report span: 7 (down from a would-be 11 flat structure) — the four Research
Engineer IIs report to their paired module lead instead, per `recruitment-plan.md` v1.3.

---

## Module Hierarchy

`core-component-00` contains five engineering modules governed by a single meta-module. The diagram below shows the hierarchical relationships among all components:

```mermaid
graph TB
    CC00(["core-component-00<br/>— LLM Engineering Laboratory —"])
    DIR["crew/<br/>Dr. Vance + 11 crew"]
    ASE["agent-systems-engineering/<br/>«Governing Framework»"]
    ENG["engineering/<br/>Layers 1, 2, 3, 5"]
    PE["prompt-engineering/<br/>Layer 1 — What to write"]
    CE["context-engineering/<br/>Layer 2 — How to structure it"]
    HE["harness-engineering/<br/>Layer 3 — How to execute safely"]
    RAG["retrieval-augmented-generation/<br/>Layer 4 — Where to get content"]
    MAE["multi-agent-engineering/<br/>Layer 5 — How agents cooperate"]

    CC00 --- DIR
    CC00 --> ASE
    ASE --> ENG
    ASE --> RAG
    ENG --> PE
    ENG --> CE
    ENG --> HE
    ENG --> MAE

    classDef lab fill:#2C3E50,stroke:#1A252F,color:#fff,font-weight:bold
    classDef ase fill:#7B241C,stroke:#641E16,color:#fff,font-weight:bold
    classDef eng fill:#154360,stroke:#0E2F44,color:#fff,font-weight:bold
    classDef mod fill:#EBF5FB,stroke:#5D6D7E,color:#2C3E50
    classDef dir fill:#515A5A,stroke:#2C3E50,color:#fff

    class CC00 lab
    class ASE ase
    class ENG eng
    class PE,CE,HE,RAG,MAE mod
    class DIR dir
```

| Flow                                                                      | What moves                                                                              |
| ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `engineering/prompt-engineering` → `engineering/context-engineering`      | Prompt patterns fill the System slot of the context window                              |
| `retrieval-augmented-generation` → `engineering/context-engineering`      | Retrieved, reranked, ACL-filtered chunks fill the Retrieved slot                        |
| `engineering/context-engineering` → `engineering/harness-engineering`     | Assembled, budget-compliant context window dispatched for safe model execution          |
| `engineering/harness-engineering` → `retrieval-augmented-generation`      | Agent-generated artifacts ingested into the RAG knowledge store (feedback loop)         |
| `engineering/multi-agent-engineering` → `engineering/harness-engineering` | Orchestrator manages agent swarm lifecycle; every model call routes through the harness |

---

## Laboratory Director

### Dr. Elias Vance

A co-founding researcher and principal engineer behind the **Claude family of large language models** at Anthropic. Operating under the internal codename **core-component-00** — the designation assigned to the original LLM reliability research programme from which this laboratory is derived.

Full agent profile and skills: [`core-component-00/crew/director/elias-vance/agent/profile.md`](./crew/director/elias-vance/agent/profile.md). Full lab roster: [`core-component-00/crew/README.md`](./crew/README.md).

#### Academic and Research Background

| Area                               | Contribution                                                                                                                                                                      |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Constitutional AI (CAI)**        | Founding contributor to the alignment framework underpinning Claude. Defined the principle-based feedback loop that replaced RLHF with self-critique.                             |
| **Context Engineering**            | Coined the term and defined the Six Pillars. First to formalise context window management as an independent engineering discipline distinct from prompt engineering.              |
| **Harness Engineering**            | Principal architect of production-grade LLM execution patterns: Error Boundary, Context Budget Monitor, and Tool Registry — now the standard reliability layer for agent systems. |
| **Multi-Agent Orchestration**      | Designed the Context Handoff Protocol (Full / Scoped / Minimal tiers) governing how orchestrator agents forward state to subagents without over-sharing or under-sharing context. |
| **Retrieval-Augmented Generation** | Early contributor to enterprise RAG architecture: slot-priority assembly, ACL-filtered retrieval, and layered retrieval (semantic + keyword fusion).                              |

#### Key Research Positions

| Year      | Role                                           | Organisation           |
| --------- | ---------------------------------------------- | ---------------------- |
| 2021–2023 | Principal Research Scientist, Language Systems | Anthropic              |
| 2023–2024 | Founding Lead, LLM Reliability Engineering     | Anthropic / Claude Lab |
| 2024–2025 | Chief Architect, Multi-Agent Orchestration     | Claude Lab             |
| 2026–     | Laboratory Director, Core Component 00         | This Organisation      |

#### Selected Publications and Frameworks

| Title                                                                                                       | Type               | Year |
| ----------------------------------------------------------------------------------------------------------- | ------------------ | ---- |
| _Constitutional AI: Harmlessness from AI Feedback_                                                          | Co-authored paper  | 2022 |
| _The Six Pillars of Context Engineering_                                                                    | Internal framework | 2025 |
| _Harness Engineering: Production Patterns for Reliable LLM Execution_                                       | Framework spec     | 2025 |
| _Sacred Context: Preserving Decision Continuity Across Long Agent Sessions_                                 | Research note      | 2026 |
| _Multi-Agent Context Handoff Protocols_                                                                     | Architecture spec  | 2026 |
| [_Agent Systems Engineering: The Convergence of Four Disciplines_](./agent-systems-engineering/CONCEPTS.md) | Foundational paper | 2026 |

#### Research Philosophy

> "The reliability of an LLM system is not determined by the model — it is determined by the engineering discipline of the team that deploys it. A state-of-the-art model wrapped in poor context management, no error recovery, and ad-hoc retrieval will fail in production. A well-engineered harness around a smaller model will outperform it. This laboratory exists to define and distribute that engineering discipline."

---

## Laboratory Mission

CC-00 operates with a four-part mission:

**1. Formalise.** Define the engineering disciplines of LLM system construction with the same rigour applied to classical software engineering. Context engineering, harness engineering, and RAG architecture are not folk practices — they are formal disciplines with documented patterns, measurable outcomes, and testable implementations.

**2. Implement.** Ship production-grade reference implementations alongside documentation. Every pattern documented in this laboratory ships with working Python code and an executable test suite. Knowledge that cannot be instantiated is not engineering — it is speculation.

**3. Distribute.** Make these disciplines accessible to every team in this organisation. CC-00 is the central dependency: every LLM-powered system built here is built on top of it. The laboratory's output quality directly determines the ceiling for every downstream product.

**4. Archive.** Preserve research findings and investigation outcomes in a permanent, traceable record. Every requirement investigation, technology evaluation, and research programme produces documented findings archived in the Telescope Research Archive Hub. This ensures decision continuity, knowledge retention, and pattern recognition across the laboratory's lifecycle.

---

## Active Research Programmes

| Programme                              | Status                    | Lead Module                        | Key Open Question                                                                                                                             |
| -------------------------------------- | ------------------------- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Context Compression Theory**         | **Resolved** (2026-06-30) | `engineering/context-engineering/` | Compaction API (`compact_20260112`) is the canonical solution — 87–95% reduction; align `context_compressor.py`.                              |
| **Multi-Agent Memory Coherence**       | **Resolved** (2026-06-30) | `engineering/context-engineering/` | git-as-substrate with `current_tasks/` file locking is the canonical pattern; GSM scope enforcement gap is a P1 security item.                |
| **Retrieval Freshness Guarantees**     | **Resolved** (2026-06-26) | `retrieval-augmented-generation/`  | Staleness is a policy variable (debounce threshold of a post-write hook), not an architectural invariant. See `patterns/index-sync-hooks.md`. |
| **Prompt Stability Under Fine-Tuning** | **Resolved** (2026-06-30) | `engineering/prompt-engineering/`  | Fine-tuning is Haiku-via-Bedrock only; schema-constrained prompts are the most stable class; CoT degrades post-FT.                            |
| **Harness Performance Benchmarking**   | **Resolved** (2026-06-30) | `engineering/harness-engineering/` | SDK default is 10-min timeout (30 min worst-case); override per tier: Haiku 15s / Sonnet 30s / Opus 90s. P0 fix in `error_boundary.py`.       |

**Research Archive:** Completed investigations and research findings are permanently archived in this Laboratory's own [Telescope instance](./telescope/README.md) (engineering + LLM research); see the workspace-root [Telescope index](../telescope/README.md) for the other departments' archives.

---

## Module Overview

| Module                                                                                    | Layer                     | Type                             | Has Code |
| ----------------------------------------------------------------------------------------- | ------------------------- | -------------------------------- | -------- |
| [`agent-systems-engineering/`](./agent-systems-engineering/README.md)                     | Governing meta-layer      | Governance framework             | No       |
| [`engineering/prompt-engineering/`](./engineering/prompt-engineering/README.md)           | 1 — What to write         | Knowledge base                   | No       |
| [`engineering/context-engineering/`](./engineering/context-engineering/README.md)         | 2 — How to structure it   | Knowledge + Production framework | Yes      |
| [`engineering/harness-engineering/`](./engineering/harness-engineering/README.md)         | 3 — How to execute safely | Production framework             | Yes      |
| [`retrieval-augmented-generation/`](./retrieval-augmented-generation/README.md)           | 4 — Where to get content  | Production framework             | Yes      |
| [`engineering/multi-agent-engineering/`](./engineering/multi-agent-engineering/README.md) | 5 — How agents cooperate  | Production framework             | Yes      |

---

## The Governing Module

### `agent-systems-engineering/` — Governance & Integration

The meta-module that sits above the five engineering pillars. It does not implement a
single layer — it governs all five. It defines the compliance standard that every
LLM-powered system must satisfy, the cross-cutting design patterns that span layer
boundaries, and the runtime integration contracts between modules.

Ratifying authority: [ADR-ASE-001](./agent-systems-engineering/governance/adr-ase-001.md) · Full module: [`agent-systems-engineering/README.md`](./agent-systems-engineering/README.md)

---

## The Five Engineering Modules

### 1. `engineering/prompt-engineering/` — Knowledge Base

The discipline of designing effective LLM instructions. Covers foundational research, zero-shot to chain-of-thought prompting, advanced patterns (Socratic, Devil's Advocate, Schema-Constrained), and workspace-specific strategy for integrating prompt techniques into skills, hooks, and agent profiles.

---

### 2. `engineering/context-engineering/` — Knowledge Base + Production Code

The discipline of architecting the LLM's context window — deciding what information to include, how to structure it across four typed slots (system / retrieved / history / tool outputs), and how to maintain it across the full lifecycle of an agent session.

Includes the four memory types (episodic, semantic, procedural, working), dynamic assembly patterns, multi-agent context handoff protocols, and production implementations.

---

### 3. `engineering/harness-engineering/` — Production Framework

The discipline of safely executing LLM model calls at runtime. Covers error boundaries (timeout, rate-limit, validation recovery), context budget monitoring, and tool use boundaries (whitelists, call limits, dangerous task detection).

The harness is the last layer before the model call — it validates, monitors, and recovers.

---

### 4. `retrieval-augmented-generation/` — Production Framework

The discipline of combining LLMs with external knowledge bases. Covers embedding pipelines, vector database architecture, reranking, chunking strategies, evaluation frameworks, security controls (ACL filtering, PII masking), and deployment templates.

RAG provides the retrieved content that feeds into the context-engineering retrieved slot.

---

### 5. `engineering/multi-agent-engineering/` — Production Framework

The discipline of designing, orchestrating, and operating coordinated systems of specialist LLM-powered agents. Covers swarm topology selection (Hierarchical, Flat, Mesh, Pipeline, Hybrid), git worktree isolation for parallel agent development, the Context Handoff Protocol (Full / Scoped / Minimal tiers), orchestration patterns, anti-patterns, and the complete agent swarm lifecycle.

Multi-agent engineering is the orchestration layer that sits above context engineering and harness engineering — it consumes context assembly, delegates execution to the harness, and feeds knowledge back into RAG.

Foundational paper: [Agent Systems Engineering: The Convergence of Four Disciplines](./agent-systems-engineering/CONCEPTS.md)

---

## Quick Navigation

| I want to…                                    | Go to                                                                                                                                                |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Write a better system prompt                  | `[engineering/prompt-engineering/fundamentals/research.md](./engineering/prompt-engineering/fundamentals/research.md)`                               |
| Decide what goes in each context slot         | `[engineering/context-engineering/fundamentals/context-window-anatomy.md](./engineering/context-engineering/fundamentals/context-window-anatomy.md)` |
| Choose the right memory type                  | `[engineering/context-engineering/fundamentals/memory-types.md](./engineering/context-engineering/fundamentals/memory-types.md)`                     |
| Assemble a context window at runtime          | `[engineering/context-engineering/implementations/context_assembler.py](./engineering/context-engineering/implementations/context_assembler.py)`     |
| Handle errors and timeouts around model calls | `[engineering/harness-engineering/implementations/error_boundary.py](./engineering/harness-engineering/implementations/error_boundary.py)`           |
| Manage token budgets during long sessions     | `[engineering/harness-engineering/implementations/context_monitor.py](./engineering/harness-engineering/implementations/context_monitor.py)`         |
| Build a RAG retrieval pipeline                | `[retrieval-augmented-generation/architecture/overview.md](./retrieval-augmented-generation/architecture/overview.md)`                               |
| Pass context between agents                   | `[engineering/context-engineering/patterns/multi-agent-handoff.md](./engineering/context-engineering/patterns/multi-agent-handoff.md)`               |
| Understand RAG security controls              | `[retrieval-augmented-generation/security/guide.md](./retrieval-augmented-generation/security/guide.md)`                                             |
| Wire all four modules together                | `[engineering/context-engineering/workspace/integration-guide.md](./engineering/context-engineering/workspace/integration-guide.md)`                 |
| Document research findings                    | `[telescope/README.md](./telescope/README.md)`                                                                                                       |

---

## Production Readiness

Each module with production code ships with:

| Module                                 | Implementations | Executable Tests                | Edge Case Guide |
| -------------------------------------- | --------------- | ------------------------------- | --------------- |
| `engineering/context-engineering/`     | 3 Python files  | 2 pytest suites (60 test cases) | Yes             |
| `engineering/harness-engineering/`     | 3 Python files  | 2 pytest suites                 | Yes             |
| `retrieval-augmented-generation/`      | 4 Python files  | 3 pytest suites (61 test cases) | Yes             |
| `engineering/multi-agent-engineering/` | 3 Python files  | 3 pytest suites                 | Yes             |

All Python implementations have been smoke-tested and import cleanly. Run all tests from the module root with:

```bash
pytest engineering/context-engineering/testing/ -v
pytest engineering/harness-engineering/testing/ -v
pytest retrieval-augmented-generation/testing/ -v
pytest engineering/multi-agent-engineering/testing/ -v
```

---

## Document Index

| Module                                   | Files  | Last Updated |
| ---------------------------------------- | ------ | ------------ |
| `agent-systems-engineering/` (Governing) | 11     | 2026-04-30   |
| `engineering/prompt-engineering/`        | 6      | 2026-04-24   |
| `engineering/context-engineering/`       | 15     | 2026-04-28   |
| `engineering/harness-engineering/`       | 11     | 2026-04-28   |
| `retrieval-augmented-generation/`        | 25     | 2026-06-30   |
| `engineering/multi-agent-engineering/`   | 11     | 2026-04-29   |
| **Total**                                | **70** | —            |

---

**Maintained by:** Claude Lab Engineering Team
**Last Updated:** 2026-07-16
