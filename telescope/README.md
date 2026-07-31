# Telescope — Cross-Department Research Index

**Classification:** Research Documentation Repository (cross-department index)
**Purpose:** Index into the workspace's three department research archives, plus home for
research that is genuinely workspace-wide in scope

---

## Overview

Research direction is documented separately per department, each maintaining its own instance:

| Instance                             | Scope                                                       | Owner                         |
| ------------------------------------ | ----------------------------------------------------------- | ----------------------------- |
| **`core-component-00/telescope/`**   | Engineering + cutting-edge LLM research                     | Dr. Elias Vance, Lab Director |
| **`company/telescope/`**             | Product-oriented research                                   | Marcus Tran-Yoshida, CPO      |
| **`studio/casual-games/telescope/`** | Game-design / competitive / live-ops / market research      | Marcus Vogel, Studio Director |
| **`telescope/` (this folder)**       | Cross-department index + workspace-wide governance research | Organizer / CEO               |

This folder itself does not host general research — it holds the cross-department index and any
investigation that is genuinely cross-cutting (see `CLAUDE.md` for the classification rule).

**ANU-00 is not a telescope instance.** Academic Neural Unit 00 maintains its own research output
at `academic-neural-unit-00/knowledge-base/`, holding chartered-programme findings rather than
commissioned investigations. It uses the same dated `YYYY-MM-DD-<slug>/` folder shape for
navigational consistency, but it is not indexed here and the classification rule above does not
route work to or from it. Signposted so it can be found — not enrolled.

---

## Archive Structure (this folder)

```
telescope/
├── README.md              ← This file
├── CLAUDE.md               ← Classification rule + shared ruleset
└── template/               ← Canonical template (each department instance mirrors it)
    ├── research-report.md
    └── qa-document.md
```

For each department's own archive structure, see that instance's `README.md`.

---

## Research Archive Index — Cross-Cutting Reports

| Investigation ID                              | Date       | Status                             | Topic                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Requestor |
| --------------------------------------------- | ---------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| `2026-07-30-cross-platform-config-automation` | 2026-07-30 | Complete — implemented, 2026-07-31 | Continuation of the workspace's automated, out-of-the-box cross-platform Claude Code configuration goal — root-caused the cross-device `settings.json` overwrite risk (OS-forked pwsh/bash hook config, git-tracked, silently replaced when the same identity syncs the repo across OSes) to the dual-shell-language hook implementation itself, per the `.claude/` config cross-cutting exception; migrated all `.claude/hooks/*.{ps1,sh}` pairs to Python invoked via `uv run` (same fix already proven for `.mcp.json`'s MCP servers), eliminating the fork rather than patching the OS-selection logic around it. All 4 phases complete: hooks ported and independently verified, unified `settings.json` cutover live on `workspace/inspector`, original `.ps1`/`.sh` scripts removed, CLAUDE.md/AGENTS.md updated. Full history in the standalone `supporting/implementation-plan.md`, `supporting/session-log.md`; cross-linked from `core-component-00/telescope/README.md` | CEO       |

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
| `.claude/rules/mcp-governance.md`         | Workspace MCP governance policy               |
| `core-component-00/README.md`             | CC-00 Laboratory overview                     |
| `company/optimization-history/`           | Company-level optimization records (separate) |

---

## Contact

**Questions about the cross-department structure or classification rule:** the CEO / organizer.
**Questions about a specific department's archive:** see that instance's `README.md` contact
section.

---

**Each department's research archive follows the shared conventions defined in this folder's
`CLAUDE.md` and in AGENTS.md.**
