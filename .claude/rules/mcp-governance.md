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

| Server                | Gates Passed                                |
| --------------------- | ------------------------------------------- |
| `workspace-knowledge` | Capability ✅ Completeness ✅ Governance ✅ |
| `agent-memory`        | Capability ✅ Completeness ⚠️ Governance ✅ |

**`workspace-knowledge`.** BM25 search + raw-FS fallback; Phase 2 semantic upgrade live.
`.mcp.json`'s `command` points at this server's own per-server venv interpreter
(gitignored/machine-local, bootstrapped from `.mcp.json.example`, patched only on an actual OS
switch).

Tiered search-degradation fallback (`HYBRID_QDRANT → HYBRID → BM25 → RAWFS`) is covered by a
scenario-regression suite (`tests/test_search_tier_degradation.py`); a query-time dependency
failure demotes to local FAISS before BM25 rather than skipping it, and a cooldown-gated single
-step reprobe climbs a demoted tier back toward its highest-reached tier once the dependency
recovers. Every registered tool produces a structured audit-log record (`tool_name`,
`duration_ms`, ok/error outcome) on entry and exit; argument summarizers log only lengths and
identifiers, never raw query text.

**`agent-memory`.** Cross-platform (`psutil`-based sibling-cleanup); `.mcp.json`'s `command`
points at this server's own per-server venv interpreter (gitignored/machine-local, bootstrapped
from `.mcp.json.example`, patched only on an actual OS switch). Read-only `search_memory` plus
write-capable `write_memory`, both routed through the shared `embedder-service` (non-degraded);
write-confirmation hook pair wired and live-verified.

One Required-level ASE gap open (merge-integration-agent designation) — tracked as
harness-engineering backlog, not blocking. PII scrubbing on the embed path is implemented:
`redact_pii()` (`pii_redaction.py`) runs on `content` in `write_tool.py`'s `write_memory`
ingestion path, ahead of collision search, injection detection, record construction, and the
embedder/payload.

`health_check`'s cached embedder-capability state carries a last-confirmed-at timestamp
(`_embedder_service_state_confirmed_at`), updated at both real probe sites, so a caller can tell a
fresh "ready" from a stale one instead of trusting the cached value alone. Every registered tool
(`search_memory`, `health_check`, `write_memory`) produces a structured audit-log record
(`tool_name`, `duration_ms`, ok/error outcome) on entry and exit; argument summarizers log only
lengths and identifiers, never raw content or query text. A minimal conformance gate
(`tests/test_tool_conformance.py`) validates each tool's declared input schema against its actual
signature.

Data-volume caveat: `memory_reflection` holds 4 real records, the other three memory types still
hold zero.

**Embedding model provisioning convention:** any CC-00 MCP server that
needs a sentence-transformers embedding model provisions it into the shared cache at
`core-component-00/platform/model-context-protocol-servers/_shared/models/<slug>/` via
`core-component-00/platform/model-context-protocol-servers/_shared/provision_model.py <hf-model-id>` — not a private
per-server cache. The slug convention (`<hf-model-id>` with `/` → `--`) matches
`workspace-knowledge/rag-system/download_model.py`'s own cache. Unlike that script, the shared
cache has no `--activate`/single-active-slot step, since different servers may need different,
incompatible-dimension models resident at once (`workspace-knowledge`: `all-mpnet-base-v2`,
768-dim; `agent-memory`: `all-MiniLM-L6-v2`, 384-dim) — each server reads its own model directly
out of its slug directory. `workspace-knowledge` has no private embedding-model cache — its
fallback loader (`SearchEngine._MODEL_DIR`, used when `embedder-service` is unavailable, for both
the query path and the batch index-build/reseed/upsert paths) reads `all-mpnet-base-v2` directly
from `_shared/models/sentence-transformers--all-mpnet-base-v2/`. Servers read the shared cache
independently at call time; there is no shared init sequence, lock, or state file between servers.

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

`core-component-00/platform/model-context-protocol-servers/_shared/embedder-service/server.py` is a persistent,
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
was the root cause of intermittent embedder-warmup stalls.

**Graceful degradation.** Both consumers treat the service being down or slow to start as a
non-error. `agent-memory` falls back to its pre-existing `embedder=None` → `degraded: true` path
(unchanged from before `embedder-service` existed). `workspace-knowledge` falls back to loading
`all-mpnet-base-v2` in-process directly from the shared cache
(`_shared/models/sentence-transformers--all-mpnet-base-v2/`, per the model-provisioning-convention
note above) — this fallback covers both the query path and the batch index-build/reseed/upsert
paths.

**Python environment.** Each registered server runs from its own venv
(`workspace-knowledge/.venv/`, `agent-memory/.venv/`) — these dependencies must not be installed
globally. `embedder-service` has no venv of its own; it inherits its interpreter from whichever
server spawns it via `sys.executable`, which is why `torch` and `sentence-transformers` pins must
stay identical across both servers' `pyproject.toml` files — that invariant, not the venv layout,
is what keeps `embedder-service`'s behavior deterministic. Full rationale:
`core-component-00/platform/model-context-protocol-servers/CLAUDE.md` § Python Environment. A bare `"python"` in `.mcp.json`
or in `manage_embedder_service.py` is a defect regardless of venv layout — it resolves via `PATH`
to the system interpreter and silently reintroduces both the global dependency and a possible
CPU-only torch.

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
