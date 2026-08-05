# Research Report — The Execute-Monitor-Evaluate Loop: Closing Reflexion's Deferred Within-Task Mechanism

---

## Metadata

| Field                | Value                                                                                                                                                                                                                                                                                                                                                                                                          |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Investigation ID** | `2026-07-28-reflexion-execute-monitor-evaluate-loop`                                                                                                                                                                                                                                                                                                                                                           |
| **Date Started**     | 2026-07-28                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Date Completed**   | 2026-07-28                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Status**           | Implemented and twice independently reviewed (Phase 3; secondary D2/D8 review, both PASS). Three real Surface-A pilot data points exist; a Surface-A-native benchmarking methodology (Option A, `supporting/07-...md`) was commissioned 2026-08-03 to measure them, but no benchmarking pass has run yet — none of its minimum-sample floors are met (see v1.18); pattern documentation (Phase 5) remains open |
| **Investigator**     | Dr. Elias Vance (Laboratory Director, Principal Investigator)                                                                                                                                                                                                                                                                                                                                                  |
| **Laboratory**       | Core Component 00                                                                                                                                                                                                                                                                                                                                                                                              |
| **Module(s)**        | Multi-Agent Engineering (within-task execution loop) × Harness Engineering (monitor/retry reuse) × Context Engineering (`WorkingMemory`-scoped reflection, existing `ReflectionMemory` boundary)                                                                                                                                                                                                               |
| **Priority**         | High                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Requestor**        | CEO                                                                                                                                                                                                                                                                                                                                                                                                            |

