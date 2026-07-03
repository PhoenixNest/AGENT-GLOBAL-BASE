# ASE Compliance Standard

> **Governing authority:** ADR-ASE-001 · Core Component 00 Laboratory
> **Version:** 1.0 · **Ratified:** 2026-04-28 · **Last Updated:** 2026-04-30

This document defines the minimum requirements an LLM-powered system must satisfy at
each ASE layer to receive an **ASE-Compliant** verdict. It is the authoritative
specification referenced during ASE compliance audits.

---

## How to Read This Standard

Each requirement has a **severity classification** indicating the consequence of
non-compliance:

| Classification  | Meaning                                                                       |
| --------------- | ----------------------------------------------------------------------------- |
| **Mandatory**   | Non-negotiable. Absence is a P0 gap. System cannot enter production.          |
| **Required**    | Expected in all standard cases. Absence is a P1 gap unless formally excepted. |
| **Recommended** | Best practice. Absence is a P2 or P3 gap depending on system scope.           |

A system achieves **ASE-Compliant** status when it has no P0 gaps and no unexcepted P1
gaps. See `adr-ase-001.md` for the exception process.

---

## Layer 1 — Prompt Engineering

**Reference implementation:** `core-component-00/prompt-engineering/`

Layer 1 governs the instruction architecture of every agent in the system.

| Requirement                                     | Classification | Specification                                                                                                                                                           |
| ----------------------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Role / persona defined**                      | Mandatory      | Each agent has a clearly specified role that constrains its expertise boundary. Vague role definitions ("You are a helpful assistant") do not satisfy this requirement. |
| **System prompt separated from task prompt**    | Mandatory      | Identity, behavioural constraints, and output format specifications are in the system slot. Task-specific instructions are in the task/user slot. These are not mixed.  |
| **Output format constrained**                   | Mandatory      | Any agent whose output is consumed by another agent or downstream system must use schema-constrained prompting. The schema is explicitly stated in the prompt.          |
| **Behavioural constraints enumerated**          | Required       | Forbidden behaviours (scope creep, silent failure, trim-to-pass) are explicitly listed in the agent's identity. See `patterns/anti-pattern-firewall.md`.                |
| **Escalation criteria defined**                 | Required       | Each agent specifies the conditions under which it escalates to a human or supervisor. These conditions are in the prompt, not inferred.                                |
| **Prompting technique appropriate to task**     | Required       | The prompting technique (zero-shot, few-shot, chain-of-thought) is matched to task type. See `core-component-00/prompt-engineering/patterns/advanced-patterns.md`.      |
| **Few-shot examples provided where beneficial** | Recommended    | Tasks with consistent structure and high precision requirements include representative examples in the prompt.                                                          |

---

## Layer 2 — Context Engineering

**Reference implementation:** `core-component-00/context-engineering/`

Layer 2 governs how the context window is assembled, managed, and handed off across
agent boundaries.

| Requirement                                 | Classification           | Specification                                                                                                                                                                              |
| ------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Four-slot context structure implemented** | Mandatory                | The context window is explicitly structured into System, Retrieved, History, and Tool Output slots. Ad-hoc string concatenation is not acceptable.                                         |
| **Slot priority order defined**             | Mandatory                | When the token budget is under pressure, the priority order for truncation is documented and enforced.                                                                                     |
| **Token budget tracked at assembly time**   | Mandatory                | The context assembler knows the total token budget and the allocation per slot before dispatching to the model.                                                                            |
| **Minimum Viable Context enforced**         | Required                 | Each agent receives only the context relevant to its task. Full conversation history is not forwarded wholesale to specialist subagents.                                                   |
| **Sacred context identified and protected** | Required                 | Irreversible decisions and non-negotiable constraints (e.g., approved PRD scope, security requirements) are designated as sacred and excluded from compression.                            |
| **History managed with compression**        | Required                 | For sessions exceeding 10 turns, history is managed with a rolling window and compression strategy. Raw history is not permitted to grow unbounded.                                        |
| **Context Handoff Protocol specified**      | Required for multi-agent | For every agent-to-agent transition, the handoff tier (Full / Scoped / Minimal) is specified and implemented. See `core-component-00/context-engineering/patterns/multi-agent-handoff.md`. |
| **Positional placement optimised**          | Recommended              | High-priority content appears at the beginning (system) and end (most recent) of the context window. Critical content is not buried in the middle.                                         |

---

## Layer 3 — Harness Engineering

**Reference implementations:** `core-component-00/harness-engineering/implementations/`

Layer 3 governs the execution envelope around every model call in the system.

| Requirement                                   | Classification           | Specification                                                                                                                                                                                  |
| --------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Timeout enforcement**                       | Mandatory                | Every model call has a timeout threshold defined and enforced. A model call with no timeout is not acceptable.                                                                                 |
| **Error boundary with typed recovery**        | Mandatory                | Every model call is wrapped in an error boundary that handles TimeoutError, RateLimitError, and ValidationError with distinct recovery paths. Catch-all exception handlers are not acceptable. |
| **Token budget monitor active**               | Mandatory                | A token budget monitor enforces context size limits at runtime and triggers pruning before the context window overflows.                                                                       |
| **Rate-limit retry with exponential backoff** | Mandatory                | Rate-limit responses (HTTP 429) trigger retry with exponential backoff and jitter. Immediate retry without backoff is not acceptable.                                                          |
| **Tool registry / whitelist defined**         | Required when tools used | The set of permitted tool calls is explicitly whitelisted. Agents cannot discover or invoke tools outside the whitelist.                                                                       |
| **Tool call limits enforced**                 | Required when tools used | Maximum tool call counts per task are defined and enforced. Unbounded tool loops are not acceptable.                                                                                           |
| **High-risk operations gated**                | Required for high-risk   | Operations with irreversible consequences (data deletion, financial transactions, external communication) require human approval gates.                                                        |
| **PII scrubbing on inputs**                   | Required                 | PII is redacted from model inputs before the API call. Raw PII must not appear in prompts or logs.                                                                                             |
| **PII scanning on outputs**                   | Required                 | Model outputs are scanned for PII exposure before returning to users or downstream systems.                                                                                                    |
| **Degradation fallback tiers defined**        | Recommended              | Each agent has a Tier 1 → Tier 2 → Tier 3 degradation plan for progressive service reduction when primary paths fail.                                                                          |

