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


class TestReflectionRetrievalHook:
    """Phase 2 proactive orchestrator-brief-time retrieval hook — see
    telescope/2026-07-14-reflexion-memory-system/supporting/01-technical-options.md §5.2
    and supporting/03-deployment-guidelines.md Phase 2's anti-pattern gate.
    """

    @pytest.mark.asyncio
    async def test_hook_fires_at_brief_issuance_time(self, agents):
        calls = []

        def reflection_fn(task_description):
            calls.append(task_description)
            return {"results": [], "count": 0, "degraded": False, "reason": None}

        captured_handoffs = []

        async def capturing_execute(task, handoff):
            captured_handoffs.append(handoff)
            return {"status": "completed", "output": "ok"}

        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join")
        orch = SwarmOrchestrator(
            config=config,
            agents=agents,
            execute_fn=capturing_execute,
            reflection_search_fn=reflection_fn,
        )
        subtasks = [SubTask(description="Build API", domain="backend")]
        plan = orch.plan("Task", subtasks=subtasks)
        await orch.execute(plan)

        assert calls == ["Build API"]
        assert len(captured_handoffs) == 1

    @pytest.mark.asyncio
    async def test_empty_collection_degrades_to_proceed(self, agents):
        def reflection_fn(task_description):
            # Expected steady state at initial rollout: no records migrated yet.
            return {"results": [], "count": 0, "degraded": False, "reason": None}

        captured_handoffs = []

        async def capturing_execute(task, handoff):
            captured_handoffs.append(handoff)
            return {"status": "completed", "output": "ok"}

        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join")
        orch = SwarmOrchestrator(
            config=config,
            agents=agents,
            execute_fn=capturing_execute,
            reflection_search_fn=reflection_fn,
        )
        subtasks = [SubTask(description="Task", domain="backend")]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.success is True
        assert captured_handoffs[0].retrieved_reflections == []
        assert captured_handoffs[0].sacred_context == []

    @pytest.mark.asyncio
    async def test_degraded_response_also_proceeds(self, agents):
        def reflection_fn(task_description):
            return {
                "results": [],
                "count": 0,
                "degraded": True,
                "reason": "qdrant-memory client unavailable",
            }

        captured_handoffs = []

        async def capturing_execute(task, handoff):
            captured_handoffs.append(handoff)
            return {"status": "completed", "output": "ok"}

        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join")
        orch = SwarmOrchestrator(
            config=config,
            agents=agents,
            execute_fn=capturing_execute,
            reflection_search_fn=reflection_fn,
        )
        subtasks = [SubTask(description="Task", domain="backend")]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.success is True
        assert captured_handoffs[0].retrieved_reflections == []
        assert captured_handoffs[0].sacred_context == []

    @pytest.mark.asyncio
    async def test_populated_match_included_in_brief(self, agents):
        def reflection_fn(task_description):
            return {
                "results": [
                    {
                        "reflection_id": "REFLECT-001",
                        "trigger_type": "process_violation",
                        "summary": "Never delete a worktree without checking git status first.",
                        "scope_of_applicability": "any git worktree cleanup task",
                        "root_cause": "...",
                        "remediation": "...",
                        "logged_by": "Dr. Elias Vance",
                        "sacred": True,
                        "status": "active",
                    }
                ],
                "count": 1,
                "degraded": False,
                "reason": None,
            }

        captured_handoffs = []

        async def capturing_execute(task, handoff):
            captured_handoffs.append(handoff)
            return {"status": "completed", "output": "ok"}

        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join")
        orch = SwarmOrchestrator(
            config=config,
            agents=agents,
            execute_fn=capturing_execute,
            reflection_search_fn=reflection_fn,
        )
        subtasks = [SubTask(description="Clean up worktree", domain="backend")]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.success is True
        assert len(captured_handoffs[0].retrieved_reflections) == 1
        note = captured_handoffs[0].retrieved_reflections[0]
        assert "REFLECT-001" in note
        assert "Never delete a worktree without checking git status first." in note
        assert "any git worktree cleanup task" in note
        # Retrieved reflections are a "required read," not a binding decision —
        # they land in retrieved_reflections even when the source record is
        # sacred=True, never in sacred_context (reserved for orchestrator-level
        # decisions/constraints per HandoffPacket's own contract).
        assert captured_handoffs[0].sacred_context == []

    @pytest.mark.asyncio
    async def test_retrieval_failure_degrades_to_proceed(self, agents):
        def failing_reflection_fn(task_description):
            raise TimeoutError("qdrant-memory call exceeded hard timeout")

        captured_handoffs = []

        async def capturing_execute(task, handoff):
            captured_handoffs.append(handoff)
            return {"status": "completed", "output": "ok"}

        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join")
        orch = SwarmOrchestrator(
            config=config,
            agents=agents,
            execute_fn=capturing_execute,
            reflection_search_fn=failing_reflection_fn,
        )
        subtasks = [SubTask(description="Task", domain="backend")]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.success is True
        assert captured_handoffs[0].retrieved_reflections == []
        assert captured_handoffs[0].sacred_context == []

    @pytest.mark.asyncio
    async def test_no_reflection_fn_configured_proceeds_unchanged(self, agents):
        """Default (unset) — no dependency on memory_reflection at all."""
        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join")
        orch = SwarmOrchestrator(config=config, agents=agents)

        subtasks = [SubTask(description="Task", domain="backend")]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.success is True


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
