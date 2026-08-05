# Supporting Document — Implementation Plan and Before/After Comparison

**Programme:** `2026-08-01-reflexion-bridge-to-real-dispatch`
**Purpose:** The detailed, phased rollout for Surface A (the `uv run`-invoked Evaluate/Reflect
helper) recommended in `research-report.md`'s Primary Recommendation, plus the CEO-requested
Before/After comparison table. No production code has been written — this is a plan, not a status
report, per this workspace's stage-gate convention (present, request sign-off, wait).
**Ownership of this deliverable:** Commissioned to Dr. Elias Vance (Laboratory Director, PI of
record) by the CEO. Per `crew/CLAUDE.md`'s Laboratory Roster and Activation Protocol, Dr. Vance
designates **Dr. Idris Farouk (Staff Research Engineer, MAE Lead)** as implementation owner — the
helper's only real dependency is `swarm_orchestrator.py`'s already-shipped, already-reviewed
`evaluate_subtask_result()` and reflection-note logic, both of which Farouk owns — with Amina
Yusuf as his paired Research Engineer II, and Kwame Asante (Harness Engineering Lead) consulted
for the invocation-contract review, matching the ownership pattern the parent Programme already
established.

---

## 0. Before / After Comparison

| Dimension                                               | Before (current state, as of `research-report.md` v1.1)                                                                                    | After (Surface A implemented and piloted)                                                                                                                                                                                                                      |
| ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Live callers of `SwarmOrchestrator`**                 | Zero — `SwarmOrchestrator(` appears only in test files and pattern docs, never in `.claude/`                                               | One real caller: `multi-agent-orchestrator`'s Execute phase, opt-in per subtask                                                                                                                                                                                |
| **Evaluate step** (`evaluate_subtask_result()`)         | Exercised only by pytest (84/84 green, Phase 3 PASS)                                                                                       | Additionally exercised against real, checkable evidence from real worktree dispatches on the pilot domain — same function, unmodified                                                                                                                          |
| **Reflect step** (`WorkingMemory` note + bounded retry) | Exercised only by pytest                                                                                                                   | Exercised for real: a failing verdict produces a real reflection-note-augmented retry of a real subagent dispatch, capped at `max_reflection_retries = 2`                                                                                                      |
| **Invocation mechanism**                                | N/A — nothing calls it; v1.0 of the research report had informally specified "Bash," corrected to `uv run` in v1.1 before any code existed | `uv run reflective_dispatch_helper.py ...` — the same cross-platform shape `.claude/hooks/*.py` already uses, no shell fork                                                                                                                                    |
| **Enforcement level**                                   | N/A                                                                                                                                        | Advisory / opt-in per subtask — explicitly not a `.claude/hooks/*.py` structural gate (Surface B stays deferred, out of scope)                                                                                                                                 |
| **Evidence source for Evaluate**                        | N/A                                                                                                                                        | A structured `checks` mapping the orchestrating subagent extracts from real subagent output (test exit code, diff summary) — never narrative text alone, preserving Dr. Wieczorek's Phase 3 requirement                                                        |
| **Adversarial/conformance review coverage**             | Phase 3 PASS (Wieczorek) covers only the in-process, pytest-reachable `WorkingMemory` design                                               | Phase 3 PASS still covers the underlying loop unchanged; the new invocation-contract layer gets Kwame Asante's conformance review (Phase 3 below) — not a fresh adversarial pass, since blast radius stays advisory/opt-in, per `research-report.md` Finding 5 |
| **Parent Programme's Phase 4 status**                   | Blocked — no dispatch path exists to pilot on                                                                                              | Unblocked — pilot runs on the domain the parent Programme already selected (single-module backend test-verification subtasks)                                                                                                                                  |
| **Real-usage data for Dr. Nwosu-Chen's benchmarking**   | None                                                                                                                                       | Real per-subtask attempts-to-pass distributions and `gate_failed` rationale history, with the Surface-A sampling-frame caveat recorded before collection begins                                                                                                |
| **`.claude/agents/multi-agent-orchestrator.md`**        | No mention of the reflective loop                                                                                                          | Execute phase (§ 2) documents when and how to invoke the helper, opt-in                                                                                                                                                                                        |
| **New files**                                           | —                                                                                                                                          | `multi-agent-engineering/implementations/reflective_dispatch_helper.py` + its test suite; this `supporting/implementation-plan.md`                                                                                                                             |
| **Files modified**                                      | —                                                                                                                                          | `.claude/agents/multi-agent-orchestrator.md` (Execute-phase documentation only — no change to its Hard Constraints or other phases)                                                                                                                            |
| **Risk / blast radius**                                 | N/A                                                                                                                                        | Bounded: per-subtask opt-in, no change to the live tool-permission gate, no new write path to `ReflectionMemory` or any persisted store                                                                                                                        |
| **CEO gate status**                                     | `research-report.md` awaiting User Approval Gate sign-off                                                                                  | Unchanged by this document — this plan is itself part of the same pending deliverable; no code exists yet                                                                                                                                                      |

