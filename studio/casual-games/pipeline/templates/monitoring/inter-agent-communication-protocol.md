# Inter-Agent Communication Protocol (IACP) — Casual Games Studio

> **ASE Layer:** 5 — Multi-Agent Engineering + Layer 2 — Context Engineering
> **Authority:** Studio Director Dr. Marcus Vogel
> **Reference:** `core-component-00/engineering/multi-agent-engineering/implementations/handoff_packet.py`
> **Compliance:** `adr-ase-001.md` (studio), `core-component-00/agent-systems-engineering/governance/compliance-standard.md` §Layer 5

This protocol defines **how crew agents communicate** within the studio pipeline — message formats, routing rules, escalation paths, and error handling. It replaces ad-hoc coordination with a structured, predictable communication model.

---

## 1. Communication Channels

| Channel                    | Direction                                  | When                                         | Format                                 |
| :------------------------- | :----------------------------------------- | :------------------------------------------- | :------------------------------------- |
| **Stage Transition**       | Stage owner → next stage owner             | At every kill gate / user approval gate      | Stage Transition Summary + JSON Schema |
| **Intra-Stage Delegation** | Division lead → crew member                | During stage execution                       | Task Dispatch Message                  |
| **Escalation**             | Any crew → division lead → Studio Director | On blockers, kill gate risk, or P0 discovery | Escalation Message                     |
| **Cross-Division Review**  | Division lead → peer division              | Stage 6 testing, Stage 7 soft launch prep    | Review Memo                            |
| **Kill Gate Report**       | Studio Director → User                     | At every kill gate                           | kill-gate-report.md                    |

---

## 2. Message Formats

### 2.1 Task Dispatch Message

Used when a division lead delegates work to a crew member.

```
DISPATCH [task-id]
FROM: [sender crew / role]
TO: [receiver crew / role]
STAGE: [N]
PRIORITY: [critical | high | normal | low]

OBJECTIVE: [1-2 sentence task description]

CONTEXT:
- [Relevant constraint 1]
- [Relevant constraint 2]
- Reference: [artifact path or GDD chapter]

OUTPUT EXPECTED:
- Format: [free text | JSON schema reference | template reference]
- Deadline: [date or milestone]

MVC FILTER APPLIED: [YES — only relevant context included per mvc-context-profile.md]
HANDOFF TIER: [Full | Scoped | Minimal]
```

### 2.2 Task Completion Message

```
COMPLETE [task-id]
FROM: [crew / role]
TO: [division lead]
STAGE: [N]

STATUS: [complete | complete_with_notes | blocked]

DELIVERABLE: [artifact path or inline content]

NOTES:
- [Any decisions made]
- [Any risks surfaced]
- [Any kill gate implications]
```

### 2.3 Escalation Message

```
ESCALATE [escalation-id]
FROM: [crew / role]
TO: [Studio Director]
STAGE: [N]
SEVERITY: [P0 | P1 | P2 | P3]
TYPE: [blocker | kill_gate_risk | resource | scope]

SITUATION: [2-3 sentence description]

IMPACT:
- Kill gate affected: [KG-N or None]
- Timeline impact: [+N days estimate]
- User notification required: [YES | NO]

RECOMMENDED ACTION: [proposed resolution]
```

### 2.4 Kill Gate Recommendation Message

Used by Studio Director to recommend a kill gate decision to the User.

```
KILL_GATE [gate-id]
FROM: Studio Director (Dr. Marcus Vogel)
TO: User (CEO)
GATE: [KG-1 through KG-5]
STAGE_TRANSITION: [N → N+1]

RECOMMENDATION: [proceed | iterate | kill]

EVIDENCE:
- Metric 1: [value vs threshold]
- Metric 2: [value vs threshold]
- Qualitative assessment: [1-2 sentences]

RISKS IF PROCEEDING: [list]
RISKS IF KILLING: [list]

AWAITING USER DECISION — pipeline is paused.
```

---

## 3. Routing Rules

| Scenario                  | Routing Path                                                         |
| :------------------------ | :------------------------------------------------------------------- |
| Task within a division    | Division lead → crew member directly                                 |
| Cross-division dependency | Division lead → Studio Director → target division lead               |
| Kill gate evaluation      | Studio Director → all relevant division leads → consolidated to User |
| P0/P1 defect discovered   | Any crew → Studio Director immediately (skip intermediate routing)   |
| CSO security gate         | Studio Director → CSO Dr. Sarah Chen (parent company)                |
| QBR outcome               | Live Ops Lead → Studio Director → User                               |

---

## 4. Handoff Tier Selection

> Reference: `core-component-00/engineering/context-engineering/patterns/multi-agent-handoff.md`

| Scenario                                 | Tier                    | Context Included                                                          |
| :--------------------------------------- | :---------------------- | :------------------------------------------------------------------------ |
| Sequential stage handoff (same pipeline) | **Scoped**              | 20–40% of prior context — key decisions, gate results, active constraints |
| New specialist joining mid-stage         | **Minimal**             | <10% — role brief, task objective, relevant kill gate criteria only       |
| Studio Director reviewing all divisions  | **Full**                | Up to 100% — complete stage history, all artifact summaries               |
| Handoff to parent company (CSO, CTO)     | **Minimal + sanitised** | <10% — studio-relevant facts only; no internal deliberation               |

```
Handoff tier decision tree:

Is the receiver in the same division?
  YES → Scoped
  NO →
    Is the receiver a new specialist?
      YES → Minimal
      NO →
        Is the receiver Studio Director or above?
          YES → Full
          NO → Scoped
```

---

## 5. Parallel Agent Workflow (Git Worktree)

> Reference: `core-component-00/engineering/multi-agent-engineering/implementations/git_worktree_manager.py`, `core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`

When multiple crew agents work concurrently on the same project (typically Stage 5 — Full Production), the **git worktree isolation pattern** applies:

| Phase         | Action                                                                    | Responsible     |
| :------------ | :------------------------------------------------------------------------ | :-------------- |
| **Provision** | Studio Director creates one worktree per parallel crew agent              | Studio Director |
| **Execute**   | Each crew agent works in its isolated worktree; commits on its own branch | Individual crew |
| **Integrate** | Lead Engineer merges branches; resolves conflicts                         | Lead Engineer   |
| **Review**    | Studio Director inspects combined diff before merge to main               | Studio Director |
| **Clean up**  | Remove worktrees; prune stale entries                                     | Lead Engineer   |

Branch naming: `agent/<division>/<task>` (e.g. `agent/art/character-rig-v2`)

Commit format: `agent/<name>: <verb-phrase>` with hyphen-bulleted body (single-line commits without body are a P2 audit-trail defect).

> **No crew agent may merge its own branch to main.** The Lead Engineer acts as Integration Agent.

---

## 6. Error Handling

| Error                                                     | Action                                                          |
| :-------------------------------------------------------- | :-------------------------------------------------------------- |
| Message not acknowledged within 24h                       | Escalate to division lead                                       |
| Dependency blocked (another crew member)                  | Escalation Message → Studio Director within 4h                  |
| Kill gate criteria cannot be met                          | Immediate escalation to Studio Director; do not attempt to hide |
| Silent failure (no status update for >48h on active task) | P0 defect — Studio Director notifies User                       |
