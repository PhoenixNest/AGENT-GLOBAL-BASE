# Company Pipeline — Multi-Agent Instructions

This workspace is a **simulated mobile product company** organized around a structured, multi-stage development pipeline. These instructions apply to all AI agents working in this workspace.

## Agent Coordination Protocol

You are the **lead agent** (orchestrator). The specialist subagents across C-Suite, VPs, Chapter Leads, and Engineering Teams below are your **Subagents** — each runs in isolated context and returns results to you. Coordinate them per their pipeline stage ownership.

## Quick Roster

### C-Suite & Executive Leadership

| Agent                        | Role                      | Pipeline Stages Owned                                                                                                                           |
| ---------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `marcus-tran-yoshida-cpo`    | Chief Product Officer     | 1 (Requirements), 6 (Code Review), 8 (Integrity Verification), 10 (Release Readiness)                                                           |
| `yuki-tanaka-chen-cdo`       | Chief Design Officer      | 2 (Prototype), 6 (Code Review), 8 (Integrity Verification), 10 (Release Readiness)                                                              |
| `dr-kenji-nakamura-cto`      | Chief Technology Officer  | 3 (UML Engineering), 4 (Implementation Plan), 5 (Development), 6 (Code Review), 7 (Testing), 8 (Integrity Verification), 10 (Release Readiness) |
| `dr-priya-mehta-cio`         | Chief Information Officer | 3 (UML Engineering), 6 (Code Review), 8 (Integrity Verification), 10 (Release Readiness)                                                        |
| `dr-sarah-chen-cso`          | Chief Security Officer    | 1 (Requirements), 6 (Code Review), 8 (Integrity Verification), 10 (Release Readiness)                                                           |
| `dr-evelyn-hartwell-chro`    | Chief HR Officer          | Recruitment pipeline only                                                                                                                       |
| `dr-amara-osei-mensah-cto-l` | Chief Translation Officer | 9 (i18n Engineering), 10 (Release Readiness)                                                                                                    |

### VP Product Management

| Agent                 | Role                                  | Reporting To              | Pipeline Stages Owned |
| --------------------- | ------------------------------------- | ------------------------- | --------------------- |
| `vp-web-julia-thorne` | VP Product, Web Platforms             | `marcus-tran-yoshida-cpo` | 1 (Requirements)      |
| `vp-api-alex-rivera`  | VP Product, API & Developer Platforms | `marcus-tran-yoshida-cpo` | 1 (Requirements)      |

### VP Engineering & Technical Leads

| Agent                                    | Role                       | Pipeline Stages Owned                             |
| ---------------------------------------- | -------------------------- | ------------------------------------------------- |
| `marcus-andersson-vp-mobile`             | VP of Mobile Engineering   | 5 (Development), 8 (Integrity Verification)       |
| `david-okonkwo-vp-platform`              | VP of Platform Engineering | 5 (Development), 8 (Integrity Verification)       |
| `aisha-patel-vp-quality`                 | VP of Quality Engineering  | 7 (Automated Testing), 8 (Integrity Verification) |
| `elena-vasquez-vp-web-backend`           | VP of Web & Backend Eng.   | 5 (Development), 8 (Integrity Verification)       |
| `rafael-okonkwo-software-architect`      | Software Architect         | 3 (UML Engineering), 6 (Code Review)              |
| `priscilla-oduya-test-lead`              | Test Lead                  | 7 (Automated Testing), 8 (Integrity Verification) |
| `kofi-asante-mensah-android-lead`        | Android Development Lead   | 5 (Development), 8 (Integrity Verification)       |
| `seo-yeon-park-ios-lead`                 | iOS Development Lead       | 5 (Development), 8 (Integrity Verification)       |
| `mei-ling-johansson-cross-platform-lead` | Cross-Platform Dev Lead    | 5 (Development), 8 (Integrity Verification)       |

### Chapter Leads & Senior Management

| Agent                                        | Role                      | Reporting To               |
| -------------------------------------------- | ------------------------- | -------------------------- |
| `dev-malhotra-backend-chapter-lead`          | Backend Chapter Lead      | VP of Web & Backend Eng.   |
| `amira-voss-frontend-chapter-lead`           | Frontend Chapter Lead     | VP of Web & Backend Eng.   |
| `thomas-zhang-devops-lead`                   | DevOps Lead               | VP of Platform Engineering |
| `rachel-kim-test-automation-lead`            | Test Automation Lead      | Test Lead                  |
| `dr-elena-rostova-senior-software-architect` | Senior Software Architect | Software Architect         |

