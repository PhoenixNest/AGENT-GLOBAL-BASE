# Telescope — Cross-Department Research Index

**Classification:** Research Documentation Repository (cross-department index)
**Established:** 2026-05-09 · **Decentralized:** 2026-07-02
**Purpose:** Index into the workspace's three department research archives, plus home for
research that is genuinely workspace-wide in scope

---

## Overview

**Telescope** began as a single unified research archive owned exclusively by Core Component 00.
On 2026-07-02, the CEO directed that each top-level system maintain its own instance, so research
direction is documented separately per department instead of all being filed under the Lab:

| Instance                             | Scope                                                       | Owner                         |
| ------------------------------------ | ----------------------------------------------------------- | ----------------------------- |
| **`core-component-00/telescope/`**   | Engineering + cutting-edge LLM research                     | Dr. Elias Vance, Lab Director |
| **`company/telescope/`**             | Product-oriented research                                   | Marcus Tran-Yoshida, CPO      |
| **`studio/casual-games/telescope/`** | Game-design / competitive / live-ops / market research      | Marcus Vogel, Studio Director |
| **`telescope/` (this folder)**       | Cross-department index + workspace-wide governance research | Organizer / CEO               |

This folder itself no longer hosts general research — it holds the cross-department index and
any investigation that is genuinely cross-cutting (see `CLAUDE.md` for the classification rule).

---

## Archive Structure (this folder)

```
telescope/
├── README.md                                        ← This file
├── CLAUDE.md                                          ← Classification rule + shared ruleset
├── template/                                          ← Canonical template (each instance mirrors it)
│   ├── research-report.md
│   └── qa-document.md
├── 2026-06-20-mcp-server-assessment/                  ← Workspace-wide governance report (stays here)
└── 2026-06-29-cross-platform-compatibility-audit/     ← Workspace-wide governance report (stays here)
```

For each department's own archive structure, see that instance's `README.md`.

---

## Research Archive Index — Cross-Cutting Reports (retained at workspace root)

| Investigation ID                                | Date       | Status   | Topic                                                                                               | Requestor |
| ----------------------------------------------- | ---------- | -------- | --------------------------------------------------------------------------------------------------- | --------- |
| `2026-06-20-mcp-server-assessment`              | 2026-06-20 | Complete | Enterprise MCP Architecture & Local RAG Recommendations — governs `.claude/rules/mcp-governance.md` | CEO       |
| `2026-06-29-cross-platform-compatibility-audit` | 2026-06-29 | Complete | Cross-Platform Compatibility Audit of the `.claude/` Configuration Layer — affects every department | CEO       |

These two were judged workspace-wide governance artifacts, not single-department research, and
were kept here rather than migrated. See `CLAUDE.md`'s classification rule for how future
cross-cutting investigations are decided.

---

## Where the Other Four Reports Went

The four remaining reports from the original unified archive were CC-00-native and migrated to
`core-component-00/telescope/` on 2026-07-02:

| Investigation ID                             | New Location                                                              |
| -------------------------------------------- | ------------------------------------------------------------------------- |
| `2026-06-19-cc00-engineering-hooks-research` | `core-component-00/telescope/2026-06-19-cc00-engineering-hooks-research/` |
| `2026-06-25-qdrant-migration-plan`           | `core-component-00/telescope/2026-06-25-qdrant-migration-plan/`           |
| `2026-06-30-llm-engineering-stack-research`  | `core-component-00/telescope/2026-06-30-llm-engineering-stack-research/`  |
| `2026-06-30-prompt-optimizer-audit`          | `core-component-00/telescope/2026-06-30-prompt-optimizer-audit/`          |

See `core-component-00/telescope/README.md` for their index entries.

---

## Access and Permissions

| Role                        | Access Level                                                        |
| --------------------------- | ------------------------------------------------------------------- |
| **All C-suite / Directors** | Full read/write access to their own department's instance           |
| **All Agents**              | Read access to every instance for reference and context             |
| **Organizer / CEO**         | Read/write on this cross-department index and cross-cutting reports |

---

## Related Documentation

| Document                                  | Purpose                                       |
| ----------------------------------------- | --------------------------------------------- |
| `telescope/CLAUDE.md`                     | Classification rule + shared ruleset          |
| `core-component-00/telescope/README.md`   | Lab research archive index                    |
| `company/telescope/README.md`             | Company research archive index                |
| `studio/casual-games/telescope/README.md` | Studio research archive index                 |
| `.claude/rules/mcp-governance.md`         | Governed by the MCP assessment report above   |
| `core-component-00/README.md`             | CC-00 Laboratory overview                     |
| `company/optimization-history/`           | Company-level optimization records (separate) |

---

## Contact

**Questions about the cross-department split or classification rule:** the CEO / organizer.
**Questions about a specific department's archive:** see that instance's `README.md` contact
section.

---

**Telescope is a cross-department index as of 2026-07-02. Each department's research archive
follows the shared conventions defined in this folder's `CLAUDE.md` and in AGENTS.md.**
