"""
Context Assembler — Production Context Window Assembly Engine

Assembles a priority-ordered, budget-compliant context window from typed
inputs (system, retrieved, history, tool outputs) according to task-aware
slot budgets.

Usage:
    assembler = ContextAssembler(max_tokens=128_000)
    assembler.set_system("You are an expert software architect.")
    assembler.add_retrieved(docs, query="authentication patterns")
    assembler.add_history(turns)
    assembler.add_tool_output("schema_validator", result)
    context = assembler.build(task_type="code_generation")
"""

import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Token estimation (replace with tiktoken in production)
# ---------------------------------------------------------------------------


def _estimate_tokens(text: str) -> int:
    try:
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        return max(1, int(len(text) / 4))


# ---------------------------------------------------------------------------
# Slot budget profiles  (system / retrieved / history / tools)
# ---------------------------------------------------------------------------

BUDGET_PROFILES: Dict[str, Dict[str, float]] = {
    "factual_qa": {"system": 0.10, "retrieved": 0.65, "history": 0.10, "tools": 0.15},
    "code_generation": {
        "system": 0.15,
        "retrieved": 0.45,
        "history": 0.20,
        "tools": 0.20,
    },
    "creative_writing": {
        "system": 0.20,
        "retrieved": 0.20,
        "history": 0.50,
        "tools": 0.10,
    },
    "tool_research": {
        "system": 0.10,
        "retrieved": 0.35,
        "history": 0.15,
        "tools": 0.40,
    },
    "multi_turn_reason": {
        "system": 0.15,
        "retrieved": 0.20,
        "history": 0.55,
        "tools": 0.10,
    },
    "orchestration": {
        "system": 0.20,
        "retrieved": 0.30,
        "history": 0.10,
        "tools": 0.40,
    },
}

VALID_TASK_TYPES = set(BUDGET_PROFILES.keys())


# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------


@dataclass
class ContextItem:
    """A single item candidate for inclusion in a context slot."""

    content: str
    slot: str  # "system" | "retrieved" | "history" | "tools"
    relevance: float = 0.5  # Semantic similarity to current query (0–1)
    recency: float = 0.5  # Recency score (1.0 = most recent)
    importance: float = 0.5  # Domain importance weight (0–1)
    sacred: bool = False  # Sacred items always included regardless of score
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def score(self) -> float:
        if self.sacred:
            return float("inf")
        return (self.relevance * 0.5) + (self.recency * 0.3) + (self.importance * 0.2)

    def token_count(self) -> int:
        return _estimate_tokens(self.content)


@dataclass
class HandoffPacket:
    """Structured context forwarded from orchestrator to subagent."""

    tier: str  # "full" | "scoped" | "minimal"
    system: str
    task: str
    sacred_context: List[str] = field(default_factory=list)
    retrieved: List[Dict] = field(default_factory=list)
    working_memory: Dict[str, Any] = field(default_factory=dict)
    acceptance_criteria: List[str] = field(default_factory=list)
    return_schema: Dict[str, Any] = field(default_factory=dict)
    budget: int = 32_000


@dataclass
class AssembledContext:
    """The final assembled context window, ready for model call."""

    messages: List[Dict[str, str]]
    total_tokens: int
    slot_usage: Dict[str, int]
    task_type: str
    warnings: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Core assembler
# ---------------------------------------------------------------------------


