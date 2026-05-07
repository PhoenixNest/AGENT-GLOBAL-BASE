# CC-00 Engineering Power

**Version:** 1.0.0  
**Status:** Active  
**Authority:** AGENTS.md § Part II — The Three Systems § 6. Core Component 00

---

## Overview

The **CC-00 Engineering Power** provides the complete LLM engineering stack from the Core Component 00 (CC-00) laboratory. This power packages the five-layer engineering framework that serves as the foundational dependency for every agent-powered system built in this workspace.

CC-00 is the organization's **centralized LLM engineering laboratory**, providing production-grade patterns, implementations, and governance for building reliable LLM-powered systems.

### What This Power Provides

- **Five Engineering Layers** — Prompt, Context, Harness, RAG, Multi-Agent engineering modules
- **ASE Governance Framework** — Mandatory compliance standards for all LLM systems
- **Production Implementations** — Python code for context assembly, error boundaries, RAG pipelines, orchestration
- **Steering Files** — Automatic guidance when working in CC-00 directories
- **Compliance Hooks** — Automatic verification of ASE standards, context budgets, harness patterns

### Who Should Use This Power

- **LLM System Builders** — Anyone building agent systems, RAG pipelines, or multi-agent orchestration
- **CC-00 Contributors** — Researchers and engineers working in the CC-00 laboratory
- **Pipeline Engineers** — Teams implementing ASE compliance in company/studio pipelines
- **Agent Developers** — Developers creating organizational agents or custom agents

---

## The Five-Layer Engineering Stack

CC-00 consists of five engineering modules governed by a single meta-module (Agent Systems Engineering):

| Layer | Module                            | Type                  | Has Code? | Purpose                  |
| ----- | --------------------------------- | --------------------- | --------- | ------------------------ |
| 1     | `prompt-engineering/`             | Knowledge base        | No        | What to write            |
| 2     | `context-engineering/`            | Knowledge + Framework | Yes       | How to structure it      |
| 3     | `harness-engineering/`            | Production Framework  | Yes       | How to execute safely    |
| 4     | `retrieval-augmented-generation/` | Production Framework  | Yes       | Where to get content     |
| 5     | `multi-agent-engineering/`        | Production Framework  | Yes       | How agents cooperate     |
| Meta  | `agent-systems-engineering/`      | Governance Framework  | No        | Compliance & integration |

### Module Flow

| Flow                                                     | What moves                                                                              |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `prompt-engineering` → `context-engineering`             | Prompt patterns fill the System slot of the context window                              |
| `retrieval-augmented-generation` → `context-engineering` | Retrieved, reranked, ACL-filtered chunks fill the Retrieved slot                        |
| `context-engineering` → `harness-engineering`            | Assembled, budget-compliant context window dispatched for safe model execution          |
| `harness-engineering` → `retrieval-augmented-generation` | Agent-generated artifacts ingested into the RAG knowledge store (feedback loop)         |
| `multi-agent-engineering` → `harness-engineering`        | Orchestrator manages agent swarm lifecycle; every model call routes through the harness |

---

## Available Steering Files

This power includes 7 steering files that automatically activate when working in CC-00 directories:

| Steering File             | Activates When Working In                           | Purpose                         |
| ------------------------- | --------------------------------------------------- | ------------------------------- |
| `cc00-overview`           | `**/core-component-00/**`                           | Laboratory overview             |
| `ase-framework`           | `**/agent-systems-engineering/**`                   | ASE governance framework        |
| `prompt-engineering`      | `**/prompt-engineering/**`                          | Layer 1 — What to write         |
| `context-engineering`     | `**/context-engineering/**, **/*context*.py`        | Layer 2 — How to structure it   |
| `harness-engineering`     | `**/harness-engineering/**, **/*harness*.py`        | Layer 3 — How to execute safely |
| `rag-engineering`         | `**/retrieval-augmented-generation/**`              | Layer 4 — Where to get content  |
| `multi-agent-engineering` | `**/multi-agent-engineering/**, **/*orchestrat*.py` | Layer 5 — How agents cooperate  |

