---
name: cc00-context-handoff-protocol-engineering
description: Tiered Context Handoff Protocol implementation (Full/Scoped/Minimal) for handoff_packet.py. Owned by Dr. Idris Farouk (Staff Research Engineer, Multi-Agent Engineering Lead). Trigger: context handoff, handoff packet, agent handoff, Full Scoped Minimal tiers.
version: "1.0.0"
---

# Context Handoff Protocol Engineering

**Skill ID:** context-handoff-protocol-engineering
**Role:** Staff Research Engineer — Multi-Agent Engineering Lead
**Seniority:** L4 — Staff

## Overview

Production implementation of `core-component-00/multi-agent-engineering/implementations/handoff_packet.py`
— the three-tier Context Handoff Protocol (Full / Scoped / Minimal) governing how orchestrator
agents forward state to subagents without over-sharing or under-sharing context, per
`core-component-00/context-engineering/patterns/multi-agent-handoff.md`.

## Tools & Frameworks

| Tool              | Proficiency | Use Case                                    |
| ----------------- | ----------- | ------------------------------------------- |
| Python            | Expert      | Handoff packet serialization and validation |
| Schema validation | Expert      | Enforcing tier-appropriate packet contents  |
| pytest            | Expert      | Cross-tier handoff regression coverage      |

## Module Ownership

- Maintains `handoff_packet.py`: packet construction for each of the three tiers, and validation
  that a packet does not exceed its tier's disclosure scope
- Owns tier-selection guidance for orchestrators: Full (complete context, same-trust-boundary
  handoff), Scoped (task-relevant subset, cross-team handoff), Minimal (task instruction only,
  external/untrusted subagent)
- Coordinates with Mei-Ling Zhao on how memory-store content maps into each handoff tier without
  leaking working-memory internals into a Minimal packet

## Scenarios & Trade-offs

### Scenario 1: Over-Sharing in Scoped Handoff

- **Approach:** Scoped packets are built from an explicit allowlist of context fields relevant to
  the subagent's task, not a filtered copy of the full context
- **Trade-off:** Allowlist construction requires the orchestrator to declare relevance explicitly,
  adding authoring overhead vs. a blanket filter
- **Quality Bar:** Zero fields present in a Scoped packet that the subagent's task does not require,
  verified by an automated packet-content audit

### Scenario 2: Minimal Handoff to External/Untrusted Subagent

- **Approach:** Minimal packets contain task instruction and explicit constraints only — no
  conversation history, no memory-store content, no System-slot identity details beyond what the
  task requires
- **Trade-off:** Minimal packets can under-inform a subagent that genuinely needs more context,
  producing lower-quality output — the tier boundary is a deliberate cost accepted for isolation
- **Quality Bar:** No credential, internal-only instruction, or unrelated task context ever appears
  in a Minimal packet, enforced by schema validation, not convention

## Quality Standards

- Every handoff tier has a schema that structurally prevents disclosure beyond its scope
- Handoff packets are logged for audit — which tier was used and why, at orchestration time
- Cross-tier regression suite verifies no tier accidentally inherits another tier's default fields

## References

- Multi-Agent Context Handoff Protocols (Dr. Vance, architecture spec, 2026)
- `core-component-00/context-engineering/patterns/multi-agent-handoff.md`
- `core-component-00/multi-agent-engineering/implementations/handoff_packet.py`
