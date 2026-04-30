"""
Multi-Agent Engineering — Implementations Package

Provides the core Python implementations for the multi-agent
engineering module: swarm orchestration, git worktree management,
and inter-agent context handoff.
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
from .git_worktree_manager import GitWorktreeManager, WorktreeInfo

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
    "GitWorktreeManager",
    "WorktreeInfo",
]