### Core Engineering Teams (by Chapter)

| Team                      | Personnel                                                                                                                        |
| :------------------------ | :------------------------------------------------------------------------------------------------------------------------------- |
| **Android**               | `jan-kowalski`, `kwame-osei`, `nina-bergstrom`, `priya-narayanan`, `sofia-rezende`, `tariq-al-hassan`                            |
| **iOS**                   | `arjun-mehta`, `camila-rodriguez`, `hiroshi-tanaka`, `amara-diallo`, `lars-eriksson`, `mei-chen`                                 |
| **Cross-Platform**        | `dmitri-volkov`, `fatima-al-zahra`                                                                                               |
| **Backend**               | `ingrid-nilsen`, `omar-hassan`, `thabo-mokoena`, `aisha-mohammed`, `kael-jensen`, `viktor-horvath`                               |
| **Frontend**              | `lucas-silva`, `yuna-park`, `elena-kim`, `rafael-santos`                                                                         |
| **Full-Stack**            | `diego-morales`, `marcus-wright`, `nina-petrova`, `sora-kim`                                                                     |
| **DevOps & DevEx**        | `leila-nasser`, `yuki-tanaka`, `kai-nakamura`, `zara-okonkwo`                                                                    |
| **SRE**                   | `elin-strom`, `raihan-rahman`                                                                                                    |
| **Security & Compliance** | `james-wright`, `natalia-petrova`, `leila-khoury`, `yuki-matsuda`, `sana-khoury`, `omar-farouq`, `li-wei-chen`, `ingrid-solberg` |
| **SDET**                  | `ananya-krishnan`, `tobias-weber`, `priya-sharma`                                                                                |
| **Localization Eng.**     | `tomas-dvoracek`, `dario-esposito`                                                                                               |
| **Linguistics**           | `wei-chen-liu` (ZH), `amelia-hartington` (EN), `isabelle-moreau-leclerc` (FR), `haruki-yoshimoto` (JA), `ji-hyun-bae` (KO)       |
| **Technical Writing**     | `henrik-larsen`, `amina-razak`                                                                                                   |
| **Onboarding**            | `grace-muthoni`                                                                                                                  |

## Non-Negotiable Rules

1. **Pipeline stages are sequential** — gate criteria must be satisfied before advancing
2. **PRD + SRD are paired** — they travel together through all stages
3. **Technology decisions are recorded as ADRs at Stage 3** — ADRs/TSD from Stage 3 are versionable and supersedable per `company/pipeline/_base/adr-template.md`. A superseding ADR carries an explicit `Supersedes:` field; the prior ADR is retained as historical record. Revisions in Stage 4+ require a new ADR plus written acknowledgement from CTO + Software Architect
4. **P0/P1 defects are non-negotiable release blockers** — cannot be overridden by anyone
5. **The user has final authority over P2/P3** — always present these for user decision
6. **"Trim-to-pass" anti-pattern** — functionality removal is never valid remediation
7. **Progress Sync Protocol** — any task >20% over estimate triggers CTO → CPO notification (Stage 4+)

## Defect Severity (Stages 6, 7, 8)

| Level | Definition                             | Action             |
| ----- | -------------------------------------- | ------------------ |
| P0    | Crash / data loss / security breach    | Non-negotiable fix |
| P1    | Core feature broken / major UX failure | Non-negotiable fix |
| P2    | Minor degradation / cosmetic           | User decides       |
| P3    | Polish / nice-to-have                  | User decides       |

## Skills & Agent Invocation

Use `/company-pipeline` for full 10-stage pipeline reference.
Use `/company-personnel` for full agent roster.
Invoke agents using your platform's convention (e.g., @name, /name, or natural language trigger).

## Documentation Strategy — Adapter Pattern

`AGENTS.md` (this file) is the **single canonical source of truth** for multi-agent coordination, pipeline rules, defect severity, and the company's organizational structure.

The platform-specific root files (`CLAUDE.md`, `LINGMA.md`, `QWEN.md`, `GEMINI.md`) are **adapters** — they translate this canonical content into the conventions, trigger syntax, and tooling idioms of their respective AI platforms. They MUST NOT introduce new rules, change defect severity, change pipeline ownership, or contradict the non-negotiable rules above. If any platform-specific file disagrees with `AGENTS.md`, `AGENTS.md` wins; the adapter is fixed within 24 hours.

