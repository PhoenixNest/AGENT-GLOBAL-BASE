# Log Entry 01 — Root Cause and Fixes — 2026-10-19

| Field            | Detail                                                                                                                                                                                                                                                                                                                                                                                                   |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-10-19-context-budget-alert-and-hook-test-failures/maintenance-record.md`, pipeline stage 1 — Investigation (`core-component-00/platform/maintenance-records/pipeline.md`)                                                                                                                                                                           |
| **Trigger**      | CEO decision, item D: "Assign the four failing tests and the context-budget alert to CC-00 Harness Engineering." Four hook tests failed on the unmodified hooks folder, and the live H-CE01 alert reported a ~21000 KB transcript as an unparseable byte-size fallback on every prompt.                                                                                                                  |
| **State before** | Failing: `test_context_budget_alert.py` (`test_between_alert_and_enforcement_alerts_without_compacting`, `test_over_enforcement_threshold_actually_compacts`, `test_large_non_text_metadata_does_not_trigger_token_based_alert`) and `test_mcp_session_start_self_heal.py::test_fresh_clone_single_session_start_pass_ends_with_corrected_mcp_json`. The live transcript was about 21 MB and 5201 lines. |

**Actions taken:**

1. Root cause of the three budget-alert failures, a hook defect: `_context_engineering_root()` resolved to `core-component-00/engineering/context-engineering`, which does not exist. The compressor import always raised, the token count stayed unset, and every run used the byte-size fallback. The path now resolves to `core-component-00/framework/02-context-engineering`.
2. Root cause of the live "unparseable transcript" report: the same stale path. The real transcript parses. Its conversation lines are top-level `user` and `assistant` records; the rest is metadata and request-snapshot records (`api-request`, `api-request-blob`, about 9 MB of 21 MB). The parser now counts only `user`/`assistant` lines (text, `tool_use` name and arguments, `tool_result` text), skips snapshot lines before decoding, discards turns before a `compact_boundary` record, and scans the whole file, because the previous 5000-line cap cut off the live tail of a 5201-line transcript. The fallback label reads "token estimator unavailable" when turns exist and "unparseable transcript" only when none do. Counts-only check of the real transcript: 195 turns, about 77.8k tokens, 0.11 s; no content was printed.
3. Root cause of the self-heal failure, an environment dependency in the test: it placed a shell-script `uv` stub on PATH, which Windows process creation does not resolve, so the hook ran the machine's real `uv sync` and created a real `.venv\Scripts\python.exe`. The test now places a `sitecustomize.py` on the hook subprocess's PYTHONPATH that fakes `uv sync` and `uv run`; hooks and assertions are unchanged.
4. Added `TestRealTranscriptStructure` (4 synthetic tests, no real content): token measure used for a real-shaped transcript, snapshot lines ignored, turns after line 5000 counted, `compact_boundary` reset.
5. Rewrote the hook's header and inline comments to state current behaviour only.
6. No change to any file written outside `.claude/hooks/.state`, and none to `.mcp.json` handling.

**Verification:**

| Check performed                                                              | Result                                |
| ---------------------------------------------------------------------------- | ------------------------------------- |
| `pytest .claude/hooks/test_context_budget_alert.py -q`                       | 9 passed                              |
| `uv run --with pytest python -m pytest .claude/hooks -q` (worktree root)     | 502 passed in 381.04s, zero failures  |
| Orchestrator re-run of the two repaired test files; assertion lines compared | 11 passed; no assertion lines removed |

Independent review: the BCU-00 orchestrator re-ran the decisive check and accepted the work.

| Field                     | Detail                                                                                                                                                         |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Outcome**               | All four tests pass and H-CE01 uses the token measure on a real transcript. Two follow-up items remain open (threshold calibration, `tiktoken` not installed). |
| **Handoff to next stage** | Close. Remaining work is listed in this topic's `maintenance-record.md` Open Follow-Up Items.                                                                  |
