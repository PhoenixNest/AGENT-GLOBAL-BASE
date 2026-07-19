# Four-Layer Composition — Runtime Integration Model

> **Governing authority:** ADR-ASE-001 · Core Component 00 Laboratory
> **Version:** 1.0 · **Last Updated:** 2026-04-30

This document specifies the runtime interaction model for the five CC-00 engineering
modules — how they compose into a complete, production-grade agent system at execution
time. It defines the integration contracts between modules, the data flow through the
stack, and the failure modes that arise when integration is broken.

---

## The Five-Layer Stack

The five CC-00 modules form a layered dependency graph. **Each layer consumes the output
of the layers below it and produces output for the layers above it.**

```
┌─────────────────────────────────────────────────────────────────────┐
│              LAYER 5 — MULTI-AGENT ENGINEERING                       │
│         Orchestration · Swarm topology · Task decomposition          │
│         Context handoff · Fork-join · Git worktree isolation         │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ orchestrates
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│              LAYER 3 — HARNESS ENGINEERING                           │
│         Error boundary · Token budget monitor · Tool registry        │
│         Retry logic · PII scrubbing · Quality gates                  │
└──────┬────────────────────────────────────────────────┬─────────────┘
       │ assembles context via                          │ feeds new knowledge to
       ▼                                               ▼
┌──────────────────────────────┐   ┌─────────────────────────────────┐
│   LAYER 2 — CONTEXT          │   │   LAYER 4 — RAG / KNOWLEDGE      │
│   ENGINEERING                │◄──┤                                  │
│   Four-slot assembly         │   │   Retrieval pipeline             │
│   Memory management          │   │   Embedding · Reranking          │
│   Handoff protocol           │   │   ACL filtering                  │
└──────────────┬───────────────┘   └─────────────────────────────────┘
               │ dispatches to
               ▼
┌─────────────────────────────────────────────────────────────────────┐
│              LAYER 1 — PROMPT ENGINEERING                            │
│         Agent identity · Role definition · Output schema             │
│         Behavioural constraints · Escalation criteria                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Integration Contracts

An integration contract defines the **interface between two adjacent layers**: the
format of the output one layer produces and the format the next layer expects. When
these formats are mismatched, the system fails at the boundary — not within either
layer individually.

### Contract 1: RAG → Context Engineering

| Field                  | Specification                                                                                             |
| ---------------------- | --------------------------------------------------------------------------------------------------------- |
| **Producer**           | Layer 4 — RAG retrieval pipeline                                                                          |
| **Consumer**           | Layer 2 — Context assembler (`context_assembler.py`)                                                      |
| **Output format**      | List of ranked document chunks with metadata: `{chunk_id, content, score, source, timestamp, acl_labels}` |
| **Slot assignment**    | Retrieved chunks are placed in the **Retrieved slot** of the context window                               |
| **Token budget**       | RAG output must respect the token allocation defined for the Retrieved slot                               |
| **Freshness contract** | Stale chunks (age > domain freshness bound) are marked with a staleness flag                              |
| **ACL contract**       | Only chunks passing ACL filter for the current agent are included                                         |

**Failure mode:** RAG returns raw text without metadata → context assembler cannot
perform slot priority ordering or staleness detection → context degrades silently.

**Reference:** `core-component-00/retrieval-augmented-generation/architecture/overview.md`

---

### Contract 2: Context Engineering → Harness Engineering

| Field              | Specification                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| **Producer**       | Layer 2 — Context assembler                                                                      |
| **Consumer**       | Layer 3 — Harness (`error_boundary.py`, `context_monitor.py`)                                    |
| **Output format**  | Assembled message list: `[{role: "system", content: ...}, {role: "user", content: ...}, ...]`    |
| **Token contract** | Total token count of assembled context must be within the budget enforced by the harness monitor |
| **Slot metadata**  | Each slot's token count is passed alongside the assembled context for monitoring                 |
| **Sacred context** | Sacred context elements are flagged — the harness must not truncate them                         |

**Failure mode:** Context assembler returns a context window that exceeds the harness
monitor's token limit → harness truncates blindly, potentially removing sacred context
→ agent loses critical decision continuity.

**Reference:** `core-component-00/engineering/context-engineering/implementations/context_assembler.py`

---

### Contract 3: Prompt Engineering → Context Engineering

| Field               | Specification                                                                                                    |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **Producer**        | Layer 1 — Agent identity prompt (system prompt)                                                                  |
| **Consumer**        | Layer 2 — Context assembler (System slot)                                                                        |
| **Output format**   | Structured markdown with defined sections: Role, Constraints, Output Format, Escalation Criteria                 |
| **Slot placement**  | Agent identity occupies the System slot — highest priority, never compressed                                     |
| **Size contract**   | System slot has a defined token allocation. Prompts exceeding this allocation must be refactored, not truncated. |
| **Schema contract** | Output format specifications in the prompt must match the schemas downstream consumers expect                    |

**Failure mode:** Agent identity prompt is unstructured free text → context assembler
cannot separate identity from instructions → token budget management is imprecise →
instructions leak into wrong context slots.

**Reference:** `core-component-00/engineering/prompt-engineering/patterns/advanced-patterns.md`

---

### Contract 4: Harness → RAG (Feedback Loop)

| Field              | Specification                                                                                       |
| ------------------ | --------------------------------------------------------------------------------------------------- |
| **Producer**       | Layer 3 — Harness (post-execution)                                                                  |
| **Consumer**       | Layer 4 — RAG knowledge store (ingestion pipeline)                                                  |
| **Output format**  | Agent execution artifact: `{artifact_type, content, agent_id, task_id, timestamp, quality_verdict}` |
| **Ingestion gate** | Only artifacts with quality verdict `pass` or `conditional` are ingested                            |
| **Metadata**       | Artifact must carry agent attribution, task ID, and pipeline stage for retrieval filtering          |

**Failure mode:** Agent-generated artifacts are not fed back to RAG → knowledge base
becomes stale → future retrieval returns outdated information → agents hallucinate
decisions already made by previous pipeline stages.

**Reference:** `core-component-00/retrieval-augmented-generation/architecture/overview.md`

---

### Contract 5: Multi-Agent → Context Engineering (Handoff Protocol)

| Field              | Specification                                                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Producer**       | Layer 5 — Orchestrator / supervisor agent                                                                                             |
| **Consumer**       | Layer 2 — Context assembler for the receiving subagent                                                                                |
| **Handoff tiers**  | Full / Scoped / Minimal — tier selection is mandatory, not optional                                                                   |
| **Handoff packet** | Structured via `handoff_packet.py`: `{tier, sacred_context, task_description, relevant_decisions, retrieved_content, working_memory}` |
| **Tier contract**  | Full tier ≤ 100% of orchestrator context. Scoped tier ≤ 40%. Minimal tier ≤ 10%.                                                      |
| **Sanitisation**   | Untrusted or third-party subagents receive Minimal tier with PII and internal decisions removed                                       |

**Failure mode:** Orchestrator forwards full conversation history to every subagent →
subagents waste token budget on irrelevant history → effective context for the actual
task is crowded out → quality degrades and costs increase linearly with swarm size.

**Reference:** `core-component-00/engineering/multi-agent-engineering/implementations/handoff_packet.py`

---

## Complete Runtime Execution Trace

The following trace shows a single task execution through all five layers in sequence:

```
[LAYER 5 — MULTI-AGENT]
  Orchestrator receives user task
  → Decomposes into subtasks
  → Selects swarm topology (e.g., Hierarchical)
  → Selects subagent for first subtask
  → Determines handoff tier (Scoped — bounded subtask)
  → Constructs handoff packet via handoff_packet.py
  ↓

