# Pattern: Progress Sync Protocol

| Field        | Value                               |
| ------------ | ----------------------------------- |
| **Category** | Pipeline Governance · Observability |
| **Layer**    | Cross-cutting (Layer 3 + Layer 5)   |
| **Status**   | Ratified — ADR-ASE-001              |

---

## Problem

Long-running multi-agent pipelines fail silently. An agent encounters a blocker —
a dependency is unavailable, an estimate is wildly wrong, a tool call is timing out
repeatedly — and either continues making slow progress without alerting anyone, or
stalls entirely while the supervisor and human operator assume work is proceeding normally.

Failures discovered late are expensive. A Stage 7 failure that could have been caught
at Stage 4 represents three stages of wasted agent compute, potential rework of
downstream artifacts, and — in production — an outage that extended beyond its minimum
possible duration.

The root cause is **absent observability**: no mechanism exists to detect when a task
has exceeded its expected trajectory and alert the appropriate authority.

---

## Solution

Implement a **Progress Sync Protocol (PSP)** at the harness level: a systematic
mechanism that detects variance from expected progress and triggers escalation when
variance exceeds defined thresholds.

The PSP has three components:

1. **Baseline estimation** — Expected duration and milestones for each task are defined
   before execution begins.
2. **Variance detection** — The harness monitors elapsed time and completion percentage
   against the baseline during execution.
3. **Escalation triggers** — When variance exceeds a threshold, a defined escalation
   action is taken automatically.

---

## Protocol Specification

### Component 1: Baseline Estimation

Before a task is dispatched to an agent, the orchestrator records:

| Field                | Description                                                              |
| -------------------- | ------------------------------------------------------------------------ |
| `task_id`            | Unique identifier for this task instance                                 |
| `agent`              | The agent responsible for the task                                       |
| `stage`              | The pipeline stage this task belongs to                                  |
| `estimated_start`    | ISO 8601 timestamp — when the task is expected to begin                  |
| `estimated_end`      | ISO 8601 timestamp — when the task is expected to complete               |
| `milestones`         | List of intermediate checkpoints with expected timestamps                |
| `variance_threshold` | The percentage over estimate at which escalation triggers (default: 20%) |

### Component 2: Variance Detection

The harness monitors each active task on a polling interval. At each poll:

```python
def detect_variance(task: Task, now: datetime) -> VarianceEvent | None:
    elapsed = (now - task.actual_start).total_seconds()
    expected = (task.estimated_end - task.estimated_start).total_seconds()

    if elapsed == 0:
        return None

    variance_pct = ((elapsed - expected) / expected) * 100 if elapsed > expected else 0

    if variance_pct >= task.variance_threshold:
        return VarianceEvent(
            task_id=task.task_id,
            agent=task.agent,
            stage=task.stage,
            elapsed_seconds=elapsed,
            expected_seconds=expected,
            variance_pct=variance_pct,
            last_milestone_reached=task.last_milestone_reached,
            timestamp=now,
        )
    return None
```

### Component 3: Escalation Triggers

Variance events trigger escalation based on severity:

| Variance                              | Escalation Action                                                                      |
| ------------------------------------- | -------------------------------------------------------------------------------------- |
| 20–50%                                | Log warning. Notify supervisor agent. Agent continues.                                 |
| 50–100%                               | Log alert. Notify supervisor + human operator. Request status update from agent.       |
| > 100%                                | Log critical. Notify supervisor + human operator. Consider task reassignment or abort. |
| No update for > 2× estimated duration | Treat as stalled. Log critical. Human intervention required.                           |

---

## Progress Tracking Artefacts

For Company pipeline Stage 4 (_UML → Implementation Plan + Gantt_) onward, three
artefacts track progress for each active project:

| Artefact          | Location                       | Updated By             | Frequency           |
| ----------------- | ------------------------------ | ---------------------- | ------------------- |
| `progress.md`     | `project/<id>/progress.md`     | Assigned agent         | Per task completion |
| `session-log.md`  | `project/<id>/session-log.md`  | All active agents      | Per session         |
| `checkpoint.json` | `project/<id>/checkpoint.json` | Harness / orchestrator | Per milestone       |

The `checkpoint.json` format:

```json
{
  "task_id": "TASK-2026-0430-001",
  "agent": "backend-dev",
  "stage": 5,
  "stage_name": "Software Development",
  "estimated_completion": "2026-05-02T17:00:00Z",
  "actual_start": "2026-04-30T09:00:00Z",
  "last_milestone": "database-schema-approved",
  "last_milestone_at": "2026-04-30T14:30:00Z",
  "variance_pct": 0.0,
  "status": "on-track"
}
```

---

## Escalation Authority

| Escalation Level | Notified Party                    | Required Action                                 |
| ---------------- | --------------------------------- | ----------------------------------------------- |
| Warning (20–50%) | Supervisor agent                  | Log. Monitor. No intervention unless requested. |
| Alert (50–100%)  | Supervisor + CPO                  | CPO acknowledges. Decides whether to intervene. |
| Critical (>100%) | Supervisor + CPO + human operator | Human reviews. Makes continuation decision.     |
| Stalled          | Human operator (mandatory)        | Human must take action. Automated systems hold. |

In the company pipeline, the CPO (Chief Product Officer) is the escalation authority
for schedule variance. The CTO is the escalation authority for technical blockers.
In the studio pipeline, escalation goes to the relevant Division Director.

---

## How to Apply

1. **Define baselines before dispatch** — Do not start an agent task without recording
   the expected start, end, and milestones. A task dispatched without a baseline cannot
   be monitored.

2. **Set realistic variance thresholds** — The default 20% threshold is appropriate for
   well-understood tasks. Experimental or research tasks may warrant 50%. Calibrate
   based on historical execution data.

3. **Implement the progress artefacts** for all Stage 4+ company pipeline projects and
   Stage 5+ studio pipeline projects. Agents update `progress.md` at each task
   completion.

4. **Review escalation logs weekly** — Patterns of recurring variance at specific stages
   or with specific agents indicate systemic estimation problems, not individual
   execution failures. Address the estimation model, not just the individual case.

---

## Consequences

**Benefits:**

- Failures are detected at the earliest possible point — not when the pipeline stalls
  visibly
- Human operators have objective data (variance percentage, last milestone reached)
  rather than subjective agent status reports
- Recurring variance patterns become visible, enabling systemic improvement

**Trade-offs:**

- Requires upfront estimation work — baselines must be set before tasks begin
- False positives are possible on genuinely unpredictable tasks — requires threshold
  calibration
- Adds observability infrastructure cost to every pipeline

---

## Related Patterns

- [`defect-severity-vocabulary.md`](./defect-severity-vocabulary.md) — Variance events
  are classified using the shared severity vocabulary (P0/P1/P2/P3)
- [`anti-pattern-firewall.md`](./anti-pattern-firewall.md) — Silent failure is a
  forbidden behaviour enforced by the firewall; the PSP is the detection mechanism
- [`paired-artifacts.md`](./paired-artifacts.md) — Progress artefacts are paired with
  task definitions and travel together through the pipeline

## CC-00 References

- `core-component-00/harness-engineering/implementations/context_monitor.py` — Token
  budget monitoring pattern analogous to variance monitoring
- `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`
  — Checkpoint commits in git serve as milestone markers for the PSP
