# 05 — Reference Applications (`open_deep_research`, `open-swe`, `openwiki`)

**Prerequisite:** `00-conventions-and-baseline.md`.
**Status:** Guidance, not code examples. **Verification boundary:** the repository facts below
(stars, activity, archived status) come from the research report's GitHub API retrieval on
2026-07-25. **The source code of these three applications was not read for this deliverable.** The
patterns described are inferred from their documented purpose and from the ecosystem architecture,
and are labelled accordingly. Do not cite this file as evidence of how their internals work.
**Deliberately out of scope for the 2026-07-27 verification effort** (`verification/` in this same
folder): this file's claims are dispositional (harvest / observe / decline), not standalone
runnable code — there is nothing here to execute independently of the three external applications
themselves, whose source was never read.

---

## Why these are in a different category

`langchain`, `langgraph`, `deepagents`, and `langchain-mcp-adapters` are **libraries you import**.
These three are **applications you run, read, or harvest**. The distinction changes what "adopt"
means: you do not add `open_deep_research` to `requirements.txt` and build on it — you either deploy
it, or you read it and take the pattern.

For CC-00 the honest position is that all three are **read-and-harvest** candidates, not adoption
candidates, and the reasoning differs per project.

| Project              | Stars (2026-07-25) | Status                    | CC-00 disposition                                             |
| -------------------- | ------------------ | ------------------------- | ------------------------------------------------------------- |
| `open_deep_research` | 12,426             | Active                    | **Harvest** — best worked example in the ecosystem            |
| `open-swe`           | 10,391             | Active                    | **Observe** — high capability, high authority cost            |
| `openwiki`           | 13,217             | Active                    | **Evaluate separately** — adjacent tooling, not agent runtime |
| `langserve`          | 2,330              | **ARCHIVED** (2026-05-05) | **Do not adopt**                                              |

---

## 1. `open_deep_research` — the reference multi-step research agent

**What it is:** a reference deep-research agent — multi-step search, synthesis, and report
generation. The research report called it "the best-documented worked example in the ecosystem",
and that is its value here.

**Why it matters to CC-00 specifically:** this laboratory's own output is research reports. The
telescope archive is full of them, and this deliverable is one. An agent that does multi-step
retrieval and produces an evidence-backed report is not a hypothetical use case here — it is the
laboratory's core workflow.

**What to harvest** _(inferred from documented purpose, not from reading the source — verify before
relying on any of these)_:

| Pattern                               | Why it transfers                                                                                                     |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Research-plan-then-execute            | Matches the telescope template's own shape: Research Questions → Methodology → Findings.                             |
| Parallel sub-researchers per question | Maps directly onto ASGF L5 decomposition — one bounded subtask per research question.                                |
| Explicit source attribution           | The telescope convention already requires it; CC-00 reports label vendor-reported and rejected sources.              |
| Report assembly as a final stage      | Separating synthesis from retrieval is what stops an agent from writing conclusions it never retrieved evidence for. |

**What NOT to harvest without adaptation:** its evaluation and tracing setup, which in the upstream
project is likely to assume LangSmith. Under the CEO's open-source-only constraint that has to be
replaced with the OpenTelemetry path in `00 §5`. **Check this before copying any observability code
out of it** — a stray `LANGSMITH_TRACING` is a constraint breach, not a convenience.

**A caution worth stating plainly.** A research agent that writes confident reports from thin
evidence is a _worse_ outcome than no research agent, because the output is indistinguishable from a
good report until someone checks the citations. If CC-00 builds on this pattern, the `critic`
subagent from `03 §Example 2` — the one holding no tools, whose only job is refutation — is not
optional garnish. It is the control that makes the rest safe.

---

## 2. `open-swe` — the asynchronous coding agent

**What it is:** "An Open-Source Asynchronous Coding Agent" — a cloud-style autonomous coding agent
built on the LangChain stack.

**Disposition: observe, do not deploy — for now.** The reasoning is authority, not capability.

An autonomous coding agent operating on this repository would hold write access to the documents that
govern it: `.claude/rules/`, `pipeline.md` stage gates, ADRs under
`agent-systems-governance-framework/governance/`, and `.mcp.json`. This workspace's guardrails are
Markdown and JSON files. An agent that can edit files can edit guardrails.

The workspace already has the right primitive for this, and it is not a LangChain feature:

> **Multi-agent / swarm work uses git worktree isolation.** Branch `agent/<role>/<task>`, commits
> with hyphen-bulleted bodies, integration through a designated merge agent. Full spec:
> `core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`

