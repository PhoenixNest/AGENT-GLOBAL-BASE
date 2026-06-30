# CC-00 Q2 2026 Research Commission — Implementation Plan

## Header

| Field           | Value                                                                                                                                        |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Plan ID**     | CC00-IMPL-2026-06-30                                                                                                                         |
| **Prepared by** | Dr. Elias Vance, Laboratory Director CC-00                                                                                                   |
| **Date**        | 2026-06-30                                                                                                                                   |
| **Status**      | Active — T01–T13 Implementation Complete; T14–T16 (GSMSE Remediation) Approved, Pending Implementation                                       |
| **Source**      | `telescope/2026-06-30-llm-engineering-stack-research/research-report.md`                                                                     |
| **Scope**       | 16 tasks (4 P0 + 12 P1) across four CC-00 modules; includes GSMSE sub-issue (TEL-2026-06-30-GSMSE)                                           |
| **Timeline**    | 2026-07-01 to 2026-07-14 (2 calendar weeks, reference only)                                                                                  |
| **Note**        | Effort estimates are reference-only; CEO pre-approves any day-count adjustments. Each task is assigned to a named agent by the Lab Director. |

---

## Executive Summary

The Q2 2026 research commission has closed all five active CC-00 research programmes with
empirically grounded findings. The resulting remediation work comprises **four P0 items**
(critical — implementation gaps that create production risk today) and **twelve P1 items**
(high — improvements that unlock the next tier of reliability). All 16 items are contained
within the existing CC-00 codebase and require no new architecture. The total estimated effort
is **~24.5 working days** across four module owners (original 23 d + ~1.5 d GSMSE remediation).
Tasks T01–T13 were implemented and merged to `core00/dev/engineering` on 2026-06-30. Tasks
T14–T16 address the GSM Scope Enforcement Gap (TEL-2026-06-30-GSMSE) identified by the T08
audit; CEO approved the remediation plan on 2026-06-30.

---

## Task Breakdown

| ID  | Priority | Item                                                                                                                | Module                  | Deliverable                            | Effort ¹ | Depends On | Assigned Agent                |
| --- | -------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------- | -------------------------------------- | -------- | ---------- | ----------------------------- |
| T01 | **P0**   | Override SDK timeouts per tier in `error_boundary.py` (Haiku 15s / Sonnet 30s / Opus 90s)                           | harness-engineering     | Updated `error_boundary.py`            | 4 h      | —          | Harness Engineering Agent     |
| T02 | **P0**   | Align `context_compressor.py` with Compaction API (`compact_20260112`); use `instructions` param for Sacred Context | context-engineering     | Updated `context_compressor.py`        | 2–3 d ²  | —          | Context Engineering Agent     |
| T03 | **P0**   | Document git-as-substrate coordination pattern with `current_tasks/` file locking spec                              | multi-agent-engineering | `patterns/git-coordination.md`         | 1 d      | —          | Multi-Agent Engineering Agent |
| T04 | **P0**   | Build cross-tier prompt evaluation harness (15 prompts, 3 tiers, perturbation variants)                             | prompt-engineering      | `testing/prompt_eval_harness.py`       | 4–5 d ²  | —          | Prompt Engineering Agent      |
| T05 | P1       | Implement 4-state circuit breaker (CLOSED / DEGRADED / OPEN / HALF-OPEN) with composite health score                | harness-engineering     | Updated `error_boundary.py`            | 2 d      | T01        | Harness Engineering Agent     |
| T06 | P1       | Swarm-level circuit breaker OPEN signal in `swarm_orchestrator.py`                                                  | multi-agent + harness   | Updated `swarm_orchestrator.py`        | 1 d      | T05        | Multi-Agent Engineering Agent |
| T07 | P1       | Implement `shared_memory_log.py` (event-sourced append log with GSM scope predicate)                                | multi-agent-engineering | `implementations/shared_memory_log.py` | 3 d      | T03        | Multi-Agent Engineering Agent |
| T08 | P1       | Audit all shared memory access paths for GSM scope enforcement                                                      | multi-agent-engineering | Audit report + patches                 | 1 d      | T07        | Multi-Agent Engineering Agent |
| T09 | P1       | Benchmark ACON methodology vs `context_compressor.py` on 100-turn session samples                                   | context-engineering     | Benchmark report + data                | 3 d      | T02        | Context Engineering Agent     |
| T10 | P1       | Add `min_tier` field to all persona agent profiles; annotate prompts with stability class                           | prompt-engineering      | Updated `profile.md` files             | 1 d      | T04        | Prompt Engineering Agent      |
| T11 | P1       | Implement classifier-selective CoT (suppress CoT for fine-tuned or low-stability prompts)                           | prompt-engineering      | `implementations/cot_classifier.py`    | 2 d      | T04        | Prompt Engineering Agent      |
| T12 | P1       | Enable streaming by default in `error_boundary.py` to reduce TTFT exposure                                          | harness-engineering     | Updated `error_boundary.py`            | 4 h      | T01        | Harness Engineering Agent     |
| T13 | P1       | Instrument CC-00 module latency benchmark (per-tier p50/p95/p99)                                                    | harness-engineering     | `testing/latency_benchmark.py`         | 2 d      | T01, T12   | Harness Engineering Agent     |

