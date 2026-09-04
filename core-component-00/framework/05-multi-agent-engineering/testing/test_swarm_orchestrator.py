"""
Tests for SwarmOrchestrator — Multi-Agent Coordination Engine

Covers: plan creation, topology execution (pipeline, fork-join, hybrid),
variance detection, feedback loop, and error handling.
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock

import sys
from pathlib import Path

# Add implementations to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent))

from implementations.handoff_packet import HandoffPacket, HandoffTier
from implementations.swarm_orchestrator import (
    AgentProfile,
    EvaluationVerdict,
    MonitorBudget,
    SubTask,
    SwarmConfig,
    SwarmOrchestrator,
    SwarmPlan,
    SwarmResult,
    SwarmTopology,
    TaskStatus,
    default_gate_criteria_tier,
    default_monitor_budget,
    evaluate_subtask_result,
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

    @pytest.mark.asyncio
    async def test_short_task_monitor_budget_actually_applied_in_dispatch(self, agents):
        """Confirms default_monitor_budget() is actually wired into
        asyncio.wait_for's timeout, not just correct in isolation — a short
        estimated_duration must produce a tighter timeout than the flat
        config default, causing a slower-than-budget execute_fn to time out."""
        async def slow_execute(task, handoff):
            await asyncio.sleep(0.2)
            return {"output": "done"}

        config = SwarmConfig(fleet_id="test_fleet", topology="fork_join", timeout_seconds=300.0)
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=slow_execute)
        subtasks = [SubTask(description="Quick task", domain="frontend", estimated_duration=0.01)]
        plan = orch.plan("Short task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert subtasks[0].status == TaskStatus.FAILED
        assert "error" in subtasks[0].result


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
    """Verifies the proactive reflection-retrieval hook fires exactly once
    per subtask at brief-issuance time (not later, not on a delay), and that
    an empty or degraded reflection-search result never blocks or delays the
    handoff — the hook can only add context, never gate execution."""

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


# ---------------------------------------------------------------------------
# Execute-Monitor-Evaluate-Reflect cycle
# ---------------------------------------------------------------------------


class TestDefaultGateCriteriaTier:
    """The default gate_criteria activation policy."""

    @pytest.mark.parametrize("domain", ["backend", "Backend API", "security-audit", "release-train"])
    def test_high_stakes_domains_enabled(self, domain):
        assert default_gate_criteria_tier(domain) == "enabled"

    @pytest.mark.parametrize("domain", ["frontend", "research", "content", ""])
    def test_generic_domains_disabled(self, domain):
        assert default_gate_criteria_tier(domain) == "disabled"

    def test_none_domain_does_not_raise(self):
        assert default_gate_criteria_tier(None) == "disabled"


class TestDefaultMonitorBudget:
    """Duration-tiered dispatch timeout."""

    def test_long_running_task_gets_extended_timeout(self):
        budget = default_monitor_budget("backend", 1800.0, base_timeout_seconds=300.0)
        assert budget.tier == "long_running"
        assert budget.timeout_seconds == 3600.0  # 1800 * 2.0 multiplier, exceeds base

    def test_short_task_gets_reduced_timeout(self):
        budget = default_monitor_budget("frontend", 10.0, base_timeout_seconds=300.0)
        assert budget.tier == "short"
        assert budget.timeout_seconds == 40.0  # 10 * 4.0 multiplier, below base

    def test_standard_duration_task_gets_base_timeout(self):
        budget = default_monitor_budget("backend", 120.0, base_timeout_seconds=300.0)
        assert budget.tier == "standard"
        assert budget.timeout_seconds == 300.0

    def test_zero_duration_does_not_raise_or_zero_out_timeout(self):
        budget = default_monitor_budget("backend", 0.0, base_timeout_seconds=300.0)
        assert budget.timeout_seconds == 300.0

    def test_long_running_never_reduces_below_base_timeout(self):
        budget = default_monitor_budget("backend", 901.0, base_timeout_seconds=5000.0)
        assert budget.timeout_seconds == 5000.0

    def test_long_running_timeout_is_capped_by_a_ceiling(self):
        """A Monitor budget exists to bound risk; an uncapped multiplier on a
        very large estimated_duration (legitimate or a units mistake) would
        defeat that purpose."""
        budget = default_monitor_budget("backend", 1_000_000.0, base_timeout_seconds=300.0)
        assert budget.timeout_seconds == 3600.0

    def test_ceiling_never_pulls_timeout_below_a_large_base(self):
        """The ceiling bounds the extension above base_timeout_seconds; it
        must never make a long-running task's budget smaller than what the
        standard tier would have given it."""
        budget = default_monitor_budget("backend", 1_000_000.0, base_timeout_seconds=5000.0)
        assert budget.timeout_seconds == 5000.0


class TestEvaluateSubtaskResult:
    """The Evaluate step itself."""

    def test_empty_gate_criteria_passes_trivially(self):
        task = SubTask(description="x", gate_criteria=None)
        verdict = evaluate_subtask_result(task, {"output": "anything"})
        assert verdict.passed is True

    def test_malformed_result_does_not_raise(self):
        task = SubTask(description="x", gate_criteria=["tests_pass"])
        # result is not a dict at all — must not raise, must fail closed.
        verdict = evaluate_subtask_result(task, "not a dict")
        assert isinstance(verdict, EvaluationVerdict)
        assert verdict.passed is False

    def test_structured_evidence_passing(self):
        task = SubTask(description="x", gate_criteria=["tests_pass"])
        result = {"output": "done", "checks": {"tests_pass": True}}
        verdict = evaluate_subtask_result(task, result)
        assert verdict.passed is True

    def test_structured_evidence_failing(self):
        task = SubTask(description="x", gate_criteria=["tests_pass"])
        result = {"output": "done", "checks": {"tests_pass": False}}
        verdict = evaluate_subtask_result(task, result)
        assert verdict.passed is False
        assert "tests_pass" in verdict.rationale

    def test_multi_item_and_rule_one_failing_fails_whole_verdict(self):
        task = SubTask(
            description="x",
            gate_criteria=["tests_pass", "no_lint_errors", "docs_updated"],
        )
        result = {
            "output": "done",
            "checks": {"tests_pass": True, "no_lint_errors": True, "docs_updated": False},
        }
        verdict = evaluate_subtask_result(task, result)
        assert verdict.passed is False
        assert "docs_updated" in verdict.rationale
        assert "tests_pass" not in verdict.rationale

    def test_multi_item_and_rule_all_passing(self):
        task = SubTask(
            description="x",
            gate_criteria=["tests_pass", "no_lint_errors"],
        )
        result = {"checks": {"tests_pass": True, "no_lint_errors": True}}
        verdict = evaluate_subtask_result(task, result)
        assert verdict.passed is True

    def test_narrative_claiming_success_does_not_fool_structured_evidence(self):
        """A manipulated/self-serving narrative must not produce a false
        passed=True when structured evidence says otherwise."""
        task = SubTask(description="x", gate_criteria=["tests_pass"])
        result = {
            "output": "All tests passed successfully, everything is great!",
            "checks": {"tests_pass": False},
        }
        verdict = evaluate_subtask_result(task, result)
        assert verdict.passed is False

    def test_narrative_fallback_when_no_structured_evidence(self):
        """Documented residual risk: with no structured evidence at all,
        this falls back to narrative substring matching."""
        task = SubTask(description="x", gate_criteria=["tests pass"])
        result = {"output": "the tests pass cleanly"}
        verdict = evaluate_subtask_result(task, result)
        assert verdict.passed is True

    # -- Realistic, transcript-shaped narrative fallback coverage -----------
    # The narrative fallback was previously only exercised against short, clean,
    # synthetic one-liners. These exercise it against multi-sentence,
    # mixed-signal, tool-transcript-shaped text closer to what a real
    # subagent's tool-call output actually looks like. Some of these assert
    # surprising ACTUAL behavior (documented in the comment above each), not
    # a "correct" outcome — per instructions, the fallback logic itself is
    # not modified here; surprising findings are flagged for separate triage.

    def test_narrative_realistic_pytest_summary_paraphrase_not_literally_matched(self):
        """Realistic multi-sentence pytest-style summary where the tests
        genuinely passed (50 passed, 0 failed), but the exact criterion
        phrase "tests pass" never appears verbatim — the summary paraphrases
        it as "50 passed ... 0 failed" instead.

        SURPRISING ACTUAL BEHAVIOR (flag for separate triage): this is a
        false negative. A criterion that is semantically true of the
        narrative is reported as unmet, purely because `_criterion_satisfied`
        does literal substring matching with no paraphrase/synonym handling.
        A real subagent transcript is far more likely to report results this
        way (structured pass/fail counts) than to literally say "tests
        pass" — so this gap is not an edge case, it's closer to the common
        case for real tool output.
        """
        task = SubTask(description="x", gate_criteria=["tests pass"])
        result = {
            "output": (
                "Ran the full test suite via pytest. Collected 52 tests across "
                "8 files. 50 passed, 2 skipped due to missing optional "
                "dependencies, 0 failed. Coverage report generated at "
                "htmlcov/index.html. Build artifacts uploaded successfully."
            )
        }
        verdict = evaluate_subtask_result(task, result)
        assert verdict.passed is False
        assert "tests pass" in verdict.rationale

    def test_narrative_mixed_pass_fail_test_names_matches_only_relevant_criterion(self):
        """Realistic paragraph naming both a passing test and an unrelated
        failing test in the same string. Only the passing test's name is the
        actual gate_criteria text. Verify the fallback correctly reports
        passed=True and is not thrown off by the failure-adjacent language
        ("failed", "ConnectionResetError") describing the other test."""
        task = SubTask(
            description="x",
            gate_criteria=["test_user_authentication_flow passed"],
        )
        result = {
            "output": (
                "test_user_authentication_flow passed after the token refresh "
                "fix landed. In the same run, test_payment_gateway_retry failed "
                "intermittently with a ConnectionResetError, seemingly unrelated "
                "to this change and already tracked as a flaky test in issue #482."
            )
        }
        verdict = evaluate_subtask_result(task, result)
        assert verdict.passed is True

    def test_narrative_stack_trace_adjacent_text_does_not_mask_genuine_pass_statement(self):
        """Transcript containing a Python traceback fragment (a non-fatal,
        expected warning) alongside a genuine passing build statement.
        Verify the fallback still correctly reads the passing statement
        rather than being thrown off by exception-looking text nearby."""
        task = SubTask(description="x", gate_criteria=["build succeeded"])
        result = {
            "output": (
                "Running build...\n"
                "Traceback (most recent call last):\n"
                '  File "scripts/prebuild_check.py", line 17, in <module>\n'
                "    warnings.warn('legacy config key detected, ignoring')\n"
                "UserWarning: legacy config key detected, ignoring\n"
                "(This is an expected, non-fatal warning from the linter shim.)\n"
                "Build succeeded with 0 errors and 1 warning in 12.4s."
            )
        }
        verdict = evaluate_subtask_result(task, result)
        assert verdict.passed is True

    def test_narrative_realistic_lint_failure_transcript_correctly_reports_failed(self):
        """Realistic transcript describing a genuine lint failure (not a
        paraphrase gap this time — the tool output plainly says errors were
        found). The exact criterion phrase never appears, and the underlying
        state genuinely does not satisfy it, so passed=False here is the
        legitimately correct outcome, not just a matching artifact."""
        task = SubTask(description="x", gate_criteria=["no lint errors"])
        result = {
            "output": (
                "Ran eslint across the changed files. Found 3 problems "
                "(3 errors, 0 warnings): no-unused-vars in "
                "src/utils/date.js:14, no-undef in src/components/Modal.jsx:52, "
                "and prefer-const in src/hooks/useToggle.js:8. These must be "
                "resolved before merge."
            )
        }
        verdict = evaluate_subtask_result(task, result)
        assert verdict.passed is False
        assert "no lint errors" in verdict.rationale

    def test_narrative_negated_criterion_text_still_matches_as_substring(self):
        """Regression guard for a false-positive found in a real pilot run.
        Adversarial-shaped but realistic transcript: the narrative explicitly DENIES the criterion
        ("It would be incorrect to say the authentication tests pass") and
        then explains three concrete failures — but the denied clause still
        contains the criterion's exact words as a contiguous substring.

        A naive substring check has no concept of negation, hedging, or
        sentence structure — it would score this denial sentence identically to an
        assertion and produce a confident false-positive passed=True.
        `_phrase_asserted_in_narrative` instead applies a bounded negation
        check (a fixed-window scan for a small negation-cue vocabulary
        immediately before each match) that
        closes this specific reproduction. This test must keep failing
        (i.e. keep asserting passed is False) if that check regresses.
        """
        task = SubTask(description="x", gate_criteria=["authentication tests pass"])
        result = {
            "output": (
                "It would be incorrect to say the authentication tests pass "
                "right now — three of them (test_login, test_mfa_challenge, "
                "test_session_refresh) are failing intermittently under load "
                "and need further investigation before this can be marked done."
            )
        }
        verdict = evaluate_subtask_result(task, result)
        assert verdict.passed is False


class TestReflectiveLoop:
    """Reflect step, bounded retry, GATE_FAILED aggregation."""

    @pytest.mark.asyncio
    async def test_gate_criteria_empty_unaffected_by_reflective_loop(self, agents):
        """Opt-in only — a SubTask with no gate_criteria completes exactly as
        before, even with enable_reflective_loop=True."""
        config = SwarmConfig(fleet_id="f", topology="fork_join", enable_reflective_loop=True)
        orch = SwarmOrchestrator(config=config, agents=agents)
        subtasks = [SubTask(description="Task", domain="backend")]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)
        assert result.success is True
        assert subtasks[0].status == TaskStatus.COMPLETED
        assert subtasks[0].reflection_retry_count == 0

    @pytest.mark.asyncio
    async def test_passing_verdict_completes_without_retry(self, agents):
        async def execute_fn(task, handoff):
            return {"checks": {"tests_pass": True}}

        config = SwarmConfig(fleet_id="f", topology="fork_join", enable_reflective_loop=True)
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=execute_fn)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)
        assert subtasks[0].status == TaskStatus.COMPLETED
        assert subtasks[0].reflection_retry_count == 0

    @pytest.mark.asyncio
    async def test_reflection_note_appears_in_retried_attempt_context(self, agents):
        attempts = []

        async def execute_fn(task, handoff):
            attempts.append(handoff.task)
            if len(attempts) < 2:
                return {"checks": {"tests_pass": False}}
            return {"checks": {"tests_pass": True}}

        config = SwarmConfig(fleet_id="f", topology="fork_join", enable_reflective_loop=True)
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=execute_fn)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert subtasks[0].status == TaskStatus.COMPLETED
        assert subtasks[0].reflection_retry_count == 1
        assert len(attempts) == 2
        assert "[WORKING MEMORY]" not in attempts[0]
        assert "[WORKING MEMORY]" in attempts[1]
        assert "Unmet gate_criteria" in attempts[1]

    @pytest.mark.asyncio
    async def test_retry_cap_enforced_and_gate_failed_reached(self, agents):
        async def always_fails(task, handoff):
            return {"checks": {"tests_pass": False}}

        config = SwarmConfig(
            fleet_id="f", topology="fork_join", enable_reflective_loop=True, max_reflection_retries=2
        )
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=always_fails)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert subtasks[0].status == TaskStatus.GATE_FAILED
        assert subtasks[0].reflection_retry_count == 3  # initial + 2 retries, all failing
        assert result.success is False

    @pytest.mark.asyncio
    async def test_final_attempt_reflection_note_requests_new_approach(self, agents):
        """The last allowed retry's injected context must ask for a
        genuinely different approach; earlier retries must not."""
        attempts = []

        async def always_fails(task, handoff):
            attempts.append(handoff.task)
            return {"checks": {"tests_pass": False}}

        config = SwarmConfig(
            fleet_id="f", topology="fork_join", enable_reflective_loop=True, max_reflection_retries=2
        )
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=always_fails)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert subtasks[0].status == TaskStatus.GATE_FAILED
        assert len(attempts) == 3
        assert "genuinely different approach" not in attempts[1]
        assert "genuinely different approach" in attempts[2]

    @pytest.mark.asyncio
    async def test_working_memory_cleared_on_completed_exit_after_retry(self, agents, monkeypatch):
        mock_memory = MagicMock()
        mock_memory.to_context_string.return_value = "[WORKING MEMORY] prior note"
        monkeypatch.setattr(
            SwarmOrchestrator, "_get_working_memory_instance", staticmethod(lambda: mock_memory)
        )

        async def execute_fn(task, handoff):
            if mock_memory.add_note.call_count == 0:
                return {"checks": {"tests_pass": False}}
            return {"checks": {"tests_pass": True}}

        config = SwarmConfig(fleet_id="f", topology="fork_join", enable_reflective_loop=True)
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=execute_fn)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert subtasks[0].status == TaskStatus.COMPLETED
        mock_memory.clear.assert_called_once()

    @pytest.mark.asyncio
    async def test_working_memory_cleared_on_gate_failed_exit(self, agents, monkeypatch):
        mock_memory = MagicMock()
        mock_memory.to_context_string.return_value = "[WORKING MEMORY] prior note"
        monkeypatch.setattr(
            SwarmOrchestrator, "_get_working_memory_instance", staticmethod(lambda: mock_memory)
        )

        async def always_fails(task, handoff):
            return {"checks": {"tests_pass": False}}

        config = SwarmConfig(
            fleet_id="f", topology="fork_join", enable_reflective_loop=True, max_reflection_retries=1
        )
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=always_fails)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert subtasks[0].status == TaskStatus.GATE_FAILED
        mock_memory.clear.assert_called_once()

    @pytest.mark.asyncio
    async def test_gate_failed_feedback_carries_rationale_history_and_gate_failed_count(self, agents):
        async def always_fails(task, handoff):
            return {"checks": {"tests_pass": False}}

        config = SwarmConfig(
            fleet_id="f",
            topology="fork_join",
            enable_reflective_loop=True,
            enable_feedback_loop=True,
            max_reflection_retries=1,
        )
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=always_fails)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert subtasks[0].status == TaskStatus.GATE_FAILED
        assert result.feedback is not None
        assert result.feedback["gate_failed"] == 1
        assert subtasks[0].task_id in result.feedback["rationale_history"]
        assert len(result.feedback["rationale_history"][subtasks[0].task_id]) == 2
        assert result.feedback["retry_counts"][subtasks[0].task_id] == 2

    @pytest.mark.asyncio
    async def test_reflective_feedback_populated_even_when_feedback_loop_disabled(self, agents):
        """'Flagged for review' must carry real reasons regardless of the
        unrelated enable_feedback_loop opt-in."""
        async def always_fails(task, handoff):
            return {"checks": {"tests_pass": False}}

        config = SwarmConfig(
            fleet_id="f",
            topology="fork_join",
            enable_reflective_loop=True,
            enable_feedback_loop=False,
            max_reflection_retries=0,
        )
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=always_fails)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert subtasks[0].status == TaskStatus.GATE_FAILED
        assert result.feedback is not None
        assert subtasks[0].task_id in result.feedback["rationale_history"]
        assert "gate_failed" not in result.feedback  # that key lives in _gen_feedback, which is off here

    @pytest.mark.asyncio
    async def test_multi_subtask_plan_mixed_outcomes(self, agents):
        async def execute_fn(task, handoff):
            if task.task_id == "pass-me":
                return {"checks": {"tests_pass": True}}
            return {"checks": {"tests_pass": False}}

        config = SwarmConfig(
            fleet_id="f",
            topology="fork_join",
            enable_reflective_loop=True,
            enable_feedback_loop=True,
            max_reflection_retries=0,
        )
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=execute_fn)
        subtasks = [
            SubTask(task_id="pass-me", description="A", domain="backend", gate_criteria=["tests_pass"]),
            SubTask(task_id="fail-me", description="B", domain="backend", gate_criteria=["tests_pass"]),
            SubTask(task_id="ungated", description="C", domain="backend"),
        ]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        by_id = {t.task_id: t for t in subtasks}
        assert by_id["pass-me"].status == TaskStatus.COMPLETED
        assert by_id["fail-me"].status == TaskStatus.GATE_FAILED
        assert by_id["ungated"].status == TaskStatus.COMPLETED
        assert result.feedback["gate_failed"] == 1
        assert "fail-me" in result.feedback["rationale_history"]
        assert "pass-me" not in result.feedback["rationale_history"]


class TestFaultAndSemanticRetryCounterIndependence:
    """Adversarial case: driving one counter must not affect the other."""

    @pytest.mark.asyncio
    async def test_repeated_infra_faults_never_touch_semantic_retry_counter(self, agents):
        async def always_raises(task, handoff):
            raise RuntimeError("simulated infra fault")

        config = SwarmConfig(
            fleet_id="f", topology="fork_join", enable_reflective_loop=True, max_reflection_retries=2
        )
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=always_raises)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        assert subtasks[0].status == TaskStatus.FAILED
        assert subtasks[0].reflection_retry_count == 0
        assert subtasks[0].reflection_rationale_history == []

    @pytest.mark.asyncio
    async def test_repeated_gate_failures_never_produce_failed_status(self, agents):
        async def always_fails_gate(task, handoff):
            return {"checks": {"tests_pass": False}}

        config = SwarmConfig(
            fleet_id="f", topology="fork_join", enable_reflective_loop=True, max_reflection_retries=3
        )
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=always_fails_gate)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        # Exhausting semantic retries must land on GATE_FAILED, never FAILED —
        # proof the two paths/counters never interact.
        assert subtasks[0].status == TaskStatus.GATE_FAILED
        assert subtasks[0].result != {"error": "circuit_breaker_open"}


class TestUnroutedTopologyLoudFailure:
    """An unrouted SwarmTopology member (SUPERVISOR_WORKER, ROUTER) must
    never silently fall through to the Hybrid executor via
    `dispatch.get(plan.topology, self._execute_hybrid)`'s default — that
    would be invisible to a green suite because nothing else asserts on
    it. Neither topology may ever reach Hybrid: each executes via its own
    explicit executor or raises loudly instead."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("topology", ["supervisor_worker", "router"])
    async def test_unrouted_topology_never_falls_through_to_hybrid(
        self, agents, topology, monkeypatch
    ):
        config = SwarmConfig(fleet_id="test_fleet", topology=topology)
        orch = SwarmOrchestrator(config=config, agents=agents)

        hybrid_calls = []
        original_hybrid = orch._execute_hybrid

        async def spy_hybrid(plan):
            hybrid_calls.append(plan)
            return await original_hybrid(plan)

        monkeypatch.setattr(orch, "_execute_hybrid", spy_hybrid)

        subtasks = [SubTask(description="Task", domain="backend")]
        plan = orch.plan("Task", subtasks=subtasks)

        try:
            await orch.execute(plan)
        except Exception:
            pass  # an explicit raise is an acceptable non-silent outcome

        assert hybrid_calls == [], (
            f"{topology} topology silently fell through to the Hybrid "
            "executor instead of executing via its own path or raising "
            "explicitly"
        )


