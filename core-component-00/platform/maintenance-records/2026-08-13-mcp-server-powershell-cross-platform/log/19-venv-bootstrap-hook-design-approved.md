# Log Entry 19 — Approval — 2026-09-01

| Field            | Detail                                                                                                                                                                                                                     |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`, pipeline stage 2 — Approval (`core-component-00/platform/maintenance-records/pipeline.md`)         |
| **Trigger**      | `log/18`'s recommendation — build a new, independent `SessionStart` hook for `uv sync`/venv bootstrap, gated on `mcp-config-platform-check.py` reporting `neither_os_path_exists`, rather than extending that hook itself. |
| **State before** | No approval recorded for this design; `log/18` left the choice open pending CEO sign-off.                                                                                                                                  |

**Actions taken:**

1. Presented the recommendation and its rationale (preserving the existing hook's fast,
   read-mostly, fail-open contract that the CEO had previously required — see `log/14`) to the
   CEO.
2. CEO approved the recommendation ("That sounds good").
3. CEO separately directed that this whole investigation-and-decision be logged as a maintenance
   record — this file and `log/18` are that record, filed as a continuation of this topic rather
   than a new one, since both concern the same system/resource already named in this topic's
   header (`.claude/hooks/mcp-config-platform-check.py`, the two servers' per-server venvs) and
   are a direct follow-up to the residual gap this topic's own Item #6 closing note (`log/17`)
   left flagged and untested.

**Verification:**

N/A — this is an approval-stage entry recording a decision, not a code change; there is no
testable claim yet. Verification of the resulting hook belongs to the Execution/Verification
stages once it is built (see Handoff below).

| Field                     | Detail                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Outcome**               | New Open Follow-Up Item #8 opens on this topic: build a new, independent venv-bootstrap hook. Design approved; implementation not yet started. No code has been changed in this investigation-and-approval pass — `mcp-config-platform-check.py`, `.mcp.json`, and both servers remain exactly as `log/17` left them.                                          |
| **Handoff to next stage** | Routes to stage 3 — Execution (build the new hook), not yet scheduled. Until then, both MCP servers remain disconnected on any machine where their `.venv` was never bootstrapped; the immediate, already-available workaround is running `uv sync` by hand in `workspace-knowledge/` and `agent-memory/` per each server's README "First-time setup" section. |
