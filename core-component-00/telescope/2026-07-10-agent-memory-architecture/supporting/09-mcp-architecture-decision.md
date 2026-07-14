# MCP Architecture Decision — Dedicated Memory Server

**Parent Report:** `../research-report.md`
**Relates to:** Post-P1 follow-on — MCP tool surface for the memory system
**Date:** 2026-07-12
**Decided by:** CEO, on Laboratory Director recommendation

---

## Context

P0 and P1 built and verified the memory system's storage/decay engineering (Qdrant
write-through, JSONL log, decay/consolidation maintenance job, telemetry). None of it is
usable by an agent yet: no MCP tool exposes memory read or write, `PersistentMemorySink` is
never instantiated outside tests, and nothing wires memory into context assembly. Closing
that gap requires an MCP tool surface. This document records the decision on where that
surface lives and what constraints govern it, before implementation begins.

## Decision 1: Dedicated server vs. extending `workspace-knowledge`

**Initial recommendation (Laboratory Director):** extend the existing `workspace-knowledge`
server with new memory tools rather than stand up a second server. Rationale at the time: MCP
tools are just functions on a FastMCP instance; `server.py` already imports across module
boundaries (it pulls from `context-engineering/implementations/` for `health_check`); a second
server means a second process, a second `.mcp.json` entry, and doubled operational surface,
with no clear capability argument for the split.

**CEO's rejection:** extending `workspace-knowledge` risks destabilizing a server that has
already achieved production stability and is load-bearing for this workspace's existing
tooling (`search_docs`, `rebuild_index`, etc.). Memory tooling is newer and carries more
untested surface — bolting it into the same process means a bug in the newer code can take
down the proven one.

**Revised recommendation (accepted):** the CEO's argument holds up technically and is
consistent with a precedent this same programme already established — `qdrant-memory` got its
own container instead of a collection inside `qdrant-workspace`, specifically for blast-radius
and failure-domain isolation. Extending that logic one layer up, from the data layer to the
MCP process layer, is the same reasoning applied consistently, not a new principle.
**Decision: a dedicated MCP server, `mcp-servers/agent-memory/`, was approved.**

## Decision 2: Usage constraints for memory MCP tools

Constraints agreed to be enforced structurally in code, not left as documentation — following
the precedent already set by the contradiction-check gate (`memory_maintenance.py`'s
`RuntimeError` on `enable_contradiction_check` without `i_have_completed_adversarial_review`):

- **Read-only first.** No write-capable tool ships in the first pass.
- **Session-scoped episodic reads by default** — cross-session access is explicit opt-in, not
  the default path.
- **Status filtering by default** — `archived` records excluded from search results unless
  explicitly requested.
- **Sacred-record retrieval completeness preserved** — no filter path may silently drop
  `sacred=true` records.
- **No caller-supplied `sacred`/`importance` override** — those remain set by the internal
  write-time heuristic only, never by a tool parameter.
- **Graceful degradation on every path** — no raised exception reaches an agent turn; mirrors
  every other class in `memory_vector_store.py`.

## Decision 3: Why a write tool is deliberately deferred

Every memory write today happens through `PersistentMemorySink`, called by trusted internal
runtime code — never by content an agent merely read. Exposing a write-capable MCP tool
changes that: anything that can get an agent to invoke a tool (including prompt-injected
content in a document, web page, or tool result) could write directly into persistent,
cross-session memory. Combined with Dr. Wieczorek's finding
(`07-adversarial-evaluation-results.md`) that the contradiction-check has zero independent
safeguards against an engineered contradiction, an agent-callable write tool would open a more
direct route to the same class of memory-poisoning risk. A write-capable tool is deferred
until it has been through an adversarial pass specifically targeting prompt-injected write
attempts — the same rigor Dr. Wieczorek already applied to the contradiction-check.

## Next steps

1. Run the Assessment Protocol in `mcp-governance.md` against `agent-memory` before further
   tool development — all four checkboxes, honestly assessed. Add it to the Registered Servers
   table once it passes.
2. Add a new `.mcp.json` entry for `agent-memory`, including the `NO_PROXY` setting already
   required for `qdrant-memory` connectivity.
3. Build the first tool, `search_memory` (read-only), with the Decision 2 constraints as code,
   not comments.
4. Migrate `health_check`'s `memory_instance` block from `workspace-knowledge/server.py` to
   the new server, since it's memory telemetry, not document telemetry.
5. Threat-model a write tool against prompt-injection-driven writes before building one.

## Status

