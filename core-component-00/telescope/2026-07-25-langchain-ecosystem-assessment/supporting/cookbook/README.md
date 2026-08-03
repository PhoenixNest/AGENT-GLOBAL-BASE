# Cookbook — Enterprise User Manuals for the LangChain Ecosystem

Eight enterprise-grade user manuals — one per open-source product in the LangChain ecosystem —
evaluated from an adoption perspective: whether and why to use it, not primarily how its API works.

## The eight manuals

| #   | Manual                                                         | Product                  | Stars   | What it is, in one line                                                                 |
| --- | -------------------------------------------------------------- | ------------------------ | ------- | --------------------------------------------------------------------------------------- |
| 1   | [`01-langchain.md`](01-langchain.md)                           | `langchain`              | 142,575 | The agent framework itself — provider abstraction, `create_agent`, middleware           |
| 2   | [`02-langgraph.md`](02-langgraph.md)                           | `langgraph`              | 38,115  | The durable-execution orchestration engine underneath — usable standalone               |
| 3   | [`03-deepagents.md`](03-deepagents.md)                         | `deepagents`             | 26,797  | Batteries-included agent harness — planning, filesystem, subagent delegation            |
| 4   | [`04-langchain-mcp-adapters.md`](04-langchain-mcp-adapters.md) | `langchain-mcp-adapters` | 3,611   | Bridges MCP servers into LangChain tools                                                |
| 5   | [`05-open-deep-research.md`](05-open-deep-research.md)         | `open_deep_research`     | 12,426  | Reference deep-research agent (application, not a library)                              |
| 6   | [`06-open-swe.md`](06-open-swe.md)                             | `open-swe`               | 10,391  | Autonomous cloud coding agent (application, not a library)                              |
| 7   | [`07-openwiki.md`](07-openwiki.md)                             | `openwiki`               | 13,217  | CLI that generates agent-facing documentation (adjacent tooling)                        |
| 8   | [`08-langserve.md`](08-langserve.md)                           | `langserve`              | 2,330   | **Archived 2026-05-05 — do not adopt.** Manual exists for completeness and to redirect. |

Every manual follows the same four-part structure, in the same order:

1. **Introduction** — what the product is and the problem it solves
2. **Usage** — installation and best-practice, heavily-commented example code
3. **Alternatives** — competing options and the rationale for choosing (or not choosing) this one
4. **Integrations** — what it composes with, inside and outside the LangChain ecosystem

## Reading order

Read `01-langchain.md` and `02-langgraph.md` first — every other manual in this folder builds on the
framework and runtime those two cover. After that, the order is by category: `03`–`04` are libraries
you install and import into your own code; `05`–`07` are applications you deploy or run rather than
`pip install`; `08` is the one product in this cookbook you should not adopt at all.

## Verification status — read before trusting any code in this folder

Not every manual rests on the same evidence, and each one states this explicitly in its own header.

| Product                                      | How it was verified                                                                                                                | Example code                                                                                                                                                                                                                                                                                                                                                                                                                               |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `langchain`, `langgraph`                     | Installed and live-tested in this investigation's runnable companion project (`supporting/enterprise-examples/`, 25 passing tests) | Reference — reflects a verified, tested API surface, not independently re-executed within this specific manual                                                                                                                                                                                                                                                                                                                             |
| `deepagents`                                 | Installed and introspected live in this session                                                                                    | **Live-executed** — `create_deep_agent(...)` ran end to end against a fake model, including the built-in tool-binding requirement this surfaced. **2026-07-27:** live execution also surfaced a real finding — `FilesystemBackend` defaults to `virtual_mode=False`, letting `..` escape `root_dir` — fixed in this manual's own example (line ~196) and reproduced as a regression test in `workspace-integration-examples/verification/` |
| `langchain-mcp-adapters`                     | Installed and introspected live in this session                                                                                    | **Live-executed** — a real MCP server was started and bridged through `MultiServerMCPClient`, tool call round-tripped successfully                                                                                                                                                                                                                                                                                                         |
| `open_deep_research`, `open-swe`, `openwiki` | GitHub metadata only (stars, description, activity) — source code not read, package not installed                                  | Not executed — usage sections describe the publicly documented deployment shape, flagged as unverified                                                                                                                                                                                                                                                                                                                                     |
| `langserve`                                  | GitHub metadata only; confirmed archived via the GitHub API                                                                        | Not applicable — archived, do-not-adopt                                                                                                                                                                                                                                                                                                                                                                                                    |

Where a manual's example is genuinely executed, it says so and shows real output. Where it is not, it
says that too, in the same place, with the same visibility — no claim in this folder is dressed up as
more verified than it is.

---

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
