# Log Entry 10 — Windows Reopen & Proposed Self-Healing Fix — 2026-08-25

Part of `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
Pipeline stage 5→1 — Reopen (`core-component-00/maintenance-records/pipeline.md`): a new problem
found on a previously-closed item routes back to Investigation, per the topic-boundary test (same
system, `.mcp.json`, direct consequence of `log/06`'s prior change). This entry also carries the
topic into stage 2 (Approval) with a proposed remediation — **not yet executed**, per explicit CEO
direction (see Trigger).

**Trigger:** User reported an MCP server connection failure on this machine and escalated it to
the CEO. CEO asked for investigation and findings; separately asked for a durable, "thorough" fix
(not another one-off path flip) to be proposed and documented as a maintenance record before any
implementation — the CEO wants the record saved locally for review first, and will decide whether
to authorize Execution afterward.

**State before:** Topic `2026-08-13-mcp-server-powershell-cross-platform` was `Status: Completed
with one follow-up item open (2026-08-20)` per `log/07` and `log/09` — Item #1 (`.mcp.json`
launch path) had been closed by pointing both servers at their per-server venvs using the
**Linux/WSL** path (`.venv/bin/python`), applied and independently confirmed via a live `/mcp
reconnect` on that WSL/Linux machine.

**Actions taken (Investigation):**

1. Read the current root `.mcp.json` — confirmed both servers' `"command"` fields still read
   `.../workspace-knowledge/.venv/bin/python` and `.../agent-memory/.venv/bin/python` (the
   `log/06` Linux path), unchanged since 2026-08-20.
2. Checked this machine's environment: Windows (win32), current session shell PowerShell.
3. Verified on disk which venv layout actually exists on this machine:

   | Path checked                                   | Exists? |
   | ---------------------------------------------- | ------- |
   | `workspace-knowledge/.venv/Scripts/python.exe` | Yes     |
   | `workspace-knowledge/.venv/bin/python`         | No      |
   | `agent-memory/.venv/Scripts/python.exe`        | Yes     |
   | `agent-memory/.venv/bin/python`                | No      |

4. Root cause confirmed: `.mcp.json`'s `"command"` is an absolute, non-PATH-resolved path per
   server. On 2026-08-20 it was pointed at the POSIX venv layout (`bin/python`) and verified
   working on a WSL/Linux machine. This machine's venvs use the Windows layout
   (`Scripts/python.exe`) instead, so the configured path does not exist here — the host attempts
   to spawn a nonexistent file, producing the reported connection failure.
5. Reviewed this topic's full history (`log/03`, `log/06`, `log/07`) to confirm this is not a new
   defect class: it is the third recurrence of the same underlying problem (`.mcp.json` cannot
   express an OS-conditional path, so every fix so far has hardcoded one OS and broken the other)
   — first the 2026-08-13 `uv`/stale-host-PATH incident, then the 2026-08-20 Linux-path fix now
   breaking this Windows session.

**Proposed remediation (Approval stage — not yet executed):**

- **Immediate unblock (tactical):** repoint `.mcp.json`'s two `"command"` values to
  `.venv/Scripts/python.exe` for this Windows session. Same class of fix as `log/03`'s revert and
  `log/06`'s Linux repoint — known-working, low-risk, but reintroduces the same fragility the next
  time the OS switches.
- **Durable fix (proposed):** a new `SessionStart` hook,
  `.claude/hooks/mcp_config_platform_check.py` (run via `uv run`, consistent with the existing
  15-hook `uv run` convention per root `CLAUDE.md` §3), that on every session start:
  1. Reads `.mcp.json` and checks whether each server's configured `"command"` file exists on
     disk.
  2. If not, rewrites it to the sibling path for the running platform
     (`Scripts/python.exe` ↔ `bin/python`), detected via `platform.system()` — never via a bare
     command name, so this cannot reintroduce the `log/03` stale-host-`PATH` failure mode; it only
     ever writes fully-resolved absolute paths that were confirmed to exist on disk.
  3. Logs what it changed (visible correction, not a silent edit) and writes the file back before
     Claude Code's own `/mcp reconnect` runs.
  4. No-ops when the configured path already matches the current OS.
  - Fallback alternative (smaller blast radius, more manual): a one-line user-triggered script
    (`uv run .claude/hooks/mcp_config_platform_check.py --fix`) doing the same detection/rewrite,
    run by hand after switching machines, instead of an automatic `SessionStart` hook.
- **Governance check:** this proposal edits `.mcp.json`'s existing `"command"` values via a hook,
  not via a new MCP server — `.claude/rules/mcp-governance.md`'s Three-Gate Inclusion Test governs
  MCP _server_ registrations and does not apply to a hook maintaining existing entries. No
  pipeline/ADR state, approval gate, or governance record is touched or bypassed.

**Verification:** Not yet applicable — no fix has been executed. Per this topic's own stage-4
gate (independent-review required for any change to `.mcp.json`, a shared production resource —
see `log/03`'s and `log/06`'s precedent that self-verification/foreground checks are insufficient
on their own), execution will require a live `/mcp reconnect` confirmation from someone other than
the executor before Status can read `Completed` again.

**Severity:** P0 — both registered MCP servers are currently unreachable for the active session on
this machine (per `pipeline.md`'s severity table: "live service broken for an active
session/user"). Not downgraded despite the CEO's explicit choice to defer Execution pending
review — the severity tag reflects present system state, not scheduling.

**Outcome:** Root cause identified and documented; two remediation options proposed (tactical
path-flip and durable self-healing hook). **No changes made to `.mcp.json`, no hook created, no
implementation performed** — this entry is documentation only, per explicit CEO instruction to
review the proposal before authorizing work.

**Handoff to next stage:** Topic reopened, now sitting at stage 2 (Approval) — pending CEO review
of this entry and the maintenance-record.md update below. On approval, the next `log/` entry
(`log/11-...md`) will record whichever remediation is authorized (tactical-only, durable hook, or
both), followed by a stage-4 independent-verification entry via a live `/mcp reconnect`.
