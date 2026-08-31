# Archive No. 0 — Sources and References Consulted

> **Core Component 00 — Cross-Module Programme (Context Engineering × Retrieval-Augmented Generation)**
> **Parent Report:** [research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md)
> **Audience:** CEO and anyone auditing the factual basis of this investigation. Written to be
> readable without an engineering background — jargon is defined on first use.
> **Last Updated:** 2026-08-12
> **Scope:** every external source consulted during the original 2026-07-10 investigation, plus
> the internal workspace documentation this design was required to build on. All external sources
> were retrieved via live web search on **2026-07-10** by a dedicated research subagent (see
> [research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md) § Methodology) — none are drawn solely from this investigator's training
> data.

---

## In Plain Terms

This document is a bibliography — a list of "where did we learn this from." When the lab designed
a memory system for AI agents (a way for an agent to remember facts, decisions, and past
conversations across sessions, instead of forgetting everything the moment a chat ends), it did
two kinds of homework first:

1. **Looked at how other AI companies and research teams solve the same problem** — Anthropic's
   own Claude, and three well-known open-source projects (MemGPT/Letta, Mem0, Zep). Nobody was
   copied wholesale; instead, one useful idea was borrowed from each.
2. **Looked at how _human_ memory actually works** — because the CEO's brief specifically asked
   for a memory system that behaves the way a human brain does: memories fade if unused, get
   reinforced by repetition, and important moments (like a firm decision) are remembered far
   longer than routine ones.

Every source below backs up a specific design choice made elsewhere in this research programme.
None of it was invented or guessed — it was retrieved by live web search on 2026-07-10 and is
cited inline wherever it's used.

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

**What this group was used for:** establishing that Anthropic's own memory tool is deliberately
simple — plain files, no vector search — and why this workspace needed something more
capable (`research-report.md` § Finding 1); and the "periodically expire unaccessed memory files"
guidance and "context rot" framing that justify having a forgetting mechanism at all
(§ 5 below, and [03-forgetting-strategy.md](03-forgetting-strategy.md) §§ 1–2).

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

**What this group was used for:** every one of these systems independently reinvented
"not all memories deserve equal weight" (`research-report.md` § Finding 2) and Zep/Graphiti's habit
of marking outdated facts superseded rather than deleting them (`research-report.md` § Finding 4).
[03-forgetting-strategy.md](03-forgetting-strategy.md) § 3 borrows Generative Agents' importance scoring, § 4 borrows its
reflection (consolidation) mechanism, and § 5 borrows Mem0's update-vs-duplicate decision and
Zep's mark-don't-delete pattern.

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

**What this group was used for:** this is the science that makes the memory system "emulate the
human brain" rather than just use a made-up decay schedule — the multi-store model and the
Ebbinghaus forgetting curve (§ 2 of [03-forgetting-strategy.md](03-forgetting-strategy.md)), the amygdala-driven "flashbulb
memory" effect that explains why decisions never fade (§ 3.1), sleep-dependent consolidation
(§ 4), and interference theory, which explains forgetting as something that happens _because new,
conflicting information arrived_ rather than merely because time passed (§ 5).

---

## 4. Internal Workspace Documentation Consulted

Not external sources, but the existing workspace documents this investigation was required to
build on rather than duplicate (a standing governance requirement — see
[agent-systems-governance-framework/governance/](core-component-00/framework/00-agent-systems-governance-framework/governance/)):

