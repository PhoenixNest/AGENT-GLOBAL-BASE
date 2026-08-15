# Research Report — CC-00 MCP Observability Stack (Prometheus + Grafana)

---

## Metadata

| Field                | Value                                                               |
| -------------------- | ------------------------------------------------------------------- |
| **Investigation ID** | `2026-08-08-cc00-mcp-observability-stack`                           |
| **Date Started**     | 2026-08-08                                                          |
| **Date Completed**   | 2026-08-08                                                          |
| **Status**           | Complete                                                            |
| **Investigator**     | Dr. Elias Vance, CC-00 Laboratory Director                          |
| **Laboratory**       | Core Component 00                                                   |
| **Module(s)**        | MCP Server Deployment Surface (`mcp-servers/`), Harness Engineering |
| **Priority**         | Medium                                                              |
| **Requestor**        | CEO, endorsing Dr. Vance's proposal                                 |

---

## Executive Summary

This report specifies a Prometheus + Grafana observability stack for every CC-00 MCP server —
not scoped to `agent-memory` alone. It generalizes the metrics design first proposed for
`agent-memory`'s Phase 5 into a shared instrumentation library, a textfile-based export
mechanism chosen specifically to survive the MCP-host subprocess-churn behavior directly
confirmed during the `agent-memory` stale-process diagnosis, and a fleet-wide Grafana dashboard
alongside per-server views. The specification covers `workspace-knowledge`, `agent-memory`, and
the shared `embedder-service` process. Implementation follows this Programme's standard
design-then-activate pattern: instrumentation code ships inert; no new container is started and
no scrape target is registered as part of delivering this specification.

---

## Investigation Scope

### What Was Investigated

Design of a unified metrics-collection and visualization system covering the operational status
of all CC-00 MCP servers and their shared supporting infrastructure — request volume, latency,
error/degradation rates, backing-store reachability, and (for `agent-memory`) disaster-recovery
freshness.

### Why This Investigation Was Needed

Today, operational status is only observable by directly calling each server's `health_check`
tool — a point-in-time snapshot with no history, no alerting, and no cross-server view. The
`agent-memory` stale-process diagnosis (§ Related Incident History below) also demonstrated that
multiple instances of a server can be alive simultaneously after
a host reconnect — a fleet-wide monitoring layer needs to reflect that reality correctly rather
than assume one process per server.

### Out of Scope

- Application-level tracing (distributed tracing / spans) — this specification covers metrics
  only, not traces or logs.
- Alertmanager routing and on-call/paging configuration — left for a follow-up once the metrics
  themselves are validated.
- Metrics for servers outside `core-component-00/mcp-servers/` (none currently exist in this
  workspace).

---

## Design Specification

### 1. Scope of Coverage

| Component             | Type                                               | Coverage in this design                                                                                             |
| --------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `workspace-knowledge` | Registered MCP server                              | Full tool-level + backing-store instrumentation                                                                     |
| `agent-memory`        | Registered MCP server                              | Full tool-level + backing-store instrumentation, plus DR-backup freshness gauges (`02-deployment-guidelines.md` §9) |
| `embedder-service`    | Shared internal process (not an MCP server itself) | Request-level instrumentation; monitored because both registered servers depend on it                               |

A future registered server picks up coverage automatically by importing the shared
instrumentation library (§2) — this is not a per-server bespoke build.

### 2. Shared Instrumentation Library

New module: `core-component-00/mcp-servers/_shared/metrics.py`. Thin wrapper around
`prometheus_client`'s core collector types:

- `record_tool_call(server, tool, status, duration_s)` — increments a `Counter` and observes a
  `Histogram`, labeled by server and tool name.
