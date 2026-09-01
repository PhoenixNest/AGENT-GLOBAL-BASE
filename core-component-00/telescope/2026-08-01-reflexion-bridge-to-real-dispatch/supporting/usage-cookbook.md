# Supporting Document — Reflective Dispatch Helper: Usage Cookbook

**Programme:** `2026-08-01-reflexion-bridge-to-real-dispatch`
**Purpose:** A concrete, example-driven usage guide for Surface A (the `uv run`-invoked
Evaluate/Reflect helper), specifying the exact invocation contract, authoring conventions, and a
full worked example on the pilot domain — for the CEO's review before Phase 1 begins.
**Authors:** Dr. Elias Vance (Laboratory Director), Dr. Idris Farouk (Staff Research Engineer, MAE
Lead — owns `swarm_orchestrator.py` and, per `implementation-plan.md` Phase 1, will own this
helper).

> **STATUS: NOT YET IMPLEMENTED.** No code in this document has been written, run, or verified.
> Every command, JSON shape, and file diff below is a **proposed interface specification** —
> the target for `implementation-plan.md` Phases 1–2, pending the CEO's User Approval Gate
> sign-off on that plan. Treat this as "here is exactly what we intend to build," not "here is
> what exists." Where the underlying, already-shipped logic is referenced (`evaluate_subtask_result()`,
> the `WorkingMemory` Reflect step), that part is real and tested (parent Programme, Phase 1–3,
> 84/84 green) — only the invocation layer described here is new and unbuilt.

---

## 1. When to Use This

Use the helper only for a `SubTask` inside the pilot domain (`05-benchmarking-methodology.md`,
parent Programme): **single-module backend test-verification subtasks** — work with a real,
checkable pass/fail signal (tests, lint), dispatched by `multi-agent-orchestrator` inside a
worktree-isolated worker. Do not use it for open-ended or exploratory subtasks (no checkable
`gate_criteria` exists for those — the underlying `evaluate_subtask_result()` already
no-ops cleanly in that case, per the parent Programme's Phase 1 § 3) and do not use it outside the
pilot domain without Dr. Farouk's and Dr. Vance's sign-off, per `implementation-plan.md` Phase 4.

---

## 2. The Invocation Contract

### 2.1 Command shape

Matches the same cross-platform pattern already shipped for every `.claude/hooks/*.py` script —
`uv`, not a raw shell:

```
uv run core-component-00/framework/05-multi-agent-engineering/implementations/reflective_dispatch_helper.py
```

Input is piped as JSON on stdin (not CLI flags — keeps the contract identical regardless of how
long `gate_criteria`/`checks` grow, and avoids shell-quoting hazards across PowerShell/Bash, which
is exactly the kind of platform-specific fragility this whole correction (v1.1) exists to avoid).
Output is a single JSON object on stdout. Kwame Asante's Phase 3 conformance review confirms this
exact shape before it ships — this section states the proposed contract, not a ratified one.

### 2.2 Request (stdin)

```json
{
  "task_description": "Implement rate-limiting middleware for the API gateway module.",
  "gate_criteria": [
    "All unit tests in test_rate_limiter.py pass",
    "No new lint errors introduced (ruff clean)"
  ],
  "checks": {
    "All unit tests in test_rate_limiter.py pass": false,
    "No new lint errors introduced (ruff clean)": true
  },
  "attempt_number": 1
}
```

`gate_criteria` — one independently-checkable statement per entry, never a compound sentence
(the existing authoring convention on `evaluate_subtask_result()`, unchanged). `checks` — a flat
mapping from each `gate_criteria` string to real, checkable evidence the orchestrator itself
extracted from the worker's actual output (an exit code, a diff summary, a structured tool
result) — **never the worker's own narrative claim of success.** This is not a new rule; it is
Dr. Wieczorek's Phase 3-required mitigation from the parent Programme, restated here as the
concrete input shape that enforces it.

### 2.3 Response (stdout)

