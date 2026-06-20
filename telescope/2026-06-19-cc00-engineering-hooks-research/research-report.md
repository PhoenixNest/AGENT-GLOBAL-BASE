# Research Report — CC-00 Engineering Domain Hook Suggestions

---

## Metadata

| Field                | Value                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Investigation ID** | `2026-06-19-cc00-engineering-hooks-research`                                                                       |
| **Date Started**     | 2026-06-19                                                                                                         |
| **Date Completed**   | 2026-06-19                                                                                                         |
| **Status**           | Complete                                                                                                           |
| **Investigator**     | Senior Engineering Architect (Claude Code)                                                                         |
| **Laboratory**       | Core Component 00                                                                                                  |
| **Module(s)**        | Context Engineering (L2), Harness Engineering (L3), RAG Engineering (L4), Multi-Agent Engineering (L5), ASE (Meta) |
| **Priority**         | High                                                                                                               |
| **Requestor**        | CEO — following completion of the prompt engineering hook system (commit `031f4f3`)                                |

---

## Executive Summary

Following the delivery of four prompt-engineering hooks (H-P01 through H-P04) in commit `031f4f3`,
the CEO requested an investigation into Claude Code hook opportunities across the remaining CC-00
engineering layers. This report identifies ten new hook candidates spanning Context Engineering
(Layer 2), Harness Engineering (Layer 3), RAG Engineering (Layer 4), Multi-Agent Engineering
(Layer 5), and ASE (Meta), each grounded in existing CC-00 production implementations. All
candidates are scored for implementation effort and enforcement impact, with four designated
high-priority for the next development cycle.

---

## Investigation Scope

### What Was Investigated

This investigation surveyed the five CC-00 engineering layers and the ASE meta-layer to identify
lifecycle events where Claude Code hooks could enforce CC-00 patterns, catch violations, or inject
grounding context. The survey was conducted against the existing production implementations in
`core-component-00/<module>/implementations/` and governance docs in
`core-component-00/agent-systems-engineering/`.

### Why This Investigation Was Needed

The prompt engineering hook system (H-P01–H-P04) demonstrated that Claude Code hooks can
materially improve output quality and enforce governance at the interaction layer. The same
enforcement surface exists for context budgeting, harness safety, RAG attribution, multi-agent
isolation, and ASE compliance — but no hooks currently cover those domains. This investigation
identifies the highest-value candidates before a second implementation cycle begins.

### Prior Art Documented

**Commit `031f4f3` — `feat(hooks): replace legacy hooks with prompt engineering hook system`**

| Hook ID | Script                          | Event                    | Trigger                            | Blocking?                       |
| ------- | ------------------------------- | ------------------------ | ---------------------------------- | ------------------------------- |
| H-P01   | `prompt-optimizer.ps1`          | UserPromptSubmit         | Score < 3/5 on 5 CC-00 dimensions  | No (inject)                     |
| H-P02   | `pipeline-context-injector.ps1` | UserPromptSubmit         | Stage 1–10 keyword detected        | No (inject)                     |
| H-P03   | `prompt-quality-gate.ps1`       | UserPromptSubmit         | ASE governance violation keyword   | Yes (`decision:block`)          |
| H-P04   | `prompt-write-guard.ps1`        | PreToolUse (Edit\|Write) | Write to GEMINI.md or .gemini/\*\* | Yes (`permissionDecision:deny`) |

Three legacy hooks (`lint-on-save.ps1`, `prettier-on-save.ps1`, `test-on-code-change.ps1`) were
also removed in this commit.

### Out of Scope

- Hook implementation code (this report is a suggestions deliverable only)
- Hooks for non-CC-00 tooling (Flutter, Android, iOS, web frameworks)
- PostToolUse and Stop event hooks (removed in `031f4f3`; may be revisited separately)

---

## Research Questions

1. Which CC-00 production patterns map naturally to a Claude Code hook enforcement point?
2. What event type (`UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`) is most appropriate
   for each candidate?
3. Does each candidate block (exit 0 with `decision:block` or `permissionDecision:deny`) or inject
   context (`additionalContext`)?
4. What is the relative implementation effort and enforcement value for each candidate?
5. Which four candidates should be prioritized for the next development cycle?

---

## Methodology

### Approach

1. **Layer-by-layer survey** — Read each CC-00 module's production implementations and governance
   docs to identify invariants that hooks could enforce.
2. **Event mapping** — Matched each invariant to the Claude Code hook event that fires closest to
   the violation point.
3. **Scoring** — Scored each candidate on Effort (S/M/L) and Impact (High/Medium/Low).
4. **Prioritization** — Selected top four candidates based on highest Impact × lowest Effort.