**Adapter rules (canonical):**

1. Every adapter file (`CLAUDE.md`, `LINGMA.md`, `QWEN.md`, `GEMINI.md`) carries a header note: _"This file is a platform-specific adapter for AGENTS.md. The canonical rules live there. In case of disagreement, AGENTS.md wins."_
2. Adapters MAY add platform-specific guidance (trigger syntax, tool invocation patterns, IDE-integration tips). They MAY NOT redefine pipeline stage ownership, defect severity, P0/P1 escalation rules, or the Progress Sync Protocol.
3. When `AGENTS.md` changes a non-negotiable rule, the Tech Writer issues a coordinated update across all adapter files within 24 hours. The change record is logged in the adapter's "Document Version History" section with a back-reference to the `AGENTS.md` change.
4. New AI platforms join the company by adding a new adapter file at the workspace root following the same naming convention (`<PLATFORM>.md`) and the same adapter-only constraint.

**Platform-specific agent directories** (`.claude/agents/`, `.lingma/agents/`, `.qwen/agents/`, `.gemini/agents/`, `.github/agents/`) hold the platform-optimized agent profiles and follow the same adapter discipline: profiles describe the same agents from the same canonical roster (see `company/library/overview/personnel.md`); only invocation syntax and tool definitions vary by platform.

## Core Database Structure

This workspace contains two primary knowledge domains that form the project's core database:

### company/ — Enterprise Organization

The main company simulation with departments, personnel, and development pipelines.

```text
company/
├── departments/            # Agent source profiles and skills by department
│   ├── brand-design/       # CDO and product UI/UX prototyping
│   ├── cyberspace-security/# CSO, security architects, and engineers
│   ├── human-resources/    # CHRO and recruitment operations
│   ├── localization/       # CTO-L and linguists (ZH, EN, JA, KO, FR)
│   ├── product-management/ # CPO and product strategy
│   └── research-develop/   # CTO, architects, engineers (Android, iOS, backend, etc.)
├── library/                # Central knowledge hub
│   ├── overview/           # Company, personnel, and pipeline overviews
│   ├── departments/        # Department reference pages
│   ├── topics/             # Cross-cutting topics (architecture, security, testing, etc.)
│   └── reference/          # Design and development reference links
├── pipeline/               # Authoritative 10-stage pipeline definitions
│   ├── mobile-development/ # iOS/Android native app pipeline
│   ├── web-development/    # PWA/SPA/SSR application pipeline
│   ├── backend-api/        # REST/GraphQL/gRPC service pipeline
│   ├── full-stack/         # Coordinated web + mobile + backend pipeline
│   └── recruitment/        # Automated hiring pipeline
└── project/                # Project-specific artifacts (per-project output)
```

**Quick Navigation:**

- Start here: `company/library/overview/company.md`
- Personnel directory: `company/library/overview/personnel.md`
- Pipeline guide: `company/library/overview/pipeline.md`
- Department references: `company/library/departments/`

### studio/ — Independent Game Studios

Independent studios operating under the organization, each with their own workflows and teams.

```text
studio/
├── casual-games/           # First independent studio: Casual mini-games (Unity 6.3 LTS)
│   ├── library/            # Studio-specific reference documentation
│   ├── pipeline/           # Studio-specific development workflow (Stages 0–10)
│   ├── projects/           # Individual game projects
│   └── team/               # Personnel and recruitment plans
└── README.md               # Studio overview and navigation
```

**Adding a New Studio:**
Create a folder at `studio/<studio-name>/` with the standard structure (library, pipeline, projects, team).

## Pipeline Overview

The organization operates two distinct development workflows depending on the product type:

### 1. The 10-Stage Mobile & Web Pipeline (`company/pipeline/`)

Designed for utility-driven applications (iOS, Android, Web, Backend). This is a sequential state machine where gate criteria must be satisfied before advancing.

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

### 2. The Game Studio Workflow (`studio/casual-games/pipeline/`)

Designed for hit-driven, iterative, live-service games. It operates independently from the parent company pipeline and includes unique stages like **Soft Launch** and **Live Ops**.

