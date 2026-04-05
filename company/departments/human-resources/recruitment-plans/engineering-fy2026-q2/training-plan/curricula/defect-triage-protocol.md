# Defect Triage Protocol (P0–P3)

## Module Objectives

After completing this module, the trainee must be able to:

1. Independently classify defects as P0–P3 using the decision tree
2. Distinguish between user-impacting defects and technical-only defects
3. Understand escalation paths for each severity level
4. Conduct defect triage sessions
5. Understand the user-decision gate process for P2/P3 defects

## Trainee

| Trainee    | Role                 | Deadline | Verification                                                    |
| ---------- | -------------------- | -------- | --------------------------------------------------------------- |
| Rachel Kim | Test Automation Lead | Day 30   | Classify 10 sample defects correctly (≥8/10 matching Test Lead) |

## Prerequisites

None required.

## Course Structure

### Session 1: Defect Severity System Overview (1.5 hours, led by Test Lead)

**Core Principle:** Calibrate to **USER impact**, not technical complexity. A P1 from a user's perspective may be a P3 from a code perspective and vice versa.

**P0 — Critical (App Crash / Data Loss / Security Breach)**

| Characteristic | Description                                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------------------------- |
| User impact    | App unusable, data destroyed, or personal information exposed                                                          |
| Scope          | Affects all or majority of users                                                                                       |
| Workaround     | None available                                                                                                         |
| Examples       | App crashes on launch; payment processing fails for all users; PII exposed in API response; login broken for all users |
| Resolution     | **Non-negotiable fix** — blocks release                                                                                |

**P1 — High (Core Feature Broken / Major UX Failure)**

| Characteristic | Description                                                                                                     |
| -------------- | --------------------------------------------------------------------------------------------------------------- |
| User impact    | Primary user journey blocked or severely degraded                                                               |
| Scope          | Affects significant subset of users (≥10%)                                                                      |
| Workaround     | None or impractical                                                                                             |
| Examples       | Search returns no results; checkout fails intermittently; push notifications not delivered; offline mode broken |
| Resolution     | **Non-negotiable fix** — blocks release                                                                         |

**P2 — Medium (Minor Feature Degraded / Cosmetic Issue)**

| Characteristic | Description                                                                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| User impact    | Secondary feature impaired; visual defect noticeable                                                                                                         |
| Scope          | Affects limited users or specific edge cases                                                                                                                 |
| Workaround     | Available but inconvenient                                                                                                                                   |
| Examples       | Profile picture not loading on specific device; sorting order incorrect in one table view; typo in error message; color contrast below WCAG AA on one screen |
| Resolution     | **User decides** — fix or defer                                                                                                                              |

**P3 — Low (Polish / Nice-to-Have)**

| Characteristic | Description                                                                                                      |
| -------------- | ---------------------------------------------------------------------------------------------------------------- |
| User impact    | No functional impact; aesthetic or convenience improvement                                                       |
| Scope          | Narrow edge cases or internal-only                                                                               |
| Workaround     | Trivial                                                                                                          |
| Examples       | Animation timing slightly off; loading state flickers for <100ms; log message has typo; code comment is outdated |
| Resolution     | **User decides** — fix or defer                                                                                  |

### Session 2: Decision Tree Walkthrough (1.5 hours, led by Test Lead)

```
Defect Reported
      │
      ▼
┌─────────────────────────────────┐
│ Does it cause app crash, data   │
│ loss, or security breach?       │
│                                 │
│ YES → **P0**                    │
│ NO  ↓                           │
└─────────────────────────────────┘
      ▼
┌─────────────────────────────────┐
│ Is a core user journey blocked  │
│ or severely degraded?           │
│                                 │
│ YES → **P1**                    │
│ NO  ↓                           │
└─────────────────────────────────┘
      ▼
┌─────────────────────────────────┐
│ Is a secondary feature impaired │
│ or is there a noticeable        │
│ cosmetic issue?                 │
│                                 │
│ YES → **P2**                    │
│ NO  ↓                           │
└─────────────────────────────────┘
      ▼
**P3** — Polish / nice-to-have
```

