"""
Swarm Orchestrator — Multi-Agent Coordination Engine

Manages the full lifecycle of a multi-agent swarm execution:
task decomposition, agent provisioning, parallel dispatch,
result collection, synthesis, and cleanup.

Version: 1.0
Last Updated: 2026-04-29
Maintained by: Claude Lab Engineering Team
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

from .handoff_packet import HandoffPacket, HandoffTier
from .shared_memory_log import MemoryScope, SharedMemoryLog

logger = logging.getLogger(__name__)


class SwarmTopology(Enum):
    PIPELINE = "pipeline"
    FORK_JOIN = "fork_join"
    ROUTER = "router"
    SUPERVISOR_WORKER = "supervisor_worker"
    HYBRID = "hybrid"


class TaskStatus(Enum):
    PENDING = "pending"
    DISPATCHED = "dispatched"
    COMPLETED = "completed"
    FAILED = "failed"
    GATE_FAILED = "gate_failed"


@dataclass
class SwarmConfig:
    fleet_id: str
    topology: str = "hybrid"
    max_agents: int = 10
    enable_git_worktree: bool = False
    variance_threshold: float = 0.20
    timeout_seconds: float = 300.0
    enable_feedback_loop: bool = True
    circuit_breaker_open_abort: bool = True
    max_reflection_retries: int = 2
    enable_reflective_loop: bool = False


@dataclass
class AgentProfile:
    agent_id: str
    name: str
    role: str
    expertise: list[str] = field(default_factory=list)
    handoff_tier_default: HandoffTier = HandoffTier.SCOPED

    def matches_task(self, task_domain: str) -> bool:
        return any(d.lower() in task_domain.lower() for d in self.expertise)


@dataclass
class SubTask:
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str = ""
    domain: str = ""
    depends_on: list[str] = field(default_factory=list)
    assigned_agent: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    estimated_duration: float = 60.0
    gate_criteria: Optional[list[str]] = None
    reflection_retry_count: int = 0
    reflection_rationale_history: list[str] = field(default_factory=list)

    @property
    def is_independent(self) -> bool:
        return len(self.depends_on) == 0

    @property
    def actual_duration(self) -> Optional[float]:
        if self.started_at is not None and self.completed_at is not None:
            return self.completed_at - self.started_at
        return None

    @property
    def variance(self) -> Optional[float]:
        duration = self.actual_duration
        if duration and self.estimated_duration > 0:
            return (duration - self.estimated_duration) / self.estimated_duration
        return None


@dataclass
class SwarmPlan:
    plan_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    user_request: str = ""
    topology: SwarmTopology = SwarmTopology.HYBRID
    subtasks: list[SubTask] = field(default_factory=list)
    agents: list[AgentProfile] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    def independent_tasks(self) -> list[SubTask]:
        completed_ids = {
            t.task_id for t in self.subtasks if t.status == TaskStatus.COMPLETED
        }
        return [
            t
            for t in self.subtasks
            if t.status == TaskStatus.PENDING
            and all(dep in completed_ids for dep in t.depends_on)
        ]

    def all_completed(self) -> bool:
        terminal = {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.GATE_FAILED}
        return all(t.status in terminal for t in self.subtasks)


@dataclass
class SwarmResult:
    plan_id: str = ""
    success: bool = True
    subtask_results: list[dict[str, Any]] = field(default_factory=list)
    synthesized_output: Optional[str] = None
    total_duration: float = 0.0
    agent_utilisation: float = 0.0
    feedback: Optional[dict[str, Any]] = None
    circuit_breaker_aborts: int = 0


@dataclass
class EvaluationVerdict:
    """The Evaluate step's judgment of a SubTask's result against its own
    gate_criteria.

    `passed` requires every item in gate_criteria to check out — an AND,
    not a threshold. `rationale` is a per-criterion account, not one
    free-text paragraph, so it can be read back into a retry attempt's
    WorkingMemory context meaningfully.
    """

    passed: bool
    rationale: str


# High-blast-radius domain keywords that default a SubTask's gate_criteria
# activation tier to "enabled" — see default_gate_criteria_tier() below.
# Deliberately a small, simple set; refining this taxonomy against real
# usage data is future work, not a learned/continuous classifier built
# ahead of that evidence.
_HIGH_STAKES_DOMAIN_KEYWORDS = ("backend", "security", "release")

# result dict keys treated as narrative text, not checkable evidence — see
# evaluate_subtask_result()'s docstring for why this distinction matters.
_NARRATIVE_RESULT_KEYS = frozenset({"output", "summary"})

# Duration thresholds and multipliers for default_monitor_budget()'s three
# tiers. Simple, documented-as-provisional constants — the same posture as
# _HIGH_STAKES_DOMAIN_KEYWORDS above: a reasonable starting default, not a
# learned/continuous allocator built ahead of real usage data.
_LONG_RUNNING_DURATION_THRESHOLD_SECONDS = 900.0
_SHORT_DURATION_THRESHOLD_SECONDS = 30.0
_LONG_RUNNING_TIMEOUT_MULTIPLIER = 2.0
_SHORT_DURATION_TIMEOUT_MULTIPLIER = 4.0

# A Monitor budget exists to bound risk; an uncapped multiplier defeats that
# purpose for any very large (legitimate or mistaken, e.g. a units error)
# estimated_duration. This ceiling is a provisional safety backstop, not a
# tuned value.
_LONG_RUNNING_TIMEOUT_CEILING_SECONDS = 3600.0


@dataclass
class MonitorBudget:
    """The timeout a single SubTask dispatch attempt gets, tiered off its
    estimated_duration rather than one flat value for every task.

    Deliberately timeout-only: circuit-breaker sensitivity would also
    reasonably scale per tier, but the breaker is an opaque object injected
    by the caller (SwarmOrchestrator.set_circuit_breaker) — tiering its
    sensitivity belongs to whatever constructs that breaker, outside this
    module's boundary, not here.
    """

    timeout_seconds: float
    tier: str


def default_monitor_budget(
    domain: str, estimated_duration: float, base_timeout_seconds: float
) -> MonitorBudget:
    """Tiers a SubTask's dispatch timeout so a long-running task isn't cut
    off by the same window as a short one, and a short task doesn't wait
    out a timeout many multiples of its own expected length.

    `domain` is accepted for forward compatibility with a future,
    data-informed tiering scheme but does not affect the current rule,
    which is duration-only.
    """
    if estimated_duration >= _LONG_RUNNING_DURATION_THRESHOLD_SECONDS:
        # The ceiling bounds the extension above base_timeout_seconds; it
        # never pulls the tiered timeout below the caller's own configured
        # base — a long-running task must never get less time than the
        # standard tier would have given it.
        return MonitorBudget(
            timeout_seconds=max(
                base_timeout_seconds,
                min(
                    estimated_duration * _LONG_RUNNING_TIMEOUT_MULTIPLIER,
                    _LONG_RUNNING_TIMEOUT_CEILING_SECONDS,
                ),
            ),
            tier="long_running",
        )
    if 0 < estimated_duration <= _SHORT_DURATION_THRESHOLD_SECONDS:
        return MonitorBudget(
            timeout_seconds=min(
                base_timeout_seconds, estimated_duration * _SHORT_DURATION_TIMEOUT_MULTIPLIER
            ),
            tier="short",
        )
    return MonitorBudget(timeout_seconds=base_timeout_seconds, tier="standard")


def _reflection_note_for_attempt(rationale: str, is_final_attempt: bool) -> str:
    """The note injected into WorkingMemory ahead of a retried dispatch.
    Every retry but the last carries the bare per-criterion critique; the
    final allowed attempt additionally asks for a genuinely different
    approach rather than a small variation on what has already failed
    twice — repeating the same fix on the last chance wastes it."""
    if not is_final_attempt:
        return rationale
    return (
        f"{rationale}\n\nThis is the final retry attempt. The prior approach has not worked — "
        "try a genuinely different approach rather than a small variation on what was already "
        "attempted."
    )


def default_gate_criteria_tier(domain: str) -> str:
    """The default activation policy for whether a SubTask should get
    gate_criteria at all: "enabled" for higher-stakes domains, "disabled"
    for open-ended/generic work. This function is guidance for the caller
    deciding whether to set SubTask.gate_criteria — it never mutates a
    SubTask itself; that stays the caller's explicit choice.

    A third tier, "skipped" (deterministic, infra-only tasks whose only
    failure mode fault-retry already covers), exists in the design but has
    no reliable signal on SubTask today — domain alone can't distinguish
    "this task is inherently deterministic" from "this task's domain is
    just unset/generic." Honestly returning only "enabled"/"disabled" here,
    rather than guessing at a "skipped" heuristic the design docs don't
    actually specify, is intentional; callers who know a task is
    deterministic simply never set gate_criteria on it, achieving the same
    effect without this function inventing an unfounded classifier.
    """
    normalized = (domain or "").lower()
    if any(keyword in normalized for keyword in _HIGH_STAKES_DOMAIN_KEYWORDS):
        return "enabled"
    return "disabled"


def _normalize_criterion(text: str) -> str:
    """Normalize a gate_criteria string for forgiving comparison against
    result["checks"] keys — lowercase, non-alphanumeric runs collapsed to
    a single underscore, so "no lint errors" and "no_lint_errors" match."""
    normalized = []
    prev_was_sep = False
    for ch in text.lower().strip():
        if ch.isalnum():
            normalized.append(ch)
            prev_was_sep = False
        elif not prev_was_sep:
            normalized.append("_")
            prev_was_sep = True
    return "".join(normalized).strip("_")


_NEGATION_CUES = frozenset(
    {
        "not", "n't", "cannot", "isn't", "aren't", "wasn't", "weren't",
        "doesn't", "don't", "didn't", "won't", "wouldn't", "no", "false",
        "incorrect", "fails", "failed", "fail", "unable", "never",
    }
)
_NEGATION_WINDOW_CHARS = 60


def _phrase_asserted_in_narrative(phrase: str, narrative: str) -> bool:
    """True if `phrase` occurs in `narrative` at least once without an
    immediately-preceding negation cue. Bounded heuristic, not real NLP: it
    only inspects a fixed character window immediately before each match
    against a small fixed negation-word vocabulary. It will miss negation
    phrased outside that window, negation cues not in the list, and double
    negation. Exists to close one concrete, reproduced false-positive (a
    narrative that explicitly denies a criterion but still contains the
    criterion's exact words as a substring) — not to generally understand
    narrative text."""
    if not phrase:
        return False
    lowered_narrative = narrative.lower()
    lowered_phrase = phrase.lower()
    start = 0
    while True:
        idx = lowered_narrative.find(lowered_phrase, start)
        if idx == -1:
            return False
        window = lowered_narrative[max(0, idx - _NEGATION_WINDOW_CHARS) : idx]
        window_words = re.findall(r"[a-z']+", window)
        if not any(word in _NEGATION_CUES for word in window_words):
            return True
        start = idx + len(lowered_phrase)


def _criterion_satisfied(criterion: str, checks: dict[str, Any], narrative: str) -> bool:
    """Judge one gate_criteria item. Structured evidence (result["checks"])
    is checked first and takes precedence; only when no matching structured
    key exists does this fall back to a substring match against narrative
    text. The fallback is an accepted, only-partially-closeable residual
    risk: a narrative string is exactly what a manipulated tool result
    could poison to fake a pass, and this function cannot close that on
    its own — it can only prefer checkable evidence over narrative
    whenever checkable evidence exists. The fallback also applies a bounded
    negation check (see `_phrase_asserted_in_narrative`) so a sentence that
    explicitly denies the criterion is not scored the same as one that
    asserts it."""
    key = _normalize_criterion(criterion)
    for check_key, check_value in checks.items():
        if _normalize_criterion(str(check_key)) == key:
            return bool(check_value)
    return _phrase_asserted_in_narrative(
        key.replace("_", " "), narrative
    ) or _phrase_asserted_in_narrative(criterion, narrative)


def evaluate_subtask_result(subtask: SubTask, result: Any) -> EvaluationVerdict:
    """The Evaluate step. Only meant to be called once a SubTask has
    executed without an infra fault — the caller (SwarmOrchestrator._dispatch)
    is responsible for that ordering.

    gate_criteria authoring convention: each entry must be one
    independently-checkable statement, not a compound sentence — this
    function judges each entry independently and does not attempt to
    split compound criteria itself.

    Checkable-evidence grounding: when `result` is a dict carrying a
    "checks" mapping (structured, caller-supplied evidence — e.g. real
    test output, a diff summary, an explicit status flag), each criterion
    is matched against that mapping first. Only a criterion with no
    corresponding structured key falls back to a substring match against
    `result`'s narrative fields ("output"/"summary") — a residual risk
    this doesn't close, documented rather than pretended away.
    """
    criteria = subtask.gate_criteria or []
    if not criteria:
        return EvaluationVerdict(
            passed=True, rationale="No gate_criteria set — Evaluate skipped, opt-in only."
        )

    checks: dict[str, Any] = {}
    narrative_parts: list[str] = []
    if isinstance(result, dict):
        checks = dict(result.get("checks") or {})
        for narrative_key in _NARRATIVE_RESULT_KEYS:
            value = result.get(narrative_key)
            if isinstance(value, str):
                narrative_parts.append(value)
    narrative = " ".join(narrative_parts)

    unmet = [c for c in criteria if not _criterion_satisfied(c, checks, narrative)]
    if unmet:
        return EvaluationVerdict(
            passed=False,
            rationale="Unmet gate_criteria: " + "; ".join(unmet),
        )
    return EvaluationVerdict(
        passed=True,
        rationale="All gate_criteria satisfied: " + "; ".join(criteria),
    )


_working_memory_module = None


def _get_working_memory_cls():
    """Lazily import WorkingMemory from context-engineering/implementations
    directly by file path (not via a package-qualified import) — this
    workspace's four CC-00 module roots all name their code directory
    `implementations`, so a package-qualified cross-module import
    (`implementations.memory_store`) risks colliding with this very
    module's own `implementations` namespace package once both module
    roots are on sys.path at once (a known collision documented elsewhere
    in this workspace's research archive). Importing memory_store.py as a
    bare top-level module, from its own directory inserted directly onto
    sys.path, sidesteps that collision entirely. Cached at module level so
    the path insertion and import only happen once per process."""
    global _working_memory_module
    if _working_memory_module is None:
        import sys
        from pathlib import Path

        memory_store_dir = (
            Path(__file__).resolve().parents[2]
            / "context-engineering"
            / "implementations"
        )
        sys.path.insert(0, str(memory_store_dir))
        import memory_store as _memory_store_module  # noqa: E402

        _working_memory_module = _memory_store_module
    return _working_memory_module.WorkingMemory


class SwarmOrchestrator:
    """Production-grade multi-agent swarm orchestrator."""

    def __init__(
        self,
        config: SwarmConfig,
        agents: Optional[list[AgentProfile]] = None,
        execute_fn: Optional[Callable] = None,
        memory_log: Optional[SharedMemoryLog] = None,
        reflection_search_fn: Optional[Callable[[str], dict[str, Any]]] = None,
    ):
        self.config = config
        self.agents = agents or []
        self._execute_fn = execute_fn or self._default_execute
        self._execution_log: list[dict[str, Any]] = []
        self._circuit_breaker = None
        self._memory_log = memory_log
        self._fleet_id = config.fleet_id
        self._reflection_search_fn = reflection_search_fn

    def set_circuit_breaker(self, cb) -> None:
        """Inject a duck-typed circuit breaker.

        The circuit breaker must implement:
            is_open() -> bool
            get_state() -> CircuitBreakerState (optional, for observability)

        Using duck typing avoids a circular import with harness error_boundary.
        """
        self._circuit_breaker = cb

    def set_reflection_search_fn(
        self, fn: Optional[Callable[[str], dict[str, Any]]]
    ) -> None:
        """Inject a duck-typed reflection-retrieval callable.

        `fn(task_description)` must return a dict shaped like agent-memory's
        `search_memory(memory_type="reflection", ...)` contract:
            {"results": [...], "count": int, "degraded": bool, "reason": str|None}
        where each entry in "results" is a ReflectionRecord.to_dict() payload
        (see mcp-servers/agent-memory/server.py's search_memory docstring).

        Optional — if never set (the default), brief issuance proceeds exactly
        as before this hook existed; no reflection retrieval is attempted.
        Duck typing avoids a hard import of the agent-memory MCP server into
        this pure-orchestration module, mirroring set_circuit_breaker's
        rationale above.
        """
        self._reflection_search_fn = fn

    def plan(
        self, user_request: str, subtasks: Optional[list[SubTask]] = None
    ) -> SwarmPlan:
        topology = SwarmTopology(self.config.topology)
        plan = SwarmPlan(
            user_request=user_request,
            topology=topology,
            subtasks=subtasks or [],
            agents=self.agents,
        )
        for task in plan.subtasks:
            if not task.assigned_agent:
                task.assigned_agent = self._select_agent(task)
        return plan

    async def execute(self, plan: SwarmPlan) -> SwarmResult:
        start_time = time.time()
        dispatch = {
            SwarmTopology.PIPELINE: self._execute_pipeline,
            SwarmTopology.FORK_JOIN: self._execute_fork_join,
            SwarmTopology.HYBRID: self._execute_hybrid,
        }
        executor = dispatch.get(plan.topology, self._execute_hybrid)
        await executor(plan)
        total_duration = time.time() - start_time

        cb_aborts = sum(
            1
            for t in plan.subtasks
            if t.result == {"error": "circuit_breaker_open"}
        )

        if self._memory_log is not None:
            for t in plan.subtasks:
                self._memory_log.write(
                    agent_id=t.assigned_agent or "unassigned",
                    fleet_id=self._fleet_id,
                    scope=MemoryScope.FLEET,
                    key=f"result:{t.task_id}",
                    value={
                        "task_id": t.task_id,
                        "status": t.status.value,
                        "result": t.result,
                        "variance": t.variance,
                    },
                )
            entries = self._memory_log.read_all(
                requesting_agent_id="orchestrator",
                requesting_fleet_id=self._fleet_id,
            )
            subtask_results: list[dict[str, Any]] = [
                entry.value  # type: ignore[misc]
                for entry in entries
            ]
        else:
            subtask_results = [
                {
                    "task_id": t.task_id,
                    "status": t.status.value,
                    "result": t.result,
                    "variance": t.variance,
                }
                for t in plan.subtasks
            ]

        result = SwarmResult(
            plan_id=plan.plan_id,
            success=all(t.status == TaskStatus.COMPLETED for t in plan.subtasks),
            subtask_results=subtask_results,
            total_duration=total_duration,
            agent_utilisation=self._calc_utilisation(plan),
            circuit_breaker_aborts=cb_aborts,
        )

        if self.config.enable_feedback_loop:
            result.feedback = self._gen_feedback(plan, result)
            self._execution_log.append(result.feedback)

        reflective_feedback = self._gen_reflective_loop_feedback(plan)
        if reflective_feedback:
            if result.feedback is None:
                result.feedback = {}
            result.feedback.update(reflective_feedback)

        return result

    def synthesize(self, result: SwarmResult) -> str:
        outputs = [
            r.get("result", {}).get("output", "")
            for r in result.subtask_results
            if r["status"] == "completed"
        ]
        result.synthesized_output = "\n\n".join(outputs)
        if self._memory_log is not None:
            self._memory_log.write(
                agent_id="orchestrator",
                fleet_id=self._fleet_id,
                scope=MemoryScope.FLEET,
                key=f"synthesized:{result.plan_id}",
                value=result.synthesized_output,
            )
        return result.synthesized_output

    # -- Topology executors ------------------------------------------------

    async def _execute_pipeline(self, plan: SwarmPlan) -> None:
        for task in plan.subtasks:
            await self._dispatch(task)
            if task.status != TaskStatus.COMPLETED:
                break

    async def _execute_fork_join(self, plan: SwarmPlan) -> None:
        independent = plan.independent_tasks()
        if independent:
            await asyncio.gather(*[self._dispatch(t) for t in independent])

    async def _execute_hybrid(self, plan: SwarmPlan) -> None:
        while not plan.all_completed():
            ready = plan.independent_tasks()
            if not ready:
                for t in plan.subtasks:
                    if t.status == TaskStatus.PENDING:
                        t.status = TaskStatus.FAILED
                break
            await asyncio.gather(*[self._dispatch(t) for t in ready])

    # -- Dispatch ----------------------------------------------------------

    async def _dispatch(self, task: SubTask) -> None:
        if self._circuit_breaker is not None and self._circuit_breaker.is_open():
            task.status = TaskStatus.FAILED
            task.result = {"error": "circuit_breaker_open"}
            task.completed_at = time.time()
            logger.warning(
                "Swarm dispatch blocked: circuit breaker OPEN for task %s",
                task.task_id,
            )
            return
        task.status = TaskStatus.DISPATCHED
        task.started_at = time.time()
        # The reflective (semantic-retry) loop below is entirely separate
        # state from this method's own fault handling: any exception at any
        # point still falls straight through to the `except` clause below
        # and sets FAILED — this module tracks no fault-retry counter of its
        # own (that lives, if used at all, inside the caller-supplied
        # _execute_fn / error_boundary.py), so the two retry classes cannot
        # share a budget by construction, not merely by convention.
        working_memory = None
        try:
            while True:
                handoff_task_text = task.description
                if working_memory is not None:
                    handoff_task_text = (
                        f"{task.description}\n\n{working_memory.to_context_string()}"
                    )
                handoff = HandoffPacket(
                    tier=HandoffTier.SCOPED,
                    task=handoff_task_text,
                    acceptance_criteria=task.gate_criteria or [],
                    retrieved_reflections=self._retrieve_reflections(task.description),
                )
                budget = default_monitor_budget(
                    task.domain, task.estimated_duration, self.config.timeout_seconds
                )
                result = await asyncio.wait_for(
                    self._execute_fn(task, handoff),
                    timeout=budget.timeout_seconds,
                )
                task.result = result

                if not (self.config.enable_reflective_loop and task.gate_criteria):
                    # Opt-in only: ungated tasks, or a SwarmConfig with the
                    # reflective loop disabled, complete without evaluation.
                    task.status = TaskStatus.COMPLETED
                    break

                verdict = evaluate_subtask_result(task, result)
                if verdict.passed:
                    task.status = TaskStatus.COMPLETED
                    break

                task.reflection_rationale_history.append(verdict.rationale)
                task.reflection_retry_count += 1
                if task.reflection_retry_count > self.config.max_reflection_retries:
                    task.status = TaskStatus.GATE_FAILED
                    break

                is_final_attempt = task.reflection_retry_count == self.config.max_reflection_retries
                working_memory = working_memory or self._get_working_memory_instance()
                working_memory.set_task(task.description)
                working_memory.add_note(
                    _reflection_note_for_attempt(verdict.rationale, is_final_attempt)
                )
                # loop back and re-dispatch with the reflection note injected
        except Exception as exc:
            task.status = TaskStatus.FAILED
            task.result = {"error": str(exc)}
        finally:
            task.completed_at = time.time()
            if working_memory is not None:
                # Ephemeral by design: the reflection note never outlives
                # this task's own retry loop. On GATE_FAILED, the rationale
                # history is preserved separately in
                # task.reflection_rationale_history (copied into
                # SwarmResult.feedback by execute(), below) before this
                # clear() runs — "flagged for review" must carry the actual
                # reasons, not just the bare fact of failure.
                working_memory.clear()

    @staticmethod
    def _get_working_memory_instance():
        return _get_working_memory_cls()()

    @staticmethod
    async def _default_execute(task: SubTask, handoff: HandoffPacket) -> Any:
        return {"status": "completed", "output": f"Result for: {task.description}"}

    def _retrieve_reflections(self, task_description: str) -> list[str]:
        """Query memory_reflection for prior reflections relevant to this
        brief, at brief-construction time — proactive retrieval so relevant
        past reflections are surfaced before the brief is issued, rather
        than only being discoverable via a later manual search.

        Never blocks or delays brief issuance and never raises: no injected
        fn, an empty/degraded response, or an exception from the fn itself
        all fall through to returning [] — "no matching reflection found,
        proceed" — the expected steady state at initial rollout before any
        records are migrated into memory_reflection. Mirrors search_memory's
        own timeout-guarded, degrade-gracefully contract one layer up; this
        call site introduces no new failure-mode class of its own.

        Returned notes are informational ("required read"), not binding
        constraints — the caller routes them into HandoffPacket's dedicated
        retrieved_reflections field, never sacred_context, since a retrieved
        reflection is not automatically a decision the receiving agent must
        not override, even when its source ReflectionRecord has sacred=True.
        Every match is treated uniformly regardless of the record's own
        sacred flag — simpler than branching sacred matches into
        sacred_context, and defensible since sacred_context's contract is
        about orchestrator-level decisions, not surfaced memory.
        """
        if self._reflection_search_fn is None:
            return []
        try:
            response = self._reflection_search_fn(task_description)
        except Exception as exc:
            logger.warning(
                "Reflection retrieval failed for brief %r — proceeding without it: %s",
                task_description,
                exc,
            )
            return []
        if not isinstance(response, dict) or response.get("degraded"):
            return []
        results = response.get("results") or []
        notes: list[str] = []
        for record in results:
            if not isinstance(record, dict):
                continue
            summary = record.get("summary")
            if not summary:
                continue
            note = f"[reflection:{record.get('reflection_id', 'unknown')}] {summary}"
            scope = record.get("scope_of_applicability")
            if scope:
                note += f" (applies when: {scope})"
            notes.append(note)
        return notes

    # -- Helpers -----------------------------------------------------------

    def _select_agent(self, task: SubTask) -> Optional[str]:
        for agent in self.agents:
            if agent.matches_task(task.domain):
                return agent.agent_id
        return self.agents[0].agent_id if self.agents else None

    @staticmethod
    def _calc_utilisation(plan: SwarmPlan) -> float:
        total = len(plan.subtasks)
        done = sum(1 for t in plan.subtasks if t.status == TaskStatus.COMPLETED)
        return done / total if total > 0 else 0.0

    @staticmethod
    def _gen_feedback(plan: SwarmPlan, result: SwarmResult) -> dict[str, Any]:
        return {
            "plan_id": plan.plan_id,
            "topology": plan.topology.value,
            "total_tasks": len(plan.subtasks),
            "completed": sum(
                1 for t in plan.subtasks if t.status == TaskStatus.COMPLETED
            ),
            "failed": sum(1 for t in plan.subtasks if t.status == TaskStatus.FAILED),
            # Several operators hitting GATE_FAILED on the same criterion
            # should read as one correlated signal on the SwarmResult, not
            # scattered per-task messages.
            "gate_failed": sum(
                1 for t in plan.subtasks if t.status == TaskStatus.GATE_FAILED
            ),
            "duration": result.total_duration,
            "utilisation": result.agent_utilisation,
        }

    @staticmethod
    def _gen_reflective_loop_feedback(plan: SwarmPlan) -> dict[str, Any]:
        """Reflective-cycle data: the rationale history behind every
        GATE_FAILED subtask, plus a per-subtask attempts-to-pass count for
        every subtask that used the loop at all (whether it ultimately
        passed, exhausted its retries, or is still mid-plan). Populated
        independently of SwarmConfig.enable_feedback_loop (a different,
        pre-existing opt-in for execution-health telemetry) — "flagged for
        review" must carry its actual reasons regardless of whether that
        unrelated flag happens to be on."""
        rationale_history = {
            t.task_id: list(t.reflection_rationale_history)
            for t in plan.subtasks
            if t.reflection_rationale_history
        }
        retry_counts = {
            t.task_id: t.reflection_retry_count
            for t in plan.subtasks
            if t.reflection_retry_count > 0
        }
        feedback: dict[str, Any] = {}
        if rationale_history:
            feedback["rationale_history"] = rationale_history
        if retry_counts:
            feedback["retry_counts"] = retry_counts
        return feedback
