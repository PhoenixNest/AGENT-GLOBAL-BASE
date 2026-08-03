# Supporting Document 02 — Technical Specification: The Execute-Monitor-Evaluate Cycle Mechanism

**Programme:** `2026-07-28-reflexion-execute-monitor-evaluate-loop`
**Purpose:** A technical specification of the Execute-Monitor-Evaluate-Reflect cycle's own working
principles and steps — the mechanism recommended in `research-report.md`'s Primary Recommendation
and phased in `supporting/01-deployment-and-implementation-plan.md`. For the full-system diagram
and how this cycle relates to the persisted `ReflectionMemory` mechanism, see
`supporting/03-reflexion-system-overview.md`. No production code has been written — this specifies
the mechanism the implementation plan phases in; it is not a status report.

---

## 1. Operational Mechanism, Step by Step

### 1.1 Execute

Unchanged. `SwarmOrchestrator` dispatches a `SubTask` exactly as it does today — this cycle adds no
new dispatch logic and does not touch `SubTask.status` transitions into `DISPATCHED`.

### 1.2 Monitor

Also unchanged in mechanism — this cycle **reuses**, rather than duplicates, two already-production
signals:

- **Fault monitoring:** `error_boundary.py`'s `retry_with_backoff()` and `CircuitBreaker` catch
  timeouts, rate limits, and service errors, and already bound how many times a fault-triggered
  retry is attempted before surfacing `MAX_RETRIES_EXCEEDED`.
- **Execution-health monitoring:** `SwarmConfig.variance_threshold` and
  `circuit_breaker_open_abort` track duration anomalies and fleet-wide abort conditions.

Neither signal is semantic — neither one asks "was the output actually correct." That question is
new, and belongs entirely to the next step.

### 1.3 Evaluate (new)

Only reached once a `SubTask` executes **without** an infra fault. A new
`evaluate_subtask_result(subtask, result) -> EvaluationVerdict` judges `result` against
`subtask.gate_criteria`. Three outcomes:

1. `gate_criteria` is empty/`None` → skip Evaluate entirely, proceed to `COMPLETED` exactly as
   today. This is what keeps the whole cycle **opt-in per subtask**.
2. `gate_criteria` present, verdict `passed=True` → proceed to `COMPLETED`.
3. `gate_criteria` present, verdict `passed=False` → proceed to Reflect.

### 1.4 Reflect (new, ephemeral)

On a failing verdict, the Evaluator's `rationale` is written into the **same task's**
`WorkingMemory` instance via the existing `add_note()` method, and re-injected into the retried
attempt's context via the existing `to_context_string()` method. Both methods already exist in
`memory_store.py` — this cycle adds no new memory type and no new persistence surface.

### 1.5 Bounded Retry — Two Independent Counters

This is the detail most load-bearing for correctness: **the semantic-retry counter introduced here
(`max_reflection_retries`) is tracked completely separately from the pre-existing fault-retry
counter** inside `error_boundary.py`. They must not share a budget:

- If they shared a counter, a task that hit one infra timeout would have less room left to
  self-correct semantically — an unrelated failure mode would silently throttle reflection.
- Conversely, a task using up all its semantic retries chasing a hard gate criterion would have no
  bearing on its separate fault-tolerance budget.

Exhausting the semantic-retry counter routes to `TaskStatus.GATE_FAILED` — the existing status
already means exactly "did not clear its gate criteria"; no new status value is introduced.

### 1.6 Cycle Exit and the Ephemeral Boundary

On either `COMPLETED` or `GATE_FAILED`, `WorkingMemory.clear()` runs and the reflection note is
gone. This is the structural boundary that keeps this cycle distinct from the persisted Reflexion
mechanism (see `supporting/03-reflexion-system-overview.md` § 2): nothing this cycle writes ever
reaches `memory_reflection`, is ever embedded, or is ever retrieved by another agent's orchestrator
brief. If a within-task lesson is judged valuable enough to survive past the task, a **named human
investigator** must separately choose to author a `ReflectionRecord` through the unchanged,
identity-gated `reflection_authoring.py` path — this cycle has no automatic promotion path into
that system, by design.

---

## 2. Dynamic Monitor Allocation

