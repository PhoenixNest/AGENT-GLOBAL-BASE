# Log Entry 03 — Idle-Recovery Repair and Self-Check — 2026-10-13

| Field            | Detail                                                                                                                                                                                                                                                                                                |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-10-12-shared-embedding-model-cache-loss/maintenance-record.md`                                                                                                                                                                                   |
| **Trigger**      | CEO authorization to repair the malfunctioning MCP servers and self-check the result, after both servers kept returning keyword-only results once the model files were restored                                                                                                                       |
| **State before** | `agent-memory` `health_check`: `embedder_service_state: ready`, `embedder_service_state_age_s: 3475.9`, `in_process_fallback_state: not started`. Nothing listening on `127.0.0.1:8791`. `search_memory` returned `degraded: true`, `tier: 3`. `workspace-knowledge` failed to connect (30 s timeout) |

**Root cause (two independent defects):**

1. Idle recovery. Each server launched `embedder-service` once at process start and cached
   `ready` for the life of the process. `embedder-service` exits after 600 s idle. Nothing
   re-checked the cached `ready`, nothing relaunched the service, and because the state still
   read `ready` the in-process fallback was never started. Every search from about ten minutes
   after the last one degraded to keyword matching while `health_check` repeated the stale
   `ready`.
2. Connect timeout. `workspace-knowledge` built its BM25 index (about 4,000 chunks, 12–18 s)
   synchronously before answering the MCP handshake.

**Actions taken:**

1. Specified and reviewed by the lead orchestrator; code written by a Sonnet engineer subagent;
   self-check run by the orchestrator. No commit, no push, no write to either Qdrant store, no
   change under `.claude/`.
2. `_shared/embedder_client.py`: added a non-blocking, single-flight, cooldown-gated relaunch
   request; the lock/pid directory is overridable for side-by-side test instances.
3. Both servers: a cached `ready` older than 30 s is re-probed; a failed probe or failed embed
   call marks the service down and requests a relaunch; a cached `unavailable` is re-probed on a
   cooldown and requests a relaunch; the tool call waits a bounded time (45 s default) for
   recovery; `health_check` reports a real probe made at call time.
4. `agent-memory`: the in-process fallback load starts only after a relaunch fails or the wait
   expires.
5. `workspace-knowledge`: the whole index initialization runs in the background thread; health
   reports `effective_search_tier` and an `embedder` block.

**Review finding during the work:** the first version started the in-process model load in
parallel with the relaunch. In a real MCP session the relaunch was then never observed by the
server (launch logged, no "came up" for over 46 s, although the port answered an external probe),
and the first and second searches after idle both degraded. The unit tests and the engineer's own
end-to-end script had passed. Corrected by making the two steps sequential (action 4).

**Verification (orchestrator, real stdio MCP sessions against the changed code, side-channel
`embedder-service` on port 8794 with a 25 s idle timeout, read-only):**

| Check performed                                  | `agent-memory`                              | `workspace-knowledge`                                 |
| ------------------------------------------------ | ------------------------------------------- | ----------------------------------------------------- |
| MCP handshake answered                           | 16.1 s                                      | 1.9 s (12.4–14.6 s before the change)                 |
| Health with service up                           | Pass — `probe: ok`, path `embedder-service` | Pass — `hybrid_qdrant`, no degradation reason         |
| Search with service up                           | Pass — `degraded: false`, `tier: 1`         | Pass                                                  |
| Service idled out, then health                   | Pass — `probe: failed`, path `unavailable`  | Pass — effective tier `bm25` with the reason stated   |
| Health check did not itself relaunch the service | Pass                                        | Pass                                                  |
| First search after idle                          | Pass — `degraded: false`, `tier: 1`, 18.2 s | Pass — same top result as with the service up, 15.4 s |
| Second search and health after recovery          | Pass — 0.1 s, `probe: ok`                   | Pass — 0.6 s, `hybrid_qdrant`, no degradation reason  |
| Test suite                                       | 349 passed, 2 failed, 1 skipped             | 83 passed                                             |

The two `agent-memory` failures
(`test_absolute_windows_backslash_launch_matches`,
`test_search_memory_source_byte_identical_to_pre_write_path_commit`) fail on the unmodified
tree as well and concern code this change does not touch.

**Not verified:**

- The servers connected to Claude Code were started before the change and run the previous code
  until reconnected; the change has not been exercised through the live connection.
- A full 600 s idle period on the default port (the check used a 25 s idle timeout).
- Simultaneous relaunch requests from several server processes.
- `agent-memory`'s MCP handshake takes about 16 s, inside but not far from the 30 s connect limit.

**Follow-up:** two statements in `.claude/rules/mcp-governance.md` no longer describe the
servers (health reporting a cached state with an age; the service being launched only by the
first consumer). Stale server processes from earlier sessions remain running.
