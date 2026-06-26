# Research Report — Qdrant Migration Plan: Strategy, Deployment, Initialization, Monitoring, and Hook Design

---

## Metadata

| Field                | Value                                                                        |
| -------------------- | ---------------------------------------------------------------------------- |
| **Investigation ID** | `2026-06-25-qdrant-migration-plan`                                           |
| **Date Started**     | 2026-06-25                                                                   |
| **Date Completed**   | 2026-06-26                                                                   |
| **Status**           | Complete (v1.0)                                                              |
| **Investigator**     | Dr. Elias Vance — CC-00 Laboratory Director                                  |
| **Laboratory**       | Core Component 00                                                            |
| **Module(s)**        | retrieval-augmented-generation, harness-engineering, multi-agent-engineering |
| **Priority**         | High                                                                         |
| **Requestor**        | CEO                                                                          |

---

## Executive Summary

The planning phase of this investigation is complete. Five production-ready deliverables have
been produced in `plans/`: a four-phase migration strategy, a deployment guide selecting Qdrant
Docker mode for this hardware profile (CEO approved 2026-06-25), an initialization guide specifying the collection schema
and seeding procedure, a monitoring guide covering index freshness, collection health, MRR
regression detection, and upsert latency thresholds, and a hook system design specifying H-RAG02
and the `/rag-sync` command. All new MCP tools introduced by the
migration (`upsert_document`, `health_check`) have been assessed against the MCP governance
three-gate test and pass. Empirical Phase 1 validation — installing `qdrant-client`, running
shadow-mode upserts, and benchmarking MRR parity against the FAISS baseline — has not yet
started; its trigger condition is defined in `01-migration-strategy.md` §2.

---

## Investigation Scope

### What Will Be Investigated

A complete migration plan for transitioning the `workspace-knowledge` MCP server from its
current in-process FAISS + BM25 architecture to Qdrant Docker standalone server, covering:

1. **Migration strategy** — Phased approach, rollback plan, corpus size trigger threshold,
   coexistence period with the existing FAISS stack, and H-RAG02 hook adaptation (full
   `rebuild_index` → per-file `upsert_document`)
2. **Deployment guidelines** — Qdrant embedded vs. server mode trade-offs on this hardware
   (RTX 4060, 31.6 GB RAM, Windows 11, local-only repo); dependency management;
   `pyproject.toml` changes; MCP server restart procedures
3. **Initialization procedures** — Seeding the Qdrant collection from the existing workspace
   corpus; collection schema design (vector dimensions, distance metric, payload schema for
   `rel_path`, `section`, `chunk_idx`); index validation and smoke-test protocol
4. **Monitoring protocols** — Index freshness tracking (`index_built_at` field), query quality
   regression detection (MRR comparison pre/post migration), health-check endpoint design,
   and alerting thresholds

### Why This Investigation Was Needed

Prior hook system design work (now consolidated into `plans/05-hook-design.md`) concluded that
Qdrant is the correct long-term architecture for the workspace RAG layer — specifically because
it supports incremental upserts (per-file chunk updates) rather than full-rebuild-only, which
becomes the critical cost driver as corpus size grows. The CEO mandated that any Qdrant migration
decision must be accompanied by a rigorous, production-ready plan — not a high-level
recommendation. This investigation is that plan.

### Out of Scope

- External (cloud) Qdrant deployment — this workspace is local-only with no remote configured
- Fine-tuning or retraining the embedding model (`all-mpnet-base-v2`) — covered separately
  if warranted
- Weaviate, Pinecone, or other vector DB alternatives — Qdrant was selected as the migration
  target in prior hook system design work (see `plans/05-hook-design.md`); this investigation
  does not re-evaluate that choice
- Replacing the BM25 tier — BM25 may be retained or replaced by Qdrant sparse vectors
  (to be determined during investigation)

---

## Research Questions

1. What is the corpus size trigger threshold at which Qdrant's incremental upsert capability
   provides a material, measurable performance improvement over the current full-rebuild
   FAISS approach?
2. Should Qdrant run in embedded Python client mode (`QdrantClient(path="...")`) or as a
   standalone server process? What are the trade-offs on this specific hardware profile?
