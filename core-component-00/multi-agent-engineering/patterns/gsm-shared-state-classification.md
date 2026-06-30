# GSM Scope Audit — Shared State Classification

**Audit Date:** 2026-06-30
**Scope:** `implementations/swarm_orchestrator.py`, `implementations/handoff_packet.py`
**Auditor:** Multi-Agent Engineering Agent
**Standard:** Governed Shared Memory (GSM) Pattern — F = (A, M, G, P, T)
**Reference:** `patterns/git-coordination.md`, `implementations/shared_memory_log.py`

---

## Executive Summary

This audit classifies every location where shared state is passed between agents
in the two in-scope files. The scope predicate `P` in the GSM formula is the
critical control: a path is COMPLIANT when shared data is either scoped to the
requesting fleet or is intentionally GLOBAL; it is AT-RISK when shared data
crosses agent or fleet boundaries without a scope predicate check.

| Classification          | Count |
| ----------------------- | ----- |
| **COMPLIANT**           | 6     |
| **AT-RISK**             | 4     |
| **OUT-OF-SCOPE**        | 4     |
| **Total paths audited** | 14    |

**Priority remediation:** `SwarmResult.subtask_results`, `SwarmResult.synthesized_output`,
`HandoffPacket.conversation_history`, and `HandoffPacket.metadata` are the four AT-RISK
paths. None is catastrophic in the current single-fleet deployment, but all four will leak
cross-fleet data if multi-fleet operation is enabled without remediation.

---

## Findings Table

