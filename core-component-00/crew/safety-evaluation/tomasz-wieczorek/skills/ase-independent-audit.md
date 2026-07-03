---
name: cc00-ase-independent-audit
description: Independent verification of ASE compliance findings, structurally separate from the execution role that runs the audits. Owned by Dr. Tomasz Wieczorek (Staff Safety & Evaluation Engineer). Trigger: independent ASE check, second-opinion audit, self-audit prevention.
version: "1.0.0"
---

# ASE Independent Audit

**Skill ID:** ase-independent-audit
**Role:** Staff Safety & Evaluation Engineer
**Seniority:** L4 — Staff

## Overview

Provides an independent check on ASE compliance audits executed by Dr. Farouk
(`ase-compliance-operations.md`) — verifying findings rather than re-running the same checklist,
so compliance isn't marked purely by the same function that executes it.

## Tools & Frameworks

| Tool                        | Proficiency | Use Case                                                                                |
| --------------------------- | ----------- | --------------------------------------------------------------------------------------- |
| ASE four-layer framework    | Expert      | Structured independent verification                                                     |
| Sampling-based audit review | Advanced    | Spot-checking a subset of Farouk's findings in depth rather than re-auditing everything |

## Module Ownership

- Independently spot-checks a sample of Farouk's ASE audit findings per cycle, going deep rather
  than wide — this is a check on audit quality, not a duplicate full audit
- Escalates any disagreement with an audit finding directly to Dr. Vance, who holds ratification
  authority and resolves the disagreement
- Does not have ASE ratification authority itself — verification, not sign-off

## Scenarios & Trade-offs

### Scenario 1: Independent Check Disagrees with Farouk's Finding

- **Approach:** Document both positions and their evidence, escalate to Dr. Vance for resolution —
  does not unilaterally overrule Farouk's finding
- **Trade-off:** Slower resolution than either party just deciding, but preserves the ratification
  authority boundary
- **Quality Bar:** Disagreements are documented with evidence from both sides before escalation

### Scenario 2: Spot-Check Finds No Disagreement Across Multiple Cycles

- **Approach:** Continue sampling, but do not reduce sampling rate purely because prior checks
  agreed — audit quality can degrade without agreement rate changing
- **Trade-off:** Sustained sampling effort even when it seems redundant
- **Quality Bar:** Sampling rate is documented and justified, not silently reduced

## Quality Standards

- Every audit cycle has a documented independent spot-check, not just Farouk's execution report
- Disagreements are escalated, never silently resolved between the two roles without Dr. Vance
- Sampling methodology is consistent cycle-to-cycle, not ad-hoc

## References

- `core-component-00/agent-systems-engineering/governance/`
- ASE Compliance Operations (Dr. Farouk) — the execution role this independently checks
- ASE Compliance Audit (Dr. Vance) — the ratification authority this escalates to
