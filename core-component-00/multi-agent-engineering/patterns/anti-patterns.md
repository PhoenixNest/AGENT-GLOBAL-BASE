# Multi-Agent Anti-Patterns

> Seven failure modes that degrade multi-agent system quality, with detection heuristics and remediation strategies.

---

## Overview

Anti-patterns are recurring design mistakes that appear reasonable but lead to predictable failures. In multi-agent systems, anti-patterns are especially dangerous because they compound: a context-dumping orchestrator feeding an agent-sprawled hierarchy produces exponentially worse results than either mistake alone.

---

## Anti-Pattern 1: The God Agent

### Description

One agent tries to handle everything — all domains, all stages, all responsibilities. The agent's prompt is enormous, its context window is saturated, and its output quality degrades across all tasks.

### Detection Heuristics

| Signal                                      | Threshold                |
| ------------------------------------------- | ------------------------ |
| Agent's system prompt exceeds               | >5,000 tokens            |
| Agent handles more than                     | >3 distinct task domains |
| Agent's context window usage                | >85% on routine tasks    |
| Agent makes errors across unrelated domains | Yes                      |

### Consequence

- Context window overflow on complex tasks
- Quality degradation across all tasks (attention diluted)
- No specialist depth in any domain
- Single point of failure for the entire system

### Remedy

1. **Decompose** the God Agent into specialists with clear expertise boundaries
2. Each specialist should have a focused system prompt (<2,000 tokens)
3. Add a router or supervisor to coordinate the specialists
4. Apply the 70% rule: if two specialists share >70% of their skills, they can be one agent

---

## Anti-Pattern 2: Agent Sprawl

### Description

Too many hyper-specialised agents are created for tasks that could be handled by fewer agents. The coordination overhead exceeds the specialisation benefit.

### Detection Heuristics

| Signal                       | Threshold                                          |
| ---------------------------- | -------------------------------------------------- |
| Number of agents per task    | >2× the number of distinct subtasks                |
| Skill overlap between agents | >70%                                               |
| Coordination overhead        | >30% of total execution time                       |
| Agents frequently idle       | >50% of dispatched agents produce no useful output |

### Consequence

- Coordination overhead exceeds specialisation benefit
- Context handoff noise amplifies with each additional agent
- Orchestrator's context window consumed by agent management
- Diminishing returns on agent count

### Remedy

1. **Audit** agent skills for overlap; merge agents sharing >70%
2. Set a minimum task complexity threshold for swarm activation
3. Use simpler topologies (Router, Fork-Join) instead of Hierarchical for bounded tasks
4. Track agent utilisation: if an agent is idle >50% of the time, consider removing it

---

## Anti-Pattern 3: Context Dumping

### Description

The orchestrator forwards its entire context window to every subagent, regardless of the subagent's actual needs. Subagents waste token budget processing irrelevant history and produce lower-quality output.

### Detection Heuristics

| Signal                                                 | Threshold                        |
| ------------------------------------------------------ | -------------------------------- |
| Handoff tier selection                                 | Always "Full" regardless of task |
| Subagent token usage for irrelevant content            | >40% of budget                   |
| Subagent output references information it doesn't need | Yes                              |
| Orchestrator never uses Scoped or Minimal tier         | Yes                              |

### Consequence

- Attention dilution: subagent attends to irrelevant information
- Slower inference: larger context windows increase latency
- Higher cost: more tokens processed per call
- Reduced quality: noise degrades output

### Remedy

1. **Always** select handoff tier explicitly based on the subagent's actual needs
2. Default to **Scoped** handoff, not Full
3. Use **Minimal** for tool-wrapper agents and pure calculations
4. Monitor subagent token utilisation; flag >40% budget spent on non-task content

---

## Anti-Pattern 4: Flat Hierarchy

### Description

All agents operate at the same level with no supervisor, no chain of command, and no conflict resolution mechanism. When agents produce conflicting outputs, there is no authority to resolve the disagreement.

### Detection Heuristics

| Signal                                  | Threshold              |
| --------------------------------------- | ---------------------- |
| Number of supervisor agents             | 0                      |
| Conflicting agent outputs per execution | >1 unresolved conflict |
| Escalation path defined                 | No                     |
| Resolution mechanism for contradictions | None                   |