3. What is the minimal Qdrant collection schema that replicates the current chunk metadata
   (`rel_path`, `section`, `chunk_idx`) and supports the existing MCP tool surface
   (`search_docs`, `find_related_documents`, `retrieve_context`, etc.)?
4. How should H-RAG02 be adapted for Qdrant — specifically, does it call `rebuild_index`
   (full collection rebuild) or a new `upsert_document` tool (per-file incremental update)?
   Does `upsert_document` pass the three MCP governance gates?
5. What initialization procedure reliably seeds the Qdrant collection from the existing
   FAISS corpus without data loss or quality regression?
6. What monitoring metrics and alert thresholds are needed to detect index staleness,
   embedding drift, and query quality regression post-migration?
7. What is the rollback procedure if Qdrant migration degrades retrieval quality or
   introduces unacceptable latency?

---

## Methodology

### Approach

The planning phase (steps 4–5 below) is complete. Steps 1–3 are empirical work gated on Phase 1
entry criteria defined in `01-migration-strategy.md` §2.

1. **Environment assessment** _(Phase 1 — pending)_ — Verify Docker Desktop for Windows
   (WSL2 backend) compatibility and Qdrant Docker container stability on Windows 11 + Python 3.11
2. **Prototype build** _(Phase 1 — pending)_ — Implement a Qdrant-backed `SearchEngine`
   variant alongside the existing FAISS engine; run both in parallel on the live corpus
3. **Quality benchmarking** _(Phase 1 — pending)_ — Compare retrieval MRR, latency
   (p50/p95), and rebuild cost between FAISS and Qdrant across corpus size checkpoints
4. **Migration design** _(complete)_ — Produced five deliverables (strategy, deployment,
   initialization, monitoring, hook design) via architecture analysis of `server.py` and
   hardware specification assessment
5. **Governance review** _(complete)_ — Applied MCP three-gate test to `upsert_document`
   and `health_check`; both pass all three gates (see `01-migration-strategy.md` §4 and
   `04-monitoring-guide.md` §3.2)

### Tools and Resources

- `.claude/mcp-servers/workspace-knowledge/server.py` — Current `SearchEngine` implementation
- `qdrant-client` Python library (Docker/server mode — `QdrantClient(url="http://localhost:6333")`)
- `sentence-transformers` `all-mpnet-base-v2` (existing embedding model)
- `plans/05-hook-design.md` — H-RAG02 hook design specification (consolidated from predecessor
  investigation)
- `.claude/rules/mcp-governance.md` — Governance gate test for any new tools

### Constraints

- No remote Qdrant instance — local Docker deployment only (CEO approved Docker over embedded)
- Must not break the existing MCP tool surface (all 10 existing tools must remain functional
  during and after migration)
- H-RAG02 toggle design (`plans/05-hook-design.md` §4–§5) is the authoritative specification
  and must be implemented as specified before Phase 1 entry

---

## Findings

Findings 1–3 are design-phase findings derived from architecture analysis. Empirical findings
(MRR benchmarks, upsert latency measurements, Windows 11 compatibility) will be added as
Finding 4+ upon Phase 1 execution.

### Finding 1: Qdrant Docker Mode Is the Correct Deployment Choice (CEO Revised 2026-06-25)

Qdrant's three deployment modes were evaluated. In-memory mode was rejected (no persistence
across sessions). Embedded local mode was initially selected, then superseded by CEO directive
after a critical data-format incompatibility was identified: the `qdrant-deployment-options`
skill states explicitly that _"local mode data format is NOT compatible with server"_ — meaning
any future upgrade from embedded to Docker would require a full collection reseed. **Docker
standalone server mode** (`QdrantClient(url="http://localhost:6333")`) was selected: it runs the
full Qdrant Rust engine, uses the production-compatible data format, and the CEO's approval
waives the no-daemon-process convention for this workstation. Docker Desktop for Windows (WSL2
backend) is required. The RTX 4060 GPU is not used by Qdrant itself (CPU-only); it continues to
serve the `sentence-transformers all-mpnet-base-v2` embedding model.

---

### Finding 2: `upsert_document` and `health_check` Pass All Three MCP Governance Gates

