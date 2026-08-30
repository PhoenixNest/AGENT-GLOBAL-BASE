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
├── pipeline.md                  ← Canonical stage definitions
├── template/
│   ├── maintenance-record.md    ← Copy for every new topic's main record
│   └── log-entry.md             ← Copy for every stage/development within a topic
└── <YYYY-MM-DD-slug>/           ← One folder per maintenance topic
    ├── maintenance-record.md    ← Short, always-current summary
    └── log/                     ← Full account of each development, one file per entry
```

Each maintenance topic is a dated **folder**, matching `core-component-00/telescope/`'s shape —
see `CLAUDE.md` for the full authoring rule and `pipeline.md` for the stage definitions that
govern how a topic moves through it.

---

## Format Note (2026-08-13, two same-day revisions)

**Revision 1 — "new file per operation" → "one file per topic, dated sections":** the original
rule was meant to stop a record's history from being silently rewritten in place, but in practice
produced exactly what the CEO flagged the same day it was first used for real: three
near-duplicate files (discovery, execution, an incident found during execution) for what was
genuinely one continuous piece of work. The actual failure mode being guarded against — someone
editing history rather than appending to it — doesn't require a new _file_ to prevent, only a rule
against deleting or rewriting a prior _section_. Revised to one file per topic with dated `##`
sections, following the pattern `core-component-00/telescope/` already used for research
investigations.

**Revision 2 — "one growing file" → "one folder per topic, with a `log/` subfolder":** the CEO's
follow-up feedback was that a single file accumulating every section could itself become
unreadably large over a long-running topic, and that the original three-file split wasn't
inherently unacceptable — the goal is accessibility matching how leading labs actually document
maintenance work, not minimizing file count for its own sake. Dr. Vance consulted the full CC-00
crew and converged on: a short, always-current **summary** file (Zhao's "working-memory" framing)
plus a **`log/` subfolder** of individually-created, numbered entries holding the full
**episodic** detail — matching `telescope/`'s `research-report.md` + `supporting/` Programme
shape exactly, governed by a new `pipeline.md` covering stage gates, severity tagging, an
explicit topic-boundary test, and a staleness bound. `.claude/rules/mcp-governance.md`'s own
history remains the cautionary tale for the opposite failure — a single table cell regrowing into
an unreadable inline changelog — so the target is still the same middle ground `telescope/`
already found, just with the folder-plus-log mechanics needed to hold it at scale.

---

## Creating or Updating a Maintenance Record

**New topic:** create folder `YYYY-MM-DD-<slug>/`, copy `template/maintenance-record.md` into it,
copy `template/log-entry.md` into `<slug>/log/01-<slug>.md` for the first development, add an
entry to the index below, run Prettier.

**Follow-up on an existing topic:** copy `template/log-entry.md` into `<slug>/log/NN-<slug>.md`
(next number, never edit a prior entry), update `<slug>/maintenance-record.md`'s header **Status**
and Pipeline Stage Log table, run Prettier.

Full authoring rules, including what counts as "the same topic" vs. a genuinely new one:
`CLAUDE.md` (this folder) and `pipeline.md` (stage gates, severity, topic-boundary test).

---

## Maintenance Log Index

Add a row here for each new topic (or update the row's Status when a topic gets a new `log/`
entry), newest-opened first.

| Date opened | Record                                                                                                        | System / Resource                                                                                                                                                                                                                                                                                                      | Status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2026-08-13  | `core-component-00/maintenance-records/2026-08-13-mcp-server-powershell-cross-platform/maintenance-record.md` | Root `.mcp.json`, `agent-memory/server.py`, `manage_embedder_service.py` (new, replacing the retired `.ps1`), `register_backup_task.py` (new 2026-08-14), both server READMEs, `.claude/hooks/mcp-config-platform-check.py` (new), `workspace-knowledge/server.py` + `workspace-knowledge/_vendor/proxytypes.py` (new) | **Completed 2026-08-26, two follow-up items open** — `.mcp.json`'s cross-platform launch-path bug re-closed via a durable `SessionStart` self-healing hook plus a Windows venv sync and a vendored `jsonref`/`proxytypes` compatibility shim; CEO's live `/mcp reconnect` confirmed both servers fully healthy, non-degraded. DR-scheduling still unverified on non-Windows. **2026-08-30:** Item #6 (Executed, pending verification) — CEO flagged that the self-healing hook's per-session `.mcp.json` rewrite could be accidentally committed; a generate-once template + gitignore redesign was proposed, CEO-approved, and implemented (`.mcp.json` now gitignored, `.mcp.json.example` is the committed template), self-tested against a simulated fresh clone; **Both closed 2026-08-30**, independently confirmed via the CEO's live `/mcp reconnect`. Item #7 (found during the same check): `workspace-knowledge` had briefly failed `CONNECTION_CLOSED` on an unrelated, pre-existing bug — `server.py` shadowing a working real `proxytypes` package with the `log/12` vendor shim — fixed by making the shim conditional and confirmed reconnected cleanly. Only Item #3 (Linux/macOS DR scheduling) remains open in this topic — see the record for detail |

---

## Related Documentation

| Document                         | Purpose                                                        |
| -------------------------------- | -------------------------------------------------------------- |
| `pipeline.md`                    | Canonical stage definitions, gates, severity tagging           |
| `template/maintenance-record.md` | The main-record template — full field-by-field authoring guide |
| `template/log-entry.md`          | The per-stage log-entry template                               |
| `core-component-00/telescope/`   | Research investigation archive (not operational maintenance)   |
| `core-component-00/README.md`    | CC-00 Laboratory overview                                      |

---

## Contact

**Laboratory Director:** Dr. Elias Vance
**Infrastructure Engineer:** Ravi Deshmukh
**Profile:** `core-component-00/crew/director/elias-vance/agent/profile.md`,
`core-component-00/crew/infrastructure/ravi-deshmukh/agent/profile.md`
**Authority:** AGENTS.md § 6. Core Component 00
