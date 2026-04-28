---
name: defect-triage-and-classification
description: Classify every identified defect by severity before remediation begins. Severity determines who decides whether to fix it, when it must be fixed, and whether it blocks release.
---

# Defect Triage and Classification

## Purpose

Classify every identified defect by severity before remediation begins. Severity determines who decides whether to fix it, when it must be fixed, and whether it blocks release. No defect proceeds to remediation without a severity classification.

## Severity Definitions

| Level | Definition                                                           | Release Impact                  | Decision Authority                |
| ----- | -------------------------------------------------------------------- | ------------------------------- | --------------------------------- |
| P0    | App crash / data loss / security breach                              | Blocks release — non-negotiable | CTO + CSO — cannot be overridden  |
| P1    | Core feature broken / major UX failure (feature completely unusable) | Blocks release — non-negotiable | CTO — cannot be overridden        |
| P2    | Minor feature degraded / cosmetic issue / edge-case UX problem       | User decides to fix or defer    | User has explicit final authority |
| P3    | Polish / nice-to-have / minor visual inconsistency                   | User decides to fix or defer    | User has explicit final authority |

**Authority rule:** P0/P1 classification is final. The user cannot override a P0 or P1 classification to permit release. P2/P3 decisions belong entirely to the user — the Test Lead makes no judgement on those deferrals.

## Classification Decision Tree

For each defect, apply the tree in order:

```
1. Does this cause an app crash or data loss?
   YES → P0. Stop here.

2. Does this involve a security vulnerability (data exposure, auth bypass, insecure storage)?
   YES → P0. Stop here. Escalate to CSO immediately.

3. Is the affected feature completely unusable for its primary purpose?
   YES → P1. Stop here.

4. Does this block the primary user flow from completing?
   YES → P1. Stop here.

5. Is the feature degraded but partially functional, or is this cosmetic?
   Degraded but usable → P2.
   Cosmetic / visual only → P3.
```

**Ambiguous cases:** If the Test Lead cannot determine between P1 and P2, classify as P1. Err toward severity, not leniency. The CTO reviews all P1 classifications and may downgrade to P2 with written rationale.

## Escalation Protocol

### P0 Escalation

1. Test Lead immediately notifies CTO and CSO — do not wait for the next review cycle
2. CTO halts all other development on the affected platform
3. CTO assigns the highest-available engineer to remediation
4. Fixed within 24 hours of identification or the release schedule is formally revised
5. CSO reviews all P0 security defects personally before re-classification to fixed

### P1 Escalation

1. Test Lead notifies CTO at the end of the current test run
2. CTO assigns a named engineer and sets a remediation deadline
3. Test Lead verifies the fix and confirms regression passes before closing

### P2/P3 User Decision Gate

After each test run, the Test Lead produces a P2/P3 Decision Request for the user:

```markdown
## P2/P3 Decision Request — {Date}

The following defects have been classified as P2 or P3. As the product owner,
you have final authority to fix or defer each item. Please confirm your decision
for each before Stage {N} can close.

| Bug ID  | Severity | Description   | Fix or Defer?     |
| ------- | -------- | ------------- | ----------------- |
| BUG-{N} | P2       | [description] | [ ] Fix [ ] Defer |
| BUG-{N} | P3       | [description] | [ ] Fix [ ] Defer |

Deferred defects are documented in the Defect Report and will not block release.
They may be addressed in a future release.
```

User confirms each decision. Decisions are recorded in the Defect Report and cannot be changed retroactively once a stage closes.

## Defect Report Format

The Defect Report is produced at Stage 6 (Code Review) and updated at Stage 7 (Automated Testing):

```markdown
# Defect Report — {Project Name} — v{N} — {Date}

## P0 Defects

[Table: Bug ID | Description | Status | Assigned | Resolved Date]

## P1 Defects

[Table: Bug ID | Description | Status | Assigned | Resolved Date]

## P2 Defects — User Decision Required

[Table: Bug ID | Description | User Decision | Decision Date]

## P3 Defects — User Decision Required

[Table: Bug ID | Description | User Decision | Decision Date]

## Sign-off Gate

- [ ] All P0 defects resolved
- [ ] All P1 defects resolved
- [ ] User has confirmed Fix or Defer for all P2 defects
- [ ] User has confirmed Fix or Defer for all P3 defects
- [ ] Test Lead sign-off: Priscilla Oduya
```
