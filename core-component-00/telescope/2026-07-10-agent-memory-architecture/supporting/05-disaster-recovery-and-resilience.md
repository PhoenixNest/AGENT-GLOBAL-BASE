# Disaster Recovery and Resilience — Persistent Agent Memory System

> **Core Component 00 — Cross-Module Programme (Context Engineering × Retrieval-Augmented Generation × Harness Engineering)**
> **Parent Report:** [research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md)
> **Audience:** Written for a general audience, with implementation-level detail where it matters.
> **Last Updated:** 2026-08-12
> **Coordinating leads:** Sofia Almeida / Diego Fontán (RAG — own the document-search fallback
> design this extends), Kwame Asante (Harness Engineering — error-boundary patterns), Dr. Elias
> Vance (Director).

---

## 1. Direct Answer: Does the Current Design Already Account for Performance and Stability?

**Performance — yes, already specified.** [02-deployment-guidelines.md](02-deployment-guidelines.md) § 7 sets explicit speed
targets (write under 100ms, retrieval under 600ms, a full maintenance pass under 5 minutes per
10,000 records), and the embedding model chosen in [01-technical-options.md](01-technical-options.md) § 4 was picked
specifically for write speed, not just search quality.

**Stability under normal operation — yes, already specified and confirmed live.** A decision or
commitment is never excluded from search, hard deletion never happens automatically, and every
memory write is first saved to a plain-text log before anything else — all of this protects
against data getting quietly lost or corrupted during ordinary use, and all of it was directly
confirmed against the running code on 2026-08-10.

**Stability if the underlying infrastructure fails — the honest picture is in this document,
kept current.** What actually happens if the memory search database fails to start, crashes
mid-session, or the machine loses power mid-write is laid out below: three of the four designed
fallback tiers are live; one (Tier 2) is not built.

---

## 2. Failure Mode Catalog

| Failure Mode                                               | What Triggers It                                                      | Impact Without Any Mitigation                                                                                                                                                                                                       |
| ---------------------------------------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Docker fails to start on the host machine                  | Windows update, resource exhaustion, a virtualization backend failure | Both the document-search database and the memory database become unreachable — but because they're deliberately separate instances ([01-technical-options.md](01-technical-options.md) § 8), one failing doesn't mean the other has |
| The memory database crashes mid-session                    | Out-of-memory kill, disk full, an unhandled internal error            | All memory search (across every memory type) loses its ability to search by meaning                                                                                                                                                 |
| The memory database's storage volume is corrupted          | An unclean shutdown, disk corruption                                  | Same as above, but persists across a restart until the storage volume is rebuilt                                                                                                                                                    |
| The host machine reboots mid-write                         | Power loss, a forced restart                                          | A single in-flight write to the search index may be lost, but never from the plain-text log (§ 4)                                                                                                                                   |
| A network port the memory database needs is already in use | Another process claims the port first                                 | The database container fails to start — the practical effect is identical to the Docker-failure row above                                                                                                                           |

---

## 3. Availability Strategy: What's Actually Built, Not Just Designed

The document-search system has a real, working four-level fallback — if its primary search fails,
it steps down automatically through a backup index, then a keyword-only search, then a raw file
scan. Memory mirrors three of those four levels:

```
[Tier 1] Qdrant semantic search + keyword fusion         ← primary — LIVE
    ↓ (fallback if Qdrant is unreachable)
[Tier 2] In-process backup search index                   ← NOT BUILT
    ↓ (fallback if that's unavailable)
[Tier 3] Keyword-only search directly over the log files   ← LIVE, automatic
    ↓ (fallback if all indexes are unavailable)
[Tier 4] Read the raw log files directly / full rebuild     ← LIVE, via a manual or scripted replay
```

