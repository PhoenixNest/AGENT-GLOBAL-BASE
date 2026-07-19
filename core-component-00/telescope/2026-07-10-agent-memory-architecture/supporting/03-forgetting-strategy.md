# Forgetting Strategy — Human-Brain-Emulating Memory Decay for Qdrant-Backed Agent Memory

> **Core Component 00 — Cross-Module Programme (Context Engineering × Retrieval-Augmented Generation)**
> **Parent Report:** `../research-report.md`
> **Audience:** Engineers implementing the memory maintenance/consolidation job.
> **Last Updated:** 2026-07-10
> **Knowledge basis:** Human-memory-science citations below were retrieved via live web search on
> 2026-07-10 for this investigation (not solely from training-data recall); source URLs are
> inline. See `research-report.md` § Methodology for the full source list.

---

## 1. Why a Forgetting Strategy Is a Design Requirement, Not an Afterthought

A memory store with no forgetting mechanism degrades in exactly the way Anthropic's own context
engineering research warns against: as stored volume grows, retrieval precision falls even when
storage capacity does not run out, because low-value records dilute the signal for every semantic
query — the same "context rot" phenomenon Anthropic describes for context windows applies to a
memory corpus at retrieval time (Anthropic Engineering, "Effective context engineering for AI
agents," 2025-09-29, retrieved 2026-07-10). Anthropic's own memory-tool security guidance names
this directly: developers should "periodically expire unaccessed memory files" (Claude Developer
Platform, Memory tool docs, retrieved 2026-07-10). A CC-00 memory system without an explicit decay
policy would violate that guidance by construction.

The brief additionally requires the strategy to **emulate the human brain**. This document
therefore grounds every mechanism below in a specific, cited element of human memory science, and
cross-validates each against how the benchmarked SOTA architectures already implement an analogous
mechanism (`research-report.md` § Findings has the full comparison).

---

## 2. The Governing Model: Multi-Store Decay With Rehearsal-Strengthened Retention

**Human-memory basis:** the Atkinson–Shiffrin multi-store model separates sensory register,
short-term/working memory, and long-term memory, with transfer between stores driven by attention
and **rehearsal** (Wikipedia: Atkinson–Shiffrin memory model; SimplyPsychology, retrieved
2026-07-10). The Ebbinghaus forgetting curve shows retention decaying exponentially — roughly 50%
loss within 30 minutes, 70–80% within 24 hours absent reinforcement — and spaced repetition
(review at increasing intervals) counteracts this, with a 254-study meta-analysis finding
distributed practice outperforms massed practice by 10–30% (Whatfix; OmniSets, retrieved
2026-07-10).

**Direct system mapping:**

| Human Memory Concept                      | CC-00 Memory System Equivalent                                                                                                                                                                           |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sensory register                          | Not modeled — sub-turn signal has no persistence value                                                                                                                                                   |
| Short-term / working memory               | `WorkingMemory` (in-process, cleared every turn — `memory_store.py`)                                                                                                                                     |
| Long-term memory (attention + rehearsal)  | `memory_episodic` / `memory_semantic` Qdrant collections, entered via explicit `MemoryStore` writes (the "attention" step) and strengthened by retrieval (the "rehearsal" step, §3)                      |
| Ebbinghaus exponential decay              | `decay_weight` recomputed on an exponential curve (§3), not linear                                                                                                                                       |
| Spaced repetition strengthening retention | Each retrieval of a record resets/extends its decay curve (§3) — the "testing effect" analog already used by Generative Agents' recency-decay retrieval scoring (Park et al. 2023, retrieved 2026-07-10) |

---

## 3. Decay Formula

Each memory record's `decay_weight` (schema in `01-technical-options.md` §3.1) is recomputed by the
periodic maintenance job (`02-deployment-guidelines.md` §5), not on every read:

```
decay_weight(t) = importance × e^(-Δt / strength)

where:
  Δt       = time since last_accessed_at (or created_at if never accessed)
  strength = base_strength × (1 + access_count × reinforcement_factor)
```

- `importance` (0.0–1.0) is assigned at write time by a **lightweight heuristic keyed on
  `event_type`/write context** — not an LLM call — so that assigning it adds no latency beyond the
  embedding step already on the write path (`02-deployment-guidelines.md` §3, §7's <100ms p95
  target). Starting mapping: `decision`/`commitment` → `1.0` (see §3.1, sacred and non-decaying
  regardless); explicit user correction or stated preference → `0.7`; ordinary tool-result or
  observation → `0.2`–`0.3`. This adapts Generative Agents' LLM-scored 1–10 importance rating (Park
  et al. 2023, retrieved 2026-07-10) to a cheaper mechanism suited to a synchronous write path — the
  _scoring method_ is borrowed in spirit (importance as a first-class signal), not the _scoring
  cost_ (an LLM call per memory). A richer, LLM-judged importance reassessment is reserved for the
  batch consolidation pass (§4), which already makes an LLM call and is not latency-sensitive in
  the same way.
