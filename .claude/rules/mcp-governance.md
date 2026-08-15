---
description: MCP server inclusion governance — three-gate test (Capability/Governance/Completeness) — always active
---

# MCP Governance — Inclusion Charter

Controls which MCP servers may be registered in `.mcp.json`. All three gates must pass before a
server is added. A server failing any gate must be removed.

---

## The Three-Gate Inclusion Test

Every MCP server must pass all three gates before registration. A single failing gate is a
blocking defect.

### Gate 1 — Capability

> The tool performs computation, subprocess execution, or stateful operation that Claude Code's
> native tools (Read, Edit, Grep, Glob, Bash, Write) cannot replicate with equivalent quality.

**Pass:** The server executes subprocesses, maintains state across calls, or performs computation
that is materially faster or more reliable when done out-of-process.

**Fail:** The server wraps file reads, keyword searches, or Markdown parsing — work that native
tools already handle. A "search_docs" tool backed purely by Python string matching is a Capability
failure when `Grep` exists.

---

### Gate 2 — Governance

> The tool enforces, not bypasses, pipeline guardrails. Any tool that can advance a pipeline
> stage, modify governance records, or skip approval gates is rejected.

**Pass:** The server returns information, raises alerts, or validates against policy — it advises
Claude, it does not act on behalf of Claude against the pipeline.

**Fail:** The server can mark a stage as complete, modify an ADR after lock, or change a
`pipeline.md` approval record. Any tool whose primary action updates governance state is a
Governance failure.

---

### Gate 3 — Completeness

> Every tool in the server produces substantively correct, actionable output for its stated
> purpose. Stub responses, "requires inspection" returns, and hardcoded-threshold heuristics
> presented as analysis do not qualify.

**Pass:** Each `@mcp.tool()` endpoint returns real, query-dependent output that an agent can act
on without further verification of the tool's own correctness.

**Fail:** A tool returns `"analysis complete — review manually"`, a static template, or a score
derived from a hardcoded rule that does not inspect the actual artifact. A tool where every query
returns the same template regardless of input content is a Completeness failure.

---

## Assessment Protocol

Before registering a new server, complete this checklist:

| Check | Question                                                                    | Gate         |
| ----- | --------------------------------------------------------------------------- | ------------ |
| ☐     | Does this server do something native tools genuinely cannot?                | Capability   |
| ☐     | Does every tool produce output that varies meaningfully with input?         | Completeness |
| ☐     | Could any tool write to a pipeline stage, ADR, or approval record?          | Governance   |
| ☐     | Has each tool been tested with a real query against real workspace content? | Completeness |

If any checkbox is ☐ (unchecked) after honest assessment, the server fails. Do not register it.

---

## Registered Servers (Post-Retirement)

