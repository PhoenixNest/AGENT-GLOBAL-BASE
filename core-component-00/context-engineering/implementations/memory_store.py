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
from typing import Any, Dict, List, Optional, Tuple


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

    def __init__(self, session_id: str = "default", sink: Optional[Any] = None):
        """
        Args:
            session_id: Session scope for this memory instance.
            sink: Optional write-through target implementing write_episodic()
                  (see context-engineering/implementations/memory_vector_store.py
                  PersistentMemorySink). None preserves the pre-existing
                  in-memory-only behaviour; production callers inject a
                  PersistentMemorySink to also persist to the JSONL log and the
                  memory_episodic Qdrant collection.
        """
        self.session_id = session_id
        self._events: List[EpisodicEvent] = []
        self._turn_counter: int = 0
        self._sink = sink

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
        if self._sink is not None:
            try:
                self._sink.write_episodic(event, self.session_id)
            except Exception as exc:
                print(f"WARNING: episodic write-through to sink failed: {exc}", file=sys.stderr)
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

    def __init__(self, sink: Optional[Any] = None):
        """
        Args:
            sink: Optional write-through target implementing write_semantic()
                  (see memory_vector_store.PersistentMemorySink). None preserves
                  the pre-existing in-memory-only behaviour.
        """
        self._facts: Dict[str, SemanticFact] = {}
        self._sink = sink

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
        if self._sink is not None:
            try:
                self._sink.write_semantic(fact)
            except Exception as exc:
                print(f"WARNING: semantic write-through to sink failed: {exc}", file=sys.stderr)
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

    def __init__(self, sink: Optional[Any] = None, source_session_id: Optional[str] = None):
        """
        Args:
            sink: Optional write-through target implementing write_procedural()
                  (see memory_vector_store.PersistentMemorySink). None preserves
                  the pre-existing in-memory-only behaviour.
            source_session_id: Session to attribute persisted corrections to.
        """
        self._procedures: Dict[str, str] = {}
        self._sink = sink
        self._source_session_id = source_session_id

    def register(self, skill_name: str, instruction: str) -> None:
        """Register a procedural skill (how to do something)."""
        self._procedures[skill_name] = instruction
        if self._sink is not None:
            try:
                self._sink.write_procedural(skill_name, instruction, self._source_session_id)
            except Exception as exc:
                print(f"WARNING: procedural write-through to sink failed: {exc}", file=sys.stderr)

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
# Reflection Memory
# ---------------------------------------------------------------------------
#
# The fourth memory type, added by the 2026-07-14-reflexion-memory-system
# Programme (Phase 1). Full design: core-component-00/telescope/
# 2026-07-14-reflexion-memory-system/supporting/01-technical-options.md §1
# and supporting/02-storage-specification.md.
#
# Unlike episodic/semantic/procedural, a ReflectionRecord is never
# constructed by application code from arbitrary agent output — only by the
# Investigator-Authored Write Path (implementations/reflection_authoring.py),
# which enforces a real, non-spoofable identity check before a record is
# ever built. No MCP write tool exists or should ever be added for this
# memory type (01-technical-options.md §4, "Option A" explicitly rejected).

TRIGGER_TYPES = {
    "process_violation",
    "defect_root_cause",
    "ase_exception_closure",
    "adversarial_finding",
    "director_flagged",
}

GOVERNANCE_TRIGGERS = {"process_violation", "defect_root_cause", "ase_exception_closure"}


