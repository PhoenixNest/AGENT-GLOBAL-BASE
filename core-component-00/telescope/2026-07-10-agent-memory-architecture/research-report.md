# Research Report — Persistent Agent Memory Architecture for the Qdrant-Backed Knowledge Base

---

## Metadata

| Field                     | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Investigation ID**      | `2026-07-10-agent-memory-architecture`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Date Started**          | 2026-07-10                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Date Completed**        | 2026-07-10                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Status**                | Complete — this refers to the research/design investigation only; see **Implementation Status** below                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Implementation Status** | P0 complete and verified. P1 complete and verified, signed off by CEO 2026-07-12: telemetry instrumentation built; Dr. Wieczorek's adversarial evaluation found the contradiction-check wrapper has no independent safeguards (0% mitigation, memory-poisoning and race-condition both reproduce) — `i_have_completed_adversarial_review` remains unset, contradiction-check stays inert. Live `qdrant-memory` instance provisioned (Docker, ports 6335/6336, 3 collections created, verified reachable). P2 (threshold recalibration) blocked — 0 points across all three collections, no real session data exists yet; a synthetic sensitivity check (not a substitute) is folded into Open Question 1 below (originally `supporting/08-threshold-sensitivity-check.md`, retired 2026-08-10). |
| **Investigator**          | Dr. Elias Vance (Laboratory Director, Principal Investigator)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Laboratory**            | Core Component 00                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Module(s)**             | Context Engineering (memory types) × Retrieval-Augmented Generation (Qdrant)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Priority**              | High                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Requestor**             | CEO                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

**Executing engineers:** Mei-Ling Zhao (Context Engineering module lead — memory taxonomy,
consolidation) and Sofia Almeida with Diego Fontán (RAG module — Qdrant collection design,
retrieval). Independent audit: Dr. Tomasz Wieczorek (Staff Safety & Evaluation Engineer) — see
§ Self-Review Findings below.

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
[supporting/01-technical-options.md](supporting/01-technical-options.md); deployment: [supporting/02-deployment-guidelines.md](supporting/02-deployment-guidelines.md); decay
mechanics: [supporting/03-forgetting-strategy.md](supporting/03-forgetting-strategy.md); self-review: § Self-Review Findings below;
visual workflow reference: [supporting/04-workflow-diagrams.md](supporting/04-workflow-diagrams.md); disaster recovery and resilience:
[supporting/05-disaster-recovery-and-resilience.md](supporting/05-disaster-recovery-and-resilience.md).

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
  alongside it, per [01-technical-options.md](supporting/01-technical-options.md) §3.
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
(§ Self-Review Findings below).

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
requirement). The recommended design ([01-technical-options.md](supporting/01-technical-options.md) §2) resolves this by keeping
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

The forgetting strategy ([supporting/03-forgetting-strategy.md](supporting/03-forgetting-strategy.md)) replaces the flat TTL with an
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

**Evidence:** see [supporting/03-forgetting-strategy.md](supporting/03-forgetting-strategy.md) §4 for the full mechanism-to-citation mapping.

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
deletion never automatic — [supporting/03-forgetting-strategy.md](supporting/03-forgetting-strategy.md) §5) directly implements this
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