[LAYER 4 — RAG]
  Receives query from context assembler
  → Reformulates query
  → Retrieves top-K chunks via vector search
  → Reranks by relevance
  → Applies ACL filter
  → Returns ranked, filtered, metadata-annotated chunks
  ↓

[LAYER 2 — CONTEXT ENGINEERING]
  Receives: handoff packet (Scoped) + RAG retrieval results
  → Assigns content to slots:
      System slot  ← agent identity from Layer 1
      Retrieved slot ← RAG results
      History slot ← relevant decisions from handoff packet
      Tool slot   ← tool definitions (if agent uses tools)
  → Enforces slot token budget
  → Flags sacred context
  → Assembles final context window
  ↓

[LAYER 3 — HARNESS ENGINEERING]
  Receives: assembled context window + token metadata
  → Verifies token count within model limit
  → Scrubs PII from inputs
  → Sets timeout for model call
  → Dispatches to model API
  → Receives response
  → Validates output against schema (Layer 1 contract)
  → Scans output for PII
  → On success: returns output to orchestrator
  → On failure: applies typed recovery (timeout → retry, validation → regenerate)
  ↓

[LAYER 1 — PROMPT ENGINEERING — executed at model]
  Model receives assembled context window
  → Operates within constraints defined by identity prompt
  → Applies output schema from identity prompt
  → Produces schema-conformant output
  ↓

