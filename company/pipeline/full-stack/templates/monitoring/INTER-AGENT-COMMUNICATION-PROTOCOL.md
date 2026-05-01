# Inter-Agent Communication Protocol (IACP) — Full-Stack Pipeline

---

## 1. Purpose

This protocol defines **how agents communicate** within the full-stack pipeline. Due to the cross-platform nature, this is the most complex IACP variant — requiring **cross-track synchronization** between Mobile, Web, and Backend sub-teams.

---

## 2. Communication Channels

| Channel                    | Direction                       | When                                      | Format                                 |
| :------------------------- | :------------------------------ | :---------------------------------------- | :------------------------------------- |
| **Stage Transition**       | Stage N owner → Stage N+1 owner | At every stage gate                       | Stage Transition Summary + JSON Schema |
| **Intra-Stage Delegation** | Stage owner → IC agent          | During stage execution                    | Task Dispatch Message                  |
| **Cross-Track Sync**       | Track lead → Track lead         | At integration milestones                 | Integration Checkpoint Message         |
| **Escalation**             | Any agent → supervisor          | On blockers, variance, or P0/P1 discovery | Escalation Message                     |
| **Cross-Review**           | Peer agent → peer agent         | Stage 6 Tier 1 reviews                    | Review Memo                            |
| **Progress Update**        | Any agent → CTO → CPO           | Per Progress Sync Protocol                | Progress Update                        |

---

## 3. Message Formats

Standard message formats (Dispatch, Completion, Escalation, Review Memo) are **identical** across all pipelines. See Mobile Development IACP §3.

### 3.5 Integration Checkpoint Message (Full-Stack Exclusive)

```
INTEGRATION-CHECKPOINT [checkpoint-id]
  milestone: IM-NNN
  tracks: [fs_mobile, fs_web, fs_api]
  type: api_contract | e2e_flow | performance
  status_per_track:
    fs_mobile: ready | blocked | not_applicable
    fs_web: ready | blocked | not_applicable
    fs_api: ready | blocked | not_applicable
  blockers: [list of blocking issues]
  next_sync: YYYY-MM-DD
```

---

## 4. Routing Rules

### 4.1 Vertical Routing (Hierarchy)

```
CEO (User)
  └─ C-Suite (7 agents) ← Stage ownership, gate sign-offs
       ├─ VP Mobile ← Mobile track coordination
       │    ├─ iOS Lead ← iOS sub-track
       │    ├─ Android Lead ← Android sub-track
       │    └─ Cross-Platform Lead ← KMP/Flutter sub-track
       ├─ VP Web/Backend ← Web + API track coordination
       │    ├─ Frontend Chapter Lead ← Web sub-track
       │    └─ Backend Chapter Lead ← API sub-track
       └─ VP Platform ← Infrastructure + DevOps
            └─ DevOps Lead ← CI/CD, deployment
```

**Rules:**

- IC agents **never communicate directly** with C-Suite — always through their Lead or VP.
- **Cross-track escalations** go through the CTO (the only agent with visibility across all tracks).
- **Exception:** P0 defects bypass the chain — any agent can escalate directly to CTO + CSO.

### 4.2 Horizontal Routing (Cross-Track)

| Sender                | Receiver             | Trigger                             |
| :-------------------- | :------------------- | :---------------------------------- |
| iOS Lead              | Backend Chapter Lead | API contract integration checkpoint |
| Android Lead          | Backend Chapter Lead | API contract integration checkpoint |
| Frontend Chapter Lead | Backend Chapter Lead | API contract integration checkpoint |
| Cross-Platform Lead   | All other leads      | Shared module synchronization       |
| Security Architect    | All leads            | STRIDE threat model distribution    |
| Red Team Reviewer     | CTO (panel)          | Red Team Report submission          |

### 4.3 Stage Transition Routing

| From Stage | Sending Agent | Receiving Agent                  | Artifacts                                    |
| :--------: | :------------ | :------------------------------- | :------------------------------------------- |
|    1→2     | CPO + CSO     | CDO                              | PRD + SRD + Schema 1→2                       |
|    2→3     | CDO           | CTO + CIO                        | Prototype + IDS (all platforms) + Schema 2→3 |
|    3→4     | CTO + CIO     | CTO                              | UML + ADRs + TSD + Schema 3→4                |
|    4→5     | CTO           | CTO + VP Mobile + VP Web/Backend | Plan + Gantt + RTM + Schema 4→5              |
|    5→6     | CTO           | CTO (panel)                      | All codebases + Integration results + Schema |
|    6→7     | CTO (panel)   | CTO                              | Defect Reports (×3) + Red Team + Schema 6→7  |
|    7→8     | CTO           | CTO (panel)                      | Test Results (all tracks) + Schema 7→8       |
|    8→9     | CTO (panel)   | CTO-L                            | Verified Codebases (×3) + Schema 8→9         |
|    9→10    | CTO-L         | CTO (panel)                      | Localized Codebases + Schema 9→10            |
|     10     | CTO (panel)   | User                             | Release Report + Schema 10                   |

---

## 5. Cross-Track Synchronization Protocol

The full-stack pipeline introduces a unique **cross-track sync** mechanism to prevent integration failures.

### 5.1 Sync Points

| Sync Point           | Tracks             | Purpose                               | Owner                |
| :------------------- | :----------------- | :------------------------------------ | :------------------- |
| API Contract Lock    | Mobile + Web + API | Freeze API schema before parallel dev | Backend Chapter Lead |
| E2E Integration Test | All                | Verify cross-platform data flow       | CTO                  |
| Performance Baseline | All                | Validate response times across stack  | VP Platform          |

### 5.2 Conflict Resolution

When two tracks produce conflicting requirements:

1. The **CTO** convenes an **Integration Review** within 24 hours.
2. The conflict is documented as an **Integration Decision Record**.
3. The losing track adapts — the API contract is the **single source of truth**.

---

## 6–8. Error Handling, SLA, Integration

See Mobile Development IACP §5–§8 for canonical definitions.

§8 **Parallel Agent Workflow (Git Worktree)** is especially critical for full-stack: Stage 5 routinely runs mobile, web, and backend agents simultaneously. Each track **must** operate in its own git worktree with its own branch. The Integration Agent (Software Architect or CTO delegate) owns all merges. Reference: `core-component-00/multi-agent-engineering/implementations/git_worktree_manager.py` and `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`.

Pipeline-specific references:

- [Stage Transition Schemas](stage-transition-schemas.md)
- [Red Team Review Protocol](company/pipeline/full-stack/templates/stage-6-code-review/RED-TEAM-REVIEW.md)
- [Git Worktree Orchestration](core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md)
