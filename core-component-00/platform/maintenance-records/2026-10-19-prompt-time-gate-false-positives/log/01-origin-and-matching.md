# Log Entry 01 — Origin Detection and Whole-Word Matching — 2026-10-19

| Field            | Detail                                                                                                                                                                                                                                                                                                                                                                                                           |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Part of**      | `core-component-00/platform/maintenance-records/2026-10-19-prompt-time-gate-false-positives/maintenance-record.md`, pipeline stages 1–4 (`core-component-00/platform/maintenance-records/pipeline.md`)                                                                                                                                                                                                           |
| **Trigger**      | The CEO approved the remediation proposed for the ASGF governance framework: the rules are right, how they are checked needs fixing. Three misfires were observed: H-P03 blocked a background-agent report, H-P02 injected "Stage 8 — Integrity + Security" on a task notification, and H-P01 asked for a prompt confirmation on a task notification                                                             |
| **State before** | All three `UserPromptSubmit` hooks scanned every prompt. H-P03 ran case-insensitive, unbounded-window regexes over the whole text, so `(change...).{0,40}(P1)` matched "p1" inside "mchlp1168" in a URL; its only outcome was block. H-P02 fired a stage hint on any stage keyword. H-P01 had no notice handling. No test file existed for H-P01, H-P02 or H-P03. Each log row held a decision and a reason only |

## 1. Investigation

**What the hook receives for a notice.** The session transcript for the observing session was searched for `SYSTEM NOTIFICATION` and `task-notification`. A background-task notice reaches the model as a message that begins, after an optional `<system-reminder>` wrapper, with `[SYSTEM NOTIFICATION - NOT USER INPUT]`, followed by a `<task-notification>` element holding `task-id`, `status`, `summary` and `result`. The transcript records the model-side message; it does not record the hook's stdin payload, and the payload carries no origin field, so origin is read from the text. The detector therefore anchors to the start of the prompt (after whitespace and one optional `<system-reminder>` wrapper) and also treats a start of `<task-notification>`, `<local-command-caveat>` or `<command-name>` as system-generated. A marker later in a prompt does not change its origin.

**Root causes.**

| Cause                        | Effect                                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Every prompt is scanned      | Agent reports and automatic notices were checked as if the user had written them                             |
| Substring regex, no boundary | "p1" matched inside an identifier in a URL                                                                   |
| Whole text, wide windows     | Matches crossed sentences and landed inside URLs, code and quotations                                        |
| One outcome                  | A negated or descriptive mention ("never downgrade a P1") blocked exactly like an instruction                |
| H-P02 had no scope test      | BCU-00 and CC-00 prompts mentioning security, review or an implementation plan received a Company stage hint |

**Design decision.** The three hooks already share `_hook_log.py`, which `uv run` makes importable because the script directory is on the module path. Origin detection and prose extraction were added as one sibling module, `_prompt_origin.py`, so the detector exists once. A second per-hook copy would drift.

## 2. Execution

1. Added `.claude/hooks/_prompt_origin.py`: `prompt_origin()` (user or notice) and `strip_non_prose()` (removes fenced code, `>` quote lines, inline code and URLs).
2. `prompt-quality-gate.py` (H-P03): notices pass unscanned. Matching runs on prose only, one sentence at a time (a sentence ends at `.`, `!`, `?`, `;` or a newline), every term a whole word, P0 and P1 matched in capitals. Each rule is a verb phrase followed by an object within the original window. Strong tier: the verb phrase opens its clause, after optional lead-ins ("please", "let's", "you should", "git"), with no negation in the clause; the prompt blocks with the unchanged message text. Weak tier: co-occurrence without that shape, a negated clause, or a generic object (`critical` as the severity object, `check` as the trim-to-pass tail); the hook emits an `additionalContext` warning naming the rule and does not block. The five rules keep their intent and message text.
3. `pipeline-context-injector.py` (H-P02): notices get no hint. A stage hint requires a Company pipeline reference: a Company path or pipeline name, or an explicit "Stage N" together with a Company or Studio term. A prompt that names BCU-00, CC-00, a lab path, the workbench or hooks needs the path or pipeline name itself. Recruitment and Studio subjects keep their existing suppression. Stage keywords are matched on prose only. `PRD`, `SRD`, `IDS`, `UML`, `ADR`, `TSD` and `RTL` gained a leading word boundary.
4. `prompt-optimizer.py` (H-P01): notices pass through with an outcome logged; scoring and the confirmation flow are unchanged.
5. Audit rows: each hook's existing row now carries `extra` with origin, tier, rule id and matched keywords (each capped at 30 characters). The prompt text is never written.
6. Added `test_prompt_quality_gate.py`, `test_pipeline_context_injector.py` and `test_prompt_optimizer.py`.

## 3. Verification

| Check performed                                                                                                                                                 | Result                                                                                                                        |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `uv run --with pytest pytest` on the three new test files                                                                                                       | 98 passed                                                                                                                     |
| The same command on `.claude/hooks` as a whole                                                                                                                  | 431 passed, 4 failed — the 4 failures are in `test_context_budget_alert.py` (3) and `test_mcp_session_start_self_heal.py` (1) |
| The 4 failing tests run against an export of the unmodified hooks folder at `HEAD`                                                                              | The same 4 fail there; none of those tests touches the changed files                                                          |
| Observed false positives replayed: URL in a notice; task notification against H-P02 and H-P01; BCU-00 and CC-00 prompts mentioning security and review          | All pass through with no block, hint or confirmation                                                                          |
| Genuine violations replayed: downgrade a P1, skip the review stage, ignore the P0, force push to master, remove the security check to pass review, auto-advance | All block with the original message text                                                                                      |
| Negated, quoted, inline-code, fenced-code and URL variants                                                                                                      | None block; negated forms warn                                                                                                |
| Log rows read back after each hook ran, with a sentinel string in the prompt                                                                                    | The sentinel is absent from every row                                                                                         |

**Independent review (stage 4 gate):** a change to governance enforcement requires review by someone other than the executor. Reviewer: Dr. Noor Haddad (BCU-00). Review status: **pending**.

| Field                     | Detail                                                                                                                 |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Outcome**               | The fixes are in place and verified by the new suites. The topic is not closed: the independent review is open         |
| **Handoff to next stage** | Stage 4 independent review by Dr. Haddad, then Close. Open follow-up items are in this topic's `maintenance-record.md` |
