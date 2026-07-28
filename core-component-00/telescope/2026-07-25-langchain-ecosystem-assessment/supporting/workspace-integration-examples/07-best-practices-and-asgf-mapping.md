# 07 — Best Practices and the Full ASGF Mapping

**Prerequisite:** `00-conventions-and-baseline.md`.
**Status:** Practice catalogue and compliance map. Derived from the research report plus the
example work in `01`–`06`. **Almost nothing here was validated by execution** — this file contains
no code blocks of its own to run, so its accuracy rests on the files it cites, several of which now
carry real execution evidence themselves (see `01`–`03`'s updated Status lines). **One exception,
added 2026-07-27:** Part 4's anti-pattern rank 4 (`FilesystemBackend` without `virtual_mode=True`)
is itself execution-verified — see its own footnote.

---

## Part 1 — The practice catalogue

### 1.1 The ten inherited practices, with CC-00 grounding

The research report established ten best practices and observed that "the dominant failure mode in
LangChain projects is not the framework — it is using too much of it." Each is restated below with
what it means _in this workspace_, and where the examples implement it.

| #   | Practice                                                                    | In this workspace                                                                                                               | Example            |
| --- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| 1   | Start with `create_agent`; drop to raw LangGraph only when it stops fitting | The pilot in `06` uses a `StateGraph` because it genuinely needs a supervisor topology and an approval gate — not on day one.   | `01 §1`, `02`      |
| 2   | Pin every package exactly                                                   | A **security control**, not hygiene — the checkpointer CVE chain. Floors in `00 §3` are non-negotiable.                         | `00 §3`            |
| 3   | Cross-cutting concerns in middleware, not tools or prompts                  | The entire CC-00 governance kit is middleware. Retry, budget, PII, and slot structure all attach there.                         | `00 §7`            |
| 4   | Constrain output with schemas, never prose                                  | ASGF L1 **Mandatory**. `Literal` enums, not "reply in JSON".                                                                    | `01 §2`, `06 §4.4` |
| 5   | Keep tools few, well-named, narrowly typed                                  | Tool descriptions are prompt surface. Say when _not_ to call. `04 §2` filters the bridged list down.                            | `01 §3`            |
| 6   | Always attach a checkpointer for multi-turn work                            | Without it: no durability, no `interrupt()`, no post-incident analysis — and no LangSmith to compensate.                        | `02 §2`            |
| 7   | Gate irreversible actions with `interrupt()`                                | ASGF L3 Required. Driven off `requires_approval` in CC-00's tool registry so the flag is load-bearing.                          | `02 §3`, `06 §4.5` |
| 8   | Bound the loop — iterations, timeouts, tool-call caps                       | `TokenBudgetMiddleware` caps model calls; `TOOL_REGISTRY` caps per-tool calls; every model has a timeout.                       | `00 §7`            |
| 9   | Manage context deliberately, before overflow                                | `ContextAssembler` budgets at assembly time. Priority fill runs _before_ dispatch, not after a failure.                         | `00 §7`, `02 §1`   |
| 10  | Do not wrap what you do not need                                            | A single schema-constrained call is a single call. But **simple enough to skip the agent ≠ simple enough to skip the harness.** | `01 §5`            |

**Practices 3, 4, 6, 7, and 8 map one-to-one onto ASGF requirements.** That convergence is the
strongest technical argument for LangChain in this workspace: a team following the framework's own
guidance lands most of the way toward Conditional without trying.

### 1.2 Practices this deliverable adds

These come from writing `01`–`06` against this workspace's actual code and configuration. They are
CC-00-specific and not in the upstream guidance.

| #   | Practice                                                                                              | Why                                                                                                                                                                                                                                           |
| --- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 11  | **Bind ACL identity in a closure, never as a tool parameter**                                         | A `user_role` parameter lets the model pass `"admin"`. Prompt injection becomes privilege escalation. `04 §5`.                                                                                                                                |
| 12  | **Namespace bridged MCP tools; drop write-capable ones by default**                                   | Both workspace servers export `health_check`; two export index mutators. Gate-passing in a supervised session ≠ safe unattended. `04 §2–3`.                                                                                                   |
| 13  | **Treat "empty result" and "backend down" as different outcomes**                                     | `agent-memory` degrades silently by design. An agent that reads empty as absent answers confidently and wrongly. `04 §4`.                                                                                                                     |
| 14  | **Keep `FourSlotContextMiddleware` innermost, always**                                                | Any middleware that rewrites messages after the assembler silently destroys an ASGF **Mandatory** guarantee. `00 §7`.                                                                                                                         |
| 15  | **Record human decisions as sacred context**                                                          | Otherwise summarisation compresses away the fact that a human said no, and the agent re-proposes it. `02 §3`.                                                                                                                                 |
| 16  | **Select the CC-00 budget profile per role, not per system**                                          | A supervisor lives on tool outputs (`orchestration`, 40% tools); a retriever lives on retrieval (`factual_qa`, 65%). `06 §4.6`.                                                                                                               |
| 17  | **Enumerate subagents statically; never ship general-purpose alone**                                  | Dynamic spawning is emergent topology, which ASGF L5 **Mandatory** prohibits. Declaring the roster resolves it. `03 §Tension`.                                                                                                                |
| 18  | **Point `FilesystemBackend.root_dir` at a disposable directory, and always pass `virtual_mode=True`** | This workspace's guardrails _are_ files. An agent with repo-root write access can edit what constrains it — and `root_dir` alone does not confine anything; without `virtual_mode=True` a `..` path escapes it. `03 §3`, anti-pattern rank 4. |
| 19  | **Derive `thread_id` from an authenticated session**                                                  | A thread id is a capability to resume someone else's conversation and read its state. `02 §2`.                                                                                                                                                |
| 20  | **Encode research hygiene as schema fields**                                                          | `vendor_reported: bool` and a `limitations: list[str]` survive being handed to an agent; a prose instruction does not. `06 §4.4`.                                                                                                             |
| 21  | **Alias CC-00 module imports; do not rely on `sys.path`**                                             | All four module roots expose a top-level `implementations` package. One process, one winner. `00 §6`.                                                                                                                                         |
| 22  | **Decide observability before building, not after**                                                   | No LangSmith means no turnkey tracing _or evaluation_. Tracing is solvable in a day; evaluation is not. `00 §5`.                                                                                                                              |

---

## Part 2 — Full ASGF requirement map

Scored against
`core-component-00/agent-systems-governance-framework/governance/compliance-standard.md`.

**Legend:** ✅ framework provides · 🔧 must be built (and is, in these examples) · ❌ gap
**"Provides"** means the framework supplies the mechanism, not that using it is automatic.

### Layer 1 — Prompt Engineering

| Requirement                              | Level       | LangChain            | Closed by                                      |
| ---------------------------------------- | ----------- | -------------------- | ---------------------------------------------- |
| Role / persona defined                   | Mandatory   | ✅ slot              | 🔧 Content is yours. `01 §1`, `06 §4.1`        |
| System prompt separated from task prompt | Mandatory   | ✅                   | Clean by construction in `create_agent`        |
| Output format constrained                | Mandatory   | ✅ `response_format` | 🔧 `ToolStrategy` + Pydantic. `01 §2`          |
| Behavioural constraints enumerated       | Required    | ❌                   | 🔧 Forbidden-behaviours section. `06 §4.1`     |
| Escalation criteria defined              | Required    | ❌                   | 🔧 Escalation section + `requires_human` field |
| Prompting technique appropriate to task  | Required    | ❌                   | 🔧 Design decision; record it                  |
| Few-shot examples where beneficial       | Recommended | ✅                   | Optional                                       |

**L1 verdict: no gaps** — every item is content, and content is authored.

### Layer 2 — Context Engineering

| Requirement                             | Level                    | LangChain                                | Closed by                                    |
| --------------------------------------- | ------------------------ | ---------------------------------------- | -------------------------------------------- |
| **Four-slot context structure**         | **Mandatory**            | ❌ free-form message list                | 🔧 `FourSlotState` + middleware. **`02 §1`** |
| **Slot priority order defined**         | **Mandatory**            | ❌                                       | 🔧 `BUDGET_PROFILES` + `_priority_fill`      |
| **Token budget tracked at assembly**    | **Mandatory**            | ⚠️ trimming exists, not slot budgeting   | 🔧 `ContextAssembler`, by construction       |
| Minimum Viable Context enforced         | Required                 | ❌                                       | 🔧 Scoped/Minimal handoff tiers. `06 §4.3`   |
| Sacred context identified and protected | Required                 | ❌                                       | 🔧 `Annotated[list[str], add]` — append-only |
| History managed with compression        | Required                 | ✅ summarisation middleware              | 🔧 Or `ContextAssembler`'s own budget        |
| Context Handoff Protocol specified      | Required for multi-agent | ⚠️ `Command` carries it; tier is CC-00's | 🔧 `HandoffPacket` + tier. `06 §4.3`         |
| Positional placement optimised          | Recommended              | ❌                                       | 🔧 `_anchor_order`                           |

**L2 is where a naive adoption fails.** Three Mandatory items, none provided. The research report
called this the sharpest risk and it remains so: `create_agent` with no typed state and no assembler
is **Non-Compliant**, not merely imperfect.

### Layer 3 — Harness Engineering

| Requirement                               | Level                    | LangChain                              | Closed by                                        |
| ----------------------------------------- | ------------------------ | -------------------------------------- | ------------------------------------------------ |
| Timeout enforcement                       | Mandatory                | ✅ per-call timeouts                   | `init_chat_model(timeout=…)`                     |
| **Error boundary with typed recovery**    | **Mandatory**            | ⚠️ `.with_retry()` ≈ catch-all         | 🔧 `TypedErrorBoundaryMiddleware`. `00 §7`       |
| Token budget monitor active               | Mandatory                | ❌                                     | 🔧 `TokenBudgetMiddleware`                       |
| Rate-limit retry with exponential backoff | Mandatory                | ✅ (verify jitter)                     | 🔧 Explicit jitter in `_classify` path           |
| Tool registry / whitelist                 | Required when tools used | ✅ explicit tool list = whitelist      | 🔧 `ToolGovernanceMiddleware` + registry         |
| Tool call limits enforced                 | Required when tools used | ❌                                     | 🔧 `max_calls_per_task` + `max_model_calls`      |
| **High-risk operations gated**            | Required for high-risk   | ✅✅ **`interrupt()` — best in class** | `02 §3`, `06 §4.5`                               |
| PII scrubbing on inputs                   | Required                 | ❌                                     | 🔧 `PIIMiddleware` (limited — see `00 §7`)       |
| PII scanning on outputs                   | Required                 | ❌                                     | 🔧 `PIIMiddleware`                               |
| Degradation fallback tiers                | Recommended              | ⚠️                                     | 🔧 `CircuitBreaker` + `MCPDegradationMiddleware` |

**`interrupt()` is the one place LangGraph is unambiguously better than CC-00's current
implementation.** The research report said so and this work confirms it: a durable, resumable,
cross-process approval pause is cleaner than anything in `harness-engineering/implementations/`.

### Layer 4 — RAG / Knowledge

| Requirement                          | Level                   | LangChain                           | Closed by                                        |
| ------------------------------------ | ----------------------- | ----------------------------------- | ------------------------------------------------ |
| Retrieval pipeline implemented       | Mandatory (if required) | ✅ retrievers                       | **CC-00 `RAGPipeline` — retained, not replaced** |
| Chunking strategy defined            | Required                | ✅ text splitters                   | CC-00 `chunker.py`                               |
| Embedding model specified and pinned | Required                | ❌                                  | 🔧 Shared cache slug convention                  |
| **Reranking step implemented**       | Required                | ✅ `ContextualCompressionRetriever` | ❌ **UNMET in this workspace** — see below       |
| **ACL filtering applied**            | Required                | ❌ **not provided**                 | ✅ **CC-00 `acl_filter` — the asset**            |
| Retrieval freshness documented       | Required                | ❌                                  | 🔧 `rag-sync-state.json` + per-corpus statement  |
| Knowledge Item pattern               | Recommended             | ❌                                  | Optional                                         |

**This layer is the reason "LangChain above CC-00, never instead of it" is the architecture.** ACL
filtering is Required, CC-00 has it, LangChain does not provide it. Replacing CC-00 RAG would create
a Required gap to gain nothing.

**The one live Required gap:** reranking. `RAGPipeline` does BM25 + RRF fusion — hybrid retrieval,
not cross-encoder reranking. Closing it costs ~560 MB of the ~7 GB free VRAM and roughly half a day,
and **it does not depend on the LangChain decision**. It is the single highest-value action available
from this whole line of work.

### Layer 5 — Multi-Agent Engineering

| Requirement                                | Level                              | LangChain                            | Closed by                                  |
| ------------------------------------------ | ---------------------------------- | ------------------------------------ | ------------------------------------------ |
| **Swarm topology explicitly selected**     | **Mandatory**                      | ✅✅ **the graph _is_ the topology** | `02 §4`, `06 §2`                           |
| Task decomposition specified               | Mandatory                          | ⚠️ nodes imply it                    | 🔧 Document it as a table. `03 §2`         |
| Context Handoff Protocol implemented       | Mandatory                          | ⚠️ `Command` carries it              | 🔧 Tier discipline. `06 §4.3`              |
| Agent roles non-overlapping                | Required                           | ❌                                   | 🔧 Design review; record the overlap check |
| Supervisor defined for hierarchical swarms | Required                           | ✅ supervisor node                   | `06 §4.2`                                  |
| Git worktree isolation for parallel dev    | Required when parallel coding      | ❌                                   | 🔧 Workspace convention — `05 §2`          |
| Merge integration agent designated         | Required when parallel development | ❌                                   | 🔧 Workspace convention. No self-merge.    |
| Anti-patterns prohibited in agent prompts  | Required                           | ❌                                   | 🔧 Forbidden-behaviours section            |

**Declarative topology is LangGraph's second unambiguous win.** `swarm_orchestrator.py` _describes_ a
topology; a `StateGraph` _is_ one. A description can drift from the implementation. The graph cannot,
because it is the implementation.

### Cross-layer

| Requirement                         | Closed by                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------------- |
| Agent → Agent handoff content match | `HandoffPacket.validate()` fails a mis-tiered packet at construction          |
| Canonical source of truth           | 🔧 The stale 0.x refs in `retrieval-augmented-generation/` violate this today |

---

## Part 3 — Adoption gate

If LangChain adoption is authorised, these are the checks. Every one is objectively verifiable, and
**every Mandatory row must pass before anything reaches production** — that is what "Mandatory"
means in the standard.

### Blocking (Mandatory — a failure here is Non-Compliant)

- [ ] Agent state is a typed schema with all four slots present as fields
- [ ] `ContextAssembler` runs before every model dispatch, and is the innermost message rewriter
- [ ] Slot priority order is documented in the state schema and enforced by the assembler
- [ ] Every model call has an explicit timeout
- [ ] Error handling distinguishes Timeout / RateLimit / Validation with distinct paths — no catch-all
- [ ] Rate-limit retry uses exponential backoff **with jitter**
- [ ] A token budget monitor can stop the run
- [ ] Every agent's system prompt defines a bounded role — not "helpful assistant"
- [ ] Any output consumed downstream is schema-constrained
- [ ] Multi-agent topology is declared and reviewed before implementation
- [ ] Every handoff names its tier

### Required (a failure here is Conditional, and needs a remediation plan)

- [ ] Tool whitelist enforced from `TOOL_REGISTRY`; per-task call caps set
- [ ] Irreversible operations gated behind `interrupt()` with a checkpointer attached
- [ ] PII scrubbed on input and scanned on output
- [ ] ACL filtering applied, with the role bound outside model control
- [ ] Reranking implemented ← **currently the open one**
- [ ] Forbidden-behaviours and escalation sections present in every agent prompt
- [ ] Role overlap checked and recorded
- [ ] Observability decided and wired before build

### Workspace-specific

- [ ] All LangChain-family packages pinned exactly; CVE floors met
- [ ] No `LANGSMITH_*` / `LANGCHAIN_TRACING_V2` anywhere
- [ ] MCP tool-name collisions resolved; write-capable MCP tools excluded or gated
- [ ] `thread_id` derived from an authenticated session
- [ ] `FilesystemBackend.root_dir` (if used) points at a disposable directory
- [ ] Stale 0.x references in `retrieval-augmented-generation/` corrected — **do this regardless of the decision**

---

## Part 4 — Anti-pattern master list

Consolidated from `01`–`06`. Ranked by how much damage the mistake does.

| Rank | Anti-pattern                                                    | Consequence                                                                                        |
| ---- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| 1    | Bare `create_agent` in production                               | Three L2 Mandatory + four L3 Mandatory unmet → **Non-Compliant**                                   |
| 2    | `user_role` as a tool parameter                                 | Prompt injection escalates to privilege escalation                                                 |
| 3    | `FilesystemBackend(root_dir=<repo root>)`                       | Agent can rewrite the governance documents constraining it                                         |
| 4    | `FilesystemBackend(root_dir=...)` without `virtual_mode=True`\* | `root_dir` does not confine anything — a `..` path segment or an absolute path escapes it entirely |
| 5    | Replacing CC-00 RAG with LangChain RAG                          | Trades an ASGF asset (ACL filtering) for a Required gap                                            |
| 6    | User input reaching `get_state_history(filter=…)`               | The literal CVE-2025-67644 precondition                                                            |
| 7    | Treating empty retrieval as absence of evidence                 | Confident wrong answers, invisible in logs                                                         |
| 8    | Undeclared / general-purpose-only subagents                     | Emergent topology — L5 Mandatory failure                                                           |
| 9    | Unpinned `langchain*` packages                                  | Drift into an incompatible or vulnerable combination                                               |
| 10   | Message-rewriting middleware after the assembler                | Silently destroys the four-slot guarantee                                                          |
| 11   | `interrupt_on` without a checkpointer                           | The approval gate silently does nothing                                                            |
| 12   | Approval UI that hides tool arguments                           | Rubber stamp; not a control                                                                        |
| 13   | Local 8B model driving tool calls                               | Malformed calls, retry storms, silent wrong answers                                                |
| 14   | Following any tutorial dated 2023–2024                          | Teaches an API that no longer resolves                                                             |
| 15   | Adopting LangServe                                              | Archived 2026-05-05                                                                                |
| 16   | Retry policy on both client and middleware                      | Retry budgets multiply                                                                             |

\* **Rank 4 is the one row in this table verified by execution, not projected.** Found and
reproduced 2026-07-27 via `workspace-integration-examples/verification/tests/test_03_deepagents_examples.py::test_filesystem_backend_virtual_mode_false_allows_path_escape`; fixed in both
`03-deepagents-examples.md` and `cookbook/03-deepagents.md` the same day.

---

**Document status:** Practice catalogue and compliance map. Projections, not an audit.
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-26
