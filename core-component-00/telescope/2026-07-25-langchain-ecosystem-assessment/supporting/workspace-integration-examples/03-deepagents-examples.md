# 03 — DeepAgents Examples (`deepagents`)

**Prerequisite:** `00-conventions-and-baseline.md`.
**Status:** Reference examples, API surface verified against `langchain-ai/docs` via Context7 on
2026-07-26. **Partially executed 2026-07-27:** Example 1's declared topology (static named
subagents, `StateBackend`, a checkpointer, gated writes) runs end to end with no API key, and
Example 3's `FilesystemBackend` confinement claim is proven by 4 real, passing tests in
`verification/` (a standalone project in this same folder — see its `README.md`). That run also
surfaced a real finding: `FilesystemBackend` defaults to `virtual_mode=False`, under which a `..`
path segment escapes `root_dir` entirely — Example 3's "root_dir is the whole confinement
boundary" claim requires `virtual_mode=True` passed explicitly; the doc's own code block above
does not set it and should be treated as incomplete until it does.
**Verification boundary:** the full parameter _signature_ was verified; the runtime _semantics_ of
`skills=`, `permissions=`, and `memory=` were not. Those three are named accurately and described
cautiously — confirm their behaviour before relying on them.

---

## What this product is, in one paragraph

DeepAgents is "the batteries-included agent harness" — a pre-wired, opinionated agent with a planning
tool, a filesystem backend, sub-agent spawning, and context management already assembled. It sits one
level above `create_agent`: where LangChain gives you a loop and somewhere to attach middleware,
DeepAgents gives you an agent that already has the middleware a long-horizon task needs. It is the
youngest component in the stack (repository created 2025-07-27) and the most opinionated, which is
both its value and its risk: **the opinions it ships are not CC-00's opinions**, and the gap between
them is where the governance work lives.

**Adopt it when** the task is long-horizon and file-shaped — multi-step research, codebase work,
anything where the agent needs to plan, take notes, and delegate. **Do not adopt it** for a bounded
single-purpose agent; `create_agent` plus the CC-00 stack is smaller and easier to reason about.

---

## The governance tension, stated up front

DeepAgents' headline feature — dynamic sub-agent spawning — sits in direct tension with an ASGF
**Mandatory** requirement:

> **L5 — Swarm topology explicitly selected (Mandatory):** "The swarm topology is documented before
> implementation. **Emergent topology without design intent is not acceptable.**"

An agent that spawns subagents at its own discretion is, by construction, emergent topology. This is
not a reason to reject DeepAgents — it is a reason to constrain it. The resolution used throughout
this file:

1. **Enumerate every subagent statically.** The `subagents=[...]` list is the topology document.
   Never leave the general-purpose subagent as the only entry, because "general-purpose" is a
   topology that says nothing.
2. **Bound each subagent's tools.** A subagent whose tool list is a subset of the parent's cannot
   escalate its own authority.
3. **Record the decomposition in the design record**, not only in code — the ASGF requirement is that
   it is _documented before implementation_, and a Python list satisfies "documented" only if
   someone reviewed it as a design.

With those three in place, DeepAgents' delegation is a _declared_ hierarchy that happens to be
dispatched dynamically — which does satisfy the requirement. Without them, it is exactly what the
standard prohibits.

---

## Example 1 — A governed deep research agent

**Use when:** the task is multi-step research or analysis that exceeds a single context window.

**ASGF requirements exercised:** L1 role/constraints/escalation, L2 sacred context (via `memory=`),
L3 high-risk gating (via `interrupt_on=`), L5 topology + decomposition + non-overlapping roles.