| Location                                                                    | Pattern                                                                                                                                                                                                                            | Classification   | Recommended Fix                                                                                                                                                                                                                                            |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `swarm_orchestrator.py:127` — `SwarmResult.subtask_results`                 | Aggregates result dicts from all agent executions; the list is built in `execute()` without a fleet_id filter and exposed to callers unscoped                                                                                      | **REMEDIATED**   | Write each result entry via `SharedMemoryLog.write(scope=MemoryScope.FLEET, key=f"result:{task_id}", value=result_dict)`; callers read via `read_all(requesting_fleet_id=fleet_id)` which applies the scope predicate automatically                        |
| `swarm_orchestrator.py:128` — `SwarmResult.synthesized_output`              | `synthesize()` concatenates outputs from all completed subtasks into a single string with no fleet attribution                                                                                                                     | **REMEDIATED**   | Scope the synthesis to the requesting fleet: filter `subtask_results` by `fleet_id` before concatenation, or store the synthesized string in `SharedMemoryLog` at `MemoryScope.FLEET`                                                                      |
| `swarm_orchestrator.py:233–240` — `HandoffPacket` in `_dispatch()`          | Constructs a `HandoffPacket(tier=HandoffTier.SCOPED, ...)` scoped to the task description and acceptance criteria; no cross-agent raw state is included                                                                            | **COMPLIANT**    | —                                                                                                                                                                                                                                                          |
| `swarm_orchestrator.py:103–104` — `SwarmPlan.subtasks` / `SwarmPlan.agents` | Shared mutable list accessed by all topology executors (`_execute_pipeline`, `_execute_fork_join`, `_execute_hybrid`) and by `_dispatch()`; asyncio cooperative scheduling guarantees no data races in the single-event-loop model | **COMPLIANT**    | —                                                                                                                                                                                                                                                          |
| `swarm_orchestrator.py:147` — `_execution_log`                              | Internal list on `SwarmOrchestrator` instance; accumulates `feedback` dicts from each run; never exposed to external agents or other fleets                                                                                        | **OUT-OF-SCOPE** | —                                                                                                                                                                                                                                                          |
| `swarm_orchestrator.py:191` — `result.feedback`                             | Dict generated by `_gen_feedback()` from plan metadata; appended to `_execution_log`; only the orchestrator itself reads it                                                                                                        | **OUT-OF-SCOPE** | —                                                                                                                                                                                                                                                          |
| `swarm_orchestrator.py:186–192` — `SwarmResult.agent_utilisation`           | Scalar ratio computed from task completion count; no agent-specific or fleet-specific state                                                                                                                                        | **COMPLIANT**    | —                                                                                                                                                                                                                                                          |
| `handoff_packet.py:46` — `HandoffPacket.sacred_context`                     | Unidirectional list of immutable constraints passed from orchestrator to receiving agent; read-only for the receiver; no cross-fleet data                                                                                          | **COMPLIANT**    | —                                                                                                                                                                                                                                                          |
| `handoff_packet.py:47` — `HandoffPacket.conversation_history`               | Populated only for `HandoffTier.FULL`; carries raw prior conversation turns that may contain context originating from other fleet's agent sessions if the orchestrator reuses a shared conversation object                         | **REMEDIATED**   | Validate that `conversation_history` entries were produced by agents in the same `fleet_id` before populating the packet; alternatively restrict FULL-tier handoffs to intra-fleet transfers with an explicit fleet-id check in `HandoffPacket.validate()` |
| `handoff_packet.py:48` — `HandoffPacket.relevant_files`                     | List of file path strings; references only, no state content; read-only hints for the receiving agent                                                                                                                              | **COMPLIANT**    | —                                                                                                                                                                                                                                                          |
| `handoff_packet.py:49` — `HandoffPacket.budget`                             | Scalar token budget; no sensitive or fleet-specific data                                                                                                                                                                           | **COMPLIANT**    | —                                                                                                                                                                                                                                                          |
| `handoff_packet.py:50` — `HandoffPacket.metadata`                           | Untyped `dict[str, Any]`; no scope enforcement; any caller may embed cross-fleet identifiers or sensitive state without detection                                                                                                  | **REMEDIATED**   | Add a `fleet_id: Optional[str]` field to `HandoffPacket`; update `validate()` to warn when `metadata` keys match known cross-fleet patterns; or pass metadata through `SharedMemoryLog.write(scope=MemoryScope.FLEET)` and resolve at read time            |
| `handoff_packet.py:52–63` — `to_dict()`                                     | Serialization of the packet fields to a plain dict for transport; mechanism only, not a state access point                                                                                                                         | **OUT-OF-SCOPE** | —                                                                                                                                                                                                                                                          |
| `handoff_packet.py:65–77` — `from_dict()`                                   | Deserialization from a plain dict; reconstructs a `HandoffPacket` from received data; does not introduce additional scope violations beyond the fields already classified                                                          | **OUT-OF-SCOPE** | —                                                                                                                                                                                                                                                          |

---

## AT-RISK Path Detail

### 1. `SwarmResult.subtask_results` (swarm_orchestrator.py:127)

**Risk:** Results from every agent in the swarm are collected into a single
unscoped list. In a multi-fleet deployment, if two fleets share an orchestrator
instance (possible through incorrect SwarmConfig reuse), each fleet's caller
receives all results, including those produced by agents in the other fleet.

**Recommended fix:**

```python
# In execute(), replace the direct list comprehension with:
result.subtask_results = [
    {
        "task_id": t.task_id,
        "status": t.status.value,
        "result": t.result,
        "variance": t.variance,
    }
    for t in plan.subtasks
    if t.assigned_agent in self._fleet_agent_ids  # scope to this fleet
]
# Or write each result to SharedMemoryLog and let callers read with scope predicate:
self._memory_log.write(
    agent_id=t.assigned_agent,
    fleet_id=self._fleet_id,
    scope=MemoryScope.FLEET,
    key=f"result:{t.task_id}",
    value={"status": t.status.value, "result": t.result},
)
```

### 2. `SwarmResult.synthesized_output` (swarm_orchestrator.py:128)

**Risk:** `synthesize()` joins outputs from all completed subtasks without
checking fleet membership of each result. In a multi-fleet scenario, synthesis
may include output from an adjacent fleet's agents.

