# Research Report — Multi-Agent Memory Coherence

---

## Metadata

| Field                | Value                                                    |
| -------------------- | -------------------------------------------------------- |
| **Investigation ID** | `2026-06-30-multi-agent-memory-coherence`                |
| **Date Started**     | 2026-06-30                                               |
| **Date Completed**   | 2026-06-30                                               |
| **Status**           | Complete                                                 |
| **Investigator**     | Dr. Elias Vance, Laboratory Director — Core Component 00 |
| **Laboratory**       | Core Component 00                                        |
| **Module(s)**        | `context-engineering/`, `multi-agent-engineering/`       |
| **Priority**         | High                                                     |
| **Requestor**        | CEO — CC-00 Research Commission (2026-06-30)             |

---

## Executive Summary

This investigation examined how distributed agents can maintain consistent shared memory without
a central store, surveying Anthropic's official multi-agent architecture, the experimental
**Claude Code Agent Teams** feature (v2.1.178), Anthropic's own 16-agent C-compiler experiment,
and recent research on Governed Shared Memory (GSM, arXiv:2606.24535) and CRDTs. The principal
finding is that Anthropic has moved toward structured file-based coordination (shared task lists
with file-locking, mailbox messaging, git as substrate) rather than abstract memory primitives.
The GSM framework provides the most rigorous formalisation of fleet memory without a central
arbiter, achieving 97.5% fleet-sibling visibility and ~830ms write-to-visibility latency. For
CC-00, the recommended path is an **event-sourced shared log** — compatible with Anthropic's
file-based coordination pattern and the CC-00 Context Handoff Protocol — as the primary vehicle
for decentralised agent memory.

---

## Investigation Scope

### What Was Investigated

1. Anthropic's official multi-agent architecture documentation and Agent Teams feature
2. Anthropic's C-compiler experiment (16 agents, ~2,000 sessions) as a production reference
3. The Model Context Protocol (MCP) specification's memory/state management capabilities
4. The Governed Shared Memory (GSM) framework (arXiv:2606.24535)
5. CRDT applicability to agent memory, including CodeCRDT (arXiv:2510.18893)
6. The three-layer memory hierarchy (arXiv:2603.10062) and its protocol gaps
7. Trade-offs between consistency models for distributed agent memory

### Why This Investigation Was Needed

The CC-00 `memory_store.py` implements single-node memory. The research programme asks
whether distributed agents — each in a separate process, without guaranteed network-level
coordination — can maintain coherent shared memory without an arbitrating central store.
This is prerequisite to designing production multi-agent swarms that share knowledge without
a single point of failure.

### Out of Scope

- Central-store approaches (Redis, Postgres) as coordination primitives
- Hardware-level distributed shared memory
- Memory coherence in GPU inference pipelines

---

## Research Questions

1. What does Anthropic's official documentation say about multi-agent memory architecture?
2. What coordination mechanism did Anthropic use in its 16-agent C-compiler experiment?
3. Does MCP provide memory primitives suitable for distributed agents?
4. What is the GSM framework, and what consistency guarantees does it provide?
5. Are CRDTs applicable to semantic agent memory, and what are the limitations?
6. What is the practical path to decentralised memory coherence within CC-00?

---

## Methodology

### Approach

1. **Official documentation review** — Surveyed `docs.anthropic.com/en/docs/build-with-claude/
agents` and the Claude Code Agent Teams documentation
2. **Anthropic engineering blog review** — Retrieved the C-compiler experiment report from
   `anthropic.com/engineering/building-c-compiler`
3. **MCP specification review** — Examined the MCP spec at `modelcontextprotocol.io`
4. **Academic literature review** — Retrieved GSM (arXiv:2606.24535), CodeCRDT
   (arXiv:2510.18893), and the three-layer hierarchy paper (arXiv:2603.10062)
5. **CC-00 pattern audit** — Cross-referenced findings against `memory_store.py`,
   `handoff_packet.py`, and the Context Handoff Protocol documentation

### Tools and Resources

