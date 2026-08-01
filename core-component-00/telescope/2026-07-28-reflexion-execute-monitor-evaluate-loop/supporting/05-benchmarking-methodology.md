# Supporting Document 05 — Phase 4 Pilot: Category Selection and Benchmarking Methodology

**Programme:** `2026-07-28-reflexion-execute-monitor-evaluate-loop`
**Author:** Dr. Amara Nwosu-Chen (methodology), Dr. Idris Farouk (pilot category selection), Dr.
Elias Vance (review)
**Purpose:** Record the Phase 4 pilot category selection and the benchmarking methodology that
will be applied once the pilot generates real usage data. This document defines what will be
measured and how — it does not itself contain results. No real `gate_criteria` traffic exists in
this workspace yet; the actual benchmarking pass runs once the pilot category below has
accumulated enough real dispatches to compare, and is reported as a separate update to this
Programme when that happens.

---

## 1. Pilot Category Selection (Dr. Farouk)

Per `01-deployment-and-implementation-plan.md` Phase 4 § 2: the pilot must be narrow, low-stakes,
and drawn from a domain Phase 1's activation policy (`default_gate_criteria_tier()`) already
turns `gate_criteria` on for by default — otherwise the pilot tells us nothing about the design as
it will actually run.

**Selected category: single-module backend test-verification SubTasks** — e.g. "run the unit test
suite for module X," "confirm a single API endpoint returns the expected status code." Concretely:
`SubTask.domain="backend"`, `gate_criteria` a single checkable item (typically `["tests_pass"]`),
`estimated_duration` typically short-tier (well under 30s per `default_monitor_budget()`).

**Why this category:**

- **In-policy:** `"backend"` is already in `_HIGH_STAKES_DOMAIN_KEYWORDS`, so these tasks get
  `gate_criteria` under the shipped default without any special-casing for the pilot.
- **Low-stakes:** a failed gate here re-runs a test, it doesn't touch production data or an
  external system — an honest low-risk starting point per the Phase 4 gate requirement.
- **Unambiguously checkable:** `evaluate_subtask_result()`'s structured-evidence path
  (`result["checks"]`) applies cleanly — no narrative-fallback ambiguity to confound the
  measurement.
- **Directly answers the open questions blocking on data:** this category sits mostly in the
  short tier, which is exactly where Dr. Wieczorek's 2026-07-30 review flagged a real (but
  unconfirmed) tension between D8's final-attempt reframing and D2's tight timeout budget. Piloting
  here produces evidence on that specific question, not just on D8 in general.

**Explicitly out of scope for this pilot:** `SUPERVISOR_WORKER`-topology swarms (per Phase 4 § 2,
the routing gap in `research-report.md` Open Question 4 is a separate precondition), and any
domain outside the three the activation policy already covers by default.

**Activation mechanism:** whichever caller dispatches this pilot category's `SubTask`s constructs
its `SwarmOrchestrator` with `SwarmConfig(enable_reflective_loop=True, ...)` scoped to that
category only — the workspace-wide default (`False`) is unchanged by this pilot, per Phase 4 § 2's
explicit instruction not to flip the default broadly in this change.

---

## 2. Benchmarking Methodology (Dr. Nwosu-Chen)

### 2.1 What Is Being Measured

Three questions, each with its own metric:

| Question                                                                                          | Metric                                                                                                                                                                      | Data Source                                                                    |
| ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Does the reflective loop recover a measurable share of Reflexion's reported retry-loop benefit?   | Gate-pass rate for pilot-category tasks with `enable_reflective_loop=True` vs. a matched control with it `False`                                                            | `TaskStatus` outcomes (`COMPLETED` vs `GATE_FAILED`) across the pilot window   |
| Does D8's final-attempt reframing measurably help over a same-approach retry?                     | Pass rate on the final allowed attempt specifically, comparing tasks whose last retry received the reframed note against a held-out comparison where it did not (see § 2.3) | `SubTask.reflection_rationale_history`, `SwarmResult.feedback["retry_counts"]` |
| Does D2's short-tier timeout budget undercut D8's reframing (Wieczorek's 2026-07-30 observation)? | Final-attempt pass rate for short-tier tasks specifically, compared against standard/long-running tiers                                                                     | Same as above, segmented by `MonitorBudget.tier`                               |

### 2.2 Comparison Design

A/B by construction, not by inference: the pilot category's real traffic is split at dispatch time
— `enable_reflective_loop=True` for the treatment group, `False` for a size-matched control group
drawn from the same category and time window, so the comparison isn't confounded by which tasks
happened to be harder that week.

### 2.3 The D8-Specific Comparison Is Harder and Needs Its Own Note

D8's reframing only fires on a task's _final_ retry, which by definition is a small subset of an
already-narrow pilot — most tasks pass before reaching it. `_reflection_note_for_attempt()` is
currently unconditional once a task reaches its final attempt (no code-level toggle exists to
withhold the reframing for a held-out A/B split at that specific point). Two honest options, to be
decided once real volume is visible rather than guessed now:

- **Option A — natural comparison:** compare each short-tier task's final-attempt pass rate
  against its own earlier (non-final) retry attempts' pass rate, within the same task. Weaker
  causal claim (attempt number and reframing are confounded) but requires no code change.
- **Option B — add a real A/B toggle:** a `SwarmConfig` flag gating whether
  `_reflection_note_for_attempt()`'s reframing actually applies, defaulting to the current
  unconditional behavior. Cleaner comparison, but is new code and would itself need its own
  review before shipping — not undertaken speculatively here.

This document does not decide between them; that decision is Dr. Nwosu-Chen's once she can see how
much real final-attempt volume the pilot is actually producing.

### 2.4 Success Criteria

Per `research-report.md`'s own framing (Risks and Limitations): the design is considered
empirically validated, not merely architecturally plausible, if the pilot category's gate-pass
rate with the loop enabled shows a **measurable, reproducible improvement** over the control group
— not a specific percentage target invented ahead of a baseline that doesn't exist yet. The first
pilot's job is establishing that baseline.

### 2.5 What This Document Does Not Do

It does not report results — none exist yet. It does not commit to a retry-cap value for Open
Question 2's final tuning, or a verdict on D8's effectiveness, or a resolution to Dr. Wieczorek's
short-tier observation. Those follow once the pilot category above has produced enough real
dispatches to measure, reported as a dedicated update to this Programme.

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-07-28-reflexion-execute-monitor-evaluate-loop`
