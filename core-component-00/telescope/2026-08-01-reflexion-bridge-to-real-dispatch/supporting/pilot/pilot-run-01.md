# Supporting Document — Pilot Run 01 (Real Data)

**Programme:** `2026-08-01-reflexion-bridge-to-real-dispatch`
**Purpose:** The first real, end-to-end record of Phase 4 (`implementation-plan.md`) — a real
worktree-isolated Executor dispatch, real evidence extraction, and a real invocation of
`reflective_dispatch_helper.py` — on the already-selected pilot domain (single-module backend
test-verification subtasks). Not a simulation and not a unit test: every step below happened for
real in this session.

---

## 1. Task Dispatched

**Domain:** Single-module backend test-verification subtask (multi-agent-engineering), per the
parent Programme's `05-benchmarking-methodology.md` pilot-category selection — no new
domain-selection decision made here.

**Concrete task:** Add unit tests to
`core-component-00/engineering/multi-agent-engineering/testing/test_swarm_orchestrator.py`
covering `evaluate_subtask_result()`'s narrative-fallback path against realistic,
transcript-shaped `result["output"]` text — closing part of Open Question 2 (both this
Programme's and the parent Programme's `research-report.md`: "new unit tests needed against
realistic (not synthetic) transcript shapes"). Chosen because it is real, useful, already-logged
work — not manufactured busywork for the pilot's sake.

**Roles (per `usage-cookbook.md` § 5.1):**

- **Executor:** a real worker subagent (`cc00-implementation-assistant`), dispatched via the Agent
  tool inside its own git worktree (`agent-ae3161b7be2e44c2d`, branch
  `worktree-agent-ae3161b7be2e44c2d`)
- **Supervisor:** this session, acting as `multi-agent-orchestrator`
- **Evaluator:** `reflective_dispatch_helper.py`, invoked for real via `uv run`

---

## 2. Execute (Real)

The Executor's worktree had been provisioned from `master`, which predates the reflexion loop
(`core00/dev/engineering` commit `a0fbd435`) — it merged that branch into its own worktree branch
first (commit `80494757`) to bring in the target code, then did the test-only work on top. It
added 5 new test functions to `TestEvaluateSubtaskResult` and committed as `82b22e51`
(`agent/pilot-executor-01: add realistic-transcript tests for evaluate_subtask_result narrative
fallback`, hyphen-bulleted body listing all five scenarios — commit format verified compliant).

---

## 3. Evidence Extraction (Real, Independently Re-Verified — Not the Executor's Narrative)

Per `usage-cookbook.md` § 2.2 and Dr. Wieczorek's binding Phase 3 requirement, the Supervisor does
not trust the Executor's own report — every claim below was independently re-checked from inside
the worktree before being used as `checks` evidence:

| Executor's claim                             | Independent re-verification                                                                                                                       | Result                                             |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| "5 new test functions added"                 | `grep -c "^\s*def test_"` on `test_swarm_orchestrator.py` before dispatch (26) vs. in the worktree after (31)                                     | Confirmed — +5                                     |
| "89 passed, full suite green"                | Re-ran `pytest engineering/multi-agent-engineering/testing/ -v` directly inside the worktree, independently of the Executor's own reported output | Confirmed — 89 passed, exit code 0                 |
| "Committed with the required message format" | `git log -1 --format="%B"` inside the worktree                                                                                                    | Confirmed — subject + hyphen-bulleted body present |

`checks` supplied to the Evaluator (structured, not narrative):

```json
{
  "New tests added covering realistic narrative-shaped result dicts": true,
  "Full multi-agent-engineering test suite passes": true
}
```

---

## 4. Evaluate (Real)

Real invocation, from the main workspace (not the worktree — the helper's own path resolution is
worktree-independent by design):

```
uv run core-component-00/engineering/multi-agent-engineering/implementations/reflective_dispatch_helper.py
```

**Response (real, attempt 1):**

```json
{
  "passed": true,
  "rationale": "All gate_criteria satisfied: New tests added covering realistic narrative-shaped result dicts; Full multi-agent-engineering test suite passes",
  "reflection_note": null,
  "retries_remaining": 1
}
```

**Outcome:** Passed on attempt 1. No Reflect/retry cycle was exercised in this run — the real
attempts-to-pass value for this first pilot subtask is **1**.

**Telemetry (real, `supporting/pilot/telemetry/invocations.jsonl`):**

```json
{
  "timestamp": "2026-08-03T07:19:12.933203+00:00",
  "passed": true,
  "retries_remaining": 1,
  "degraded": false
}
```

One real record, matching one real invocation — the invocation-counter telemetry (Phase 4 § 2)
worked correctly on its first real use.

---

## 5. A Real Finding the Pilot Surfaced

The Executor's new tests — deliberately written against realistic, not synthetic, transcript text
— found two genuine, previously-undetected behaviors in `evaluate_subtask_result()`'s
narrative-fallback path (`_criterion_satisfied()`, `swarm_orchestrator.py`), unmodified by this
pilot (test-only work, per the Executor's own scope constraint):

1. **False negative:** a realistic pytest summary that genuinely satisfies a criterion
   ("50 passed, 0 failed") scores `passed=False` if the criterion text never appears as a literal
   substring — the fallback has no paraphrase handling.
2. **False positive (more serious):** a narrative that explicitly _denies_ a criterion — e.g. "It
   would be incorrect to say the tests pass — three are failing" — still scores `passed=True`,
   because the denied clause happens to contain the criterion text as a contiguous substring and
   the fallback has no negation awareness.

**Why this is real pilot value, not a defect in this Programme's own scope:** `evaluate_subtask_result()`'s own docstring already documents the narrative fallback as "an accepted, only-partially-closeable residual risk" — this pilot did not break that promise, it produced the first concrete, reproducible example of it, which is exactly what running the loop on real work (rather than more synthetic exercises) was supposed to surface. Per `implementation-plan.md`'s explicit scope boundary, this pilot does not modify `evaluate_subtask_result()` — the Executor was instructed accordingly and complied (documented the finding in test docstrings, did not attempt a fix).

**Severity (per `.claude/rules/quality-assurance.md`):** P2 — non-critical, a documented workaround
already exists and is already the mandated convention (`usage-cookbook.md` § 6: "Do not build
`checks` from a worker's narrative summary. Only structured, checkable evidence"). Not P0/P1: the
fallback is the secondary path, only reached when no structured evidence exists for a criterion;
the primary, structured-evidence path is unaffected.

**Disposition:** Logged here as new, dated, real-world evidence. Not fixed in this Programme
(out of scope per `implementation-plan.md`'s explicit boundary; `evaluate_subtask_result()` is
Dr. Farouk's owned, already-reviewed code from the parent Programme). Recommended next step below.

---

## 6. Dr. Vance's Review (Phase 4 Gate)

Per `implementation-plan.md` Phase 4's gate ("Pilot results reviewed by Dr. Vance before
recommending the helper's use beyond this one domain"):

- The full Execute → Evaluate cycle ran for real, end to end, exactly as designed:
  worktree-isolated real dispatch, independently re-verified evidence (not narrative), a real
  `uv run` invocation, a correct verdict, and correctly-recorded telemetry.
- One data point is not enough to recommend expanding past the pilot domain — consistent with
  this lab's standing practice of not generalizing from a single run. Further pilot subtasks
  should accumulate before Dr. Nwosu-Chen's benchmarking pass begins in earnest.
- The negation-blindness finding (§ 5.2) should be escalated to Dr. Wieczorek (Safety &
  Evaluation) as a new, dated item for his own backlog — not fixed here, not blocking this pilot's
  continuation, since it confirms rather than breaks an already-acknowledged, already-mitigated
  (via the structured-evidence-first design) residual risk.
- **Verdict: pilot run 01 is a successful, real first data point. Continue accumulating pilot
  runs before recommending expansion.** The worktree branch (`worktree-agent-ae3161b7be2e44c2d`,
  commit `82b22e51`) is real, useful work (5 legitimate new tests) and is recommended for merge to
  `master` — pending the CEO's usual sign-off on merging session work, per this workspace's git
  safety rules, not a Phase 4 gate requirement.

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-08-01-reflexion-bridge-to-real-dispatch`