---

## 1. Preconditions

1. `research-report.md` (this investigation) remains at v1.1 — Findings 1–6, the Bash→`uv run`
   correction, and the risk classification are treated as settled inputs to this plan, not
   reopened here.
2. `swarm_orchestrator.py`'s test suite stays green before this plan's Phase 1 begins:
   `pytest engineering/multi-agent-engineering/testing/ -v` (run from `core-component-00/`, per
   that module's own `CLAUDE.md`) — re-verified immediately before Phase 1, in case an unrelated
   change landed since the parent Programme's own last verification.
3. No change is made to `evaluate_subtask_result()`, the `WorkingMemory` Reflect logic, or any
   other Phase 1–3 code from the parent Programme — this plan only adds a new caller and a new
   thin wrapper module.
4. **Owner:** Dr. Idris Farouk (module owner of record for `swarm_orchestrator.py` and, by
   extension, its new helper).

---

## Phase 1 — Evidence-Extraction Contract and `reflective_dispatch_helper.py` Core (P0)

1. Define the evidence-extraction contract first, as plain documentation (a docstring-level
   convention, not a runtime schema, mirroring how `gate_criteria`'s own authoring convention was
   handled in the parent Programme): the orchestrating subagent is responsible for producing a
   `{"checks": {<criterion-key>: <bool-or-value>}}` mapping from whatever real, checkable output
   the worker subagent actually generated (a test exit code, a diff summary, an explicit pass/fail
   flag) — the helper itself never parses free-text transcripts.
2. Add `reflective_dispatch_helper.py`
   (`engineering/multi-agent-engineering/implementations/`), following `reflection_bridge.py`'s
   established shape: deferred import of `swarm_orchestrator`'s public functions (no new heavy
   dependency), a single entry point taking `(task_description, gate_criteria, checks, attempt_number)`
   and returning `{"passed": bool, "rationale": str, "reflection_note": str | None,
"retries_remaining": int}`, and a never-raises contract — any internal failure degrades to
   `{"passed": True, "rationale": "helper unavailable: <reason>", ...}` so a helper fault can never
   block a real dispatch, only skip the loop for that attempt.
3. The helper calls `evaluate_subtask_result()` and, on a failing verdict within
   `max_reflection_retries`, formats a reflection note via the existing
   `_reflection_note_for_attempt()` logic — both reused unmodified from `swarm_orchestrator.py`.
4. Unit tests in `engineering/multi-agent-engineering/testing/`: passing verdict passthrough,
   failing verdict produces a correctly-formatted reflection note, retry cap enforced and reported
   correctly via `retries_remaining`, malformed/missing `checks` handled without raising, and the
   never-raises degrade path itself (simulated internal failure) confirmed to return
   `passed: True` rather than propagating an exception into a live subagent's workflow.

**Gate:** `pytest engineering/multi-agent-engineering/testing/ -v` stays green, including all
existing tests unmodified in behavior. **Owner:** Dr. Idris Farouk (design + review), Amina Yusuf
(implementation).

---

