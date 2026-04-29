# Inter-Agent Communication Protocol (IACP)

> **Addresses Gap:** #5 (Schema-Driven Communication)

---

## 1. Purpose

This protocol defines **how agents communicate** within the multi-agent pipeline — message formats, routing rules, escalation paths, and error handling. It replaces ad-hoc information passing with a structured, predictable communication model.

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

### 3.1 Task Dispatch Message

Used when a stage owner delegates work to an IC agent.

```
DISPATCH [task-id]
FROM: [sender agent / role]
TO: [receiver agent / role]
STAGE: [N]
PRIORITY: [P0 | P1 | P2 | P3 | normal]

OBJECTIVE: [1-2 sentence task description]

CONTEXT:
- [Relevant constraint 1]
- [Relevant constraint 2]
- Reference: [artifact path or schema reference]

OUTPUT EXPECTED:
- Format: [free text | JSON schema reference | template reference]
- Deadline: [date or milestone]

MVC FILTER APPLIED: [YES — only relevant context included]
```

### 3.2 Task Completion Message

Used when an IC agent reports task completion back to the stage owner.

```
COMPLETE [task-id]
FROM: [agent / role]
TO: [stage owner]
STAGE: [N]
STATUS: [done | blocked | partial]

RESULT SUMMARY: [2-3 sentences]

ARTIFACTS PRODUCED:
- [artifact name] → [path]

DEFECTS FOUND: [N] (P0: N, P1: N, P2: N, P3: N)

BLOCKERS: [none | description]
VARIANCE: [within estimate | +N% over estimate]
```

### 3.3 Escalation Message

Used when any agent encounters a blocker, P0/P1 defect, or >20% variance.

```
ESCALATE [escalation-id]
FROM: [agent / role]
TO: [supervisor agent]
STAGE: [N]
SEVERITY: [P0 | P1 | variance | blocker]

ISSUE: [1-2 sentence description]
IMPACT: [What breaks if unresolved]
RECOMMENDED ACTION: [Agent's suggestion]
DEADLINE: [When this becomes critical]

EVIDENCE: [file path, line number, test result, etc.]
```

### 3.4 Review Memo (Stage 6 Tier 1)

Already defined in the existing DEFECT-REPORT.md template. No change required.

---

## 4. Routing Rules

### 4.1 Vertical Routing (Hierarchy)

```
CEO (User)
  └─ C-Suite (7 agents) ← Stage ownership, gate sign-offs
       └─ VP Layer (6 agents) ← Domain routing, resource allocation
            └─ Lead Layer (8 agents) ← Team coordination, cross-review
                 └─ IC Layer (58 agents) ← Task execution
```

**Rules:**

- IC agents **never communicate directly** with C-Suite — always through their Lead or VP.
- Escalations follow the chain: IC → Lead → VP → C-Suite.
- **Exception:** P0 defects bypass the chain — any agent can escalate directly to CTO + CSO.

### 4.2 Horizontal Routing (Cross-Review)

| Sender              | Receiver            | Trigger                           |
| :------------------ | :------------------ | :-------------------------------- |
| Android Lead        | iOS Lead            | Stage 6 Tier 1 cross-review       |
| iOS Lead            | Android Lead        | Stage 6 Tier 1 cross-review       |
| Cross-Platform Lead | Both platform leads | KMP/Flutter contract verification |
| Security Architect  | All platform leads  | STRIDE threat model distribution  |
| Red Team Reviewer   | CTO (panel)         | Red Team Report submission        |

### 4.3 Stage Transition Routing

| From Stage | Sending Agent | Receiving Agent | Artifacts                             |
| :--------: | :------------ | :-------------- | :------------------------------------ |
|    1→2     | CPO + CSO     | CDO             | PRD + SRD + Schema 1→2                |
|    2→3     | CDO           | CTO + CIO       | Prototype + IDS + Schema 2→3          |
|    3→4     | CTO + CIO     | CTO             | UML + ADRs + TSD + Schema 3→4         |
|    4→5     | CTO           | CTO + VP Mobile | Plan + Gantt + RTM + Schema 4→5       |
|    5→6     | CTO           | CTO (panel)     | Codebase + Schema 5→6                 |
|    6→7     | CTO (panel)   | CTO             | Defect Report + Red Team + Schema 6→7 |
|    7→8     | CTO           | CTO (panel)     | Test Results + Schema 7→8             |
|    8→9     | CTO (panel)   | CTO-L           | Verified Codebase + Schema 8→9        |
|    9→10    | CTO-L         | CTO (panel)     | Localized Codebase + Schema 9→10      |
|     10     | CTO (panel)   | User            | Release Report + Schema 10            |

---

## 5. Error Handling

| Error Type                   | Detection                                            | Response                                          |
| :--------------------------- | :--------------------------------------------------- | :------------------------------------------------ |
| **Missing schema field**     | Receiving agent validates JSON                       | Reject handoff; request correction from sender    |
| **Sign-off missing**         | Schema shows `false` for required sign-off           | Block stage advancement; escalate to stage owner  |
| **Stale artifact reference** | Path references a superseded ADR                     | Reject; sender must reference current version     |
| **Orphaned constraint**      | `constraints_forward` references deleted requirement | Flag as P2; stage owner resolves before advancing |
| **Agent unavailable**        | Delegation fails (no response within SLA)            | Escalate to VP; VP reassigns to alternate agent   |

---

## 6. SLA (Response Time Guidelines)

| Message Type     | Expected Response           | Escalation Trigger             |
| :--------------- | :-------------------------- | :----------------------------- |
| Task Dispatch    | Begin within same session   | If not started by next session |
| Escalation (P0)  | Immediate                   | Auto-escalate to CTO + CSO     |
| Escalation (P1)  | Same session                | If no response within session  |
| Stage Transition | Validation within 1 session | If schema rejected twice       |
| Progress Update  | Per milestone               | >20% variance auto-fires       |

---

## 7. Integration with Existing Infrastructure

| Existing Component            | IACP Integration                                                 |
| :---------------------------- | :--------------------------------------------------------------- |
| `AGENTS.md` § Quick Roster    | Defines the routing hierarchy (Section 4.1)                      |
| `pipeline.md` per stage       | Defines which agents participate (Section 4.3)                   |
| `DEFECT-REPORT.md`            | Tier 1 Review Memo format (Section 3.4)                          |
| `RED-TEAM-REVIEW.md`          | Red Team report follows Escalation format for P0/P1              |
| `STAGE-TRANSITION-SCHEMAS.md` | JSON schemas referenced in all transition messages               |
| `STAGE-TRANSITION-SUMMARY.md` | Human-readable companion to JSON schema output                   |
| Progress Sync Protocol        | IACP Section 5 variance detection aligns with existing >20% rule |

---

## 8. References

- [Context Engineering Guideline](../../skills/shared/guidelines/context-engineering.md)
- [Stage Transition Schemas](STAGE-TRANSITION-SCHEMAS.md)
- [Stage Transition Summary Template](STAGE-TRANSITION-SUMMARY.md)
- [Red Team Review Protocol](../stage-6-code-review/RED-TEAM-REVIEW.md)
- `AGENTS.md` § Non-Negotiable Rules, Defect Severity, Quick Roster