### Tools and Resources

- `core-component-00/` — Five-module engineering stack documentation and implementations
- `core-component-00/agent-systems-engineering/governance/` — ASE compliance rules
- `.claude/hooks/` — Existing H-P01–H-P04 as implementation reference
- `.claude/settings.json` — Confirmed exec-form configuration using `C:/PROGRA~1/PowerShell/7/pwsh.exe`
- Official Claude Code Hooks documentation (`https://code.claude.com/docs/en/hooks`)

---

## Findings

### Finding 1: Context Engineering (Layer 2) — Two High-Value Candidates

**CC-00 Layer 2** (`context-engineering/`) provides the four-slot context window model
(System / Retrieved / Conversation / Working), the Sacred Context principle, token budget
enforcement via `context_monitor.py`, and the three-tier Context Handoff Protocol.

**Candidate H-CE01 — Context Budget Alert** (`UserPromptSubmit`, non-blocking)

Reads `transcript_path` file size as a proxy for session length. When the transcript exceeds a
configurable threshold (e.g., 500 KB), injects `additionalContext` directing Claude to apply
Sacred Context principles and flag context compression readiness. References
`context-engineering/implementations/context_monitor.py`.

**Candidate H-CE02 — Handoff Packet Validator** (`PreToolUse` on `Write`, blocking)

Detects file writes targeting paths matching `*handoff*.md`, `*context-bundle*.json`, or
`*handoff-packet*.md`. Parses the planned content for presence of the three mandatory tiers
(Full / Scoped / Minimal) defined in
`context-engineering/patterns/multi-agent-handoff.md`. Blocks writes missing required fields
with `permissionDecision:deny`.

**Evidence:** The `context_monitor.py` implementation already defines token budget thresholds and
enforcement actions — the hook exposes those checks at the interaction layer without requiring
Python to be invoked mid-session.

**Implications:** H-CE01 is the only mechanism that can proactively warn Claude about context
pressure before a tool call fails or context is silently truncated.

---

### Finding 2: Harness Engineering (Layer 3) — Two High-Value Candidates

**CC-00 Layer 3** (`harness-engineering/`) provides the error boundary (timeout / rate-limit /
validation recovery), circuit breaker patterns, tool call limits via `tool_registry.py`, and
structured output validation.

**Candidate H-HE01 — Tool Rate Limiter** (`PreToolUse` on `Bash|PowerShell`, blocking)

Maintains a per-session counter in a temp file (keyed by `session_id`). On each `PreToolUse`
event, increments and checks against a configurable limit (default: 40 tool calls). When the
limit is reached, returns `permissionDecision:deny` citing `tool_registry.py` call-limit
enforcement. Mirrors the `max_calls` field in `ToolRegistry`.

**Candidate H-HE02 — Python Error Boundary Monitor** (`PostToolUse` on `Bash`, non-blocking)

Reads `tool_output` (string) and scans for Python exception patterns
(`Traceback (most recent call last)`, `Error:`, `Exception:`). When detected, injects
`additionalContext` presenting the three recovery actions from `error_boundary.py`:
retry-with-backoff, fallback-to-safe-default, and graceful-degradation. Avoids silent failure
masking.

**Evidence:** `tool_registry.py` defines `max_calls` limits per tool; `error_boundary.py` defines
three recovery strategies with structured exception hierarchies. Both invariants are currently
unenforced at the hook layer.

**Implications:** H-HE01 prevents runaway tool-call loops (a known risk in complex agentic
sessions). H-HE02 surfaces Python error recovery at the exact moment an error occurs rather than
relying on Claude to notice it.

---

### Finding 3: RAG Engineering (Layer 4) — Two Medium-Value Candidates

**CC-00 Layer 4** (`retrieval-augmented-generation/`) covers retrieval strategies (semantic /
keyword / hybrid), freshness guarantees, source attribution, and chunk quality scoring.

**Candidate H-RAG01 — Knowledge Freshness Flag** (`UserPromptSubmit`, non-blocking)

Detects prompts containing freshness-sensitive language (`latest version`, `current state`,
`as of today`, `most recent`, `up to date`). Injects `additionalContext` requiring Claude to
disclose retrieval date, flag potential knowledge staleness, and cite sources when drawing on
retrieved content.

**Candidate H-RAG02 — RAG Source Attribution Guard** (`PreToolUse` on `Write|Edit`, blocking)

