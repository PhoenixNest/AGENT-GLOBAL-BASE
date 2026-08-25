# Implementation Plan — Harness Engineering (Layer 3) — Token-Count Compaction Trigger

---

## Metadata

| Field                       | Value                                                                                                                                                                                                                                                                                            |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Plan ID**                 | `2026-08-25-harness-compaction-trigger-remediation`                                                                                                                                                                                                                                              |
| **Layer**                   | 3 — Harness Engineering                                                                                                                                                                                                                                                                          |
| **Source Benchmark Report** | `core-component-00/benchmarks/engineering/harness-engineering/2026-08-25-harness-engineering-enterprise-assessment/enterprise-assessment.md`                                                                                                                                                     |
| **Owner**                   | Kwame Asante (Harness Engineering module lead)                                                                                                                                                                                                                                                   |
| **Reviewer**                | Dr. Elias Vance (independent of Owner)                                                                                                                                                                                                                                                           |
| **Hook-Change Gate**        | **Pending User sign-off** — item I1 touches `.claude/hooks/context-budget-alert.py`; per `pipeline.md`'s Hook-Change Gate, this requires a separate, explicit User approval naming the item and the date, distinct from this plan's own opening — not delegable to Reviewer, Owner, or Dr. Vance |
| **Status**                  | Open — see `log/01-drafting-i1-opened.md`                                                                                                                                                                                                                                                        |

**Reviewer requirement.** No item in this plan may reach `Status: Verified` on the strength of
Owner self-verification — see `pipeline.md` stage 4.

**Execution blocker.** Per `pipeline.md`, Execution on I1 cannot begin until the Hook-Change Gate
above is explicitly granted by the User — Approval-stage sign-off does not substitute for this.

---

## Included Items

| ID  | Source Row                                | Gap (restated, one line)                                                                                                                                                 | Severity (inherited) | Item Owner   | Approach                                                                                                                                                                                                                                                                                                          | Acceptance Criteria                                                                                                    | Test Plan                                                                                                                                                                     | Target Date | Item Status |
| --- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ----------- |
| I1  | Harness R10 (2026-08-25 refresh, row B12) | H-CE01's compaction-enforcement trigger uses raw transcript byte-size rather than an actual token count, per the hook's own code comment naming this as an interim proxy | P2                   | Kwame Asante | Replace the `ALERT_THRESHOLD_KB`/`ENFORCEMENT_THRESHOLD_KB` byte-size proxy in `.claude/hooks/context-budget-alert.py` with an actual token count — the hook already has the transcript content in hand, so a tokenizer call or the model's own reported usage would suffice, per the hook's own stated follow-up | The alert and enforcement thresholds fire based on an actual token-count estimate of the transcript, not raw byte-size | New/updated test in `.claude/hooks/test_context_budget_alert.py` asserting the trigger fires based on token count, with a case where byte-size and token-count would disagree | TBD         | Not Started |

**Rules.**

- **Severity is inherited, never re-derived here** — P2 per the source benchmark's Severity-Ordered
  Remediation Plan (row R3 there, tracked as Backlog row Harness R10 before this plan existed).
- **This item touches `.claude/hooks/*.py`.** Per root `CLAUDE.md` §11, this file governs an
  active hook protocol every qualifying session depends on — the Hook-Change Gate is not a
  formality and Execution must not begin before it is explicitly granted.

---

## Cross-Layer Dependencies

[None identified]

---

## Gate Log

| Stage       | Entry                                                                                                                                          | Summary                                                                                           |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 0 — Trigger | `core-component-00/remediation/engineering/harness-engineering/2026-08-25-harness-compaction-trigger-remediation/log/01-drafting-i1-opened.md` | Topic opened from the 2026-08-25 Harness benchmark refresh's P2 finding (Backlog row Harness R10) |

---

## Open Follow-Up Items

| Item                                                  | Owner | Target Date                      |
| ----------------------------------------------------- | ----- | -------------------------------- |
| Obtain explicit User Hook-Change Gate sign-off for I1 | User  | Before Execution can start on I1 |

---

## Related Records

- **Source benchmark report:** `core-component-00/benchmarks/engineering/harness-engineering/2026-08-25-harness-engineering-enterprise-assessment/enterprise-assessment.md`
- **Prior Harness remediation (closed, unrelated items):** `core-component-00/remediation/engineering/harness-engineering/2026-08-17-harness-engineering-remediation/implementation-plan.md` (item I5 there is the related, but distinct, fix that made H-CE01's enforcement path real in the first place — this plan's I1 refines the trigger signal that fix already enforces on)
- **Sibling plan from the same refresh:** `core-component-00/remediation/engineering/harness-engineering/2026-08-25-harness-rate-limiter-remediation/implementation-plan.md` (Harness R9, `Verified`)
- **Backlog items for this layer (not in this plan):** `core-component-00/remediation/README.md` § Remediation Backlog (Harness R5–R8)
