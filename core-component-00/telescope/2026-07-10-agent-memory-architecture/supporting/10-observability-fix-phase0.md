# Observability Fix — Phase 0 (agent-memory Enterprise-Readiness Build)

**Parent Report:** `../research-report.md`
**Relates to:** `09-mcp-architecture-decision.md` (Next Steps items 1 and 5),
`2026-07-17-agent-memory-client-instability/research-report.md` (Recommendations item 2)
**Date:** 2026-08-06
**Authorized by:** CEO, via Dr. Elias Vance (Lab Director) — Phase 0 (full execution)
**Executed by:** Worker A (`agent/observability/phase0-health-check`), git-worktree-isolated build

---

## Context

Earlier the same day (2026-08-06), a P1 was found and fixed (commit `f655c21e`): the
embedder-service readiness check in `agent-memory/server.py` was one-shot — a single probe at
process startup that, if it lost the race against the shared `embedder-service` still coming up,
permanently recorded `_embedder_service_state = "unavailable"` for the rest of the process's life,
even after the service became healthy seconds later. The fix (`_embedder_service_ready()`'s
re-probe-on-cooldown logic) closed the underlying bug, but it also exposed a separate, structural
gap: **nothing in `health_check`'s output would have told anyone the search path was degraded in
the first place.** A caller watching `health_check` alone had no way to distinguish "search is
fully healthy" from "search is silently falling back, or fully unavailable" — the only visible
signal was `memory_instance` (Qdrant reachability/point counts), which says nothing about whether
`search_memory`'s embedding step can actually run. This document records the fix for that
observability blind spot, plus the other Phase 0 deliverables authorized alongside it.

---

## What Was Built

### 1. `search_capability` block in `health_check`

`agent-memory/server.py`'s `health_check()` tool now returns a second top-level block, sibling to
`memory_instance`:

```python
{
  "memory_instance": {...unchanged...},
  "search_capability": {
    "embedder_service_enabled": bool,
    "embedder_service_state": str,     # "disabled" | "starting" | "ready" | "unavailable"
    "in_process_fallback_state": str,  # "not started" | "loading" | "ready" | "failed: <reason>"
    "effective_path": str,             # "embedder-service" | "in-process-fallback" | "unavailable"
  }
}
```

Implemented as a new pure function, `_get_search_capability_snapshot()`, kept separate from the
`@mcp.tool()` wrapper — the same split already used for `_search_memory_impl()` vs. `search_memory()`,
so the logic is directly unit-testable without a live embedder-service or Qdrant instance.

**Design constraints honored:**

- **No second source of truth.** The snapshot reads the exact same module globals
  `_get_embedder()`/`_get_embedder_unavailable_reason()` already use
  (`EMBEDDER_SERVICE_ENABLED`, `_embedder_service_state`, `_embedder_state`, `_embedder_cache`),
  under the same locks. It re-presents that state in a `health_check`-shaped block; it does not
  compute a second, independently-derived answer that could drift from what `_get_embedder()`
  would actually do.
- **Read-only — never triggers the lazy warmup thread.** `_get_search_capability_snapshot()` does
  not call `_ensure_embedder_load_started()`. Calling `health_check` must never itself cause the
  eager background-import work the 2026-07-17 fix deliberately made lazy-only (see that
  investigation's Findings 4/5, and `.claude/rules/mcp-governance.md`'s `agent-memory` row) — a
  monitoring call triggering the exact class of side effect that fix removed would be a
  regression, not an improvement. `effective_path`'s precedence mirrors `_get_embedder()`'s own
  precedence exactly (service-ready wins, else in-process-cache-if-already-loaded, else
  "unavailable") but never starts anything that isn't already running.
- **Never raises.** Every state read is a plain lock-guarded attribute read; any unexpected error
  degrades to a clearly-labeled `effective_path: "unavailable"` / `in_process_fallback_state:
"failed: snapshot error: <exc>"` rather than propagating — consistent with every other function
  in this module (`_search_memory_impl`, `_search_reflection`, `health_check`'s own outer
  try/except).

