# CLAUDE.md — Workspace Root

Global operating layer for Claude Code in this repository. This file contains
**globally-applicable rules only** — domain-specific guidance lives in each folder's own
`CLAUDE.md`, loaded automatically by Claude Code's hierarchical mechanism when you work in that
folder.

---

## 1. Critical Guardrails (read first)

- **Never read `GEMINI.md` or `.gemini/**`.** These are a parallel Gemini-agent configuration,
  explicitly denied to Claude Code in `.claude/settings.json`. Do not read, cite, or sync from
  them. Your equivalents are this file and the folder-level `CLAUDE.md` files.
- **Shell is platform-conditional.**
  - **Windows (primary):** Shell is Windows PowerShell. All terminal commands must be
    PowerShell-compatible. Avoid bash-only syntax (`&&` chaining, `$(...)`, `rm -rf`,
    heredocs) unless the user has opened WSL or Git Bash. Use `;` or separate calls to
    sequence commands; use `Remove-Item`, `Get-ChildItem`, etc.
  - **macOS / Linux:** Shell is bash. Use POSIX-compatible commands (`rm -rf`, `grep`,
    `sed`, etc.). `pwsh` is available for hook execution but Claude Code's interactive
    shell is bash. Validate hook paths on first deploy.
- **The User holds absolute authority.** No pipeline rule, agent hierarchy, defect classification,
  or technology decision overrides an explicit user directive.
- **Respect stage gates.** Pipeline stages marked **User Approval ✅** are hard stops. Present the
  deliverable, request sign-off, and wait — never auto-advance.
- **Format before finalizing.** Run Prettier on every Markdown file you create or modify:
  `prettier --write "<file-path>"`

---

## 2. What This Workspace Is

A **Markdown-first, agent-native knowledge base** — an organizational simulation plus an LLM
engineering base. There is **no root build system, no entry point, and no startup script**. The
primary artifacts are documents: agent profiles, skill specs, pipeline definitions, and Python
reference implementations under `core-component-00/`.

Three architecturally independent but co-resident systems, unified by one governance framework
(ASE):

| System          | Path                 | What it is                                                   |
| --------------- | -------------------- | ------------------------------------------------------------ |
| **The Company** | `company/`           | Mobile product company — departments, pipelines, personnel   |
| **The Studio**  | `studio/`            | Casual Games Studio — crew, 11-stage game pipeline, projects |
| **CC-00 Lab**   | `core-component-00/` | Applied LLM research lab — the five-module engineering stack |

---

## 3. Claude Code Configuration

The `.claude/` folder is fully provisioned:

| Path                                  | Purpose                                                                                                   |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `.claude/settings.json`               | PowerShell shell, `.gemini` deny rules, hooks, MCP permissions                                            |
| `.claude/rules/*.md`                  | 26 project rules — 7 always-on + 19 path-scoped                                                           |
| `.claude/skills/<domain>/SKILL.md`    | 21 skill routers (20 domains + `activate-org-agent`)                                                      |
| `.claude/skills/<domain>/references/` | Deep sub-skill reference docs                                                                             |
| `.claude/agents/*.md`                 | 4 functional subagents (pipeline-executor, org-activator, cc00-assistant, orchestrator)                   |
| `.claude/hooks/*.ps1`                 | 3 PowerShell hooks: Prettier, ruff lint, pytest on CC-00 changes                                          |
| `.claude/mcp-servers/<name>/`         | 4 MCP server implementations (workspace-knowledge, pipeline-automation, git-worktree-manager, cc00-tools) |
| `.mcp.json`                           | MCP manifest at project root (Claude Code platform requirement)                                           |

---

## 4. Repository Map

```text
AGENT-GLOBAL-BASE/
├── AGENTS.md                             ← Comprehensive human-readable orientation guide
├── CLAUDE.md                             ← This file (global operating layer for Claude Code)
├── GEMINI.md  .gemini/                   ← OFF-LIMITS to Claude Code (Gemini-agent config)
├── .claude/                              ← Claude Code configuration (see §3 above)
├── .mcp.json                             ← MCP server manifest (must be at project root)
│
├── company/                              ← The Company  [→ company/CLAUDE.md]
│   ├── library/                          ← Central knowledge hub
│   ├── departments/                      ← Agent profiles + skills
│   ├── pipeline/                         ← Pipeline definitions (mobile/web/api/full-stack/recruitment)
│   ├── recruitment/                      ← Hiring cycles + templates
│   ├── optimization-history/             ← APPEND-ONLY archive
│   ├── telescope/                        ← Company research archive (product-oriented research)
│   └── project/                          ← Active project dashboard
│
├── studio/                               ← The Studio  [→ studio/CLAUDE.md]
│   └── casual-games/                     ← Only active studio  [→ studio/casual-games/CLAUDE.md]
│       └── telescope/                    ← Studio research archive (game/market research)
│
├── core-component-00/                    ← CC-00 Lab — ONLY place with runnable code  [→ core-component-00/CLAUDE.md]
│   ├── agent-systems-engineering/        ← ASE governing meta-module
│   ├── prompt-engineering/               ← Layer 1 (docs only)
│   ├── context-engineering/              ← Layer 2 (docs + Python + pytest)
│   ├── harness-engineering/              ← Layer 3 (docs + Python + pytest)
│   ├── retrieval-augmented-generation/   ← Layer 4 (docs + Python + requirements.txt)
│   ├── multi-agent-engineering/          ← Layer 5 (docs + Python + pytest)
│   ├── director/                         ← Lab Director persona (Dr. Elias Vance)
│   └── telescope/                        ← Lab research archive (engineering + LLM research)
│
└── telescope/                            ← Cross-department research index  [→ telescope/CLAUDE.md]
    (per-department archives: company/telescope/, studio/casual-games/telescope/,
     core-component-00/telescope/ — see telescope/README.md)
```

