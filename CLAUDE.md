@AGENTS.md

# CLAUDE.md

Guidance for Claude Code when working in this repository.

> **`AGENTS.md` is imported above** (via the `@AGENTS.md` line) so Claude Code loads it into context
> at session start — Claude Code reads `CLAUDE.md`, not `AGENTS.md`, so the import is what makes the
> authoritative guide actually load. `AGENTS.md` is the complete orientation document (workspace
> identity, the three systems, pipelines, governance, personnel). This file is the **Claude Code
> operating layer** that adds Claude-specific guardrails on top. When the two ever disagree,
> `AGENTS.md` and the canonical `pipeline.md` files win.

---

## 1. Critical guardrails (read first)

- **Never read `GEMINI.md` or `.gemini/**`.** These are a parallel Gemini-agent configuration and
are explicitly denied to Claude Code in `.claude/settings.json`. They are not your context — do
not read, cite, or sync from them. Your equivalents are this file and `AGENTS.md`.
- **Shell is Windows PowerShell.** All terminal commands must be PowerShell-compatible. Avoid
  bash-only syntax (`&&` chaining, `$(...)`, `rm -rf`, heredocs) unless the user has opened WSL or
  Git Bash. Use `;` or separate calls to sequence commands; use `Remove-Item`, `Get-ChildItem`, etc.
- **The User holds absolute authority.** No pipeline rule, agent hierarchy, defect classification, or
  technology decision overrides an explicit user directive (`AGENTS.md` §9 Rule 2).
- **Respect stage gates.** Pipeline stages marked **User Approval ✅** are hard stops. Present the
  deliverable, request sign-off, and wait — never auto-advance (`AGENTS.md` §3.2, §9 Rule 4).
- **Format before finalizing.** Run Prettier on every Markdown file you create or modify:
  `prettier --write "<file-path>"` (`AGENTS.md` §8.7).

---

## 2. What this workspace is

A **Markdown-first, agent-native knowledge base** — an organizational simulation plus an LLM
engineering base. There is **no root build system, no entry point, and no startup script**. The
primary artifacts are documents: agent profiles, skill specs, pipeline definitions, and a layer of
Python reference implementations under `core-component-00/`.

Three architecturally independent but co-resident systems, unified by one governance framework (ASE):

| System          | Path                 | What it is                                                   |
| --------------- | -------------------- | ------------------------------------------------------------ |
| **The Company** | `company/`           | Mobile product company — departments, pipelines, personnel   |
| **The Studio**  | `studio/`            | Casual Games Studio — crew, 11-stage game pipeline, projects |
| **CC-00 Lab**   | `core-component-00/` | Applied LLM research lab — the five-module engineering stack |

---

## 3. Claude Code configuration

The `.claude/` folder is fully provisioned:

| Path                                  | Purpose                                                                                                   |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `.claude/settings.json`               | PowerShell shell, `.gemini` deny rules, hooks, MCP permissions                                            |
| `.claude/rules/*.md`                  | 26 project rules — 7 always-on (no `paths`) + 19 path-scoped (`paths` glob frontmatter)                   |
| `.claude/skills/<domain>/SKILL.md`    | 21 skill routers (20 domains + `activate-org-agent`)                                                      |
| `.claude/skills/<domain>/references/` | Deep sub-skill reference docs                                                                             |
| `.claude/agents/*.md`                 | 4 functional subagents (pipeline-executor, org-activator, cc00-assistant, orchestrator)                   |
| `.claude/hooks/*.ps1`                 | 3 PowerShell hooks: Prettier, ruff lint, pytest on CC-00 changes                                          |
| `.claude/mcp-servers/<name>/`         | 4 MCP server implementations (workspace-knowledge, pipeline-automation, git-worktree-manager, cc00-tools) |
| `.mcp.json`                           | MCP manifest at project root (Claude Code platform requirement — cannot move into `.claude/`)             |

---

## 4. Repository map

