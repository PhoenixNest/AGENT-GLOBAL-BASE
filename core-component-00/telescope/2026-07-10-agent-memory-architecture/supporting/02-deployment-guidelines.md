# Deployment Guidelines — Persistent Agent Memory

> **Core Component 00 — Cross-Module Programme (Context Engineering × Retrieval-Augmented Generation)**
> **Parent Report:** `../research-report.md`
> **Audience:** Engineers deploying the memory system into the existing `workspace-knowledge` MCP
> server / lightweight RAG retrieval component.
> **Last Updated:** 2026-07-10

---

## 1. Relationship to the Existing Lightweight RAG Deployment

The memory system reuses the **retrieval engineering principles** of the lightweight RAG
deployment described in `retrieval-augmented-generation/deployment/lightweight-rag-deployment.md`,
but runs on **its own dedicated Qdrant instance**, physically separate from the document
knowledge base's `qdrant-workspace` container — per `01-technical-options.md` §8, this is a
deliberate architectural boundary (blast radius, workload isolation, security boundary), not a
shared-instance convenience. It reuses:

- The same Qdrant deployment mode mandate (Docker/Server mode only, never embedded) — on a
  **separate container** (`qdrant-memory`, `http://localhost:6335`), not `qdrant-workspace`
- The same embedding-in-process architecture (no standalone embedding service)
- The same four-tier graceful degradation stack (Qdrant → FAISS → BM25 → raw scan), instantiated
  independently against the memory instance
- The same `health_check` MCP tool _pattern_ for observability — extended to report against both
  instances (see §6)

It does **not** reuse the H-RAG02 post-write hook mechanism as-is — memory has a materially
simpler freshness problem than document RAG, addressed in §3 below.

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

Same dependency pin as the document knowledge base: `qdrant-client>=1.7.0,<2.0.0`
(`lightweight-rag-deployment.md`).

---

## 2. Directory Layout

```
core-component-00/context-engineering/memory/
├── episodic/
│   └── <session_id>.jsonl        ← append-only log, one file per session
├── semantic.jsonl                 ← append-only log, cross-session facts
├── procedural.jsonl               ← append-only log, runtime-learned corrections
└── memory-sync-state.json         ← shared state file (mirrors rag-sync-state.json contract)
```

Each `.jsonl` line is one payload record matching the schema in `01-technical-options.md` §3.1. This
mirrors the existing `core-component-00/mcp-servers/workspace-knowledge/rag-system/` convention of
keeping retrieval-adjacent state next to the server implementation, not scattered into module
`fundamentals/` or `patterns/` folders.

---

## 3. Write Path: Synchronous Upsert, Not a Post-Write Hook

The H-RAG02 pattern (`patterns/index-sync-hooks.md`) exists because **document** writes happen
through the filesystem, outside the retrieval server's control, so a separate hook process must
detect them. Memory writes are different: every memory write already happens through an explicit
`MemoryStore` API call (`record_event`, `store`, `register`) made by the agent runtime itself. The
write path can therefore embed the index update directly — no separate hook process, no debounce,
no state-file IPC problem:

```
MemoryStore.record_event(...) / .store(...)
    → append JSONL line (source of truth)
    → embed content (all-MiniLM-L6-v2, per 01-technical-options.md §4)
    → client.upsert(collection_name=<type collection>, points=[point])
    → return to caller (single synchronous call, typical latency <50ms per 01-technical-options.md §4 model choice)
```

This path is deliberately embedding-only — no LLM call sits on it. `importance` is assigned by a
write-time heuristic, not an LLM judgment, and the Mem0-style contradiction check is deferred to
the batch maintenance pass rather than run synchronously here (`03-forgetting-strategy.md` §3, §5)
— both are LLM-call-dependent and would otherwise put the §7 <100ms p95 write target out of reach.

This makes memory retrieval **always consistent with the last write in the same session** — the
staleness problem the Retrieval Freshness Guarantees programme resolved for documents
(`patterns/index-sync-hooks.md` — bounded by hook debounce) does not exist for memory, because
there is no separate process boundary to cross. Bulk/replay scenarios (e.g., rebuilding all
`memory_semantic` points from `semantic.jsonl` after a Qdrant collection loss) use the same
`rebuild_index`-style batch path already implemented for the document corpus.

**Memory-sync state file** (`memory-sync-state.json`) exists only to record the last successful
batch-rebuild timestamp per collection — it is not a hook dispatch mechanism like
`rag-sync-state.json`:

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
# Assumes the qdrant-memory container (§1.1) is already running — NOT qdrant-workspace
python -c @'
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6335")
for name in ["memory_episodic", "memory_semantic", "memory_procedural"]:
    client.create_collection(
        collection_name=name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),  # all-MiniLM-L6-v2 dim
    )
