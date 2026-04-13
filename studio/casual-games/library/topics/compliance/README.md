# Compliance — Casual Games Studio

Compliance documentation addressing regulatory, legal, and platform policy requirements.

**Owned by:** CIO (Dr. Priya Mehta) + CSO (Dr. Sarah Chen)

---

## Audit Conditions Addressed

| Condition | Audit Reference              | Risk ID | Severity | Document                                                 | Status   |
| --------- | ---------------------------- | ------- | -------- | -------------------------------------------------------- | -------- |
| **C1**    | CIO Technology Audit, Item 5 | R4      | 🟠 P1    | [UNITY-LICENSING-REVIEW.md](./UNITY-LICENSING-REVIEW.md) | Proposed |
| **C2**    | CIO Technology Audit, Item 7 | R3      | 🔴 P0    | [COPPA-ASSESSMENT-PLAN.md](./COPPA-ASSESSMENT-PLAN.md)   | Proposed |

---

## Documents

| Document                      | Description                                                                                                       | Owner     | Last Updated |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------- | --------- | ------------ |
| **UNITY-LICENSING-REVIEW.md** | Unity 6.3 LTS licensing risk assessment, legal review plan, exit strategy (Godot/Unreal), and ADR-001             | CIO       | 2026-04-12   |
| **COPPA-ASSESSMENT-PLAN.md**  | COPPA applicability analysis, SDK audit, privacy policy, data architecture alignment, and implementation timeline | CIO + CSO | 2026-04-12   |

---

## Compliance Status Dashboard

### Condition C1 — Unity Licensing Legal Review

| Milestone                       | Target   | Status      | Notes                                |
| ------------------------------- | -------- | ----------- | ------------------------------------ |
| Engage external legal counsel   | Week 1   | Not started | Pending CIO action                   |
| Legal review of Unity EULA      | Week 1–2 | Not started | Dependent on counsel engagement      |
| Legal Memorandum delivered      | Week 2   | Not started | C1 gate deliverable                  |
| Enterprise contract negotiation | Week 2–4 | Not started | Dependent on legal findings          |
| Signed contract executed        | Week 4   | Not started | C1 condition satisfied               |
| ADR-001 Accepted                | Week 2   | Proposed    | Pending CTO + Studio Director review |

### Condition C2 — COPPA Compliance Assessment

| Milestone                         | Target | Status      | Notes                             |
| --------------------------------- | ------ | ----------- | --------------------------------- |
| FTC multi-factor test completed   | Week 3 | Not started | Preliminary determination drafted |
| SDK audit completed               | Week 4 | Not started | SDK inventory compiled            |
| Privacy policy published          | Week 4 | Not started | Draft template provided           |
| Data architecture COPPA-aligned   | Week 5 | Not started | Design specifications ready       |
| COPPA Assessment Report delivered | Week 6 | Not started | C2 gate deliverable               |

---

## Related References

| Document                                           | Location                                                               |
| -------------------------------------------------- | ---------------------------------------------------------------------- |
| CIO Technology Audit                               | `../../../team/recruitment-plan/audit-reports/cio-technology-audit.md` |
| COPPA & Platform Compliance Reference              | `library/reference/coppa-platform-compliance.md`                       |
| Game Security & Anti-Cheat (SDK Vetting Checklist) | `library/reference/game-security-anti-cheat.md`                        |
| Strategic Brief (Risk Register)                    | `library/overview/casual-games-studio.md`                              |

---

## Governance

- **Owner:** Dr. Priya Mehta, CIO
- **Co-Owner:** Dr. Sarah Chen, CSO
- **Review Cycle:** Weekly until both conditions (C1, C2) are satisfied, then monthly
- **Escalation:** Unresolved P0 conditions escalate to C-Suite panel within 48 hours

---

_This directory was created on April 12, 2026, in response to the CIO Technology Audit conditions C1 and C2._
