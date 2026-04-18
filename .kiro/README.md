# .kiro/ Directory Index

This directory contains Kiro IDE/CLI configurations, subagent definitions, skills, and workflow definitions for the mobile product development pipeline.

**Converted from:** `.qwen/` directory structure
**Conversion Date:** April 18, 2026
**Total Subagents:** 77 (role-first naming)
**Total Skills:** 199 (organized in 14 categories)

## Environment

### Hardware — Asus Zenbook Pro 14 Duo OLED (UX8402VV)

| Component             | Specification                                            |
| --------------------- | -------------------------------------------------------- |
| **CPU**               | Intel Core i9-13900H — 14 cores / 20 threads             |
| **GPU**               | NVIDIA GeForce RTX 4060 — 8 GB GDDR6                     |
| **RAM**               | 32 GB DDR5                                               |
| **Storage**           | M.2 NVMe PCIe 4.0 SSD (1 TB)                             |
| **Primary Display**   | 14.5" OLED, 2880×1800, 120 Hz, Touch                     |
| **Secondary Display** | 12.7" ScreenPad Plus, IPS, 2880×864                      |
| **OS**                | Windows 11 Home Chinese Edition (家庭中文版)             |

### Software

| Component    | Value                                                                    |
| ------------ | ------------------------------------------------------------------------ |
| **Python**   | `C:\Program Files\Python\313\python.exe` (use `python`, NOT `python3`)   |
| **Git Bash** | `C:\Program Files\Git\bin\bash.exe`                                      |
| **Shell**    | PowerShell (primary), cmd.exe (secondary)                                |
| **Kiro**     | Local installation with agents and skills enabled                        |

---

## Directory Structure

```
.kiro/
├── README.md                    # This index file
├── agents/                      # Kiro subagent configurations (77 agents)
│   ├── C-Suite (7 files)
│   ├── VP Engineering (4 files)
│   ├── R&D Supervisors (5 files)
│   ├── R&D Leads & Architects (7 files)
│   ├── R&D Engineers (37 files)
│   ├── Security (6 files)
│   ├── HR (3 files)
│   ├── Localization (7 files)
│   └── Brand Design (1 file)
├── pipeline/                    # Pipeline definitions
│   ├── mobile-development/      # 10-stage mobile development workflow
│   ├── web-development/         # 10-stage web application workflow
│   ├── backend-api/             # 10-stage backend API workflow
│   ├── full-stack/              # 10-stage full-stack workflow
│   └── recruitment/             # 10-stage automated recruitment pipeline
├── skills/                      # Kiro skills (14 categories, 199 guidelines)
│   ├── architecture/            # CTO/CIO/Architect skills (21 guidelines)
│   ├── product-management/      # CPO skills (3 guidelines)
│   ├── design/                  # CDO skills (8 guidelines)
│   ├── security/                # CSO/Security skills (25 guidelines)
│   ├── hr-recruiting/           # CHRO/HR skills (9 guidelines)
│   ├── localization/            # CTO-L skills (8 guidelines)
│   ├── android/                 # Android team skills (13 guidelines)
│   ├── ios/                     # iOS team skills (16 guidelines)
│   ├── cross-platform/          # KMP/Flutter skills (6 guidelines)
│   ├── frontend-web/            # Web frontend skills (20 guidelines)
│   ├── backend/                 # Backend skills (21 guidelines)
│   ├── testing-qa/              # SDET/QA skills (21 guidelines)
│   ├── devops/                  # DevOps/SRE skills (21 guidelines)
│   └── shared/                  # Cross-cutting skills (7 guidelines)
├── hooks/                       # Kiro hooks (to be configured)
├── rules/                       # Workspace rules
└── settings/                    # Kiro settings
    └── mcp.json                 # MCP server configurations
```

---

## Subagent Configurations

All 77 company personnel are configured as Kiro subagents using the `invokeSubAgent` tool. Each subagent file contains:

- **YAML frontmatter** with `name`, `description`, `tools`, `model`, and `skills`
- **Full agent profile** with background, strengths, gaps, and operating mode
- **Skills index** linking to skill files
- **Pipeline stages owned** for workflow reference

### Tool Mapping (Qwen → Kiro)

| Qwen Tool            | Kiro Tool |
| -------------------- | --------- |
| `read_file`          | `Read`    |
| `write_file`         | `Write`   |
| `read_many_files`    | `Read`    |
| `run_shell_command`  | `Bash`    |
| `search_files`       | `Glob`    |
| `search_content`     | `Grep`    |
| (auto-added)         | `Edit`    |

### C-Suite Supervisors (7)