---

## Layer 4 — RAG / Knowledge

**Reference implementations:** `core-component-00/retrieval-augmented-generation/`

Layer 4 governs how the system retrieves and manages knowledge beyond model weights.

> **Layer 4 may be intentionally absent.** If the system operates entirely on parametric
> knowledge with no retrieval requirement, document the rationale and mark this layer as
> _intentionally absent_. This is the only ASE layer that can be absent without a
> compliance gap, provided the rationale is documented and approved.

| Requirement                                               | Classification          | Specification                                                                                                                                                                                         |
| --------------------------------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Retrieval pipeline implemented**                        | Mandatory (if required) | If external, domain-specific, or time-sensitive knowledge is needed, a retrieval pipeline must be implemented. Reliance on parametric knowledge for facts that should be retrieved is not acceptable. |
| **Chunking strategy defined**                             | Required                | The chunking strategy (size, overlap, method) is documented and appropriate for the content type.                                                                                                     |
| **Embedding model specified and pinned**                  | Required                | The embedding model is specified and pinned to a version. Unpinned embedding models risk silent re-ranking changes on model updates.                                                                  |
| **Reranking step implemented**                            | Required                | Retrieved chunks are reranked by relevance before context assembly. Top-k retrieval without reranking is not acceptable for production.                                                               |
| **ACL filtering applied**                                 | Required                | Retrieval results are filtered by access control rules before entering the context window.                                                                                                            |
| **Retrieval freshness characteristics documented**        | Required                | The staleness characteristics of the knowledge base are understood and documented. Time-sensitive domains require freshness bounds.                                                                   |
| **Knowledge Item (KI) pattern used for frequent queries** | Recommended             | Frequently-retrieved content is distilled into curated Knowledge Items for low-latency lookup.                                                                                                        |

---

## Layer 5 — Multi-Agent Engineering

**Reference implementations:** `core-component-00/multi-agent-engineering/`

Layer 5 is **required when the system involves more than one coordinated LLM agent**.
For single-agent systems, this layer is not applicable.

| Requirement                                              | Classification                     | Specification                                                                                                                                                      |
| -------------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Swarm topology explicitly selected**                   | Mandatory                          | The swarm topology (Hierarchical, Flat, Mesh, Pipeline, Hybrid) is documented before implementation. Emergent topology without design intent is not acceptable.    |
| **Task decomposition specified**                         | Mandatory                          | The decomposition of the overall task into agent-level subtasks is documented. Each agent's scope is bounded and non-overlapping.                                  |
| **Context Handoff Protocol implemented**                 | Mandatory                          | Every agent-to-agent handoff uses the Full / Scoped / Minimal tier protocol. See Context Engineering Layer 2 requirement.                                          |
| **Agent roles non-overlapping**                          | Required                           | Each agent has a distinct, bounded role. Agents with >70% skill-set overlap should be consolidated.                                                                |
| **Supervisor agent defined for hierarchical swarms**     | Required                           | Hierarchical swarms have a supervisor agent responsible for task delegation, output synthesis, and conflict resolution.                                            |
| **Git worktree isolation used for parallel development** | Required when parallel coding      | Agent parallel development uses git worktree for filesystem isolation. See `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`. |
| **Merge integration agent designated**                   | Required when parallel development | A designated Integration Agent is responsible for conflict resolution and merge to main. No agent self-merges without review.                                      |
| **Anti-patterns explicitly prohibited in agent prompts** | Required                           | Agent identity prompts include an explicit Forbidden Behaviours section. See `patterns/anti-pattern-firewall.md`.                                                  |

---

## Cross-Layer Integration Requirements

Beyond per-layer compliance, the layers must be **compatible at their interfaces**:

| Interface                   | Requirement                                                                                                      |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **RAG → Context**           | Retrieved document format matches the format expected by the context assembler's retrieved slot.                 |
| **Context → Harness**       | Token budget assumptions in the context assembler match the limits enforced by the harness token budget monitor. |
| **Prompt → Context**        | Prompt output schemas match what the context assembler or downstream tool calls expect as input.                 |
| **Harness → RAG**           | New knowledge generated by agent execution is captured and fed back into the knowledge store.                    |
| **Agent → Agent (handoff)** | The handoff packet content matches what the receiving agent's prompt declares as its required input.             |

---

## Compliance Verdict Criteria

| Verdict           | Conditions                                                                     |
| ----------------- | ------------------------------------------------------------------------------ |
| **ASE-Compliant** | No Mandatory requirements unmet. No Required requirements unmet (or excepted). |
| **Conditional**   | No Mandatory gaps. One or more Required gaps with active remediation plan.     |
| **Non-Compliant** | One or more Mandatory requirements unmet. System may not enter production.     |

---

## Audit Instrument

Compliance audits are conducted using:

> `core-component-00/crew/director/elias-vance/skills/ase-compliance-audit.md`

The skill provides layer-by-layer audit checklists, gap severity classification, and
output format for the compliance report.
