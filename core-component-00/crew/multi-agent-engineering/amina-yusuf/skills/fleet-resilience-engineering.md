---
name: cc00-fleet-resilience-engineering
description: Failover pattern design for orchestrator-agent loss mid-task in swarm_orchestrator.py. Owned by Amina Yusuf (Senior Research Engineer II, Multi-Agent Engineering). Trigger: fleet resilience, orchestrator failover, agent loss recovery.
version: "1.0.0"
---

# Fleet Resilience Engineering

**Skill ID:** fleet-resilience-engineering
**Role:** Senior Research Engineer II — Multi-Agent Engineering
**Seniority:** L3 — Senior

## Overview

Designs failover behavior for `swarm_orchestrator.py` when an orchestrator agent is lost
mid-task — ensuring partial results are preserved and the fleet degrades gracefully rather than
losing all in-flight work.

## Tools & Frameworks

| Tool                          | Proficiency | Use Case                                    |
| ----------------------------- | ----------- | ------------------------------------------- |
| Distributed failover patterns | Expert      | Orchestrator-loss recovery design           |
| Fleet state checkpointing     | Advanced    | Preserving partial progress across failover |

## Module Ownership

- Co-owns `swarm_orchestrator.py` with Dr. Farouk, focused specifically on resilience and
  failover behavior — Farouk retains primary ownership of topology selection
- Reports resilience gaps found during design work to Farouk before implementing fixes, since he
  is her direct module lead

## Scenarios & Trade-offs

### Scenario 1: Orchestrator Lost with In-Flight Subagent Tasks

- **Approach:** A standby orchestrator resumes from the last checkpointed fleet state rather than
  restarting the entire fleet from scratch
- **Trade-off:** Checkpointing adds overhead to every orchestration cycle, even when failover
  never triggers
- **Quality Bar:** Checkpoint overhead is benchmarked and kept below a documented latency budget

### Scenario 2: Ambiguous Fleet State After Partial Failover

- **Approach:** When checkpoint state is ambiguous (e.g., a subagent's completion status unknown
  at time of orchestrator loss), the resumed orchestrator treats it as incomplete and re-verifies
  rather than assuming success
- **Trade-off:** Re-verification wastes some work if the task actually did complete
- **Quality Bar:** No resumed fleet ever silently drops a task as "assumed complete" without
  verification

## Quality Standards

- Every failover path is tested with simulated orchestrator loss at multiple points in a task
  lifecycle
- Checkpoint state is versioned and auditable
- Resilience changes are reviewed by Dr. Farouk before merge, per module co-ownership

## References

- `core-component-00/engineering/multi-agent-engineering/implementations/swarm_orchestrator.py`
- Swarm Topology Engineering (Dr. Farouk) — the module lead's primary ownership area
