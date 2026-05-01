# Risk Register — Template

> **Stage:** 4 — Production Planning (maintained through all stages)
> **Producer:** Executive Producer (James Okonkwo)
> **Kill Gate:** KG-4 — Production Planning (initial version)
> **Update frequency:** Review at every milestone and stage transition

---

## Risk Matrix

| Risk ID | Risk Description   | Category                                          | Likelihood | Impact  |  Score  | Mitigation          | Owner   | Status |
| :------ | :----------------- | :------------------------------------------------ | :--------: | :-----: | :-----: | :------------------ | :------ | :----- |
| R-001   | [Risk description] | [Technical / Schedule / Market / People / Budget] |  [H/M/L]   | [H/M/L] | [H/M/L] | [Mitigation action] | [Owner] | ☐ Open |
| R-002   | [Risk description] |                                                   |  [H/M/L]   | [H/M/L] | [H/M/L] |                     |         | ☐ Open |

---

## Risk Scoring Guide

|   Likelihood    |   Impact   |  Score   |
| :-------------: | :--------: | :------: |
|   High (>70%)   |    High    | Critical |
|      High       | Low/Medium |   High   |
| Medium (30–70%) |    High    |   High   |
|     Medium      |   Medium   |  Medium  |
|   Low (<30%)    |    Any     |   Low    |

---

## Standard Risk Library (Pre-populated for game projects)

| Risk ID   | Risk                                                          | Category  | Default Likelihood | Default Mitigation                                                            |
| :-------- | :------------------------------------------------------------ | :-------- | :----------------: | :---------------------------------------------------------------------------- |
| R-STD-001 | Unity version upgrade mid-production breaks existing features | Technical |        Low         | Pin to Unity 6.3 LTS; test all upgrades in isolated branch                    |
| R-STD-002 | Third-party SDK API breaking change                           | Technical |       Medium       | Monitor SDK changelogs; pin SDK versions in TSD                               |
| R-STD-003 | Kill gate metric misses (D1/D7 below threshold)               | Market    |       Medium       | Early playtesting in Stage 5; iterate on feel before content lock             |
| R-STD-004 | Key crew member departure mid-production                      | People    |        Low         | Cross-training; ensure Tier 2/3 knowledge documented per KTP                  |
| R-STD-005 | App store policy change affecting monetisation                | Market    |        Low         | Monitor Apple/Google policy updates monthly; CSO flagging                     |
| R-STD-006 | Budget overrun (>15% of contingency)                          | Budget    |       Medium       | Weekly budget tracking; Executive Producer escalation at 10%                  |
| R-STD-007 | Performance regression on low-end devices                     | Technical |       Medium       | Device farm testing at M1 Alpha; performance budget enforced by Lead Engineer |
| R-STD-008 | GDPR/CCPA compliance gap discovered post-build                | Legal     |        Low         | SRD compliance checklist at every stage gate; CSO review                      |

---

## Resolved Risks

| Risk ID | Risk | Resolution Date | Outcome |
| :------ | :--- | :-------------: | :------ |
|         |      |                 |         |

---

## Escalation Protocol

| Score        | Escalation Action                                                   |
| :----------- | :------------------------------------------------------------------ |
| **Critical** | Immediate notification to Studio Director; User notified within 24h |
| **High**     | Studio Director review within 48h; mitigation plan produced         |
| **Medium**   | Executive Producer manages; reviewed at next milestone              |
| **Low**      | Logged; reviewed at next stage gate                                 |

---

**Maintained by:** [Executive Producer]
**Last reviewed:** YYYY-MM-DD at [Stage N / Milestone M]