```text
AGENTS.md              ← Authoritative full orientation guide (read this)
CLAUDE.md              ← This file (Claude Code operating layer)
GEMINI.md  .gemini/    ← OFF-LIMITS to Claude Code (Gemini-agent config)
.claude/               ← Claude Code configuration (see §3 above)
.mcp.json              ← MCP server manifest (must be at project root)

company/               ← The Company
  library/             ← Central knowledge hub — START HERE for company work
  departments/         ← Agent profiles + skills (canonical source of identities)
  pipeline/            ← _base/ skeleton + per-pipeline deltas (mobile/web/api/full-stack/recruitment)
  recruitment/         ← Hiring cycles + templates
  optimization-history/← APPEND-ONLY archive (never edit past entries)

studio/                ← The Studio
  casual-games/        ← Only active studio: library/, pipeline/, team/crew/, projects/

core-component-00/     ← CC-00 Lab — the ONLY place with runnable code
  agent-systems-engineering/      ← ASE governing meta-module (ADRs, compliance, maturity)
  prompt-engineering/             ← Layer 1 (docs only)
  context-engineering/            ← Layer 2 (docs + Python + pytest)
  harness-engineering/            ← Layer 3 (docs + Python + pytest)
  retrieval-augmented-generation/ ← Layer 4 (docs + Python + requirements.txt)
  multi-agent-engineering/        ← Layer 5 (docs + Python + pytest)
  director/                       ← Lab Director persona (Dr. Elias Vance)

telescope/             ← Research Archive Hub (root-level, owned by CC-00)
```

---

## 5. Working with the Python code (CC-00)

The only executable code lives under `core-component-00/`. Tests are `pytest` suites that import via
`from implementations.<module>` after inserting the module root on `sys.path`, so **run them from the
module folder** (or from `core-component-00/` with the module-path prefix). Run per-module, not all at
once, to avoid duplicate-package import collisions.

```powershell
# From core-component-00/ — run a module's test suite
pytest context-engineering/testing/ -v
pytest harness-engineering/testing/ -v
pytest multi-agent-engineering/testing/ -v

# Lint / type-check / format Python (tools listed in the RAG requirements.txt)
ruff check .
black --check .
mypy implementations/
```

**Modules with tests:** `context-engineering`, `harness-engineering`, `multi-agent-engineering`.
`retrieval-augmented-generation` ships an implementation but no test suite.

**Environment notes (Windows / this machine — `AGENTS.md` §10):**

- RAG dependencies are heavy. Install only when needed:
  `pip install -r core-component-00/retrieval-augmented-generation/requirements.txt`.
  spaCy models are separate: `python -m spacy download en_core_web_sm`.
- GPU work: RTX 4060 (8 GB) supports CUDA — always verify `torch.cuda.is_available()` before
  assuming GPU availability.
- Parallel tests: i9-13900H handles workers well, but keep `pytest -n` ≤ 10 for system headroom.
- `__pycache__/` and `*.py[cod]` are git-ignored.

---

## 6. Conventions

| Item                 | Convention                                                                                     |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| Folders              | `kebab-case` (e.g. `brand-design`, `casual-games`, `puzzle-rush`)                              |
| Agent identity       | `agent/profile.md` (six required YAML frontmatter fields)                                      |
| Skills               | `skills/<skill-name>.md` adjacent to the agent folder — **executable contracts, not hints**    |
| Pipelines            | `pipeline.md` inside the pipeline folder is the canonical truth                                |
| Optimization records | `optimization-history/YYYY-MM-DD-<slug>/` with `optimization-plan.md` + `execution-tracker.md` |
| Research reports     | `telescope/YYYY-MM-DD-<slug>/research-report.md` (template in `telescope/template/`)           |
| Markdown formatting  | Prettier (`prettier --write`) on every created/modified file                                   |

