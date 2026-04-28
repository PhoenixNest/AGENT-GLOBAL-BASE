# Assessment Workflow: Verification at Each Gate

## Assessment Workflow: Verification at Each Gate

### Self-Assessment Methodology

MASVS self-assessment is performed by the CSO (or delegated Security Engineer) at each relevant pipeline stage:

| Step | Activity                                      | Responsible     | Stage    |
| ---- | --------------------------------------------- | --------------- | -------- |
| 1    | Identify applicable MASVS controls from SRD   | CSO             | Stage 1  |
| 2    | Create verification checklist per control     | CSO             | Stage 1  |
| 3    | Implement controls per platform conventions   | Platform Leads  | Stage 5  |
| 4    | Verify controls via code review               | CTO Panel + CSO | Stage 6  |
| 5    | Verify controls via automated testing         | Test Lead       | Stage 7  |
| 6    | Confirm compliance via integrity verification | CSO             | Stage 8  |
| 7    | Final sign-off at release readiness           | CSO             | Stage 10 |

### Evidence Collection Requirements

For each MASVS control, the following evidence must be collected:

| Evidence Type               | Description                                                                    | Collection Point |
| --------------------------- | ------------------------------------------------------------------------------ | ---------------- |
| **Design evidence**         | ADRs, UML diagrams, threat models showing control is addressed in architecture | Stage 3          |
| **Implementation evidence** | Source code references, configuration files, platform API usage                | Stage 5          |
| **Test evidence**           | Unit tests, integration tests, penetration test results                        | Stage 7          |
| **Review evidence**         | Code review sign-off, panel verification notes                                 | Stage 6, 8       |
| **Runtime evidence**        | Play Integrity / App Attest results, crash reports, security monitoring        | Stage 10         |

Evidence is stored in `company/project/<project>/security/` with subdirectories:

- `audits/` — Security audit reports
- `compliance/` — MASVS control-by-control evidence
- `penetration-tests/` — Penetration test results

### Panel Review Process

At each MASVS-related gate review (Stages 6, 8, 10), the panel follows this process:

1. **CSO presents MASVS compliance matrix** — showing each control as Pass/Fail/Partial
2. **Panel reviews failures** — any Fail is classified as P0/P1 defect
3. **Panel reviews partials** — classified as P2 defects (user decides)
4. **Panel signs off** — if all mandatory controls Pass, gate is approved
5. **User reviews P2/P3** — at Stages 6 and 7, user makes final decision on deferrable items

### External Certification Path

For applications requiring formal MASVS certification (beyond self-assessment):

| Step | Action                                         | Notes                                                    |
| ---- | ---------------------------------------------- | -------------------------------------------------------- |
| 1    | Engage accredited MASVS assessor               | OWASP maintains list of accredited assessors             |
| 2    | Provide SRD + compliance evidence              | From `security/compliance/` directory                    |
| 3    | Assessor performs independent verification     | Includes manual testing and reverse engineering analysis |
| 4    | Assessor issues certification report           | Report is stored in `security/audits/`                   |
| 5    | Report is included in Stage 10 release package | Part of release readiness evidence                       |

External certification is **recommended for L2 applications** in regulated industries and **mandatory for government contracts** that require it.

---