```python
"""Example 1 — DeepAgents with the topology declared and writes gated.

Note what is passed explicitly rather than defaulted: subagents (topology),
interrupt_on (approval gate), backend (blast radius), checkpointer (durability),
state_schema (four-slot structure). Every one of those defaults to something
reasonable and none of the reasonable defaults are ASGF-sufficient.
"""

from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from langgraph.checkpoint.sqlite import SqliteSaver

from cc00_langchain.asgf import cc00_middleware_stack
from cc00_langchain.telemetry import install_tracing

install_tracing(service_name="cc00-deep-research")

SYSTEM_PROMPT = """\
# Role

You are the Lead Research Agent for the CC-00 laboratory. You plan multi-step
investigations, delegate bounded subtasks to named specialists, and synthesise
their findings into a single evidence-backed report.

# Behavioural constraints (forbidden behaviours)

- Never present a retrieved claim as your own conclusion. Attribute every factual
  claim to its source.
- Never fabricate a citation, a version number, or a statistic. If a figure cannot
  be retrieved, say it could not be retrieved.
- Never trim scope to finish faster. If the investigation is larger than the budget,
  report what was covered and what was not.
- Never delegate to a specialist outside your declared roster.

# Escalation criteria

Return control to the human when: the evidence is contradictory and the contradiction
changes the recommendation; a required source is unreachable; or the task as stated
cannot be completed within the token budget.

# Delegation

You have exactly three specialists. Use `retriever` for corpus questions, `analyst`
for numerical or comparative reasoning, and `critic` before finalising anything.
"""

# --- ASGF L5: the topology, declared. This list IS the topology document. -----------
#
# DECOMPOSITION — bounded and non-overlapping:
#   retriever : question         -> cited passages     (retrieval tools only)
#   analyst   : cited passages   -> comparison/figures (calculator only, no retrieval)
#   critic    : draft finding    -> refutation attempt (no tools at all)
#
# The critic holds NO tools deliberately: its job is to attack the draft using only
# what the draft claims, which is the check that catches unsupported inference.
SUBAGENTS = [
    {
        "name": "retriever",
        "description": "Retrieves and cites passages from the workspace corpus. Read-only.",
        "system_prompt": (
            "Retrieve passages answering the question. Return each passage with its source "
            "path verbatim. Never summarise away the source. If nothing relevant is found, "
            "say so — do not return the closest available match as if it answered."
        ),
        "tools": [search_workspace],          # from 04 — the MCP-bridged tools
    },
    {
        "name": "analyst",
        "description": "Compares and computes over already-retrieved passages. No retrieval.",
        "system_prompt": (
            "Reason only over the passages you are given. You have no retrieval tool; if the "
            "passages are insufficient, say what is missing rather than inferring it."
        ),
        "tools": [calculator],
    },
    {
        "name": "critic",
        "description": "Attempts to refute a draft finding. Holds no tools.",
        "system_prompt": (
            "Try to refute the finding you are given, using only the evidence it cites. "
            "Report every unsupported inference, overstated confidence, and missing "
            "counter-consideration. Default to 'not established' when uncertain."
        ),
        "tools": [],
    },
]

checkpointer = SqliteSaver(connection)

agent = create_deep_agent(
    model="anthropic:claude-sonnet-5",
    tools=[search_workspace, calculator],
    system_prompt=SYSTEM_PROMPT,
    subagents=SUBAGENTS,

    # --- Blast radius: virtual filesystem held in graph state, not on disk --------
    # StateBackend keeps the agent's scratch files inside checkpointed state. The
    # agent gets its notes and its planning surface; the host filesystem is
    # untouched. See Example 3 before changing this.
    backend=StateBackend(),

    # --- ASGF L3: high-risk operations gated ------------------------------------
    # Even with a virtual filesystem, writes are gated: the state IS the deliverable,
    # and a silent overwrite of a synthesis is a real loss.
    interrupt_on={
        "write_file": True,     # approve / edit / reject
        "edit_file": True,
        "read_file": False,     # reads are cheap and reversible
        "ls": False,
    },

    # REQUIRED for interrupt_on to work at all — no checkpointer, no durable pause.
    checkpointer=checkpointer,

    # The CC-00 governance stack composes with DeepAgents' own middleware.
    # ORDERING CAVEAT: DeepAgents installs its own context-management middleware.
    # FourSlotContextMiddleware must remain the innermost message-rewriter or the
    # four-slot guarantee is silently lost. Verify the effective order on first run.
    middleware=cc00_middleware_stack(
        system_prompt=SYSTEM_PROMPT,
        task_type="tool_research",     # CC-00 profile: 40% tool outputs, 35% retrieved
        max_model_calls=60,            # long-horizon work; still bounded
    ),

    name="cc00-deep-research",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": research_question}]},
    config={"configurable": {"thread_id": f"research-{investigation_id}"}},
)
```

**The ordering caveat is not boilerplate.** DeepAgents ships its own context-management middleware,
and `cc00_middleware_stack()` was designed on the assumption that `FourSlotContextMiddleware` is the
last thing to touch messages before dispatch. Those two assumptions have not been tested together —
they cannot be, with no package installed. **First-run shakedown item #1: log the assembled message
list immediately before dispatch and confirm the four-slot structure survived.**

---

## Example 2 — Subagents as declared decomposition

**Use when:** you need the topology in reviewable form, separate from the code that runs it.

