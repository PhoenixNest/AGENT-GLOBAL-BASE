"""
Tests for reflective_dispatch_helper — the Evaluator wrapping SwarmOrchestrator's
already-shipped evaluate_subtask_result()/_reflection_note_for_attempt() for real
subagent dispatches.

Covers: passing verdict passthrough, failing verdict reflection-note formatting,
retry-cap enforcement via retries_remaining, malformed/missing checks handled
without raising, and the never-raises degrade path itself (simulated internal
failure) returning passed: True. A second class, TestCLIInvocation,
additionally exercises the real `uv run` subprocess contract — this is
wiring-level verification of the CLI entry point, not a substitute for
verifying the underlying evaluate_dispatch() logic covered above.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations import reflective_dispatch_helper as helper

_HELPER_PATH = Path(__file__).parent.parent / "implementations" / "reflective_dispatch_helper.py"

# Disables this module's own pilot-invocation telemetry for every CLI-level
# subprocess test below, so repeated pytest runs don't inflate the real
# invocation count the telemetry is meant to track.
_NO_TELEMETRY_ENV = {**os.environ, "REFLECTIVE_DISPATCH_HELPER_TELEMETRY": "0"}


class TestPassingVerdict:
    def test_passing_verdict_passes_through(self):
        response = helper.evaluate_dispatch(
            task_description="Implement rate-limiting middleware.",
            gate_criteria=["All unit tests pass", "No new lint errors"],
            checks={"All unit tests pass": True, "No new lint errors": True},
            attempt_number=1,
        )
        assert response["passed"] is True
        assert "All gate_criteria satisfied" in response["rationale"]
        assert response["reflection_note"] is None
        assert response["retries_remaining"] == 1

    def test_no_gate_criteria_passes_through_as_ungated(self):
        response = helper.evaluate_dispatch(
            task_description="Open-ended exploratory research task.",
            gate_criteria=[],
            checks={},
            attempt_number=1,
        )
        assert response["passed"] is True
        assert "Evaluate skipped" in response["rationale"]


class TestFailingVerdict:
    def test_failing_verdict_produces_reflection_note(self):
        response = helper.evaluate_dispatch(
            task_description="Implement rate-limiting middleware.",
            gate_criteria=["All unit tests in test_rate_limiter.py pass", "No new lint errors introduced (ruff clean)"],
            checks={
                "All unit tests in test_rate_limiter.py pass": False,
                "No new lint errors introduced (ruff clean)": True,
            },
            attempt_number=1,
            max_reflection_retries=2,
        )
        assert response["passed"] is False
        assert "All unit tests in test_rate_limiter.py pass" in response["rationale"]
        assert response["reflection_note"] is not None
        assert "All unit tests in test_rate_limiter.py pass" in response["reflection_note"]
        # Not the final attempt (attempt 1 of 2) — no "final retry" framing yet.
        assert "final retry" not in response["reflection_note"]

    def test_final_attempt_reflection_note_asks_for_different_approach(self):
        response = helper.evaluate_dispatch(
            task_description="Implement rate-limiting middleware.",
            gate_criteria=["All unit tests pass"],
            checks={"All unit tests pass": False},
            attempt_number=2,
            max_reflection_retries=2,
        )
        assert response["passed"] is False
        assert response["retries_remaining"] == 0
        assert "final retry" in response["reflection_note"]
        assert "genuinely different approach" in response["reflection_note"]


class TestRetryCapAccounting:
    @pytest.mark.parametrize(
        "attempt_number,max_reflection_retries,expected_retries_remaining",
        [
            (1, 2, 1),
            (2, 2, 0),
            (1, 0, 0),
            (3, 2, 0),
        ],
    )
    def test_retries_remaining_computed_correctly(
        self, attempt_number, max_reflection_retries, expected_retries_remaining
    ):
        response = helper.evaluate_dispatch(
            task_description="A task.",
            gate_criteria=["A criterion"],
            checks={"A criterion": False},
            attempt_number=attempt_number,
            max_reflection_retries=max_reflection_retries,
        )
        assert response["retries_remaining"] == expected_retries_remaining


class TestMalformedInputHandledWithoutRaising:
    def test_missing_checks_treated_as_empty(self):
        response = helper.evaluate_dispatch(
            task_description="A task.",
            gate_criteria=["A criterion never mentioned anywhere"],
            checks=None,
            attempt_number=1,
        )
        assert response["passed"] is False

    def test_non_dict_checks_degrades_not_raises(self):
        response = helper.evaluate_dispatch(
            task_description="A task.",
            gate_criteria=["A criterion"],
            checks="not-a-dict",
            attempt_number=1,
        )
        assert response["passed"] is True
        assert "helper unavailable" in response["rationale"]

    def test_invalid_attempt_number_degrades_not_raises(self):
        response = helper.evaluate_dispatch(
            task_description="A task.",
            gate_criteria=["A criterion"],
            checks={"A criterion": True},
            attempt_number=0,
        )
        assert response["passed"] is True
        assert "helper unavailable" in response["rationale"]
        assert response["retries_remaining"] == 0

    def test_non_numeric_attempt_number_degrades_not_raises(self):
        response = helper.evaluate_dispatch(
            task_description="A task.",
            gate_criteria=["A criterion"],
            checks={"A criterion": True},
            attempt_number="not-a-number",
        )
        assert response["passed"] is True
        assert "helper unavailable" in response["rationale"]


class TestNeverRaisesDegradePath:
    def test_internal_failure_in_loader_degrades_to_passed_true(self, monkeypatch):
        def _boom():
            raise RuntimeError("simulated swarm_orchestrator import failure")

        monkeypatch.setattr(helper, "_load_swarm_orchestrator_symbols", _boom)
        response = helper.evaluate_dispatch(
            task_description="A task.",
            gate_criteria=["A criterion"],
            checks={"A criterion": False},
            attempt_number=1,
        )
        assert response["passed"] is True
        assert "helper unavailable" in response["rationale"]
        assert "simulated swarm_orchestrator import failure" in response["rationale"]
        assert response["reflection_note"] is None
        assert response["retries_remaining"] == 0

    def test_internal_failure_in_evaluator_degrades_to_passed_true(self, monkeypatch):
        SubTask, _real_evaluate, note_fn = helper._load_swarm_orchestrator_symbols()

        def _boom(*_args, **_kwargs):
            raise RuntimeError("simulated evaluate_subtask_result failure")

        monkeypatch.setattr(
            helper,
            "_load_swarm_orchestrator_symbols",
            lambda: (SubTask, _boom, note_fn),
        )
        response = helper.evaluate_dispatch(
            task_description="A task.",
            gate_criteria=["A criterion"],
            checks={"A criterion": True},
            attempt_number=1,
        )
        assert response["passed"] is True
        assert "helper unavailable" in response["rationale"]


class TestStructuredStderrLogging:
    """Verifies every degrade path logs a structured stderr note (matching
    error_boundary.py's own log_warning shape) so a degrade is
    incident-traceable, without the log line ever leaking into stdout's
    pure-JSON contract."""

    def test_degrade_path_logs_warning_to_stderr(self, monkeypatch, capsys):
        monkeypatch.setattr(
            helper,
            "_load_swarm_orchestrator_symbols",
            lambda: (_ for _ in ()).throw(RuntimeError("simulated failure")),
        )
        helper.evaluate_dispatch(
            task_description="A task.",
            gate_criteria=["A criterion"],
            checks={"A criterion": False},
            attempt_number=1,
        )
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "[WARNING]" in captured.err
        assert "simulated failure" in captured.err

    def test_log_warning_never_raises_on_unusual_kwargs(self, capsys):
        class _Unprintable:
            def __str__(self):
                raise RuntimeError("cannot stringify")

        helper._log_warning("a message", reason=_Unprintable())
        captured = capsys.readouterr()
        assert captured.err == ""  # swallowed internally, never propagates

    def test_cli_malformed_stdin_logs_to_stderr_not_stdout(self):
        import subprocess

        proc = subprocess.run(
            ["uv", "run", str(_HELPER_PATH)],
            input="{not valid json",
            capture_output=True,
            text=True,
            timeout=60,
            env=_NO_TELEMETRY_ENV,
        )
        assert proc.returncode == 0
        response = json.loads(proc.stdout)
        assert response["passed"] is True
        assert "[WARNING]" in proc.stderr


class TestInvocationTelemetry:
    """A simple invocation counter so how often the Execute phase actually
    calls the helper is visible, not
    assumed. Covers: a record is appended per real call, the env-var opt-out
    this module's own CLI tests rely on, and that a write failure never
    raises or blocks the response — telemetry is best-effort, same posture
    as _log_warning."""

    def test_record_invocation_appends_jsonl_line(self, tmp_path, monkeypatch):
        telemetry_file = tmp_path / "invocations.jsonl"
        monkeypatch.setattr(helper, "_TELEMETRY_PATH", telemetry_file)
        monkeypatch.delenv("REFLECTIVE_DISPATCH_HELPER_TELEMETRY", raising=False)

        helper._record_invocation({"passed": True, "retries_remaining": 1, "rationale": "ok"})
        helper._record_invocation(
            {"passed": True, "retries_remaining": 0, "rationale": "helper unavailable: boom"}
        )

        lines = telemetry_file.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        first, second = (json.loads(line) for line in lines)
        assert first["passed"] is True
        assert first["degraded"] is False
        assert second["degraded"] is True

    def test_telemetry_disabled_via_env_var(self, tmp_path, monkeypatch):
        telemetry_file = tmp_path / "invocations.jsonl"
        monkeypatch.setattr(helper, "_TELEMETRY_PATH", telemetry_file)
        monkeypatch.setenv("REFLECTIVE_DISPATCH_HELPER_TELEMETRY", "0")

        helper._record_invocation({"passed": True, "retries_remaining": 1, "rationale": "ok"})

        assert not telemetry_file.exists()

    def test_telemetry_write_failure_never_raises(self, monkeypatch):
        # A directory where a file path is expected — mkdir/open will fail.
        monkeypatch.setattr(helper, "_TELEMETRY_PATH", Path("."))
        monkeypatch.delenv("REFLECTIVE_DISPATCH_HELPER_TELEMETRY", raising=False)

        helper._record_invocation({"passed": True, "retries_remaining": 1, "rationale": "ok"})  # must not raise


class TestReadRequest:
    def test_malformed_json_returns_none(self, monkeypatch):
        import io

        assert helper._read_request(io.StringIO("{not valid json")) is None

    def test_empty_stdin_returns_none(self):
        import io

        assert helper._read_request(io.StringIO("")) is None

    def test_non_object_json_returns_none(self):
        import io

        assert helper._read_request(io.StringIO("[1, 2, 3]")) is None

    def test_valid_object_parsed(self):
        import io

        payload = helper._read_request(io.StringIO(json.dumps({"attempt_number": 1})))
        assert payload == {"attempt_number": 1}


class TestCLIInvocation:
    """Real subprocess invocation via `uv run`. Verifies the CLI wiring
    genuinely works end to end (stdin JSON in, stdout JSON out, exit code
    always 0) — not a substitute for the unit tests above, which cover the
    underlying evaluate_dispatch() logic; this class only checks the process
    boundary, not argument/error-reporting conventions."""

    def _run(self, stdin_text: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["uv", "run", str(_HELPER_PATH)],
            input=stdin_text,
            capture_output=True,
            text=True,
            timeout=60,
            env=_NO_TELEMETRY_ENV,
        )

    def test_cli_passing_verdict_via_uv_run(self):
        request = {
            "task_description": "Implement rate-limiting middleware.",
            "gate_criteria": ["All unit tests pass"],
            "checks": {"All unit tests pass": True},
            "attempt_number": 1,
        }
        proc = self._run(json.dumps(request))
        assert proc.returncode == 0, proc.stderr
        response = json.loads(proc.stdout)
        assert response["passed"] is True

    def test_cli_failing_verdict_via_uv_run(self):
        request = {
            "task_description": "Implement rate-limiting middleware.",
            "gate_criteria": ["All unit tests pass"],
            "checks": {"All unit tests pass": False},
            "attempt_number": 1,
            "max_reflection_retries": 2,
        }
        proc = self._run(json.dumps(request))
        assert proc.returncode == 0, proc.stderr
        response = json.loads(proc.stdout)
        assert response["passed"] is False
        assert response["retries_remaining"] == 1
        assert response["reflection_note"] is not None

    def test_cli_malformed_stdin_exits_zero_and_degrades(self):
        proc = self._run("{not valid json")
        assert proc.returncode == 0, proc.stderr
        response = json.loads(proc.stdout)
        assert response["passed"] is True
        assert "helper unavailable" in response["rationale"]

    def test_cli_empty_stdin_exits_zero_and_degrades(self):
        proc = self._run("")
        assert proc.returncode == 0, proc.stderr
        response = json.loads(proc.stdout)
        assert response["passed"] is True
