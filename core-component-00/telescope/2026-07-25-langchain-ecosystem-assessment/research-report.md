# Research Report — LangChain Ecosystem Assessment: Architecture, Adoption, and Local Deployment on CC-00 Hardware

---

## Metadata

| Field                | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Investigation ID** | `2026-07-25-langchain-ecosystem-assessment`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **Date Started**     | 2026-07-25                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Date Completed**   | 2026-07-25                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Status**           | Complete — advisory. Local-serving tool decided: **LM Studio** (2026-07-26). Enterprise examples added 2026-07-26 (see § Addendum), consolidated 2026-07-27 into `supporting/workspace-integration-examples/` (see § Consolidation and Version History v1.7), then given an independent test harness the same day (`verification/`, 13 real passing tests, see § Independent verification harness and Version History v1.8), which surfaced a `FilesystemBackend` finding closed workspace-wide the same day per CEO requirement (see § Complete fix and Version History v1.9), then independently re-checked by the relevant CC-00 crew per CEO direction the same day (see § Crew review and Version History v1.10), then formally closed out as an exploratory study per CEO direction on 2026-07-28 (see § Closure and Version History v1.11); a runnable companion project added 2026-07-27, relocated same day into `supporting/` and later renamed to `supporting/enterprise-examples/` per CEO direction (see § Runnable Companion and Version History v1.3–v1.4); an eight-manual enterprise cookbook added the same day at `supporting/cookbook/`, covering every ecosystem product including LangChain and LangGraph directly (see § Cookbook and Version History v1.5–v1.6). Broader LangChain pilot-adoption decision still pending. |
| **Investigator**     | CC-00 Laboratory (Director: Dr. Elias Vance)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Laboratory**       | Core Component 00                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **Module(s)**        | All five layers (L1 Prompt, L2 Context, L3 Harness, L4 RAG, L5 Multi-Agent) + ASGF meta-layer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Priority**         | High                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **Requestor**        | CEO + User (joint request)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Shape**            | Programme — this report plus one `supporting/` folder (8 enterprise-example documents, added 2026-07-26)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

---

> **Reading note (added 2026-07-26).** This investigation now has two parts. **Findings 1–10,
> Analysis, and Recommendations below are the original 2026-07-25 assessment and are unchanged.**
> The CEO subsequently commissioned enterprise-grade examples and best practices built on that
> assessment; those live in `supporting/` and are summarised in § Addendum — 2026-07-26, which adds
> **Findings 11–14** and supplementary recommendations. The examples are a deliverable of this
> investigation, **not a separate assessment** — there is one LangChain assessment report, and this
> is it.

---

## Knowledge Freshness Disclosure

Per the CC-00 RAG freshness protocol:

- **Assistant knowledge cutoff:** May 2026. LangChain moves faster than that cutoff, so every
  version number, star count, adoption figure, and CVE in this report was **retrieved live on
  2026-07-25** rather than recalled.
- **Primary sources preferred.** Version and popularity figures come from the GitHub REST API and
  the PyPI JSON API directly, not from secondary summaries.
- **Sources deliberately rejected.** Initial searches surfaced several statistics aggregators
  (`zipdo.co`, `gitnux.org`, `worldmetrics.org`, `wifitalents.com`) carrying precise-sounding
  claims — "65% of production RAG apps", "42% of Fortune 500 piloting LangChain agents",
  "100M+ monthly downloads". These are SEO content farms with no traceable methodology and they
  disagree with each other on figures that should be identical. **None of them are cited here and
  none of those numbers appear in this report.** Where a number appears below, it is either from a
  vendor API or explicitly labelled as vendor-reported.
- **Vendor-reported figures are labelled as such.** LangChain Inc. publishes its own adoption
  survey and its own customer list. Both are used below, and both are flagged, because a vendor
  reporting on its own adoption is an interested party.

---

## Executive Summary

**LangChain in 2026 is not the library it was in 2023.** The v1.0 release (October 2025) discarded
the chain-composition identity that made its name and re-founded the project as an _agent_ runtime:
`create_agent` on top of the LangGraph durable-execution engine, with legacy chains exiled to a
separate `langchain-classic` package. It is, by a wide margin, the most-adopted open-source agent
framework — 142,575 GitHub stars against LlamaIndex's 51,086 and CrewAI's 56,120 — and its
open-source surface now spans an orchestration engine (LangGraph), an agent harness (DeepAgents),
a coding agent (Open SWE), a research agent (Open Deep Research), and an MCP bridge.

**For CC-00 the relevant finding is architectural, not promotional.** LangChain does not confer
ASGF compliance; it is a _substrate_ on which ASGF compliance must still be built. It is, however,
an unusually good substrate, because LangGraph makes two ASGF Mandatory requirements — explicit
swarm topology (L5) and human-approval gating of high-risk operations (L3) — first-class primitives
rather than things you bolt on. Assessed against `compliance-standard.md`, a LangChain-based system
would inherit **no Mandatory gaps but several Required gaps**, giving a projected **Conditional**
verdict absent deliberate remediation.

**The local-deployment answer is constrained by the machine's measured GPU capacity, not by
LangChain.** An RTX 4060 Laptop with 8,188 MiB of VRAM is too small to host a tool-reliable agent
model but far larger than the embedding and reranking stack needs. The recommended architecture
therefore spends the 8 GB of VRAM on embeddings and reranking (small, latency-critical, called
constantly) and keeps the agent "brain" on API models — not on a quantized 8B local model whose
tool-calling reliability is the weakest link in any agent loop.

---

## Investigation Scope

### What Was Investigated

The four questions posed jointly by the CEO and the User:

1. What LangChain is — core principles, functions, usage, and best practices.
2. The remaining core products and applications of the LangChain ecosystem, **open source only**.
3. LangChain's usage rate and coverage in the community and among top technology companies, and
   why they choose it over other frameworks.
4. Given the above and this workspace's actual local hardware, how to deploy LangChain's products
   locally while maximising both agent performance and hardware performance/smoothness.

### Why This Investigation Was Needed

CC-00's five-module stack (`core-component-00/`) was built as a first-party implementation. The
workspace already contains latent LangChain dependencies —
`retrieval-augmented-generation/requirements.txt` pins `langchain>=0.1.0` and
`langchain-community>=0.0.19`, and four RAG documents contain `from langchain.text_splitter import
...` code samples — that were written against the pre-1.0 API and have **never been installed or
executed** (verified: no `langchain*` package is present in the local Python environment). Deciding
whether to modernise, remove, or expand that dependency requires knowing what LangChain actually is
in 2026 and whether it earns its place under ASGF.

### Out of Scope

Per the CEO's explicit constraint — **business cooperation or any paid content is not currently
being considered** — the following were surveyed only far enough to mark the open-source boundary
and were **not** evaluated for adoption:

> - **LangSmith** — the observability/evaluation platform. Free tier exists; the platform itself is
>   a hosted commercial service. Excluded from recommendations.
> - **LangGraph Platform / LangGraph Cloud** — managed agent deployment. Commercial. Excluded.
> - **LangChain Academy paid courses**, enterprise support, and any vendor engagement. Excluded.
> - Model-provider API pricing and commercial-terms comparison. Excluded.

Also out of scope: fine-tuning or training local models; LLM throughput benchmarking (no model was
run on this machine — every generation-performance figure below is a labelled estimate); the state
and provisioning of the local Python/GPU environment, which is a precondition rather than a subject
here; and any change to workspace code. This is a research deliverable only.

---

## Research Questions

1. What is LangChain's architecture and design philosophy after v1.0, and what are its core
   principles, functions, usage model, and best practices?
2. What else does the LangChain organisation ship as open source, and what is each component for?
3. What is LangChain's measurable adoption relative to competing frameworks, and what technical
   properties explain that position?
4. What is this workspace's actual hardware and software baseline, and what deployment topology
   maximises agent quality and hardware utilisation within it?
5. Does a LangChain-based system satisfy the ASGF compliance standard, and where are the gaps?

---

## Methodology

### Approach

Four-phase investigation, conducted 2026-07-25:

1. **Hardware and runtime measurement** — direct WMI/CIM queries, `nvidia-smi`, a live
   `torch.cuda.is_available()` probe, and inventory of the installed Python/Docker/Node stack.
   Nothing about the machine was assumed.
2. **Primary-source version and popularity retrieval** — GitHub REST API and PyPI JSON API for
   exact, same-day figures on LangChain and four competing frameworks.
3. **Documentation retrieval** — the official LangChain documentation repository via Context7, for
   the v1 architecture and the v0→v1 migration surface.
4. **Workspace grounding** — grep sweep for existing LangChain references, and a read of the ASGF
   `compliance-standard.md` so the governance assessment is scored against the real criteria rather
   than a paraphrase.

### Tools and Resources

- PowerShell / `Get-CimInstance`, `nvidia-smi` (driver 610.62) — hardware inventory
- `python -c "import torch; ..."` — live CUDA availability probe
- GitHub REST API (`api.github.com/repos/...`) — star, fork, and activity data
- PyPI JSON API (`pypi.org/pypi/<pkg>/json`) — authoritative current versions
- Context7 MCP → `/langchain-ai/docs` — official LangChain v1 documentation and migration guide
- Check Point Research — CVE detail for the LangGraph checkpointer chain
- `core-component-00/framework/00-agent-systems-governance-framework/governance/compliance-standard.md`

### Constraints

- **No benchmarks were run.** Every tokens/second, latency, and speedup figure in this report is a
  labelled estimate derived from model size and hardware class, not a measurement on this machine.
  Section §Open Questions lists what would need to be measured to convert them into facts.
- **`pypistats.org` returned HTTP 429**, so package download volumes could not be verified from a
  primary source. Download-count claims are therefore **omitted entirely** rather than sourced from
  the aggregators described above.
- **Vendor-survey bias.** The only structured adoption survey available is LangChain's own.
- **Single-machine scope.** The hardware analysis describes this ASUS Zenbook only.

---

## Findings

### Finding 1: LangChain v1 is an agent framework wearing an old name

The project's centre of gravity moved. In the 0.x era LangChain's identity was **LCEL** — the
LangChain Expression Language — and the `Runnable` protocol, which let you compose prompt → model →
parser pipelines with a `|` operator. That machinery still exists and still underpins the model and
message abstractions, but as of **v1.0 (October 2025)** it is no longer the headline. The headline
is `create_agent`.

**Evidence:**

- Official docs state `create_agent` is "the new standard for building agents in LangChain 1.0,"
  replacing `langgraph.prebuilt.create_react_agent`, and that "LangChain's `create_agent` runs on
  LangGraph's runtime under the hood." (Source: `langchain-ai/docs`, `releases/langchain-v1.mdx`
  and `langchain/runtime.mdx`, retrieved 2026-07-25.)
- The minimal agent is now three arguments:

  ```python
  from langchain.agents import create_agent

  agent = create_agent(
      model="claude-sonnet-4-6",
      tools=[search_web, analyze_data, send_email],
      system_prompt="You are a helpful research assistant.",
  )
  result = agent.invoke({"messages": [{"role": "user", "content": "Research AI safety trends"}]})
  ```

- Current released versions (PyPI, retrieved 2026-07-25): **`langchain` 1.3.14**
  (`>=3.10.0,<4.0.0`), **`langgraph` 1.2.9** (`>=3.10`).
- The `langchain` package was deliberately _slimmed_. Legacy chains, retrievers, the indexing API,
  and the `hub` module moved out to **`langchain-classic`**:

  ```python
  from langchain.chains import LLMChain          # v0.x — no longer resolves
  from langchain_classic.chains import LLMChain  # v1.x
  ```