**Executing engineers:** Dr. Idris Farouk with Amina Yusuf (Multi-Agent Engineering — within-task
loop / `SwarmOrchestrator` integration point); Kwame Asante with Connor O'Malley (Harness
Engineering — conformance review of reusing `error_boundary.py`'s retry/circuit-breaker signals
as the Monitor channel); Mei-Ling Zhao with Hana Kobayashi (Context Engineering — confirming
`WorkingMemory` as the correct, non-persistent host for the Reflect step); Dr. Tomasz Wieczorek
(Staff Safety & Evaluation Engineer — required adversarial review before any activation, per the
precedent set in the parent Programme); Dr. Amara Nwosu-Chen (Staff Research Scientist —
benchmarking this design against Reflexion's own reported retry-loop numbers). Assignments follow
`crew/CLAUDE.md`'s Laboratory Roster and Activation Protocol.

---

## Executive Summary

The CEO observed that the prior Reflexion memory system design (`2026-07-14-reflexion-memory-system`)
did not fully realize a closed "Execute-Monitor-Evaluate" loop, and asked this Programme to (1)
re-examine that system and confirm the observation, and (2) study how to integrate the missing
mechanism into the existing Reflexion framework. **The observation is confirmed.** The 2026-07-14
report deliberately implemented only the persistent, cross-session, investigator-gated half of the
Reflexion architecture (a durable `ReflectionRecord` written by a named human after the fact); it
explicitly declined — and openly documented declining — Reflexion's original tight, autonomous,
within-task retry loop, deferring it to "its own future, separately-commissioned Programme" (that
report's Open Question 4, CEO-approved in principle 2026-07-15). This report is that commissioned
Programme. We recommend closing the gap with an **ephemeral, `WorkingMemory`-scoped**
Execute→Monitor→Evaluate→Reflect loop layered onto existing `SwarmOrchestrator` and
`error_boundary.py` primitives — deliberately not extending the persistent, identity-gated
`ReflectionMemory` write path, which remains structurally wrong for an autonomous per-task loop for
the same reason the original report rejected an MCP write tool for it.

> **Phase 4 Update (2026-08-03):** `2026-08-01-reflexion-bridge-to-real-dispatch` (Surface A, an
> advisory `uv run` helper bridging this loop's decision logic to real Claude Code dispatch)
> produced three real pilot data points. Dr. Nwosu-Chen assessed them against this Programme's own
> `05-benchmarking-methodology.md` and found a structural mismatch, not a sampling issue: Surface A
> calls `evaluate_subtask_result()`/`_reflection_note_for_attempt()` directly, bypassing
> `SwarmOrchestrator.execute()` entirely, so none of this methodology's stated data sources
> (`TaskStatus`, `retry_counts`, `MonitorBudget.tier`, a control group) exist for those three runs.
> **The Phase 4 benchmarking pass described below has not begun** — three data points with no
> control group wouldn't be enough even if the schema matched. Full assessment and two proposed
> paths forward (a Surface-A-native methodology, or waiting for `SwarmOrchestrator.execute()` to
> get a real caller): `supporting/06-pilot-data-schema-assessment.md`. Decision between those paths
> is Dr. Vance's, not made here.

> **Phase 4 Update 2 (2026-08-03) — Decision:** The CEO returned decision-making authority to Dr.
> Vance and the cc00 lab team, with an explicit directive to take a long-term view and strengthen
> the reflection system's robustness. **Decision: commission Option A.** Dr. Nwosu-Chen has
> written `supporting/07-surface-a-native-benchmarking-methodology.md` — falsifiable metrics scoped
> to what Surface A's real dispatch data actually contains (Evaluator agreement rate,
> attempts-to-pass distribution, rationale actionability), each with a stated minimum-sample floor
> before any result counts as more than exploratory. None of the three floors are met today (n=3
> against floors of 20/10/blind-rater) — this commissions the methodology, not a benchmarking
> result, and authorizes no new pilot dispatches. `05-benchmarking-methodology.md` (Option B) is
> retained unchanged and un-superseded, for whenever `SwarmOrchestrator.execute()` gets a real
> production caller — see doc 07 § 5. Separately, the two real P2 findings from pilot testing
> (`_criterion_satisfied()` negation-blindness; `HandoffPacket.validate()` fleet_id-omission
> fail-open) were fixed and verified same-day (129/129 multi-agent-engineering tests green) — full
> record in `../2026-08-01-reflexion-bridge-to-real-dispatch/research-report.md`.

---

## Investigation Scope

### What Was Investigated

(1) Whether the 2026-07-14 Reflexion memory system report actually implements a closed
Execute-Monitor-Evaluate loop, or only part of one; (2) what "Monitor" and "Evaluate" capability
already exists elsewhere in the CC-00 stack (harness-layer retry/circuit-breaking,
multi-agent-layer variance tracking) that a closed loop could reuse rather than duplicate; (3) what
integration design would add the missing within-task loop without reopening the write-tool threat
model the original report deliberately closed for persistent reflections.

### Why This Investigation Was Needed

The CEO's own reading of the prior report's status could not be settled by re-reading its Executive
Summary alone — the report's Primary Recommendation and its Audit History both read as a complete,
"Ready for ASGF ratification" deliverable, and the gap is disclosed only in two specific places (the
Director Alignment Review's required clarification paragraph, and Open Question 4) rather than
surfaced at the top. A literal re-examination against the actual production code (`memory_store.py`,
`swarm_orchestrator.py`, `error_boundary.py`) was needed to confirm the gap is real and not just a
framing artifact of the prior report's prose.

### Out of Scope

- Modifying the 2026-07-14 report, `memory_store.py`'s existing `ReflectionMemory`/`ReflectionRecord`
  classes, or the investigator-gated write path (`reflection_authoring.py`). This investigation adds
  a distinct, ephemeral mechanism alongside them; it does not alter the persisted design or reopen
  its already-settled write-tool decision.
- A production implementation of the loop. This report specifies the design and integration point;
  implementation is a follow-up task per Next Steps, consistent with this Programme's scope as a
  research/study deliverable only.
- Extending this mechanism to Company or Studio pipeline stage retries. Scoped to CC-00 per
  `telescope/CLAUDE.md`'s department-scope rule (see Open Questions).

---

## Research Questions

1. Did the 2026-07-14 Reflexion memory system report implement a closed Execute-Monitor-Evaluate
   loop? If not, precisely what is missing and where is that gap already disclosed?
2. What existing CC-00 harness/orchestration infrastructure already performs "Monitor"-like or
   "Evaluate"-like functions that a closed loop should reuse rather than reinvent?
3. Where should an ephemeral, within-task reflection live, given that the existing `ReflectionMemory`
   type is deliberately investigator-gated and cross-session?
4. What integration point into `SwarmOrchestrator` (or a new orchestration primitive) would add the
   loop without reopening the write-tool threat model Finding 4 of the original report closed?
5. What governance/safety review must gate activation, consistent with the precedent already set for
   the persistent reflection system?

---

## Methodology

### Approach

Two phases: (1) a direct re-read of `2026-07-14-reflexion-memory-system/research-report.md` in full,
cross-checked against the production code it produced (`memory_store.py`'s `WorkingMemory` and
`ReflectionMemory` classes, `error_boundary.py`, `swarm_orchestrator.py`) to confirm whether the
disclosed gap is also a gap in the shipped implementation, not only in the prose; (2) a design pass
mapping the missing Execute-Monitor-Evaluate loop onto existing harness and orchestration primitives,
explicitly avoiding duplication of monitoring logic that already exists.

### Tools and Resources

- `core-component-00/telescope/2026-07-14-reflexion-memory-system/research-report.md` (full read,
  including § Audit History and Open Questions)
- `core-component-00/engineering/context-engineering/implementations/memory_store.py`
  (`WorkingMemory`, class at line 380; `ReflectionMemory`/`ReflectionRecord`, from line 450)
- `core-component-00/engineering/harness-engineering/implementations/error_boundary.py`
  (`SafeModelCall.execute`, `retry_with_backoff`, `CircuitBreaker`)
- `core-component-00/engineering/multi-agent-engineering/implementations/swarm_orchestrator.py`
  (`SwarmConfig.enable_feedback_loop`/`variance_threshold`/`circuit_breaker_open_abort`, `SubTask`)
- `crew/director/elias-vance/agent/profile.md`, `crew/CLAUDE.md` (Laboratory Roster, Activation
  Protocol)

### Constraints

- No production code was written or modified during this investigation — findings and the
  integration design are recommendations pending an implementation task.
- Benchmarking against Reflexion's own reported numbers (Shinn et al., NeurIPS 2023) is carried
  forward by reference from the 2026-07-14 report's bibliography, not re-run fresh in this
  investigation.

---

## Findings

### Finding 1: The Gap Is Real, Disclosed, and Confirmed Against the Shipped Code — Not Just a Framing Artifact

The 2026-07-14 report's Director Alignment Review states, verbatim, that the shipped design "is
investigator-gated, cross-session, and persisted for months — materially different in cadence and
authorship from Reflexion's tight autonomous within-task retry loop," and that this loop "was
considered and rejected (Finding 4, Option A) because it would reopen a write-tool threat model
this workspace's `agent-memory` server has already and deliberately declined to accept." Open
Question 4 of that report asks explicitly whether "a purely ephemeral, agent-authored, within-task
reflection... should be added alongside the persistent, investigator-gated design" and records that
the CEO approved standing this up "as its own future, independently-commissioned Programme" on
2026-07-15 — not folded into that Programme's implementation.

This is confirmed against the actual code, not just the prose: `memory_store.py`'s `ReflectionMemory`
(from line 624) requires a verified `IdentityVerification` token for every `record_reflection()`
call, sourced only from `reflection_authoring.verify_authorized_identity()` — a human-in-the-loop
step incompatible with an autonomous per-task retry cadence. `swarm_orchestrator.py`'s `SubTask` and
`SwarmResult` dataclasses carry no field for a self-generated critique or a retry-triggering
evaluation signal; `SwarmConfig.enable_feedback_loop` exists but (per its name and neighboring
`variance_threshold`/`circuit_breaker_open_abort` fields) governs execution-health feedback, not a
semantic Actor→Evaluator→Reflect cycle over task output.

**Evidence:**

- Director Alignment Review's required clarification paragraph (verbatim, quoted above)
- Open Question 4, Status: "Resolved by CEO decision (2026-07-15)... approved standing up this
  ephemeral, `WorkingMemory`-only variant as its own future, independently-commissioned Programme"
- `ReflectionMemory.record_reflection()` (`memory_store.py:672`) hard-requires an `IdentityVerification`
  — structurally cannot be called autonomously by an executing agent mid-task
- No `SubTask`/`SwarmResult` field or `SwarmOrchestrator` method implements a self-critique-then-retry
  cycle; `enable_feedback_loop` is scoped to execution-health signals (Finding 2)

**Implications:**

The CEO's observation is correct: this workspace's Reflexion system, as it exists today, closes the
loop from failure to a durable cross-session lesson, but does not close the tighter loop from a
single task attempt through monitoring and evaluation back into a same-task retry. Confirming this
was the first deliverable the CEO asked for; the remainder of this report is the second.

---

### Finding 2: Execution-Health Monitoring Already Exists — What's Missing Is Semantic Evaluation, Not Monitoring Infrastructure

`error_boundary.py` already implements a Monitor-equivalent for infrastructure failure:
`retry_with_backoff()` (bounded retries with jittered exponential backoff), `SafeModelCall.execute()`
(returns a structured `MAX_RETRIES_EXCEEDED` code rather than raising unbounded), and `CircuitBreaker`
(trips on a failure-rate threshold to abort further attempts). `swarm_orchestrator.py`'s `SwarmConfig`
independently tracks `variance_threshold` (actual vs. estimated task duration) and
`circuit_breaker_open_abort`. Both are real, tested, production monitoring — but both monitor
**execution health** (did the call time out, error, or run long), never **output quality against
task intent** (did the result actually satisfy the goal). Reflexion's Evaluator step is the latter:
a judgment on whether the Actor's output achieved the task, not whether it executed without a
runtime exception.

**Evidence:**

- `retry_with_backoff`, `SafeModelCall.execute`, `CircuitBreaker` (`error_boundary.py`) — all
  fault-triggered, none output-quality-triggered
- `SwarmConfig.variance_threshold`/`circuit_breaker_open_abort` (`swarm_orchestrator.py:46-54`) —
  duration and fault-rate signals, not semantic correctness signals
- `SubTask.gate_criteria: Optional[list[str]]` (`swarm_orchestrator.py:81`) already exists as an
  unused-for-this-purpose field — the closest existing hook to an Evaluator's judgment criteria

**Implications:**

The Monitor half of Execute-Monitor-Evaluate is substantially already built and battle-tested; it
should be reused, not duplicated. The Evaluate half genuinely does not exist and is the actual gap
to close. `SubTask.gate_criteria` is the natural extension point — it already exists as a per-task
list of criteria but is not yet wired to any evaluation step that acts on it.

---

### Finding 3: `WorkingMemory` Is the Correct, Already-Existing Host for an Ephemeral Reflection — No New Memory Type Needed

`WorkingMemory` (`memory_store.py:380`) is already scoped exactly the way Reflexion's tight loop
requires: "single-turn memory for the current task," "cleared after each turn," living "entirely in
the active context window." It already exposes `add_note()` for "a reasoning note or intermediate
conclusion" and `to_context_string()` to re-inject that note into the next attempt's context. No
fifth memory type, and no extension of the persisted `ReflectionMemory`, is needed to host an
ephemeral, agent-authored reflection — the existing class already does exactly this job; it has
simply never been wired into a retry loop that calls it between attempts.

**Evidence:**

- `WorkingMemory.add_note()` / `to_context_string()` (`memory_store.py:420-438`) — already the exact
  shape of "write a verbal reflection, re-inject it into the next attempt"
- `WorkingMemory.clear()` (`memory_store.py:440`) — already guarantees the note does not outlive the
  turn/task, the precise safety property Finding 4 depends on

**Implications:**

This closes what would otherwise be the biggest implementation question: where does an autonomous,
agent-written reflection live without reopening the persisted write-tool decision? It lives
nowhere new — it lives in the memory type this module already built for exactly this scope.

---

### Finding 4: Ephemeral Scope Is What Makes an Agent-Autonomous Write Safe Here, Where It Was Correctly Rejected for Persistent Storage

The original report's Finding 4 rejected an MCP write tool for `ReflectionMemory` because "a
prompt-injected call could write an arbitrary 'reflection' that a future orchestrator brief would
then trust and surface" — the danger was persistence and cross-session/cross-agent reach. An
ephemeral, `WorkingMemory`-scoped reflection does not have that reach: it is cleared at the end of
the turn/task (`WorkingMemory.clear()`), is never embedded, never written to `memory_reflection`,
and is never retrieved by another agent's orchestrator brief. A poisoned note under this design can
only mislead the same task's own next retry attempt within the same session — a materially smaller
blast radius than a persisted, cross-session, cross-agent-visible record, but not zero, since it can
still bias that task's own remaining retries within the current session.

**Evidence:**

- `WorkingMemory.clear()` guarantees no cross-turn survival (`memory_store.py:440-446`)
- `ReflectionMemory`'s identity gate and cross-session persistence (`memory_store.py:660-730`) are
  precisely the properties this ephemeral design avoids inheriting
- The original report's own Finding 4 rationale ("a future orchestrator brief would then trust and
  surface") does not apply when the note never leaves the current task's `WorkingMemory` instance

**Implications:**

The design is not risk-free — an agent can still talk itself into a wrong self-correction within a
single task — but it does not reopen the specific threat model (poisoned cross-session, cross-agent
persistent memory) Finding 4 of the original report was built to close. This distinction is the
basis for recommending the loop proceed without requiring the same investigator-gated write path,
while still requiring Dr. Wieczorek's adversarial review of the narrower, remaining risk before
activation.

---

## Analysis

### Interpretation of Findings

The CEO's observation names a real and previously disclosed gap: the Reflexion system as shipped
implements Reflect→Persist but not Execute→Monitor→Evaluate→Reflect within a single task. Closing it
does not require new infrastructure so much as **wiring existing infrastructure together**: the
Monitor half (`error_boundary.py`'s retry/circuit-breaker signals, `SwarmConfig`'s variance
tracking) already exists; the Reflect-storage half (`WorkingMemory.add_note()`) already exists; what
is missing is (a) an Evaluate step that judges output against `SubTask.gate_criteria`, and (b) the
loop that connects Evaluate's failure verdict to a `WorkingMemory.add_note()` call and a bounded
retry. This is consistent with this laboratory's governance requirement to build on established
CC-00 patterns rather than inventing ad hoc mechanisms.

### Trade-offs Identified

| Decision                                                                      | Benefit                                                                                                  | Cost                                                                                                                                                             |
| ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ephemeral `WorkingMemory`-scoped loop, not an extension of `ReflectionMemory` | Recovers Reflexion's tight retry-loop benefit without reopening the persisted write-tool decision        | A second, structurally distinct "reflection" concept now exists in the module — must be clearly documented as never promoted automatically to persistent storage |
| Reuse `error_boundary.py`/`SwarmConfig` signals as Monitor, add only Evaluate | No duplicate monitoring logic; stays consistent with harness-engineering's existing reliability patterns | Evaluate's judgment quality is bounded by `gate_criteria`'s specificity — vague criteria produce a weak Evaluator                                                |
| Bounded retries (reuse `retry_with_backoff`'s cap pattern)                    | Prevents runaway self-correction loops burning budget indefinitely                                       | A genuinely hard task may exhaust retries without resolution, same ceiling trade-off the original report accepted for its own investigator-gated write path      |
| No automatic promotion from ephemeral note to persisted `ReflectionRecord`    | Keeps the human-in-the-loop gate on anything durable, per Finding 4                                      | A genuinely valuable within-task lesson is lost once `WorkingMemory.clear()` runs, unless a human investigator separately chooses to log it                      |

### Risks and Limitations

- This design has not yet been benchmarked against Reflexion's own reported numbers (91% pass@1 vs.
  GPT-4's 80% baseline on HumanEval, Shinn et al., 2023) on a representative CC-00 task — assigned to
  Dr. Nwosu-Chen as a Next Step, not yet executed.
- `SubTask.gate_criteria` is currently an unused, unstructured `list[str]` field — its adequacy as an
  Evaluator's judgment basis is unvalidated until a real Evaluate step is implemented and tested
  against it.
- The narrower within-session risk identified in Finding 4 (an agent's own reflection biasing its
  own subsequent retries) has not yet been adversarially tested; Dr. Wieczorek's review is a
  prerequisite for activation, not yet performed.

---

## Recommendations

### Primary Recommendation

**Add an opt-in Execute→Monitor→Evaluate→Reflect loop to `SwarmOrchestrator`, scoped entirely to
`WorkingMemory` and never touching `ReflectionMemory`/`memory_reflection`.** Concretely: (1) Execute
— unchanged, existing `SubTask` dispatch; (2) Monitor — reuse `error_boundary.py`'s
`retry_with_backoff`/`CircuitBreaker` and `SwarmConfig.variance_threshold` for fault/timeout/duration
signals, no new code; (3) Evaluate — a new step that judges the `SubTask` result against its existing
`gate_criteria` field and returns pass/needs-reflection; (4) Reflect — on a needs-reflection verdict,
call `WorkingMemory.add_note()` with the Evaluator's verbal critique and feed
`to_context_string()`'s output into the retried attempt's prompt, bounded by a fixed retry cap
mirroring `retry_with_backoff`'s existing pattern. Never write to `ReflectionMemory` from this loop;
promotion of a within-task lesson to a persisted `ReflectionRecord` remains a separate, human
investigator decision, unchanged from the original report's Finding 4.

### Secondary Recommendations

1. **Dr. Wieczorek adversarial review before activation** — targeting the narrower within-session
   self-bias risk identified in Finding 4, mirroring the review the persistent system already
   underwent.
2. **Dr. Nwosu-Chen benchmarking pass** — validate that the design recovers a measurable share of
   Reflexion's reported retry-loop benefit on a representative CC-00 task, before treating the
   design as proven rather than architecturally plausible.
3. **Document as a named pattern** in `multi-agent-engineering/patterns/` once implemented, so future
   orchestrator work does not reinvent this loop or conflate it with the persisted reflection system.

### Implementation Priority

| Recommendation                                                    | Priority | Effort   | Impact                                                      |
| ----------------------------------------------------------------- | -------- | -------- | ----------------------------------------------------------- |
| Evaluate step wired to `SubTask.gate_criteria`                    | P0       | 2 days   | High — the actual missing mechanism                         |
| Reflect step via `WorkingMemory.add_note()` + bounded retry       | P0       | 1–2 days | High                                                        |
| Dr. Wieczorek adversarial review of within-session self-bias risk | P0       | 1–2 days | High (risk mitigation, required before activation)          |
| Dr. Nwosu-Chen benchmarking pass vs. Reflexion's reported numbers | P1       | 2–3 days | Medium (validates design, not required for safe activation) |
| Pattern documentation in `multi-agent-engineering/patterns/`      | P2       | 4 hours  | Medium                                                      |

### Next Steps

1. Present this Programme's full documentation set — this report, the deployment plan
   (`supporting/01-deployment-and-implementation-plan.md`), the technical specification
   (`supporting/02-technical-specification.md`), and the system overview
   (`supporting/03-reflexion-system-overview.md`) — to the CEO for sign-off (User Approval Gate).
2. On approval, open an implementation task against
   `multi-agent-engineering/implementations/swarm_orchestrator.py` per the deployment plan's
   phased rollout (Evaluate step, Reflect step and bounded retry, adversarial review, gradual
   enablement, pattern documentation).
3. Dr. Wieczorek's adversarial review (deployment plan Phase 3) must complete and pass before the
   loop is enabled for any task, including pilot.
4. Dr. Nwosu-Chen's benchmarking pass (deployment plan Phase 4) validates the design against
   Reflexion's reported retry-loop benefit once a pilot implementation exists to test.

---

## References

### Internal Documentation

- `core-component-00/telescope/2026-07-14-reflexion-memory-system/research-report.md` — the parent
  Programme this investigation directly follows up on (Open Question 4)
- `core-component-00/engineering/context-engineering/implementations/memory_store.py` —
  `WorkingMemory` (line 380), `ReflectionMemory`/`ReflectionRecord` (from line 450/624)
- `core-component-00/engineering/harness-engineering/implementations/error_boundary.py` —
  `retry_with_backoff`, `SafeModelCall`, `CircuitBreaker`
- `core-component-00/engineering/multi-agent-engineering/implementations/swarm_orchestrator.py` —
  `SwarmConfig`, `SubTask`
- `crew/director/elias-vance/agent/profile.md`; `crew/CLAUDE.md` (Laboratory Roster, Activation
  Protocol)
- `supporting/06-pilot-data-schema-assessment.md` — Dr. Nwosu-Chen's assessment of why
  `2026-08-01-reflexion-bridge-to-real-dispatch`'s three real pilot data points don't yet satisfy
  this Programme's own `05-benchmarking-methodology.md` (added 2026-08-03)
- `supporting/07-surface-a-native-benchmarking-methodology.md` — Dr. Nwosu-Chen's Option A
  methodology, commissioned by Dr. Vance 2026-08-03, scoped to Surface A's actual data shape
  (added 2026-08-03)
- `core-component-00/telescope/2026-08-01-reflexion-bridge-to-real-dispatch/` — the bridge
  Programme whose Surface A pilot produced the three data points assessed above

### External Sources

- Shinn et al., "Reflexion: Language Agents with Verbal Reinforcement Learning" (NeurIPS 2023;
  arXiv:2303.11366) — cited by reference from the parent report's bibliography
  (`2026-07-14-reflexion-memory-system/supporting/00-sources-and-references.md`); not re-retrieved
  fresh in this investigation

- `supporting/01-deployment-and-implementation-plan.md` — deployment scheme and implementation
  plan (this Programme's own supporting document)
- `supporting/02-technical-specification.md` — the Execute-Monitor-Evaluate cycle's own
  operational mechanism, dynamic-Monitor-allocation recommendation, user-facing feedback, and the
  GATE_FAILED handoff (this Programme's own supporting document)
- `supporting/03-reflexion-system-overview.md` — Mermaid flowchart and whole-system explanation of
  how the persisted and ephemeral reflection mechanisms relate (this Programme's own supporting
  document)
- `supporting/04-state-based-decision-logic.md` — consolidated `SubTask` state model, full decision
  map, and pass/fail criteria for every decision point in the cycle (this Programme's own
  supporting document)
- `supporting/implementation-tracking/` (`progress.md`, `session-log.md`, `checkpoint.json`) —
  live oversight and progress-monitoring records for this Programme's implementation stage,
  reusing the pattern from `2026-07-13-mcp-embedder-service-redesign`
- `meeting/2026-07-29-implementation-readiness-planning.md` — Dr. Vance and the cc00 team's meeting
  minutes resolving a concrete follow-through path for Open Question 2 and the three Gate items
  (this Programme's own meeting record)
- `supporting/05-benchmarking-methodology.md` — Phase 4 pilot category selection (Dr. Farouk) and
  Dr. Nwosu-Chen's benchmarking methodology; defines what will be measured once the pilot produces
  real usage data (this Programme's own supporting document)

### Related Work

- `2026-07-14-reflexion-memory-system` — the parent Programme; this report closes its Open Question 4

---

## Open Questions

Five open questions were originally recorded here. On 2026-07-29, the CEO authorized Dr. Vance and
the cc00 team to resolve every open item within CC-00's own engineering authority — this section
records those decisions where a real decision was possible, and states plainly where one wasn't.

1. **Does `SubTask.gate_criteria` as currently defined (an unstructured `list[str]`) provide enough
   structure for a reliable Evaluator judgment, or does it need a more formal schema?**
   **Decision (2026-07-29):** No schema change. `gate_criteria` stays `list[str]` — introducing a
   new dataclass now would be speculative structure ahead of any real usage. Instead, a single
   authoring convention is adopted: each `gate_criteria` entry must be one independently-checkable
   statement, not a compound sentence bundling multiple conditions — this is what makes § 5's
   per-item checklist rollup (Open Question 5, below) actually meaningful. Encoded as a docstring
   requirement on `evaluate_subtask_result()`, not a runtime validator, at Phase 1.
   Status: Resolved.
   Priority: Medium
   Assigned: Dr. Farouk, to encode the convention at Phase 1 implementation.

2. **What retry cap best balances recovering Reflexion's benefit against runaway token/time cost?**
   **Decision (2026-07-29):** Partially resolved, and no amount of delegated authority closes the
   rest of it. The committed starting value is `max_reflection_retries = 2` (already in
   `supporting/01-deployment-and-implementation-plan.md` Phase 2 § 1) — that stands as the Phase 1
   default. Whether 2 is actually the _right_ number is an empirical question about recovered
   pass-rate versus cost that only real measurement can answer; it is not decided here and is not
   something authority can substitute for data.
   Status: Default committed. The implementation and the benchmarking methodology
   (`supporting/05-benchmarking-methodology.md`) are both now in place; the pilot category is
   selected (single-module backend test-verification `SubTask`s). Final tuning is blocked only on
   real usage accumulating from that pilot — no remaining decision or code stands between here and
   an answer, just time and real traffic.
   Priority: Medium
   **Update (2026-08-03):** The measurement path itself is now decided — Dr. Nwosu-Chen's
   `supporting/07-surface-a-native-benchmarking-methodology.md` (M2, "Attempts-to-Pass
   Distribution") is the specific test this will run under, with a stated floor of 10 real
   dispatches that fail-then-retry. That floor is currently unmet (0 qualifying dispatches — the
   Reflect/retry path has never been exercised in real data). The retry-cap default therefore
   remains unresolved for the same reason as before: no amount of authority substitutes for the
   data.
   Assigned: Dr. Amara Nwosu-Chen, once the pilot has produced ≥ 10 real dispatches that retry at
   least once (doc 07 § 2, M2).

3. **Should this loop extend to Company/Studio pipeline stage retries, or remain scoped to CC-00
   multi-agent orchestration?**
   **Decision (2026-07-29):** Closed. Stays scoped to CC-00 multi-agent orchestration only. If
   Company or Studio wants equivalent capability, that requires its own commissioned Programme
   through the relevant department, per `telescope/CLAUDE.md`'s department-scope rule — this
   Programme does not extend itself into another department's pipeline by default.
   Status: Resolved — closed, no extension planned.
   Priority: Low
   Assigned: N/A — closed.

4. **Does `SwarmOrchestrator.execute()` need a distinct `SUPERVISOR_WORKER` execution path?**
   `swarm_orchestrator.py`'s dispatch table currently routes `ROUTER` and `SUPERVISOR_WORKER`
   through the `HYBRID` executor by default — a precondition for the multi-operator,
   multi-regulator routing described in `supporting/03-reflexion-system-overview.md` § 3.
   **Decision (2026-07-29):** The code gap itself isn't closed by a decision — it still needs
   implementation work when it's needed. What's resolved is _whether it blocks this Programme now_:
   it doesn't. Phases 1–4 pilot at ordinary `FORK_JOIN`/`HYBRID` scale, which doesn't require it.
   Closing this gap becomes an explicit precondition check gating any future enablement of the loop
   on a `SUPERVISOR_WORKER`-topology swarm specifically — not a blocker before that.
   Status: Resolved (scope/sequencing decision); the underlying code gap remains open by design,
   deferred to first real need.
   Priority: Medium
   Assigned: Dr. Farouk, only when a `SwarmPlan` first needs supervisor-level `GATE_FAILED`
   routing.

5. **Does `passed=True` require every `gate_criteria` item to check out, or is a partial pass
   (majority/weighted) enough?**
   **Decision (2026-07-29):** Adopted. `passed = True` requires every item in `gate_criteria` to
   check out — a strict AND, not a threshold — for Phase 1. A weighted or partial-credit model is
   explicitly out of scope unless real usage data (once Phase 1 ships) shows the strict-AND rule is
   too brittle in practice; it is not pursued speculatively ahead of that evidence.
   Status: Resolved — adopted as committed design, superseding the "default, not yet confirmed"
   status recorded in `supporting/04-state-based-decision-logic.md` § 5.
   Priority: Medium
   Assigned: Dr. Farouk, to implement per this decision at Phase 1.

6. **Does the shipped implementation's test coverage actually match the D1–D14 decision catalogue,
   or are there decisions on paper with no automated check behind them?**
   **Finding (2026-07-30):** A systematic pass running the full reflection-cycle test surface (73
   multi-agent-engineering + 141 context-engineering reflection tests, 213 passed / 1
   environment-only skip) against `supporting/04-state-based-decision-logic.md`'s D1–D14 catalogue
   found 11 of 14 decisions directly covered. Three gaps: D2 (Monitor budget tiering) has no
   implementation footprint at all — no `MonitorBudget` class exists anywhere in the module; D8
   (final-attempt reflection reframing) is likewise unimplemented — every retry sends an identical
   note regardless of attempt number; D9 (`WorkingMemory.clear()` on every cycle exit) is
   implemented correctly but has no direct assertion in the test suite, only incidental exercise.
   D9 is a genuine coverage gap in already-shipped behavior; D2/D8 were, at the time of this
   finding, recorded design intent that had not yet been built.
   **Update (2026-07-30):** The CEO rejected deferring D2/D8 to a future phase and directed Dr.
   Vance and cc00 lab personnel to implement both now. Both are implemented in
   `swarm_orchestrator.py`: D2 as `MonitorBudget`/`default_monitor_budget()` — duration-tiered
   dispatch timeout only (short/standard/long-running), wired into `_dispatch()`'s
   `asyncio.wait_for`; breaker-sensitivity tiering, the other part of D2's original design intent,
   is explicitly out of scope here — the circuit breaker is caller-injected
   (`set_circuit_breaker()`), so tiering its sensitivity is a harness-engineering change to
   whatever constructs that breaker, not something this module can honestly implement, and is
   logged as its own cross-module follow-up. D8 as `_reflection_note_for_attempt()` — the final
   allowed retry's reflection note now explicitly asks for a genuinely different approach; Dr.
   Nwosu-Chen's benchmarking pass will assess whether it measurably helps, as a validation of a
   shipped default rather than a precondition for building it. D9's gap was closed the same
   session it was found: two new tests (`test_working_memory_cleared_on_completed_exit_after_retry`,
   `test_working_memory_cleared_on_gate_failed_exit`) were added to `TestReflectiveLoop`. D2 and D8
   additionally gained 7 new tests (`TestDefaultMonitorBudget`'s 5 unit tests, one dispatch-level
   wiring test in `TestExecution`, one final-attempt-phrasing test in `TestReflectiveLoop`). Full
   suite re-verified green at 82/82.
   Status: Resolved and implemented. D2's timeout-tiering half and D8 are shipped; D2's
   breaker-sensitivity half is a distinct, explicitly-scoped cross-module item, not a deferral of
   this decision. D9's test-coverage gap is closed.
   Priority: Low (all three now closed or correctly scoped out).
   Assigned: N/A — D2 (timeout half)/D8/D9 closed; D2 (breaker-sensitivity half) owned jointly by
   Dr. Farouk and harness engineering, tracked as its own follow-up item.

7. **Does the D2/D8 implementation itself hold up under independent adversarial review, and is the
   overall reflection-cycle development now complete?**
   **Finding (2026-07-30):** Per CEO directive, Dr. Wieczorek conducted a secondary adversarial
   review of the D2/D8 modifications. Two real findings: (1) `default_monitor_budget()`'s
   long-running tier had no upper ceiling — a very large `estimated_duration` (legitimate or a
   units mistake) produced an unbounded timeout, defeating the Monitor budget's own purpose; fixed
   same-day with `_LONG_RUNNING_TIMEOUT_CEILING_SECONDS` (3600s), which never pulls the timeout
   below the caller's configured base. (2) The new dispatch-wiring test used a 10ms margin between
   its tiered timeout and its execute_fn's sleep — a CI-flakiness risk; widened to 160ms. One
   negative result documented with equal rigor: checked whether the executing agent could
   self-inflate its own `estimated_duration` mid-run to buy extra time — it cannot,
   `estimated_duration` is fixed at plan-construction time and nothing in the dispatch path writes
   back to it. One non-blocking design observation: a short-tier task's final, reframed retry
   (D8) still runs under that same short tier's tight timeout (D2) — a real tuning question left
   for Dr. Nwosu-Chen's benchmarking pass rather than an invented threshold today. 2 new tests
   added for the ceiling fix; full suite re-verified green at 84/84 multi-agent-engineering + 102
   context-engineering reflection tests (1 environment-only skip, unchanged).
   Status: Resolved. Both real findings fixed and verified same-day; the negative result and the
   design observation are documented per Dr. Wieczorek's standard rather than left silent. The
   reflection-cycle development this Programme scoped is now complete: Phases 1–3 shipped and
   reviewed, D2 (timeout half)/D8/D9 shipped and re-reviewed, D2 (breaker-sensitivity half) is an
   explicitly-scoped follow-up rather than an unfinished part of this Programme's own scope.
   Priority: N/A — closed.
   Assigned: N/A — closed.

---

## Version History

| Version | Date       | Author                                | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------- | ---------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-07-28 | Dr. Elias Vance                       | Initial research report completed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 1.1     | 2026-07-28 | Dr. Elias Vance                       | Added `supporting/01-deployment-and-implementation-plan.md`; investigation converted from Simple to Programme shape                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 1.2     | 2026-07-28 | Dr. Elias Vance                       | Added `supporting/02-technical-specification.md` (cycle mechanism, dynamic Monitor allocation, user-facing feedback, `GATE_FAILED` handoff)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 1.3     | 2026-07-28 | Dr. Elias Vance                       | Extracted the system-wide diagram and the persisted-vs-ephemeral relationship into new `supporting/03-reflexion-system-overview.md`; `02-technical-specification.md` now covers only the cycle's own mechanism                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 1.4     | 2026-07-28 | Dr. Elias Vance                       | Final-draft editorial pass across all four Programme documents — prose and structure only, no technical content changed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 1.5     | 2026-07-28 | Dr. Elias Vance                       | Added activation criteria (`02-technical-specification.md` § 5) and multi-operator/multi-regulator scaling design (`03-reflexion-system-overview.md` § 3); added Open Question 4 (`SUPERVISOR_WORKER` dispatch gap)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 1.6     | 2026-07-28 | Dr. Elias Vance                       | Folded the § 1.5 additions into `supporting/01-deployment-and-implementation-plan.md`'s Phase 1 (default activation policy), Phase 2 (`GATE_FAILED` aggregation in `SwarmResult.feedback`), and Phase 4 (pilot category tied to the default-enabled tier; supervisor/regulator routing scoped out of the pilot); no new phases                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 1.7     | 2026-07-28 | Dr. Elias Vance                       | Added `supporting/04-state-based-decision-logic.md` — consolidated `SubTask` state model, full decision map (D1–D14), and pass/fail criteria; added Open Question 5 (`gate_criteria` AND-vs-threshold aggregation, previously unspecified)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 1.8     | 2026-07-29 | Dr. Elias Vance                       | Under CEO-delegated authority, resolved Open Questions 1, 3, 4, and 5 as committed decisions and confirmed Open Question 2's provisional default (final tuning still blocked on benchmarking data); recorded Dr. Wieczorek's Phase 3 adversarial review — CONDITIONAL PASS, two required mitigations folded into `01-deployment-and-implementation-plan.md` Phase 1/2; Dr. Nwosu-Chen's benchmarking pass and CEO sign-off remain explicitly unresolved, not something delegated authority can substitute for                                                                                                                                                                                                                                                                                                                                      |
| 1.9     | 2026-07-29 | Dr. Elias Vance                       | Added `meeting/2026-07-29-implementation-readiness-planning.md` — Dr. Vance convened Asante, Nwosu-Chen, Wieczorek, and Farouk to plan concrete follow-through on OQ2 and the three Gate items; committed to Phase 2 retry-count instrumentation, a post-implementation Wieczorek spot-check to convert CONDITIONAL PASS to PASS, and a pre-Phase-4 benchmarking methodology note; recommends CEO sign-off proceed on the current documentation set, with these as in-flight commitments, not preconditions                                                                                                                                                                                                                                                                                                                                        |
| 1.10    | 2026-07-29 | Dr. Elias Vance                       | CEO approved the meeting outcomes and delegated full implementation responsibility to Dr. Vance and the cc00 lab; `01-deployment-and-implementation-plan.md` updated with a second-presentation personnel and parallel-work feasibility assessment (§ 0.1) — Phase 1→2 confirmed as one sequential critical-path chain, Asante's counter-independence test and Nwosu-Chen's methodology note confirmed as genuinely parallelizable alongside it; final go/no-go on starting Phase 1 explicitly still pending CEO review of this second presentation                                                                                                                                                                                                                                                                                                |
| 1.11    | 2026-07-29 | Dr. Elias Vance                       | Confirmed no oversight/progress-monitoring mechanism existed for this Programme, a genuine gap; established `supporting/implementation-tracking/` (`progress.md`, `session-log.md`, `checkpoint.json`), reusing the pattern from `2026-07-13-mcp-embedder-service-redesign` rather than inventing a new one; added `01-deployment-and-implementation-plan.md` § 0.3 documenting it, including the precedent's own cautionary lesson about maintaining it live rather than compiling it after the fact                                                                                                                                                                                                                                                                                                                                              |
| 1.12    | 2026-07-29 | Dr. Elias Vance                       | CEO granted go-ahead; Phases 1–2 and Phase 2's conformance test implemented for real in `swarm_orchestrator.py` (`EvaluationVerdict`, `evaluate_subtask_result()`, `default_gate_criteria_tier()`, the Reflect/bounded-retry loop, `GATE_FAILED` aggregation, retry-count telemetry), with 27 new tests (73/73 total green in multi-agent-engineering). Dr. Wieczorek's Phase 3 spot-check converted CONDITIONAL PASS to **PASS** — both required mitigations confirmed present in the shipped code/tests. Phase 4 scaffolding (`enable_reflective_loop`, off by default) done; the real pilot/benchmarking pass and Phase 5 documentation explicitly left undone, not fabricated. Discovered and flagged (not fixed, out of scope) pre-existing, unrelated test failures in harness-engineering and context-engineering that predate this session |
| 1.13    | 2026-07-30 | Dr. Elias Vance                       | Per CEO request, ran systematic usability testing of the full reflection cycle (213 tests passed, 1 environment-only skip) and cross-checked coverage against every D1–D14 decision; added Open Question 6 documenting the result — 11/14 decisions directly covered, D2/D8 correctly deferred by design, D9 flagged as a genuine test-coverage gap (behavior correct, no direct assertion) and found and immediately closed a genuine D9 test-coverage gap (`WorkingMemory.clear()` had no direct assertion) with two new tests, full suite re-verified at 75/75 green                                                                                                                                                                                                                                                                            |
| 1.14    | 2026-07-30 | Dr. Elias Vance                       | CEO rejected deferring D2/D8 to a future phase; directed implementation now. Implemented D2's timeout-tiering half (`MonitorBudget`, `default_monitor_budget()`, wired into `_dispatch()`) and D8 (`_reflection_note_for_attempt()`) in `swarm_orchestrator.py`; D2's breaker-sensitivity half scoped out as a distinct cross-module item owned jointly with harness engineering, not a deferral. Added 7 new tests; full suite green at 82/82                                                                                                                                                                                                                                                                                                                                                                                                     |
| 1.15    | 2026-07-30 | Dr. Elias Vance                       | Per CEO directive, Dr. Wieczorek conducted a secondary adversarial review of the D2/D8 modifications (Open Question 7). Two real findings fixed same-day: uncapped long-running timeout multiplier (added `_LONG_RUNNING_TIMEOUT_CEILING_SECONDS`), flaky 10ms test margin (widened to 160ms). One negative result documented (estimated_duration is not agent-influenced, confirmed clean) and one non-blocking design observation logged (D8 reframing under D2's tight short-tier budget). 2 new tests; full suite green at 84/84 multi-agent-engineering + 102 context-engineering. Updated Metadata Status to reflect actual current state                                                                                                                                                                                                    |
| 1.16    | 2026-07-30 | Dr. Elias Vance                       | Per CEO approval, moved on the next concrete action: added `supporting/05-benchmarking-methodology.md` recording Dr. Farouk's Phase 4 pilot category selection (single-module backend test-verification `SubTask`s) and Dr. Nwosu-Chen's benchmarking methodology (what will be measured, comparison design, the harder D8-specific comparison left as an open decision pending real volume). No results exist yet — this defines what will be measured once the pilot accumulates real usage, not a completed benchmarking pass. Updated Open Question 2's status accordingly                                                                                                                                                                                                                                                                     |
| 1.17    | 2026-08-03 | Dr. Amara Nwosu-Chen, Dr. Elias Vance | Per CEO direction to begin the Phase 4 benchmarking pass using the three real pilot data points from `2026-08-01-reflexion-bridge-to-real-dispatch`, Dr. Nwosu-Chen assessed them against `05-benchmarking-methodology.md` first, per her own falsifiability standard. Found a structural schema mismatch, not a sampling issue: Surface A bypasses `SwarmOrchestrator.execute()` entirely, so none of this methodology's stated data sources exist for those three runs. Added `supporting/06-pilot-data-schema-assessment.md`. **The Phase 4 benchmarking pass has not begun** — flagged honestly rather than treating three schema-mismatched data points as a start. Two paths forward proposed, decision reserved for Dr. Vance                                                                                                               |
| 1.18    | 2026-08-03 | Dr. Amara Nwosu-Chen, Dr. Elias Vance | Per CEO delegation of full decision authority back to Dr. Vance and the cc00 lab, with direction to take a long-term robustness view: decided Option A (Surface-A-native methodology) over Option B (wait for a `SwarmOrchestrator.execute()` caller). Added `supporting/07-surface-a-native-benchmarking-methodology.md` — three falsifiable metrics (Evaluator agreement rate, attempts-to-pass distribution, rationale actionability), each with a stated minimum-sample floor, none currently met. Commissions the methodology only, not a benchmarking result; authorizes no new pilot dispatches. `05-benchmarking-methodology.md` retained unchanged for whenever a real `SwarmOrchestrator.execute()` caller exists. Updated Open Question 2 and Metadata Status accordingly                                                               |

---

**Template Version:** 1.0
**Last Updated:** 2026-07-28
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
