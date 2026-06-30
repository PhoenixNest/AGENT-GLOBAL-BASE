# Research Report — GSM Scope Enforcement Gap

---

## Metadata

| Field                | Value                                                    |
| -------------------- | -------------------------------------------------------- |
| **Investigation ID** | `2026-06-30-gsm-scope-enforcement`                       |
| **Date Started**     | 2026-06-30                                               |
| **Date Completed**   | — (Open)                                                 |
| **Status**           | Open — Pending Remediation                               |
| **Investigator**     | Dr. Elias Vance, Laboratory Director — Core Component 00 |
| **Laboratory**       | Core Component 00                                        |
| **Module(s)**        | `multi-agent-engineering/`                               |
| **Priority**         | P1 — High                                                |
| **Requestor**        | CEO — CC-00 Implementation Review (2026-06-30)           |
| **Parent Survey**    | `TEL-2026-06-30-CC00-COMMISSION`                         |
| **Issue Type**       | Sub-Issue (Implementation Finding)                       |

---

## Executive Summary

During the CC00-IMPL-2026-06-30 implementation sprint, a GSM scope audit (Task T08) identified
four data paths in the multi-agent engineering stack that cross agent boundaries without scope
enforcement: `SwarmResult.subtask_results`, `SwarmResult.synthesized_output`,
`HandoffPacket.conversation_history`, and `HandoffPacket.metadata`. These fields are stored and
accessed as plain Python objects with no fleet-scope predicate applied. While harmless in current
single-fleet deployments, they represent a latent cross-fleet data leakage risk once multi-fleet
operation is enabled. The GSM framework (arXiv:2606.24535) classifies this as the bimodal scope
enforcement vulnerability. Remediation routes all four paths through `SharedMemoryLog` with
`MemoryScope.FLEET` enforcement across three targeted deliverables (D1 – D3). CEO approved the
remediation plan on 2026-06-30.

---

## Investigation Scope

### What Was Investigated

This is not an original research programme — it is an implementation-phase finding from the
CC00-IMPL-2026-06-30 sprint. The GSM scope audit (Task T08) cross-referenced the multi-agent
implementations against the Governed Shared Memory scope predicate requirement established in the
Multi-Agent Memory Coherence sub-report (`multi-agent-memory-coherence/research-report.md`,
Finding 4).

Files audited:

- `core-component-00/multi-agent-engineering/implementations/swarm_orchestrator.py`
- `core-component-00/multi-agent-engineering/implementations/handoff_packet.py`

### Why This Was Raised

The Multi-Agent Memory Coherence research report documented the bimodal scope enforcement
vulnerability: every data access path must enforce scope predicates, not only search paths. When
`shared_memory_log.py` was implemented (T07) and introduced `MemoryScope` as a first-class
pattern, an audit of existing inter-agent data carriers (T08) revealed that `SwarmResult` and
`HandoffPacket` — the two primary cross-agent data objects — carried no scope enforcement
whatsoever. The CEO reviewed the audit finding and required CC-00 to document the risk and
provide a resolution plan.

### Out of Scope

- Single-fleet deployments (not affected by this issue in current production use)
- The `workspace-knowledge` MCP server (audited separately; passed the GSM governance gate)
- RAG module ACL filtering in `retrieval.py` (already implements scope predicates correctly)

---

## Risk Statement

The following four data paths in the CC-00 multi-agent stack carry no scope predicate:

| #   | Location        | Field                  | Risk if Multi-Fleet Deployed              |
| --- | --------------- | ---------------------- | ----------------------------------------- |
| 1   | `SwarmResult`   | `subtask_results`      | Cross-fleet subtask output visibility     |
| 2   | `SwarmResult`   | `synthesized_output`   | Cross-fleet synthesised output leakage    |
| 3   | `HandoffPacket` | `conversation_history` | Cross-fleet conversation context exposure |
| 4   | `HandoffPacket` | `metadata`             | Cross-fleet task metadata leakage         |

---

## Methodology

### How the Risk Was Identified

1. **Implementation of `shared_memory_log.py`** (T07) — introduced `MemoryScope` (FLEET /
   GLOBAL) and scope-enforced read semantics as a first-class CC-00 pattern.
