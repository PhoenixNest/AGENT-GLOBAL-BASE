# Research Report — Persistent Agent Memory Architecture for the Qdrant-Backed Knowledge Base

---

## Metadata

| Field                     | Value                                                                                                                                                                                                                |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Investigation ID**      | `2026-07-10-agent-memory-architecture`                                                                                                                                                                               |
| **Date Started**          | 2026-07-10                                                                                                                                                                                                           |
| **Date Completed**        | 2026-07-10                                                                                                                                                                                                           |
| **Status**                | Complete — this refers to the research/design investigation only; see **Implementation Status** below                                                                                                                |
| **Implementation Status** | Not started. No code has been written, no Qdrant collections created, no maintenance job deployed. This report is a design specification pending a separate implementation task (see § Recommendations, Next Steps). |
| **Investigator**          | Dr. Elias Vance (Laboratory Director, Principal Investigator)                                                                                                                                                        |
| **Laboratory**            | Core Component 00                                                                                                                                                                                                    |
| **Module(s)**             | Context Engineering (memory types) × Retrieval-Augmented Generation (Qdrant)                                                                                                                                         |
| **Priority**              | High                                                                                                                                                                                                                 |
| **Requestor**             | CEO                                                                                                                                                                                                                  |

**Executing engineers:** Mei-Ling Zhao (Context Engineering module lead — memory taxonomy,
consolidation) and Sofia Almeida with Diego Fontán (RAG module — Qdrant collection design,
retrieval). Independent audit: Dr. Tomasz Wieczorek (Staff Safety & Evaluation Engineer) — see
`supporting/06-self-review-and-evaluation.md`.

---

## Executive Summary

The CEO commissioned CC-00 to design a persistent memory system for the workspace's lightweight
Qdrant-backed knowledge base, benchmarked against Anthropic's own published Claude memory
architecture and other top-tier agent memory designs, with an explicit requirement for a
human-brain-emulating forgetting strategy. We surveyed Anthropic's memory tool, context editing,
and consumer Claude memory feature; MemGPT/Letta; Stanford's Generative Agents; Mem0; Zep/Graphiti;
and LangGraph's memory taxonomy, then cross-referenced five human-memory-science mechanisms
(multi-store model, Ebbinghaus decay, sleep-dependent consolidation, interference theory,
salience-weighted retention) to ground the design in both engineering precedent and biological
analogy.

**Recommendation:** extend this workspace's existing four-memory-type model
(`context-engineering/implementations/memory_store.py`) with three Qdrant-backed collections
following a **Memory-as-Corpus** principle — an append-only JSONL log is the source of truth,
Qdrant is a derived, rebuildable semantic index — preserving the same rebuild/rollback guarantees
already established for document RAG. Forgetting is implemented as a three-stage decay
(`active → dormant → archived`) driven by an Ebbinghaus-style exponential formula strengthened by
retrieval (spaced-repetition analog), with a sacred-memory exemption for decisions/commitments
(a flashbulb-memory analog) and a sleep-consolidation-modeled maintenance job that promotes
recurring episodic detail into distilled semantic facts. Full technical specification:
`supporting/01-technical-options.md`; deployment: `supporting/02-deployment-guidelines.md`; decay
mechanics: `supporting/03-forgetting-strategy.md`; self-review: `supporting/06-self-review-and-evaluation.md`;
visual workflow reference: `supporting/04-workflow-diagrams.md`; disaster recovery and resilience:
`supporting/05-disaster-recovery-and-resilience.md`.

---

## Investigation Scope

### What Was Investigated

We investigated (1) what categories of agent-generated or agent-observed information warrant
persistence as "memory" versus what should remain ephemeral, (2) how that information should be
stored against this workspace's existing Qdrant/BM25 hybrid retrieval infrastructure, (3) the
rationale for persisting each category, (4) the technical options for embedding, chunking,
collection design, and deployment, and (5) a decay/forgetting policy explicitly modeled on human
memory science.

### Why This Investigation Was Needed

