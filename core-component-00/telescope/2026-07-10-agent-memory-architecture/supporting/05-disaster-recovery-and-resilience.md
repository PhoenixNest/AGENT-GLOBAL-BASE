# Disaster Recovery and Resilience — Persistent Agent Memory System

> **Core Component 00 — Cross-Module Programme (Context Engineering × Retrieval-Augmented Generation × Harness Engineering)**
> **Parent Report:** `../research-report.md`
> **Audience:** Engineers implementing the memory system's availability and recovery behavior.
> **Last Updated:** 2026-07-10
> **Coordinating leads:** Sofia Almeida / Diego Fontán (RAG — own the document-RAG Graceful
> Degradation Stack this design extends), Kwame Asante (Harness Engineering — error-boundary
> patterns), Dr. Elias Vance (Director).

---

## 1. Direct Answer: Does the Current Design Already Account for Performance and Stability?

**Performance — yes, already specified.** `02-deployment-guidelines.md` §7 sets explicit p95
targets (write <100ms, retrieval <600ms, maintenance pass <5 min per 10,000 points), and the
embedding model choice in `01-technical-options.md` §4 was made specifically for write-frequency
performance, not just retrieval quality.

**Stability under normal operation — yes, already specified.** Sacred-record completeness (100%,
never excluded by decay), never-automatic hard deletion, and the Memory-as-Corpus principle
(JSONL as source of truth) all already protect against _data-integrity_ instability.

**Stability under host/infrastructure failure — addressed in this document.** What happens if the
`qdrant-memory` container fails to start, crashes mid-session, or the host machine loses power
mid-write is specified below, extending the document knowledge base's existing answer to this
class of failure (the Graceful Degradation Stack,
`retrieval-augmented-generation/architecture/overview.md` §11) to the memory system as well.

---

## 2. Failure Mode Catalog

| Failure Mode                                      | Trigger                                                                       | Blast Radius Without Mitigation                                                                                                                                                                         |
| ------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Docker daemon fails to start on host/user machine | Windows update, resource exhaustion, WSL2 backend failure                     | Both `qdrant-workspace` and `qdrant-memory` unreachable — but they fail _independently_ per the dedicated-instance decision (`01-technical-options.md` §8), so one failing does not imply the other has |
| `qdrant-memory` container crash mid-session       | OOM kill, disk-full on the named volume, unhandled exception in Qdrant itself | All memory retrieval (episodic + semantic + procedural) loses its semantic-search layer                                                                                                                 |
| Corrupted named volume (`qdrant_memory_store`)    | Unclean shutdown, disk corruption                                             | Same as above, but persists across container restart until volume is rebuilt                                                                                                                            |
| Host machine reboot mid-write                     | Power loss, forced restart                                                    | A single in-flight write may be lost from Qdrant, but not from the JSONL log (§4)                                                                                                                       |
| Port conflict (`6335`/`6336` already bound)       | Another process claims the port before `qdrant-memory` starts                 | Container fails to start; identical failure mode to daemon failure from the memory system's perspective                                                                                                 |

---

## 3. Availability Strategy: Extending the Graceful Degradation Stack to Memory

The document-RAG Graceful Degradation Stack (`architecture/overview.md` §11) is the direct
precedent. Memory gets its own four-tier stack, running against the JSONL logs and the
`qdrant-memory` instance rather than the document corpus and `qdrant-workspace`:

```
[Tier 1] qdrant-memory semantic search + BM25 fusion        ← primary
    ↓ (fallback, qdrant-memory unreachable)
[Tier 2] In-process FAISS index, rebuilt from JSONL logs     ← hot standby
    ↓ (fallback, FAISS index not yet built or stale)
[Tier 3] BM25 keyword-only search directly over JSONL logs  ← warm standby
    ↓ (fallback, all indexes unavailable)
[Tier 4] Raw JSONL scan — no index required                  ← cold fallback
```

Tier 4 is **always available** without any additional engineering, for the same reason it's always
available for the document corpus: the Memory-as-Corpus principle (`01-technical-options.md` §2)
already guarantees the JSONL logs are plain text and the actual source of truth. This is the single
biggest advantage of that earlier design decision — it was made for rebuild/rollback reasons, but
it also happens to be exactly what a disaster-recovery cold-fallback needs, at no extra cost.

**Recency-filtered retrieval (`01-technical-options.md` §6) degrades trivially** — it never
required Qdrant to begin with when filtering is by `session_id` + `created_at`; a JSONL scan
satisfies it directly at any tier. Only semantic-similarity retrieval actually depends on which
tier is active.

---

## 4. Write-Path Resilience: JSONL Append Is Never Blocked by Qdrant

The write path in `02-deployment-guidelines.md` §3 already appends to the JSONL log **before**
embedding and upserting to Qdrant. This ordering, chosen originally for source-of-truth reasons, is
also the correct disaster-recovery ordering: **the JSONL append must never be made conditional on
Qdrant's availability.**

Revised write path under failure:

```
MemoryStore call
    → append JSONL line                              ← always succeeds (local disk write)
    → attempt embed + Qdrant upsert
        → success: done, fully synced
        → failure (qdrant-memory unreachable):
              mark record as pending in memory-sync-state.json
              return to caller normally — no error surfaced to the agent
```

**Result: RPO (recovery point objective) is zero.** No memory content is ever lost due to a
`qdrant-memory` outage — only its searchability at Tier 1 is delayed until resync (§5). This is a
direct, load-bearing consequence of the Memory-as-Corpus decision already made in
`01-technical-options.md` §2, not a new mechanism bolted on afterward.