2. **GSM scope audit** (T08) — cross-referenced all inter-agent data-carrying classes against
   the GSM scope predicate requirement from `multi-agent-memory-coherence/research-report.md`.
3. **Static path tracing** — each field of `SwarmResult` and `HandoffPacket` traced from write
   site to read site; fields without a scope predicate at any read path flagged AT-RISK.
4. **Reference comparison** — compared against the GSM bimodal vulnerability pattern: direct
   field access bypasses the scope-aware `SharedMemoryLog.read()` path.

### Audit Record

Full audit documented in:
`core-component-00/multi-agent-engineering/patterns/gsm-audit-2026-06-30.md`

---

## Findings

### Finding 1: SwarmResult Carries No Scope Enforcement

`SwarmResult` is the final output object of a `SwarmOrchestrator.run()` call. Its two primary
data fields have no scope predicate:

```python
@dataclass
class SwarmResult:
    task_id: str
    topology: SwarmTopology
    subtask_results: Dict[str, Any]    # ← no scope enforcement
    synthesized_output: Optional[str]  # ← no scope enforcement
    circuit_breaker_aborts: int = 0
```

`subtask_results` maps `task_id → agent output` for all subtasks in the swarm. In a
multi-fleet deployment, if two fleet orchestrators share a result store (file system, MCP
resource, or shared memory), the subtask outputs of Fleet A are readable by Fleet B agents
with no enforcement barrier.

**Risk level:** AT-RISK — blocked by single-fleet constraint; latent if multi-fleet enabled

---

### Finding 2: HandoffPacket Carries No Scope Enforcement

`HandoffPacket` implements the three-tier context handoff protocol (Full / Scoped / Minimal).
Both the Full and Scoped tiers carry unscoped fields:

```python
@dataclass
class HandoffPacket:
    conversation_history: List[Dict]  # ← no scope enforcement (Full tier)
    metadata: Dict[str, Any]          # ← no scope enforcement (Full + Scoped tier)
```

The `conversation_history` field may carry sensitive in-context data — prior tool outputs,
agent reasoning chains, partial results. In a multi-fleet handoff scenario, a receiving agent
in a different fleet could access this without a scope check.

**Risk level:** AT-RISK — same single-fleet constraint; higher data sensitivity

---

### Finding 3: Current Single-Fleet Deployment Is Not Affected

All four AT-RISK paths are benign in current single-fleet deployments because there is only one
fleet operating at a time — scope denial can never trigger. No data has been leaked and no
production incident has occurred. This risk is **latent and forward-looking**: it becomes an
active vulnerability when multi-fleet operation is introduced.

---

## Analysis

### Root Cause

`SwarmResult` and `HandoffPacket` predate the `SharedMemoryLog` implementation (T07). They
were designed as in-process data transfer objects with no persistence or cross-fleet sharing
model — the `MemoryScope` concept did not exist in the codebase when they were written.

When T07 introduced formal scope semantics, the existing data carriers were not retroactively
audited or updated. Standard technical debt accumulation during an implementation sprint.

### Bimodal Vulnerability Pattern

The GSM framework (arXiv:2606.24535, Security Finding) identifies this as the **bimodal scope
enforcement vulnerability**: scope predicates enforced on some access paths
(e.g., `SharedMemoryLog.read()`) but not on others (e.g., direct field access on
`SwarmResult`) create a bypass. The framework requirement is: every access path to governed
data must enforce identical scope predicates.

### Risk Assessment

| Dimension              | Assessment                                     |
| ---------------------- | ---------------------------------------------- |
| Current impact         | None (single-fleet only)                       |
| Forward risk           | High (cross-fleet data leakage in multi-fleet) |
| Exploitability         | Medium (requires multi-fleet configuration)    |
| Detection difficulty   | High (silent — no error raised, no audit log)  |
| Remediation complexity | Low (three focused, targeted changes)          |

---

## Recommendations

### Remediation Plan

**D1 — Patch `swarm_orchestrator.py`**

