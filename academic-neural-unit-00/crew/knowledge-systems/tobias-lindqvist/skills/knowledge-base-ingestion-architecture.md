# Skill: Knowledge Base Ingestion Architecture

**Owner:** Tobias Lindqvist, Knowledge Systems Engineer
**Purpose:** Design and operate ANU-00's knowledge-base ingestion, taxonomy, and cross-reference
indexing — independent of Core Component 00's own MCP tooling.

---

## When to Use

Whenever a new research-report entry is filed by any ANU-00 researcher, or when the taxonomy
itself needs revision as the knowledge base grows.

## Process

1. **Taxonomy before tooling.** Never build ingestion automation against a taxonomy that hasn't
   stabilized. If a new research-report entry doesn't fit the current taxonomy cleanly, resolve
   the taxonomy gap first — propose an extension to Dr. Mokoena — before ingesting the entry under
   a forced-fit category.
2. **File under the workspace convention.** Every entry lives at
   `academic-neural-unit-00/knowledge-base/YYYY-MM-DD-<slug>/research-report.md`, matching the
   dated research-archive pattern already used by `telescope/`-style archives elsewhere in the
   workspace, for consistent navigability — not because of any link to those archives themselves.
3. **Cross-reference on ingestion.** When a new entry cites or extends a prior ANU-00 entry, record
   that link bidirectionally at ingestion time, not as a later cleanup pass.
4. **ASE boundary, checked every time a new tool is built.** Any LLM-powered component of this
   ingestion pipeline (e.g., automated tagging, embedding-based search) is bound by the
   workspace-wide ASE framework (`core-component-00/agent-systems-engineering/governance/`) as a
   technical standard — this applies regardless of ANU-00's organizational independence from CC-00.
   Do **not** assume reuse of CC-00's `workspace-knowledge` or `agent-memory` MCP servers; if
   ANU-00 needs equivalent capability, it is built or provisioned independently, subject to the
   same three-gate inclusion test CC-00 applies to its own MCP servers
   (`.claude/rules/mcp-governance.md`) if it is ever registered as an MCP server.
5. **No silent taxonomy drift.** If the taxonomy changes, re-tag existing entries explicitly and
   log the change — never let old and new taxonomy versions coexist silently.

## What This Skill Does Not Cover

- Research question design or evidencing rigor — that belongs to the relevant Research Scientist's
  own skill file.
- ASE ratification itself — Dr. Vance retains that authority workspace-wide; this skill only
  covers compliance with the standard, not authoring or changing it.
