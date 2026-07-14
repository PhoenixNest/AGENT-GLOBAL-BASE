# Research Report — Persistent Embedder Service for CC-00 MCP Servers

---

## Metadata

| Field                | Value                                                                         |
| -------------------- | ----------------------------------------------------------------------------- |
| **Investigation ID** | `2026-07-13-mcp-embedder-service-redesign`                                    |
| **Date Started**     | 2026-07-13                                                                    |
| **Date Completed**   | In Progress                                                                   |
| **Status**           | Gating experiment complete (failed) — redesign proposal awaiting CEO decision |
| **Investigator**     | Dr. Elias Vance, Laboratory Director                                          |
| **Laboratory**       | Core Component 00                                                             |
| **Module(s)**        | MCP server infrastructure (`agent-memory`, `workspace-knowledge`)             |
| **Priority**         | Medium — quality gap, not an outage (see Findings)                            |
| **Requestor**        | CEO                                                                           |

---

## Executive Summary

> The `agent-memory` MCP server has a confirmed, reproducible embedder-initialization stall
> specific to how the MCP host launches its subprocess — not a code defect in this workspace.
> Two rounds of direct, evidence-based investigation ruled out a Python-level import-lock
> deadlock, cold-cache/antivirus latency as a sufficient cause, and general OS-level process
> concurrency. This report proposes moving embedding-model loading out of every host-spawned MCP
> server process and into a persistent, independently-lifecycled local service shared by
> `agent-memory` and `workspace-knowledge`, and recommends a cheap, untested, same-day experiment
> be run first before committing to that larger redesign.

---

## Investigation Scope

### What Was Investigated

Why `agent-memory`'s background embedder-loading thread intermittently freezes indefinitely
inside live, host-spawned MCP server processes, and what architecture would durably resolve it
for both CC-00 MCP servers that load embedding models (`agent-memory`, `workspace-knowledge`).

### Why This Investigation Was Needed

`search_memory` (agent-memory) needs a loaded embedding model to return real (non-degraded)
results. The stall means this frequently fails to happen — not because the model is missing or
misconfigured, but because model _loading_ itself can hang indefinitely in the live server
process. This was traced back from an earlier, separate incident: a full server hang on
`health_check`/`search_memory` (now fixed — see `.claude/rules/mcp-governance.md`'s
`agent-memory` row), during which this embedder-loading stall was discovered as a distinct,
second issue.

### Out of Scope

- The Qdrant network-call hang and its fix (hard-timeout watchdog) — already resolved, documented
  in `.claude/rules/mcp-governance.md`, not revisited here.
- Any change to MCP tool routing, permissions, or the tool surface itself.
- `workspace-knowledge`'s own architecture beyond the embedder-loading question — it is included
  here only as a second consumer of the proposed shared service, not audited independently.

---

## Research Questions

1. What is actually causing the embedder-loading thread to freeze, and is it something inside
   this codebase's control?
2. Does the freeze correlate with thread-level contention, disk/AV cold-cache state, general
   process concurrency, or something specific to the MCP host's own subprocess-launch mechanism?
3. What architecture would remove the failure mode structurally rather than mitigate around it?
4. Is there a cheaper intervention worth trying before committing to a larger architectural
   change?

---

## Methodology

### Approach

Two sequential rounds of hypothesis-driven investigation, each testing specific, falsifiable
claims rather than accepting a plausible-sounding explanation without direct evidence:

1. **Round 1** — tested whether a Python-level per-module import lock could deadlock the
   embedder-warmup thread against the server's own asyncio event loop or other threads. Built a
   minimal repro of the real threading structure; also ran the real server under artificial
   concurrent CPU load.
2. **Round 2** — after a proposed mitigation (provisioning-time cache warm-up) was verified twice
   in isolation, then contradicted by a live failure minutes later, re-tested the concurrency
   hypothesis directly (same-host and independent-process concurrent imports, 17 total controlled
   launches) and, opportunistically, captured two live MCP-host-launched processes stalled
   simultaneously at the same import point.

### Tools and Resources

- `py-spy` (live Python stack sampling, including native-frame resolution)
- PowerShell `Start-Job` / `Start-Process` with hard timeouts for every bounded reproduction
  attempt (this stall is confirmed capable of running 10+ minutes; no test was ever left
  unbounded)
- The existing shared embedding-model cache (`core-component-00/mcp-servers/_shared/models/`)

### Constraints

- No administrative access in-session to disable Windows Defender or add scan exclusions, which
  would have been the decisive experiment for the cold-cache hypothesis.
- Cannot introspect Claude Code's own MCP-host subprocess-launch implementation from inside this
  session — the final finding identifies host-launch behavior as the trigger without being able
  to see _why_ at the host-implementation level.

---

## Findings

### Finding 1: Not a code-level thread deadlock

**Evidence:** A minimal repro reproducing the real server's exact threading structure (asyncio
event loop + daemon thread importing `sentence_transformers`) completed cleanly in ~10s. The real
server, run directly and also under deliberately heavy artificial concurrent load, completed
cleanly both times.

