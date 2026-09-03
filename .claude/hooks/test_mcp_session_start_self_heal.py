"""Regression test for the Item #11 fix (fresh-clone same-session self-heal).

Maintenance record: core-component-00/platform/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/
(log/29-fresh-clone-dry-run-first-session-gap-found.md, log/30-*.md).

Before the fix: on a genuinely fresh clone, the two `SessionStart` hooks
(`mcp-config-platform-check.py` then `mcp-venv-bootstrap.py`, run exactly once, in that
order, matching `.claude/settings.json`) left `.mcp.json` pointing at a nonexistent
interpreter path for the server whose `.venv` `mcp-venv-bootstrap.py` had to create --
`mcp-config-platform-check.py`'s own correction pass ran *before* that venv existed, so it
had nothing to find. The fix: `mcp-venv-bootstrap.py` now re-invokes
`mcp-config-platform-check.py` a second time, in-process, immediately after a successful
`uv sync` -- see `mcp-venv-bootstrap.py`'s "Post-sync re-check" docstring section.

This test reproduces that exact two-hook sequence against an isolated fake repo (not the
real workspace -- no real `uv sync`/network/GPU dependency), using a stub `uv` on PATH that
fakes `sync` (creates a `.venv/bin/python` marker instantly) and forwards `run <script>` to
the real interpreter so the real hook code under test still executes unmodified. Invokes
each hook exactly as `SessionStart` does: `uv run <script>.py` fed a JSON stdin payload,
`CLAUDE_PROJECT_DIR` set. Run with:
    pytest .claude/hooks/test_mcp_session_start_self_heal.py -v
"""

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

HOOKS_DIR = Path(__file__).resolve().parent
PLATFORM_CHECK = HOOKS_DIR / "mcp-config-platform-check.py"
VENV_BOOTSTRAP = HOOKS_DIR / "mcp-venv-bootstrap.py"
HOOK_LOG = HOOKS_DIR / "_hook_log.py"

STUB_UV_SCRIPT = """#!/bin/sh
# Fakes just enough of `uv` for this test: `sync` creates a POSIX-layout venv marker
# instantly (no real install), `run <script>` execs the real interpreter on the script so
# the hook code under test still runs unmodified, stdin/exit-code passed through.
set -e
if [ "$1" = "sync" ]; then
    mkdir -p .venv/bin
    printf '#!/bin/sh\\nexit 0\\n' > .venv/bin/python
    chmod +x .venv/bin/python
    exit 0
elif [ "$1" = "run" ]; then
    shift
    exec "%s" "$@"
fi
exit 1
""" % sys.executable


def _make_fake_repo(tmp_path: Path) -> Path:
    """Builds an isolated fake repo: real (copied) hook scripts under .claude/hooks/, a
    .mcp.json.example with one server whose command uses the Windows suffix (matching the
    real template's hardcoded default -- see mcp-config-platform-check.py's docstring), and
    that server's root directory (with a venv not yet created, matching a fresh clone)."""
    repo = tmp_path / "repo"
    hooks_dir = repo / ".claude" / "hooks"
    hooks_dir.mkdir(parents=True)
    for src in (PLATFORM_CHECK, VENV_BOOTSTRAP, HOOK_LOG):
        shutil.copy(src, hooks_dir / src.name)

    # _hook_log.py locates its state dir via `git rev-parse --show-toplevel`, which is
    # how mcp-venv-bootstrap.py learns what mcp-config-platform-check.py found (see
    # mcp-venv-bootstrap.py's own docstring: "single source of truth ... avoiding drift
    # between the two hooks") -- the fake repo needs to actually be one, or that channel
    # silently carries nothing and both hooks take their (correct, but untested-by-this)
    # fast no-op path.
    subprocess.run(["git", "init", "-q", str(repo)], check=True)

    server_dir = repo / "server-under-test"
    server_dir.mkdir()
    (server_dir / "pyproject.toml").write_text("[project]\nname = \"fake\"\n", encoding="utf-8")

    example = {
        "mcpServers": {
            "testserver": {
                "command": "${CLAUDE_PROJECT_DIR:-.}/server-under-test/.venv/Scripts/python.exe",
                "args": ["${CLAUDE_PROJECT_DIR:-.}/server-under-test/server.py"],
            }
        }
    }
    (repo / ".mcp.json.example").write_text(json.dumps(example, indent=2), encoding="utf-8")

    return repo