**Core principles, as they actually operate in v1:**

| Principle                           | What it means in practice                                                                                                                                                                                                      |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Provider abstraction**            | A uniform chat-model interface across ~all providers. Swapping `claude-sonnet-4-6` for a local LM Studio-served model is a one-line change, not a rewrite. This is the single most durable value LangChain has ever delivered. |
| **The agent loop is the primitive** | Call model → model picks tools → execute → repeat until no tool call. Everything else is a hook around that loop.                                                                                                              |
| **Middleware over inheritance**     | Cross-cutting concerns (model routing, summarisation, guardrails, PII handling) attach as `AgentMiddleware` objects rather than subclasses. This is the most important v1 design change for CC-00 — see Finding 8.             |
| **Durable execution**               | State lives in a LangGraph checkpointer, so an agent can be interrupted, persisted, resumed, and time-travelled. Agents survive process death.                                                                                 |
| **Explicit graph topology**         | Multi-agent structure is a declared graph of nodes and edges, not emergent behaviour.                                                                                                                                          |
| **Composability via Runnables**     | LCEL survives as the substrate for non-agentic pipelines and for wiring components together.                                                                                                                                   |

The middleware interface is the mechanism worth understanding, because it is where governance
attaches:

```python
class DynamicModelMiddleware(AgentMiddleware):
    def wrap_model_call(self, request: ModelRequest, handler) -> ModelResponse:
        model = advanced_model if len(request.state.messages) > self.threshold else basic_model
        return handler(request.override(model=model))

agent = create_agent(model=basic_model, tools=tools,
                     middleware=[DynamicModelMiddleware(messages_threshold=10)])
```

`wrap_model_call` receives the request _and_ the downstream handler, so middleware can inspect,
rewrite, short-circuit, retry, or budget every model call. That is structurally the same shape as
CC-00's own `error_boundary.py` and `context_monitor.py` wrap the call — which is why integration is
plausible rather than adversarial.

**Implications:**

- Any LangChain knowledge dated 2023–2024 is **actively misleading** for v1 work. Tutorials
  teaching `LLMChain`, `ConversationChain`, `initialize_agent`, or `AgentExecutor` describe an API
  that no longer resolves from the `langchain` package.
- **The workspace's own RAG documentation is in exactly this stale category.** See Finding 9.

---

### Finding 2: Best practices are mostly about restraint

The dominant failure mode in LangChain projects is not the framework — it is using too much of it.
Synthesising the official guidance with the v1 architecture:

| #   | Practice                                                                               | Rationale                                                                                                                                                                                                                                        |
| --- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | **Start with `create_agent`, drop to raw LangGraph only when the loop no longer fits** | The prebuilt loop covers most agents. Hand-rolling a `StateGraph` on day one buys complexity you have not yet earned.                                                                                                                            |
| 2   | **Pin every package exactly**                                                          | The ecosystem versions independently (`langchain`, `langchain-core`, `langgraph`, `langchain-<provider>`, `langgraph-checkpoint-*`). Unpinned installs drift into incompatible combinations. This is a security requirement too — see Finding 7. |
| 3   | **Put cross-cutting concerns in middleware, not in tools or prompts**                  | Retry, budget, summarisation, and guardrails belong in `wrap_model_call`, where they apply uniformly and can be tested in isolation.                                                                                                             |
| 4   | **Constrain output with schemas, never with prose**                                    | Use structured output / `response_format` rather than asking the model to "reply in JSON". This is also ASGF L1 Mandatory.                                                                                                                       |
| 5   | **Keep tools few, well-named, and narrowly typed**                                     | Tool-selection accuracy degrades sharply as the tool count grows. Descriptions are prompt surface — write them as such.                                                                                                                          |
| 6   | **Always attach a checkpointer for anything multi-turn**                               | Without it there is no durability, no human-in-the-loop, no resume. With it you get all three nearly free.                                                                                                                                       |
| 7   | **Gate irreversible actions with `interrupt()`**                                       | LangGraph's interrupt primitive is the cleanest human-approval mechanism in any agent framework, and it directly satisfies an ASGF L3 Required item.                                                                                             |
| 8   | **Bound the loop** — max iterations, timeouts, tool-call caps                          | Unbounded agent loops are the standard way to burn a token budget at 3am.                                                                                                                                                                        |
| 9   | **Manage context deliberately**                                                        | Use summarisation middleware or trimming before the window overflows, rather than after.                                                                                                                                                         |
| 10  | **Do not wrap what you do not need**                                                   | If the task is one model call with a schema, call the model. LangChain's abstraction tax is only worth paying when you need provider portability, durability, or the agent loop.                                                                 |

**Implications:** practices 3, 4, 6, 7, and 8 map one-to-one onto ASGF requirements. A team
following LangChain's own best practices lands most of the way toward ASGF Conditional without
trying — which is the strongest argument in the framework's favour for this workspace.

---

### Finding 3: The open-source ecosystem is five real projects and one archived one

Retrieved from the GitHub REST API on **2026-07-25**. All figures are exact as of that date, and
all listed repositories are MIT-licensed.

| Project                      | Stars   | Forks  | Status                              | What it is                                                                                                                                                                                                 |
| ---------------------------- | ------- | ------ | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`langchain`**              | 142,575 | 23,735 | Active (pushed 2026-07-25)          | The framework itself. Model/tool/message abstractions, `create_agent`, middleware, ~1,000+ provider integrations.                                                                                          |
| **`langgraph`**              | 38,115  | 6,400  | Active (pushed 2026-07-25)          | The durable-execution orchestration engine underneath. Stateful graphs, cycles, checkpointing, interrupts, time-travel. Usable standalone.                                                                 |
| **`deepagents`**             | 26,797  | 3,752  | Active (created 2025-07-27)         | "The batteries-included agent harness." A pre-wired opinionated agent with a planning tool, a virtual filesystem backend, sub-agent spawning, and context management. Python + a JS twin (`deepagentsjs`). |
| **`open_deep_research`**     | 12,426  | —      | Active (pushed 2026-07-25)          | A reference deep-research agent — multi-step search, synthesis, and report generation. The best-documented worked example in the ecosystem.                                                                |
| **`open-swe`**               | 10,391  | —      | Active (pushed 2026-07-25)          | "An Open-Source Asynchronous Coding Agent." Cloud-style autonomous coding agent built on the stack.                                                                                                        |
| **`langchain-mcp-adapters`** | 3,611   | —      | Active (pushed 2026-07-25)          | Bridges **MCP servers into LangChain tools**. Directly relevant to this workspace — see Finding 10.                                                                                                        |
| **`openwiki`**               | 13,217  | —      | Active                              | CLI that writes and maintains agent-facing documentation for a codebase. Adjacent tooling, not part of the agent runtime.                                                                                  |
| **`langserve`**              | 2,330   | —      | **ARCHIVED** (last push 2026-05-05) | Formerly the "deploy an LCEL chain as a FastAPI REST endpoint" tool. **Do not adopt.**                                                                                                                     |

**Evidence:** each row was fetched individually from `api.github.com/repos/langchain-ai/<name>`;
`langserve`'s response carries `"archived": true`.

**Correction worth recording:** secondary sources retrieved during this investigation still
describe LangServe as a current "deployment tool to host LCEL code as a production-ready API," and
separately dated DeepAgents' launch to March 2026. The GitHub API contradicts both — LangServe is
archived, and the `deepagents` repository was created **2025-07-27**. Where a secondary source and
the vendor's own API disagreed, the API was taken as authoritative.

**The commercial boundary (excluded per CEO constraint):** **LangSmith** (observability,
evaluation, tracing) and **LangGraph Platform / Cloud** (managed deployment, Studio debugger) are
the commercial products. The `langsmith` Python SDK is open source and the tracing protocol can be
pointed at self-hosted alternatives, but the platform is a hosted service. **Excluded from all
recommendations in this report.** The practical consequence is real and should not be minimised:
observability is where LangChain monetises, so the open-source-only path means bringing your own
tracing — OpenTelemetry, or CC-00's existing instrumentation.

---

### Finding 4: LangChain's adoption lead is large and measurable; the "why" is mostly integrations and gravity

**Evidence — same-day GitHub API figures, 2026-07-25:**

| Framework                              | Stars       | Forks  | Relative to LangChain |
| -------------------------------------- | ----------- | ------ | --------------------- |
| **LangChain** (`langchain`)            | **142,575** | 23,735 | —                     |
| CrewAI (`crewAIInc/crewAI`)            | 56,120      | 7,951  | 39%                   |
| LlamaIndex (`run-llama/llama_index`)   | 51,086      | 7,810  | 36%                   |
| LangGraph (`langchain-ai/langgraph`)   | 38,115      | 6,400  | 27%                   |
| DeepAgents (`langchain-ai/deepagents`) | 26,797      | 3,752  | 19%                   |
| Pydantic AI (`pydantic/pydantic-ai`)   | 18,808      | 2,413  | 13%                   |

LangChain alone has **more stars than CrewAI, LlamaIndex, and Pydantic AI combined** (126,014).
Counting the org's agent stack together (`langchain` + `langgraph` + `deepagents` = 207,487) the
gap widens further. Star counts measure attention, not production usage — but at this magnitude the
directional conclusion is safe.

**Evidence — survey (vendor-reported, flag the bias):** LangChain's _State of AI Agents_ report
surveyed 1,340 respondents between 2025-11-18 and 2025-12-02. Headline findings: **57.3%** report
agents running in production (up from ~51% the prior year), another **30.4%** actively developing
with concrete deployment plans; top use cases customer service (26.5%) and research/data analysis
(24.4%); the top production blocker is **quality** (~one third of respondents), with **latency**
second (~20%). This is a vendor surveying a self-selected audience drawn largely from its own
userbase — treat the _trend_ as informative and the _absolute levels_ as optimistic.

**Evidence — named production users (vendor-reported):** LangChain publicly names Uber, LinkedIn,
Klarna, Replit, Elastic, GitLab, Workday, Rakuten, JP Morgan, BlackRock, and Cisco among
LangGraph production users. These are marketing claims from the vendor's own site, not independently
audited deployments; several are corroborated by the companies' own engineering blogs, but this
report did not verify each one.

**Why organisations pick it — the honest reasons:**

1. **Integration breadth is the actual moat.** ~1,000+ pre-built integrations across model
   providers, vector stores, document loaders, and tools. Nobody else is close. The value is not
   that the abstractions are elegant — it is that the connector you need already exists.
2. **Provider portability as vendor-risk insurance.** One-line model swaps mean a provider price
   change, outage, or deprecation is a config edit. For an enterprise this is a procurement
   argument, not a technical one.
3. **LangGraph solved the control problem that made 0.x LangChain distrusted.** The 2023-era
   criticism — opaque abstractions, uncontrollable agent behaviour, impossible debugging — was
   legitimate. LangGraph's explicit graphs, checkpointing, and interrupts answered it directly, and
   that is what unlocked the enterprise deployments above.
4. **Ecosystem gravity.** Largest community, most Stack Overflow answers, most tutorials, best LLM
   familiarity with the API, easiest hiring. Self-reinforcing and rational to weight.
5. **One vendor, whole lifecycle.** Build (LangChain) → orchestrate (LangGraph) → observe
   (LangSmith). Coherent — and also the commercial funnel, which is precisely why the CEO's
   open-source-only constraint matters when evaluating this argument.

**Where competitors legitimately win** — and this report will not pretend otherwise:

| Framework           | Wins when                                                                                                                                                             |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **LlamaIndex**      | The system is fundamentally _retrieval over a large heterogeneous document corpus_. Purpose-built for it; faster to production for pure RAG.                          |
| **CrewAI**          | You want a role/task "crew" running in an afternoon. Materially lower time-to-first-working-agent; teams that bounced off LangChain's learning curve often land here. |
| **AutoGen**         | Research on dynamic, open-ended multi-agent conversation patterns.                                                                                                    |
| **Pydantic AI**     | Strict type safety is the primary requirement and the team already lives in Pydantic. Smallest, cleanest surface of the five.                                         |
| **Semantic Kernel** | Microsoft/.NET enterprise SDK discipline.                                                                                                                             |

**Implications:** LangChain's lead is real but it is a _breadth_ lead, not a quality-per-feature
lead. The rational reading for CC-00: adopt LangChain where breadth is the binding constraint
(provider abstraction, integrations, MCP bridging) and do not adopt it where CC-00 already has a
purpose-built implementation that works.

---

### Finding 5: The measured hardware baseline — ~7.4 GB of free VRAM is the binding constraint

All values measured directly on 2026-07-25.

| Component    | Measured value                                                                                   |
| ------------ | ------------------------------------------------------------------------------------------------ |
| **Machine**  | ASUSTeK Zenbook UX8402VV                                                                         |
| **OS**       | Windows 11 Home China, build 10.0.26200                                                          |
| **CPU**      | Intel Core i9-13900H — **14 cores / 20 threads**, 2.6 GHz base (hybrid P+E)                      |
| **RAM**      | **31.61 GB** LPDDR5-6400, 8 × 4 GB SK Hynix — **soldered, not upgradeable**                      |
| **RAM free** | **~16 GB** free at measurement — i.e. roughly half already committed                             |
| **dGPU**     | **NVIDIA RTX 4060 Laptop** — **8,188 MiB VRAM**, compute capability **8.9** (Ada), driver 610.62 |
| **GPU load** | ~570 MiB / 8,188 MiB used — the resident embedding stack; ~7.4 GB free                           |
| **iGPU**     | Intel Iris Xe (shares system RAM)                                                                |
| **Storage**  | C: 951.7 GB total, **~238 GB free**                                                              |

Software baseline:

| Item                  | Measured                                                                                                                                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Python                | 3.13.5                                                                                                                                                                                                             |
| **PyTorch**           | **`2.13.0+cu130`** — **`torch.cuda.is_available()` → `True`**                                                                                                                                                      |
| transformers          | 5.14.1                                                                                                                                                                                                             |
| sentence-transformers | 5.6.1                                                                                                                                                                                                              |
| qdrant-client         | 1.18.0                                                                                                                                                                                                             |
| Docker                | 29.6.1 — `qdrant-workspace` and `qdrant-memory` both running                                                                                                                                                       |
| Ollama                | 0.23.0 installed — **`ollama list` is empty; zero models pulled**. Measured fact; **not the adopted local-serving tool** — see Recommendations.                                                                    |
| LM Studio             | **Not part of this inventory — presence/version on this machine unverified.** Adopted 2026-07-26 as the local-serving tool for the scoped generation tier; installation is an open precondition, not yet measured. |
| Node.js               | v24.15.0                                                                                                                                                                                                           |
| MCP server env        | Shared venv at `mcp-servers/.venv/`; embedding stack resident on the GPU                                                                                                                                           |
| LangChain             | **not installed** (no `langchain*` package present)                                                                                                                                                                |

**What this baseline means for the deployment question.** The GPU is available and already serving
the embedding stack, which occupies ~570 MiB and leaves roughly **7.4 GB of VRAM free**. That free
capacity — not CPU throughput — is the binding constraint on what else can be hosted locally, and
it is the number Finding 6 reasons against.

**Implications:**

- The soldered 32 GB of system RAM is a real ceiling. Any plan that assumes "just run a big model
  in RAM" is not viable on this machine.
- ~238 GB free disk is comfortable but not unlimited — a handful of Q4 8B models plus embedding
  caches will consume 30–60 GB.
- The embedding stack's GPU residency is a precondition this report builds on, not a subject of it.
  Its configuration and operating rules are documented in `core-component-00/platform/model-context-protocol-servers/CLAUDE.md`
  § Python Environment.

---

### Finding 6: On 8 GB of VRAM, the GPU should serve embeddings — not the agent's brain

The instinctive local-LLM plan is "run an 8B model locally via LM Studio and point LangChain at
it." The arithmetic argues against making that the _primary_ path.

**VRAM budget (8,188 MiB total):**

| Workload                                            | Approx. VRAM (fp16 / Q4_K_M) | Notes                                       |
| --------------------------------------------------- | ---------------------------- | ------------------------------------------- |
| Resident embedding stack (both models)              | **~570 MB** (measured)       | `all-MiniLM-L6-v2` + `all-mpnet-base-v2`    |
| A cross-encoder reranker (e.g. `bge-reranker-base`) | ~560 MB                      | Currently absent — ASGF L4 **Required** gap |
| **Embedding + reranking together**                  | **~1.1 GB**                  | Leaves ~7 GB free                           |
| An 8B model @ Q4_K_M (weights only)                 | ~4.7 GB                      | Llama 3.1 8B / Qwen3 8B class               |
| + KV cache @ 8K context (GQA 8B class)              | ~1.0 GB                      | Grows linearly with context                 |
| **8B model total @ 8K context**                     | **~5.7 GB**                  | Fits — but crowds everything else           |

_(The resident stack is measured on this machine. The reranker and 8B-model rows are standard
published figures for those model classes, not measurements.)_

Both can technically co-reside (~6.8 GB of 8.1 GB). But the decisive argument is not capacity, it
is **what each workload is worth**:

- **Embeddings are called constantly, are latency-critical, and are quality-invariant to hardware.**
  Every RAG query, every memory write, every `search_docs` call. GPU residency here is a pure
  latency win with zero quality cost, and it is already in place — GPU execution measures roughly
  16–21× CPU on batch embedding and ~6.5× on the live query path, with output numerically identical
  to the CPU path.
- **Generation is quality-critical, and an 8B local model is a large quality downgrade.** The
  binding weakness is specifically **tool-calling reliability**, which is the single capability an
  agent loop cannot tolerate being flaky. Retrieved guidance is consistent that dependable tool
  calling starts around the 14B+ class (Qwen3 14B+, Mistral Small 3.1, Llama 4 Scout) and that
  smaller models "do not reliably parse tool schemas." **Those models do not fit in 8 GB at usable
  context lengths.**

An 8B agent that fumbles tool schemas produces malformed calls, retry storms, and silent wrong
answers — expensive failure modes that no amount of local-inference speed compensates for.

**Implications:** the correct allocation is **GPU → embeddings + reranking (permanent residency);
API models → the agent's reasoning and tool selection; local LM Studio-served models → an optional,
explicitly scoped tier** for offline work, privacy-sensitive documents, and cheap bulk
classification where a wrong answer is cheap. This is a deliberate architectural choice, not a
concession.

**Serving mechanism:** LM Studio has no dedicated LangChain partner package (unlike Ollama's
`langchain-ollama`). Reach it through LM Studio's local server (`lms server start`), which exposes
an OpenAI-compatible `/v1` endpoint — wire it up as `langchain_openai.ChatOpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")`.
This is a client-wiring detail only; it does not change the tool-calling-reliability ceiling above.

---

### Finding 7: A live security requirement — pin the LangGraph checkpointer

Check Point Research published (**2026-06-11**) a three-vulnerability chain in LangGraph's
checkpointer implementations that escalates from SQL injection to remote code execution:

| CVE                | Component                     | Nature                                                                                                                                                                       |
| ------------------ | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CVE-2025-67644** | `langgraph-checkpoint-sqlite` | SQL injection — user-controlled keys in the `filter` dict interpolated directly into SQL, permitting `UNION SELECT` injection of malicious serialized payloads               |
| **CVE-2026-28277** | `langgraph` (deserialization) | Unsafe msgpack deserialization — `getattr(importlib.import_module(t[0]), t[1])(t[2])` enables arbitrary function calls (e.g. `os.system`) with attacker-controlled arguments |
| **CVE-2026-27022** | `langgraph-checkpoint-redis`  | SQL/query injection in the Redis checkpoint implementation                                                                                                                   |

**Fixed in:** `langgraph-checkpoint-sqlite` ≥ 3.0.1, `langgraph` ≥ 1.0.10,
`langgraph-checkpoint-redis` ≥ 1.0.2.

**Exploitation preconditions:** self-hosted LangGraph _and_ SQLite/Redis checkpointer _and_ an
exposed `get_state_history()` _and_ an unsanitised user-controlled `filter` parameter.

**Current released versions are already past the fixes** (PyPI, 2026-07-25): `langgraph` **1.2.9**,
`langgraph-checkpoint-sqlite` **3.1.0**. A fresh install today is not vulnerable.

**Implications:**

- The precondition chain requires _user-controlled filter input reaching `get_state_history()`_. A
  local, single-operator workspace deployment does not meet it. **Risk here is low but not zero**,
  and it becomes material the moment any agent surface accepts untrusted input.