Detects writes to knowledge-claim document types (`.md` files under `telescope/`, `library/`,
or `company/library/`) that contain factual claims (sentences with numbers, percentages,
proper nouns) but no citation markers (`[^`, `— Source:`, `Reference:`). Warns via
`additionalContext` before allowing the write, directing attribution per CC-00 RAG patterns.

**Evidence:** The RAG architecture emphasizes source provenance and freshness guarantees as
first-class design concerns. Neither is currently enforced at the write layer.

---

### Finding 4: Multi-Agent Engineering (Layer 5) — Two High-Value Candidates

**CC-00 Layer 5** (`multi-agent-engineering/`) covers swarm orchestration, git worktree
isolation, the Context Handoff Protocol, agent branch naming, and multi-agent commit format.
`git-worktree-orchestration.md` defines the mandatory branch naming convention
(`agent/<role>/<task>`) and commit format (`agent/<name>: <verb-phrase>` with a body).

**Candidate H-MAE01 — Worktree Branch Naming Guard** (`PreToolUse` on `Bash|PowerShell`, blocking)

Detects `git worktree add` or `git checkout -b` commands and extracts the branch name.
Validates it matches `agent/<role>/<task>` or `stage<N>/agent/<role>/<task>`. Non-conforming
branch names are blocked with `permissionDecision:deny`. References
`core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`.

**Candidate H-MAE02 — Agent Commit Format Guard** (`PreToolUse` on `Bash|PowerShell`, blocking)

Detects `git commit -m` invocations on branches matching `agent/*`. Parses the commit message
and validates: (1) subject matches `agent/<name>: <verb-phrase>`; (2) a body (hyphen-bulleted)
is present. Bodyless single-line agent commits are classified as P2 defects in CLAUDE.md §6.
Blocks non-conforming commits with `permissionDecision:deny`.

**Evidence:** The multi-agent git spec in `git-worktree-orchestration.md` is a mandatory
standard, but nothing currently enforces it at commit time. Branch naming violations are only
caught during integration, which is the most expensive point to remediate.

---

### Finding 5: ASE Meta-Layer — Two High-Value Candidates

**ASE** (`core-component-00/agent-systems-engineering/`) is the governance meta-layer defining
Technology Decision Lock, P0/P1 severity immutability, ADR ratification, and stage gate
protection. H-P03 (prompt-quality-gate) already enforces some ASE rules at prompt entry; these
candidates enforce at the write layer.

**Candidate H-ASE01 — ADR Immutability Guard** (`PreToolUse` on `Edit`, blocking)

Detects edits to files matching `**/adr-*.md` or `**/ADR-*.md`. Reads the file content for
`Status: Accepted` or `Status: Ratified`. If found, blocks the edit with `permissionDecision:deny`
citing Technology Decision Lock (CLAUDE.md §8). New ADRs require a separate file; accepted
ADRs are immutable.

**Candidate H-ASE02 — Pipeline Deliverable Schema Guard** (`PreToolUse` on `Write|Edit`,
non-blocking)

Detects writes to files named `prd.md`, `srd.md`, `tsd.md`, `ids.md`, or `pipeline.md` (any
depth). Checks for the presence of required metadata frontmatter fields per the pipeline spec.
Missing fields are flagged via `additionalContext` before the write proceeds. Enforces
deliverable completeness without hard-blocking (the user may be mid-draft).

---

### Finding 6: Workspace Environment Layer — Two Cycle 3 Candidates + One Config Fix

**CEO audit (2026-06-19)** revealed two gaps not addressed by Cycles 1 or 2: Windows PowerShell
syntax enforcement and line-encoding consistency on git commits. An audit of all 11 deployed hooks
and the workspace git configuration confirmed neither requirement is enforced at the hook layer.

**Gap 1 — Windows PowerShell Syntax Enforcement**

CLAUDE.md §1 mandates: _"Shell is Windows PowerShell. All terminal commands must be
PowerShell-compatible."_ `settings.json` sets `"defaultShell": "powershell"`. However no hook
intercepts shell commands containing bash-only constructs before they execute.

**Candidate H-SYS01 — PowerShell Syntax Guard** (`PreToolUse` on `Bash|PowerShell`, non-blocking)

Detects bash-only constructs in the planned command string — `rm -rf`, bare `grep`/`sed`/`awk`,
`export VAR=val`, `$(subshell)` substitution — and injects `additionalContext` listing the
PowerShell equivalent before the command runs. Non-blocking by design: Git Bash usage inside a
PowerShell context is sometimes intentional, so a hard block would be too aggressive. References
`CLAUDE.md §1` and the workspace `rules/` for the approved command set.

**Gap 2 — Line-Encoding Enforcement on git commits**