**Tier 3 falls through automatically.** `search_memory` detects a degraded Tier 1 — Qdrant
unreachable, timed out, or the embedder unavailable — via `QdrantMemoryIndex.search_with_status()`
(episodic/semantic/procedural) or `_search_reflection_with_status()` (reflection), and falls
through to `keyword_search_log()` / `keyword_search_reflection_log()`
(`engineering/context-engineering/implementations/memory_vector_store.py`,
`mcp-servers/agent-memory/server.py`) in the same call — no person or scheduled job has to notice
the outage first. This reuses the RAG module's own `bm25_score()` reference implementation
(`retrieval-augmented-generation/implementations/retrieval.py`) rather than a second BM25
implementation, and every `search_memory` response carries a `tier` field (1 or 3) so a caller or
operator can tell which one actually served a given result. Sacred (decision/commitment) record
completeness carries over automatically: Tier 3 applies the identical `status_in` filter Tier 1
applies, and a sacred record is already permanently pinned at `status="active"` by
`apply_decay()` (`memory_maintenance.py`) — there is no separate bypass to maintain.

`search_memory`'s `degraded` flag reflects the true state of Tier 1, not just whether a Qdrant
client was injected: `search_with_status()`/`_search_reflection_with_status()` report
`degraded=True` with a `reason` for a missing client or embedder, a connection error, a timeout,
or a malformed response alike — this is the signal Tier 3's automatic handoff depends on.

Tier 2 (an in-process backup search index) is not built.

**Why the "always available" cold-fallback still holds:** Tier 4 (reading the log files directly)
requires no extra engineering to exist, for the same reason it doesn't for the document-search
system — the Memory-as-Corpus principle ([01-technical-options.md](01-technical-options.md) § 2) already guarantees the log
files are plain text and are the actual source of truth. Tier 3 sits between Tier 1 and Tier 4 as
a second, real safety net.

**One thing that degrades gracefully without any extra work:** recency-filtered lookups (see
[01-technical-options.md](01-technical-options.md) § 6 — "what happened recently in this session?") never actually needed
Qdrant to begin with; they can always be satisfied by scanning the log files directly, at any
tier.

---

## 4. Write-Path Resilience: The Log Write Is Never Blocked by the Search Database

**This part was confirmed fully built and working, unchanged from the original design.** The write
path ([02-deployment-guidelines.md](02-deployment-guidelines.md) § 3) always appends to the plain-text log **before** it embeds
and updates the search index. That ordering — chosen originally just to keep the log as the source
of truth — turns out to be exactly the right ordering for disaster recovery too: **the log write
must never depend on whether the search database happens to be available.**

Write path if the search database is down:

```
MemoryStore call
    → append one line to the log file              ← always succeeds (this is a local disk write)
    → attempt to embed + update the search index
        → success: done, fully in sync
        → failure (search database unreachable):
              mark the record as pending in memory-sync-state.json
              return to the caller normally — the agent sees no error
```

**Result: zero data loss, guaranteed.** No memory content is ever lost because the search database
happened to be down — only its _searchability_ is delayed until a resync happens (§ 5). This is a
direct, load-bearing consequence of the Memory-as-Corpus decision made in
[01-technical-options.md](01-technical-options.md) § 2, not a separate mechanism bolted on afterward.

---

## 5. Self-Check and Resync — What Happens When the Database Comes Back

Modeled on the document-search module's own existing "find records the index is missing" check,
run in reverse: instead of finding search-index entries with no matching source document
(orphaned), memory's version finds **log records with no matching search-index entry**
(unsynced).

| Step        | What Happens                                                                                                                                                     |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Detect   | When the memory database reconnects successfully after a prior failure, compare each collection's log-file record count against its actual point count in Qdrant |
| 2. Identify | Any record flagged pending during the outage, plus anything newer than the collection's last known rebuild time, is a candidate to resync                        |
| 3. Resync   | Batch-embed and upload every candidate — the same batch process already used for a full rebuild                                                                  |
| 4. Verify   | Recheck the counts; if they still don't match after one resync attempt, flag it for a person to look at rather than silently retrying forever                    |
| 5. Clear    | Only clear the pending-record list once step 4 confirms everything matches                                                                                       |

This check runs automatically as soon as a reconnect is detected — it doesn't wait for a person to
notice the outage first, unlike the equivalent document-search check (which today is triggered
manually or by inspecting `health_check`). Given how much more often memory is written to than
documents are, waiting for someone to notice would let the backlog of un-synced records grow
unnecessarily.

