# Inter-Agent Communication Protocol (IACP) — Web Pipeline

---

## 1. Purpose

This protocol defines **how agents communicate** within the web development pipeline — message formats, routing rules, escalation paths, and error handling. It replaces ad-hoc information passing with a structured, predictable communication model.

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

### 3.1–3.4

Message formats are **identical** across all pipelines. See the canonical definitions in the Mobile Development IACP:

- **3.1 Task Dispatch Message** — `DISPATCH [task-id]`
- **3.2 Task Completion Message** — `COMPLETE [task-id]`
- **3.3 Escalation Message** — `ESCALATE [escalation-id]`
- **3.4 Review Memo** — Defined in DEFECT-REPORT.md

---

## 4. Routing Rules

### 4.1 Vertical Routing (Hierarchy)

```
CEO (User)
  └─ C-Suite (7 agents) ← Stage ownership, gate sign-offs
       └─ VP Layer (VP Web + Backend) ← Domain routing, resource allocation
            └─ Chapter Leads (Frontend + Backend) ← Team coordination, cross-review
                 └─ IC Layer (Frontend + Backend + Full-Stack devs) ← Task execution
```

**Rules:**

- IC agents **never communicate directly** with C-Suite — always through their Lead or VP.
- Escalations follow the chain: IC → Chapter Lead → VP → C-Suite.
- **Exception:** P0 defects bypass the chain — any agent can escalate directly to CTO + CSO.

### 4.2 Horizontal Routing (Cross-Review)

| Sender                | Receiver              | Trigger                          |
| :-------------------- | :-------------------- | :------------------------------- |
| Frontend Chapter Lead | Backend Chapter Lead  | Stage 6 Tier 1 cross-review      |
| Backend Chapter Lead  | Frontend Chapter Lead | Stage 6 Tier 1 cross-review      |
| Security Architect    | All chapter leads     | STRIDE threat model distribution |
| Red Team Reviewer     | CTO (panel)           | Red Team Report submission       |

### 4.3 Stage Transition Routing

| From Stage | Sending Agent | Receiving Agent      | Artifacts                             |
| :--------: | :------------ | :------------------- | :------------------------------------ |
|    1→2     | VP Web + CSO  | CDO                  | PRD + SRD + Schema 1→2                |
|    2→3     | CDO           | CTO + CIO            | Prototype + IDS + Schema 2→3          |
|    3→4     | CTO + CIO     | CTO                  | UML + ADRs + TSD + Schema 3→4         |
|    4→5     | CTO           | CTO + VP Web/Backend | Plan + Gantt + RTM + Schema 4→5       |
|    5→6     | CTO           | CTO (panel)          | Codebase + Schema 5→6                 |
|    6→7     | CTO (panel)   | CTO                  | Defect Report + Red Team + Schema 6→7 |
|    7→8     | CTO           | CTO (panel)          | Test Results + Schema 7→8             |
|    8→9     | CTO (panel)   | CTO-L                | Verified Codebase + Schema 8→9        |
|    9→10    | CTO-L         | CTO (panel)          | Localized Codebase + Schema 9→10      |
|     10     | CTO (panel)   | User                 | Release Report + Schema 10            |

---

## 5–8. Error Handling, SLA, Integration, References

These sections are **identical** across all pipelines. See the canonical definitions in:

- `mobile-development/templates/monitoring/INTER-AGENT-COMMUNICATION-PROTOCOL.md` §5–§8

Pipeline-specific references:

- [Stage Transition Schemas](STAGE-TRANSITION-SCHEMAS.md)
- [Stage Transition Summary Template](STAGE-TRANSITION-SUMMARY.md)
- [Red Team Review Protocol](../stage-6-code-review/RED-TEAM-REVIEW.md)
- `AGENTS.md` § Non-Negotiable Rules, Defect Severity, Quick Roster
