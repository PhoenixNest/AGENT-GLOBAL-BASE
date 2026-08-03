# supporting/ — LangChain Ecosystem Assessment Deliverables

Reading guide to this investigation's enterprise-grade LangChain deliverables. Three
CEO-commissioned bodies of work live here, each with its own audience and purpose:

- **[`workspace-integration-examples/`](workspace-integration-examples/README.md)** — eight
  Markdown reference documents proving the ecosystem wires into _this specific workspace_: this
  repo's CC-00 modules, its two governed MCP servers, its ASGF governance kit. Folded into
  `2026-07-25-langchain-ecosystem-assessment` per the 2026-07-26 addendum in
  `../research-report.md` — **this is a deliverable of that investigation, not a separate
  assessment.** Five of its eight files now carry real execution evidence — three via its own
  standalone `verification/` harness (added 2026-07-27), the other two via `enterprise-examples/`
  below; see the file's own README for the full breakdown.
- **[`enterprise-examples/`](enterprise-examples/README.md)** — the runnable counterpart: an
  installable Python package implementing the governance kit and the research-assistant graph
  described in `workspace-integration-examples/06-ecosystem-integration-example.md`, with a real
  pytest suite that was actually run. It lives here (a `supporting/` subfolder) rather than at the
  CC-00 lab root, per CEO direction: it is a research output of this investigation, not a
  standalone CC-00 lab deliverable.
- **[`cookbook/`](cookbook/README.md)** — eight self-contained enterprise adoption manuals, one
  per LangChain open-source product: introduction, usage, alternatives, integrations. Written for
  someone deciding whether to adopt a product, not someone wiring it into this workspace.

Where the Markdown in `workspace-integration-examples/` and the runnable `enterprise-examples/`
project disagree on a signature, the runnable project is correct — Markdown does not get updated
after the fact per the telescope append-only rule, so this note is the pointer instead.

---

## Start here

Read `workspace-integration-examples/00-conventions-and-baseline.md` first, always. Every other
file in that folder assumes its pins, its environment assumptions, and — most importantly — **the
ASGF governance kit in its §7**, which every product example imports rather than re-deriving
controls.

## Reading order

Each of the three deliverables below has its own file/section table and its own recommended
order — they differ in audience, structure, and file count enough that one shared table would
either flatten `workspace-integration-examples/`'s eight documents into single rows, or bury
`enterprise-examples/`'s and `cookbook/`'s own internal structure. Read whichever deliverable
matches what you need; none of the three requires reading the others first.

### `workspace-integration-examples/` — workspace-specific integration reference

| #   | File                                                                                                            | Read this to understand                                                                                                                                                                                                                                      |
| --- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 0   | [`00-conventions-and-baseline.md`](workspace-integration-examples/00-conventions-and-baseline.md)               | Version pins and CVE floors, the CEO's open-source-only constraint, hardware allocation, observability without LangSmith, the CC-00 module-import workaround, and **the six-class governance middleware kit** — the reusable asset everything else builds on |
| 1   | [`01-langchain-examples.md`](workspace-integration-examples/01-langchain-examples.md)                           | `create_agent`, schema-constrained output, tool design, model routing (API vs. local), and the file-by-file migration of this workspace's own stale v0.x references                                                                                          |
| 2   | [`02-langgraph-examples.md`](workspace-integration-examples/02-langgraph-examples.md)                           | Typed four-slot state, checkpointing as a security boundary, `interrupt()` human-approval gates, declarative swarm topology, `Command` as the Context Handoff Protocol carrier                                                                               |
| 3   | [`03-deepagents-examples.md`](workspace-integration-examples/03-deepagents-examples.md)                         | Planning, filesystem backends, subagent delegation, and the direct tension between dynamic sub-agent spawning and ASGF L5's ban on emergent topology                                                                                                         |
| 4   | [`04-langchain-mcp-adapters-examples.md`](workspace-integration-examples/04-langchain-mcp-adapters-examples.md) | Bridging this workspace's two governed MCP servers (`workspace-knowledge`, `agent-memory`) into LangChain tools — including the `health_check` name collision and the write-capable-tool hazard                                                              |
| 5   | [`05-reference-applications.md`](workspace-integration-examples/05-reference-applications.md)                   | What to harvest, observe, or decline from `open_deep_research`, `open-swe`, `openwiki`, and why `langserve` (archived) should not be adopted                                                                                                                 |
| 6   | [`06-ecosystem-integration-example.md`](workspace-integration-examples/06-ecosystem-integration-example.md)     | **The flagship** — one end-to-end system (a telescope research assistant) using every product above together, proposed as the named pilot task the original report's Next Steps ask for                                                                      |
| 7   | [`07-best-practices-and-asgf-mapping.md`](workspace-integration-examples/07-best-practices-and-asgf-mapping.md) | The full practice catalogue (22 items) and the requirement-by-requirement ASGF compliance map — the reference to cite in a design review                                                                                                                     |