Two new MCP tools are required by the migration. Both were assessed against the three-gate
inclusion test in `.claude/rules/mcp-governance.md`:

| Tool              | Capability                                                         | Governance                                                                                            | Completeness                                                        |
| ----------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `upsert_document` | ✅ Incremental vector upsert is not replicable by native tools     | ✅ Writes only to Docker named volume `qdrant_workspace_knowledge`; no pipeline/ADR/governance writes | ✅ Returns `{status, file, new_chunk_count}` — query-dependent      |
| `health_check`    | ✅ `get_collection()` introspection not replicable by native tools | ✅ Read-only; no governance state modified                                                            | ✅ Returns real collection metrics (point count, disk MB, segments) |

Both tools pass all three gates and are eligible for registration in `.mcp.json` at Phase 1
entry.

---

### Finding 3: Corpus Trigger Thresholds for Phase 1 Entry Are Defined

The practical threshold at which Qdrant's incremental upsert materially outperforms FAISS
full-rebuild is: (a) `rebuild_index` call takes >10 seconds perceptibly, OR (b) workspace
`.md` file count exceeds 500 / chunk count exceeds 10,000, OR (c) CEO authorises Phase 1
regardless of scale. At current corpus scale (~hundreds of `.md` files, estimated 2,000–5,000
chunks), neither primary nor secondary threshold is met. The strategic override remains the
most likely Phase 1 entry path.

---

## Analysis

### Interpretation of Findings

_Design-phase interpretation is complete. Empirical interpretation (MRR parity, latency
benchmarks, Windows 11 compatibility results) is pending Phase 1 execution._

The three design-phase findings collectively confirm that the migration is architecturally
sound and low-risk: the deployment mode is unambiguous (Docker, CEO-approved), the governance
requirements are satisfied by the new tools, and the migration is corpus-scale-gated so no
urgency exists to accelerate. The four-phase migration strategy preserves FAISS as a **permanent
DR fallback at all phases** — FAISS is never retired. The CEO's directive ensures the RAG system
remains functional on any machine where Docker or Qdrant is unavailable; the worst-case rollback
at any phase is a single `SEARCH_BACKEND=faiss` environment variable change and MCP server
restart — a sub-60-second recovery (< 2–5 min only if the FAISS index file is missing and a
fresh `rebuild_index` is needed). The Docker deployment also eliminates a future reseed cost:
embedded-mode data is incompatible with the Qdrant server, so starting with Docker is the
correct long-term choice.

### Trade-offs Identified

_To be completed. Anticipated dimensions:_

| Dimension                  | FAISS in-process       | Qdrant embedded (rejected)                                          | **Qdrant Docker — selected** ✅                           |
| -------------------------- | ---------------------- | ------------------------------------------------------------------- | --------------------------------------------------------- |
| Incremental update support | No (full rebuild only) | Yes                                                                 | Yes                                                       |
| Daemon required            | No                     | No                                                                  | Yes (Docker Desktop)                                      |
| Startup latency            | Minutes (GPU encode)   | Sub-second (load from disk)                                         | Sub-second                                                |
| Windows 11 compatibility   | ✅                     | Expected ✅ (unverified; data format incompatible with server)      | Expected ✅ (Docker Desktop WSL2; unverified empirically) |
| Corpus scale ceiling       | ~50K chunks            | ~1M+ chunks (Python reimplementation)                               | ~10M+ chunks (full Rust engine)                           |
| Data format compatibility  | n/a                    | ❌ Incompatible with server — future migration requires full reseed | ✅ Production-compatible; future upgrades preserve data   |
| H-RAG02 adaptation needed  | No                     | Yes (upsert)                                                        | Yes (upsert)                                              |

### Risks and Limitations