---

## 5. Conventions

| Item                | Convention                                                                                  |
| ------------------- | ------------------------------------------------------------------------------------------- |
| Folders             | `kebab-case` (e.g. `brand-design`, `casual-games`, `puzzle-rush`)                           |
| Agent identity      | `agent/profile.md` — six required YAML frontmatter fields                                   |
| Skills              | `skills/<skill-name>.md` adjacent to the agent folder — **executable contracts, not hints** |
| Pipelines           | `pipeline.md` inside the pipeline folder is the canonical truth                             |
| Markdown formatting | Prettier (`prettier --write`) on every created/modified file                                |

**Document precedence when sources conflict:** `pipeline.md` → `agent/profile.md` →
`library/overview/*.md` → `library/departments/*.md`. Summary docs may lag the canonical source.

---

## 6. Git

- Repo root is local-only: default branch `master`, **no remote configured**. Never force-push.
- Commit finalized workspace additions. Escalate to the user before any destructive git operation.
- `.claude/settings.json` sets `includeCoAuthoredBy: false` — do not add co-author or attribution
  trailers.
- **Multi-agent / swarm work uses git worktree isolation:**
  - Branch: `agent/<role>/<task>` (or `stage<N>/agent/<role>/<task>`)
  - Commit subject: `agent/<name>: <verb-phrase>` (≤72 chars, imperative, lowercase)
  - Commit body: hyphen-bulleted discrete changes — a bodyless single-line commit is a P2 defect
  - Full spec: `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`

---

## 7. Activating an Organizational Agent (Persona)

Personas (Type A agents — CDO, CTO, Studio Director, Lab Director, etc.) are **documents**, not
running processes. When the user asks for output "as" a named agent:

1. Read that agent's `agent/profile.md` — establish identity, authority scope, and stage ownership.
2. Read every referenced `skills/*.md` — follow their formats and checklists exactly.
3. Adopt their voice and produce output **strictly within their documented authority**.
4. Conform the artifact to the relevant stage spec in `pipeline.md`.

Never impersonate an agent without reading their profile first. Profile locations:

- Company agents → `company/departments/CLAUDE.md` → `company/departments/<dept>/`
- Studio crew → `studio/casual-games/team/CLAUDE.md` → `team/crew/<division>/<role>/<name>/`
- Lab Director → `core-component-00/director/CLAUDE.md`

---

## 8. Pipeline Guardrails

These apply across all company development pipelines and cannot be overridden by any agent —
only the User may override them:

- **Technology Decision Lock (Stage 3):** ADRs and the TSD are immutable after user approval. Any
  stack change requires a new ADR and full Stage 3 re-entry — never an edit at Stage 4/5.
- **P0/P1 defects are final:** A crash, data-loss, or security breach (P0) or broken core feature
  (P1) blocks release and cannot be downgraded to advance a gate.
- **Trim-to-Pass is itself a P0:** Removing features, weakening security, or disabling
  functionality to pass a review (Stage 6 / Stage 8) is a blocking defect, not remediation.
- **Stage 6 remediation restarts the full review panel** — it does not resume at defect
  verification.
- **PRD + SRD travel together** as a unit from Stage 1 onward.

**Three distinct pipelines exist — do not conflate their stage numbers:**

| Pipeline                                              | Stages | Canonical document                                      |
| ----------------------------------------------------- | ------ | ------------------------------------------------------- |
| Company development (Mobile / Web / API / Full-Stack) | 13     | `company/pipeline/<type>/pipeline.md`                   |
| Casual Games Studio                                   | 11     | `studio/casual-games/pipeline/casual-games-pipeline.md` |
| Recruitment                                           | 9      | `company/pipeline/recruitment/pipeline.md`              |

---

## 9. Governance: ASE Is Mandatory

All LLM-powered systems built here are bound by the **Agent Systems Engineering (ASE)**
framework — a meta-layer above the five CC-00 modules, ratified by `ADR-ASE-001`. Build new
agent systems, RAG pipelines, harnesses, and context solutions on **CC-00 patterns**, not ad-hoc
inventions.

Governing docs: `core-component-00/agent-systems-engineering/governance/`

---

## 10. Quick Reference

