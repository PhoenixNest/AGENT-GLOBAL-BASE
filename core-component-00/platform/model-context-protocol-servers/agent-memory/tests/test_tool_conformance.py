"""
R5 (2026-09-02) — minimal conformance-check test gate for agent-memory's
registered `@mcp.tool()` endpoints (search_memory, health_check,
write_memory).

Per the 2026-09-01 MCP servers enterprise assessment
(platform/benchmarks/model-context-protocol-servers/
2026-09-01-mcp-servers-enterprise-assessment/enterprise-assessment.md,
B5/R5): agent-memory already had strong scenario-test coverage (9 test
files exercising write-gate, adversarial write-path evaluation, embedder
reliability, cross-server health comparison, and Tier 3 keyword search) but
no conformance-harness gate. This file adds exactly that gate — kept
deliberately minimal per R5's own scope ("defer load/pentest testing
entirely, that's explicitly out of scope for R5"):

1. Each tool's declared input schema — the JSON schema FastMCP generates
   from its signature/type hints at registration time, the same shape a
   real MCP client sees over the wire — is well-formed: a JSON-Schema
   object with a `properties` dict, every `required` name present in
   `properties`, and every property carrying a `type` or `anyOf`
   declaration.
2. Each tool's return shape for one basic call matches the key-set its own
   docstring documents. This is a *contract* check, not a *behavior* check
   — whether the right records come back under a given query/degradation
   scenario is already covered by test_server.py's and
   test_write_memory.py's scenario suites; this file only asks "does the
   documented shape hold at all."

Tools are registered into a throwaway scratch FastMCP instance rather than
read off the module's own `mcp` object, so this suite's schema assertions
never depend on AGENT_MEMORY_WRITE_TOOL_ENABLED — write_memory is only
*conditionally* registered on the real module-level `mcp`
(see tests/test_write_memory.py's TestActivationFlag) — and the same three
tools are checked here regardless of that flag's value in whatever
environment this suite runs in.

No live Qdrant instance or embedder-service is required: every test below
monkeypatches `_get_memory_client`/`_get_embedder` to None, exactly like
test_server.py's TestHealthCheckTool and test_write_memory.py's
TestWriteMemoryWrapperNeverRaises already do — this file follows that same
established dependency-injection pattern rather than inventing a new one.
"""
import asyncio
import sys
from pathlib import Path

import pytest

_AGENT_MEMORY_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_AGENT_MEMORY_DIR))

from fastmcp import FastMCP  # noqa: E402

TOOL_NAMES = ("search_memory", "health_check", "write_memory")


# ---------------------------------------------------------------------------
# Schema well-formedness
# ---------------------------------------------------------------------------


def _registered_tools(agent_memory_server):
    """Registers agent-memory's three tool-shaped functions into a fresh,
    throwaway FastMCP instance and returns {name: Tool}. This never touches
    the real module-level `agent_memory_server.mcp` registry, so it works
    identically regardless of whether write_memory is live there."""
    scratch = FastMCP("conformance-scratch")
    for fn in (
        agent_memory_server.search_memory,
        agent_memory_server.health_check,
        agent_memory_server.write_memory,
    ):
        scratch.tool()(fn)
    tools = asyncio.run(scratch.list_tools())
    return {t.name: t for t in tools}


def _assert_well_formed_json_schema(schema: dict) -> None:
    assert isinstance(schema, dict)
    assert schema.get("type") == "object"
    properties = schema.get("properties")
    assert isinstance(properties, dict)
    required = schema.get("required", [])
    assert isinstance(required, list)
    for name in required:
        assert name in properties, f"required param {name!r} missing from properties"
    for name, prop_schema in properties.items():
        assert isinstance(prop_schema, dict), f"property {name!r} schema is not an object"
        assert "type" in prop_schema or "anyOf" in prop_schema, (
            f"property {name!r} declares neither 'type' nor 'anyOf': {prop_schema!r}"
        )


@pytest.fixture(scope="module")
def tools(agent_memory_server):
    return _registered_tools(agent_memory_server)


