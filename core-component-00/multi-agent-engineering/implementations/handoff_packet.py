"""
Handoff Packet — Structured Inter-Agent Context Transfer

Implements the Three-Tier Handoff Protocol from the Context Engineering
module, providing a typed data structure for transferring context
between agents in a multi-agent swarm.

Version: 1.0
Last Updated: 2026-04-29
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class HandoffTier(Enum):
    """The three tiers of the Handoff Protocol."""

    FULL = "full"  # Complete context — use sparingly
    SCOPED = "scoped"  # Filtered to task-relevant context
    MINIMAL = "minimal"  # Task instruction + acceptance criteria only


@dataclass
class HandoffPacket:
    """
    Structured context transfer unit between agents.

    Attributes:
        tier: The handoff tier (Full, Scoped, Minimal).
        task: Description of the task to perform.
        acceptance_criteria: Criteria the result must satisfy.
        sacred_context: Decisions/constraints that MUST NOT be overridden.
        conversation_history: Prior conversation turns (Full tier only).
        relevant_files: File paths relevant to the task.
        budget: Token budget for the receiving agent.
        metadata: Arbitrary key-value metadata.
    """

    tier: HandoffTier = HandoffTier.SCOPED
    task: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    sacred_context: list[str] = field(default_factory=list)
    conversation_history: Optional[list[dict[str, str]]] = None
    relevant_files: list[str] = field(default_factory=list)
    budget: int = 128_000
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary for transport."""
        return {
            "tier": self.tier.value,
            "task": self.task,
            "acceptance_criteria": self.acceptance_criteria,
            "sacred_context": self.sacred_context,
            "conversation_history": self.conversation_history,
            "relevant_files": self.relevant_files,
            "budget": self.budget,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> HandoffPacket:
        """Deserialize from dictionary."""
        return cls(
            tier=HandoffTier(data.get("tier", "scoped")),
            task=data.get("task", ""),
            acceptance_criteria=data.get("acceptance_criteria", []),
            sacred_context=data.get("sacred_context", []),
            conversation_history=data.get("conversation_history"),
            relevant_files=data.get("relevant_files", []),
            budget=data.get("budget", 128_000),
            metadata=data.get("metadata", {}),
        )

    def validate(self) -> list[str]:
        """Validate the packet and return a list of issues."""
        issues = []
        if not self.task:
            issues.append("Task description is empty")
        if self.tier == HandoffTier.FULL and not self.conversation_history:
            issues.append("Full tier requires conversation_history")
        if self.tier == HandoffTier.MINIMAL and self.conversation_history:
            issues.append("Minimal tier should not include conversation_history")
        return issues

    @property
    def estimated_tokens(self) -> int:
        """Rough estimate of token count for this packet."""
        text = self.task + " ".join(self.acceptance_criteria)
        text += " ".join(self.sacred_context)
        if self.conversation_history:
            for msg in self.conversation_history:
                text += msg.get("content", "")
        return len(text) // 4  # Rough token estimate
