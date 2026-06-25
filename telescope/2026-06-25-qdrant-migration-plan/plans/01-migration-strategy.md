# Qdrant Migration Strategy

**Document Type:** Migration Planning Deliverable
**Investigation:** `2026-06-25-qdrant-migration-plan`
**Author:** Dr. Elias Vance — CC-00 Laboratory Director
**Date:** 2026-06-25
**Status:** Approved — Phase 0 Active

---

## 1. Migration Philosophy

This workspace is a **markdown-first, corpus-as-source-of-truth system**. Every search index —
whether FAISS or Qdrant — is a derived artifact that can be fully rebuilt from the `.md` files
at any time. This means migration risk is structurally lower than in a classical database
migration: there is no data to "move," only index representations to rebuild and validate.

The migration proceeds in four phases. Each phase gate has explicit go/no-go criteria. The
existing FAISS stack is **permanently retained** — it serves as the disaster-recovery fallback
at every phase and is never removed from the codebase.

---

## 2. Corpus Size Trigger Threshold

Migration becomes materially worthwhile when incremental Qdrant upserts are measurably faster
than full FAISS rebuilds. The thresholds (in order of priority):

| Trigger                      | Condition                                                             | Rationale                                                |
| ---------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------- |
| **Primary (practical)**      | `rebuild_index` call takes >10 seconds perceptibly                    | User-observable latency on H-RAG02 auto-trigger          |
| **Secondary (volumetric)**   | Workspace `.md` file count exceeds 500, or chunk count exceeds 10,000 | FAISS full re-encode of 10K chunks on RTX 4060 ≈ 15–30 s |
| **Strategic (CEO override)** | CEO authorises Phase 1 regardless of scale                            | Invest in readiness before urgency                       |

At current corpus scale (~hundreds of `.md` files, estimated 2,000–5,000 chunks), neither
primary nor secondary threshold is met. Phase 1 can be entered on strategic trigger or when
either threshold is reached.

---

## 3. Migration Phases

### Phase 0 — Foundation (Current State)

**Status:** In progress
**Deliverable:** H-RAG02 hook + `/rag-sync` toggle (specified in
`plans/05-hook-design.md`)

- H-RAG02 calls `rebuild_index` (full FAISS rebuild) on qualifying doc writes
- `/rag-sync` toggle controls `auto` / `warn` / `off` modes
- FAISS mtime-based delta detection handles cross-session freshness at startup
- **No Qdrant dependency yet**

**Exit criteria:** H-RAG02 implemented and verified; `/rag-sync` custom command working.

---

### Phase 1 — Shadow Mode (Qdrant Writes, FAISS Reads)

**Trigger:** Any one corpus trigger met, or CEO strategic override.

**Objective:** Validate Qdrant on this hardware without risking production search quality.

**Architecture:**

```
Write path:  Doc edit → H-RAG02 →  ① rebuild_index (FAISS, primary)
                                    ② upsert_document (Qdrant, shadow — writes only)

Read path:   search_docs → FAISS (reads primary)
             Qdrant results logged for quality comparison only
```

**Actions:**

1. Install Docker Desktop for Windows and start the Qdrant container (see `02-deployment-guide.md` §3)
2. Install `qdrant-client>=1.7.0` in `.venv` (see `02-deployment-guide.md` §4)
3. Add `SEARCH_BACKEND=faiss` environment variable (Qdrant shadow writes only)
4. Seed initial Qdrant collection from existing corpus (see `03-initialization-guide.md`)
5. Validate Qdrant MRR against FAISS MRR on a representative query set
6. Monitor for Docker and Windows 11 compatibility issues (see `04-monitoring-guide.md`)

**Duration:** Minimum 2 weeks of shadow operation.

**Exit criteria (go to Phase 2):**

- Qdrant MRR ≥ FAISS MRR (within 5% tolerance)
- No Windows 11 embedding or storage compatibility issues
- Shadow upsert latency < 5 s per file
- Zero data loss in Qdrant collection (point count matches corpus chunk count)