class TestRouterAndSupervisorWorkerExecutors:
    """Basic functional coverage for I1's beyond-the-floor executors —
    the plan scopes their full behavior as tested separately, but these
    confirm the minimal implementations actually do something real rather
    than being a second silent no-op dressed up as a fix."""

    @pytest.mark.asyncio
    async def test_router_routes_by_domain_keyword_and_completes(self, agents):
        config = SwarmConfig(fleet_id="test_fleet", topology="router")
        orch = SwarmOrchestrator(config=config, agents=agents)
        subtasks = [
            SubTask(description="Build API", domain="backend"),
            SubTask(description="Build UI", domain="frontend"),
        ]
        plan = orch.plan("Route work", subtasks=subtasks)
        result = await orch.execute(plan)

        assert result.success is True
        assert subtasks[0].assigned_agent == "backend-01"
        assert subtasks[1].assigned_agent == "frontend-01"

    @pytest.mark.asyncio
    async def test_supervisor_worker_completes_when_gate_criteria_satisfied(self, agents):
        async def execute_fn(task, handoff):
            return {"checks": {"tests_pass": True}}

        config = SwarmConfig(fleet_id="test_fleet", topology="supervisor_worker")
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=execute_fn)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Supervised work", subtasks=subtasks)
        result = await orch.execute(plan)

        assert subtasks[0].status == TaskStatus.COMPLETED
        assert result.success is True

    @pytest.mark.asyncio
    async def test_supervisor_worker_demotes_to_gate_failed_without_reflective_loop(self, agents):
        """The supervisor validation tier catches an unmet gate_criteria
        even when enable_reflective_loop is off (the default) — it is an
        independent post-dispatch check, not a repackaging of that
        opt-in in-dispatch retry cycle."""
        async def execute_fn(task, handoff):
            return {"checks": {"tests_pass": False}}

        config = SwarmConfig(fleet_id="test_fleet", topology="supervisor_worker")
        assert config.enable_reflective_loop is False
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=execute_fn)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Supervised work", subtasks=subtasks)
        result = await orch.execute(plan)

        assert subtasks[0].status == TaskStatus.GATE_FAILED
        assert "tests_pass" in subtasks[0].reflection_rationale_history[-1]
        assert result.success is False


class TestGradualEnablementScaffolding:
    """enable_reflective_loop ships off by default; setting gate_criteria
    alone (without also flipping enable_reflective_loop) must not change
    behavior."""

    @pytest.mark.asyncio
    async def test_disabled_by_default_even_with_gate_criteria_set(self, agents):
        async def would_fail_gate_if_evaluated(task, handoff):
            return {"checks": {"tests_pass": False}}

        config = SwarmConfig(fleet_id="f", topology="fork_join")  # enable_reflective_loop defaults False
        assert config.enable_reflective_loop is False
        orch = SwarmOrchestrator(config=config, agents=agents, execute_fn=would_fail_gate_if_evaluated)
        subtasks = [SubTask(description="Task", domain="backend", gate_criteria=["tests_pass"])]
        plan = orch.plan("Task", subtasks=subtasks)
        result = await orch.execute(plan)

        # Identical to pre-Phase-1 behavior: Evaluate never runs, task completes.
        assert subtasks[0].status == TaskStatus.COMPLETED
        assert subtasks[0].reflection_retry_count == 0
        assert result.success is True