Monitor's resource allocation — timeout budget, retry caps, circuit-breaker sensitivity — adapts
to task characteristics rather than being fixed globally. Today's `SwarmConfig.timeout_seconds`,
`variance_threshold`, and this cycle's own `max_reflection_retries` are static, workspace-wide
defaults; a five-minute lookup task and a two-hour multi-step research task should not share one
timeout or one retry cap.

**Design: derive the allocation from fields `SubTask` already carries — no new
input-classification infrastructure.** `SubTask` already has `domain` (e.g., "backend",
"research", "content") and `estimated_duration`; this cycle adds `gate_criteria`. These three,
taken together, already express how much monitoring/retry budget a given task warrants, before
this cycle adds a single new field. A per-`SubTask` `MonitorBudget` (timeout, fault-retry cap,
semantic-retry cap, circuit-breaker sensitivity) is derived at dispatch time as a function of
`domain` and `estimated_duration` — a small number of tiers (short/standard/long-running;
strict/lenient gate criteria), not a continuous or learned function.

**Trade-off:** a tiered, field-derived allocator is easy to reason about, easy to test, and ships
alongside this cycle with no new infrastructure — but it is coarser than a model that learns the
right budget from historical task outcomes, and a genuinely novel task type may not fit any
existing tier well. The tiered approach ships now, as part of this cycle's own implementation
(Dr. Farouk); a learned/adaptive allocator is a separate, later research question for Dr.
Nwosu-Chen, taken up only if the tiered approach proves insufficient once real usage data exists.
Building the learned version first would be premature complexity this laboratory's engineering
conventions caution against.

---

## 3. User-Facing Feedback During the Cycle

When Evaluate rejects an attempt and the cycle retries, the workspace's existing agent-narration
convention carries the update — a short, plain-language line at the moment it happens, the same
convention every agent in this workspace already follows for a finding, a direction change, or a
blocker. A rejected Evaluate verdict triggering a Reflect-and-retry is exactly such a moment; it
needs no new notification mechanism.

- **On reject-and-retry**, the executing agent surfaces one plain-language line before
  re-attempting: _"That attempt didn't fully meet the task's requirements — retrying once more
  with what I learned (attempt 2 of 3)."_ Not the raw `EvaluationVerdict.rationale` string
  verbatim (written for the next prompt, not for a person), and not silence.
- **On exhausting retries (`GATE_FAILED`)**, one plain-language line states the outcome honestly:
  _"I wasn't able to fully satisfy the requirements after 3 attempts — flagging this for review
  rather than reporting it as done."_ This must never be silently reported as `COMPLETED`.
- **The structured version** lives in `SwarmResult.feedback` (`swarm_orchestrator.py`, already
  present, currently unused) — the existing field carries the structured record of
  attempts/verdicts for anything downstream that wants it (logs, a dashboard, a later audit); this
  cycle populates it rather than adding a new result field.

**Delivery form:** plain text, inline in whatever interface the user is already reading the
agent's work through — the same running text stream carrying every other line the agent produces
during a task. Not a pop-up, toast, or GUI element, and not a server-side log file the user has to
go find. For a task running as a background or delegated agent, the same line surfaces through
that channel's existing completion/status reporting rather than a new one. This cycle introduces
no new delivery surface — only new content (the two lines above) carried over a channel that
already exists.

Design confirmed against `swarm_orchestrator.py` (Dr. Farouk) and this workspace's execution-status
conventions in `error_boundary.py` (Kwame Asante).

---

## 4. The GATE_FAILED Handoff — What "Flagged for Review" Carries

The exhausted-retries message ("flagging this for review," § 3) names an outcome; this section
specifies what it carries, who acts on it, and how.