`memory-sync-state.json` (`02-deployment-guidelines.md` §3) gains one additional field per
collection to track this:

```json
{
  "memory_episodic": {
    "last_rebuild_at": 0,
    "point_count": 0,
    "pending_resync_ids": []
  }
}
```

---

## 5. Self-Check and Resync Procedure (Runs Once Recovery Is Underway)

Directly modeled on the RAG module's existing **Orphaned Point Detection and Remediation**
framework (`retrieval-augmented-generation/evaluation/reference-table.md` § Orphaned Point
Detection), inverted: instead of detecting Qdrant points with no corresponding source (orphaned),
memory's recovery check detects **JSONL records with no corresponding Qdrant point** (unsynced).

| Step        | Action                                                                                                                                                                                                                                                                                                                |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Detect   | On `qdrant-memory` reconnect (health check succeeds after a prior failure), compare each collection's JSONL record count against its Qdrant `points_count`                                                                                                                                                            |
| 2. Identify | Any JSONL record ID in `pending_resync_ids` (§4), plus any record whose `created_at` is newer than the collection's `last_rebuild_at`, is a resync candidate                                                                                                                                                          |
| 3. Resync   | Batch embed + upsert all resync candidates — the same batch path already used for full rebuild-from-corpus (`02-deployment-guidelines.md` §4)                                                                                                                                                                         |
| 4. Verify   | Re-run the parity check; if `points_count` still doesn't match JSONL record count after resync, escalate rather than retry silently (mirrors the RAG module's "not detected automatically" caution for orphaned points — an unresolved mismatch after one resync attempt is a signal worth surfacing, not looping on) |
| 5. Clear    | Empty `pending_resync_ids` only after step 4 confirms parity                                                                                                                                                                                                                                                          |

This procedure runs automatically on reconnect detection — it does not require an operator to
notice the outage first, unlike the RAG module's parity check (which is currently triggered
manually or via `health_check` inspection). Given memory's write frequency is much higher than
document writes, waiting for an operator to notice would let the resync backlog grow
unnecessarily.

---

## 6. Recovery Objectives

| Objective                                 | Target                                                                                                                                                                                                                                                   | Basis                                                                                           |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| RPO (data loss)                           | Zero                                                                                                                                                                                                                                                     | JSONL append is unconditional on Qdrant availability (§4)                                       |
| RTO — degraded retrieval capability       | Immediate (next query)                                                                                                                                                                                                                                   | Tier 2–4 fallback requires no manual intervention (§3)                                          |
| RTO — full Tier-1 capability restored     | Bounded by resync batch duration — same order as the RAG module's 2–5 min corpus rebuild precedent (`architecture/overview.md` §11 Rollback Procedure), scaled to the pending-record count rather than full corpus size, so typically faster in practice | Resync only replays records written during the outage window, not the full collection           |
| Detection latency (outage → resync start) | Bounded by `health_check` polling interval — recommend ≤60s in production                                                                                                                                                                                | No existing precedent specifies this; workspace-specific recommendation, not literature-derived |

---

## 7. Operator Control Interface

Extends the existing `health_check` MCP tool's `memory_instance` block (`02-deployment-guidelines.md` §6)
with recovery-specific fields, and reuses the same five-operation control pattern already
established for the RAG module's index-sync hook (`patterns/index-sync-hooks.md` § Operator
Control Interface) rather than inventing a new interface shape:

| Operation                         | Effect                                                                                                                                             |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `status`                          | Report current tier, `pending_resync_ids` count per collection, last resync timestamp                                                              |
| `force-resync`                    | Manually trigger the resync procedure (§5) without waiting for automatic reconnect detection                                                       |
| `force-tier <N>`                  | Manually pin retrieval to a specific degradation tier — for testing the fallback stack without actually taking `qdrant-memory` down                |
| `set-mode auto` / `set-mode warn` | Same semantics as the RAG module's H-RAG02 hook — `auto` resyncs automatically on reconnect, `warn` surfaces a notice and waits for `force-resync` |

---

## 8. What This Document Does Not Change

This document adds a resilience layer around the mechanisms already finalized and indexed in
`00-sources-and-references.md` §6 (Design Mechanism Rationale) — it does not modify the memory
scoring, decay, importance, consolidation, or contradiction-handling mechanisms. A `qdrant-memory`
outage delays _when_ Tier-1 semantic scoring becomes available again; it does not change _how_
scoring, decay, or importance are computed once it is.

---

## References

| Resource                                                  | Location                                                                                                                    |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Graceful Degradation Stack (document RAG precedent)       | `core-component-00/retrieval-augmented-generation/architecture/overview.md` §11                                             |
| Orphaned Point Detection (inverted precedent for §5)      | `core-component-00/retrieval-augmented-generation/evaluation/reference-table.md` § Orphaned Point Detection and Remediation |
| Index Sync Hook operator interface (precedent for §7)     | `core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md` § Operator Control Interface                |
| Memory-as-Corpus principle (basis for zero-RPO guarantee) | `01-technical-options.md` §2                                                                                                |
| Write path and memory-sync-state.json                     | `02-deployment-guidelines.md` §3                                                                                            |
| Deployment topology (dedicated `qdrant-memory` instance)  | `01-technical-options.md` §8; `02-deployment-guidelines.md` §1                                                              |
| Design mechanism index                                    | `00-sources-and-references.md` §6                                                                                           |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Coordinating Leads:** Sofia Almeida & Diego Fontán (RAG), Kwame Asante (Harness Engineering)