## Phase 2 — Invocation Wiring and `multi-agent-orchestrator.md` Documentation (P0)

1. Add a thin CLI entry point to `reflective_dispatch_helper.py` (`if __name__ == "__main__":`,
   reading its arguments as JSON on stdin or as CLI flags — Kwame Asante's Phase 3 review below
   decides which, consistent with existing harness-engineering CLI conventions) so it is
   `uv run`-invokable exactly like every migrated `.claude/hooks/*.py` script.
2. Update `.claude/agents/multi-agent-orchestrator.md`'s Execute phase (currently § "2 — Execute")
   to document the opt-in call: after a real worker subagent completes, the orchestrator may
   construct `gate_criteria` and a `checks` mapping from that worker's real output and invoke
   `uv run <path>/reflective_dispatch_helper.py ...`; on a failing verdict within the retry cap, it
   re-dispatches that worker with the returned reflection note appended to its task prompt. This is
   documentation only — no change to the Hard Constraints, other phases, or Agent Roles sections of
   that file.
3. Scope the initial opt-in to the pilot domain only (Phase 4 below) — the documentation states
   this explicitly, so the helper is not silently invoked workspace-wide on day one.

**Gate:** `multi-agent-orchestrator.md` diff reviewed by Dr. Vance for scope creep beyond the
documented Execute-phase addition. **Owner:** Dr. Idris Farouk (design), Dr. Elias Vance (doc
scope review).

---

## Phase 3 — Kwame Asante's Invocation-Contract Review (P0, blocking gate)

Per `research-report.md` Finding 5, this is a conformance review, not a fresh adversarial pass —
Dr. Wieczorek's existing Phase 3 PASS (parent Programme) already covers the underlying
Evaluate/Reflect logic this helper only wraps. Review scope:

- Does the CLI/stdin invocation contract (Phase 2 § 1) follow existing harness-engineering
  conventions for script arguments and error reporting?
- Does the never-raises degrade path (Phase 1 § 2) actually hold when invoked as a real subprocess
  (not just as a direct Python call in a unit test) — e.g., a non-zero exit code or malformed
  stdout must not be misread by the orchestrating subagent as a passing verdict?
- Is the helper's own retry-count bookkeeping independent of `error_boundary.py`'s fault-retry
  counters, consistent with the parent Programme's Phase 2 requirement (no shared budget between
  infrastructure faults and semantic evaluation)?

**Gate:** Kwame Asante records a pass/required-fixes verdict before Phase 4 begins. **Owner:**
Kwame Asante.

### Kwame Asante's Verdict (recorded 2026-08-02)

**Required fixes identified, applied same-day, re-verified — PASS.** Findings against the three
review-scope questions above:

1. **CLI/stdin invocation contract vs. harness-engineering conventions — required fix, applied.**
   The contract itself (stdin JSON in, one JSON object on stdout, always exit 0) correctly matches
   the shape every migrated `.claude/hooks/*.py` script already uses. But the original submission
   had no structured stderr logging on its degrade paths, unlike `error_boundary.py`'s own
   `log_warning`/`log_error` convention (mine to own) — a degrade would have been silent outside
   the stdout JSON's `rationale` field, with nothing incident-traceable in a log. Fixed: added
   `_log_warning()`, matching `error_boundary.py`'s `[LEVEL] message k=v ...` stderr format
   exactly, called on every degrade path. Stdout stays pure JSON; stderr now carries a
   `[WARNING]` note. Verified via a real subprocess test that a malformed-stdin invocation
   produces `[WARNING]` on stderr and nothing but the JSON object on stdout.
2. **Never-raises degrade path under a real subprocess — required fix, applied.** The
   in-process contract holds (verified: malformed JSON, empty stdin, non-dict JSON, a `checks`
   value of the wrong type, and a simulated internal exception all degrade to `passed: true`
   without raising, including across a real `uv run` subprocess boundary, not just a direct
   Python call). But the _documentation_ had a real gap: nothing said what the orchestrating
   subagent should do if the `uv run` invocation itself fails to produce any well-formed JSON at
   all (e.g. a non-zero exit with no output) — as opposed to a well-formed degrade response. An
   undefined case is exactly the kind of gap this review question exists to catch. Fixed: added
   one clause to `.claude/agents/multi-agent-orchestrator.md`'s Execute-phase documentation
   stating that case must be treated identically to a `passed: true` degrade — never as a pass or
   fail signal in its own right.
