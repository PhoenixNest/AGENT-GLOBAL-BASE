# Research Report — agent-memory Live Client Instability (Post-Outage Follow-Up)

---

## Metadata

| Field                | Value                                                                                                                                          |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Investigation ID** | `2026-07-17-agent-memory-client-instability`                                                                                                   |
| **Date Started**     | 2026-07-17                                                                                                                                     |
| **Date Completed**   | 2026-07-17                                                                                                                                     |
| **Status**           | Complete — root-caused, fixed, and independently live-verified by Dr. Vance; both `agent-memory` MCP tools are reliable again as of 2026-07-17 |
| **Investigator**     | Dr. Elias Vance, Laboratory Director                                                                                                           |
| **Laboratory**       | Core Component 00                                                                                                                              |
| **Module(s)**        | MCP server infrastructure (`agent-memory`, `workspace-knowledge`, `_shared/embedder-service`)                                                  |
| **Priority**         | Resolved — was High; fix implemented by Mei-Ling Zhao, independently live-verified by Dr. Vance (Finding 5)                                    |
| **Requestor**        | CEO                                                                                                                                            |

---

## Executive Summary

> A CEO-requested review of the agent-memory system on 2026-07-17 found and fixed a P0 outage:
> both `agent-memory` and `workspace-knowledge` MCP servers were crash-looping at import time due
> to three stale relative paths left over from the 2026-07-16 `engineering/` module relocation
> (`77acde86`). The fix was verified in-process and committed (`2fc3cd2c`). Retesting the live,
> host-spawned `agent-memory` server after reconnect surfaced a second, distinct problem: its
> `health_check` tool reports `reachable: false` with all-zero point counts even though the
> `qdrant-memory` instance is confirmed healthy (verified independently via `workspace-knowledge`,
> which reads the same instance and reports correctly), and its `search_memory` tool hangs
> indefinitely in the live tool-call context. This is a new symptom, not a reproduction of the
> already-closed embedder-warmup stall from `2026-07-13-mcp-embedder-service-redesign` — it
> implicates `agent-memory`'s `_get_memory_client()` / `_call_with_hard_timeout` watchdog path
> specifically, which `workspace-knowledge` does not share. **Update:** a CEO-authorized narrow fix
> (Option A) was implemented and live-tested but did not resolve the hang; live `py-spy` evidence
> then identified the true root cause — an always-on in-process embedder-warmup thread that
> reliably wedges on a `scipy.sparse.linalg` import and permanently holds CPython's import lock,
> blocking `QdrantClient` construction process-wide (Finding 4). That fix was delegated to Mei-Ling
> Zhao (context-engineering module lead), implemented, and independently live-verified by Dr. Vance
> — both `agent-memory` tools are confirmed reliable again (Finding 5). Investigation closed.

---

## Investigation Scope

### What Was Investigated

Two related but distinct things, in sequence:

1. Whether the CC-00 memory system's MCP servers (`agent-memory`, `workspace-knowledge`) run
   correctly, following a CEO request to review and test the memory system and confirm disaster
   recovery is ready.
2. After fixing a P0 found during (1), whether the live `agent-memory` server is now fully
   reliable, or exhibits any remaining live-instability symptoms distinct from the already-closed
   embedder stall.

### Why This Investigation Was Needed

