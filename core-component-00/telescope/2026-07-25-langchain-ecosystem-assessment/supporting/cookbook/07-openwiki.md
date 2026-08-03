# openwiki — Enterprise User Manual

**Repository:** `langchain-ai/openwiki` · **Stars:** 13,217 (2026-07-25) · **Status:** Active
**Verification status:** GitHub metadata only (stars, description, retrieved via the GitHub REST API
on 2026-07-25 by the parent assessment). **The repository's source code was not read** and the
application was not installed or run in this session.

---

## 1. Introduction

### What it is

openwiki is a CLI that writes and maintains agent-facing documentation for a codebase — per the
research report's Finding 3 classification, "adjacent tooling, not part of the agent runtime." It is
notably the most-starred single repository in the entire ecosystem inventory the assessment gathered
(13,217 — more than DeepAgents at 26,797's sibling `open_deep_research` at 12,426, and more than
`langgraph` itself would suggest for a documentation tool, reflecting real demand for this category of
tooling), yet it is the one product in this cookbook that a LangChain agent never imports or calls at
runtime.

### The category it belongs to

openwiki is unlike every other product in this cookbook in one specific way: it is not something an
_agent_ uses, it is something a _development team_ uses to produce the documentation that agents
(and humans) later read. It sits adjacent to the agent runtime, not inside it.

### Why it is nonetheless relevant to this workspace

This workspace is, by its own description, "a Markdown-first, agent-native knowledge base" whose
primary artefacts are exactly the category of document openwiki generates: `CLAUDE.md` files,
`AGENTS.md`, skill contracts, and rules. A tool that generates and maintains agent-facing
documentation overlaps, category-for-category, with work this workspace already does — by hand, and
deliberately.

### Enterprise framing

For a non-technical stakeholder: this is a tool for keeping "the documentation that tells an AI
assistant how a codebase works" in sync with the codebase itself, automatically, rather than relying
on developers to remember to update it. The value proposition is real and the demand signal (star
count) is strong. The risk is specific to _this_ workspace, not to the tool generally, and is
explained in §3.

---

## 2. Usage

> Everything in this section is **UNVERIFIED** — sourced from the general pattern for documentation-
> generation CLIs of this kind, not from reading this specific repository. Consult
> `github.com/langchain-ai/openwiki`'s own README before running anything.

The typical shape for a tool in this category:

```powershell
# UNVERIFIED — illustrative of the common pattern for this class of CLI tool,
# not confirmed against this specific repository.

pip install openwiki        # or: npm install -g openwiki, if it ships as a Node CLI — unconfirmed
cd /path/to/target-codebase
openwiki generate           # typical entry point for this category of tool — exact command unconfirmed
```

Tools in this category typically scan a codebase's structure, infer purpose from code and existing
comments, and emit or update Markdown documentation files — commonly with a model API key required
for the inference step. None of these specifics are confirmed for openwiki itself.

### The one instruction given with confidence, regardless of exact CLI syntax

**Do not point openwiki at this workspace's authored `CLAUDE.md` files, `AGENTS.md`, skill contracts,
or rules and let it regenerate them.** See §3 for why — this is a governance boundary, not a technical
limitation of the tool.

---

## 3. Alternatives and rationale

| Option                                                                                   | Choose it when                                                                                                                                            | Trade-off against openwiki                                                                                                                                                                     |
| ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Authored `CLAUDE.md` / `AGENTS.md` documentation (this workspace's current approach)** | Documentation is a deliberate policy decision — role boundaries, forbidden behaviours, escalation criteria — not a summary of what the code happens to do | This workspace's current approach, and the recommended one for governance documents specifically. Costs more human authoring time; gains documents that encode intent rather than description. |
| **openwiki, scoped to genuinely descriptive, non-governance documentation**              | The target is API reference docs, module-purpose summaries, or onboarding material for a codebase with no governance content mixed in                     | Automated, kept in sync with the code, low ongoing maintenance cost. Appropriate for exactly the content it's built for — descriptive documentation, not policy documents.                     |
| **Manual documentation review as part of the existing PR/pipeline process**              | The codebase changes slowly enough that automated regeneration adds more risk (silently overwriting intent) than it saves in effort                       | Slower, but nothing is ever silently rewritten. This workspace's existing convention.                                                                                                          |

**Rationale — the caution stated plainly:** `CLAUDE.md` files in this workspace are deliberate policy
documents, not summaries of code. A tool that regenerates documentation from what the code _does_
would overwrite documentation that encodes what the code (and its surrounding agents) _are permitted
to do_ — a categorically different kind of content. This is exactly the failure mode ASGF's
`canonical-source-of-truth` cross-cutting pattern exists to prevent: two documents both claiming
authority over the same question, one generated and one authored, with no explicit subordination
between them. **If openwiki is evaluated for this workspace, that evaluation should happen on its own
merits, scoped explicitly away from governance documents, and is out of scope for the LangChain
ecosystem adoption decision this investigation addresses** — per `../workspace-integration-examples/05-reference-applications.md`
§3, folding the two decisions together would conflate unrelated questions.

---

## 4. Integrations

| Integrates with                                                 | How (confidence)                                                                                                                                                                                                                                                                                                          |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A chat-model API**                                            | **Likely, unconfirmed** — documentation-inference tools of this kind typically call an LLM to summarise code purpose; not confirmed for this specific repository.                                                                                                                                                         |
| **Source control (git)**                                        | **Likely, unconfirmed** — typically scans a repository's working tree or git history to infer structure; not confirmed.                                                                                                                                                                                                   |
| **This workspace's existing `CLAUDE.md` hierarchy**             | **Explicitly NOT recommended as an integration** — see §3. Any use of openwiki in this workspace should be scoped away from the authored governance-document hierarchy.                                                                                                                                                   |
| **CI/CD pipelines** (typical for this tool category, generally) | **Likely, unconfirmed** — documentation-generation CLIs are commonly wired into CI to keep docs in sync with merges; not confirmed for this repository specifically, and this workspace's own CI/pipeline conventions (`company/pipeline/`, `studio/casual-games/pipeline/`) are unrelated to this investigation's scope. |

---

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