---

### Phase 2 — Qdrant Primary, FAISS Standby

**Trigger:** Phase 1 exit criteria met.

**Objective:** Switch reads to Qdrant while keeping FAISS as a hot DR fallback.

**Architecture:**

```
Write path:  Doc edit → H-RAG02 →  ① upsert_document (Qdrant, primary)
                                    ② rebuild_index (FAISS, DR standby)

Read path:   search_docs → Qdrant (primary)
             SEARCH_BACKEND=faiss → immediate fallback to FAISS
```

**Actions:**

1. Set `SEARCH_BACKEND=qdrant` in MCP server config
2. Adapt H-RAG02 to call `upsert_document` (Qdrant incremental) as primary action;
   retain `rebuild_index` call for FAISS DR parity
3. Verify all 10 existing MCP tools continue functioning (search_docs, check_adr_precedent, etc.)
4. Reduce H-RAG02 debounce threshold from 30 s to 10 s (upsert is faster than full rebuild)
5. Monitor search quality and latency via monitoring guide

**Rollback trigger:** Any of — MRR drops >10% vs. Phase 1 baseline; search latency p95 > 1000 ms;
Qdrant storage corruption detected.

**Duration:** Minimum 30 days.

**Exit criteria (go to Phase 3):**

- 30 days without rollback trigger
- MRR stable within 3% of FAISS baseline
- upsert_document < 3 s per file on average
- No unresolved Windows 11 compatibility issues

---

### Phase 3 — Qdrant Primary, FAISS Permanent Standby

**Trigger:** Phase 2 exit criteria met.

**Objective:** Shift the H-RAG02 write path to Qdrant-only upserts (removing the dual-write
overhead) while retaining FAISS as a **permanent warm DR standby**. FAISS code paths, imports,
and `pyproject.toml` dependencies are **never removed** — they provide in-process search
resilience for any environment where Docker or Qdrant is unavailable.

**Architecture:**

```
Write path:  Doc edit → H-RAG02 →  upsert_document (Qdrant primary only)
             FAISS index kept on disk; self-heals from corpus via mtime detection on startup

Read path:   search_docs → Qdrant (primary)
             SEARCH_BACKEND=faiss → immediate fallback to FAISS warm standby
```

**Actions:**

1. Remove the `rebuild_index` call from H-RAG02 (Qdrant upsert only — debounce stays at 10 s)
2. **Retain** all FAISS imports, code paths, and fallback logic in `server.py`
3. **Retain** `faiss` and `sentence-transformers` in `pyproject.toml`
4. **Retain** `rebuild_index` MCP tool for on-demand FAISS rebuild and manual DR invocation
5. Document FAISS warm-standby status in this plan
6. Mark `2026-06-25-qdrant-migration-plan` research report Status: Complete

**Rollback after Phase 3:** Set `SEARCH_BACKEND=faiss` + restart the MCP server.
If the FAISS index file is on disk, FAISS loads immediately (< 60 s). If the index is missing
(e.g., fresh machine), call `rebuild_index` to rebuild from corpus (2–5 min).

---

## 4. H-RAG02 Hook Adaptation per Phase

| Phase                       | H-RAG02 Action                                                                             | Debounce | Mode default |
| --------------------------- | ------------------------------------------------------------------------------------------ | -------- | ------------ |
| 0 (current)                 | `rebuild_index` (full FAISS)                                                               | 30 s     | `warn`       |
| 1 (shadow)                  | `rebuild_index` (FAISS) + shadow `upsert_document` (Qdrant)                                | 30 s     | `warn`       |
| 2 (Qdrant primary)          | `upsert_document` (Qdrant) + `rebuild_index` (FAISS DR)                                    | 10 s     | `auto`       |
| 3 (FAISS permanent standby) | `upsert_document` (Qdrant primary only); FAISS self-heals from corpus via mtime on startup | 10 s     | `auto`       |