**GSMSE Remediation — TEL-2026-06-30-GSMSE (CEO Approved 2026-06-30; status: Pending Implementation)**

| ID  | Priority | Item                                                                                                              | Module                  | Deliverable                                     | Effort ¹ | Depends On | Assigned Agent                |
| --- | -------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------- | ----------------------------------------------- | -------- | ---------- | ----------------------------- |
| T14 | P1       | Patch `swarm_orchestrator.py` — inject `SharedMemoryLog`; scope `subtask_results` + `synthesized_output` to FLEET | multi-agent-engineering | Updated `swarm_orchestrator.py`                 | 4 h      | T07        | Multi-Agent Engineering Agent |
| T15 | P1       | Patch `handoff_packet.py` — add `write_to_log()` / `read_from_log()` with `MemoryScope.FLEET`                     | multi-agent-engineering | Updated `handoff_packet.py`                     | 4 h      | T07        | Multi-Agent Engineering Agent |
| T16 | P1       | Add `test_gsm_scope_enforcement.py`; update `gsm-shared-state-classification.md` to mark 4 paths REMEDIATED       | multi-agent-engineering | `testing/test_gsm_scope_enforcement.py` + audit | 2 h      | T14, T15   | Multi-Agent Engineering Agent |

¹ All effort estimates are reference-only. The CEO pre-approves any day-count adjustments proposed by the assigned agent.
² Lab Director note (Dr. Vance, 2026-06-30): T02 may require 3d due to beta API integration surface; T04 may require 5d due to harness fixture complexity. Assigned agents to confirm on Day 1.

**Total effort:** ~23 working days across 4 module tracks (parallelised to 2 calendar weeks; reference only)

---

## Gantt Timeline

### Week 1 — 2026-07-01 to 2026-07-05 (P0 Items)

All four P0 items execute in parallel across module tracks from day one.

```
Module                 │ Mon 07/01 │ Tue 07/02 │ Wed 07/03 │ Thu 07/04 │ Fri 07/05 │
───────────────────────┼───────────┼───────────┼───────────┼───────────┼───────────┤
harness-engineering    │  T01 ████ │           │           │           │           │
context-engineering    │  T02 ████ │  T02 ████ │           │           │           │
multi-agent-eng.       │  T03 ████ │           │           │           │           │
prompt-engineering     │  T04 ████ │  T04 ████ │  T04 ████ │  T04 ████ │           │
```

**Week 1 gate:** All four P0 items must be complete before Week 2 begins. T01 (4 h) unblocks
T05, T12, and T13. T03 (1 d) unblocks T07.

### Week 2 — 2026-07-07 to 2026-07-11 (P1 Items)

P1 items execute sequenced by dependency chain; parallel tracks continue.

```
Module                 │ Mon 07/07 │ Tue 07/08 │ Wed 07/09 │ Thu 07/10 │ Fri 07/11 │
───────────────────────┼───────────┼───────────┼───────────┼───────────┼───────────┤
harness-engineering    │  T05 ████ │  T05 ████ │  T12 ████ │  T13 ████ │  T13 ████ │
context-engineering    │  T09 ████ │  T09 ████ │  T09 ████ │           │           │
multi-agent-eng.       │  T07 ████ │  T07 ████ │  T07 ████ │  T08 ████ │  T06 ████ │
prompt-engineering     │  T10 ████ │  T11 ████ │  T11 ████ │           │           │
```

