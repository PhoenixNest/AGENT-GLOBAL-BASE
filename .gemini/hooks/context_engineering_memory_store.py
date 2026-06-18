"""
Memory Store — Four Memory Type Implementations

Provides EpisodicMemory, SemanticMemory, ProceduralMemory, and WorkingMemory
classes corresponding to the four memory types defined in:
    fundamentals/memory-types.md

Usage:
    em = EpisodicMemory(session_id="session-abc")
    em.record_event("decision", "User chose PostgreSQL over MySQL")
    sacred = em.get_sacred_context()

    sm = SemanticMemory()
    sm.store("user_stack", "User prefers FastAPI, PostgreSQL, pytest")
    facts = sm.query("Which database?", top_k=3)
"""

import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------

def _now() -> float:
    return time.time()


def _estimate_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except ImportError:
        return max(1, int(len(text) / 4))


# ---------------------------------------------------------------------------
# Episodic Memory
# ---------------------------------------------------------------------------

@dataclass
class EpisodicEvent:
    """A single recorded event in episodic memory."""
    event_type: str      # "decision" | "commitment" | "task_complete" | "error" | "general"
    content: str
    timestamp: float = field(default_factory=_now)
    turn: int = 0
    sacred: bool = False  # Decisions and commitments are sacred


SACRED_EVENT_TYPES = {"decision", "commitment"}


class EpisodicMemory:
    """
    Session-scoped memory for events that happened during the conversation.

    Decisions and commitments are automatically marked as sacred and
    returned verbatim via get_sacred_context().

    Usage:
        em = EpisodicMemory(session_id="session-abc123")
        em.record_event("decision", "User chose PostgreSQL")
        em.record_event("task_complete", "Schema design finished")
        sacred = em.get_sacred_context()
        recent = em.recent_turns(n=5)
    """

    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self._events: List[EpisodicEvent] = []
        self._turn_counter: int = 0

    def advance_turn(self) -> int:
        """Increment the turn counter. Call once per conversation turn."""
        self._turn_counter += 1
        return self._turn_counter

    def record_event(self, event_type: str, content: str) -> EpisodicEvent:
        """
        Record a new episodic event.

        Args:
            event_type: "decision" | "commitment" | "task_complete" | "error" | "general"
            content: Human-readable description of the event.

        Returns:
            The recorded EpisodicEvent.
        """
        is_sacred = event_type in SACRED_EVENT_TYPES
        event = EpisodicEvent(
            event_type=event_type,
            content=content,
            turn=self._turn_counter,
            sacred=is_sacred,
        )
        self._events.append(event)
        if is_sacred:
            print(f"INFO: Sacred context recorded [{event_type}]: {content[:60]}...",
                  file=sys.stderr)
        return event

    def get_sacred_context(self) -> List[str]:
        """
        Return all decisions and commitments verbatim.
        These must be re-injected into every context window for the session.
        """
        return [
            f"[{e.event_type.capitalize()} — Turn {e.turn}] {e.content}"
            for e in self._events
            if e.sacred
        ]

    def recent_turns(self, n: int = 5) -> List[Dict[str, Any]]:
        """Return the N most recent events as message-compatible dicts."""
        recent = self._events[-n:]
        return [
            {"role": "system", "content": f"[{e.event_type}] {e.content}"}
            for e in recent
        ]

    def get_events_by_type(self, event_type: str) -> List[EpisodicEvent]:
        """Filter events by type."""
        return [e for e in self._events if e.event_type == event_type]

    def summarise(self, max_tokens: int = 500) -> str:
        """Create a compressed summary of all non-sacred events."""
        non_sacred = [e for e in self._events if not e.sacred]
        lines = [f"Turn {e.turn} [{e.event_type}]: {e.content}" for e in non_sacred]
        summary = " | ".join(lines)
        if _estimate_tokens(summary) > max_tokens:
            # Truncate to budget
            words = summary.split()
            truncated = []
            count = 0
            for w in words:
                count += 1
                if count * 1.3 > max_tokens:
                    break
                truncated.append(w)
            summary = " ".join(truncated) + " [truncated]"
        return summary

    def clear(self) -> None:
        """Clear all events (use at session end)."""
        self._events.clear()
        self._turn_counter = 0

    def __len__(self) -> int:
        return len(self._events)


