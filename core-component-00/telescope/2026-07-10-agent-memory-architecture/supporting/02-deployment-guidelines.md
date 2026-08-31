# Deployment Guidelines — Persistent Agent Memory

> **Core Component 00 — Cross-Module Programme (Context Engineering × Retrieval-Augmented Generation)**
> **Parent Report:** [research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md)
> **Audience:** Engineers deploying or operating the memory system.
> **Last Updated:** 2026-08-10

---

## 1. Relationship to the Existing Lightweight RAG Deployment

The memory system reuses the same underlying retrieval technology as the document knowledge base
([lightweight-rag-deployment.md](core-component-00/framework/04-retrieval-augmented-generation/deployment/lightweight-rag-deployment.md)), but runs on **its own,
separate Qdrant instance** rather than sharing the document knowledge base's — see
[01-technical-options.md](01-technical-options.md) § 8 for why. What it reuses:

- The same rule that Qdrant must run in Docker/Server mode, never "embedded" mode — just on a
  **separate container** (`qdrant-memory`, `http://localhost:6335`), not `qdrant-workspace`
- The same in-process embedding approach (no standalone embedding step beyond the shared
  `embedder-service` process both systems now route through — see [01-technical-options.md](01-technical-options.md) § 4)
- The same idea of a multi-tier fallback if the primary search index is unavailable — though, as
  of this rewrite, only two of the document knowledge base's four tiers have actually been built
  for memory. See [05-disaster-recovery-and-resilience.md](05-disaster-recovery-and-resilience.md) § 3 for the honest current picture.
- The same `health_check` tool, extended with a memory-specific section rather than a second,
  separate health tool (§ 6)

**What it does _not_ reuse:** the document knowledge base's post-write "index sync hook" — a
background process that notices when a document file changed on disk and re-indexes it. Memory
doesn't need that, because every memory write already happens through a direct API call from the
agent itself; there's no separate file-change-detection problem to solve (§ 3).

### 1.1 Provisioning the Dedicated Memory Qdrant Instance (PowerShell)

```powershell
# Separate container and named volume from qdrant-workspace — different host ports
# to avoid colliding with the document knowledge base's 6333/6334 mapping.
docker run -d `
  --name qdrant-memory `
  -p 6335:6333 -p 6336:6334 `
  -v qdrant_memory_store:/qdrant/storage `
  qdrant/qdrant
```

```python
# Python client — connect to the dedicated memory instance
from qdrant_client import QdrantClient
client = QdrantClient(url="http://localhost:6335")
```

Same dependency pin as the document knowledge base: `qdrant-client>=1.7.0,<2.0.0`.

**A Windows-specific gotcha, discovered during provisioning (2026-07-12):** the Qdrant Python
client can fail with an obscure `502 Bad Gateway` error against `http://localhost:6335`, even
though the container is healthy and reachable by every other tool (PowerShell, `curl`, a plain
browser). The cause was a Windows proxy setting invisible to the usual `HTTP_PROXY` environment
variables, intercepting only this one library's connections. **Fix:** set `NO_PROXY=localhost,127.0.0.1`
(and the lowercase `no_proxy` variant) in the environment before creating the client — this has to
be set at the environment level; the client library provides no equivalent setting of its own.

---

## 2. Where the Data Actually Lives

```
core-component-00/context-engineering/memory/
├── episodic/
│   └── <session_id>.jsonl        ← append-only log, one file per session
├── semantic.jsonl                 ← append-only log, cross-session facts
├── procedural.jsonl               ← append-only log, runtime-learned corrections
├── reflection/
│   └── reflection-log.jsonl       ← append-only log, added after the original design (see 01-technical-options.md § 3)
└── memory-sync-state.json         ← tracks the last successful full rebuild per collection
```

Each line in a `.jsonl` file is one memory record, matching the schema in
[01-technical-options.md](01-technical-options.md) § 3.1. This mirrors the existing convention in the document knowledge
base's own server folder of keeping retrieval-adjacent state next to the code that uses it.

---

## 3. Write Path: A Direct Call, Not a Background Hook

The document knowledge base needs a background "index sync hook" because document writes happen
through the filesystem — someone edits a Markdown file directly — outside the retrieval server's
knowledge, so a separate watcher process has to notice the change. Memory is simpler: every memory
write already happens through a direct, explicit API call made by the agent itself
(`record_event`, `store`, `register`). There's no separate process boundary to cross, so the write
path can update the search index immediately, in the same call:

