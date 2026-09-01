---
paths:
  - "**/agent-systems-governance-framework/**"
description: Agent Systems Governance Framework (ASGF) — active when working in agent-systems-governance-framework/
---

# Agent Systems Governance Framework (ASGF)

**Authority:** ADR-ASGF-001 (ratified 2026-04-28)
**Governing Authority:** Dr. Elias Vance, Laboratory Director — Core Component 00

---

## What Is ASGF?

ASGF is the **mandatory governing framework** for all LLM-powered systems in this organization. It is the meta-layer above the five CC-00 engineering modules, defining:

- **Compliance standards** every LLM system must satisfy before production
- **Cross-cutting patterns** that span multiple CC-00 layers
- **Integration contracts** between the five engineering modules

---

## ASGF Compliance Workflow

| Step | Action                                                     | Gate                   |
| ---- | ---------------------------------------------------------- | ---------------------- |
| 1    | Build the system against CC-00 module patterns             | —                      |
| 2    | Run ASGF compliance audit against `compliance-standard.md` | Checklist per layer    |
| 3    | Remediate all P0 and P1 gaps                               | ASGF-Compliant verdict |
| 4    | System enters production                                   | —                      |
| 5    | Post-incident or quarterly: re-audit                       | Updated verdict        |

---

## Key Governance Documents

All in `core-component-00/framework/00-agent-systems-governance-framework/`:

| Document                                | Purpose                                   |
| --------------------------------------- | ----------------------------------------- |
| `governance/adr-asgf-001.md`            | The ratifying ADR — why ASGF is mandatory |
| `governance/compliance-standard.md`     | Per-layer requirements                    |
| `governance/maturity-model.md`          | Levels 0–5 maturity model                 |
| `integration/four-layer-composition.md` | Runtime integration contracts             |

---

## Cross-Cutting Design Patterns

| Pattern                         | Problem Solved                            |
| ------------------------------- | ----------------------------------------- |
| `canonical-source-of-truth.md`  | Agent identity drift                      |
| `paired-artifacts.md`           | Security as afterthought                  |
| `defect-severity-vocabulary.md` | Inconsistent escalation thresholds        |
| `anti-pattern-firewall.md`      | Local optimization at system expense      |
| `progress-sync-protocol.md`     | Silent failures in long-running pipelines |

---

## Behavior Rules for ASGF Work

1. ASGF is mandatory — no LLM system bypasses ASGF compliance before production
2. Run compliance audits using `compliance-standard.md`
3. Remediate all P0/P1 gaps before declaring production-ready
4. Escalate compliance interpretation questions to Dr. Elias Vance
5. Apply cross-cutting patterns for cross-layer problems
