# Log Entry 01 — Investigation and Restore — 2026-10-12

| Field            | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-10-12-shared-embedding-model-cache-loss/maintenance-record.md`, pipeline stages 1 — Investigation, 2 — Approval, 3 — Execution (`core-component-00/platform/maintenance-records/pipeline.md`)                                                                                                                                                                                                                                                                                                                                |
| **Trigger**      | CEO assignment on 2026-10-12: coordinate remediation of a fault in the memory system. The CEO approved restoring the missing model files and approved a re-test afterwards. Symptoms and the initial fact base were established by the lead orchestrator and handed to the Laboratory Director                                                                                                                                                                                                                                                                                    |
| **State before** | `_shared/models/` held two slug folders, `sentence-transformers--all-MiniLM-L6-v2` and `sentence-transformers--all-mpnet-base-v2`, each containing one empty `1_Pooling` subfolder and no files. `embedder-service` not running, nothing listening on `127.0.0.1:8791`. `agent-memory` connected but degraded: `search_memory` on the tier 3 keyword path, `write_memory` rejecting every write. `workspace-knowledge` failed to reconnect (30 s connection timeout). `agent-memory` server process PID 34588 running since 2026-10-12 00:18:23 with a failed in-process embedder |

## Symptom

- `agent-memory` `health_check` reported `embedder_service_state: unavailable`. Its in-process
  fallback reported `loading` for hours, then
  `failed: Unrecognized model in ...all-MiniLM-L6-v2. Should have a model_type key in its config.json`.
- `search_memory` ran degraded and returned reflection records for the unrelated query "recipe
  for chocolate cake".
- `write_memory` rejected every write with "cannot embed content for collision search or write".
- `memory_reflection` holds 4 records; the other three collections hold 0.
- `workspace-knowledge` `health_check` reported `search_tier: hybrid_qdrant` with no degradation
  reason while its model slug folder was equally empty. This was not confirmed with a live
  search. The server later failed to reconnect; the cause of that failure is not established.

## Findings

Items 1–3 were verified by the lead orchestrator before handoff. Items 4–9 were verified by the
Laboratory Director during this entry, by reading the code and inspecting the machine.

1. Both slug folders under `_shared/models/` were empty apart from an empty `1_Pooling`
   subfolder. The directory is ignored by `_shared/.gitignore` (line 3, `models/`).
2. Complete copies of both models exist in the user's Hugging Face cache
   (`%USERPROFILE%\.cache\huggingface\hub\models--sentence-transformers--all-MiniLM-L6-v2`,
   29 files, 87.3 MB; `...--all-mpnet-base-v2`, 29 files, 418.4 MB).
3. The lead orchestrator observed the launch lock naming PID 23928, a process that does not
   exist.
4. **No model file was ever tracked.** `git log --all` over the models path returns no commit on
   any ref, so the files were never under version control on any branch.
5. **The loss is dated.** The lead orchestrator recorded the slug folders' last-write time as
   2026-08-31 23:51 (local, UTC−07:00). The slug folders' creation time is 2026-07-19 20:48,
   so they were populated before that date and emptied at 23:51 on 2026-08-31.
6. **That minute falls inside a burst of git operations.** The reflog shows, on 2026-08-31
   between 23:44 and 23:58, more than twenty branch checkouts and merges, and three `git reset`
   operations on `anu00/dev/thinking` at 23:49:22, 23:49:39 and 23:50:16, with the next entry at
   23:54:07. A sibling directory `core-component-00/engineering` was created at 23:50:33. The
   branches involved straddled commit `b019714f` (2026-08-31 07:16), which moved the MCP servers
   under `platform/`.
7. **The idempotency guard in `provision_model.py` is defeated by an empty skeleton.** The
   script skips a model when `dest.exists() and any(dest.iterdir())`. An empty `1_Pooling`
   subfolder satisfies that test, so the script reported both models as cached at 0.0 MB and did
   nothing.
8. **A stale launch lock does not block a relaunch.** `embedder_client._acquire_lock()` treats
   a lock older than `LOCK_STALE_AFTER_S` (60 s) as stale, unlinks it and retries. Staleness is
   judged by file age alone; the PID written into the lock is never read.
9. **The lock changed after the handoff.** At inspection the lock file held PID 16912, with a
   last-write time of 2026-10-12 00:27:16. Neither PID 16912 nor PID 23928 is running.
   `ensure_service_running()` releases the lock in a `finally` block, so a lock left behind
   means the launcher process was terminated during its wait of up to 90 s.

## Root Cause

The provisioned embedding-model files were missing from the shared cache. With no model to load,
`embedder-service` cannot serve, and the `agent-memory` in-process fallback fails on the same
empty folder.

The mechanism of the loss is **unconfirmed**. The CEO's hypothesis is that the files were removed
during branch switching. Findings 5 and 6 support it by timing: the loss coincides to the minute
with a sequence of checkouts, merges and resets across branches on either side of the directory
reorganization. Finding 4 limits it: the files were untracked and ignored, and git does not
normally delete such files on checkout or reset. The timing establishes correlation, not the
operation responsible. A `git clean`, a script, or a tool acting in the same window would leave
the same evidence and would not appear in the reflog.

By the folder timestamps the cache has been empty on this machine since 2026-08-31. How the
memory system behaved between that date and 2026-10-12 was not examined.

## Approval

The CEO approved restoring the missing files and approved re-testing afterwards. No code, hook,
rule or configuration change is approved; those are listed in the main record as proposals.

**Actions taken:**

1. Ran the provisioning script for both models with the `agent-memory` venv interpreter:

   ```powershell
   $r = 'core-component-00\platform\model-context-protocol-servers'
   & "$r\agent-memory\.venv\Scripts\python.exe" "$r\_shared\provision_model.py" sentence-transformers/all-MiniLM-L6-v2
   & "$r\agent-memory\.venv\Scripts\python.exe" "$r\_shared\provision_model.py" sentence-transformers/all-mpnet-base-v2
   ```

   Result: exit code 0 for both, output `Already cached: ... (0.0 MB) — no-op`. Nothing was
   restored (finding 7).

2. Removed the two empty `1_Pooling` subfolders so the script's guard would no longer treat the
   slug folders as populated. Each was confirmed to hold zero entries immediately beforehand,
   and removed with a non-recursive delete that fails on a non-empty directory:

   ```powershell
   [System.IO.Directory]::Delete("$m\sentence-transformers--all-MiniLM-L6-v2\1_Pooling", $false)
   [System.IO.Directory]::Delete("$m\sentence-transformers--all-mpnet-base-v2\1_Pooling", $false)
   ```

   This step was not in the handed-down instruction. It deleted no file and copied none; it was
   the smallest change that let the approved script perform the approved restore. It also
   discarded those two subfolders' own timestamps. The slug folders' creation times survive.

3. Re-ran the same two commands from action 1.
   - `all-MiniLM-L6-v2`: exit code 0, `Saved 87.3 MB ... (embedding dim: 384)`, 43.7 s.
   - `all-mpnet-base-v2`: exit code 0, `Saved 418.4 MB ... (embedding dim: 768)`, 40.7 s.

   Both loaded from the local Hugging Face cache. The script contacted the Hub for metadata
   (it printed an unauthenticated-request warning), but the weight blobs in the Hugging Face
   cache keep their original dates (2026-07-12 and 2026-06-24) and no download progress was
   reported.

4. Left `embedder-service.lock` in place. It is more than 60 s old, so the next consumer to
   call `ensure_service_running()` clears it without help (finding 8). PID 16912 is confirmed
   not running.

5. Changed no code, hook, rule or configuration. Wrote no reflection record to the memory
   store; that path requires live human confirmation, and one is owed once the system is
   verified healthy.

**Verification:**

| Check performed                                                                                                                                       | Result                                                                                                                                                                                                                                   |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| File inventory of `_shared/models/sentence-transformers--all-MiniLM-L6-v2`                                                                            | Pass — 10 files, 87.3 MB: top-level `config.json`, `model.safetensors` (90,864,192 bytes), `tokenizer.json`, `tokenizer_config.json`, `modules.json`, plus `1_Pooling/config.json` and `2_Normalize/config.json`                         |
| File inventory of `_shared/models/sentence-transformers--all-mpnet-base-v2`                                                                           | Pass — 10 files, 418.4 MB: top-level `config.json`, `model.safetensors` (437,967,672 bytes), `tokenizer.json`, `tokenizer_config.json`, `modules.json`, plus `1_Pooling/config.json` and `2_Normalize/config.json`                       |
| Offline load and encode of each slug folder with `HF_HUB_OFFLINE=1`, `agent-memory` venv interpreter, `SentenceTransformer(<slug dir>).encode([...])` | Pass — `all-MiniLM-L6-v2`: `model_type=bert`, output shape `(1, 384)`, device `cuda:0`. `all-mpnet-base-v2`: `model_type=mpnet`, output shape `(1, 768)`, device `cuda:0`. The `model_type` key the fallback reported missing is present |
| `git status --short` after the restore                                                                                                                | Pass — no tracked change from the restore; the models directory remains ignored                                                                                                                                                          |
| Nothing listening on `127.0.0.1:8791`                                                                                                                 | Unchanged — `embedder-service` is still down. No consumer has attempted a launch since the restore                                                                                                                                       |
| `agent-memory` `health_check`, `search_memory`, `write_memory` through the MCP tools                                                                  | **Not run** — pending an MCP server restart                                                                                                                                                                                              |
| `workspace-knowledge` reconnect, `health_check`, and a live search                                                                                    | **Not run** — the server is not connected in this session                                                                                                                                                                                |

Independent-review gate: this topic is P0 and touches a resource both registered MCP servers
depend on. The executor's checks above do not satisfy the gate. The lead orchestrator's re-test
through the MCP tools after a server restart is the review that does; Dr. Tomasz Wieczorek is
named as reviewer of record for the result.

| Field                     | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Outcome**               | Both models are restored to the shared cache and load correctly from disk. The memory system itself is **not yet confirmed restored**: the running `agent-memory` process still holds a failed embedder, `embedder-service` is down, and `workspace-knowledge` is disconnected. The mechanism that emptied the cache is unconfirmed, so a recurrence is possible on the next comparable git session                                                                      |
| **Handoff to next stage** | Stage 4 — Verification. Restart the MCP servers, then re-test `agent-memory` (`health_check` non-degraded, `search_memory` returning nothing for an unrelated query, `write_memory` accepting a write) and `workspace-knowledge` (reconnect, `health_check`, one live search). If `workspace-knowledge` still fails to reconnect with the models present, that is a separate cause and routes to the Reopen edge. Open items are in this topic's `maintenance-record.md` |
