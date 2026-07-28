# verification/ — Standalone Test Harness for `workspace-integration-examples/`

Proves the runnable claims in `01-langchain-examples.md`, `02-langgraph-examples.md`, and
`03-deepagents-examples.md` with real, executed, passing tests — no API key required. Built per
CEO direction, with one explicit constraint carried over from that decision: **this project does
not import from, share a venv with, or otherwise merge into `supporting/enterprise-examples/`.**
The two are architecturally separate on purpose — `enterprise-examples/` is the one tested
flagship system; this harness independently proves five of the eight
`workspace-integration-examples/` files' own, narrower claims. Where duplication was the price of
that separation (e.g. the `ToolCapableFakeChatModel` workaround), it was duplicated deliberately.

`04-langchain-mcp-adapters-examples.md`, `06-ecosystem-integration-example.md`, and
`00-conventions-and-baseline.md` are not covered here because their specific patterns are already
executed and tested inside `enterprise-examples/` — see that project's own
"Relationship to the Markdown examples" table. `05-reference-applications.md` and
`07-best-practices-and-asgf-mapping.md` are not covered because they contain no standalone
runnable claims of their own (see their updated Status lines).

---

## Setup

```powershell
cd core-component-00/telescope/2026-07-25-langchain-ecosystem-assessment/supporting/workspace-integration-examples/verification
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
```

Same security-floor discipline as `enterprise-examples/`: `requirements.txt` pins
`langgraph>=1.0.10` / `langgraph-checkpoint-sqlite>=3.0.1` (the CVE-2025-67644 /
CVE-2026-28277 chain); `requirements.lock.txt` records what actually resolved on 2026-07-27
(`langchain==1.3.14`, `langgraph==1.2.9`, `deepagents==0.6.12` — the same versions
`enterprise-examples/` resolved to, independently).

## Run the tests

```powershell
.venv/Scripts/python.exe -m pytest -v
```

Real output from this environment, 2026-07-27 (13 tests, all passing, no API key, ~2 seconds):

```
tests/test_01_langchain_examples.py::test_governed_agent_baseline_builds_and_invokes_with_declared_state PASSED
tests/test_01_langchain_examples.py::test_schema_constrained_output_agent_builds_with_tool_strategy PASSED
tests/test_01_langchain_examples.py::test_triage_result_literal_fields_are_enforced_by_the_parser_not_prose PASSED
tests/test_01_langchain_examples.py::test_tiered_routing_sends_any_tool_bearing_request_to_the_reasoning_model PASSED
tests/test_01_langchain_examples.py::test_tiered_routing_sends_tool_free_bulk_classification_to_the_local_model PASSED
tests/test_02_langgraph_examples.py::test_sacred_context_reducer_is_append_only_and_cannot_be_erased PASSED
tests/test_02_langgraph_examples.py::test_checkpointer_keeps_two_thread_ids_fully_isolated PASSED
tests/test_02_langgraph_examples.py::test_hierarchical_command_topology_routes_every_specialist_back_to_supervisor PASSED
tests/test_02_langgraph_examples.py::test_command_handoff_tier_invariants_are_enforced_at_construction PASSED
tests/test_03_deepagents_examples.py::test_declared_subagent_roster_has_no_tool_overlap PASSED
tests/test_03_deepagents_examples.py::test_deep_agent_with_declared_topology_and_gated_writes_runs_end_to_end PASSED
tests/test_03_deepagents_examples.py::test_filesystem_backend_confines_writes_to_its_declared_root_dir PASSED
tests/test_03_deepagents_examples.py::test_filesystem_backend_virtual_mode_false_allows_path_escape PASSED

============================== 13 passed in 1.82s ==============================
```

## What each file's tests actually prove

| Source file                 | What was already proven elsewhere (not repeated here)                                  | What this harness newly proves                                                                                                                                                                                                                                                                                                                           |
| --------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `01-langchain-examples.md`  | —                                                                                      | A tool-bearing `create_agent` accepts declared extra state keys; `ToolStrategy`'s `Literal` fields are enforced by the parser; the tiered-routing guard never sends a tool-bearing request to the local tier                                                                                                                                             |
| `02-langgraph-examples.md`  | Single-thread checkpoint pause/resume, one `interrupt()` gate (`enterprise-examples/`) | `sacred_context`'s append-only reducer cannot be erased by a node; two `thread_id`s are fully isolated under one checkpointer; a hierarchical `Command` topology enforces "specialists report only to the supervisor"; handoff-tier invariants (Full requires history, Minimal forbids it) fail at construction                                          |
| `03-deepagents-examples.md` | —                                                                                      | `create_deep_agent` itself (not a hand-rolled graph) runs end to end with a static, named subagent roster, `StateBackend`, a checkpointer, and gated writes; **a real finding:** `FilesystemBackend`'s `virtual_mode=False` default lets `..` escape `root_dir` — reproduced, and the source doc's own example was corrected to pass `virtual_mode=True` |

## A real finding from running this, not from reading the docs

`FilesystemBackend(root_dir=...)` without `virtual_mode=True` does not confine writes the way
`03-deepagents-examples.md`'s Example 3 claims — a `..` path segment escapes `root_dir` under the
library's own default. `test_filesystem_backend_virtual_mode_false_allows_path_escape` reproduces
this directly; `test_filesystem_backend_confines_writes_to_its_declared_root_dir` shows the fix.
The source document's code block and rules table were corrected in place once this was confirmed.

## Project layout

```
verification/
├── README.md                — this file
├── pyproject.toml           — pytest config + packaging metadata
├── requirements.txt / .lock.txt
├── src/cc00_wie_verification/
│   ├── __init__.py
│   └── fakes.py              ← ToolCapableFakeChatModel (duplicated from enterprise-examples/, deliberately)
└── tests/                    — 13 tests, all real executions, see § above
```

---

**Investigation:** `2026-07-25-langchain-ecosystem-assessment`
**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
