# Supporting Document 03 — Deployment Guidelines

**Programme:** `2026-07-14-reflexion-memory-system`
**Purpose:** The rollout path for the design specified in `01-technical-options.md` and
`02-storage-specification.md`, phased and gated consistent with this workspace's User Approval
Gate and ASE governance conventions. No production deployment has occurred — this is a plan, not
a status report.

---

## 0. Preconditions

This deployment adds to, and depends on, already-provisioned infrastructure — it does not stand
up a new instance:

- The `qdrant-memory` Docker container (`localhost:6335`) must already be running — it was
  provisioned by the prior `2026-07-10-agent-memory-architecture` programme and is a precondition,
  not part of this rollout.
- The `sentence-transformers/all-MiniLM-L6-v2` model must already be present in the shared model
  cache (`core-component-00/mcp-servers/_shared/models/`) — also a precondition from the prior
  programme, reused unchanged (`01-technical-options.md` §2).
- `agent-memory/server.py` must be reachable and its existing `search_memory`/`health_check`
  tools functioning (even if degraded, per its documented degrade-gracefully contract) before
  extending it.

---

## Phase 1 — Schema and Collection (P0)

1. Add `TRIGGER_TYPES`, `GOVERNANCE_TRIGGERS`, `ReflectionRecord`, and `ReflectionMemory` to
   `context-engineering/implementations/memory_store.py` per `01-technical-options.md` §1.
