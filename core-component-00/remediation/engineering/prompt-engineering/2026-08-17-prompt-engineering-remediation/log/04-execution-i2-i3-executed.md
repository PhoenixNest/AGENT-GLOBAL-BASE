# Log Entry 04 — Execution — 2026-08-24

Part of `core-component-00/remediation/engineering/prompt-engineering/2026-08-17-prompt-engineering-remediation/implementation-plan.md`.
Pipeline stage 3 — Execution (`core-component-00/remediation/pipeline.md`).

**Trigger:** Stage 2 Approval complete for I2 and I3 (`log/02-approval-i1-i5-approved.md`); User
instruction to execute the approved plan. Executed together because both items land in the same
file (`cot_classifier.py`) and I3's query-side signal is the mechanism that replaces I2's
misattributed routing key.

**Items covered:** I2, I3.

**Actions taken:**

1. Re-fetched the benchmark report's Source Register entries S7–S10 (arXiv:2505.11423 abstract
   and full text) as carried into the plan, confirming the paper's actual claim: evaluating 15
   models on IFEval and ComplexBench, CoT prompting consistently degrades instruction-following
   (13/14 models regress on IFEval, all models regress on ComplexBench); Llama3-8B-Instruct's
   75.2% → 59.0% drop is an Original-vs-CoT comparison on the same model, not a base-vs-fine-tuned
   comparison. The paper's proposed mitigation ("classifier-selective reasoning") keys on the
   instance (task/constraints), not model identity.
2. Rewrote the module docstring in `cot_classifier.py` to state this claim accurately, name the
   prior misattribution explicitly, and cite this remediation item for the correction (I2).
3. Removed `ModelVariant`, `FINE_TUNING_MARKERS`, and `classify_model()` — the fine-tuning-status
   routing key the docstring's misreading justified.
4. Added `TaskType` (`STRUCTURED_OUTPUT` / `HIGH_CONSTRAINT` / `GENERAL`), `STRUCTURED_OUTPUT_MARKERS`,
   `CONSTRAINT_MARKERS`, and `CoTClassifier.classify_task()` / `count_constraints()` — a
   query-content-derived signal covering both benchmarks the paper actually measures
   (IFEval-style single rule-verifiable constraints via structured-output markers;
   ComplexBench-style compositional constraints via a constraint-marker count) (I3).
5. Rewrote `should_use_cot()` to take `prompt_text` (previously `model_id`) as its primary
   argument, suppressing CoT for `STRUCTURED_OUTPUT`/`HIGH_CONSTRAINT` task types or `BRITTLE`
   stability, and updated `CoTDecision` to carry `task_type` instead of `model_variant`.
6. Updated the `__main__` block to demonstrate the decision varying across queries of different
   content against an implicit constant model — no `model_id` parameter exists any more for a
   decision to vary by.

**Verification:**

| Check performed                                                                                                                                                                         | Result                                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `python implementations/cot_classifier.py` (module's own demo)                                                                                                                          | Pass — 5 test cases print distinct ENABLED/SUPPRESSED decisions with reasons; see console output captured below |
| Grep rewritten file for `FINE_TUNING_MARKERS`                                                                                                                                           | Pass — absent                                                                                                   |
| Grep rewritten file for `ModelVariant`                                                                                                                                                  | Pass — absent                                                                                                   |
| Grep rewritten file for `model_id`                                                                                                                                                      | Pass — absent (no routing parameter left for a `-ft-` substring to affect)                                      |
| `should_use_cot()` called twice with the same implicit model, differing only in `prompt_text` ("What is the capital of France?" vs. a JSON-schema request with a "must not" constraint) | Pass — decisions differ (`True` vs. `False`), confirming output varies with query content alone                 |

Captured console output from the module's own `__main__` demo:

```
Prompt                                                       Stability      Decision
--------------------------------------------------------------------------------------------------------------
What is the capital of France?                               TIER_SENSITIVE CoT ENABLED: low-constraint task with stable prompt: CoT enabled
Return JSON: {"name": "...", "age": 0}. Name: Alice.         TIER_SENSITIVE CoT SUPPRESSED: structured_output task: CoT degrades instruction-following (arXiv:2505.11423)
You must not use analogies. You must not exceed 50 words.    TIER_SENSITIVE CoT SUPPRESSED: high_constraint task: CoT degrades instruction-following (arXiv:2505.11423)
Summarize this document in one paragraph.                    BRITTLE        CoT SUPPRESSED: BRITTLE prompt: CoT injection causes output variance
Explain quantum entanglement simply.                         STABLE         CoT ENABLED: low-constraint task with stable prompt: CoT enabled
```

**Outcome:** I2 — the docstring now states the paper's actual finding and no longer attributes a
fine-tuned-vs-base claim to it. I3 — `should_use_cot()` now varies its decision by query
task/constraint content (the axis both the benchmark row and external practice named), not by a
model-identity string, and the fine-tuning-status signal that had no supporting source (B6 in the
benchmark: "Unassessed — no source") has been removed rather than kept alongside the new signal.

**Note on scope not taken:** the plan's Approach for I3 offered two options — add a query-side
signal, or implement the paper's full trained-classifier form. This entry implements the
query-side heuristic signal (marker/constraint-count based), not a trained classifier — no
training data or model-serving path exists in this module or environment for the latter. This is
the option the Approach explicitly permits ("Add a query-side signal ... OR implement the
trained-classifier form"), stated here so the choice is visible to the Reviewer rather than
implied.

**Handoff to next stage:** Stage 4 — Verification, alongside I1, I4, I5. Owner has not marked this
`Verified` — that requires independent Reviewer sign-off.
