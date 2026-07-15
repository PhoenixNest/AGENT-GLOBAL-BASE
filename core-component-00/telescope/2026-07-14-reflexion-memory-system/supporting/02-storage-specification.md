# Supporting Document 02 — Storage Specification

**Programme:** `2026-07-14-reflexion-memory-system`
**Purpose:** Answer the CEO's three explicit questions directly: what warrants storage as a
reflection, how it is stored, and why it must be persistent rather than ephemeral. This document
is the storage-design counterpart to `01-technical-options.md`'s implementation options — read
that document for embedding model, collection topology, and API surface; this document is about
_what_ goes in and _why_, not the wire format.

---

## 1. What Warrants Storage as a Reflection

A reflection is not a log entry. It is a **derived, synthesized judgment about why something
happened and what should change** — the output of an Evaluator step, per Reflexion's triad
(`research-report.md` Finding 2), not a copy of the triggering event itself. Storing every
`error`-typed episodic event as a reflection would fail Finding 3's importance-gate lesson from
Generative Agents and flood retrieval with noise. The gate below is this workspace's categorical
translation of that principle, chosen to match the governance model this workspace already uses
(`quality-assurance.md`'s P0–P3 severity scale) rather than a numeric importance score.

### 1.1 Trigger Taxonomy — the only five categories that warrant a reflection record

| Trigger type            | Definition                                                                                                                                            | Concrete precedent in this workspace                                                                                                                                                                   | Does NOT include                                                                                                 |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `process_violation`     | A documented workspace rule, convention, or written commitment was violated during execution                                                          | `MISTAKE-001` — a progress-tracking-file requirement violated across a full 6-phase build                                                                                                              | A style-guide nitpick or a P3 polish item                                                                        |
| `defect_root_cause`     | Root cause of a P0 or P1 defect (`quality-assurance.md` severity scale) — never P2/P3                                                                 | The embedder-loading stall root-caused to the MCP host's subprocess-launch path (`2026-07-13-mcp-embedder-service-redesign`)                                                                           | A P2 "workaround exists" defect, or a P3 typo                                                                    |
| `ase_exception_closure` | An ADR-ASE-001 Exceptions Log entry reaches `REMEDIATED, CLOSED` status                                                                               | `EX-001` — catch-all exception handling remediated and closed 2026-07-14                                                                                                                               | An exception still open/unresolved (reflect only once the lesson is confirmed, not speculative)                  |
| `adversarial_finding`   | Dr. Wieczorek's independent evaluation surfaces a systemic gap, not just a single bug                                                                 | The contradiction-check wrapper found to have "0% mitigation" against memory-poisoning/race-condition attacks (`2026-07-10-agent-memory-architecture/supporting/07-adversarial-evaluation-results.md`) | A finding already fully mitigated with no residual systemic risk                                                 |
| `director_flagged`      | Dr. Vance (or another Director-tier persona, cross-department) explicitly designates a lesson as reflection-worthy, outside the four categories above | Reserved for judgment calls the taxonomy doesn't yet anticipate — see Open Question 1 in `research-report.md`                                                                                          | A routine design decision already captured as sacred episodic `decision`/`commitment` content — do not duplicate |

**Explicitly excluded, regardless of category:** routine task completions, P2/P3 defects, ordinary
`general`-typed episodic events, and anything already fully and correctly captured by existing
sacred episodic memory (`SACRED_EVENT_TYPES = {"decision", "commitment"}` in `memory_store.py`) —
duplicating that content into `memory_reflection` would violate the Memory-as-Corpus principle's
existing single-source-of-truth discipline established by the prior programme.

### 1.2 The Gate Is a Necessary, Not Sufficient, Condition

Clearing a trigger category is necessary but not sufficient — the investigator authoring the
record must still be able to state a `root_cause` and a `remediation` (§2.2 below) in the schema.
An event that clears a trigger category but produces no actionable remediation (e.g., a one-off
environmental fluke with no systemic cause) is logged in the originating report's own findings
section, not promoted to a persistent reflection. This mirrors Reflexion's Evaluator step
producing a feedback _signal_ that the Self-Reflection step must still be able to turn into
useful verbal guidance — not every negative signal yields a usable reflection.

---

## 2. How Reflections Are Stored

### 2.1 Collection and Log Placement

A fourth Qdrant collection, `memory_reflection`, on the existing `qdrant-memory` instance
(`http://localhost:6335`) — not a new instance. Reflections are a memory _type_, not a new
blast-radius domain; they share `agent-memory`'s existing isolation from `workspace-knowledge`
(`09-mcp-architecture-decision.md` from the prior programme already made that isolation call at
the instance level, and it still holds). Source of truth is a single, cross-session, append-only
JSONL log — `context-engineering/memory/reflection/reflection-log.jsonl` — not one file per
session, because reflections are inherently cross-session by nature (unlike `memory_episodic`,
which is legitimately per-session). Full schema and embedding details: `01-technical-options.md` §2.

### 2.2 Record Shape (summary — full dataclass in `01-technical-options.md` §1)

Every reflection record carries: a stable ID, the `trigger_type` (§1.1), a pointer to the
originating event/report (`source_event_ref`), a synthesized `summary` (the verbal
self-reflection text, Reflexion-style — not a copy-paste of the source), an explicit
`root_cause` and `remediation`, a `scope_of_applicability` (what future situations should
surface this record — the field the orchestrator-brief-time retrieval hook queries against),
a `severity` aligned to `quality-assurance.md`'s P0–P3 scale where applicable, `logged_by` (the
named investigator — never `"agent"`, per §3), a timestamp, a `sacred` flag, a `status`
(`active`/`dormant`/`archived`), and an optional `migrated_from` pointer for records like
`MISTAKE-001` that originate in a pre-reflexion document.