class TestToolInputSchemasAreWellFormed:
    @pytest.mark.parametrize("tool_name", TOOL_NAMES)
    def test_all_three_tools_are_registerable(self, tools, tool_name):
        assert tool_name in tools

    @pytest.mark.parametrize("tool_name", TOOL_NAMES)
    def test_schema_is_well_formed(self, tools, tool_name):
        _assert_well_formed_json_schema(tools[tool_name].parameters)

    @pytest.mark.parametrize("tool_name", TOOL_NAMES)
    def test_tool_has_a_substantive_description(self, tools, tool_name):
        # FastMCP sources this from the function's docstring — an empty or
        # trivial description means a calling agent gets no usage contract
        # for the tool at all.
        description = tools[tool_name].description
        assert description
        assert len(description.strip()) > 20

    def test_search_memory_required_params_match_signature(self, tools):
        assert set(tools["search_memory"].parameters["required"]) == {"query", "memory_type"}

    def test_health_check_takes_no_params(self, tools):
        assert tools["health_check"].parameters.get("properties", {}) == {}
        assert tools["health_check"].parameters.get("required", []) == []

    def test_write_memory_required_params_match_signature(self, tools):
        assert set(tools["write_memory"].parameters["required"]) == {
            "content",
            "memory_type",
            "session_id",
            "provenance_source",
            "provenance_triggering_context_excerpt",
            "provenance_from_external_content",
            "provenance_confidence",
        }

    def test_write_memory_has_no_sacred_importance_or_status_param(self, tools):
        # Mirrors test_write_memory.py's TestSignature — repeated here as a
        # schema-level (not just inspect.signature-level) assertion, since
        # this is exactly the shape a real MCP client would see and could
        # attempt to pass args against.
        properties = tools["write_memory"].parameters["properties"]
        assert "sacred" not in properties
        assert "importance" not in properties
        assert "status" not in properties


# ---------------------------------------------------------------------------
# Return shape vs. each tool's own documented contract — one basic call
# each, not a scenario/behavior check (see test_server.py and
# test_write_memory.py for those).
# ---------------------------------------------------------------------------


class TestReturnShapeMatchesDocumentedContract:
    def test_search_memory_returns_documented_keys(self, agent_memory_server, monkeypatch):
        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: None)
        monkeypatch.setattr(agent_memory_server, "_get_embedder", lambda: None)
        result = agent_memory_server.search_memory(query="conformance ping", memory_type="semantic")
        # search_memory's docstring/graceful-degradation discipline:
        # results/count/degraded/reason are always present, regardless of
        # which failure mode was hit (unknown type, missing embedder,
        # unreachable Qdrant, ...). `tier` is documented as present on some
        # paths but is not part of the minimal always-present contract.
        assert {"results", "count", "degraded", "reason"} <= set(result.keys())
        assert isinstance(result["results"], list)
        assert isinstance(result["count"], int)
        assert isinstance(result["degraded"], bool)

    def test_health_check_returns_documented_keys(self, agent_memory_server, monkeypatch):
        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: None)
        result = agent_memory_server.health_check()
        assert set(result.keys()) == {"memory_instance", "search_capability", "write_rate_limiting"}
        assert isinstance(result["memory_instance"], dict)
        assert isinstance(result["search_capability"], dict)
        assert isinstance(result["write_rate_limiting"], dict)

    def test_write_memory_returns_documented_keys(self, agent_memory_server, monkeypatch):
        # write_tool._write_memory_impl's docstring: "Return shape (always
        # all five keys present): written, status, reason, record_id,
        # lane". This calls the real *registered* write_memory wrapper
        # (not just the testable core) to check the actual endpoint's
        # contract — with _get_memory_client short-circuited to None, the
        # call is rejected at write_tool.py's "client is None" check, which
        # runs before anything touches the real WriteConfirmationGate
        # marker file or a real QdrantClient (see write_tool.py's
        # _write_memory_impl ordering), so this exercises the registered
        # endpoint's contract with no live-infrastructure side effect.
        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: None)
        monkeypatch.setattr(agent_memory_server, "_get_embedder", lambda: None)
        result = agent_memory_server.write_memory(
            content="conformance check content",
            memory_type="semantic",
            session_id="conformance-test-session",
            provenance_source="conformance-test",
            provenance_triggering_context_excerpt="automated conformance check",
            provenance_from_external_content=False,
            provenance_confidence=0.5,
        )
        assert set(result.keys()) == {"written", "status", "reason", "record_id", "lane"}
        assert result["written"] is False
        assert isinstance(result["status"], str)
