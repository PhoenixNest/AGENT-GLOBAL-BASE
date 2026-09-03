# Log Entry 12 — Windows Venv Sync & jsonref/proxytypes Fix — 2026-08-26

| Field            | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`, pipeline stage 3 — Execution (`core-component-00/platform/maintenance-records/pipeline.md`), a new incident found while performing `log/11`'s Handoff step (live `/mcp reconnect` verification), routed per the topic-boundary test (same system, `.mcp.json`-registered servers, direct consequence of attempting to verify `log/11`'s fix) rather than opened as a new topic |
| **Trigger**      | CEO ran `/mcp` (reconnect) per `log/11`'s Handoff instruction. Both servers returned `Failed to reconnect ...: CONNECTION_CLOSED` — a new failure, distinct from the OS-path bug `log/11` fixed (which is confirmed still correct: both `.mcp.json` commands point at the right, existing `.venv/Scripts/python.exe` for this machine).                                                                                                                                                                |
| **State before** | `.mcp.json` correct (per `log/11`). Both servers' per-server venvs on this Windows machine had never received the full dependency sync that `log/06`/`log/09` applied only to the WSL/Linux machine used for those entries — a fact not previously surfaced because no one had foreground-launched either server on this specific Windows machine since `log/02`'s original 2026-08-13 remediation.                                                                                                    |

**Actions taken:**

1. Foreground-launched each server directly (`<venv>/Scripts/python.exe server.py --help`), the
   same diagnostic method `log/03` and `log/06` used, to get the real error the generic
   `CONNECTION_CLOSED` message hides:
   - `workspace-knowledge`: `ModuleNotFoundError: No module named 'proxytypes'` (raised from
     inside the installed `jsonref` package, itself imported transitively by `fastmcp`).
   - `agent-memory`: `ModuleNotFoundError: No module named 'psutil'`.
2. Ran `uv sync` for both `workspace-knowledge` and `agent-memory` (backgrounded — the shared
   `torch==2.13.0+cu130` wheel is ~1.8GB). `agent-memory`'s first attempt failed after a 300s
   timeout acquiring a lock on the shared `uv` wheel cache, because `workspace-knowledge`'s sync
   was mid-download of the same cached `torch` wheel at the time — resource contention between the
   two concurrent syncs, not a real dependency problem. Re-ran `agent-memory`'s sync after
   `workspace-knowledge`'s finished; it completed in ~34s reusing the now-cached wheel.
3. `agent-memory` foreground-relaunched cleanly after its sync (`psutil` now present, FastMCP
   banner, exit 0). `workspace-knowledge` still failed with the identical `proxytypes` error even
   after a clean `uv sync` — the missing package was never a sync-staleness problem.
4. Investigated the `proxytypes` failure directly: the installed `jsonref==1.1.0` wheel's
   `jsonref.py` contains a plain `from proxytypes import LazyProxy` (absolute import, no
   try/except). `jsonref`'s own `pyproject.toml`/`uv.lock` metadata does not declare `proxytypes`
   as a dependency at all, so `uv sync` never installs it — this is an upstream packaging defect in
   the published `jsonref==1.1.0` wheel (confirmed via `jsonref.readthedocs.io`'s hosted source,
   which shows a _relative_ `from .proxytypes import LazyProxy` in the current repo — the published
   1.1.0 wheel predates that fix and still ships the broken absolute import).
5. Ran `uv add proxytypes` in `workspace-knowledge/` to make a fix attempt — it resolved and
   installed `ProxyTypes==0.10.0` successfully, but the launch still failed with the same
   `ModuleNotFoundError`. Inspected the installed package directly: `ProxyTypes` 0.10.0 installs
   its actual code at `peak/util/proxies.py` (a legacy setuptools namespace-package layout), not a
   top-level `proxytypes` module — so `jsonref`'s bare `import proxytypes` still cannot resolve it,
   even though the correct implementation (`peak.util.proxies.LazyProxy`) is present and importable
   under its real name. Confirmed directly: `python -c "from peak.util.proxies import LazyProxy"`
   succeeds.
6. Added a small vendored compatibility shim,
   `core-component-00/platform/model-context-protocol-servers/workspace-knowledge/_vendor/proxytypes.py`, which re-exports
   `peak.util.proxies`'s contents (including `LazyProxy`) under the top-level name `jsonref`'s
   wheel expects. Edited `server.py` to insert `_vendor/` onto `sys.path` before the `fastmcp`
   import (fastmcp transitively imports `jsonref`, so the shim must be resolvable before that
   import runs) — mirrors the file's existing pattern of `sys.path.insert(...)` for local-module
   resolution, just earlier in the file since this import happens before that block.
7. Re-verified `workspace-knowledge`'s foreground launch: FastMCP banner printed, exit 0, no
   `ModuleNotFoundError`.

**Verification:**

| Check performed                                                                                            | Result                                                                                                                          |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Foreground launch, `agent-memory`, after its `uv sync`                                                     | FastMCP banner, `agent-memory, 3.4.5`, exit code 0                                                                              |
| Foreground launch, `workspace-knowledge`, after `uv sync` alone (before the shim)                          | Still failed — `ModuleNotFoundError: No module named 'proxytypes'`, confirming sync wasn't the cause                            |
| `uv add proxytypes` in `workspace-knowledge/`, then re-verify launch                                       | Package installed (`ProxyTypes==0.10.0`), launch still failed — confirmed the namespace mismatch, not a missing-package problem |
| `python -c "from peak.util.proxies import LazyProxy"`                                                      | Succeeds — confirms the real implementation is present and correctly named under its own namespace                              |
| Foreground launch, `workspace-knowledge`, after adding `_vendor/proxytypes.py` + `server.py` sys.path edit | FastMCP banner, `workspace-knowledge, 3.2.4`, exit code 0                                                                       |

**Independent-review gate (`pipeline.md` stage 4):** **Not yet satisfied.** Same standing
requirement as `log/11` — a live `/mcp reconnect` performed by someone other than the executor is
this topic's actual bar for a `.mcp.json`-registered-server change, not a foreground check alone.
Not yet performed for this entry's fixes specifically.

| Field                     | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Outcome**               | Both servers now foreground-launch cleanly on this Windows machine. Two genuinely new, separate root causes were found and fixed beyond the OS-path bug `log/10`/`log/11` addressed: (1) this machine's venvs had never received the dependency sync `log/06`/`log/09` only applied on the WSL/Linux machine, and (2) `jsonref==1.1.0`'s published wheel has a real upstream packaging defect (an absolute import of a module name no current PyPI package provides under that name), worked around with a small vendored shim rather than waiting on an upstream fix. |
| **Handoff to next stage** | Ask the user/CEO to run `/mcp` (reconnect) again, then call each server's `health_check` tool over the live connection — the same two-step confirmation `log/07` used. If it succeeds, this topic can finally return to `Status: Completed`. If it fails again, this is a third distinct incident and needs its own entry, not a repeat of this one.                                                                                                                                                                                                                   |
