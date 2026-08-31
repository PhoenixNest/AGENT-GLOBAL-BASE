# Implementation Plan — Harness Engineering (Layer 3) — Token-Aware Rate Limiting

---

## Metadata

| Field                       | Value                                                                                                                                                 |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Plan ID**                 | `2026-08-25-harness-rate-limiter-remediation`                                                                                                         |
| **Layer**                   | 3 — Harness Engineering                                                                                                                               |
| **Source Benchmark Report** | `core-component-00/platform/benchmarks/engineering/harness-engineering/2026-08-25-harness-engineering-enterprise-assessment/enterprise-assessment.md` |
| **Owner**                   | Kwame Asante (Harness Engineering module lead)                                                                                                        |
| **Reviewer**                | Dr. Elias Vance (independent of Owner)                                                                                                                |
| **Hook-Change Gate**        | N/A — the fix lands in `implementations/error_boundary.py`'s `RateLimiter` class, not `.claude/hooks/*.py`                                            |
| **Status**                  | Verified — see `log/04-verification-i1-verified.md`                                                                                                   |

**Reviewer requirement.** No item in this plan may reach `Status: Verified` on the strength of
Owner self-verification — see `pipeline.md` stage 4.

---

## Included Items

| ID  | Source Row                              | Gap (restated, one line)                                                                                                                                 | Severity (inherited) | Item Owner   | Approach                                                                                                                                                                                                                                                                            | Acceptance Criteria                                                                                                                              | Test Plan                                                                                                                                                                                                              | Target Date | Item Status                                         |
| --- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | --------------------------------------------------- |
| I1  | Harness R9 (2026-08-25 refresh, row B7) | `RateLimiter` counts requests, not tokens — a burst of large-payload prompts can exhaust real provider capacity while the limiter still reports headroom | P1                   | Kwame Asante | Add a per-request token-cost parameter to `RateLimiter.acquire()` (estimated pre-call or measured post-call) and size the bucket in tokens/minute rather than requests/minute, matching the shared-registry/typed-classification precedent already set by this module's I1–I5 fixes | A sequence of large-payload requests whose cumulative token cost exceeds capacity is throttled by the limiter even while request count stays low | New test asserting `acquire()` blocks/delays once cumulative token cost (not request count) exceeds the configured budget, and a regression test confirming small-payload bursts still pass through at the old cadence | TBD         | Verified — see `log/04-verification-i1-verified.md` |

**Rules.**

- **Severity is inherited, never re-derived here** — P1 per the source benchmark's Severity-Ordered
  Remediation Plan (row R1 there, tracked as Backlog row Harness R9 before this plan existed).
- No other item is admitted into this plan — the refresh's other new finding (H-CE01's byte-size
  compaction trigger, tracked as Harness R10) is P2 with no dependency link to this P1, so per
  `pipeline.md` § Scoping Rule it stays in the Remediation Backlog rather than joining this plan.

---

## Cross-Layer Dependencies

[None identified]

---

## Gate Log

| Stage            | Entry                                                                                                                                                   | Summary                                                                                                                                           |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0 — Trigger      | `core-component-00/platform/remediation/engineering/harness-engineering/2026-08-25-harness-rate-limiter-remediation/log/01-drafting-i1-opened.md`       | Topic opened from the 2026-08-25 Harness benchmark refresh's new P1 finding (Backlog row Harness R9)                                              |
| 2 — Approval     | `core-component-00/platform/remediation/engineering/harness-engineering/2026-08-25-harness-rate-limiter-remediation/log/02-approval-i1-approved.md`     | Dr. Vance approved Kwame Asante's Approach as independent Reviewer                                                                                |
| 3 — Execution    | `core-component-00/platform/remediation/engineering/harness-engineering/2026-08-25-harness-rate-limiter-remediation/log/03-execution-i1-executed.md`    | `RateLimiter` made token-aware (`token_cost` param, tokens/minute bucket, oversized-call fix); 5 new/updated tests; full suite 83 passed          |
| 4 — Verification | `core-component-00/platform/remediation/engineering/harness-engineering/2026-08-25-harness-rate-limiter-remediation/log/04-verification-i1-verified.md` | Dr. Vance independently re-read the diff, re-derived the test arithmetic, and re-ran the suite himself (83 passed); confirmed; `Status: Verified` |

---

## Open Follow-Up Items

[None]

---

## Related Records

- **Source benchmark report:** `core-component-00/platform/benchmarks/engineering/harness-engineering/2026-08-25-harness-engineering-enterprise-assessment/enterprise-assessment.md`
- **Prior Harness remediation (closed, unrelated items):** `core-component-00/platform/remediation/engineering/harness-engineering/2026-08-17-harness-engineering-remediation/implementation-plan.md`
- **Backlog items for this layer (not in this plan):** `core-component-00/platform/remediation/README.md` § Remediation Backlog (Harness R5–R8, R10)