```json
{
  "passed": false,
  "rationale": "1 of 2 gate_criteria failed: 'All unit tests in test_rate_limiter.py pass' — checks reported false.",
  "reflection_note": "Attempt 1 failed: All unit tests in test_rate_limiter.py pass. Review the failing test output and address the specific assertion before retrying.",
  "retries_remaining": 1
}
```

On the never-raises degrade path (helper unavailable, malformed input, or any internal error):

```json
{
  "passed": true,
  "rationale": "helper unavailable: <reason> — Evaluate skipped, subtask proceeds as if ungated.",
  "reflection_note": null,
  "retries_remaining": 0
}
```

This mirrors `reflection_bridge.py`'s own never-raises, degrade-to-neutral contract — a helper
fault can only skip the loop for that attempt, never block or fail a real dispatch.

---

## 3. Where This Gets Called From: `multi-agent-orchestrator.md`

The proposed diff to that subagent's Execute phase (§ "2 — Execute"), per `implementation-plan.md`
Phase 2 — **not yet applied**:

```diff
 ## Five-Phase Lifecycle

 | Phase             | Action                      | Commands                                                    |
 | ----------------- | ---------------------------- | ----------------------------------------------------------- |
 | **1 — Provision** | Create worktree per agent   | `git worktree add ../agent-<name> -b agent/<name>/<task>`   |
-| **2 — Execute**   | Agent works in its worktree | `git add -A && git commit -m "agent/<name>: ..."`           |
+| **2 — Execute**   | Agent works in its worktree | `git add -A && git commit -m "agent/<name>: ..."`           |
+
+**Reflective loop (pilot domain only — single-module backend test-verification subtasks):**
+After a worker completes, before marking its subtask done, extract real checkable evidence
+(test/lint output — never the worker's own narrative) into a `checks` mapping and invoke:
+`uv run <path-to>/reflective_dispatch_helper.py` with the JSON contract in this cookbook § 2.
+On `passed: false` with `retries_remaining > 0`, re-dispatch the same worker with
+`reflection_note` appended to its task prompt, then repeat. On exhaustion, mark the subtask
+GATE_FAILED and surface `rationale` in the final report to the calling session — do not merge
+silently and do not drop the failure silently.
```

No other section of that file changes — Hard Constraints, Agent Roles, and Phases 1/3–5 are
untouched.

---

## 4. Worked Example, End to End (Pilot Domain)

**Task:** "Implement rate-limiting middleware for the API gateway module, verified by pytest."
**`gate_criteria`:** `["All unit tests in test_rate_limiter.py pass", "No new lint errors introduced (ruff clean)"]`

| Step | What happens                                                                                                                                                | Real Claude Code mechanism                                                                                 |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 1    | `multi-agent-orchestrator` provisions a worktree and dispatches a worker subagent with the task                                                             | Existing Phase 1–2 lifecycle, unchanged                                                                    |
| 2    | Worker implements the middleware, runs `pytest test_rate_limiter.py` and `ruff check`, gets 1 test failure and 0 lint errors                                | Worker's own tool calls (Bash/PowerShell, whichever the session uses)                                      |
| 3    | Orchestrator extracts `checks = {"...tests...pass": false, "...ruff clean": true}` from the real pytest/ruff exit codes — not from the worker's own summary | New: evidence-extraction step, § 2.2                                                                       |
| 4    | Orchestrator runs `uv run .../reflective_dispatch_helper.py` with `attempt_number: 1`                                                                       | New: invocation, § 2.1                                                                                     |
| 5    | Helper returns `passed: false`, `reflection_note` naming the failing test, `retries_remaining: 1`                                                           | New: helper response, § 2.3 — internally calls the unmodified, already-shipped `evaluate_subtask_result()` |
| 6    | Orchestrator re-dispatches the **same worker, same worktree**, with the reflection note appended to its prompt                                              | Existing Agent-tool dispatch, new prompt content only                                                      |
| 7    | Worker fixes the failing assertion, re-runs pytest (now passing) and ruff (still clean)                                                                     | Worker's own tool calls                                                                                    |
| 8    | Orchestrator extracts `checks = {"...tests...pass": true, "...ruff clean": true}`, calls the helper again with `attempt_number: 2`                          | Same mechanism as step 3–4                                                                                 |
| 9    | Helper returns `passed: true`                                                                                                                               | Same mechanism as step 5                                                                                   |
| 10   | Orchestrator proceeds to Integrate exactly as it does today for any passing subtask                                                                         | Existing Phase 3 lifecycle, unchanged                                                                      |

