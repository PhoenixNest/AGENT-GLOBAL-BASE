# Log Entry 08 — Per-Server Venv Architecture Decision — 2026-08-20

| Field            | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`, pipeline stage 2 — Approval (`core-component-00/platform/maintenance-records/pipeline.md`), resolving Open Follow-Up Item #4 from `log/06-linux-launch-applied-and-verified.md`                                                                                                                                                                                                            |
| **Trigger**      | CEO asked Dr. Vance for advice on Item #4 (per-server vs. shared venv architecture) rather than a unilateral executor decision, per this topic's authority model (a cross-module architecture change is outside Infrastructure Engineer's unilateral authority per `crew/CLAUDE.md` § Authority Scope; Dr. Vance's sign-off applies).                                                                                                                                                                              |
| **State before** | `mcp-servers/CLAUDE.md` and `.claude/rules/mcp-governance.md` both documented a single shared venv at `mcp-servers/.venv/` as the required architecture, with an explicit rationale (deterministic `embedder-service` interpreter inheritance via `sys.executable`, ~2.7 GB disk savings). The actual live `.mcp.json` (since `log/06`) pointed at per-server venvs instead, because the shared venv had never been provisioned on this machine — a documented discrepancy between the docs and reality (Item #4). |

**Actions taken:**

1. Analyzed the tradeoff rather than defaulting to "match the docs" or "match what's already
   running":
   - Checked both servers' `pyproject.toml` for the actual risk the shared-venv design defends
     against (embedder-service interpreter drift). Found `torch>=2.13.0` and
     `sentence-transformers>=5.6.0` declared identically in both files, from the same explicit
     `pytorch-cu130` index — the nondeterminism risk is theoretical on this machine today, not
     observed, and is actually a version-pin discipline question, not strictly a venv-layout one.
   - Weighed per-server venvs as uv's idiomatic default (each server manages its own dependency
     lifecycle independently) against the shared venv's real benefits (disk savings, one lockfile)
     and its real cost here (migrating two already-working, already-verified venvs into one merged
     `pyproject.toml` for a benefit — ~2.5 GB disk — that doesn't bind on this machine).
   - Recommended: keep per-server venvs as the permanent architecture, conditioned on keeping the
     `torch`/`sentence-transformers` pins identical across both servers' `pyproject.toml` files —
     that condition, not the venv layout, is what actually preserves `embedder-service`'s
     deterministic behavior.
2. Presented the recommendation to the CEO (not implemented pending sign-off, since this is a
   cross-module architecture claim in `mcp-servers/CLAUDE.md`, not a routine maintenance edit).
3. CEO approved keeping per-server venvs as the permanent architecture.
4. Updated `mcp-servers/CLAUDE.md` § Python Environment: retitled "One Shared Venv" →
   "Per-Server Venvs," rewrote the interpreter-selection table and CUDA install commands to the
   per-server paths, added the pin-lockstep invariant as the documented safeguard, and added a
   **Decision history** note in the existing "Cross-platform consequence" callout pointing back to
   this entry.
5. Updated `.claude/rules/mcp-governance.md`: rewrote the "Python environment" paragraph under
   Shared Infrastructure to describe per-server venvs and the pin-lockstep invariant, and updated
   both the `workspace-knowledge` and `agent-memory` Registered Servers row notes to mark this
   follow-up closed rather than pending.

**Verification:**

| Check performed                                                                                | Result                                                                  |
| ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `torch` pin comparison, `workspace-knowledge/pyproject.toml` vs. `agent-memory/pyproject.toml` | Identical: `torch>=2.13.0`, same `[tool.uv.sources]` CUDA index in both |
| `sentence-transformers` pin comparison, same two files                                         | Identical: `sentence-transformers>=5.6.0` in both                       |
| CEO sign-off on the recommendation                                                             | Approved — "keep the per-server design now"                             |

**Independent-review gate (`pipeline.md` stage 2 — Approval):** Satisfied. This is an architecture
decision, not a shared-production-resource code change, so stage 2's approval gate (not stage 4's
independent-review gate) applies — CEO approval is the required sign-off, recorded above.

| Field                     | Detail                                                                                                                                                                                                                                                                                                                           |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Outcome**               | Open Follow-Up Item #4 is closed. Per-server venvs are now the documented, CEO-approved architecture for this workspace's MCP servers, not merely this machine's ad-hoc state. The shared-venv design's real guarantee is preserved via the pin-lockstep invariant rather than via venv layout.                                  |
| **Handoff to next stage** | Does not close this topic. Two items remain open (see `maintenance-record.md`, updated alongside this entry): Item #5 (completing the full dependency sync so both servers run at full capability — in progress as of this entry, tracked separately) and Item #3 (Linux/macOS DR-scheduling verification, explicitly deferred). |