| Server                | Gates Passed                                | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace-knowledge` | Capability ✅ Completeness ✅ Governance ✅ | BM25 search + raw-FS fallback; Phase 2 semantic upgrade live. **Cross-platform `.mcp.json` fix reverted (2026-08-13):** a same-day attempt to resolve the launch path per-OS via `uv run` + `UV_PROJECT_ENVIRONMENT` broke live `/mcp reconnect` for both servers (`"uv"` resolved via `PATH` in a fresh shell but not in the Claude Code host's own long-lived process environment) — reverted back to the direct, hardcoded `.venv/Scripts/python.exe` path. Full record: `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `agent-memory`        | Capability ✅ Completeness ⚠️ Governance ✅ | **Cross-platform: partial (2026-08-13).** `server.py`'s sibling-cleanup successfully ported from `powershell`/`Get-CimInstance` to `psutil` — cross-platform, verified against the full 249-test suite plus one real (non-mocked) run against live OS processes, stands unaffected by the item below. `.mcp.json`'s launch-command portion was attempted via `uv run` + `UV_PROJECT_ENVIRONMENT` the same day, but that broke live `/mcp reconnect` in production (root cause: `"uv"` resolves via `PATH` in a fresh shell but not in the Claude Code host's own long-lived process environment) and was reverted back to a hardcoded `.venv/Scripts/python.exe` path — that portion of the original finding is reopened. User `/mcp reconnect` still needed to pick up the reverted command. Full record (discovery, remediation, and the incident + revert, as dated sections in one topic file): `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md` — not narrated here, per this cell's own condensation history below. **Condensed 2026-08-10** (per CEO consolidation request — this cell had regrown into a full inline changelog, the same anti-pattern `telescope/README.md` fixed 2026-08-06; full narrative history was never deleted, it already lives in the linked reports below, this is a pointer index). Read-only `search_memory` plus (as of 2026-08-10) write-capable `write_memory`, both live over the dedicated `qdrant-memory` instance, routed through the shared `embedder-service` (non-degraded). **Current state:** reachable; `search_capability.effective_path: embedder-service`; `write_memory` registered and live-verified; write-confirmation hook pair wired. Two Required-level ASE gaps open (PII scrubbing on the embed path; merge-integration-agent designation) — tracked as harness-engineering backlog, neither blocking. Data-volume caveat: `memory_reflection` holds 4 real records, `memory_episodic`/`memory_semantic`/`memory_procedural` still hold zero (no production writes yet), so retrieval quality against real content is unverified for those three. **History, dated, full detail in the linked doc — not reproduced here:** 2026-07-13 P0 (`health_check`/`search_memory` indefinite hang, root-caused to an unbounded Qdrant `read()`, fixed with a hard watchdog) and the persistent embedder-service redesign it motivated (6 phases, Conditional ASE verdict, implemented and live at `core-component-00/mcp-servers/_shared/embedder-service/server.py`; telescope record removed 2026-08-13 as a completed maintenance-operation, implementation verified via git history — this cell is now the sole surviving summary). 2026-07-17 P0 (crash-loop post-relocation) and embedder-warmup import-lock stall, both root-caused and fixed (lazy embedder warmup, see `core-component-00/mcp-servers/agent-memory/README.md`; telescope record removed 2026-08-13 as a completed maintenance-operation, implementation verified via git history). 2026-08-06 observability fix (`search_capability` health block) and write-path threat model (no-go for a write tool at the time) → `telescope/2026-07-10-agent-memory-architecture/research-report.md` § Architecture Decisions and Write-Path Security Posture (formerly the standalone `supporting/09-mcp-architecture-decision.md`, `10-observability-fix.md`, `11-write-path-threat-model.md`, all retired 2026-08-10 — 10's content moved to `core-component-00/telescope/2026-08-08-cc00-mcp-observability-stack/research-report.md` § Related Incident History). 2026-08-08 write-capable `write_memory` tool built and independently adversarially evaluated (conditional go, one partial-success finding pending hook wiring) → `core-component-00/telescope/2026-08-08-cc00-mcp-observability-stack/research-report.md` § Related Build (moved there 2026-08-10 from the former standalone `13-write-path-implementation.md`). 2026-08-09/10 reconnect-reliability regression (mutual-kill race) root-caused and fixed, confirmation-hook pair wired, `write_memory` activated and live-verified → `core-component-00/telescope/2026-08-08-cc00-mcp-observability-stack/research-report.md` § Related Build, `supporting/implementation-tracking/session-log.md`. **Boundary reminder:** this row spans two separate build plans — `2026-07-10-agent-memory-architecture` (write-path, phases 0–2) and `2026-07-13-mcp-embedder-service-redesign` (embedder-service, phases 0–5); do not read "Phase N" as one continuous numbering across them — see `research-report.md` § Related Work there for a cross-reference pointer to the latter's later stages (the former standalone `14-embedder-service-phases-3-5-summary.md` was retired 2026-08-10, judged too thin to stand as its own document). |

**Embedding model provisioning convention (established 2026-07-12):** any CC-00 MCP server that
needs a sentence-transformers embedding model provisions it into the shared cache at
`core-component-00/mcp-servers/_shared/models/<slug>/` via
`core-component-00/mcp-servers/_shared/provision_model.py <hf-model-id>` — not a private
per-server cache. The slug convention (`<hf-model-id>` with `/` → `--`) matches
`workspace-knowledge/rag-system/download_model.py`'s own cache. Unlike that script, the shared
cache has no `--activate`/single-active-slot step, since different servers may need different,
incompatible-dimension models resident at once (`workspace-knowledge`: `all-mpnet-base-v2`,
768-dim; `agent-memory`: `all-MiniLM-L6-v2`, 384-dim) — each server reads its own model directly
out of its slug directory. **`workspace-knowledge`'s former private cache
(`workspace-knowledge/embedding/model/`) was retrofitted onto this convention 2026-08-06** as
Phase 6 of a workspace-knowledge batch-encoding migration (telescope record removed 2026-08-13 as
a completed maintenance-operation, implementation verified via git history) — its fallback
loader (`SearchEngine._MODEL_DIR`, used when `embedder-service` is unavailable, for both the
query path and the newly-migrated batch index-build/reseed/upsert paths) now reads
`all-mpnet-base-v2` directly from `_shared/models/sentence-transformers--all-mpnet-base-v2/`
instead of a duplicated private copy — verified byte-identical output (cosine similarity 1.0)
before the 418.4 MB private copy was deleted. The line below, "this convention governs
new/future provisioning, not a retrofit of what already works," was the standing position on
this specific gap until that date; it no longer describes `workspace-knowledge`'s embedding-model
loading, though the general principle (don't retrofit working systems without cause) still holds
for future cases. Servers read the shared cache independently at call time; there is no shared
init sequence, lock, or state file between servers.

**The shared cache has a third consumer beyond the two registered servers.** `embedder-service`
(see "Shared Infrastructure" below) loads every model any of its consumers route through it
directly from `_shared/models/<slug>/` — including `all-mpnet-base-v2`, which `workspace-knowledge`
now also reads directly from the same shared-cache slug for its no-service fallback path (see
above; no longer a separate private copy). Do not assume a model present in the shared cache but
"unused" by a registered server's own code is dead weight — check `embedder-service`'s
`MODEL_ALIASES` table and each consumer's `EMBEDDER_SERVICE_ENABLED` wiring before deleting
anything from `_shared/models/`.

---

## Shared Infrastructure — `embedder-service` (Not Individually Gated)

`core-component-00/mcp-servers/_shared/embedder-service/server.py` is a persistent,
localhost-only HTTP process that `workspace-knowledge` and `agent-memory` both route embedding
calls through when it's available. It is **not** an entry in `.mcp.json` and Claude Code never
connects to it directly — it is an internal implementation detail of the two registered servers,
not a standalone MCP server, so the Three-Gate Inclusion Test does not apply to it: there is no
`.mcp.json` entry to gate.

**Lifecycle.** Self-launched by whichever consumer needs it first
(`embedder_client.ensure_service_running()`, guarded by a real atomic lock file —
`embedder-service.lock`, created `O_CREAT|O_EXCL` so concurrent launches don't race — distinct
from `embedder-service.pid`, which `server.py` writes purely for introspection and does not use
for locking), and self-terminating after an idle timeout (600s default) once its in-flight
request counter reaches zero — no external supervisor process has to remember to stop it.

**What it does.** Loads every sentence-transformers model provisioned in
`_shared/models/<slug>/` once at process startup — today that's `all-MiniLM-L6-v2` (for
`agent-memory`) and `all-mpnet-base-v2` (for `workspace-knowledge`) — then serves
`POST /embed {model, texts}` over plain HTTP (`127.0.0.1:8791` by default). This removes the
failure mode described in the `agent-memory` row above: a heavy `sentence_transformers` →
`torch`/`scipy` import happening inside a process the MCP host itself spawns and churns, which
was the root cause of the intermittent embedder-warmup stalls fixed 2026-07-17.

**Graceful degradation.** Both consumers treat the service being down or slow to start as a
non-error. `agent-memory` falls back to its pre-existing `embedder=None` → `degraded: true` path
(unchanged from before `embedder-service` existed). `workspace-knowledge` falls back to loading
`all-mpnet-base-v2` in-process directly from the shared cache
(`_shared/models/sentence-transformers--all-mpnet-base-v2/` — no longer a private copy, see the
model-provisioning-convention note above) — this fallback now covers both the query path (Phase 4,
2026-07-14) and the batch index-build/reseed/upsert paths (Phase 6, 2026-08-06).

**Python environment.** All three processes — both registered servers and `embedder-service` — run
from **one shared venv** at `core-component-00/mcp-servers/.venv/`. These dependencies must not be
installed globally. `embedder-service` inherits its interpreter from the spawning server via
`sys.executable`, which is why a single shared venv is used rather than per-server ones: per-server
venvs would make the shared service's environment depend on whichever server started it first. A
bare `"python"` in `.mcp.json` or in `manage_embedder_service.py` (2026-08-13 Python port, retiring
the former Windows-only `.ps1`) is a defect — it resolves via
`PATH` to the system interpreter and silently reintroduces both the global dependency and a
possible CPU-only torch. Full rationale and the interpreter-resolution chain:
`core-component-00/mcp-servers/CLAUDE.md` § Python Environment.

**Config (env vars, all optional, sane localhost defaults):** `EMBEDDER_SERVICE_HOST`
(`127.0.0.1`), `EMBEDDER_SERVICE_PORT` (`8791`), `EMBEDDER_SERVICE_IDLE_TIMEOUT_S` (`600`),
`EMBEDDER_SERVICE_MAX_BODY_BYTES` (2 MB), `EMBEDDER_SERVICE_MAX_TEXTS` (256 texts/request),
`EMBEDDER_SERVICE_MAX_TEXT_CHARS` (20,000 chars/text). `workspace-knowledge` additionally reads
`EMBEDDER_SERVICE_ENABLED` (default `true`) to decide whether to attempt the service at all.

**Retired servers:**

| Server                 | Failing Gate                  | Reason                                                                                                                                                                                                          |
| ---------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pipeline-automation`  | Completeness ❌               | `advance_stage` returns template regardless of actual stage state                                                                                                                                               |
| `cc00-tools`           | Completeness ❌               | `check_context_budget` returns hardcoded arithmetic, not model-layer data                                                                                                                                       |
| `git-worktree-manager` | Governance ❌ Completeness ❌ | `merge_branch` and `check_merge_conflicts` run `git checkout` on the main workspace (actor, not advisor); default branch hardcoded to `master`, wrong for workspace; replaced by direct PowerShell git commands |

---

## Adding a New Server

1. Complete the Assessment Protocol above.
2. All four checkboxes must be checked.
3. Add the server to `.mcp.json` only after all gates pass.
4. Document the server in the Registered Servers table above.

---

## Removing a Server

A server must be removed from `.mcp.json` when:

- It fails a gate (immediately, no grace period)
- It duplicates capability now provided by a native tool
- It has been unmaintained for two or more sprints

Removal procedure: delete the server's entry from `.mcp.json`, update the Retired Servers table
above with the reason, commit.

---

**Authority:** CEO → CC-00 Laboratory Director (Dr. Elias Vance)
**Established:** 2026-06-24
