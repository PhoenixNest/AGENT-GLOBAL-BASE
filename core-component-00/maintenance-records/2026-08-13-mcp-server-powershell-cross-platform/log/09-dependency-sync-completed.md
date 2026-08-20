# Log Entry 09 — Full Dependency Sync Completed — 2026-08-20

Part of `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md`.
Pipeline stage 3 — Execution (`core-component-00/maintenance-records/pipeline.md`), closing Open
Follow-Up Item #5.

**Trigger:** CEO approved continuing the dependency sync (raised alongside the Item #4 advice
request). Both venvs' `uv sync` were relaunched in the background to install the full
CUDA/torch/transformers/scikit-learn stack that `log/06`'s launch fix had left incomplete.

**State before:** `agent-memory/.venv/` and `workspace-knowledge/.venv/` both had `fastmcp` and
their core dependencies but not `torch`, `sentence-transformers`, or (for `workspace-knowledge`)
`rank_bm25` — both servers ran with embedding/search degraded, directly observed via
`health_check` in `log/07`.

**Actions taken:**

1. Relaunched `uv sync` for `agent-memory` and `workspace-knowledge` as detached background
   processes so they could run to completion independent of the interactive session.
2. A session-level interruption (transient model unavailability, mid-task) killed the tracking
   shell and cleared `/tmp`, silently orphaning both background processes without a clean
   completion record — surfaced later as stopped-task notifications.
3. Verified each venv directly rather than trusting the interrupted logs: `agent-memory`'s sync
   had actually completed (`torch==2.13.0+cu130`, `sentence_transformers`, `psutil` all
   importable, `torch.cuda.is_available() == True`). `workspace-knowledge`'s had not — only 52 MB
   installed, `torch`/`sentence_transformers`/`rank_bm25` all still missing.
4. Relaunched `workspace-knowledge`'s `uv sync` alone, logging to the session's durable job `tmp/`
   directory this time (not `/tmp`, which had already been cleared once) so a repeat interruption
   wouldn't lose the record again. Let it run to completion (~5 GB installed).
5. Verified both venvs directly post-sync and foreground-launched `workspace-knowledge` to confirm
   a clean start on the now-complete dependency set.

**Verification:**

| Check performed                                                                        | Result                                                                                       |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `import torch, sentence_transformers, psutil, fastmcp` — `agent-memory` venv           | All OK; `torch==2.13.0+cu130`, `torch.cuda.is_available()` → `True`                          |
| `import torch, sentence_transformers, rank_bm25, fastmcp` — `workspace-knowledge` venv | All OK; `torch==2.13.0+cu130`, `torch.cuda.is_available()` → `True`                          |
| Foreground launch, `workspace-knowledge/.venv/bin/python server.py`                    | Started cleanly — FastMCP banner, `workspace-knowledge, 3.2.4`, exit code 0                  |
| Venv disk size, both servers                                                           | `agent-memory`: 4.9 GB; `workspace-knowledge`: 5.0 GB — consistent with a full CUDA/ML stack |

**Not verified:** live `search_memory`/`search_docs` retrieval quality, or `embedder-service`'s
warm-start behavior now that both venvs can support it — those require exercising the tools over
a real MCP connection with real queries, which is the next opportunistic step (Item #2's remaining
half: `manage_embedder_service.py`'s Linux/macOS path), not something this entry claims.

**Outcome:** Open Follow-Up Item #5 is closed. Both servers' venvs now hold the full declared
dependency set from their respective `pyproject.toml`/`uv.lock`, verified by direct import and one
foreground launch each — not just process-exit-code trust, given the session interruption that
made exactly that kind of unverified trust fail silently earlier in this same item's history.

**Handoff to next stage:** One item remains open on this topic: Item #3 (Linux/macOS DR-scheduling
verification for `register_backup_task.py`), explicitly kept deferred per CEO direction. This
entry does not close the topic — `maintenance-record.md`'s Status is updated alongside it to
reflect one remaining open item.
