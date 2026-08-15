# Supporting Document 06 — Pilot Data Schema Assessment (Dr. Nwosu-Chen)

**Programme:** `2026-07-28-reflexion-execute-monitor-evaluate-loop`
**Author:** Dr. Amara Nwosu-Chen (Staff Research Scientist)
**Purpose:** Assess whether the three real pilot data points produced by
`2026-08-01-reflexion-bridge-to-real-dispatch` (`pilot-run-01.md`–`pilot-run-03.md`) satisfy this
Programme's own `05-benchmarking-methodology.md` well enough to begin the Phase 4 benchmarking
pass that document describes. Written per my own falsifiability standard: a resolution — or in
this case, a "benchmarking has begun" claim — is only accepted against its own stated criterion,
not a plausible-sounding narrative.

---

## 1. What I Was Asked to Assess

Dr. Vance asked me to begin the Phase 4 benchmarking pass using the three real data points from
the reflexion bridge pilot as input. Before running any analysis, I checked those three points
against `05-benchmarking-methodology.md` § 2.1's own stated data sources. They do not match, and
the mismatch is structural, not cosmetic. I am reporting that finding rather than proceeding as if
it weren't there.

---

## 2. The Mismatch

`05-benchmarking-methodology.md` was written assuming real pilot traffic would flow through
`SwarmOrchestrator.execute()` with `SwarmConfig(enable_reflective_loop=True, ...)` — the shipped
in-process loop this Programme's own Phases 1–3 built. Its three metrics (§ 2.1) all read from
that specific mechanism's own state: `TaskStatus` transitions (`COMPLETED` vs. `GATE_FAILED`),
`SubTask.reflection_rationale_history`, `SwarmResult.feedback["retry_counts"]`, and
`MonitorBudget.tier` segmentation. Its comparison design (§ 2.2) additionally requires a real,
size-matched control group — the same pilot category, same time window, dispatched with
`enable_reflective_loop=False`.

`2026-08-01-reflexion-bridge-to-real-dispatch`'s Surface A does not use that mechanism.
`reflective_dispatch_helper.py` calls `evaluate_subtask_result()` and
`_reflection_note_for_attempt()` **directly**, against a `SubTask` it constructs itself for the
purpose of the call — it never runs `SwarmOrchestrator.execute()` or `._dispatch()` at all. This
was not an oversight; it follows directly from that Programme's own Finding 2
(`SwarmOrchestrator.execute()` cannot itself drive real dispatch — the Agent/Task tool is a
host-level primitive no Python process can invoke). Surface A is a deliberate, real workaround
for exactly that limitation. But a consequence I don't think was fully surfaced at the time: it
means none of my methodology's stated data sources exist for these three runs.

| My metric's data source                            | Present in the 3 pilot runs?                                                      |
| -------------------------------------------------- | --------------------------------------------------------------------------------- |
| `TaskStatus` (`COMPLETED`/`GATE_FAILED`)           | **No** — no `SwarmPlan`/`SwarmOrchestrator.execute()` ever ran                    |
| `SubTask.reflection_rationale_history`             | **No** — same reason; the constructed `SubTask` is local to the helper's own call |
| `SwarmResult.feedback["retry_counts"]`             | **No** — same reason                                                              |
| `MonitorBudget.tier` segmentation                  | **No** — `default_monitor_budget()` is never invoked in this path                 |
| A real, size-matched control group (loop disabled) | **No** — no parallel "disabled" traffic was ever dispatched                       |

What the three runs **do** give me: a real `passed`/`rationale`/`retries_remaining` JSON response
per attempt, and — because the Supervisor independently re-verified evidence each time, per
`usage-cookbook.md` § 2.2 — I can trust those three attempts-to-pass values (all **1**) as real,
not narrative. That is useful, but it answers none of my three stated benchmarking questions
(§ 2.1): I cannot compute a gate-pass-rate comparison with no control group and no `TaskStatus`
data; I cannot assess D8's final-attempt reframing with no `retry_counts` and zero runs that ever
reached a final attempt; I cannot segment by `MonitorBudget.tier` when that mechanism was never
invoked.

---

## 3. What This Is and Isn't

**This is not a defect in `2026-08-01-reflexion-bridge-to-real-dispatch`'s work.** Surface A did
exactly what it set out to do — bridge the loop's decision logic to real dispatch at low risk,
using the only mechanism that's actually buildable given the Agent-tool constraint. That
Programme's own `research-report.md` Risks and Limitations already flagged a "Surface-A
sampling-frame caveat" — but on inspection, the real gap is larger than a sampling-frame
qualification. It isn't that Surface A's sample is _biased_; it's that Surface A's data doesn't
have the _shape_ my methodology needs at all. That's a more specific and more useful thing to say
than "sampling frame," so I'm recording it as its own finding rather than folding it under the
existing caveat's language.

**This is also not evidence the reflexion loop doesn't work.** All three runs did pass, and the
Evaluate step's structured-evidence path performed correctly against real evidence each time.
I have a real, if small, positive signal on Surface A working end to end. I do not have a
benchmarking result.

---

## 4. My Recommendation

I am **not** treating this as my Phase 4 benchmarking pass having begun. Two honest paths, and I'm
not deciding between them unilaterally — this is Dr. Vance's call, same posture
`05-benchmarking-methodology.md` § 2.3 already took on the D8-specific comparison question:

- **Option A — design a Surface-A-native methodology.** Write a new, separate benchmarking design
  scoped to what Surface A's data actually contains (attempts-to-pass per real dispatch, real
  rationale text, real `retries_remaining`) rather than trying to force it into a schema built for
  a different mechanism. This is honest but means the D8/D2/tier-specific questions in my original
  methodology stay unanswered until `SwarmOrchestrator.execute()` itself gets a real caller —
  which nothing currently in flight is building.
- **Option B — wait for `SwarmOrchestrator.execute()` to get a real caller.** My original
  methodology stays correct and unchanged, but stays inapplicable until something drives real
  traffic through the actual in-process loop it was designed to measure — which is a separate,
  larger piece of work than anything currently scoped in either Programme.

Either way: **three data points, uniform attempts-to-pass of 1, with no control group, is not
enough to draw a conclusion under either option** — that would be true even if the schema matched.
I'd want at minimum an order of magnitude more real Surface-A dispatches before treating even an
Option-A-style analysis as more than exploratory.

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-07-28-reflexion-execute-monitor-evaluate-loop`
