# Log Entry 16 — Reopen & Fix — workspace-knowledge `peak` Shim Regression — 2026-08-30

| Field            | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`, pipeline stage 5→1 — Reopen, immediately followed by Stage 3 — Execution (same entry, per the `log/03-incident-revert.md` precedent for a self-contained root-cause-and-fix) (`core-component-00/platform/maintenance-records/pipeline.md`)                                                                                                                                                                                           |
| **Trigger**      | CEO ran a live `/mcp reconnect` as the independent-review check `log/15` (Item #6) was waiting on. `agent-memory` reconnected successfully. `workspace-knowledge` failed: `Failed to reconnect to workspace-knowledge: CONNECTION_CLOSED`.                                                                                                                                                                                                                                                                                                                    |
| **State before** | `workspace-knowledge`'s `_vendor/proxytypes.py` shim (added `log/12`, 2026-08-26, to fix a genuine jsonref-vs-ProxyTypes packaging mismatch) was being unconditionally prepended to `sys.path` by `server.py`, ahead of `site-packages`. This CONNECTION_CLOSED state was **already present at the very start of this session**, before any of today's `.mcp.json`/Item #6 work — confirmed by the session's own initial tool listing, which already reported `workspace-knowledge (CONNECTION_CLOSED): "Connection closed"` prior to any file being touched. |

**Actions taken:**

1. Foreground-launched `workspace-knowledge/server.py` directly (`.venv/bin/python server.py`) to
   get the real traceback instead of Claude Code's opaque `CONNECTION_CLOSED`:
   `ModuleNotFoundError: No module named 'peak'`, raised inside `_vendor/proxytypes.py`'s
   `from peak.util.proxies import *`.
2. Checked whether `peak` exists anywhere in the venv — it does not (`find ... -iname "*peak*"`
   returned nothing). Checked what `uv sync` actually installed for the `proxytypes` dependency
   (`pyproject.toml`/`uv.lock`, resolving to PyPI `ProxyTypes==0.10.0`): a **top-level
   `proxytypes.py`** module directly in `site-packages`, containing `Proxy`, `CallbackProxy`, and
   `LazyProxy` — i.e. it already satisfies jsonref's `from proxytypes import LazyProxy` import
   with no `peak.util.proxies` namespace involved at all.
3. Confirmed directly: importing `jsonref` with the vendor shim's directory removed from
   `sys.path` succeeds cleanly, `jsonref.LazyProxy` resolves to `proxytypes.LazyProxy` (the real
   site-packages module).
4. Root cause: `log/12`'s fix assumed `ProxyTypes` always installs under `peak.util.proxies`. On
   this Linux venv it does not — it installs the top-level `proxytypes` module the shim exists to
   work around. `server.py`'s unconditional `sys.path.insert(0, _VENDOR_ROOT)` shadows the
   perfectly working real module with the shim, which then fails on an import (`peak`) that was
   never actually needed here.
5. Fixed `workspace-knowledge/server.py`: the vendor-path insertion is now conditional — it
   `import proxytypes` first and only prepends `_vendor/` if that import fails or the resulting
   module lacks `LazyProxy`. This makes the shim a genuine fallback for the packaging layout
   `log/12` was written against, without breaking the layout this venv actually has.
6. Foreground-verified the fix: `workspace-knowledge` now imports `fastmcp` cleanly, launches
   `embedder-service`, and reaches `Starting MCP server 'workspace-knowledge' with transport
'stdio'` before exiting on stdin EOF (expected — no MCP client attached in a foreground test;
   `agent-memory`'s prior foreground checks in this topic exhibit the same exit-on-EOF behavior).

**Verification:**

| Check performed                                                    | Result                                                                                                                                                                                             |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `python3 -c "import ast; ast.parse(...)"` on the fixed `server.py` | Syntax OK                                                                                                                                                                                          |
| Foreground launch, before fix                                      | `ModuleNotFoundError: No module named 'peak'`, traceback through `_vendor/proxytypes.py`                                                                                                           |
| `jsonref` import with `_vendor/` removed from `sys.path`           | Succeeds; `jsonref.LazyProxy` resolves to the real `site-packages/proxytypes.py`'s `LazyProxy`                                                                                                     |
| Foreground launch, after fix                                       | Clean import, `embedder-service` launched, reached `Starting MCP server 'workspace-knowledge' with transport 'stdio'` before exiting on stdin EOF (expected for a foreground stdio-transport test) |

**Independent-review gate (pipeline.md stage 4):** Not yet satisfied — this is a foreground/manual
verification only, self-executed. A live `/mcp reconnect` by the CEO (or anyone other than this
session) confirming `workspace-knowledge` actually connects through the real Claude Code MCP
client is still needed before this closes.

| Field                     | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Outcome**               | Root-caused and fixed. `workspace-knowledge/server.py`'s vendor-shim path insertion is now conditional on the real `proxytypes` package actually lacking `LazyProxy`, instead of unconditionally shadowing it. This is unrelated to Item #6 (`.mcp.json` bootstrap redesign) — confirmed pre-existing before this session's Item #6 work began — but was discovered while verifying Item #6, and does touch a resource this topic already names in scope (`workspace-knowledge/server.py`, `_vendor/proxytypes.py`), so it's logged here rather than as a new topic, per the topic-boundary test. `agent-memory` reconnecting cleanly during the same `/mcp reconnect` attempt that surfaced this bug is itself a positive, live data point for Item #6: the new bootstrap mechanism worked end-to-end for at least one server on the real host, not just the simulated clone in `log/15`. |
| **Handoff to next stage** | Routes to Stage 4 — Verification for both this entry and `log/15`/Item #6 together — a single live `/mcp reconnect` for both servers now covers both. Requesting the CEO run `/mcp` again to confirm `workspace-knowledge` connects cleanly under the fix. Item #3 (Linux/macOS DR scheduling) remains explicitly deferred per CEO direction this turn — no work done on it.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
