"""
Tests for the 2026-08-09 embedder-path reliability fixes in server.py and
embedder_client.py:

1. _cleanup_stale_sibling_processes() -- terminates other live processes
   running this exact server.py before proceeding, on-demand only (runs
   once at module-import time, gated off entirely during tests via
   AGENT_MEMORY_ENABLE_SIBLING_CLEANUP -- see conftest.py). Includes a
   minimum-age gate (_SIBLING_CLEANUP_MIN_AGE_S) so two processes spawned
   near-simultaneously never treat each other as stale.
2. Widened on-demand cold-start timeout budgets
   (embedder_client.STARTUP_WAIT_TIMEOUT_S, server._EMBEDDER_LOAD_TIMEOUT_S)
   matched to values actually observed live on 2026-08-09.
3. _get_embedder_unavailable_reason()'s "starting (retry shortly)" wording
   for a recently-launched, not-yet-confirmed-ready embedder-service, versus
   a flat "unavailable" once the grace window has elapsed.

No live Qdrant instance, live embedder-service, or real subprocess spawn is
required for anything in this file -- subprocess.run is monkeypatched at the
module level exactly like server.py's other collaborators are elsewhere in
this suite.
"""
import subprocess
import sys
import time

import pytest


# ---------------------------------------------------------------------------
# _cleanup_stale_sibling_processes
# ---------------------------------------------------------------------------


class TestCleanupStaleSiblingProcesses:
    def test_skipped_when_disabled_via_env_var(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "false")
        called = []
        monkeypatch.setattr(
            agent_memory_server.subprocess, "run", lambda *a, **k: called.append(1)
        )
        agent_memory_server._cleanup_stale_sibling_processes()
        assert called == []

    def test_skipped_on_non_windows(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server.sys, "platform", "linux")
        called = []
        monkeypatch.setattr(
            agent_memory_server.subprocess, "run", lambda *a, **k: called.append(1)
        )
        agent_memory_server._cleanup_stale_sibling_processes()
        assert called == []

    def test_terminates_stale_siblings_but_never_self(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server.sys, "platform", "win32")
        monkeypatch.setattr(
            agent_memory_server, "_SELF_PID", 111, raising=False
        )

        scan_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="111\n222\n333\n", stderr=""
        )
        killed_pids = []

        def _fake_run(cmd, **kwargs):
            joined = " ".join(cmd)
            if "Select-Object -ExpandProperty ProcessId" in joined or "Get-CimInstance" in joined:
                return scan_result
            if "Stop-Process" in joined:
                for pid in (222, 333):
                    if f"-Id {pid}" in joined:
                        killed_pids.append(pid)
                return subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
            raise AssertionError(f"unexpected command: {joined}")

        monkeypatch.setattr(agent_memory_server.subprocess, "run", _fake_run)
        agent_memory_server._cleanup_stale_sibling_processes()

        assert sorted(killed_pids) == [222, 333]
        assert 111 not in killed_pids  # self must never be targeted

    def test_no_siblings_found_is_a_noop(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server.sys, "platform", "win32")

        scan_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=f"{agent_memory_server._SELF_PID}\n", stderr=""
        )
        stop_process_calls = []

        def _fake_run(cmd, **kwargs):
            joined = " ".join(cmd)
            if "Stop-Process" in joined:
                stop_process_calls.append(joined)
            return scan_result

        monkeypatch.setattr(agent_memory_server.subprocess, "run", _fake_run)
        agent_memory_server._cleanup_stale_sibling_processes()
        assert stop_process_calls == []

    def test_never_raises_when_scan_itself_fails(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server.sys, "platform", "win32")

        def _raise(*a, **k):
            raise OSError("powershell not found")

        monkeypatch.setattr(agent_memory_server.subprocess, "run", _raise)
        # Must not raise.
        agent_memory_server._cleanup_stale_sibling_processes()

    def test_never_raises_when_scan_itself_times_out(self, agent_memory_server, monkeypatch):
        """_call_with_hard_timeout is specifically built to interrupt a hung
        subprocess.run call -- exercise the exact exception type it's meant
        to catch (subprocess.TimeoutExpired), not just a generic OSError."""
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server.sys, "platform", "win32")

        def _raise(cmd, **kwargs):
            raise subprocess.TimeoutExpired(cmd=cmd, timeout=15)

        monkeypatch.setattr(agent_memory_server.subprocess, "run", _raise)
        # Must not raise.
        agent_memory_server._cleanup_stale_sibling_processes()

    def test_never_raises_when_a_single_kill_fails(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server.sys, "platform", "win32")
        monkeypatch.setattr(agent_memory_server, "_SELF_PID", 111, raising=False)

        scan_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="111\n222\n", stderr=""
        )

        def _fake_run(cmd, **kwargs):
            joined = " ".join(cmd)
            if "Stop-Process" in joined:
                raise subprocess.TimeoutExpired(cmd=cmd, timeout=10)
            return scan_result

        monkeypatch.setattr(agent_memory_server.subprocess, "run", _fake_run)
        # Must not raise even though the kill itself times out.
        agent_memory_server._cleanup_stale_sibling_processes()

    def test_nonzero_scan_returncode_is_treated_as_unusable(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server.sys, "platform", "win32")

        scan_result = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="boom")
        stop_process_calls = []

        def _fake_run(cmd, **kwargs):
            joined = " ".join(cmd)
            if "Stop-Process" in joined:
                stop_process_calls.append(joined)
            return scan_result

        monkeypatch.setattr(agent_memory_server.subprocess, "run", _fake_run)
        agent_memory_server._cleanup_stale_sibling_processes()
        assert stop_process_calls == []

    def test_scan_command_uses_relative_suffix_not_absolute_path(
        self, agent_memory_server, monkeypatch
    ):
        """
        Asserts the actual PowerShell command text contains the relative
        suffix (not the absolute path) plus the backslash-normalizing
        -replace, rather than trusting a mocked subprocess.run alone --
        that mock can't prove anything about the command text itself.
        """
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server.sys, "platform", "win32")
        captured_commands = []

        def _fake_run(cmd, **kwargs):
            captured_commands.append(" ".join(cmd))
            return subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        monkeypatch.setattr(agent_memory_server.subprocess, "run", _fake_run)
        agent_memory_server._cleanup_stale_sibling_processes()

        assert captured_commands, "scan command was never issued"
        scan_cmd = captured_commands[0]
        assert agent_memory_server._AGENT_MEMORY_SERVER_SCRIPT not in scan_cmd
        assert agent_memory_server._AGENT_MEMORY_RELATIVE_SUFFIX in scan_cmd
        assert "-replace" in scan_cmd