'@
```

`size=384` matches `all-MiniLM-L6-v2`'s output dimension (01-technical-options.md §4). If a different
embedding model is substituted, recompute this value — Qdrant collections are dimension-fixed at
creation and require a full recreate (not a migration) to change.

---

## 5. Consolidation / Decay Maintenance Job

The forgetting strategy (`03-forgetting-strategy.md`) requires a periodic maintenance pass —
recomputing `decay_weight`, promoting episodic → semantic, archiving low-salience records. Deploy
this as a scheduled job, not an inline per-turn computation (recomputing decay for the entire
collection on every turn would scale linearly with memory size and add latency to every agent
response). Two supported invocation patterns in this workspace:

| Pattern                                                | When to Use                                                                                                                            |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `ScheduleWakeup`-driven periodic pass (session-scoped) | Development / single long-running session — schedule at 1200–1800s intervals                                                           |
| `CronCreate`-driven scheduled agent (cross-session)    | Production-style deployment — run once per real-world day, mirroring the sleep-consolidation cadence in `03-forgetting-strategy.md` §2 |

Both invoke the same underlying maintenance routine — only the trigger differs. See
`03-forgetting-strategy.md` §5 for the routine's exact steps and thresholds.

---

## 6. Observability

Extend the existing `health_check` MCP tool response (do not create a second health-check tool)
with a distinct `memory_instance` block, reported **separately** from the existing document
knowledge-base fields — the two instances are independent and must never be collapsed into a
single combined status, since a healthy `qdrant-workspace` says nothing about `qdrant-memory`'s
health or vice versa (§1):

| Field                                   | Description                                                                                                                                                         |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `memory_instance.reachable`             | Whether `qdrant-memory` (`http://localhost:6335`) responded to a connectivity check                                                                                 |
| `memory_instance.point_counts`          | Per-collection point count (`memory_episodic`, `memory_semantic`, `memory_procedural`)                                                                              |
| `memory_instance.last_consolidation_at` | ISO 8601 UTC timestamp of the last maintenance pass (§5)                                                                                                            |
| `memory_instance.dormant_ratio`         | Fraction of points with `status = "dormant"` — a rising ratio without a corresponding `archived` increase signals the maintenance job is not completing its GC step |

Call `health_check` after any manual JSONL edit, collection recreate, or after the first
maintenance pass in a new deployment, mirroring the existing parity-check discipline in
`lightweight-rag-deployment.md` §Observability. A `qdrant-workspace` outage and a `qdrant-memory`
outage are now distinct incidents with independent recovery procedures — this is the direct
operational consequence of the dedicated-instance decision in §1, accepted deliberately rather
than left implicit.

---

## 7. Performance Targets

| Metric                               | Target                   | Rationale                                                                                                               |
| ------------------------------------ | ------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Memory write latency (p95)           | <100ms                   | Must not be perceptible within a single agent turn (embed + upsert, all-MiniLM-L6-v2)                                   |
| Memory retrieval latency (p95)       | <600ms                   | Matches existing RAG query latency target (`lightweight-rag-deployment.md`)                                             |
| Maintenance pass duration            | <5 min per 10,000 points | Bounded by corpus-scale precedent (7,793 points seeded in Phases 1–3, `lightweight-rag-deployment.md` §Windows 11 Note) |
| Sacred-record retrieval completeness | 100%                     | `sacred = true` records must never be excluded by a decay-driven filter (01-technical-options.md §6)                    |

---

## 8. Rollback

Because memory follows the Memory-as-Corpus principle (`01-technical-options.md` §2), any Qdrant
collection loss or corruption is recoverable by replaying the corresponding `.jsonl` log through
the same batch path used in §4/§5 — never by attempting point-level repair inside Qdrant. This is
the same rollback posture already established for the document corpus
(`architecture/overview.md` §10) and requires no new tooling beyond a JSONL replay script.

---

## References

| Resource                               | Location                                                                                                     |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Technical options (schema, models)     | `../supporting/01-technical-options.md`                                                                      |
| Forgetting strategy (decay, promotion) | `../supporting/03-forgetting-strategy.md`                                                                    |
| Lightweight RAG deployment             | `core-component-00/retrieval-augmented-generation/deployment/lightweight-rag-deployment.md`                  |
| Index Sync Hook pattern (contrast)     | `core-component-00/retrieval-augmented-generation/patterns/index-sync-hooks.md`                              |
| RAG sync state schema (contrast)       | `core-component-00/retrieval-augmented-generation/deployment/lightweight/reference/rag-sync-state-schema.md` |

---

**Maintained by:** Core Component 00 Laboratory
**Laboratory Director:** Dr. Elias Vance
**Executing Engineers:** Mei-Ling Zhao (Context Engineering), Sofia Almeida & Diego Fontán (RAG)
