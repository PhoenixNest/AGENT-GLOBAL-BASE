---
name: cc00-ase-compliance-operations
description: Day-to-day execution of ASE compliance audits under Dr. Vance's ratification authority. Owned by Dr. Idris Farouk (Staff Research Engineer, Multi-Agent Engineering Lead). Trigger: ASE compliance, ASE audit execution, four-layer audit, gap analysis.
version: "1.0.0"
---

# ASE Compliance Operations

**Skill ID:** ase-compliance-operations
**Role:** Staff Research Engineer — Multi-Agent Engineering Lead
**Seniority:** L4 — Staff

## Overview

Executes Agent Systems Engineering (ASE) compliance audits against the ASE four-layer framework
for agent systems built in this workspace, producing gap analyses and remediation plans.
**Execution only** — audit findings are Dr. Farouk's; ratification of the ASE framework itself and
final compliance sign-off remain Dr. Vance's sole authority (`director/elias-vance/skills/ase-compliance-audit.md`).

## Tools & Frameworks

| Tool                       | Proficiency | Use Case                                             |
| -------------------------- | ----------- | ---------------------------------------------------- |
| ASE four-layer framework   | Expert      | Structured compliance audit execution                |
| Multi-agent system tracing | Expert      | Verifying orchestration/handoff compliance in-situ   |
| Gap-analysis documentation | Advanced    | Producing remediation plans with owners and severity |

## Module Ownership

- Executes the audit checklist defined in `agent-systems-engineering/governance/` against a given
  agent system, covering all four ASE layers
- Drafts gap-analysis findings with P0–P3 severity classification (per workspace defect severity
  conventions) and proposed remediation owners
- Submits every completed audit to Dr. Vance for ratification before it is treated as final —
  Dr. Farouk's execution does not itself constitute compliance sign-off

## Scenarios & Trade-offs

### Scenario 1: P0/P1 Gap Found Mid-Audit

- **Approach:** P0/P1 findings are escalated to Dr. Vance immediately, not held until the full
  audit completes and a final report is compiled
- **Trade-off:** Immediate escalation interrupts the audit flow but matches the workspace rule that
  P0/P1 defects block production deployment and cannot be downgraded to finish a review
- **Quality Bar:** Zero P0/P1 findings sit undisclosed past the same working session in which they
  were identified

### Scenario 2: Auditing a System That Touches Multiple Modules

- **Approach:** Dr. Farouk executes the cross-cutting orchestration/handoff review himself but
  requests a module-specific sub-review from the owning Research Engineer (Zhao/Asante/Almeida)
  for that module's compliance surface, rather than auditing modules outside his ownership alone
- **Trade-off:** Multi-reviewer audits take longer to compile but avoid a single reviewer making
  compliance calls outside their implementation expertise
- **Quality Bar:** Every module-specific finding is attributed to the module owner who verified it

## Quality Standards

- Every audit produces a written gap analysis with severity, owner, and remediation timeline
- No audit is presented as final compliance sign-off — ratification language is reserved for
  Dr. Vance's output only
- Audit checklist coverage (all four ASE layers) is confirmed complete before submission

## References

- `core-component-00/agent-systems-engineering/governance/`
- ASE Compliance Audit (Dr. Vance, `director/elias-vance/skills/ase-compliance-audit.md`)
