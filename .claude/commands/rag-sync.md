Read the file `.claude/hooks/rag-sync-state.json`. If it does not exist, treat the
current state as `{"mode": "warn", "debounce_seconds": 30, "last_rebuild_at": 0}`.

Based on the argument provided after `/rag-sync`:

- `auto` → set mode to `"auto"`, write the updated state file, confirm:
  _"RAG sync set to AUTO — index will rebuild automatically after qualifying doc writes
  (debounce: \<N\>s)."_
- `warn` → set mode to `"warn"`, write the updated state file, confirm:
  _"RAG sync set to WARN — you will be notified of stale index but no automatic rebuild."_
- `off` → set mode to `"off"`, write the updated state file, confirm:
  _"RAG sync DISABLED — no notifications or automatic rebuilds."_
- `status` → read the state file, report: current mode, debounce threshold in seconds,
  last rebuild timestamp formatted as a human-readable datetime.
- `threshold <N>` → set `debounce_seconds` to N, write the updated state file, confirm:
  _"Debounce threshold set to \<N\> seconds."_

After writing, display the full new state as a JSON block for confirmation.
