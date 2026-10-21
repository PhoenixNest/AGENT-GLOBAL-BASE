# Maintenance Record — H-CE01 Context Budget Alert and Four Failing Hook Tests

| Field                          | Detail                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owner**                      | Kwame Asante (Senior Research Engineer, Harness Engineering)                                                                                                                                                                                                                                                                                          |
| **Authorized / reviewed by**   | Authorized by the CEO (item D: assign the four failing tests and the context-budget alert to CC-00 Harness Engineering). Reviewed by the BCU-00 orchestrator; review complete, accepted.                                                                                                                                                              |
| **System / resource affected** | `.claude/hooks/context-budget-alert.py` (H-CE01, `UserPromptSubmit`), `.claude/hooks/test_context_budget_alert.py`, `.claude/hooks/test_mcp_session_start_self_heal.py`. Python environment: the test runner's `uv run --with pytest` interpreter; the hook itself is stdlib-only. No file outside `.claude/hooks/` and no `.mcp.json` write changed. |
| **Severity**                   | P1 (confirmed defect, not broken live: the alert always fell back to byte size, and four tests failed)                                                                                                                                                                                                                                                |
| **Status**                     | Completed with follow-up open                                                                                                                                                                                                                                                                                                                         |

---

## Pipeline Stage Log

| Stage             | Entry                                                                                                                                  | Summary                                                                                                                                                                                                            |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1 — Investigation | `core-component-00/platform/maintenance-records/2026-10-19-context-budget-alert-and-hook-test-failures/log/01-root-cause-and-fixes.md` | Root causes found for all four failing tests and for the live "unparseable transcript" report; hook parser and path fixed, the self-heal test made hermetic, full hooks suite green (502 passed), review accepted. |

---

## Open Follow-Up Items

| Item                                                                                                                                                                                                          | Owner                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Alert (32,000) and enforcement (96,000) token thresholds are not checked against the target model's context window; the live session measures about 77.8k tokens, above the alert tier and below enforcement. | Kwame Asante, with Dr. Elias Vance for the threshold decision |
| `tiktoken` is not installed in the hook's environment, so the estimator uses the character/4 fallback; the skill's 1% accuracy bar against the real tokenizer is not demonstrated.                            | Kwame Asante                                                  |

---

## Related Records

- `.claude/hooks/context-budget-alert.py` — the hook
- `core-component-00/framework/02-context-engineering/implementations/context_compressor.py` — the estimator and compressor the hook imports
- `core-component-00/framework/03-harness-engineering/implementations/context_monitor.py` — the reference named in the alert text