Audit findings:

- `.gitattributes` normalises `.md`, `.json`, `.py`, `.html` to `eol=crlf` for the working tree
  (LF stored in repo via `text`). However **`.ps1` files have no explicit rule** — covered only
  by `* text=auto`, which produces inconsistent results across editors and platforms.
- `core.autocrlf=true` and `core.safecrlf=warn` are set globally (user git config), meaning
  git silently converts line endings on checkout but only warns on mismatch — no hook validates
  before staging.
- Git warnings observed during Cycle 1 and 2 commits (`"LF will be replaced by CRLF"`) confirm
  `.ps1` files were being committed without an explicit line-ending rule.

**Config Fix (P0 — no hook needed):** Add `*.ps1 text eol=lf` to `.gitattributes`. This
normalises hook script storage to LF (consistent with how they are authored) without affecting
Windows working-tree checkout behaviour, since PowerShell reads both CRLF and LF correctly.

**Candidate H-GIT01 — Pre-Commit Line Encoding Validator** (`PreToolUse` on `Bash|PowerShell`,
non-blocking)

Detects `git add` or `git commit` commands and runs `git diff --check` inline to surface
whitespace and line-ending warnings before they are committed. Injects `additionalContext` with
the specific file and line if mixed endings are found. Non-blocking: validation warning only,
so the commit can proceed after the operator reviews the flag. References `.gitattributes` and
`rules/git-workflow.md`.

**Evidence:** The missing `.ps1` rule in `.gitattributes` is confirmed by the file contents
(`* text=auto / *.md text eol=crlf / *.json text eol=crlf / *.py text eol=crlf /
*.html text eol=crlf` — no `.ps1` entry). The `core.autocrlf=true` / `core.safecrlf=warn`
settings confirm git is handling conversion silently rather than enforcing it.

**Implications:** Both candidates address workspace-environment concerns that sit above the CC-00
engineering layers — they belong in a new "System / Environment" category (SYS) and "Git
Workflow" category (GIT) in the hook taxonomy.

---

## Analysis

### Interpretation of Findings

The ten candidates divide cleanly into two tiers:

**Tier 1 — Blocking enforcement** (6 candidates): H-CE02, H-HE01, H-MAE01, H-MAE02, H-ASE01,
H-RAG02. These guard invariants that, if violated, cause downstream failures: malformed handoff
packets break multi-agent orchestration; runaway tool calls exhaust budgets; non-standard branch
names break integration scripts; edited accepted ADRs corrupt the architecture record.

**Tier 2 — Context injection** (4 candidates): H-CE01, H-HE02, H-RAG01, H-ASE02. These
surface information at the moment it's most useful without hard-blocking, enabling Claude to
self-correct before a problem occurs.

### CEO-Ready Hook Suggestions — Master Table

| ID      | Name                          | Event            | Matcher          | Blocks? | CC-00 Layer | CC-00 Reference                               | Effort | Impact |
| ------- | ----------------------------- | ---------------- | ---------------- | ------- | ----------- | --------------------------------------------- | ------ | ------ |
| H-CE01  | Context Budget Alert          | UserPromptSubmit | —                | No      | CE (L2)     | `context_monitor.py`                          | S      | High   |
| H-CE02  | Handoff Packet Validator      | PreToolUse       | Write            | Yes     | CE (L2)     | `multi-agent-handoff.md`                      | M      | High   |
| H-HE01  | Tool Rate Limiter             | PreToolUse       | Bash\|PowerShell | Yes     | HE (L3)     | `tool_registry.py` (`max_calls`)              | S      | High   |
| H-HE02  | Python Error Boundary Monitor | PostToolUse      | Bash             | No      | HE (L3)     | `error_boundary.py`                           | S      | Medium |
| H-RAG01 | Knowledge Freshness Flag      | UserPromptSubmit | —                | No      | RAG (L4)    | RAG freshness architecture docs               | S      | Medium |
| H-RAG02 | RAG Source Attribution Guard  | PreToolUse       | Write\|Edit      | No      | RAG (L4)    | RAG source provenance patterns                | M      | Medium |
| H-MAE01 | Worktree Branch Naming Guard  | PreToolUse       | Bash\|PowerShell | Yes     | MAE (L5)    | `git-worktree-orchestration.md`               | S      | High   |
| H-MAE02 | Agent Commit Format Guard     | PreToolUse       | Bash\|PowerShell | Yes     | MAE (L5)    | `git-worktree-orchestration.md`, CLAUDE.md §6 | S      | High   |
| H-ASE01 | ADR Immutability Guard        | PreToolUse       | Edit             | Yes     | ASE (Meta)  | CLAUDE.md §8 (Technology Decision Lock)       | S      | High   |
| H-ASE02 | Pipeline Deliverable Schema   | PreToolUse       | Write\|Edit      | No      | ASE (Meta)  | `company/pipeline/<type>/pipeline.md`         | M      | Medium |
| H-SYS01 | PowerShell Syntax Guard       | PreToolUse       | Bash\|PowerShell | No      | SYS (Env)   | `CLAUDE.md §1`, `rules/git-workflow.md`       | S      | High   |
| H-GIT01 | Pre-Commit Line Encoding Flag | PreToolUse       | Bash\|PowerShell | No      | GIT (Env)   | `.gitattributes`, `rules/git-workflow.md`     | S      | Medium |