**Calibration Examples (10 real-world defects discussed in session):**

| #   | Defect                                                          | Classification | Reasoning                                                                         |
| --- | --------------------------------------------------------------- | -------------- | --------------------------------------------------------------------------------- |
| 1   | App crashes on Android 13 when opening camera                   | **P0**         | Crash on core feature; affects all Android 13 users                               |
| 2   | Payment succeeds but confirmation email not sent                | **P1**         | Core user journey (payment confirmation) degraded; users can't verify transaction |
| 3   | Button color is #3366FF instead of #336699                      | **P3**         | Cosmetic only; no functional impact                                               |
| 4   | Search results sorted by date instead of relevance              | **P2**         | Secondary feature impaired; users can still find results by scrolling             |
| 5   | Login fails for users with email containing + character         | **P1**         | Core user journey (login) broken for a subset of users; no workaround             |
| 6   | Stack trace visible in error response body                      | **P0**         | Security breach — exposes internal implementation details to attacker             |
| 7   | Loading spinner appears for 50ms before cached content displays | **P3**         | Polish — functional but visually jarring                                          |
| 8   | Push notification delivered but tapping it opens wrong screen   | **P1**         | Core feature (notification navigation) broken; user experience severely degraded  |
| 9   | Profile page shows "Last active: null" for new users            | **P2**         | Cosmetic issue; workaround exists (refresh page)                                  |
| 10  | API returns 500 error when request body exceeds 10MB            | **P2**         | Edge case; most users won't hit 10MB; workaround exists (compress upload)         |

### Session 3: Escalation Paths (1 hour, led by Test Lead)

| Severity | Who Decides           | Escalation Path                           | Release Impact                      |
| -------- | --------------------- | ----------------------------------------- | ----------------------------------- |
| **P0**   | Test Lead (automatic) | Test Lead → CTO → CSO (if security)       | **Blocks release** — non-negotiable |
| **P1**   | Test Lead (automatic) | Test Lead → VP of affected division → CTO | **Blocks release** — non-negotiable |
| **P2**   | **USER**              | Test Lead → CPO → User for decision       | User decides fix or defer           |
| **P3**   | **USER**              | Test Lead → CPO → User for decision       | User decides fix or defer           |

**User-Decision Gate Process (P2/P3):**

1. Defect classified as P2 or P3 by Test Lead
2. Defect added to P2/P3 decision queue
3. CPO reviews queue weekly, adds recommendation (fix/defer)
4. User reviews P2/P3 queue and makes final decision
5. If user defers, defect logged for future consideration; does not block release
6. If user fixes, defect assigned to owning team with priority based on release timeline

**Key Rule:** P0/P1 classification is **final** — no one can override it, including the user. P2/P3 classification can be challenged by the user (e.g., user may upgrade a P2 to P1 if it impacts their specific use case).

### Session 4: Self-Directed Classification Exercise (2 hours, trainee works independently)

The trainee independently classifies 10 sample defects using the decision tree. The Test Lead will provide the 10 defect descriptions after Session 3. The trainee must:

1. Read each defect description
2. Apply the decision tree
3. Classify as P0, P1, P2, or P3
4. Write 1-2 sentences of reasoning for each classification

### Session 5: Classification Review (1 hour, led by Test Lead)

- Trainee's 10 classifications compared against Test Lead's classifications
- Discrepancies discussed — reasoning compared
- If ≥8/10 match: PASS
- If <8/10 match: FAIL — one revision cycle (trainee re-classifies the incorrect ones with Test Lead guidance, then re-takes exercise with 10 new defects)

## Pass/Fail Criteria

**PASS:** ≥8 of 10 classifications match Test Lead's classification.

**FAIL:** <8 of 10 match after second attempt. Position reopened for recruitment.

**Deadline:** Day 30 of probationary period. No extensions.

## Resources

- Defect severity system: `company/library/topics/testing.md` (defect severity section)
- Decision tree diagram: this document, Session 2
- Sample defects for exercises: Provided by Test Lead after Session 3
