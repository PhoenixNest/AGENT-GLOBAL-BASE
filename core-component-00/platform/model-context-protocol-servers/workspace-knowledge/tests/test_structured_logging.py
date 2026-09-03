"""
Tests for R4 (2026-09-02) — structured per-call audit logging around each
@mcp.tool() function's entry/exit. See server.py's `_log_tool_call`/
`_call_outcome` and platform/benchmarks/model-context-protocol-servers/
2026-09-01-mcp-servers-enterprise-assessment/enterprise-assessment.md (B3/R4)
for the gap this closes. Mirrors
agent-memory/tests/test_structured_logging.py's coverage shape, adapted to
this server's own failure-signaling conventions ({"error": ...} /
{"status": "error", ...} rather than agent-memory's {"degraded": True, ...}).

Covers, per the remediation item's own acceptance bar: at least one success
and one failure case with expected fields actually emitted, plus the
argument-redaction discipline (no raw search query text ever reaches a log
record — only its length).

Import pattern (bare `import server` after inserting this server's own root
onto sys.path) matches the existing convention in this directory —
test_search_tier_degradation.py and test_upsert_delete_ordering_fix.py both
do the same, and there is no conftest.py fixture here yet (unlike
agent-memory/tests/conftest.py's importlib-based `agent_memory_server`
fixture) to add one to.
"""
import inspect
import logging
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import server  # noqa: E402


class TestLogToolCallDecoratorInIsolation:
    """Exercises `_log_tool_call` directly against small standalone
    functions, independent of any real tool's own return-value shape."""

    def test_success_call_emits_info_record_with_expected_fields(self, caplog):
        @server._log_tool_call()
        def _ok_tool(x: int) -> dict:
            return {"value": x * 2}

        with caplog.at_level(logging.INFO, logger="server"):
            result = _ok_tool(21)

        assert result == {"value": 42}
        records = [r for r in caplog.records if r.name == "server"]
        assert len(records) == 1
        record = records[0]
        assert record.levelno == logging.INFO
        assert record.tool_name == "_ok_tool"
        assert isinstance(record.duration_ms, float)
        assert record.duration_ms >= 0
        assert record.ok is True

    def test_raised_exception_emits_error_record_and_still_propagates(self, caplog):
        @server._log_tool_call()
        def _exploding_tool() -> dict:
            raise RuntimeError("simulated failure")

        with caplog.at_level(logging.ERROR, logger="server"):
            with pytest.raises(RuntimeError, match="simulated failure"):
                _exploding_tool()

        records = [r for r in caplog.records if r.name == "server"]
        assert len(records) == 1
        record = records[0]
        assert record.levelno == logging.ERROR
        assert record.tool_name == "_exploding_tool"
        assert record.ok is False
        assert "simulated failure" in record.reason
        assert record.exc_info is not None

    def test_error_key_result_emits_error_record_without_raising(self, caplog):
        """A tool that returns {"error": "..."} (this server's own
        failure-signaling shape — see retrieve_context/find_related_documents)
        without raising must still surface as an ERROR-level audit record."""

        @server._log_tool_call()
        def _failing_tool() -> dict:
            return {"error": "File not found: missing.md"}

        with caplog.at_level(logging.INFO, logger="server"):
            result = _failing_tool()

        assert "error" in result
        records = [r for r in caplog.records if r.name == "server"]
        assert len(records) == 1
        record = records[0]
        assert record.levelno == logging.ERROR
        assert record.ok is False
        assert record.reason == "File not found: missing.md"

    def test_degradation_reason_alone_is_not_an_error(self, caplog):
        """A non-null `_meta.degradation_reason` (tiered-search graceful
        degradation, e.g. HYBRID_QDRANT -> BM25) is expected, working
        behavior per B1 of the enterprise assessment ("Pass at parity") —
        _call_outcome deliberately does not treat it as a failure."""

        @server._log_tool_call()
        def _degraded_but_working_tool() -> dict:
            return {
                "results": [{"file": "x.md"}],
                "_meta": {"search_tier": "bm25", "degradation_reason": "Qdrant unreachable"},
            }

        with caplog.at_level(logging.INFO, logger="server"):
            _degraded_but_working_tool()

        records = [r for r in caplog.records if r.name == "server"]
        assert len(records) == 1
        assert records[0].levelno == logging.INFO
        assert records[0].ok is True

    def test_summarize_args_failure_never_breaks_the_call(self, caplog):
        def _broken_summarizer(*_args, **_kwargs):
            raise ValueError("summarizer bug")

        @server._log_tool_call(summarize_args=_broken_summarizer)
        def _tool(y: int) -> dict:
            return {"y": y}

        with caplog.at_level(logging.INFO, logger="server"):
            result = _tool(5)

        assert result == {"y": 5}
        records = [r for r in caplog.records if r.name == "server"]
        assert len(records) == 1
        assert records[0].ok is True