---

### Trade-offs Identified

| Decision                                   | Option A                      | Option B                            | Recommendation                         |
| ------------------------------------------ | ----------------------------- | ----------------------------------- | -------------------------------------- |
| H-HE01 counter storage                     | Temp file per session         | In-memory (session_id key)          | Temp file — survives hook restarts     |
| H-MAE02 commit body check                  | Regex on `-m` arg only        | Parse `--message` and HEREDOC forms | Regex + `--message` alias              |
| H-RAG02 blocking vs. injecting             | Block writes missing citation | Inject warning (non-blocking)       | Inject (mid-draft tolerance)           |
| H-ASE01 scope (all ADRs vs. accepted only) | Block all ADR edits           | Block only `Status: Accepted`       | Accepted-only (drafts remain editable) |

### Risks and Limitations

- **H-HE01 counter drift**: If the session_id changes mid-session (edge case), the counter
  resets. Use `transcript_path` as the stable session key if `session_id` is not stable.
- **H-MAE02 HEREDOC detection**: PowerShell `@'...'@` commit messages are harder to parse than
  `-m` strings. Initial implementation may miss heredoc form; add as a follow-up.
- **H-RAG02 false positives**: Aggressive citation detection may flag internal reasoning
  documents. Scope the matcher to `telescope/**` and `**/library/**` only.

---

## Recommendations

### Primary Recommendation

**Implement the four high-effort/high-impact candidates in the next development cycle:**

Priority order (highest leverage first):

1. **H-HE01 — Tool Rate Limiter** (S effort, High impact) — Runaway tool-call loops are the
   most likely failure mode in complex agentic sessions. Implement first.
2. **H-MAE01 — Worktree Branch Naming Guard** (S effort, High impact) — Branch naming
   violations are caught cheapest at creation, not integration.
3. **H-MAE02 — Agent Commit Format Guard** (S effort, High impact) — Bodyless agent commits
   are a P2 defect per CLAUDE.md §6; this is the only automated enforcement.
4. **H-ASE01 — ADR Immutability Guard** (S effort, High impact) — Technology Decision Lock
   violations are the most governance-critical write-layer risk.

### Secondary Recommendations

1. **H-CE01 — Context Budget Alert** (S effort) — Low-risk, high-value for long sessions.
   Implement immediately after the priority four.
2. **H-HE02 — Python Error Boundary Monitor** (S effort) — Re-enables PostToolUse event
   coverage that was removed in `031f4f3`.
3. **H-RAG01 — Knowledge Freshness Flag** (S effort) — Completes the UserPromptSubmit chain
   for research-mode prompts.
4. **H-CE02, H-RAG02, H-ASE02** (M effort) — Implement in a third cycle after the S-effort
   candidates are live and tested.

### Implementation Priority

| Hook                 | Priority | Effort | Impact | Cycle         |
| -------------------- | -------- | ------ | ------ | ------------- |
| H-HE01               | P0       | S      | High   | 2             |
| H-MAE01              | P0       | S      | High   | 2             |
| H-MAE02              | P0       | S      | High   | 2             |
| H-ASE01              | P0       | S      | High   | 2             |
| H-CE01               | P1       | S      | High   | 2             |
| H-HE02               | P1       | S      | Medium | 2             |
| H-RAG01              | P1       | S      | Medium | 2             |
| H-CE02               | P2       | M      | High   | 3             |
| H-RAG02              | P2       | M      | Medium | 3             |
| H-ASE02              | P2       | M      | Medium | 3             |
| `.gitattributes` fix | P0       | XS     | High   | 3 (immediate) |
| H-SYS01              | P1       | S      | High   | 3             |
| H-GIT01              | P1       | S      | Medium | 3             |

### Next Steps

