# Log Entry 06 — Linux Launch Path Applied and Verified — 2026-08-20

| Field            | Detail                                                                                                                                                                                                                                                                                                                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`, pipeline stage 3 — Execution (`core-component-00/platform/maintenance-records/pipeline.md`), on the existing topic per the topic-boundary test — same system (`.mcp.json`'s `"command"`), direct follow-up to Open Follow-Up Item #1 from this topic's Close |
| **Trigger**      | CEO asked for this topic's Open Follow-Up Item #1 (`.mcp.json` still Windows-only, requires a manual per-OS edit) to be treated as a maintenance task and fixed on a WSL/Linux machine now actually available for testing.                                                                                                                                                           |
| **State before** | `.mcp.json`'s `"command"` for both servers was `${CLAUDE_PROJECT_DIR:-.}/core-component-00/platform/model-context-protocol-servers/.venv/Scripts/python.exe` — the Windows-only path, per the 2026-08-13 revert (`log/03-incident-revert.md`). No `.venv` existed at `core-component-00/platform/model-context-protocol-servers/.venv/` on this machine at all.                      |

**Actions taken:**

1. Inspected this machine directly rather than applying the documented one-line edit blind:
   confirmed no shared venv exists at `core-component-00/platform/model-context-protocol-servers/.venv/`. Instead, each server
   has its own independent, working venv — `workspace-knowledge/.venv/` and `agent-memory/.venv/` —
   each with its own `pyproject.toml`/`uv.lock`, matching neither this topic's documented
   architecture (`mcp-servers/CLAUDE.md` § Python Environment: "one shared venv... do not add
   per-server `.venv/` directories") nor the two READMEs' `.mcp.json` example. See **New finding**
   below — this is a real divergence, not something this entry resolves.
2. Edited `.mcp.json`'s `"command"` for both servers to point at each server's own per-server venv
   interpreter instead of the (non-existent, on this machine) shared-venv path:
   - `workspace-knowledge`: `${CLAUDE_PROJECT_DIR:-.}/core-component-00/platform/model-context-protocol-servers/workspace-knowledge/.venv/bin/python`
   - `agent-memory`: `${CLAUDE_PROJECT_DIR:-.}/core-component-00/platform/model-context-protocol-servers/agent-memory/.venv/bin/python`
     Both remain direct, absolute interpreter paths — no bare command name, no `PATH` resolution, no
     `uv run` indirection — consistent with the guardrail this topic's incident (`log/03-incident-revert.md`)
     established.
3. Foreground-launched `workspace-knowledge` with the new path — started cleanly on the first try.
4. Foreground-launched `agent-memory` with the new path — failed: `ModuleNotFoundError: No module
named 'psutil'`, even though `psutil>=6.0.0` is declared in `agent-memory/pyproject.toml` (the
   2026-08-13 psutil port). The per-server venv predates that dependency being added and was never
   re-synced.
5. Ran `uv sync` in `agent-memory/` to bring the venv in line with its lockfile. Its resolve step
   found `agent-memory/uv.lock` itself was stale — missing `psutil`, `sentence-transformers`, and
   `torch` even though all three are declared in `pyproject.toml` — and rewrote the lockfile to
   match (this is why `uv.lock` shows as changed even though installation did not complete). The
   subsequent download of the full CUDA/torch/transformers/scikit-learn dependency set (~2.5 GB)
   was too slow for this session's turnaround; killed it after ~9 minutes at ~160 MB downloaded, no
   packages installed from it. The regenerated `uv.lock` itself is kept — it is a correctness fix
   independent of whether the download finishes.
6. Installed just the missing blocker directly instead: `uv pip install --python .venv/bin/python
psutil` in `agent-memory/` — resolved and installed in under 10 seconds (`psutil==7.2.2`).
7. Re-ran the foreground launch for `agent-memory` — started cleanly, and its startup diagnostic
   line confirmed the 2026-08-13 psutil sibling-cleanup port itself works correctly on Linux:
   `[DIAG ...] sibling-cleanup: no sibling processes older than 200s found`.
8. Updated both server READMEs' Configuration sections with a dated note pointing at this entry,
   since their existing `.mcp.json` example and prose describe the shared-venv path this machine
   does not have.

**Verification:**

| Check performed                                                                                | Result                                                                                                   |
| ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Foreground launch, `workspace-knowledge/.venv/bin/python server.py`, fixed `.mcp.json` command | Started cleanly — FastMCP banner, `workspace-knowledge, 3.2.4`, exit code 0                              |
| Foreground launch, `agent-memory/.venv/bin/python server.py`, before psutil fix                | Failed — `ModuleNotFoundError: No module named 'psutil'`                                                 |
| `uv pip install --python .venv/bin/python psutil` in `agent-memory/`                           | Succeeded — `psutil==7.2.2` installed                                                                    |
| Foreground launch, `agent-memory/.venv/bin/python server.py`, after psutil fix                 | Started cleanly — sibling-cleanup diagnostic printed, FastMCP banner, `agent-memory, 3.4.5`, exit code 0 |
| `import torch` / `import sentence_transformers` in both servers' venvs                         | Both MISSING in both venvs — neither venv has the full ML dependency set synced                          |

**Not verified:** an actual `/mcp reconnect` from a live Claude Code host process against this
`.mcp.json` — all verification above is direct foreground process launch, which is the same class
of check the 2026-08-13 incident showed is **not sufficient on its own** for `.mcp.json` changes
(the `uv` attempt also launched cleanly in the foreground and still failed under the host's actual
spawn environment). Whoever next runs `/mcp reconnect` on this machine should treat that as the
real confirming test, not this entry's foreground checks alone.

**New finding — per-server venvs, not the shared venv, on this machine:** `mcp-servers/CLAUDE.md`
and `.claude/rules/mcp-governance.md` both document a single shared venv at
`core-component-00/platform/model-context-protocol-servers/.venv/`, with an explicit rationale (deterministic `embedder-service`
interpreter inheritance via `sys.executable`, disk savings). This machine has never had that shared
venv — each server was set up independently with its own venv and lockfile. This entry does **not**
resolve that discrepancy; it applies the pragmatic fix (point `.mcp.json` at what actually exists
and works) and flags the architecture question as its own open item below, since choosing between
"adopt per-server venvs" and "provision the documented shared venv on this machine" is an
architecture call outside a maintenance follow-up's scope.

**Independent-review gate (`pipeline.md` stage 4):** `.mcp.json` is a shared production resource
other sessions depend on — per this topic's own Verification-stage gate, Status may not read
"Completed" on the strength of this entry's self-verification alone. No reviewer other than the
executor was available in this session. **Status stays "Executed, pending independent
verification"** until someone else confirms `/mcp reconnect` actually works on this machine.

| Field                     | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Outcome**               | Both servers now launch cleanly on this WSL/Linux machine via direct per-server venv interpreter paths in `.mcp.json`. The original 2026-08-13 finding (Windows-only hardcoded path) is functionally fixed for this machine — not by the documented shared-venv one-line edit (that venv doesn't exist here), but by an equivalent direct-path edit against each server's real, working venv. Neither server's venv has the full CUDA/torch/ML stack synced, so both would currently run with `embedder-service`/local-model embedding degraded rather than fully capable — a separate, already-documented graceful-degradation path (`.claude/rules/mcp-governance.md` § Shared Infrastructure), not a new failure this entry introduces. |
| **Handoff to next stage** | Does not close this topic. Three items now open (see `maintenance-record.md`'s Open Follow-Up Items, updated alongside this entry): (1) independent confirmation that `/mcp reconnect` actually works on this machine with the new paths; (2) the shared-vs-per-server venv architecture question, owned by Dr. Vance/Ravi Deshmukh; (3) completing the full `uv sync` (CUDA/torch/transformers/scikit-learn) in both venvs so embedding runs at full capability rather than degraded. None of the three block the launch-path fix itself from standing.                                                                                                                                                                                   |