2. Create the `memory_reflection` Qdrant collection on the existing `qdrant-memory` instance
   (384-dim, matching the existing three collections' vector config exactly).
3. Create `context-engineering/memory/reflection/reflection-log.jsonl` (empty, source-of-truth
   log) and wire `PersistentMemorySink.write_reflection()` alongside its existing
   `write_episodic`/`write_semantic`/`write_procedural` methods.
4. Unit tests in `context-engineering/testing/` covering: trigger-type validation, sacred-default
   behavior for `GOVERNANCE_TRIGGERS`, and round-trip JSONL write/read — run from
   `core-component-00/` per this module's existing test-suite discipline
   (`context-engineering/CLAUDE.md`): `pytest context-engineering/testing/ -v` must stay green.
5. Implement an identity-enforcement mechanism on the authoring script so `logged_by` cannot be
   an arbitrary unauthenticated string — e.g. requiring the script to run only under an
   authenticated human/Director session, matching how git commit authorship is already enforced
   in this workspace. This closes `audits/01-design-stage/01-safety-self-review.md` §2.2
   (Dr. Wieczorek's Open finding: a non-empty-string check is a formatting check, not identity
   verification).

**Gate — Phase 1 begins:** does not start until Phase 1's test suite passes and Dr. Wieczorek has
reviewed the schema for the write-path threat-model concerns raised in `research-report.md`
Finding 4 (see `audits/01-design-stage/01-safety-self-review.md`).

**Gate — Phase 1 is done:** per `01-safety-self-review.md` §3's explicit condition, Phase 1 is not
considered complete until step 5 above is implemented and Dr. Wieczorek has verified it closes
§2.2 with a concrete mechanism, not a documented expectation. This is a P1 item — it blocks
treating Phase 1 as finished, not CEO sign-off on the design itself (§3's own distinction).
`MISTAKE-001`'s Phase 3 migration (the only planned use of the authoring path before broader
rollout) must not proceed until this gate closes.

---

## Phase 2 — Retrieval Surface (P1/P2)

1. Extend `agent-memory/server.py`'s `search_memory` tool to accept `memory_type="reflection"`,
   reusing the existing timeout-guarded, degrade-gracefully call pattern verbatim — no new failure
   mode class introduced.
2. Extend `health_check`'s `point_counts` to include `memory_reflection`, matching the existing
   shape.
3. Add the proactive orchestrator-brief-time retrieval call site to
   `multi-agent-engineering/implementations/swarm_orchestrator.py`, per `01-technical-options.md`
   §5.2. This module has its own existing test suite
   (`multi-agent-engineering/testing/`) — it must stay green after this change:
   `pytest multi-agent-engineering/testing/ -v`.

**Gate:** Phase 2's `swarm_orchestrator.py` change is reviewed against
`multi-agent-engineering/patterns/anti-patterns.md`'s "implicit dependencies" check before merge
— the new retrieval call site must not silently assume `memory_reflection` is populated; an empty
collection (the expected state at initial rollout) must degrade to "no matching reflection found,
proceed" rather than block brief issuance.

---

## Phase 3 — Migration (P1)

1. Author the `MISTAKE-001` `ReflectionRecord` using the Investigator-Authored Write Path
   (`01-technical-options.md` §4), with `migrated_from = "mistake-log.md#MISTAKE-001"` and
   `logged_by` preserving the original investigator of record (Dr. Elias Vance).
2. Update `mistake-log.md`'s status line to record the migration and mark the file superseded,
   per its own stated terms ("migrated into it and this file is superseded, not deleted") — the
   file is not deleted, consistent with this workspace's append-only archive convention.
3. Verify the migrated record round-trips correctly through `search_memory` with
   `memory_type="reflection"` before declaring the migration complete.

---

## Rollback

Every write goes through the JSONL-first pattern already proven for the other three memory
types: if the Qdrant upsert fails or the collection needs to be rebuilt, `reflection-log.jsonl`
is replayed to reconstruct `memory_reflection` from scratch — the same disaster-recovery
guarantee already documented for the other collections in
`2026-07-10-agent-memory-architecture/supporting/05-disaster-recovery-and-resilience.md`. No new
disaster-recovery mechanism is introduced; this is a direct reuse.

---

## Deployment Checklist

**Revised 2026-07-15** by Dr. Elias Vance, under CEO-delegated full authority over this
Programme, after verifying agent assignments against `crew/README.md` and `crew/CLAUDE.md`'s
Laboratory Roster. Two gaps were found and closed: (1) the §0 Preconditions had no named owner —
they were being implicitly assumed rather than verified by anyone before Phase 1 starts, despite
Ravi Deshmukh's cross-cutting dev-environment/dependency mandate existing specifically to own
this; (2) Phase 1/2's reuse of the harness-engineering `error_boundary.py` timeout-guarded,
degrade-gracefully pattern was asserted ("reused verbatim") but never actually reviewed by
harness-engineering's own module lead, Kwame Asante — the plan trusted the authoring engineer's
self-assessment of a pattern they don't own. The Phase 2 anti-pattern review also had a gate
criterion with no named reviewer; Dr. Idris Farouk (the module lead who owns
`multi-agent-engineering/patterns/anti-patterns.md`) is now named explicitly. All other
assignments (Zhao for Phase 1, Wieczorek for the write-path review, Almeida/Fontán for retrieval,
Farouk/Yusuf for the orchestrator hook, Vance for the Phase 3 migration) were verified correct
against each person's actual module ownership and left unchanged.

**Revised again 2026-07-15** (same day, director's final pre-implementation review): Phase 1 §5
added above, and a corresponding checklist row below, so `01-safety-self-review.md` §2.2's Open
finding (no identity enforcement on the authoring script's `logged_by` field) is a checkable
Phase-1 completion gate here, not only a note inside the audit document.

| Step                                                                                                              | Owner                                                                                        | Gate                                                                                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Preconditions verified (§0: `qdrant-memory` container, shared model cache, `agent-memory/server.py` reachability) | Ravi Deshmukh                                                                                | All three §0 preconditions confirmed before Phase 1 begins — his cross-cutting dev-environment/dependency mandate, not implicitly assumed by whoever starts Phase 1                                                                      |
| Phase 1 schema + collection + tests green                                                                         | Mei-Ling Zhao                                                                                | `pytest context-engineering/testing/ -v` passes                                                                                                                                                                                          |
| Phase 1 §5 — authoring-script identity enforcement                                                                | Mei-Ling Zhao (implementation); Dr. Tomasz Wieczorek (verification)                          | Closes `audits/01-design-stage/01-safety-self-review.md` §2.2 with a concrete mechanism — Phase 1 is not "done," and `MISTAKE-001`'s migration (Phase 3) must not proceed, until Wieczorek confirms this closes cleanly                  |
| Phase 1/2 harness-pattern conformance review                                                                      | Kwame Asante                                                                                 | Confirms the `error_boundary.py` timeout-guarded, degrade-gracefully pattern this plan claims to reuse "verbatim" (§0, Phase 2 §1) is applied correctly and introduces no new failure-mode class — signed off by the pattern's own owner |
| Dr. Wieczorek's write-path review                                                                                 | Dr. Tomasz Wieczorek                                                                         | Sign-off recorded in `audits/01-design-stage/01-safety-self-review.md` or a follow-up adversarial-evaluation doc                                                                                                                         |
| Phase 2 retrieval extension + orchestrator hook + tests green                                                     | Sofia Almeida / Diego Fontán (retrieval); Dr. Idris Farouk / Amina Yusuf (orchestrator hook) | `pytest multi-agent-engineering/testing/ -v` passes; anti-pattern review complete (Dr. Idris Farouk, against `multi-agent-engineering/patterns/anti-patterns.md`)                                                                        |
| Phase 3 `MISTAKE-001` migration                                                                                   | Dr. Elias Vance                                                                              | Round-trip verified via `search_memory`                                                                                                                                                                                                  |
| CEO sign-off                                                                                                      | CEO                                                                                          | User Approval Gate — required before Phase 1 begins, per this workspace's stage-gate convention                                                                                                                                          |

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-07-14-reflexion-memory-system`