**Buffer:** 2026-07-14 (Mon) reserved as overflow / integration day for any slippage.

### Week 3 — GSMSE Remediation (T14–T16)

T14 and T15 execute in parallel (independent files); T16 follows after both complete.

```
Module                 │ T14 ████   │ T15 ████   │ T16 ██   │
multi-agent-eng.       │ (4 h)      │ (4 h)      │ (2 h)    │
```

**Gate:** All four AT-RISK paths must pass `pytest multi-agent-engineering/testing/ -v` (including
`test_gsm_scope_enforcement.py`) before `gsm-shared-state-classification.md` is updated to REMEDIATED.

---

## Risk Register

| Risk                                                                                                                        | Item(s)            | Severity | Mitigation                                                                                                                 |
| --------------------------------------------------------------------------------------------------------------------------- | ------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------- |
| Compaction API (`compact_20260112`) is in beta — breaking change possible                                                   | T02, T09           | Medium   | Pin to exact beta version string; add integration test that detects API version change at import time                      |
| GSM scope audit may reveal more access paths than estimated                                                                 | T08                | Medium   | Cap initial scope to `swarm_orchestrator.py` + `handoff_packet.py`; file separate tickets for additional paths             |
| Prompt eval harness requires cross-tier model access (Haiku + Sonnet + Opus)                                                | T04                | Low      | Confirm API key has all three tiers before starting; fallback: mock Opus responses in CI                                   |
| Circuit breaker DEGRADED state requires a composite health metric not yet defined                                           | T05                | Medium   | Use v1 composite: error rate (40%) + p99 latency vs threshold (40%) + 429 rate (20%); document as v1                       |
| T06 spans two modules — coordination risk                                                                                   | T06                | Low      | Assign single owner; T06 is a thin wrapper over T05's OPEN signal; keep PR small                                           |
| T04 cascade — if prompt eval harness slips, T10 and T11 slip with it                                                        | T04, T10, T11      | Medium   | Checkpoint T04 at ~80% completion before Week 2; invoke buffer day (07/14) if needed; compress T10+T11 into 3-day sequence |
| `error_boundary.py` regression chain — T01, T05, T12, T13 all modify the same file                                          | T01, T05, T12, T13 | Medium   | Run `pytest harness-engineering/testing/ -v` as mandatory gate before merging each of T05, T12, and T13                    |
| GSMSE: `fleet_id` not yet enforced by `SwarmOrchestrator` — T14/T15 require a persistent fleet ID per orchestrator instance | T14, T15           | Medium   | Add `fleet_id: str` to `SwarmConfig`; generate UUID if not provided; treat as prerequisite for T14 and T15                 |
| GSMSE: scope decision for `synthesized_output` — GLOBAL may be appropriate in orchestrator hierarchies                      | T14                | Low      | Lab Director to confirm scope before T14; default FLEET unless an explicit hierarchy requirement is stated                 |

---

## Sign-Off Block

**T01–T13:** CEO approved 2026-06-30; implementation complete 2026-06-30 (merged to `core00/dev/engineering`).

**T14–T16 (GSMSE Remediation):** CEO approved remediation plan 2026-06-30; implementation pending Lab Director scheduling.

| Approver | Decision | Date       | Scope           | Notes                                   |
| -------- | -------- | ---------- | --------------- | --------------------------------------- |
| CEO      | Approved | 2026-06-30 | T01–T13         | Full commission implementation approved |
| CEO      | Approved | 2026-06-30 | T14–T16 (GSMSE) | Remediation plan D1/D2/D3 approved      |

---

## Version History

| Version | Date       | Author       | Changes                                                                                                                                                                                                                                 |
| ------- | ---------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-06-30 | Dr. E. Vance | Initial plan — awaiting CEO approval                                                                                                                                                                                                    |
| 1.1     | 2026-06-30 | Dr. E. Vance | CEO guidance applied: effort estimates marked reference-only; Assigned Agent column added (T01–T13); T12→T13 dependency added; two missing risks added (T04 cascade, `error_boundary.py` regression chain); T02/T04 effort ranges noted |
| 1.2     | 2026-06-30 | Dr. E. Vance | Status updated (T01–T13 complete); T14–T16 added for GSMSE remediation (TEL-2026-06-30-GSMSE); Week 3 Gantt added; two GSMSE risks added; Sign-Off Block updated with dual CEO approval rows                                            |
