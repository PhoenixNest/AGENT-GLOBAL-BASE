# Open Deep Research — Enterprise User Manual

**Repository:** `langchain-ai/open_deep_research` · **Stars:** 12,426 (2026-07-25) · **Status:** Active
(pushed 2026-07-25)
**Verification status:** GitHub metadata only (stars, description, activity, retrieved via the
GitHub REST API on 2026-07-25 by the parent assessment). **The repository's source code was not
read** and the application was not installed or run in this session. Everything below is scoped
accordingly: architectural and adoption analysis is presented with normal confidence; anything about
specific commands, configuration, or code is explicitly flagged as unverified and sourced to "the
typical documented pattern for this class of repository," not to this repository directly.

---

## 1. Introduction

### What it is

Open Deep Research is the LangChain organisation's reference implementation of a deep-research
agent: given a question, it plans a multi-step investigation, searches and retrieves supporting
material across multiple steps, and synthesises the results into a structured report. The research
report (Finding 3) calls it "the best-documented worked example in the ecosystem" — its role is
demonstrative as much as functional: it exists to show what a well-built research agent on the
LangChain/LangGraph stack looks like, not primarily to be embedded as a library dependency inside
another application.

### The category it belongs to

This is the first of three products in this cookbook that are **applications**, not libraries — you
run or deploy them, you do not `pip install` and `import` them into your own codebase the way you
would `langchain` or `deepagents`. `../workspace-integration-examples/05-reference-applications.md` establishes this distinction for
all three (Open Deep Research, Open SWE, openwiki) and assigns Open Deep Research the most favourable
disposition of the three: **Harvest** — read it, take the patterns, don't necessarily deploy it
as-is.

### Why it matters to this workspace specifically

CC-00's own output _is_ research reports — the telescope archive, including this document, is exactly
the kind of artefact Open Deep Research is built to produce. An agent that plans a multi-step
investigation and writes an evidence-backed report is not a hypothetical use case for this
laboratory; it overlaps directly with the laboratory's actual workflow. `../workspace-integration-examples/06-ecosystem-integration-example.md`
proposes a CC-00-specific research-assistant graph inspired directly by this pattern.

### Enterprise framing

For a non-technical stakeholder: this is closer to a **reference architecture with working code**
than a product you install. Its business value is as a design template — read to understand a proven
plan-research-synthesise structure, then adapt CC-00's own governance requirements (attribution,
citation discipline, refutation of weak claims) on top of it, rather than deploying the upstream
repository unmodified into a governed environment.

---

## 2. Usage

> **Everything in this section is UNVERIFIED — sourced from the general, publicly documented pattern
> for LangChain-organisation reference-agent repositories of this kind, not from reading this specific
> repository's code.** Treat it as "what to expect," not as tested instructions. Before running
> anything, read the repository's own `README.md` at `github.com/langchain-ai/open_deep_research` —
> that is the authoritative source, and this manual does not substitute for it.

The typical shape for this class of repository:

```powershell
# UNVERIFIED — illustrative of the common pattern, not confirmed against this
# specific repository. Confirm every step against the upstream README first.

git clone https://github.com/langchain-ai/open_deep_research.git
cd open_deep_research
pip install -r requirements.txt

# Reference agents of this kind typically need at minimum a chat-model API key
# and a web-search-tool API key (commonly Tavily, given the multi-step search
# design), supplied via a .env file. The exact variable names are UNCONFIRMED
# for this repository — check its .env.example or README.
```

```powershell
# LangChain-organisation reference agents commonly ship a langgraph.json and
# are run/inspected via the LangGraph CLI's dev server, which also gives a
# local Studio UI for watching the plan → search → synthesise steps execute.
# UNVERIFIED for this specific repository.
pip install "langgraph-cli[inmem]"
langgraph dev
```

**What NOT to assume:** do not assume this repository's observability is self-hosted-friendly out of
the box. LangChain reference repositories commonly default to LangSmith tracing
(`LANGSMITH_TRACING=true` / `LANGCHAIN_TRACING_V2=true` environment variables). **If you deploy this
repository, check for and disable any LangSmith-enabling configuration before running it** — the
CEO's open-source-only constraint excludes LangSmith from every example in this investigation, and an
upstream repository's defaults do not carry that constraint automatically. This is the one operational
instruction in this section given with full confidence, precisely because it is a "check for and
remove," not a "add and configure," instruction.