Server skeleton created (`mcp-servers/agent-memory/`) — not yet registered in `.mcp.json`. This
document records the architecture decision; it does not itself constitute governance sign-off
for registration.

**Assessment Protocol run 2026-07-12 (post-skeleton, pre-tool-implementation): fails, as
expected.** Capability and Governance gates pass in principle (semantic search is a genuine
capability gap versus native tools; the only planned tool is read-only, touching no governance
state). Completeness fails outright — zero tools are implemented, so "does every tool produce
real, query-dependent output" and "has each tool been tested against real content" are both
unevaluable, not merely unmet. Per the charter, any unchecked box fails the server regardless of
how the other gates look.

**Assessment Protocol re-run 2026-07-12 (post-`search_memory` implementation): passes, with one
caveat flagged rather than hidden.**

- Capability — pass. Embedding-based semantic search over Qdrant; not replicable with Grep/Glob.
- Governance — pass. Read-only; no pipeline stage, ADR, or approval record is touched; confirmed
  by inspection that the public tool signature accepts no `sacred`/`importance` override.
- Completeness (output varies meaningfully with input) — pass. 17 unit tests confirm the actual
  Qdrant filter construction changes correctly with `memory_type`, `session_id`, `include_dormant`,
  `include_archived`, and `top_k` — not a template returning the same shape regardless of input.
- Completeness (tested against real content) — pass with a caveat. Verified end-to-end against
  the live `qdrant-memory` instance (real network round-trip, real collection targeting, real
  query construction) — this is not mock-only testing. The caveat: `all-MiniLM-L6-v2` (the
  embedding model the memory collections were built for) is not installed in this environment, so
  the live verification used a stub embedding vector, and the live collections hold zero real
  records (same "no production data yet" gap noted for P2). The tool's _correctness_ is verified;
  its _semantic search quality against real content_ is not yet, because neither the model nor the
  content exist yet. That is a data/dependency gap, not a defect in `search_memory` itself.

**Registered 2026-07-12.** CEO accepted the caveat as documented. `agent-memory` is now in
`.mcp.json` (own process, own `env` block including `NO_PROXY`) and in `mcp-governance.md`'s
Registered Servers table, with the Completeness caveat recorded there verbatim rather than
rounded up to an unqualified pass — Capability ✅, Governance ✅, Completeness ⚠️ (pending
`all-MiniLM-L6-v2` installation and real memory writes for a genuine retrieval-quality check).

## Resolution 2026-07-12: embedding-model gap closed, standing provisioning convention established

CEO approved a plan to resolve the `all-MiniLM-L6-v2` gap flagged above and, at the same time,
establish a durable convention for embedding-model provisioning across every CC-00 MCP server —
not a one-off fix scoped only to `agent-memory`.

**What was built:**

- `core-component-00/mcp-servers/_shared/models/` — new shared model cache, a sibling of
  `workspace-knowledge/` and `agent-memory/` under `mcp-servers/`, keyed by slug
  (`<hf-model-id>` with `/` → `--`), matching the naming convention
  `workspace-knowledge/rag-system/download_model.py` already used for its own private cache.
- `core-component-00/mcp-servers/_shared/provision_model.py` — a generalized, idempotent version
  of `download_model.py` that downloads into `_shared/models/<slug>/`. It deliberately drops
  `download_model.py`'s `--activate` step: that step promotes one model into a single active
  slot, which fits `workspace-knowledge` (one FAISS/Qdrant collection, one active model) but not
  the shared cache, which holds multiple concurrently-needed, incompatible-dimension models
  (`workspace-knowledge`'s 768-dim `all-mpnet-base-v2` and `agent-memory`'s 384-dim
  `all-MiniLM-L6-v2`) — there is no single "active" model to promote.
- `agent-memory/server.py`'s `_get_embedder()` updated to a three-tier fallback: (1) load from
  the shared cache if `_shared/models/sentence-transformers--all-MiniLM-L6-v2/` exists, (2) else
  attempt the original direct Hub download, (3) else return `None` and let `search_memory`
  degrade gracefully as before. Tier 3's graceful-degradation behavior is unchanged — this
  resolution adds a faster/offline-capable path in front of it, it does not remove the safety
  net.

**What was explicitly not touched:** `workspace-knowledge/server.py`,
`workspace-knowledge/embedding/`, and `workspace-knowledge/rag-system/download_model.py` — all
out of scope by design, per the CEO's approved plan. `workspace-knowledge`'s existing private
cache is not migrated into the shared cache; the two caches coexist. No cross-server coupling
was introduced: neither `server.py` imports from or references the other, and both read the
shared cache independently at call time (a filesystem convention, not a shared init sequence,
lock, or state file).