- Anthropic Agents Documentation:
  `https://docs.anthropic.com/en/docs/build-with-claude/agents` (accessed 2026-06-30)
- Claude Code Agent Teams Documentation:
  `https://code.claude.com/docs/en/agent-teams` (accessed 2026-06-30)
- Anthropic Engineering — Building a C Compiler with Claude:
  `https://www.anthropic.com/engineering/building-c-compiler` (accessed 2026-06-30)
- MCP Specification: `https://modelcontextprotocol.io/specification` (accessed 2026-06-30)
- GSM Framework: `https://arxiv.org/html/2606.24535v1` (accessed 2026-06-30)
- CodeCRDT: `https://arxiv.org/pdf/2510.18893` (accessed 2026-06-30)
- Three-layer memory hierarchy: `https://arxiv.org/html/2603.10062` (accessed 2026-06-30)

### Constraints

- Claude Code Agent Teams is experimental (v2.1.178); behaviour may change
- GSM empirical results are from the paper's authors, not an independent CC-00 experiment
- CRDT applicability analysis is theoretical; no CC-00 prototype was built

---

## Findings

### Finding 1: Anthropic's Coordination Pattern Is File-Based, Not Abstract Memory

Anthropic's official multi-agent architecture does not provide a shared memory primitive.
Each agent has access only to what is explicitly passed in its context window.

**Claude Code Agent Teams (experimental, v2.1.178)** uses three coordination primitives:

| Primitive                | Mechanism                                                                                   | Consistency Model                   |
| ------------------------ | ------------------------------------------------------------------------------------------- | ----------------------------------- |
| **Shared task list**     | JSON task files in `~/.claude/tasks/{team-name}/`; OS file locking prevents race conditions | Pessimistic locking (task claim)    |
| **Peer-to-peer mailbox** | Named message delivery; no polling required by sender                                       | Asynchronous message passing        |
| **Shared filesystem**    | Git repository as the shared state medium                                                   | Optimistic concurrency + file locks |

**Evidence:**

- Claude Code Docs: "Teammates share a task list, claim work, and communicate directly with
  each other." `https://code.claude.com/docs/en/agent-teams` (accessed 2026-06-30)
- Docs on auto memory: "Auto memory is machine-local. All worktrees within the same git
  repository share one auto memory directory. Files are not shared across machines or cloud
  environments." `https://code.claude.com/docs/en/memory` (accessed 2026-06-30)

**Implications:**

- Anthropic's production pattern is **structured files + file locking**, not a distributed
  memory layer. CC-00 should align with this pattern rather than designing a novel
  memory abstraction that diverges from the platform direction.

---

### Finding 2: Anthropic's 16-Agent C-Compiler Experiment Used Git as Memory Substrate

Anthropic's own engineering team coordinated 16 parallel Claude agents over ~2,000 sessions
to produce a 100,000-line C compiler, using **git as the shared coordination and memory substrate**.

**Coordination mechanism:**

- Task locking: agents write a file to `current_tasks/` to "claim" a task (optimistic locking)
- Git push/pull: agents push commits to an upstream bare repo and pull before committing;
  git merge conflicts force agents to select a different task (natural conflict resolution)
- Shared state: `README` and `progress` documents in the repo serve as shared knowledge

**Evidence:**

- Anthropic Engineering: "Claude takes a 'lock' on a task by writing a text file to
  current_tasks/… git synchronisation forced one to select a different task."
  `https://www.anthropic.com/engineering/building-c-compiler` (accessed 2026-06-30)

**Implications:**

- This is the most authoritative real-world reference for CC-00 multi-agent coordination.
  Git-as-substrate requires no additional infrastructure, is compatible with the CC-00
  git worktree isolation pattern, and scales to at least 16 concurrent agents empirically.

---

### Finding 3: MCP Does Not Provide Distributed Memory Primitives

The Model Context Protocol defines Tools, Resources, and Prompts. Resources are URI-addressable
content blobs. Neither Resources nor any other MCP primitive provides write-with-observe
semantics across agents — update visibility requires explicit re-query.

