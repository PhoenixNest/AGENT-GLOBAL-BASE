---
name: cc00-swarm-topology-engineering
description: Swarm topology orchestration implementation and selection for swarm_orchestrator.py. Owned by Dr. Idris Farouk (Staff Research Engineer, Multi-Agent Engineering Lead). Trigger: swarm orchestration, swarm topology, agent fleet coordination, orchestration pattern.
version: "1.0.0"
---

# Swarm Topology Engineering

**Skill ID:** swarm-topology-engineering
**Role:** Staff Research Engineer — Multi-Agent Engineering Lead
**Seniority:** L4 — Staff

## Overview

Production implementation of `core-component-00/engineering/multi-agent-engineering/implementations/swarm_orchestrator.py`
— swarm topology selection (hierarchical, mesh, pipeline, hub-and-spoke) and orchestration
execution for multi-agent fleets, including the `fleet_id`-scoped orchestration required by
`core-component-00/engineering/multi-agent-engineering/testing/test_swarm_orchestrator.py`.

## Tools & Frameworks

| Tool                         | Proficiency | Use Case                                       |
| ---------------------------- | ----------- | ---------------------------------------------- |
| Python (async orchestration) | Expert      | Swarm coordination implementation              |
| Distributed systems patterns | Expert      | Topology selection under partial observability |
| pytest                       | Expert      | Fleet-scoped orchestration test coverage       |

## Module Ownership

- Maintains `swarm_orchestrator.py`: topology selection logic, fleet lifecycle management, and
  `fleet_id` scoping for concurrent independent swarms
- Owns topology-selection guidance: when to use hierarchical vs. mesh vs. pipeline vs.
  hub-and-spoke, tied to task decomposition characteristics (see Dr. Vance's
  `multi-agent-orchestration-design.md` for the design-level framework this implements)
- Runs regression benchmarks comparing topology performance under varying fleet sizes and task
  dependency graphs

## Scenarios & Trade-offs

### Scenario 1: High Task Interdependency

- **Approach:** Hierarchical topology with an orchestrator agent holding the dependency graph,
  rather than mesh (peer-to-peer) coordination which struggles with complex dependency ordering
- **Trade-off:** Hierarchical adds a coordination bottleneck at the orchestrator; mesh distributes
  load but risks deadlock on interdependent tasks
- **Quality Bar:** No deadlock or missed-dependency execution in the benchmark suite for
  interdependency graphs up to depth 5

### Scenario 2: Independent Parallel Subtasks at Scale

- **Approach:** Hub-and-spoke topology with the orchestrator fanning out and collecting results,
  no peer-to-peer agent communication needed
- **Trade-off:** Hub-and-spoke is simple and scales well for independent work but wastes the
  opportunity for peer agents to share intermediate findings
- **Quality Bar:** Fan-out/fan-in overhead scales sub-linearly with fleet size up to the tested
  fleet size ceiling

## Quality Standards

- Every topology has a benchmark demonstrating its performance characteristics, not just a design
  rationale
- `fleet_id` scoping is tested for cross-fleet isolation — no state leak between concurrent fleets
- Orchestration failures degrade gracefully (partial results returned) rather than losing all
  in-flight work

## References

- `core-component-00/engineering/multi-agent-engineering/implementations/swarm_orchestrator.py`
- Multi-Agent Orchestration Design (Dr. Vance, `skills/multi-agent-orchestration-design.md`)