def _stub_uv_bin(tmp_path: Path) -> Path:
    bin_dir = tmp_path / "stub-bin"
    bin_dir.mkdir()
    uv_path = bin_dir / "uv"
    uv_path.write_text(STUB_UV_SCRIPT, encoding="utf-8")
    uv_path.chmod(uv_path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return bin_dir


def _run_hook(script: Path, repo: Path, stub_bin: Path, session_id: str):
    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(repo)
    env["PATH"] = f"{stub_bin}{os.pathsep}{env.get('PATH', '')}"
    payload = json.dumps({"session_id": session_id})
    return subprocess.run(
        ["uv", "run", str(repo / ".claude" / "hooks" / script.name)],
        input=payload,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(repo),
        timeout=30,
    )


def test_fresh_clone_single_session_start_pass_ends_with_corrected_mcp_json(tmp_path):
    repo = _make_fake_repo(tmp_path)
    stub_bin = _stub_uv_bin(tmp_path)
    session_id = "test-session-fresh-clone"

    # Hook 1, exactly as registered first in .claude/settings.json: bootstraps .mcp.json
    # from the template. Neither OS's venv exists yet -- this must report "bootstrapped"
    # and leave the Windows-default path in place (nothing to correct against yet).
    result1 = _run_hook(PLATFORM_CHECK, repo, stub_bin, session_id)
    assert result1.returncode == 0, result1.stderr
    mcp_json_after_1 = json.loads((repo / ".mcp.json").read_text(encoding="utf-8"))
    command_after_1 = mcp_json_after_1["mcpServers"]["testserver"]["command"]
    assert command_after_1.endswith("/.venv/Scripts/python.exe"), (
        "hook 1 should bootstrap the template's default (Windows) path verbatim when no "
        f"venv exists yet for either OS, got: {command_after_1!r}"
    )

    # Hook 2, exactly as registered second: syncs the missing venv (stubbed), then --
    # the fix under test -- re-invokes hook 1's correction pass a second time before
    # returning. This must leave .mcp.json corrected within THIS SAME pass, matching what
    # a real fresh-clone user's single SessionStart should now produce.
    result2 = _run_hook(VENV_BOOTSTRAP, repo, stub_bin, session_id)
    assert result2.returncode == 0, result2.stderr

    mcp_json_after_2 = json.loads((repo / ".mcp.json").read_text(encoding="utf-8"))
    command_after_2 = mcp_json_after_2["mcpServers"]["testserver"]["command"]
    assert command_after_2.endswith("/.venv/bin/python"), (
        "Item #11 regression: .mcp.json was not corrected within the same SessionStart "
        f"pass after mcp-venv-bootstrap.py's sync. Got: {command_after_2!r}"
    )

    # The venv-bootstrap hook's own message should reflect the successful re-check, not
    # the old (misleading, per log/29) unconditional "/mcp reconnect" guidance.
    stdout2 = json.loads(result2.stdout)
    additional_context = stdout2["hookSpecificOutput"]["additionalContext"]
    assert "re-verified" in additional_context


def test_ordinary_session_stays_a_fast_no_op_for_both_hooks(tmp_path):
    """Once both the venv and a correct .mcp.json already exist (the state right after the
    fresh-clone pass above), a further SessionStart must not shell out again -- guards
    against the fix regressing either hook's fast/fail-open contract for the common case."""
    repo = _make_fake_repo(tmp_path)
    stub_bin = _stub_uv_bin(tmp_path)
    session_a = "test-session-fresh-clone"
    _run_hook(PLATFORM_CHECK, repo, stub_bin, session_a)
    _run_hook(VENV_BOOTSTRAP, repo, stub_bin, session_a)

    session_b = "test-session-ordinary"
    result1 = _run_hook(PLATFORM_CHECK, repo, stub_bin, session_b)
    result2 = _run_hook(VENV_BOOTSTRAP, repo, stub_bin, session_b)
    assert result1.returncode == 0 and result2.returncode == 0
    # Fast no-op path prints nothing to stdout (no hookSpecificOutput emitted).
    assert result1.stdout.strip() == ""
    assert result2.stdout.strip() == ""
