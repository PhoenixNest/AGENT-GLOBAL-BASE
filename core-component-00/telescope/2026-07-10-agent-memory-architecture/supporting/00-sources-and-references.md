# Archive No. 0 — Sources and References Consulted

> **Core Component 00 — Cross-Module Programme (Context Engineering × Retrieval-Augmented Generation)**
> **Parent Report:** `../research-report.md`
> **Audience:** CEO and anyone auditing the factual basis of this investigation.
> **Last Updated:** 2026-07-10
> **Scope:** Every external source (research paper, official documentation, official product
> website, or third-party technical write-up) consulted during this investigation, plus the
> internal workspace documentation used to ground the design. All external sources were retrieved
> via live web search on **2026-07-10** by a dedicated research subagent (see
> `research-report.md` § Methodology) — none are drawn solely from this investigator's training
> data. No source below was invented for this list; each one is already cited inline in
> `research-report.md` and/or `03-forgetting-strategy.md`.

---

## 1. Anthropic / Claude — Primary Benchmark Sources

| #   | Source                                                                                               | URL                                                                                                                 |
| --- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 1   | Claude Developer Platform — Memory tool docs (`memory_20250818`)                                     | https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool                                           |
| 2   | Claude Developer Platform — Context editing docs (`clear_tool_uses_20250919`)                        | https://platform.claude.com/docs/en/build-with-claude/context-editing                                               |
| 3   | Anthropic — "Bringing memory to teams"                                                               | https://www.anthropic.com/news/memory                                                                               |
| 4   | Anthropic Engineering — "Effective context engineering for AI agents" (2025-09-29)                   | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents                                   |
| 5   | Claude Help Center — "Use Claude's chat search and memory to build on previous context"              | https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context    |
| 6   | Claude Support — "Use incognito chats"                                                               | https://support.claude.com/en/articles/12260368-use-incognito-chats                                                 |
| 7   | Apito.ai — "Claude Memory Tool Guide" (developer guide)                                              | https://apito.ai/en/blog/dev-guides/claude-memory-tool-guide/                                                       |
| 8   | Skywork.ai — "Claude Memory: A Deep Dive Into Anthropic's Persistent Context Solution"               | https://skywork.ai/blog/claude-memory-a-deep-dive-into-anthropics-persistent-context-solution/                      |
| 9   | inkeybit — "Claude Projects: Complete Guide"                                                         | https://www.inkeybit.com/blog/claude-projects-complete-guide                                                        |
| 10  | Sider.ai — "How to Use Claude's Incognito Chats & Memory Controls to Protect Sensitive Info"         | https://sider.ai/blog/ai-tools/how-to-use-claude-s-incognito-chats-memory-controls-to-protect-sensitive-info        |
| 11  | VentureBeat — "Anthropic Adds Memory to Claude Team and Enterprise, Incognito for All"               | https://venturebeat.com/ai/anthropic-adds-memory-to-claude-team-and-enterprise-incognito-for-all                    |
| 12  | Caucasus Business Journal — "Claude Memory APIs Developer Guide 2026"                                | https://caucasusbusinessjournal.com/news/claude-memory-apis-developer-guide-2026                                    |
| 13  | EdTech Innovation Hub — "Anthropic Brings Persistent Memory to Claude Managed Agents in Public Beta" | https://www.edtechinnovationhub.com/news/anthropic-brings-persistent-memory-to-claude-managed-agents-in-public-beta |
| 14  | a2a-mcp.org — Memory MCP server entry (reference knowledge-graph MCP implementation)                 | https://a2a-mcp.org/entry/memory-mcp                                                                                |
| 15  | Model Context Protocol — Example Servers                                                             | https://modelcontextprotocol.io/examples                                                                            |

