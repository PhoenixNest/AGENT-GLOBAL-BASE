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
├── pipeline.md                  ← Canonical stage definitions — read before opening a topic
├── template/
│   ├── maintenance-record.md    ← Copy for every new topic's main record
│   └── log-entry.md             ← Copy for every stage/development within a topic
└── <YYYY-MM-DD-slug>/           ← One folder per maintenance topic
    ├── maintenance-record.md    ← Short, always-current summary + status + open items
    └── log/
        ├── 01-<slug>.md         ← Full account of the first development
        ├── 02-<slug>.md         ← Full account of the second development
        └── ...
```

**One folder per maintenance topic.** This matches `core-component-00/telescope/`'s directory
structure exactly (dated folder per topic, per the `research-report.md` + `supporting/` Programme
shape) rather than a single growing file. For the reasoning behind this shape, see `README.md`'s
Format Note.

The split within a topic folder follows Zhao's (`crew/context-engineering/mei-ling-zhao/`)
memory-tier framing: `maintenance-record.md` is the **working-memory** summary — short, always
current, never grows unboundedly — while `log/` holds the **episodic** detail, one numbered file
per development, individually created (never a shared file two people edit at once) and never
edited or deleted after the fact. This is how both of the CEO's concerns get satisfied at once: no
single document becomes unreadably large (each `log/` entry is one development, not the whole
topic's history), and no flat proliferation of near-duplicate top-level files (they're grouped
under one folder per topic, same as `telescope/`).

Stage definitions, gates, severity tagging, the topic-boundary test, and the staleness bound are
all canonical in `pipeline.md` — read it before opening a topic, not just this file.

---

## Creating or Updating a Maintenance Record

**New topic:**

1. Create folder `YYYY-MM-DD-<slug>/` in this directory (e.g.
   `2026-08-13-embedder-service-idle-timeout-tune/`), dated to when the topic first opened.
2. Copy `template/maintenance-record.md` → `<slug>/maintenance-record.md`; fill in the header
   fields including **Severity** (per `pipeline.md`'s severity table).
3. Copy `template/log-entry.md` → `<slug>/log/01-<slug>.md` for the first development (typically
   pipeline stage 1 — Investigation); fill it in and link it from the main record's Pipeline Stage
   Log table.
4. Add an entry to `README.md` (the log index).
5. Run Prettier before finalizing: `prettier --write "<file-path>"`.

**Follow-up on an existing topic** (a later stage, an incident found during execution, a status
change) — per `pipeline.md`'s topic-boundary test, not a new topic:

1. Copy `template/log-entry.md` → `<slug>/log/NN-<slug>.md`, numbered sequentially — never edit
   or delete a prior `log/` entry. If a later entry corrects an earlier claim, say so explicitly
   in the new entry rather than rewriting the old one.
2. Update `<slug>/maintenance-record.md`'s header **Status** field to the current truth (the
   staleness bound in `pipeline.md` applies — this must happen in the same session, not later)
   and add a row to its Pipeline Stage Log table linking the new entry.
3. Run Prettier before finalizing.

A genuinely different topic (different system, different root cause per `pipeline.md`'s
topic-boundary test) gets its own new folder — this rule consolidates the _same_ topic's
lifecycle, it does not merge unrelated maintenance work together.

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