### 2.3 Sacred-by-Default for Governance Triggers

`process_violation`, `defect_root_cause`, and `ase_exception_closure` reflections default
`sacred = True` — matching the existing `SACRED_EVENT_TYPES` precedent for decisions and
commitments — and are therefore exempt from the `active → dormant → archived` decay job (reused,
not redesigned, from `2026-07-10-agent-memory-architecture/supporting/03-forgetting-strategy.md`).
`adversarial_finding` and `director_flagged` reflections are sacred only if the authoring
investigator marks them so; a narrowly-scoped tactical finding (e.g., "this one specific API call
needs a retry wrapper," if ever raised to reflection status) may legitimately decay once its
remediation has shipped and been stable for a consolidation cycle. This two-tier default is a
judgment call, not an automated classification — flagged as Risk/Limitation in the main report.

---

## 3. Why Persistent Storage Is Required — Not Ephemeral Context

Three independent justifications, each sufficient on its own:

**3.1 — The lesson must outlive the session that produced it.** `MISTAKE-001` happened because a
correction to `git-worktree-orchestration.md` existed, but no future orchestrator brief was
required to consult it. Working memory and session-scoped episodic memory are both cleared or left
behind at session end (`memory_store.py`'s `WorkingMemory.clear()` and `EpisodicMemory`'s
session-scoping) — neither survives to the next swarm that needs the lesson. Only a persistent,
independently-retrievable store makes a lesson available to a _differently staffed_ future
session, exactly the gap `mistake-log.md` names.

**3.2 — The lesson must outlive the investigation that produced it.** A telescope report is
itself durable, but it is not designed to be _proactively retrieved_ — nothing today causes a
future orchestrator brief to consult `2026-07-13-mcp-embedder-service-redesign/` before issuing a
new brief on unrelated work. A dedicated, embedded, queryable store is what makes
`scope_of_applicability`-based retrieval possible at brief-issuance time (`research-report.md`
Recommendations §2) — a telescope report alone cannot be efficiently searched at that granularity
across dozens of past investigations.

**3.3 — Every benchmarked architecture treats this exact content as worth persisting.**
Reflexion's episodic reflection buffer, Generative Agents' reflection tree, and Anthropic's own
external-memory-under-truncation pattern (`research-report.md` Finding 1) all persist synthesized
judgments specifically because they are expensive to re-derive and cheap to reuse once captured.
A process-violation root cause, once correctly diagnosed, does not need to be re-diagnosed by a
future investigator encountering the same failure mode — that re-diagnosis cost is exactly what
persistence eliminates, and is the same cost/benefit argument that justified persisting
`memory_semantic` facts in the prior programme.

---

## 4. What Explicitly Stays Ephemeral

For symmetry with §1's inclusion criteria: `WorkingMemory` (task-scoped, cleared every turn),
ordinary `general`-typed episodic events, and any `error`-typed episodic event that does not clear
a §1.1 trigger category remain exactly where they are today — in session-scoped or
`memory_episodic` storage, never promoted to `memory_reflection`. This is a deliberate boundary,
not an oversight: promoting everything would recreate the noise problem Finding 3 of the main
report identifies, and would undermine the precision that makes proactive orchestrator-brief-time
retrieval (§3.2) useful rather than another source of context bloat this workspace's own Sacred
Context principle already warns against (`context-engineering/fundamentals/`).

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-07-14-reflexion-memory-system`
