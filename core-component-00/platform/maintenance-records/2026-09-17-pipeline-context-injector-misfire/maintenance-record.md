# Maintenance Record — H-P02 Pipeline Context Injector

| Field                          | Detail                                                                                                                                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Owner**                      | Dr. Elias Vance, CC-00 Laboratory Director                                                                                                                                                        |
| **Authorized / reviewed by**   | CEO — the fix was directed under delegated authority to resolve root causes. Hook behaviour spans every pipeline in the workspace and is outside the Infrastructure Engineer's unilateral scope   |
| **System / resource affected** | `.claude/hooks/pipeline-context-injector.py`, the H-P02 `UserPromptSubmit` hook. No venv or interpreter change; the hook runs under the same `uv run` invocation as the other 18 registered hooks |
| **Severity**                   | P1 — a confirmed defect injecting incorrect governance context on every qualifying prompt. Not P0: the hook advises the model and breaks no live service                                          |
| **Status**                     | Completed — both defects fixed and verified against three observed misfires and four true positives                                                                                               |

---

## Pipeline Stage Log

| Stage                         | Entry                                                                                                                            | Summary                                                                                                                                                                                                 |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1–4 — Investigation to Verify | `core-component-00/platform/maintenance-records/2026-09-17-pipeline-context-injector-misfire/log/01-wrong-pipeline-injection.md` | Three misfires in one session traced to two defects: a regular expression missing a leading word boundary, and a bare stage number treated as unambiguous across three independently numbered pipelines |

---

## Open Follow-Up Items

| Item                                                                                                                                                                                                                                                          | Owner     | Target                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | --------------------------- |
| The hook has no test file, unlike `context-budget-alert.py` which has `test_context_budget_alert.py`. The three misfire cases and four true positives were verified by hand and are not held anywhere a regression would fail                                 | Dr. Vance | Before the next hook change |
| The remaining `STAGE_SIGNALS` patterns were not audited for the same missing-boundary defect beyond Stage 10. `PRD\b`, `SRD\b`, `IDS\b`, `UML\b`, `ADR\b` and `TSD\b` all lack a leading boundary and are lower-risk only because they are uppercase acronyms | Dr. Vance | Before the next hook change |

---

## Related Records

- `.claude/rules/scope-and-obligations.md` — the workspace rule written from the same governance review this defect was found during; that rule covers where scope statements and obligations belong, this record covers the hook
- `.claude/hooks/pipeline-context-injector.py` — the file changed
- `CLAUDE.md` § 8 — the rule against conflating stage numbers across the three pipelines, which the hook was breaching automatically
