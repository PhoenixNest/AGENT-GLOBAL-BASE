# Project Overview

| Concept           | Description                                                                                                     |
| :---------------- | :-------------------------------------------------------------------------------------------------------------- |
| **Identity**      | Unified organizational simulation and LLM engineering base.                                                     |
| **Format**        | Markdown-first, agent-native knowledge base for AI agents.                                                      |
| **Architecture**  | Three architecturally independent co-resident systems governed by an Agent Systems Engineering (ASE) framework. |
| **Key Artifacts** | Documents, agent profiles, executable skill files (`skills/*.md`), and Python reference implementations.        |

# Directory Overview

| System          | Path                 | Description                           | Key Details                                                                                                                                                                                                                                                                                      |
| :-------------- | :------------------- | :------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ecosystem**   | `.gemini/`           | Agent CLI & Swarm Ecosystem           | **Hub:** `.gemini/ECOSYSTEM_SPEC.md`<br>**Agents:** 119 migrated sub-agents natively loadable via `invoke_agent`.<br>**Skills:** Progressive disclosure router system grouped by 19 domain-specific `SKILL.md` files.<br>**Hooks:** Native event wrappers mapped in `settings.json`.             |
| **The Company** | `company/`           | Mobile product company simulation     | **Hub:** `company/library/README.md`<br>**Pipeline:** 13-stage (Mobile, Web, Backend API, Full-Stack) with strict approval gates, defect severity rules (P0-P3), and Stage 3 tech lock.<br>**Departments:** Brand Design, Cyberspace Security, HR, Legal, Localization, Product Management, R&D. |
| **The Studio**  | `studio/`            | Creative game development environment | **Hub:** `studio/casual-games/library/overview/casual-games-studio.md`<br>**Tech Stack:** Unity 6.3 LTS, C#, <50MB binary target, multi-tenant backend.<br>**Pipeline:** 11-stage focusing on soft launches and retention thresholds (e.g., D1 ≥ 35% for hybrid-casual).                         |
| **CC-00**       | `core-component-00/` | Applied LLM research laboratory       | Canonical base for reliable LLM-powered systems governed by ASE framework.<br>**Modules:** prompt, context, harness, RAG, and multi-agent engineering.                                                                                                                                           |

## CC-00 Modules Breakdown

| Layer       | Module                            | Focus                    | Details                                                                         |
| :---------- | :-------------------------------- | :----------------------- | :------------------------------------------------------------------------------ |
| **Layer 1** | `prompt-engineering/`             | Agent identity           | Roles, decision frameworks.                                                     |
| **Layer 2** | `context-engineering/`            | Information architecture | MVC (Minimum Viable Context), positional bias, memory types. (Has Python code)  |
| **Layer 3** | `harness-engineering/`            | Execution orchestration  | Error boundaries, context budget monitoring, tool registries. (Has Python code) |
| **Layer 4** | `retrieval-augmented-generation/` | Dynamic memory           | Vector stores, Knowledge Item (KI) patterns. (Has Python code)                  |
| **Layer 5** | `multi-agent-engineering/`        | Swarm orchestration      | Git worktree isolation, Context Handoff Protocols. (Has Python code)            |

# Key Files

| File Path                                                 | Description                                                                                                                                     |
| :-------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| `AGENTS.md`                                               | Authoritative entry point and orientation guide for all AI agents. Defines identity, agent types (Type A/Type B), command structure, and rules. |
| `.gemini/ECOSYSTEM_SPEC.md`                               | Architecture and migration specifications for the `.gemini/` CLI integration (Sub-agents, Router Skills, Hooks).                                |
| `core-component-00/agent-systems-engineering/CONCEPTS.md` | Theoretical synthesis of the five LLM engineering disciplines, illustrating the "outside-in" approach.                                          |

# Usage

AI Executor agents (Type B) are expected to read `AGENTS.md` before taking any action.

| #     | Rule                        | Description                                                                                                                      |
| :---- | :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| **1** | **Read Before Acting**      | Consult `profile.md`, `pipeline.md`, and skill files before executing tasks or adopting a persona (Type A).                      |
| **2** | **Respect Pipelines**       | Follow stage gates (User Approval checkmarks) in `pipeline.md`. No auto-advancing past user approval.                            |
| **3** | **Use Worktrees**           | Follow git worktree isolation for parallel swarm work (`fundamentals/git-worktree-orchestration.md`).                            |
| **4** | **Format Content**          | Run `prettier --write "<file-path>"` on created or modified files.                                                               |
| **5** | **Absolute User Authority** | User holds final authority over all decisions, overriding pipelines or hierarchies.                                              |
| **6** | **Apply MVC**               | Pass only necessary info for the task, placing critical instructions at the beginning and end of the context window.             |
| **7** | **Tabular Formatting**      | Present document content in tabular form (tables) to enhance readability.                                                        |
| **8** | **Ecosystem Authority**     | All agentic workflows, sub-agent invocations, and hook implementations MUST adhere to governance in `.gemini/ECOSYSTEM_SPEC.md`. |