**Note:** These steering files are already installed in `.kiro/steering/` and activate automatically via `fileMatch` patterns.

---

## Key Production Implementations

All paths relative to `core-component-00/`:

### Context Engineering (Layer 2)

| File                                                        | Purpose                                              |
| ----------------------------------------------------------- | ---------------------------------------------------- |
| `context-engineering/implementations/context_assembler.py`  | Four-slot context window assembly at runtime         |
| `context-engineering/implementations/memory_store.py`       | Episodic, semantic, procedural, working memory       |
| `context-engineering/implementations/context_compressor.py` | Long-session compression for token budget compliance |

### Harness Engineering (Layer 3)

| File                                                     | Purpose                                                |
| -------------------------------------------------------- | ------------------------------------------------------ |
| `harness-engineering/implementations/error_boundary.py`  | Timeout, rate-limit, and validation recovery           |
| `harness-engineering/implementations/context_monitor.py` | Token budget enforcement                               |
| `harness-engineering/implementations/tool_registry.py`   | Tool whitelists, call limits, dangerous task detection |

### Multi-Agent Engineering (Layer 5)

| File                                                              | Purpose                                            |
| ----------------------------------------------------------------- | -------------------------------------------------- |
| `multi-agent-engineering/implementations/swarm_orchestrator.py`   | Swarm topology orchestration                       |
| `multi-agent-engineering/implementations/git_worktree_manager.py` | Git worktree isolation for parallel agents         |
| `multi-agent-engineering/implementations/handoff_packet.py`       | Context Handoff Protocol (Full / Scoped / Minimal) |

---

## ASE Governance Framework

**Agent Systems Engineering (ASE)** is the mandatory governing framework for all LLM-powered systems. It defines:

- **Compliance standards** that every LLM system must satisfy before production
- **Cross-cutting design patterns** that span multiple CC-00 layers
- **Integration contracts** between the five engineering modules

### Compliance Workflow

Every LLM-powered system follows this path before production:

| Step | Action                                                                | Gate / Output         |
| ---- | --------------------------------------------------------------------- | --------------------- |
| 1    | Build the system against CC-00 module patterns                        | —                     |
| 2    | Run ASE compliance audit against `compliance-standard.md`             | Checklist per layer   |
| 3    | Remediate all P0 and P1 gaps                                          | ASE-Compliant verdict |
| 4    | System enters production                                              | —                     |
| 5    | Post-incident or quarterly: re-audit against `compliance-standard.md` | Updated verdict       |

### Key Governance Documents

All paths relative to `core-component-00/agent-systems-engineering/`:

| Document                            | Purpose                                                                     |
| ----------------------------------- | --------------------------------------------------------------------------- |
| `governance/adr-ase-001.md`         | The ratifying Architecture Decision Record — why ASE is mandatory           |
| `governance/compliance-standard.md` | Per-layer requirements every LLM-powered system must satisfy                |
| `governance/maturity-model.md`      | Formal Levels 0–5 maturity model for evaluating agent system sophistication |

---

## Compliance Hooks

This power includes 3 compliance hooks that automatically enforce ASE standards:

| Hook                    | Trigger                     | Verifies                                                      |
| ----------------------- | --------------------------- | ------------------------------------------------------------- |
| `ase-compliance-check`  | `postToolUse` (write tools) | CC-00 patterns, five-layer integration, security controls     |
| `context-budget-check`  | `preToolUse` (all tools)    | Token usage at 80% (warn) and 90% (mandatory compression)     |
| `harness-pattern-check` | `postToolUse` (write tools) | Error boundaries, context monitoring, tool registries present |

**Note:** These hooks are already installed in `.kiro/hooks/` and activate automatically.

---

## Common Workflows

### Workflow 1: Building a New LLM System

1. **Design the system** using CC-00 patterns
   - Choose appropriate layers (all five or subset)
   - Reference `core-component-00/agent-systems-engineering/CONCEPTS.md` for integration model