class ContextAssembler:
    """
    Assembles a priority-ordered, budget-compliant context window.

    Usage:
        assembler = ContextAssembler(max_tokens=128_000)
        assembler.set_system("You are an expert software architect.")
        assembler.add_retrieved(docs, query="auth patterns")
        assembler.add_history(turns)
        context = assembler.build(task_type="code_generation")
    """

    SAFETY_BUFFER = 0.90  # Never use more than 90% of the context window

    def __init__(self, max_tokens: int = 128_000):
        self.max_tokens = max_tokens
        self.usable_tokens = int(max_tokens * self.SAFETY_BUFFER)
        self._system: Optional[str] = None
        self._retrieved: List[ContextItem] = []
        self._history: List[ContextItem] = []
        self._tools: List[ContextItem] = []
        self._sacred: List[str] = []

    # ------------------------------------------------------------------
    # Input setters
    # ------------------------------------------------------------------

    def set_system(self, content: str) -> "ContextAssembler":
        """Set the system slot content. Called once per session."""
        self._system = content
        return self

    def add_retrieved(
        self,
        items: List[Dict],
        query: str = "",
        relevance_scores: Optional[List[float]] = None,
    ) -> "ContextAssembler":
        """
        Add documents to the retrieved slot.

        Args:
            items: List of dicts with at least a 'content' key.
                   Optional: 'source', 'timestamp', 'importance'.
            query: Used to label the retrieval context.
            relevance_scores: Optional pre-computed relevance scores.
        """
        scores = relevance_scores or [0.5] * len(items)
        for i, item in enumerate(items):
            content = item.get("content", str(item))
            source = item.get("source", "unknown")
            timestamp = item.get("timestamp", "")
            label = f"[Source: {source}"
            if timestamp:
                label += f", {timestamp}"
            label += "]"

            self._retrieved.append(
                ContextItem(
                    content=f"{label}\n{content}",
                    slot="retrieved",
                    relevance=scores[i],
                    recency=item.get("recency", 0.5),
                    importance=item.get("importance", 0.5),
                    metadata={"source": source, "query": query},
                )
            )
        return self

    def add_history(
        self,
        turns: List[Dict],
        sacred_indices: Optional[List[int]] = None,
    ) -> "ContextAssembler":
        """
        Add conversation turns to the history slot.

        Args:
            turns: List of dicts with 'role' and 'content' keys.
            sacred_indices: Indices of turns that must never be compressed.
        """
        sacred_set = set(sacred_indices or [])
        n = len(turns)
        for i, turn in enumerate(turns):
            recency = (i + 1) / n  # Higher = more recent
            is_sacred = i in sacred_set
            self._history.append(
                ContextItem(
                    content=f"[{turn.get('role', 'user').capitalize()}]: {turn.get('content', '')}",
                    slot="history",
                    relevance=0.5,
                    recency=recency,
                    importance=1.0 if is_sacred else 0.5,
                    sacred=is_sacred,
                )
            )
        return self

    def add_sacred_context(self, text: str) -> "ContextAssembler":
        """
        Add a decision or commitment that must be preserved verbatim.
        Sacred context is re-injected at the top of the history slot on every turn.
        """
        self._sacred.append(text)
        return self

    def add_tool_output(
        self,
        tool_name: str,
        result: Any,
        importance: float = 0.8,
    ) -> "ContextAssembler":
        """Add a validated tool result to the tool output slot."""
        content = f"[Tool: {tool_name}]\n{result}"
        self._tools.append(
            ContextItem(
                content=content,
                slot="tools",
                relevance=0.8,
                recency=1.0,
                importance=importance,
            )
        )
        return self

    # ------------------------------------------------------------------
    # Assembly
    # ------------------------------------------------------------------

    def build(self, task_type: str = "multi_turn_reason") -> AssembledContext:
        """
        Assemble the final context window.

        Args:
            task_type: One of VALID_TASK_TYPES. Determines slot budget split.

        Returns:
            AssembledContext with messages list ready for model call.
        """
        if task_type not in VALID_TASK_TYPES:
            print(
                f"WARNING: Unknown task_type '{task_type}', falling back to multi_turn_reason",
                file=sys.stderr,
            )
            task_type = "multi_turn_reason"

        profile = BUDGET_PROFILES[task_type]
        budgets = {
            slot: int(ratio * self.usable_tokens) for slot, ratio in profile.items()
        }
        warnings = []
        slot_usage: Dict[str, int] = {}

        # --- System slot ---
        system_content = self._system or "You are a helpful assistant."
        system_tokens = _estimate_tokens(system_content)
        if system_tokens > budgets["system"]:
            warnings.append(
                f"System slot exceeds budget ({system_tokens} > {budgets['system']} tokens). "
                "Consider shortening system instructions."
            )
        slot_usage["system"] = system_tokens

        # --- Retrieved slot ---
        selected_retrieved = _priority_fill(self._retrieved, budgets["retrieved"])
        # Slot-order anchoring: highest score first + last
        selected_retrieved = _anchor_order(selected_retrieved)
        retrieved_content = "\n\n".join(i.content for i in selected_retrieved)
        slot_usage["retrieved"] = sum(i.token_count() for i in selected_retrieved)

        # --- History slot ---
        # Sacred context always injected first
        sacred_block = ""
        if self._sacred:
            lines = "\n".join(f"- {s}" for s in self._sacred)
            sacred_block = (
                "═══ DECISIONS AND COMMITMENTS (NEVER COMPRESS) ═══\n"
                f"{lines}\n"
                "══════════════════════════════════════════════════"
            )
        sacred_tokens = _estimate_tokens(sacred_block) if sacred_block else 0
        remaining_history_budget = budgets["history"] - sacred_tokens

        selected_history = _priority_fill(self._history, remaining_history_budget)
        selected_history = sorted(selected_history, key=lambda x: x.recency)
        history_parts = []
        if sacred_block:
            history_parts.append(sacred_block)
        history_parts.extend(i.content for i in selected_history)
        history_content = "\n".join(history_parts)
        slot_usage["history"] = _estimate_tokens(history_content)

        # --- Tool output slot (placed last for maximum recency) ---
        selected_tools = _priority_fill(self._tools, budgets["tools"])
        tools_content = "\n\n".join(i.content for i in selected_tools)
        slot_usage["tools"] = sum(i.token_count() for i in selected_tools)

        # --- Assemble messages ---
        messages: List[Dict[str, str]] = []
        full_system = system_content
        if retrieved_content:
            full_system += f"\n\n--- RETRIEVED CONTEXT ---\n{retrieved_content}"
        messages.append({"role": "system", "content": full_system})

        if history_content:
            messages.append({"role": "user", "content": history_content})

        if tools_content:
            messages.append({"role": "tool", "content": tools_content})

        total_tokens = sum(slot_usage.values())
        if total_tokens > self.usable_tokens:
            warnings.append(
                f"Total assembled context ({total_tokens} tokens) exceeds "
                f"safety buffer ({self.usable_tokens} tokens). Consider compressing history."
            )
            print(f"WARNING: {warnings[-1]}", file=sys.stderr)

        return AssembledContext(
            messages=messages,
            total_tokens=total_tokens,
            slot_usage=slot_usage,
            task_type=task_type,
            warnings=warnings,
        )

    def build_handoff(
        self,
        tier: str,
        subagent_task: str,
        relevant_decisions: Optional[List[str]] = None,
        retrieved_filter=None,
        acceptance_criteria: Optional[List[str]] = None,
        return_schema: Optional[Dict] = None,
        subagent_budget: int = 32_000,
    ) -> HandoffPacket:
        """
        Build a context handoff packet for a subagent.

        Args:
            tier: "full" | "scoped" | "minimal"
            subagent_task: Description of what the subagent must produce.
            relevant_decisions: Subset of sacred context to forward (scoped tier).
            retrieved_filter: Callable to filter retrieved items (scoped tier).
            acceptance_criteria: What "done" looks like.
            return_schema: Expected output format dict.
            subagent_budget: Token budget allocated to the subagent.
        """
        if tier not in ("full", "scoped", "minimal"):
            raise ValueError(
                f"Invalid handoff tier: '{tier}'. Use 'full', 'scoped', or 'minimal'."
            )

        system = self._system or "You are a helpful assistant."
        sacred = relevant_decisions if tier == "scoped" else self._sacred
        retrieved: List[Dict] = []

        if tier in ("full", "scoped"):
            items = self._retrieved
            if tier == "scoped" and retrieved_filter:
                items = [i for i in items if retrieved_filter(i)]
            retrieved = [{"content": i.content, "metadata": i.metadata} for i in items]

        working_mem: Dict[str, Any] = {}
        if self._tools:
            working_mem["last_tool_outputs"] = [t.content for t in self._tools[-2:]]

        return HandoffPacket(
            tier=tier,
            system=system,
            task=subagent_task,
            sacred_context=list(sacred or []),
            retrieved=retrieved,
            working_memory=working_mem,
            acceptance_criteria=acceptance_criteria or [],
            return_schema=return_schema or {},
            budget=subagent_budget,
        )

    def reset(self) -> "ContextAssembler":
        """Clear all accumulated context (start a new turn)."""
        self._retrieved.clear()
        self._history.clear()
        self._tools.clear()
        self._sacred.clear()
        return self


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _priority_fill(items: List[ContextItem], budget_tokens: int) -> List[ContextItem]:
    """Greedily fill a slot budget by priority score, sacred items always included."""
    sacred = [i for i in items if i.sacred]
    candidates = sorted(
        [i for i in items if not i.sacred],
        key=lambda x: x.score,
        reverse=True,
    )
    selected = list(sacred)
    used = sum(i.token_count() for i in sacred)

    for item in candidates:
        cost = item.token_count()
        if used + cost <= budget_tokens:
            selected.append(item)
            used += cost

    return selected


def _anchor_order(items: List[ContextItem]) -> List[ContextItem]:
    """
    Apply slot-order anchoring: highest-score item first, second-highest last.
    Items in between are ordered by descending score.
    This maximises attention on the most important content.
    """
    if len(items) <= 2:
        return sorted(items, key=lambda x: x.score, reverse=True)

    ranked = sorted(items, key=lambda x: x.score, reverse=True)
    middle = ranked[2:]
    return [ranked[0]] + middle + [ranked[1]]
