---
name: defect-triage-protocol
description: Automated defect triage protocol for mobile test automation — classifying CI test failures into genuine defects vs. environmental noise vs. flaky tests, producing structured Bug Reports from automated failures, correlating test failures to code changes, and escalating to the correct owner. Use when automated tests fail in CI and a triage decision must be made about the failure's nature, severity, and ownership before remediation begins.
version: "1.0.0"
---

# Defect Triage Protocol

## Purpose

When automated tests fail, the failure must be triaged before any remediation begins. Raw
test output is not a defect report — it is evidence. This skill governs how Rachel Kim
converts automated test failures into classified, actionable defect tickets routed to the
correct engineer.

The output of every triage pass is one of three dispositions:

| Disposition                              | Meaning                                                 | Action                              |
| ---------------------------------------- | ------------------------------------------------------- | ----------------------------------- |
| **Genuine defect**                       | Code change introduced a regression                     | File Bug Report; assign to owner    |
| **Flaky test**                           | Test is non-deterministic — no code regression involved | Quarantine test; notify test author |
| **Environment / infrastructure failure** | CI runner, device farm, or network issue                | Retry pipeline; alert DevOps lead   |

## Why This Matters

Automated tests that fail for environmental reasons create noise that masks real defects.
Without triage, engineers waste time investigating CI runner timeouts and treat genuine
regressions as flakiness. A triage protocol converts raw CI failures into a clean signal:
every Bug Report filed against code is a real defect, not a false alarm.

## Triage Process

### Step 1 — Failure Classification

For each failing test, apply this decision tree in order:

```
1. Did the test pass on the previous commit for the same code path?
   NO → probable genuine defect. Continue to Step 2.
   YES → compare environment (runner version, device, OS). If environment changed → infrastructure failure. Otherwise → probable flaky test.

2. Does the failure reproduce on re-run without a code change?
   ALWAYS REPRODUCES → genuine defect. Proceed to Bug Report.
   SOMETIMES REPRODUCES → flaky test. Proceed to quarantine.
   NEVER REPRODUCES → infrastructure failure. Log and retry.

3. Is the failure isolated to a single device, OS version, or runner?
   YES → environment-scoped failure. Investigate device farm / runner health.
   NO → affects all configurations → genuine defect or widespread flakiness.
```

### Step 2 — Genuine Defect: Produce Bug Report

Use this template for every genuine defect identified from automated test output:

```markdown
## Bug Report — BUG-{NNN}

**Test ID:** TC-{NNN}
**Severity:** [P0 | P1 | P2 | P3] ← see severity criteria below
**Platform:** [Android | iOS | Both | Web | Backend]
**Pipeline Stage:** [Stage 6 | Stage 7 | Stage 8 | Stage 10]
**Introduced by:** [Commit SHA] — [Author] — [PR #]

### Description

[One sentence: what the test verified and what failed]

### Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. ...

### Expected Result

[What the test expected]

### Actual Result

[What the test observed — exact assertion failure, stack trace excerpt]

### Evidence

- Test log: [link or attachment]
- Screenshot / recording: [link or attachment]
- Stack trace: [embedded or link]

### Assigned To

[Platform lead for the affected code area — determined by file ownership in git log]
```

### Step 3 — Severity Assignment

Severity is determined by user impact, not by test layer:

| Criterion                                                          | Severity                              |
| ------------------------------------------------------------------ | ------------------------------------- |
| Test failure indicates app crash or data loss                      | P0                                    |
| Test failure indicates security control broken (auth, encryption)  | P0 — also escalate immediately to CSO |
| Test failure indicates a core user flow is completely broken       | P1                                    |
| Test failure indicates a feature is degraded but partially usable  | P2                                    |
| Test failure indicates cosmetic or minor behavioural inconsistency | P3                                    |

When the evidence is ambiguous between P1 and P2, assign P1. The CTO may downgrade to P2
with written rationale. Never assign lower severity to avoid escalation.

### Step 4 — Ownership Assignment

Determine the owning engineer using git log on the failing files:

```bash
# Find most recent author for the failing module
git log --format="%ae %an" -- <path/to/failing/module> | head -5
```

If the failing code spans multiple owners, assign to the chapter lead for the affected
platform (Android Lead, iOS Lead, Backend Chapter Lead, Frontend Chapter Lead).

### Step 5 — Flaky Test: Quarantine

If the failure is classified as flaky:

1. Add the test to `quarantined_tests.yaml` with:
   - Test ID and name
   - Flakiness score (observed failure rate over last N runs)
   - Suspected root cause (timing, shared state, environment dependency)
   - Stabilization owner (test author or feature team lead)
   - Quarantine date and SLA deadline (5 business days from quarantine)

2. Move the test to the non-blocking "flaky suite" in CI — it continues running but no
   longer blocks pipeline gates.

3. Notify the stabilization owner via the defect ticket with the quarantine SLA.

4. Track weekly: if a quarantined test is not fixed within SLA, escalate to VP of Quality
   and the affected platform lead.

### Step 6 — Infrastructure Failure: Log and Escalate

If the failure is classified as an infrastructure or environment failure:

1. Log the incident with timestamp, runner ID, device ID, and failure type.
2. Retry the pipeline to confirm the failure does not reproduce.
3. If the failure reproduces twice on retry: escalate to Thomas Zhang (DevOps Lead) with
   the incident log.
4. Do not file a Bug Report against the application code for an infrastructure failure.

## Triage Batch Report

After each pipeline run with failures, produce a Triage Batch Report:

```markdown
# Triage Batch Report — {Date} — Pipeline Run #{N}

## Summary

| Disposition             | Count |
| ----------------------- | ----- |
| Genuine defects filed   | {N}   |
| Flaky tests quarantined | {N}   |
| Infrastructure failures | {N}   |
| Retried and resolved    | {N}   |

## Genuine Defects

[Table: BUG-NNN | Platform | Severity | Assigned To | Test ID]

## Quarantined Tests

[Table: Test ID | Flakiness Score | Owner | SLA Deadline]

## Infrastructure Failures

[Table: Runner/Device | Failure Type | Action Taken | DevOps Notified?]
```

Publish the Triage Batch Report to the project's `session-log.md` (for Stage 4+ projects)
and distribute to the CTO and affected platform leads.

## Relationship to Defect Classification (Priscilla Oduya)

This skill governs **automated test failure triage** — converting CI output into
classified Bug Reports. The authoritative **P0–P3 severity definitions and escalation
protocol** are owned by the Test Lead (Priscilla Oduya) via her
`defect-triage-and-classification.md` skill. When in doubt about severity classification,
defer to Priscilla's decision tree.

The two skills are complementary:

| Skill                                 | Owner           | Scope                                          |
| ------------------------------------- | --------------- | ---------------------------------------------- |
| `defect-triage-protocol.md`           | Rachel Kim      | Converting automated failures into Bug Reports |
| `defect-triage-and-classification.md` | Priscilla Oduya | P0–P3 classification and escalation authority  |

## Pipeline Cross-References

| Pipeline      | Stage                       | Activity                                       |
| ------------- | --------------------------- | ---------------------------------------------- |
| All pipelines | Stage 5 (Development)       | Triage unit/integration failures from CI       |
| All pipelines | Stage 6 (Code Review)       | Triage failures from review-triggered test run |
| All pipelines | Stage 7 (Automated Testing) | Full triage pass; produce Triage Batch Report  |
| All pipelines | Stage 8 (Integrity)         | Triage regression suite failures               |
| All pipelines | Stage 10 (Release)          | Final release candidate triage pass            |
