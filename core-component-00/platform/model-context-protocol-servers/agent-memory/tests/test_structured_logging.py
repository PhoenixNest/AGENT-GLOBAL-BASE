"""
Tests for R4 (2026-09-02) — structured per-call audit logging around each
@mcp.tool() function's entry/exit. See server.py's `_log_tool_call`/
`_call_outcome` and platform/benchmarks/model-context-protocol-servers/
2026-09-01-mcp-servers-enterprise-assessment/enterprise-assessment.md (B3/R4)
for the gap this closes.

Covers, per the remediation item's own acceptance bar: at least one success
and one failure case with expected fields actually emitted, plus the
argument-redaction discipline (no raw `content`/`query` text ever reaches a
log record — only lengths and other non-content metadata).
"""
import logging

import pytest


class TestLogToolCallDecoratorInIsolation:
    """Exercises `_log_tool_call` directly against small standalone
    functions, independent of any real tool's own internal
    never-raises contract, so the decorator's own exception-path behavior
    (defense-in-depth — see its docstring) is covered even though none of
    this server's actual @mcp.tool() functions are expected to trigger it
    in normal operation."""

    def test_success_call_emits_info_record_with_expected_fields(
        self, agent_memory_server, caplog
    ):
        @agent_memory_server._log_tool_call()
        def _ok_tool(x: int) -> dict:
            return {"value": x * 2}

        with caplog.at_level(logging.INFO, logger="agent_memory_server"):
            result = _ok_tool(21)

        assert result == {"value": 42}
        records = [r for r in caplog.records if r.name == "agent_memory_server"]
        assert len(records) == 1
        record = records[0]
        assert record.levelno == logging.INFO
        assert record.tool_name == "_ok_tool"
        assert isinstance(record.duration_ms, float)
        assert record.duration_ms >= 0
        assert record.ok is True

    def test_raised_exception_emits_error_record_and_still_propagates(
        self, agent_memory_server, caplog
    ):
        @agent_memory_server._log_tool_call()
        def _exploding_tool() -> dict:
            raise RuntimeError("simulated failure")

        with caplog.at_level(logging.ERROR, logger="agent_memory_server"):
            with pytest.raises(RuntimeError, match="simulated failure"):
                _exploding_tool()

        records = [r for r in caplog.records if r.name == "agent_memory_server"]
        assert len(records) == 1
        record = records[0]
        assert record.levelno == logging.ERROR
        assert record.tool_name == "_exploding_tool"
        assert record.ok is False
        assert "simulated failure" in record.reason
        assert record.exc_info is not None

    def test_result_flagged_degraded_emits_error_record_without_raising(
        self, agent_memory_server, caplog
    ):
        """A tool that returns {"degraded": True, "reason": ...} (this
        module's own graceful-degradation contract — see search_memory)
        without raising must still surface as an ERROR-level audit record,
        not a silently-swallowed INFO one — this is exactly the outcome
        _call_outcome exists to detect."""

        @agent_memory_server._log_tool_call()
        def _degraded_tool() -> dict:
            return {"results": [], "degraded": True, "reason": "qdrant unreachable"}

        with caplog.at_level(logging.INFO, logger="agent_memory_server"):
            result = _degraded_tool()

        assert result["degraded"] is True
        records = [r for r in caplog.records if r.name == "agent_memory_server"]
        assert len(records) == 1
        record = records[0]
        assert record.levelno == logging.ERROR
        assert record.ok is False
        assert record.reason == "qdrant unreachable"

    def test_summarize_args_failure_never_breaks_the_call(self, agent_memory_server, caplog):
        """A broken summarizer must not prevent the underlying tool from
        running or being logged — see _log_tool_call's docstring."""

        def _broken_summarizer(*_args, **_kwargs):
            raise ValueError("summarizer bug")

        @agent_memory_server._log_tool_call(summarize_args=_broken_summarizer)
        def _tool(y: int) -> dict:
            return {"y": y}

        with caplog.at_level(logging.INFO, logger="agent_memory_server"):
            result = _tool(5)

        assert result == {"y": 5}
        records = [r for r in caplog.records if r.name == "agent_memory_server"]
        assert len(records) == 1
        assert records[0].ok is True


class TestCallOutcome:
    def test_non_dict_result_is_ok(self, agent_memory_server):
        assert agent_memory_server._call_outcome([1, 2, 3]) == (True, None)
        assert agent_memory_server._call_outcome(None) == (True, None)

    def test_degraded_true_is_error(self, agent_memory_server):
        ok, reason = agent_memory_server._call_outcome({"degraded": True, "reason": "x"})
        assert ok is False
        assert reason == "x"

    def test_status_error_is_error(self, agent_memory_server):
        ok, reason = agent_memory_server._call_outcome(
            {"status": "error", "reason": "boom"}
        )
        assert ok is False
        assert reason == "boom"

    def test_written_false_with_confirmation_required_is_ok(self, agent_memory_server):
        """write_memory's confirmation_required branch is a legitimate
        pending state, not a failure — see _call_outcome's docstring."""
        ok, reason = agent_memory_server._call_outcome(
            {"written": False, "status": "confirmation_required"}
        )
        assert ok is True
        assert reason is None

    def test_written_false_rejected_is_error(self, agent_memory_server):
        ok, reason = agent_memory_server._call_outcome(
            {"written": False, "status": "rejected", "reason": "invalid content"}
        )
        assert ok is False
        assert reason == "invalid content"

    def test_written_true_is_ok(self, agent_memory_server):
        ok, reason = agent_memory_server._call_outcome(
            {"written": True, "status": "active", "reason": None}
        )
        assert ok is True


