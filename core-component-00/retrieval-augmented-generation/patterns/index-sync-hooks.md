# Pattern: Phase-Adaptive Index Sync Hook

**Status:** Production-verified (agent-native deployment, 2026-06-26)
**Closes:** Retrieval Freshness Guarantees research programme

---

## Problem Statement

RAG pipelines built on embedded or out-of-process vector indexes face a structural staleness
problem in agent-native environments: indexes are typically built at server startup and remain
frozen for the lifetime of the process. When agents write or modify source documents mid-session,
subsequent retrieval operations silently return pre-modification content — a correctness failure
with no error signal. The agent observes no exception; it simply receives stale results.

This failure mode is especially pronounced in document-editing workflows where the same session
that writes documents immediately queries them (e.g., pipeline documentation updates, knowledge
base maintenance). The staleness window is unbounded without an explicit refresh mechanism.

---

## Solution Overview

Deploy a **post-write hook** that:

1. Detects writes to indexed source directories
2. Reads a **shared state file** to determine the active sync mode and retrieval backend
3. Dispatches the appropriate index-update tool — either a full rebuild or an incremental
   upsert — based on the active backend

The hook is **phase-adaptive**: its update path changes as the underlying retrieval backend
evolves (e.g., FAISS full-rebuild → Qdrant incremental upsert) without requiring code changes
to the hook itself. Only the state file requires updating at each phase transition.

---

## Critical Design Constraint: State File, Not Environment Variables

The hook process and the MCP server process are **separate OS processes**. Environment variables
set within the MCP server's process environment (e.g., `SEARCH_BACKEND`) are invisible to
the hook process. Using an environment variable as the inter-process signal for backend selection
produces a silent correctness bug: the hook reads the variable as absent or at its default value
regardless of what the server has configured, and dispatches the wrong update tool indefinitely.

**Use a shared JSON state file as the inter-process communication channel.** Both the MCP server
and the hook process can read and write a file on disk, making it the only reliable mechanism for
sharing configuration state across process boundaries.

### Common Pitfall: Process-Scoped Configuration Leakage

Do not use environment variables set by the retrieval server process to govern hook behaviour.
Environment variables are scoped to the process that sets them and are not inherited by unrelated
processes such as post-write hooks. Relying on them produces a silent correctness failure: the
hook reads the variable as absent (or at its shell default) regardless of the server's runtime
configuration, and dispatches the wrong index-update tool with no error signal.

This failure mode is particularly dangerous because it is invisible at deployment time — the hook
appears to function correctly (it fires and produces output) while systematically dispatching the
wrong tool for the active backend.

**Rule:** Any configuration value that must be shared between the retrieval server process and the
hook process must be stored in a file accessible to both. The state file is the designated shared
channel for this purpose. Do not use process-scoped environment variables, in-memory singletons,
or other process-scoped mechanisms as cross-process signals.

---

## State File Contract

**Location:** Adjacent to the retrieval server implementation directory — e.g.,
`<retrieval-server-dir>/rag-system/rag-sync-state.json`

**Schema:**

```json
{
  "mode": "auto",
  "debounce_seconds": 10,
  "last_rebuild_at": 1750000000,
  "search_backend": "qdrant"
}
```

| Field              | Type    | Values                      | Description                                         |
| ------------------ | ------- | --------------------------- | --------------------------------------------------- |
| `mode`             | string  | `"auto"`, `"warn"`, `"off"` | Hook operating mode                                 |
| `debounce_seconds` | integer | ≥ 0                         | Minimum seconds between consecutive update triggers |
| `last_rebuild_at`  | integer | Unix epoch seconds          | Timestamp of the last triggered index update        |
| `search_backend`   | string  | `"faiss"`, `"qdrant"`       | Active retrieval backend — governs tool dispatch    |

**Mode semantics:**

