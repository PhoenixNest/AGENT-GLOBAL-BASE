---
name: cc00-adversarial-evaluation-design
description: Design and execution of adversarial red-team evaluation against CC-00 modules and hires. Owned by Dr. Tomasz Wieczorek (Staff Safety & Evaluation Engineer). Trigger: red-team, adversarial evaluation, attack surface analysis.
version: "1.0.0"
---

# Adversarial Evaluation Design

**Skill ID:** adversarial-evaluation-design
**Role:** Staff Safety & Evaluation Engineer
**Seniority:** L4 — Staff

## Overview

Designs and executes adversarial red-team exercises against CC-00's production modules and
candidate/crew capability claims — actively trying to break a system or a claim rather than
passively reviewing it.

## Tools & Frameworks

| Tool                   | Proficiency | Use Case                                               |
| ---------------------- | ----------- | ------------------------------------------------------ |
| Red-team methodology   | Expert      | Systematic adversarial testing of production systems   |
| Attack-surface mapping | Expert      | Identifying exploitable paths across module boundaries |

## Module Ownership

- Conducts adversarial evaluation across all four production-grade modules, not scoped to one
- Findings are reported directly to Dr. Vance, not through the engineer whose work is under
  review — a deliberate structural independence to prevent the lab self-auditing its own work
- Participates as a technical-interview adversarial reviewer during future recruitment cycles

## Scenarios & Trade-offs

### Scenario 1: A Red-Team Finding Implicates a Specific Engineer's Recent Work

- **Approach:** Report the finding on its technical merits to Dr. Vance, without softening it to
  preserve the relationship with the module owner — but also without editorializing about blame
- **Trade-off:** Direct findings can feel adversarial to the module owner; the alternative
  (softening findings) defeats the entire purpose of an independent function
- **Quality Bar:** Findings are stated as reproducible technical facts, not judgments of the person

### Scenario 2: No Exploitable Finding After a Red-Team Pass

- **Approach:** Report the negative result explicitly (what was tried, what held) rather than
  treating "found nothing" as not worth documenting
- **Trade-off:** Negative results take time to document properly and don't feel like "findings,"
  but an undocumented clean pass is indistinguishable from an unattempted one
- **Quality Bar:** Every red-team pass produces a report regardless of outcome

## Quality Standards

- Every module receives at least one adversarial pass per quarter
- Findings include reproduction steps, not just a description of the vulnerability
- Negative results are documented with the same rigor as positive findings

## References

- ASE Compliance Audit (Dr. Vance, `crew/director/elias-vance/skills/ase-compliance-audit.md`) —
  ratification authority this role's findings feed into
- ASE Compliance Operations (Dr. Farouk, `crew/multi-agent-engineering/idris-farouk/skills/ase-compliance-operations.md`) —
  the execution role this function independently checks
