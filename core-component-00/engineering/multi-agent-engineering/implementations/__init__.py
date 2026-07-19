"""
Multi-Agent Engineering — Implementations Package

Provides the core Python implementations for the multi-agent
engineering module: swarm orchestration and inter-agent context handoff.

Git worktree lifecycle management is handled at the Claude Code session
layer via the EnterWorktree tool and direct git subprocess calls, per
the five-phase specification in fundamentals/git-worktree-orchestration.md.
"""

from .handoff_packet import HandoffPacket, HandoffTier
from .swarm_orchestrator import (
    AgentProfile,
    SubTask,
    SwarmConfig,
    SwarmOrchestrator,
    SwarmPlan,
    SwarmResult,
    SwarmTopology,
    TaskStatus,
)

__all__ = [
    "HandoffPacket",
    "HandoffTier",
    "AgentProfile",
    "SubTask",
    "SwarmConfig",
    "SwarmOrchestrator",
    "SwarmPlan",
    "SwarmResult",
    "SwarmTopology",
    "TaskStatus",
]
