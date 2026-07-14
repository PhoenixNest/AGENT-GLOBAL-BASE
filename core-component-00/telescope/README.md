# CC-00 Telescope — Laboratory Research Archive

**Classification:** Research Documentation Repository
**Owner:** Core Component 00 Laboratory
**Director:** Dr. Elias Vance
**Purpose:** Archive for engineering and cutting-edge LLM research produced by the CC-00 Laboratory

---

## Overview

This is the Laboratory's dedicated research archive, documenting CC-00's engineering/LLM-research
direction separately from the Company's product research (`company/telescope/`) and the Studio's
game/market research (`studio/casual-games/telescope/`). See workspace-root `telescope/README.md`
for the cross-department index.

---

## Archive Structure

```
core-component-00/telescope/
├── README.md                    ← This file
├── template/                    ← Research documentation templates
│   ├── research-report.md
│   └── qa-document.md
└── <YYYY-MM-DD-slug>/           ← Individual research reports (none yet)
```

Naming convention, lifecycle, template usage, append-only policy, versioning, and quality
standards follow the shared conventions — see workspace-root `telescope/CLAUDE.md` for the full
ruleset, including the Simple/Programme report shape and the four-state Status Lifecycle.

---

## Research Archive Index

| Investigation ID                           | Date       | Status                                          | Topic                                                                                                                                                                                                                                | Requestor |
| ------------------------------------------ | ---------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------- |
| `2026-07-10-agent-memory-architecture`     | 2026-07-10 | Approved — implementation authorized 2026-07-12 | Persistent agent memory architecture for the Qdrant-backed knowledge base, benchmarked against Claude/industry memory research, with a human-brain-emulating forgetting strategy                                                     | CEO       |
| `2026-07-13-mcp-embedder-service-redesign` | 2026-07-13 | Proposed — awaiting CEO decision                | Root-cause of the agent-memory embedder-loading stall (traced to the MCP host's subprocess-launch path) and a proposed persistent embedder service shared across CC-00 MCP servers, gated behind a cheaper untested retry experiment | CEO       |

---

## Related Documentation

| Document                                                  | Purpose                                                      |
| --------------------------------------------------------- | ------------------------------------------------------------ |
| `telescope/README.md` (workspace root)                    | Cross-department index and workspace-wide governance reports |
| `core-component-00/README.md`                             | CC-00 Laboratory overview                                    |
| `core-component-00/agent-systems-engineering/CONCEPTS.md` | Theoretical synthesis of all five modules                    |

---

## Contact

**Laboratory Director:** Dr. Elias Vance
**Profile:** `core-component-00/crew/director/elias-vance/agent/profile.md`
**Authority:** AGENTS.md § 6. Core Component 00