This workspace already has a four-type memory model (episodic, semantic, procedural, working —
`memory_store.py`) and a production Qdrant-backed RAG pipeline for the document knowledge base
(`retrieval-augmented-generation/`), but the two have never been architecturally joined: the
memory store's docstring explicitly notes "In production, back this with a vector database
(Qdrant/Weaviate)... This implementation uses an in-memory dict." No forgetting/decay policy exists
for any memory type beyond a flat TTL (`SemanticFact.expires_after_seconds`). The CEO's mandate
closes both gaps at once and requires the design be benchmarked against the field's actual
state of the art rather than invented ad hoc, per the workspace's ASE governance requirement to
build on established patterns (`agent-systems-engineering/governance/`).

### Out of Scope

- Modifying the existing document-corpus RAG collection or its retrieval pipeline
  (`retrieval-augmented-generation/implementations/`) — this investigation adds new collections
  alongside it, per `01-technical-options.md` §3.
- A production implementation of the maintenance job — this report specifies the design; a
  follow-up implementation task would produce the runnable Python module.
- Cross-organization memory sharing between the Company, Studio, and CC-00 telescopes — this
  investigation is scoped to CC-00's own knowledge-base memory, consistent with
  `core-component-00/telescope/CLAUDE.md`'s scope boundary.

---

## Research Questions

1. What is Anthropic's own published architecture for Claude memory and context management, and
   what design principles does it embody?
2. How do other top-tier agent memory architectures (MemGPT/Letta, Generative Agents, Mem0,
   Zep/Graphiti, LangGraph) structure long-term memory, and where do they converge or diverge?
3. What categories of information should this workspace's agents persist as memory, and what is
   the rationale for persisting each category (vs. treating it as ephemeral working state)?
4. How should persisted memory be stored against the existing Qdrant/BM25 hybrid infrastructure
   without violating the workspace's Corpus-as-Source-of-Truth principle?
5. What forgetting/decay mechanism would emulate human memory science while remaining consistent
   with this workspace's safety posture (no silent, irreversible data loss)?

---

## Methodology

### Approach

Three phases: (1) a dedicated research pass over Anthropic's own published memory/context-
management documentation and engineering blog, plus five comparator SOTA architectures, conducted
via live web search on 2026-07-10 (all external claims below carry inline source citations and a
retrieval date — see the freshness note below); (2) a design synthesis phase mapping each surveyed
mechanism onto this workspace's existing `memory_store.py` taxonomy and RAG infrastructure; (3) an
independent self-review pass cross-checking the design against the CEO's five explicit requirements
(`supporting/06-self-review-and-evaluation.md`).

**Freshness note (per RAG freshness protocol):** several cited Anthropic features (the memory
tool, context editing, an April 2026 Managed Agents public beta) postdate this investigator's
training cutoff and were retrieved fresh via web search on 2026-07-10, not recalled from training
data. Anthropic-internal continuity note: several patterns below were independently anticipated in
this lab's own prior work before this investigation confirmed them against Anthropic's public
documentation — notably `context_compressor.py`'s existing `CompactionAPIClient`
(`compact_20260112`), which already models the compaction concept Anthropic's engineering blog
describes, and the existing Sacred Context principle, which independently converges with the
memory tool's decision/commitment persistence pattern.

### Tools and Resources

- Live web search and document retrieval (2026-07-10)
- This workspace's existing `context-engineering/implementations/memory_store.py`,
  `context_compressor.py`, and `retrieval-augmented-generation/` architecture documentation
- Cross-department conventions: `telescope/CLAUDE.md`, `core-component-00/telescope/CLAUDE.md`

### Constraints

- No production Qdrant instance was queried or modified during this investigation — all
  collection/schema specifications are design recommendations pending implementation.
- Human-memory-science citations are drawn from secondary sources (review articles, summary sites)
  in addition to primary literature (PNAS, PMC, arXiv) — sufficient for design-grounding purposes
  but not a substitute for a dedicated neuroscience literature review.

---

## Findings

### Finding 1: Anthropic's Own Architecture Deliberately Avoids Vector Stores for Memory — and This Is a Considered Divergence Point, Not an Oversight to Copy Blindly