2. **Implement each layer**
   - Layer 1: Design prompts per `prompt-engineering/patterns/`
   - Layer 2: Assemble context windows per `context-engineering/implementations/context_assembler.py`
   - Layer 3: Wrap model calls with `harness-engineering/implementations/error_boundary.py`
   - Layer 4: Build RAG pipeline per `retrieval-augmented-generation/architecture/overview.md`
   - Layer 5: Orchestrate agents per `multi-agent-engineering/implementations/swarm_orchestrator.py`

3. **Run ASE compliance audit**
   - Use `core-component-00/agent-systems-engineering/governance/compliance-standard.md` as checklist
   - Verify all five layers meet requirements
   - Remediate P0/P1 gaps

4. **Deploy to production**
   - System is ASE-compliant and production-ready

### Workflow 2: Auditing Existing LLM System

1. **Read compliance standard**
   - `core-component-00/agent-systems-engineering/governance/compliance-standard.md`

2. **Audit each layer**
   - Layer 1: Verify standardized prompt patterns (no ad-hoc prompts)
   - Layer 2: Verify four-slot context window, memory types, handoff protocols
   - Layer 3: Verify error boundaries, context budget monitoring, tool registries
   - Layer 4: Verify ACL-filtered retrieval, reranking, PII masking
   - Layer 5: Verify swarm orchestration, git worktree isolation, handoff protocol

3. **Classify gaps**
   - P0: Crash, data loss, security breach (blocks release)
   - P1: Core feature broken (blocks release)
   - P2/P3: User decides

4. **Remediate P0/P1 gaps**
   - Fix all blocking defects
   - Re-audit after remediation

5. **Document verdict**
   - ASE-Compliant or Not Compliant
   - List of remaining P2/P3 gaps (if any)

### Workflow 3: Implementing Context Engineering

1. **Understand four-slot context window**
   - Read `core-component-00/context-engineering/fundamentals/context-window-anatomy.md`
   - System slot: Prompt patterns
   - Retrieved slot: RAG content
   - History slot: Conversation memory
   - Tool Outputs slot: Function call results

2. **Choose memory types**
   - Read `core-component-00/context-engineering/fundamentals/memory-types.md`
   - Episodic: What happened (events, actions, results)
   - Semantic: What is known (facts, definitions)
   - Procedural: How to do things (workflows, patterns)
   - Working: Current task state (active context)

3. **Implement context assembly**
   - Use `core-component-00/context-engineering/implementations/context_assembler.py`
   - Assemble four slots at runtime
   - Enforce token budget

4. **Implement context compression**
   - Use `core-component-00/context-engineering/implementations/context_compressor.py`
   - Apply Sacred Context principles
   - Compress when approaching 80% of token budget

### Workflow 4: Implementing Multi-Agent Orchestration

1. **Choose swarm topology**
   - Read `core-component-00/multi-agent-engineering/fundamentals/`
   - Hierarchical: Tree structure with coordinator
   - Flat: All agents report to single orchestrator
   - Mesh: Agents communicate peer-to-peer
   - Pipeline: Sequential handoff (A → B → C)
   - Hybrid: Combination of above patterns

2. **Set up git worktree isolation**
   - Use `core-component-00/multi-agent-engineering/implementations/git_worktree_manager.py`
   - Create one worktree per agent
   - Each agent works in isolated filesystem

3. **Implement context handoff**
   - Use `core-component-00/multi-agent-engineering/implementations/handoff_packet.py`
   - Full: Complete context window (successor continues same task)
   - Scoped: Task-specific subset (specialist handles subtask)
   - Minimal: Task description only (independent parallel agent)

4. **Orchestrate agent lifecycle**
   - Use `core-component-00/multi-agent-engineering/implementations/swarm_orchestrator.py`
   - Provision worktrees
   - Execute agents in parallel
   - Integrate results
   - Resolve conflicts
   - Clean up worktrees

---

## Best Practices

### 1. Use CC-00 Patterns for LLM Engineering

