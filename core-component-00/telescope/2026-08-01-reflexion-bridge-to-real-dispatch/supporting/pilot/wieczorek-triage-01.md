# Supporting Document — Dr. Wieczorek's Triage of Pilot Findings 01–03

**Programme:** `2026-08-01-reflexion-bridge-to-real-dispatch`
**Author:** Dr. Tomasz Wieczorek (Staff Safety & Evaluation Engineer)
**Purpose:** Independent triage of the three P2 findings the real pilot runs surfaced
(`pilot-run-01.md`–`pilot-run-03.md`), per my structurally-independent safety/evaluation mandate —
reported directly to Dr. Vance, not through Dr. Farouk, whose code these findings concern.
Findings below are stated as reproducible technical facts, not judgments of anyone's work.

---

## Finding 1 — Narrative-Fallback Negation-Blindness (`_criterion_satisfied()`)

**What it is:** a narrative that explicitly _denies_ a criterion — e.g. "it would be incorrect to
say the tests pass" — still scores `passed=True`, because the denial sentence contains the
criterion text as a contiguous substring and the fallback has no negation awareness.

**Reproduction:** `test_narrative_negated_criterion_text_still_matches_as_substring`
(`test_swarm_orchestrator.py`, added by pilot run 01) — deterministic, no flakiness risk.

**Exploitability:** bounded, not primary-path. This fallback only fires when `result["checks"]`
has no structured key for a criterion at all — the primary, structured-evidence path is unaffected
and is the mandated convention (`usage-cookbook.md` § 6: "Do not build `checks` from a worker's
narrative summary"). A real exploit requires a caller to have already violated that convention
before this gap becomes reachable. That's a real mitigating factor, not a reason to close this —
"the caller shouldn't do X" is not itself a control, and I've seen mandated conventions get
violated under real deadline pressure before.

**Severity: P2, real, open.** Not P0/P1 — it can't currently silently pass a subtask that's on
the primary, structured-evidence path, only one that has fallen back to unstructured narrative
entirely, which this codebase already discourages.

**Recommendation:** commission a fix to `_criterion_satisfied()`'s narrative-fallback path — a
minimal negation-detection heuristic (checking for a negation cue word/phrase within some token
window before the matched substring) would close the specific reproduction case without requiring
a full NLP dependency. This is Dr. Farouk's module; I am not scoping the fix myself, per my
role's boundary (independent evaluation, not implementation). Once fixed, the existing
reproduction test becomes a permanent entry in my cross-module safety regression suite — I do not
consider a safety finding closed until it has a regression test that would catch it coming back,
and this one already has one, ready to promote.

---

## Finding 2 — `HandoffPacket.validate()` Fleet-ID-Omission Bypass

**What it is:** the GSMSE T15 cross-fleet `conversation_history` check
(`if turn_fleet is not None and turn_fleet != expected_fleet_id`) silently treats a turn with no
`fleet_id` key at all as compliant — it is never flagged as cross-fleet, regardless of
`expected_fleet_id`.

**Reproduction:** `test_turn_missing_fleet_id_not_flagged` (`test_handoff_packet.py`, added by
pilot run 02).

**Exploitability — checked, not assumed:** I grepped every call site of `HandoffPacket.validate()`
across `implementations/` before assessing this. Result: **`validate()` has zero live callers
anywhere in production code** — `SwarmOrchestrator._dispatch()` constructs a `HandoffPacket` on
every dispatch but never calls `.validate()` on it. The only callers of `validate()` in this
entire workspace are its own test suite. This is the same zero-live-caller pattern
`2026-08-01-reflexion-bridge-to-real-dispatch`'s own Finding 1 already established for
`SwarmOrchestrator` itself — a real, recurring pattern in this module worth Dr. Vance's attention
on its own, separate from this specific finding.

**Severity: P2, real, currently not exploitable in production** (there is no live enforcement path
to bypass yet), **but I am not closing it as low-priority.** A validation method whose entire
purpose is catching a cross-fleet policy violation should fail closed on missing data, not treat
absence-of-evidence as evidence-of-compliance — that's the wrong default for a security-adjacent
check regardless of whether it's wired up today. If `validate()` is ever wired into a real
enforcement path (which I'd consider the natural next step for `HandoffPacket`, given it already
has the check written), this gap becomes live on day one of that wiring, silently, unless fixed
first.

**Recommendation:** treat this as a **precondition**, not an urgent patch: fix
`validate()`'s missing-`fleet_id` handling (a turn with no `fleet_id` should itself be flagged as
unverified/suspect origin, not silently passed) **before** `validate()` is wired into any real
call path — not after. I'm recording this as a blocking item for that future wiring work
specifically, so it doesn't get missed when someone picks that up. Same regression-suite
promotion plan as Finding 1 once fixed.

