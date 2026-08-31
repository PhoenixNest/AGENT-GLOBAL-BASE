# Implementation Plan — Prompt Engineering (Layer 1)

---

## Metadata

| Field                       | Value                                                                                                                                                          |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Plan ID**                 | `2026-08-17-prompt-engineering-remediation`                                                                                                                    |
| **Layer**                   | 1 — Prompt Engineering                                                                                                                                         |
| **Source Benchmark Report** | `core-component-00/platform/benchmarks/engineering/prompt-engineering/2026-08-16-prompt-engineering-enterprise-assessment/enterprise-assessment.md`                     |
| **Owner**                   | Dr. Elias Vance (module retained directly — Prompt Engineering has no dedicated crew lead)                                                                     |
| **Reviewer**                | Dr. Tomasz Wieczorek (independent — Vance owns most items in this plan and cannot review his own work, same reason he did not review his own benchmark report) |
| **Hook-Change Gate**        | N/A — no item in this plan touches `.claude/hooks/*.py`                                                                                                        |
| **Status**                  | Verified — see `log/06-verification-i4-verified.md` (I4) and `log/07-verification-i1-i2-i3-i5-verified.md` (I1, I2, I3, I5)                                    |

**Per-item reviewer note.** Wieczorek reviews the plan overall, but cannot review his own item
(I4) under the Owner-≠-Reviewer rule — Dr. Vance verifies I4 specifically at pipeline stage 4,
even though he is the plan's Owner for the other four items.

---

## Included Items

| ID  | Source Row | Gap (restated, one line)                                                                                         | Severity (inherited) | Item Owner           | Approach                                                                                                                                                                                                                                                                                          | Acceptance Criteria                                                                                                                       | Test Plan                                                                                               | Target Date | Item Status                                                  |
| --- | ---------- | ---------------------------------------------------------------------------------------------------------------- | -------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------ |
| I1  | Prompt R1  | Eval harness grades an md5 hash — its stability classification carries no model signal                           | P1                   | Dr. Elias Vance      | Wire a real client behind the existing `client` injection point and re-derive classification from actual model outputs, or delete the classification path and keep the file as an unexecuted benchmark-set definition                                                                             | Classifier output changes only in response to actual model output changes, never prompt-text hashing alone                                | New test with two distinct mocked model outputs producing two distinct classifications                  | TBD         | Verified — see `log/07-verification-i1-i2-i3-i5-verified.md` |
| I2  | Prompt R2  | CoT classifier attributes to arXiv:2505.11423 a fine-tuned-vs-base finding the paper doesn't make                | P1                   | Dr. Elias Vance      | Correct the docstring to the paper's actual claim (CoT degrades instruction-following on IFEval/ComplexBench across 15 general models); re-derive the routing key from task/constraint type, not fine-tuning status                                                                               | Docstring citation matches a verbatim excerpt from the paper; routing key no longer keys off `-ft-` in a model ID                         | Unit test asserting routing key is unaffected by a `-ft-` substring in the model identifier             | TBD         | Verified — see `log/07-verification-i1-i2-i3-i5-verified.md` |
| I3  | Prompt R3  | Conditional CoT implemented on neither axis (query difficulty/cost, trained classifier) external practice uses   | P1                   | Dr. Elias Vance      | Add a query-side signal (task type, constraint density, or effort budget) to `should_use_cot`; implement the trained-classifier form or rename the module to stop claiming a technique it doesn't implement                                                                                       | `should_use_cot` output varies across two queries to the same model differing only in query content                                       | New test with two same-model, different-query cases yielding different `should_use_cot` results         | TBD         | Verified — see `log/07-verification-i1-i2-i3-i5-verified.md` |
| I4  | Prompt R4  | Module advertises "prompt robustness — handling adversarial inputs"; no injection-defense guidance exists        | P1                   | Dr. Tomasz Wieczorek | Author a prompt-injection section in `fundamentals/research.md` covering provenance tracking, structural separation of untrusted content, capability scoping, deterministic policy enforced outside the model, egress constraint; state plainly that system-prompt instructions are not a control | Section exists, cites the same external sources as the benchmark finding, and explicitly states the system-prompt-is-not-a-control caveat | Doc-only — reviewed by Dr. Vance for excerpt-to-claim accuracy per the Owner-≠-Reviewer exception above | TBD         | Verified — see `log/06-verification-i4-verified.md`          |
| I5  | Prompt R5  | Structured-output guidance stops at prompt-level instruction; doesn't cover provider-native constrained decoding | P1                   | Dr. Elias Vance      | Extend `research.md` § 3.4 to lead with constrained decoding as the primary mechanism, demote prompt-level schema instruction to fallback; add a catalog entry discoverable from `patterns/advanced-patterns.md`                                                                                  | Section reordered; new catalog entry exists and links correctly                                                                           | Doc-only — reviewed by Wieczorek for excerpt-to-claim accuracy                                          | TBD         | Verified — see `log/07-verification-i1-i2-i3-i5-verified.md` |

