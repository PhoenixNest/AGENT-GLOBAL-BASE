# Role Reconciliation Checkpoint

**Owner:** CHRO Office (Dr. Evelyn Hartwell)  
**Status:** Active  
**Effective Date:** 2026-04-12  
**Trigger:** Before any hiring wave begins  
**Audit Reference:** CHRO Audit Concern 1 — "G39 Ad-Hoc Recruitment — Process Gap"

---

## 1. Executive Summary

During the CHRO audit, a process gap was identified: the **G39 UX Writer (Sarah Chen)** was recruited as an **ad-hoc corrective action** because the role was "inadvertently never assigned to a phase." This created two downstream problems:

1. **Planning gap:** A role existed in the roster but had no phase assignment, meaning it was invisible to the recruitment planning process.
2. **ID sequencing issue:** G-ID `G20` was originally assigned to the UX Writer role in Phase 3B but was never recruited in that phase. The role was later filled as `G39` outside the normal sequence, leaving G20 as an orphaned identifier.

This checkpoint document establishes a **mandatory pre-hiring reconciliation process** to prevent recurrence. It must be executed before any recruitment wave begins — including the upcoming 3-game scaling cycle.

---

## 2. The Role Reconciliation Process

The Role Reconciliation Checkpoint is a **six-step verification** that must be completed and signed off before recruitment execution begins.

### Step 1: Extract All Roles from Approved Recruitment Plan

Extract the complete role inventory from the approved recruitment plan. Each role record must include:

| Field            | Description                                        |
| ---------------- | -------------------------------------------------- |
| Role Name        | e.g., "Studio Director", "Senior Android Engineer" |
| G-ID             | e.g., G1, G2, G3...                                |
| Priority         | e.g., P0 (critical), P1 (high), P2 (standard)      |
| Phase Assignment | e.g., "Phase 1A", "Phase 3B", "Unassigned"         |
| Status           | e.g., "Filled", "Open", "Deferred", "Cancelled"    |
| Division         | e.g., "Engineering", "Production", "Art"           |
| Employment Type  | e.g., "FTE", "Contract"                            |

**Output:** Complete role extraction table.

### Step 2: Cross-Reference Against Phased Assignment Tables

For each extracted role, verify that a phase assignment exists in the recruitment plan's phased assignment tables.

**Validation rule:** `phase_assignment != "Unassigned"` for all roles with `status != "Cancelled"`.

**Output:** List of roles with missing phase assignments (must be empty to proceed).

### Step 3: Verify No Role Is Left Unassigned

Confirm that every role with `status = "Open"` or `status = "Filled"` has a valid phase assignment.

**If any role is found unassigned:**

1. Assign it to the appropriate phase
2. Document the rationale for the late assignment
3. Obtain C-suite sign-off on the corrected plan
4. **Do not proceed** until all roles are assigned

### Step 4: Verify G-ID Sequence Is Continuous

Check that G-IDs are assigned sequentially with no gaps.

**Expected sequence:** G1, G2, G3, ..., Gn (no skipped numbers).

**If gaps are found:**

1. Document each gap with justification (e.g., "G20: UX Writer role — originally Phase 3B G20, recruited as G39 ad-hoc")
2. Retire orphaned IDs so they cannot be reused
3. Continue sequence from the highest used ID + 1

### Step 5: Verify Total FTE Count Matches Plan

Confirm that the total number of roles (FTE + Contract) in the extraction matches the approved headcount plan.

**Validation rule:** `sum(all roles) == approved_headcount`.

**If mismatch is found:**

1. Identify missing or duplicate roles
2. Reconcile with approved plan
3. Obtain C-suite sign-off on corrected plan

### Step 6: C-Suite Sign-Off Before Recruitment Execution

The reconciliation output must be reviewed and signed off by:

| Signatory  | Role                | Confirms                                                                |
| ---------- | ------------------- | ----------------------------------------------------------------------- |
| CHRO       | Dr. Evelyn Hartwell | All roles reconciled, phase assignments valid, G-ID sequence documented |
| CPO        | Marcus Tran-Yoshida | Product org roles align with product roadmap staffing needs             |
| CTO        | Dr. Kenji Nakamura  | Technical org roles align with engineering capacity plan                |
| CDO        | Yuki Tanaka-Chen    | Design org roles align with creative production needs                   |
| User (CEO) | Final authority     | approves the reconciled recruitment plan for execution                  |

**No recruitment may begin without all five sign-offs.**