**1. Reasons for failure.** §1.4–1.6's Evaluator rationale accumulates in the task's own
`WorkingMemory` across retries (each `add_note()` call adds to that instance's note list;
`clear()` isn't called until cycle exit) — but §1.6 calls `WorkingMemory.clear()` on both
`COMPLETED` and `GATE_FAILED` exit, discarding that history with nothing captured on failure. On
`GATE_FAILED` specifically, the full ordered list of per-attempt rationales is copied into
`SwarmResult.feedback` _before_ `WorkingMemory.clear()` runs — otherwise "flagged for review"
would carry no actual reasons, only the fact of failure.

**2. Implementation owner.** Unchanged from `supporting/01-deployment-and-implementation-plan.md`:
Dr. Idris Farouk (design), Amina Yusuf (implementation) — entirely inside `swarm_orchestrator.py`'s
existing `SubTask`/`SwarmResult` handling, no new module boundary.

**3. Supervision.** `GATE_FAILED` surfaces to the same recipient `TaskStatus.FAILED` already
surfaces to today — whoever is running or watching that task — via the plain-language line in § 3,
not a routed notification to a named reviewer. No new supervisory role or escalation layer. A
named human investigator may still separately choose to promote a `GATE_FAILED` task's lesson into
the persisted `ReflectionMemory` system, exactly as `supporting/03-reflexion-system-overview.md`
§ 2 describes — a voluntary, human-initiated act, not an automatic assignment.

**4. Evaluation scoring.** None exists — `EvaluationVerdict` (Phase 1 of the deployment plan) is
`passed: bool` plus a free-text `rationale`. No numeric score for Phase 1: a calibrated score is a
harder, separate problem (Dr. Nwosu-Chen's territory). The cheap improvement made now instead:
`rationale` is structured as a per-criterion checklist (which specific `gate_criteria` items
passed/failed) rather than one free-text paragraph — most of a score's triage value, none of its
calibration risk.

**5. Same approach vs. a new angle.** Every retry today re-attempts with the same approach plus a
critique note — standard Reflexion behavior, but it can fail identically again if the approach
itself, not just its execution, was wrong. On the final retry attempt only (earlier retries still
try the direct fix first), the reflection note explicitly asks for a different approach rather
than a patch to the same one. Treated as a hypothesis, not a mandate: Dr. Nwosu-Chen's Phase 4
benchmarking pass tests same-approach-only retries against angle-shifted-final-retry before this is
adopted as the default.

---

## 5. Activation Criteria — When a `SubTask` Should Enable the Cycle

The cycle is opt-in per `SubTask` via `gate_criteria` (§ 1.3): presence triggers Evaluate, absence
skips it. That mechanism needs a default policy, not a blank per-author choice each time. The
policy reuses the same `domain`/`estimated_duration` inputs § 2's `MonitorBudget` tiering already
derives from — activation tier and monitor tier are set together, at dispatch time, from one
classification pass, not two.

- **Enable by default.** Tasks with an objectively checkable output — an existing spec, schema,
  test suite, or acceptance criteria that costs little to state — and tasks in high-blast-radius
  domains (e.g. `domain` values like `"backend"`, `"security"`, `"release"`), where an ungated
  `SubTask` is itself a risk worth surfacing. A `SubTask` in such a domain dispatched without
  `gate_criteria` is a conformance-review finding, not a silent default.
- **Leave disabled.** Open-ended or exploratory work — research, brainstorming, draft
  generation — where pass/fail isn't well-defined. Evaluating against an absent or forced
  criterion produces false `GATE_FAILED` verdicts and wasted retries, which is worse than no
  evaluation.
- **Skip regardless of domain.** Deterministic, idempotent operations (a lookup, a fixed
  transform) whose only failure mode is infrastructural. Fault-retry (§ 1.2, unchanged) already
  covers these completely; Evaluate would have nothing semantic left to judge.

**Ownership.** Dr. Farouk sets the default tier-to-domain mapping at implementation time (Phase
1/2, deployment plan). Kwame Asante's conformance review confirms the mapping doesn't quietly
leave a high-stakes domain ungated.

---

## 6. Scope Note

This document specifies the Execute-Monitor-Evaluate cycle's own mechanism only — for the
full-system picture (how this relates to the persisted `ReflectionMemory` mechanism) and how the
cycle scales to multi-operator, multi-regulator collaboration, see
`supporting/03-reflexion-system-overview.md`; for a consolidated map of every state and decision
point across the whole cycle, with pass/fail criteria stated explicitly, see
`supporting/04-state-based-decision-logic.md`. It introduces no changes beyond what
`supporting/01-deployment-and-implementation-plan.md` already phases in, and proposes the
dynamic-allocation tiering and activation criteria as additions to that plan's Phase 1/2 scope
(owner: Dr. Farouk), not as new phases or new infrastructure. No production code has been written.

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-07-28-reflexion-execute-monitor-evaluate-loop`