```
MemoryStore.record_event(...) / .store(...)
    → append one JSONL line (this is the permanent record)
    → embed the content (all-MiniLM-L6-v2, via the shared embedder process — 01-technical-options.md § 4)
    → upsert into the matching Qdrant collection
    → return to caller (single call, typically well under 100ms)
```

This path deliberately makes no AI-judgment call — `importance` comes from a cheap, rule-based
heuristic, not an AI decision, and the contradiction check ([03-forgetting-strategy.md](03-forgetting-strategy.md) §§ 3, 5)
is deferred to a separate batch pass rather than run on every write. Both of those would be too
slow to sit on the fast write path.

Because there's no separate background process, memory search results are **always consistent
with the very last write in the same session** — there's no window where a just-written memory
temporarily doesn't show up yet, unlike the bounded delay that's an accepted trade-off for document
search. Rebuilding all of a collection's points from its log file (e.g. after a Qdrant collection
was lost) uses the same batch path as the document knowledge base's own rebuild tooling.

**The sync-state file** (`memory-sync-state.json`) exists only to record the last successful full
rebuild time per collection — it is _not_ a hook-dispatch mechanism the way the document knowledge
base's equivalent file is:

```json
{
  "memory_episodic": { "last_rebuild_at": 0, "point_count": 0 },
  "memory_semantic": { "last_rebuild_at": 0, "point_count": 0 },
  "memory_procedural": { "last_rebuild_at": 0, "point_count": 0 }
}
```

---

## 4. Collection Creation (PowerShell)

```powershell
# Assumes the qdrant-memory container (§ 1.1) is already running — NOT qdrant-workspace
python -c @'
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6335")
for name in ["memory_episodic", "memory_semantic", "memory_procedural", "memory_reflection"]:
    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),  # all-MiniLM-L6-v2 dim
    )
'@
```

`size=384` matches the embedding model's output dimension. If the model is ever changed, this
value must be recomputed — Qdrant fixes a collection's vector size at creation time, so a change
means recreating the collection from scratch, not migrating it in place.

---

## 5. The Maintenance Job (Decay, Consolidation, Forgetting)

The forgetting strategy ([03-forgetting-strategy.md](03-forgetting-strategy.md)) needs a periodic pass over the data —
recomputing how much each memory has faded, promoting well-reinforced episodic clusters into
durable facts, archiving low-value records. This runs as a scheduled job, not something computed
fresh on every single agent turn — recalculating decay for the entire collection on every turn
would get slower as memory grows and add latency to every response for no benefit.

| Pattern                                                | When to Use                                                                                                                        |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| Session-scoped periodic pass (`ScheduleWakeup`-driven) | Development / a single long-running session — schedule roughly every 20–30 minutes                                                 |
| Cross-session scheduled job (`CronCreate`-driven)      | Production-style deployment — run about once per real-world day, echoing the sleep-consolidation cadence this design is modeled on |

Both trigger the same underlying maintenance routine — only what kicks it off differs. See
[03-forgetting-strategy.md](03-forgetting-strategy.md) § 5 for the routine's exact steps and thresholds, and
[00-sources-and-references.md](00-sources-and-references.md) § 6 for which of those steps are actually live in production today
(the contradiction-check step, specifically, is built but currently switched off — see that
section for why).

---

## 6. Observability

The memory system reports its health as an extra section of the workspace's existing
`health_check` tool — deliberately not a second, separate tool — reported **independently** from
the document knowledge base's own health fields, since the two Qdrant instances are fully
independent: a healthy document index says nothing about whether memory is healthy, and vice
versa.

| Field                                   | Description                                                                                                                                                                                 |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `memory_instance.reachable`             | Whether the memory Qdrant instance responded to a connectivity check                                                                                                                        |
| `memory_instance.point_counts`          | How many records are stored per collection (episodic, semantic, procedural, reflection)                                                                                                     |
| `memory_instance.last_consolidation_at` | Timestamp of the last maintenance pass (§ 5)                                                                                                                                                |
| `memory_instance.dormant_ratio`         | Fraction of records that have faded to "dormant" status — a rising number here without a matching rise in "archived" records is a sign the maintenance job isn't finishing its cleanup step |

