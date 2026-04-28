# Pipeline Integration: Mapping to Stages 1, 6, 8, 10

## Pipeline Integration: Mapping to Stages 1, 6, 8, 10

MASVS is enforced by the CSO (Dr. Sarah Chen) through the Cyberspace Security department across four pipeline stages:

### Stage 1: Requirements — Defining MASVS Compliance Targets

**Producer:** CSO (with CPO for PRD alignment)
**Artifact:** SRD (Security Requirements Document)
**Location:** `company/project/<project>/requirements/srd/`

At Stage 1, the SRD defines:

| SRD Section               | MASVS Mapping                                          |
| ------------------------- | ------------------------------------------------------ |
| Security baseline         | MASVS L1 or L2 determination                           |
| MASVS control selection   | Per-category (V1-V8) applicability matrix              |
| MASVS-R applicability     | MASVS-R control selection                              |
| Platform security targets | iOS ATS, Android Keystore, Play Integrity / App Attest |
| Compliance evidence plan  | How each MASVS control will be verified downstream     |

**Gate criterion:** "User has confirmed target platform(s)" — this includes confirming the MASVS level (L1 or L2).

### Stage 6: Code Review — Defect Classification Using MASVS Criteria

**Producer:** CTO (panel) with CSO review
**Artifact:** DEFECT-REPORT.md
**Location:** `company/project/<project>/reviews/code-review/`

At Stage 6, the code review panel classifies defects against MASVS controls:

| MASVS Category                            | Defect Classification     |
| ----------------------------------------- | ------------------------- |
| Any MASVS L1 control failure              | P0 or P1 (blocks release) |
| Any MASVS L2 control failure              | P0 or P1 (blocks release) |
| Any MASVS-R control failure (if selected) | P1 (blocks release)       |
| MASVS control partially implemented       | P2 (user decides)         |
| MASVS control exceeds requirements        | P3 (polish)               |

**Gate criterion:** "User has reviewed Defect Report and made decisions on P2/P3 defects."

### Stage 8: Integrity Verification — MASVS Compliance Confirmation

**Producer:** CTO (panel) with CSO, CPO, CTO-L
**Artifact:** Integrity Verification Sign-off (includes MASVS compliance matrix)
**Location:** `company/project/<project>/reviews/integrity-verification/`

At Stage 8, the panel verifies:

| Verification                                                 | Responsible          |
| ------------------------------------------------------------ | -------------------- |
| All MASVS V1-V7 controls are implemented per SRD             | CSO                  |
| All MASVS V8 controls (if L2) are implemented                | CSO + Platform Leads |
| All MASVS-R controls (if selected) are implemented           | CSO                  |
| Regression testing on all fixed MASVS-related defects passed | Test Lead            |
| No "trim-to-pass" anti-pattern (functionality removal)       | CTO Panel            |

**Gate criterion:** Panel sign-off only — no user approval required at this stage.

### Stage 10: Release Readiness — MASVS Gate Checklist Item #4

**Producer:** CTO (panel) + USER
**Artifact:** RELEASE-CHECKLIST-7-ITEM.md
**Location:** `company/project/<project>/reviews/release/`

Stage 10 includes 7 sign-off items. Item #4 is the MASVS compliance gate:

| #   | Domain                                         | Sign-off Authority | MASVS Reference             |
| --- | ---------------------------------------------- | ------------------ | --------------------------- |
| 4   | Security — SRD enforced, OWASP MASVS compliant | CSO                | All V1-V8 controls verified |

**Gate criterion:** "User has issued the final release decision." All 7 items must be signed off.

---
