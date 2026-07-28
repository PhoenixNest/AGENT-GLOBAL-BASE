# cc00-enterprise-examples

**A runnable companion to the eight documents in this same `supporting/` folder** — part of the
`2026-07-25-langchain-ecosystem-assessment` investigation
(`core-component-00/telescope/2026-07-25-langchain-ecosystem-assessment/`). Everything else in
`supporting/` is Markdown reference code — written against a verified API surface but never executed.
This project is the executable counterpart: an installable Python package implementing the CC-00 ASGF
governance middleware kit and a working version of the telescope research assistant, with a real
pytest suite that was actually run.

**Placement, per CEO direction:** this is a research output of the assessment investigation, not a
standalone CC-00 lab deliverable — it lives inside this investigation's `supporting/` folder rather
than at the CC-00 lab root. (It was briefly placed at `core-component-00/examples/` on 2026-07-27
before the CEO corrected that; see the parent report's Version History v1.3.) `core-component-00/CLAUDE.md`'s
note that CC-00 is "the only place with runnable code in this entire workspace" still holds — this
project is still under `core-component-00/`, just nested inside the telescope archive rather than at
its root, which is itself a small departure from the archive's normal documents-only convention,
made deliberately for this one investigation.

---

## What is actually verified, versus what is not

Read this section before trusting anything else in this README.

| Claim                                                                                                                                                                                             | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `langchain==1.3.14`, `langgraph==1.2.9`, `deepagents==0.6.12`, `langchain-mcp-adapters==0.3.0` install cleanly from PyPI                                                                          | **Verified 2026-07-27** — real `pip install`, see `requirements.lock.txt` for the full resolved set                                                                                                                                                                                                                                                                                                                                                                  |
| The CC-00 module loader (`cc00_path.py`) imports real CC-00 code from all four module roots in one process                                                                                        | **Verified** — `tests/test_cc00_path.py`, including the two harder cases (an absolute import in `memory_store.py`, internal relative imports in `swarm_orchestrator.py`)                                                                                                                                                                                                                                                                                             |
| The six ASGF governance middleware classes run inside a real `create_agent(...)` call and do what they claim (token cap, PII scrub/scan, tool whitelist, four-slot assembly, ordering-dependence) | **Verified** — `tests/test_asgf_middleware.py`, against `FakeListChatModel`, **no API key used or required**                                                                                                                                                                                                                                                                                                                                                         |
| CC-00's `RAGPipeline` wrapped as a LangChain tool with the ACL role closure-bound (not a tool parameter) genuinely filters by role                                                                | **Verified** — `tests/test_rag_tool.py`                                                                                                                                                                                                                                                                                                                                                                                                                              |
| The end-to-end research-assistant graph (plan → ACL-retrieve → governed draft → `interrupt()` approval gate → gated file write) runs, pauses, resumes, and writes/discards correctly              | **Verified** — `tests/test_research_assistant_graph.py`, including a real `SqliteSaver` checkpoint/resume cycle                                                                                                                                                                                                                                                                                                                                                      |
| The CLI demo (`scripts/run_demo.py`) runs end to end and produces a real output file                                                                                                              | **Verified** — ran it directly during development, see § Try it                                                                                                                                                                                                                                                                                                                                                                                                      |
| Reasoning **quality** from a real LLM (Claude, GPT, etc.)                                                                                                                                         | **NOT verified.** No `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` was available in this environment (checked: neither is set). Every test above uses `langchain_core.language_models.fake_chat_models.FakeListChatModel` — it returns canned text, not reasoning. The middleware, the graph mechanics, the ACL filtering, and the CC-00 integration are all genuinely exercised; whether a real model produces a _good_ research report through this pipeline is untested. |
| `response_format=ToolStrategy(ResearchReport)` (schema-constrained output, per `supporting/01 §2` / `06 §4.4`)                                                                                    | **Reference only in the runnable graph.** `FakeListChatModel` does not implement `bind_tools`, so live structured output could not be exercised without a real provider. `ResearchReport.model_validate_json(...)` — the schema itself — is not separately unit-tested in this deliverable; treat it as documented, not verified.                                                                                                                                    |
| `langchain-mcp-adapters` bridging the workspace's real `workspace-knowledge`/`agent-memory` MCP servers                                                                                           | **Not exercised.** `langchain-mcp-adapters` installs and imports cleanly (see below), but no test in this project spins up the real MCP servers — that would require the Qdrant containers running and is out of scope for an offline, fast pytest suite. `supporting/04` remains the reference for that integration.                                                                                                                                                |
| DeepAgents (`deepagents==0.6.12`) usage patterns from `supporting/03`                                                                                                                             | **Installs cleanly; not exercised.** No test in this project builds a `create_deep_agent(...)` instance.                                                                                                                                                                                                                                                                                                                                                             |

**Bottom line:** the governance mechanics, the CC-00 integration, the LangGraph durability/interrupt
primitives, and the ACL security property are real and tested. Live model reasoning quality,
structured-output tool-calling, MCP-server bridging, and DeepAgents are installed and importable but
not exercised — that gap is the honest boundary of what "no API key available" allows.

---

## Two findings this project surfaced that the Markdown examples could not

Writing runnable code found two real integration problems that reading the API docs did not surface.
Both are documented in `src/cc00_langchain/asgf.py`'s module docstring and fixed in the code, not
worked around:

1. **CC-00's `ContextAssembler` output isn't LangChain-message-valid once tool output is added.**
   `assembler.build()` can emit `{"role": "tool", "content": ...}`, and
   `langchain_core.messages.convert_to_messages` raises `KeyError: 'tool_call_id'` on that shape —
   confirmed directly. `FourSlotContextMiddleware` folds the assembled content into
   `request.system_message` instead of replacing `request.messages` wholesale, which is a real
   adaptation from what `supporting/00 §7` describes.
2. **`create_agent`'s default `AgentState` silently drops any state key it doesn't declare.**
   `sacred_context`, `retrieved`, and `tool_outputs` never reached the middleware until a custom
   `state_schema=CC00AgentState` was passed — confirmed by printing `request.state.keys()` with and
   without it. This is now a documented, enforced requirement: every `create_agent(...)` call in this
   project passes `state_schema=CC00AgentState`.

A third bug (not an API-surface finding, just a plain bug) was caught the same way:
`write_node`'s original filename sanitisation missed Windows-invalid characters like `?`, and a
question containing one raised `OSError: [Errno 22] Invalid argument`. Fixed and covered by
`test_filename_sanitization_handles_windows_invalid_characters`.

None of these three would have been found by writing Markdown code samples — they only surface when
the code actually runs.

---

## Setup

```powershell
cd core-component-00/telescope/2026-07-25-langchain-ecosystem-assessment/supporting/enterprise-examples
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
```

**Do not install these dependencies into `core-component-00/mcp-servers/.venv/`.** That venv is
shared by the production `workspace-knowledge` and `agent-memory` MCP servers
(`.claude/rules/mcp-governance.md`); installing an unrelated dependency set there risks a version
conflict that breaks a production server. This project gets its own venv, deliberately.

`requirements.txt` is intentionally unpinned on first install so the resolver picks current releases;
`requirements.lock.txt` (checked in) records exactly what that resolved to on 2026-07-27 — re-pin
`requirements.txt` to the lock file once this project stabilises. See
`../../telescope/2026-07-25-langchain-ecosystem-assessment/supporting/workspace-integration-examples/00-conventions-and-baseline.md`
§3 for why exact pinning is a **security control** here (the LangGraph checkpointer CVE chain), not
hygiene.

## Run the tests

```powershell
.venv/Scripts/python.exe -m pytest -v
```

Real output from this environment, 2026-07-27 (25 tests, all passing, no API key, ~1–3 seconds):

```
tests/test_asgf_middleware.py::test_full_stack_runs_end_to_end_with_no_api_key PASSED
tests/test_asgf_middleware.py::test_default_agent_state_silently_drops_extra_keys PASSED
tests/test_asgf_middleware.py::test_four_slot_middleware_assembles_retrieved_and_sacred_context PASSED
tests/test_asgf_middleware.py::test_token_budget_middleware_enforces_model_call_cap PASSED
tests/test_asgf_middleware.py::test_pii_middleware_scrubs_input_before_dispatch PASSED
tests/test_asgf_middleware.py::test_pii_middleware_blocks_output_leak PASSED
tests/test_asgf_middleware.py::test_tool_governance_rejects_unregistered_tools PASSED
tests/test_asgf_middleware.py::test_middleware_ordering_is_load_bearing PASSED
tests/test_cc00_path.py::test_cc00_root_resolves_to_the_real_directory PASSED
tests/test_cc00_path.py::test_layer2_context_assembler_is_the_real_cc00_class PASSED
tests/test_cc00_path.py::test_layer3_harness_classes_are_real PASSED
tests/test_cc00_path.py::test_layer4_rag_pipeline_is_real PASSED
tests/test_cc00_path.py::test_layer5_handoff_packet_is_real PASSED
tests/test_cc00_path.py::test_memory_store_absolute_import_fix PASSED
tests/test_cc00_path.py::test_swarm_orchestrator_internal_relative_imports_resolve PASSED
tests/test_rag_tool.py::test_public_role_cannot_see_staff_only_document PASSED
tests/test_rag_tool.py::test_staff_role_sees_both PASSED
tests/test_rag_tool.py::test_tool_signature_has_no_role_parameter PASSED
tests/test_rag_tool.py::test_top_k_is_capped_at_ten PASSED
tests/test_research_assistant_graph.py::test_graph_pauses_at_the_approval_gate PASSED
tests/test_research_assistant_graph.py::test_approval_writes_the_file PASSED
tests/test_research_assistant_graph.py::test_rejection_writes_nothing PASSED
tests/test_research_assistant_graph.py::test_acl_role_propagates_into_retrieval PASSED
tests/test_research_assistant_graph.py::test_handoff_packet_is_real_and_validated PASSED
tests/test_research_assistant_graph.py::test_filename_sanitization_handles_windows_invalid_characters PASSED

============================= 25 passed in 2.60s ==============================
```

## Try it

```powershell
.venv/Scripts/python.exe scripts/run_demo.py "What does LangGraph provide?" --auto-approve
```

Runs fully offline (`FakeListChatModel`), retrieves from a small in-process corpus, drafts a finding
through the full governance middleware stack, auto-approves the write, and produces a real file under
`.demo-output/reports/` plus a real SQLite checkpoint under `.demo-output/checkpoints.sqlite` (both
gitignored). Drop `--auto-approve` to be prompted interactively instead. Pass `--role staff` to see
the ACL filter admit a document a `public` role cannot retrieve.

`--real` routes the draft step through `init_chat_model("anthropic:claude-sonnet-5")` if
`ANTHROPIC_API_KEY` is set. **This path was not executed in this deliverable** — no credentials were
available — and the model identifier string was not confirmed against the pinned
`langchain-anthropic` version. Confirm both before relying on it.

---

## Project layout

```
enterprise-examples/
├── README.md                        ← this file
├── pyproject.toml                   ← pytest config + packaging metadata
├── requirements.txt / .lock.txt     ← deps; lock file is what was actually installed
├── src/cc00_langchain/
│   ├── cc00_path.py                 ← Finding-11 loader: real CC-00 code, one process
│   ├── asgf.py                      ← the six governance middleware classes + CC00AgentState
│   ├── telemetry.py                 ← span recorder (in-memory by default; real OTel if installed)
│   ├── rag_tool.py                  ← RAGPipeline as a tool, ACL role closure-bound (Finding 14)
│   └── graphs/research_assistant.py ← the flagship: plan → retrieve → draft → gate → write/discard
├── tests/                           ← 25 tests, all real executions, see § above
└── scripts/run_demo.py              ← CLI entry point
```

## Relationship to the Markdown examples

| Markdown (`supporting/`)                                         | This project                                                                             | Relationship                                                                                                                                                                                                   |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `00 §6` CC-00 import workaround                                  | `src/cc00_langchain/cc00_path.py`                                                        | Same design, now executed and tested                                                                                                                                                                           |
| `00 §7` governance middleware kit                                | `src/cc00_langchain/asgf.py`                                                             | Same intent; two real deviations documented above                                                                                                                                                              |
| `04 §5` ACL closure                                              | `src/cc00_langchain/rag_tool.py`                                                         | Same design, executed and tested                                                                                                                                                                               |
| `06` ecosystem integration example                               | `src/cc00_langchain/graphs/research_assistant.py`                                        | A runnable **subset** — simpler topology (no multi-specialist supervisor), same governance/interrupt/ACL mechanics, structured output out of scope (see table above)                                           |
| `01`–`03` LangChain / LangGraph / DeepAgents individual examples | Installed and importable (`requirements.lock.txt`); DeepAgents not exercised by any test | Where this project's code overlaps their patterns (middleware, `interrupt()`, `create_agent`), it is executed. Where it doesn't (DeepAgents subagents, MCP bridging), the Markdown remains the only reference. |

Where the two disagree, **this project is correct** — the Markdown documents are append-only per the
telescope convention and are not retroactively rewritten; their own module docstrings note where this
project's execution changed the design.

---

**Author:** Dr. Elias Vance, CC-00 Laboratory Director
**Date:** 2026-07-27