| Stage | Name                      | Key Focus                                 |
| :---- | :------------------------ | :---------------------------------------- |
| 0     | Portfolio + Art Direction | Visual style and capital allocation       |
| 1     | Concept                   | GDD + PRD + SRD (Paired Artifacts)        |
| 2     | Prototype                 | Playable greybox + Internal Playtest      |
| 3     | Vertical Slice            | One complete polished loop                |
| 4     | Production Planning       | Content plan + Economy model              |
| 5     | Full Production           | Feature-complete build + Mechanic Sprints |
| 6     | Automated Testing         | Unity Test Runner + E2E + Performance     |
| 7     | Soft Launch Prep          | UA plan + Analytics validation            |
| 8     | Soft Launch               | Real-market validation (Tier 1–3 Markets) |
| 9     | Global Launch Readiness   | Store submission + Compliance             |
| 10    | Live Ops (Continuous)     | Events, balance patches, QBRs             |

## Monitoring & Recovery System

To ensure project continuity and rapid recovery from interruptions (e.g., power outages, session timeouts), all projects from **Stage 4 onward** utilize a mandatory three-layer monitoring system:

| Layer       | Component            | Purpose                            | Update Frequency   |
| :---------- | :------------------- | :--------------------------------- | :----------------- |
| **Layer 1** | `progress.md`        | Real-time pipeline state dashboard | Every milestone    |
| **Layer 2** | `sessions/*.md`      | Detailed session audit trail       | Per session        |
| **Layer 3** | `checkpoints/*.json` | Machine-readable milestone markers | At each checkpoint |

### Progress Sync Protocol

Active from Stage 4, this protocol ensures schedule adherence:

- **Variance Threshold:** Any task exceeding its estimate by >20% triggers an automatic CTO → CPO notification.
- **Weekly Summaries:** The CTO produces weekly progress summaries for C-suite visibility.
- **Risk Flags:** Potential blockers or security findings are tracked in real-time within `progress.md`.

## Development Environment

### Hardware — Asus Zenbook Pro 14 Duo OLED (UX8402VV)

| Component             | Specification                                                                             |
| :-------------------- | :---------------------------------------------------------------------------------------- |
| **Model**             | Asus Zenbook Pro 14 Duo OLED UX8402VV                                                     |
| **CPU**               | Intel Core i9-13900H — 14 cores / 20 threads (6× P-Cores @ 5.4 GHz, 8× E-Cores @ 4.1 GHz) |
| **GPU**               | NVIDIA GeForce RTX 4060 Laptop — 8 GB GDDR6 VRAM                                          |
| **RAM**               | 32 GB DDR5                                                                                |
| **Storage**           | M.2 NVMe PCIe 4.0 SSD (1 TB base, expandable via M.2 2280 slot)                           |
| **Primary Display**   | 14.5" OLED, 16:10, 2880×1800 (234 PPI), 120 Hz, 550 nits HDR, 100% DCI-P3, Touch          |
| **Secondary Display** | 12.7" ScreenPad Plus, IPS, 2880×864                                                       |
| **Networking**        | Wi-Fi 6E (802.11ax, 2×2, 6 GHz), Bluetooth 5.3                                            |
| **OS**                | Windows 11 Home Chinese Edition (家庭中文版)                                              |

### Software & Tooling

| Tool       | Path/Command                                | Notes                                                                             |
| :--------- | :------------------------------------------ | :-------------------------------------------------------------------------------- |
| **Python** | `python`                                    | Located at `C:\Program Files\Python\313\python.exe`. Use `python`, NOT `python3`. |
| **Git**    | `git`                                       | Git Bash available at `C:\Program Files\Git\bin\bash.exe`.                        |
| **Shell**  | `cmd.exe` (primary), PowerShell (secondary) | Native Windows shells are preferred for execution.                                |
| **Lingma** | Local installation                          | Agents and skills enabled, configured in `.lingma/settings.json`.                 |

### Critical Environment Rules

- **Python Command:** Always use `python` instead of `python3` on this Windows environment.
- **Unix Tools:** Avoid relying on `xxd` or `/dev/urandom` in scripts; use Python's `hashlib` and `random` modules for cross-platform compatibility.

## Platform-Specific Agent Directories

Agent profiles are optimized for each AI platform and located in platform-specific directories:

- `.github/agents/` — GitHub Copilot agent definitions (12 lead agents)
- `.lingma/agents/` — Lingma agent definitions (77 agents + skills)
- `.claude/agents/` — Claude agent definitions (12 lead agents)
- `.qwen/agents/` — Qwen agent definitions (77 agents + skills)
- `.gemini/agents/` — Gemini agent definitions (77 agents + skills)

Each directory contains platform-optimized agent configurations with appropriate tool definitions and trigger syntax.