The CEO asked for a live health/readiness check of the memory system, not a documentation review.
Direct testing (not just reading `mcp-governance.md`'s status table) surfaced a full outage that
the existing documentation did not describe, and — after fixing it — a second live symptom that
does not match any previously-documented failure mode. Both needed a paper trail distinct from the
chat transcript that produced them, per this workspace's telescope conventions.

### Out of Scope

- Root-causing the new client-instability symptom itself was originally out of scope for the
  session that first observed it — flagged as follow-up work at the time, consistent with
  `2026-07-13-mcp-embedder-service-redesign`'s own precedent of running a bounded, evidence-based
  investigation rather than guessing at a fix live. **This was later brought back in scope in the
  same investigation and completed — see Findings 4 and 5.**
- The embedder-warmup stall itself — already investigated and closed in
  `2026-07-13-mcp-embedder-service-redesign`; not reopened here.
- `workspace-knowledge`'s internals beyond confirming it does not reproduce this symptom.

---

## Research Questions

1. Was the memory system actually running correctly before this review? (No — see Finding 1.)
2. Is the disaster-recovery path (`QdrantMemoryIndex.rebuild_from_log()`) genuinely functional
   against live infrastructure, not just unit-tested? (Yes — see Finding 2.)
3. After fixing the P0 outage, is `agent-memory`'s live MCP tool surface now fully reliable?
   (Not initially — see Finding 3. Yes, as of Finding 5, after the Finding 4 fix was implemented
   and independently live-verified.)
4. Does the new instability reproduce in `workspace-knowledge`, which reads the same Qdrant
   instance? (No — see Finding 3, which is the key evidence this is `agent-memory`-specific.)

---

## Methodology

### Approach

1. Read `.mcp.json`, `agent-memory/README.md`, and `agent-memory/server.py` to establish the
   documented-correct configuration.
2. Attempted to reach the live `agent-memory`/`workspace-knowledge` MCP tools via `ToolSearch` —
   neither was reachable, which was the first sign something was wrong beyond documentation drift.
3. Directly executed both `server.py` files via `python <path>` to capture real startup
   tracebacks, rather than guessing from static analysis.
4. Fixed the identified path bug, then re-verified via in-process module import and live tool
   calls (`health_check`, `search_memory` happy-path and guard-path cases).
5. Built and ran a standalone disaster-recovery acceptance test against a disposable Qdrant
   collection (never touching production `memory_*` collections), mirroring the rigor described
   in `mcp-governance.md`'s "Disaster-recovery layer acceptance-tested 2026-07-13" entry.
6. After the user reconnected the `agent-memory` MCP server, re-ran `health_check` and
   `search_memory` live and compared against `workspace-knowledge`'s simultaneous view of the same
   underlying Qdrant instance.

### Tools and Resources

- Direct `python <server.py>` execution to capture real import-time tracebacks
- `docker ps` / Qdrant REST API (`/collections`) to independently verify container health,
  decoupled from either MCP server's own self-report
- A disposable-collection Qdrant acceptance script (temp JSONL log → `rebuild_from_log()` →
  search → idempotency re-run → cleanup), not committed to the repo
- Live MCP tool calls (`mcp__agent-memory__health_check`, `mcp__agent-memory__search_memory`,
  `mcp__workspace-knowledge__health_check`) via the active session

### Constraints

- The live client-instability symptom (Finding 3) was initially observed but not instrumented with
  `py-spy` or a controlled multi-launch protocol, unlike the rigor `2026-07-13-mcp-embedder-
service-redesign` applied to the embedder stall. **That instrumentation was performed later in
  this same investigation — see Finding 4.**
- Two live `search_memory`/`health_check` calls were left running as background tasks; one
  (`kumzqb3vu`) was confirmed to fail after a 1800s idle timeout. A second (`k0f0qql23`) was still
  running when this constraint was first written — its outcome was not recorded at that point to
  avoid reporting a fabricated result. **It has since resolved — see Open Question 3.**

---

## Findings

### Finding 1: Both registered MCP servers were fully down (P0)

Neither `agent-memory` nor `workspace-knowledge` could start. Both crashed at import time with
`ModuleNotFoundError: No module named 'implementations'`, before FastMCP could register any tool —
so neither server's tools were reachable at all, in any session, since the 2026-07-16 relocation
commit (`77acde86`) that moved `context-engineering`/`harness-engineering`/etc. under
`core-component-00/engineering/`.

**Evidence:**

- `python core-component-00/mcp-servers/agent-memory/server.py` → traceback at line 32
  (`from implementations.memory_vector_store import ...`).
- `python core-component-00/mcp-servers/workspace-knowledge/server.py` → identical traceback.
- Root cause: three hardcoded `Path(__file__).resolve().parents[2] / "context-engineering"` (and
  one `.../"harness-engineering"`) references, in `agent-memory/server.py`,
  `workspace-knowledge/server.py`, and `_shared/embedder_client.py`, all still pointing at the
  pre-relocation location (`core-component-00/context-engineering`, confirmed not to exist via
  `Test-Path`).

**Implications:**

- This was a silent, total outage — no error surfaced to any prior session short of trying to
  actually invoke the tools or run the server directly, which is presumably why it went unnoticed
  since 2026-07-16.

**Fix:** inserted the missing `engineering/` path segment in all three files. Verified via
in-process import (no longer raises) and live tool calls post-fix. Committed as `2fc3cd2c`.

---

### Finding 2: Disaster recovery is genuinely functional, not just documented as such

`QdrantMemoryIndex.rebuild_from_log()` was exercised live against a disposable Qdrant collection
(`dr_acceptance_test_disposable`, deleted after the test): 3 synthetic records written to a temp
JSONL log, replayed into Qdrant, confirmed searchable, confirmed idempotent on a second rebuild
(no duplication), collection cleaned up afterward. Production `memory_*` collections' point counts
were confirmed unchanged before/after.

**Evidence:**

- `rebuild_from_log()` returned `3` on first run, post-rebuild search returned 3 matching results,
  second rebuild also returned `3` with no increase in `count_points()`.

**Implications:**

- The CEO's disaster-recovery readiness question can be answered "yes, confirmed live" rather than
  "yes, per prior documentation" — a stronger claim than what existed before this session.

---

### Finding 3: `agent-memory`'s live MCP tools are unreliable even after the Finding 1 fix

After the user reconnected `agent-memory` post-fix, `health_check` reproducibly returned
`{"reachable": false, "point_counts": {all zero}}` on every call — while `workspace-knowledge`,
queried in the same breath, correctly reported `reachable: true` with the real point counts
(`memory_reflection: 4`) for the _same_ `qdrant-memory` instance. A subsequent `search_memory`
call hung and was moved to a background task, mirroring an earlier `health_check` call that had
hung for the full 1800s idle timeout before this reconnect.

**Evidence:**

- Three consecutive live `mcp__agent-memory__health_check` calls: first hung 1800s and failed
  (task `kumzqb3vu`); after `/mcp reconnect agent-memory`, next two returned promptly but with
  `reachable: false` / all-zero counts, both times.
- Simultaneous `mcp__workspace-knowledge__health_check` calls in the same turns: `reachable: true`,
  correct counts, both times.
- Docker/Qdrant REST checks (`docker ps`, `GET /collections`) independently confirm
  `qdrant-memory` itself is healthy throughout — ruling out the container as the cause.
- A subsequent `mcp__agent-memory__search_memory` call also hung, moved to background task
  `k0f0qql23`.

**Implications:**

- This is not the same failure as the embedder-warmup stall documented in
  `2026-07-13-mcp-embedder-service-redesign` (that stall was about the _embedding model import_
  hanging; this is about `_get_memory_client()`'s `QdrantClient` construction / the
  `_call_with_hard_timeout` watchdog itself misbehaving specifically inside the live, host-spawned
  FastMCP async tool-call context — a context this session's direct-script testing in Finding 1/2
  did not exercise, since those ran synchronously outside FastMCP).
- `workspace-knowledge` does not share this failure mode: it builds its Qdrant client without the
  hard-timeout watchdog wrapper agent-memory uses, and has been reliable throughout this session.
  That asymmetry is itself a clue for the follow-up investigation.
- Net effect: the P0 crash-loop is fixed and confirmed, but `agent-memory`'s live tool surface
  cannot currently be trusted to return correct `health_check`/`search_memory` results on demand —
  a Completeness-gate-relevant gap per `.claude/rules/mcp-governance.md`, distinct from and
  additional to the already-tracked embedder-warmup gap.

---

### Finding 4: Option A was implemented, live-tested, and did not resolve Finding 3 — but `py-spy` identified the actual root cause

Per CEO authorization (2026-07-17), Option A was implemented exactly as scoped: `_get_memory_client()`
in `agent-memory/server.py` now constructs a single `QdrantClient` once per process, cached in a
module-level variable behind a lock, with a plain `timeout=5` and no `_call_with_hard_timeout`
watchdog wrapper — matching `workspace-knowledge`'s proven pattern verbatim. The server was
reconnected so the change would take effect (FastMCP subprocesses do not hot-reload on file edits).

`health_check` was called live immediately after reconnect. It hung again, moved to a background
task after 120s, behaviorally identical to the pre-Option-A symptom. Rather than let it run to the
full 1800s timeout a third time, the live server process (confirmed via `Get-CimInstance
Win32_Process`, PID resolved by cross-referencing its freshly-spawned `embedder-service` child
process) was inspected directly with `py-spy dump`, twice, 8 seconds apart.

**Evidence — both `py-spy` dumps are frame-for-frame identical**, confirming a true deadlock, not
a slow-but-progressing call:

- Thread `"qdrant-call-watchdog"` (actually the in-process embedder-warmup thread, `_load_embedder_
background` → `_import_and_build_embedder`, `server.py:108`) is frozen mid-import at
  `scipy\sparse\linalg\_eigen\arpack\arpack.py:49`. This reproduces, precisely, the unresolved
  symptom `mcp-governance.md`'s `agent-memory` row already documents from 2026-07-13 ("reproducibly
  stuck importing `scipy.sparse.linalg._svdp` on some fresh server processes, never completing") —
  same failure family, a neighboring file in the same `scipy.sparse.linalg` submodule tree, four
  days later, independently reproduced.
- A second thread, the warmup's own retry (`_EMBEDDER_LOAD_MAX_ATTEMPTS = 2`), is frozen at
  `_lock_unlock_module`, waiting to acquire the same import lock — proof the first thread never
  releases it.
- The thread actually executing the live `health_check` tool call is frozen inside
  `_get_memory_client()` → `QdrantClient.__init__` (`qdrant_client\qdrant_remote.py:264`) →
  `threading.Thread(...).start()` → `self._started.wait()` (`threading.py:981/659/359`) — i.e.
  waiting for a new OS thread that `qdrant-client`'s own constructor spawns internally to finish
  bootstrapping. On CPython, a new thread's bootstrap can itself require the import lock; with that
  lock held indefinitely by the stuck warmup thread, the new thread can never signal `_started`, so
  `Thread.start()` never returns.

**Implications:**

- **This is why Option A could not have worked, and the finding is not a failure of that
  recommendation's reasoning — it correctly identified and eliminated one real difference between
  `agent-memory` and `workspace-knowledge` (the watchdog wrapper), but the actual blocking
  mechanism is one level upstream of both: `agent-memory/server.py` unconditionally starts an
  in-process embedder-warmup fallback thread at module-import time (line 150), regardless of
  whether the already-fixed, already-running `embedder-service` (2026-07-13/14) makes it
  redundant. That thread reliably wedges on the same `scipy` import that stalled in the original
  2026-07-13 investigation, and — because it never releases CPython's import lock — it eventually
  blocks _any_ other thread in the process that needs to start a new native thread, which includes
  `qdrant-client`'s own constructor. `workspace-knowledge/server.py` has no equivalent always-on
  in-process fallback thread, which is the real reason it has been reliable throughout this
  investigation, not the absence of a watchdog per se.**
- This resolves Open Questions 1 and 2 below with direct evidence rather than inference.
- Option A (client caching, dropping the watchdog) remains implemented and is not being reverted —
  it is a correct simplification that matches the proven-reliable pattern and removes one moving
  part — but it is confirmed insufficient alone. A second, narrowly-scoped fix is required and is
  proposed in Recommendations below. **That fix has not been implemented — it is outside the
  Option A scope the CEO explicitly authorized, and per standing instruction no implementation
  proceeds without a separate sign-off.**

---

### Finding 5: The Finding 4 fix was implemented, delegated, and independently live-verified — resolved

Per Dr. Vance's direction, implementation of the Finding 4 fix was delegated to Mei-Ling Zhao
(Senior Research Engineer, `context-engineering` module lead, per `core-component-00/crew/CLAUDE.md`'s
Authority Scope — this fix sits inside her module's ownership), rather than performed directly by
the Director, consistent with the Lab's normal division between architectural direction and
module-level implementation.

**What was implemented** (`agent-memory/server.py`): the in-process embedder-warmup thread no
longer starts unconditionally at module-import time. A new guarded function,
`_ensure_embedder_load_started()`, starts it exactly once, lazily, only from inside `_get_embedder()`
and only when the persistent `embedder-service` is not ready. The loading mechanism itself
(`_load_embedder_background`, `_import_and_build_embedder`, the `_call_with_hard_timeout`-guarded
retry) is untouched — only the trigger changed. `_embedder_state`'s default changed from
`"loading"` to `"not started"` so the degraded-reason message never claims a warmup is in progress
before one has actually been triggered. Option A (the cached `QdrantClient`, implemented earlier
today) was left untouched, as instructed.

**Independent verification performed by Dr. Vance** (not accepted on the engineer's report alone,
per standing instruction):

1. Read the actual diff in `agent-memory/server.py` directly and confirmed it matches what was
   reported — no eager thread start remains at module level, the lazy trigger is reachable only
   from `_get_embedder()`, and `_get_embedder_unavailable_reason()` covers all four states.
2. Independently ran `python -m py_compile` — compiles clean.
3. After the user reconnected `agent-memory` (required for the FastMCP subprocess to pick up the
   change), called `health_check` live: `reachable: true`, correct point counts
   (`memory_reflection: 4`, matching `workspace-knowledge`'s independent report earlier this
   session), returned instantly — no hang.
4. Called `search_memory` live (`memory_type="reflection"`, real query): returned 3 real,
   correctly-shaped results instantly, `degraded: false` — not a hang, not an empty
   silently-degraded response.
5. Took a `py-spy dump` of the freshly-reconnected live process. Only three threads exist: the
   FastMCP/asyncio main thread and two idle AnyIO worker threads — **no embedder-warmup thread is
   present at all**, confirming the lazy trigger correctly never fired (the `embedder-service` was
   already ready, so `_get_embedder()` never needed the in-process fallback). No import-lock
   contention, no wedged thread — a clean process, in direct contrast to the two identical stuck
   dumps captured before this fix (Finding 4).

**Implications:**

- This closes the investigation. Both of `agent-memory`'s live MCP tools are confirmed reliable
  again, verified against the actual live process rather than inferred from the fix's design.
- The delegation-and-independent-verification structure worked as intended: the assigned
  engineer's own report was treated as a claim to check, not a result to relay — and the check
  surfaced no discrepancy, but was performed regardless.
- The underlying `scipy.sparse.linalg` import stall itself (first observed 2026-07-13, still not
  root-caused as to _why_ it wedges on this environment) is no longer on any live-blocking code
  path, since the in-process embedder fallback it lives inside now only ever runs if the
  `embedder-service` is down. That narrower open question is downgraded from a live-reliability risk
  to a lower-urgency curiosity, tracked in Open Questions below rather than left conflated with the
  (now closed) live-hang risk.

---

## Analysis

### Interpretation of Findings

The 2026-07-17 review surfaced two failure classes at different layers of the same system: a
straightforward, fully-fixable configuration bug (Finding 1, closed) sitting on top of an
environment-specific reliability gap in how `agent-memory` talks to Qdrant when actually running
inside the MCP host's process-management model (Finding 3, closed by Findings 4 and 5). Fixing
Finding 1 was necessary to even observe Finding 3 — the server could not previously get far enough
to exhibit it. This mirrors the shape of the 2026-07-13 investigation, where an underlying
Qdrant-hang fix (also already resolved, per `mcp-governance.md`) was itself a precondition for
discovering the deeper embedder-loading stall.

At the time this section was first written, the working hypothesis was that `agent-memory`'s
`_call_with_hard_timeout`-guarded call sites in general might behave differently under live
FastMCP host-spawn conditions than under direct script execution, warranting systematic review.
Finding 4's `py-spy` evidence superseded that hypothesis with a more precise one: the actual cause
was not the watchdog mechanism misbehaving under FastMCP, but a specific always-on background
thread (the in-process embedder-warmup fallback) wedging on an unrelated import and blocking
`QdrantClient` construction process-wide. The broader "review every watchdog-guarded call site"
recommendation is superseded by the narrower, evidence-backed fix in Finding 4/5; it is not being
carried forward as a separate action item.

### Risks and Limitations

- At the point this section was first written, the report documented only _evidence of_ a live
  instability, not its root cause, and treating it as "understood" would have been premature —
  exactly the mistake the 2026-07-13 investigation's Round 1 cautions against (accepting a
  plausible-sounding explanation without direct evidence). That caution was upheld rather than
  overridden: the root cause was subsequently established with direct `py-spy` evidence (Finding
  4), not inferred, before the fix was implemented and independently live-verified (Finding 5).
- The two hung background tasks (`kumzqb3vu`, `k0f0qql23`) consumed real session time (up to 1800s
  each) without resolving — any follow-up investigation should use bounded, killable reproduction
  attempts from the start, per the existing `2026-07-13` methodology's own lesson.

---

## Architectural Assessment — Does the MCP System Need a Redesign?

**Commissioned 2026-07-17: the CEO assigned the Lab Director full ownership of this question,
explicitly asking it be examined from the perspective of the overall architecture, not just this
one symptom. This section is that assessment as originally produced, before any fix was
implemented — kept intact as the historical record of the reasoning at the time. Outcome: Option A
was implemented and found insufficient (Finding 4); the fix that Finding 4's direct evidence
actually pointed to was then implemented and independently live-verified (Finding 5). Option B was
never triggered — its pre-committed escalation criterion did not fire.**

### Current architecture, as it actually stands today

Two independent failure-mitigation patterns coexist in this codebase, applied at different times
to different call sites, and Finding 3 exists in the gap between them.

**1. The embedder-loading path (fixed 2026-07-13/14):** `agent-memory` and `workspace-knowledge`
both now call a persistent, independently-lifecycled local HTTP service
(`_shared/embedder-service/server.py`, `127.0.0.1:8791`) instead of importing
`sentence_transformers` inside the host-spawned MCP process. The service loads its models once,
outside the MCP host's spawn/churn lifecycle, and both servers talk to it via `embedder_client.py`
with an automatic in-process fallback if the service is unavailable. This directly and effectively
removed the original embedder-import stall from the host-spawned process's critical path. It is
running right now (confirmed via its `run/*.pid`/`*.lock` files) and was not touched by today's
investigation.

**2. The Qdrant-connectivity path (never migrated):** `agent-memory`'s `_get_memory_client()`
still constructs a fresh `QdrantClient` inside the host-spawned process, on every single tool
call, wrapped in `_call_with_hard_timeout` — a disposable-daemon-thread watchdog defined in
`memory_vector_store.py`. No caching, no reuse, no persistent out-of-process broker. This is
architecturally identical in shape to the embedder problem the 2026-07-13 redesign already
solved — heavy/fragile work happening inside a process the MCP host spawns and churns — but it
was never brought under the same fix, because the 2026-07-13 investigation was explicitly scoped
to the embedder import only (see that report's Out of Scope: "The Qdrant network-call hang and its
fix (hard-timeout watchdog) — already resolved... not revisited here"). That prior fix addressed
slow Qdrant calls; it did not anticipate the watchdog mechanism itself misbehaving in the live
host-spawned context, which is what Finding 3 now shows.

### The key comparative evidence

`workspace-knowledge`'s own `health_check` computes its `memory_instance` block by building a
`QdrantClient` directly, with no watchdog wrapper at all (`client = QdrantClient(url=...,
timeout=5)`, a plain try/except). In every test this session, `workspace-knowledge` reported
correctly; `agent-memory`, hitting the same `qdrant-memory` instance but through the
watchdog-wrapped path, hung unconditionally both times it was tried live (`health_check` and
`search_memory`, both to the full 1800s timeout). The simpler, unguarded code path is the one that
works. That is a specific, falsifiable lead, not a restatement of "MCP host-spawn is flaky" — and
it points at the watchdog-thread mechanism itself as the more likely proximate cause, not the
Qdrant network call it was built to guard.

### Redesign options considered

| Option                                                                                                                                                                                                        | Scope                                                                                                         | Effort             | Confidence it fixes Finding 3                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| A — Narrow fix: cache a single `QdrantClient` per process and drop the custom watchdog thread, using the plain `timeout=` parameter `workspace-knowledge` already uses successfully                           | `agent-memory/server.py` only                                                                                 | Low (0.5-1 day)    | Medium-high — targets the one variable that differs between the working and failing code paths                                          |
| B — Extend the proven pattern: generalize `embedder-service` (or add a sibling service) so Qdrant connectivity, not just embedding, is brokered through a persistent local process for every CC-00 MCP server | `_shared/`, both MCP servers, new service, phased rollout mirroring the 2026-07-13 report's 6-phase structure | Medium-high (days) | High — structurally removes the entire host-spawn hazard class                                                                          |
| C — Full MCP layer redesign: every MCP server becomes a thin stdio relay over a persistent backend-services layer; no server does heavy or fragile work in-process                                            | Workspace-wide MCP architecture                                                                               | High (multi-week)  | Unproven — no evidence the whole in-process model is unsound; `workspace-knowledge`'s reliability this session is a live counterexample |

### Recommendation

**Option A first, with Option B as the pre-committed escalation path if A doesn't hold up under
the same instrumented reproduction rigor the embedder stall received — not Option C.** This
mirrors the epistemic discipline the CEO's own 2026-07-13 investigation already established for
this exact subsystem ("recommends a cheap, untested, same-day experiment be run first before
committing to that larger redesign"): the comparative evidence points at a specific, cheap,
falsifiable candidate fix (the watchdog thread, not general host-spawn flakiness or the in-process
MCP model itself), and it should be tried and instrumented before committing to Option B's larger
build. Option C is not justified by current evidence.

**If Option A is tried and does not resolve Finding 3** (the hang persists even with a cached
client and no watchdog), that result itself would be strong evidence for Option B, since it would
rule out the one concrete mechanism-level difference identified here between the working and
failing paths — at that point the same persistent-service pattern that already fixed the embedder
problem should be extended to Qdrant connectivity, following the 2026-07-13 report's proven
phased-rollout structure rather than inventing a new one.

**Status at the time this assessment was written: no implementation had been started on any
option**, per the CEO's explicit instruction at that point. **Since then:** Option A was
implemented and authorized live-testing showed it insufficient alone (Finding 4); the fix Finding
4 actually pointed to was implemented and independently live-verified (Finding 5); Option B's
escalation criterion never triggered; Option C was not pursued, consistent with the recommendation
below.

---

## Recommendations

### Primary Recommendation

**Implemented and closed.** Option A was implemented and found insufficient alone (Finding 4).
The follow-on fix `py-spy` evidence pointed to — stop starting `agent-memory`'s in-process
embedder-warmup fallback thread unconditionally at module-import time, and instead gate it so it
only ever runs lazily, on demand, if/when `_get_embedder()` is called and the persistent
`embedder-service` (2026-07-13/14) is confirmed unavailable — was subsequently authorized,
implemented by Mei-Ling Zhao, and independently live-verified by Dr. Vance (Finding 5). This
resolved the blocking mechanism directly: `py-spy` evidence (Finding 4) showed the old always-on
thread reliably wedging on a `scipy.sparse.linalg` import and then permanently holding CPython's
import lock, which blocked `QdrantClient`'s constructor (it spawns its own thread internally,
which needs that same lock to bootstrap). The change was scoped to `agent-memory/server.py` only.

### Secondary Recommendations

1. **Instrument `_get_memory_client()`/`_call_with_hard_timeout` with the same `py-spy` + bounded
   multi-launch protocol** the embedder-stall investigation used, rather than ad hoc live retries.
2. **Add a lightweight comparison test** that calls both servers' `health_check` back-to-back in
   CI-like conditions, so a future regression like Finding 3 surfaces automatically instead of
   requiring a manual CEO-requested review to discover.
3. **This is now closed — resolved.** Finding 3 showed `agent-memory`'s `search_memory`/
   `health_check` were not reachable at all, worse than a degraded response, not a variant of one
   (the existing degrade-never-block design was correct in principle; the gap was upstream of it,
   in why the tools weren't reachable at all). Finding 5 confirms both tools are reachable and
   correct again; they may be treated as trustworthy for production decisions as of 2026-07-17.
4. **Pre-commit the Option B escalation criterion now** (see Architectural Assessment above), so
   the decision to escalate isn't re-litigated from scratch if Option A's result comes back
   negative.

### Implementation Priority

| Recommendation                                                                    | Priority | Effort      | Impact | Status                                                                                       |
| --------------------------------------------------------------------------------- | -------- | ----------- | ------ | -------------------------------------------------------------------------------------------- |
| Option A (cached client, drop watchdog)                                           | P0       | 0.5-1 day   | Medium | Implemented — kept; insufficient alone, superseded as the sole fix by the item below         |
| Gate the in-process embedder-warmup thread to lazy/on-demand only (Finding 4 fix) | P0       | Low (hours) | High   | Implemented (Mei-Ling Zhao) and independently live-verified (Dr. Vance) — closed (Finding 5) |
| Option B (persistent Qdrant-broker service)                                       | N/A      | Days        | High   | Not needed — the Finding 4 fix resolved the issue; escalation criterion never triggered      |
| Automated cross-server health_check comparison test                               | P2       | 0.5 day     | Medium | Not started                                                                                  |

### Next Steps

1. **Done:** Option A implemented, `agent-memory` reconnected, live-retested, found insufficient;
   root cause identified via `py-spy` (Finding 4).
2. **Done:** the Finding 4 fix was delegated to Mei-Ling Zhao (`context-engineering` module lead),
   implemented in `agent-memory/server.py`, and independently live-verified by Dr. Vance — diff
   reviewed directly, `health_check`/`search_memory` both confirmed working live, and a follow-up
   `py-spy` dump confirmed no thread holds the import lock (Finding 5). This investigation is
   closed.
3. Cross-link this report from `2026-07-13-mcp-embedder-service-redesign`'s own follow-up tracking
   if/when that report is next touched (not edited retroactively here, per the append-only rule).
4. Not required now, but recorded for completeness: the pre-committed Option B escalation
   criterion never triggered, since the Finding 4 fix resolved the issue on the first attempt.
5. Separately (lower priority, tracked as an Open Question below, not blocking closure): the
   embedder-warmup thread's underlying `scipy.sparse.linalg` import stall is itself still not
   root-caused — only newly-reproduced. It is no longer on any live-blocking path after the
   Finding 4 fix, so it is downgraded from a reliability risk to a lower-urgency curiosity.

---

## References

### Internal Documentation

- `core-component-00/telescope/2026-07-13-mcp-embedder-service-redesign/research-report.md` —
  prior, related (but distinct) investigation into `agent-memory`'s embedder-loading stall
- `.claude/rules/mcp-governance.md` — `agent-memory` row, Registered Servers table
- `core-component-00/mcp-servers/agent-memory/README.md`
- `core-component-00/engineering/context-engineering/implementations/memory_vector_store.py`

### Related Work

- Commit `2fc3cd2c` — the Finding 1 fix (path-relocation bug)
- Commit `77acde86` — the relocation that introduced Finding 1

---

## Open Questions

1. **Why does `agent-memory`'s `_get_memory_client()` report `reachable: false` with zeroed counts
   while `workspace-knowledge` succeeds against the same Qdrant instance in the same session?**
   - Status: **Resolved by Finding 4.** Not the watchdog itself — `agent-memory`'s always-on
     in-process embedder-warmup thread wedges on a `scipy.sparse.linalg` import and permanently
     holds CPython's import lock, which blocks `QdrantClient`'s constructor (it spawns its own
     thread internally). `workspace-knowledge` has no equivalent always-on thread, hence no
     exposure. Confirmed live via two identical `py-spy` dumps 8s apart.
   - Priority: N/A — closed.
   - Assigned: N/A.

2. **Is this the same underlying host-spawn asymmetry documented in `2026-07-13`'s Round 2
   findings, or a genuinely new failure mode specific to the hard-timeout watchdog?**
   - Status: **Resolved by Finding 4.** Neither, precisely — it is a fresh manifestation of the
     _same underlying, still-unexplained_ `scipy.sparse.linalg` import stall the 2026-07-13
     investigation first observed (never itself root-caused, only mitigated by moving the primary
     embedder path out-of-process), now shown to have a second, more severe consequence this
     session: because `agent-memory/server.py` still starts that same fragile in-process import as
     an always-on fallback thread, the stall — when it occurs — now also takes down `QdrantClient`
     construction process-wide, which the 2026-07-13 investigation had no reason to anticipate
     since it only tested the embedder path in isolation. Not a host-spawn asymmetry and not
     specific to the watchdog; both were plausible leads that this evidence rules out.
   - Priority: N/A — closed.
   - Assigned: N/A.

3. **Did background task `k0f0qql23` (`search_memory`) ever resolve, and if so, how?**
   - Status: **Resolved.** It failed after the full 1800s idle timeout with no response —
     identical outcome to `health_check`'s earlier hang (`kumzqb3vu`). This confirms Finding 3 is
     not `health_check`-specific: both of `agent-memory`'s live tools hang unconditionally under
     the same conditions, which is why Priority was raised to High in the Metadata table above and
     folds directly into the Architectural Assessment below.
   - Priority: N/A — closed.
   - Assigned: N/A.

4. **Why does the `scipy.sparse.linalg` import chain reproducibly wedge on this environment in the
   first place (first observed 2026-07-13, reproduced independently 2026-07-17, root cause never
   confirmed in either investigation)?**
   - Status: Open, but downgraded. The Finding 4/5 fix removes this stall from every live-blocking
     code path (it now only runs, lazily, if the `embedder-service` is down) — so it is no longer a
     live-reliability risk. The question of _why_ the import itself wedges (Windows Defender /
     cold-disk-cache latency was the leading, never-confirmed hypothesis in 2026-07-13) remains
     genuinely unanswered.
   - Priority: P3 — lower-urgency curiosity, not blocking this report's closure.
   - Assigned: TBD, optional future work.

---

## Version History

| Version | Date       | Author                               | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------- | ---------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-07-17 | Dr. Elias Vance, Laboratory Director | Initial report filed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 1.1     | 2026-07-17 | Dr. Elias Vance, Laboratory Director | Added Architectural Assessment section (CEO-commissioned redesign-vs-narrow-fix study); resolved Open Question 3; raised Priority to High                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 1.2     | 2026-07-17 | Dr. Elias Vance, Laboratory Director | Implemented CEO-authorized Option A in `agent-memory/server.py`; live retest still hung; added Finding 4 with `py-spy`-confirmed root cause (embedder-warmup thread wedging CPython's import lock, blocking `QdrantClient`'s constructor); resolved Open Questions 1 and 2; proposed a new, narrower fix (not yet implemented, awaiting authorization)                                                                                                                                                                                                          |
| 1.3     | 2026-07-17 | Dr. Elias Vance, Laboratory Director | Delegated the Finding 4 fix to Mei-Ling Zhao (context-engineering module lead); implemented, then independently live-verified by Dr. Vance (diff review, live `health_check`/`search_memory`, follow-up `py-spy` dump showing a clean process) — added Finding 5, closed the investigation (Status: Complete), added Open Question 4 for the still-unexplained underlying import stall at lower priority                                                                                                                                                        |
| 1.4     | 2026-07-17 | Dr. Elias Vance, Laboratory Director | Reconciled internal consistency: several sections (Out of Scope, Research Questions, Constraints, Analysis, Risks and Limitations, Architectural Assessment, Recommendations) were written before Findings 4/5 existed and still read as unresolved after the investigation closed. Annotated each with its actual outcome rather than rewriting the original point-in-time reasoning, so the report reads consistently end-to-end without losing the historical record of what was known when each section was written. No findings or verified facts changed. |

---

**Template Version:** 1.0
**Last Updated:** 2026-07-17
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