Any coding-agent adoption — `open-swe` or otherwise — must land inside that pattern rather than
beside it. ASGF L5 makes this explicit: "Git worktree isolation used for parallel development"
(Required when parallel coding) and "Merge integration agent designated … **No agent self-merges
without review**" (Required when parallel development).

**Preconditions before this is worth revisiting:**

1. A worktree-isolated execution path, so the agent never writes to the primary working tree.
2. A path denylist covering `.claude/`, `.mcp.json`, `**/pipeline.md`, and
   `agent-systems-governance-framework/governance/**` — enforced at the tool layer, not requested in
   a prompt.
3. A designated human or integration agent on every merge. No self-merge.
4. An answer to "what does review look like when the agent produces more diff than a human can read?"
   This one is unsolved and should not be hand-waved.

Until those exist, the useful thing to take from `open-swe` is its **task decomposition and
verification structure**, read as a design reference.

---

## 3. `openwiki` — adjacent tooling

**What it is:** a CLI that writes and maintains agent-facing documentation for a codebase. The
research report classified it as "adjacent tooling, not part of the agent runtime", and that
classification is correct — it is not something a LangChain agent imports.

**Why it is nonetheless interesting here:** this workspace is a Markdown-first, agent-native
knowledge base whose primary artefacts _are_ agent-facing documents — `CLAUDE.md` files, `AGENTS.md`,
skill contracts, rules. A tool that generates and maintains exactly that category of document
overlaps with work this workspace already does by hand.

**Disposition: evaluate separately, on its own merits.** It is out of scope for a LangChain adoption
decision because it is not part of the agent runtime, and folding it into that decision would
conflate two unrelated questions. Two cautions if it is evaluated later:

- **Generated documentation competes with authored governance.** `CLAUDE.md` files here are
  deliberate policy documents, not summaries of code. A tool that regenerates them would overwrite
  intent with description.
- **The `canonical-source-of-truth` pattern applies.** ASGF's cross-cutting rule exists precisely to
  prevent two documents claiming the same authority. A generated wiki alongside authored
  `CLAUDE.md` files creates that conflict unless one is explicitly subordinate.

---

## 4. `langserve` — do not adopt

**Archived 2026-05-05.** Formerly the "deploy an LCEL chain as a FastAPI REST endpoint" tool.

Recorded here because the research report found that **secondary sources retrieved during that
investigation still describe LangServe as a current deployment tool**. They are wrong; the GitHub API
response carries `"archived": true`. Anyone searching for "how to deploy LangChain" today will
plausibly land on that stale advice.

**What to do instead** — deployment is a normal web-service question, and LangChain has no special
answer to it:

```python
"""Serving a LangGraph agent — plain FastAPI, no LangChain deployment layer needed.

An agent is a callable. Serving it is ordinary web engineering: authenticate,
derive the thread_id from the authenticated session, invoke, return.
"""

from fastapi import Depends, FastAPI
from pydantic import BaseModel

app = FastAPI()


class TriageRequest(BaseModel):
    ticket_text: str


@app.post("/triage")
async def triage(request: TriageRequest, session=Depends(authenticated_session)):
    # thread_id derives from the AUTHENTICATED session, never from the request body.
    # See 02 §2 — a thread_id is a capability to resume someone else's conversation.
    config = {"configurable": {"thread_id": f"triage-{session.id}"}}
    result = await agent.ainvoke(
        {
            "messages": [{"role": "user", "content": request.ticket_text}],
            "user_role": session.role,      # ACL binding — never model-chosen (04 §5)
            "sacred_context": [],
            "retrieved": [],
            "tool_outputs": [],
            "task_type": "factual_qa",
        },
        config,
    )
    return result["structured_response"]
```

**LangGraph Platform / Cloud** is the vendor's answer to deployment and is **commercial —
excluded** by the CEO's constraint. Self-hosted FastAPI plus a pinned SQLite or Postgres checkpointer
is the open-source path, and for a single-machine workspace it is also the simpler one.

---

## Summary of dispositions

| Project              | Adopt?            | What to do                                                                                                     |
| -------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------- |
| `open_deep_research` | Harvest           | Read it; take the plan-execute-synthesise structure and the attribution discipline. Replace its observability. |
| `open-swe`           | No (yet)          | Observe. Revisit only behind worktree isolation, a governance-path denylist, and a no-self-merge rule.         |
| `openwiki`           | Separate decision | Not part of the agent runtime. Evaluate on its own, watching for conflict with authored `CLAUDE.md` policy.    |
| `langserve`          | **No**            | Archived. Serve agents with plain FastAPI.                                                                     |

---

**Document status:** Guidance. Source code of these applications was **not** read — patterns are inferred and labelled.
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-26
