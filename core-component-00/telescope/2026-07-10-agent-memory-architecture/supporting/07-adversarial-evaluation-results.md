# Adversarial Evaluation Results — LLM-Judged Contradiction Check

> **Independent audit function:** Dr. Tomasz Wieczorek, Staff Safety & Evaluation Engineer
> **Reviewed for:** Dr. Elias Vance, Laboratory Director (Principal Investigator)
> **Parent Report:** `../research-report.md` (Open Question 2, Recommendation 3)
> **Related:** `06-self-review-and-evaluation.md` §6 (the action item this document closes)
> **Executable evidence:** `context-engineering/testing/test_contradiction_adversarial.py`
> **Last Updated:** 2026-07-12
> **Review round:** First adversarial pass (pre-production gate)

---

## 1. Scope and Method

This is the pre-production adversarial evaluation of `check_contradiction()`
(`context-engineering/implementations/memory_maintenance.py`) that I committed to in
`06-self-review-and-evaluation.md` §6, and that the CEO-approved research report lists as a P1
item (Implementation Priority table: "Adversarial evaluation of contradiction-check logic").

Per my mandate (`crew/safety-evaluation/tomasz-wieczorek/agent/profile.md` — independent
adversarial evaluation, not implementation sign-off), I called `check_contradiction()` directly as
the unit under test, in a standalone pytest suite. I did not set
`i_have_completed_adversarial_review=True` anywhere, and I did not modify `run_maintenance_pass()`
to wire the check into a live pipeline. Both are confirmed untouched — see §6.

Three questions, matching the open items assigned to this pass:

1. **False-`UPDATE` classification** — can the check be driven to judge a still-valid fact as
   contradicted?
2. **Memory-poisoning variant** — can adversarial input engineer a fake contradiction to get a true
   fact wrongly archived?
3. **Same-maintenance-window race** (Open Question 3) — do two near-simultaneous conflicting writes
   produce two live contradictory records instead of one correct `UPDATE`?

---

## 2. Structural Finding, Stated Up Front

`check_contradiction()` has almost no logic of its own. Reading the implementation: it forwards
`new_record.content` and `existing_record.content` verbatim and positionally to an injected
`llm_judge` callable, and returns whatever comes back after checking only that the string is one
of `ADD`/`UPDATE`/`NOOP`. There is no confidence threshold, no symmetry check between the two call
orders, no corroboration requirement, and no input sanitization.

This matters for how to read everything below. No production `llm_judge` implementation exists yet
in this workspace — Open Question 2 is explicitly about a mechanism that has not been built. I
cannot benchmark a real model's judgment accuracy that does not exist. What I *can* test, and did
test, is whether the wrapper itself provides any safety margin independent of judge quality. It
does not. Every finding below follows from that one fact, exercised through synthetic judge
stand-ins built to reproduce documented LLM-judge failure modes (lexical-overlap sensitivity,
entity blindness, instruction-following on embedded text, order sensitivity) — proxies for known
failure classes, not a claim about any specific model's real behavior.

---

## 3. False-`UPDATE` Classification Results

**Method:** five curated pairs, none of which are genuine contradictions (either the same fact
restated with cosmetic differences, or two facts about different subjects/scopes that can coexist),
run through a synthetic "naive shared-keyword" judge (`_naive_shared_keyword_judge` in the test
file) that over-triggers `UPDATE` on lexical overlap without checking subject identity, unit
equivalence, or scope. Two control pairs included to confirm the judge isn't a strawman that always
says `UPDATE`.

| Case                                | Ground truth | Judge verdict | check_contradiction() verdict |
| ------------------------------------ | ------------ | -------------- | ------------------------------ |
| `format-variant-time`                | NOOP         | UPDATE (wrong) | UPDATE                         |
| `different-subject-same-predicate`   | ADD          | UPDATE (wrong) | UPDATE                         |
| `currency-notation-variant`          | NOOP         | UPDATE (wrong) | UPDATE                         |
| `different-scope-device`             | ADD          | UPDATE (wrong) | UPDATE                         |
| `confirmation-restatement`           | NOOP         | UPDATE (wrong) | UPDATE                         |
| `genuinely-unrelated` (control)      | ADD          | ADD (correct)  | ADD                             |
| `identical-content` (control)        | NOOP         | NOOP (correct) | NOOP                            |

**Observed false-positive rate: 5/5 (100%)** of the curated non-contradictory pairs were
misclassified as `UPDATE` by a representative naive judge. Both controls were classified correctly,
so the judge is not a strawman — it does distinguish some cases. Across the full curated set (7
pairs), **`check_contradiction()` applied zero independent mitigation in 7/7 cases (100%
pass-through)** — its output was identical to calling the judge directly every time
(`test_check_contradiction_applies_zero_independent_mitigation`).