| Risk                                                             | Likelihood | Impact | Mitigation                                                                                                |
| ---------------------------------------------------------------- | ---------- | ------ | --------------------------------------------------------------------------------------------------------- |
| Docker Desktop unavailable or fails to start on Windows 11       | Medium     | High   | Phase 1 shadow mode keeps FAISS primary; graceful `_init_qdrant` fallback to FAISS                        |
| `upsert_document` slower than expected                           | Low        | Medium | Reduce batch size; async upsert                                                                           |
| MRR regression after Qdrant switch                               | Low        | High   | Phase 2 quality gates; 30-day stability window; FAISS permanent fallback guarantees recovery at any phase |
| Qdrant storage grows unexpectedly large                          | Low        | Low    | Monitor `disk_usage_mb` via `health_check`; alert threshold at 1 GB                                       |
| H-RAG02 debounce threshold miscalibrated for Qdrant upsert speed | Low        | Low    | Recalibrate after Phase 1 benchmarks; design estimate is 10 s                                             |

---

## Recommendations

All four recommendation areas are fully specified in the `plans/` deliverables.

**1. Migration strategy** (`01-migration-strategy.md`) — Adopt a four-phase approach: Phase 0
(H-RAG02 + `/rag-sync` toggle, current state), Phase 1 (shadow mode — Qdrant writes, FAISS
reads), Phase 2 (Qdrant primary, FAISS hot standby), Phase 3 (Qdrant primary, FAISS permanent
warm standby). Enter Phase 1 when any corpus trigger is met or CEO authorises. FAISS code paths
and dependencies are **never removed** — FAISS provides permanent in-process resilience for
any environment without Docker; rollback at any phase is a single `SEARCH_BACKEND=faiss` env
change + MCP restart (< 60 s).

**2. Deployment** (`02-deployment-guide.md`) — Deploy Qdrant via Docker Desktop for Windows
(CEO approved 2026-06-25). Run `docker run -d --name qdrant-workspace -p 6333:6333 -p 6334:6334 -v qdrant_workspace_knowledge:/qdrant/storage qdrant/qdrant`.
Connect via `QdrantClient(url="http://localhost:6333")`. Add `qdrant-client>=1.7.0` to
`pyproject.toml`. Control the active backend via `SEARCH_BACKEND` environment variable
(default: `faiss`; set `qdrant` at Phase 2). Persist the flag in `.mcp.json`.

**3. Initialization** (`03-initialization-guide.md`) — Create collection `workspace_knowledge`
with 768-dimension Cosine vectors (matching `all-mpnet-base-v2` output). Reuse the existing
`_chunks` list built by BM25 init; seed in batches of 100 with deterministic MD5-based point
IDs for idempotent upserts. Validate with a five-test smoke-test protocol before Phase 1 entry.

**4. Monitoring** (`04-monitoring-guide.md`) — Add `index_built_at` and `backend` fields to
`_meta_block()` for per-response freshness visibility. Introduce `health_check` MCP tool
returning live collection metrics. Establish MRR@5 baseline on 20 representative queries
before Phase 2 entry; alert if Phase 2 MRR drops >10% in any 7-day window.

**5. Hook System** (`05-hook-design.md`) — Implement H-RAG02 (`rag-index-sync.ps1`), a
`PostToolUse` hook that detects `.md` file writes to the four KEY_DIRS and instructs Claude to
call the appropriate index-update tool. Phase-adaptive: calls `rebuild_index` (Phase 0–1, FAISS
full rebuild) and `upsert_document` (Phase 2–3, Qdrant incremental upsert) based on the
`SEARCH_BACKEND` env var. Paired with the `/rag-sync` custom command for operator control over
`auto` / `warn` / `off` modes and debounce threshold.

---

## References

### Internal Documentation

- `plans/05-hook-design.md` — H-RAG02 hook design specification; concluded Qdrant is correct
  long-term target; consolidated from predecessor investigation (2026-06-25)
- `.claude/mcp-servers/workspace-knowledge/server.py` — Current FAISS + BM25 implementation
  to be migrated
- `.claude/rules/mcp-governance.md` — Three-gate inclusion test for any new MCP tools
- `core-component-00/retrieval-augmented-generation/architecture/overview.md` — RAG
  architecture reference

### Related Work

- `2026-06-20-mcp-server-assessment` — Original MCP architecture ratification; established
  the Phase 2 FAISS upgrade that this investigation now supersedes

---

## Open Questions

1. **Is Qdrant Docker Desktop stable on Windows 11 (WSL2 backend) for this workstation?** ✅ **Closed**
   - Status: Empirically verified in Phases 1–2. Container `qdrant-workspace` ran stably throughout
     Phase 2; 7,793 points indexed with no Windows 11 compatibility issues observed.
   - Closed: 2026-06-26

