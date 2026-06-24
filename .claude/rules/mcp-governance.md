# MCP Governance — Inclusion Charter

Controls which MCP servers may be registered in `.mcp.json`. All three gates must pass before a
server is added. A server failing any gate must be removed.

---

## The Three-Gate Inclusion Test

Every MCP server must pass all three gates before registration. A single failing gate is a
blocking defect.

### Gate 1 — Capability

> The tool performs computation, subprocess execution, or stateful operation that Claude Code's
> native tools (Read, Edit, Grep, Glob, Bash, Write) cannot replicate with equivalent quality.

**Pass:** The server executes subprocesses, maintains state across calls, or performs computation
that is materially faster or more reliable when done out-of-process.

**Fail:** The server wraps file reads, keyword searches, or Markdown parsing — work that native
tools already handle. A "search_docs" tool backed purely by Python string matching is a Capability
failure when `Grep` exists.

---

### Gate 2 — Governance

> The tool enforces, not bypasses, pipeline guardrails. Any tool that can advance a pipeline
> stage, modify governance records, or skip approval gates is rejected.

**Pass:** The server returns information, raises alerts, or validates against policy — it advises
Claude, it does not act on behalf of Claude against the pipeline.

**Fail:** The server can mark a stage as complete, modify an ADR after lock, or change a
`pipeline.md` approval record. Any tool whose primary action updates governance state is a
Governance failure.

---

### Gate 3 — Completeness

> Every tool in the server produces substantively correct, actionable output for its stated
> purpose. Stub responses, "requires inspection" returns, and hardcoded-threshold heuristics
> presented as analysis do not qualify.

**Pass:** Each `@mcp.tool()` endpoint returns real, query-dependent output that an agent can act
on without further verification of the tool's own correctness.

**Fail:** A tool returns `"analysis complete — review manually"`, a static template, or a score
derived from a hardcoded rule that does not inspect the actual artifact. A tool where every query
returns the same template regardless of input content is a Completeness failure.

---

## Assessment Protocol

Before registering a new server, complete this checklist:

| Check | Question                                                                    | Gate         |
| ----- | --------------------------------------------------------------------------- | ------------ |
| ☐     | Does this server do something native tools genuinely cannot?                | Capability   |
| ☐     | Does every tool produce output that varies meaningfully with input?         | Completeness |
| ☐     | Could any tool write to a pipeline stage, ADR, or approval record?          | Governance   |
| ☐     | Has each tool been tested with a real query against real workspace content? | Completeness |

If any checkbox is ☐ (unchecked) after honest assessment, the server fails. Do not register it.

---

## Registered Servers (Post-Retirement)

| Server                | Gates Passed                                | Notes                                                        |
| --------------------- | ------------------------------------------- | ------------------------------------------------------------ |
| `workspace-knowledge` | Capability ✅ Completeness ✅ Governance ✅ | BM25 search + raw-FS fallback; Phase 2 semantic upgrade live |

**Retired servers:**

| Server                 | Failing Gate                  | Reason                                                                                                                                                                                                          |
| ---------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pipeline-automation`  | Completeness ❌               | `advance_stage` returns template regardless of actual stage state                                                                                                                                               |
| `cc00-tools`           | Completeness ❌               | `check_context_budget` returns hardcoded arithmetic, not model-layer data                                                                                                                                       |
| `git-worktree-manager` | Governance ❌ Completeness ❌ | `merge_branch` and `check_merge_conflicts` run `git checkout` on the main workspace (actor, not advisor); default branch hardcoded to `master`, wrong for workspace; replaced by direct PowerShell git commands |

---

## Adding a New Server

1. Complete the Assessment Protocol above.
2. All four checkboxes must be checked.
3. Add the server to `.mcp.json` only after all gates pass.
4. Document the server in the Registered Servers table above.
5. Reference: `telescope/2026-06-20-mcp-server-assessment/research-report.md` (Appendix C)

---

## Removing a Server

A server must be removed from `.mcp.json` when:

- It fails a gate (immediately, no grace period)
- It duplicates capability now provided by a native tool
- It has been unmaintained for two or more sprints

Removal procedure: delete the server's entry from `.mcp.json`, update the Retired Servers table
above with the reason, commit.

---

**Authority:** CEO → CC-00 Laboratory Director (Dr. Elias Vance)
**Reference:** `telescope/2026-06-20-mcp-server-assessment/research-report.md` Appendix C
**Established:** 2026-06-24