- `record_degraded(server, tool, reason)` — increments a `Counter` labeled by reason string,
  mirroring the `reason` field every tool in this codebase already returns on degradation (no new
  vocabulary — reuses each server's existing degradation-reason strings verbatim).
- `set_state_gauge(server, name, value, active_label)` — encodes an enum-shaped state (e.g.
  `embedder_service_state: "ready"`) as the standard Prometheus enum pattern: one gauge per
  possible label value, set to `1` for the active state and `0` for all others.
- `write_textfile(path)` — atomic write (temp file + `os.replace`) of the current registry in
  Prometheus text-exposition format.

Every instrumentation call reuses values each server's `health_check`/tool implementations
already compute — no second source of truth is introduced, the same design constraint the
`agent-memory` Phase 0 `search_capability` block was built under
(§ Related Incident History below, "No second source of truth"). Every call in this library is
non-blocking and never raises, matching every other design in this codebase (`search_memory`,
`health_check`, `QdrantMemoryIndex`'s graceful-degradation contract).

### 3. Export Mechanism — Textfile Collector, Not a Per-Process HTTP Endpoint

The obvious design — each server runs its own embedded `/metrics` HTTP endpoint, the pattern
`embedder-service` already uses — does not fit `workspace-knowledge` or `agent-memory`. The
`agent-memory` stale-process diagnosis directly confirmed (live PID snapshots + `py-spy`,
§ Related Incident History below) that multiple instances of the same server can be
alive simultaneously after a host reconnect. A per-process HTTP endpoint on a fixed port either
port-conflicts across those instances or silently exposes whichever stale instance happens to be
listening — neither is a correct monitoring signal.

Instead, `workspace-knowledge` and `agent-memory` each atomically overwrite one shared textfile
per server identity — `_shared/metrics/workspace-knowledge.prom`,
`_shared/metrics/agent-memory.prom` — after every tool call. Process identity becomes irrelevant:
whichever instance last handled a call has the freshest state, and the atomic-write discipline
(already used for `memory-sync-state.json`) prevents a torn read.

`embedder-service` is the one component where the direct HTTP-endpoint approach is correct and
simplest: it is a genuine long-lived singleton, self-electing via its existing atomic lock file
(`embedder-service.lock`) and self-terminating on idle timeout — there is no multi-instance
question for it the way there is for the two host-spawned MCP servers. It exposes `/metrics`
directly via `prometheus_client.start_http_server()` on a new port (`8793`, alongside its
existing `8791` embed endpoint).

### 4. Collection and Scrape Path

- **New container: `node-exporter`** (or an equivalently minimal purpose-built textfile HTTP
  exporter, to avoid pulling in unrelated host-level metrics `node_exporter` collects by
  default) — configured with `--collector.textfile.directory` pointed at
  `_shared/metrics/`, exposing the two MCP servers' textfiles for scraping.
- **New container: `prometheus`** — two scrape jobs: one against the textfile exporter
  (`workspace-knowledge`, `agent-memory`), one against `embedder-service`'s own `/metrics`
  endpoint directly.
- **New container: `grafana`** — Prometheus as its datasource.

This is three new containers, alongside the two already-running `qdrant-workspace` /
`qdrant-memory` containers.

### 5. Metrics Catalog

**Generic, every component:**

| Metric                           | Type      | Labels                     |
| -------------------------------- | --------- | -------------------------- |
| `mcp_tool_calls_total`           | Counter   | `server`, `tool`, `status` |
| `mcp_tool_call_duration_seconds` | Histogram | `server`, `tool`           |
| `mcp_tool_degraded_total`        | Counter   | `server`, `tool`, `reason` |

**`workspace-knowledge` specific** (sourced from `_document_kb_health_block()`'s existing
computed values):

| Metric                 | Type                 | Notes                                        |
| ---------------------- | -------------------- | -------------------------------------------- |
| `wk_search_tier`       | Gauge (enum pattern) | Mirrors `_tier.value`                        |
| `wk_degraded`          | Gauge                | `1` when `degradation_reason` is non-null    |
| `wk_qdrant_reachable`  | Gauge                | From `memory_instance`/KB reachability block |
| `wk_index_point_count` | Gauge                | Per collection                               |

**`agent-memory` specific** (sourced from `_get_search_capability_snapshot()` and
`compute_memory_instance_telemetry()`, both already built in Phase 0):

| Metric                                  | Type                 | Notes                                                                                                                                              |
| --------------------------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `am_embedder_service_state`             | Gauge (enum pattern) | `disabled` / `starting` / `ready` / `unavailable`                                                                                                  |
| `am_effective_search_path`              | Gauge (enum pattern) | `embedder-service` / `in-process-fallback` / `unavailable`                                                                                         |
| `am_qdrant_reachable`                   | Gauge                |                                                                                                                                                    |
| `am_point_count`                        | Gauge                | Per collection                                                                                                                                     |
| `am_dr_backup_last_success_age_seconds` | Gauge                | Sourced once the DR-backup scripts (`02-deployment-guidelines.md` §9) are activated; reports `NaN`/absent until then rather than a fabricated zero |
| `am_dr_backup_last_verify_age_seconds`  | Gauge                | Same caveat                                                                                                                                        |

**`embedder-service` specific:**

| Metric                              | Type      | Notes                                          |
| ----------------------------------- | --------- | ---------------------------------------------- |
| `es_embed_requests_total`           | Counter   | Labeled by `model`                             |
| `es_embed_request_duration_seconds` | Histogram | Labeled by `model`                             |
| `es_model_loaded`                   | Gauge     | `1` per resident model                         |
| `es_idle_seconds`                   | Gauge     | Time since last in-flight request reached zero |

### 6. Grafana Dashboards

- **Fleet overview** — one row per component, top-line request rate / error rate / p95 latency,
  matching the "golden signals" framing used throughout §5.
- **Per-server detail** — one dashboard each for `workspace-knowledge`, `agent-memory`,
  `embedder-service`, using that component's specific gauges from §5.
- **DR-backup panel** (`agent-memory` dashboard) — `am_dr_backup_last_success_age_seconds` /
  `..._verify_age_seconds` as single-stat panels, directly consuming the Phase 5 backup design
  once it is activated.

### 7. Rollout Sequence

Follows this Programme's standard design-then-activate methodology (the same split already used
for the `agent-memory` DR-backup scripts and, before that, for the Phase 1 write-tool gate):

1. Add `_shared/metrics.py` and wire instrumentation calls into `workspace-knowledge/server.py`,
   `agent-memory/server.py`, and `embedder-service/server.py`. Always-on, always-safe,
   non-blocking — this step alone changes no externally observable behavior of any tool.
2. Add unit tests for `_shared/metrics.py` (atomic write correctness, enum-gauge correctness,
   never-raises contract) following the same test discipline as every other CC-00 module.
3. Author `docker-compose` (or equivalent) definitions for `node-exporter`, `prometheus`, and
   `grafana`, plus the Prometheus scrape config and starter Grafana dashboard JSON.
4. Register the three new containers and confirm end-to-end scrape → dashboard rendering.

Steps 1–3 produce artifacts with no running effect until step 4. Starting the three new
containers requires a separate, explicit authorization, distinct from authorization to produce
this specification.

---

## Analysis

### Trade-offs Identified

| Approach                                                                                 | Survives MCP-host process churn                                | New infra required                  | Complexity |
| ---------------------------------------------------------------------------------------- | -------------------------------------------------------------- | ----------------------------------- | ---------- |
| Per-process embedded `/metrics` endpoint                                                 | No — port conflicts / stale-process exposure (confirmed)       | None                                | Low        |
| Textfile collector + `node-exporter` (recommended, `workspace-knowledge`/`agent-memory`) | Yes                                                            | `node-exporter` container           | Medium     |
| Direct `/metrics` endpoint (recommended, `embedder-service` only)                        | N/A — component is a self-electing singleton, not host-spawned | None (reuses existing HTTP surface) | Low        |

### Risks and Limitations

- Three new always-on containers is a real increase in this workspace's standing infrastructure
  footprint, on top of the two Qdrant containers and `embedder-service` already running.
- `node-exporter`'s default collector set exposes host-level metrics (CPU, disk, etc.) beyond
  what this design needs; the textfile-only configuration in §4 should disable other default
  collectors explicitly, or a minimal purpose-built exporter should be used instead.
- The DR-backup freshness gauges (§5) are only meaningful once the backup scripts
  (`02-deployment-guidelines.md` §9) are themselves activated — until then they correctly report
  absent/`NaN`, not a misleading zero.

---

## Recommendations

### Primary Recommendation

**Adopt the textfile-collector design in §3–4** for `workspace-knowledge` and `agent-memory`,
and the direct-HTTP-endpoint design for `embedder-service`, per the asymmetry justified in §3.

### Implementation Priority

| Recommendation                                                        | Priority | Effort    | Impact                          |
| --------------------------------------------------------------------- | -------- | --------- | ------------------------------- |
| `_shared/metrics.py` + per-server instrumentation (rollout steps 1–2) | P1       | ~1–2 days | High — unblocks everything else |
| Container definitions + scrape config (rollout step 3)                | P1       | ~0.5 day  | Medium                          |
| Activation (rollout step 4)                                           | P2       | ~0.5 day  | High, once authorized           |
| Grafana dashboard JSON (§6)                                           | P2       | ~0.5 day  | Medium                          |

### Next Steps

1. Implement `_shared/metrics.py` and wire it into all three components (rollout step 1).
2. Add the unit test suite for the metrics library (rollout step 2).
3. Author container/compose definitions and Prometheus scrape config (rollout step 3).
4. Obtain explicit authorization for rollout step 4 before starting any new container.

---

## Related Build — `agent-memory` Write-Path Tool Status

> **Moved here 2026-08-10** from the former standalone `2026-07-10-agent-memory-architecture/
supporting/13-write-path-implementation.md`, per CEO direction that implementation-detail
> content for a server's operational status belongs alongside that server's other monitoring
> facts rather than as its own document. This section is the current source of truth for the
> write-path tool's build, evaluation, and activation status; the original document's full
> attack-by-attack methodology remains at that path for readers who need the complete detail
> (Attack Shape write-ups, exact test names, full reversal-condition reasoning) — this section is
> the condensed status record, not a duplicate of it.

**What was built** (five parallel workers, independently reviewed by a sixth, the Final
Integration Agent): `write_gate.py` + a `PreToolUse`/`PostToolUse` hook pair (confirmation gate,
quarantine primitives) — Worker A; `production_judge.py` (`evaluate_contradiction()`, a hardened
judge wrapper with an injection pre-check, symmetry/confidence gates, same-window sequencing) —
Worker B; `write_provenance.py` (non-optional provenance validation, per-session rate limiting) —
Worker C; `write_tool.py` + `server.py` wiring (the testable core and the `@mcp.tool()` wrapper,
gated behind `AGENT_MEMORY_WRITE_TOOL_ENABLED`) — Worker D; an independent re-verification of the
six read-only constraints from Decision 2 (`2026-07-10-agent-memory-architecture/research-report.md`
§ Architecture Decisions) — Worker E.

**Independent adversarial evaluation** (Final Integration Agent, against the real merged code, not
a self-report) ran all five attack shapes enumerated in
`2026-07-10-agent-memory-architecture/research-report.md` § Write-Path Security:

| Attack shape                                          | Result                                                                                                                                                                                                                                                                               |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1. Direct instruction injection                       | **Partial success at the time of evaluation.** Obvious/regex-evading injections were caught and quarantined/gated. The confirmation hook pair existed but was not yet wired into `.claude/settings.json`, leaving a marker-deletion bypass reachable via ordinary shell tool access. |
| 2. Engineered fake contradiction                      | **Full mitigation** — stronger than anticipated: the write tool has no code path that archives/mutates an existing record at all, so this attack cannot succeed against the current build regardless of judge quality.                                                               |
| 3. Repeated/automated write attempts                  | **Full mitigation** — `WriteRateLimiter` rejects well before 50 calls, with telemetry reflecting the rejected burst.                                                                                                                                                                 |
| 4. Cross-session/cross-user persistence amplification | **Full mitigation** — quarantined records are unreachable from `search_memory` under every filter combination; no signature parameter can self-promote a quarantined record.                                                                                                         |
| 5. Metadata/parameter smuggling                       | **Full mitigation** — `sacred`/`importance`/`status`/`tags` are excluded from the tool signature and hardcoded server-side; runtime smuggling attempts raise `TypeError`.                                                                                                            |

**Go/no-go verdict at evaluation time: conditional go.** Condition for activation: wire the
confirmation hook pair into `.claude/settings.json` before setting
`AGENT_MEMORY_WRITE_TOOL_ENABLED=true`. That condition was subsequently satisfied (2026-08-09/10):
the hook pair was wired and independently re-audited, closing the marker-deletion bypass for
sequential tool-call sessions. **One uncertainty remains open:** whether `PreToolUse` hooks fire
strictly sequentially for a batched/parallel set of tool calls within one assistant turn was never
directly tested — a dedicated concurrency test is recommended before treating this condition as
unconditionally closed.

**Current activation status (2026-08-10, live-verified):** `AGENT_MEMORY_WRITE_TOOL_ENABLED=true`
in `.mcp.json`; `write_memory` confirmed registered as a live MCP tool via `ToolSearch` schema
load and a live `health_check()` call (`reachable: true`, `search_capability.effective_path:
"embedder-service"`, populated `write_rate_limiting` telemetry). The confirmation-hook pair and
this workspace's H-P01 write-confirmation flow both still apply to any actual write attempt.

**Regression suites at merge time:** `mcp-servers/agent-memory/tests/` — 205 passed (186
pre-existing + 19 new adversarial tests). `engineering/context-engineering/testing/` — 308 passed,
1 pre-existing unrelated failure (`test_acon_vs_context_compressor`, untouched by this build).

**Monitoring implication for this report's own metrics catalog (§5):** the `write_rate_limiting`
telemetry block `health_check()` now returns is not yet reflected in the `am_*` metrics table
above — a future revision of this catalog should add `am_write_tool_enabled` (Gauge) and
`am_write_rate_limit_rejections_total` (Counter) sourced from that block, following the same
"reuse values the server already computes" constraint §2 establishes for every other metric here.

Full detail on the threat model this build was evaluated against (exact attack-shape definitions,
reversal-condition reasoning): `2026-07-10-agent-memory-architecture/research-report.md` §
Write-Path Security (formerly the standalone `supporting/11-write-path-threat-model.md`, retired).
The former standalone `13-write-path-implementation.md` (this section's source, before this move)
is retired — its executable evidence (`test_write_path_adversarial_evaluation.py`) remains in
place and is the authoritative record for anyone needing the exact per-test methodology this
section condenses.

---

## Related Incident History — `agent-memory` Observability Fix and Issue Log

> **Moved here 2026-08-10** from the former standalone `2026-07-10-agent-memory-architecture/
supporting/10-observability-fix.md`, per CEO direction to consolidate agent-memory's monitoring
> and incident history alongside this report's other operational facts rather than as its own
> document. Content condensed from the original; no finding, timing figure, or root-cause
> conclusion was altered.

### The observability blind spot and its fix (2026-08-06)

A same-day P1 fix (embedder-service readiness retry — one-shot startup probe that permanently
recorded `_embedder_service_state = "unavailable"` if it lost the race against the shared
`embedder-service` still starting) exposed a structural gap: nothing in `health_check`'s output
would have told anyone the search path was degraded in the first place. **Fix:** a new
`search_capability` block, sibling to `memory_instance`, reporting
`embedder_service_enabled`/`embedder_service_state`/`in_process_fallback_state`/`effective_path`.
Implemented as a pure function (`_get_search_capability_snapshot()`) reading the same module
globals `_get_embedder()` already uses — no second source of truth — never triggering the lazy
warmup thread, and never raising (degrades to a labeled `"unavailable"` state instead).

**Cross-server `health_check` comparison test** (closing a P2 from the 2026-07-17
agent-memory client-instability investigation — telescope record removed 2026-08-13 as a
completed maintenance-operation, per this correction, dated 2026-08-13; summary preserved in
`.claude/rules/mcp-governance.md`'s `agent-memory` row): a pure comparison function plus
7 deterministic unit tests, plus one live integration test that calls both servers' real
`health_check` construction paths independently (not a shared client, since the original incident's
failure mode was one server's own construction path hanging while the other succeeded). Result in
this environment: live and reachable, no divergence found.

**Stale duplicate-process investigation:** static analysis (all background threads are
`daemon=True`; no self-spawned subprocess; stdio transport's `async for line in stdin` is the
standard clean-exit mechanism) plus a direct empirical test (zero new threads spawned by
`QdrantClient` construction/first-call in the installed version, contradicting one detail of an
earlier incident's `py-spy` evidence — recorded as an open discrepancy, not smoothed over).
Conclusion at the time: no agent-memory-owned defect found; root locus reasoned (not yet
empirically confirmed) to be MCP-host subprocess lifecycle. A concrete diagnosis plan was left for
a future live-reconnect session — see the addendum below, where it was executed.

**Test suite gap closed:** governance docs cited a committed `mcp-servers/agent-memory/tests/`
suite that didn't exist in git history. Root cause: `agent-memory/.gitignore` had a bare `tests/`
line — a bare directory pattern excludes the directory from Git's tree-walk entirely, so
`!tests/<file>` negation exceptions after it can never re-include anything, regardless of intent.
Fixed to the `tests/*` + explicit-exceptions form `workspace-knowledge/.gitignore` already used
correctly. A real, committed suite followed: 43 tests (`conftest.py`, `test_server.py`,
`health_comparison.py`, `test_cross_server_health_comparison.py`), all passing, including the live
cross-server test actually exercising real Qdrant. Regression suite: 283 passed, 1 pre-existing
unrelated failure, confirmed unchanged.

### Addendum — stale-process diagnosis, live verification (2026-08-07)

Executed directly by Dr. Elias Vance in a live interactive session (the real MCP client connection
capability no subagent/worktree build had). One reconnect cycle: a process-list snapshot before
(4 PIDs) and after (2 of 4 old PIDs survived, 2 cleaned up, 2 new spawned) confirmed stale PIDs
_do_ survive reconnects, non-deterministically, and reconnects net _add_ processes. `py-spy dump`
on a surviving PID showed the main thread idle inside the asyncio event loop's I/O poll — genuinely
still waiting for input the host never sent after reconnecting, not crashed or spinning. **This
upgraded the 2026-08-06 hypothesis from reasoned-but-unobserved to directly confirmed: stdin is not
being closed by the host on reconnect, an MCP-host (Claude Code CLI) subprocess-lifecycle question,
not an `agent-memory`-owned defect.** No code fix against `agent-memory`/`server.py` was warranted
from this finding.

### Addendum — sibling-process cleanup, built on this diagnosis, and its own bug history (2026-08-09/10)

The diagnosis above didn't rule out an on-demand, best-effort mitigation running inside
`agent-memory` itself, and one was built: `_cleanup_stale_sibling_processes()`, run at module-import
time, terminating other live `python.exe` processes running the same script (gated by
`AGENT_MEMORY_ENABLE_SIBLING_CLEANUP`, default on). Its own bug history, found and fixed same
day/week:

1. **Path-matching bug.** First version compared against a fully-resolved absolute path; `.mcp.json`
   launches with a relative path, so the scan matched zero real processes on any run. Fixed to
   match on a workspace-relative path suffix.
2. **Mutual-kill race.** Once path-matching worked, it exposed that the host spawns two agent-memory
   processes seconds apart on reconnect, each treating the other as stale and killing it before
   either completed the MCP handshake — reconnects began failing outright. Fixed with a
   minimum-age gate.
3. **Three further gaps from independent deep review** (Kwame Asante, Connor O'Malley, Dr. Tomasz
   Wieczorek): the age margin didn't cover the documented cold-start worst case; the path-suffix
   match alone was identical across every git-worktree checkout, so a worktree's live server could
   be killed by the main checkout's cleanup (fixed by additionally scoping to the same host process
   via `ParentProcessId`); a NaN override could slip past the age-floor clamp (fails safe in
   practice, but violated the code's own stated invariant — fixed).

### Inherited incident — embedding-model gap closed, standing provisioning convention established (2026-07-12)

An `all-MiniLM-L6-v2` availability gap flagged during `agent-memory`'s Assessment Protocol re-run
was closed while simultaneously establishing a durable embedding-model provisioning convention for
every CC-00 MCP server: a new shared cache (`mcp-servers/_shared/models/`, keyed by slug), a
generalized `provision_model.py` (no single-active-slot promotion, since the shared cache holds
multiple concurrently-needed, incompatible-dimension models), and a three-tier `_get_embedder()`
fallback (shared cache → direct Hub download → graceful `None` degradation, unchanged safety net).
Verified: `sentence-transformers/all-MiniLM-L6-v2` downloaded (87.3 MB, dim 384, idempotent re-run
confirmed); `search_memory` re-verified end-to-end against live `qdrant-memory` with the real
embedder (`degraded: False`); 180 context-engineering tests passed (1 pre-existing unrelated
failure); 22 agent-memory tests passed (17 original + 5 new).

### Inherited incident — `search_memory` hangs on cold MCP server start (2026-07-12)

Live tool calls repeatedly failed to return after registration. Two hypotheses tested in order:
(1) a real but not-the-cause permission/allowlist gap (fixed independently, hang persisted); (2)
**cold-start import latency, confirmed root cause** — a genuinely cold process measured
`import sentence_transformers` alone at 44.67s, total cold wall time 52.80s, because `_get_embedder()`
loaded synchronously on the _first tool call_, blocking well past the MCP client's timeout. Earlier
passes in the same session had measured ~10s because the process was already warm (OS file cache,
compiled bytecode) — masking the real cold-start cost. **Fix:** `server.py` now starts loading the
embedder in a background daemon thread at module-import time instead of lazily on first call;
`_get_embedder()` is a non-blocking getter, returning `degraded: True` immediately if the load
hasn't finished rather than blocking. Verified: an immediate call on a fresh process dropped from
44+ seconds to 0.463s.

---

## References

### Internal Documentation

- § Related Incident History above — `search_capability` block design, stale-process diagnosis evidence this report's §3 argument depends on (merged 2026-08-10 from the former standalone `2026-07-10-agent-memory-architecture/supporting/10-observability-fix.md`)
- `core-component-00/telescope/2026-07-10-agent-memory-architecture/supporting/02-deployment-guidelines.md` §9 — DR-backup scripts (merged there 2026-08-10 from the former standalone `12-dr-backup-design.md`), source of the `am_dr_backup_*` gauges in §5
- `core-component-00/mcp-servers/_shared/embedder_client.py` — `embedder-service` lifecycle (self-election lock file, idle self-termination) underlying the §3 asymmetry
- `.claude/rules/mcp-governance.md` § Shared Infrastructure — `embedder-service` — existing HTTP-endpoint precedent this design's `embedder-service` branch follows
- `core-component-00/mcp-servers/workspace-knowledge/server.py` — `_document_kb_health_block()`, `search_tier`/`degradation_reason` fields sourced in §5

---

## Version History

| Version | Date       | Author                               | Changes                                                                                                                                                                                                                                                                                     |
| ------- | ---------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-08-08 | Dr. Elias Vance (Lab Director)       | Initial specification, CEO-endorsed                                                                                                                                                                                                                                                         |
| 1.1     | 2026-08-10 | Claude (CC-00 documentation steward) | Added "Related Build — `agent-memory` Write-Path Tool Status" section, moved from the former standalone `13-write-path-implementation.md` per CEO documentation-coherence direction; updated `12-dr-backup-design.md` references to point at its new home, `02-deployment-guidelines.md` §9 |
| 1.2     | 2026-08-10 | Claude (CC-00 documentation steward) | Added "Related Incident History — `agent-memory` Observability Fix and Issue Log" section, moved from the former standalone `10-observability-fix.md` per CEO direction to remove documents 06–11 from that investigation's `supporting/` folder                                            |

---

**Template Version:** 1.0
**Last Updated:** 2026-08-08
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
