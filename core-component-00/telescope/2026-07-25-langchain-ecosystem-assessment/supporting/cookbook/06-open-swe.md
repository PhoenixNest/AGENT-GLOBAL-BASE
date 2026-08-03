# Open SWE — Enterprise User Manual

**Repository:** `langchain-ai/open-swe` · **Stars:** 10,391 (2026-07-25) · **Status:** Active (pushed
2026-07-25)
**Verification status:** GitHub metadata only (stars, description, activity, retrieved via the
GitHub REST API on 2026-07-25 by the parent assessment). **The repository's source code was not read**
and the application was not installed or run in this session. This manual's disposition is more
cautionary than the others in this cookbook, and that caution is the main content — read §1 and §2
before anything else.

---

## 1. Introduction

### What it is

Open SWE is described by the LangChain organisation as "an Open-Source Asynchronous Coding Agent" —
a cloud-style autonomous agent, built on the LangChain/LangGraph stack, that operates on a codebase:
reading, writing, and presumably committing code changes with limited human supervision per
interaction cycle.

### The category it belongs to

Like Open Deep Research and openwiki, this is an **application**, not a library — something you
deploy and run, not something you `pip install` into another codebase.

### Why this manual leads with caution, not adoption guidance

An autonomous coding agent is categorically different from the other five products in this cookbook.
DeepAgents, `langchain-mcp-adapters`, Open Deep Research, and openwiki all operate on **information**
— they read, retrieve, synthesise, or generate documentation. Open SWE, by design, operates on **the
codebase itself**, including (per its own description) with limited supervision.

In this workspace specifically, that is a governance question before it is a technical one. This
workspace's guardrails — `.claude/rules/`, `pipeline.md` stage gates, ADRs under
`agent-systems-governance-framework/governance/`, and `.mcp.json` — are themselves files. An agent
with unrestricted write access to the repository can edit the documents that constrain it. This is
not a hypothetical concern specific to Open SWE; it is the general reason `../workspace-integration-examples/05-reference-applications.md`
assigns Open SWE the disposition **Observe, do not deploy — for now**, and that disposition still
holds. This manual does not reverse it.

### Enterprise framing

For a non-technical stakeholder: this is the difference between "an AI that helps write code" (which
this workspace already has, in the form of the assistant producing this document) and "an AI that
operates with standing, less-supervised authority to modify a codebase." The second is a materially
larger authority grant, and granting it requires infrastructure this workspace has not yet built —
not a policy objection to the concept in principle.

---

## 2. Usage

> **Do not deploy Open SWE against this workspace's primary repository under any current
> configuration.** The preconditions below are not yet satisfied. This section describes what would
> need to be true before revisiting that position, not instructions to follow now.

### Preconditions before any deployment is reconsidered

Reproduced from `../workspace-integration-examples/05-reference-applications.md` §2, because it is the operative content of this
manual:

1. **A worktree-isolated execution path**, so the agent never writes to the primary working tree.
   This workspace already has the right primitive — `agent/<role>/<task>` branches in dedicated git
   worktrees, per `core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`
   — but Open SWE would need to be wired into that pattern, not run beside it.
2. **A path denylist** covering `.claude/`, `.mcp.json`, `**/pipeline.md`, and
   `agent-systems-governance-framework/governance/**`, enforced at the tool layer (i.e., the agent
   cannot write to these paths even if it tries), not merely requested in a system prompt. A prompt
   instruction is not a control; a tool-layer denylist is.
3. **A designated human or integration agent on every merge — no self-merge.** ASGF L5 is explicit:
   "Merge integration agent designated ... No agent self-merges without review" (Required when
   parallel development).
4. **An answer to "what does review look like when the agent produces more diff than a human can
   read?"** This is named explicitly because it is unsolved, not because it has an easy answer that
   was simply omitted here.

### If deployed, once preconditions are met (unverified specifics)

> Everything below this point is the general, publicly documented pattern for cloud-style coding
> agents of this kind — **not confirmed against this specific repository's actual configuration
> surface.** Consult the repository's own README before acting on any of it.

```powershell
# UNVERIFIED — illustrative, not confirmed for this repository.
git clone https://github.com/langchain-ai/open-swe.git
cd open-swe
pip install -r requirements.txt
# Coding agents in this class typically need: a chat-model API key, a
# git-hosting API token scoped to the TARGET repository (not a personal or
# org-wide token), and a sandboxed execution environment for running tests
# and installing dependencies inside the target codebase.
```

**The one instruction given with full confidence:** whatever credential this agent is configured
with, scope it to the narrowest possible target — a single disposable worktree or fork, never a token
with write access to the primary repository or to any of the denylisted governance paths above.

---

## 3. Alternatives and rationale

| Option                                                                                                        | Choose it when                                                                                    | Trade-off against Open SWE                                                                                                                                                                                                                                                |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Code itself, human-supervised, in this session's normal mode**                                       | The default for essentially all coding work in this workspace today                               | Every write is visible to and approved by the human in the loop, in real time. This is precisely the supervision Open SWE's "asynchronous" design relaxes — which is the whole point of Open SWE, and the whole reason it needs more infrastructure before adoption here. |
| **A bounded, tool-restricted `create_agent`** with a narrow, explicitly whitelisted set of file-editing tools | You want AI-assisted code changes with a smaller blast radius than a full autonomous coding agent | Smaller capability, smaller risk. Does not require solving the worktree-isolation / denylist / no-self-merge preconditions above, because its authority is bounded by tool whitelist from the start rather than by after-the-fact isolation.                              |
| **Not adopting an autonomous coding agent at all, for now**                                                   | The preconditions in §2 are not yet built, and there is no urgent need forcing the question       | This is the report's own implicit position: `../workspace-integration-examples/05-reference-applications.md` observes rather than recommends. Zero new capability, zero new risk.                                                                                         |

**Rationale:** the comparison that matters here is not "Open SWE vs. a competing autonomous coding
agent" — the research report did not survey that category — it is "Open SWE vs. the supervision level
this workspace currently operates at." The honest answer is that adopting any autonomous coding agent,
Open SWE or otherwise, is a governance-infrastructure decision first and a tool-selection decision
second. Until the four preconditions in §2 are satisfied, the tool-selection question is premature.

---

## 4. Integrations

| Integrates with                                     | How (confidence)                                                                                                                                                                                                                      |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **LangGraph**                                       | **Confirmed by category** — built on the LangChain/LangGraph stack per its own description.                                                                                                                                           |
| **Git hosting platforms** (GitHub, likely)          | **Likely, unconfirmed** — a coding agent of this kind requires some git-hosting integration for reading/writing code and opening changes; specific mechanism not verified.                                                            |
| **This workspace's git worktree isolation pattern** | **Not upstream — a CC-00 precondition, not a feature.** Any future deployment must be wired into `core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`'s existing pattern, per §2 above. |
| **A designated Integration Agent / merge reviewer** | **Not upstream — a CC-00 requirement.** ASGF L5's no-self-merge rule applies regardless of what Open SWE itself supports natively.                                                                                                    |
| **Sandboxed execution environments**                | **Likely, unconfirmed** — running and testing code changes typically requires an isolated execution environment; specific mechanism (container, VM, cloud sandbox) not verified for this repository.                                  |

---

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