1. ~~**CEO review** — Present master table and priority order for sign-off.~~ ✅ Complete
2. ~~**Cycle 2 implementation** — Implement H-HE01, H-MAE01, H-MAE02, H-ASE01, H-CE01, H-HE02,
   H-RAG01 as a batch.~~ ✅ Complete — all 7 hooks live and tested (2026-06-19)
3. ~~**Update `settings.json`** — Add new hook entries in exec-form.~~ ✅ Complete — 11 hooks
   active across 4 lifecycle events
4. **`.gitattributes` fix** — Add `*.ps1 text eol=lf` entry to close the `.ps1` line-ending gap
   identified in the Cycle 3 audit. P0 — implement before next Cycle 3 hook.
5. **Cycle 3 implementation** — Implement H-CE02, H-RAG02, H-ASE02, H-SYS01, H-GIT01 in
   priority order after CEO sign-off.
6. **ADR** — Draft an Architecture Decision Record for the overall hook governance strategy
   once Cycle 3 is complete.

---

## References

### Internal Documentation

- `core-component-00/context-engineering/implementations/context_monitor.py` — Token budget
  enforcement reference for H-CE01
- `core-component-00/context-engineering/patterns/multi-agent-handoff.md` — Three-tier handoff
  protocol reference for H-CE02
- `core-component-00/harness-engineering/implementations/tool_registry.py` — Tool call limit
  reference for H-HE01
- `core-component-00/harness-engineering/implementations/error_boundary.py` — Recovery strategy
  reference for H-HE02
- `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md` —
  Branch naming and commit format spec for H-MAE01, H-MAE02
- `core-component-00/agent-systems-engineering/governance/` — ASE compliance rules for H-ASE01,
  H-ASE02
- `.claude/hooks/` — H-P01–H-P04 as implementation pattern reference
- `.claude/settings.json` — Current exec-form configuration (`C:/PROGRA~1/PowerShell/7/pwsh.exe`)
- `CLAUDE.md §6` — Git conventions (branch naming, commit format)
- `CLAUDE.md §8` — Pipeline guardrails (Technology Decision Lock, P0/P1, Trim-to-Pass)
- `CLAUDE.md §1` — Windows PowerShell shell requirement; bash-only syntax prohibition (H-SYS01)
- `.claude/rules/git-workflow.md` — Commit format, safety rules, no-force-push (H-GIT01, H-SYS01)
- `.gitattributes` — Line-ending normalisation rules; `.ps1` gap identified in Cycle 3 audit
- `git config core.autocrlf=true / core.safecrlf=warn` — Global line-ending conversion settings

### External Sources

- Claude Code Hooks documentation — event types, exit codes, JSON output format, exec-form spec

### Related Work

- `commit 031f4f3` — Prompt engineering hook system (H-P01–H-P04); this report is the
  direct continuation of that work
- Cycle 2 implementation (2026-06-19) — H-CE01, H-HE01, H-HE02, H-MAE01, H-MAE02, H-ASE01,
  H-RAG01 delivered and tested; `settings.json` updated to 11 hooks across 4 lifecycle events
- CEO hook coverage audit (2026-06-19) — identified H-SYS01 and H-GIT01 gaps and `.gitattributes`
  `.ps1` line-ending deficiency; findings appended in Finding 6 of this report
- H-HE01 interactive-limit enhancement (2026-06-19) — CEO-directed post-implementation change;
  replaced hard-coded 40-call limit with per-session config-file-driven limit (default 150) and
  interactive `AskUserQuestion` flow at the limit boundary; documented in Appendix C of this report

---

## Appendix A: Suggested `settings.json` Hook Entries (Cycle 2)

The following entries extend the existing `hooks` object in `.claude/settings.json`. All use the
established exec-form pattern.

```json
"PreToolUse": [
  {
    "matcher": "Edit|Write|NotebookEdit",
    "hooks": [
      { "type": "command", "command": "C:/PROGRA~1/PowerShell/7/pwsh.exe",
        "args": ["-ExecutionPolicy", "Bypass", "-File", ".claude/hooks/prompt-write-guard.ps1"] },
      { "type": "command", "command": "C:/PROGRA~1/PowerShell/7/pwsh.exe",
        "args": ["-ExecutionPolicy", "Bypass", "-File", ".claude/hooks/ase-adr-immutability-guard.ps1"] }
    ]
  },
  {
    "matcher": "Bash|PowerShell",
    "hooks": [
      { "type": "command", "command": "C:/PROGRA~1/PowerShell/7/pwsh.exe",
        "args": ["-ExecutionPolicy", "Bypass", "-File", ".claude/hooks/harness-tool-rate-limiter.ps1"] },
      { "type": "command", "command": "C:/PROGRA~1/PowerShell/7/pwsh.exe",
        "args": ["-ExecutionPolicy", "Bypass", "-File", ".claude/hooks/mae-branch-naming-guard.ps1"] },
      { "type": "command", "command": "C:/PROGRA~1/PowerShell/7/pwsh.exe",
        "args": ["-ExecutionPolicy", "Bypass", "-File", ".claude/hooks/mae-commit-format-guard.ps1"] }
    ]
  }
],
"PostToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      { "type": "command", "command": "C:/PROGRA~1/PowerShell/7/pwsh.exe",
        "args": ["-ExecutionPolicy", "Bypass", "-File", ".claude/hooks/harness-error-boundary-monitor.ps1"] }
    ]
  }
]
```

