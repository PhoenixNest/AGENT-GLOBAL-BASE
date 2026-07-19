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
        try:
            handoff = HandoffPacket(
                tier=HandoffTier.SCOPED,
                task=task.description,
                acceptance_criteria=task.gate_criteria or [],
                retrieved_reflections=self._retrieve_reflections(task.description),
            )
            result = await asyncio.wait_for(
                self._execute_fn(task, handoff),
                timeout=self.config.timeout_seconds,
            )
            task.result = result
            task.status = TaskStatus.COMPLETED
        except Exception as exc:
            task.status = TaskStatus.FAILED
            task.result = {"error": str(exc)}
        finally:
            task.completed_at = time.time()

    @staticmethod
    async def _default_execute(task: SubTask, handoff: HandoffPacket) -> Any:
        return {"status": "completed", "output": f"Result for: {task.description}"}

    def _retrieve_reflections(self, task_description: str) -> list[str]:
        """Query memory_reflection for prior reflections relevant to this
        brief, at brief-construction time — proactive retrieval per
        telescope/2026-07-14-reflexion-memory-system/supporting/
        01-technical-options.md §5.2.

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
            "duration": result.total_duration,
            "utilisation": result.agent_utilisation,
        }