- The decay/consolidation thresholds in [03-forgetting-strategy.md](supporting/03-forgetting-strategy.md) §6 are starting defaults derived
  from a mix of borrowed literature values (Generative Agents' 150-importance reflection trigger)
  and order-of-magnitude reasoning (7-day base strength) — none have been empirically validated
  against this workspace's actual session data yet.
- The LLM-judged contradiction check (Finding 4) introduces a dependency on LLM judgment quality at
  write time; a false "UPDATE" classification could incorrectly archive a still-valid fact. This
  was subsequently adversarially evaluated and found unsafe as specified — see § Contradiction-Check
  Adversarial Evaluation below.
- This design has not been implemented or load-tested against the workspace's actual corpus scale
  (7,793 points at last measurement, per `lightweight-rag-deployment.md`).

---

## Architecture Decisions and Write-Path Security Posture (Post-Design Record)

This section records two decision streams that happened after the initial design above was
approved, so a reader of this report gets the current governing facts without having to piece
them together from individual supporting documents. Full detail and reasoning remain in the
documents cited; nothing here supersedes them, it only surfaces their conclusions centrally.

### Architecture: a dedicated `agent-memory` MCP server, read-only first (full record)

_Merged here from the retired `supporting/09-mcp-architecture-decision.md` — this is now the
authoritative citation._ Decided 2026-07-12, CEO on Laboratory Director recommendation.

**Context.** P0/P1 built and verified the memory system's storage/decay engineering, but none of
it was usable by an agent yet — no MCP tool exposed memory read or write.

**Decision 1 — dedicated server vs. extending `workspace-knowledge`.** The Lab Director's initial
recommendation was to extend the existing `workspace-knowledge` server rather than stand up a
second process. The CEO rejected that: extending `workspace-knowledge` risks destabilizing a
server that has already achieved production stability, with newer, less-tested memory code able to
take down proven document-search tooling if bolted into the same process. **Decision: a dedicated
MCP server, `mcp-servers/agent-memory/`, was approved** — the same blast-radius-isolation reasoning
already applied one layer down, where `qdrant-memory` got its own container rather than a
collection inside `qdrant-workspace`.

**Decision 2 — usage constraints for memory MCP tools, enforced in code, not left as
documentation** (following the precedent set by the contradiction-check gate's `RuntimeError` on
`enable_contradiction_check` without `i_have_completed_adversarial_review`):

- Read-only first — no write-capable tool ships in the first pass.
- Session-scoped episodic reads by default — cross-session access is explicit opt-in.
- Status filtering by default — `archived` records excluded unless explicitly requested.
- Sacred-record retrieval completeness preserved — no filter path may silently drop `sacred=true`.
- No caller-supplied `sacred`/`importance` override — set only by the internal write-time
  heuristic, never by a tool parameter.
- Graceful degradation on every path — no raised exception reaches an agent turn.

**Decision 3 — why a write tool was deliberately deferred.** Every memory write went through
`PersistentMemorySink`, called only by trusted internal runtime code — never by content an agent
merely read. A write-capable MCP tool changes that categorically: anything that gets an agent to
invoke a tool (including prompt-injected content in a document, web page, or tool result) could
write directly into persistent, cross-session memory. Combined with the contradiction-check finding
above (zero independent safeguards against an engineered contradiction), an agent-callable write
tool would open a direct route to the same class of memory-poisoning risk. Deferred until threat-
modeled specifically against prompt-injected write attempts (see below).

**Assessment Protocol history (Three-Gate Inclusion Test, `.claude/rules/mcp-governance.md`):**
run 2026-07-12 post-skeleton/pre-tool — failed as expected (Completeness unevaluable with zero
tools implemented). Re-run post-`search_memory` implementation — passed, with one caveat flagged
rather than hidden: Capability and Governance both clean passes; Completeness passed on "output
varies meaningfully with input" (17 unit tests) and passed-with-caveat on "tested against real
content" (verified end-to-end against live `qdrant-memory`, but using a stub embedding vector since
`all-MiniLM-L6-v2` wasn't installed yet and the live collections held zero real records — a
data/dependency gap, not a defect in `search_memory` itself). Registered 2026-07-12 with the
caveat recorded verbatim in the governance table rather than rounded up to an unqualified pass.

### Write-path security: threat-modeled, then built, then adversarially cleared with one residual caveat (full record)

_Merged here from the retired `supporting/11-write-path-threat-model.md` — this is now the
authoritative citation._ Threat-modeled 2026-08-06 (Worker B, scoping-only, no code) against a
hypothetical write-capable tool; the tool was separately authorized and built two days later.

**Five prompt-injection-driven attack shapes** (content an agent merely _read_ driving a write,
distinct from a live human instruction):

1. **Direct instruction injection** — a document/page/tool-result the agent reads contains text
   ordering a `write_memory` call. Nothing in the MCP protocol or FastMCP's tool-dispatch mechanism
   distinguishes "the user asked for this" from "a document the agent read asked for this."
2. **Engineered fake contradiction against a true existing record** — a poisoned document primes
   the agent to write content close enough to trigger a contradiction-check `UPDATE` verdict
   against a real record, archiving the truth and replacing it with attacker content. Inherits the
   contradiction-check's demonstrated weaknesses (above) wholesale unless independently mitigated.