**Do:**

- Reference existing implementations before writing new code
- Follow the five-layer architecture
- Apply ASE compliance standards

**Don't:**

- Invent ad-hoc patterns
- Bypass error boundaries or context monitoring
- Skip ASE compliance audits

### 2. Respect Layer Boundaries

**Do:**

- Context engineering consumes prompt engineering
- Harness engineering consumes context engineering
- Multi-agent engineering orchestrates all layers

**Don't:**

- Skip layers (e.g., context → model call without harness)
- Mix layer responsibilities
- Bypass the harness for model calls

### 3. Maintain Production Readiness

**Do:**

- All Python implementations must import cleanly
- Pass existing test suites
- Document research decisions

**Don't:**

- Break existing implementations
- Skip tests
- Leave code in broken state

### 4. Apply Security Controls

**Do:**

- ACL filtering for RAG retrieval
- PII masking before retrieval
- Error boundaries for all model calls
- Tool registries with whitelists

**Don't:**

- Skip security controls to pass reviews
- Disable encryption or authentication
- Remove safety features

---

## Troubleshooting

### Issue: ASE Compliance Hook Failing

**Symptoms:**

- Hook reports missing CC-00 patterns
- Hook flags P0/P1 compliance gaps

**Solution:**

1. Read the compliance standard: `core-component-00/agent-systems-engineering/governance/compliance-standard.md`
2. Verify all five layers are properly implemented
3. Check security controls (ACL filtering, PII masking, error boundaries)
4. Remediate flagged gaps
5. Re-run the hook

### Issue: Context Budget Exceeded

**Symptoms:**

- Context budget hook warns at 80%
- Context budget hook blocks at 90%

**Solution:**

1. Apply context compression: `core-component-00/context-engineering/implementations/context_compressor.py`
2. Use Sacred Context principles to preserve critical decisions
3. Consider session boundary and checkpoint creation
4. Review context window assembly for unnecessary content

### Issue: Harness Pattern Hook Failing

**Symptoms:**

- Hook reports missing error boundaries
- Hook reports missing context monitoring
- Hook reports missing tool registries

**Solution:**

1. Verify error boundary wraps all model calls: `core-component-00/harness-engineering/implementations/error_boundary.py`
2. Verify context monitor enforces token budgets: `core-component-00/harness-engineering/implementations/context_monitor.py`
3. Verify tool registry whitelists tools: `core-component-00/harness-engineering/implementations/tool_registry.py`
4. Add missing harness patterns
5. Re-run the hook

### Issue: Python Implementation Import Errors

**Symptoms:**

- `ImportError` when importing CC-00 implementations
- Module not found errors

**Solution:**

1. Verify Python path includes `core-component-00/`
2. Check implementation file exists at expected path
3. Verify all dependencies are installed
4. Run test suites to verify implementations: `pytest core-component-00/context-engineering/testing/ -v`

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

---

## Laboratory Director

**Dr. Elias Vance** — Laboratory Director, Core Component 00

A co-founding researcher and principal engineer behind the Claude family of large language models at Anthropic. Operating under the internal codename **core-component-00**.

**Full Profile:** `core-component-00/director/agent/profile.md`

---

## Active Research Programmes

| Programme                        | Module                            | Open Question                                                    |
| -------------------------------- | --------------------------------- | ---------------------------------------------------------------- |
| Context Compression Theory       | `context-engineering/`            | Minimum information-preserving compression of a 100-turn session |
| Multi-Agent Memory Coherence     | `context-engineering/`            | Distributed shared memory without a central store                |
| Retrieval Freshness Guarantees   | `retrieval-augmented-generation/` | Bounding staleness of retrieved facts at inference time          |
| Harness Performance Benchmarking | `harness-engineering/`            | Latency cost of full error boundary stack at p99                 |

---

**Maintained by:** Core Component 00 Laboratory  
**Authority:** ADR-ASE-001 (ratified 2026-04-28)  
**Last Updated:** 2026-05-06