- The durable lesson is not this CVE, it is the shape: **the checkpointer is a deserialization
  boundary and a SQL boundary at once.** Any adoption must pin these packages explicitly (best
  practice #2) and treat checkpointer upgrades as security-relevant.
- Under ASGF this belongs in the L3 Harness envelope: checkpoint state is untrusted input to the
  agent runtime and should be validated as such.

---

### Finding 8: ASGF assessment — no inherent Mandatory gaps, several Required gaps

Scored against `agent-systems-governance-framework/governance/compliance-standard.md`. The question
asked is: _if a system were built on LangChain v1 + LangGraph, which requirements does the framework
help satisfy, and which must still be built?_

| Layer              | Framework provides                                                                                                                                                                                                      | Must still be built                                                                                                                                                                                                                                         | Severity if skipped   |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| **L1 Prompt**      | `system_prompt` (role/persona), clean system-vs-task separation, structured output / `response_format` (schema-constrained output)                                                                                      | Behavioural-constraint enumeration; escalation criteria — these are content, not framework                                                                                                                                                                  | P1 (Required)         |
| **L2 Context**     | Summarisation middleware; message trimming; explicit graph state                                                                                                                                                        | **Four-slot structure (System/Retrieved/History/Tool Output) is Mandatory and LangGraph state is free-form** — must be imposed via a typed state schema + middleware; slot priority order; Sacred Context protection; token budget tracked at assembly time | **P0 if not imposed** |
| **L3 Harness**     | `.with_retry()` (exponential backoff), per-call timeouts, explicit tool list (= whitelist), **`interrupt()` for human approval gates — best-in-class**                                                                  | Typed error boundary with distinct Timeout/RateLimit/Validation paths (LangChain's default is closer to catch-all); token budget monitor; tool-call caps; PII scrub on input and scan on output                                                             | P0/P1 mix             |
| **L4 RAG**         | Retriever abstractions; `ContextualCompressionRetriever` for reranking; `langchain-qdrant` vectorstore                                                                                                                  | Embedding-model version pinning; **ACL filtering** (Qdrant payload filters — must be authored); freshness documentation                                                                                                                                     | P1 (Required)         |
| **L5 Multi-Agent** | **Graph topology is explicit and declarative — directly satisfies the Mandatory topology requirement**; `Command(goto=..., update=...)` is a natural Context Handoff Protocol carrier; sub-agent spawning in DeepAgents | Handoff **tier** discipline (Full/Scoped/Minimal) is CC-00's own vocabulary and must be mapped onto `Command`; non-overlapping role enforcement; anti-pattern firewall sections in prompts                                                                  | P1 (Required)         |

**Projected verdict: `Conditional`.**

Per the standard's own criteria — _"No Mandatory gaps. One or more Required gaps with active
remediation plan."_ LangChain introduces **no Mandatory gap that cannot be closed within the
framework**, because middleware and typed graph state give a place to put every Mandatory control.
But it **confers nothing automatically**. The L2 four-slot structure is the sharpest risk: it is
Mandatory, LangGraph's default state is an unstructured message list, and "ad-hoc string
concatenation is not acceptable" is exactly what a naive `create_agent` adoption would produce.

**Two things LangChain does better than CC-00's current implementation, stated plainly:**

1. **`interrupt()` / human-in-the-loop.** ASGF L3 requires high-risk operations to be gated behind
   human approval. LangGraph's durable interrupt — pause mid-graph, persist, resume on approval —
   is a cleaner mechanism than anything currently in `harness-engineering/implementations/`.
2. **Declarative topology.** ASGF L5 makes explicit topology Mandatory. A LangGraph `StateGraph`
   _is_ the topology document — it cannot drift from the implementation, because it is the
   implementation. `swarm_orchestrator.py` describes topology; LangGraph enforces it.

**MCP governance note:** the three-gate inclusion test in `.claude/rules/mcp-governance.md` governs
`.mcp.json` entries. LangChain is a **library**, not an MCP server, so the test does not apply
directly. It _would_ apply if any LangChain-based agent were later exposed as an MCP server, and
Gate 2 (Governance) would need close attention, since an agent that can act is precisely the
category that rule exists to restrain.

---

### Finding 9: The workspace already carries stale LangChain 0.x references

**Evidence:** grep sweep across the repository found LangChain references in 9 files, of which
these are actionable:

| Location                                                           | Issue                                                                                                                                                                                        |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `retrieval-augmented-generation/requirements.txt` (lines 30–31)    | Pins `langchain>=0.1.0`, `langchain-community>=0.0.19`. An open-ended `>=0.1.0` **resolves to 1.3.14 today** — a different, incompatible library from the one the docs were written against. |
| `retrieval-augmented-generation/tools/utility-guide.md:598`        | `from langchain.text_splitter import RecursiveCharacterTextSplitter` — 0.x path                                                                                                              |
| `retrieval-augmented-generation/components/quick-reference.md:232` | Same 0.x import                                                                                                                                                                              |
| `retrieval-augmented-generation/integrations/reference.md:96, 273` | Same 0.x import (two occurrences)                                                                                                                                                            |
| `retrieval-augmented-generation/components/quick-reference.md:180` | `from langchain.retrievers import ContextualCompressionRetriever` — moved to `langchain-classic` in v1                                                                                       |
| `retrieval-augmented-generation/components/quick-reference.md:470` | LangSmith tracing example — **commercial dependency** inside a CC-00 reference doc                                                                                                           |
| `retrieval-augmented-generation/architecture/overview.md:60`       | Names "LangChain/LlamaIndex" as the RAG Orchestrator technology — an architectural claim never realised                                                                                      |

Cross-checked against the v1 migration guide: legacy chains, retrievers, indexing, and `hub` all
moved to `langchain-classic`. The text-splitter import path likewise does not survive as written.

**Mitigating fact:** **none of this is currently executing.** No `langchain*` package is installed,
so these are documentation and dependency-declaration defects, not runtime failures. The RAG
module's own tests do not import LangChain.

**Implications:** the risk is latent but real — anyone running
`pip install -r retrieval-augmented-generation/requirements.txt` today installs LangChain 1.3.14
alongside documentation describing LangChain 0.1, and every code sample in those four files fails on
import. Under ASGF's `canonical-source-of-truth` cross-cutting pattern this is documentation drift
of exactly the kind the pattern exists to prevent. **Severity: P2** — misleading, not breaking,
because nothing depends on it yet.

---

### Finding 10: The strongest integration point is MCP, not RAG

`langchain-mcp-adapters` (3,611 stars, actively maintained) converts MCP servers into LangChain
tools. This workspace already runs two MCP servers that passed the three-gate test —
`workspace-knowledge` and `agent-memory` — plus the shared `embedder-service` behind them.

That means a LangChain agent could consume the _existing, already-governed_ knowledge and memory
infrastructure as tools, **without** re-implementing retrieval in LangChain and **without**
duplicating the embedder. The governance properties that `mcp-governance.md` already established
carry over intact, because the tools are the same tools.

This inverts the obvious integration story. The instinct is "use LangChain for RAG" — but
`retrieval-augmented-generation/` already has `chunker.py`, `retrieval.py` (BM25 + RRF + ACL
filtering), and `pipeline.py`, and the ACL filtering in particular is an ASGF L4 Required item that
CC-00 has and LangChain does not provide out of the box. **Replacing working, compliant CC-00 RAG
with LangChain RAG would trade an ASGF asset for a gap.**

**Implications:** the high-value LangChain surface for this workspace is
`create_agent` + LangGraph orchestration + MCP adapters, sitting _above_ CC-00's existing retrieval
layer — not a rewrite of it.

---

## Analysis

### Interpretation of Findings

The four questions converge on a single reading.

LangChain earned its adoption position through breadth, and repaired its credibility problem
through LangGraph. Both facts are verifiable from primary sources — 142,575 stars versus 56,120 for
the nearest competitor, and a v1 architecture that made durability and explicit topology the
defaults. For a workspace whose governing framework already _requires_ explicit topology and
human-approval gating, that is a genuine alignment, not a coincidence: LangChain and ASGF converged
on the same lessons about agent control, from different directions.

But the adoption question and the deployment question have different answers, and conflating them
would be the error here. **Adoption is a moderate-value, moderate-risk architectural choice.
Deployment is decided almost entirely by the VRAM budget**, which LangChain neither improves nor
worsens — the framework is agnostic to where the models run.

The 8 GB VRAM ceiling forces a genuinely useful discipline. It is too small to host a
tool-reliable agent brain, which removes the temptation to try — and it is far more than enough for
the entire embedding and reranking stack, which is what actually benefits. The resulting
architecture (GPU for retrieval, API for reasoning, local models as an explicit scoped tier) is
better than what an unconstrained machine would have encouraged.

### Trade-offs Identified

| Option                                                    | Agent capability | Hardware fit       | ASGF posture                         | Effort | Recommended                |
| --------------------------------------------------------- | ---------------- | ------------------ | ------------------------------------ | ------ | -------------------------- |
| **Do nothing** — keep CC-00 first-party stack only        | Baseline         | Unchanged          | Current                              | None   | Viable — no new capability |
| **Add LangChain agent layer over existing MCP/CC-00 RAG** | **High**         | **Strong**         | Conditional; gains L3/L5 primitives  | Days   | **Yes — pilot scope**      |
| **Replace CC-00 RAG with LangChain RAG**                  | Neutral          | Neutral            | **Regression** — loses ACL filtering | Weeks  | **No**                     |
| **Local 8B model as primary agent brain**                 | **Degraded**     | Marginal (~5.7 GB) | Worse — unreliable tool calls        | Days   | **No — scoped tier only**  |
| **Adopt LangSmith for observability**                     | High             | N/A                | Strong                               | Low    | **Excluded — commercial**  |

### Risks and Limitations

- **No LangChain benchmarks were executed.** The local-LLM tokens/second figures and the 8B-model
  VRAM rows are estimates from model size and hardware class, not measurements. They are
  directionally reliable and numerically unverified.
- **Vendor-sourced adoption data.** The survey and the customer list both come from LangChain Inc.
  The GitHub and PyPI figures do not, and are the load-bearing evidence.
- **System RAM headroom is tight.** Adding a LangChain process alongside Docker, two Qdrant
  containers, the embedder service, and the editor needs headroom planning against a soldered
  32 GB that is already roughly half committed.
- **Python 3.13.5 is supported** by `langchain` (`>=3.10,<4.0`) and `langgraph` (`>=3.10`), but it
  remains ahead of where much of the integration ecosystem is best-tested. Some
  `langchain-<provider>` packages may lag. _(Assessed from declared metadata; not empirically
  tested.)_
- **The open-source-only constraint has a real cost:** no LangSmith means no turnkey agent tracing.
  For a framework whose top reported production blocker is _quality_, giving up the evaluation
  tooling is a genuine trade-off, and self-hosted OpenTelemetry is more work than it sounds.
- **Framework churn.** LangChain reorganised itself substantially at v1.0. Nothing guarantees v2
  will not do so again.

---

## Recommendations

### Primary Recommendation

> **If LangChain is adopted, adopt it as an agent/orchestration layer above the existing CC-00
> stack, never as a replacement for it.** Specifically: `create_agent` + LangGraph for the loop and
> topology; `langchain-mcp-adapters` to consume `workspace-knowledge` and `agent-memory` as tools;
> CC-00's `retrieval-augmented-generation/` retained as the retrieval implementation. This keeps the
> ACL filtering that ASGF L4 requires and that LangChain does not supply.
>
> The corollary matters as much as the recommendation: **do not replace CC-00's retrieval layer.**
> Doing so would trade a working, ASGF-compliant implementation for a framework that does not
> provide ACL filtering out of the box.

### Secondary Recommendations

1. **Keep the GPU reserved for embeddings + reranking.** The resident stack costs ~570 MB, leaving
   ample room to close the standing **ASGF L4 reranking gap** (`ContextualCompressionRetriever` or a
   direct cross-encoder), which is a Required item currently unmet.
2. **Treat local generation as an explicit, scoped tier — not the default.** **LM Studio** is the
   adopted local-serving tool (decision 2026-07-26); it is not yet installed on this machine and
   installation is an open precondition (unlike Ollama, which is already present with zero models
   pulled — Ollama is not used in this architecture; see Finding 5). Once installed, load a
   Q4_K_M 8B-class model (Qwen3 8B / Llama 3.1 8B) and scope it to offline work, privacy-sensitive
   documents, and cheap bulk classification. **Do not route agent tool-calling through it** — that
   is where sub-14B models fail, regardless of serving tool.
3. **Pin every LangChain-family package exactly, and treat checkpointer versions as security-
   relevant.** Minimum floors from Finding 7: `langgraph>=1.0.10`, `langgraph-checkpoint-sqlite>=3.0.1`,
   `langgraph-checkpoint-redis>=1.0.2`. Current releases already exceed these.
4. **Impose the ASGF four-slot context structure explicitly via a typed LangGraph state schema plus
   middleware.** This is the one Mandatory requirement a naive adoption would miss, and it will not
   emerge on its own.
5. **Correct the stale 0.x references in `retrieval-augmented-generation/` regardless of the
   adoption decision.** Either pin to a v1-compatible constraint and fix the four import samples, or
   remove the dependency declaration entirely if LangChain is not adopted. Leaving
   `langchain>=0.1.0` next to 0.x code samples is documentation drift that will mislead someone.
6. **Plan observability now, not later.** Open-source-only means no LangSmith. Decide on
   OpenTelemetry or CC-00 instrumentation _before_ building, since quality is the most-reported
   production blocker and tracing is how it gets diagnosed.
7. **Do not adopt LangServe** — archived 2026-05-05.

### Implementation Priority

| Recommendation                                                                              | Priority | Effort   | Impact     | Depends on LangChain? |
| ------------------------------------------------------------------------------------------- | -------- | -------- | ---------- | --------------------- |
| Fix stale 0.x LangChain refs in RAG docs + requirements.txt                                 | P2       | 1–2 h    | Medium     | No                    |
| Add cross-encoder reranking (closes ASGF L4 Required gap)                                   | P1       | 0.5 day  | High       | No                    |
| LangChain + LangGraph pilot on a bounded internal task                                      | P2       | 2–3 days | Medium     | Yes                   |
| `langchain-mcp-adapters` bridge to existing MCP servers                                     | P2       | 1 day    | Medium     | Yes                   |
| Typed four-slot LangGraph state schema (ASGF L2 Mandatory)                                  | P1*      | 1 day    | High       | Yes                   |
| Install LM Studio + verify OpenAI-compatible local server (adopted tool, open precondition) | P2       | 0.5 h    | Medium     | No                    |
| Load + evaluate one Q4_K_M 8B model in LM Studio (scoped tier)                              | P3       | 0.5 day  | Low–Medium | No                    |
| Observability plan (OpenTelemetry / CC-00 instrumentation)                                  | P1*      | 1 day    | High       | Yes                   |

\* P1 _conditional on adoption_ — not applicable if LangChain is declined.

### Next Steps

This report is advisory. **No code was changed and no adoption decision has been taken.** Awaiting
CEO/User direction on:

1. Decide whether to authorise a **bounded LangChain pilot**, and if so name the target task.
2. Approve the **stale-reference cleanup** in `retrieval-augmented-generation/`.
3. If adoption proceeds: commission a formal ASGF compliance audit using
   `crew/director/elias-vance/skills/asgf-compliance-audit.md`, and record the decision as an ADR
   under `agent-systems-governance-framework/governance/`.

---

## References

### Internal Documentation

- `core-component-00/framework/00-agent-systems-governance-framework/governance/compliance-standard.md` — the
  per-layer criteria used in Finding 8
- `core-component-00/framework/00-agent-systems-governance-framework/governance/adr-asgf-001.md` — ratifying
  authority
- `core-component-00/framework/04-retrieval-augmented-generation/` — existing RAG implementation
  (`chunker.py`, `retrieval.py`, `pipeline.py`) and the stale references in Finding 9
- `core-component-00/platform/model-context-protocol-servers/_shared/embedder-service/server.py` — the shared embedding service
  a LangChain layer would route through
- `core-component-00/platform/model-context-protocol-servers/CLAUDE.md` § Python Environment — the shared-venv and GPU
  configuration this report treats as a precondition
- `.claude/rules/mcp-governance.md` — three-gate inclusion test; `embedder-service` and
  `agent-memory` history
- `core-component-00/telescope/2026-07-13-mcp-embedder-service-redesign/research-report.md`
- `core-component-00/telescope/2026-07-17-agent-memory-client-instability/research-report.md`

### External Sources

_All retrieved 2026-07-25 unless otherwise noted._

- [LangChain and LangGraph Agent Frameworks Reach v1.0 Milestones](https://www.langchain.com/blog/langchain-langgraph-1dot0)
- [LangChain 1.0 now generally available — Changelog](https://changelog.langchain.com/announcements/langchain-1-0-now-generally-available)
- [LangGraph 1.0 is now generally available — Changelog](https://changelog.langchain.com/announcements/langgraph-1-0-is-now-generally-available)
- `langchain-ai/docs` via Context7 — `releases/langchain-v1.mdx`, `migrate/langchain-v1.mdx`,
  `langchain/runtime.mdx` (v1 architecture, middleware, `langchain-classic` migration)
- GitHub REST API — `langchain-ai/langchain`, `langchain-ai/langgraph`, `langchain-ai/deepagents`,
  `langchain-ai/open_deep_research`, `langchain-ai/open-swe`, `langchain-ai/langchain-mcp-adapters`,
  `langchain-ai/langserve`, `run-llama/llama_index`, `crewAIInc/crewAI`, `pydantic/pydantic-ai`
- PyPI JSON API — `langchain` (1.3.14), `langgraph` (1.2.9), `langgraph-checkpoint-sqlite` (3.1.0)
- [From SQLi to RCE — Exploiting LangGraph's Checkpointer, Check Point Research (2026-06-11)](https://research.checkpoint.com/2026/from-sqli-to-rce-exploiting-langgraphs-checkpointer/)
- [LangChain — State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering)
  _(vendor-reported; n=1,340, surveyed 2025-11-18 → 2025-12-02)_
- [LangChain Deep Agents](https://www.langchain.com/deep-agents) · [Deep Agents overview — Docs](https://docs.langchain.com/oss/python/deepagents/overview)
- [The best AI agent frameworks in 2026 — LangChain](https://www.langchain.com/resources/ai-agent-frameworks)
  _(vendor-authored comparison)_
- [Best open source frameworks for building AI agents in 2026 — Firecrawl](https://www.firecrawl.dev/blog/best-open-source-agent-frameworks)
- [Agentic AI Frameworks Compared 2026 — Knowlee](https://www.knowlee.ai/blog/agentic-ai-frameworks-comparison-2026)
- [LangChain and LangGraph with Ollama: Build Local AI Agents in Python 2026](https://vucense.com/dev-corner/langchain-langgraph-local-agents-python-2026/)
- [Best Local LLMs for 8GB VRAM — LocalLLM.in](https://localllm.in/blog/best-local-llms-8gb-vram-2025)

**Sources evaluated and rejected:** `zipdo.co`, `gitnux.org`, `worldmetrics.org`,
`wifitalents.com` — statistics aggregators with untraceable methodology and mutually inconsistent
figures. See § Knowledge Freshness Disclosure.

---

## Appendices

### Appendix A: Measured Hardware and Software Inventory

Captured 2026-07-25 on `ASUSTeK Zenbook UX8402VV`. Raw command output condensed.

```text
SYSTEM   ASUSTeK COMPUTER INC. Zenbook UX8402VV_UX8402VV
OS       Microsoft Windows 11 Home China — 10.0.26200

CPU      13th Gen Intel(R) Core(TM) i9-13900H
         Cores 14 | Logical 20 | MaxClock 2600 MHz

RAM      Total 31.61 GB | ~16 GB free
         8 x 4 GB SK Hynix @ 6400 MT/s (LPDDR5, soldered)

GPU0     Intel(R) Iris(R) Xe Graphics — driver 32.0.101.7088
GPU1     NVIDIA GeForce RTX 4060 Laptop GPU — driver 32.0.16.1062
nvidia-smi:
  NVIDIA GeForce RTX 4060 Laptop GPU, 8188 MiB total, ~570 MiB used
  (resident embedding stack), driver 610.62, compute_cap 8.9

DISK     C: 951.70 GB total | ~238 GB free

Python                3.13.5
torch                 2.13.0+cu130   <-- cuda_available: True
transformers          5.14.1
sentence-transformers 5.6.1
qdrant-client         1.18.0
Docker                29.6.1  — qdrant-memory (Up), qdrant-workspace (Up)
Ollama                0.23.0  — `ollama list` returns zero models (installed; not the adopted tool)
LM Studio             NOT INSTALLED / NOT MEASURED IN THIS INVENTORY (adopted 2026-07-26; pending)
Node.js               v24.15.0
MCP server env        shared venv at mcp-servers/.venv
langchain / langgraph NOT INSTALLED
```

---

### Appendix B: Proposed Deployment Topology

Conceptual target with an optional LangChain layer. The reasoning and tool tiers are **not
implemented**; the GPU and storage tiers describe the current state.

```text
┌──────────────────────────────────────────────────────────────────────┐
│  REASONING TIER  —  API models (Claude / other)                      │
│  Agent brain: planning, tool selection, synthesis.                    │
│  Rationale: tool-calling reliability is the binding constraint and     │
│  8 GB VRAM cannot host a model that meets it.                         │
└───────────────────────────────┬──────────────────────────────────────┘
                                │  create_agent + LangGraph  (OPTIONAL)
                                │  · explicit graph topology  → ASGF L5
                                │  · interrupt() approval gate → ASGF L3
                                │  · typed 4-slot state       → ASGF L2
                                │  · SQLite checkpointer (pinned ≥3.0.1)
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│  TOOL TIER  —  langchain-mcp-adapters                                 │
│  Existing, already three-gate-approved MCP servers become tools:      │
│    · workspace-knowledge      · agent-memory                          │
│  CC-00 RAG (chunker / retrieval / pipeline) retained — it carries the │
│  ACL filtering that ASGF L4 requires and LangChain does not provide.  │
└───────────────────────────────┬──────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│  GPU TIER  —  RTX 4060, 8188 MiB                                      │
│    all-mpnet-base-v2   (768-dim, workspace-knowledge)   ─┐            │
│    all-MiniLM-L6-v2    (384-dim, agent-memory)          ─┴ ~570 MB    │
│    cross-encoder reranker  [proposed — closes ASGF L4]   ~560 MB      │
│    ───────────────────────────────────────────────────────────       │
│    ~1.1 GB of 8 GB once the reranker is added; ~7 GB free.            │
│                                                                       │
│  OPTIONAL, MUTUALLY EXCLUSIVE WITH HEADROOM:                          │
│    LM Studio 8B @ Q4_K_M  ~4.7 GB + ~1.0 GB KV @ 8K ctx               │
│    (adopted tool; not yet installed — open precondition)              │
│    Scoped tier only — offline / privacy / bulk classification.        │
│    NOT for agent tool-calling.                                        │
└───────────────────────────────┬──────────────────────────────────────┘
                                ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STORAGE TIER  —  Docker (already running)                            │
│    qdrant-workspace          qdrant-memory                            │
└──────────────────────────────────────────────────────────────────────┘
```

---

### Appendix C: VRAM Budget Arithmetic

Total VRAM: **8,188 MiB**.

| Configuration                               | VRAM used | Headroom    | Verdict                                     |
| ------------------------------------------- | --------- | ----------- | ------------------------------------------- |
| Embeddings only (2 models) — current        | ~570 MB   | ~7.6 GB     | Measured; the resident stack is inexpensive |
| Embeddings + cross-encoder reranker         | ~1.1 GB   | ~7.0 GB     | **Recommended steady state**                |
| Above + 8B @ Q4_K_M, 8K context             | ~6.8 GB   | ~1.4 GB     | Fits; tight. Fragmentation risk under load  |
| Above + 8B @ Q4_K_M, 32K context (KV ~4 GB) | ~9.8 GB   | **−1.6 GB** | **Does not fit** — spills to system RAM     |

The last row is the practical ceiling: long-context local generation is not available on this
machine while the embedding stack is resident. _(Only the current-state row is measured. The
reranker and 8B-model figures are standard published sizes for those classes; KV-cache figures
assume GQA 8B-class geometry.)_

---

### Appendix D: Version Floors for Any Future Adoption

Derived from Finding 7 and the PyPI state on 2026-07-25. Recorded for reference only — **no
installation is proposed by this report.**

| Package                       | Security floor | Released as of 2026-07-25 |
| ----------------------------- | -------------- | ------------------------- |
| `langchain`                   | —              | 1.3.14                    |
| `langgraph`                   | **≥ 1.0.10**   | 1.2.9                     |
| `langgraph-checkpoint-sqlite` | **≥ 3.0.1**    | 3.1.0                     |
| `langgraph-checkpoint-redis`  | **≥ 1.0.2**    | not surveyed              |

Python requirement for both `langchain` and `langgraph`: `>=3.10` — satisfied by the local 3.13.5.

---

## Open Questions

1. **How reliable is tool-calling for an 8B Q4_K_M model on real CC-00 tool schemas?**
   - Status: Untested. Finding 6 relies on retrieved general guidance, not local evaluation.
   - Priority: Medium — determines whether the local tier can ever be more than a scoped fallback.

2. **Does the LangGraph `Command(goto=..., update=...)` mechanism cleanly express CC-00's
   three-tier Context Handoff Protocol (Full / Scoped / Minimal)?**
   - Status: Assessed as plausible in Finding 8; not prototyped.
   - Priority: Medium — conditional on adoption.

3. **What is the open-source observability substitute for LangSmith?**
   - Status: Unresolved. OpenTelemetry is the obvious candidate; effort unestimated.
   - Priority: Medium–High if adoption proceeds, given that quality is the top reported blocker.

4. **Are all needed `langchain-<provider>` integration packages Python 3.13-ready?**
   - Status: Core packages declare `>=3.10`. Individual integrations not surveyed.
   - Priority: Low until a specific provider set is chosen.

---

## Addendum — 2026-07-26: Enterprise Examples Deliverable

### Origin

Following completion of the assessment above, the **CEO commissioned enterprise-grade examples and
best practices** for LangChain and its open-source companions, to be produced by Dr. Vance and the
CC-00 lab team. The CEO subsequently ruled that this work is **not a new assessment**; it is a
deliverable of this investigation. It is therefore recorded here rather than as a second report, and
the investigation moved from Simple to Programme shape to hold it.

Everything above this addendum is the original 2026-07-25 assessment and is unchanged.

### What was produced

Eight documents in `supporting/`, covering each adoptable product individually plus one integrated
system:

| Document                                | Covers                                       | Contents                                                                           |
| --------------------------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------- |
| `00-conventions-and-baseline.md`        | —                                            | Pins and CVE floors, environment, CC-00 module loader, **the ASGF governance kit** |
| `01-langchain-examples.md`              | `langchain` 1.3.14                           | `create_agent`, schemas, tools, model routing, **the v0.x cleanup mapping**        |
| `02-langgraph-examples.md`              | `langgraph` 1.2.9                            | Typed four-slot state, checkpointing, `interrupt()`, topology, `Command` handoffs  |
| `03-deepagents-examples.md`             | `deepagents`                                 | Planning, backends, subagents, and the ASGF L5 tension they create                 |
| `04-langchain-mcp-adapters-examples.md` | `langchain-mcp-adapters`                     | Bridging this workspace's two governed MCP servers                                 |
| `05-reference-applications.md`          | `open_deep_research`, `open-swe`, `openwiki` | Dispositions: harvest, observe, evaluate separately; LangServe archived            |
| `06-ecosystem-integration-example.md`   | **all of the above**                         | One end-to-end governed system + a proposed pilot task and acceptance criteria     |
| `07-best-practices-and-asgf-mapping.md` | —                                            | 22 practices, full requirement-by-requirement ASGF map, adoption gate              |

### Verification status

The LangChain v1, LangGraph, DeepAgents, and MCP-adapter API surfaces were **verified live** against
the official `langchain-ai/docs` repository via Context7 on 2026-07-26. CC-00 class names and
signatures, the MCP tool inventory, and `.mcp.json` were verified by direct file read on the same
date.

**No code in the deliverable was executed.** No `langchain*` package is installed in this workspace
(Finding 5, still true). Every example is unexecuted reference code written against a verified API
surface — a credible starting point, not working software. This is labelled at the top of every
supporting document and must not be softened when the material is reused. Three `create_deep_agent`
parameters (`skills`, `memory`, `permissions`) had their signature verified but **not** their
semantics; the reference applications' source was not read, and patterns attributed to them are
labelled as inferred.

### Principal engineering result: the ASGF governance kit

Finding 8 above established that LangChain confers no ASGF compliance but provides places to attach
it. Building against the API turns that into a concrete, reusable artefact: **six middleware classes
that close nine ASGF requirements — six of them Mandatory — by delegating to CC-00 implementations
that already exist and are already tested** (`supporting/00 §7`).

| Middleware                     | Delegates to                                       | Closes                          |
| ------------------------------ | -------------------------------------------------- | ------------------------------- |
| `FourSlotContextMiddleware`    | `context_assembler.ContextAssembler`               | 3 Mandatory (L2) + 1 Required   |
| `TokenBudgetMiddleware`        | `context_monitor.TokenBudgetManager`               | 1 Mandatory (L3)                |
| `TypedErrorBoundaryMiddleware` | `error_boundary.CircuitBreaker` + typed exceptions | 3 Mandatory (L3)                |
| `ToolGovernanceMiddleware`     | `tool_registry.ToolRegistry`                       | 2 Required (L3)                 |
| `PIIMiddleware`                | — (new; no CC-00 equivalent)                       | 2 Required (L3)                 |
| `ObservabilityMiddleware`      | — (OpenTelemetry)                                  | replaces the excluded LangSmith |

The controls stay in CC-00 where they are tested; the middleware is thin glue. **Middleware ordering
is load-bearing and non-obvious** — `FourSlotContextMiddleware` must be innermost, because anything
that rewrites messages after the assembler silently destroys a Mandatory guarantee. That is the most
likely way for a correct-looking adoption to be non-compliant.

### Finding 11: CC-00's four module roots collide on the package name `implementations`

**A CC-00 packaging gap, not a LangChain problem** — and it blocks any multi-layer integration.

**Evidence:** static inspection on 2026-07-26 found all four module roots exposing a directory named
`implementations/`. CC-00's own test suites place **one** module root on `sys.path` and import
`from implementations.<module>`, which is why `core-component-00/CLAUDE.md` warns against running all
four suites in one process. A LangChain agent legitimately needs L2, L3, L4, and L5 code resident
simultaneously; the convention cannot express that. The modules are also not uniform — seven files
are stdlib-only, three use relative imports (`handoff_packet`, `swarm_orchestrator`, `pipeline`), and
`memory_store` uses the absolute form `from implementations.reflection_authoring import …`. Only
`multi-agent-engineering/implementations/` has an `__init__.py`.

**Implications:** an alias loader (`supporting/00 §6`) makes integration possible today and is
labelled a workaround. The durable fix is to publish the four module roots as one installable `cc00`
package with distinct subpackage names — independent of LangChain, and it would also unblock
single-process test runs.

### Finding 12: Bridging this workspace's MCP servers naively ships two hazards

Finding 10 identified MCP as the strongest integration point; that stands. But
`MultiServerMCPClient.get_tools()` returns one flat list, and this workspace's two servers do not
compose cleanly into one.

**Evidence** (direct read of both `server.py` files, 2026-07-26):

1. **Name collision** — `workspace-knowledge` and `agent-memory` **both** define `health_check`.
2. **Write-capable tools** — `workspace-knowledge` exposes `rebuild_index()` and
   `upsert_document(file_path)`. Both correctly passed Gate 2 of the inclusion charter, but that gate
   was passed **for a human-supervised Claude Code session**. An agent calling `rebuild_index()` in
   an unobserved loop is a different risk profile.

**Implications:** bridged tool lists need a governance pass — namespace collisions, drop or gate
write-capable tools, and fail loudly on any _new_ collision, since that means a server changed.
**The general principle worth recording in `mcp-governance.md`: the three-gate test evaluates a
server for the context in which it was gated. Re-exposing a gated server to an unattended agent is a
new governance question, not an inherited answer.**

### Finding 13: `agent-memory`'s graceful degradation becomes a confident-wrong-answer mode under an agent

`search_memory` never raises; on any failure it returns an empty result with `degraded=True` and a
`reason`. That is correct server design and is why a stalled embedder never blocked a tool call
during the 2026-07-13 and 2026-07-17 investigations.

**Evidence:** in a human-driven session a `degraded: true` field is visible and a human notices. In
an agent loop **nothing reads it unless something is written to read it**, and an empty result is
semantically indistinguishable from "no prior context exists".

**Implications:** an agent whose memory backend is down concludes there is no prior context and
proceeds confidently — a wrong answer at full confidence with no error in the logs.
`MCPDegradationMiddleware` (`supporting/04 §4`) injects an explicit notice so the model treats
degraded output as _unknown_ rather than _absent_. This generalises: **graceful degradation and
autonomous agent consumption are in tension by default.**

### Finding 14: ACL identity must be closure-bound, never a tool parameter

**Evidence:** `RAGPipeline.query(query, user_role="public")` takes the ACL role as an argument — this
is CC-00's L4 Required control. The natural LangChain wrapping exposes `user_role` as a `@tool`
parameter. **That wrapping is a privilege-escalation vector:** tool parameters are model-chosen, so
the model can pass `"admin"` and `acl_filter` will correctly honour it. Prompt injection escalates
directly to unauthorised retrieval.

**Implications:** bind the role in a closure at agent-construction time, from the authenticated
session (`supporting/04 §5`). **General rule: any parameter constituting an authority claim must be
bound outside model control.** The same applies to `thread_id`, which is a capability to resume and
read another conversation's state.

This is the one finding where the _obvious_ implementation is actively dangerous rather than merely
non-compliant. A missing token budget degrades gracefully; a model-chosen ACL role does not.

### Finding 15: DeepAgents' dynamic sub-agent spawning conflicts with an ASGF Mandatory requirement

ASGF L5 states that topology "is documented before implementation" and that "emergent topology
without design intent is not acceptable". An agent that spawns subagents at its own discretion is
emergent topology by construction.

**Implications:** constrain rather than reject. Enumerate every subagent statically so the
`subagents=[…]` list _is_ the topology document; bound each subagent's tools to a subset of the
parent's so delegation cannot escalate authority; and record the decomposition as a reviewed table.
With those, delegation is a _declared_ hierarchy dispatched dynamically, which satisfies the
requirement. A secondary consequence: composing DeepAgents' individual middleware into a plain
`create_agent` is often preferable to `create_deep_agent`, because an ASGF audit must answer "what
touches the context window, in what order" — a list answers that, a bundle does not.

### Finding 16: The open-source-only constraint has two costs, differing by an order of magnitude

The assessment above recorded this as one item ("no turnkey agent tracing"). Building the examples
separates it:

| Lost capability                                                       | Substitute                                                     | Effort       |
| --------------------------------------------------------------------- | -------------------------------------------------------------- | ------------ |
| Tracing — what happened in this run                                   | OpenTelemetry middleware + LangGraph checkpoint-history replay | ~1 day, done |
| **Evaluation — datasets, regression tracking, is-this-getting-worse** | **none identified**                                            | **unscoped** |

**Implications:** tracing is genuinely solved by the examples, and checkpoint history is a bonus that
answers "what happened" better than a trace alone. **Evaluation is not solved and should not be
presented as though it were.** For a framework whose top reported production blocker is _quality_,
that is the most significant open cost of the constraint and deserves its own scoping.

### Supplementary recommendations

These extend, and do not replace, the Recommendations section above.

1. **Adopt the governance kit as the unit of adoption, not LangChain as a whole.** If a pilot is
   authorised, build `supporting/00 §7`'s kit first, promoted into real CC-00 code with a real test
   suite — it is what makes every subsequent agent compliant by default rather than by diligence.
2. **Fix the CC-00 `implementations` collision (Finding 11).** No LangChain dependency.
3. **Record the MCP re-exposure principle in `.claude/rules/mcp-governance.md` (Finding 12).** No
   LangChain dependency.
4. **Scope evaluation tooling as its own piece of work (Finding 16).**
5. **If a pilot is authorised, the telescope research assistant in `supporting/06` is proposed as the
   named target task** that § Next Steps item 1 asks for, with pre-committed acceptance criteria.

### Implementation priority (addendum)

| Recommendation                                      | Priority | Effort   | Impact | Depends on LangChain adoption? |
| --------------------------------------------------- | -------- | -------- | ------ | ------------------------------ |
| Close the L4 reranking gap (Recommendation 1 above) | **P1**   | 0.5 day  | High   | **No**                         |
| Fix the CC-00 `implementations` collision           | P2       | 0.5 day  | Medium | **No**                         |
| Stale 0.x cleanup (Recommendation 5 above)          | P2       | 1–2 h    | Medium | **No**                         |
| Record the MCP re-exposure principle                | P2       | 1 h      | Medium | **No**                         |
| Promote the governance kit to tested CC-00 code     | P1\*     | 2–3 days | High   | Yes                            |
| Telescope research assistant pilot                  | P2\*     | 3–5 days | Medium | Yes                            |
| Evaluation-tooling scoping study                    | P1\*     | 1 day    | High   | Yes                            |

\* Conditional on adoption.

**The top four rows carry no LangChain dependency.** If the adoption decision stalls indefinitely,
they remain worth doing and would leave the workspace better off regardless. **Closing the L4
reranking gap is the single highest-value action arising from this entire line of work** — it is the
only Required gap standing between the demonstrated architecture and full compliance, and it costs
half a day.

### Additional open questions

5. **Does the CC-00 middleware stack compose correctly with DeepAgents' own context management?**
   - Status: Unresolved — undeterminable without execution. First-run shakedown item #1.
   - Priority: **High** — a silent failure here breaks an ASGF Mandatory guarantee.
6. **Should CC-00's module roots be published as one installable package?**
   - Status: Recommended (Finding 11), not scoped. Priority: Medium.
7. **What is the open-source evaluation story for agent quality?**
   - Status: Unsolved (Finding 16). Note this supersedes open question 3 above in part: tracing is
     now answered (OpenTelemetry, ~1 day); evaluation is not. Priority: High.
8. **Are DeepAgents' `memory=` entries compressible, and does `permissions=` constrain subagents?**
   - Status: Unverified. If `memory=` is compressible it is **not** a substitute for CC-00 sacred
     context. Priority: Medium.
9. **What does human review look like when an agent produces more diff than a person can read?**
   - Status: Unsolved; blocks any coding-agent adoption (`supporting/05 §2`). Priority: Medium.

### Scope discipline

The addendum changes no workspace code. The stale-reference cleanup identified in Finding 9 and
Recommendation 5 **remains unperformed** and still awaits direction; `supporting/01 §6` provides the
file-by-file mapping for when it is authorised. No adoption decision is taken or implied.

### Runnable Companion — 2026-07-27

Per CEO direction, a runnable, enterprise-grade project now accompanies the Markdown examples above:
**`supporting/enterprise-examples/`** — an installable Python package implementing the
ASGF governance middleware kit (§ Addendum above) and a working version of the telescope research
assistant (`supporting/06`), with a real pytest suite (25 tests) that was actually run. **Placement
corrected 2026-07-27:** initially placed at `core-component-00/examples/langchain-ecosystem-reference/`;
the CEO clarified this is a research output of this investigation, not a standalone CC-00 lab
deliverable, and it was relocated into this investigation's `supporting/` folder the same day — see
Version History v1.3. **Renamed same day, also per CEO direction:** the folder name
`langchain-ecosystem-reference` risked being read as another Markdown reference document sitting
among the seven `*-examples.md` files, rather than as the one runnable, executable artefact — renamed
to `enterprise-examples` to make both properties (runnable, and the answer to the CEO's original
"enterprise-grade examples" request) legible from the name itself. See Version History v1.4. See that
project's own `README.md` for the exact, honest boundary between what was executed (the governance
mechanics, CC-00 integration, LangGraph durability/interrupt primitives, and ACL filtering — all
real) and what was not (live model reasoning quality, since no Anthropic/OpenAI API key was
available; MCP-server bridging; DeepAgents usage).

Building runnable code surfaced two integration bugs that the Markdown-only deliverable could not
have found by construction, both fixed in code and documented in
`src/cc00_langchain/asgf.py`'s module docstring: CC-00's `ContextAssembler` output is not
LangChain-message-valid once tool output is present (`KeyError: 'tool_call_id'`), and
`create_agent`'s default `AgentState` silently drops any state key it does not declare — so
`sacred_context` / `retrieved` / `tool_outputs` never reached middleware without a custom
`state_schema`. This is recorded here as a pointer, not folded into the Findings/Addendum numbering
above, per the same "deliverable of this investigation, not a new assessment" scoping this report
already applies to the 2026-07-26 examples.

This note does not change the projected `Conditional` verdict, the pending pilot-adoption decision,
or the unperformed stale-reference cleanup — all remain as stated above.

### Cookbook — 2026-07-27

A third, separate CEO-commissioned deliverable: `supporting/cookbook/` — one enterprise adoption
manual (introduction, usage with commented examples, alternatives with rationale, integrations) per
LangChain open-source product **not** already covered by `supporting/01` (LangChain) and
`supporting/02` (LangGraph); those two are referenced via a table in `cookbook/README.md` rather than
duplicated. Manuals cover DeepAgents and `langchain-mcp-adapters` (both live-executed in this
session — a real `create_deep_agent(...)` run and a real MCP server bridged and called), Open Deep
Research, Open SWE, and openwiki (all three: GitHub metadata only, source not read, usage sections
explicitly flagged unverified), and LangServe (archived — redirection only, no usage section). See
`cookbook/README.md` for the full manual index and per-manual verification status. This note does
not change anything stated above.

**Revised same day, per CEO/user feedback:** the reference-table approach for LangChain and LangGraph
above was reversed. Two additional standalone manuals — `01-langchain.md` and `02-langgraph.md` —
were written directly into the cookbook, and the six existing manuals were renumbered `03`–`08` to
make room ahead of them. The cookbook is now eight self-contained manuals covering every product in
the ecosystem inventory, none of them a reference table pointing elsewhere. See Version History v1.6.

### Consolidation — 2026-07-27

The eight documents described in § What was produced above (originally sitting loose directly in
`supporting/`) were consolidated into their own subfolder, **`supporting/workspace-integration-examples/`**,
per CEO direction — naming their purpose explicitly rather than leaving them as undifferentiated
loose files alongside `enterprise-examples/` and `cookbook/`. The name was chosen over several
alternatives (`examples/`, `reference-examples/`, `integration-examples/`) to name what these eight
documents actually verify: that the ecosystem wires into **this workspace's own** CC-00 modules,
governed MCP servers, and ASGF governance kit — not generic LangChain usage. All internal
cross-references between the eight files, from `cookbook/` (six manuals), from
`supporting/enterprise-examples/` (`README.md` and `src/cc00_langchain/asgf.py`), and from
`supporting/README.md` were updated to the new path; verified via a full repository grep sweep that
no stale reference to the old flat `supporting/0N-*.md` paths remains outside this report's own
unchanged pre-2026-07-27 prose (which is preserved verbatim below per the append-only rule). See
Version History v1.7.

### Independent verification harness — 2026-07-27

Following a CEO/user exchange about testing the `workspace-integration-examples/` files directly
(Markdown itself is not executable, and merging that folder into `enterprise-examples/` was
explicitly rejected as unwise — it would have collapsed two deliberately separate deliverables
into one), the CEO approved building **`workspace-integration-examples/verification/`**: a fully
independent test project (its own `pyproject.toml`, `requirements.txt`, `.venv`, `tests/`) proving
the standalone claims in `01-langchain-examples.md`, `02-langgraph-examples.md`, and
`03-deepagents-examples.md` with 13 real, passing tests, no API key required, and no import from
or shared venv with `enterprise-examples/`. Dr. Vance owned this work directly.

**What it proved:** a tool-bearing `create_agent` accepting declared extra state keys and
`ToolStrategy`'s `Literal`-field enforcement (`01`); `sacred_context`'s append-only reducer,
checkpoint thread-ID isolation as a security boundary, a hierarchical `Command` topology, and
handoff-tier construction invariants (`02`); and `create_deep_agent` itself — not a hand-rolled
graph — running end to end with a static named subagent roster, `StateBackend`, a checkpointer,
and gated writes (`03`).

**A real finding, not anticipated going in:** `deepagents`'s `FilesystemBackend` defaults to
`virtual_mode=False`, under which a `..` path segment escapes its declared `root_dir` entirely —
directly contradicting `03-deepagents-examples.md`'s Example 3 claim that "root_dir is the whole
confinement boundary." Reproduced with a dedicated test, then corrected: the source document's
code block and rules table now require `virtual_mode=True` explicitly, and its Status line records
the finding.

`00`, `04`, and `06` were deliberately not re-tested here — their patterns are already proven
inside `enterprise-examples/`, and duplicating that work inside a second project would have
reintroduced the same merge-by-another-name the CEO rejected. `05` and `07` were also left out,
not by oversight: neither contains a standalone runnable claim of its own to execute. Every file's
own Status line and `workspace-integration-examples/README.md`'s file table now state which of
these three categories it falls into — no file is left silently unaddressed. See Version History
v1.8.

### Complete fix — 2026-07-27

The CEO required a **complete** fix for the `FilesystemBackend` `virtual_mode=False` finding
above, and reaffirmed that CC-00 Laboratory owns this workspace's LangChain research work in
full. A grep sweep of the entire `supporting/` tree (`workspace-integration-examples/`,
`enterprise-examples/`, `cookbook/`) for every `FilesystemBackend(` construction site found one
additional, unfixed occurrence: `cookbook/03-deepagents.md` (line 196) — an independently-authored
manual that predates, and was never touched by, the `verification/` work. It carried the identical
hazard and has now been corrected the same way (`virtual_mode=True` passed explicitly, with an
inline note citing the verified finding). `enterprise-examples/` does not construct
`FilesystemBackend` anywhere (its flagship graph uses `StateBackend`) and required no change.

To harden against recurrence rather than leave this as a one-off correction, the hazard was also
promoted into `07-best-practices-and-asgf-mapping.md`'s permanent record: a new anti-pattern
(rank 4, inserted ahead of the existing lower-ranked items, with a footnote marking it as the one
row in that table verified by execution rather than projected) and a correction to existing
practice #18, which previously implied `root_dir` alone was sufficient confinement. Both
`cookbook/README.md`'s verification table and `03-deepagents-examples.md`'s own Status line were
updated to point to the completed fix. `workspace-integration-examples/verification/`'s full
13-test suite was re-run after every change and remains 13/13 passing — the fix required no code
changes, only documentation, since the workaround (`virtual_mode=True`) was already correct.

**Scope of "complete," stated precisely:** complete within this workspace's own documents and
example code — every known construction site in `supporting/` now passes `virtual_mode=True`. Not
complete in the sense of patching the `deepagents` library itself, which still defaults to the
insecure `virtual_mode=False`; that remains an upstream fact outside CC-00's control, and
`test_filesystem_backend_virtual_mode_false_allows_path_escape` exists specifically to keep
re-confirming it stays true. See Version History v1.9.

### Crew review — 2026-07-27

Per CEO direction, Dr. Vance convened the relevant CC-00 crew — the four module leads (Zhao,
Asante, Almeida, Farouk) plus Dr. Wieczorek (Safety & Evaluation) and Ravi Deshmukh
(Infrastructure) — to independently re-check this investigation's claims against the underlying
records, not against prior summaries of them. Full record:
`2026-07-27-crew-review.md` (sibling to this report, following the workspace's
`templates/review-records/final-review.md` shape). All six reviewers confirmed their module's
claims hold up under direct re-checking; three non-blocking open items were named (an
`ContextAssembler`-usage follow-up, an untested DeepAgents/harness retry interaction, and the
lab's pre-existing lack of CI-for-research automation), and one already-disclosed tension
(DeepAgents' dynamic sub-agent spawning vs. ASGF L5) was reaffirmed as a workaround, not a
resolution. Dr. Wieczorek independently reproduced the `FilesystemBackend` finding rather than
taking the prior fix on trust. See Version History v1.10.

### Closure — 2026-07-28

Per CEO direction — this investigation has been primarily exploratory in nature, and the CEO
requested a findings report to confirm it is successfully completed — this section closes out
`2026-07-25-langchain-ecosystem-assessment` as a research study. It does not reopen or extend the
work; the Status field already read `Complete — advisory` as of 2026-07-27 and remains so. This is
a synthesis for sign-off, not new investigation.

**What was asked and what was delivered.** The original charge was to assess LangChain v1
architecture, ecosystem adoption, and local-deployment feasibility on this workspace's own
hardware and governance stack (Findings 1–10), which the CEO twice extended same-week into
executable proof: a runnable governance-kit companion (`enterprise-examples/`, 25 tests), an
eight-manual adoption cookbook (`cookbook/`), workspace-specific integration references
(`workspace-integration-examples/`, 8 documents, 6 now execution-backed), a security-hardening
pass (Findings 11–16 plus the `FilesystemBackend` finding), and an independent crew review
(6 reviewers, all confirmed). Every extension is recorded in this report's own Version History
(v1.1–v1.10) — nothing here is asserted without a version row backing it.

**The exploratory question is answered.** LangChain v1 is architecturally sound for this
workspace as an agent/orchestration layer _above_ the existing CC-00 stack — never a replacement,
since CC-00's ACL filtering is an ASGF L4 Required item LangChain does not itself supply (Finding
8, Finding 14). Projected ASGF verdict: **Conditional** — no inherent Mandatory gaps, several
Required gaps, all closeable with the governance kit already built and tested. The binding
constraint is local hardware, not the framework (Finding 5–6). Two real defects were found only by
executing code, not by reading documentation — both worked around, both honestly attributed to
their true origin (one CC-00's own, one LangChain's intended strict behavior; neither a LangChain
defect to report upstream) — and one additional real security finding (`FilesystemBackend`
confinement) was found, fixed everywhere it appeared in this workspace, and hardened against
recurrence in the permanent anti-pattern catalogue.

**What stays explicitly open, not smoothed over.** Three items the crew review logged as
non-blocking (a `ContextAssembler`-usage follow-up, an untested DeepAgents/harness retry
interaction, the lab's pre-existing lack of CI-for-research automation); one governance tension
correctly disclosed rather than resolved (DeepAgents' dynamic sub-agent spawning vs. ASGF L5); and
the CE-side `tool_call_id` gap in `context_assembler.py`, whose fix is deferred per CEO direction
while this investigation stays focused on LangChain itself — deferred, not deleted; still fully
documented in `asgf.py`'s docstring and `enterprise-examples/README.md`.

**Distinct from this closure: broader LangChain pilot-adoption remains its own, separate business
decision**, not automatically resolved by the research being complete. The research answers
_whether LangChain is sound to build on here_; it does not itself commit the lab to building a
production pilot on it. That decision, if and when the CEO wants it, is a new charge — not
something this closure section decides on the CEO's behalf.

**Status confirmed:** `Complete` (telescope four-state lifecycle) — was already correctly set,
verified against `telescope/README.md`'s index entry, no change required. See Version History
v1.11.

---

## Version History

| Version | Date       | Author                                       | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------- | ---------- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-07-26 | CC-00 Laboratory (Director: Dr. Elias Vance) | Reorganized for clarity per CEO direction. LM Studio adopted as the local-serving tool for the scoped local-generation tier, replacing Ollama in that role throughout Findings 1/5/6, Recommendations, and Appendices A/B. LM Studio's installation on this machine remains an open, unverified precondition (Finding 5); Ollama remains installed but is not the adopted tool.                                                                                                                                                                                                                                                                                                                                             |
| 1.1     | 2026-07-26 | CC-00 Laboratory (Director: Dr. Elias Vance) | Enterprise examples deliverable folded in per CEO ruling that it is **not a new assessment**. Investigation moved from Simple to Programme shape: added `supporting/` with 8 example documents. Added § Addendum — 2026-07-26 recording the governance-kit result, **Findings 11–16**, supplementary recommendations, and open questions 5–9. Findings 1–10, Analysis, and Recommendations are unchanged.                                                                                                                                                                                                                                                                                                                   |
| 1.2     | 2026-07-27 | CC-00 Laboratory (Director: Dr. Elias Vance) | Added `supporting/README.md` (index of the 8 example documents) and a pointer to a new runnable companion project (25 real pytest passes, no API key). See § Runnable Companion — 2026-07-27. No prior content changed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 1.3     | 2026-07-27 | CC-00 Laboratory (Director: Dr. Elias Vance) | **Placement correction, same day.** CEO directed that the runnable companion project is a research output of this investigation, not a standalone CC-00 lab deliverable — relocated from `core-component-00/examples/langchain-ecosystem-reference/` to `supporting/langchain-ecosystem-reference/`. Reinstalled and re-ran the full pytest suite from the new location (25/25 passing, unchanged) before treating the move as complete. `core-component-00/CLAUDE.md`'s "Where to Look" table entry for the old location was removed.                                                                                                                                                                                      |
| 1.4     | 2026-07-27 | CC-00 Laboratory (Director: Dr. Elias Vance) | **Rename, same day, per CEO direction.** `supporting/langchain-ecosystem-reference/` → `supporting/enterprise-examples/`. Raised as a naming-ambiguity concern: "reference" read as another Markdown document among the seven `*-examples.md` files rather than as the one runnable artefact, and the old name did not signal "enterprise-grade examples" — the CEO's original framing — at all. Updated internal package metadata (`pyproject.toml` project name, `__init__.py` version lookup) and every cross-reference in this report and in `supporting/README.md` / `telescope/README.md`. Re-ran the full pytest suite from the renamed directory (25/25 passing, unchanged) before treating the rename as complete. |
| 1.5     | 2026-07-27 | CC-00 Laboratory (Director: Dr. Elias Vance) | **New deliverable, same day, per CEO direction.** Added `supporting/cookbook/` — six enterprise adoption manuals (DeepAgents, `langchain-mcp-adapters`, Open Deep Research, Open SWE, openwiki, LangServe) plus an index that references `supporting/01`/`02` for LangChain/LangGraph instead of duplicating them. DeepAgents' and `langchain-mcp-adapters`' manuals include live-executed examples (a real `create_deep_agent(...)` invocation and a real bridged MCP server call, both run in this session); the three reference-application manuals and the archived-product manual are explicitly labelled as sourced from GitHub metadata only, source code not read. See § Cookbook — 2026-07-27.                     |
| 1.6     | 2026-07-27 | CC-00 Laboratory (Director: Dr. Elias Vance) | **Correction, same day, per CEO/user feedback.** The v1.5 reference-table approach for LangChain/LangGraph was reversed -- reference tables that just point elsewhere were judged to defeat the purpose of a self-contained manual. Wrote `01-langchain.md` and `02-langgraph.md` directly, extracting and rewriting the relevant content as original manual prose with no provenance commentary, and renumbered the six existing manuals `03`-`08` to make room. `cookbook/README.md` rewritten to drop the reference table and list all eight manuals.                                                                                                                                                                    |
| 1.7     | 2026-07-27 | CC-00 Laboratory (Director: Dr. Elias Vance) | **Consolidation, same day, per CEO direction.** The eight loose documents in `supporting/` were moved into a new subfolder, `supporting/workspace-integration-examples/`, named for their actual purpose (verifying the ecosystem integrates with this workspace's own modules, MCP servers, and governance kit). All cross-references from `cookbook/`, `enterprise-examples/`, and `supporting/README.md` updated; a full grep sweep confirmed no stale references to the old flat paths remain. See § Consolidation -- 2026-07-27.                                                                                                                                                                                       |
| 1.8     | 2026-07-27 | CC-00 Laboratory (Director: Dr. Elias Vance) | **Independent verification harness, same day, per CEO approval.** Added `supporting/workspace-integration-examples/verification/` -- a standalone test project (own venv, no import from `enterprise-examples/`) proving `01`, `02`, and `03`'s claims with 13 real, passing tests. Surfaced a real finding: `deepagents`'s `FilesystemBackend` defaults to `virtual_mode=False`, letting `..` escape `root_dir`; `03-deepagents-examples.md` corrected in place. `00`/`04`/`06` intentionally not re-tested (already proven in `enterprise-examples/`); `05`/`07` intentionally left untested (no standalone runnable claims). See § Independent verification harness -- 2026-07-27.                                       |
| 1.9     | 2026-07-27 | CC-00 Laboratory (Director: Dr. Elias Vance) | **Complete fix, same day, per CEO requirement.** Grep-swept all of `supporting/` for `FilesystemBackend(` construction sites; found and fixed one additional unfixed occurrence in `cookbook/03-deepagents.md`. Hardened against recurrence: added anti-pattern rank 4 (execution-verified, footnoted) to `07-best-practices-and-asgf-mapping.md` and corrected practice #18's wording. Updated `cookbook/README.md`'s verification table. `verification/`'s 13-test suite re-confirmed passing throughout. See § Complete fix -- 2026-07-27.                                                                                                                                                                               |
| 1.10    | 2026-07-27 | CC-00 Laboratory (Director: Dr. Elias Vance) | **Crew review, same day, per CEO direction.** Convened the four module leads plus Safety & Evaluation and Infrastructure to independently re-check this investigation's claims against underlying records. All confirmed; three non-blocking open items logged; one tension (DeepAgents vs. ASGF L5) reaffirmed as disclosed, not resolved. Full record: `2026-07-27-crew-review.md`. See § Crew review -- 2026-07-27.                                                                                                                                                                                                                                                                                                      |
| 1.11    | 2026-07-28 | CC-00 Laboratory (Director: Dr. Elias Vance) | **Closure, per CEO direction.** The CEO characterized this work as primarily exploratory and requested a findings report confirming successful completion. Added a closure synthesis covering what was asked/delivered, the exploratory question's answer (Conditional ASGF verdict, LangChain as a layer above CC-00, not a replacement), what stays explicitly open (three non-blocking items, one disclosed tension, one deferred CE-side gap), and an explicit note that broader pilot-adoption remains a separate, still-open business decision. Status confirmed Complete, no change required. See § Closure -- 2026-07-28.                                                                                           |

---

**Report Status:** Complete — advisory. The local-serving tool for the scoped local-generation tier
is decided: **LM Studio**, replacing Ollama in that role, per CEO decision 2026-07-26 (Finding 6,
Recommendations, Appendices A/B). No workspace code has been modified, LM Studio has not yet been
installed on this machine (open precondition, Finding 5), and the broader question of whether to
pilot LangChain itself remains undecided. Awaiting CEO/User direction per § Next Steps.

The CEO-commissioned **enterprise examples deliverable** is folded into this report as
§ Addendum — 2026-07-26, with the examples themselves in `supporting/`. Per the CEO's ruling it is a
deliverable of this investigation, **not a separate assessment** — this remains the single canonical
LangChain assessment report. All example code in `supporting/` is **unexecuted**.

**Scope note:** this report assesses LangChain only. The state of the local Python and GPU
environment is treated as a **precondition** — a fact the deployment analysis reasons against, not
a subject of this research. That environment is documented in
`core-component-00/platform/model-context-protocol-servers/CLAUDE.md` § Python Environment.