@dataclass
class ReflectionRecord:
    """A single synthesized, investigator-gated reflection.

    See 02-storage-specification.md §1.1 for the trigger taxonomy and §2.2
    for the field-by-field rationale. `summary` is the Reflexion-style
    verbal lesson — synthesized, not a copy of the triggering event — and,
    together with `scope_of_applicability`, is the text embedded into the
    memory_reflection Qdrant collection (01-technical-options.md §2).
    """
    reflection_id: str                 # e.g. "REFLECT-001"
    trigger_type: str                  # one of TRIGGER_TYPES — see 02-storage-specification.md §1.1
    source_event_ref: str              # pointer to the originating report/event, e.g.
                                        # "core-component-00/telescope/2026-07-13-mcp-embedder-service-redesign/supporting/mistake-log.md#MISTAKE-001"
    summary: str                       # synthesized verbal reflection (Reflexion-style) — not a copy of the source
    root_cause: str
    remediation: str
    scope_of_applicability: str        # what future situations should surface this record
    severity: Optional[str] = None     # "P0" | "P1" | None (only for defect_root_cause)
    logged_by: str = ""                # named investigator of record — never "agent"
    timestamp: float = field(default_factory=_now)
    sacred: bool = False               # defaults True for GOVERNANCE_TRIGGERS at construction time
    status: str = "active"             # "active" | "dormant" | "archived" — irrelevant while sacred
    migrated_from: Optional[str] = None  # e.g. "mistake-log.md#MISTAKE-001"

    def __post_init__(self):
        if self.trigger_type not in TRIGGER_TYPES:
            raise ValueError(f"Unknown trigger_type: {self.trigger_type}")
        if self.trigger_type in GOVERNANCE_TRIGGERS and not self.sacred:
            self.sacred = True  # governance triggers are sacred unless the caller already set it
        if not self.logged_by:
            raise ValueError("ReflectionRecord requires a named logged_by investigator")

    def to_dict(self) -> Dict[str, Any]:
        """Serialise to a JSON-safe dict — the full reflection payload
        persisted verbatim to reflection-log.jsonl and to the
        memory_reflection Qdrant collection's point payload
        (01-technical-options.md §2: "Payload fields: All ReflectionRecord
        fields verbatim")."""
        return {
            "reflection_id": self.reflection_id,
            "trigger_type": self.trigger_type,
            "source_event_ref": self.source_event_ref,
            "summary": self.summary,
            "root_cause": self.root_cause,
            "remediation": self.remediation,
            "scope_of_applicability": self.scope_of_applicability,
            "severity": self.severity,
            "logged_by": self.logged_by,
            "timestamp": self.timestamp,
            "sacred": self.sacred,
            "status": self.status,
            "migrated_from": self.migrated_from,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReflectionRecord":
        """Reconstruct a ReflectionRecord from a dict produced by to_dict()
        (or an equivalent JSONL/Qdrant payload). Re-runs __post_init__
        validation, so a corrupted or hand-edited record on disk is caught
        on read, not silently trusted."""
        return cls(
            reflection_id=data["reflection_id"],
            trigger_type=data["trigger_type"],
            source_event_ref=data["source_event_ref"],
            summary=data["summary"],
            root_cause=data["root_cause"],
            remediation=data["remediation"],
            scope_of_applicability=data["scope_of_applicability"],
            severity=data.get("severity"),
            logged_by=data.get("logged_by", ""),
            timestamp=data.get("timestamp", _now()),
            sacred=data.get("sacred", False),
            status=data.get("status", "active"),
            migrated_from=data.get("migrated_from"),
        )


@dataclass(frozen=True)
class IdentityVerification:
    """
    Opaque proof that implementations/reflection_authoring.py's
    verify_authorized_identity() has run and passed for a specific
    logged_by value. ReflectionMemory.record_reflection() requires one of
    these — never a bare logged_by string — as its `identity` argument.

    This closes the direct-import bypass documented in
    core-component-00/telescope/2026-07-14-reflexion-memory-system/
    supporting/audits/mistake-log.md (MISTAKE-2026-07-16-001): before this
    gate existed, any caller importing memory_store.py directly (rather
    than going through reflection_authoring.py) could call
    record_reflection() with an arbitrary logged_by and no identity check
    ran at all — reflection_authoring.py's wrapper was the *only* enforced
    checkpoint, and it was trivially skippable by importing this module
    instead.

    Honest limitation, per mistake-log.md's 2026-07-16 Update (second
    Wieczorek pass): this is not a cryptographic guarantee, and cannot be
    made into one. Python has no true encapsulation — a caller who reads
    this module's source can still construct an IdentityVerification
    instance directly (`IdentityVerification(logged_by=..., git_identity=...,
    governance_confirmation=...)`) without ever having called
    verify_authorized_identity() or require_governance_confirmation(). Two
    rounds of adversarial review established this is a structural ceiling,
    not an engineering gap awaiting a cleverer fix: in a process an agent
    has import access to, any in-process check is skippable by calling
    something lower. What each field here does is narrower and honestly
    bounded:

    - logged_by / git_identity close the *zero-effort* bypass (import
      memory_store, call record_reflection() with nothing but a string) —
      raises the bar to "requires deliberately fabricating this token."
    - governance_confirmation (added after the second Wieczorek pass) folds
      require_governance_confirmation()'s TTY-gated human confirmation
      result into the token itself, so forging a GOVERNANCE_TRIGGERS
      IdentityVerification requires fabricating *this* field too, not just
      skipping a separate, independently-callable confirmation step. This
      is a composition-gap fix, not a new unforgeability claim — the field
      is still a plain dataclass attribute, directly settable by any caller.

    For GOVERNANCE_TRIGGERS records, per 03-deployment-guidelines.md's
    revised Phase 1 "done" gate, the actual security boundary is procedural
    — genuine, live, in-transcript human confirmation in the coordinating
    session — not this token or any other code-level check. See
    implementations/reflection_authoring.py's module docstring for the
    full, current statement of that boundary.
    """
    logged_by: str
    git_identity: Tuple[str, str]
    verified_at: float = field(default_factory=_now)
    governance_confirmation: Optional[str] = None
    """Set only for GOVERNANCE_TRIGGERS records: the reflection_id
    require_governance_confirmation() (reflection_authoring.py) confirmed
    via a real interactive TTY + typed confirmation. record_reflection()
    requires this to equal the record's own reflection_id whenever
    trigger_type is in GOVERNANCE_TRIGGERS — see that method."""


class UnverifiedReflectionError(ValueError):
    """Raised by ReflectionMemory.record_reflection() when called without a
    valid IdentityVerification token, or with one issued for a different
    logged_by than the one supplied. Subclasses ValueError so any existing
    `except ValueError` handling around ReflectionRecord construction still
    catches this, while remaining distinguishable by type (isinstance
    checks, exception-type assertions in tests) from a plain schema-level
    ValueError raised by ReflectionRecord.__post_init__."""


class ReflectionMemory:
    """
    Cross-session persistent memory for investigator-gated reflections.

    Mirrors EpisodicMemory/SemanticMemory's sink write-through pattern
    exactly — record_reflection() plays the role of record_event()/store(),
    query() mirrors SemanticMemory.query()'s signature — so the module stays
    internally consistent for anyone already familiar with the other three
    memory types (01-technical-options.md §1).

    record_reflection() itself enforces the identity gate (requires a valid
    IdentityVerification — see that class's docstring) — this was
    previously enforced only by the reflection_authoring.py wrapper one
    layer up, which meant any caller importing this module directly bypassed
    the check entirely (MISTAKE-2026-07-16-001). The only sanctioned way to
    obtain an IdentityVerification in production use is
    implementations/reflection_authoring.py's verify_authorized_identity().

    Usage:
        from implementations.reflection_authoring import verify_authorized_identity
        identity = verify_authorized_identity("Mei-Ling Zhao")
        rm = ReflectionMemory(sink=sink)
        rm.record_reflection(
            reflection_id="REFLECT-001",
            trigger_type="process_violation",
            source_event_ref="core-component-00/telescope/.../mistake-log.md#MISTAKE-001",
            summary="...",
            root_cause="...",
            remediation="...",
            scope_of_applicability="...",
            logged_by="Mei-Ling Zhao",
            identity=identity,
        )
        matches = rm.query("git worktree orchestration", top_k=3)
    """

    def __init__(self, sink: Optional[Any] = None):
        """
        Args:
            sink: Optional write-through target implementing
                  write_reflection() (see
                  context-engineering/implementations/memory_vector_store.py
                  PersistentMemorySink). None preserves in-memory-only
                  behaviour, useful for tests.
        """
        self._reflections: Dict[str, ReflectionRecord] = {}
        self._sink = sink

    def record_reflection(
        self,
        reflection_id: str,
        trigger_type: str,
        source_event_ref: str,
        summary: str,
        root_cause: str,
        remediation: str,
        scope_of_applicability: str,
        logged_by: str,
        identity: IdentityVerification,
        severity: Optional[str] = None,
        sacred: bool = False,
        status: str = "active",
        migrated_from: Optional[str] = None,
    ) -> ReflectionRecord:
        """
        Construct, validate (via ReflectionRecord.__post_init__), store, and
        write through a new ReflectionRecord.

        Args:
            identity: The IdentityVerification returned by
                      reflection_authoring.verify_authorized_identity() for
                      this exact logged_by value. Required — there is no
                      default — so a caller cannot accidentally omit it.

        Raises:
            UnverifiedReflectionError: if `identity` is not a genuine
                IdentityVerification, was issued for a different logged_by
                than the one supplied here, or (for GOVERNANCE_TRIGGERS
                trigger types only) does not carry a governance_confirmation
                matching this exact reflection_id.
            ValueError: if trigger_type is not in TRIGGER_TYPES, or
                        logged_by is empty (ReflectionRecord.__post_init__).
        """
        if not isinstance(identity, IdentityVerification):
            raise UnverifiedReflectionError(
                "record_reflection() requires a verified IdentityVerification "
                "token (see implementations/reflection_authoring.py "
                "verify_authorized_identity()) — refusing to construct a "
                "ReflectionRecord without one, regardless of which module the "
                "caller imports from."
            )
        if identity.logged_by != logged_by:
            raise UnverifiedReflectionError(
                f"IdentityVerification was issued for logged_by="
                f"{identity.logged_by!r}, not {logged_by!r} — refusing to "
                "record under a mismatched identity."
            )
        if trigger_type in GOVERNANCE_TRIGGERS and identity.governance_confirmation != reflection_id:
            raise UnverifiedReflectionError(
                f"GOVERNANCE_TRIGGERS reflection {reflection_id!r} requires an "
                "IdentityVerification carrying a governance_confirmation that "
                "matches this exact reflection_id — the TTY-gated human "
                "confirmation (reflection_authoring.require_governance_confirmation()) "
                "was not attested for this record. Defense-in-depth only, per "
                "MISTAKE-2026-07-16-001: the actual security boundary for these "
                "records is procedural, not this check."
            )

        record = ReflectionRecord(
            reflection_id=reflection_id,
            trigger_type=trigger_type,
            source_event_ref=source_event_ref,
            summary=summary,
            root_cause=root_cause,
            remediation=remediation,
            scope_of_applicability=scope_of_applicability,
            severity=severity,
            logged_by=logged_by,
            sacred=sacred,
            status=status,
            migrated_from=migrated_from,
        )
        self._reflections[record.reflection_id] = record
        if record.sacred:
            print(f"INFO: Sacred reflection recorded [{trigger_type}]: {summary[:60]}...",
                  file=sys.stderr)
        if self._sink is not None:
            try:
                # identity is passed through so the sink can independently
                # re-verify it (PersistentMemorySink.write_reflection() —
                # memory_vector_store.py) rather than trusting that this
                # method already did — defense-in-depth against a caller
                # who bypasses ReflectionMemory and calls the sink directly
                # (the second bypass MISTAKE-2026-07-16-001 documents).
                self._sink.write_reflection(record, identity)
            except Exception as exc:
                print(f"WARNING: reflection write-through to sink failed: {exc}", file=sys.stderr)
        return record

    def get(self, reflection_id: str) -> Optional[ReflectionRecord]:
        """Retrieve a reflection by exact ID."""
        return self._reflections.get(reflection_id)

    def query(self, scope_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve top-K reflections most relevant to scope_text, scored by
        keyword overlap against `summary` + `scope_of_applicability` — the
        same two fields the memory_reflection Qdrant collection embeds
        (01-technical-options.md §2).

        Production note: this in-memory keyword-overlap implementation is a
        development/test fallback, mirroring SemanticMemory.query()'s own
        documented limitation. Production retrieval goes through
        agent-memory's search_memory tool with memory_type="reflection"
        (Phase 2 — out of scope for this module).

        Args:
            scope_text: Natural language description of the current
                        situation/task.
            top_k: Maximum number of reflections to return.

        Returns:
            List of dicts with 'reflection_id', 'summary',
            'scope_of_applicability', 'trigger_type', 'sacred'.
        """
        query_words = set(scope_text.lower().split())
        scored = []
        for record in self._reflections.values():
            haystack = f"{record.summary} {record.scope_of_applicability}".lower()
            haystack_words = set(haystack.split())
            overlap = len(query_words & haystack_words)
            score = overlap / max(len(query_words), 1)
            if score > 0:
                scored.append((score, record))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "reflection_id": r.reflection_id,
                "summary": r.summary,
                "scope_of_applicability": r.scope_of_applicability,
                "trigger_type": r.trigger_type,
                "sacred": r.sacred,
            }
            for _, r in scored[:top_k]
        ]

    def get_sacred_reflections(self) -> List[ReflectionRecord]:
        """Return all sacred reflections verbatim. GOVERNANCE_TRIGGERS
        records default sacred=True and are exempt from the decay job
        (02-storage-specification.md §2.3)."""
        return [r for r in self._reflections.values() if r.sacred]

    def __len__(self) -> int:
        return len(self._reflections)
