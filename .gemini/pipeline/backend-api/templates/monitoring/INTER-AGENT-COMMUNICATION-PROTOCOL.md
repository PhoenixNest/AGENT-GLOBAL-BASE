# Inter-Agent Communication Protocol (IACP) — Backend API Pipeline

---

## 1. Purpose

This protocol defines **how agents communicate** within the backend API pipeline — message formats, routing rules, escalation paths, and error handling.

---

## 2. Communication Channels

| Channel                    | Direction                       | When                                      | Format                                 |
| :------------------------- | :------------------------------ | :---------------------------------------- | :------------------------------------- |
| **Stage Transition**       | Stage N owner → Stage N+1 owner | At every stage gate                       | Stage Transition Summary + JSON Schema |
| **Intra-Stage Delegation** | Stage owner → IC agent          | During stage execution                    | Task Dispatch Message                  |
| **Escalation**             | Any agent → supervisor          | On blockers, variance, or P0/P1 discovery | Escalation Message                     |
| **Cross-Review**           | Peer agent → peer agent         | Stage 6 Tier 1 reviews                    | Review Memo                            |
| **Progress Update**        | Any agent → CTO → CPO           | Per Progress Sync Protocol                | Progress Update                        |

---

## 3. Message Formats

Canonical message formats (Dispatch, Completion, Escalation, Review Memo) are **identical** across all pipelines. See Mobile Development IACP §3.

---

## 4. Routing Rules

### 4.1 Vertical Routing (Hierarchy)

```
CEO (User)
  └─ C-Suite (7 agents) ← Stage ownership, gate sign-offs
       └─ VP Platform + VP Web/Backend ← Domain routing, infra allocation
            └─ Backend Chapter Lead + DevOps Lead ← Team coordination
                 └─ IC Layer (Backend + DevOps + SRE engineers) ← Task execution
```

**Rules:**

- IC agents **never communicate directly** with C-Suite — always through their Lead or VP.
- Escalations follow the chain: IC → Chapter Lead → VP → C-Suite.
- **Exception:** P0 defects bypass the chain — any agent can escalate directly to CTO + CSO.

### 4.2 Horizontal Routing (Cross-Review)

| Sender               | Receiver             | Trigger                          |
| :------------------- | :------------------- | :------------------------------- |
| Backend Chapter Lead | DevOps Lead          | Stage 6 Tier 1 cross-review      |
| DevOps Lead          | Backend Chapter Lead | Stage 6 Tier 1 cross-review      |
| Security Architect   | All leads            | STRIDE threat model distribution |
| Red Team Reviewer    | CTO (panel)          | Red Team Report submission       |

### 4.3 Stage Transition Routing

| From Stage | Sending Agent | Receiving Agent   | Artifacts                             |
| :--------: | :------------ | :---------------- | :------------------------------------ |
|    1→2     | VP API + CSO  | CDO               | PRD + SRD + Schema 1→2                |
|    2→3     | CDO           | CTO + CIO         | API Spec + IDS + Schema 2→3           |
|    3→4     | CTO + CIO     | CTO               | UML + ADRs + TSD + Schema 3→4         |
|    4→5     | CTO           | CTO + VP Platform | Plan + Gantt + RTM + Schema 4→5       |
|    5→6     | CTO           | CTO (panel)       | Codebase + API Spec + Schema 5→6      |
|    6→7     | CTO (panel)   | CTO               | Defect Report + Red Team + Schema 6→7 |
|    7→8     | CTO           | CTO (panel)       | Test + Load Results + Schema 7→8      |
|    8→9     | CTO (panel)   | CTO-L             | Verified Codebase + Schema 8→9        |
|    9→10    | CTO-L         | CTO (panel)       | Localized Codebase + Schema 9→10      |
|     10     | CTO (panel)   | User              | Release Report + Schema 10            |

---

## 5–8. Error Handling, SLA, Integration, References

See Mobile Development IACP §5–§8 for canonical definitions.

Pipeline-specific references:

- [Stage Transition Schemas](STAGE-TRANSITION-SCHEMAS.md)
- [Red Team Review Protocol](../stage-6-code-review/RED-TEAM-REVIEW.md)
- `AGENTS.md` § Non-Negotiable Rules, Defect Severity, Quick Roster
