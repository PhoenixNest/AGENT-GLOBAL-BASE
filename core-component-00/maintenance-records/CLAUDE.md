# core-component-00/maintenance-records/ — CC-00 Maintenance Log

Maintenance operations log for the Core Component 00 Laboratory. Read this before documenting any
maintenance operation performed on a CC-00 lab server or engineering resource.

---

## What This Is

A record of maintenance operations performed on CC-00 lab infrastructure — the local dev
environment, GPU/CUDA stack, shared dependency footprint (`_shared/`), MCP server processes
(`workspace-knowledge`, `agent-memory`, `embedder-service`), or any other lab-owned resource.
Created at CEO direction to give maintenance work a durable, structured history separate from
`core-component-00/telescope/`, which archives research investigations, not operational upkeep.

---

## Scope

**In scope:** any maintenance operation on a CC-00 lab server, dev environment, dependency stack,
GPU/CUDA configuration, MCP server process, or CI tooling — routine, scheduled, or
incident-response.

**Out of scope:** research investigations and engineering/LLM-research findings
(→ `core-component-00/telescope/`), recruitment and personnel records
(→ `company/recruitment/`), and ASGF governance/compliance audits
(→ `core-component-00/agent-systems-governance-framework/`).

---

## Directory Structure

```
core-component-00/maintenance-records/
├── README.md                    ← Log index
├── CLAUDE.md                    ← This file
├── template/
│   └── maintenance-record.md    ← Copy this for every new maintenance operation
└── <YYYY-MM-DD-slug>.md         ← Individual maintenance records
```

Unlike `telescope/`'s dated-folder-per-investigation shape, a maintenance record is a single file
per operation — it's a point-in-time snapshot, not a document that accumulates supporting files.

---

## Creating a New Maintenance Record

1. Copy `template/maintenance-record.md` → `YYYY-MM-DD-<slug>.md` in this folder (e.g.
   `2026-08-13-embedder-service-idle-timeout-tune.md`).
2. Complete every bracketed placeholder; delete the instructional HTML comments once each section
   is filled in.
3. A follow-up operation on the same resource gets a **new** file, not an edit to a prior one —
   link back to the earlier record instead (same point-in-time-snapshot rule as
   `templates/README.md`'s two cross-system templates).
4. Add an entry to `README.md` (the log index).
5. Run Prettier before finalizing: `prettier --write "<file-path>"` (root `CLAUDE.md` §1).

---

## Who Can Write Here

- Ravi Deshmukh (Infrastructure Engineer) is the primary owner — dev-environment provisioning,
  dependency management, and GPU/CUDA configuration are his documented authority
  (`crew/infrastructure/ravi-deshmukh/agent/profile.md`).
- Module leads and Research Engineer IIs may file a record for maintenance touching their own
  module's infrastructure (e.g. an MCP server they operate).
- Dr. Vance may file or countersign any record; see Ownership below.

---

## Ownership

- **Owner:** Dr. Elias Vance, CC-00 Laboratory Director
- **Operational owner:** Ravi Deshmukh, Infrastructure Engineer
- **Profile:** `core-component-00/crew/director/elias-vance/agent/profile.md`,
  `core-component-00/crew/infrastructure/ravi-deshmukh/agent/profile.md`
- **Authority:** AGENTS.md § 6. Core Component 00