3. **Repeated/automated write attempts, no rate limiting** — worse at the MCP layer than at the
   function-call layer, because a single poisoned document read once can drive retries across many
   turns and sessions, not just one call.
4. **Cross-session/cross-user persistence amplification** — a successful injected write is durable
   and retrievable in every future session, including sessions with no exposure to the original
   poisoned document — temporally unbounded blast radius versus a poisoned single-turn tool result.
5. **Metadata/parameter smuggling** — even a tool careful about the `content` field could be
   attacked through `memory_type` routing (e.g. into `memory_procedural`, which future agent
   behavior may treat as instructions) or any caller-settable parameter affecting retrieval ranking.

**The unforgeable-boundary question (`REFLECT-003`).** No purely code-level check in this
workspace has held up as an actual security boundary against a determined bypass — only live,
in-transcript human confirmation has, demonstrated on a directly analogous mechanism (the
Investigator-Authored Write Path's identity-enforcement layer, which survived three implementation
rounds before Dr. Wieczorek demonstrated the final round was still bypassable by calling the
persistence sink directly). Code-level checks are not discarded — they're retained as
defense-in-depth against careless/accidental misuse, just not treated as _the_ boundary. The
required confirmation must be genuine, live, in-transcript, from the real human, **never relayed
through an intermediary agent.**

**Resulting design position:** blocked-until-reviewed for high-consequence writes (sacred records,
anything that would silently overwrite/archive an existing record via a contradiction-style
verdict); write-then-quarantine-then-async-review for routine, non-colliding new-fact writes. A
design requiring synchronous human confirmation on _every_ write would defeat the tool's purpose;
this narrower design closes the injection hole for the high-consequence class while preserving
autonomous operation for the routine one. The workspace's `H-P01` prompt-optimization gate (a real
`PreToolUse`/`PostToolUse` hook pair, not a docstring instruction) was the structural-enforcement
precedent for how to make the human-facing gate binding rather than advisory.

**No-go verdict at the time**, with six checkable reversal conditions: (1) a genuinely human-facing,
structurally-enforced confirmation step for high-consequence writes, routine writes going through
write-then-quarantine-then-async-review instead; (2) if any write routes through a
contradiction-style judge, the four items the contradiction-check evaluation listed (production
judge implementation, confidence threshold/majority-vote, input-untrusted-data separation,
same-window sequencing) independently satisfied first; (3) real rate limiting and anomaly flagging,
not a documented gap; (4) non-optional provenance/metadata fields on every write, enforced in code;
(5) a fresh adversarial evaluation pass against the actual write-tool implementation; (6) all of
Decision 2's six constraints re-verified for the write tool's read-side behavior, not assumed to
carry over by inheritance.

**All six conditions were subsequently satisfied:** a write-capable `write_memory` tool was built
(five parallel workers), independently adversarially re-evaluated against the real merged code (not
a self-report), and activated. Result against the same five attack shapes, run against the actual
implementation: four fully mitigate; the fifth (direct instruction injection) was a **partial-
success finding** — a structurally-enforced confirmation hook existed but was not yet wired into
`.claude/settings.json`, leaving a marker-deletion bypass reachable via ordinary shell tool access.
That hook pair was subsequently wired and independently re-audited, closing the bypass for
sequential tool-call sessions. **One uncertainty remains open, honestly flagged rather than closed
by assumption:** whether `PreToolUse` hooks fire strictly sequentially for a _batched/parallel_ set
of tool calls within one assistant turn was never directly tested — if hooks can dispatch
concurrently, a narrower version of the bypass could theoretically reopen. A dedicated concurrency
test is recommended before treating this condition as unconditionally closed.

`write_memory` is registered and live as of 2026-08-10 (`AGENT_MEMORY_WRITE_TOOL_ENABLED=true`,
confirmed via live `ToolSearch` schema load and `health_check()`). The confirmation-hook pair and
this workspace's H-P01 write-confirmation flow both still apply to any actual write attempt —
registration is not the same as bypassing the confirmation gate for high-consequence writes.

