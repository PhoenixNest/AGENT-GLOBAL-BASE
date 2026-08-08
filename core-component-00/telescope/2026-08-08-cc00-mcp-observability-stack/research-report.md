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
`agent-memory` stale-process diagnosis (`2026-07-10-agent-memory-architecture/supporting/10-observability-fix-phase0.md`,
addendum) also demonstrated that multiple instances of a server can be alive simultaneously after
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

| Component             | Type                                               | Coverage in this design                                                                                     |
| --------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `workspace-knowledge` | Registered MCP server                              | Full tool-level + backing-store instrumentation                                                             |
| `agent-memory`        | Registered MCP server                              | Full tool-level + backing-store instrumentation, plus DR-backup freshness gauges (`12-dr-backup-design.md`) |
| `embedder-service`    | Shared internal process (not an MCP server itself) | Request-level instrumentation; monitored because both registered servers depend on it                       |

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
(`10-observability-fix-phase0.md` § "No second source of truth"). Every call in this library is
non-blocking and never raises, matching every other design in this codebase (`search_memory`,
`health_check`, `QdrantMemoryIndex`'s graceful-degradation contract).

### 3. Export Mechanism — Textfile Collector, Not a Per-Process HTTP Endpoint

The obvious design — each server runs its own embedded `/metrics` HTTP endpoint, the pattern
`embedder-service` already uses — does not fit `workspace-knowledge` or `agent-memory`. The
`agent-memory` stale-process diagnosis directly confirmed (live PID snapshots + `py-spy`,
`10-observability-fix-phase0.md` § Addendum) that multiple instances of the same server can be
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
| `am_dr_backup_last_success_age_seconds` | Gauge                | Sourced once the Phase 5 DR-backup scripts (`12-dr-backup-design.md`) are activated; reports `NaN`/absent until then rather than a fabricated zero |
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
- The DR-backup freshness gauges (§5) are only meaningful once the Phase 5 backup scripts
  (`12-dr-backup-design.md`) are themselves activated — until then they correctly report
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

## References

### Internal Documentation

- `core-component-00/telescope/2026-07-10-agent-memory-architecture/supporting/10-observability-fix-phase0.md` — `search_capability` block design, stale-process diagnosis evidence this report's §3 argument depends on
- `core-component-00/telescope/2026-07-10-agent-memory-architecture/supporting/12-dr-backup-design.md` — Phase 5 DR-backup scripts, source of the `am_dr_backup_*` gauges in §5
- `core-component-00/mcp-servers/_shared/embedder_client.py` — `embedder-service` lifecycle (self-election lock file, idle self-termination) underlying the §3 asymmetry
- `.claude/rules/mcp-governance.md` § Shared Infrastructure — `embedder-service` — existing HTTP-endpoint precedent this design's `embedder-service` branch follows
- `core-component-00/mcp-servers/workspace-knowledge/server.py` — `_document_kb_health_block()`, `search_tier`/`degradation_reason` fields sourced in §5

---

## Version History

| Version | Date       | Author                         | Changes                             |
| ------- | ---------- | ------------------------------ | ----------------------------------- |
| 1.0     | 2026-08-08 | Dr. Elias Vance (Lab Director) | Initial specification, CEO-endorsed |

---

**Template Version:** 1.0
**Last Updated:** 2026-08-08
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
