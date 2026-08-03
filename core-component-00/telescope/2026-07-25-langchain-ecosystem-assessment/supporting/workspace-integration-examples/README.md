# workspace-integration-examples/ — Workspace-Specific LangChain Integration Reference

Eight Markdown reference documents proving the LangChain ecosystem wires into **this specific
workspace** — its CC-00 engineering modules, its two governed MCP servers
(`workspace-knowledge`, `agent-memory`), and its ASGF governance kit — not a generic LangChain
tutorial. Most of each file's code was written against a verified API surface but not executed at
authoring time; six of the eight files (`00`, `01`, `02`, `03`, `04`, `06` — see the table below)
now carry real execution evidence, from two independent projects: `../enterprise-examples/` (the
flagship system) and `verification/` (this folder's own standalone test harness, added
2026-07-27 per CEO direction — see its own `README.md`). The remaining two (`05`, `07`) have no
standalone runnable claims of their own to execute.

This is distinct in audience from `../cookbook/`: the cookbook answers "should we adopt this
product, and how does it compare to alternatives?" for a decision-maker. This folder answers "how
does this product connect to _our_ modules, _our_ MCP servers, and _our_ governance
requirements?" for whoever builds the integration.

## Files

| #   | File                                                                             | Covers                                                                                                                                                                                                        | Execution evidence                                                                     |
| --- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 0   | [`00-conventions-and-baseline.md`](00-conventions-and-baseline.md)               | Version pins and CVE floors, the CEO's open-source-only constraint, hardware allocation, observability without LangSmith, the CC-00 module-import workaround, and **the six-class governance middleware kit** | `enterprise-examples/` (import workaround, governance kit)                             |
| 1   | [`01-langchain-examples.md`](01-langchain-examples.md)                           | `create_agent`, schema-constrained output, tool design, model routing, this workspace's own stale v0.x reference migration                                                                                    | `verification/` (5 tests)                                                              |
| 2   | [`02-langgraph-examples.md`](02-langgraph-examples.md)                           | Typed four-slot state, checkpointing as a security boundary, `interrupt()` human-approval gates, declarative swarm topology, `Command` as the Context Handoff Protocol carrier                                | `verification/` (4 tests) + `enterprise-examples/` (interrupt/checkpoint pause-resume) |
| 3   | [`03-deepagents-examples.md`](03-deepagents-examples.md)                         | Planning, filesystem backends, subagent delegation, and the tension with ASGF L5's ban on emergent topology                                                                                                   | `verification/` (4 tests) — surfaced a real `FilesystemBackend` finding, see below     |
| 4   | [`04-langchain-mcp-adapters-examples.md`](04-langchain-mcp-adapters-examples.md) | Bridging this workspace's two governed MCP servers into LangChain tools — including the `health_check` name collision and a write-capable-tool hazard                                                         | `enterprise-examples/` (ACL/RAG tool)                                                  |
| 5   | [`05-reference-applications.md`](05-reference-applications.md)                   | What to harvest, observe, or decline from `open_deep_research`, `open-swe`, `openwiki`, and why `langserve` (archived) should not be adopted                                                                  | None — no standalone runnable claims (dispositional analysis of unread source)         |
| 6   | [`06-ecosystem-integration-example.md`](06-ecosystem-integration-example.md)     | **The flagship** — one end-to-end system (a telescope research assistant) using every product above together                                                                                                  | `enterprise-examples/` (the flagship graph itself)                                     |
| 7   | [`07-best-practices-and-asgf-mapping.md`](07-best-practices-and-asgf-mapping.md) | The full practice catalogue (22 items) and the requirement-by-requirement ASGF compliance map                                                                                                                 | None — no code blocks of its own                                                       |

Read `00` first — every other file assumes its pins and its governance kit. See
`../README.md` for how this folder relates to `enterprise-examples/` and `cookbook/`.

## Status

Every file's code is now either executed and tested, or explicitly documented as containing no
independently-runnable claims — nothing here is silently left as "reference only" without saying
why. `00`, `04`, and `06`'s patterns are proven inside `../enterprise-examples/`; `01`, `02`, and
`03`'s are proven inside this folder's own `verification/` harness (13 tests, no API key,
deliberately independent of `enterprise-examples/` — see `verification/README.md`); `05` and `07`
have no standalone runnable claims to execute. `verification/` also surfaced a real finding,
corrected in `03-deepagents-examples.md`: `FilesystemBackend` defaults to `virtual_mode=False`,
under which a `..` path segment escapes its declared `root_dir` entirely.

---

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