If step 7 had failed again, `retries_remaining` would be `0` at step 8's call, and the subtask
would transition to `GATE_FAILED` with both attempts' rationale surfaced in the orchestrator's
final report — a flagged item for human review, not a silent merge.

---

## 5. Roles: Executor, Supervisor, Evaluator

> Still **NOT YET IMPLEMENTED** — this section specifies the intended role separation for
> Phases 1–2, the same status as every other section of this cookbook.

### 5.1 Role definitions

| Role           | Maps to                                                                                   | Responsibility                                                                                                                                                                                                          | Authority boundary                                                                                                                      |
| -------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **Executor**   | The real worker subagent dispatched via the Agent tool inside its own worktree            | Performs the actual work (writes code, runs tests/lint) and produces real, checkable output                                                                                                                             | Cannot mark its own subtask passed — never self-evaluates; never invokes the helper itself                                              |
| **Supervisor** | The `multi-agent-orchestrator` subagent                                                   | Decomposes tasks, dispatches Executors, extracts `checks` evidence, invokes the Evaluator, decides retry vs. `GATE_FAILED` vs. Integrate, aggregates results across Executors, surfaces failures to the calling session | Cannot override an Evaluator's verdict; cannot exceed `max_reflection_retries`; cannot promote a note to persisted `ReflectionMemory`   |
| **Evaluator**  | `reflective_dispatch_helper.py`, wrapping the already-shipped `evaluate_subtask_result()` | Judges an Executor's real evidence against `gate_criteria`; returns pass/fail, rationale, and a reflection note                                                                                                         | Judges only what it's handed — never fetches its own evidence, never talks to the Executor directly, never raises (degrades to neutral) |

This is a strict separation of duties, inherited directly from Dr. Wieczorek's Phase 3 requirement
(parent Programme): the entity that produces evidence (Executor) is never the entity that judges
it (Evaluator), and the entity that judges (Evaluator) is never the entity that decides what
happens next (Supervisor). Three distinct roles, not one component wearing three hats — a
manipulated Executor output can at worst corrupt its own evidence, not also grant itself a passing
verdict or override the retry decision.

### 5.2 Iterative execution for complex tasks

The built-in mechanism is the bounded retry already shipped in `evaluate_subtask_result()`/
`WorkingMemory` (parent Programme, Phase 2): the **same** Executor, in the **same** worktree,
re-attempts the **same** subtask with a reflection note appended, up to `max_reflection_retries =
2`. This is retry, not re-planning — the Supervisor does not change the subtask's scope or
`gate_criteria` between attempts.

For a task too complex for that alone — where two retries of the same approach won't resolve a
structural problem (wrong decomposition, missing dependency, unclear spec) — the retry loop is not
the right tool, and this cookbook does not stretch it to be one. Today the only defined fallback is
`GATE_FAILED`: the Supervisor surfaces the failure with full rationale history to the calling
session for a human (or a fresh Supervisor decomposition, started as a new task, not a mid-loop
reattempt) to decide the next step. **Automatic re-decomposition on repeated `GATE_FAILED` is not
implemented and not proposed here** — it would mean the Supervisor unilaterally changing scope
based on its own Evaluator's verdict, which starts to blur the § 5.1 role separation and deserves
its own design pass, not an ad hoc addition to this cookbook.

### 5.3 Multiple Executors (supported today, opt-in per subtask)

