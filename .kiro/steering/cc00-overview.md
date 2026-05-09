---
inclusion: fileMatch
fileMatchPattern: "**/core-component-00/**"
---

# CC-00 Laboratory Overview

**Steering File:** CC-00 Laboratory Overview  
**Inclusion:** Conditional — Activated when working in `core-component-00/`  
**Authority:** AGENTS.md § Part II — The Three Systems § 6. Core Component 00

---

## Laboratory Identity

**Core Component 00 (CC-00)** is the organization's **centralized LLM engineering laboratory** and the foundational dependency for every agent-powered system built in this workspace.

| Field              | Detail                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------ |
| **Designation**    | Core Component 00 (CC-00)                                                                                    |
| **Classification** | Applied LLM Research Laboratory                                                                              |
| **Status**         | CEO-approved · Formally chartered · Active                                                                   |
| **Founded**        | 2026-04-28                                                                                                   |
| **Director**       | Dr. Elias Vance (Anthropic Claude Lab → This Organisation)                                                   |
| **Research Scope** | Prompt Engineering · Context Engineering · Harness Engineering · Retrieval Systems · Multi-Agent Engineering |
| **Output Format**  | Production frameworks · Executable implementations · Peer-reviewed documentation                             |

---

## The Five-Module Engineering Stack

CC-00 consists of five engineering modules governed by a single meta-module (Agent Systems Engineering):

| Layer | Module                            | Type                  | Has Code? | Purpose                  |
| ----- | --------------------------------- | --------------------- | --------- | ------------------------ |
| 1     | `prompt-engineering/`             | Knowledge base        | No        | What to write            |
| 2     | `context-engineering/`            | Knowledge + Framework | Yes       | How to structure it      |
| 3     | `harness-engineering/`            | Production Framework  | Yes       | How to execute safely    |
| 4     | `retrieval-augmented-generation/` | Production Framework  | Yes       | Where to get content     |
| 5     | `multi-agent-engineering/`        | Production Framework  | Yes       | How agents cooperate     |
| Meta  | `agent-systems-engineering/`      | Governance Framework  | No        | Compliance & integration |

---

## Module Flow

| Flow                                                     | What moves                                                                              |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `prompt-engineering` → `context-engineering`             | Prompt patterns fill the System slot of the context window                              |
| `retrieval-augmented-generation` → `context-engineering` | Retrieved, reranked, ACL-filtered chunks fill the Retrieved slot                        |
| `context-engineering` → `harness-engineering`            | Assembled, budget-compliant context window dispatched for safe model execution          |
| `harness-engineering` → `retrieval-augmented-generation` | Agent-generated artifacts ingested into the RAG knowledge store (feedback loop)         |
| `multi-agent-engineering` → `harness-engineering`        | Orchestrator manages agent swarm lifecycle; every model call routes through the harness |

---

## Agent Behavior Rules for CC-00 Work

When working in `core-component-00/`:

1. **Use CC-00 patterns for LLM engineering** — New agent systems, RAG pipelines, harness implementations, and context solutions must be grounded in CC-00. Do not invent ad-hoc patterns.

2. **Reference existing implementations** — Before writing new code, check if a production implementation already exists in `implementations/` directories.

3. **Follow module hierarchy** — Respect the layer boundaries. Context engineering consumes prompt engineering. Harness engineering consumes context engineering. Multi-agent engineering orchestrates all layers.

4. **Maintain production readiness** — All Python implementations must import cleanly and pass existing test suites.

5. **Document research decisions** — Active research programmes have open questions. Document findings and update research status.

6. **Archive research investigations** — When conducting requirement investigations, technology evaluations, or research programme work, document findings in the Telescope Research Archive Hub (`telescope/`) following the standardized template. This ensures permanent traceability and knowledge retention.

---

## Key Production Implementations

All paths relative to `core-component-00/`:

| File                                                              | Module | Purpose                                                |
| ----------------------------------------------------------------- | ------ | ------------------------------------------------------ |
| `context-engineering/implementations/context_assembler.py`        | CE     | Four-slot context window assembly at runtime           |
| `context-engineering/implementations/memory_store.py`             | CE     | Episodic, semantic, procedural, working memory         |
| `context-engineering/implementations/context_compressor.py`       | CE     | Long-session compression for token budget compliance   |
| `harness-engineering/implementations/error_boundary.py`           | HE     | Timeout, rate-limit, and validation recovery           |
| `harness-engineering/implementations/context_monitor.py`          | HE     | Token budget enforcement                               |
| `harness-engineering/implementations/tool_registry.py`            | HE     | Tool whitelists, call limits, dangerous task detection |
| `multi-agent-engineering/implementations/swarm_orchestrator.py`   | MAE    | Swarm topology orchestration                           |
| `multi-agent-engineering/implementations/git_worktree_manager.py` | MAE    | Git worktree isolation for parallel agents             |
| `multi-agent-engineering/implementations/handoff_packet.py`       | MAE    | Context Handoff Protocol (Full / Scoped / Minimal)     |

---

## Active Research Programmes

| Programme                        | Module                            | Open Question                                                    |
| -------------------------------- | --------------------------------- | ---------------------------------------------------------------- |
| Context Compression Theory       | `context-engineering/`            | Minimum information-preserving compression of a 100-turn session |
| Multi-Agent Memory Coherence     | `context-engineering/`            | Distributed shared memory without a central store                |
| Retrieval Freshness Guarantees   | `retrieval-augmented-generation/` | Bounding staleness of retrieved facts at inference time          |
| Harness Performance Benchmarking | `harness-engineering/`            | Latency cost of full error boundary stack at p99                 |

---

## Quick Navigation

| I want to…                           | Go to                                                            |
| ------------------------------------ | ---------------------------------------------------------------- |
| Understand the full laboratory       | `core-component-00/README.md`                                    |
| Learn about ASE governance           | `core-component-00/agent-systems-engineering/README.md`          |
| Write better prompts                 | `core-component-00/prompt-engineering/fundamentals/research.md`  |
| Design context windows               | `core-component-00/context-engineering/fundamentals/`            |
| Implement error boundaries           | `core-component-00/harness-engineering/implementations/`         |
| Build RAG pipelines                  | `core-component-00/retrieval-augmented-generation/architecture/` |
| Orchestrate multi-agent systems      | `core-component-00/multi-agent-engineering/fundamentals/`        |
| Understand how all modules integrate | `core-component-00/agent-systems-engineering/CONCEPTS.md`        |
| Document research findings           | `telescope/README.md`                                            |

---

**This steering file is automatically activated when working in `core-component-00/` directories.**