---

## Finding 3 — `SharedMemoryLog` TTL Boundary Semantics

**What it is:** an entry exactly at `elapsed == ttl_seconds` is not yet expired (strict `>`
comparison); one tick past it, it is. Newly documented by
`test_is_expired_boundary_behavior` (`test_shared_memory_log.py`, added by pilot run 03).

**Assessment: not a safety finding.** This is previously-undocumented, now-verified behavior, not
a vulnerability or a policy-enforcement gap — TTL boundary semantics have no cross-fleet or
access-control implication on their own. I reviewed it in case a strict-boundary read gave a
narrow window for a stale entry to be read as fresh (or vice versa) in a way that mattered for GSM
scope enforcement; it doesn't — `_scope_predicate()`'s fleet-isolation check is entirely
independent of `is_expired`, so this boundary choice doesn't weaken cross-fleet isolation either
way.

**Disposition: closed, informational.** No fix needed, no regression-suite entry required beyond
the test that already exists and already documents the behavior.

---

## Summary for Dr. Vance

| Finding                                  | Severity | Status                         | Owner for fix |
| ---------------------------------------- | -------- | ------------------------------ | ------------- |
| Narrative negation-blindness             | P2       | Open — fix recommended         | Dr. Farouk    |
| `HandoffPacket` fleet_id-omission bypass | P2       | Open — precondition for wiring | Dr. Farouk    |
| `SharedMemoryLog` TTL boundary           | —        | Closed — informational only    | N/A           |

Neither open finding blocks the current pilot (Phase 4) or anything already merged — both concern
code paths that are either a documented fallback (Finding 1) or not yet live in production
(Finding 2). I'd like both scoped as real backlog items, not left as footnotes in a pilot-run
document where they're easy to lose track of.

> **Update (2026-08-03) — both findings fixed and verified, recorded by Dr. Vance.** Per CEO
> delegation of full decision authority with direction to take a long-term robustness view, both
> open findings were fixed same-day. Finding 1: `_criterion_satisfied()`'s narrative fallback now
> runs a bounded negation-detection heuristic (`_phrase_asserted_in_narrative()` in
> `swarm_orchestrator.py`) before treating a substring match as an assertion — a fixed-window scan
> for a small negation-cue vocabulary immediately preceding each match, explicitly documented as a
> heuristic bound, not general negation/NLP handling. Finding 2: `HandoffPacket.validate()` now
> treats a turn missing the `fleet_id` key entirely as an unverified-origin issue in its own right,
> rather than silently compliant — fails closed instead of open. Both reproduction tests named
> above were inverted to assert the corrected behavior and are now permanent regression guards, per
> the closure standard stated above ("I do not consider a safety finding closed until it has a
> regression test that would catch it coming back"). Full `multi-agent-engineering` suite
> re-verified green at 129/129 (same total — two tests corrected in place, none added or removed).
> Finding 2's status as a "precondition, not urgent patch" is now moot for the specific gap
> identified — it's fixed — but the broader precondition framing (re-confirm zero-live-caller
> status before any future wiring into a real enforcement path) still stands and is assigned to Dr.
> Farouk. Full decision record: `../research-report.md` Phase 5 Update.

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-08-01-reflexion-bridge-to-real-dispatch`