Anthropic's memory tool (`memory_20250818`, generally available, no beta header required as of
this writing) is explicitly **file-based**, not vector-based: Claude reads/writes plain files under
a `/memories` directory via `view`/`create`/`str_replace`/`insert`/`delete`/rename operations, and
Anthropic's own framing credits this choice with transparency and user-editability — "rather than
complex vector databases and semantic search," per third-party analysis of Anthropic's design
rationale (Skywork.ai, retrieved 2026-07-10; Claude Developer Platform Memory tool docs, retrieved
2026-07-10). Anthropic pairs this with a separate **context editing** feature
(`clear_tool_uses_20250919`) that server-side clears stale tool results once a token/count threshold
is crossed, reporting an 84% token reduction and 29% eval improvement when combined with the memory
tool (Context editing docs, retrieved 2026-07-10). Claude.ai's consumer memory feature is likewise a
**generated, user-viewable/editable summary**, not raw embeddings, and is deliberately
project-scoped for compartmentalization (Anthropic, "Bringing memory to teams," retrieved
2026-07-10).

**Evidence:**

- Memory tool file operations and `/memories` path prefix (Memory tool docs, retrieved 2026-07-10)
- 84% token reduction / 100-turn workflow completion claim (Context editing docs, retrieved
  2026-07-10)
- Explicit avoidance of vector/semantic-search architecture (Skywork.ai, retrieved 2026-07-10)
- Project-scoped memory isolation for compartmentalization (Anthropic "Bringing memory to teams,"
  retrieved 2026-07-10)

**Implications:**

This workspace's requirement is different in kind from Anthropic's: Anthropic's memory tool serves
a single agent's own continuity across context resets, where transparency and direct
editability dominate the design. This workspace's ask is a **shared, cross-session,
multi-agent knowledge base** at team scale, where semantic recall over a growing corpus of facts
is the primary value (matching this workspace's existing RAG investment, not a divergent new
requirement). The recommended design (`01-technical-options.md` §2) resolves this by keeping
Anthropic's transparency property — an append-only, human-readable JSONL log as the actual source
of truth — while adding Qdrant purely as a derived, rebuildable recall layer on top, so the system
gets semantic search without sacrificing auditability. This is stated explicitly as a **deliberate,
justified divergence**, not an inconsistency with the benchmark.

---

### Finding 2: Every Surveyed SOTA Architecture Converges on Some Form of Importance/Salience-Weighted Retention — Not Flat TTL

MemGPT/Letta's tiered core/recall/archival paging (Letta Docs; Leonie Monigatti, retrieved
2026-07-10), Generative Agents' `recency + importance + relevance` retrieval score (Park et al.
2023, retrieved 2026-07-10), Mem0's LLM-driven ADD/UPDATE/DELETE/NOOP consolidation (Dwarves Memo,
retrieved 2026-07-10), and Zep/Graphiti's bi-temporal fact-invalidation model (Zep arXiv paper,
retrieved 2026-07-10) all reject a single flat expiry timer in favor of a weighted, dynamically
recomputed retention signal. This workspace's existing `SemanticMemory.expires_after_days` is a
flat TTL — the exact pattern every surveyed architecture has moved past.

**Evidence:**

| Architecture             | Retention Mechanism                                                               |
| ------------------------ | --------------------------------------------------------------------------------- |
| MemGPT/Letta             | Tiered paging (core/recall/archival), self-editing by the agent itself            |
| Generative Agents        | `score = recency + importance + relevance`, exponential recency decay (0.995/hr)  |
| Mem0                     | LLM-judged ADD/UPDATE/DELETE/NOOP on every write                                  |
| Zep/Graphiti             | Bi-temporal validity intervals; contradiction triggers invalidation, not deletion |
| This workspace (current) | Flat TTL (`expires_after_seconds`) — no importance weighting                      |

**Implications:**

The forgetting strategy (`supporting/03-forgetting-strategy.md`) replaces the flat TTL with an
importance-and-access-weighted exponential decay formula (§3 of that document), directly closing
this gap and bringing the design in line with every surveyed comparator.

---

### Finding 3: Episodic→Semantic Consolidation Is Both a Human-Memory Mechanism and an Existing SOTA Pattern — a Convergent, Not Speculative, Design Choice