---

## Appendix B: Cycle 3 Candidates — `.gitattributes` Fix and Hook Entries

### P0 Config Fix — `.gitattributes`

Add the following line to `.gitattributes` to give `.ps1` files an explicit LF-storage rule:

```
*.ps1 text eol=lf
```

Full updated `.gitattributes` target state:

```gitattributes
* text=auto
*.md   text eol=crlf
*.json text eol=crlf
*.py   text eol=crlf
*.html text eol=crlf
*.ps1  text eol=lf
```

**Rationale:** PowerShell scripts authored with LF endings should be stored as LF. `eol=lf`
means: store LF in repo, leave working-tree copy as-is (PowerShell reads both). The `eol=crlf`
choice for other text files follows the existing repo convention.

### Suggested `settings.json` Additions (Cycle 3 hooks)

Extend the existing `Bash|PowerShell` PreToolUse matcher with two new entries:

```json
{ "type": "command", "command": "C:/PROGRA~1/PowerShell/7/pwsh.exe",
  "args": ["-ExecutionPolicy", "Bypass", "-File", ".claude/hooks/sys-powershell-syntax-guard.ps1"] },
{ "type": "command", "command": "C:/PROGRA~1/PowerShell/7/pwsh.exe",
  "args": ["-ExecutionPolicy", "Bypass", "-File", ".claude/hooks/git-line-encoding-validator.ps1"] }
```

---

## Appendix C: H-HE01 Interactive Limit Enhancement (Post-Implementation)

### Background

After Cycle 2 delivery, the CEO raised a valid concern: the hard-coded 40-call-per-session limit
in H-HE01 is too aggressive for long interactive working sessions. A single complex implementation
sprint (e.g., Cycles 2+3 in this session) consumes 40+ tool calls legitimately.

### Design Decision

Replace the hard block with a two-tier interactive system:

1. **Per-session config file** — `$TEMP/cc00-tool-limit-<session-id>.txt` stores the active limit
   as a plain integer. Absence = default (150). Claude writes to this file to extend or cancel the
   limit at runtime.
2. **At-limit block + `additionalContext`** — when `currentCount > maxCalls`, H-HE01 blocks the
   tool call and injects `additionalContext` with a mandatory instruction to present
   `AskUserQuestion` with three options.

### AskUserQuestion Options at the Limit

| Option | User Label       | Action Claude Takes                                            |
| ------ | ---------------- | -------------------------------------------------------------- |
| A      | Extend by 100    | Write `maxCalls + 100` to the limit config file; retry command |
| B      | Remove limit     | Write `999999` to the limit config file; retry command         |
| C      | End conversation | Summarise progress; do not retry                               |

### Key Architecture Notes

- `AskUserQuestion` is not a `Bash|PowerShell` tool call — H-HE01 does **not** block it at the
  limit. The interactive flow is unblocked by design.
- The `Write` tool is also not matched by H-HE01 — Claude can update the limit config file
  without hitting the rate limiter.
- Default limit raised from **40 → 150** to accommodate realistic long sessions.
- H-HE01 reads the limit file on every call — no session restart needed after an extension.

### Test Results

| Test                     | Scenario                                     | Result                                              |
| ------------------------ | -------------------------------------------- | --------------------------------------------------- |
| Syntax check             | Parse H-HE01 as ScriptBlock                  | PASS                                                |
| Functional — at limit    | Counter 150/150, no limit file (default 150) | PASS — deny + AskUserQuestion instructions injected |
| Functional — extend path | Counter 151/250 (limit file = 250)           | PASS — allowed through (no output)                  |

---

## Appendix D: H-HE01 v2 — Per-Turn Counting + Session Ceiling Architecture

### Background