Full build detail, independent adversarial evaluation, and activation status:
[2026-08-08-cc00-mcp-observability-stack/research-report.md](core-component-00/telescope/2026-08-08-cc00-mcp-observability-stack/research-report.md) § Related
Build.

### Self-review findings (design-stage audit, full record)

_Merged here from the retired `supporting/06-self-review-and-evaluation.md` — this is now the
authoritative citation._ Independent design-stage audit, Dr. Tomasz Wieczorek, 2026-07-10, covering
the complete design as a single proposal before implementation began.

**Requirement checklist:** all nine explicit CEO requirements were assessed **Met** or
**Conditionally Met** — benchmarking against top-tier memory architectures, a stated design
philosophy, storage types specified, deployment guidelines, a forgetting strategy emulating the
human brain, a visualized workflow, disaster-recovery coverage, and a self-review having been
conducted. "Accurate documentation and content" was assessed **Conditionally Met** (see below).

**Accuracy verification — partial, not independent re-derivation.** The review checked internal
consistency (every external claim traces to a named source — pass) and plausibility (cited
mechanisms consistent with the reviewer's general knowledge — pass), but did not independently
re-fetch and re-verify primary sources (open). Recommendation, still standing: spot-check the most
load-bearing figures (the memory-tool token-reduction claim, the Ebbinghaus decay-curve figure, the
Generative Agents importance-threshold value) before they inform a tuned production constant.

**Overall verdict at the time: conditionally ready for CEO sign-off**, with five pre-implementation
gates disclosed rather than hidden. Two were subsequently closed: the contradiction-check red-team
pass (closed negative, see below) and the resync-trigger question (folded into that same pass's
scope). **Three remain genuinely open, tracked in this report's Open Questions item 4:**
borderline-case worked examples for [01-technical-options.md](supporting/01-technical-options.md), a multimodal-specific security
review, and workflow-diagram coverage of deployment topology and disaster-recovery flow.

### Contradiction-check adversarial evaluation (full record)

_Merged here from the retired `supporting/07-adversarial-evaluation-results.md` — this is now the
authoritative citation for the finding._

**Independent audit:** Dr. Tomasz Wieczorek, Staff Safety & Evaluation Engineer, 2026-07-12,
against `check_contradiction()` (`context-engineering/implementations/memory_maintenance.py`).
Executable evidence: `context-engineering/testing/test_contradiction_adversarial.py` (16 tests).

**Structural finding:** `check_contradiction()` has almost no logic of its own — it forwards both
records' content verbatim to an injected `llm_judge` callable and returns whatever comes back,
checking only that the result is one of `ADD`/`UPDATE`/`NOOP`. No confidence threshold, no
symmetry check between call orders, no corroboration requirement, no input sanitization. No
production `llm_judge` implementation exists in this workspace, so the evaluation tested the
wrapper itself against synthetic judge stand-ins built to reproduce documented LLM-judge failure
modes (lexical-overlap sensitivity, entity blindness, instruction-following on embedded text,
order sensitivity) — proxies for known failure classes, not a claim about any specific model.

**Three questions tested, three positive findings:**

1. **False-`UPDATE` classification:** a curated set of 5 genuinely non-contradictory pairs (cosmetic
   restatements, different-subject/different-scope facts), run through a naive shared-keyword
   judge, produced a **100% false-positive rate (5/5)** — `check_contradiction()` applied **zero
   independent mitigation** across the full 7-pair set (2 controls both classified correctly, so the
   judge itself isn't a strawman). Also found: `check_contradiction(a, b)` and `check_contradiction(b, a)`
   can disagree under a plausible judge purely by call order — no symmetry check exists. Most
   concerning case: a judge firing on predicate overlap without checking subject identity would
   archive one user's fact because of an unrelated user's similarly-worded fact — a cross-subject
   memory-corruption path, not just an ordinary false positive.
2. **Memory-poisoning:** an `_instruction_following_judge` stand-in (simulating an LLM judge that
   complies with an embedded imperative rather than performing genuine comparison — the textbook
   prompt-injection failure mode) showed an embedded `"SYSTEM OVERRIDE: UPDATE ..."` instruction
   forces the verdict regardless of actual content, and a constructed case showed a true, unrelated
   fact can be archived via an engineered fake contradiction — per [03-forgetting-strategy.md](supporting/03-forgetting-strategy.md) § 5,
   an `UPDATE` verdict is the sole trigger for archival, with no corroboration step. 50 consecutive
   identical poisoning attempts all succeeded identically, with no rate limiting or anomaly flagging.
3. **Same-maintenance-window race (reproduces):** two independent new writes checked against the
   same stale existing record, in the same batch pass, both get classified `UPDATE` independently —
   nothing ever checks the two new writes against each other. Both survive as live, mutually
   contradictory active records. Confirmed structurally, not just as a scenario demo:
   `check_contradiction()`'s signature has no new-vs-new comparison capability even in principle, and
   `run_maintenance_pass()` never calls `check_contradiction()` under any flag combination — the race
   is unresolved by construction, not merely untested.

**Verdict: `i_have_completed_adversarial_review=True` should NOT be authorized.** None of these
findings are surprising given the structural read above — `check_contradiction()` was built,
correctly, as a thin, testable wrapper around an as-yet-unbuilt judge, not as a safety-complete
mechanism. The gate requiring sign-off before activation is doing exactly what it was designed to
do. **What would need to change before authorization:**

1. A concrete production `llm_judge` implementation, itself adversarially evaluated against at
   minimum the five false-positive patterns above, with a materially better than 100% failure rate.
2. A confidence threshold or second-judge/majority-vote step before an `UPDATE` verdict is trusted.
3. Input handling that treats memory content as untrusted data with respect to the judge call —
   structural separation of "content to compare" from "instructions to the judge."
4. A same-window sequencing mechanism (serialized checks with re-fetched candidacy, or an explicit
   new-vs-new comparison pass) before the batch design in [03-forgetting-strategy.md](supporting/03-forgetting-strategy.md) § 5 can be
   trusted not to produce the race above.

**Confirmed inert:** `i_have_completed_adversarial_review=True` is not set anywhere in production
or default code paths; `run_maintenance_pass()` still refuses `enable_contradiction_check=True`
without that flag (`RuntimeError`, unchanged). This evaluation informs the eventual activation
decision — it does not perform it.

---

## Recommendations

### Primary Recommendation

**Adopt the Memory-as-Corpus architecture in [supporting/01-technical-options.md](supporting/01-technical-options.md)** — three Qdrant
collections (`memory_episodic`, `memory_semantic`, `memory_procedural`) layered onto the existing
`workspace-knowledge` MCP server, backed by an append-only JSONL log as the durable source of
truth, with the decay/consolidation policy in [supporting/03-forgetting-strategy.md](supporting/03-forgetting-strategy.md) run as a
scheduled maintenance job per [supporting/02-deployment-guidelines.md](supporting/02-deployment-guidelines.md) §5.

### Secondary Recommendations

1. **Implement the maintenance job as a standalone, testable module** (not inline in the MCP
   server) so its decay formula can be unit-tested against synthetic memory records before
   production deployment, consistent with this module's existing test-suite discipline
   (`retrieval-augmented-generation/CLAUDE.md` — no merge without a green `pytest` suite).
2. **Instrument decay/consolidation telemetry from day one** — `dormant_ratio`,
   `last_consolidation_at`, and per-collection point counts ([02-deployment-guidelines.md](supporting/02-deployment-guidelines.md) §6) — so the
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

- [memory_store.py](core-component-00/framework/02-context-engineering/implementations/memory_store.py)
- [context_compressor.py](core-component-00/framework/02-context-engineering/implementations/context_compressor.py)
- [overview.md](core-component-00/framework/04-retrieval-augmented-generation/architecture/overview.md)
- [lightweight-rag-deployment.md](core-component-00/framework/04-retrieval-augmented-generation/deployment/lightweight-rag-deployment.md)
- [index-sync-hooks.md](core-component-00/framework/04-retrieval-augmented-generation/patterns/index-sync-hooks.md)
- [reference-table.md](core-component-00/framework/04-retrieval-augmented-generation/evaluation/reference-table.md)
- [supporting/00-sources-and-references.md](supporting/00-sources-and-references.md), [supporting/01-technical-options.md](supporting/01-technical-options.md),
  [supporting/02-deployment-guidelines.md](supporting/02-deployment-guidelines.md) (deployment; now also the DR-backup design, merged
  2026-08-10), [supporting/03-forgetting-strategy.md](supporting/03-forgetting-strategy.md), [supporting/04-workflow-diagrams.md](supporting/04-workflow-diagrams.md),
  [supporting/05-disaster-recovery-and-resilience.md](supporting/05-disaster-recovery-and-resilience.md) (this programme)
- § Architecture Decisions and Write-Path Security Posture above — full records merged 2026-08-10
  from the former standalone `supporting/06-self-review-and-evaluation.md`,
  `supporting/09-mcp-architecture-decision.md`, and `supporting/11-write-path-threat-model.md`, all
  retired
- [2026-08-08-cc00-mcp-observability-stack/research-report.md](core-component-00/telescope/2026-08-08-cc00-mcp-observability-stack/research-report.md) — the
  monitoring/observability design for all CC-00 MCP servers, including this server; also now holds
  the write-path tool's implementation/evaluation/activation record and (merged 2026-08-10 from the
  former standalone `supporting/10-observability-fix.md`, retired) this server's full incident
  history

### External Sources (all retrieved via live web search, 2026-07-10)

**Full bibliography with URLs and retrieval dates:** [supporting/00-sources-and-references.md](supporting/00-sources-and-references.md)
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
- **Separate investigation, same embedding infrastructure:**
  `core-component-00/telescope/2026-07-13-mcp-embedder-service-redesign/` — the persistent
  `embedder-service` this server's `search_memory`/`write_memory` route through when available. That
  investigation's own `supporting/implementation-plan.md` §4/§10 is the authoritative record of its
  adversarial/fault-injection evaluation, its `workspace-knowledge` migration, and its ASE
  ratification (Conditional verdict, two Required-level gaps tracked as harness-engineering
  backlog under exception EX-001). The two investigations have independent internal stage
  numbering — do not carry stage/phase numbers across them.

---

## Open Questions

1. **Are the decay/consolidation threshold defaults ([03-forgetting-strategy.md](supporting/03-forgetting-strategy.md) §6) correct for this
   workspace's actual session lengths and write frequency?**
   Status: Unvalidated — requires production telemetry. A synthetic (non-empirical) sanity check of
   the actual `compute_decay_weight`/`next_status`/`cumulative_salience` formulas against hand-picked
   inputs found the formulas behave as designed, but surfaced one coupling worth checking once real
   write-time importance scores exist: any record written with `importance < 0.5` is born `dormant`
   at t=0 (decay_weight at creation equals importance itself), so if the write-time importance
   heuristic commonly scores below 0.5, a large fraction of memory could enter the corpus already
   dormant — not necessarily wrong, but undiscussed elsewhere. This synthetic check does not close
   this question; real session data is still required.
   Priority: Medium
   Assigned: Follow-up investigation post-deployment.

2. **Does the LLM-judged contradiction check (Finding 4 / [03-forgetting-strategy.md](supporting/03-forgetting-strategy.md) §5) produce an
   acceptable false-positive rate for incorrectly archiving still-valid facts?**
   Status: **Adversarially tested (2026-07-12) — result negative.** `check_contradiction()` applied
   zero independent mitigation across a curated non-contradictory set (100% false-`UPDATE` rate),
   an engineered fake contradiction can archive a true unrelated fact (memory-poisoning reproduces),
   and the same-maintenance-window race (Open Question 3 below) also reproduces. Full method and
   findings: § Contradiction-Check Adversarial Evaluation (Full Record), above.
   `i_have_completed_adversarial_review` remains unset; the contradiction-check gate stays inert in
   production — this question is answered (negative), not closed as a to-do, and the gate should
   stay inert until the four conditions § Contradiction-Check Adversarial Evaluation (Full Record)
   lists (above) are independently satisfied.
   Priority: High
   Assigned: Closed by Dr. Tomasz Wieczorek's evaluation; re-open only if a production `llm_judge`
   is later built and needs its own pass.

3. **How does this design interact with the open Multi-Agent Memory Coherence research question
   (distributed shared memory without a central store)?**
   Status: Not addressed — this design assumes a single dedicated `qdrant-memory` instance
   ([01-technical-options.md](supporting/01-technical-options.md) §8), separate from the document knowledge base but still a single
   centralized store for memory itself, consistent with this workspace's current single-node
   deployment. It does not resolve the distributed case (multiple memory-owning nodes with no
   central store). A concrete instance of this open question already exists within the current
   single-instance design: because the contradiction check runs in a batch maintenance pass rather
   than synchronously at write time ([03-forgetting-strategy.md](supporting/03-forgetting-strategy.md) §5), two agents or sessions writing
   conflicting facts to `memory_semantic` in the same maintenance window could both be classified
   `ADD` against the same now-stale existing fact, producing two live contradictory records instead
   of one `UPDATE`. This does not require a distributed store to occur — it is a same-instance race
   condition — but it is the same underlying coordination problem this open question is about, and
   should be resolved together with it rather than treated as a separate concern later.
   Priority: Low (no current multi-node requirement), though the same-instance race condition above
   was included in Dr. Wieczorek's pre-production adversarial pass (§ Contradiction-Check
   Adversarial Evaluation below, which confirms this race reproduces) regardless of priority on the
   distributed question.
   Assigned: Mei-Ling Zhao, if/when that programme is next active.