| Mode   | Behaviour                                                                        |
| ------ | -------------------------------------------------------------------------------- |
| `auto` | Trigger index update automatically after qualifying writes (subject to debounce) |
| `warn` | Emit a passive staleness notice; operator must invoke the update tool manually   |
| `off`  | Silent; no notification and no update trigger                                    |

`warn` is the recommended default for new deployments and for any batch-write scenario where
automatic updates would produce multiple transient partial-index states visible to concurrent
queries.

---

## Phase-Adaptive Tool Dispatch

The `search_backend` field maps directly to the index-update tool the hook instructs:

| `search_backend` | Index update tool | Rationale                                                                                                   |
| ---------------- | ----------------- | ----------------------------------------------------------------------------------------------------------- |
| `"faiss"`        | `rebuild_index`   | FAISS requires full re-encoding of all corpus chunks; no incremental update path exists                     |
| `"qdrant"`       | `upsert_document` | Qdrant supports per-file incremental upsert; full collection rebuild is unnecessary for single-file changes |

**Migration phase alignment:**

| Phase                                                 | `search_backend` | Primary update tool                                 | Recommended `debounce_seconds` |
| ----------------------------------------------------- | ---------------- | --------------------------------------------------- | ------------------------------ |
| 0 — FAISS only                                        | `"faiss"`        | `rebuild_index`                                     | 30                             |
| 1 — Shadow mode (FAISS primary, Qdrant shadow writes) | `"faiss"`        | `rebuild_index` (+ shadow `upsert_document`)        | 30                             |
| 2 — Qdrant primary, FAISS hot standby                 | `"qdrant"`       | `upsert_document` (+ `rebuild_index` for DR parity) | 10                             |
| 3 — Qdrant primary, FAISS permanent warm standby      | `"qdrant"`       | `upsert_document` only                              | 10                             |

Phase transitions require only a state file update (`search_backend` field). The hook code
requires no modification at any phase transition.

---

## Debounce Calibration

The debounce threshold prevents cascade-triggered updates during batch write operations (e.g.,
an agent writing 20 files in a single turn, which would otherwise trigger 20 sequential
partial-index states). Calibrate the threshold to the latency of the active update tool:

- **Full rebuild (FAISS):** 15–60 s depending on corpus size and hardware. Set `debounce_seconds` ≥ 30.
- **Incremental upsert (Qdrant):** 1–5 s per file at current corpus scale (≤ 10,000 chunks on
  RTX 4060). Set `debounce_seconds` ≥ 10.

Recalibrate at each migration phase transition by benchmarking the new update tool before
adjusting the threshold. Do not inherit the prior phase's threshold without re-measurement.

---

## Indexed Directory Scope

Apply the hook only to source directories that are indexed by the retrieval pipeline. Triggering
on all file writes is wasteful (unnecessary index updates) and potentially incorrect (unintended
seeding from temporary or generated files).

**Pattern for directory matching (pseudocode):**

```
# Normalize path separators to forward slashes (step is platform-specific)
normalized_path = normalize_path_separators(file_path)

# Define the set of indexed root directories
indexed_dirs = ["company/", "studio/", "core-component-00/", "telescope/"]

# Require a boundary match: the directory name must begin at the path root or
# immediately follow a separator — prevents partial-name matches
# (e.g., "extra-company/" must NOT match "company/")
in_indexed_dir = false
for dir in indexed_dirs:
    if normalized_path matches regex pattern "(^|/)" + dir:
        in_indexed_dir = true
        break

if not in_indexed_dir:
    skip()  # file is outside all indexed directories — no action

# Apply only to source document files (extension is deployment-specific)
if not normalized_path ends_with(".md"):
    skip()
```

The boundary-match pattern `(^|/)dir` ensures the indexed directory name is matched at the path
root or after a separator, not as a substring of another directory name.

---

## Freshness Signal in MCP Tool Responses

Surface index freshness directly in every MCP tool response via a `_meta` block. This allows
agents to inspect whether the current index reflects recent writes without requiring a separate
health-check call.

