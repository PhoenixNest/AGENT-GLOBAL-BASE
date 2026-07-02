# telescope/ — Cross-Department Research Index

Cross-department pointer for the workspace's three research archives, plus the home for research
that is genuinely workspace-wide in scope. Read this before documenting any investigation, or
before deciding which department's telescope a new investigation belongs in.

---

## What This Is (as of 2026-07-02)

Until 2026-07-02, `telescope/` was a single unified archive owned exclusively by Core Component 00. The CEO directed that each top-level system maintain its own instance instead, so that
research direction is documented separately per department:

| Instance                         | Scope                                                       | Owner                         |
| -------------------------------- | ----------------------------------------------------------- | ----------------------------- |
| `core-component-00/telescope/`   | Engineering + cutting-edge LLM research                     | Dr. Elias Vance, Lab Director |
| `company/telescope/`             | Product-oriented research                                   | Marcus Tran-Yoshida, CPO      |
| `studio/casual-games/telescope/` | Game-design/competitive/live-ops/market research            | Marcus Vogel, Studio Director |
| `telescope/` (this folder)       | Cross-department index + workspace-wide governance research | Organizer / CEO               |

This folder is no longer a general document repository. It holds only:

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
4. This rule was established following the 2026-07-02 decentralization and applies to all future
   investigations; it does not require re-litigating per report.

---

## Directory Structure

```
telescope/
├── README.md              ← Cross-department index — see this for the full picture
├── template/               ← Canonical report template (each department instance mirrors this)
│   ├── research-report.md
│   └── qa-document.md
├── 2026-06-20-mcp-server-assessment/           ← Workspace-wide governance (stays here)
└── 2026-06-29-cross-platform-compatibility-audit/  ← Workspace-wide governance (stays here)
```

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

## Rules (unchanged across all telescope instances)

- Every report lives in a `YYYY-MM-DD-<slug>/` folder containing `research-report.md`.
- Every report is indexed in its instance's `README.md`.
- Use the shared template — do not invent alternative formats.
- This archive is append-oriented. Do not edit published reports except to correct factual errors
  (note the correction with a date in the report's metadata).
- Template skeleton (Metadata, Executive Summary, Investigation Scope, Research Questions,
  Methodology, Findings, Analysis, Recommendations, References, optional Appendices/Research
  Log/Open Questions) is fixed across all instances for citation and ADR-linkage consistency.
  Departments may add optional domain-specific addenda without forking the core structure.

---

## Related Documentation

| Document                                  | Purpose                                             |
| ----------------------------------------- | --------------------------------------------------- |
| `telescope/README.md`                     | Full cross-department index                         |
| `core-component-00/telescope/CLAUDE.md`   | Lab research archive charter                        |
| `company/telescope/CLAUDE.md`             | Company research archive charter                    |
| `studio/casual-games/telescope/CLAUDE.md` | Studio research archive charter                     |
| `.claude/rules/mcp-governance.md`         | Governed by the MCP assessment report retained here |