**Used for:** `research-report.md` § Finding 1 (Anthropic's file-based, non-vector memory architecture and its deliberate divergence from this design); `03-forgetting-strategy.md` §1 (the "periodically expire unaccessed memory files" guidance) and §2 (the "context rot" / attention-budget framing).

---

## 2. Comparator Top-Tier Agent Memory Architectures

| #   | Source                                                                                  | URL                                                               |
| --- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| 16  | Letta Docs — MemGPT architecture (core/recall/archival memory)                          | https://docs.letta.com/letta-memgpt                               |
| 17  | Leonie Monigatti — MemGPT architecture summary                                          | https://www.leoniemonigatti.com/blog/memgpt.html                  |
| 18  | Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (2023, ar5iv) | https://ar5iv.labs.arxiv.org/html/2304.03442                      |
| 19  | Dwarves Memo — Mem0 architecture breakdown                                              | https://memo.d.foundation/breakdown/mem0                          |
| 20  | DeepWiki — Mem0 Graph Memory                                                            | https://deepwiki.com/mem0ai/mem0/4-graph-memory                   |
| 21  | Mem0 — "Long-Term Memory for AI Agents" (blog)                                          | https://mem0.ai/blog/long-term-memory-ai-agents                   |
| 22  | Graphiti (GitHub) — temporal knowledge graph engine underlying Zep                      | https://github.com/getzep/graphiti                                |
| 23  | Zep — temporal knowledge graph paper (arXiv:2501.13956)                                 | https://arxiv.org/html/2501.13956v1                               |
| 24  | Zep — "Temporal Knowledge Graph" (product page)                                         | https://www.getzep.com/ai-agents/temporal-knowledge-graph/        |
| 25  | Neo4j Developer Blog — "Graphiti: Knowledge Graph Memory for a Post-RAG Agentic World"  | https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/ |
| 26  | LangChain Docs — Memory overview (short-term/long-term, semantic/episodic/procedural)   | https://docs.langchain.com/oss/python/concepts/memory             |
| 27  | Patronus AI — "Agentic Memory"                                                          | https://www.patronus.ai/ai-agent-development/agentic-memory       |
| 28  | LangChain — "LangMem SDK Launch" (blog)                                                 | https://www.langchain.com/blog/langmem-sdk-launch                 |

**Used for:** `research-report.md` § Finding 2 (importance/salience-weighted retention across every surveyed architecture) and § Finding 4 (Zep/Graphiti's bi-temporal fact invalidation); `03-forgetting-strategy.md` §3 (Generative Agents' recency/importance/relevance scoring), §4 (Generative Agents' reflection mechanism), and §5 (Mem0's ADD/UPDATE/DELETE/NOOP consolidation decision, Zep's fact invalidation).

---

## 3. Human Memory Science — Forgetting Strategy Grounding

| #   | Source                                                                                      | URL                                                                                                             |
| --- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 29  | Wikipedia — "Atkinson–Shiffrin memory model"                                                | https://en.wikipedia.org/wiki/Atkinson%E2%80%93Shiffrin_memory_model                                            |
| 30  | SimplyPsychology — "Multi-Store Model"                                                      | https://www.simplypsychology.org/multi-store.html                                                               |
| 31  | Whatfix — "Ebbinghaus Forgetting Curve" (blog)                                              | https://whatfix.com/blog/ebbinghaus-forgetting-curve/                                                           |
| 32  | OmniSets — "Unveiling the Secrets of Spaced Repetition and the Ebbinghaus Forgetting Curve" | https://www.omnisets.com/blog/5/unveiling-the-secrets-of-spaced-repetition-and-the-ebbinghaus-forgetting-curve/ |
| 33  | PMC — Sleep-dependent memory consolidation model                                            | https://pmc.ncbi.nlm.nih.gov/articles/PMC9636926/                                                               |
| 34  | PMC — "Memory Consolidation"                                                                | https://pmc.ncbi.nlm.nih.gov/articles/PMC4526749/                                                               |
| 35  | Springer — "System Consolidation During Sleep"                                              | https://link.springer.com/article/10.1007/s00426-011-0335-6                                                     |
| 36  | Wikipedia — "Interference Theory"                                                           | https://en.wikipedia.org/wiki/Interference_theory                                                               |
| 37  | SimplyPsychology — "Proactive and Retroactive Interference"                                 | https://www.simplypsychology.org/proactive-and-retroactive-interference.html                                    |
| 38  | PNAS — "Making Lasting Memories: Remembering the Significant"                               | https://www.pnas.org/doi/10.1073/pnas.1301209110                                                                |
| 39  | PMC — "Amygdala and the Prioritization of Declarative Memories"                             | https://pmc.ncbi.nlm.nih.gov/articles/PMC5049500/                                                               |
| 40  | PMC — Basolateral amygdala activation and post-encoding consolidation                       | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9295787/                                                           |

**Used for:** `03-forgetting-strategy.md` in full — §2 (multi-store model, Ebbinghaus decay, spaced repetition), §3.1 (amygdala-mediated salience/flashbulb-memory exemption for sacred records), §4 (sleep-dependent episodic→semantic consolidation), §5 (interference theory as the basis for invalidation-over-deletion).

---

## 4. Internal Workspace Documentation Consulted

Not external sources, but the existing workspace documents this investigation was required to
build on rather than duplicate (ASE governance requirement, `agent-systems-engineering/governance/`):

| Document                                                                                    | Role in This Investigation                                                                  |
| ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `core-component-00/context-engineering/implementations/memory_store.py`                     | Existing four-memory-type model this design extends                                         |
| `core-component-00/context-engineering/implementations/context_compressor.py`               | Existing `CompactionAPIClient`/summarization primitive reused for consolidation             |
| `core-component-00/retrieval-augmented-generation/architecture/overview.md`                 | Corpus-as-Source-of-Truth principle and Graceful Degradation Stack, extended by this design |
| `core-component-00/retrieval-augmented-generation/architecture/diagrams.md`                 | Mermaid diagram convention followed in `04-workflow-diagrams.md`                            |
| `core-component-00/retrieval-augmented-generation/deployment/lightweight-rag-deployment.md` | Existing Qdrant deployment-mode mandate this design must not violate                        |
| `core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md`             | Contrast case (document freshness) informing why memory's write path is simpler             |
| `core-component-00/telescope/CLAUDE.md`, `telescope/CLAUDE.md` (workspace root)             | Report shape and status-lifecycle conventions this programme follows                        |

---

## 5. Framework Selection Rationale — Why a Custom Design Was Built

**We did not adopt any single existing framework wholesale — we built a custom design for this
workspace, and took specific, individually-borrowed mechanisms from each system surveyed in §1–2
above.** No off-the-shelf option was a clean fit, because each was built to solve a different
problem than the one this workspace actually has:

- **Anthropic's own Claude memory tool** (§1) is built for a single assistant remembering things
  for itself across its own context resets. It is deliberately file-based with no vector search —
  the right choice for that problem, but insufficient for this workspace's need: a shared,
  searchable, cross-session team knowledge base that already exists and must be extended, not
  replaced.
- **MemGPT/Letta, Mem0, and Zep** (§2) are each frameworks a team would typically install as a
  whole new system from scratch. This workspace already runs its own Qdrant-backed retrieval
  infrastructure (`retrieval-augmented-generation/`) — adopting any one of them wholesale would
  mean discarding working infrastructure rather than extending it.
- **Generative Agents** (§2) is a research simulation, not a deployable system — its scoring and
  reflection mechanisms are genuinely useful ideas, but there is no product to adopt, only a
  technique to borrow.

**What was actually taken from each**, specifically:

| Source                    | Idea Borrowed                                                                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Anthropic's memory tool   | Memory must stay human-readable and editable — never an opaque, vector-only black box (`01-technical-options.md` §2, Memory-as-Corpus)       |
| Generative Agents         | Importance-weighted retention scoring, so significant memories persist longer than routine ones (`03-forgetting-strategy.md` §3)             |
| Mem0                      | Checking whether a new memory contradicts an existing one, and updating rather than accumulating duplicates (`03-forgetting-strategy.md` §5) |
| Zep/Graphiti              | Never deleting outdated information outright — marking it superseded while preserving the record (`03-forgetting-strategy.md` §5)            |
| Human memory science (§3) | The forgetting/decay behavior itself — grounded in neuroscience, not any of the surveyed tech systems                                        |

This is the same reasoning already presented in `research-report.md` § Findings 1–2 and in the
Executive Summary's Recommendation — this section exists to give it a permanent, directly citable
home addressing the CEO's specific question, rather than requiring it be reconstructed from the
findings narrative each time it comes up.

---

## 6. Design Mechanism Rationale

Consolidated, standardized summary of every core design mechanism in this programme, for future
review without needing to reconstruct rationale from prose scattered across multiple documents.
Every row reflects a decision already specified elsewhere in this programme — nothing here is new;
this table is a cross-referenced index into it.

| #   | Mechanism                                 | Design Choice                                                                                                                                                                                                                                                                         | Rationale                                                                                                                                                                                                                                                                                                                             | Precedent / Source                                                                                                                                                                                                                                                                               | Specified In                                                                                       |
| --- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| 1   | **Memory scoring / retrieval**            | Two modes: recency-filtered (`session_id` + `created_at`, no embedding) and semantic-similarity (Qdrant embedding + BM25 RRF fusion, filtered to `status = "active"`); sacred records always merged in regardless of decay-driven status                                              | Matches the workspace's existing hybrid-retrieval mandate; recency-filtered mode avoids unnecessary embedding cost for session-scoped lookups; sacred bypass preserves the pre-existing `EpisodicMemory.get_sacred_context()` contract                                                                                                | RAG module's existing RRF fusion (`retrieval.py`); no external framework prescribes the sacred-bypass rule — that is this workspace's own invariant                                                                                                                                              | `01-technical-options.md` §6                                                                       |
| 2   | **Decay mechanism**                       | `decay_weight(t) = importance × e^(-Δt/strength)`, where `strength` grows with `access_count` (spaced-repetition reinforcement)                                                                                                                                                       | Emulates the Ebbinghaus exponential forgetting curve rather than a flat TTL; retrieval-driven strengthening reflects the "testing effect" from spaced-repetition research                                                                                                                                                             | Ebbinghaus curve / spaced repetition literature (`00-sources-and-references.md` §3, sources #31–32); replaces the pre-existing flat `expires_after_seconds` TTL in `memory_store.py`                                                                                                             | `03-forgetting-strategy.md` §3                                                                     |
| 3   | **Importance mechanism**                  | Importance assigned 0.0–1.0 at write time by a lightweight, non-LLM heuristic keyed on write context (decision/commitment → 1.0, correction/preference → 0.7, routine observation → 0.2–0.3); `sacred = true` records permanently exempt from decay                                   | Adapts Generative Agents' LLM-scored 1–10 importance rating to a cheaper mechanism, since a per-write LLM call would put the <100ms write-latency target out of reach; sacred exemption grounded in amygdala-mediated salience/"flashbulb memory" literature and the pre-existing `SACRED_EVENT_TYPES` invariant in `memory_store.py` | Park et al. 2023 (source #18, scoring concept only, not scoring cost); PNAS/PMC amygdala literature (source #38–40); existing `EpisodicMemory.SACRED_EVENT_TYPES`                                                                                                                                | `03-forgetting-strategy.md` §3, §3.1                                                               |
| 4   | **Consolidation (episodic → semantic)**   | Trigger: cumulative `importance × access_count` per session ≥ 150; synthesize via LLM summarization (`ContextCompressor`) into a new `memory_semantic` record with `consolidated_from` provenance; source episodic records are not deleted                                            | Models sleep-dependent systems consolidation (hippocampus → neocortex; episodic detail → semantic gist); the 150 threshold is borrowed directly from Generative Agents' empirically-tuned reflection trigger as a starting point, not independently derived                                                                           | Park et al. 2023 reflection mechanism (source #18); PMC/Springer sleep-consolidation literature (source #33, #35)                                                                                                                                                                                | `03-forgetting-strategy.md` §4                                                                     |
| 5   | **Contradiction / invalidation**          | Checked during the batch maintenance pass, not synchronously at write time: LLM-judged `ADD` / `UPDATE` / `DELETE` / `NOOP` classification against similar existing facts; on `UPDATE`, the superseded record is marked `status = "archived"` — never physically deleted at this step | Implements interference theory (retroactive interference is the primary driver of everyday forgetting) as an explicit, auditable state transition rather than a silent overwrite; deferred to batch because the LLM judgment call would otherwise sit on the synchronous write path alongside embedding                               | Mem0's Updater decision logic (source #19); Zep/Graphiti's bi-temporal fact invalidation (source #22–23); interference-theory literature (source #36–37)                                                                                                                                         | `03-forgetting-strategy.md` §5; `02-deployment-guidelines.md` §3                                   |
| 6   | **Status transition / forgetting**        | Three-stage ladder: `active` → `dormant` (`decay_weight < 0.5`) → `archived` (`decay_weight < 0.15` AND 30-day access grace period); hard deletion is never automatic and requires explicit operator confirmation                                                                     | "Weakened synapse, not yet pruned" analogy; prioritizes this workspace's git-safety/append-only convention over literal biological fidelity — synaptic pruning is not human-reversible, and this design deliberately diverges from that literal analogy, disclosed explicitly rather than left implicit                               | Closest external precedent is Zep's mark-don't-delete pattern, generalized here into a two-stage soft archive; the never-automatic-hard-delete rule is workspace-specific, not literature-derived                                                                                                | `03-forgetting-strategy.md` §5–6; divergence flagged in `06-self-review-and-evaluation.md` §4      |
| 7   | **Storage / corpus mechanism**            | Append-only JSONL log per memory type is the source of truth; the Qdrant collection is a derived, rebuildable semantic index over it ("Memory-as-Corpus")                                                                                                                             | Extends the workspace's existing Corpus-as-Source-of-Truth RAG principle to memory, which otherwise has no external document to re-derive from if the index were lost                                                                                                                                                                 | `retrieval-augmented-generation/architecture/overview.md` §10; Anthropic's own file-based, auditable memory-tool philosophy (source #1, #8) — explicit divergence: Anthropic omits the vector layer entirely, this design adds it back for cross-session semantic recall at knowledge-base scale | `01-technical-options.md` §2                                                                       |
| 8   | **Deployment topology**                   | Memory runs on its own dedicated Qdrant instance (`qdrant-memory`), physically separate from the document knowledge base's `qdrant-workspace` instance                                                                                                                                | Blast-radius isolation, workload isolation (per-turn write frequency vs. occasional document writes), and a harder security boundary — chosen over shared-instance convenience per explicit CEO direction favoring architectural rigor over current single-node hardware-scale pragmatism                                             | Workspace-specific decision — none of the five benchmarked frameworks (§1–2) address this workspace's particular co-location question; this is not literature-derived                                                                                                                            | `01-technical-options.md` §8; `02-deployment-guidelines.md` §1                                     |
| 9   | **Multimodal memory**                     | `modality`/`media_ref` payload fields; the model generates its own caption/transcript as `content` at write time; raw media stored on disk, never embedded directly in v1                                                                                                             | Preserves the Memory-as-Corpus principle for non-text sources; avoids an external OCR/ASR round-trip since the model already has native multimodal understanding in-context at write time                                                                                                                                             | MarkItDown explicitly scoped **out** of this path — reserved for RAG document-corpus ingestion only, not memory writes                                                                                                                                                                           | `01-technical-options.md` §3.2; security follow-up logged in `06-self-review-and-evaluation.md` §7 |
| 10  | **Disaster recovery / degradation stack** | Four-tier fallback (qdrant-memory hybrid → in-process FAISS → BM25 over JSONL → raw JSONL scan); JSONL append never blocked by Qdrant availability (zero RPO); automatic self-check/resync on reconnect                                                                               | Extends the document-RAG Graceful Degradation Stack to memory; the Memory-as-Corpus principle already guarantees a cold-fallback at no extra cost, giving the design stability under infrastructure failure alongside its existing normal-operation stability guarantees                                                              | Direct precedent: `architecture/overview.md` §11 (degradation stack) and `evaluation/reference-table.md` § Orphaned Point Detection (inverted, for resync detection)                                                                                                                             | `05-disaster-recovery-and-resilience.md`                                                           |

---

## 7. Verification Status (Cross-Reference)

Per `06-self-review-and-evaluation.md` §5: this bibliography reflects what the research subagent
retrieved and what the Director cited — it has not been independently re-fetched and re-verified
against primary sources by the Safety & Evaluation reviewer. That remains an open item, not
resolved by the existence of this archive. See `06-self-review-and-evaluation.md` §5 for the
standing recommendation to spot-check the most load-bearing figures (the memory-tool 84%
token-reduction claim, the Ebbinghaus 50%/30-minute figure, and the Generative Agents
importance-threshold value) before they inform a tuned production constant.

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Compiled from:** Research synthesis produced by the background research agent tasked for this
investigation (`research-report.md` § Methodology)
