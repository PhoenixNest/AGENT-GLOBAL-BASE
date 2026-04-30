# Multi-Agent Engineering: Core Concepts and Foundations

## 1. What Is Multi-Agent Engineering?

### Definition

**Multi-Agent Engineering** is the discipline of designing, orchestrating, and operating coordinated systems of specialised LLM-powered agents. It treats the collection of agents not as independent tools but as a **unified system** whose emergent capability exceeds the sum of its parts.

### The Central Insight

A single LLM agent — no matter how well-prompted — cannot reliably handle problems that span multiple domains, require parallel execution, or demand adversarial review. The solution is not a bigger model; it is a **better-orchestrated system of smaller, specialised agents**.

> Multi-Agent Engineering is the discipline of making that system work.

### How Multi-Agent Engineering Differs from Related Disciplines

| Dimension           | Prompt Engineering              | Context Engineering                       | Harness Engineering                     | Multi-Agent Engineering               |
| ------------------- | ------------------------------- | ----------------------------------------- | --------------------------------------- | ------------------------------------- |
| **Core Question**   | How do I instruct one agent?    | What information should be in the window? | How do I safely execute one model call? | How do many agents solve one problem? |
| **Primary Concern** | Wording, structure, examples    | Memory, assembly, slot allocation         | Error handling, token limits, tools     | Decomposition, routing, synthesis     |
| **Time Horizon**    | Single prompt                   | Entire agent session                      | Single model call                       | Entire multi-agent workflow           |
| **Key Output**      | A well-structured prompt        | A precision-assembled context window      | A safely wrapped API call               | A coordinated multi-agent execution   |
| **Primary Skill**   | Language and reasoning patterns | Information architecture                  | Software engineering                    | Systems architecture                  |

---

## 2. The Agent Swarm

### Definition

An **Agent Swarm** is a coordinated system of specialised subagents that collectively solve a problem through structured decomposition, parallel execution, contextual handoff, and synthesised integration — producing emergent system-level intelligence that exceeds any individual agent's capability.

The metaphor is biological: like ant colonies or bee swarms, no individual agent understands the complete solution. But through local rules (agent identity), pheromone trails (context handoff), role specialisation (prompt engineering), and collective infrastructure (harness + RAG), the swarm produces solutions of extraordinary complexity.

### The Five Capabilities of an Effective Swarm

| #   | Capability              | Description                                                                                 | CC-00 Pillar        |
| --- | ----------------------- | ------------------------------------------------------------------------------------------- | ------------------- |
| 1   | **Task Decomposition**  | The orchestrator breaks a user request into atomic subtasks assignable to specialist agents | Harness Engineering |
| 2   | **Specialist Dispatch** | Each subtask is routed to the agent best equipped to handle it, based on role expertise     | Prompt Engineering  |
| 3   | **Context Isolation**   | Each agent receives only the context it needs — no more, no less — via the Handoff Protocol | Context Engineering |
| 4   | **Parallel Execution**  | Independent subtasks run concurrently; dependent tasks are sequenced                        | Harness Engineering |
| 5   | **Result Synthesis**    | A supervisor agent assembles subagent outputs into a coherent final deliverable             | All Four Pillars    |

### Swarm Topology Patterns

| Topology         | Description                                                     | When to Use                                          | Agent Count | Coordination Cost |
| ---------------- | --------------------------------------------------------------- | ---------------------------------------------------- | ----------- | ----------------- |
| **Hierarchical** | Supervisor agents delegate to worker agents in a tree structure | Complex projects with clear domain boundaries        | 10–80+      | Medium            |
| **Flat**         | All agents at the same level, coordinated by a single router    | Many independent subtasks of similar complexity      | 3–10        | Low               |
| **Mesh**         | Agents communicate peer-to-peer via a shared artifact store     | Research exploration, adversarial review             | 3–6         | High              |
| **Pipeline**     | Strict sequential chain; each agent's output feeds the next     | Well-defined workflows with sequential dependencies  | 5–12        | Very Low          |
| **Hybrid**       | Dynamically combines hierarchical + fork-join + pipeline        | Production-grade systems handling diverse task types | 10–80+      | Medium-High       |

---

## 3. Git Worktree Orchestration

### Definition