### Consequence

- Conflicting decisions with no resolution
- User receives contradictory recommendations
- No quality oversight or synthesis
- System output quality is random

### Remedy

1. Add at least one **supervisor agent** per domain cluster
2. Define explicit escalation paths: worker → supervisor → orchestrator → human
3. Implement a synthesis step that detects and resolves contradictions
4. Use the Defect Severity vocabulary (P0–P3) as shared conflict classification

---

## Anti-Pattern 5: Synchronous Everything

### Description

All subtasks are executed sequentially even when many are independent and could run concurrently. Wall-clock time is unnecessarily multiplied by the number of agents.

### Detection Heuristics

| Signal                                              | Threshold         |
| --------------------------------------------------- | ----------------- |
| Tasks with no data dependency executed sequentially | >30% of subtasks  |
| Total wall-clock time vs. critical path time        | >2× critical path |
| Fork-Join pattern used                              | Never             |
| Agent idle time during sequential execution         | >50%              |

### Consequence

- Unnecessarily slow pipeline execution
- Poor resource utilisation
- User waiting time multiplied by agent count
- Competitive disadvantage vs. systems that parallelise

### Remedy

1. **Analyse** the task dependency graph before execution
2. Identify independent subtasks and execute them via **Fork-Join**
3. Only sequence tasks with true data dependencies
4. Measure critical path time vs. actual time; target ≤1.5× ratio

---

## Anti-Pattern 6: Missing Feedback Loop

### Description

No mechanism for the swarm to learn from past executions. The same mistakes are repeated, the same routing paths are used regardless of outcomes, and no quality improvement occurs over time.

### Detection Heuristics

| Signal                                  | Threshold              |
| --------------------------------------- | ---------------------- |
| Episodic memory entries per execution   | 0                      |
| Routing path optimisation               | Static (never updated) |
| Post-execution analysis                 | Not performed          |
| Same errors recurring across executions | >2 recurrences         |

### Consequence

- Same mistakes repeated across executions
- No quality improvement over time
- Routing paths never optimised
- Context assembly never refined based on what was actually useful

### Remedy

1. Record **episodic memory** for every swarm execution (task, agents, outcomes)
2. Implement **post-execution analysis** that identifies failure points
3. Feed execution outcomes back into routing decisions
4. Track context assembly metrics: what information was used vs. what was ignored

---

## Anti-Pattern 7: Trim-to-Pass

### Description

An agent "fixes" failing tests or quality gates by removing the functionality being tested, rather than fixing the underlying issue. The system appears to pass quality checks but has silently lost features.

### Detection Heuristics

| Signal                                                       | Threshold          |
| ------------------------------------------------------------ | ------------------ |
| Lines of code deleted in "fix" commit                        | >50% of the change |
| Test cases removed or disabled                               | Any                |
| Features present in PRD but absent in code                   | Any                |
| Agent's fix description mentions "simplifying" or "removing" | Yes                |

### Consequence

- Feature regression shipped to user
- Quality gates rendered meaningless
- User requirements not met
- Erosion of trust in the testing pipeline

### Remedy

1. **Explicitly forbid** trim-to-pass in every agent's identity prompt
2. Add an integrity verification gate that cross-references PRD features against code
3. Track code coverage direction: coverage must not decrease after a "fix"
4. Flag any commit that removes test cases for mandatory human review

---

## Anti-Pattern Interaction Matrix

Some anti-patterns amplify each other:

| Combination                        | Result                                                                           |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| Context Dumping + Agent Sprawl     | Every agent in a large swarm receives full context → exponential token waste     |
| Flat Hierarchy + Missing Feedback  | Conflicts never resolved AND never learned from → quality degrades monotonically |
| God Agent + Synchronous Everything | One overloaded agent processing everything sequentially → maximum latency        |
| Trim-to-Pass + Missing Feedback    | Feature removal goes undetected AND unrecorded → permanent regression            |

---

**Version:** 1.0
**Last Updated:** 2026-04-29
**See also:** [Orchestration Patterns](./orchestration-patterns.md) · [Quick Reference](../quick_reference.md) · [CONCEPTS.md](../CONCEPTS.md)