- `strength` grows with `access_count` — every retrieval of a record extends how long it resists
  decay before the next maintenance pass, directly implementing the spaced-repetition finding that
  reinforcement through retrieval (not just elapsed time) governs retention (Whatfix; OmniSets,
  retrieved 2026-07-10). This is the same principle Generative Agents encodes as an exponential
  recency term recomputed relative to "game hours since last accessed" with decay factor 0.995
  (Park et al. 2023, retrieved 2026-07-10); this system generalizes it with a per-record strength
  parameter instead of a single global decay factor, so frequently-retrieved facts decay slower
  than the global average rather than at a fixed population-wide rate.
- `reinforcement_factor` and `base_strength` are deployment-tunable constants (§6); no single
  correct value exists, mirroring the same "policy, not architectural invariant" conclusion the
  Retrieval Freshness Guarantees programme reached for document staleness
  (`patterns/index-sync-hooks.md`).

### 3.1 Sacred Exemption — the "Flashbulb Memory" Analog

Records with `sacred = true` (decisions/commitments, per `EpisodicMemory.SACRED_EVENT_TYPES` in
`memory_store.py`) are **exempt from this formula entirely** — `decay_weight` is pinned at `1.0`
and `status` remains `"active"` indefinitely. This is not merely a carry-over of the existing
sacred-context invariant; it has a direct human-memory analog: emotionally salient events undergo
amygdala-mediated priority consolidation, producing memories that are unusually resistant to
forgetting (the "flashbulb memory" effect) — mechanistically, amygdala activation via
noradrenergic/adrenal signaling biases the hippocampus toward prioritizing that event for long-term
consolidation and suppresses competing processing during the consolidation window (PNAS, "Making
lasting memories"; PMC, "Amygdala and prioritization of declarative memories," retrieved
2026-07-10). A user's explicit decision is this system's equivalent of a high-salience event —
importance is not merely high, it is maximal and non-decaying by design.

### 3.2 Local LLM Options for a Richer Importance Reassessment — Reference Only, Not Adopted

§3 notes that a richer, LLM-judged importance reassessment (beyond the write-time heuristic) was
considered as a possible future enhancement. This subsection records that discussion and the
resulting decision.

**Decision: deferred.** Given this workspace's current hardware capability (single RTX 4060, 8GB
VRAM, shared with the embedding model and document-RAG pipeline), the CEO has decided to forgo
introducing local-LLM-based importance scoring for the time being. The write-time heuristic in §3
remains the standing design — this subsection is reference material for if/when this decision is
revisited, not a specification of current or planned behavior.

**Options considered, for reference:**

| Option                                           | Fit for This Job                                                                                                                                                    | Note                                                                                                                   |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Kimi K2.6 14B (Q4_K_M, ~3.8GB VRAM)              | Already vetted for this hardware profile; lowest VRAM and fastest inference among models in the workspace's existing coding-model reference                         | Reuses already-validated infrastructure — no new model to vet — but sized for coding tasks, not classification/scoring |
| Smaller ~3B-class general-purpose instruct model | Better task-fit for a lightweight classification/scoring job (not code generation); smaller VRAM footprint than any option in the existing coding-focused reference | Not currently vetted in this workspace — would need its own evaluation pass if pursued later                           |

**Source and its limits:** these options were discussed against
`retrieval-augmented-generation/deployment/full-stack/reference/model-comparison-2026.md`, this
workspace's existing local-model reference for the RTX 4060 / i9-13900H hardware profile. That
document is scoped to coding tasks (HumanEval, SWE-bench), not the classification/summarization
jobs relevant here, and several of its named models/benchmarks fall outside independent
verification at the time of this discussion — treat its specific figures with that caveat if this
subsection is revisited.

**What this does not change:** the contradiction check (§5) and consolidation summarization (§4)
already make LLM calls in the batch maintenance pass — that was decided independently of this
subsection and is unaffected by it. This subsection is specifically about the _optional, not yet
adopted_ richer importance-reassessment enhancement, nothing else.

---

## 4. Consolidation — Episodic → Semantic Promotion