**Git Worktree Orchestration** is the practice of using `git worktree` to provision isolated, branch-backed working directories for each agent in a swarm — enabling true parallel file-system-level development with Git-native conflict resolution, atomic merge, and full audit trail.

### The Problem It Solves

Traditional multi-agent coding has a critical bottleneck: **filesystem contention**. If two agents edit the same file simultaneously, one overwrites the other. Git worktrees eliminate this by giving each agent its own checkout. Merging is deferred to a controlled integration step.

### How It Works

| Step                   | Git Command                                                  | What It Does                                        |
| ---------------------- | ------------------------------------------------------------ | --------------------------------------------------- |
| 1. Create worktree     | `git worktree add ../agent-<name> -b agent/<name>/task-<id>` | Isolated working directory on a dedicated branch    |
| 2. Agent works         | _(edits files in its worktree)_                              | Exclusive filesystem access; no contention          |
| 3. Agent commits       | see commit format below                                      | Version-controlled with attribution and audit trail |
| 4. Integration         | `git checkout main && git merge agent/<name>/task-<id>`      | Orchestrator merges into main branch                |
| 5. Conflict resolution | `git merge --abort` or manual resolution                     | Integration Agent resolves conflicts                |
| 6. Cleanup             | `git worktree remove ../agent-<name>`                        | Worktree removed; branch optionally deleted         |

**Required commit message format** — agents MUST use the multi-line HEREDOC with a hyphenated body:

```bash
git add -A
git commit -m "$(cat <<'EOF'
agent/<name>: <brief verb-phrase in imperative mood>

- <discrete change 1>
- <discrete change 2>
- <discrete change 3>
- <rationale or cross-reference if non-obvious>

EOF
)"
```

A single-line commit message with no body is a **P2 defect** — it eliminates the audit trail that `git log` and `git blame` rely on for swarm attribution.

### Branch Naming Convention

| Pattern            | Example                                 | Purpose                                          |
| ------------------ | --------------------------------------- | ------------------------------------------------ |
| Agent namespace    | `agent/cto/arch-review-042`             | Identifies which agent owns the branch           |
| Task ID suffix     | `agent/backend-dev/TASK-2026-0429-001`  | Links branch to a specific subtask               |
| Stage prefix       | `stage5/agent/ios-lead/settings-screen` | Links branch to the pipeline stage               |
| Integration branch | `integration/sprint-42`                 | Intermediate merge target before main            |
| Swarm prefix       | `swarm/dark-mode-feature`               | Groups all agent branches for a single execution |

### Git Worktree vs. Alternatives

| Approach                      | FS Isolation       | Attribution      | Conflict Handling  | Rollback      | Native Tooling |
| ----------------------------- | ------------------ | ---------------- | ------------------ | ------------- | -------------- |
| **Git Worktree**              | ✅ Full            | ✅ Per-commit    | ✅ Git 3-way merge | ✅ Per-commit | ✅ Native Git  |
| **Single Checkout + Locks**   | ❌ Shared          | ⚠️ File-level    | ❌ Manual          | ❌ Coarse     | ❌ Custom      |
| **Copy-on-Write Dirs**        | ✅ Isolated        | ❌ None          | ❌ Manual diff     | ⚠️ Dir-level  | ❌ Custom      |
| **Container per Agent**       | ✅ Full OS-level   | ⚠️ Volume mounts | ❌ No native merge | ⚠️ Snapshot   | ⚠️ Docker      |
| **Branch-Only (no worktree)** | ❌ Shared checkout | ✅ Per-commit    | ✅ Git merge       | ✅ Per-commit | ✅ Native Git  |

---

## 4. The Context Handoff Protocol

### The Problem

When an orchestrator delegates to a subagent, two failure modes emerge:

- **Over-sharing:** The full context window is forwarded. The subagent wastes tokens on irrelevant history.
- **Under-sharing:** Only the task description is forwarded. The subagent lacks decisions and constraints.

### The Three Handoff Tiers

| Tier        | What Is Forwarded                                                                  | Token Budget Impact | When to Use                                   |
| ----------- | ---------------------------------------------------------------------------------- | ------------------- | --------------------------------------------- |
| **Full**    | System slot + sacred context + recent history + retrieved content + working memory | ~100%               | Subagent continues the exact same task        |
| **Scoped**  | Scoped role + task-relevant decisions + sub-task description + filtered retrieval  | 20–40%              | Subagent handles one bounded sub-task         |
| **Minimal** | Task description + input data only                                                 | <10%                | Subagent is an independent specialist or tool |