### 2. Automated cross-server `health_check` comparison test

Closes Recommendation 2 from `2026-07-17-agent-memory-client-instability/research-report.md`
("Add a lightweight comparison test that calls both servers' health_check back-to-back in
CI-like conditions, so a future regression like Finding 3 surfaces automatically instead of
requiring a manual CEO-requested review to discover") — previously tracked as "Not started" in
that report's Implementation Priority table.

**`workspace-knowledge/server.py` refactor (the one narrow, explicitly-permitted touch to that
file):** `_memory_instance_health_block()` previously constructed its own `QdrantClient`
internally with no way to inject a different one. Split into:

- `_memory_instance_health_block_impl(client)` — the actual telemetry-assembly logic, now
  accepting an injected client (or `None`), mirroring the dependency-injection pattern
  `agent-memory/server.py` already uses for `_search_memory_impl`.
- `_memory_instance_health_block()` — thin wrapper, unchanged behavior: constructs the real
  production `QdrantClient` (or `None` on failure) and delegates to `_impl`.

No other change was made to `workspace-knowledge/server.py`.

**Test structure** (`agent-memory/tests/`), split into two layers per the assigned design:

- `health_comparison.py` — `compare_memory_instance_health(block_a, block_b)`, a pure,
  side-effect-free function that flags a differing `reachable` flag or a differing per-collection
  point count between two `memory_instance`-shaped blocks. Not a registered MCP tool; test-support
  code only.
- `test_cross_server_health_comparison.py::TestCompareMemoryInstanceHealthLogic` — 7 deterministic
  unit tests against fixed, hand-built input dicts (identical blocks, differing `reachable`,
  differing point count, a collection present on only one side, multiple simultaneous
  differences, both-empty, missing keys). No live Qdrant instance required.
- `test_cross_server_health_comparison.py::TestLiveCrossServerComparison` — one live integration
  test. Calls `agent_memory_server.health_check()` first as the reachability gate (using
  agent-memory's own real production code path, not a hand-rolled duplicate probe); `pytest.skip()`s
  cleanly if `qdrant-memory` is unreachable. If reachable, imports `workspace-knowledge/server.py`
  (with `WORKSPACE_ROOT` pointed at a throwaway empty directory first, so its module-level
  `SearchEngine` construction has nothing to scan) and calls its own
  `_memory_instance_health_block()` — **each server exercises its own client-construction path
  independently**, not a shared client object, since Finding 3's actual failure mode
  (`2026-07-17-agent-memory-client-instability/research-report.md`) was specifically one server's
  own construction path hanging/failing while the other succeeded; a shared client would not have
  been able to catch that class of regression.

**Result in this environment:** `qdrant-memory` was live and reachable during this build, so the
live test ran for real (not skipped) and reported **no divergence** between the two servers'
`memory_instance` views of the same instance.

### 3. Stale duplicate-process investigation

**Outcome: investigated via static analysis and direct testing in this environment; no
agent-memory-owned defect found; root locus judged, with reasoning but not direct observation, to
be MCP-host-side subprocess lifecycle — documented here as a deferred, concretely-scoped
follow-up rather than silently dropped, per the explicit instruction not to guess without
evidence.**

What was checked:

- **Every background thread `agent-memory/server.py` starts is `daemon=True`**
  (`_load_embedder_background`'s `embedder-warmup` thread, `_start_embedder_service_background`'s
  `embedder-service-warmup` thread). A daemon thread cannot by itself keep the Python process
  alive past normal interpreter shutdown — ruled out as a self-inflicted cause of a lingering
  process.
- **`agent-memory/server.py` never spawns a subprocess of itself** and carries no
  `DETACHED_PROCESS`/`CREATE_NEW_PROCESS_GROUP` flags (unlike `embedder_client.py`'s deliberate
  use of those flags for `embedder-service` — see below for why that distinction matters).
- **The stdio transport itself** (`mcp/server/stdio.py`, vendored dependency, not this
  workspace's code): `stdin_reader()` does `async for line in stdin`, which ends normally on EOF,
  closing `read_stream_writer` and (via the owning `anyio.create_task_group()`) unwinding
  `mcp.run()` so the process should fall off the bottom of `server.py` and exit — this is the
  standard, expected mechanism by which an MCP host disconnecting/closing a subprocess's stdin
  causes that subprocess to exit cleanly. Nothing in this vendored code is workspace-owned or was
  modified here.
- **Direct empirical test in this environment** (not inference): constructed a real `QdrantClient`
  against `http://localhost:6335` and enumerated `threading.enumerate()` before/after both
  construction and a live `get_collections()` call. **Result: zero new threads spawned in either
  case**, in the currently-installed `qdrant-client` version. This directly contradicts one
  specific detail of `2026-07-17-agent-memory-client-instability/research-report.md`'s Finding 4
  `py-spy` evidence, which showed a thread blocked inside `QdrantClient.__init__` →
  `threading.Thread(...).start()`. Two explanations are both plausible and neither was chased
  further here (out of this investigation's scope — Finding 4's underlying hang is already fixed
  and closed): a `qdrant-client` version difference between that session and this one, or that
  thread only being spawned on a different code path (e.g. gRPC-preferring construction) not
  exercised by this server's plain REST usage. Recorded honestly as a discrepancy, not smoothed
  over, since it is directly relevant evidence for anyone investigating this further.
- **Whether the embedder-service self-terminating idle-timeout pattern
  (`_shared/embedder_client.py`) is reusable here: no, judged architecturally inapplicable, not
  merely "not yet built."** That pattern exists because `embedder-service` is a decoupled,
  cross-process, multi-consumer singleton, deliberately detached (`DETACHED_PROCESS` /
  `start_new_session`) so it can outlive any one spawning MCP server and be discovered/reused by a
  later process via its lock/PID files. `agent-memory` is not that — it is the primary MCP server
  the host itself spawns and owns 1:1 per connection; its expected lifecycle is "live exactly as
  long as this MCP connection is open," managed by the host, not by a self-owned idle timer.
  Applying a self-terminate-when-idle pattern to it would actively fight the host's own lifecycle
  management: a legitimately idle-but-still-connected server could self-terminate mid-session, the
  host would then have to notice the connection died and respawn — net effect more process churn,
  not less, plus a real risk of racing an in-flight tool call. This is a reasoned rejection of the
  proposed pattern for this specific case, not evidence about the duplication's actual cause.

What could not be checked from this session: an actual live `/mcp reconnect agent-memory` cycle,
and a process-list snapshot (`Get-CimInstance Win32_Process`) before/after one, to directly observe
whether a prior subprocess's PID survives a reconnect. A background/subagent build context has no
mechanism to issue an MCP client reconnect — that capability belongs to the interactive session
that owns the MCP client connection.

**Concrete remediation/diagnosis plan for a future session with live reconnect access:**

1. Snapshot `Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'agent-memory' }`
   before a deliberate `/mcp reconnect agent-memory`, reconnect 2–3 times in a row, snapshot again
   after each. Direct evidence of whether old PIDs survive is the prerequisite for any further
   step — do not skip straight to a fix.
2. If old PIDs do survive: check whether their stdin pipe is actually closed by the host (e.g. via
   `py-spy dump` on the stale PID — is it blocked inside `stdin_reader()`'s `async for line in
stdin`, i.e. genuinely still waiting for input that will never arrive?). If so, this is squarely
   an MCP-host (Claude Code CLI) subprocess-lifecycle question, not fixable inside
   `agent-memory/server.py` — the fix would need to happen in the host's reconnect logic, outside
   this workspace's code entirely.
3. If stdin is closed but the process still doesn't exit, that would contradict the static-analysis
   findings above and warrants the same `py-spy` + bounded multi-launch rigor
   `2026-07-13-mcp-embedder-service-redesign` and `2026-07-17-agent-memory-client-instability`
   both already established as this Programme's standard for this class of problem — not a guess.
4. Only after step 2 or 3 produces direct evidence of an agent-memory-owned cause should a code fix
   be attempted here. Absent that evidence, this remains correctly out of `agent-memory`'s own
   scope.

### 4. Test suite (previously undocumented gap, now closed)

`.claude/rules/mcp-governance.md` and `09-mcp-architecture-decision.md` both cited a committed
`mcp-servers/agent-memory/tests/` suite ("22 passed", "17 original + 5 new"). No such directory
existed in the working tree or anywhere in git history (`git log --follow` / `git log
--diff-filter=D` both empty).

**Root cause found, not just worked around:** `agent-memory/.gitignore` contained a bare `tests/`
line ("Local evaluation harness — test scripts and generated outputs stay local"). That is not
merely "the tests were forgotten" — a bare `dir/` gitignore pattern excludes the directory itself
from Git's tree-walk, so `!tests/<file>` negation exceptions placed after it **cannot** re-include
anything inside (Git never recurses into an already-excluded directory to evaluate per-file
negations). Any test suite ever written in `agent-memory/tests/` was structurally uncommittable
under that pattern, regardless of intent. The sibling server, `workspace-knowledge/.gitignore`,
already encodes the correct form of this same policy: `tests/*` (not bare `tests/`) followed by
explicit `!tests/<file>` exceptions — which is exactly how that server's one permanent regression
test (`test_upsert_delete_ordering_fix.py`) is committed today. `agent-memory/.gitignore` has been
corrected to the same `tests/*` + explicit-exception form, with this build's four files
(`conftest.py`, `test_server.py`, `health_comparison.py`,
`test_cross_server_health_comparison.py`) added as the exceptions — so this suite does not
silently repeat the exact same disappearance the next time someone runs `git status` and sees a
clean tree.

This build creates a real, committed suite:

- `agent-memory/tests/conftest.py` — imports `agent-memory/server.py` and
  `workspace-knowledge/server.py` via `importlib` under distinct module names (both files are
  literally named `server.py`, so a bare `import server` for both in one process would collide);
  sets `EMBEDDER_SERVICE_ENABLED=false` before import so no unit test attempts to reach the live
  embedder-service; provides `reset_embedder_globals`, a fixture that snapshots/restores every
  embedder-state module global so tests exercising specific state combinations never leak into
  later tests.
- `agent-memory/tests/test_server.py` — 35 tests covering `_search_memory_impl` (unknown type,
  episodic session-scoping, top_k clamping both directions, status-filter defaults and
  opt-ins, reflection routing, client-none degradation), `_search_reflection` (empty-on-no-client,
  payload parsing, status filter construction, timeout degradation, malformed-payload degradation,
  connection-error degradation), `_get_embedder`/`_get_embedder_unavailable_reason` (service-ready
  precedence, service-call-failure fallback, lazy-trigger-without-blocking, idempotent trigger,
  all four unavailable-reason message shapes), `_get_search_capability_snapshot` (all four
  `effective_path` outcomes, the disabled-vs-unavailable distinction, the never-triggers-warmup
  guarantee, graceful degradation on an internal error), and the `health_check`/`search_memory`
  tool wrappers' never-raises contract.
- `agent-memory/tests/health_comparison.py` + `test_cross_server_health_comparison.py` — see
  above.

**43 passed, 0 failed** (`pytest agent-memory/tests/ -v`, from the shared
`mcp-servers/.venv/Scripts/python.exe`). Live-Qdrant-dependent test included and actually ran
(not skipped) in this environment.

**Regression check:** `pytest engineering/context-engineering/testing/ -v` (from
`core-component-00/`) — **283 passed, 1 pre-existing failure**
(`test_acon_benchmark.py::test_acon_vs_context_compressor`), which is out of scope for this build
and unrelated to anything touched here (confirmed unchanged before/after — the failure is in
`ContextCompressor` vs. `acon_compress` token-reduction comparison logic, nothing this build
touched).

---

## Verification Performed vs. Not Performed

**Performed, this session:**

- `python -m py_compile` on both modified files (`agent-memory/server.py`,
  `workspace-knowledge/server.py`) — compiles clean.
- Full `agent-memory/tests/` suite run against the shared venv — 43/43 passed, including the live
  cross-server comparison test (qdrant-memory was reachable; the test exercised its real live
  path, not its skip path).
- Full `context-engineering/testing/` regression suite run — 283 passed, 1 known-unrelated
  pre-existing failure, confirmed no new breakage.
- Direct empirical thread-enumeration test of `QdrantClient` construction and first call against
  live `qdrant-memory`.

**Not performed — explicitly flagged as pending, not silently skipped:**

- **Live MCP-reconnect verification of the `search_capability` block or the
  `_memory_instance_health_block_impl` refactor through an actual `mcp__agent-memory__health_check`
  / `mcp__workspace-knowledge__health_check` tool call over a live MCP connection.** This build ran
  in a background/subagent git-worktree context, which has no mechanism to issue an MCP client
  reconnect — only the interactive session that owns the MCP client connection can do that. Per
  this Programme's own established discipline (`2026-07-17-agent-memory-client-instability/
research-report.md`'s explicit distinction between "implemented" and "independently
  live-verified by Dr. Vance"), this gap is recorded here plainly rather than blurred: **code-level
  verification (compile + full test suite, including one test that does exercise live Qdrant) is
  complete; live-MCP-protocol verification of the new `health_check` output shape is pending human
  verification** via an actual reconnect in an interactive session.
- The stale-duplicate-process investigation's step 1 (process-list snapshot across a real
  reconnect) — see Section 3 above; requires the same live-reconnect capability this build does
  not have.

---

## Files Changed

- `core-component-00/mcp-servers/agent-memory/server.py` — added
  `_get_search_capability_snapshot()`; `health_check()` now returns `search_capability` alongside
  `memory_instance` (both the success and exception-fallback branches).
- `core-component-00/mcp-servers/workspace-knowledge/server.py` — extracted
  `_memory_instance_health_block_impl(client)` from `_memory_instance_health_block()`; the latter
  is now a thin wrapper. No other change.
- `core-component-00/mcp-servers/agent-memory/tests/` — new directory: `conftest.py`,
  `test_server.py`, `health_comparison.py`, `test_cross_server_health_comparison.py`.
- `core-component-00/mcp-servers/agent-memory/.gitignore` — fixed the bare `tests/` pattern that
  made every prior test file in that directory structurally uncommittable (see "Test suite"
  above); now mirrors `workspace-knowledge/.gitignore`'s proven `tests/*` +
  explicit-`!`-exceptions form.
- `.claude/rules/mcp-governance.md` — dated append to the `agent-memory` row (see that file).
- This document.

---

## References

### Internal Documentation

- `core-component-00/telescope/2026-07-17-agent-memory-client-instability/research-report.md` —
  Findings 3–5 (the incident this fix prevents a recurrence of), Recommendations item 2 (the
  comparison test built here)
- `core-component-00/telescope/2026-07-10-agent-memory-architecture/supporting/09-mcp-architecture-decision.md`
  — Decision 2 constraints (read-only-first, no caller-supplied sacred/importance override,
  graceful degradation everywhere) — not weakened anywhere in this build
- `.claude/rules/mcp-governance.md` — `agent-memory` row, full incident history
- `core-component-00/mcp-servers/_shared/embedder_client.py` — the self-terminating
  idle-timeout pattern evaluated (and judged inapplicable) in Section 3

### Related Work

- Commit `f655c21e` — the same-day P1 fix (embedder-service readiness retry) that exposed this
  observability gap

---

## Addendum — Stale-Process Diagnosis, Steps 1–2 (Live Verification, 2026-08-07)

**Authorized by:** CEO, via Dr. Elias Vance (Lab Director) — Phase 5, item 1 (stale-process
diagnosis)
**Executed by:** Dr. Elias Vance, directly, in a live interactive session (the capability Section
3 above identified as missing from any prior subagent/worktree build — a real MCP client
connection able to issue `/mcp reconnect`)

This addendum closes steps 1 and 2 of the diagnosis plan in Section 3 above with direct,
first-hand evidence gathered in this environment. One reconnect cycle was run (not the 2–3 the
plan suggested) — sufficient to answer the mechanism question conclusively via `py-spy`, though
not exhaustive on multi-reconnect accumulation rate. A second/third cycle remains available as a
future confirmatory step if ever wanted, but is not required to act on this finding.

**Step 1 — process-list snapshot before/after a real reconnect:**

|              | Before reconnect                                               | After reconnect                                                               |
| ------------ | -------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| PIDs present | 30780, 21612, 44176, 38708 (all created `2026-08-07 02:27:19`) | 44176, 38708 (survived) + 25508, 35800 (new, created `02:41:17`)              |
| Outcome      | —                                                              | 2 of 4 old PIDs survived the reconnect; 2 were cleaned up; 2 new ones spawned |

**Direct evidence: old PIDs partially survive a reconnect.** This alone confirms the plan's step-1
prerequisite question (do stale PIDs survive?) — yes, non-deterministically, and reconnects net
_add_ processes rather than cleanly swapping them.

**Step 2 — is a surviving stale PID genuinely blocked waiting on stdin?**

`py-spy dump --pid 38708` (one of the two survivors) succeeded and returned:

```
Thread 11096 (idle): "MainThread"
    _poll (asyncio\windows_events.py:775)
    select (asyncio\windows_events.py:446)
    _run_once (asyncio\base_events.py:2004)
    run_forever (asyncio\base_events.py:683)
    run_until_complete (asyncio\base_events.py:712)
    run (asyncio\runners.py:118)
    run (anyio\_backends\_asyncio.py:2481)
    run (anyio\_core\_eventloop.py:83)
    run (fastmcp\server\mixins\transport.py:124)
    <module> (server.py:658)
```

(`py-spy dump --pid 44176` failed with `Failed to find python version from target process` — a
py-spy/CPython 3.13 read quirk on that specific PID, not evidence of anything; 38708 is the same
server binary and gave a clean read, which is sufficient to answer the question.)

The main thread is idle inside the asyncio event loop's I/O poll (`select`/`_poll` on Windows'
`ProactorEventLoop`) — the exact mechanism underneath the stdio transport's `async for line in
stdin` read (see Section 3's third bullet above). It is not crashed, not spinning, not doing any
work: it is genuinely still waiting for input the host never sent after reconnecting.

**Conclusion.** Per the plan's own decision criteria (Section 3, steps 2–4): stdin is not being
closed by the host on reconnect, which places this squarely as an **MCP-host (Claude Code CLI)
subprocess-lifecycle question, not an `agent-memory`-owned defect.** Step 4's precondition for
attempting a code fix here ("only after step 2 or 3 produces direct evidence of an
agent-memory-owned cause") is not met — the evidence points the opposite direction. The
2026-08-06 static-analysis hypothesis is upgraded from _reasoned-but-unobserved_ to **directly
confirmed**. No further diagnostic work or code change against `agent-memory`/`server.py` is
warranted from this finding; a fix, if pursued, would need to target the host's own reconnect
logic, which is outside this workspace's code.

No files under `core-component-00/mcp-servers/` were modified as part of this addendum —
diagnosis only, per Phase 5 scope.

---

## Version History

| Version | Date       | Author                               | Changes                                                                                    |
| ------- | ---------- | ------------------------------------ | ------------------------------------------------------------------------------------------ |
| 1.0     | 2026-08-06 | Worker A (agent/observability build) | Initial report                                                                             |
| 1.1     | 2026-08-07 | Dr. Elias Vance (live session)       | Addendum: stale-process diagnosis steps 1–2 confirmed via live `/mcp reconnect` + `py-spy` |

---

**Template Version:** 1.0
**Last Updated:** 2026-08-07
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