**Human-memory basis:** systems consolidation theory holds that hippocampally-dependent episodic
traces are gradually transformed into hippocampus-independent, neocortical representations,
substantially mediated by memory reactivation during sleep (slow-wave sleep, with coupled
cortical slow oscillations, thalamocortical spindles, and hippocampal sharp-wave ripples). This
transfer characteristically **strips contextual/episodic detail and yields gist-based, fact-like
semantic representation** (PMC, "Sleep-dependent consolidation model"; PMC, "Memory Consolidation";
Springer, "System consolidation during sleep," retrieved 2026-07-10).

**System mapping — the maintenance job's consolidation step:**

1. Scan `memory_episodic` records (scoped per session) with cumulative
   `importance × access_count` exceeding a threshold — directly modeled on Generative Agents'
   reflection trigger, which fires when the summed importance of recent records crosses 150,
   occurring roughly 2–3 times per simulated day (Park et al. 2023, retrieved 2026-07-10).
2. Synthesize the qualifying episodic cluster into a single distilled semantic fact via an LLM
   summarization call (reusing `ContextCompressor`'s summarization path,
   `context-engineering/implementations/context_compressor.py`), discarding session-specific detail
   and retaining the generalizable conclusion — this is the direct implementation of the
   detail-stripping, gist-forming episodic→semantic transformation cited above.
3. Write the result to `memory_semantic` with `consolidated_from` populated with the source
   episodic record IDs — preserving provenance exactly as Generative Agents' reflection objects
   store pointers back to the evidence records that produced them (Park et al. 2023, retrieved
   2026-07-10), and as this workspace's append-only telescope convention preserves history rather
   than overwriting it.
4. The source episodic records are **not deleted** at consolidation time — they transition toward
   normal decay (§3) independently. Consolidation creates a new semantic record; it does not
   destroy the episodic one. This mirrors standard consolidation theory's observation that some
   remote episodic detail can remain independently retrievable even after semantic consolidation
   (PMC, "Memory Consolidation," retrieved 2026-07-10) — consolidation is additive, not a
   move-and-delete operation.

Consolidation should run on the same maintenance cadence as decay recomputation (once per real-world
day is the recommended default — `02-deployment-guidelines.md` §5 — echoing the sleep-consolidation
cadence this mechanism is modeled on).

---

## 5. Forgetting — Status Transitions, Not Immediate Deletion

**Human-memory basis:** the better-supported account of everyday forgetting is **interference**,
not mere time-based decay — specifically **retroactive interference**, where new information
degrades retrieval of older, related memories (Wikipedia, "Interference theory"; SimplyPsychology,
"Proactive & Retroactive Interference," retrieved 2026-07-10). Forgetting is therefore modeled here
as something that happens _because new, conflicting information arrived_, not only because time
passed.

**System mapping — contradiction-driven invalidation before decay-driven archival:**

