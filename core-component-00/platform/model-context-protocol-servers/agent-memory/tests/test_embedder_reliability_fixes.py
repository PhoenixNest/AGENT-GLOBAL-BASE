"""
Tests for the 2026-08-09 embedder-path reliability fixes in server.py and
embedder_client.py, plus the 2026-08-13 psutil cross-platform port of the
sibling-cleanup scan (see
core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md):

1. _cleanup_stale_sibling_processes() -- terminates other live processes
   running this exact server.py before proceeding, on-demand only (runs
   once at module-import time, gated off entirely during tests via
   AGENT_MEMORY_ENABLE_SIBLING_CLEANUP -- see conftest.py). Includes a
   minimum-age gate (_SIBLING_CLEANUP_MIN_AGE_S) so two processes spawned
   near-simultaneously never treat each other as stale. Implemented via
   `psutil` (cross-platform) rather than `powershell`/`Get-CimInstance` --
   tests fake process iteration via `_iter_sibling_candidates` and process
   termination via `psutil.Process`, not `subprocess.run`.
2. Widened on-demand cold-start timeout budgets
   (embedder_client.STARTUP_WAIT_TIMEOUT_S, server._EMBEDDER_LOAD_TIMEOUT_S)
   matched to values actually observed live on 2026-08-09.
3. _get_embedder_unavailable_reason()'s "starting (retry shortly)" wording
   for a recently-launched, not-yet-confirmed-ready embedder-service, versus
   a flat "unavailable" once the grace window has elapsed.

No live Qdrant instance, live embedder-service, or real process
enumeration/termination is required for anything in this file --
_iter_sibling_candidates and psutil.Process are monkeypatched at the module
level exactly like server.py's other collaborators are elsewhere in this
suite.
"""
import sys
import time


def _fake_process_info(pid, ppid, cmdline, create_time):
    return {"pid": pid, "ppid": ppid, "cmdline": cmdline, "create_time": create_time}


# ---------------------------------------------------------------------------
# _cleanup_stale_sibling_processes
# ---------------------------------------------------------------------------


