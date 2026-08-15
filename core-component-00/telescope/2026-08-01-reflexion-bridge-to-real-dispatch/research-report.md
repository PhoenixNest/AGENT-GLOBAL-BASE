# Research Report — Bridging the Execute-Monitor-Evaluate-Reflect Loop to Real Dispatch

---

## Metadata

| Field                | Value                                                                                                                                                                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Investigation ID** | `2026-08-01-reflexion-bridge-to-real-dispatch`                                                                                                                                                                                     |
| **Date Started**     | 2026-08-01                                                                                                                                                                                                                         |
| **Date Completed**   | In Progress — Phases 1–3 complete (2026-08-02); Phase 4 pilot (3 real runs) merged 2026-08-03; both real P2 findings from the pilot fixed and verified 2026-08-03 (129/129 green); long-term robustness decisions recorded (v1.10) |
| **Status**           | In Progress — pilot branches merged; two real findings fixed; benchmarking methodology (Option A) commissioned but not yet run; zero-live-caller architecture question deferred as a future research item, not solved here         |
| **Investigator**     | Dr. Elias Vance (Laboratory Director, Principal Investigator)                                                                                                                                                                      |
| **Laboratory**       | Core Component 00                                                                                                                                                                                                                  |
| **Module(s)**        | Multi-Agent Engineering (`swarm_orchestrator.py` decision logic) × Harness Engineering (hook-mechanism risk classification) × the workspace's own Claude Code configuration surface (`.claude/agents/multi-agent-orchestrator.md`) |
| **Priority**         | High                                                                                                                                                                                                                               |
| **Requestor**        | CEO                                                                                                                                                                                                                                |