**Implications:** Rules out the most common class of explanation for a silent multi-thread hang
in Python. No fix was needed or attempted here.

### Finding 2: Not sufficiently explained by cold disk/AV cache

**Evidence:** A provisioning-time cache warm-up script (`warm_embedder_cache.py`) was built and
verified to run successfully twice in direct succession (~9.3–9.5s each). Minutes later, on the
same machine, a live server process launched via a normal MCP reconnect stalled at the identical
import point for 3+ minutes.

**Implications:** Whatever role OS/AV file-cache state plays, it is not sufficient on its own to
explain the failure — the cache was demonstrably warm and the stall still occurred.

### Finding 3: Not general cross-process concurrency

**Evidence:** 17 controlled concurrent import launches across two independent mechanisms
(`Start-Job` and `Start-Process`), including simulating two MCP servers restarting at once, all
completed cleanly in 9–18s. Zero reproductions.

**Implications:** Concurrent heavy imports on this machine, launched normally, do not trigger the
stall. This was the leading hypothesis going into Round 2 and was directly falsified.

### Finding 4: Specific to the MCP host's subprocess-launch path

**Evidence:** Two independent live `agent-memory` server processes, both spawned by Claude Code's
own MCP host at the same second, were caught stalled simultaneously at the same import point
(confirmed via two separate `py-spy` dumps roughly a minute apart, no progress). Every one of 13
manually-launched test processes across both investigation rounds succeeded without exception,
regardless of launch mechanism or concurrency.

**Implications:** The asymmetry — host-launched processes fail, identically-shaped manually
launched processes never do — is the actual finding. Something about how the MCP host spawns its
subprocess (stdio pipe setup, an isolation/sandboxing layer, or handle inheritance not visible
from inside this session) creates the triggering condition. This is outside CC-00's authority to
patch directly.

### Finding 5: The freeze point is not fixed

**Evidence:** Different occurrences froze at different files within the same import chain
(`scipy\sparse\linalg\_svdp.py:23` in one case, `scipy\special\__init__.py:784` in another).

**Implications:** Consistent with an external, per-file I/O cost (e.g., a scan or handle
operation charged per file touched) rather than a fixed code-level lock-ordering deadlock, which
would be expected to freeze at the same line every time.

---

## Analysis

### Interpretation of Findings

The stall's cause sits at a layer this workspace does not own or control: the MCP host's process
launch path. No amount of change inside `server.py` or its dependencies can fix the trigger
itself. The only two classes of response available are (a) mitigate — keep the failure mode but
make it harmless, which is already substantially true today via graceful degradation, or (b)
architect around it — remove the precondition (a heavy compiled-extension import happening inside
a host-spawned process at all) by relocating that work to a process the host does not spawn or
churn.

### Trade-offs Identified

| Approach                                    | Removes trigger?        | New operational surface                | Effort        |
| ------------------------------------------- | ----------------------- | -------------------------------------- | ------------- |
| Status quo (graceful degradation only)      | No                      | None                                   | None          |
| Retry-with-timeout inside current process   | Unproven, cheap to test | None                                   | Same-day      |
| Persistent embedder service (this proposal) | Yes (structurally)      | New always-on process to own/supervise | ~2.5 sessions |

### Risks and Limitations

- **The persistent-service fix is a reasonable bet, not a proven one.** It assumes the trigger is
  specifically "heavy compiled-extension import inside a host-spawned process." If the true
  trigger is broader (e.g., something about host-spawned process I/O in general), a thin HTTP
  client from the MCP server to the new service is far less likely to touch the same condition,
  but this has not been tested in isolation.
- **New infrastructure creates new failure modes.** This session independently encountered
  orphaned and duplicate `agent-memory` MCP processes multiple times, with just the two servers
  that exist today. A third long-lived, independently-supervised process is a real addition to
  that surface, not a neutral one.
- **The cheap alternative is untested.** Nothing in either investigation round tried a second
  import attempt within the same host-spawned process after the first stalls. If a retry
  succeeds, most of the cost below is avoidable.

---

## Recommendations

### Primary Recommendation — RUN, RESULT: retry did not resolve the stall

> **Approved and implemented 2026-07-13.** Added a bounded retry to `_load_embedder_background`
> in `agent-memory/server.py`, reusing the existing `_call_with_hard_timeout` watchdog pattern:
> attempt the import with a 60s bound (generous — above every observed successful load time of
> 9–18s, well below the confirmed 3–14+ minute stalls), retry once in a fresh thread on timeout,
> then degrade cleanly. Verified in isolation first (a simulated stall-then-succeed case recovers
> correctly on the second attempt) before any live test.
>
> **Live result:** tested against a real MCP-host-launched process after a normal `/mcp
reconnect`. The live `search_memory` response changed from the old ambiguous "still loading"
> message to `"embedding model failed to load (failed: import did not complete within 60.0s
across 2 attempts)"` — confirming both attempts ran and both stalled. The retry mechanism
> itself worked exactly as designed (clean, bounded, accurately-labeled failure instead of an
> indefinite hang), but **did not recover real results**. This means the trigger is not a brief,
> retry-shakeable blip — it affects a launched process persistently, not transiently.
>
> Per this report's own pre-committed decision criteria: the persistent-service case is now
> justified by direct evidence, not merely a plausible assumption.

