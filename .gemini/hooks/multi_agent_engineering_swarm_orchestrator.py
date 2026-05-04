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
    topology: str = "hybrid"
    max_agents: int = 10
    enable_git_worktree: bool = False
    variance_threshold: float = 0.20
    timeout_seconds: float = 300.0
    enable_feedback_loop: bool = True


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
        if self.started_at and self.completed_at:
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


class SwarmOrchestrator:
    """Production-grade multi-agent swarm orchestrator."""

    def __init__(
        self,
        config: SwarmConfig,
        agents: Optional[list[AgentProfile]] = None,
        execute_fn: Optional[Callable] = None,
    ):
        self.config = config
        self.agents = agents or []
        self._execute_fn = execute_fn or self._default_execute
        self._execution_log: list[dict[str, Any]] = []

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

        result = SwarmResult(
            plan_id=plan.plan_id,
            success=all(t.status == TaskStatus.COMPLETED for t in plan.subtasks),
            subtask_results=[
                {
                    "task_id": t.task_id,
                    "status": t.status.value,
                    "result": t.result,
                    "variance": t.variance,
                }
                for t in plan.subtasks
            ],
            total_duration=total_duration,
            agent_utilisation=self._calc_utilisation(plan),
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
        task.status = TaskStatus.DISPATCHED
        task.started_at = time.time()
        try:
            handoff = HandoffPacket(
                tier=HandoffTier.SCOPED,
                task=task.description,
                acceptance_criteria=task.gate_criteria or [],
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


# ---------------------------------------------------------------------------
# CLI Standard JSON I/O Runner
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json
    import sys
    
    try:
        input_data = sys.stdin.read()
        if input_data.startswith('\ufeff'):
            input_data = input_data[1:]
        if not input_data.strip():
            print(json.dumps({}))
            sys.exit(0)
            
        event_payload = json.loads(input_data)
        
        # Swarm Orchestrator is a BeforeAgent hook. 
        # Perform task distribution or sub-agent checks here.
        # For now, simply act as a safe pass-through.
        
        # Print strictly formatted JSON to stdout
        print(json.dumps(event_payload))
        sys.exit(0)
        
    except Exception as e:
        print(f"Swarm Orchestrator Error: {e}", file=sys.stderr)
        sys.exit(1)