class TestCallOutcome:
    def test_non_dict_result_is_ok(self):
        assert server._call_outcome([1, 2, 3]) == (True, None)
        assert server._call_outcome(None) == (True, None)

    def test_error_key_is_error(self):
        ok, reason = server._call_outcome({"error": "boom"})
        assert ok is False
        assert reason == "boom"

    def test_status_error_is_error(self):
        ok, reason = server._call_outcome({"status": "error", "error": "boom"})
        assert ok is False
        assert reason == "boom"

    def test_status_skipped_is_ok(self):
        """upsert_document's SEARCH_BACKEND != qdrant no-op branch — a
        legitimate, expected outcome, not a failure."""
        ok, reason = server._call_outcome({"status": "skipped", "reason": "not qdrant backend"})
        assert ok is True

    def test_valid_false_is_ok(self):
        """validate_pipeline_document's structural-validation verdict is the
        tool's normal output, not a call failure."""
        ok, reason = server._call_outcome({"valid": False, "missing_sections": ["Stage"]})
        assert ok is True


class TestSearchDocsToolLogging:
    def test_success_case_logs_info_with_query_len_not_raw_query(self, monkeypatch, caplog):
        monkeypatch.setattr(
            server.engine,
            "_search_with_fallback",
            lambda query, top_k: [{"file": "x.md", "section": "", "score": 1.0, "snippet": "s"}],
        )
        monkeypatch.setattr(
            server.engine,
            "_meta_block",
            lambda: {"search_tier": "bm25", "degradation_reason": None},
        )

        secret_query = "find docs about jane.doe@example.com"
        with caplog.at_level(logging.INFO, logger="server"):
            result = server.search_docs(query=secret_query, top_k=5)

        assert result["results"]
        records = [
            r for r in caplog.records if r.name == "server" and getattr(r, "tool_name", None) == "search_docs"
        ]
        assert len(records) == 1
        record = records[0]
        assert record.levelno == logging.INFO
        assert record.ok is True
        assert "jane.doe@example.com" not in caplog.text
        assert record.call_args["query_len"] == len(secret_query)


class TestRetrieveContextToolLogging:
    def test_missing_file_logs_error_with_reason(self, tmp_path, monkeypatch, caplog):
        monkeypatch.setattr(server, "WORKSPACE_ROOT", tmp_path)
        monkeypatch.setattr(server.engine, "_meta_block", lambda: {"search_tier": "bm25"})

        with caplog.at_level(logging.INFO, logger="server"):
            result = server.retrieve_context(file_path="does-not-exist.md")

        assert "error" in result
        records = [
            r
            for r in caplog.records
            if r.name == "server" and getattr(r, "tool_name", None) == "retrieve_context"
        ]
        assert len(records) == 1
        record = records[0]
        assert record.levelno == logging.ERROR
        assert record.ok is False
        assert "does-not-exist.md" in record.reason
        # file_path itself is not content and is fine to log directly.
        assert record.call_args["file_path"] == "does-not-exist.md"


class TestAllToolsAreWrapped:
    """Confirms the decorator was actually applied to every @mcp.tool()
    function, not just a subset — the original R4 scope was "each
    @mcp.tool() function's entry/exit" for both servers."""

    TOOL_NAMES = [
        "search_docs",
        "retrieve_context",
        "list_indexed_files",
        "rebuild_index",
        "rebuild_status",
        "upsert_document",
        "summarize_context",
        "check_adr_precedent",
        "validate_pipeline_document",
        "find_related_documents",
        "list_research_by_topic",
        "agent_knowledge_brief",
        "health_check",
    ]

    @pytest.mark.parametrize("tool_name", TOOL_NAMES)
    def test_tool_is_wrapped_with_logging(self, tool_name):
        func = getattr(server, tool_name)
        assert hasattr(func, "__wrapped__"), f"{tool_name} is missing the logging wrapper"
        # Original signature must still be introspectable through the
        # wrapper (functools.wraps preserves __wrapped__), since FastMCP's
        # schema generation depends on it.
        assert inspect.signature(func).parameters is not None