| Agent                         | File                            | Pipeline Stages      |
| ----------------------------- | ------------------------------- | -------------------- |
| Chief Technology Officer      | `cto-dr-kenji-nakamura.md`      | 3, 4, 5, 6, 7, 8, 10 |
| Chief Design Officer          | `cdo-yuki-tanaka-chen.md`       | 2, 6, 8, 10          |
| Chief Product Officer         | `cpo-marcus-tran-yoshida.md`    | 1, 6, 8, 10          |
| Chief Information Officer     | `cio-dr-priya-mehta.md`         | 3, 6, 8, 10          |
| Chief Security Officer        | `cso-dr-sarah-chen.md`          | 1, 6, 8, 10          |
| Chief Human Resources Officer | `chro-dr-evelyn-hartwell.md`    | Recruitment only     |
| Chief Translation Officer     | `cto-l-dr-amara-osei-mensah.md` | 9, 10                |

### VP Engineering (4)

| Agent                            | File                              | Pipeline Stages |
| -------------------------------- | --------------------------------- | --------------- |
| Marcus Andersson (VP Mobile)     | `vp-mobile-marcus-andersson.md`   | 5, 8            |
| Elena Vasquez (VP Web & Backend) | `vp-web-backend-elena-vasquez.md` | 5, 8            |
| David Okonkwo (VP Platform)      | `vp-platform-david-okonkwo.md`    | 5, 8            |
| Aisha Patel (VP Quality)         | `vp-quality-aisha-patel.md`       | 7, 8            |

### R&D Team Supervisors (5)

| Agent                           | File                                        | Pipeline Stages |
| ------------------------------- | ------------------------------------------- | --------------- |
| Software Architect              | `software-architect-rafael-okonkwo.md`      | 3, 6, 8         |
| Test Lead                       | `test-lead-priscilla-oduya.md`              | 7, 8            |
| Android Development Lead        | `android-lead-kofi-asante-mensah.md`        | 5, 8            |
| iOS Development Lead            | `ios-lead-seo-yeon-park.md`                 | 5, 8            |
| Cross-Platform Development Lead | `cross-platform-lead-mei-ling-johansson.md` | 5, 8            |

---

## Pipeline Overview

The organization operates a structured 10-stage development workflow:

| Stage | Name                                | Key Output                              |
| :---- | :---------------------------------- | :-------------------------------------- |
| 1     | Requirements → PRD + SRD            | Product + Security Requirements         |
| 2     | PRD → Web Prototype + IDS           | Interactive prototype + design specs    |
| 3     | Prototype → UML Engineering Package | Architecture diagrams + ADRs + TSD      |
| 4     | UML → Coding Implementation Plan    | Implementation plan + Gantt chart       |
| 5     | Plan → Software Development         | Platform codebases                      |
| 6     | Development → Code Review           | Defect Report + sign-off                |
| 7     | Code Review → Automated Testing     | Test suite + results report             |
| 8     | Automated Testing → Integrity Check | Integrity sign-off                      |
| 9     | Integrity → i18n Engineering        | Localized codebase + translation report |
| 10    | i18n → Release Readiness Check      | Release decision                        |

---

## Using Kiro Subagents

### Invocation Syntax

Use the `invokeSubAgent` tool to delegate tasks to specialist subagents:

```typescript
invokeSubAgent({
  name: "cto-dr-kenji-nakamura",
  prompt: "Produce a UML Engineering Package for the user authentication feature",
  explanation: "Delegating Stage 3 architecture work to the CTO",
  contextFiles: [
    { path: "docs/prd.md" },
    { path: "docs/srd.md" }
  ]
})
```

### Agent Selection Guidelines

- **Stage 1 (Requirements):** `cpo-marcus-tran-yoshida` (PRD), `cso-dr-sarah-chen` (SRD)
- **Stage 2 (Prototype):** `cdo-yuki-tanaka-chen`, `prototyper-lena-vasquez`
- **Stage 3 (Architecture):** `cto-dr-kenji-nakamura`, `cio-dr-priya-mehta`, `software-architect-rafael-okonkwo`
- **Stage 4 (Planning):** `cto-dr-kenji-nakamura`
- **Stage 5 (Development):** Platform leads + engineers (Android, iOS, Backend, Frontend, etc.)
- **Stage 6 (Code Review):** `cto-dr-kenji-nakamura` (convener), C-suite panel
- **Stage 7 (Testing):** `test-lead-priscilla-oduya`, SDET team
- **Stage 8 (Integrity):** `cto-dr-kenji-nakamura` (convener), full panel
- **Stage 9 (i18n):** `cto-l-dr-amara-osei-mensah`, linguists, i18n engineers
- **Stage 10 (Release):** `cto-dr-kenji-nakamura` (convener), C-suite panel