---

## Cross-Layer Dependencies

[None identified]

---

## Gate Log

| Stage            | Entry                                                                                                                                                | Summary                                                                                                                                                                                                               |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0 — Trigger      | `core-component-00/platform/remediation/engineering/prompt-engineering/2026-08-17-prompt-engineering-remediation/log/01-drafting-i1-i5-opened.md`             | Topic opened from the signed-off Prompt benchmark's 5 in-scope P1 rows                                                                                                                                                |
| 2 — Approval     | `core-component-00/platform/remediation/engineering/prompt-engineering/2026-08-17-prompt-engineering-remediation/log/02-approval-i1-i5-approved.md`           | Wieczorek signed off on I1/I2/I3/I5; Vance signed off on I4 per the per-item reviewer exception                                                                                                                       |
| 3 — Execution    | `core-component-00/platform/remediation/engineering/prompt-engineering/2026-08-17-prompt-engineering-remediation/log/03-execution-i1-executed.md`             | I1: fake md5-hash classification path removed from `prompt_eval_harness.py`; file kept as unexecuted benchmark-set definition (plan's stated fallback, taken because no live model access exists in this environment) |
| 3 — Execution    | `core-component-00/platform/remediation/engineering/prompt-engineering/2026-08-17-prompt-engineering-remediation/log/04-execution-i2-i3-executed.md`          | I2+I3: `cot_classifier.py` docstring corrected to the paper's actual claim; fine-tuning-status routing key removed and replaced with a query-content-derived task/constraint signal                                   |
| 3 — Execution    | `core-component-00/platform/remediation/engineering/prompt-engineering/2026-08-17-prompt-engineering-remediation/log/05-execution-i4-i5-executed.md`          | I4+I5: new § 3.7 prompt-injection-defense section and reordered § 3.4 (constrained decoding primary, prompt instruction fallback) added to `research.md`; new P-015 catalog entry added to `advanced-patterns.md`     |
| 4 — Verification | `core-component-00/platform/remediation/engineering/prompt-engineering/2026-08-17-prompt-engineering-remediation/log/06-verification-i4-verified.md`          | Dr. Vance independently verified I4 only, per the plan's per-item reviewer exception; word-for-word cross-check against benchmark row R4's Fix column confirmed                                                       |
| 4 — Verification | `core-component-00/platform/remediation/engineering/prompt-engineering/2026-08-17-prompt-engineering-remediation/log/07-verification-i1-i2-i3-i5-verified.md` | Dr. Wieczorek independently re-read all four diffs, re-fetched arXiv:2505.11423 himself, and re-ran both scripts himself; I1/I2/I3/I5 confirmed. Plan `Status: Verified` — all 5 items complete                       |

---

## Open Follow-Up Items

[None]

---

## Related Records

- **Source benchmark report:** `core-component-00/platform/benchmarks/engineering/prompt-engineering/2026-08-16-prompt-engineering-enterprise-assessment/enterprise-assessment.md`
- **Backlog items for this layer:** `core-component-00/platform/remediation/README.md` § Remediation Backlog (Prompt R6–R8)