```python
def _meta_block(self) -> dict:
    return {
        "search_tier": self._tier.value,
        "backend": SEARCH_BACKEND,
        "index_built_at": self._index_built_at,   # ISO 8601 UTC timestamp
    }
```

`index_built_at` is set on server startup and updated after each rebuild or upsert. Agents can
cross-reference this timestamp against the `last_rebuild_at` in the state file to detect whether
a write has occurred since the last index update.

---

## Operator Control Interface

Pair the hook with an operator-facing configuration manager that reads and writes the state file
without requiring direct JSON editing. The invocation mechanism is runtime-specific; the
following five operations must be exposed regardless of implementation:

| Operation           | Effect                                                         |
| ------------------- | -------------------------------------------------------------- |
| `set-mode auto`     | Enable automatic updates with debounce                         |
| `set-mode warn`     | Passive notices only; operator-triggered updates               |
| `set-mode off`      | All sync disabled; no notifications                            |
| `status`            | Report current mode, debounce threshold, last update timestamp |
| `set-threshold <N>` | Set `debounce_seconds` to N                                    |

**Recommended mode by scenario:**

| Scenario                                              | Mode                                          |
| ----------------------------------------------------- | --------------------------------------------- |
| Normal single-file edits                              | `auto`                                        |
| Batch pipeline operations (≥ 10 file writes per turn) | `warn` before batch; restore after            |
| Multi-agent swarm (agents share the MCP server)       | `warn` — let each agent decide when to update |
| Exploratory / performance-sensitive sessions          | `off` + manual update call at checkpoints     |

---

## Resolution of Retrieval Freshness Guarantees Research Programme

**Research question (prior):** "Bounding staleness of retrieved facts at inference time."

**Empirical resolution:** In agent-native, document-editing deployments with a shared MCP
retrieval server, the staleness bound is determined by the hook debounce threshold, not by an
architectural property of the index.

With `mode = auto` and `debounce_seconds = 10` using an incremental upsert backend:

```
max_staleness ≤ debounce_seconds + upsert_tool_latency
              ≤ 10 s + 5 s   (Qdrant upsert, RTX 4060, ≤ 10,000 chunks)
              = 15 s worst case under single-file edit cadence
```

For batch-write scenarios (`mode = warn`): staleness is bounded by the operator's explicit
decision to call the update tool. This is intentional — automatic updates during a large batch
would produce multiple sequential partial-index states, each briefly visible to concurrent
queries.

**Conclusion:** Freshness guarantees in this architecture class are a **policy decision** (debounce
threshold and mode selection), not an architectural invariant. The appropriate guarantee level is
configurable and must be calibrated to the deployment's tolerance for staleness vs. update churn.
There is no single correct threshold — the tradeoff is between retrieval currency and update
overhead.

---

## Generalisation to Other Deployment Contexts

This pattern applies to any deployment satisfying all three conditions:

1. A retrieval index is built at process startup and not refreshed in-process during a session
2. Agent tool calls can modify source documents within the same session
3. Multiple processes (retrieval server + hook or trigger) share retrieval configuration state

The state file IPC mechanism is universally applicable. The tool dispatch logic (rebuild vs.
upsert) is backend-specific and must be re-specified for backends other than FAISS and Qdrant.
The debounce threshold is hardware- and corpus-specific and must be calibrated empirically.

---

## References

- `telescope/2026-06-25-qdrant-migration-plan/plans/05-hook-design.md` — H-RAG02 implementation
  specification (workspace-specific production implementation)
- `telescope/2026-06-25-qdrant-migration-plan/plans/04-monitoring-guide.md` — Index freshness
  monitoring and MRR regression detection
- `core-component-00/retrieval-augmented-generation/architecture/overview.md` — Graceful
  Degradation Stack (§11) and Corpus-as-Source-of-Truth Principle (§10)
- `core-component-00/retrieval-augmented-generation/evaluation/reference-table.md` —
  Incremental Upsert vs. Full-Rebuild Decision Framework
