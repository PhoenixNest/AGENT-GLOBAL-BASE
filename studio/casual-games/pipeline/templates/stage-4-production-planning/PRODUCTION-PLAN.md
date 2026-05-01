# Production Plan — Template

> **Stage:** 4 — Production Planning
> **Producer:** Executive Producer (James Okonkwo) + Studio Director (Dr. Marcus Vogel)
> **Kill Gate:** KG-4 — Production Planning
> **User Approval:** ✅ Required before advancing to Stage 5 (Full Production)

---

## Document Control

| Field          | Value                |
| :------------- | :------------------- |
| **Game Title** | [Working title]      |
| **Version**    | v1.0                 |
| **Date**       | YYYY-MM-DD           |
| **Author**     | [Executive Producer] |

---

## 1. Production Overview

| Field                       | Value        |
| :-------------------------- | :----------- |
| **Total planned duration**  | [N months]   |
| **Stage 5 start date**      | YYYY-MM-DD   |
| **Target Stage 5 end date** | YYYY-MM-DD   |
| **Soft launch target**      | YYYY-MM-DD   |
| **Global launch target**    | YYYY-MM-DD   |
| **Budget cap (Stage 5)**    | $[X,XXX,XXX] |

---

## 2. Milestone Table

|  #  | Milestone         | Target Date | Owner             | Success Criteria                                 |
| :-: | :---------------- | :---------- | :---------------- | :----------------------------------------------- |
| M1  | Alpha build       | YYYY-MM-DD  | Lead Engineer     | All core features integrated; no P0 bugs         |
| M2  | Content complete  | YYYY-MM-DD  | Creative Director | All levels, art, audio at planned content count  |
| M3  | Beta build        | YYYY-MM-DD  | Lead Engineer     | Feature-complete; performance targets met        |
| M4  | Gold candidate    | YYYY-MM-DD  | Studio Director   | Zero P0/P1 bugs; all KG-5 criteria estimated-met |
| M5  | Soft launch ready | YYYY-MM-DD  | Studio Director   | KG-5 submission package complete                 |

---

## 3. Team Allocation by Division

| Division        | Head Count | Key Responsibilities                             | Stages |
| :-------------- | :--------: | :----------------------------------------------- | :----- |
| Leadership      |     3      | Pipeline governance, sign-offs                   | All    |
| Production      |     2      | Schedule management, cross-division coordination | 5–9    |
| Creative Design |    [N]     | GDD updates, level design, economy tuning        | 5–6    |
| Art             |    [N]     | Final asset production, VFX, UI polish           | 5–6    |
| Audio           |    [N]     | Music composition, SFX production                | 5–6    |
| Engineering     |    [N]     | Feature implementation, CI/CD, testing           | 5–7    |
| Live Ops        |    [N]     | Analytics wiring, soft launch monitoring         | 7–10   |

---

## 4. Dependency Map

| Dependency       | From           | To          | Risk if Late                     |
| :--------------- | :------------- | :---------- | :------------------------------- |
| Art assets       | Art division   | Engineering | Blocks feature integration       |
| Audio assets     | Audio division | Engineering | Blocks final build               |
| Backend services | Engineering    | Live Ops    | Blocks analytics and soft launch |
| [Dependency]     | [From]         | [To]        | [Risk]                           |

---

## 5. Critical Path

```
[Art assets ready] ──────────────────────────┐
                                              ├──→ [Integration] → [Beta] → [Soft Launch]
[Core engineering complete] ─────────────────┘
                    ↑
[Audio production complete] ─────────────────┘
```

**Critical path items** (any delay cascades to launch):

1. [Item 1]
2. [Item 2]
3. [Item 3]

---

## 6. Budget Allocation

| Category                |    Allocation    | % of Total |
| :---------------------- | :--------------: | :--------: |
| Personnel (Stage 5)     |     $[X,XXX]     |    [X]%    |
| Technology / licences   |     $[X,XXX]     |    [X]%    |
| QA and testing          |     $[X,XXX]     |    [X]%    |
| Marketing (soft launch) |     $[X,XXX]     |    [X]%    |
| Contingency (15%)       |     $[X,XXX]     |    15%     |
| **Total**               | **$[X,XXX,XXX]** |  **100%**  |

---

## 7. Kill Gate 4 Decision

| Field                                        | Value                              |
| :------------------------------------------- | :--------------------------------- |
| **Milestone table complete and achievable?** | ☐ Yes / ☐ No                       |
| **Team fully allocated?**                    | ☐ Yes / ☐ No                       |
| **Budget approved?**                         | ☐ Yes / ☐ No                       |
| **Risk register complete?**                  | ☐ Yes / ☐ No                       |
| **Gantt approved?**                          | ☐ Yes / ☐ No                       |
| **Studio Director recommendation**           | ☐ Proceed / ☐ Revise plan / ☐ Kill |

---

**Produced by:** [Executive Producer] on YYYY-MM-DD
**Reviewed by:** [Studio Director] on YYYY-MM-DD
**Awaiting User (CEO) budget approval and go/no-go.**
