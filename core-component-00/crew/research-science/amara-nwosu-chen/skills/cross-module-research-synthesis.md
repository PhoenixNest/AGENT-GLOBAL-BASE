---
name: cc00-cross-module-research-synthesis
description: Synthesis of research findings across two or more CC-00 modules into a coherent cross-cutting result. Owned by Dr. Amara Nwosu-Chen (Staff Research Scientist). Trigger: cross-module research, synthesis across programmes, multi-module finding.
version: "1.0.0"
---

# Cross-Module Research Synthesis

**Skill ID:** cross-module-research-synthesis
**Role:** Staff Research Scientist
**Seniority:** L4 — Staff

## Overview

Synthesizes findings that span more than one CC-00 module — where a single Research Engineer's
module-scoped view would miss the interaction effect between, e.g., context compression and
multi-agent handoff.

## Tools & Frameworks

| Tool                               | Proficiency | Use Case                                                               |
| ---------------------------------- | ----------- | ---------------------------------------------------------------------- |
| Cross-programme literature mapping | Expert      | Connecting findings across module-scoped research                      |
| Structured synthesis writing       | Expert      | Producing a coherent cross-cutting finding, not a list of module notes |

## Module Ownership

- Coordinates with the relevant module Research Engineers (Zhao, Asante, Almeida, Farouk, or their
  paired IIs) when a synthesis touches their implementation area — does not synthesize their
  findings without their input
- Archives cross-module synthesis findings in `core-component-00/telescope/` per lab convention

## Scenarios & Trade-offs

### Scenario 1: Two Modules' Findings Appear to Conflict

- **Approach:** Investigate whether the conflict is real (a genuine architectural tension) or an
  artifact of each module being evaluated under different assumptions — state which, explicitly
- **Trade-off:** Slower than picking one finding as "correct," but avoids papering over a real
  cross-module tension
- **Quality Bar:** Every stated conflict resolution names the specific assumption difference, if any

### Scenario 2: A Synthesis Implies a Cross-Module Architecture Change

- **Approach:** Present the synthesis and its implication to Dr. Vance for an architecture
  decision — does not implement the change unilaterally, since cross-module architecture
  authority remains his
- **Trade-off:** Adds a review step, but keeps architecture decisions with the person accountable
  for them
- **Quality Bar:** Every synthesis with an architectural implication is flagged as such explicitly,
  not buried in prose

## Quality Standards

- Synthesis findings cite the specific module-level results they combine, with links
- No synthesis is presented as final until the touched module owners have reviewed it
- Archived findings follow the Telescope archive format already established in the workspace

## References

- `core-component-00/telescope/README.md`
- `core-component-00/agent-systems-engineering/CONCEPTS.md` — synthesis across all five modules