---

## Skills System

Skills are organized into 14 functional categories. Each category has a parent `SKILL.md` with a table of sub-guidelines.

### Skill Reference Format

In agent frontmatter, skills are referenced as:

```yaml
skills:
  - company:spec-development
  - company:software-architecture-design
  - company:mobile-technology-strategy
```

### Skill Categories

| Category              | Guidelines | Location                  |
| --------------------- | ---------- | ------------------------- |
| Architecture          | 21         | `skills/architecture/`    |
| Product Management    | 3          | `skills/product-management/` |
| Design                | 8          | `skills/design/`          |
| Security              | 25         | `skills/security/`        |
| HR & Recruiting       | 9          | `skills/hr-recruiting/`   |
| Localization          | 8          | `skills/localization/`    |
| Android               | 13         | `skills/android/`         |
| iOS                   | 16         | `skills/ios/`             |
| Cross-Platform        | 6          | `skills/cross-platform/`  |
| Frontend Web          | 20         | `skills/frontend-web/`    |
| Backend               | 21         | `skills/backend/`         |
| Testing & QA          | 21         | `skills/testing-qa/`      |
| DevOps                | 21         | `skills/devops/`          |
| Shared                | 7          | `skills/shared/`          |

---

## Defect Severity System (Stages 6, 7, 8)

| Level | Definition                             | Action             |
| ----- | -------------------------------------- | ------------------ |
| P0    | Crash / data loss / security breach    | Non-negotiable fix |
| P1    | Core feature broken / major UX failure | Non-negotiable fix |
| P2    | Minor degradation / cosmetic           | User decides       |
| P3    | Polish / nice-to-have                  | User decides       |

---

## Non-Negotiable Rules

1. **Pipeline stages are sequential** — gate criteria must be satisfied before advancing
2. **PRD + SRD are paired** — they travel together through all stages
3. **Technology decisions lock at Stage 3** — ADRs/TSD from Stage 3 are not revisable in Stage 4+
4. **P0/P1 defects are non-negotiable release blockers** — cannot be overridden by anyone
5. **The user has final authority over P2/P3** — always present these for user decision
6. **"Trim-to-pass" anti-pattern** — functionality removal is never valid remediation
7. **Progress Sync Protocol** — any task >20% over estimate triggers CTO → CPO notification (Stage 4+)

---

## Monitoring & Recovery System

From **Stage 4 onward**, all projects utilize a mandatory three-layer monitoring system:

| Layer       | Component            | Purpose                            | Update Frequency   |
| :---------- | :------------------- | :--------------------------------- | :----------------- |
| **Layer 1** | `progress.md`        | Real-time pipeline state dashboard | Every milestone    |
| **Layer 2** | `sessions/*.md`      | Detailed session audit trail       | Per session        |
| **Layer 3** | `checkpoints/*.json` | Machine-readable milestone markers | At each checkpoint |

---

## Conversion Notes

This `.kiro/` directory was automatically converted from `.qwen/` with the following adaptations:

1. **Agent Format:** Converted YAML frontmatter from Qwen tool names to Kiro tool names
2. **Tool Mapping:** Applied tool name translations (see table above)
3. **Skills:** Copied entire skills directory structure unchanged
4. **Pipeline:** Copied all pipeline definitions unchanged
5. **Model:** Set default model to `sonnet` for all agents

### Verification Steps

To verify the conversion:

1. Check agent count: `ls .kiro/agents/*.md | wc -l` (should be 77)
2. Check skills structure: `ls .kiro/skills/*/SKILL.md` (should be 14)
3. Test agent invocation: Use `invokeSubAgent` with any agent name
4. Review agent frontmatter: Ensure tools are in Kiro format (Read, Write, Edit, Bash, Glob, Grep)

---

## Next Steps

1. **Configure Hooks:** Add Kiro-specific hooks in `.kiro/hooks/`
2. **Test Agents:** Invoke a few agents to verify they work correctly
3. **Customize Skills:** Adapt skills if needed for Kiro-specific workflows
4. **MCP Configuration:** Add MCP servers in `.kiro/settings/mcp.json` if needed

---

## Support

For questions about:

- **Pipeline stages:** See `pipeline/mobile-development/pipeline.md`
- **Agent roster:** See this README's subagent tables
- **Skills:** See `skills/*/SKILL.md` for each category
- **Kiro documentation:** Refer to Kiro's built-in help system

**Last Updated:** April 18, 2026
