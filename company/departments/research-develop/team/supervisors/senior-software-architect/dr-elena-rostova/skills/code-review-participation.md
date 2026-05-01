---
name: code-review-participation
description: Conduct architecture-focused code reviews during Stage 6 — evaluating implementation conformance to ADRs, identifying architectural drift, and producing structured defect reports with P0–P3 severity classifications that feed the Stage 6 remediation loop.
version: "1.0.0"
---

# Code Review Participation

| Competency                    | Description                                                            | Quality Criteria                                                                                                                          |
| ----------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| ADR Conformance Check         | Verify implementation matches approved Stage 3 architectural decisions | Every ADR decision has a corresponding code-level verification; deviations are flagged as P0 (if security) or P1–P2 (if functional)       |
| Architectural Drift Detection | Identify patterns that deviate from the agreed architecture            | Catches coupling violations, layering breaches, and technology substitutions not covered by an ADR; documents with code evidence          |
| Defect Classification         | Classify review findings as P0/P1/P2/P3 per pipeline severity rules    | P0 = crash/security breach; P1 = core feature broken; P2/P3 = quality/style. Classification matches pipeline definitions — non-negotiable |
| Remediation Guidance          | Provide specific, actionable remediation per finding                   | Each finding includes: file + line number, defect description, severity, and a concrete corrected code example or architectural pattern   |

## Execution Guidance

### Stage 6 Architecture Review Checklist

For each ADR in the Stage 3 Engineering Package, verify:

| Verification Point   | Check                                                          |
| -------------------- | -------------------------------------------------------------- |
| Technology selection | Frameworks/libraries in use match ADR-approved choices         |
| Layer boundaries     | No cross-layer direct dependencies (e.g., UI calling DB layer) |
| Security controls    | All ADR-mandated security controls are implemented             |
| Data flow            | Data flows match the approved architecture diagram             |
| Error handling       | All external call sites have documented error boundaries       |

### Defect Severity Classification

Apply the pipeline severity definitions strictly:

| Severity | Definition                                   | Action at Stage 6                                    |
| -------- | -------------------------------------------- | ---------------------------------------------------- |
| P0       | Crash, data loss, or security breach         | Blocks all advancement; re-review required after fix |
| P1       | Core feature non-functional or ADR deviation | Blocks advancement; re-review after fix              |
| P2       | Degraded UX; non-critical path broken        | User decides whether to block                        |
| P3       | Style, naming, minor quality issue           | Fix in next sprint; does not block                   |

After any P0/P1 remediation, the full Stage 6 review panel repeats from the beginning — it does not resume at defect verification only.