class TestSiblingCleanupMinAge:
    """
    The scan must exclude any sibling younger than
    _SIBLING_CLEANUP_MIN_AGE_S, so two processes spawned near-
    simultaneously by the host never treat each other as stale.
    """

    def test_default_min_age_is_200_seconds(self, agent_memory_server, monkeypatch):
        monkeypatch.delenv("AGENT_MEMORY_SIBLING_CLEANUP_MIN_AGE_S", raising=False)
        assert agent_memory_server._resolve_sibling_cleanup_min_age_s() == 200.0

    def test_invalid_override_falls_back_to_default(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_SIBLING_CLEANUP_MIN_AGE_S", "not-a-number")
        assert agent_memory_server._resolve_sibling_cleanup_min_age_s() == 200.0

    def test_override_below_floor_is_clamped(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_SIBLING_CLEANUP_MIN_AGE_S", "-5")
        assert (
            agent_memory_server._resolve_sibling_cleanup_min_age_s()
            == agent_memory_server._SIBLING_CLEANUP_MIN_AGE_FLOOR_S
        )

    def test_nan_override_is_clamped_to_floor(self, agent_memory_server, monkeypatch):
        """NaN comparisons are always False, so a plain `value < floor` check
        would silently let NaN through uncaught -- regression for the
        2026-08-09 adversarial finding. `float("nan")` parses without
        raising, so this must be caught by the floor check, not the
        except-ValueError branch."""
        monkeypatch.setenv("AGENT_MEMORY_SIBLING_CLEANUP_MIN_AGE_S", "nan")
        result = agent_memory_server._resolve_sibling_cleanup_min_age_s()
        assert result == agent_memory_server._SIBLING_CLEANUP_MIN_AGE_FLOOR_S

    def test_valid_override_above_floor_is_respected(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_SIBLING_CLEANUP_MIN_AGE_S", "60")
        assert agent_memory_server._resolve_sibling_cleanup_min_age_s() == 60.0

    def test_scan_command_includes_age_filter(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server.sys, "platform", "win32")
        captured_commands = []

        def _fake_run(cmd, **kwargs):
            captured_commands.append(" ".join(cmd))
            return subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        monkeypatch.setattr(agent_memory_server.subprocess, "run", _fake_run)
        agent_memory_server._cleanup_stale_sibling_processes()

        assert captured_commands, "scan command was never issued"
        scan_cmd = captured_commands[0]
        assert "CreationDate" in scan_cmd
        assert "TotalSeconds" in scan_cmd
        assert "-gt" in scan_cmd
        assert str(agent_memory_server._SIBLING_CLEANUP_MIN_AGE_S) in scan_cmd


class TestSiblingMatchFilterRealPowerShellSemantics:
    """
    Actually invokes PowerShell against the exact filter clause production
    builds (_build_sibling_match_filter_clause), substituting a synthetic
    $_ object for the pipeline variable -- not a hand-duplicated copy of
    the logic, so these tests cannot silently drift from what production
    actually runs. A mocked subprocess.run cannot catch a defect living in
    the PowerShell expression text itself. Skipped on non-Windows
    platforms.
    """

    @staticmethod
    def _matches(
        agent_memory_server,
        command_line: str,
        age_seconds: float,
        min_age: float = 45.0,
        self_parent_pid: int = 9999,
        candidate_parent_pid: int = 9999,
    ) -> bool:
        suffix = agent_memory_server._AGENT_MEMORY_RELATIVE_SUFFIX.replace("'", "''")
        filter_clause = agent_memory_server._build_sibling_match_filter_clause(suffix, min_age, self_parent_pid)
        escaped_cmdline = command_line.replace("'", "''")
        ps_command = (
            "$_ = [PSCustomObject]@{ CommandLine = '" + escaped_cmdline + "'; "
            "CreationDate = (Get-Date).AddSeconds(-" + repr(age_seconds) + "); "
            "ParentProcessId = " + repr(int(candidate_parent_pid)) + " }; "
            "if (" + filter_clause + ") { Write-Output 'MATCH' } else { Write-Output 'NOMATCH' }"
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=15,
        )
        # "MATCH" in "NOMATCH" is also True -- must compare the exact token.
        return result.stdout.strip() == "MATCH"

    def test_direct_relative_launch_old_enough_matches(self, agent_memory_server):
        if sys.platform != "win32":
            pytest.skip("Windows-only scan expression")
        cmdline = (
            "./core-component-00/mcp-servers/.venv/Scripts/python.exe "
            "./core-component-00/mcp-servers/agent-memory/server.py"
        )
        assert self._matches(agent_memory_server, cmdline, age_seconds=100.0) is True

    def test_absolute_windows_backslash_launch_matches(self, agent_memory_server):
        if sys.platform != "win32":
            pytest.skip("Windows-only scan expression")
        cmdline = (
            r"C:\Users\ASUS\Documents\Code\Local\AGENT-GLOBAL-BASE\core-component-00"
            r"\mcp-servers\.venv\Scripts\python.exe "
            r"C:\Users\ASUS\Documents\Code\Local\AGENT-GLOBAL-BASE\core-component-00"
            r"\mcp-servers\agent-memory\server.py"
        )
        assert self._matches(agent_memory_server, cmdline, age_seconds=100.0) is True

    def test_unrelated_file_does_not_match(self, agent_memory_server):
        if sys.platform != "win32":
            pytest.skip("Windows-only scan expression")
        cmdline = (
            "./core-component-00/mcp-servers/.venv/Scripts/python.exe "
            "./core-component-00/mcp-servers/workspace-knowledge/server.py"
        )
        assert self._matches(agent_memory_server, cmdline, age_seconds=100.0) is False

    def test_file_referenced_as_non_trailing_argument_does_not_match(self, agent_memory_server):
        """A pytest/lint invocation that references this file among several
        arguments (not as the launched script) must never be mistaken for
        a direct launch of it."""
        if sys.platform != "win32":
            pytest.skip("Windows-only scan expression")
        cmdline = (
            "./core-component-00/mcp-servers/.venv/Scripts/python.exe -m pytest "
            "agent-memory/tests/test_server.py agent-memory/server.py agent-memory/write_tool.py"
        )
        assert self._matches(agent_memory_server, cmdline, age_seconds=100.0) is False

    def test_younger_than_threshold_does_not_match(self, agent_memory_server):
        if sys.platform != "win32":
            pytest.skip("Windows-only scan expression")
        cmdline = (
            "./core-component-00/mcp-servers/.venv/Scripts/python.exe "
            "./core-component-00/mcp-servers/agent-memory/server.py"
        )
        assert self._matches(agent_memory_server, cmdline, age_seconds=0.7, min_age=45.0) is False

    def test_just_under_threshold_does_not_match(self, agent_memory_server):
        # A literal exact-45.0s boundary isn't reliably testable via two
        # separate Get-Date calls with intervening script execution time --
        # this half-second margin approximates the boundary deterministically.
        if sys.platform != "win32":
            pytest.skip("Windows-only scan expression")
        cmdline = (
            "./core-component-00/mcp-servers/.venv/Scripts/python.exe "
            "./core-component-00/mcp-servers/agent-memory/server.py"
        )
        assert self._matches(agent_memory_server, cmdline, age_seconds=44.5, min_age=45.0) is False

    def test_just_over_threshold_matches(self, agent_memory_server):
        if sys.platform != "win32":
            pytest.skip("Windows-only scan expression")
        cmdline = (
            "./core-component-00/mcp-servers/.venv/Scripts/python.exe "
            "./core-component-00/mcp-servers/agent-memory/server.py"
        )
        assert self._matches(agent_memory_server, cmdline, age_seconds=45.5, min_age=45.0) is True

    def test_older_than_threshold_matches(self, agent_memory_server):
        if sys.platform != "win32":
            pytest.skip("Windows-only scan expression")
        cmdline = (
            "./core-component-00/mcp-servers/.venv/Scripts/python.exe "
            "./core-component-00/mcp-servers/agent-memory/server.py"
        )
        assert self._matches(agent_memory_server, cmdline, age_seconds=3600.0, min_age=45.0) is True

    def test_different_parent_process_id_does_not_match(self, agent_memory_server):
        """A same-suffix process spawned by a DIFFERENT host process (e.g. a
        separate checkout or git worktree session, per CLAUDE.md section 6)
        must never be matched, even when the path suffix and age both
        qualify -- this is the 2026-08-09 cross-checkout finding."""
        if sys.platform != "win32":
            pytest.skip("Windows-only scan expression")
        cmdline = (
            "./core-component-00/mcp-servers/.venv/Scripts/python.exe "
            "./core-component-00/mcp-servers/agent-memory/server.py"
        )
        assert self._matches(
            agent_memory_server, cmdline, age_seconds=3600.0, min_age=45.0,
            self_parent_pid=9999, candidate_parent_pid=1234,
        ) is False

    def test_same_parent_process_id_matches(self, agent_memory_server):
        if sys.platform != "win32":
            pytest.skip("Windows-only scan expression")
        cmdline = (
            "./core-component-00/mcp-servers/.venv/Scripts/python.exe "
            "./core-component-00/mcp-servers/agent-memory/server.py"
        )
        assert self._matches(
            agent_memory_server, cmdline, age_seconds=3600.0, min_age=45.0,
            self_parent_pid=9999, candidate_parent_pid=9999,
        ) is True


# ---------------------------------------------------------------------------
# Widened timeout budgets
# ---------------------------------------------------------------------------


class TestWidenedTimeoutBudgets:
    def test_embedder_service_startup_wait_timeout_widened(self):
        sys.path.insert(
            0,
            str(
                __import__("pathlib").Path(__file__).resolve().parents[2] / "_shared"
            ),
        )
        import embedder_client

        assert embedder_client.STARTUP_WAIT_TIMEOUT_S == 90.0

    def test_in_process_fallback_load_timeout_widened(self, agent_memory_server):
        assert agent_memory_server._EMBEDDER_LOAD_TIMEOUT_S == 90.0


# ---------------------------------------------------------------------------
# _get_embedder_unavailable_reason "starting (retry shortly)" wording
# ---------------------------------------------------------------------------


class TestEmbedderUnavailableReasonWording:
    def test_recently_started_and_unavailable_reads_as_starting(
        self, reset_embedder_globals
    ):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = True
        m._embedder_service_state = "unavailable"
        m._embedder_service_process_started_at = time.time()
        reason = m._get_embedder_unavailable_reason()
        assert "starting (retry shortly)" in reason
        assert "embedder-service: unavailable" not in reason

    def test_grace_window_expired_reads_as_unavailable(self, reset_embedder_globals):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = True
        m._embedder_service_state = "unavailable"
        m._embedder_service_process_started_at = (
            time.time() - m._EMBEDDER_SERVICE_STARTING_GRACE_S - 1.0
        )
        reason = m._get_embedder_unavailable_reason()
        assert "embedder-service: unavailable" in reason
        assert "starting (retry shortly)" not in reason

    def test_ready_state_is_never_relabeled(self, reset_embedder_globals):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = True
        m._embedder_service_state = "ready"
        m._embedder_service_process_started_at = time.time()
        reason = m._get_embedder_unavailable_reason()
        assert "embedder-service: ready" in reason

    def test_disabled_service_path_unaffected(self, reset_embedder_globals):
        m = reset_embedder_globals
        m.EMBEDDER_SERVICE_ENABLED = False
        m._embedder_state = "not started"
        reason = m._get_embedder_unavailable_reason()
        assert "retry shortly" in reason
        assert "embedder-service" not in reason