**ASGF requirements:** L5 task decomposition (Mandatory), L5 agent roles non-overlapping (Required),
L5 supervisor defined for hierarchical swarms (Required).

The `SUBAGENTS` list in Example 1 is executable. This is the same information in the form a reviewer
can sign off on — and ASGF asks for the topology to be documented _before_ implementation, which
means this table should exist first.

| Agent          | Role                                          | Inputs            | Tools              | Outputs              | May delegate to |
| -------------- | --------------------------------------------- | ----------------- | ------------------ | -------------------- | --------------- |
| **supervisor** | Plan, delegate, synthesise, resolve conflicts | Research question | all                | Final report         | all three       |
| `retriever`    | Retrieve and cite                             | A single question | `search_workspace` | Cited passages       | none            |
| `analyst`      | Compare and compute                           | Cited passages    | `calculator`       | Comparison / figures | none            |
| `critic`       | Refute                                        | Draft finding     | _(none)_           | Refutation report    | none            |

**Topology:** Hierarchical. **Supervisor:** the parent deep agent (implicit in DeepAgents — it _is_
the top-level agent, and ASGF's "supervisor agent defined for hierarchical swarms" is satisfied by
naming it, which the `name=` parameter does).

**Overlap check (ASGF L5 Required, >70% overlap ⇒ consolidate):** `retriever` and `analyst` share no
tools and take different inputs. `critic` shares no tools with either. No pair approaches the
threshold. **Recorded, not assumed.**

**Per-subagent model override** — when one specialist genuinely needs different capability:

```python
{
    "name": "critic",
    "description": "Attempts to refute a draft finding. Holds no tools.",
    "system_prompt": "...",
    "tools": [],
    "model": "anthropic:claude-opus-5",   # refutation is the quality-critical step
}
```

Use this sparingly and record why. A per-subagent model override is a cost and latency decision
disguised as a configuration line, and an undocumented one is impossible to review later.

---

## Example 3 — Backend choice is a blast-radius decision

**Use when:** deciding between `StateBackend` and `FilesystemBackend`. Decide it deliberately; the
difference is what the agent can destroy.

```python
"""Example 3 — the two backends, and what each one costs you.

StateBackend      : virtual filesystem inside graph state. Nothing touches the host.
FilesystemBackend : real files under root_dir. The agent can write to your disk.
"""

from deepagents.backends import FilesystemBackend, StateBackend

# --- Default for research and analysis --------------------------------------------
# Files live in checkpointed state: durable, replayable, time-travellable, and
# incapable of damaging anything outside the graph. Costs: the "filesystem" dies
# with the thread, and large artefacts inflate every checkpoint.
backend = StateBackend()


# --- Only when the deliverable IS files on disk ------------------------------------
# root_dir is the ONLY confinement -- but ONLY if virtual_mode=True is also passed.
# FOUND BY RUNNING THIS 2026-07-27 (verification/tests/test_03_deepagents_examples.py):
# virtual_mode defaults to False, and under that default a ".." path segment or an
# absolute path escapes root_dir entirely. Point it at a dedicated working directory —
# never at a repository root, never at a home directory, never at the workspace.
backend = FilesystemBackend(root_dir="./.cc00/agent-workspace/{run_id}", virtual_mode=True)
```

**Rules for `FilesystemBackend` in this workspace:**

| Rule                                                                | Reason                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `root_dir` is a dedicated, disposable directory                     | It is the whole confinement boundary. Everything inside it is at risk.                                                                                                                                                                               |
| **`virtual_mode=True` is passed explicitly, always**                | **Verified 2026-07-27:** the library's own default (`False`) allows `..` and absolute paths to bypass `root_dir` — reproduced in `verification/tests/test_03_deepagents_examples.py::test_filesystem_backend_virtual_mode_false_allows_path_escape`. |
| Never point it at the repository root                               | An agent with write access to `.claude/`, `.mcp.json`, or a `pipeline.md` can rewrite governance.                                                                                                                                                    |
| Pair it with `interrupt_on={"write_file": True, "edit_file": True}` | ASGF L3: irreversible operations require human approval. Disk writes are irreversible.                                                                                                                                                               |
| Prefer a git worktree when the agent edits real code                | Workspace convention for multi-agent work; isolation plus a reviewable diff.                                                                                                                                                                         |

**The governance-capture risk is specific and worth naming.** This workspace's guardrails live in
Markdown and JSON — `pipeline.md` stage gates, ADRs, `.claude/rules/`, `.mcp.json`. An agent with
unrestricted filesystem write access can edit the documents that constrain it. `root_dir` is what
prevents that, and it prevents it only if it points somewhere harmless.