**Reading order:** `00` first, always — every other file assumes its pins and its governance kit.
After that, read by product if you have a specific one in mind, or straight through `01` → `07` if
not. If you only read one file beyond `00`, read `06` — it is where every other document's pieces
compose into a single governed system, with pre-committed pilot acceptance criteria.

**Execution evidence, added 2026-07-27:** `01`, `02`, and `03`'s claims are now proven by a
standalone test harness, [`verification/`](workspace-integration-examples/verification/README.md)
(13 real, passing tests, no API key — deliberately independent of `enterprise-examples/`, per CEO
direction that the two folders not be merged). `00`, `04`, and `06`'s patterns are separately
proven inside `enterprise-examples/` itself. `05` and `07` have no standalone runnable claims to
execute. `verification/` also surfaced a real finding: `FilesystemBackend` (`deepagents`) defaults
to `virtual_mode=False`, under which a `..` path segment escapes its declared `root_dir` —
corrected in `03-deepagents-examples.md`.

### `enterprise-examples/` — the runnable companion

| File / Section                                                                                                   | Read this to understand                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`README.md`](enterprise-examples/README.md) — §§ What is actually verified / Two findings this project surfaced | **Read first.** The honest, item-by-item boundary between what was live-executed (governance mechanics, CC-00 integration, LangGraph durability/interrupt, ACL filtering) and what was not (live model reasoning quality, MCP bridging, DeepAgents usage) — no API key was available in this environment. Also documents two real bugs found only by running the code: `ContextAssembler` output isn't LangChain-message-valid once tool output is present, and `create_agent`'s default `AgentState` silently drops undeclared keys |
| `src/cc00_langchain/cc00_path.py`                                                                                | The CC-00 four-module `implementations` package-name-collision workaround (Finding 11), executed and tested                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `src/cc00_langchain/asgf.py`                                                                                     | The six governance middleware classes plus `CC00AgentState` — the tested implementation of `workspace-integration-examples/00 §7`'s kit, including its documented deviations                                                                                                                                                                                                                                                                                                                                                         |
| `src/cc00_langchain/rag_tool.py`                                                                                 | `RAGPipeline` wrapped as a LangChain tool with the ACL role closure-bound, not a tool parameter (Finding 14)                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `src/cc00_langchain/graphs/research_assistant.py`                                                                | The flagship graph: plan → ACL-retrieve → governed draft → `interrupt()` approval gate → gated write/discard                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `tests/` (5 files, 25 tests)                                                                                     | The actual evidence — every claim in the README's verification table traces to a specific test here                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `scripts/run_demo.py`                                                                                            | The CLI entry point — run it yourself, see the README's § Try it                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

**Reading order:** the README's verification table first — know what's real before reading any
code. Then `src/cc00_langchain/asgf.py` (the governance kit, the most-reused piece). Then
`graphs/research_assistant.py` (the flagship, ties every other module together). From there,
either `tests/` for the proof or straight to `scripts/run_demo.py` if you just want to run it.

### `cookbook/` — enterprise adoption manuals

