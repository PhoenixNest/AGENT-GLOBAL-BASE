"""
Executable pytest suite for ToolRegistry's dangerous-task detection (Harness I1 / R1).

Run with:
    pytest testing/test_tool_registry.py -v
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from implementations.tool_registry import ToolRegistry, SafeAgentToolUse


def _make_agent():
    return SafeAgentToolUse(ToolRegistry())


class TestDangerousTaskDetectionCrossPlatform:
    """Regression coverage for Harness R1: an empty regex pattern on win32
    previously matched every string, refusing every task as UNSAFE_TASK
    regardless of content."""

    BENIGN_TASKS = [
        "Find information about the solar system",
        "Summarize this document for the reader",
        "Format this report as markdown",  # must NOT trip the disk-format pattern
        "Reformat the codebase's imports",
    ]

    DANGEROUS_TASKS = [
        "delete system32.dll from the machine",
        "rm -rf the project directory",
        "format c: to wipe the drive",
        "kill the running process immediately",
    ]

    @pytest.mark.parametrize("task", BENIGN_TASKS)
    def test_benign_task_is_never_flagged_dangerous(self, task, monkeypatch):
        agent = _make_agent()
        for platform in ("win32", "linux", "darwin"):
            monkeypatch.setattr(sys, "platform", platform)
            assert agent._is_dangerous_task(task) is False, (
                f"benign task incorrectly flagged dangerous on platform={platform}: {task!r}"
            )

    @pytest.mark.parametrize("task", DANGEROUS_TASKS)
    def test_dangerous_task_is_flagged_on_every_platform(self, task, monkeypatch):
        agent = _make_agent()
        for platform in ("win32", "linux", "darwin"):
            monkeypatch.setattr(sys, "platform", platform)
            assert agent._is_dangerous_task(task) is True, (
                f"dangerous task not flagged on platform={platform}: {task!r}"
            )

    def test_sudo_task_flagged_off_win32_not_on_win32(self, monkeypatch):
        agent = _make_agent()
        task = "sudo rm the config file"

        monkeypatch.setattr(sys, "platform", "linux")
        assert agent._is_dangerous_task(task) is True

        monkeypatch.setattr(sys, "platform", "win32")
        # sudo has no win32 equivalent — this platform difference is intentional,
        # unlike the prior bug where win32 flagged everything regardless of content
        assert agent._is_dangerous_task(task) is False

    @pytest.mark.asyncio
    async def test_execute_plan_never_refuses_benign_task_on_win32(self, monkeypatch):
        monkeypatch.setattr(sys, "platform", "win32")
        agent = _make_agent()
        result = await agent.execute_plan("Find information about the solar system")
        assert result.get("error", {}).get("code") != "UNSAFE_TASK"