---

## Example 4 — Borrowing DeepAgents' middleware without the whole harness

**Use when:** you want planning and a scratch filesystem, but you want `create_agent`'s smaller,
more predictable surface and your own middleware ordering.

This composition is the verified pattern from the official docs, and it is the recommended shape when
the DeepAgents ordering caveat in Example 1 makes you uncomfortable — here **you** own the order.

```python
"""Example 4 — DeepAgents' capabilities, create_agent's control.

TodoListMiddleware      : gives the agent a planning surface (the todo tool)
FilesystemMiddleware    : gives it a scratch filesystem over the chosen backend
SubAgentMiddleware      : gives it bounded delegation

Take the ones you need. Leave the rest.
"""

from deepagents.backends import StateBackend
from deepagents.middleware import FilesystemMiddleware
from deepagents.middleware.subagents import SubAgentMiddleware
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware

from cc00_langchain.asgf import (
    FourSlotContextMiddleware,
    ObservabilityMiddleware,
    PIIMiddleware,
    TokenBudgetMiddleware,
    ToolGovernanceMiddleware,
    TypedErrorBoundaryMiddleware,
)

backend = StateBackend()

agent = create_agent(
    model="anthropic:claude-sonnet-5",
    tools=[search_workspace, calculator],
    system_prompt=SYSTEM_PROMPT,
    middleware=[
        # --- CC-00 governance, outermost-first (see 00 §7 on ordering) ------------
        ObservabilityMiddleware(),
        TypedErrorBoundaryMiddleware(),
        TokenBudgetMiddleware(max_tokens=128_000, max_model_calls=60),
        PIIMiddleware(),
        ToolGovernanceMiddleware(),

        # --- DeepAgents capabilities ---------------------------------------------
        TodoListMiddleware(),
        FilesystemMiddleware(backend=backend),
        SubAgentMiddleware(backend=backend, subagents=SUBAGENTS),

        # --- Innermost: nothing may rewrite messages after this -------------------
        FourSlotContextMiddleware(
            system_prompt=SYSTEM_PROMPT, task_type="tool_research"
        ),
    ],
)
```

**Why this is often the better choice in this workspace.** `create_deep_agent` is a bundle; this is a
list. The bundle is faster to stand up and harder to audit — and an ASGF audit has to answer "what
touches the context window, in what order", which a list answers directly.

---

## Unverified parameters — handle with care

`create_deep_agent` accepts `skills=`, `memory=`, and `permissions=`. The signature is verified; the
semantics are not. What can be said accurately:

| Parameter                            | What was verified                                                                       | What to confirm before use                                                                                                                                 |
| ------------------------------------ | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `memory=["./AGENTS.md"]`             | Appears in official examples alongside `FilesystemBackend`; loads files as agent memory | Whether entries are re-read per turn, and whether they are compressible. **If they are compressible, they are not a substitute for CC-00 sacred context.** |
| `permissions=[FilesystemPermission]` | Parameter exists and is filesystem-scoped                                               | Whether it constrains subagents as well as the parent — that determines whether it is an authority boundary or a convenience.                              |
| `skills=[...]`                       | Parameter exists, takes a list of strings                                               | Resolution mechanism and whether skill content enters the System slot (which would affect the L2 budget).                                                  |

Do not build a control on any of these three until its behaviour is confirmed by execution. An
unverified control is worse than a missing one.

---

## Anti-pattern summary for this product

| Anti-pattern                                                 | Why it fails                                                                             |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Leaving subagents undeclared / general-purpose only          | Emergent topology. Explicitly prohibited by ASGF L5 Mandatory.                           |
| `FilesystemBackend(root_dir=<repo root>)`                    | The agent can rewrite the governance documents that constrain it.                        |
| `interrupt_on` omitted while writes are enabled              | ASGF L3: irreversible operations ungated.                                                |
| `interrupt_on` set without a checkpointer                    | The gate silently does nothing. The docs are explicit that the checkpointer is required. |
| Subagent with a _superset_ of the parent's tools             | Authority escalation through delegation.                                                 |
| Assuming DeepAgents' context management satisfies ASGF L2    | It manages context; it does not impose the four-slot structure. Different requirement.   |
| Using `create_deep_agent` for a bounded single-purpose agent | Paying a large opinionated surface for a loop you could declare in six lines.            |

---

**Document status:** Reference examples — unexecuted. Parameter semantics for `skills`/`memory`/`permissions` unverified.
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-26