class TestSearchMemoryToolLogging:
    """Real end-to-end coverage through the actual, registered search_memory
    tool — not just the decorator in isolation — for both a success and a
    failure (degraded) case."""

    def test_success_case_logs_info_with_query_len_not_raw_query(
        self, agent_memory_server, monkeypatch, caplog
    ):
        monkeypatch.setattr(agent_memory_server, "_get_memory_client", lambda: None)

        def _fake_embed(_text):
            return [0.0] * 384

        monkeypatch.setattr(agent_memory_server, "_get_embedder", lambda: _fake_embed)
        monkeypatch.setattr(
            agent_memory_server,
            "_search_reflection_with_status",
            lambda **_kw: agent_memory_server.SearchOutcome([], degraded=False),
        )

        with caplog.at_level(logging.INFO, logger="agent_memory_server"):
            result = agent_memory_server.search_memory(
                query="a very secret query about jane.doe@example.com",
                memory_type="reflection",
            )

        assert result["degraded"] is False
        records = [
            r
            for r in caplog.records
            if r.name == "agent_memory_server" and getattr(r, "tool_name", None) == "search_memory"
        ]
        assert len(records) == 1
        record = records[0]
        assert record.levelno == logging.INFO
        assert record.ok is True
        # The raw query text — including the embedded email address — must
        # never reach the log; only its length is captured.
        assert "jane.doe@example.com" not in caplog.text
        assert "a very secret query" not in caplog.text
        assert record.call_args["query_len"] == len(
            "a very secret query about jane.doe@example.com"
        )

    def test_unknown_memory_type_logs_error_with_reason(
        self, agent_memory_server, caplog
    ):
        with caplog.at_level(logging.INFO, logger="agent_memory_server"):
            result = agent_memory_server.search_memory(query="q", memory_type="not-a-type")

        assert result["degraded"] is True
        records = [
            r
            for r in caplog.records
            if r.name == "agent_memory_server" and getattr(r, "tool_name", None) == "search_memory"
        ]
        assert len(records) == 1
        record = records[0]
        assert record.levelno == logging.ERROR
        assert record.ok is False
        assert "unknown memory_type" in record.reason


class TestWriteMemoryArgSummaryRedaction:
    """write_memory's arguments are the highest PII-risk surface this
    server has (see pii_redaction.py) — verify the logging layer never logs
    raw content or provenance excerpt text, only lengths."""

    def test_summarizer_reports_lengths_not_content(self, agent_memory_server):
        summary = agent_memory_server._summarize_write_memory_args(
            content="my SSN is 123-45-6789",
            memory_type="semantic",
            session_id="sess-1",
            provenance_source="test",
            provenance_triggering_context_excerpt="excerpt with jane.doe@example.com",
            provenance_from_external_content=True,
            provenance_confidence=0.9,
        )
        assert summary["content_len"] == len("my SSN is 123-45-6789")
        assert summary["excerpt_len"] == len("excerpt with jane.doe@example.com")
        assert "content" not in summary
        assert "provenance_triggering_context_excerpt" not in summary
        assert all(
            "123-45-6789" not in str(v) and "jane.doe@example.com" not in str(v)
            for v in summary.values()
        )

    def test_write_memory_is_wrapped_with_logging(self, agent_memory_server):
        """write_memory is intentionally reassigned (not decorated on its
        `def`) to preserve the read-only-first static-analysis invariant —
        see server.py's comment just above the
        `write_memory = _log_tool_call(...)(write_memory)` line. Confirm the
        wrapping actually took effect (the module-level name is the wrapped
        callable, and its original signature is still introspectable)."""
        import inspect

        assert agent_memory_server.write_memory.__wrapped__ is not None
        params = set(inspect.signature(agent_memory_server.write_memory).parameters)
        assert params == {
            "content",
            "memory_type",
            "session_id",
            "provenance_source",
            "provenance_triggering_context_excerpt",
            "provenance_from_external_content",
            "provenance_confidence",
        }


class TestAllToolsAreWrapped:
    """Confirms the decorator was actually applied to every @mcp.tool()
    function (plus write_memory, conditionally registered) — the original
    R4 scope was "each @mcp.tool() function's entry/exit" for both
    servers."""

    TOOL_NAMES = ["search_memory", "health_check", "write_memory"]

    @pytest.mark.parametrize("tool_name", TOOL_NAMES)
    def test_tool_is_wrapped_with_logging(self, agent_memory_server, tool_name):
        import inspect

        func = getattr(agent_memory_server, tool_name)
        assert hasattr(func, "__wrapped__"), f"{tool_name} is missing the logging wrapper"
        assert inspect.signature(func).parameters is not None