[LAYER 5 — MULTI-AGENT — returns]
  Orchestrator receives validated output
  → Logs to episodic memory (feeds Layer 4 feedback loop)
  → Routes output to next subagent or synthesises final result
```

---

## Common Integration Failure Modes

| Failure Mode                        | Root Cause                                               | Layer Boundary        | Detection Signal                         |
| ----------------------------------- | -------------------------------------------------------- | --------------------- | ---------------------------------------- |
| Context overflow despite monitoring | RAG output ignores Retrieved slot token allocation       | RAG → Context         | Token count spike at assembly time       |
| Sacred context truncated            | Harness truncates without checking sacred flags          | Context → Harness     | Decision continuity loss mid-session     |
| Schema mismatch between agents      | Prompt output schema ≠ downstream consumer's expectation | Prompt → Context      | Downstream parse failures                |
| Stale knowledge despite RAG         | Harness feedback loop not implemented                    | Harness → RAG         | Repeated retrieval of superseded facts   |
| Subagent context bloat              | Handoff tier always set to Full                          | Multi-Agent → Context | Cost and latency scaling with swarm size |
| Orphaned agent decisions            | Handoff packet excludes previous decisions               | Multi-Agent → Context | Subagent repeats already-made decisions  |

---

## Integration Testing Protocol

Each integration contract should be tested independently:

| Contract              | Test Approach                                                                                 |
| --------------------- | --------------------------------------------------------------------------------------------- |
| RAG → Context         | Inject a RAG output without metadata; verify context assembler raises a schema error          |
| Context → Harness     | Assemble a context window 10% over token limit; verify harness rejects, not truncates         |
| Prompt → Context      | Submit an unstructured system prompt; verify assembler flags missing schema                   |
| Harness → RAG         | Execute a task; verify the output artifact appears in the RAG store with correct metadata     |
| Multi-Agent → Context | Send a Full handoff to a Minimal-tier agent; verify context assembler enforces the tier limit |

---

## References

- [Foundational Paper](core-component-00/agent-systems-engineering/CONCEPTS.md) — Convergence thesis
- [Compliance Standard](core-component-00/agent-systems-engineering/governance/compliance-standard.md) — Per-layer requirements
- [Context Assembler](core-component-00/engineering/context-engineering/implementations/context_assembler.py)
- [Harness Error Boundary](core-component-00/engineering/harness-engineering/implementations/error_boundary.py)
- [Token Budget Monitor](core-component-00/engineering/harness-engineering/implementations/context_monitor.py)
- [Handoff Packet](core-component-00/engineering/multi-agent-engineering/implementations/handoff_packet.py)
- [RAG Architecture](core-component-00/retrieval-augmented-generation/architecture/overview.md)