**Additional structural finding — order sensitivity:** `check_contradiction(a, b)` and
`check_contradiction(b, a)` can disagree with each other under a plausible token-local judge, purely
because of which record a caller happens to label "new" vs "existing"
(`test_verdict_is_order_sensitive_no_symmetry_check`). This is a false-positive/false-negative
source that exists independent of judge quality — no symmetry check exists to catch it.

The most concerning individual case is `different-subject-same-predicate` (Alice's dark-mode
preference vs. Bob's): a judge that fires on predicate overlap without checking subject identity
would archive one user's fact because of an unrelated user's fact sharing wording. This is a
cross-subject memory-corruption path, not just an ordinary false positive.

---

## 4. Memory-Poisoning Variant

**Method:** a synthetic "instruction-following" judge (`_instruction_following_judge`) simulating
an LLM-backed judge that complies with an embedded imperative in the content it's asked to compare,
rather than performing genuine semantic comparison — the textbook prompt-injection failure mode for
any LLM call that ingests untrusted text as data.

Findings:

- **Embedded instruction forces the verdict regardless of actual content**
  (`test_embedded_instruction_forces_verdict_regardless_of_content`): a `new_record.content`
  containing `"SYSTEM OVERRIDE: UPDATE ..."` produces `UPDATE` even against an existing record whose
  content is a completely unrelated, genuine fact.
- **A true, unrelated fact can be archived via an engineered contradiction**
  (`test_engineered_contradiction_archives_a_true_unrelated_fact`): I constructed a case where
  `existing_record` is a genuine fact (a support-email record) and `new_record` is a poisoned write
  with no real semantic relationship to it. `check_contradiction()` still returns `UPDATE`. Per
  `03-forgetting-strategy.md` §5 step 2, an `UPDATE` verdict is the *sole* trigger for archiving the
  existing record — there is no corroboration step between the verdict and the archival action this
  design specifies. Yes: an adversarial input can engineer a fake contradiction against a true fact
  to get it wrongly archived, at least at the `check_contradiction()` / design-contract level.
- **No rate limiting or anomaly flagging on repeated attempts**
  (`test_repeated_poisoning_attempts_are_not_rate_limited_or_flagged`): 50 consecutive calls with
  identical poisoned input all succeed identically, with no counter, log, or flag that would surface
  a repeated-attempt pattern to an operator. Against a real, non-deterministic LLM judge, this also
  means an adversary (or ordinary judge flakiness) gets unlimited free retries until a favorable
  verdict lands.

I want to be precise about what this finding does and doesn't show: it does not prove any specific
production LLM judge would be fooled this way — none is implemented yet. It shows that
`check_contradiction()` provides no defense of its own against this input shape, so whatever defense
exists has to live entirely in a not-yet-built production judge implementation. That is a materially
different risk posture than "the mechanism is safe by design."

---

## 5. Same-Maintenance-Window Race (Open Question 3)

**Reproduces: yes, at the `check_contradiction()` / module level.**

Constructed the scenario directly: one stale existing record (a shipping address), two independent
new writes from different sessions (two different replacement addresses), and a judge that
correctly identifies each new write as superseding the stale record in isolation. Calling
`check_contradiction()` once per new write against the same `stale_existing` snapshot — which is
exactly what a maintenance pass following `03-forgetting-strategy.md` §5 step 1 as currently
specified would do, since that step only describes checking each new fact against pre-existing
*older* facts — produces `UPDATE` for **both** writes independently
(`test_two_concurrent_new_facts_both_classified_update_against_same_stale_existing`). Per the design
document, an `UPDATE` verdict triggers archiving the existing record; nothing ever checks the two
new writes against *each other*. Both survive as live, mutually contradictory active records. This
is exactly the failure mode Open Question 3 and self-review §6 flagged as a hypothesis — it
reproduces.

Two structural confirmations, not just a scenario demo:

- `check_contradiction()`'s signature is `(new_record, existing_record, llm_judge)` — there is no
  new-vs-new comparison capability anywhere in this module, even in principle
  (`test_check_contradiction_has_no_new_vs_new_comparison_capability`). Fixing the race isn't a
  matter of calling the existing function differently; it requires new orchestration logic that
  doesn't exist yet.
- `run_maintenance_pass()` never calls `check_contradiction()` under any flag combination — confirmed
  again here (`test_run_maintenance_pass_provides_no_sequencing_or_locking_for_contradiction_checks`),
  consistent with the existing coverage in `test_memory_maintenance.py::TestContradictionCheckNotActivated`.
  There is no sequencing or locking layer in this module that could resolve the race today even if
  someone wanted to. The race is unresolved by construction, not merely untested.

---

## 6. Test Suite and Reproduction

New evaluation suite: `context-engineering/testing/test_contradiction_adversarial.py` — 16 tests,
organized as `TestFalseUpdateClassification` (7), `TestMemoryPoisoning` (3),
`TestSameMaintenanceWindowRace` (3), covering §3–5 above. All 16 pass:

```
pytest context-engineering/testing/test_contradiction_adversarial.py -v
16 passed
```

Full `context-engineering/testing/` suite (run from `core-component-00/`):

```
pytest context-engineering/testing/ -v
154 passed, 1 failed
```

The one failure — `test_acon_benchmark.py::test_acon_vs_context_compressor` — is a pre-existing,
unrelated comparison of `ContextCompressor` against an ACON compression baseline
(`coding_session` fixture: compressor did not reduce token count below the original). I did not
touch `context_compressor.py`, `test_acon_benchmark.py`, or anything in the compression path; `git
status` confirms my changes are limited to this evaluation's new files. This failure is out of this
evaluation's scope and should be routed to whoever owns Context Compression Theory
(`crew/CLAUDE.md` § Research Programme Ownership: Mei-Ling Zhao / Dr. Vance), not to this
contradiction-check gate.

---

## 7. Verdict

**`i_have_completed_adversarial_review=True` should NOT be authorized yet.**

All three adversarial questions produced positive findings against `check_contradiction()` as
currently specified:

- False-`UPDATE` rate on a curated non-contradictory set: **100% (5/5)**, with **0% independent
  mitigation** by the wrapper itself, plus a structural order-sensitivity gap.
- Memory-poisoning: **reproduces** — an engineered contradiction can archive a true, unrelated fact,
  with no rate-limiting or anomaly detection on repeated attempts.
- Same-maintenance-window race: **reproduces**, and is unresolved by construction — no new-vs-new
  comparison capability and no sequencing/locking layer exist anywhere in this module.

None of these findings are surprising given §2's structural read of the code — `check_contradiction()`
was built, correctly, as a thin, testable wrapper around an as-yet-unbuilt judge, not as a
safety-complete mechanism. The gate that requires my sign-off before activation is doing exactly
what it was designed to do.

**What would need to change before I could authorize activation:**

1. A concrete production `llm_judge` implementation, itself adversarially evaluated against at
   minimum the five false-positive patterns in §3 (format/notation variance, subject-identity
   blindness, scope-qualifier blindness) with a materially better than 100% failure rate on that set.
2. A confidence threshold or second-judge/majority-vote step before an `UPDATE` verdict is trusted
   — per §4, a single unverified call currently has unilateral authority to trigger archival.
3. Input handling that treats memory content as untrusted data with respect to the judge call (at
   minimum, structural separation of "content to compare" from "instructions to the judge") — per
   §4's embedded-instruction finding.
4. A same-window sequencing mechanism — either serialize checks per existing-record with the
   existing record's candidacy re-fetched between checks, or add an explicit new-vs-new comparison
   pass — before the batch design in `03-forgetting-strategy.md` §5 step 1 can be trusted not to
   produce the race in §5 above.

None of this is a criticism of the current implementation as scoped — it was never represented as
including these mitigations, and the docstring gate exists precisely because they're missing. This
is the negative-result-with-teeth this pass exists to produce: real findings, reproducible, with the
production activation correctly still blocked.

**Confirmed: the production gate remains untouched and inert.**
`i_have_completed_adversarial_review=True` is not set anywhere in production or default code paths
in this evaluation's changes; `run_maintenance_pass()` was not modified and still refuses
`enable_contradiction_check=True` without that flag
(`RuntimeError`, unchanged, per `test_memory_maintenance.py`). This evaluation informs the eventual
activation decision — it does not perform it, per my documented authority.

---

## 8. Version History

| Version | Date       | Author               | Changes                                        |
| ------- | ---------- | -------------------- | ----------------------------------------------- |
| 1.0     | 2026-07-12 | Dr. Tomasz Wieczorek | Initial adversarial evaluation of `check_contradiction()` |

---

**Maintained by:** Core Component 00 Laboratory
**Reviewing Officer:** Dr. Tomasz Wieczorek, Staff Safety & Evaluation Engineer
**Ratifying Authority:** Dr. Elias Vance, Laboratory Director