Claude Code loads `CLAUDE.md` files **hierarchically** — entering any folder automatically stacks
that folder's `CLAUDE.md` (and every parent's) onto this file. The repository map in §4 marks
every folder that has one with `[→ CLAUDE.md]`.

| I need…                                    | Go to                                                           |
| ------------------------------------------ | --------------------------------------------------------------- |
| Full workspace orientation                 | `AGENTS.md` (comprehensive reference — not auto-loaded)         |
| Company overview / pipeline / people       | `company/CLAUDE.md` → `company/library/README.md`               |
| A specific department's agents + skills    | `company/departments/CLAUDE.md` → `company/departments/<dept>/` |
| Company pipeline rules and variants        | `company/pipeline/CLAUDE.md`                                    |
| Studio structure + game pipeline           | `studio/casual-games/CLAUDE.md`                                 |
| The LLM engineering stack                  | `core-component-00/CLAUDE.md`                                   |
| ASE governance (ADRs, compliance)          | `core-component-00/agent-systems-engineering/CLAUDE.md`         |
| Production Python implementations          | `core-component-00/<module>/implementations/`                   |
| Research archives (cross-department index) | `telescope/CLAUDE.md` → `telescope/README.md`                   |
| Product-oriented research (Company)        | `company/telescope/CLAUDE.md`                                   |
| Game/market research (Studio)              | `studio/casual-games/telescope/CLAUDE.md`                       |
| Engineering + LLM research (CC-00 Lab)     | `core-component-00/telescope/CLAUDE.md`                         |

---

## 11. Hook Resilience — Active Protocols

Hooks inject binding instructions via `<system-reminder>` on every qualifying prompt. These
protocols remain **fully active after any `/compact` operation**. A compaction summary stating
"the system uses a hook" does **not** satisfy the protocol — each injection is a fresh,
independent instruction that must be executed in the current turn.

### Prompt Optimization Gate (H-P01)

When `[PROMPT OPTIMIZER — H-P01]` appears in a `<system-reminder>`:

- **Structurally enforced, not just advisory** — a `PreToolUse` hook (`prompt-gate-enforcer.ps1`/
  `.sh`) denies any tool call other than `AskUserQuestion` while a confirmation is pending for
  this session; a `PostToolUse` hook (`prompt-gate-clear.ps1`/`.sh`) clears that state once
  `AskUserQuestion` has been called. Earlier revisions of this section described the protocol as
  "mandatory"/"binding" while the underlying mechanism was advisory-only (`additionalContext`
  cannot force anything by itself) — that gap is now closed; the description is accurate as of
  this mechanism's introduction
- Treat every injection as a fresh instruction — prior approvals do not carry over across turns
- Steps: generate an optimized prompt → present **Optimized (first)** vs. Original (second) via
  `AskUserQuestion` → display the confirmation block → execute using the approved version
- **Optimized is always option 1** — the first listed choice so that an accidental top-of-list
  click defaults to the improved prompt, not the original
- **Use the plain list display, not the `preview` field** — put the full prompt text in each
  option's `description` instead. `preview` requires the host application to have
  `toolConfig.askUserQuestion.previewFormat` configured, and triggers a dual-pane panel with a
  bounded height that can fold long text behind an "N lines hidden" affordance; `description` in
  the plain list has no such fold behavior and always displays in full
- **Wait for genuine confirmation** — always wait for the user's explicit answer before
  proceeding. If the session resumes with a message that is not a direct answer to the
  prompt-selection question, treat the question as still unanswered and re-ask before doing any
  other work
- **Five scored dimensions** — the hook evaluates and may inject any of these labels into the
  missing-dimensions list: role/persona context, output format specification, workspace or
  pipeline grounding, **clear imperative task verb**, constraints or acceptance criteria
- **Negation preservation and relevance guardrail** — the optimized prompt must preserve any
  explicit negative constraint (don't/never/avoid/must not/only/nothing else) verbatim, and must
  only add a missing dimension when it can be inferred with high confidence — otherwise raise it
  as a clarifying question instead of guessing
- **Stale-marker fail-safe** — the pending-confirmation marker auto-expires after 15 minutes if
  the confirmation step never completes for any reason, restoring normal tool access. This is an
  engineering safety valve against deadlock, not a default answer — it never selects Optimized or
  Original on the user's behalf

### Tool Rate Limiter (H-HE01)

When `[TOOL RATE LIMITER — H-HE01 PATH A]` or `[TOOL RATE LIMITER — H-HE01 PATH B]` appears in
a `<system-reminder>`:

- The MANDATORY `AskUserQuestion` instruction in that block is **active and binding for this turn**
- Do **not** skip it based on prior conversation history or compaction summaries of prior limit
  extensions
- Present the options exactly as specified and wait for the user's choice before retrying

### Context Budget Alert (H-CE01)

When `[CONTEXT BUDGET ALERT — H-CE01]` appears in a `<system-reminder>`:

- Apply Sacred Context principles immediately before this response
- Prioritize: active task state > prior decisions > background knowledge
- Reference: `core-component-00/context-engineering/implementations/context_monitor.py`