# ---------------------------------------------------------------------------
# Semantic Memory
# ---------------------------------------------------------------------------

@dataclass
class SemanticFact:
    """A single persistent fact in semantic memory."""
    key: str
    value: str
    created_at: float = field(default_factory=_now)
    expires_after_seconds: Optional[float] = None  # None = never expires
    confidence: float = 1.0
    tags: List[str] = field(default_factory=list)

    @property
    def is_expired(self) -> bool:
        if self.expires_after_seconds is None:
            return False
        return (_now() - self.created_at) > self.expires_after_seconds

    @property
    def age_days(self) -> float:
        return (_now() - self.created_at) / 86_400


class SemanticMemory:
    """
    Cross-session persistent memory for facts that outlive sessions.

    In production, back this with a vector database (Qdrant/Weaviate) or
    a key-value store (Redis). This implementation uses an in-memory dict
    suitable for development and testing.

    Usage:
        sm = SemanticMemory()
        sm.store("user_stack", "Prefers FastAPI, PostgreSQL, pytest",
                 expires_after_days=180)
        facts = sm.query("database preference", top_k=3)
    """

    def __init__(self):
        self._facts: Dict[str, SemanticFact] = {}

    def store(
        self,
        key: str,
        value: str,
        expires_after_days: Optional[float] = None,
        confidence: float = 1.0,
        tags: Optional[List[str]] = None,
    ) -> SemanticFact:
        """
        Store a persistent fact.

        Args:
            key: Unique identifier for this fact.
            value: The fact content.
            expires_after_days: TTL in days. None = permanent.
            confidence: How confident we are this fact is current (0–1).
            tags: Optional topic tags for filtering.
        """
        expires_secs = expires_after_days * 86_400 if expires_after_days else None
        fact = SemanticFact(
            key=key,
            value=value,
            expires_after_seconds=expires_secs,
            confidence=confidence,
            tags=tags or [],
        )
        self._facts[key] = fact
        return fact

    def get(self, key: str) -> Optional[str]:
        """Retrieve a fact by exact key. Returns None if missing or expired."""
        fact = self._facts.get(key)
        if fact is None:
            return None
        if fact.is_expired:
            print(f"INFO: Semantic fact '{key}' has expired and was evicted.", file=sys.stderr)
            del self._facts[key]
            return None
        return fact.value

    def query(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve top-K facts most relevant to the query.

        Production note: Replace this keyword-overlap implementation with
        a proper semantic similarity search using your vector database.

        Args:
            query_text: Natural language query.
            top_k: Maximum number of facts to return.

        Returns:
            List of dicts with 'key', 'value', 'confidence', 'age_days'.
        """
        query_words = set(query_text.lower().split())
        scored = []
        for key, fact in self._facts.items():
            if fact.is_expired:
                continue
            fact_words = set((key + " " + fact.value).lower().split())
            overlap = len(query_words & fact_words)
            score = (overlap / max(len(query_words), 1)) * fact.confidence
            if score > 0:
                scored.append((score, fact))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "key": f.key,
                "value": f.value,
                "confidence": f.confidence,
                "age_days": round(f.age_days, 1),
            }
            for _, f in scored[:top_k]
        ]

    def invalidate(self, key: str) -> bool:
        """Explicitly remove a fact."""
        if key in self._facts:
            del self._facts[key]
            return True
        return False

    def evict_expired(self) -> int:
        """Remove all expired facts. Returns count removed."""
        expired = [k for k, f in self._facts.items() if f.is_expired]
        for k in expired:
            del self._facts[k]
        return len(expired)

    def __len__(self) -> int:
        return len(self._facts)


# ---------------------------------------------------------------------------
# Procedural Memory
# ---------------------------------------------------------------------------

class ProceduralMemory:
    """
    Cross-session memory for behavioural patterns — how to act in situations.

    In this workspace, procedural memory is primarily represented by the
    agent profile (system prompt) and skill files. This class provides a
    runtime interface for loading and activating skill-level procedures.

    Usage:
        pm = ProceduralMemory()
        pm.register("code_review", "Review for correctness, security, performance.")
        instruction = pm.activate("code_review")
    """

    def __init__(self):
        self._procedures: Dict[str, str] = {}

    def register(self, skill_name: str, instruction: str) -> None:
        """Register a procedural skill (how to do something)."""
        self._procedures[skill_name] = instruction

    def activate(self, skill_name: str) -> Optional[str]:
        """
        Activate a procedure. Returns the instruction text to inject into
        the system slot, or None if the skill is not registered.
        """
        return self._procedures.get(skill_name)

    def list_skills(self) -> List[str]:
        """Return all registered skill names."""
        return list(self._procedures.keys())

    def __len__(self) -> int:
        return len(self._procedures)


# ---------------------------------------------------------------------------
# Working Memory
# ---------------------------------------------------------------------------

class WorkingMemory:
    """
    Single-turn memory for the current task and its immediate sub-goals.

    Lives entirely in the active context window (tool output slot).
    Cleared after each turn.

    Usage:
        wm = WorkingMemory()
        wm.set_task("Build authentication API")
        wm.set_current_step("Step 2 of 4: Define endpoint schemas")
        wm.add_tool_result("schema_validator", {"valid": True})
        context_fragment = wm.to_context_string()
    """

    def __init__(self):
        self._task: Optional[str] = None
        self._current_step: Optional[str] = None
        self._completed_steps: List[str] = []
        self._tool_results: List[Dict[str, Any]] = []
        self._notes: List[str] = []

    def set_task(self, description: str) -> "WorkingMemory":
        self._task = description
        return self

    def set_current_step(self, step: str) -> "WorkingMemory":
        self._current_step = step
        return self

    def complete_step(self, step: str) -> "WorkingMemory":
        self._completed_steps.append(step)
        if self._current_step == step:
            self._current_step = None
        return self

    def add_tool_result(self, tool_name: str, result: Any) -> "WorkingMemory":
        self._tool_results.append({"tool": tool_name, "result": result})
        return self

    def add_note(self, note: str) -> "WorkingMemory":
        """Add a reasoning note or intermediate conclusion."""
        self._notes.append(note)
        return self

    def to_context_string(self) -> str:
        """Serialise working memory to a string for injection into tool output slot."""
        lines = ["[WORKING MEMORY]"]
        if self._task:
            lines.append(f"Task: {self._task}")
        if self._current_step:
            lines.append(f"Current step: {self._current_step}")
        if self._completed_steps:
            lines.append(f"Completed: {', '.join(self._completed_steps)}")
        for tr in self._tool_results:
            lines.append(f"Tool [{tr['tool']}]: {tr['result']}")
        for note in self._notes:
            lines.append(f"Note: {note}")
        return "\n".join(lines)

    def clear(self) -> "WorkingMemory":
        """Reset for the next turn."""
        self._task = None
        self._current_step = None
        self._completed_steps.clear()
        self._tool_results.clear()
        self._notes.clear()
        return self


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
        
        # Memory Store is an AfterAgent hook. 
        # Perform any instantiation or saving logic here.
        # For now, simply act as a safe pass-through.
        wm = WorkingMemory()
        
        # Print strictly formatted JSON to stdout
        print(json.dumps(event_payload))
        sys.exit(0)
        
    except Exception as e:
        print(f"Memory Store Error: {e}", file=sys.stderr)
        sys.exit(1)