**Evidence:**

- MCP specification: `https://modelcontextprotocol.io/specification` (accessed 2026-06-30)
- The `workspace-knowledge` MCP server in this workspace is a read-write Resource store;
  agents must explicitly call `search_docs` or `retrieve_context` after a write to observe
  updated content

**Implications:**

- MCP can serve as a **shared external store** for agent memory, but it does not eliminate
  the need for a coordination mechanism to manage concurrent writes and read visibility.

---

### Finding 4: GSM Framework Formalises Decentralised Fleet Memory

The **Governed Shared Memory (GSM)** framework (arXiv:2606.24535) provides the most rigorous
published formalisation of agent fleet memory without a central arbiter.

**Formal definition:** F = (A, M, G, P, T) where:

- A = agents, M = memory records, G = governance policies
- P = provenance chains, T = temporal markers

**Five design principles:** scoped retrieval, explicit provenance, temporal correctness,
policy-governed propagation, persistent shared state.

**Empirical results:**

| Metric                                  | Result                                 |
| --------------------------------------- | -------------------------------------- |
| Fleet-sibling visibility                | 97.5% (117/120 probes)                 |
| Cross-fleet leakage                     | 0% (80 foreign-fleet attempts blocked) |
| Write-to-visibility latency             | ~830ms (strong enrichment mode)        |
| Provenance chain reconstruction (4-hop) | Median ~291ms per hop                  |

**Security finding — Bimodal Scope Enforcement Vulnerability:** Direct GET-by-id handlers
may bypass agent-scope predicates enforced on search paths, creating silent unauthorised
access. Every access path must implement identical scope predicates.

**Evidence:**

- GSM paper: `https://arxiv.org/html/2606.24535v1` (accessed 2026-06-30)

**Implications:**

- GSM's locally-enforced governance model is directly applicable to CC-00. The CC-00 ACL
  filtering in `retrieval.py` (RAG module) is an implementation of the GSM scope predicate
  principle. The bimodal enforcement vulnerability is a concrete security requirement: all
  memory access paths must enforce scope, not only search paths.

---

### Finding 5: Three-Layer Memory Hierarchy Identifies Two Unresolved Protocol Gaps

A 2026 academic survey (arXiv:2603.10062) proposes a three-layer agent memory hierarchy:

| Layer        | Characteristics               | Example          |
| ------------ | ----------------------------- | ---------------- |
| I/O layer    | External knowledge, documents | RAG corpus       |
| Cache layer  | Fast, limited, per-agent      | Context window   |
| Memory layer | Persistent, large-capacity    | Vector DB, files |

**Two critical protocol gaps identified:**

1. **No standard cache-sharing protocol** for transferring in-context cached artifacts between
   agents — this is the primary unresolved architectural gap.
2. **No standard memory access control protocol** — no formalised permission model for
   which agents can read/write which memory records.

**Evidence:**