3. **Retry-count bookkeeping independence from `error_boundary.py` — PASS, no fix needed.** The
   helper holds zero internal retry state of its own; `retries_remaining` is computed purely from
   the caller-supplied `attempt_number`/`max_reflection_retries` on each call. There is no shared
   counter, budget, or object with `error_boundary.py`'s fault-retry logic to entangle with —
   independence holds trivially by construction, not by careful bookkeeping.

Both required fixes are implemented and covered by new fault-injection tests (3 added, matching
my own team's quality bar that every recovery/degrade path gets a test forcing that specific
failure mode). Full suite: **109/109 passing** (106 prior + 3 new). This review does not
constitute or repeat Dr. Wieczorek's Phase 3 PASS on the underlying Evaluate/Reflect logic
(unchanged, out of scope here) — it is independent input to Dr. Vance's Phase 4 go decision,
scoped strictly to the invocation layer this Programme added.

---

## Phase 4 — Pilot on the Already-Selected Domain (P1)

1. Pilot on the same domain the parent Programme already selected in
   `05-benchmarking-methodology.md` — single-module backend test-verification subtasks. No new
   domain-selection decision is made here.
2. Add a simple invocation counter (per `research-report.md`'s Recommendation 5) so how often the
   Execute phase actually calls the helper is visible, not assumed — silent under-collection would
   otherwise be indistinguishable from "the helper wasn't needed."
3. Real per-subtask attempts-to-pass data and `gate_failed` rationale history accumulate for the
   duration of the pilot, feeding directly into the parent Programme's own still-open Phase 4
   (Dr. Nwosu-Chen's benchmarking pass).

**Gate:** Pilot results reviewed by Dr. Vance before recommending the helper's use beyond this one
domain — a separate future decision, not made in this plan. **Owner:** Dr. Idris Farouk (pilot
oversight).

---

## Phase 5 — Hand-Off to Parent Programme's Benchmarking (P1)

Dr. Nwosu-Chen's benchmarking pass (parent Programme, `2026-07-28-reflexion-execute-monitor-
evaluate-loop`, Phase 4) begins once Phase 4 above has produced real data. This plan does not
redefine her methodology (`05-benchmarking-methodology.md`); it only unblocks it. She records the
Surface-A sampling-frame caveat (`research-report.md` Risks and Limitations) in her own analysis
before drawing any workspace-wide conclusion from pilot data.

**Gate:** N/A — downstream of this plan, tracked in the parent Programme's own documents. **Owner:**
Dr. Amara Nwosu-Chen.

---

## Explicitly Out of Scope for This Plan

- **Surface B** (a `.claude/hooks/*.py` gate on the Agent/Task tool) — per `research-report.md`
  Findings 4–5, deferred pending its own, separately-commissioned adversarial review. Nothing in
  this plan builds toward it.
- **Any change to `evaluate_subtask_result()`, `WorkingMemory`, or the parent Programme's shipped
  Phase 1–3 code.** This plan adds a caller and a thin wrapper; it does not modify the reviewed
  loop.
- **Any change to `ReflectionMemory`, the persisted write path, or `reflection_bridge.py`.**
  Unrelated boundary, unchanged.

---

## Rollback

Because the helper is a new, separate, opt-in module and the only other change is documentation in
`multi-agent-orchestrator.md`'s Execute phase, rollback is simple: revert the
`reflective_dispatch_helper.py` commit(s) and the documentation change. No persisted state, no
schema, no `ReflectionMemory` data is touched by this plan, so there is nothing to reconstruct.

---

## Deployment Checklist

> **Updated 2026-08-02, append-only:** rows below reflect real status as of the CEO's Phase 1–2
> authorization. The plan's original "Not started" state for every row is preserved in this
> document's own Version History below rather than silently overwritten.

| Step                                                         | Owner                                            | Gate                                                                                                                                                                                                                                                                        |
| ------------------------------------------------------------ | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Preconditions verified (§ 1)                                 | Dr. Idris Farouk                                 | **Verified 2026-08-02** — `pytest engineering/multi-agent-engineering/testing/ -v` green pre-Phase-1 (84/84)                                                                                                                                                                |
| Phase 1 — Evidence-extraction contract + helper core + tests | Dr. Idris Farouk (design), Amina Yusuf (impl.)   | **Complete 2026-08-02** — `reflective_dispatch_helper.py` shipped; 22/22 new tests green                                                                                                                                                                                    |
| Phase 2 — Invocation wiring + `multi-agent-orchestrator.md`  | Dr. Idris Farouk, Dr. Elias Vance (scope review) | **Complete 2026-08-02** — Execute-phase diff applied verbatim per `usage-cookbook.md` § 3; scope-reviewed                                                                                                                                                                   |
| Phase 3 — Invocation-contract conformance review             | Kwame Asante                                     | **PASS, recorded 2026-08-02** — 2 required fixes found and applied same-day (stderr logging; `multi-agent-orchestrator.md` no-JSON-output clause); see verdict above                                                                                                        |
| Phase 4 — Pilot + invocation-counter telemetry               | Dr. Idris Farouk                                 | **In progress, 3 real runs recorded 2026-08-03** — see `pilot/pilot-run-01.md`–`pilot/pilot-run-03.md`; all 3 passed on attempt 1 (telemetry: 3/3 real records), no retry yet observed, 3 P2 findings logged and triaged (`pilot/wieczorek-triage-01.md`)                   |
| Phase 5 — Hand-off to Dr. Nwosu-Chen's benchmarking          | Dr. Amara Nwosu-Chen                             | **Attempted, blocked 2026-08-03** — assessed the 3 real data points against the parent Programme's benchmarking schema; they don't fit (no `TaskStatus`/control group). Benchmarking pass has not begun; see `2026-07-28-.../supporting/06-pilot-data-schema-assessment.md` |
| Final go/no-go on starting Phase 1                           | CEO                                              | **Granted 2026-08-02.** CEO approved this plan and authorized Phase 1 implementation.                                                                                                                                                                                       |

---

## Version History

| Version | Date       | Author                        | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------- | ---------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0     | 2026-08-02 | Dr. Elias Vance               | Initial plan: Before/After comparison, Preconditions, Phases 1–5, rollback, Deployment Checklist — all rows "Not started", pending CEO sign-off                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 1.1     | 2026-08-02 | Dr. Elias Vance               | CEO approved this plan and authorized Phase 1–2. Deployment Checklist updated to reflect Phase 1 (`reflective_dispatch_helper.py` + 22 tests, green) and Phase 2 (`multi-agent-orchestrator.md` diff, scope-reviewed) as complete. Phase 3 (Kwame Asante's review) remains not started and is the next blocking gate — not self-granted by this update                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 1.2     | 2026-08-02 | Kwame Asante, Dr. Elias Vance | Phase 3 conducted: Kwame Asante's invocation-contract conformance review recorded (§ Phase 3, "Kwame Asante's Verdict"). Found and fixed 2 required issues same-day — missing structured stderr logging on degrade paths (now matches `error_boundary.py`'s `log_warning` convention) and an undocumented case in `multi-agent-orchestrator.md` for a `uv run` invocation that produces no well-formed JSON at all. Retry-count independence from `error_boundary.py` confirmed with no fix needed. 3 new fault-injection tests added; full suite 109/109 green. **Verdict: PASS.** Phase 4 (the pilot) is now unblocked                                                                                                                                                                                                                                                                                                                               |
| 1.3     | 2026-08-03 | Dr. Elias Vance               | Phase 4 begun: added the invocation-counter telemetry (`_record_invocation`, opt-out env var, 3 new tests; full suite 112/112 green) and ran the first real pilot dispatch — a real worktree-isolated Executor, real independently-re-verified evidence, and a real `uv run` Evaluate call. Passed on attempt 1; full record in new `supporting/pilot-run-01.md`. Surfaced one real P2 finding (narrative-fallback negation-blindness in `evaluate_subtask_result()`) for Dr. Wieczorek, logged not fixed, per this plan's explicit out-of-scope boundary. Deployment Checklist Phase 4 row updated to "in progress, 1 run recorded"                                                                                                                                                                                                                                                                                                                   |
| 1.4     | 2026-08-03 | Dr. Elias Vance               | Two more real pilot runs, dispatched in parallel per CEO direction: run 02 (`HandoffPacket` cross-fleet validation tests) and run 03 (`SharedMemoryLog` TTL/expiry tests), both on real, previously zero-coverage code paths. Both independently re-verified and both passed on attempt 1 — telemetry now shows 3/3 real invocations, all first-attempt passes, no Reflect/retry cycle observed yet across any run. Run 02's independent verification caught a minor Executor self-reporting discrepancy (claimed 6 new tests, actually 5) — logged as a data-quality note, not a defect; the Evaluator was fed the independently-confirmed count either way. Two more real P2 findings logged for Dr. Wieczorek (cross-fleet `fleet_id`-omission bypass; TTL boundary semantics now documented). Full records: `supporting/pilot-run-02.md`, `supporting/pilot-run-03.md`. Deployment Checklist Phase 4 row updated to "in progress, 3 runs recorded" |
| 1.5     | 2026-08-03 | Dr. Elias Vance               | Merged the three pilot worktree branches into `core00/dev/engineering` per CEO direction (`--no-ff`, no conflicts; 129/129 green post-merge); worktrees cleaned up. Main workspace's own pending changes left uncommitted per explicit CEO instruction. Phase 5 attempted: Dr. Nwosu-Chen assessed the 3 pilot data points against the parent Programme's benchmarking schema and found they don't fit it — benchmarking pass has not begun, full assessment in the parent Programme. Dr. Wieczorek independently triaged all 3 P2 findings (`supporting/wieczorek-triage-01.md`) — 2 open with fixes recommended for Dr. Farouk, 1 closed as informational; severity grounded in real call-site checks, not assumption                                                                                                                                                                                                                                |
| 1.6     | 2026-08-03 | Dr. Elias Vance               | Per CEO-approved reorganization proposal, moved `pilot-run-01.md`, `pilot-run-02.md`, `pilot-run-03.md`, and `wieczorek-triage-01.md` into a new `supporting/pilot/` subfolder to separate pilot-derived material from the two pre-pilot design docs (`implementation-plan.md`, `usage-cookbook.md`), which stay at the top level. `pilot-telemetry/` was deliberately left at its current path -- its location is hardcoded in `reflective_dispatch_helper.py`'s `_TELEMETRY_PATH` and moving it would require a production code change, out of scope for a docs-only reorg. Updated all cross-references to the moved files across both Programmes' documents (this file's Deployment Checklist row above; `research-report.md`; `telescope/README.md`; the parent Programme's `06-pilot-data-schema-assessment.md` and `07-surface-a-native-benchmarking-methodology.md`). No content changed in any moved file, only location and inbound links    |
| 1.7     | 2026-08-03 | Dr. Elias Vance               | Per CEO follow-up approval, completed the reorganization: moved `pilot-telemetry/` (with its 3 real telemetry records intact, SHA256 hash matched before/after) into `supporting/pilot/`, renamed to `telemetry/` -- final path `supporting/pilot/telemetry/invocations.jsonl`. Updated `reflective_dispatch_helper.py`'s `_TELEMETRY_PATH` and docstring (production code change, unlike v1.6's pure doc move); full suite re-verified green at 129/129; a live CLI round-trip confirmed the helper still works end to end. Updated remaining doc references in `07-surface-a-native-benchmarking-methodology.md` and `pilot/pilot-run-01.md`                                                                                                                                                                                                                                                                                                         |

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-08-01-reflexion-bridge-to-real-dispatch`