Generative Agents' reflection mechanism (triggered when cumulative importance crosses a threshold,
synthesizing raw observations into higher-level insights with provenance pointers — Park et al.
2023, retrieved 2026-07-10) is mechanistically parallel to human sleep-dependent systems
consolidation, in which hippocampal episodic traces are progressively transformed into
gist-based, neocortical semantic representations (PMC, "Sleep-dependent consolidation model";
Springer, "System consolidation during sleep," retrieved 2026-07-10). Independently, this
workspace's `SACRED_EVENT_TYPES` mechanism already treats decisions/commitments as needing
special, non-decaying handling — convergent with the amygdala-mediated salience-priority
consolidation literature (PNAS, "Making lasting memories," retrieved 2026-07-10) without having
been designed with that literature in mind.

**Evidence:** see `supporting/03-forgetting-strategy.md` §4 for the full mechanism-to-citation mapping.

**Implications:** the consolidation step in the forgetting strategy is not a novel invention risk —
it is independently supported by both an engineering precedent (Generative Agents' reflection,
already shipped and evaluated in a published system) and a biological mechanism (sleep-dependent
consolidation), which raises confidence in recommending it for implementation ahead of empirical
validation in this workspace specifically.

---

### Finding 4: Forgetting-as-Interference (Not Forgetting-as-Decay) Better Matches This Workspace's Safety Posture

Interference theory — specifically retroactive interference, where new information degrades
retrieval of older related memories — is the better-supported account of everyday human forgetting
versus pure time-based decay (Wikipedia, "Interference theory"; SimplyPsychology, retrieved
2026-07-10). This maps directly onto Zep/Graphiti's design choice to invalidate contradicted facts
rather than delete them (Zep arXiv paper, retrieved 2026-07-10) — a state transition, not
destruction. This is materially more compatible with this workspace's standing rules than a
decay-only model would be: the workspace's git-safety conventions require escalation before
irreversible operations, and the telescope archive convention is explicitly append-oriented
(`telescope/CLAUDE.md` § Rules).

**Implications:** the forgetting strategy's status model (`active → dormant → archived`, with hard
deletion never automatic — `supporting/03-forgetting-strategy.md` §5) directly implements this
finding, and resolves what would otherwise be a tension between "emulate human forgetting" and
"never silently destroy data."

---

## Analysis

### Interpretation of Findings