1. **Check for contradiction during the maintenance pass, not synchronously at write time.** A new
   `memory_semantic` fact is written immediately as `active` — the write path only embeds and
   upserts (`02-deployment-guidelines.md` §3); it does not block on a contradiction check, because
   that check requires an LLM judgment call and the write path's <100ms p95 target
   (`02-deployment-guidelines.md` §7) assumes embedding latency only. At the next maintenance pass
   (same cadence as decay recomputation and consolidation, §4), retrieve existing facts above a
   similarity threshold for every fact written since the last pass, and use an LLM judgment step to
   classify the relationship as one of `ADD` (genuinely new, no conflict) / `UPDATE` (supersedes an
   existing fact) / `NOOP` (duplicate, no action) — the same three-way decision Mem0's "Updater"
   makes over retrieved candidate memories (Dwarves Memo, "Mem0 breakdown," retrieved 2026-07-10).
   Deferring this check to batch trades a short window — bounded by the maintenance cadence —
   during which a newly-contradicted older fact may still be returned by retrieval, for a bounded
   write path. This is the same latency-vs-freshness trade already made explicit for document
   retrieval in this workspace (`patterns/index-sync-hooks.md` — staleness is "a policy decision,
   not an architectural invariant"), applied here to write-time correctness instead of read-time
   freshness.
2. **On `UPDATE`, invalidate — do not delete.** The superseded record's `status` is set to
   `"archived"` and it is excluded from active retrieval, but the record itself is retained in the
   JSONL log (`01-technical-options.md` §2, Memory-as-Corpus). This directly follows Zep/Graphiti's
   bi-temporal fact-invalidation model: rather than deleting a contradicted edge, its validity
   interval is closed (`t_invalid` set) while the fact remains queryable for historical/audit
   purposes, and only the currently-valid fact is returned for present-tense queries (Zep arXiv
   paper, arXiv:2501.13956; Neo4j blog, "Graphiti," retrieved 2026-07-10). This is retroactive
   interference implemented as an explicit, auditable state transition instead of silent
   overwrite — consistent with this workspace's append-only archival ethos
   (`telescope/CLAUDE.md` § Rules) and its git-safety convention against unconfirmed destructive
   operations.
3. **On decay alone (§3), transition through two soft states before any hard deletion is even
   possible:** `active → dormant` when `decay_weight` falls below `0.5` (excluded from default
   semantic retrieval but still directly queryable by ID — the "weakened synapse, not yet pruned"
   state); `dormant → archived` when `decay_weight` falls below `0.15` **and** the record has had
   no access for a configurable grace period (default 30 days) — fully excluded from all retrieval
   tiers, though still present in the JSONL log and therefore still recoverable.
4. **Hard deletion (physical removal from the JSONL log) is never automatic.** It requires an
   explicit operator-confirmed garbage-collection pass, consistent with this workspace's standing
   rule to escalate before irreversible operations. This is a deliberate, documented divergence
   from a literal biological analog (synaptic pruning is not human-reversible) in favor of the
   workspace's safety posture — noted explicitly in `06-self-review-and-evaluation.md` rather than
   left as a silent inconsistency.

---

## 6. Tunable Constants (Deployment Defaults)

| Constant                         | Default                                                    | Basis                                                                                                                                                                                                                           |
| -------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `base_strength`                  | 7 days                                                     | Order-of-magnitude anchor between Ebbinghaus's hours-scale initial decay and a persistent fact's intended cross-session lifespan                                                                                                |
| `reinforcement_factor`           | 0.5 per access                                             | Each retrieval extends effective strength by 50% — tunable; no canonical value exists in the cited literature, this is a deployment policy choice                                                                               |
| Dormant threshold                | `decay_weight < 0.5`                                       | Matches the "weakened, not gone" framing of interference-driven forgetting rather than a hard cliff                                                                                                                             |
| Archival threshold               | `decay_weight < 0.15` AND 30-day access grace period       | Conservative — errs toward retaining borderline records, consistent with §5's bias against irreversible loss                                                                                                                    |
| Reflection/consolidation trigger | cumulative `importance × access_count` ≥ 150 (per session) | Directly reused from Generative Agents' empirically-tuned threshold (Park et al. 2023, retrieved 2026-07-10) as a starting point; recalibrate against this workspace's actual session lengths after the first deployment period |

These are starting defaults, not validated thresholds — validating them against real session data
is listed as an open question in `research-report.md` § Open Questions.

---

## References

| Resource                                                                                | Role                                                                                        |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `research-report.md` § Findings                                                         | Full architecture-by-architecture benchmark comparison                                      |
| `01-technical-options.md` §2–3                                                          | Payload schema fields this document mutates (`decay_weight`, `status`, `consolidated_from`) |
| `context-engineering/implementations/memory_store.py`                                   | `SACRED_EVENT_TYPES`, existing sacred-context exemption this document extends               |
| `context-engineering/implementations/context_compressor.py`                             | Summarization primitive reused for consolidation (§4)                                       |
| Anthropic Engineering, "Effective context engineering for AI agents" (2025-09-29)       | Context rot / attention budget framing (§1) — retrieved 2026-07-10                          |
| Claude Developer Platform, Memory tool docs                                             | "Periodically expire unaccessed memory files" guidance (§1) — retrieved 2026-07-10          |
| Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (2023, ar5iv) | Importance scoring, recency decay, reflection mechanism (§3–4) — retrieved 2026-07-10       |
| Mem0 breakdown (Dwarves Memo)                                                           | ADD/UPDATE/DELETE/NOOP consolidation decision (§5) — retrieved 2026-07-10                   |
| Zep temporal knowledge graph paper (arXiv:2501.13956) / Neo4j Graphiti blog             | Bi-temporal fact invalidation (§5) — retrieved 2026-07-10                                   |
| Wikipedia, "Atkinson–Shiffrin memory model"; SimplyPsychology                           | Multi-store model (§2) — retrieved 2026-07-10                                               |
| Whatfix; OmniSets — Ebbinghaus curve / spaced repetition                                | Exponential decay, rehearsal strengthening (§2–3) — retrieved 2026-07-10                    |
| PMC, "Sleep-dependent consolidation model"; "Memory Consolidation"; Springer            | Episodic→semantic consolidation (§4) — retrieved 2026-07-10                                 |
| Wikipedia, "Interference theory"; SimplyPsychology                                      | Retroactive/proactive interference (§5) — retrieved 2026-07-10                              |
| PNAS, "Making lasting memories"; PMC, amygdala prioritization                           | Salience-weighted, non-decaying retention (§3.1) — retrieved 2026-07-10                     |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Executing Engineers:** Mei-Ling Zhao (Context Engineering), Sofia Almeida & Diego Fontán (RAG)