---

## 3. Checkpoint Checklist

Before recruitment execution begins, complete this checklist:

- [ ] All roles extracted from recruitment plan (role name, G-ID, priority, phase, status, division, employment type)
- [ ] All roles assigned to a phase (no role has `phase_assignment = "Unassigned"`)
- [ ] No unassigned roles found (or all unassigned roles have been assigned with documented rationale)
- [ ] G-ID sequence is continuous (or all gaps are documented with justification and orphaned IDs are retired)
- [ ] Total FTE count matches approved headcount plan
- [ ] Contract roles identified and separated from FTE roles in the extraction
- [ ] C-suite sign-off obtained (CHRO, CPO, CTO, CDO, User)

**Pass Criteria:** All checklist items checked. Zero open findings.

**Fail Criteria:** Any unchecked item. Recruitment is **blocked** until all findings are resolved.

---

## 4. Application to 3-Game Scaling

### 4.1 Context

The 3-game scaling model adds **45 additional FTEs** to the current roster, growing from **38 FTE + 1 Contract (39 total)** to **85 total**.

### 4.2 Expected Output

The Role Reconciliation Checkpoint will produce:

1. **Reconciled role list** — All 45 new roles with:
   - Role name, G-ID, priority, phase assignment, division, employment type
   - Every role assigned to a specific phase (Phase 1 through Phase N, as defined by the scaling plan)

2. **G-ID sequence map** — Continuous sequence from G40 (next available after G39) through G84 (45 new roles), with G20 documented as retired.

3. **Headcount reconciliation** — Verified total: 39 (current) + 45 (new) = 85 (post-scaling).

### 4.3 Execution Timeline

| Milestone                    | Timing                                         |
| ---------------------------- | ---------------------------------------------- |
| Checkpoint initiated         | Before 3-game scaling recruitment begins       |
| Reconciliation complete      | No later than 2 weeks before first hiring wave |
| C-suite sign-off complete    | No later than 1 week before first hiring wave  |
| Recruitment execution begins | Only after all sign-offs obtained              |

---

## 5. G20 ID Gap Documentation

### 5.1 Root Cause

G-ID `G20` was originally assigned to the **UX Writer** role in **Phase 3B** of the recruitment plan. However, the role was never recruited during Phase 3B execution. The gap went unnoticed because:

1. No Role Reconciliation Checkpoint existed at that time
2. The role was not flagged as "unfilled" during phase completion reviews
3. The recruitment plan was not re-validated between phases

### 5.2 Resolution

The UX Writer role was later identified as a staffing gap and recruited **ad-hoc** outside the normal recruitment sequence. It was assigned G-ID `G39` (next available at time of recruitment).

### 5.3 G20 Status

| Field               | Value                                                                                                 |
| ------------------- | ----------------------------------------------------------------------------------------------------- |
| G-ID                | G20                                                                                                   |
| Status              | **Retired**                                                                                           |
| Original Assignment | UX Writer, Phase 3B                                                                                   |
| Actual Recruitment  | G39 (Sarah Chen), ad-hoc corrective action                                                            |
| Retirement Note     | "UX Writer role — originally Phase 3B G20, recruited as G39 ad-hoc. ID retired to prevent confusion." |
| Future Use          | **Never reuse G20.** Future ID assignments skip G20.                                                  |

### 5.4 G-ID Sequence After G39

The next available G-ID after G39 is **G40**. The 3-game scaling cycle will use G40 through G84 (45 roles), with G20 documented as retired and excluded from the sequence.

**Full sequence:** G1–G19, [G20 retired], G21–G39, G40–G84.

---

## 6. Revision History

| Version | Date       | Author                    | Changes                                             |
| ------- | ---------- | ------------------------- | --------------------------------------------------- |
| v1      | 2026-04-12 | Dr. Evelyn Hartwell, CHRO | Initial checkpoint — addresses CHRO Audit Concern 1 |

---

**Acknowledged by:**

| Name                | Role | Date       | Signature |
| ------------------- | ---- | ---------- | --------- |
| Dr. Evelyn Hartwell | CHRO | 2026-04-12 | _Pending_ |
| Marcus Tran-Yoshida | CPO  | —          | _Pending_ |
| Dr. Kenji Nakamura  | CTO  | —          | _Pending_ |
| Yuki Tanaka-Chen    | CDO  | —          | _Pending_ |
| User                | CEO  | —          | _Pending_ |
