# ASE Maturity Model

> **Governing authority:** ADR-ASE-001 · Core Component 00 Laboratory
> **Version:** 1.0 · **Last Updated:** 2026-04-30

The ASE Maturity Model provides a structured progression for evaluating and evolving
the sophistication of LLM-powered agent systems. Each level builds on the previous and
corresponds to a measurable increase in system capability, resilience, and architectural
coherence.

The model is used in two ways:

1. **Assessment** — determine where an existing system currently sits
2. **Roadmap** — plan the investment sequence for elevating a system to the next level

---

## The Six Levels

| Level | Name                  | Core Capability                                                             | ASE Compliance |
| ----- | --------------------- | --------------------------------------------------------------------------- | -------------- |
| **0** | Single Agent          | One LLM, one prompt, no orchestration                                       | Not required   |
| **1** | Prompt Specialisation | Multiple structured prompts; router selects the right one per task type     | Layer 1        |
| **2** | Subagent Delegation   | Orchestrator + 2–5 specialists with defined handoff protocol                | Layers 1–2     |
| **3** | Agent Swarm           | 5–20+ agents in hierarchical or hybrid topology with fork-join              | Layers 1–3     |
| **4** | Git-Backed Swarm      | Level 3 + git worktree isolation; full filesystem isolation and audit trail | Layers 1–4     |
| **5** | Self-Improving Swarm  | Level 4 + episodic memory feedback loops; swarm optimises its own routing   | All Layers     |

---

## Level 0 — Single Agent

**What it is:** One LLM, one prompt, no orchestration, no retrieval, no error handling
beyond what the application layer provides.

**Characteristics:**

| Feature                                           | Present                                         |
| ------------------------------------------------- | ----------------------------------------------- |
| Single `system` prompt defining the agent's role  | Yes                                             |
| Direct API call with no wrapper or error boundary | Yes (bare)                                      |
| External knowledge retrieval                      | No — parametric knowledge only                  |
| Session management                                | No — each interaction is stateless              |
| Suitable for                                      | Prototypes, demos, and bounded low-stakes tasks |

**Why this is not ASE-compliant:** The absence of harness engineering means the system
fails silently when rate limits, timeouts, or context overflows occur. Acceptable for
exploration; not for production.

**Prerequisite to advance:** Decide to invest in structured prompt engineering (Level 1)
or structured orchestration (skip to Level 2 if delegation is the natural next step).

---

## Level 1 — Prompt Specialisation

**What it is:** Multiple structured prompts, each designed for a specific task type.
A router — human or automated — selects the appropriate prompt based on the incoming
request.

**Characteristics:**

| Feature             | Detail                                                                               |
| ------------------- | ------------------------------------------------------------------------------------ |
| Prompt design       | Each task type has a dedicated, structured prompt (role, constraints, output format) |
| Prompting technique | Matched to task type — zero-shot, few-shot, or CoT as appropriate                    |
| Output format       | Schema-constrained where downstream processing requires structured output            |
| Agent count         | Single-agent per invocation — no inter-agent communication                           |
| Error handling      | Basic only — retry on failure                                                        |

**ASE requirements satisfied:** Layer 1 (Prompt Engineering) — basic compliance.

**What it lacks:** Context engineering for long sessions, harness-level error
boundaries, retrieval, and multi-agent coordination.

**Prerequisite to advance to Level 2:** Identify tasks that exceed single-agent scope
and require delegation to specialists.

---

## Level 2 — Subagent Delegation

**What it is:** An orchestrator agent decomposes complex tasks and delegates subtasks
to 2–5 specialist agents. The Context Handoff Protocol governs what each specialist
receives.

**Characteristics:**

| Feature                  | Detail                                                      |
| ------------------------ | ----------------------------------------------------------- |
| Orchestrator             | Defined decomposition strategy; does not do work directly   |
| Specialist agents        | 2–5 agents with bounded, non-overlapping roles              |
| Context handoff          | Full / Scoped / Minimal protocol implemented per handoff    |
| Context window structure | Four-slot (System / Retrieved / History / Tool) implemented |
| Token budget             | Tracked and managed at context assembly time                |

**ASE requirements satisfied:** Layers 1–2 (Prompt + Context Engineering).

**What it lacks:** Harness-level error boundaries for tool use and model calls,
retrieval pipeline for external knowledge, and swarm-level orchestration for large
parallel workloads.

**Prerequisite to advance to Level 3:** Harness engineering — implement error
boundaries, token budget monitoring, and tool registries.

---

## Level 3 — Agent Swarm

**What it is:** A fully orchestrated multi-agent swarm of 5–20+ agents operating in a
hierarchical or hybrid topology. Fork-join parallelism is implemented. The full harness
engineering stack is in place.