**Added since the original design, and worth knowing about even though they weren't in the
original scope of this document:**

| Field                 | Description                                                                                                                                              |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `search_capability`   | Whether embedding requests are going through the shared `embedder-service` process or an in-process fallback, and whether that's degraded                |
| `write_rate_limiting` | Telemetry from the write-path rate limiter added when the write-capable memory tool shipped (see § 9 and the observability-stack report for full detail) |

Call `health_check` after any manual edit to a log file, after recreating a collection, or after
the first maintenance pass in a new deployment — the same discipline already used for the document
knowledge base. A document-instance outage and a memory-instance outage are two distinct
incidents with independent recovery steps, by design (§ 1).

---

## 7. Performance Targets

| Metric                                     | Target                             | Why                                                                               |
| ------------------------------------------ | ---------------------------------- | --------------------------------------------------------------------------------- |
| Memory write latency (95th percentile)     | Under 100ms                        | Must not be noticeable within a single agent turn                                 |
| Memory retrieval latency (95th percentile) | Under 600ms                        | Matches the document knowledge base's existing query-latency target               |
| Maintenance pass duration                  | Under 5 minutes per 10,000 records | Sized against the document knowledge base's own corpus-scale experience           |
| Sacred-record retrieval completeness       | 100%                               | A decision or commitment must never be silently excluded by a decay-driven filter |

These are the original design targets. They have not been re-measured against live production
traffic as part of this rewrite — that remains an open item (see [research-report.md](core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md) §
Open Questions).

---

## 8. Rollback

Because of the Memory-as-Corpus principle ([01-technical-options.md](01-technical-options.md) § 2), losing or corrupting a
Qdrant collection is always recoverable by replaying its log file through the same batch path used
in §§ 4–5 — never by trying to repair individual points inside Qdrant directly. This is the same
recovery posture already established for the document knowledge base, and needs no new tooling
beyond a log-replay script, which already exists.

---

## 9. Disaster Recovery — Backup Design (Disk-Level, JSONL Log)

> **Merged here 2026-08-10** from the former standalone `12-dr-backup-design.md`, per CEO
> direction that architectural-design content belongs alongside this document's other deployment
> guidance rather than as its own document. Content below is unchanged from that merge except for
> this note — it was already current and already written in accessible language.

### 9.1 What This Closes

§ 8's rollback guarantee (replay the log through the batch path) and
[05-disaster-recovery-and-resilience.md](05-disaster-recovery-and-resilience.md)'s zero-data-loss guarantee against Qdrant outages both
rest on one assumption neither document states outright: **the log file itself survives.** Neither
covers disk failure, accidental deletion, filesystem corruption, or losing the whole machine —
anything that destroys `core-component-00/framework/02-context-engineering/memory/` directly, the
one thing every Qdrant collection can be rebuilt from. This section designs the missing layer:
backing up the log file itself, off the single copy § 8's guarantee depends on existing at all.