### What to harvest instead of deploying wholesale

Per `../workspace-integration-examples/05-reference-applications.md` §1, the higher-value action is reading the repository for its
**structure**, not running it as-is:

- Research-plan-then-execute decomposition — matches the telescope template's own shape (Research
  Questions → Methodology → Findings)
- Parallel sub-researchers per question — maps onto ASGF L5 task decomposition
- Explicit source attribution in the synthesis step — matches this workspace's own citation
  discipline

A caution repeated deliberately from `../workspace-integration-examples/05-reference-applications.md`: a research agent that writes
confident reports from thin evidence is worse than no research agent, because the output is
indistinguishable from a well-evidenced report until someone checks the citations. If this pattern is
adopted, a refutation step (an agent whose only job is to attack the draft's citations, holding no
tools of its own) is not optional — it is the control that makes the rest safe.

---

## 3. Alternatives and rationale

| Option                                                                     | Choose it when                                                                                                                                                              | Trade-off against Open Deep Research                                                                                                                                                                                                                                                                           |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Build the research-assistant graph from scratch on LangGraph**           | You want CC-00's governance (ACL retrieval, ASGF middleware, telescope-format output) as the design's first-class constraint, not retrofitted onto someone else's structure | This is what `../workspace-integration-examples/06-ecosystem-integration-example.md` and `supporting/enterprise-examples/`'s research-assistant graph already do — a purpose-built alternative that exists in this investigation today, verified and tested, unlike this upstream repository.                  |
| **A commercial deep-research product** (e.g. a hosted research-agent SaaS) | Speed to a working demo matters more than auditability, and the CEO's open-source-only constraint doesn't apply to the use case                                             | Excluded outright by the CEO's standing constraint for this investigation's scope; noted only for completeness.                                                                                                                                                                                                |
| **A narrower, single-purpose retrieval agent** (no multi-step planning)    | The task is "answer this question from the corpus," not "investigate this question and produce a report"                                                                    | Simpler, smaller, easier to audit. Costs you the multi-step planning and synthesis Open Deep Research demonstrates — appropriate when the task genuinely doesn't need it (per best practice #10 in `../workspace-integration-examples/07-best-practices-and-asgf-mapping.md`: don't wrap what you don't need). |

**Rationale:** for this workspace, Open Deep Research earns its place as a **reference to read**, not
as a **dependency to deploy**. The workspace already has a purpose-built alternative
(`../workspace-integration-examples/06-ecosystem-integration-example.md`) that starts from CC-00's own governance requirements rather
than adapting them onto an upstream structure after the fact. Harvesting the pattern captures the
value; deploying the repository unmodified would import an untested dependency with unconfirmed
LangSmith defaults for a capability this workspace can already build governed, from the ground up.

---

## 4. Integrations

| Integrates with                                       | How (confidence)                                                                                                                                                                                                                                                                              |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **LangGraph**                                         | **Confirmed by category** — it is a LangGraph-based reference agent per the research report's own classification (Finding 3). Specific graph structure not verified.                                                                                                                          |
| **A web-search tool** (commonly Tavily)               | **Likely, unconfirmed** — multi-step research agents in this ecosystem commonly use a search API; not confirmed for this specific repository.                                                                                                                                                 |
| **LangSmith** (by upstream default, likely)           | **Caution, not a recommendation** — see the explicit warning in §2. Must be disabled/removed before any deployment in this workspace.                                                                                                                                                         |
| **This workspace's `workspace-knowledge` MCP server** | **Not upstream — a CC-00-specific harvesting opportunity.** If the plan-research-synthesise pattern is adopted, wire retrieval through the existing governed MCP bridge (`04-langchain-mcp-adapters.md` in this folder) rather than whatever retrieval the upstream repository ships with.    |
| **CC-00 governance middleware**                       | **Not upstream — apply when harvesting the pattern.** Any adapted version of this agent built in this workspace should use the six-class governance kit (`../workspace-integration-examples/00-conventions-and-baseline.md` §7), the same as every other agent example in this investigation. |

---

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