### Secondary Recommendations — now justified by the retry experiment's result

1. **Build `embedder-service`** as a persistent, independently-lifecycled local process (local
   HTTP, matching the existing Qdrant-over-HTTP precedent in this codebase; apply the `NO_PROXY`
   lesson from `02-deployment-guidelines.md` from day one) that loads both
   `all-MiniLM-L6-v2` and `all-mpnet-base-v2` once from the existing shared model cache.
2. **Migrate incrementally**, `agent-memory` first (behind a feature flag, keeping the current
   in-process loader as fallback so the degrade-never-block guarantee is never weakened), then
   `workspace-knowledge` once proven.
3. **Resolve service lifecycle ownership before implementation, not after.** Given this session's
   own repeated experience with orphaned MCP processes, an unowned "who starts and supervises
   this" answer is a blocker, not a detail to defer. Candidates: OS-level scheduled/login-trigger
   (persists across reboots, adds a permanent background process); manual per-session start
   (simplest, but silently falls back to today's status quo if forgotten — an acceptable but
   real failure mode); or launched-and-owned by the first MCP server that needs it (most
   automatic, but ownership of shutdown is the hardest of the three to get right).
4. **Decide blast-radius posture explicitly.** This workspace already separated `qdrant-memory`
   from `qdrant-workspace` specifically for isolation (`2026-07-10-agent-memory-architecture/
supporting/09-mcp-architecture-decision.md`). Whether one shared embedder service or two
   isolated ones is the right call given that precedent is a CEO decision, not an engineering
   default.

### Implementation Priority

| Recommendation                           | Priority       | Effort        | Impact                                        |
| ---------------------------------------- | -------------- | ------------- | --------------------------------------------- |
| Retry-with-timeout experiment            | P1             | Same-day      | May resolve entirely at near-zero cost        |
| Persistent embedder service (if needed)  | P2             | ~2.5 sessions | Structural fix, new operational surface       |
| Service lifecycle decision               | Blocker for P2 | N/A           | Prevents a new orphaned-process class         |
| Blast-radius decision (shared vs. split) | Blocker for P2 | N/A           | Consistency with existing isolation precedent |

### Next Steps

1. CEO decision: authorize the retry-with-timeout experiment (low cost, no open questions).
2. If the CEO wants to proceed with the persistent-service architecture regardless of the retry
   experiment's outcome, the two blocker decisions above (lifecycle, blast radius) need answers
   before implementation begins.
3. Either path: no change to the existing Qdrant watchdog, disaster-recovery replay path, or
   graceful-degradation contract — all remain correct and unaffected.

---

## References

### Internal Documentation

- `.claude/rules/mcp-governance.md` — `agent-memory` row: full incident history (Qdrant hang fix,
  embedder-stall root-cause chain this report continues)
- `core-component-00/telescope/2026-07-10-agent-memory-architecture/research-report.md` and its
  `supporting/` folder — the parent memory-system programme this infrastructure serves
- `core-component-00/telescope/2026-07-10-agent-memory-architecture/supporting/
02-deployment-guidelines.md` §1.1 — the Windows `NO_PROXY` precedent to reapply in any new
  HTTP-based service
- `core-component-00/telescope/2026-07-10-agent-memory-architecture/supporting/
09-mcp-architecture-decision.md` — the blast-radius-isolation precedent referenced in
  Recommendations

### Related Work

- `core-component-00/mcp-servers/_shared/provision_model.py`,
  `core-component-00/mcp-servers/_shared/warm_embedder_cache.py` — existing shared-cache and
  warm-up tooling this proposal builds on rather than replaces

---

## Open Questions

1. **Does the retry-with-timeout experiment resolve this at near-zero cost?**
   - Status: Not yet tried — this report's primary recommendation
   - Priority: High
   - Assigned: Next session

2. **Service lifecycle ownership**, if the redesign proceeds
   - Status: Three candidate answers identified, none selected
   - Priority: Blocker for implementation
   - Assigned: CEO decision

3. **Shared vs. isolated embedder service per model**, if the redesign proceeds
   - Status: Precedent exists (Qdrant instance separation) but not yet applied to this decision
   - Priority: Blocker for implementation
   - Assigned: CEO decision

---

## Version History

| Version | Date       | Author                               | Changes                                                                                                                        |
| ------- | ---------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| 1.0     | 2026-07-13 | Dr. Elias Vance, Laboratory Director | Initial report — reframed from `agent-memory-architecture` supporting docs into a standalone telescope study per CEO direction |

---

**Template Version:** 1.0
**Last Updated:** 2026-07-13
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