Already covered by the existing `FORK_JOIN`/`HYBRID` swarm topologies (`swarm_orchestrator.py`,
unmodified): the Supervisor dispatches N Executors in parallel, each independently
worktree-isolated, each running its own full Executor→Evaluator cycle. `SwarmResult.feedback`'s
existing `gate_failed` count and rationale history (parent Programme, Phase 2) already aggregate
across all N — a correlated failure (three Executors all failing the same criterion) reads as one
visible signal, not three easy-to-miss messages. No new code is needed for this case; it is the
swarm's existing fan-out, with the Evaluator wired in per Executor.

### 5.4 Multiple Supervisors — explicitly out of scope, not silently unsupported

A second Supervisor coordinating several first-line Supervisors (each running its own
Executor/Evaluator fleet) maps to `SwarmTopology.SUPERVISOR_WORKER`. This is a real, named gap,
not something this cookbook can quietly work around: `SwarmOrchestrator.execute()`'s dispatch
table currently routes `SUPERVISOR_WORKER` through the `HYBRID` executor with no distinct
execution path — logged as the parent Programme's Open Question 4, deliberately deferred "to
first real need," not blocking Phases 1–4 of this pilot. Multi-Supervisor use is therefore **not
usable today** and is not part of this cookbook's worked example — it requires that dispatch-path
gap closed first, by Dr. Farouk, as its own scoped piece of work, per the existing Open Question 4
assignment. Nothing in this document should be read as offering it.

### 5.5 Multiple Evaluators — not part of the current design

`evaluate_subtask_result()` is one deterministic function call per attempt, judging the full
`gate_criteria` list at once under the strict-AND rule (parent Programme, Open Question 5). There
is no per-criterion Evaluator, no ensemble/voting Evaluator, and no plan in
`implementation-plan.md` to add one. If a future need arises for independent judgment across
different criteria (e.g. a security criterion evaluated separately from a style criterion), that
is a new design question for Dr. Farouk and Dr. Wieczorek to scope — this cookbook does not assume
or half-build it.

---

## 6. What Not To Do

- **Do not invoke via a raw `bash`/`pwsh` shell-out.** Always `uv run <path>.py` — this is the
  exact mistake corrected in `research-report.md` v1.1 (Finding 6); repeating it reintroduces the
  OS-fork problem `2026-07-30-cross-platform-config-automation` already closed.
- **Do not build `checks` from a worker's narrative summary.** Only structured, checkable evidence
  — this is Dr. Wieczorek's binding Phase 3 mitigation, not a style preference.
- **Do not use outside the pilot domain** without Dr. Farouk's and Dr. Vance's explicit go-ahead
  (`implementation-plan.md` Phase 4 gate).
- **Do not promote a `reflection_note` or rationale to persisted `ReflectionMemory`.** This stays
  entirely `WorkingMemory`-scoped and cleared at cycle exit, per the parent Programme's Finding 4 —
  a human investigator may separately choose to log a genuinely valuable lesson, but the helper
  itself never writes to persisted memory.
- **Do not wire this into a `.claude/hooks/*.py` gate.** That is Surface B, explicitly deferred
  pending its own, separately-commissioned adversarial review (`research-report.md` Findings 4–5)
  — nothing in this cookbook builds toward it.
- **Do not assume multi-Supervisor or multi-Evaluator support exists.** See § 5.4–5.5 —
  `SUPERVISOR_WORKER` topology is unsupported by this loop today, and there is no multi-Evaluator
  design at all.

---

## 7. Relationship to Other Documents in This Programme

| Document                                       | Role                                                                             |
| ---------------------------------------------- | -------------------------------------------------------------------------------- |
| `research-report.md`                           | Why this bridge exists, the two candidate surfaces, and why Surface A was chosen |
| `supporting/implementation-plan.md`            | The phased build plan, owners, gates, and the Before/After comparison table      |
| `supporting/usage-cookbook.md` (this document) | The concrete interface spec and worked example, for review before Phase 1        |

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-08-01-reflexion-bridge-to-real-dispatch`