| #   | Manual                                                                  | Product                  | Stars   | What it is, in one line                                                                 |
| --- | ----------------------------------------------------------------------- | ------------------------ | ------- | --------------------------------------------------------------------------------------- |
| 1   | [`01-langchain.md`](cookbook/01-langchain.md)                           | `langchain`              | 142,575 | The agent framework itself — provider abstraction, `create_agent`, middleware           |
| 2   | [`02-langgraph.md`](cookbook/02-langgraph.md)                           | `langgraph`              | 38,115  | The durable-execution orchestration engine underneath — usable standalone               |
| 3   | [`03-deepagents.md`](cookbook/03-deepagents.md)                         | `deepagents`             | 26,797  | Batteries-included agent harness — planning, filesystem, subagent delegation            |
| 4   | [`04-langchain-mcp-adapters.md`](cookbook/04-langchain-mcp-adapters.md) | `langchain-mcp-adapters` | 3,611   | Bridges MCP servers into LangChain tools                                                |
| 5   | [`05-open-deep-research.md`](cookbook/05-open-deep-research.md)         | `open_deep_research`     | 12,426  | Reference deep-research agent (application, not a library)                              |
| 6   | [`06-open-swe.md`](cookbook/06-open-swe.md)                             | `open-swe`               | 10,391  | Autonomous cloud coding agent (application, not a library)                              |
| 7   | [`07-openwiki.md`](cookbook/07-openwiki.md)                             | `openwiki`               | 13,217  | CLI that generates agent-facing documentation (adjacent tooling)                        |
| 8   | [`08-langserve.md`](cookbook/08-langserve.md)                           | `langserve`              | 2,330   | **Archived 2026-05-05 — do not adopt.** Manual exists for completeness and to redirect. |

Every manual follows the same four-part structure: (1) introduction, (2) usage with best-practice
commented example code, (3) alternatives and rationale, (4) integrations.

**Reading order:** `01-langchain.md` and `02-langgraph.md` first — every other manual builds on
the framework and runtime those two cover. After that, the order is by category: `03`–`04` are
libraries you install and import into your own code; `05`–`07` are applications you deploy or run
rather than `pip install`; `08` is the one product in this cookbook you should not adopt at all.

---

## What ties them together

Every product example imports the same governance kit rather than re-deriving controls per document:

| Middleware                     | Closes                                                                                         |
| ------------------------------ | ---------------------------------------------------------------------------------------------- |
| `FourSlotContextMiddleware`    | ASGF L2 four-slot structure, slot priority, token budget at assembly — all three **Mandatory** |
| `TokenBudgetMiddleware`        | ASGF L3 token budget monitor — **Mandatory**                                                   |
| `TypedErrorBoundaryMiddleware` | ASGF L3 typed error recovery, timeout, backoff-with-jitter — **Mandatory**                     |
| `ToolGovernanceMiddleware`     | ASGF L3 tool whitelist and call limits — Required                                              |
| `PIIMiddleware`                | ASGF L3 PII scrub/scan — Required                                                              |
| `ObservabilityMiddleware`      | Cross-layer tracing, replacing the excluded LangSmith                                          |

Full definitions in `workspace-integration-examples/00 §7`. The runnable project's
`src/cc00_langchain/asgf.py` is the tested implementation of the same six classes.

## Status of everything in this folder

| Deliverable                       | Status                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace-integration-examples/` | **Mixed, per file, since 2026-07-27.** `00`, `04`, `06` are proven inside `enterprise-examples/`; `01`, `02`, `03` are proven inside this folder's own `verification/` harness (13 real pytest passes, no API key); `05` and `07` have no standalone runnable claims and remain reference/analysis by nature. Nothing is silently left unstated — each file's own Status line says which of these applies.                                     |
| `enterprise-examples/`            | **Executed and tested.** 25 real pytest passes, no API key required. Governance mechanics, CC-00 integration, LangGraph durability/interrupt, and ACL filtering are genuinely exercised; live model reasoning quality, MCP-server bridging, and DeepAgents usage are installed/importable but not exercised — see its own README's verification table for the item-by-item boundary.                                                           |
| `cookbook/`                       | **Mixed, per product.** `langchain`/`langgraph` reference the tested `enterprise-examples/` API surface; `deepagents` and `langchain-mcp-adapters` were live-executed directly in the session that wrote those manuals; the three reference-application manuals and the archived-product manual are GitHub-metadata-only, explicitly flagged unverified. See `cookbook/README.md`'s own verification table for the full per-product breakdown. |

Treat unexecuted code blocks as a credible, API-accurate starting point, not as working software —
that is what `enterprise-examples/` is for.

---

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
