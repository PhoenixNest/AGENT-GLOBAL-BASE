---
paths:
  - "**/core-component-00/**"
description: CC-00 Laboratory overview and behavior rules — active when working in core-component-00/
---

# CC-00 Laboratory Overview

**Designation:** Core Component 00 (CC-00)
**Classification:** Applied LLM Research Laboratory
**Director:** Dr. Elias Vance
**Founded:** 2026-04-28

---

## The Five-Module Engineering Stack

| Layer | Module                            | Type                  | Purpose                  |
| ----- | --------------------------------- | --------------------- | ------------------------ |
| 1     | `prompt-engineering/`             | Knowledge base        | What to write            |
| 2     | `context-engineering/`            | Knowledge + Framework | How to structure it      |
| 3     | `harness-engineering/`            | Production Framework  | How to execute safely    |
| 4     | `retrieval-augmented-generation/` | Production Framework  | Where to get content     |
| 5     | `multi-agent-engineering/`        | Production Framework  | How agents cooperate     |
| Meta  | `agent-systems-engineering/`      | Governance            | Compliance & integration |

---

## Key Production Implementations

| File                                                              | Module | Purpose                                        |
| ----------------------------------------------------------------- | ------ | ---------------------------------------------- |
| `context-engineering/implementations/context_assembler.py`        | CE     | Four-slot context window assembly              |
| `context-engineering/implementations/memory_store.py`             | CE     | Episodic, semantic, procedural, working memory |
| `context-engineering/implementations/context_compressor.py`       | CE     | Long-session compression                       |
| `harness-engineering/implementations/error_boundary.py`           | HE     | Timeout, rate-limit, validation recovery       |
| `harness-engineering/implementations/context_monitor.py`          | HE     | Token budget enforcement                       |
| `harness-engineering/implementations/tool_registry.py`            | HE     | Tool whitelists, call limits                   |
| `multi-agent-engineering/implementations/swarm_orchestrator.py`   | MAE    | Swarm topology orchestration                   |
| `multi-agent-engineering/implementations/handoff_packet.py`       | MAE    | Context Handoff Protocol                       |

---

## Behavior Rules for CC-00 Work

1. **Use CC-00 patterns** — Do not invent ad-hoc LLM patterns; anchor to existing implementations
2. **Check implementations first** — Before writing new code, check if it exists in `implementations/`
3. **Follow module hierarchy** — Respect layer boundaries and integration contracts
4. **Maintain production readiness** — All Python must import cleanly and pass test suites
5. **Document research decisions** — Update research status and archive findings in `telescope/`

---

## Quick Navigation

| I want to…                      | Go to                                                            |
| ------------------------------- | ---------------------------------------------------------------- |
| Understand the full laboratory  | `core-component-00/README.md`                                    |
| Learn about ASE governance      | `core-component-00/agent-systems-engineering/README.md`          |
| Design context windows          | `core-component-00/context-engineering/fundamentals/`            |
| Implement error boundaries      | `core-component-00/harness-engineering/implementations/`         |
| Build RAG pipelines             | `core-component-00/retrieval-augmented-generation/architecture/` |
| Orchestrate multi-agent systems | `core-component-00/multi-agent-engineering/fundamentals/`        |
| Document research findings      | `telescope/README.md`                                            |
