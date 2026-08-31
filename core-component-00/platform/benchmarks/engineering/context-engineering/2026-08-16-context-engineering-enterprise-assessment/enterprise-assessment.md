# Enterprise-Level Engineering Assessment — Context Engineering (Layer 2)

---

## Metadata

| Field                           | Value                                                                       |
| ------------------------------- | --------------------------------------------------------------------------- |
| **Assessment ID**               | `2026-08-16-context-engineering-enterprise-assessment`                      |
| **Date**                        | 2026-08-16                                                                  |
| **Assessor**                    | Mei-Ling Zhao (Senior Research Engineer — Context Engineering, module lead) |
| **Reviewer**                    | Dr. Elias Vance (Laboratory Director) — reviewed 2026-08-16                 |
| **Module(s) / System Assessed** | `core-component-00/framework/02-context-engineering/`                        |
| **Requestor**                   | CEO, via user                                                               |
| **Prior Assessment**            | None — first pass                                                           |

**Reviewer requirement.** Dr. Vance has completed the excerpt-to-claim check specified in the
template (see Metadata) — this document is signed off and citable. Every external excerpt in the
Source Register below was copied out of a page fetched this session, and every internal excerpt
was copied out of a file opened this session; the Reviewer independently confirmed both rather
than taking that statement on trust.

---

## Research Freshness (Mandatory)

**Knowledge cutoff of assessor:** January 2026 — no claim below is sourced from training data.
Every external row was retrieved by fetching the page itself this session, not from a search-result
snippet; every internal row was read out of the working tree this session. Nothing carries
`[Knowledge Cutoff - verify]`.

**Live research performed this session:** Yes

### Source Register

#### External sources