class TestCleanupStaleSiblingProcesses:
    def test_skipped_when_disabled_via_env_var(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "false")
        called = []
        monkeypatch.setattr(
            agent_memory_server, "_iter_sibling_candidates", lambda: called.append(1) or iter([])
        )
        agent_memory_server._cleanup_stale_sibling_processes()
        assert called == []

    def test_terminates_stale_siblings_but_never_self(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server, "_SELF_PID", 111, raising=False)
        monkeypatch.setattr(agent_memory_server, "_SELF_PARENT_PID", 9999, raising=False)
        suffix = agent_memory_server._AGENT_MEMORY_RELATIVE_SUFFIX
        old_enough = time.time() - agent_memory_server._SIBLING_CLEANUP_MIN_AGE_S - 100.0

        candidates = [
            _fake_process_info(111, 9999, ["python.exe", f"./{suffix}"], old_enough),  # self
            _fake_process_info(222, 9999, ["python.exe", f"./{suffix}"], old_enough),
            _fake_process_info(333, 9999, ["python.exe", f"./{suffix}"], old_enough),
        ]
        monkeypatch.setattr(agent_memory_server, "_iter_sibling_candidates", lambda: iter(candidates))

        killed_pids = []

        class _FakeProcess:
            def __init__(self, pid):
                self.pid = pid

            def kill(self):
                killed_pids.append(self.pid)

        monkeypatch.setattr(agent_memory_server.psutil, "Process", _FakeProcess)
        agent_memory_server._cleanup_stale_sibling_processes()

        assert sorted(killed_pids) == [222, 333]
        assert 111 not in killed_pids  # self must never be targeted

    def test_no_siblings_found_is_a_noop(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server, "_iter_sibling_candidates", lambda: iter([]))

        kill_calls = []
        monkeypatch.setattr(
            agent_memory_server.psutil,
            "Process",
            lambda pid: kill_calls.append(pid),
        )
        agent_memory_server._cleanup_stale_sibling_processes()
        assert kill_calls == []

    def test_diagnostic_fires_when_siblings_exist_under_a_different_ppid(
        self, agent_memory_server, monkeypatch, capsys
    ):
        """When the primary (PPID-scoped) scan finds nothing but a same-
        suffix, old-enough process exists under a different
        ParentProcessId, the diagnostic scan must say so -- otherwise this
        is indistinguishable in the logs from "no stale siblings at all"."""
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server, "_SELF_PID", 111, raising=False)
        monkeypatch.setattr(agent_memory_server, "_SELF_PARENT_PID", 9999, raising=False)
        suffix = agent_memory_server._AGENT_MEMORY_RELATIVE_SUFFIX
        old_enough = time.time() - agent_memory_server._SIBLING_CLEANUP_MIN_AGE_S - 100.0

        # Same suffix, old enough, but a DIFFERENT ParentProcessId -- must
        # not be killed, only counted by the diagnostic scan.
        candidates = [_fake_process_info(222, 1234, [f"./{suffix}"], old_enough)]
        monkeypatch.setattr(agent_memory_server, "_iter_sibling_candidates", lambda: iter(candidates))

        killed_pids = []

        class _FakeProcess:
            def __init__(self, pid):
                killed_pids.append(pid)

            def kill(self):
                pass

        monkeypatch.setattr(agent_memory_server.psutil, "Process", _FakeProcess)
        agent_memory_server._cleanup_stale_sibling_processes()

        assert killed_pids == []  # never kills based on the diagnostic scan
        captured = capsys.readouterr()
        assert "DIFFERENT ParentProcessId" in captured.err

    def test_diagnostic_silent_when_truly_no_siblings_exist(
        self, agent_memory_server, monkeypatch, capsys
    ):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server, "_SELF_PID", 111, raising=False)
        monkeypatch.setattr(agent_memory_server, "_iter_sibling_candidates", lambda: iter([]))

        agent_memory_server._cleanup_stale_sibling_processes()

        captured = capsys.readouterr()
        assert "DIFFERENT ParentProcessId" not in captured.err

    def test_never_raises_when_diagnostic_scan_itself_fails(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")

        calls = {"n": 0}

        def _iter_raising_on_second_call():
            calls["n"] += 1
            if calls["n"] == 1:
                return iter([])
            raise OSError("diagnostic scan failed")

        monkeypatch.setattr(agent_memory_server, "_iter_sibling_candidates", _iter_raising_on_second_call)
        # Must not raise even though the diagnostic (PPID-less) scan errors.
        agent_memory_server._cleanup_stale_sibling_processes()

    def test_never_raises_when_scan_itself_fails(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")

        def _raise():
            raise OSError("process enumeration not permitted")

        monkeypatch.setattr(agent_memory_server, "_iter_sibling_candidates", _raise)
        # Must not raise.
        agent_memory_server._cleanup_stale_sibling_processes()

    def test_never_raises_when_scan_itself_times_out(self, agent_memory_server, monkeypatch):
        """_call_with_hard_timeout is specifically built to interrupt a hung
        scan -- simulate the hang by having the scan sleep past the hard
        timeout it's wrapped in."""
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")

        def _hang():
            time.sleep(30)
            return iter([])

        monkeypatch.setattr(agent_memory_server, "_iter_sibling_candidates", _hang)
        # Must not raise (the 20s hard timeout in _cleanup_stale_sibling_processes
        # returns None rather than propagating).
        agent_memory_server._cleanup_stale_sibling_processes()

    def test_never_raises_when_a_single_kill_fails(self, agent_memory_server, monkeypatch):
        monkeypatch.setenv("AGENT_MEMORY_ENABLE_SIBLING_CLEANUP", "true")
        monkeypatch.setattr(agent_memory_server, "_SELF_PID", 111, raising=False)
        monkeypatch.setattr(agent_memory_server, "_SELF_PARENT_PID", 9999, raising=False)
        suffix = agent_memory_server._AGENT_MEMORY_RELATIVE_SUFFIX
        old_enough = time.time() - agent_memory_server._SIBLING_CLEANUP_MIN_AGE_S - 100.0

        candidates = [_fake_process_info(222, 9999, [f"./{suffix}"], old_enough)]
        monkeypatch.setattr(agent_memory_server, "_iter_sibling_candidates", lambda: iter(candidates))

        class _FakeProcess:
            def __init__(self, pid):
                self.pid = pid

            def kill(self):
                raise agent_memory_server.psutil.NoSuchProcess(self.pid)

        monkeypatch.setattr(agent_memory_server.psutil, "Process", _FakeProcess)
        # Must not raise even though the kill itself fails.
        agent_memory_server._cleanup_stale_sibling_processes()

    def test_scan_uses_relative_suffix_not_absolute_path(
        self, agent_memory_server, monkeypatch
    ):
        """
        _scan_sibling_pids must match on the workspace-relative suffix, not
        the absolute path -- exercised directly (not via a mock) so this
        proves something about the actual matching logic, not just that
        some scan function was called.
        """
        suffix = agent_memory_server._AGENT_MEMORY_RELATIVE_SUFFIX
        assert agent_memory_server._AGENT_MEMORY_SERVER_SCRIPT.replace("\\", "/").endswith(suffix)

        now = time.time()
        old_enough = now - agent_memory_server._SIBLING_CLEANUP_MIN_AGE_S - 100.0
        # Absolute path built from the suffix alone (as if run from a
        # different checkout root) must still match -- the scan cares about
        # the trailing suffix, never the leading absolute prefix.
        assert agent_memory_server._sibling_matches(
            ["python.exe", f"/some/other/checkout/root/{suffix}"],
            old_enough, 9999, now, suffix,
            agent_memory_server._SIBLING_CLEANUP_MIN_AGE_S, 9999,
        ) is True


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

    def test_scan_includes_age_filter(self, agent_memory_server):
        """_sibling_matches must reject a same-suffix, same-PPID candidate
        that is younger than min_age -- exercised directly against the
        production predicate, not a mocked collaborator."""
        suffix = agent_memory_server._AGENT_MEMORY_RELATIVE_SUFFIX
        now = time.time()
        assert agent_memory_server._sibling_matches(
            [f"./{suffix}"], now - 1.0, 9999, now, suffix, 45.0, 9999,
        ) is False
        assert agent_memory_server._sibling_matches(
            [f"./{suffix}"], now - 100.0, 9999, now, suffix, 45.0, 9999,
        ) is True


class TestSiblingMatchFilterSemantics:
    """
    Exercises _sibling_matches directly -- the pure-Python predicate that
    replaced the PowerShell WHERE-clause (_build_sibling_match_filter_clause,
    retired 2026-08-13; see
    core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md).
    No subprocess, no platform skip -- runs identically on every OS, which
    is the whole point of the port.
    """

    @staticmethod
    def _matches(
        agent_memory_server,
        cmdline,
        age_seconds: float,
        min_age: float = 45.0,
        self_parent_pid: int = 9999,
        candidate_parent_pid: int = 9999,
    ) -> bool:
        suffix = agent_memory_server._AGENT_MEMORY_RELATIVE_SUFFIX
        now = time.time()
        return agent_memory_server._sibling_matches(
            cmdline, now - age_seconds, candidate_parent_pid, now,
            suffix, min_age, self_parent_pid,
        )

    def test_direct_relative_launch_old_enough_matches(self, agent_memory_server):
        cmdline = [
            "./core-component-00/platform/model-context-protocol-servers/.venv/Scripts/python.exe",
            "./core-component-00/platform/model-context-protocol-servers/agent-memory/server.py",
        ]
        assert self._matches(agent_memory_server, cmdline, age_seconds=100.0) is True

    def test_absolute_windows_backslash_launch_matches(self, agent_memory_server):
        cmdline = [
            r"C:\Users\ASUS\Documents\Code\Local\AGENT-GLOBAL-BASE\core-component-00"
            r"\mcp-servers\.venv\Scripts\python.exe",
            r"C:\Users\ASUS\Documents\Code\Local\AGENT-GLOBAL-BASE\core-component-00"
            r"\mcp-servers\agent-memory\server.py",
        ]
        assert self._matches(agent_memory_server, cmdline, age_seconds=100.0) is True

    def test_absolute_posix_launch_matches(self, agent_memory_server):
        """Linux/macOS-shaped absolute path -- the scenario the 2026-08-13
        psutil port exists to cover, since the former implementation never
        ran here at all (Windows-only gate)."""
        cmdline = [
            "/home/user/AGENT-GLOBAL-BASE/core-component-00/platform/model-context-protocol-servers/.venv/bin/python",
            "/home/user/AGENT-GLOBAL-BASE/core-component-00/platform/model-context-protocol-servers/agent-memory/server.py",
        ]
        assert self._matches(agent_memory_server, cmdline, age_seconds=100.0) is True

    def test_unrelated_file_does_not_match(self, agent_memory_server):
        cmdline = [
            "./core-component-00/platform/model-context-protocol-servers/.venv/Scripts/python.exe",
            "./core-component-00/platform/model-context-protocol-servers/workspace-knowledge/server.py",
        ]
        assert self._matches(agent_memory_server, cmdline, age_seconds=100.0) is False

    def test_file_referenced_as_non_trailing_argument_does_not_match(self, agent_memory_server):
        """A pytest/lint invocation that references this file among several
        arguments (not as the launched script) must never be mistaken for
        a direct launch of it."""
        cmdline = [
            "./core-component-00/platform/model-context-protocol-servers/.venv/Scripts/python.exe", "-m", "pytest",
            "agent-memory/tests/test_server.py", "agent-memory/server.py", "agent-memory/write_tool.py",
        ]
        assert self._matches(agent_memory_server, cmdline, age_seconds=100.0) is False

    def test_empty_cmdline_does_not_match(self, agent_memory_server):
        assert self._matches(agent_memory_server, [], age_seconds=100.0) is False

    def test_younger_than_threshold_does_not_match(self, agent_memory_server):
        cmdline = [
            "./core-component-00/platform/model-context-protocol-servers/.venv/Scripts/python.exe",
            "./core-component-00/platform/model-context-protocol-servers/agent-memory/server.py",
        ]
        assert self._matches(agent_memory_server, cmdline, age_seconds=0.7, min_age=45.0) is False

    def test_just_under_threshold_does_not_match(self, agent_memory_server):
        cmdline = [
            "./core-component-00/platform/model-context-protocol-servers/.venv/Scripts/python.exe",
            "./core-component-00/platform/model-context-protocol-servers/agent-memory/server.py",
        ]
        assert self._matches(agent_memory_server, cmdline, age_seconds=44.5, min_age=45.0) is False

    def test_just_over_threshold_matches(self, agent_memory_server):
        cmdline = [
            "./core-component-00/platform/model-context-protocol-servers/.venv/Scripts/python.exe",
            "./core-component-00/platform/model-context-protocol-servers/agent-memory/server.py",
        ]
        assert self._matches(agent_memory_server, cmdline, age_seconds=45.5, min_age=45.0) is True

    def test_older_than_threshold_matches(self, agent_memory_server):
        cmdline = [
            "./core-component-00/platform/model-context-protocol-servers/.venv/Scripts/python.exe",
            "./core-component-00/platform/model-context-protocol-servers/agent-memory/server.py",
        ]
        assert self._matches(agent_memory_server, cmdline, age_seconds=3600.0, min_age=45.0) is True

    def test_different_parent_process_id_does_not_match(self, agent_memory_server):
        """A same-suffix process spawned by a DIFFERENT host process (e.g. a
        separate checkout or git worktree session, per CLAUDE.md section 6)
        must never be matched, even when the path suffix and age both
        qualify -- this is the 2026-08-09 cross-checkout finding."""
        cmdline = [
            "./core-component-00/platform/model-context-protocol-servers/.venv/Scripts/python.exe",
            "./core-component-00/platform/model-context-protocol-servers/agent-memory/server.py",
        ]
        assert self._matches(
            agent_memory_server, cmdline, age_seconds=3600.0, min_age=45.0,
            self_parent_pid=9999, candidate_parent_pid=1234,
        ) is False

    def test_same_parent_process_id_matches(self, agent_memory_server):
        cmdline = [
            "./core-component-00/platform/model-context-protocol-servers/.venv/Scripts/python.exe",
            "./core-component-00/platform/model-context-protocol-servers/agent-memory/server.py",
        ]
        assert self._matches(
            agent_memory_server, cmdline, age_seconds=3600.0, min_age=45.0,
            self_parent_pid=9999, candidate_parent_pid=9999,
        ) is True

    def test_parent_pid_none_omits_ppid_condition(self, agent_memory_server):
        """parent_pid=None is the diagnostic-scan mode -- suffix and age
        alone are sufficient, regardless of ParentProcessId."""
        suffix = agent_memory_server._AGENT_MEMORY_RELATIVE_SUFFIX
        now = time.time()
        assert agent_memory_server._sibling_matches(
            [f"./{suffix}"], now - 3600.0, 1234, now, suffix, 45.0, None,
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