**Data footprint at the time this was designed** (verified 2026-08-07): only the reflection log
had real content (9,616 bytes, 4 records); episodic memory was empty; semantic and procedural logs
didn't exist yet. No automated write path existed yet, so write volume was near zero — directly
relevant to the recovery targets below, both of which were sized for that reality. **This
assumption no longer holds as of 2026-08-10** — the write-capable memory tool has since shipped
and been turned on (§ 6 above; full detail in the observability-stack report's write-path section).
The targets below were not re-derived against live write volume as part of that change — see
§ 9.5, item 1.

**Scheduler choice:** this workspace's session-scoped scheduling tool was considered and rejected
— it dies when the authoring session ends and only fires while a chat is idle, which doesn't work
for a job that needs to run independently of any chat session. **Windows Task Scheduler** is used
instead.

### 9.2 Recovery Objectives (Proposed)

| Objective                              | Target         | Justification                                                                                                                                                                                      |
| -------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Maximum acceptable data loss**       | **24 hours**   | No automated write path existed at design time; write volume was near-zero and manual. Revisit now that an automated write path is live (§ 9.1).                                                   |
| **Maximum acceptable time to restore** | **15 minutes** | At the data volume observed at design time (~10 KB), replaying the log back into Qdrant takes under a second. The 15-minute figure is dominated by a human noticing the failure, not compute time. |

Distinct from — and additive to — [05-disaster-recovery-and-resilience.md](05-disaster-recovery-and-resilience.md) § 6's zero-data-loss /
immediate-recovery objectives, which cover a Qdrant outage _while the log file is still intact_.
This section's objectives cover the case where the log file itself is the thing that was lost.

### 9.3 The Four Design Components

1. **Backup mechanism** — `mcp-servers/agent-memory/scripts/backup_memory_log.py`. Copies the
   entire memory folder into a dated, timestamped snapshot directory under
   `mcp-servers/agent-memory/backups/snapshots/<UTC timestamp>/`. A plain file copy — no external
   dependency, no network call.
2. **Scheduler** — `mcp-servers/agent-memory/scripts/register_backup_task.ps1`. Registers a
   Windows Task Scheduler job that runs the backup script daily at 03:00. **Safety property:**
   defaults to a dry run — it prints what it _would_ register without actually registering
   anything. Only passing `-Activate` performs the real registration.
3. **Restore verification** — `mcp-servers/agent-memory/scripts/verify_backup_restore.py`. Takes
   the most recent snapshot, replays it into a disposable, clearly-named test collection per
   memory type (never a production collection), then compares the replayed record count against
   the snapshot's own record count. Reports a clean pass or names exactly what mismatched. Every
   test collection is deleted afterward regardless of outcome.
4. **Retention policy** — keeps the 14 most recent snapshots by default, deleting older ones
   automatically as part of the backup script.

### 9.4 Activation Status

| Component              | File                                | State                                                                                                                                              |
| ---------------------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backup mechanism       | `backup_memory_log.py`              | Written. Not scheduled, not run by anything automatically — only runs if someone runs it by hand.                                                  |
| Scheduler registration | `register_backup_task.ps1`          | Written, **dry-run by default**. No scheduled task exists just because this file exists. Requires a future, explicitly-authorized `-Activate` run. |
| Restore verification   | `verify_backup_restore.py`          | Written. Not scheduled, not run yet — there's no snapshot yet for it to check.                                                                     |
| Retention policy       | (built into `backup_memory_log.py`) | Written as inert logic — only takes effect once the backup script itself actually runs.                                                            |

No part of `core-component-00/platform/model-context-protocol-servers/agent-memory/server.py` was touched by this design —
these are standalone scripts only. A live connection to the memory server behaves identically
whether or not this design exists.

### 9.5 What Remains for a Future Activation Decision

1. Confirm the recovery targets in § 9.2 still make sense now that an automated write path is live
   and write volume is no longer near-zero (§ 9.1).
2. Decide on an off-machine backup target — this design deliberately covers only local-disk
   versioned snapshots; copying backups somewhere else is a separate future decision.
3. Only run `register_backup_task.ps1 -Activate` after explicit authorization — this design is the
   input to that future decision, not the decision itself.
4. Once activated, run `verify_backup_restore.py` at least once to confirm the very first real
   snapshot actually restores, before trusting the schedule alone.

Metrics for this backup mechanism, once activated, are already specified in the observability-
stack report's metrics catalog.

---

## References

| Resource                                                                  | Location                                                                                                                                             |
| ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Technical options (schema, models)                                        | [01-technical-options.md](01-technical-options.md)                                                                                                   |
| Forgetting strategy (decay, promotion)                                    | [03-forgetting-strategy.md](03-forgetting-strategy.md)                                                                                               |
| Disaster recovery (Qdrant-outage case, distinct from § 9's log-loss case) | [05-disaster-recovery-and-resilience.md](05-disaster-recovery-and-resilience.md)                                                                     |
| Implementation status audit (what's actually running)                     | [00-sources-and-references.md](00-sources-and-references.md) § 6                                                                                     |
| Lightweight RAG deployment                                                | [lightweight-rag-deployment.md](core-component-00/framework/04-retrieval-augmented-generation/deployment/lightweight-rag-deployment.md)                           |
| Replay mechanism, backing § 9's design                                    | [memory_vector_store.py](core-component-00/framework/02-context-engineering/implementations/memory_vector_store.py)                                   |
| Monitoring for the backup mechanism                                       | [2026-08-08-cc00-mcp-observability-stack/research-report.md](core-component-00/telescope/2026-08-08-cc00-mcp-observability-stack/research-report.md) |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Executing Engineers:** Mei-Ling Zhao (Context Engineering), Sofia Almeida & Diego Fontán (RAG)
**Last Updated:** 2026-08-10