### Tier Selection Matrix

| Subagent Scenario                                     | Tier                | Rationale                                            |
| ----------------------------------------------------- | ------------------- | ---------------------------------------------------- |
| Continues the same task (e.g., coding after planning) | Full                | Same context needed                                  |
| Writes one module in a larger system                  | Scoped              | Needs architectural decisions, not full conversation |
| Performs a pure calculation                           | Minimal             | Input → output; no context needed                    |
| Calls an external API                                 | Minimal             | No model reasoning required beyond the call          |
| Is third-party / untrusted                            | Minimal + sanitised | Do not expose internal decisions or history          |
| Is a language translator                              | Scoped              | Needs source text + style guidelines only            |
| Is a security reviewer                                | Scoped              | Needs code + security requirements; not all history  |

---

## 5. The Unified Architecture

### The Four-Layer Model

| Layer                      | Pillar              | Contribution to Multi-Agent Systems                                  |
| -------------------------- | ------------------- | -------------------------------------------------------------------- |
| **Layer 1: Identity**      | Prompt Engineering  | Each agent has a defined role, expertise boundary, and output format |
| **Layer 2: Context**       | Context Engineering | Handoff Protocol delivers Minimum Viable Context to each agent       |
| **Layer 3: Orchestration** | Harness Engineering | Task decomposition, routing, fork-join, pipeline, state management   |
| **Layer 4: Knowledge**     | RAG Systems         | Shared knowledge base; episodic memory of swarm executions           |

### The Feedback Loop

The system learns from each execution:

1. **Agent outputs** become **new knowledge** in RAG (dynamic memory)
2. **Execution patterns** inform **harness optimization** (which routing paths work best)
3. **Context assembly metrics** improve **future context engineering** (what information was actually useful)
4. **Agent performance** feeds back into **prompt refinement** (identity tuning)

---

## 6. Maturity Model

> The full formal maturity model with level assessment guide is maintained by the
> ASE governance module:
> [`core-component-00/agent-systems-engineering/governance/maturity-model.md`](../agent-systems-engineering/governance/maturity-model.md)

Summary:

| Level | Name                  | Prerequisite                          |
| ----- | --------------------- | ------------------------------------- |
| **0** | Single Agent          | —                                     |
| **1** | Prompt Specialisation | Prompt Engineering                    |
| **2** | Subagent Delegation   | Context Engineering                   |
| **3** | Agent Swarm           | Harness Engineering + RAG             |
| **4** | Git-Backed Swarm      | Git infrastructure + all five pillars |
| **5** | Self-Improving Swarm  | RAG + analytics pipeline              |

---

## 7. Relationship to Other Modules

| Module                            | Provides to Multi-Agent Engineering                       | Receives from Multi-Agent Engineering          |
| --------------------------------- | --------------------------------------------------------- | ---------------------------------------------- |
| `prompt-engineering/`             | Agent identity patterns and role definitions              | Requirements for multi-agent identity design   |
| `context-engineering/`            | Handoff Protocol implementation, context assembly         | Multi-agent context flow architecture          |
| `harness-engineering/`            | Error boundary, tool registry, token monitoring per agent | Orchestration patterns that wrap harness calls |
| `retrieval-augmented-generation/` | Shared knowledge base, episodic memory                    | New knowledge generated by swarm executions    |

---

## 8. References

- [Agent Systems Engineering — Convergence of Four Disciplines](../agent-systems-engineering/CONCEPTS.md)
- [Swarm Topologies](./fundamentals/swarm-topologies.md)
- [Git Worktree Orchestration](./fundamentals/git-worktree-orchestration.md)
- [Orchestration Patterns](./patterns/orchestration-patterns.md)
- [Anti-Patterns](./patterns/anti-patterns.md)
- [Context Handoff Protocol](../context-engineering/patterns/multi-agent-handoff.md)
- [Context Assembler](../context-engineering/implementations/context_assembler.py)
- [Error Boundary](../harness-engineering/implementations/error_boundary.py)

---

**Version:** 1.0
**Last Updated:** 2026-04-29
**Maintained by:** Claude Lab Engineering Team