| ID  | Claim Supported                                                                                               | Query Run                                                                                            | Source                                                                                                                                         | Retrieval Date | Verbatim Excerpt                                                                                                                                                                                                                                                                        | Status                                        |
| --- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| S1  | Production memory products advertise token reduction "up to 80%", framed as fidelity-preserving               | "enterprise context engineering LLM agents best practices 2026"                                      | [Context Engineering AI: How To Build Smarter LLM Agents In 2026](https://mem0.ai/blog/context-engineering-ai-agents-guide)                    | 2026-08-16     | "Mem0's memory compression engine intelligently distills conversations into optimized representations, cutting token usage by up to 80% while preserving fidelity."                                                                                                                     | Verified — excerpt supports claim             |
| S2  | Turn count is used as a practical signal that compression is due                                              | "enterprise context engineering LLM agents best practices 2026"                                      | [Context Engineering AI: How To Build Smarter LLM Agents In 2026](https://mem0.ai/blog/context-engineering-ai-agents-guide)                    | 2026-08-16     | "If you're seeing degraded performance after 10 to 15 conversation turns or spending a lot of budget on tokens, compression can reduce usage while preserving conversation quality."                                                                                                    | Verified — excerpt supports claim             |
| S3  | Working memory carries an explicit percentage-of-window budget in the tiered model                            | "context engineering production AI agents memory compression token budget enforcement 2026"          | [Agent Memory Compression and State Budget Management](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/) | 2026-08-16     | "Tier 1: Working Memory (Always In-Context)" containing "full, unmodified, lossless content" with "Budget: typically 10–15% of the context window."                                                                                                                                     | Verified — excerpt supports claim             |
| S4  | Enterprise practice assigns a fixed percentage allocation per context category                                | "context engineering production AI agents memory compression token budget enforcement 2026"          | [Agent Memory Compression and State Budget Management](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/) | 2026-08-16     | System instructions "10–15%"; Tool schemas "15–20%"; Retrieved context (RAG) "30–40%"; Conversation history "Remainder"                                                                                                                                                                 | Verified — excerpt supports claim             |
| S5  | Bitemporal annotation is the field's contradiction-handling mechanism                                         | "context engineering production AI agents memory compression token budget enforcement 2026"          | [Agent Memory Compression and State Budget Management](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/) | 2026-08-16     | "Each relationship carries both event time and ingestion time (bitemporal annotation), allowing precise handling of contradictions without information loss."                                                                                                                           | Verified — excerpt supports claim             |
| S6  | An immutable raw log is expected to survive aggressive compression                                            | "context engineering production AI agents memory compression token budget enforcement 2026"          | [Agent Memory Compression and State Budget Management](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/) | 2026-08-16     | "Preserve the raw log. Even aggressive compression of the working state should leave an immutable record somewhere — session logs, git history, or archival files."                                                                                                                     | Verified — excerpt supports claim             |
| S7  | Retention scoring is expected to be multi-signal, including a tool-outcome-derived weight                     | "context engineering production AI agents memory compression token budget enforcement 2026"          | [Agent Memory Compression and State Budget Management](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/) | 2026-08-16     | "Recency, frequency of access, task relevance, a cognitive weight signal derived from tool-execution outcomes (did using this memory lead to successful tool calls?), and a PPO-learned policy weight."                                                                                 | Verified — excerpt supports claim             |
| S8  | Budget overflow triggers an automatic consolidation pass, in code                                             | "context engineering production AI agents memory compression token budget enforcement 2026"          | [Agent Memory Compression and State Budget Management](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/) | 2026-08-16     | "When Tier 1 (working memory) exceeds its budget, trigger a consolidation pass that archives completed items and compresses verbose entries." / "Before incorporating any new observation, the agent checks remaining capacity and decides whether to compress existing history first." | Verified — excerpt supports claim             |
| S9  | A published compression-ratio-vs-fidelity baseline exists to benchmark against                                | "context engineering production AI agents memory compression token budget enforcement 2026"          | [Agent Memory Compression and State Budget Management](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/) | 2026-08-16     | "At 2–3x compression, accuracy loss is typically under 1.5% on reasoning benchmarks."                                                                                                                                                                                                   | Verified — excerpt supports claim             |
| S10 | The recommended compaction trigger is ≈70–75% of the window, explicitly not 95–98%                            | "agent context compaction triggered at percentage of context window utilization threshold"           | [Agent Context Compaction for Long-Running Sessions](https://zylos.ai/research/2026-04-21-agent-context-compaction-long-running-sessions/)     | 2026-08-16     | "Set compaction threshold at ≈70–75% of the context window, not 95–98%." / "Triggering compaction early (at 150K tokens for a 200K window) gives the model adequate output tokens to write a high-quality summary."                                                                     | Verified — excerpt supports claim             |
| S11 | A shipped agent framework exposes the trigger as a configurable utilization fraction                          | "agent context compaction triggered at percentage of context window utilization threshold"           | [Compaction — Inspect AI](https://inspect.aisi.org.uk/compaction.html)                                                                         | 2026-08-16     | "The default threshold is `0.9` (90% of the context window)."                                                                                                                                                                                                                           | Verified — excerpt supports claim             |
| S12 | Model reliability degrades with input length before the advertised limit is reached                           | "Chroma context rot research long context degradation input length"                                  | [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://www.trychroma.com/research/context-rot)                             | 2026-08-16     | "models do not use their context uniformly; instead, their performance grows increasingly unreliable as input length grows." / "even under these minimal conditions, model performance degrades as input length increases, often in surprising and non-uniform ways."                   | Verified — excerpt supports claim             |
| S13 | A peer-reviewable compression benchmark reports a specific peak-token reduction band                          | `"context compression" "60%" "without information loss" LLM agent`                                   | [ACON: Optimizing Context Compression for Long-horizon LLM Agents](https://arxiv.org/abs/2510.00615)                                           | 2026-08-16     | "ACON reduces peak token usage by 26-54% while improving task success over existing compression baselines."                                                                                                                                                                             | Verified — excerpt supports claim             |
| S14 | Sub-agents return a size-bounded condensed summary, not their working context                                 | "LangGraph AutoGen multi-agent handoff context passing subagent context isolation 2026"              | [Effective Context Engineering for AI Agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)   | 2026-08-16     | "Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)."                                                                                                           | Verified — excerpt supports claim             |
| S15 | Compaction is defined by proximity to the window limit, not by transcript size on disk                        | "LangGraph AutoGen multi-agent handoff context passing subagent context isolation 2026"              | [Effective Context Engineering for AI Agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)   | 2026-08-16     | "Compaction is the practice of taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary."                                                                                                               | Verified — excerpt supports claim             |
| S16 | Compaction firing "once the window begins to fill" is described as typical production practice                | "context engineering production AI agents memory compression token budget enforcement 2026"          | [Context Engineering: A Practical Guide for AI Agents — Sourcegraph](https://sourcegraph.com/blog/context-engineering)                         | 2026-08-16     | "Production memory systems typically maintain both, with a compaction step that condenses older turns into a summary once the window begins to fill."                                                                                                                                   | Verified — excerpt supports claim             |
| S17 | Budget-setting plus alert-on-exceed is itself a named practice — the alerting half of enforcement             | "context engineering production AI agents memory compression token budget enforcement 2026"          | [Context Engineering: A Practical Guide for AI Agents — Sourcegraph](https://sourcegraph.com/blog/context-engineering)                         | 2026-08-16     | "setting budgets, and alerting when an agent class regularly exceeds them."                                                                                                                                                                                                             | Verified — excerpt supports claim             |
| S18 | Enterprise context governance is an access-control concern, sited at the retrieval/catalog layer              | "enterprise context engineering LLM agents best practices 2026"                                      | [How to Build Context for LLMs in Enterprise (5-Layer Guide)](https://atlan.com/know/how-to-build-context-for-llms-enterprise/)                | 2026-08-16     | "RBAC policies that govern human access to data should also govern LLM and agent access to context" / "Agents and LLMs are assigned identities with scoped permissions. A Finance LLM gets the same catalog access a Finance analyst would have"                                        | Verified — supports the scope exclusion below |
| S19 | _Sought:_ an external source stating context compression achieves ~60% reduction **without information loss** | `"context compression" "60%" "without information loss" LLM agent`                                   | —                                                                                                                                              | 2026-08-16     | —                                                                                                                                                                                                                                                                                       | Searched — no supporting source found         |
| S20 | _Sought:_ an external source establishing doc-to-code parity as an enforced enterprise CI gate                | "enterprise practice CI gate documentation code parity drift enforcement LLM framework repositories" | —                                                                                                                                              | 2026-08-16     | —                                                                                                                                                                                                                                                                                       | Searched — no supporting source found         |
| S21 | _Sought:_ staged pressure thresholds (70/80/85/90/99%) for progressive context eviction                       | "agent context compaction triggered at percentage of context window utilization threshold"           | [Beyond Compaction: Structured Context Eviction for Long-Horizon Agents](https://arxiv.org/pdf/2606.11213)                                     | 2026-08-16     | —                                                                                                                                                                                                                                                                                       | Searched — no supporting source found         |

**Note on S19.** This search was run specifically to test a figure that seemed plausible from
memory. Nothing found supports it. The nearest real figures are S1 ("up to 80% while preserving
fidelity" — a vendor claim about its own product, and "preserving fidelity" is not "without
information loss"), S13 (26–54% peak-token reduction), and S9 (2–3× compression at <1.5% accuracy
loss). The claim is therefore not made anywhere in this document; the sourced figures are used
instead, attributed to the sources that actually contain them.

**Note on S21.** The PDF was fetched but its text layer did not extract into readable prose, so no
passage could be quoted. Logged as a negative result rather than cited from the search snippet
that surfaced it — a snippet is not a verified excerpt.

#### Internal sources

| ID  | Claim Supported                                                                  | Query Run        | Source                                                                                 | Retrieval Date | Verbatim Excerpt                                                                                                                                                                                                                       | Status                                     |
| --- | -------------------------------------------------------------------------------- | ---------------- | -------------------------------------------------------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| I1  | We define percentage slot budgets, task-aware, in code                           | [n/a — internal] | `implementations/context_assembler.py:41-48`                                           | 2026-08-16     | `BUDGET_PROFILES: Dict[str, Dict[str, float]] = {` … `"factual_qa": {"system": 0.10, "retrieved": 0.65, "history": 0.10, "tools": 0.15},` … `"code_generation": {"system": 0.15, "retrieved": 0.45, "history": 0.20, "tools": 0.20,},` | Internal — verified against primary source |
| I2  | Our only in-code window-utilization constant is an assembly-time headroom cap    | [n/a — internal] | `implementations/context_assembler.py:148`                                             | 2026-08-16     | `SAFETY_BUFFER = 0.90  # Never use more than 90% of the context window`                                                                                                                                                                | Internal — verified against primary source |
| I3  | Assembly-time item selection is multi-signal                                     | [n/a — internal] | `implementations/context_assembler.py:97-99`                                           | 2026-08-16     | `return (self.relevance * 0.5) + (self.recency * 0.3) + (self.importance * 0.2)`                                                                                                                                                       | Internal — verified against primary source |
| I4  | Compression is caller-driven by a target, with no utilization trigger of its own | [n/a — internal] | `implementations/context_compressor.py:160-167`                                        | 2026-08-16     | `if original_tokens <= target_tokens:` … `strategy="no_compression_needed",`                                                                                                                                                           | Internal — verified against primary source |
| I5  | Compression tiering is positional, not signal-driven                             | [n/a — internal] | `implementations/context_compressor.py:405, 426-428`                                   | 2026-08-16     | `"""Split turns into equal-sized tiers (oldest first)."""` … `if level == "paragraph":` `# Keep first 300 chars as a paragraph summary` `return combined[:300] + ("..." if len(combined) > 300 else "")`                               | Internal — verified against primary source |
| I6  | A compression-ratio metric exists as a property but is not asserted anywhere     | [n/a — internal] | `implementations/context_compressor.py:87-91`                                          | 2026-08-16     | `@property` `def compression_ratio(self) -> float:` … `return 1.0 - (self.compressed_tokens / self.original_tokens)`                                                                                                                   | Internal — verified against primary source |
| I7  | H-CE01 is advisory by construction and never blocks a turn                       | [n/a — internal] | `.claude/hooks/context-budget-alert.py:8-10`                                           | 2026-08-16     | `# to a single stdlib-only Python 3 implementation. This is a purely advisory` `# UserPromptSubmit hook (it never denies/blocks a turn) — every code path below` `# terminates with exit 0`                                            | Internal — verified against primary source |
| I8  | H-CE01's trigger is transcript file size, not context utilization                | [n/a — internal] | `.claude/hooks/context-budget-alert.py:54-55`                                          | 2026-08-16     | `size_kb = (size_bytes + 512) // 1024` `threshold_kb = 500`                                                                                                                                                                            | Internal — verified against primary source |
| I9  | The harness token monitor explicitly disclaims the Claude Code session surface   | [n/a — internal] | `engineering/harness-engineering/implementations/context_monitor.py:9-12`              | 2026-08-16     | `This module does NOT manage Claude Code session context. Session-level token` `pressure is handled by the context-budget-alert.ps1 hook and the /context` `command at the Claude Code session layer.`                                 | Internal — verified against primary source |
| I10 | Memory retention already weights recency, importance, and access frequency       | [n/a — internal] | `implementations/memory_maintenance.py:87-88`                                          | 2026-08-16     | `decay_weight(t) = importance * e^(-delta_t / strength)` `strength = base_strength * (1 + access_count * reinforcement_factor)`                                                                                                        | Internal — verified against primary source |
| I11 | The contradiction check is built and unconditionally refused                     | [n/a — internal] | `implementations/memory_maintenance.py:305-306`                                        | 2026-08-16     | `The contradiction check (check_contradiction()) is refused unconditionally` `and cannot be enabled by any caller.`                                                                                                                    | Internal — verified against primary source |
| I12 | Our memory record carries one time axis, not two                                 | [n/a — internal] | `implementations/memory_vector_store.py:293`                                           | 2026-08-16     | `created_at: float`                                                                                                                                                                                                                    | Internal — verified against primary source |
| I13 | The JSONL log is the durable source of truth; Qdrant is a derived index          | [n/a — internal] | `implementations/memory_vector_store.py:5-8`                                           | 2026-08-16     | `durable, human-readable JSONL log (the source of truth); the Qdrant collection` `is a derived, rebuildable semantic index over that log`                                                                                              | Internal — verified against primary source |
| I14 | A fifth memory type exists in code beyond the four documented                    | [n/a — internal] | `implementations/memory_store.py:621`                                                  | 2026-08-16     | `class ReflectionMemory:`                                                                                                                                                                                                              | Internal — verified against primary source |
| I15 | Handoff budgets the sub-agent's input; nothing budgets its return                | [n/a — internal] | `implementations/context_assembler.py:369-370, 382`                                    | 2026-08-16     | `return_schema: Optional[Dict] = None,` `subagent_budget: int = 32_000,` … `subagent_budget: Token budget allocated to the subagent.`                                                                                                  | Internal — verified against primary source |
| I16 | Three handoff tiers are specified and tier-selected by an explicit matrix        | [n/a — internal] | `patterns/multi-agent-handoff.md:16, 36, 61, 79`                                       | 2026-08-16     | `### Tier 1: Full Handoff` / `### Tier 2: Scoped Handoff` / `### Tier 3: Minimal Handoff` / `### Tier Selection Matrix`                                                                                                                | Internal — verified against primary source |
| I17 | Module docs describe three implementation files; seven exist                     | [n/a — internal] | `README.md:30-32` and `README.md:113`                                                  | 2026-08-16     | `                                                                                                                                                                                                                                      | implementations/context_assembler.py       | Production context assembly engine | `…` | README.md | 1.0 | 2026-04-28 | `   | Internal — verified against primary source |
| I18 | Live test-suite state, run this session                                          | [n/a — internal] | `pytest engineering/context-engineering/testing/ -q`                                   | 2026-08-16     | `1 failed, 326 passed, 1 skipped in 9.99s` / `AssertionError: ContextCompressor did not reduce tokens for coding_session` / `assert 1236 < 909`                                                                                        | Internal — verified against primary source |
| I19 | The failing benchmark and the compressor count tokens differently                | [n/a — internal] | `testing/test_acon_benchmark.py:91` vs `implementations/context_compressor.py:155-158` | 2026-08-16     | Test: `original_tokens = sum(_estimate_tokens(t["content"]) for t in turns)` — Compressor: `original_text = "\n".join(f"[{t.get('role', 'user')}]: {t.get('content', '')}" for t in turns)`                                            | Internal — verified against primary source |

**Internal-source discipline note.** `context_compressor.py:21` declares
`COMPACTION_API_VERSION = "compact_20260112"` and the module wraps an Anthropic beta Compaction
API. Per the template's Internal-Source Verification clause, our file saying so establishes only
that our file says so — it is not evidence about the external API's behaviour or availability, so
no Enterprise-Standard Practice claim in this document rests on it. The external compaction claims
below rest on S15/S16/S10/S11 instead.

---

## Assessment Scope

### What Was Assessed

The Context Engineering module's seven production implementations (`context_assembler.py`,
`memory_store.py`, `context_compressor.py`, `memory_vector_store.py`, `memory_maintenance.py`,
`production_judge.py`, `reflection_authoring.py`), its `patterns/` and `fundamentals/` docs, its
pytest suite (run live this session), and its one cross-module runtime integration point,
`.claude/hooks/context-budget-alert.py` (H-CE01).

### Why Now

CEO-directed enterprise benchmark of the CC-00 stack, requested via the user, conducted in the
canonical layer order defined in `core-component-00/platform/benchmarks/CLAUDE.md` § Layer sequence.

### Out of Scope

- **Harness Engineering (Layer 3), RAG (Layer 4), Multi-Agent Engineering (Layer 5)** — each has
  its own assessment folder. Where a finding here has a Layer 3 owner (H-CE01 lives in
  `.claude/hooks/`), the remediation row names that owner rather than absorbing the work.
- **Context-source governance / RBAC.** S18 establishes this as a live enterprise dimension
  ("RBAC policies that govern human access to data should also govern LLM and agent access to
  context"), but it is sited at the catalog and retrieval layer. In CC-00 that is Layer 4's
  `retrieval.py` (ACL filtering), not Layer 2's assembly path. Benchmarking it here would flag a
  gap that a different layer already owns — the failure mode `benchmarks/CLAUDE.md` § Layer
  sequence warns against. Recorded here so the exclusion is deliberate and visible, not silent.
- **The `agent-memory` MCP server's deployment posture** — governed by
  `.claude/rules/mcp-governance.md`, not by a benchmark.

---

## Verdict Vocabulary (Binding)

This assessment uses the template's fixed vocabulary without additions: **Pass at parity**,
**Pass, ahead**, **Partial**, **Gap**, **N/A**, **Unassessed — no source**.

No row below is rated `Pass, ahead`. Two dimensions felt like candidates while writing — our
task-aware budget profiles (six profiles versus S4's single fixed table) and our refusal to ship
an unreviewed LLM contradiction judge. Neither is claimed, because in both cases I have no
external excerpt that positively establishes the comparison; I only have an absence of a
counterexample, which the template explicitly rules insufficient for that verdict. Both are
recorded at the verdict their evidence actually supports.

---

## Benchmark Table

| ID  | Dimension                                       | Our Current State                                                                                                                                                                                                                                                                                            | Internal Source ID(s) | Enterprise-Standard Practice                                                                                                                                                                   | External Source ID(s) | Verdict                | Severity |
| --- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ---------------------- | -------- |
| B1  | Per-slot percentage budget allocation           | Six task-aware profiles fix the fractional split across system / retrieved / history / tools, applied against a 90%-of-window usable ceiling                                                                                                                                                                 | I1, I2                | A fixed allocation table: system instructions "10–15%", tool schemas "15–20%", retrieved (RAG) "30–40%", conversation history the "Remainder"                                                  | S4                    | Pass at parity         | —        |
| B2  | Compaction trigger threshold                    | No utilization-based trigger exists. `SAFETY_BUFFER = 0.90` is an assembly-time headroom cap, not a compaction trigger; `compress_history()` acts only when the caller's `target_tokens` is already exceeded                                                                                                 | I2, I4                | Trigger at "≈70–75% of the context window, not 95–98%"; framework default exposed as `0.9`; compaction defined as acting on "a conversation nearing the context window limit"                  | S10, S11, S15, S12    | Gap                    | P1       |
| B3  | Runtime budget enforcement                      | H-CE01 is "a purely advisory UserPromptSubmit hook (it never denies/blocks a turn)" and fires on a 500 KB transcript-file-size proxy; nothing in the execution path calls `context_compressor.py`                                                                                                            | I7, I8, I9            | Two named practices: "setting budgets, and alerting when an agent class regularly exceeds them" **and** "When Tier 1 (working memory) exceeds its budget, trigger a consolidation pass"        | S17, S8, S16          | Partial                | P1       |
| B4  | Compression effectiveness metric                | `CompressionResult.compression_ratio` exists as a property but no test asserts a ratio floor or a fidelity bound; the one benchmark test that touches it is red (see B4 note)                                                                                                                                | I6, I18, I19          | Published, quotable baselines to benchmark against: "26-54%" peak-token reduction with improved task success; "At 2–3x compression, accuracy loss is typically under 1.5%"; vendor "up to 80%" | S13, S9, S1           | Gap                    | P1       |
| B5  | Memory-tier ↔ slot budget binding               | Four documented memory types plus an undocumented `ReflectionMemory`; none of the tiers carries a token-budget percentage, and the assembler's `history` slot is not wired to `memory_store.py`'s tiers                                                                                                      | I1, I14               | The tiered model assigns the working tier a budget directly: "Budget: typically 10–15% of the context window", lossless and always in-context                                                  | S3                    | Partial                | P2       |
| B6  | Multi-signal retention scoring                  | Recency, importance, and access frequency are all implemented — at assembly (`relevance*0.5 + recency*0.3 + importance*0.2`) and at maintenance (Ebbinghaus decay reinforced by `access_count`). The compressor consumes none of them; its tiering is positional and its summaries are character truncations | I3, I10, I5           | "Recency, frequency of access, task relevance, a cognitive weight signal derived from tool-execution outcomes … and a PPO-learned policy weight"                                               | S7                    | Partial                | P2       |
| B7  | Contradiction / stale-fact resolution           | `check_contradiction()` is built but "refused unconditionally and cannot be enabled by any caller"; `MemoryRecord` carries `created_at` / `last_accessed_at` — one time axis, no ingestion-time axis                                                                                                         | I11, I12              | "Each relationship carries both event time and ingestion time (bitemporal annotation), allowing precise handling of contradictions without information loss"                                   | S5                    | Gap                    | P2       |
| B8  | Durable raw-log preservation under compression  | The append-only JSONL log is "the source of truth"; the Qdrant collection is "a derived, rebuildable semantic index over that log"                                                                                                                                                                           | I13                   | "Preserve the raw log. Even aggressive compression of the working state should leave an immutable record somewhere — session logs, git history, or archival files."                            | S6                    | Pass at parity         | —        |
| B9  | Sub-agent context isolation and return contract | Three handoff tiers with an explicit selection matrix; `build_handoff()` budgets the sub-agent's **input** (`subagent_budget: int = 32_000`) and accepts a `return_schema`, but places no size bound on the return                                                                                           | I15, I16              | The sub-agent "returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)" — the return side is explicitly size-bounded                                                | S14                   | Partial                | P2       |
| B10 | Documentation–code parity as a CI gate          | `README.md` lists three implementation files and is stamped `1.0 / 2026-04-28`; seven implementation files exist                                                                                                                                                                                             | I17                   | —                                                                                                                                                                                              | S20                   | Unassessed — no source | —        |

**Note on B4.** The suite is `1 failed, 326 passed, 1 skipped`. The failure is
`test_acon_vs_context_compressor`, and the live output (`assert 1236 < 909`) makes the root cause
specific: the test measures `original_tokens` as the sum of per-turn `content` (909), while
`compress_history()` measures it over the role-prefixed joined transcript (1236) against a target
of 1500. The compressor's `no_compression_needed` return is therefore correct **by its own
accounting** — what is defective is that the two accountings differ and neither is contractual.
This is the same underlying gap the row records: there is no agreed compression metric to test
against. Stating it as "the compressor is buggy" would be a more dramatic finding and a less true
one.

**Note on B10.** I searched for an external source establishing doc-to-code parity as an enforced
enterprise CI gate and found none that could be quoted (S20). Rather than assert it as industry
practice with a hedge, the row is `Unassessed — no source` and carries no severity. The drift is
real and I am not disputing it — but "our README is stale relative to our own code" is an
internal-compliance finding, and per the template's own guidance it belongs to
`crew/director/elias-vance/skills/asgf-compliance-audit.md`, not to a benchmark. It is flagged
there rather than smuggled in here behind an unsourced claim about what mature teams do.

---

## Severity-Ordered Remediation Plan

**Declared scale for this assessment:** **Scale A — ASGF Gap Severity**
(`crew/director/elias-vance/skills/asgf-compliance-audit.md` § Gap Severity Classification). The
assessed surface is a CC-00 engineering module, not a shipping product surface, so Scale A governs
throughout and no row below mixes in Scale B.

| ID  | Priority | Benchmark Row | Gap                                                                                                     | Source ID(s)               | Owner                                              | Fix                                                                                                                                                                                                                                                                                              | Severity Justification                                                                                                                                                                                                                                                                             |
| --- | -------- | ------------- | ------------------------------------------------------------------------------------------------------- | -------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1  | P1       | B3            | Budget enforcement stops at the alert; no code path consolidates or compresses when the budget is hit   | S17, S8, S16, I7, I9       | Kwame Asante (harness owns H-CE01)                 | Add the enforcement half **inside the hook layer itself** — H-CE01 computes utilization and invokes compaction. Do **not** route this through `context_monitor.py`: that module states it "does NOT manage Claude Code session context" (I9) and is scoped to standalone Python LLM applications | ASGF — "Gap that will degrade output quality or reliability at scale but does not cause outages"; the host runtime still compacts the session, so no outage follows, but Sacred Context ordering is left to model self-application and degrades over long sessions. See P0 Boundary Analysis below |
| R2  | P1       | B2            | No utilization-based compaction trigger anywhere in the module                                          | S10, S11, S15, S12, I2, I4 | Mei-Ling Zhao                                      | Add an explicit utilization trigger to `ContextCompressor` (default in S10's ≈70–75% band, configurable as S11 does), separate from `SAFETY_BUFFER`, and document it in `fundamentals/context-window-anatomy.md`                                                                                 | ASGF — "Gap that will degrade output quality or reliability at scale but does not cause outages"; S12 establishes reliability decay before the limit is reached, which is quality degradation at scale, not an outage trigger                                                                      |
| R3  | P1       | B4            | No compression-ratio or fidelity metric is asserted; the one benchmark test is red on a metric mismatch | S13, S9, S1, I6, I18, I19  | Mei-Ling Zhao                                      | Define one contractual token-accounting basis, align `test_acon_benchmark.py` and `compress_history()` to it, then assert a ratio floor and a decision-continuity floor against the fixed long-session corpus. Cite S13/S9 as the external comparison band — not an unsourced round number       | ASGF — "Gap that will degrade output quality or reliability at scale but does not cause outages"; without an asserted fidelity bound, a regression that silently drops decision-critical turns ships undetected, degrading output quality without any outage signal                                |
| R4  | P2       | B5            | Memory tiers carry no token budget; the assembler's history slot is not bound to them                   | S3, I1, I14                | Hana Kobayashi                                     | Give each memory tier an explicit percentage-of-window budget (S3's 10–15% for working) and wire `memory_store.py`'s tiers to the assembler's `history` allocation so one number governs both                                                                                                    | ASGF — "Gap that reduces engineering maintainability or makes the system harder to extend"; two independent budget notions with no binding is a maintainability defect, not a runtime one — the assembler enforces its own split correctly today                                                   |
| R5  | P2       | B6            | The compressor consumes none of the retention signals the rest of the module already computes           | S7, I3, I10, I5            | Hana Kobayashi                                     | Have `_split_into_tiers`/`_summarise_tier` consume the existing `ContextItem.score` and `compute_decay_weight` signals instead of position; add S7's tool-execution-outcome cognitive weight as a new signal. The PPO-learned policy weight in S7 is out of scope for this fix                   | ASGF — "Gap that reduces engineering maintainability or makes the system harder to extend"; the signals exist and are correct, so this is wiring debt rather than a reliability defect — but it makes every future retention change require touching three files                                   |
| R6  | P2       | B9            | The handoff contract bounds the sub-agent's input but not its return                                    | S14, I15, I16              | Mei-Ling Zhao                                      | Add a `return_budget` alongside `return_schema` in `HandoffPacket`, defaulted into S14's 1,000–2,000 token band, and enforce it where handoff results are ingested                                                                                                                               | ASGF — "Gap that reduces engineering maintainability or makes the system harder to extend"; an unbounded return re-imports the context the tiering just isolated, which makes the tier abstraction leaky and harder to reason about as sub-agent count grows                                       |
| R7  | P2       | B7            | Contradiction handling is blocked behind a refused LLM judge; no bitemporal alternative exists          | S5, I11, I12               | Dr. Elias Vance (PI, Multi-Agent Memory Coherence) | Evaluate adding an ingestion-time axis to `MemoryRecord` alongside `created_at` (S5), which resolves contradictions without an LLM call in the loop — potentially unblocking the write path without lifting the adversarial-review gate at all                                                   | ASGF — "Gap that reduces engineering maintainability or makes the system harder to extend"; the refusal is currently a correct safety posture with no reliability cost, so this is an architecture-simplification opportunity rather than a quality or outage defect                               |

### P0 Boundary Analysis (R1)

R1 is the highest-severity finding in this document and the one that most invites a P0 rating, so
the boundary is argued rather than asserted.

**The case for P0.** ASGF P0 is "Gap that will cause production failure under normal load or after
extended sessions." The same skill file that defines the scale also names the Context Engineering
failure mode as "Degrades over long sessions as the context window fills with low-priority
content" — which is close to a verbatim description of an unenforced budget, and "after extended
sessions" is exactly the trigger the P0 wording calls out.

**Why it is P1 anyway.** The wording is "will cause production failure", and for the surface this
module actually runs on, it does not. Session-level token pressure on the assessed surface is
handled at the Claude Code host layer, not by this module — `context_monitor.py:9-12` states so
directly (I9), and S15's compaction is a host-runtime behaviour, not something our hook is the
last line of defence for. H-CE01 is an **additional** advisory layer stacked on top of a host that
already compacts; removing our layer does not remove compaction. There is also no identified load
or session-length trigger at which the advisory gap has produced a failure — the template's own
guidance is that "a design shortcoming that has never produced a failure and has no identified
load or session-length trigger is not 'will cause production failure' — it is P1 or P2." What the
gap does cause is that Sacred Context ordering is left to the model's own compliance with a text
reminder, so decision-critical content is not _guaranteed_ to survive host compaction. That is
"degrade output quality or reliability at scale but does not cause outages" — P1, as written.

**The condition this depends on, stated plainly.** This P1 holds _because_ a host runtime performs
compaction underneath us. If this module is embedded in a standalone Python LLM application with
no host-level compaction — which is precisely the deployment `context_monitor.py` says it _is_
scoped for — the same gap does meet the P0 wording, because nothing else would enforce the budget
and extended sessions would overflow the window. Any consumer taking Layer 2 outside the Claude
Code host should re-rate R1 as P0 for their deployment. I would rather write that condition down
than pick the softer number and stay quiet about what it rests on.

**What this changes about the verdict.** Under Scale A, "P0 and P1 gaps must be remediated before
the system is considered ASGF-compliant." R1 being P1 rather than P0 changes the urgency label, not
the obligation — it is still blocking for compliance, and it is still the first row in the plan.

---

## Compliance Verdict

**Conditional — P1 gaps open**

Against current external practice the module holds up structurally: per-slot percentage budgeting
(B1) and durable raw-log preservation under compression (B8) are at parity with what production
systems are documented as doing, and the retention signals external practice calls for are already
computed in two of the three places they belong (B6). The open P1s are all variations on one
theme — the module can compress, budget, and score, but nothing decides _when_ to do so: there is
no utilization trigger (B2), no enforcement path past the alert (B3), and no asserted metric that
would tell us whether a compression pass did its job (B4). Closing B2 and B3 together, in the hook
layer rather than through `context_monitor.py`, is the highest-value single move; B4 is what makes
the other two verifiable rather than merely present.

### Evidence Completeness Statement

Ten benchmark rows. Nine carry a `Verified` external source with a quoted excerpt; one (B10,
documentation–code parity) is `Unassessed — no source` and carries no severity, because the search
for an external source establishing doc-parity as an enforced CI gate returned nothing quotable
(S20).

Three searches were run and returned nothing usable, and all three are logged rather than dropped:
S19 (a ~60% compression-without-information-loss figure — no source found; the sourced figures
S13, S9 and S1 are used in its place, and no unsourced round number appears anywhere in this
document), S20 (above), and S21 (an arXiv PDF that fetched but did not yield extractable prose, so
nothing from it is cited — including the search snippet that surfaced it).

Dimensions I considered important but did not benchmark: context-source governance / RBAC, which
S18 confirms is a live enterprise dimension but which sits in Layer 4's ACL filtering rather than
Layer 2's assembly path (see Out of Scope); and CI discipline around the one red test, which is an
internal-compliance question rather than an external-benchmark one and is routed to the ASGF audit
skill instead. Both exclusions are deliberate and recorded so a reader can disagree with them.

The Reviewer named in Metadata (Dr. Elias Vance) has completed the excerpt-to-claim check. This
document is signed off under the template's Reviewer requirement and is citable and eligible for
the index in `benchmarks/README.md`.

---

## Sources

- **S1** — [Context Engineering AI: How To Build Smarter LLM Agents In 2026](https://mem0.ai/blog/context-engineering-ai-agents-guide)
- **S2** — [Context Engineering AI: How To Build Smarter LLM Agents In 2026](https://mem0.ai/blog/context-engineering-ai-agents-guide)
- **S3** — [Agent Memory Compression and State Budget Management for Long-Running Autonomous Systems](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/)
- **S4** — [Agent Memory Compression and State Budget Management for Long-Running Autonomous Systems](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/)
- **S5** — [Agent Memory Compression and State Budget Management for Long-Running Autonomous Systems](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/)
- **S6** — [Agent Memory Compression and State Budget Management for Long-Running Autonomous Systems](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/)
- **S7** — [Agent Memory Compression and State Budget Management for Long-Running Autonomous Systems](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/)
- **S8** — [Agent Memory Compression and State Budget Management for Long-Running Autonomous Systems](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/)
- **S9** — [Agent Memory Compression and State Budget Management for Long-Running Autonomous Systems](https://zylos.ai/research/2026-06-30-agent-memory-compression-state-budget-management/)
- **S10** — [Agent Context Compaction for Long-Running Sessions: Techniques and Tradeoffs](https://zylos.ai/research/2026-04-21-agent-context-compaction-long-running-sessions/)
- **S11** — [Compaction — Inspect AI](https://inspect.aisi.org.uk/compaction.html)
- **S12** — [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://www.trychroma.com/research/context-rot)
- **S13** — [ACON: Optimizing Context Compression for Long-horizon LLM Agents](https://arxiv.org/abs/2510.00615)
- **S14** — [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **S15** — [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **S16** — [Context Engineering: A Practical Guide for AI Agents](https://sourcegraph.com/blog/context-engineering)
- **S17** — [Context Engineering: A Practical Guide for AI Agents](https://sourcegraph.com/blog/context-engineering)
- **S18** — [How to Build Context for LLMs in Enterprise (5-Layer Guide)](https://atlan.com/know/how-to-build-context-for-llms-enterprise/)
- **S19** — _Searched, no supporting source found: `"context compression" "60%" "without information loss" LLM agent`_
- **S20** — _Searched, no supporting source found: "enterprise practice CI gate documentation code parity drift enforcement LLM framework repositories"_
- **S21** — _Searched, no supporting source found (page fetched, text layer not extractable, nothing quotable):_ [Beyond Compaction: Structured Context Eviction for Long-Horizon Agents](https://arxiv.org/pdf/2606.11213)
- **I1** — `core-component-00/framework/02-context-engineering/implementations/context_assembler.py:41-48`
- **I2** — `core-component-00/framework/02-context-engineering/implementations/context_assembler.py:148`
- **I3** — `core-component-00/framework/02-context-engineering/implementations/context_assembler.py:97-99`
- **I4** — `core-component-00/framework/02-context-engineering/implementations/context_compressor.py:160-167`
- **I5** — `core-component-00/framework/02-context-engineering/implementations/context_compressor.py:405, 426-428`
- **I6** — `core-component-00/framework/02-context-engineering/implementations/context_compressor.py:87-91`
- **I7** — `.claude/hooks/context-budget-alert.py:8-10`
- **I8** — `.claude/hooks/context-budget-alert.py:54-55`
- **I9** — `core-component-00/framework/03-harness-engineering/implementations/context_monitor.py:9-12`
- **I10** — `core-component-00/framework/02-context-engineering/implementations/memory_maintenance.py:87-88`
- **I11** — `core-component-00/framework/02-context-engineering/implementations/memory_maintenance.py:305-306`
- **I12** — `core-component-00/framework/02-context-engineering/implementations/memory_vector_store.py:293`
- **I13** — `core-component-00/framework/02-context-engineering/implementations/memory_vector_store.py:5-8`
- **I14** — `core-component-00/framework/02-context-engineering/implementations/memory_store.py:621`
- **I15** — `core-component-00/framework/02-context-engineering/implementations/context_assembler.py:369-370, 382`
- **I16** — `core-component-00/framework/02-context-engineering/patterns/multi-agent-handoff.md:16, 36, 61, 79`
- **I17** — `core-component-00/framework/02-context-engineering/README.md:30-32, 113`
- **I18** — Live run: `pytest engineering/context-engineering/testing/ -q` (2026-08-16)
- **I19** — `core-component-00/framework/02-context-engineering/testing/test_acon_benchmark.py:91` and `implementations/context_compressor.py:155-158`

---

## Version History

| Version | Date       | Author        | Changes                       |
| ------- | ---------- | ------------- | ----------------------------- |
| 1.0     | 2026-08-16 | Mei-Ling Zhao | Initial enterprise assessment |

---

**Template Version:** 1.0
**Last Updated:** 2026-08-16
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