**Verification:**

- `sentence_transformers` installed into the environment (was previously absent, confirmed by
  `pip show` returning "Package(s) not found" beforehand).
- `sentence-transformers/all-MiniLM-L6-v2` downloaded via `provision_model.py` into
  `_shared/models/sentence-transformers--all-MiniLM-L6-v2/` — 87.3 MB, embedding dim 384,
  confirmed idempotent (re-run reports "Already cached ... no-op").
- `search_memory` re-verified end-to-end against live `qdrant-memory`
  (`http://localhost:6335`) with the real embedder (not a stub): `_get_embedder()` returns a
  working callable loaded from the shared cache, `search_memory` returns `degraded: False`. The
  live collections still hold zero real records, so results are `count: 0` — expected, and a
  separate gap from the embedder gap just closed (no memory writes exist yet, independent of
  whether the embedder works).
- `context-engineering/testing/`: 180 passed, 1 pre-existing unrelated failure
  (`test_acon_vs_context_compressor`, untouched).
- `mcp-servers/agent-memory/tests/`: 22 passed (17 original + 5 new, covering the shared-cache
  lookup path in `_get_embedder()`) — the one test whose premise was invalidated by this fix
  (`test_wrapper_degrades_gracefully_without_embedding_model_installed`, which asserted
  degradation specifically _because_ the model was absent) was updated to assert the new,
  correct behavior instead of being deleted.

**Governance record updated:** `mcp-governance.md`'s `agent-memory` row and a new standing
"Embedding model provisioning convention" entry — see that file for the current wording. The
Completeness caveat is revised, not cleared: the embedder gap is closed, but retrieval-quality
verification against real content remains blocked on real memory writes existing at all, which
this work did not create.

## Incident 2026-07-12: `search_memory` hangs on cold MCP server start — root cause and fix

After registration, live `mcp__agent-memory__search_memory` tool calls through the actual MCP
protocol repeatedly failed to return, surfaced by the harness as a generic rejection message. Two
hypotheses were investigated and ruled out or confirmed in order, rather than guessing:

1. **Permission/allowlist gap (real, but not the cause of this symptom).** `agent-memory` was
   never added to `.claude/settings.json`'s `enabledMcpjsonServers` (only `workspace-knowledge`
   was listed), and `mcp__agent-memory__search_memory` wasn't in `permissions.allow`. Both were
   fixed — a real, independently-worth-having correction — but the tool call still hung
   identically afterward, ruling this out as the actual cause of the hang.

2. **Cold-start import latency (confirmed root cause).** Measured a genuinely cold Python process
   (not warmed by prior invocations in the same shell session, which had been masking this):

   | Phase | Time |
   |---|---|
   | `import torch` | 2.38s |
   | `import sentence_transformers` | **44.67s** |
   | `import server.py` (fastmcp + qdrant_client + memory_vector_store) | 4.47s |
   | First `search_memory()` call | 1.28s |
   | **Total cold wall time** | **52.80s** |

   The `_get_embedder()` design at the time loaded synchronously on the *first tool call* — so
   that call blocked for 50+ seconds on a freshly-spawned server process, comfortably exceeding
   whatever timeout the MCP client applies. Earlier verification passes in this same session had
   measured ~10s for the equivalent step because the process was already warm (OS file cache,
   compiled `.pyc` bytecode from repeated runs) — a genuinely fresh process pays the full cost.

**Fix:** `server.py` now starts loading the embedder in a background daemon thread the moment the
module is imported (i.e. at server process startup), instead of lazily on first tool call.
`_get_embedder()` is now a non-blocking getter — a call arriving before the background load
finishes returns `degraded: True` immediately (same graceful-degradation contract as every other
failure mode in this module) rather than blocking. Verified: an immediate call on a fresh process
now returns in 0.463s instead of 44+ seconds.

This also required rewriting two tests (`TestGetEmbedderSharedCache`) that assumed the old
synchronous-load contract of `_get_embedder()` — they now call the actual loading function
(`_load_embedder_background()`) directly and synchronously within the test, which tests the real
shared-cache-lookup logic deterministically instead of racing the background thread. Full suite
re-verified: `mcp-servers/agent-memory/tests/`: 22 passed; `context-engineering/testing/`: 180
passed, 1 pre-existing unrelated failure.