**Characteristics:**

| Feature             | Detail                                                                          |
| ------------------- | ------------------------------------------------------------------------------- |
| Swarm topology      | Explicitly designed: Hierarchical, Flat, Mesh, Pipeline, or Hybrid              |
| Harness stack       | Error boundaries, token budget monitors, and tool registries deployed per agent |
| Parallelism         | Fork-join for independent subtasks                                              |
| Synthesis           | Supervisor agent responsible for output synthesis and conflict resolution       |
| Knowledge retrieval | RAG pipeline implemented for domain knowledge                                   |
| Retrieval quality   | Reranking, ACL filtering, and freshness management in place                     |

**ASE requirements satisfied:** Layers 1–4 (all four original ASE pillars).

**What it lacks:** Filesystem-level isolation for parallel coding agents — agents
sharing a repository risk overwriting each other's work.

**Prerequisite to advance to Level 4:** Git infrastructure with worktree support and
an Integration Agent role.

---

## Level 4 — Git-Backed Swarm

**What it is:** A Level 3 swarm augmented with git worktree isolation — each agent
receives a dedicated, branch-backed working directory. An Integration Agent manages
merge sequencing and conflict resolution.

**Characteristics:**

| Feature         | Detail                                                                          |
| --------------- | ------------------------------------------------------------------------------- |
| Agent isolation | Every coding agent operates in an isolated `git worktree` on a dedicated branch |
| Branch naming   | `agent/<name>/task-<id>` convention enforced                                    |
| Commit messages | Multi-line with agent attribution — no anonymous commits                        |
| Merge lifecycle | Owned by a dedicated Integration Agent; no agent self-merges                    |
| Audit trail     | Every change attributable to a specific agent and task                          |
| Reproducibility | Swarm executions are reproducible and rollback-safe                             |

**ASE requirements satisfied:** All five layers — full ASE compliance.

**What it lacks:** The ability to learn from execution history to improve future
routing and performance.

**Prerequisite to advance to Level 5:** Episodic memory infrastructure and an
analytics pipeline to surface routing optimisation signals.

---

## Level 5 — Self-Improving Swarm

**What it is:** A Level 4 swarm augmented with episodic memory and feedback loops.
The swarm records execution outcomes — routing paths, agent performance, context
efficiency metrics — and uses this data to optimise its own behaviour over time.

**Characteristics:**

| Feature                     | Detail                                                                                                            |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Episodic memory             | Captures per-execution outcomes: routing decisions, latency, quality verdicts, error frequencies                  |
| Feedback loop               | A feedback agent or scheduled pipeline analyses episodic memory and proposes routing and prompt refinements       |
| Context efficiency tracking | Identifies which retrieved chunks were actually referenced — unused context is deprioritised in future assemblies |
| Agent identity refinement   | Identity prompts updated from performance data — not by hand, but by ground-truth feedback analysis               |
| Self-assessment             | The swarm knows where it is failing and why — maturity is continuously monitored                                  |

**ASE requirements satisfied:** All five layers + continuous compliance monitoring.

This is the target state for any production-grade, long-lived LLM-powered system. It
is the architectural equivalent of a self-healing distributed system.

---

## Level Assessment Guide

Use this checklist to determine the current maturity level of a system:

| Question                                                                                   | Level Gate      |
| ------------------------------------------------------------------------------------------ | --------------- |
| Are all agent prompts structured with role, constraints, and output format?                | Gate to Level 1 |
| Is a Context Handoff Protocol implemented for every agent-to-agent transition?             | Gate to Level 2 |
| Is a full harness stack (error boundary, token monitor, tool registry) deployed per agent? | Gate to Level 3 |
| Is an external knowledge retrieval pipeline implemented with reranking and ACL filtering?  | Gate to Level 3 |
| Are parallel coding agents isolated in git worktrees with an Integration Agent?            | Gate to Level 4 |
| Is episodic memory captured and used to refine routing and prompts?                        | Gate to Level 5 |

A system satisfies a level gate when **all** questions for that gate are answered
affirmatively. A partial affirmative moves the system to the level below.

---

## References

- [ADR-ASE-001](./adr-ase-001.md) — Governing ratification decision
- [Compliance Standard](./compliance-standard.md) — Per-layer requirements
- [Foundational Paper](core-component-00/agent-systems-engineering/CONCEPTS.md) — Convergence thesis
- [Multi-Agent Engineering Module](core-component-00/engineering/multi-agent-engineering/README.md) — Swarm implementation
- [Git Worktree Orchestration](core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md) — Level 4 infrastructure