The `upsert_document` MCP tool (new, required from Phase 1) must pass all three MCP governance
gates before Phase 1 entry. Governance gate assessment:

| Gate             | Assessment                                                                                                                               |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Capability**   | ✅ Pass — incremental vector upsert into Qdrant is not replicable by `Grep`, `Read`, or `Glob`                                           |
| **Governance**   | ✅ Pass — writes only to the Docker named volume `qdrant_workspace_knowledge`; does not touch pipeline docs, ADRs, or governance records |
| **Completeness** | ✅ Pass — returns `{"status": "upserted", "point_count": N, "file": "..."}` — query-dependent, not a template                            |

---

## 5. Disaster Recovery and Rollback Procedure

### During Phase 1–2 (FAISS hot standby)

```powershell
# Immediate rollback — switches reads back to FAISS in under 60 seconds
$env:SEARCH_BACKEND = "faiss"
# Restart the workspace-knowledge MCP server (Claude Code will restart it on next session)
# FAISS index self-heals from corpus via mtime detection on next startup
```

No data loss possible: the markdown corpus is the source of truth. FAISS rebuilds from files.

### During Phase 3 (FAISS warm standby — permanently retained)

```powershell
# Immediate rollback — FAISS is never removed; switch reads back to FAISS
$env:SEARCH_BACKEND = "faiss"
# Restart the workspace-knowledge MCP server
# FAISS index self-heals from corpus via mtime detection on startup
# If FAISS index file is on disk: available immediately (< 60 s)
# If FAISS index file is missing: call rebuild_index MCP tool (2–5 min)
```

FAISS code paths, imports, and `pyproject.toml` entries are **never removed**. This ensures
the RAG system remains functional on any machine where Docker or Qdrant is unavailable.

### DR Decision Matrix

| Scenario                              | Action                                                                  | Time to recovery                                        |
| ------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------- |
| Qdrant query returns wrong results    | `/rag-sync off` + investigate                                           | < 1 min                                                 |
| Qdrant collection corrupted (Phase 2) | `SEARCH_BACKEND=faiss` + restart                                        | < 60 s                                                  |
| Qdrant collection corrupted (Phase 3) | `SEARCH_BACKEND=faiss` + restart (FAISS warm standby — always retained) | < 60 s (index on disk); 2–5 min (after `rebuild_index`) |
| Embedding model fails to load         | RAWFS tier auto-activates (existing fallback)                           | < 1 s                                                   |

---

## 6. Go/No-Go Criteria Summary

| Gate        | Condition                                                       | Owner                |
| ----------- | --------------------------------------------------------------- | -------------------- |
| Phase 0 → 1 | H-RAG02 + toggle verified; corpus trigger met or CEO authorises | CEO                  |
| Phase 1 → 2 | Qdrant MRR within 5% of FAISS; 2 weeks shadow without issues    | CC-00 Lab Director   |
| Phase 2 → 3 | 30 days stable; MRR within 3%; rollback never triggered         | CEO (final approval) |

---

## 7. Risk Register

| Risk                                                    | Likelihood | Impact | Mitigation                                                                      |
| ------------------------------------------------------- | ---------- | ------ | ------------------------------------------------------------------------------- |
| Docker Desktop unavailable or not running on Windows 11 | Medium     | High   | Phase 1 shadow mode; FAISS primary throughout; graceful `_init_qdrant` fallback |
| upsert_document slower than expected                    | Low        | Medium | Reduce batch size; async upsert                                                 |
| MRR regression after switch                             | Low        | High   | Phase 2 quality gates; 30-day stability window                                  |
| Qdrant storage file grows unexpectedly large            | Low        | Low    | Monitor disk usage; set storage size alert                                      |
| H-RAG02 debounce too aggressive for Qdrant upsert       | Low        | Low    | Recalibrate debounce after Phase 1 benchmarks                                   |