**Executing engineers:** Dr. Idris Farouk with Amina Yusuf (Multi-Agent Engineering — adapter
design, since the loop's decision logic lives in `swarm_orchestrator.py`, a module Farouk owns);
Kwame Asante (Harness Engineering — hook-mechanism risk classification, consulted per his existing
conformance-review role on this loop); Dr. Tomasz Wieczorek (Staff Safety & Evaluation Engineer —
flags scope of required future review; does not conduct one yet, since no code exists);
Dr. Amara Nwosu-Chen (Staff Research Scientist — sampling-frame caveat for her downstream Phase 4
benchmarking pass). Assignments follow `crew/CLAUDE.md`'s Laboratory Roster and Activation
Protocol.

---

## Executive Summary

Following the CEO's 2026-08-01 question of whether the `2026-07-28-reflexion-execute-monitor-
evaluate-loop` Programme should be integrated into the current Claude Code configuration for
real-world evaluation, this investigation found that Phases 1–3 of that Programme, though fully
shipped and adversarially passed, have **zero live callers anywhere in this workspace** —
`SwarmOrchestrator(` is instantiated only in test files and pattern documentation, never in
`.claude/`. Phase 4's pilot plan implicitly assumed a real dispatch path would exist by the time
piloting started; none does. A deeper architectural fact sharpens the gap further: `execute_fn`'s
only shipped implementation (`_default_execute`) returns a canned literal, and Python code in this
workspace has no capability to invoke the Agent/Task tool — that is a host-level primitive
available only to the assistant turn issuing it. **`SwarmOrchestrator.execute()` therefore cannot
itself drive real subagent dispatch, by construction, not merely by missing configuration.** We
recommend a narrower, achievable bridge instead: expose the loop's Evaluate/Reflect decision logic
(`evaluate_subtask_result()`, reflection-note construction, retry-count bookkeeping) as a
`uv run`-invokable helper script — the same cross-platform invocation convention this workspace
already standardized on for `.claude/hooks/*.py` (`2026-07-30-cross-platform-config-automation`) —
that the existing `multi-agent-orchestrator` subagent's own real worktree-dispatch workflow
consults between real Agent-tool dispatches — advisory, opt-in, and explicitly not yet
structurally enforced via a `.claude/hooks/*.py` gate, which is scoped out here pending its own
future review.

> **Correction (2026-08-02):** v1.0 of this report specified the helper as "Bash-invokable,"
> reintroducing the exact OS-fork problem `2026-07-30-cross-platform-config-automation` closed for
> `.claude/hooks/*.py` — a plain oversight, not an intentional deviation; see Finding 6 and the
> corrected Recommendations, below.

> **Implementation Update (2026-08-02):** The CEO approved `supporting/implementation-plan.md` and
> endorsed the Option-3 (Workflow-tool) design discussed separately as a later-round candidate, then
> authorized Phase 1–2 to begin. `reflective_dispatch_helper.py` now exists
> (`multi-agent-engineering/implementations/`), built exactly to the request/response contract
> `supporting/usage-cookbook.md` § 2 specified, wrapping the unmodified `evaluate_subtask_result()`/
> `_reflection_note_for_attempt()`. Its test suite (22 tests — passing/failing verdict passthrough,
> reflection-note formatting, retry-cap accounting, malformed-input handling, the never-raises
> degrade path, and a real `uv run` subprocess round-trip) is green, and the full
> multi-agent-engineering suite remains green at 106/106 (84 pre-existing + 22 new), confirming no
> regression to Phase 1–3 code from the parent Programme. `.claude/agents/multi-agent-orchestrator.md`
> has been updated per the Phase 2 diff (Execute-phase documentation only — Hard Constraints, Agent
> Roles, and the other four phases are unchanged; self-reviewed by Dr. Vance for scope creep, per
> `implementation-plan.md` Phase 2's gate). No pilot data exists yet. See
> `supporting/implementation-plan.md`'s updated Deployment Checklist and Version History (v1.5) for
> the full status.

> **Phase 3 Update (2026-08-02):** Kwame Asante conducted the invocation-contract conformance
> review and recorded a **PASS**, after finding and fixing two required issues same-day: (1) the
> helper had no structured stderr logging on its degrade paths, unlike `error_boundary.py`'s own
> `log_warning` convention he owns — fixed by adding a matching `_log_warning()` that logs to
> stderr while keeping stdout pure JSON; (2) `multi-agent-orchestrator.md`'s Execute-phase
> documentation did not say what to do if the `uv run` invocation itself produces no well-formed
> JSON at all (as opposed to a well-formed degrade response) — fixed with one added clause stating
> that case must be treated identically to a `passed: true` degrade. Retry-count independence from
> `error_boundary.py`'s fault-retry counters was confirmed with no fix needed (the helper carries no
> internal retry state of its own). 3 new fault-injection tests added; full suite green at
> **109/109**. Full verdict recorded in `supporting/implementation-plan.md` § Phase 3. **Phase 4
> (the pilot) is now unblocked** — not yet started; no pilot data exists yet. See
> `supporting/implementation-plan.md` Version History (v1.2) for the full status.

> **Phase 4 Update (2026-08-03):** Added the invocation-counter telemetry (Phase 4 § 2) and ran the
> first real pilot dispatch end to end — a real `cc00-implementation-assistant` Executor, dispatched
> via the Agent tool inside its own git worktree, on the already-selected pilot domain
> (single-module backend test-verification subtasks): new realistic-transcript tests for
> `evaluate_subtask_result()`'s narrative-fallback path (Open Question 2). Every piece of evidence
> the Supervisor used was independently re-verified in the worktree, not taken from the Executor's
> own report. The real `uv run` Evaluate call returned `passed: true` on attempt 1 — no retry was
> needed for this run — and the telemetry file recorded exactly one matching entry. The pilot's own
> tests surfaced a real, previously-undetected P2 finding in the narrative-fallback path (a
> negation-blindness false positive: a sentence explicitly _denying_ a criterion can still score
> `passed=True`) — logged for Dr. Wieczorek, not fixed here, consistent with this Programme's
> explicit scope boundary (`evaluate_subtask_result()` is unmodified, out of scope). Full record:
> `supporting/pilot/pilot-run-01.md`. Dr. Vance's Phase 4 gate review: one real data point is a genuine
> success but not enough to recommend expanding past the pilot domain — continue accumulating runs.
> See `supporting/implementation-plan.md` Version History (v1.3) for the full status.

> **Phase 4 Update 2 (2026-08-03):** Per CEO direction, ran two more real pilot cycles, dispatched
> in parallel (separate worktrees, separate files, no shared state) — run 02 (`HandoffPacket`
> cross-fleet `conversation_history` validation) and run 03 (`SharedMemoryLog` TTL/expiry logic),
> both real, previously zero-coverage code paths. Both independently re-verified exactly as run 01
> was, and both passed on attempt 1. Combined three-run summary:
>
> | Run | Task                                           | Attempts to pass | Retry exercised? | P2 finding logged                               |
> | --- | ---------------------------------------------- | ---------------- | ---------------- | ----------------------------------------------- |
> | 01  | `evaluate_subtask_result()` narrative fallback | 1                | No               | Negation-blindness false positive               |
> | 02  | `HandoffPacket` cross-fleet validation         | 1                | No               | `fleet_id`-omission silently bypasses the check |
> | 03  | `SharedMemoryLog` TTL/expiry                   | 1                | No               | None (documented boundary behavior, not a bug)  |
>
> Invocation telemetry: 3/3 real records, all `passed: true`, all `degraded: false` — the
> counter is working correctly. **Honest reading of this data:** three for three on the first
> attempt is a genuinely good sign for the Executor/Supervisor/Evaluator mechanics working
> end-to-end, but it means the Reflect/bounded-retry half of this loop — the actual point of the
> parent Programme's "reflexion" design — has **not yet been exercised for real, at all**, across
> any of the three runs. That is not something to force artificially (an engineered failure would
> not be real data), but it is a real, honestly-reported gap in what these three runs can tell
> Dr. Nwosu-Chen: real attempts-to-pass distribution data exists (uniformly 1), but real retry
> behavior does not yet. Run 02's independent re-verification also caught a small Executor
> self-reporting discrepancy (claimed 6 new tests, wrote and delivered 5) — logged as a
> data-quality note in `pilot-run-02.md`, not a defect, and a live demonstration of why the
> Supervisor independently checks evidence rather than trusting the Executor's narrative. Full
> records: `supporting/pilot/pilot-run-02.md`, `supporting/pilot/pilot-run-03.md`. See
> `supporting/implementation-plan.md` Version History (v1.4) for the full status.

> **Phase 4 Update 3 (2026-08-03):** Per CEO direction, the three pilot worktree branches were
> merged into `core00/dev/engineering` (`--no-ff`, no conflicts — the three runs touched disjoint
> files) and the worktrees cleaned up; full suite re-verified green at 129/129 post-merge. The
> main workspace's own pending changes (the helper, its tests, the `multi-agent-orchestrator.md`
> diff, this Programme's documentation) remain uncommitted, per explicit CEO instruction not to
> commit them yet. Separately, two crew members were activated to continue the CEO's next-steps
> items: **Dr. Nwosu-Chen** assessed the three pilot data points against the parent Programme's
> benchmarking methodology and found they don't fit its data schema — full assessment cross-linked
> in the parent Programme (`2026-07-28-.../supporting/06-pilot-data-schema-assessment.md`), not
> duplicated here. **Dr. Wieczorek** independently triaged the three P2 findings this pilot
> surfaced: the narrative-negation-blindness finding (run 01) and the `HandoffPacket`
> `fleet_id`-omission finding (run 02) are both real and open, with fixes recommended for Dr.
> Farouk (neither is currently exploitable on the primary evidence path — Finding 1 requires the
> already-discouraged narrative-only fallback, and Finding 2's `validate()` has zero live callers
> anywhere in production code, the same zero-live-caller pattern this Programme's own Finding 1
> established for `SwarmOrchestrator`); the TTL boundary observation (run 03) is closed as
> informational, not a safety finding. Full triage: `supporting/pilot/wieczorek-triage-01.md`.

> **Phase 5 Update (2026-08-03) — Robustness Decisions:** The CEO returned full decision-making
> authority to Dr. Vance and the cc00 lab, directing a long-term view on strengthening the
> reflection system. Three decisions, made and recorded here:
>
> **1. Both open Wieczorek findings fixed and verified same-day.** `_criterion_satisfied()`'s
> narrative fallback now applies a bounded negation-detection heuristic
> (`_phrase_asserted_in_narrative()`, a fixed-window scan for a small negation-cue vocabulary
> immediately before each substring match) — closes Finding 1 without adding an NLP dependency;
> documented as a bounded heuristic, not general language understanding.
> `HandoffPacket.validate()`'s cross-fleet check now fails closed on a turn missing `fleet_id`
> entirely (flagged as unverified-origin) instead of silently treating it as compliant — closes
> Finding 2. Both reproduction tests (`test_narrative_negated_criterion_text_still_matches_as_substring`,
> renamed `test_turn_missing_fleet_id_flagged_as_unverified_origin`) were inverted to assert the
> corrected behavior and promoted into permanent regression guards, per Dr. Wieczorek's stated
> closure standard. Full multi-agent-engineering suite re-verified green at **129/129** after both
> fixes (same count as before — no tests added or removed, two inverted in place).
>
> **2. The Reflect/retry path's real-data gap is accepted as a known, honestly-tracked limitation,
> not something to force.** Across all 5 real pilot dispatches to date (3 from Phase 4 here, plus
> the two fixes above didn't add new pilot runs), the Reflect/bounded-retry mechanism has never
> once been exercised for real — every run passed on attempt 1. Per this lab's standing practice
> (never manufacture a failure to generate data), no artificial failure will be constructed. This
> gap closes on its own only as real Surface-A volume grows; the parent Programme's
> `supporting/07-surface-a-native-benchmarking-methodology.md` (commissioned the same day, see that
> Programme's Phase 4 Update 2) now states an explicit floor — 10 real dispatches that fail-then-
> retry — before any claim about Reflect effectiveness may be made.
>
> **3. `SwarmOrchestrator.execute()` and `HandoffPacket.validate()` having zero live production
> callers is a real, structural architecture question — bigger than either open Programme, not
> solved here.** Both this Programme's own Finding 1 and Wieczorek's Finding 2 independently
> surfaced the same pattern: real, adversarially-reviewed, fully-tested code with no live caller
> anywhere in `.claude/`. Wiring either one into a real call path is a genuine future design
> decision (what calls `.validate()`, under what authority; what would finally drive real traffic
> through `.execute()` now that Surface A has shown the Agent-tool bridge works for the
> Evaluate/Reflect logic alone) — not a bug fix, and not undertaken here without its own scoping
> and review. Decision: this becomes a standing item for Dr. Nwosu-Chen to consider originating as
> a future research question (her documented role, per `crew/CLAUDE.md`), not commissioned as a
> Programme today. Dr. Farouk is assigned to re-confirm `HandoffPacket.validate()`'s zero-caller
> status before any future work wires it into a real enforcement path, per Wieczorek's own
> precondition framing. No new pilot runs, commits, or merges were authorized or performed as part
> of this update.

---

## Investigation Scope

### What Was Investigated

(1) Why `swarm_orchestrator.py`'s fully-shipped, fully-reviewed Execute-Monitor-Evaluate-Reflect
loop has never been exercised outside pytest; (2) what integration surfaces exist for connecting
real Claude Code multi-agent work to that loop's decision logic, and what each surface can and
cannot actually do given this workspace's architecture; (3) which surface is safe to build first,
consistent with this lab's practice of shipping the lower-risk version and letting real data
justify anything riskier.

### Why This Investigation Was Needed

In the same conversation, Dr. Vance and the cc00 team advised the CEO that the reflexion loop was
real and tested but had no real-world caller, and recommended scoping a "bridge to real dispatch"
task rather than treating integration as a simple activation. The CEO asked for that task drafted
as a formal report. This investigation is that report — it also corrects an assumption made
verbally in that same conversation (that `execute_fn` could be made to "shell out to spawn real
subagents"), which turns out not to be achievable as stated; see Finding 2.

### Out of Scope

- Any change to Phases 1–3's shipped code in `swarm_orchestrator.py`. This investigation adds a
  new, separate adapter; it does not modify the reviewed loop itself.
- Building a live `.claude/hooks/*.py` gate on the Agent/Task tool ("Surface B" below). Identified
  as a candidate, explicitly deferred pending its own adversarial review — not attempted here.
- Any change to `ReflectionMemory`, the persisted write path, or `reflection_bridge.py`'s existing
  read-only wiring to agent-memory. Unrelated boundary, unchanged.
- Dr. Nwosu-Chen's actual benchmarking pass. Downstream of this bridge existing; not run here.

---

## Research Questions

1. Why does `SwarmOrchestrator` have zero live callers despite Phases 1–3 being fully shipped and
   passed?
2. Can `SwarmOrchestrator.execute()` itself be wired to drive real Claude Code subagent dispatch,
   as informally proposed in the prior conversation?
3. What integration surfaces remain once Q2 is answered, and how do they differ in blast radius
   and in what governance review, if any, already covers them?
4. What concrete adapter design lets the existing `multi-agent-orchestrator` subagent's real
   worktree dispatches consult the loop's decision logic with the least new surface area?
5. What is the minimal safe pilot scope, consistent with the parent Programme's already-selected
   pilot category?

---

## Methodology

### Approach

A direct code and configuration audit: (1) grep every `.claude/` file for the loop's own symbols
(`SwarmOrchestrator`, `reflective_loop`, `EvaluationVerdict`, `reflection_bridge`) and every
workspace file for `SwarmOrchestrator(` instantiation, to establish Finding 1; (2) read
`SwarmOrchestrator.__init__`, `_default_execute`, and `evaluate_subtask_result()` directly to
determine what a real caller would actually need to supply; (3) read `reflection_bridge.py` as the
workspace's existing precedent for "real but bounded" wiring; (4) read
`.claude/agents/multi-agent-orchestrator.md` to determine what that subagent actually is
(a system-prompt-driven Claude Code subagent, not a Python caller) and what it can realistically be
asked to do.

### Tools and Resources

- `core-component-00/engineering/multi-agent-engineering/implementations/swarm_orchestrator.py`
  (`SwarmOrchestrator.__init__` at line 387, `_default_execute` at line 648,
  `evaluate_subtask_result()` at line 306)
- `core-component-00/engineering/multi-agent-engineering/implementations/reflection_bridge.py`
  (existing real-wiring precedent)
- `.claude/agents/multi-agent-orchestrator.md` (the real subagent definition)
- `core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`
- Root `CLAUDE.md` § 11 (H-P01's own documented history of the gap between advisory
  `additionalContext` and structural `PreToolUse`/`PostToolUse` enforcement — directly relevant
  precedent for classifying Surface A vs. Surface B below)
- `core-component-00/telescope/2026-07-28-reflexion-execute-monitor-evaluate-loop/` (parent
  Programme, full document set)

### Constraints

- No production code was written during this investigation — this is a design/scoping report,
  consistent with this workspace's stage-gate convention (present, request sign-off, wait).
- Benchmarking design itself is out of scope; only the sampling-frame implication for that future
  work is noted (Risks and Limitations).

---

## Findings

### Finding 1: Zero Live Callers Exist Anywhere in the Workspace, Including `.claude/`

`SwarmOrchestrator(` is instantiated in exactly five files workspace-wide, and every one is a test
file or a documentation reference: `test_swarm_orchestrator.py`, `test_reflection_bridge.py`,
`test_gsm_scope_enforcement.py`, `README.md`, and `patterns/git-coordination.md`. A grep of every
file under `.claude/` for `SwarmOrchestrator`, `reflective_loop`, `EvaluationVerdict`, or
`reflection_bridge` returns zero matches. Phase 4 of the parent Programme's deployment plan reads
as though a real dispatch path would exist by pilot time ("pilot on one narrow, low-stakes
`SubTask` category first"); none does, and none ever has.

**Evidence:**

- `Grep SwarmOrchestrator\( → 5 files, all tests/docs`
- `Grep (SwarmOrchestrator|reflective_loop|EvaluationVerdict|reflection_bridge) under .claude/ → 0 matches`
- `01-deployment-and-implementation-plan.md` Phase 4 § 2 ("pilot on one narrow... category") has no
  stated caller to pilot

**Implications:**

Phase 4 is not blocked on "waiting for traffic." There is no road for traffic to arrive on. This
is the actual, previously unstated precondition the CEO's integration question was really asking
about.

---

### Finding 2: `SwarmOrchestrator.execute()` Cannot Itself Drive Real Subagent Dispatch

`SwarmOrchestrator.__init__` takes `execute_fn` as an injectable callable; its only shipped
implementation, `_default_execute` (`swarm_orchestrator.py:648-649`), returns a canned literal
(`{"status": "completed", "output": f"Result for: {task.description}"}`) regardless of input. This
confirms, by construction rather than by omission, that no real dispatch mechanism has ever been
wired into this module — because none can be, from inside a plain Python process. The Agent/Task
tool that actually spawns a real Claude Code subagent is a host-level primitive available only to
the assistant turn that issues it; it is not an importable capability this workspace's Python code
can call. This directly corrects an assumption voiced in the prior conversation (that `execute_fn`
could "shell out to spawn real subagents") — it cannot, as stated.

**Evidence:**

- `_default_execute` (`swarm_orchestrator.py:648-649`) — literal stub, not a dispatch mechanism
- `evaluate_subtask_result()` (`swarm_orchestrator.py:306-382`) is a deterministic string/
  structured-key matcher against `gate_criteria`, not a model call — confirming the whole module is
  decision-logic scaffolding, never a live executor
- No file in this workspace imports or otherwise references a mechanism for a Python process to
  invoke the Agent/Task tool

**Implications:**

Any real bridge must be inverted from what was informally proposed: instead of `SwarmOrchestrator`
driving real dispatch, the entity that already performs real dispatch — a Claude Code subagent
following its own system prompt — must be the one that calls out to this module's decision logic
as a helper, at checkpoints it already controls.

---

### Finding 3: `reflection_bridge.py` Is the Workspace's Existing Template for "Real but Bounded" Wiring

`reflection_bridge.py` (commit `1b5056e1`) already wires `SwarmOrchestrator.set_reflection_search_fn`
to agent-memory's real `search_memory` core — read-only, deferred-import (paying the heavy-dependency
cost only when actually invoked), and a never-raises degrade-to-`{degraded: true}` contract on any
failure. It predates this Programme (it serves the persisted-reflection read path) and is itself
never called by anything outside tests either — but its _shape_ is the right template: bounded
blast radius, explicit degradation, no new failure-mode class introduced at the call site.

**Evidence:**

- `reflection_bridge.py` docstring and `build_agent_memory_reflection_search_fn()` — explicit
  never-raises, degraded-shape contract
- `wire_reflection_retrieval()` — a one-line convenience binder, the shape a new adapter should
  mirror

**Implications:**

A new bridge should follow this same architectural discipline (deferred import, never raises,
explicit degradation) rather than inventing a new integration style.

---

### Finding 4: Two Candidate Surfaces Exist, With Materially Different Enforcement and Risk

- **Surface A — advisory helper, called from `multi-agent-orchestrator`'s own workflow.** A small
  script exposing `evaluate_subtask_result()` and the reflection-note/retry-count logic as a
  `uv run`-invokable decision aid (see Finding 6) — not a shell script forked by OS. The
  `multi-agent-orchestrator` subagent (`.claude/agents/
multi-agent-orchestrator.md`) already performs real worktree-isolated dispatch via its own
  system prompt; its Phase 2 ("Execute") step could be extended to call this helper after each
  real worker agent completes, using its own judgment about whether to route a given subtask
  through it. This never touches `.claude/hooks/`, `settings.json`, or the live tool-permission
  gate — it is opt-in per invocation, at the same enforcement level as any other command that
  subagent's prompt tells it to run.
- **Surface B — a `.claude/hooks/*.py` `PostToolUse` hook on the Agent/Task tool.** Structurally
  enforced for every real Agent-tool call in every session, the same mechanism class as
  `prompt-gate-enforcer.py` (H-P01) and the rate limiter (H-HE01). This surface _can_ actually see
  and act on real dispatch results directly (a hook receives the tool call and its result over
  stdin JSON), which Surface A cannot guarantee — Surface A only fires if the orchestrating
  subagent's prompt is followed, not because anything forces it to.

**Evidence:**

- `.claude/agents/multi-agent-orchestrator.md` — a system-prompt-driven subagent with a documented
  Execute phase, the natural call site for Surface A
- Root `CLAUDE.md` § 11 — H-P01's own documented history: it was advisory-only via
  `additionalContext` for a period, explicitly noted as a real gap ("cannot force anything by
  itself"), closed only once a structurally-enforced `PreToolUse`/`PostToolUse` hook was actually
  built. Surface A starts at exactly that same advisory-only maturity level H-P01 once had.

**Implications:**

Surface A is lower blast radius and buildable now with no new hook-execution-contract engineering,
but it is not structurally enforced — a real risk this workspace has already lived through once
with H-P01, and should not repeat by pretending Surface A is stronger than it is. Surface B is
higher value (sees every real dispatch, not just what one subagent's prompt chooses to route) but
is a new, higher-risk mechanism class.

---

### Finding 5: Dr. Wieczorek's Existing PASS Verdict Does Not Cover Either Surface

The parent Programme's Phase 3 adversarial review was scoped explicitly to "the narrower
within-session risk... an agent's own reflection note biasing its own subsequent retry within the
same task" for the `WorkingMemory`-scoped design _as specified_ — an in-process, pytest-reachable
mechanism. It never evaluated a mechanism invoked from a real subagent's live workflow (Surface A)
or one sitting inside the live tool-permission gate (Surface B). Neither surface inherits that
PASS.

**Evidence:**

- `01-deployment-and-implementation-plan.md` Phase 3 review scope (three bullet questions, all
  about the in-process `WorkingMemory` design) — no mention of a real-dispatch or hook-level
  mechanism
- Dr. Wieczorek's verdict text: "This review does not itself constitute ASGF ratification... it is
  independent evaluation input to Dr. Vance's decision" — scoped to what was actually reviewed

**Implications:**

Surface A, as advisory helper code, is low-risk enough that Dr. Vance can authorize a pilot under
existing lab authority (same class of decision as the original Programme's own Open Questions 1/3/
4/5). Surface B must not be built without its own, freshly-scoped adversarial review — this report
does not request or imply one, and none should be assumed.

---

### Finding 6 (added 2026-08-02): v1.0 Specified Bash Invocation, Reintroducing an Already-Closed OS-Fork Problem

The CEO asked why this report chose Bash for Surface A's helper invocation when this workspace
had already migrated `.claude/hooks/*.{ps1,sh}` to a unified `uv run <script>.py` invocation
specifically to eliminate OS-forked script invocation
(`2026-07-30-cross-platform-config-automation`, closed 2026-07-31, commit `abc29e7a`). Checking
v1.0 of this report against that migration confirms the CEO's premise: v1.0's Executive Summary,
Finding 4, and Recommendations all specified the new helper as "Bash-invokable" — a plain
oversight, not a deliberate choice. Nothing in this investigation's own Findings 1–5 depended on
Bash specifically; the design only ever needed "the orchestrating subagent can invoke a script
between real dispatches," and `uv run <script>.py` satisfies that identically to a raw `bash`
call, with the added benefit of matching this workspace's own standardized invocation shape
instead of reintroducing the exact per-OS command-string fork
`2026-07-30-cross-platform-config-automation` was commissioned to remove.

**Evidence:**

- `.claude/settings.json` hook entries: `"command": "uv", "args": ["run", "<path>.py"]` — the
  live, shipped pattern for every migrated hook
- `2026-07-30-cross-platform-config-automation/research-report.md` §§ Recommendations: "Migrate
  hooks to Python, invoked via `uv run`, removing the OS fork at its root" — the explicit
  rationale this report failed to apply by analogy
- This session's own environment notes: PowerShell is the primary shell on this machine, with a
  separate Bash tool available for POSIX scripts, "each takes its own syntax" — precisely the kind
  of platform assumption a bare `bash` invocation bakes in

**Implications:**

Surface A's design is otherwise unaffected — this is an invocation-mechanism correction, not a
scope or risk-model change. All "Bash" references in the Executive Summary, Finding 4, and
Recommendations have been corrected in place to `uv run` per this workspace's append-only
telescope convention (correction noted with a date, not a silent rewrite). No other finding or
recommendation in this report changes as a result.

---

## Analysis

### Interpretation of Findings

The CEO's integration question has a real, buildable answer, but not the one informally sketched
in the prior conversation. `SwarmOrchestrator` cannot become a live dispatcher; it can become a
decision-logic library a real dispatcher already consults. Surface A realizes that at low risk and
with no new enforcement mechanism; Surface B would realize it more completely but requires new
governance work this report does not do. Consistent with this lab's established pattern (ship the
conservative version, let real data justify anything riskier — see the parent Programme's own OQ2
resolution), Surface A is the right first step.

### Trade-offs Identified

| Surface                                            | Data Coverage                                                                                                        | Enforcement                                                                           | New Review Required                                                       |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| A — advisory helper via `multi-agent-orchestrator` | Only tasks that subagent's own workflow routes through it (narrower, likely biased toward worktree/multi-agent work) | Advisory only — same maturity H-P01 started at, a known gap pattern in this workspace | No — within Dr. Vance's existing lab authority, mirroring OQ1/3/4/5       |
| B — `.claude/hooks/*.py` `PostToolUse` gate        | Every real Agent-tool dispatch in every session                                                                      | Structurally enforced, same class as H-P01/H-HE01                                     | Yes — a fresh, hook-scoped adversarial review, not inherited from Phase 3 |
| Do nothing (leave Phase 4 blocked)                 | None                                                                                                                 | N/A                                                                                   | N/A — but leaves the CEO's original diagnosis unaddressed                 |

### Risks and Limitations

- Surface A's data is not representative of all Claude Code usage — only tasks the
  `multi-agent-orchestrator` subagent's own workflow chooses to route through the helper. Dr.
  Nwosu-Chen's eventual benchmarking pass must treat this as a sampling-frame caveat, not silently
  generalize pilot results workspace-wide.
- No file in this workspace has ever cross-verified `evaluate_subtask_result()` against real
  subagent output, since a real subagent returns free-text transcripts and tool-call results, not
  a tidy `{"checks": {...}}` mapping. This is new, unbuilt design surface — an evidence-extraction
  step turning a real transcript into the structured evidence `evaluate_subtask_result()` already
  prefers over narrative text (per the parent Programme's Dr. Wieczorek-required mitigation). Not
  solved by this report; assigned below.
- Because Surface A is advisory, a subagent invocation that skips calling the helper produces no
  data and no error — silent under-collection is possible and would not be visible without a
  separate audit of how often the Execute phase actually invokes it.

---

## Recommendations

### Primary Recommendation

**Build Surface A: an advisory Evaluate/Reflect helper the `multi-agent-orchestrator` subagent's
own real Execute phase invokes via `uv run` — matching the same cross-platform convention
`.claude/hooks/*.py` already uses (`"command": "uv", "args": ["run", "<path>.py"]`), not a raw
`bash`/`pwsh` shell-out — and not a change to `SwarmOrchestrator.execute()` itself or a
`.claude/hooks/*.py` gate.** Concretely:

1. A new module, `reflective_dispatch_helper.py`
   (`multi-agent-engineering/implementations/`), following `reflection_bridge.py`'s
   deferred-import/never-raises pattern: given a task description, `gate_criteria`, and structured
   evidence (test exit code, diff summary, or other checkable output the real subagent already
   produced), it calls the existing, unmodified `evaluate_subtask_result()` and, on a failing
   verdict within the retry cap, returns a reflection note formatted via the existing
   `_reflection_note_for_attempt()` logic for re-injection into the retried subagent's prompt.
2. A small evidence-extraction contract: the caller (the orchestrating subagent, via its own
   instructions) is responsible for producing the structured `checks` mapping from whatever real,
   checkable output the worker subagent actually generated (test output, a diff, a status code) —
   this helper does not attempt to parse free-text transcripts itself, preserving the parent
   Programme's checkable-evidence-over-narrative requirement rather than quietly reopening it.
3. `.claude/agents/multi-agent-orchestrator.md`'s Execute phase (§ "2 — Execute") documents when
   and how to invoke the helper — opt-in, per subtask, mirroring how `gate_criteria`-empty tasks
   already pass through the underlying loop unaffected.
4. Piloted only on the domain already selected in the parent Programme's
   `05-benchmarking-methodology.md` (single-module backend test-verification subtasks) — no change
   to that selection.
5. Explicitly never becomes a `.claude/hooks/*.py` file in this phase.

### Secondary Recommendations

1. **Defer Surface B entirely** — log it as a distinct, explicitly out-of-scope future item
   requiring its own hook-scoped adversarial review, not a fallback if Surface A "isn't enough
   data."
2. **Dr. Farouk owns the evidence-extraction contract** (Recommendation 1 § 2) — it directly
   extends his `evaluate_subtask_result()` checkable-evidence requirement from the parent
   Programme.
3. **Kwame Asante reviews the helper's invocation contract** (how the orchestrating subagent's
   `uv run` call and the helper's return value are shaped) for consistency with existing
   harness-engineering conventions, before it is documented as callable.
4. **Dr. Nwosu-Chen logs the Surface-A sampling-frame caveat** in her benchmarking methodology
   before the pilot starts collecting data, not after.
5. **Track how often the Execute phase actually invokes the helper** (Risks and Limitations, last
   bullet) — a simple invocation counter, so silent under-collection is visible rather than
   assumed away.

### Implementation Priority

| Recommendation                                                   | Priority | Effort      | Impact                                                                         |
| ---------------------------------------------------------------- | -------- | ----------- | ------------------------------------------------------------------------------ |
| `reflective_dispatch_helper.py` (Evaluate/Reflect helper)        | P0       | 1–2 days    | High — the actual missing bridge                                               |
| Evidence-extraction contract definition                          | P0       | 1 day       | High — without it, Evaluate has nothing checkable to use                       |
| `multi-agent-orchestrator.md` Execute-phase documentation update | P0       | 2 hours     | High — otherwise the helper is undiscoverable, same failure as the loop itself |
| Kwame Asante's invocation-contract review                        | P1       | 4 hours     | Medium                                                                         |
| Invocation-counter telemetry                                     | P1       | 4 hours     | Medium                                                                         |
| Surface B (hook-based) scoping                                   | P2       | Not started | Deferred — own future review required                                          |

### Next Steps

1. Present this report, together with `supporting/implementation-plan.md`'s detailed phased plan
   and Before/After comparison, to the CEO for the User Approval Gate sign-off, per this
   workspace's stage-gate convention — no code has been written.
2. On approval, Dr. Farouk and Amina Yusuf implement `reflective_dispatch_helper.py` and the
   evidence-extraction contract (plan Phase 1); Kwame Asante reviews the invocation contract
   (plan Phase 3).
3. Update `.claude/agents/multi-agent-orchestrator.md`'s Execute phase to document opt-in use
   (plan Phase 2).
4. Run the pilot on the already-selected domain (plan Phase 4); feed results to Dr. Nwosu-Chen's
   benchmarking pass (parent Programme, Phase 4; this investigation's plan Phase 5), with the
   sampling-frame caveat recorded up front.
5. Revisit Surface B only after Surface A has produced real data and only via its own,
   separately-commissioned adversarial review.

---

## References

### Internal Documentation

- `core-component-00/telescope/2026-07-28-reflexion-execute-monitor-evaluate-loop/` — the parent
  Programme this investigation bridges to real usage
- `core-component-00/engineering/multi-agent-engineering/implementations/swarm_orchestrator.py` —
  `SwarmOrchestrator.__init__` (line 387), `_default_execute` (line 648),
  `evaluate_subtask_result()` (line 306)
- `core-component-00/engineering/multi-agent-engineering/implementations/reflection_bridge.py` —
  the existing real-wiring precedent this bridge's shape follows
- `.claude/agents/multi-agent-orchestrator.md` — the real subagent this bridge extends
- `core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`
- Root `CLAUDE.md` § 11 — H-P01's advisory-vs-structural-enforcement history, the direct precedent
  for classifying Surface A vs. Surface B
- `supporting/implementation-plan.md` — this Programme's own detailed phased implementation plan
  and CEO-requested Before/After comparison table (added v1.2, converting this investigation from
  Simple to Programme shape)
- `supporting/usage-cookbook.md` — this Programme's own concrete invocation contract, worked
  example, and anti-pattern list for the reflective dispatch helper (added v1.3, for CEO review)
- `supporting/pilot/pilot-run-01.md` — the first real, end-to-end Phase 4 pilot record: real Execute →
  Evaluate cycle, independently-re-verified evidence, real telemetry, and the negation-blindness
  finding (added v1.7; moved into `supporting/pilot/` v1.11)
- `supporting/pilot/pilot-run-02.md`, `supporting/pilot/pilot-run-03.md` — the second and third real Phase 4
  pilot records, run in parallel; combined three-run summary in the Executive Summary's second
  Phase 4 Update note (added v1.8; moved into `supporting/pilot/` v1.11)
- `supporting/pilot/wieczorek-triage-01.md` — Dr. Wieczorek's independent triage of the three P2
  findings the pilot runs surfaced, with severity/exploitability assessed against real call-site
  checks, not assumed (added v1.9; moved into `supporting/pilot/` v1.11)
- `core-component-00/telescope/2026-07-28-reflexion-execute-monitor-evaluate-loop/supporting/06-pilot-data-schema-assessment.md`
  — Dr. Nwosu-Chen's assessment of why these three pilot data points don't yet satisfy the parent
  Programme's benchmarking methodology (added v1.9, primary copy lives in the parent Programme)
- `core-component-00/telescope/2026-07-28-reflexion-execute-monitor-evaluate-loop/supporting/07-surface-a-native-benchmarking-methodology.md`
  — Dr. Nwosu-Chen's Option A methodology, commissioned 2026-08-03 (added v1.10, primary copy
  lives in the parent Programme)

### External Sources

- None new; Shinn et al. (Reflexion, NeurIPS 2023) remains cited by reference via the parent
  Programme, not re-retrieved here.

### Related Work

- `2026-07-28-reflexion-execute-monitor-evaluate-loop` — parent Programme; this report supplies its
  missing Phase 4 precondition
- `2026-07-14-reflexion-memory-system` — origin of `reflection_bridge.py`'s real-wiring pattern

---

## Open Questions

1. **Should the helper eventually also cover single-agent (non-worktree) dispatches, or stay
   scoped to `multi-agent-orchestrator`'s own workflow?**
   Status: Not decided — out of scope for this pilot; revisit once Surface A has real data.
   Priority: Low
   Assigned: Dr. Farouk, post-pilot.

2. **Who validates the evidence-extraction contract's own reliability (i.e., that the structured
   `checks` mapping a real subagent's output produces is actually trustworthy)?**
   Status: Open — new unit tests needed against realistic (not synthetic) transcript shapes.
   Priority: Medium
   Assigned: Dr. Farouk, at implementation.

3. **When, if ever, does Surface B (the hook-based gate) get its own review commissioned?**
   Status: Open — explicitly not requested by this report; a future decision contingent on
   Surface A's pilot results.
   Priority: Low
   Assigned: N/A — CEO/Dr. Vance, if and when raised.

---

## Version History

| Version | Date       | Author                                                      | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------- | ---------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-08-01 | Dr. Elias Vance                                             | Initial research report completed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 1.1     | 2026-08-02 | Dr. Elias Vance                                             | CEO flagged that v1.0 specified Bash invocation despite the workspace's already-standardized `uv run` cross-platform convention (`2026-07-30-cross-platform-config-automation`). Added Finding 6; corrected all "Bash-invokable" references in the Executive Summary, Finding 4, and Recommendations to `uv run` — invocation mechanism only, no change to Surface A's scope, risk model, or any other finding                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 1.2     | 2026-08-02 | Dr. Elias Vance                                             | Per CEO request for a detailed implementation plan and a Before/After comparison table, added `supporting/implementation-plan.md` — converting this investigation from Simple to Programme shape. The plan phases the build (evidence-extraction contract + helper core → invocation wiring + `multi-agent-orchestrator.md` documentation → Kwame Asante's conformance review → pilot → hand-off to Dr. Nwosu-Chen's benchmarking), with owners, gates, and rollback mirroring the parent Programme's own deployment plan. No production code written; still awaiting CEO sign-off                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 1.3     | 2026-08-02 | Dr. Elias Vance, Dr. Idris Farouk                           | Per CEO request for specific implementation details, added `supporting/usage-cookbook.md` — the concrete `uv run` invocation contract (stdin/stdout JSON shapes), the `gate_criteria`/`checks` evidence-extraction convention, the proposed `multi-agent-orchestrator.md` Execute-phase diff, a full worked example on the pilot domain, and an explicit anti-pattern list. Marked prominently as an unbuilt interface specification, not shipped documentation — no code exists yet, still awaiting CEO sign-off                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 1.4     | 2026-08-02 | Dr. Elias Vance, Dr. Idris Farouk                           | Per CEO request, extended `supporting/usage-cookbook.md` § 5 with explicit Executor/Supervisor/Evaluator role definitions and authority boundaries; iterative execution for complex tasks (bounded same-Executor retry vs. the explicitly-not-implemented re-decomposition fallback); multiple-Executor support (already covered by existing `FORK_JOIN`/`HYBRID` `gate_failed` aggregation, no new code); and multiple-Supervisor/multiple-Evaluator scenarios, both honestly flagged as out of scope today — the former blocked on the parent Programme's still-open `SUPERVISOR_WORKER` dispatch gap (Open Question 4), the latter simply not part of the current design. Still no code written; still awaiting CEO sign-off                                                                                                                                                                                                                                                                                                               |
| 1.5     | 2026-08-02 | Dr. Elias Vance, Dr. Idris Farouk                           | CEO approved `implementation-plan.md` and authorized Phase 1–2. Implemented and shipped `reflective_dispatch_helper.py` (22 new tests, all green) and the `multi-agent-orchestrator.md` Execute-phase documentation diff (scope-reviewed, no creep beyond the documented addition); full module suite green at 106/106. Phase 3 (Kwame Asante's conformance review) and Phase 4 (pilot) remain outstanding — no pilot data collected yet. See the new Implementation Update note in the Executive Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 1.6     | 2026-08-02 | Kwame Asante, Dr. Elias Vance                               | Phase 3 conducted: Kwame Asante's invocation-contract conformance review recorded a **PASS**, after finding and fixing 2 required issues same-day — missing structured stderr logging on the helper's degrade paths (now matches `error_boundary.py`'s `log_warning` convention) and an undocumented no-JSON-output case in `multi-agent-orchestrator.md`'s Execute-phase documentation. Retry-count independence from `error_boundary.py` confirmed with no fix needed. 3 new fault-injection tests added; full suite green at 109/109. Full verdict in `supporting/implementation-plan.md` § Phase 3. **Phase 4 (the pilot) is now unblocked** — not yet started, no pilot data collected yet                                                                                                                                                                                                                                                                                                                                               |
| 1.7     | 2026-08-03 | Dr. Elias Vance                                             | Phase 4 begun: added invocation-counter telemetry (112/112 green) and ran the first real pilot dispatch end to end (real worktree-isolated Executor, independently-re-verified evidence, real `uv run` Evaluate call — passed on attempt 1). Added `supporting/pilot-run-01.md`. Surfaced and logged (not fixed, out of scope) a real P2 narrative-fallback negation-blindness finding for Dr. Wieczorek. Dr. Vance's Phase 4 gate review: successful first data point, continue accumulating runs before recommending expansion past the pilot domain                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 1.8     | 2026-08-03 | Dr. Elias Vance                                             | Per CEO direction, ran two more real pilot cycles in parallel (runs 02–03), on `HandoffPacket` cross-fleet validation and `SharedMemoryLog` TTL/expiry — both real, previously zero-coverage code paths, both independently re-verified, both passed on attempt 1. Added `supporting/pilot-run-02.md`, `supporting/pilot-run-03.md`, and a combined three-run summary table in the Executive Summary. Telemetry now 3/3 real records. Two more P2 findings logged for Dr. Wieczorek. Honestly flagged the real gap this data still has: the Reflect/bounded-retry half of the loop has not been exercised in any of the three real runs, since none has failed yet — not artificially forced, and not yet observed                                                                                                                                                                                                                                                                                                                            |
| 1.9     | 2026-08-03 | Dr. Amara Nwosu-Chen, Dr. Tomasz Wieczorek, Dr. Elias Vance | Per CEO direction, merged the three pilot worktree branches into `core00/dev/engineering` (`--no-ff`, no conflicts; 129/129 green post-merge), leaving the main workspace's own pending changes uncommitted per explicit instruction. Activated Dr. Nwosu-Chen and Dr. Wieczorek per the Activation Protocol to continue the CEO's next-steps items 2–3: Dr. Nwosu-Chen found the three pilot data points don't fit the parent Programme's benchmarking data schema (cross-linked, primary copy in the parent Programme). Dr. Wieczorek independently triaged the three P2 findings — two real and open with fixes recommended for Dr. Farouk, one closed as informational — grounding severity in real call-site checks (`HandoffPacket.validate()` confirmed to have zero live callers) rather than assumption. Added `supporting/wieczorek-triage-01.md`                                                                                                                                                                                   |
| 1.10    | 2026-08-03 | Dr. Elias Vance                                             | Per CEO delegation of full decision authority with direction to take a long-term robustness view: fixed and verified both open Wieczorek findings same-day (`_criterion_satisfied()` negation-blindness via a bounded negation heuristic; `HandoffPacket.validate()` fail-open on missing `fleet_id` now fails closed) — both reproduction tests inverted into permanent regression guards, full suite green at 129/129 (same count, two tests corrected in place). Decided not to force the still-unexercised Reflect/retry path (stays an honestly-tracked gap, now with an explicit 10-dispatch floor in the parent Programme's new `07-surface-a-native-benchmarking-methodology.md`). Decided the zero-live-caller architecture question (`SwarmOrchestrator.execute()`, `HandoffPacket.validate()`) is a real future research question for Dr. Nwosu-Chen to consider originating, not solved here; assigned Dr. Farouk to re-confirm `validate()`'s zero-caller status before any future wiring. No new pilot runs, commits, or merges |
| 1.11    | 2026-08-03 | Dr. Elias Vance                                             | Per CEO-approved reorganization proposal, moved `pilot-run-01.md`–`pilot-run-03.md` and `wieczorek-triage-01.md` into a new `supporting/pilot/` subfolder, separating pilot-derived material from the two pre-pilot design docs (`implementation-plan.md`, `usage-cookbook.md`), which stay at the top level. `pilot-telemetry/` deliberately left in place at this step — its path was hardcoded in `reflective_dispatch_helper.py`, a production-code change out of scope for a docs-only reorg. Updated all live cross-references across both Programmes; historical Version History rows recording the original paths left untouched, per append-only policy. No content changed in any moved file                                                                                                                                                                                                                                                                                                                                        |
| 1.12    | 2026-08-03 | Dr. Elias Vance                                             | Per CEO follow-up approval, completed the reorganization: moved `pilot-telemetry/` (with its 3 real telemetry records intact, content integrity confirmed via matching SHA256 hash before/after) into `supporting/pilot/`, renamed to `telemetry/` — final path `supporting/pilot/telemetry/invocations.jsonl`. This step does touch production code, unlike v1.11: updated `reflective_dispatch_helper.py`'s `_TELEMETRY_PATH` and its docstring, then re-verified full suite green at 129/129 and confirmed a live CLI round-trip still works end to end. Updated the remaining doc references (`07-surface-a-native-benchmarking-methodology.md`, `pilot/pilot-run-01.md`)                                                                                                                                                                                                                                                                                                                                                                 |

---

**Template Version:** 1.0
**Last Updated:** 2026-08-01
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
