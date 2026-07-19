# telescope/ — Cross-Department Research Index

Cross-department pointer for the workspace's three department research archives, plus the home
for research that is genuinely workspace-wide in scope. Read this before documenting any
investigation, or before deciding which department's telescope a new investigation belongs in.

---

## What This Is

Research direction is documented separately per department, each with its own dedicated archive:

| Instance                         | Scope                                                       | Owner                         |
| -------------------------------- | ----------------------------------------------------------- | ----------------------------- |
| `core-component-00/telescope/`   | Engineering + cutting-edge LLM research                     | Dr. Elias Vance, Lab Director |
| `company/telescope/`             | Product-oriented research                                   | Marcus Tran-Yoshida, CPO      |
| `studio/casual-games/telescope/` | Game-design / competitive / live-ops / market research      | Marcus Vogel, Studio Director |
| `telescope/` (this folder)       | Cross-department index + workspace-wide governance research | Organizer / CEO               |

This folder is not a general document repository. It holds only:

1. This index/pointer documentation
2. Research that is genuinely cross-cutting — see the classification rule below
3. The canonical `template/` (each department instance also keeps its own copy)

---

## Classification Rule — Where Does a New Investigation Go?

Applied at the time a research investigation is commissioned:

1. **Default:** file it under the requesting or most-affected department's instance.
2. **Cross-cutting exception:** if the investigation's findings affect workspace-wide governance
   or shared configuration used by every department (e.g. `.claude/` config, a workspace-wide
   rule like `mcp-governance.md`, or cross-cutting infrastructure no single department owns),
   it stays here at the workspace root instead.
3. When a cross-cutting report is filed here, cross-link it from any department instance's index
   it materially concerns, so it isn't siloed from departments that rely on its findings.

---

## Directory Structure

```
telescope/
├── README.md              ← Cross-department index — see this for the full picture
└── template/               ← Canonical report template (each department instance mirrors this)
    ├── research-report.md
    └── qa-document.md
```

A cross-cutting investigation gets its own `YYYY-MM-DD-<slug>/` folder under this root per the
rule above.

---

## Creating a New Research Report Here

Only create a report directly in this folder if it meets the cross-cutting exception above.
Otherwise, go to the relevant department's `telescope/` instance and follow its `CLAUDE.md`.

1. Create a new folder: `YYYY-MM-DD-<slug>/`
2. Copy the template: `template/research-report.md` → `YYYY-MM-DD-<slug>/research-report.md`
3. Complete the report in the new folder
4. Add an entry to `README.md` (the cross-department index) and cross-link from any department
   index it concerns

---

## Telescope Conventions

These rules apply to **every** telescope instance — root and all three departments.

### Report Shape — two canonical forms

- **Simple** — a single `research-report.md` (+ optional `qa-document.md`) at the investigation
  folder root. Nothing else. Use this for any self-contained investigation.
- **Programme** — a top-level `research-report.md` (required; the consolidated synthesis) and
  optional `qa-document.md`, plus exactly **one** `supporting/` folder holding everything
  ancillary: diagrams, deployment/migration plans, sub-investigation reports, implementation
  plans. No other subfolder name is permitted at the investigation root. A sub-investigation's
  own report still lives at `supporting/<sub-slug>/research-report.md`, and stays fully
  template-conformant. No inventing new folder names per report.

### Status Lifecycle — four states

`In Progress` / `Complete` / `Superseded` / `Abandoned`. An investigation's Status must be
updated in both its own `research-report.md` metadata table **and** its instance `README.md`
index entry in the same commit — the README is the authoritative "what's active" view; do not
rely on opening every folder to find out. Any `In Progress` investigation untouched for 90+ days
must be reviewed by the instance owner (Lab Director / CPO / Studio Director-or-delegate) and
reclassified as `Complete`, `Abandoned`, or recommitted with a new note — it may not sit silently
as "active" indefinitely.

**No physical `archive/`/`running/` subfolders.** Status-based physical reorganization forces a
file move on every status change, which fights the append-only rule below and churns git history
without improving retrieval — the README Status column already does this job.

---

## Rules (unchanged across all telescope instances)

- Every report lives in a `YYYY-MM-DD-<slug>/` folder containing `research-report.md`.
- Every report is indexed in its instance's `README.md`.
- Use the shared template — do not invent alternative formats.
- This archive is append-oriented. Do not edit published reports except to correct factual errors
  (note the correction with a date in the report's metadata), and do not delete completed
  research reports without explicit direction from the User.
- Template skeleton (Metadata, Executive Summary, Investigation Scope, Research Questions,
  Methodology, Findings, Analysis, Recommendations, References, optional Appendices/Research
  Log/Open Questions) is fixed across all instances for citation and ADR-linkage consistency.
  Departments may add optional domain-specific addenda without forking the core structure.

---

## Related Documentation

| Document                                  | Purpose                          |
| ----------------------------------------- | -------------------------------- |
| `telescope/README.md`                     | Full cross-department index      |
| `core-component-00/telescope/CLAUDE.md`   | Lab research archive charter     |
| `company/telescope/CLAUDE.md`             | Company research archive charter |
| `studio/casual-games/telescope/CLAUDE.md` | Studio research archive charter  |
| `.claude/rules/mcp-governance.md`         | Workspace MCP governance policy  |