**Recommended fix:** Filter `result.subtask_results` by `fleet_id` before
joining, or store the synthesized output under `MemoryScope.FLEET` in
`SharedMemoryLog` and return the key rather than the raw string.

### 3. `HandoffPacket.conversation_history` (handoff_packet.py:47)

**Risk:** The FULL tier is designed for high-context transfers. If the
orchestrator populates `conversation_history` from a shared session object
that is not fleet-scoped, prior turns from other fleets' agents leak into the
receiving agent's context window.

**Recommended fix:** Add a fleet-origin check in `validate()`:

```python
# In HandoffPacket.validate():
if self.tier == HandoffTier.FULL and self.conversation_history:
    for turn in self.conversation_history:
        if turn.get("fleet_id") not in (None, expected_fleet_id):
            issues.append(
                f"Cross-fleet turn detected in conversation_history: "
                f"fleet={turn.get('fleet_id')}"
            )
```

### 4. `HandoffPacket.metadata` (handoff_packet.py:50)

**Risk:** `metadata: dict[str, Any]` is a completely open channel. There is no
type constraint, no scope predicate, and no audit mechanism. Any caller can
embed fleet-crossing identifiers, raw agent outputs, or sensitive state without
detection.

**Recommended fix:**

```python
# Option A — scope-tagged metadata
self._memory_log.write(
    agent_id=sender_agent_id,
    fleet_id=fleet_id,
    scope=MemoryScope.FLEET,
    key=f"handoff_meta:{packet_id}",
    value=metadata_dict,
)
# Receiver reads with read(), which applies scope predicate silently.

# Option B — add fleet_id to HandoffPacket and validate metadata keys
@dataclass
class HandoffPacket:
    ...
    fleet_id: Optional[str] = None  # NEW — required for multi-fleet operation
```

---

## Compliance Notes

- All six COMPLIANT paths rely either on asyncio's cooperative scheduling
  (for `SwarmPlan.subtasks` mutation safety) or on the existing HandoffTier
  mechanism (for context scoping). Both are sound for current single-fleet
  deployments.
- The four OUT-OF-SCOPE paths are orchestrator-internal accumulators; they are
  not shared with external agents and require no remediation.
- Remediation of the four AT-RISK paths is **recommended before enabling
  multi-fleet operation** (`SwarmConfig.max_agents > 1` across multiple
  concurrent `SwarmOrchestrator` instances sharing a `SharedMemoryLog`).

---

---

## Remediation Status

**Formal sub-issue raised:** TEL-2026-06-30-GSMSE
(`telescope/2026-06-30-llm-engineering-stack-research/gsm-scope-enforcement/research-report.md`)

**CEO approval:** 2026-06-30 — remediation plan D1/D2/D3 approved.

**Implementation tasks:** CC00-IMPL-2026-06-30 v1.2, tasks T14–T16 (Multi-Agent Engineering Agent):

| Task | Deliverable                                                                                           | Status                  |
| ---- | ----------------------------------------------------------------------------------------------------- | ----------------------- |
| T14  | Patch `swarm_orchestrator.py` — scope `subtask_results` + `synthesized_output` to `MemoryScope.FLEET` | Complete — 2026-06-30   |
| T15  | Patch `handoff_packet.py` — add `write_to_log()` / `read_from_log()` with `MemoryScope.FLEET`         | Complete — 2026-06-30   |
| T16  | Add `test_gsm_scope_enforcement.py`; update this audit to mark 4 paths REMEDIATED                     | Complete — 2026-06-30   |

**Current state of AT-RISK paths:** REMEDIATED. All four paths now route through SharedMemoryLog with MemoryScope.FLEET scope enforcement (T14/T15) or validate fleet origin (T15). Multi-fleet operation gate cleared — T16 tests pass.

---

_Related:_ `implementations/shared_memory_log.py` (GSM reference implementation)
_Related:_ `patterns/git-coordination.md` (fleet isolation, cross-fleet rules)
_Related:_ `implementations/swarm_orchestrator.py`, `implementations/handoff_packet.py`
