"""
Tests for SwarmOrchestrator — Multi-Agent Coordination Engine

Covers: plan creation, topology execution (pipeline, fork-join, hybrid),
variance detection, feedback loop, and error handling.
"""

import asyncio
import pytest
from unittest.mock import AsyncMock

import sys
from pathlib import Path

# Add implementations to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.handoff_packet import HandoffPacket, HandoffTier
from implementations.swarm_orchestrator import (
    AgentProfile,
    SubTask,
    SwarmConfig,
    SwarmOrchestrator,
    SwarmPlan,
    SwarmResult,
    SwarmTopology,
    TaskStatus,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def agents():
    return [
        AgentProfile(
            agent_id="backend-01",
            name="Backend Agent",
            role="backend",
            expertise=["backend", "api", "database"],
        ),
        AgentProfile(
            agent_id="frontend-01",
            name="Frontend Agent",
            role="frontend",
            expertise=["frontend", "ui", "css"],
        ),
        AgentProfile(
            agent_id="tester-01",
            name="Test Agent",
            role="tester",
            expertise=["testing", "qa"],
        ),
    ]


@pytest.fixture
def config():
    return SwarmConfig(fleet_id="test_fleet", topology="hybrid", max_agents=5)


@pytest.fixture
def orchestrator(config, agents):
    return SwarmOrchestrator(config=config, agents=agents)


# ---------------------------------------------------------------------------
# Plan Tests
# ---------------------------------------------------------------------------


class TestPlanCreation:
    def test_plan_basic(self, orchestrator):
        subtasks = [
            SubTask(description="Build API", domain="backend"),
            SubTask(description="Build UI", domain="frontend"),
        ]
        plan = orchestrator.plan("Add dark mode", subtasks=subtasks)

        assert plan.user_request == "Add dark mode"
        assert len(plan.subtasks) == 2
        assert plan.topology == SwarmTopology.HYBRID

    def test_plan_auto_assigns_agents(self, orchestrator):
        subtasks = [
            SubTask(description="Build API", domain="backend"),
            SubTask(description="Build UI", domain="frontend"),
        ]
        plan = orchestrator.plan("Task", subtasks=subtasks)

        assert plan.subtasks[0].assigned_agent == "backend-01"
        assert plan.subtasks[1].assigned_agent == "frontend-01"

    def test_plan_fallback_agent(self, orchestrator):
        subtasks = [SubTask(description="Unknown task", domain="unknown")]
        plan = orchestrator.plan("Task", subtasks=subtasks)

        # Should fallback to first agent
        assert plan.subtasks[0].assigned_agent == "backend-01"

    def test_plan_empty_subtasks(self, orchestrator):
        plan = orchestrator.plan("Empty task")
        assert len(plan.subtasks) == 0


# ---------------------------------------------------------------------------
# Execution Tests
# ---------------------------------------------------------------------------


class TestExecution:
    @pytest.mark.asyncio
    async def test_fork_join_execution(self, agents):
        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join")
        orch = SwarmOrchestrator(config=config, agents=agents)

        subtasks = [
            SubTask(description="Task A", domain="backend"),
            SubTask(description="Task B", domain="frontend"),
        ]
        plan = orch.plan("Parallel work", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.success is True
        assert len(result.subtask_results) == 2
        assert all(r["status"] == "completed" for r in result.subtask_results)

    @pytest.mark.asyncio
    async def test_pipeline_execution(self, agents):
        config = SwarmConfig(fleet_id="test_fleet", topology="pipeline")
        orch = SwarmOrchestrator(config=config, agents=agents)

        subtasks = [
            SubTask(task_id="s1", description="Stage 1", domain="backend"),
            SubTask(
                task_id="s2",
                description="Stage 2",
                domain="frontend",
                depends_on=["s1"],
            ),
        ]
        plan = orch.plan("Sequential work", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.success is True

    @pytest.mark.asyncio
    async def test_hybrid_with_dependencies(self, agents):
        config = SwarmConfig(fleet_id="test_fleet", topology="hybrid")
        orch = SwarmOrchestrator(config=config, agents=agents)

        subtasks = [
            SubTask(task_id="a", description="Independent A", domain="backend"),
            SubTask(task_id="b", description="Independent B", domain="frontend"),
            SubTask(
                task_id="c",
                description="Depends on A and B",
                domain="testing",
                depends_on=["a", "b"],
            ),
        ]
        plan = orch.plan("Hybrid work", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.success is True
        assert len(result.subtask_results) == 3

    @pytest.mark.asyncio
    async def test_execution_failure(self, agents):
        async def failing_execute(task, handoff):
            raise RuntimeError("Agent crashed")

        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join")
        orch = SwarmOrchestrator(
            config=config, agents=agents, execute_fn=failing_execute
        )

        subtasks = [SubTask(description="Will fail", domain="backend")]
        plan = orch.plan("Failing task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.success is False
        assert result.subtask_results[0]["status"] == "failed"


# ---------------------------------------------------------------------------
# Synthesis Tests
# ---------------------------------------------------------------------------


class TestSynthesis:
    @pytest.mark.asyncio
    async def test_synthesize(self, orchestrator):
        subtasks = [
            SubTask(description="Part A", domain="backend"),
            SubTask(description="Part B", domain="frontend"),
        ]
        plan = orchestrator.plan("Synth test", subtasks=subtasks)
        result = await orchestrator.execute(plan)
        output = orchestrator.synthesize(result)

        assert "Result for: Part A" in output
        assert "Result for: Part B" in output


# ---------------------------------------------------------------------------
# Feedback Loop Tests
# ---------------------------------------------------------------------------


class TestFeedback:
    @pytest.mark.asyncio
    async def test_feedback_generated(self, agents):
        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join", enable_feedback_loop=True)
        orch = SwarmOrchestrator(config=config, agents=agents)

        subtasks = [SubTask(description="Task", domain="backend")]
        plan = orch.plan("Feedback test", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.feedback is not None
        assert result.feedback["completed"] == 1

    @pytest.mark.asyncio
    async def test_feedback_disabled(self, agents):
        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join", enable_feedback_loop=False)
        orch = SwarmOrchestrator(config=config, agents=agents)

        subtasks = [SubTask(description="Task", domain="backend")]
        plan = orch.plan("No feedback", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.feedback is None


# ---------------------------------------------------------------------------
# SubTask Property Tests
# ---------------------------------------------------------------------------


class TestSubTaskProperties:
    def test_is_independent(self):
        task = SubTask(description="Independent")
        assert task.is_independent is True

    def test_is_not_independent(self):
        task = SubTask(description="Dependent", depends_on=["other"])
        assert task.is_independent is False

    def test_variance_not_measurable(self):
        task = SubTask(description="Not started")
        assert task.variance is None

    def test_variance_calculation(self):
        task = SubTask(
            description="Completed",
            estimated_duration=100.0,
            started_at=0.0,
            completed_at=120.0,
        )
        assert task.variance == pytest.approx(0.20)