| Document                                                                                                                                | Role in This Investigation                                                                  |
| --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [memory_store.py](core-component-00/framework/02-context-engineering/implementations/memory_store.py)                                   | Existing four-memory-type model this design extends                                         |
| [context_compressor.py](core-component-00/framework/02-context-engineering/implementations/context_compressor.py)                       | Existing summarization primitive reused for consolidation                                   |
| [overview.md](core-component-00/framework/04-retrieval-augmented-generation/architecture/overview.md)                                   | Corpus-as-Source-of-Truth principle and Graceful Degradation Stack, extended by this design |
| [diagrams.md](core-component-00/framework/04-retrieval-augmented-generation/architecture/diagrams.md)                                   | Diagram convention followed in [04-workflow-diagrams.md](04-workflow-diagrams.md)           |
| [lightweight-rag-deployment.md](core-component-00/framework/04-retrieval-augmented-generation/deployment/lightweight-rag-deployment.md) | Existing Qdrant deployment-mode mandate this design must not violate                        |
| [index-sync-hooks.md](core-component-00/framework/04-retrieval-augmented-generation/patterns/index-sync-hooks.md)                       | Contrast case (document freshness) informing why memory's write path is simpler             |
| [core-component-00 telescope/CLAUDE.md](core-component-00/telescope/CLAUDE.md), [workspace telescope/CLAUDE.md](telescope/CLAUDE.md)    | Report shape and status-lifecycle conventions this programme follows                        |

---

## 5. Why a Custom Design, Not an Off-the-Shelf Framework

**Short version: nothing on the market was actually built for this workspace's problem, so a
custom design was assembled from the best individual idea in each system surveyed above,** rather
than adopting any one of them wholesale.

- **Anthropic's own Claude memory tool** (§ 1) is built for a single assistant remembering things
  for itself between its own resets. It's deliberately file-based, with no vector search — the
  right call for that narrower problem, but not enough for this workspace's actual need: a shared,
  searchable, cross-session team knowledge base that already exists and had to be extended, not
  replaced.
- **MemGPT/Letta, Mem0, and Zep** (§ 2) are each meant to be installed as a whole new system from
  scratch. This workspace already runs its own Qdrant-backed retrieval infrastructure
  (`retrieval-augmented-generation/`) — adopting any one of them wholesale would mean throwing
  away working infrastructure instead of extending it.
- **Generative Agents** (§ 2) is a research simulation, not a shippable product — its scoring and
  reflection ideas are genuinely useful, but there was no actual system to install, only a
  technique to borrow.

**What was actually taken from each, specifically:**

| Source                     | Idea Borrowed                                                                                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Anthropic's memory tool    | Memory must stay human-readable and editable — never an opaque, vector-only black box ([01-technical-options.md](01-technical-options.md) § 2, "Memory-as-Corpus") |
| Generative Agents          | Importance-weighted retention, so a significant memory survives longer than a routine one ([03-forgetting-strategy.md](03-forgetting-strategy.md) § 3)             |
| Mem0                       | Checking whether a new memory contradicts an existing one, and updating rather than duplicating ([03-forgetting-strategy.md](03-forgetting-strategy.md) § 5)       |
| Zep/Graphiti               | Never deleting outdated information outright — marking it superseded while keeping the record ([03-forgetting-strategy.md](03-forgetting-strategy.md) § 5)         |
| Human memory science (§ 3) | The forgetting/decay behavior itself — grounded in neuroscience, not in any of the surveyed tech systems                                                           |

This is the same reasoning already presented in `research-report.md` §§ Findings 1–2 and the
Executive Summary's Recommendation — it lives here too so it has one permanent, directly citable
home, instead of needing to be reconstructed from the findings narrative every time the question
comes up.

---

## 6. Design Mechanism Index — What Was Designed, and Is It Actually Running?

This table is the single most important part of this document. Every row was a decision already
specified somewhere else in this research programme — nothing here is a new decision. What's new
(2026-08-10) is the **Actually Running?** column: an engineering audit against the live codebase
and test suite, so this bibliography tells you not just "what was designed" but "is this real
today."