After the interactive-limit enhancement (v1.2 / Appendix C), the CEO identified a structural
flaw in the session-level accumulation model: a user deep into a long session who starts a fresh,
simple prompt could be blocked immediately because the counter carries baggage from all prior
turns. This is a poor user experience for legitimate multi-turn workflows.

### Design Decision

Replace single session-level counter with a **dual-counter, dual-trigger architecture**:

| Counter         | Scope               | Reset?                         | Default Limit | Config File                        |
| --------------- | ------------------- | ------------------------------ | ------------- | ---------------------------------- |
| Per-turn        | Current prompt only | Yes — on each UserPromptSubmit | 150 calls     | `cc00-tool-limit-turn-<id>.txt`    |
| Session ceiling | Entire chat session | Never                          | 1,000 calls   | `cc00-tool-limit-session-<id>.txt` |

### New File: H-HE01-RESET (`harness-he01-turn-reset.ps1`)

A `UserPromptSubmit` hook fires at the start of every new prompt and:

1. Resets the per-turn counter file to `0`
2. Deletes the per-turn limit file (so any mid-turn extension the user granted is wiped)
3. Does **not** touch the session counter or session ceiling

This ensures per-turn extensions are automatically scoped to a single response cycle.

### Dual AskUserQuestion Trigger Paths

**Path A — Per-turn limit hit** (turn counter > 150):

| Option | User Label             | Action Claude Takes                                      |
| ------ | ---------------------- | -------------------------------------------------------- |
| A      | Extend this turn by 50 | Write `limit + 50` to per-turn limit file; retry command |
| B      | End this response      | Summarise progress; do not retry                         |

Extension lasts only for the current response — deleted by H-HE01-RESET on the next prompt.

**Path B — Session ceiling hit** (session counter > 1,000, only fires if Path A passed):

| Option | User Label             | Action Claude Takes                                        |
| ------ | ---------------------- | ---------------------------------------------------------- |
| A      | Extend session by 500  | Write `ceiling + 500` to session limit file; retry command |
| B      | Remove session ceiling | Write `999999` to session limit file; retry command        |
| C      | End conversation       | Summarise progress; do not retry                           |

### Key Architecture Notes

- The two paths never collide in a single tool call (Path B only checks if Path A passed).
- `AskUserQuestion` and `Write` are not `Bash|PowerShell` — neither path blocks them.
- All four counter and config files are keyed by `session_id`, ensuring per-session isolation.
- The session counter increments on every call regardless of which path fires.

### Changed Files

| File                                          | Change                                                          |
| --------------------------------------------- | --------------------------------------------------------------- |
| `.claude/hooks/harness-tool-rate-limiter.ps1` | Rewritten with dual-counter logic and two AskUserQuestion paths |
| `.claude/hooks/harness-he01-turn-reset.ps1`   | New file — UserPromptSubmit reset hook                          |
| `.claude/settings.json`                       | Added H-HE01-RESET under `UserPromptSubmit` hooks               |

### Test Results

| Scenario                         | Input State                           | Expected                                | Result |
| -------------------------------- | ------------------------------------- | --------------------------------------- | ------ |
| S1: Under both limits            | turn=10, session=50                   | exit 0, empty                           | PASS   |
| S2: Per-turn limit hit (Path A)  | turn=150, session=200                 | deny, PATH A, Extend/End options        | PASS   |
| S3: Session ceiling hit (Path B) | turn=5, session=1000                  | deny, PATH B, Extend/Remove/End options | PASS   |
| S4: Extend-turn retry            | turn=151, limit-turn=200, session=300 | exit 0, empty                           | PASS   |

---

## Version History

| Version | Date       | Author                            | Changes                                                                                                                                                     |
| ------- | ---------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-06-19 | Senior Engineering Architect (CC) | Initial research report — 10 hook candidates across CC-00 L2–L5 and ASE                                                                                     |
| 1.1     | 2026-06-19 | Senior Engineering Architect (CC) | Appended Finding 6 (Cycle 3 gaps: H-SYS01, H-GIT01, `.gitattributes` `.ps1` fix); updated master table, priority table, Next Steps, References, Appendix B  |
| 1.2     | 2026-06-19 | Senior Engineering Architect (CC) | Post-implementation amendment: H-HE01 interactive-limit enhancement (CEO-directed); Appendix C added with design decision, architecture notes, test results |
| 1.3     | 2026-06-20 | Senior Engineering Architect (CC) | H-HE01 v2 upgrade (CEO-directed): per-turn reset via H-HE01-RESET hook, session ceiling at 1,000, dual AskUserQuestion paths; Appendix D added              |

---

**Template Version:** 1.0
**Last Updated:** 2026-06-20
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
