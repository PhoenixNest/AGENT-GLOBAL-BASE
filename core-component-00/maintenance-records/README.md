# CC-00 Maintenance Records — Laboratory Maintenance Log

**Classification:** Operational Maintenance Log
**Owner:** Core Component 00 Laboratory
**Director:** Dr. Elias Vance
**Operational Owner:** Ravi Deshmukh, Infrastructure Engineer
**Purpose:** Record of maintenance operations performed on CC-00 lab servers and engineering
resources

---

## Overview

This folder holds the history of maintenance work performed on CC-00 lab infrastructure — the
local dev environment, GPU/CUDA stack, shared dependency footprint, MCP server processes
(`workspace-knowledge`, `agent-memory`, `embedder-service`), and other lab-owned resources.
Created at CEO direction as a dedicated home for this operational history, separate from
`core-component-00/telescope/` (research investigations) and `company/recruitment/` (personnel).

---

## Directory Structure

```
core-component-00/maintenance-records/
├── README.md                    ← This file
├── CLAUDE.md                    ← Claude Code operating layer for this folder
├── template/
│   └── maintenance-record.md    ← Copy this for every new maintenance operation
└── <YYYY-MM-DD-slug>.md         ← Individual maintenance records
```

Each maintenance record is a single dated file, not a folder — see `CLAUDE.md` for the full
authoring rule (point-in-time snapshot; a follow-up operation gets a new file, not an edit).

---

## Creating a New Maintenance Record

1. Copy `template/maintenance-record.md` → `YYYY-MM-DD-<slug>.md` in this folder.
2. Complete every bracketed placeholder in the template.
3. Add an entry to the Maintenance Log Index below.
4. Run Prettier on the new file before finalizing.

Full authoring rules: `CLAUDE.md` (this folder).

---

## Maintenance Log Index

No maintenance operations have been recorded yet. Add a row here for each new record, newest
first.

| Date | Record | System / Resource | Status |
| ---- | ------ | ----------------- | ------ |
| —    | —      | —                 | —      |

---

## Related Documentation

| Document                         | Purpose                                                      |
| -------------------------------- | ------------------------------------------------------------ |
| `template/maintenance-record.md` | The record template — full field-by-field authoring guide    |
| `core-component-00/telescope/`   | Research investigation archive (not operational maintenance) |
| `core-component-00/README.md`    | CC-00 Laboratory overview                                    |

---

## Contact

**Laboratory Director:** Dr. Elias Vance
**Infrastructure Engineer:** Ravi Deshmukh
**Profile:** `core-component-00/crew/director/elias-vance/agent/profile.md`,
`core-component-00/crew/infrastructure/ravi-deshmukh/agent/profile.md`
**Authority:** AGENTS.md § 6. Core Component 00
