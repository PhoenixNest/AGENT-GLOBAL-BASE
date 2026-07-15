# Supporting Document 01 — Technical Options

**Programme:** `2026-07-14-reflexion-memory-system`
**Purpose:** The implementation-level counterpart to `02-storage-specification.md`. That document
answers what/why; this document answers _how_ — schema, collection design, embedding, and API
surface — precise enough to implement without further clarification, per this lab's
`llm-system-design.md` quality bar.

---

## 1. Schema — `ReflectionRecord`

Proposed addition to `context-engineering/implementations/memory_store.py`, following the existing
`EpisodicEvent`/`SemanticFact` dataclass style exactly (see that file's current contents):

```python
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
    """A single synthesized, investigator-gated reflection."""
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
```

`ReflectionMemory` (a new class alongside `EpisodicMemory`/`SemanticMemory`/`ProceduralMemory`/
`WorkingMemory`) exposes `record_reflection(...)` (construction + validation + write-through to
the sink, mirroring `EpisodicMemory.record_event`'s existing sink pattern exactly) and
`query(scope_text, top_k)` (mirroring `SemanticMemory.query`'s existing signature). No new pattern
is introduced at the Python API level — this is intentional, so the module stays internally
consistent for anyone already familiar with the other three memory types.

---

## 2. Collection Design

| Property               | Value                                                                                       | Rationale                                                                                                                                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Collection name        | `memory_reflection`                                                                         | Matches `memory_episodic`/`memory_semantic`/`memory_procedural` naming convention exactly                                                                                                                |
| Qdrant instance        | Existing `qdrant-memory` (`localhost:6335`), not a new instance                             | Reflections are a memory type, not a new blast-radius domain — reuses the isolation decision already made in `09-mcp-architecture-decision.md`                                                           |
| Embedding model        | `sentence-transformers/all-MiniLM-L6-v2` (384-dim) — same as the three existing collections | Consistency within one Qdrant instance; avoids provisioning a second model into the shared cache for no retrieval-quality reason                                                                         |
| Embedded field         | `summary` concatenated with `scope_of_applicability` (not `root_cause`/`remediation`)       | The two fields most predictive of "does this reflection apply to the task at hand" — keeps embedding focused on retrieval relevance, not full-text completeness (full record is still stored as payload) |
| Payload fields         | All `ReflectionRecord` fields verbatim                                                      | Full record retrievable without a second lookup, matching the existing collections' pattern                                                                                                              |
| Source-of-truth log    | `context-engineering/memory/reflection/reflection-log.jsonl` (single cross-session file)    | Per `02-storage-specification.md` §2.1 — reflections are inherently cross-session, unlike per-session episodic logs                                                                                      |
| Indexed payload fields | `trigger_type`, `sacred`, `status`, `severity`                                              | Enables filtered search (e.g., "only `process_violation`, only `sacred=true`") matching the existing collections' filter pattern in `search_memory`                                                      |

---

## 3. Decay/Lifecycle Reuse

No new decay formula. `ReflectionRecord.status` transitions through the same
`active → dormant → archived` lifecycle and the same Ebbinghaus-style exponential decay
implementation already specified in `2026-07-10-agent-memory-architecture/supporting/03-forgetting-strategy.md`
and (once implemented) the maintenance job that runs it — the only change is that
`GOVERNANCE_TRIGGERS`-sourced records are constructed `sacred=True` by default (§1), which the
existing decay job already knows how to skip (it already skips all `sacred=True` records
regardless of memory type, per that document's §5). This is a configuration-level reuse, not new
decay-engineering work.

---

## 4. Write Path — No New MCP Tool

Per `research-report.md` Finding 4, the write path deliberately does **not** add a tool to
`agent-memory`'s MCP server. Two concrete options were considered and compared as "Option A" and
"Option B" during this evaluation — those labels are retired below now that the CEO has finalized
the design, so this section is the one place they're recorded for historical reference; every
other document in this Programme names the chosen path directly instead.

| Candidate                                                                                    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                            | Verdict                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **MCP Write Tool** (`log_reflection`) — evaluated as "Option A"                              | An MCP tool an agent could call directly to persist a reflection                                                                                                                                                                                                                                                                                                                                                                                       | **Rejected.** Reopens the exact threat model `agent-memory/README.md` already declined to accept for its other three memory types — a prompt-injected call could write an arbitrary "reflection" that a future orchestrator brief would then trust and surface. No adversarial evaluation of this attack surface exists yet, and building it without one would violate the same caution the existing server already applies. |
| **Investigator-Authored Write Path** — evaluated as "Option B"; this is the finalized design | A named investigator/Director persona constructs a `ReflectionRecord` directly (e.g., via a short Python helper script or a documented manual step run by the authoring persona, analogous to how `mistake-log.md`'s entry or an ADR Exceptions Log entry is written today), which is validated against the dataclass's `__post_init__` checks and then written through the existing `PersistentMemorySink` pattern (JSONL append, then Qdrant upsert) | **Recommended and adopted.** Matches the gating step present in every benchmarked architecture (Finding 4); reuses the existing trusted-internal sink rather than opening a new externally-callable surface; keeps `logged_by` meaningfully attributable to a real person, not a spoofable agent identity.                                                                                                                   |

The Investigator-Authored Write Path is intentionally low-ceremony (a short script, not a new
service) — the ceremony belongs to the human judgment step (does this event clear §1.1's
taxonomy?), not to the software mechanics of writing the record once that judgment has been made.

---

## 5. Retrieval Surface

Two retrieval paths, both read-only, both reusing `agent-memory`'s existing timeout-guarded,
never-raises `search_memory` contract:

1. **On-demand:** extend `search_memory`'s `memory_type` parameter to accept `"reflection"`
   alongside the existing `"episodic"|"semantic"|"procedural"` — no new tool, no new failure
   mode class, same degrade-gracefully contract already documented in
   `agent-memory/README.md` § Tools.
2. **Proactive, orchestrator-brief-time:** a new call site inside
   `multi-agent-engineering/implementations/swarm_orchestrator.py`, at brief-construction time,
   querying `memory_reflection` against the brief's task description before the brief is issued
   to worker agents — surfacing any matching `scope_of_applicability` as a required read for the
   orchestrator, mirroring the Context Handoff Protocol's existing "Scoped" tier
   (`context-engineering/patterns/multi-agent-handoff.md`) rather than inventing a new handoff
   shape.

---

## 6. Effort Estimate

| Component                                                                                   | Effort   |
| ------------------------------------------------------------------------------------------- | -------- |
| `ReflectionRecord` + `ReflectionMemory` in `memory_store.py`, with unit tests               | 1–2 days |
| `memory_reflection` Qdrant collection creation + JSONL log wiring in `PersistentMemorySink` | 1 day    |
| `search_memory` extension (`memory_type="reflection"`)                                      | 0.5 day  |
| Investigator-Authored Write Path helper script                                              | 0.5 day  |
| `swarm_orchestrator.py` proactive-retrieval call site + test coverage                       | 2–3 days |

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-07-14-reflexion-memory-system`
