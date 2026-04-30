# Swarm Topologies

> The five canonical patterns for organising multiple agents into a coordinated system.

---

## Overview

A swarm topology defines **how agents are arranged, how they communicate, and who has authority** in a multi-agent system. The choice of topology determines the system's throughput, latency, quality ceiling, and coordination overhead.

| Topology     | Structure                   | Communication                            | Authority                           |
| ------------ | --------------------------- | ---------------------------------------- | ----------------------------------- |
| Hierarchical | Tree (supervisor → workers) | Top-down delegation, bottom-up reporting | Supervisors decide                  |
| Flat         | Star (router → peers)       | Hub-and-spoke via router                 | Router dispatches; agents are equal |
| Mesh         | Fully connected             | Peer-to-peer via shared store            | No single authority; consensus      |
| Pipeline     | Linear chain                | Sequential handoff                       | Previous stage gates next stage     |
| Hybrid       | Dynamic combination         | Mixed                                    | Context-dependent                   |

---

## Topology 1: Hierarchical Swarm

### Structure

```mermaid
flowchart TB
    O(["Orchestrator<br/>(CEO / CTO)"])
    S1["Supervisor<br/>(VP Eng)"]
    S2["Supervisor<br/>(VP QA)"]
    S3["Supervisor<br/>(VP Sec)"]
    W1["Workers"]
    W2["Workers"]
    W3["Workers"]

    O --> S1
    O --> S2
    O --> S3
    S1 --> W1
    S2 --> W2
    S3 --> W3
```

### Properties

| Property              | Value                                              |
| --------------------- | -------------------------------------------------- |
| **Agent count**       | 10–80+                                             |
| **Coordination cost** | Medium (scales with tree depth)                    |
| **Quality ceiling**   | Very High (supervisor oversight)                   |
| **Parallelism**       | Within each supervisor's worker pool               |
| **Best for**          | Complex projects with clear domain boundaries      |
| **Example**           | Full product pipeline: CPO → CDO → CTO → Dev teams |

### Context Flow

- Orchestrator uses **Scoped handoff** to each supervisor
- Supervisors use **Scoped handoff** to workers (further filtered)
- Workers use **Minimal handoff** for tool calls
- Results flow bottom-up through the same chain

### Strengths and Weaknesses

| Strengths                             | Weaknesses                              |
| ------------------------------------- | --------------------------------------- |
| Clear chain of command                | Supervisor is a bottleneck              |
| Quality gates at each level           | Deep trees increase latency             |
| Natural domain boundaries             | Information loss at each handoff level  |
| Mirrors real organisational structure | Requires high-quality supervisor agents |

---

## Topology 2: Flat Swarm (Fork-Join)

### Structure

```mermaid
flowchart TB
    R["Router Agent"]
    A1["Agent 1"]
    A2["Agent 2"]
    A3["Agent 3"]
    A4["Agent 4"]
    SY["Synthesis Agent"]

    R --> A1
    R --> A2
    R --> A3
    R --> A4
    A1 --> SY
    A2 --> SY
    A3 --> SY
    A4 --> SY
```

### Properties

| Property              | Value                                              |
| --------------------- | -------------------------------------------------- |
| **Agent count**       | 3–10                                               |
| **Coordination cost** | Low                                                |
| **Quality ceiling**   | Medium (no deep oversight)                         |
| **Parallelism**       | Full (all agents run concurrently)                 |
| **Best for**          | Independent subtasks of similar complexity         |
| **Example**           | Translating an app into 5 languages simultaneously |

### Context Flow

- Router uses **Minimal or Scoped handoff** to each worker
- All workers execute in parallel
- Synthesis agent receives all results and produces combined output

---

## Topology 3: Mesh Swarm

### Structure

```mermaid
flowchart TB
    A1["Agent 1"] <--> A2["Agent 2"]
    A1 <--> A3["Agent 3"]
    A1 <--> A4["Agent 4"]
    A2 <--> A3
    A2 <--> A4
    A3 <--> A4

    AS[("Shared Artifact<br/>Store")]
    A1 <--> AS
    A2 <--> AS
    A3 <--> AS
    A4 <--> AS
```

### Properties

| Property              | Value                                                         |
| --------------------- | ------------------------------------------------------------- |
| **Agent count**       | 3–6 (beyond 6, coordination explodes)                         |
| **Coordination cost** | High (O(n²) communication paths)                              |
| **Quality ceiling**   | High for creative/research tasks                              |
| **Parallelism**       | Full (but with synchronisation points)                        |
| **Best for**          | Research exploration, brainstorming, adversarial review       |
| **Example**           | Architecture proposal where each agent critiques others' work |