Inject a `SharedMemoryLog` instance into `SwarmOrchestrator`. On subtask completion, write the
result to the log under `MemoryScope.FLEET` keyed by `task_id`. Store `synthesized_output`
under the same fleet scope. Replace direct dict assignment on `SwarmResult` with
`shared_memory_log.write(...)` calls; reads use `shared_memory_log.read(...)` which silently
returns `None` on cross-fleet access.

**D2 — Patch `handoff_packet.py`**

Add `write_to_log(memory_log, agent_id, fleet_id)` and
`read_from_log(memory_log, requesting_agent_id, requesting_fleet_id, packet_id)` to
`HandoffPacket`. Store `conversation_history` and `metadata` under `MemoryScope.FLEET`. The
`read_from_log()` factory enforces the scope predicate at retrieval; cross-fleet reads
silently return `None` (consistent with GSM's enumeration-attack prevention pattern).

**D3 — Tests and audit update**

Add `test_gsm_scope_enforcement.py` to `multi-agent-engineering/testing/` with:

- `test_same_fleet_read_succeeds()` — write and read within the same `fleet_id` → non-None
- `test_cross_fleet_read_denied()` — write under fleet A, read as fleet B → `None`

Update `gsm-audit-2026-06-30.md` to mark all four paths REMEDIATED with implementation date.

### Implementation Priority

| Deliverable                        | Priority | Effort                     | Blocker For             |
| ---------------------------------- | -------- | -------------------------- | ----------------------- |
| D1 — `swarm_orchestrator.py` patch | P1       | ~4 hours                   | Multi-fleet operation   |
| D2 — `handoff_packet.py` patch     | P1       | ~4 hours                   | Multi-fleet operation   |
| D3 — Tests + audit update          | P1       | ~2 hours                   | Test suite completeness |
| **Total**                          |          | ~10 hours (~1.5 days ref.) |                         |

### Approval Status

CEO approved remediation plan: **2026-06-30**. Implementation pending Lab Director scheduling.

---

## References

### Internal Documentation

- `core-component-00/multi-agent-engineering/patterns/gsm-audit-2026-06-30.md`
  — Full audit record with all AT-RISK path details
- `core-component-00/multi-agent-engineering/implementations/swarm_orchestrator.py`
  — File to be patched (D1)
- `core-component-00/multi-agent-engineering/implementations/handoff_packet.py`
  — File to be patched (D2)
- `core-component-00/multi-agent-engineering/implementations/shared_memory_log.py`
  — The scope enforcement primitive (T07 deliverable)
- `telescope/2026-06-30-llm-engineering-stack-research/multi-agent-memory-coherence/research-report.md`
  — Source of GSM scope predicate principle (Finding 4, Security Finding)
- `telescope/2026-06-30-llm-engineering-stack-research/implementation-plan.md`
  — CC00-IMPL-2026-06-30 (Tasks T07, T08)

### External Sources

- GSM: Governed Shared Memory (arXiv:2606.24535):
  `https://arxiv.org/html/2606.24535v1` (accessed 2026-06-30)

---

## Open Questions

1. **Should `MemoryScope.GLOBAL` ever apply to `synthesized_output`?**
   - If Fleet A's synthesis is intentionally consumed by Fleet B in an orchestrator hierarchy,
     GLOBAL scope is appropriate. Current remediation assumes FLEET only.
   - Priority: Medium — decision required before D1 implementation
   - Owner: Lab Director (Dr. Elias Vance)

2. **Does multi-fleet operation require a formal fleet registry?**
   - For scope predicates to function across fleets, each fleet must carry a unique, persistent
     `fleet_id`. The current `SwarmOrchestrator` does not enforce or assign fleet IDs.
   - Priority: High — architectural prerequisite for D1 / D2
   - Owner: Lab Director

---

## Version History

| Version | Date       | Author                                                   | Changes                                  |
| ------- | ---------- | -------------------------------------------------------- | ---------------------------------------- |
| 1.0     | 2026-06-30 | Dr. Elias Vance, Laboratory Director — Core Component 00 | Initial risk record (implementation T08) |

---

**Template Version:** 1.0
**Last Updated:** 2026-06-30
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