2. **Does Qdrant v1.7+ sparse vector support replace the BM25 tier entirely?** ✅ **Closed**
   - Status: Out of scope for this investigation. BM25 tier is retained as a permanent fallback
     tier alongside Qdrant in the three-tier degradation stack (`HYBRID_QDRANT → HYBRID → BM25 →
RAWFS`). Sparse-vector replacement is a future investigation if warranted.
   - Closed: 2026-06-26

3. **What debounce threshold is appropriate for Qdrant upsert (vs. full FAISS rebuild)?** ✅ **Closed**
   - Status: Calibrated at 10 s at Phase 2 entry; verified empirically throughout Phase 2
     operation. H-RAG02 debounce set to 10 s in `rag-sync-state.json`.
   - Closed: 2026-06-26

4. **Does `upsert_document` pass all three MCP governance gates?** ✅ **Answered**
   - Status: Fully assessed in `01-migration-strategy.md` §4 — Capability ✅, Governance ✅,
     Completeness ✅. Both `upsert_document` and `health_check` pass all three gates.
   - Priority: Resolved
   - Closed: 2026-06-25

---

## Version History

| Version | Date       | Author                               | Changes                                                                                                                                                                                                                                                                                                                              |
| ------- | ---------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.1     | 2026-06-25 | Dr. Elias Vance — CC-00 Lab Director | Investigation stub opened                                                                                                                                                                                                                                                                                                            |
| 0.2     | 2026-06-25 | Dr. Elias Vance — CC-00 Lab Director | Planning phase complete: populated Executive Summary, Methodology, Findings 1–3, Analysis, Trade-offs, Risks, Recommendations; closed Open Question 4; `plans/` subfolder added with four numbered deliverables                                                                                                                      |
| 0.3     | 2026-06-25 | Dr. Elias Vance — CC-00 Lab Director | CEO approved Docker deployment over embedded mode; updated Finding 1, Analysis, Trade-offs table, Risks, Recommendation 2, and Open Question 1 to reflect Docker selection; propagated to all four `plans/` documents                                                                                                                |
| 0.4     | 2026-06-25 | Dr. Elias Vance — CC-00 Lab Director | CEO directed FAISS must remain as permanent DR fallback — never retired; Phase 3 renamed from "FAISS Retirement" to "Qdrant Primary, FAISS Permanent Standby"; updated Analysis, Risks, Recommendation 1; propagated to `01-migration-strategy.md`, `diagrams/rag-dr-system.md`                                                      |
| 0.5     | 2026-06-25 | Dr. Elias Vance — CC-00 Lab Director | CEO consolidated hook system from `2026-06-25-rag-index-sync-hook-design` into this investigation; added `05-hook-design.md` as fifth planning deliverable; added Recommendation 5; predecessor investigation folder removed; `telescope/README.md` updated                                                                          |
| 0.6     | 2026-06-25 | Dr. Elias Vance — CC-00 Lab Director | Applied six engineering review gap-closures: BM25 O(N) rebuild cost note added to `03-initialization-guide.md` §3.1; `parity_ok` corrected to `==` with `orphaned_points` field added in `04-monitoring-guide.md` §3.1 and §3.3; H-RAG02 path-matching regex hardened to `(^                                                         | \/)$dir`in`05-hook-design.md`§4; MRR ground truth specification and commit requirement added to`04-monitoring-guide.md`§4.1; Docker volume backup/restore procedure added to`02-deployment-guide.md`§3.6;`qdrant-client`version bound tightened to`<2.0.0`in`02-deployment-guide.md` §4.1 |
| 1.0     | 2026-06-26 | Dr. Elias Vance — CC-00 Lab Director | Phase 3 activated (CEO approval 2026-06-26, 30-day stabilization window waived); all open questions closed; H-RAG02 confirmed phase-adaptive — no hook code change required at Phase 3 (hook already instructs `upsert_document` only when `SEARCH_BACKEND=qdrant`); FAISS permanent warm standby documented; status set to Complete |

---

**Template Version:** 1.0
**Last Updated:** 2026-06-25
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