---

## 6. Recovery Objectives

| Objective                                      | Target                                                                                                                                                                                                                      | Basis                                                                                     |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Maximum data loss (against a search-DB outage) | Zero                                                                                                                                                                                                                        | The log write never depends on the search database being available (§ 4) — confirmed live |
| Time to _some_ working search after an outage  | **Immediate — automatic, same call.** `search_memory` falls through to Tier 3 (keyword search over the log) the moment Tier 1 reports degraded; no reconnect wait, no manual rebuild needed just to keep answering queries. | Tier 3 (§ 3) — Tier 2 (in-process backup index) remains not built                         |
| Time to full primary search restored           | Bounded by how long the resync batch takes — roughly proportional to how many records were written during the outage, not the full collection size                                                                          | Resync only replays records from the outage window, not the whole collection              |
| How fast an outage is even noticed             | Bounded by how often `health_check` is polled — recommended at 60 seconds or less in production; a client of `search_memory` also sees it immediately via `degraded`/`tier` in every response                               | Workspace-specific recommendation; not drawn from external precedent                      |

---

## 7. Operator Control Interface

Extends the memory-specific section of the workspace's existing `health_check` tool
([02-deployment-guidelines.md](02-deployment-guidelines.md) § 6) with recovery-specific fields, reusing the same operator
command shape already established for the document-search module's own equivalent, rather than
inventing a new one:

| Command                           | What It Does                                                                                                                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `status`                          | Reports current tier, how many records are pending resync per collection, and when the last resync happened                                                                           |
| `force-resync`                    | Manually starts the resync process (§ 5) without waiting for automatic reconnect detection                                                                                            |
| `force-tier <N>`                  | Manually pins retrieval to a specific tier, for testing — **note: Tiers 1, 3, and 4 are built and live; pinning to Tier 2 (in-process backup index) still has no effect — not built** |
| `set-mode auto` / `set-mode warn` | `auto` resyncs automatically on reconnect; `warn` raises a notice and waits for a manual `force-resync` instead                                                                       |

---

## 8. What This Document Does Not Change

This document adds a resilience layer around the mechanisms already specified in
[00-sources-and-references.md](00-sources-and-references.md) § 6 (the full design-mechanism index) — it doesn't change how
memory is scored, decays, gains importance, consolidates, or (once re-enabled) checks for
contradictions. A search-database outage only delays _when_ meaning-based search is available
again; it doesn't change _how_ scoring, decay, or importance are calculated once it is.

---

## References

| Resource                                                                                             | Location                                                                                                                    |
| ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Document-search fallback design (the precedent this extends)                                         | `core-component-00/framework/04-retrieval-augmented-generation/architecture/overview.md` § 11                                            |
| Orphaned-record detection (inverted precedent for § 5)                                               | `core-component-00/framework/04-retrieval-augmented-generation/evaluation/reference-table.md` § Orphaned Point Detection and Remediation |
| Operator command interface (precedent for § 7)                                                       | `core-component-00/framework/04-retrieval-augmented-generation/patterns/index-sync-hooks.md` § Operator Control Interface                |
| Memory-as-Corpus principle (basis for the zero-data-loss guarantee)                                  | [01-technical-options.md](01-technical-options.md) § 2                                                                      |
| Write path and the sync-state file                                                                   | [02-deployment-guidelines.md](02-deployment-guidelines.md) § 3                                                              |
| Deployment topology (dedicated memory database instance)                                             | [01-technical-options.md](01-technical-options.md) § 8; [02-deployment-guidelines.md](02-deployment-guidelines.md) § 1      |
| Full implementation-status audit (what's actually built, mechanism by mechanism)                     | [00-sources-and-references.md](00-sources-and-references.md) § 6                                                            |
| Disk-level backup design (the JSONL-log-loss case, distinct from this document's Qdrant-outage case) | [02-deployment-guidelines.md](02-deployment-guidelines.md) § 9                                                              |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Coordinating Leads:** Sofia Almeida & Diego Fontán (RAG), Kwame Asante (Harness Engineering)