- Three-layer hierarchy paper: `https://arxiv.org/html/2603.10062` (accessed 2026-06-30)
- Survey finding: "36.9% of multi-agent system failures stem from state misalignment" — not
  communication failure (O'Reilly Radar, 2026)

**Implications:**

- Gap 1 (cache-sharing) means there is no platform-supported way to share the in-context
  compressed cache between agents — each agent must rebuild its context from the shared
  store. Gap 2 (access control) is partially addressed by GSM and by CC-00's ACL filtering
  in the RAG module; a generalisation to non-RAG memory is needed.

---

### Finding 6: CRDTs Are Applicable to Structural Agent Memory but Not Semantic Conflicts

CRDTs (Conflict-free Replicated Data Types) allow agents to write independently without
coordination locks, guaranteeing eventual consistency. CodeCRDT (arXiv:2510.18893) applies
observation-driven CRDT coordination to multi-agent code generation.

**Critical limitation:** CRDTs resolve structural conflicts (append sets, counters, maps)
but cannot resolve **semantic contradiction** — if Agent A asserts "X is True" and Agent B
asserts "X is False," no CRDT merge rule produces the correct result without model-layer
arbitration.

**Evidence:**

- CodeCRDT: `https://arxiv.org/pdf/2510.18893` (accessed 2026-06-30)
- Shapiro et al. (2011). "Conflict-free Replicated Data Types." INRIA Research Report.

**Implications:**

- CRDTs are appropriate for **structural shared state** (task lists, counters, agent
  registration) but not for **semantic shared knowledge** (beliefs, facts, conclusions).
  A hybrid approach — CRDTs for structure, semantic arbitration for knowledge — is the
  correct architecture.

---

## Analysis

### Interpretation of Findings

The research question ("How do distributed agents maintain consistent shared memory without a
central store?") is answered at the practical level:

1. **Anthropic's production answer:** git-as-substrate with file locking and structured
   documents. This eliminates the need for novel distributed memory infrastructure.
2. **Research frontier answer:** GSM-style locally-enforced governance with provenance
   chains and temporal markers — achieving 97.5% visibility without a central arbiter.
3. **Mathematical answer:** CRDTs for structural state; semantic arbitration for knowledge;
   event-sourced log for the full audit trail.

For CC-00, the practical architecture is: **git-as-substrate (aligned with Anthropic's
production pattern) + event-sourced append log (for semantic observations) + CRDTs for
task claiming and counters**. This hybrid covers the full memory spectrum without a
central store.

### Trade-offs Identified

| Pattern                      | Consistency           | Availability | Complexity | Anthropic-Aligned | CC-00 Fit |
| ---------------------------- | --------------------- | ------------ | ---------- | ----------------- | --------- |
| Git-as-substrate (Anthropic) | Eventual (per-commit) | High         | Low        | Yes               | High      |
| File locking (Agent Teams)   | Strong (per-task)     | Medium       | Low        | Yes               | High      |
| Event-sourced log            | Causal                | High         | Medium     | Partial           | High      |
| GSM (scoped DB)              | Causal + governed     | High         | High       | Research          | Medium    |
| CRDT (structural)            | Strong eventual       | Very High    | Medium     | Research          | Medium    |
| Semantic arbiter agent       | Strong                | Low          | Very High  | No                | Low       |

### Risks and Limitations

- **Agent Teams is experimental**: the shared task list mechanism may change before GA
- **Git merge conflicts at scale**: the C-compiler experiment used 16 agents; at 50+ agents,
  merge conflict frequency may become a performance bottleneck
- **CRDT semantic limitation**: any knowledge-sharing use case requires arbitration beyond
  what CRDTs can provide
- **Bimodal enforcement vulnerability**: all CC-00 memory access paths must enforce scope
  predicates — a security requirement, not an optimisation

---

## Recommendations

### Primary Recommendation

**Adopt git-as-substrate as the CC-00 canonical multi-agent coordination pattern,
supplemented by an event-sourced append log for semantic observations.**

1. **Formalise the git coordination pattern** in `multi-agent-engineering/patterns/` as
   a CC-00 canonical pattern (task files in `current_tasks/`, push/pull protocol,
   `progress.json` as shared state)
2. **Implement `shared_memory_log.py`** — per-agent JSONL append logs with Lamport
   timestamps; merge-at-read semantics; integrates with `handoff_packet.py` Scoped tier

### Secondary Recommendations

1. **Apply GSM scope predicate principle to all CC-00 memory access paths** — ensure every
   read path (not only search) enforces agent-scope filtering. Fix the bimodal enforcement
   vulnerability proactively.
2. **Evaluate Claude Code Agent Teams for CC-00 multi-agent swarms** — when Agent Teams
   reaches GA, assess replacing the custom `swarm_orchestrator.py` coordination layer.
3. **Add CRDT-based task claiming to `swarm_orchestrator.py`** — replace the current
   in-memory task queue with a file-lock-based CRDT counter to survive orchestrator restart.

### Implementation Priority

| Recommendation                         | Priority | Effort | Impact          |
| -------------------------------------- | -------- | ------ | --------------- |
| Git coordination pattern documentation | P0       | 1 day  | High            |
| `shared_memory_log.py` implementation  | P1       | 3 days | High            |
| GSM scope predicate audit              | P1       | 1 day  | High (security) |
| Agent Teams evaluation                 | P2       | 2 days | Medium          |
| CRDT task claiming                     | P2       | 2 days | Medium          |

### Next Steps

1. Document git coordination pattern in `multi-agent-engineering/patterns/git-coordination.md`
2. Design `AgentEvent` schema (agent ID, Lamport timestamp, event type, payload)
3. Implement `shared_memory_log.py` with file-based per-agent logs
4. Audit all CC-00 memory access paths for bimodal scope enforcement vulnerability
5. Validate against a synthetic 5-agent swarm with concurrent writes

---

## References

### Internal Documentation

- `core-component-00/multi-agent-engineering/implementations/swarm_orchestrator.py`
- `core-component-00/multi-agent-engineering/implementations/handoff_packet.py`
- `core-component-00/context-engineering/implementations/memory_store.py`
- `core-component-00/retrieval-augmented-generation/implementations/retrieval.py`
  (ACL filtering — implements GSM scope predicate principle)

### External Sources

- Anthropic Agents Documentation:
  `https://docs.anthropic.com/en/docs/build-with-claude/agents` (accessed 2026-06-30)
- Claude Code Memory Documentation:
  `https://code.claude.com/docs/en/memory` (accessed 2026-06-30)
- Claude Code Agent Teams Documentation:
  `https://code.claude.com/docs/en/agent-teams` (accessed 2026-06-30)
- Anthropic Engineering — Building a C Compiler with Claude:
  `https://www.anthropic.com/engineering/building-c-compiler` (accessed 2026-06-30)
- MCP Specification: `https://modelcontextprotocol.io/specification` (accessed 2026-06-30)
- GSM: Governed Shared Memory (arXiv:2606.24535):
  `https://arxiv.org/html/2606.24535v1` (accessed 2026-06-30)
- CodeCRDT (arXiv:2510.18893):
  `https://arxiv.org/pdf/2510.18893` (accessed 2026-06-30)
- Three-layer memory hierarchy (arXiv:2603.10062):
  `https://arxiv.org/html/2603.10062` (accessed 2026-06-30)
- Shapiro, M. et al. (2011). "Conflict-free Replicated Data Types." INRIA Research Report.

### Related Work

- `telescope/2026-06-25-qdrant-migration-plan/research-report.md`
- Dr. Elias Vance, _Multi-Agent Context Handoff Protocols_ (Architecture Spec, 2026)

---

## Open Questions

1. **At what agent count do git merge conflicts become a coordination bottleneck?**
   - Anthropic's C-compiler used 16 agents without reported conflict problems
   - Priority: Medium; relevant for swarms > 16 agents
   - Assigned: Future experimental programme

2. **Can the bimodal scope enforcement vulnerability be detected by static analysis?**
   - A linter rule checking that all read paths enforce scope predicates would prevent regressions
   - Priority: High (security)
   - Assigned: CC-00 Harness Engineering

3. **When will Claude Code Agent Teams reach GA, and what are the breaking changes?**
   - Experimental status limits production adoption
   - Priority: Medium; dependent on Anthropic release timeline
   - Assigned: Monitor Anthropic changelog

---

## Version History

| Version | Date       | Author                                                   | Changes                                              |
| ------- | ---------- | -------------------------------------------------------- | ---------------------------------------------------- |
| 1.0     | 2026-06-30 | Dr. Elias Vance, Laboratory Director — Core Component 00 | Initial draft (pre-fork research)                    |
| 2.0     | 2026-06-30 | Dr. Elias Vance, Laboratory Director — Core Component 00 | Full revision with Agent Teams, C-compiler, GSM data |

---

**Template Version:** 1.0
**Last Updated:** 2026-06-30
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