**Document precedence when sources conflict** (`AGENTS.md` §8.2): `pipeline.md` → `agent/profile.md`
→ `library/overview/*.md` → `library/departments/*.md`. Summary docs may lag the canonical source.

---

## 7. Git

- Repo root is local-only: default branch `master`, **no remote configured**. Never force-push.
- Commit finalized workspace additions (profiles, pipelines, skills, docs). Escalate to the user
  before any destructive git operation. `.claude/settings.json` sets `includeCoAuthoredBy: false` and
  empty commit/PR attribution — do not add co-author or attribution trailers.
- **Multi-agent / swarm work uses git worktree isolation** (one isolated worktree + branch per agent):
  - Branch: `agent/<role>/<task>` (or `stage<N>/agent/<role>/<task>`)
  - Commit subject: `agent/<name>: <verb-phrase>` (≤72 chars, imperative, lowercase)
  - Commit body: hyphen-bulleted discrete changes (a bodyless single-line commit is a P2 defect)
  - Full spec: `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`

---

## 8. Activating an organizational agent (persona)

Personas (Type A agents — CDO, CTO, Studio Director, Lab Director, etc.) are **documents**, not
running processes. When the user asks for output "as" a named agent (`AGENTS.md` §2.3):

1. Read that agent's `agent/profile.md` — establish identity, authority scope, and stage ownership.
2. Read every referenced `skills/*.md` — follow their formats/checklists exactly.
3. Adopt their voice and produce output **strictly within their documented authority**.
4. Conform the artifact to the relevant stage spec in `pipeline.md`.

Never impersonate an agent without reading their profile first.

---

## 9. Pipeline guardrails (company development pipelines)

These are non-negotiable and cannot be overridden by any agent (only the User) — see `AGENTS.md` §4.4
and §9:

- **Technology Decision Lock (Stage 3):** ADRs and the TSD are immutable after user approval. Any
  stack change requires a **new ADR and full Stage 3 re-entry** — never an edit at Stage 4/5.
- **P0/P1 defects are final:** A crash, data-loss, security breach (P0) or broken core feature (P1)
  blocks release and cannot be downgraded to advance a gate.
- **Trim-to-Pass is itself a P0:** Removing features, weakening security, or disabling functionality
  to pass a review (Stage 6 / Stage 8) is a blocking defect, not remediation.
- **Stage 6 remediation restarts the full review panel** — it does not resume at defect verification.
- **PRD + SRD travel together** as a unit from Stage 1 onward.

**Mind the distinct pipelines:** the Company development pipeline (see `AGENTS.md` §4.4), the Casual
Games Studio's **separate 11-stage** pipeline (`AGENTS.md` §5.3), and the standalone **9-stage**
recruitment process are different. Do not conflate their stage numbers — defer to the relevant
`pipeline.md`.

---

## 10. Governance: ASE is mandatory

All LLM-powered systems built here are bound by the **Agent Systems Engineering (ASE)** framework — a
meta-layer above the five CC-00 modules, ratified by `ADR-ASE-001`. Build new agent systems, RAG
pipelines, harnesses, and context solutions on **CC-00 patterns**, not ad-hoc inventions
(`AGENTS.md` §7, §9 Rule 9). Governing docs: `core-component-00/agent-systems-engineering/governance/`.

---

## 11. Where to look

| I need…                              | Go to                                             |
| ------------------------------------ | ------------------------------------------------- |
| The full workspace guide             | `AGENTS.md`                                       |
| Company overview / pipeline / people | `company/library/README.md` → `library/overview/` |
| A department's agents + skills       | `company/departments/<dept>/`                     |
| Studio structure + game pipeline     | `studio/casual-games/README.md` → `pipeline/`     |
| The LLM engineering stack            | `core-component-00/README.md`                     |
| ASE governance (ADRs, compliance)    | `core-component-00/agent-systems-engineering/`    |
| Production Python implementations    | `core-component-00/<module>/implementations/`     |
| Document a research investigation    | `telescope/README.md`                             |