| #   | Mechanism                                 | Design Choice                                                                                                                                                                                                                                | Why (Rationale)                                                                                                                                                                                                                                | Precedent / Source                                                                                                                                                     | Specified In                                                                                                                                                                                                             | Actually Running? (audited 2026-08-10)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --- | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Memory scoring / retrieval**            | Two modes: recency-filtered (session + timestamp, no embedding) and semantic-similarity (Qdrant embedding + keyword search fusion, filtered to active records); decisions/commitments always included regardless of decay-driven status      | Matches the workspace's existing hybrid-retrieval standard; recency mode skips unnecessary embedding cost; the decision-bypass rule preserves a pre-existing contract in the codebase                                                          | RAG module's existing fusion logic; the decision-bypass rule is this workspace's own invariant, not literature-derived                                                 | [01-technical-options.md](01-technical-options.md) § 6                                                                                                                                                                   | **✅ Implemented as documented.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 2   | **Decay mechanism**                       | `decay_weight(t) = importance × e^(-Δt/strength)`, where `strength` grows with how often a memory has been retrieved                                                                                                                         | Emulates the Ebbinghaus exponential forgetting curve instead of a flat expiry timer; retrieval-driven strengthening reflects the "testing effect" from spaced-repetition research                                                              | Ebbinghaus curve / spaced repetition literature (§ 3, sources #31–32)                                                                                                  | [03-forgetting-strategy.md](03-forgetting-strategy.md) § 3                                                                                                                                                               | **✅ Implemented exactly as documented** — formula and every default constant (7-day base strength, 0.5 reinforcement per access, 0.5/0.15 thresholds) match the code verbatim (`memory_maintenance.py`).                                                                                                                                                                                                                                                                                                                                                     |
| 3   | **Importance mechanism**                  | Importance assigned 0.0–1.0 at write time by a cheap, rule-based heuristic (decision/commitment → 1.0, correction/preference → 0.7, routine → 0.2–0.3); decisions/commitments permanently exempt from decay                                  | Adapts Generative Agents' importance idea to something cheap enough to run on every write, since an AI-judged score per write would be too slow; the permanent-exemption rule is grounded in the amygdala/"flashbulb memory" literature        | Park et al. 2023 (§ 2, scoring concept only); PNAS/PMC amygdala literature (§ 3, sources #38–40)                                                                       | [03-forgetting-strategy.md](03-forgetting-strategy.md) §§ 3, 3.1                                                                                                                                                         | **✅ Implemented as documented.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 4   | **Consolidation (episodic → semantic)**   | Trigger: cumulative importance × access-count per session reaches 150; an AI summarization call distills the cluster into one new durable fact, with a record of which source events it came from; the originals are not deleted             | Models how the brain turns detailed episodic memory into general semantic knowledge during sleep; the 150 threshold is borrowed directly from Generative Agents' own tuned value, not independently derived                                    | Park et al. 2023 (§ 2); PMC/Springer sleep-consolidation literature (§ 3, sources #33, #35)                                                                            | [03-forgetting-strategy.md](03-forgetting-strategy.md) § 4                                                                                                                                                               | **✅ Implemented as documented.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 5   | **Contradiction / invalidation check**    | Checked in a periodic batch pass, not on every write: an AI judgment step classifies each new fact against similar existing ones as new / an update / a duplicate; an update marks the old record archived — never deletes it                | Implements interference theory (new information degrades recall of older, related memories) as an explicit, reviewable step rather than a silent overwrite; deferred to batch so the AI judgment call doesn't sit on the fast write path       | Mem0's update-decision logic (§ 2, source #19); Zep/Graphiti's mark-don't-delete pattern (§ 2, sources #22–23); interference theory (§ 3, sources #36–37)              | [03-forgetting-strategy.md](03-forgetting-strategy.md) § 5; [02-deployment-guidelines.md](02-deployment-guidelines.md) § 3                                                                                               | **⚠️ Built, but deliberately switched off.** The code exists and works in isolation, but a 2026-07-12 safety test found it flagged genuinely new facts as contradicting old ones 100% of the time — including two ways an attacker could exploit that to poison memory. It is gated behind a flag that a human must not yet set, and the maintenance job never calls it. See [research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md) § Contradiction-Check Adversarial Evaluation for the full test record. |
| 6   | **Status transition / forgetting**        | Three-stage ladder: active → dormant (weakened) → archived (excluded from all retrieval, 30-day grace period); a memory is never physically deleted automatically — that always requires a human to confirm it                               | The "weakened synapse, not yet pruned" analogy; this workspace prioritizes never losing data by accident over strict biological realism (real synaptic pruning isn't reversible — this design deliberately isn't that strict)                  | Closest real-world precedent is Zep's mark-don't-delete pattern; the never-automatic-deletion rule is a workspace safety policy, not something drawn from the research | [03-forgetting-strategy.md](03-forgetting-strategy.md) §§ 5–6; divergence flagged in `06-self-review-and-evaluation.md` § 4                                                                                              | **✅ Implemented as documented.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 7   | **Storage / corpus mechanism**            | An append-only plain-text log per memory type is the permanent record; the Qdrant search index is a derived copy that can always be rebuilt from that log ("Memory-as-Corpus")                                                               | Extends the workspace's existing "the document is the source of truth, the index is disposable" principle to memory, which otherwise has nothing else to rebuild from if the index were ever lost                                              | `retrieval-augmented-generation/architecture/overview.md` § 10; Anthropic's own file-based, auditable memory-tool philosophy (§ 1, sources #1, #8)                     | [01-technical-options.md](01-technical-options.md) § 2                                                                                                                                                                   | **✅ Implemented as documented** — and the codebase quietly added a fourth memory type on top of the three originally scoped here (**reflection memory**, its own log and Qdrant collection). Not a problem, just not something this original design anticipated; see [01-technical-options.md](01-technical-options.md) § 3 for the correction.                                                                                                                                                                                                              |
| 8   | **Deployment topology**                   | Memory runs on its own dedicated Qdrant instance, physically separate from the document knowledge base's instance                                                                                                                            | Isolates blast radius and workload (memory is written on nearly every turn; documents are written occasionally) and gives a harder security boundary, at the CEO's explicit direction favoring architectural rigor over short-term convenience | Workspace-specific decision — none of the five benchmarked frameworks address this question; not literature-derived                                                    | [01-technical-options.md](01-technical-options.md) § 8; [02-deployment-guidelines.md](02-deployment-guidelines.md) § 1                                                                                                   | **✅ Implemented as documented.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 9   | **Multimodal memory**                     | Images/audio get a `modality`/`media_ref` field; the model writes its own caption or transcript as the searchable text at write time; the raw file lives on disk, never embedded directly                                                    | Keeps the "the log is the source of truth" principle intact for non-text memories; avoids a wasteful round-trip through an external captioning tool when the model already has the media in view                                               | An external document-conversion tool was explicitly ruled out for this path — reserved for the separate document-knowledge-base pipeline                               | [01-technical-options.md](01-technical-options.md) § 3.2; security follow-up logged in [research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md) § Open Questions item 4 | **Not separately re-audited in this pass** — no change in status reported by the 2026-08-10 engineering audit; treat as unchanged from the original design intent pending its own review.                                                                                                                                                                                                                                                                                                                                                                     |
| 10  | **Disaster recovery / degradation stack** | Four-level fallback if the search index is unavailable: full hybrid search → an in-process backup index → keyword-only search over the raw log → a plain scan of the raw log; the plain-log write always succeeds regardless of index health | Extends the document-RAG module's existing multi-tier fallback design to memory; because the log is already the source of truth, the last-resort fallback exists for free                                                                      | Direct precedent: `architecture/overview.md` § 11; `evaluation/reference-table.md` § Orphaned Point Detection                                                          | [05-disaster-recovery-and-resilience.md](05-disaster-recovery-and-resilience.md)                                                                                                                                         | **⚠️ 3 of 4 levels exist; one (Tier 2) is not built.** See [05-disaster-recovery-and-resilience.md](05-disaster-recovery-and-resilience.md) § 3 for the full picture.                                                                                                                                                                                                                                                                                                                                                                                         |

---

## 7. Verification Status (Cross-Reference)

Per [research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md) § Self-Review Findings: this bibliography reflects what the research
subagent retrieved and what the Director cited — it has not been independently re-fetched and
re-verified against primary sources by the Safety & Evaluation reviewer. That remains an open item,
not resolved by this rewrite. See that section for the standing
recommendation to spot-check the most load-bearing figures (the memory-tool token-reduction claim,
the Ebbinghaus decay-curve figure, and the Generative Agents importance-threshold value) before
they inform a tuned production constant.

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Compiled from:** Research synthesis produced by the background research agent tasked for this
investigation (`research-report.md` § Methodology), rewritten 2026-08-10 with implementation-status
findings from a live codebase and git-history audit.