The four findings converge on a single design posture: **decay as a demotion in retrieval priority,
not as destruction.** Every top-tier architecture surveyed — including Anthropic's own — treats
forgetting as something that changes what is _surfaced_, while preserving the option to recover or
re-surface a memory later (Anthropic's memory tool is directly user-editable; Zep never deletes,
only invalidates; this workspace's own telescope archive is append-only by rule). The design
recommended here is therefore not a compromise between "biologically faithful" and "operationally
safe" — the two turned out to point the same direction once the literature was actually consulted,
which is itself a useful validation of the benchmarking exercise the CEO requested.

### Trade-offs Identified

| Decision                                                                                                    | Benefit                                                                                                      | Cost                                                                                                                                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Qdrant semantic layer over Anthropic's file-only model                                                      | Cross-session semantic recall at knowledge-base scale                                                        | An additional derived-index maintenance burden Anthropic's simpler model avoids                                                                                                                                                                                                                           |
| Exponential decay with access-based strengthening                                                           | Matches Ebbinghaus curve + spaced-repetition evidence more closely than flat TTL                             | More tunable parameters (`base_strength`, `reinforcement_factor`) with no single validated value yet                                                                                                                                                                                                      |
| Soft-archival instead of automatic hard deletion                                                            | Matches interference-theory-as-invalidation and this workspace's safety posture                              | Requires an explicit, separately-scheduled GC step and human confirmation — more operational surface than "just expire it"                                                                                                                                                                                |
| Consolidation via LLM summarization call                                                                    | Produces genuinely distilled semantic facts, not naive concatenation                                         | Adds LLM-call cost and latency to the maintenance job, not to per-turn writes                                                                                                                                                                                                                             |
| Dedicated `qdrant-memory` instance, in-process FAISS fallback, and separate decay/consolidation/resync jobs | Blast-radius isolation, workload isolation, and disaster recovery independent of the document knowledge base | Meaningful running infrastructure for a corpus that, by the document knowledge base's own precedent, is currently a few thousand points at most — this design is sized for anticipated growth, not the current corpus size, which is a deliberate trade disclosed here rather than an unstated assumption |

### Risks and Limitations

- The decay/consolidation thresholds in `03-forgetting-strategy.md` §6 are starting defaults derived
  from a mix of borrowed literature values (Generative Agents' 150-importance reflection trigger)
  and order-of-magnitude reasoning (7-day base strength) — none have been empirically validated
  against this workspace's actual session data yet.
- The LLM-judged contradiction check (Finding 4) introduces a dependency on LLM judgment quality at
  write time; a false "UPDATE" classification could incorrectly archive a still-valid fact. No
  adversarial evaluation of this specific mechanism has been run yet (see
  `supporting/06-self-review-and-evaluation.md`).
- This design has not been implemented or load-tested against the workspace's actual corpus scale
  (7,793 points at last measurement, per `lightweight-rag-deployment.md`).

---

## Recommendations

### Primary Recommendation

**Adopt the Memory-as-Corpus architecture in `supporting/01-technical-options.md`** — three Qdrant
collections (`memory_episodic`, `memory_semantic`, `memory_procedural`) layered onto the existing
`workspace-knowledge` MCP server, backed by an append-only JSONL log as the durable source of
truth, with the decay/consolidation policy in `supporting/03-forgetting-strategy.md` run as a
scheduled maintenance job per `supporting/02-deployment-guidelines.md` §5.

### Secondary Recommendations

1. **Implement the maintenance job as a standalone, testable module** (not inline in the MCP
   server) so its decay formula can be unit-tested against synthetic memory records before
   production deployment, consistent with this module's existing test-suite discipline
   (`retrieval-augmented-generation/CLAUDE.md` — no merge without a green `pytest` suite).
2. **Instrument decay/consolidation telemetry from day one** — `dormant_ratio`,
   `last_consolidation_at`, and per-collection point counts (`02-deployment-guidelines.md` §6) — so the
   unvalidated thresholds in Finding/Risk above can be recalibrated from real data rather than left
   as permanent guesses.
3. **Route the LLM-judged contradiction check through Dr. Wieczorek's independent evaluation
   function** before production activation, given the risk identified above — this is exactly the
   adversarial-evaluation mandate his role was created for (`crew/safety-evaluation/tomasz-wieczorek/agent/profile.md`).

### Implementation Priority

| Recommendation                                      | Priority | Effort                   | Impact                 |
| --------------------------------------------------- | -------- | ------------------------ | ---------------------- |
| Qdrant collection creation + JSONL write-through    | P0       | 2–3 days                 | High                   |
| Maintenance job (decay + consolidation)             | P0       | 3–4 days                 | High                   |
| Telemetry instrumentation                           | P1       | 1 day                    | Medium                 |
| Adversarial evaluation of contradiction-check logic | P1       | 2 days                   | High (risk mitigation) |
| Threshold recalibration from real session data      | P2       | Ongoing, post-deployment | Medium                 |

### Next Steps

1. Present this report and its four supporting documents to the CEO for sign-off (this is a hard
   stop per this workspace's User Approval Gate convention — see the covering message).
2. On approval, open an implementation task against `context-engineering/implementations/` and
   `retrieval-augmented-generation/` for the maintenance-job module.
3. Schedule the first adversarial evaluation pass with Dr. Wieczorek ahead of production activation.

---

## References

### Internal Documentation

- `core-component-00/context-engineering/implementations/memory_store.py`
- `core-component-00/context-engineering/implementations/context_compressor.py`
- `core-component-00/retrieval-augmented-generation/architecture/overview.md`
- `core-component-00/retrieval-augmented-generation/deployment/lightweight-rag-deployment.md`
- `core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md`
- `core-component-00/retrieval-augmented-generation/evaluation/reference-table.md`
- `supporting/00-sources-and-references.md`, `supporting/01-technical-options.md`,
  `supporting/02-deployment-guidelines.md`, `supporting/03-forgetting-strategy.md`,
  `supporting/06-self-review-and-evaluation.md`, `supporting/04-workflow-diagrams.md`,
  `supporting/05-disaster-recovery-and-resilience.md` (this programme)

### External Sources (all retrieved via live web search, 2026-07-10)

**Full bibliography with URLs and retrieval dates:** `supporting/00-sources-and-references.md`
("Archive No. 0") — the summary below is a condensed pointer, not a substitute for that archive.

- Claude Developer Platform — Memory tool docs; Context editing docs
- Anthropic — "Bringing memory to teams"; "Effective context engineering for AI agents" (Anthropic
  Engineering, 2025-09-29)
- Skywork.ai — "Claude Memory: A Deep Dive Into Anthropic's Persistent Context Solution"
- Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (2023, ar5iv)
- Letta Docs; Leonie Monigatti — MemGPT architecture summaries
- Dwarves Memo — Mem0 architecture breakdown; Mem0 blog
- Zep — arXiv:2501.13956; Neo4j Developer Blog — "Graphiti"
- LangChain Docs — Memory overview; LangMem SDK launch; Patronus AI — "Agentic Memory"
- Wikipedia — "Atkinson–Shiffrin memory model"; "Interference theory"; SimplyPsychology (multiple)
- Whatfix; OmniSets — Ebbinghaus forgetting curve / spaced repetition
- PMC — "Sleep-dependent consolidation model"; "Memory Consolidation"; Springer — "System
  consolidation during sleep"
- PNAS — "Making lasting memories"; PMC — amygdala prioritization of declarative memories

### Related Work

- Prior CC-00 programmes this investigation builds on: Retrieval Freshness Guarantees (resolved,
  `patterns/index-sync-hooks.md`); Multi-Agent Memory Coherence (open, `context-engineering/CLAUDE.md`)
  — this investigation's findings are directly relevant to that open question and should be
  cross-referenced when it is next picked up.

---

## Open Questions

1. **Are the decay/consolidation threshold defaults (`03-forgetting-strategy.md` §6) correct for this
   workspace's actual session lengths and write frequency?**
   Status: Unvalidated — requires production telemetry.
   Priority: Medium
   Assigned: Follow-up investigation post-deployment.

2. **Does the LLM-judged contradiction check (Finding 4 / `03-forgetting-strategy.md` §5) produce an
   acceptable false-positive rate for incorrectly archiving still-valid facts?**
   Status: Not yet adversarially tested.
   Priority: High
   Assigned: Dr. Tomasz Wieczorek, pre-production.

3. **How does this design interact with the open Multi-Agent Memory Coherence research question
   (distributed shared memory without a central store)?**
   Status: Not addressed — this design assumes a single dedicated `qdrant-memory` instance
   (`01-technical-options.md` §8), separate from the document knowledge base but still a single
   centralized store for memory itself, consistent with this workspace's current single-node
   deployment. It does not resolve the distributed case (multiple memory-owning nodes with no
   central store). A concrete instance of this open question already exists within the current
   single-instance design: because the contradiction check runs in a batch maintenance pass rather
   than synchronously at write time (`03-forgetting-strategy.md` §5), two agents or sessions writing
   conflicting facts to `memory_semantic` in the same maintenance window could both be classified
   `ADD` against the same now-stale existing fact, producing two live contradictory records instead
   of one `UPDATE`. This does not require a distributed store to occur — it is a same-instance race
   condition — but it is the same underlying coordination problem this open question is about, and
   should be resolved together with it rather than treated as a separate concern later.
   Priority: Low (no current multi-node requirement), though the same-instance race condition above
   should be included in Dr. Wieczorek's pre-production adversarial pass
   (`06-self-review-and-evaluation.md` §6) regardless of priority on the distributed question.
   Assigned: Mei-Ling Zhao, if/when that programme is next active.

---

## Version History

| Version | Date       | Author          | Changes                           |
| ------- | ---------- | --------------- | --------------------------------- |
| 1.0     | 2026-07-10 | Dr. Elias Vance | Initial research report completed |

---

**Template Version:** 1.0
**Last Updated:** 2026-07-10
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