### Context Flow

- Agents read from and write to a shared artifact store
- No central orchestrator — agents self-coordinate
- Requires strong convergence criteria to terminate

---

## Topology 4: Pipeline Swarm

### Structure

```mermaid
flowchart LR
    S1["Stage 1<br/>(PRD)"] -->|"Gate"| S2["Stage 2<br/>(Proto)"]
    S2 -->|"Gate"| S3["Stage 3<br/>(Arch)"]
    S3 -->|"Gate"| S4["Stage 4<br/>(Code)"]
    S4 -->|"Gate"| S5["Stage 5<br/>(Test)"]
```

### Properties

| Property              | Value                                               |
| --------------------- | --------------------------------------------------- |
| **Agent count**       | 5–12                                                |
| **Coordination cost** | Very Low (linear; each stage has one predecessor)   |
| **Quality ceiling**   | High (gate criteria prevent defect propagation)     |
| **Parallelism**       | None (strictly sequential)                          |
| **Best for**          | Well-defined workflows with sequential dependencies |
| **Example**           | 10-stage development pipeline                       |

### Context Flow

- Each stage agent receives the output of the previous stage via **Scoped handoff**
- Gate criteria must be satisfied before advancing
- Hierarchical summarisation prevents context growth across stages

---

## Topology 5: Hybrid Swarm

### Structure

The Hybrid Swarm dynamically combines multiple topologies based on the task:

```mermaid
flowchart TB
    U["User Request"] --> O(["Orchestrator<br/>(selects topology per subtask)"])
    O --> P["Pipeline<br/>(Stage 1 → 2 → 3)"]
    O --> F["Fork-Join<br/>(Review A ∥ B ∥ C)"]
    O --> D["Debate<br/>(Advocate vs Critic)"]
```

### Properties

| Property              | Value                                                                                                |
| --------------------- | ---------------------------------------------------------------------------------------------------- |
| **Agent count**       | 10–80+                                                                                               |
| **Coordination cost** | Medium-High (orchestrator must manage multiple topologies)                                           |
| **Quality ceiling**   | Very High (best-fit topology per subtask)                                                            |
| **Parallelism**       | Selective (parallelise where possible, sequence where required)                                      |
| **Best for**          | Production-grade systems handling diverse task types                                                 |
| **Example**           | Full-stack application: pipeline for core flow, fork-join for reviews, debate for security decisions |

### Context Flow

- Orchestrator maintains a task graph with topology annotations
- Each subtask inherits the appropriate context flow from its topology
- Results are synthesised at join points

---

## Topology Selection Decision Tree

```mermaid
flowchart TD
    Q1{"Is the task<br/>decomposable?"}
    Q2{"Are subtasks<br/>independent?"}
    Q3{"Sequential<br/>dependencies?"}
    Q4{"Adversarial<br/>review needed?"}
    SA["Single Agent"]
    FJ["Fork-Join<br/>(Flat Swarm)"]
    PL["Pipeline Swarm"]
    MS["Mesh Swarm<br/>(Debate)"]
    HS["Hierarchical<br/>(Supervisor)"]
    HY["Hybrid Swarm"]

    Q1 -->|"No"| SA
    Q1 -->|"Yes"| Q2
    Q2 -->|"Yes"| FJ
    Q2 -->|"No"| Q3
    Q3 -->|"Yes"| PL
    Q3 -->|"No"| Q4
    Q4 -->|"Yes"| MS
    Q4 -->|"No"| HS
    Q2 -->|"Both independent<br/>& dependent"| HY

    style SA fill:#27ae60,stroke:#1e8449,color:#fff
    style FJ fill:#2980b9,stroke:#1a5276,color:#fff
    style PL fill:#e67e22,stroke:#d35400,color:#fff
    style MS fill:#8e44ad,stroke:#6c3483,color:#fff
    style HS fill:#c0392b,stroke:#922b21,color:#fff
    style HY fill:#2c3e50,stroke:#1a252f,color:#fff
```

---

**Version:** 1.0
**Last Updated:** 2026-04-29
**See also:** [CONCEPTS.md](../CONCEPTS.md) · [Orchestration Patterns](../patterns/orchestration-patterns.md) · [Quick Reference](../quick_reference.md)
