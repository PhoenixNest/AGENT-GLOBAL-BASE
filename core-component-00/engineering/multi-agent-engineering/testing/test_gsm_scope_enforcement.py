"""
Tests for GSM Scope Enforcement — T16 GSMSE Remediation

Verifies that SharedMemoryLog scope predicates correctly gate cross-fleet access
when integrated with SwarmOrchestrator, and that backward-compatible fallback
operates correctly when no memory_log is provided.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.swarm_orchestrator import (
    SwarmConfig,
    SwarmOrchestrator,
    SwarmPlan,
    SubTask,
    SwarmTopology,
)
from implementations.shared_memory_log import SharedMemoryLog


def test_same_fleet_read_succeeds():
    """FLEET-scoped results written by fleet_alpha are readable by fleet_alpha."""
    memory_log = SharedMemoryLog()
    config = SwarmConfig(fleet_id="fleet_alpha", topology="hybrid", max_agents=2)
    orchestrator = SwarmOrchestrator(config, memory_log=memory_log)
    task = SubTask(description="Test task", domain="general")
    plan = SwarmPlan(subtasks=[task], topology=SwarmTopology.HYBRID)

    result = asyncio.run(orchestrator.execute(plan))

    entries = memory_log.read_all(
        requesting_agent_id="test",
        requesting_fleet_id="fleet_alpha",
    )
    assert len(entries) >= 1
    assert all(e.fleet_id == "fleet_alpha" for e in entries)
    assert result.success is True


def test_cross_fleet_read_denied():
    """FLEET-scoped results written by fleet_alpha are denied to fleet_beta."""
    memory_log = SharedMemoryLog()
    config = SwarmConfig(fleet_id="fleet_alpha", topology="hybrid", max_agents=2)
    orchestrator = SwarmOrchestrator(config, memory_log=memory_log)
    task = SubTask(description="Test task", domain="general")
    plan = SwarmPlan(subtasks=[task], topology=SwarmTopology.HYBRID)

    asyncio.run(orchestrator.execute(plan))

    entries = memory_log.read_all(
        requesting_agent_id="test",
        requesting_fleet_id="fleet_beta",
    )
    assert entries == []


def test_no_memory_log_falls_back_gracefully():
    """Orchestrator without a memory_log falls back to direct subtask_results list."""
    config = SwarmConfig(fleet_id="fleet_alpha", topology="hybrid", max_agents=2)
    orchestrator = SwarmOrchestrator(config)
    task = SubTask(description="Test task", domain="general")
    plan = SwarmPlan(subtasks=[task], topology=SwarmTopology.HYBRID)

    result = asyncio.run(orchestrator.execute(plan))

    assert result.success is True
    assert len(result.subtask_results) == 1
    assert result.subtask_results[0]["task_id"] == task.task_id
