# Supporting Document 07 — Surface-A-Native Benchmarking Methodology (Option A)

**Programme:** `2026-07-28-reflexion-execute-monitor-evaluate-loop`
**Author:** Dr. Amara Nwosu-Chen (Staff Research Scientist)
**Commissioned by:** Dr. Elias Vance, 2026-08-03, exercising CEO-delegated decision authority —
see `research-report.md` Phase 4 Update 2. This is Option A from
`supporting/06-pilot-data-schema-assessment.md` § 4: a new methodology scoped to what Surface A's
data actually contains, rather than forcing it into `05-benchmarking-methodology.md`'s schema,
which requires data sources Surface A structurally cannot produce.

**Status of this document:** methodology only. No benchmarking pass has been run under it — see
§ 4 for the minimum sample size before any result under this methodology is more than exploratory.
`05-benchmarking-methodology.md` is retained unchanged and is not superseded by this document; see
§ 5.

---

## 1. What Surface A's Data Actually Contains

Every real Surface A dispatch (via `reflective_dispatch_helper.py`, invoked `uv run` from a
worktree-isolated Executor's context) produces, per real invocation:

- A request the Supervisor constructs: `gate_criteria` (list of independently-checkable
  statements) + `checks` (structured evidence the Supervisor independently re-verified — never
  the Executor's own narrative claim, per `usage-cookbook.md` § 2.2) + `narrative` (the Executor's
  own summary text, kept only as the documented fallback path, not the primary evidence).
- A response: `passed` (bool), `rationale` (str), `retries_remaining` (int), all real,
  deterministic output of `evaluate_subtask_result()`/`_reflection_note_for_attempt()`.
- Since Phase 4: an invocation-counter telemetry record
  (`../2026-08-01-reflexion-bridge-to-real-dispatch/supporting/pilot/telemetry/invocations.jsonl`,
  one line per real call) — timestamp, whether
  the call itself degraded (never-raises contract), and `passed`.

This is real, falsifiable, machine-checkable data. It is a different shape from
`05-benchmarking-methodology.md`'s three metrics (`TaskStatus`, `retry_counts`,
`MonitorBudget.tier`), not a subset of them — see `06-pilot-data-schema-assessment.md` § 2 for the
full comparison.

---

## 2. Metrics This Methodology Measures

### M1 — Evaluator Agreement Rate

**What it measures:** across all real dispatches, the rate at which the Evaluator's `passed`
verdict agrees with the Supervisor's independent judgment of the same, separately-re-verified
evidence (computed by the Supervisor manually reviewing the same `checks` before calling the
helper, as already practiced in every pilot run to date).

**Falsification test:** M1 is a calibration check, not a loop-performance check — it can be
computed meaningfully starting at a small n, unlike M2/M3 below. **Threshold: if M1 falls below
90% over at least 20 real dispatches, the structured-evidence-first design in
`_criterion_satisfied()` needs re-examination** — that would mean the Evaluator's own judgment is
diverging from independently-verified ground truth often enough to not be trustworthy as an
automated gate.

**Current status:** n=3 (pilot runs 01–03), M1 = 100% (3/3) after the 2026-08-03 fixes to the two
real disagreement-adjacent bugs Wieczorek's triage found (`_criterion_satisfied` negation
blindness; `HandoffPacket.validate()` fail-open on missing `fleet_id` — see
`../2026-08-01-reflexion-bridge-to-real-dispatch/supporting/pilot/wieczorek-triage-01.md`). n=3 is far
below the n=20 floor this test requires — 100% at n=3 is not evidence of calibration, it is an
absence of disconfirming data so far.

### M2 — Attempts-to-Pass Distribution

**What it measures:** across real dispatches that fail on a first attempt and retry, how many
attempts it actually takes to reach `passed=True` (or exhaust `retries_remaining`), and whether
the final-attempt reflection reframing (D8) measurably changes the outcome versus an identical
retry note.

**Falsification test: requires at least 10 real dispatches whose first attempt returns
`passed=False` and which retry at least once.** Below that floor, no claim about the Reflect
step's recovery effectiveness may be made under this methodology, full stop — not "weak evidence
suggesting," not stated at all.

**Current status:** 0 qualifying dispatches. All three real pilot runs passed on attempt 1
(honestly documented as such in each `pilot-run-0N.md`, never forced). M2 is currently
unmeasurable, not "weakly positive" or any other soft characterization — the Reflect/retry path
has never once been exercised in real Surface-A data, and this methodology will not paper over
that with a false-precision estimate from zero qualifying samples. Per this lab's standing
practice, no dispatch will be artificially constructed to fail solely to generate this data;
qualifying dispatches must arise from genuine pilot-domain work.

### M3 — Rationale Actionability (Qualitative)

**What it measures:** whether a `rationale` string, read cold by someone who didn't run the
dispatch, states specifically enough what was wrong (or right) that a human or a future automated
Reflect step could act on it, versus a generic pass/fail restatement.

**Falsification test:** scored on a 3-point rubric (specific-and-actionable / generic-but-correct
/ uninformative) by an evaluator who did not construct the `checks` for that dispatch. **This
metric is inherently qualitative and is reported as a distribution, never averaged into a single
number** — a mean of ordinal categories is a fabricated precision this lab does not manufacture.

**Current status:** not yet scored — scoring requires a rater blind to the original `checks`
construction, which the pilot's Supervisor-authored evidence does not yet support at n=3 without
compromising blindness (the same three people who built each pilot's `checks` are the only
readers so far).

---

## 3. Data Collection Going Forward

No new data collection is authorized by this document. `invocations.jsonl` already captures the
raw substrate for M1 automatically on every real `reflective_dispatch_helper.py` call (Phase 4
telemetry, already shipped). When real Surface-A dispatch volume grows through ordinary future use
of the pilot domain (single-module backend test-verification subtasks) or any domain it's
extended to, M1 can be recomputed at any time by replaying `checks` against the Supervisor's own
independent record. M2 and M3 require dispatches this lab is not manufacturing — they accumulate
only as real qualifying cases occur.

---

## 4. Minimum Sample Size Before Any Result Is More Than Exploratory

Restating `06-pilot-data-schema-assessment.md` § 4's floor, made specific per metric:

| Metric                       | Floor before non-exploratory claims  | Current |
| ---------------------------- | ------------------------------------ | ------- |
| M1 (Evaluator agreement)     | 20 real dispatches                   | 3       |
| M2 (attempts-to-pass)        | 10 real dispatches that retry ≥ once | 0       |
| M3 (rationale actionability) | blind rater available                | 0       |

None of the three floors are met today. This document exists to make the eventual pass
reproducible and falsifiable when volume exists — it does not itself constitute that pass.

---

## 5. Relationship to `05-benchmarking-methodology.md`

That document is retained unchanged and is not wrong — it is scoped to a different mechanism
(real traffic through `SwarmOrchestrator.execute()` itself) that this lab has not yet built a
caller for. If and when that caller exists, `05-benchmarking-methodology.md`'s `TaskStatus`/
`retry_counts`/`MonitorBudget.tier` metrics become measurable again and should be used as
originally designed — this document (07) does not replace it, only covers the gap while Surface A
is the only real-traffic mechanism this lab has.

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-07-28-reflexion-execute-monitor-evaluate-loop`