4. **Three documentation gaps the design-stage self-review flagged as pre-implementation gates
   remain open** (see § Self-Review Findings above for the full audit; promoted here 2026-08-10 so
   they are tracked centrally rather than only inside that section):
   - A worked-example section for borderline "is this memory?" cases is still missing from
     [01-technical-options.md](supporting/01-technical-options.md) §3.
   - The pre-production adversarial pass never got a multimodal-specific extension — whether an
     image caption or audio transcript can leak more than the equivalent text memory would remains
     unassessed.
   - [04-workflow-diagrams.md](supporting/04-workflow-diagrams.md)'s three diagrams still don't cover deployment topology
     (`qdrant-memory` vs. `qdrant-workspace`) or the disaster-recovery/resync flow.
     Status: Open — none of the three have been closed by any later work in this investigation.
     Priority: Medium (documentation-only; none block current production use)
     Assigned: Unassigned — next engineer to touch the referenced sections should close the
     corresponding gap rather than treat it as settled.

---

## Version History

| Version | Date       | Author                                                 | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------- | ---------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-07-10 | Dr. Elias Vance                                        | Initial research report completed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 1.1     | 2026-07-12 | CEO                                                    | Reviewed briefing packet from all five contributors (Vance, Zhao, Almeida, Fontán, Wieczorek); signed off per Next Steps §1 User Approval Gate; implementation authorized                                                                                                                                                                                                                                                                                                                                                                                                   |
| 1.2     | 2026-07-12 | CEO                                                    | Signed off on P1 (telemetry instrumentation; Wieczorek's adversarial evaluation of the contradiction-check logic); live `qdrant-memory` instance provisioned with `memory_episodic`/`memory_semantic`/`memory_procedural` collections created and verified reachable                                                                                                                                                                                                                                                                                                        |
| 1.3     | 2026-08-10 | Dr. Elias Vance / Claude (CC-00 documentation steward) | Documentation-coherence pass per CEO directive: Open Questions 1–2 updated with 07/08's actual findings (previously stale); a new item 4 tracks 06's three still-open documentation gaps; new "Architecture Decisions and Write-Path Security Posture" section summarizes 09/11's still-governing decisions and verdicts; References updated to reflect 12's merge into [02-deployment-guidelines.md](supporting/02-deployment-guidelines.md), 13's move into the observability-stack report, 14's retirement, and 09's incident logs moving into `10-observability-fix.md` |
| 1.4     | 2026-08-10 | Claude (CC-00 documentation steward)                   | Per CEO directive to remove documents 06–11 from `supporting/`: 07 (already retired) and now 06, 09, 10, 11 retired outright. Full records merged in before deletion — 06's self-review and 09's architecture decisions and 11's threat model into this report's Architecture Decisions and Write-Path Security Posture section; 10's incident log into `2026-08-08-cc00-mcp-observability-stack/research-report.md`. All workspace references swept and redirected.                                                                                                        |

---

**Template Version:** 1.0
**Last Updated:** 2026-07-10
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
