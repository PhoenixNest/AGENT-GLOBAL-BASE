# Implementation Plan — Context Engineering (Layer 2)

---

## Metadata

| Field                       | Value                                                                                                                                        |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Plan ID**                 | `2026-08-17-context-engineering-remediation`                                                                                                 |
| **Layer**                   | 2 — Context Engineering                                                                                                                      |
| **Source Benchmark Report** | `core-component-00/benchmarks/engineering/context-engineering/2026-08-16-context-engineering-enterprise-assessment/enterprise-assessment.md` |
| **Owner**                   | Mei-Ling Zhao (Context Engineering lead)                                                                                                     |
| **Reviewer**                | Dr. Elias Vance (independent of Owner)                                                                                                       |
| **Hook-Change Gate**        | N/A — neither item in this plan touches `.claude/hooks/*.py`                                                                                 |
| **Status**                  | Verified — see `log/04-verification-i1-i2-verified.md`                                                                                       |

---

## Included Items

| ID  | Source Row | Gap (restated, one line)                                                                                | Severity (inherited) | Item Owner    | Approach                                                                                                                                                                                               | Acceptance Criteria                                                                                                          | Test Plan                                                                                                 | Target Date | Item Status                                            |
| --- | ---------- | ------------------------------------------------------------------------------------------------------- | -------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------ |
| I1  | Context R2 | No utilization-based compaction trigger anywhere in the module                                          | P1                   | Mei-Ling Zhao | Add an explicit utilization trigger to `ContextCompressor` (default ~70-75%, configurable), separate from `SAFETY_BUFFER`; document in `fundamentals/context-window-anatomy.md`                        | Compressor fires automatically once configured utilization threshold is crossed in a test session                            | New test asserting trigger fires at threshold; `pytest engineering/context-engineering/testing/ -v` green | 2026-08-24  | Verified — see `log/04-verification-i1-i2-verified.md` |
| I2  | Context R3 | No compression-ratio or fidelity metric is asserted; the one benchmark test is red on a metric mismatch | P1                   | Mei-Ling Zhao | Define one contractual token-accounting basis, align `test_acon_benchmark.py` and `compress_history()` to it, assert a ratio floor and decision-continuity floor against the fixed long-session corpus | `test_acon_benchmark.py` passes against the agreed accounting basis; ratio/continuity floors are asserted, not just measured | `pytest engineering/context-engineering/testing/ -v` fully green, including the previously-red test       | 2026-08-24  | Verified — see `log/04-verification-i1-i2-verified.md` |

**Relocation note.** Context R1 (budget enforcement — no consolidation/compression code path when
the hook fires) is **not** in this plan. Its fix lands in `.claude/hooks/context-budget-alert.py`,
which is Harness-owned infrastructure — it is tracked as item I5 in the Harness Engineering
Implementation Plan instead. See Cross-Layer Dependencies below.

---

## Cross-Layer Dependencies

| This Item  | Related Item                            | Relationship                                                                                                                                                                                                                                                                                                                                                                             | Arbitrated By          |
| ---------- | --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| (external) | Harness plan I5 (originally Context R1) | **Owned elsewhere.** This gap was originally identified in the Context Engineering benchmark report, but its fix requires harness-owned hook code — see the Harness Engineering Implementation Plan, item I5, and its arbitration entry against I4 (Harness R4). This plan does not track its execution; it is listed here only so a reader following this plan doesn't lose the thread. | N/A — see Harness plan |

---

## Gate Log

| Stage            | Entry                                                                                                                                            | Summary                                                                                                                                                                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0 — Trigger      | `core-component-00/remediation/engineering/context-engineering/2026-08-17-context-engineering-remediation/log/01-drafting-i1-i2-opened.md`       | Topic opened from the signed-off Context benchmark's 2 in-scope P1 rows (R1 relocated to Harness)                                                                                                                                              |
| 2 — Approval     | `core-component-00/remediation/engineering/context-engineering/2026-08-17-context-engineering-remediation/log/02-approval-i1-i2-approved.md`     | Dr. Vance signed off as Reviewer on I1 and I2's Approach; no hook dependency, cleared to Execution once Zhao begins                                                                                                                            |
| 3 — Execution    | `core-component-00/remediation/engineering/context-engineering/2026-08-17-context-engineering-remediation/log/03-execution-i1-i2-executed.md`    | I1 (utilization trigger) and I2 (token-accounting basis + ratio/continuity floors, plus a discovered sacred-turn indexing bugfix) implemented; full suite green (341 passed, 1 skipped), including the previously-red `test_acon_benchmark.py` |
| 4 — Verification | `core-component-00/remediation/engineering/context-engineering/2026-08-17-context-engineering-remediation/log/04-verification-i1-i2-verified.md` | Dr. Vance independently re-read both diffs and re-ran the suite himself (341 passed, 1 skipped); both items confirmed; `Status: Verified`                                                                                                      |

---

## Open Follow-Up Items

[None]

---

## Related Records

- **Source benchmark report:** `core-component-00/benchmarks/engineering/context-engineering/2026-08-16-context-engineering-enterprise-assessment/enterprise-assessment.md`
- **R1's tracked location:** `core-component-00/remediation/engineering/harness-engineering/2026-08-17-harness-engineering-remediation/implementation-plan.md` (item I5)
- **Backlog items for this layer:** `core-component-00/remediation/README.md` § Remediation Backlog (Context R4–R7)
