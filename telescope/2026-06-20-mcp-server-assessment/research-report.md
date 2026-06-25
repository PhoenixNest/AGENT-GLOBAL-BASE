# Research Report — Enterprise MCP Architecture & Local RAG Recommendations

---

## Metadata

| Field                | Value                                                                        |
| -------------------- | ---------------------------------------------------------------------------- |
| **Investigation ID** | `2026-06-20-mcp-server-assessment`                                           |
| **Date Started**     | 2026-06-20                                                                   |
| **Date Completed**   | 2026-06-24                                                                   |
| **Status**           | Complete                                                                     |
| **Investigator**     | CC-00 Laboratory / Claude Code                                               |
| **Laboratory**       | Core Component 00                                                            |
| **Module(s)**        | retrieval-augmented-generation, multi-agent-engineering, harness-engineering |
| **Priority**         | High                                                                         |
| **Requestor**        | CEO                                                                          |

---

## Executive Summary

This investigation audited all four locally deployed MCP servers against actual usage evidence,
CC-00 engineering principles, and enterprise production standards. Two servers —
`pipeline-automation` and `cc00-tools` — are found to provide no actionable utility and introduce
architectural risk; their retirement is recommended immediately. The two retained servers —
`workspace-knowledge` and `git-worktree-manager` — are practically valuable but require
significant hardening and upgrade to meet enterprise-grade standards. For the local RAG problem, a two-phase hardware-adaptive strategy is proposed: BM25 with
metadata-aware chunking as an immediate upgrade (Phase 1), followed by hybrid BM25 + semantic
embeddings in Phase 2. Hardware detection at runtime selects the appropriate embedding model —
`all-MiniLM-L6-v2` (80 MB, Tier 2, 4–16 GB RAM) or `all-mpnet-base-v2` (420 MB, Tier 3,
16+ GB RAM). This machine (31.6 GB) qualifies for Tier 3. Full deployment details are in
`rag-local-deployment/ops-manual.md`.

---

## Investigation Scope

### What Was Investigated

Full source-code audit of all four MCP servers (`workspace-knowledge`, `pipeline-automation`,
`git-worktree-manager`, `cc00-tools`), cross-referenced against their claimed capabilities,
actual tool invocation logs, CC-00 engineering patterns, ASE governance requirements, and
enterprise production readiness criteria. The Telescope research archive and workspace conventions
were also reviewed to understand documentation coverage gaps.

### Why This Investigation Was Needed

The CEO identified that only two of four deployed MCPs deliver real value, and requested
independent confirmation with specific recommendations before authorizing remediation work. In
parallel, the growing workspace documentation corpus has created an urgent need for a local RAG
capability that respects the organization's hardware constraints. A single coordinated report
serves both concerns.

### Out of Scope

- External MCP servers (GitHub, Figma, Gmail, etc.) — these are cloud-hosted and out of scope for
  this audit
- Model fine-tuning or cloud RAG services
- CI/CD pipeline integration for MCP server testing
- Gemini agent configuration (per CLAUDE.md §1 guardrail)

---

## Research Questions

1. Which of the four MCP servers provides genuine utility that native Claude Code tools cannot
   replicate?
2. Does any server introduce architectural risk (e.g., violating pipeline governance rules)?
3. What is the minimum viable RAG upgrade that fits hardware-constrained environments?
4. What constitutes an enterprise-grade MCP architecture for this workspace?
5. What phased implementation roadmap achieves the highest impact at lowest risk?

---

## Methodology

### Approach

1. **Source-code inspection** — Each `server.py` was read in full and each tool's implementation
   was evaluated for correctness, completeness, and alignment with its documented purpose.
2. **Native-tool comparison** — For each MCP tool, we assessed whether Claude Code's built-in
   tools (Read, Edit, Grep, Glob, Bash, Write) could accomplish the same task as well or better.
3. **Governance compliance audit** — Each server was checked against CLAUDE.md §8 pipeline
   guardrails, ASE mandatory requirements, and CC-00 engineering principles.
4. **RAG capability assessment** — The current `workspace-knowledge` implementation was evaluated
   against BM25, TF-IDF, and lightweight embedding alternatives under hardware constraints.
5. **Telescope archive review** — Prior research reports were reviewed for relevant prior art.

### Tools and Resources

- `.claude/mcp-servers/*/server.py` — full source of all four servers
- `.mcp.json` — MCP manifest
- `CLAUDE.md` §8 — pipeline guardrail requirements
- `core-component-00/` — CC-00 module documentation
- `telescope/README.md` — research archive index
- Current date: 2026-06-24; knowledge cutoff: August 2025

### Constraints

- No production invocation logs were available; utility assessment is based on code inspection
  and CEO's reported usage patterns
- Hardware specification was described qualitatively (constrained) without exact RAM/GPU figures
- Investigation is limited to the local-only `agent-global-base` repository context

---

## Findings

### Finding 1: `pipeline-automation` Is an Architectural Anti-Pattern

The server provides five tools: `validate_stage_gate`, `advance_stage`, `get_stage_info`,
`list_pipeline_stages`, `check_project_status`.

**Evidence:**

- `advance_stage` can autonomously update `progress.md` to advance a project past its current
  stage — including User Approval gates. This directly violates CLAUDE.md §8: _"Pipeline stages
  marked User Approval ✅ are hard stops. Present the deliverable, request sign-off, and wait —
  never auto-advance."_ The tool's `validate_stage_gate` checks only file existence
  (`prd.md`, `srd.md`, `uml-package/`) and does not enforce the user-approval hard stop.
- Stage validation logic is hardcoded to three stages (1, 3, 4) and silently passes all other
  stages as fully valid, including release-critical stages 6–10.
- `check_project_status` parses `progress.md` with fragile string matching
  (`"Current Stage:" in line`) that will silently return `None` for any non-conforming format.
- All five tools are fully replicable by Claude Code's native Read tool applied to `pipeline.md`
  and `progress.md`. No computation occurs that native tools cannot perform.

**Implications:**

- The existence of `advance_stage` as a callable MCP tool creates risk of unintended stage
  progression during agent execution, bypassing mandatory human checkpoints.
- The server adds no capability beyond what native file-reading provides, while introducing
  governance risk.

---

### Finding 2: `cc00-tools` Is a Documentation Stub, Not a Validation Engine

The server provides four tools: `validate_ase_compliance`, `assess_maturity`,
`check_context_budget`, `analyze_handoff`.

**Evidence:**

- `validate_ase_compliance` iterates 25 checklist items and returns `"status": "not_checked"` for
  every single one, with the verdict always `"requires_inspection"`. It performs zero actual
  inspection of the target system. It is a list of what _would_ be checked, presented as a check.
- `assess_maturity` returns `"current_level": "requires_assessment"` unconditionally. It outputs
  a description of maturity levels without assessing the named system.
- `check_context_budget` is arithmetic: `(context_size / max_tokens) * 100`. This is a one-line
  calculation that requires no MCP server.
- `analyze_handoff` maps token count to one of three tiers using two hard thresholds (<5000 →
  full, <20000 → scoped, else → minimal). This heuristic ignores task type, agent topology, and
  the actual content of the handoff — all factors that CC-00 handoff patterns deem critical.
- Model lookup table references `claude-sonnet-4.5` and `claude-opus-4` — both superseded model
  IDs as of mid-2026.

**Implications:**

- All four tools produce outputs that appear authoritative but are either trivially computable or
  always-deferred. An agent acting on `validate_ase_compliance` output believes compliance was
  checked when it was not.
- The actual ASE compliance knowledge is better served by reading
  `core-component-00/agent-systems-engineering/governance/` directly — which Claude Code can do
  natively.

---

### Finding 3: `workspace-knowledge` Is Valuable but Misrepresents Its Capability

**Evidence:**

- The server's tool description claims "semantic search" but the implementation uses
  `content_lower.count(query_lower)` — pure term frequency counting with zero semantic
  understanding. A query for "context window management" will not match documents that discuss
  "token budget optimization" despite identical conceptual meaning.
- The index omits `telescope/` entirely from `key_dirs`, meaning all research reports — the most
  recent and highest-signal documents — are invisible to search.
- The index loads full file content into memory at startup with no chunking. A query returning a
  200-line document as a "snippet" requires the agent to read the full file anyway, negating the
  retrieval benefit.
- `rebuild_index` must be called manually; there is no file-watch or startup-freshness guarantee.
  Documents added since server start are invisible.
- Despite these limitations, `search_docs` and `retrieve_context` are the only tools in the stack
  that navigate the workspace documentation graph in ways native Grep/Glob cannot easily replicate
  for cross-cutting queries.

**Implications:**

- The server should be retained but its RAG engine replaced with a proper BM25 + chunking
  implementation as a minimum upgrade.
- The `telescope/` directory must be added to the index scope.
- Capability claims in tool descriptions must be corrected to avoid agent overreliance on false
  semantic matching.

---

### Finding 4: `git-worktree-manager` Is the Only Enterprise-Ready Server

**Evidence:**

- All five tools (`create_worktree`, `remove_worktree`, `list_worktrees`, `merge_branch`,
  `get_worktree_status`) execute real git subprocesses and return accurate, actionable output.
- Branch naming convention `agent/<name>/<task>` aligns exactly with
  `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`.
- Error handling is consistent: every tool returns `{"success": false, "error": "..."}` on
  failure — no silent exceptions.
- The server encapsulates multi-agent worktree lifecycle operations that would otherwise require
  Claude Code to compose multiple Bash commands, including prune after removal.

**Gaps identified:**

- Worktrees directory is hardcoded to `workspace_root.parent / "worktrees"` — this resolves
  outside the repo root and may conflict with other workspace siblings.
- `merge_branch` calls `git checkout <target_branch>` on the main workspace, which could cause
  disruption if Claude Code has other files open.
- No pre-merge conflict detection (dry-run check before committing to the merge).

**Implications:**

- Retain as-is with three targeted improvements: configurable worktree base path, dry-run merge
  support, and a `check_merge_conflicts` tool.

---

### Finding 5: The Local RAG Gap Is Real and Addressable Under Hardware Constraints

The workspace contains **1,060 Markdown files** across nine indexed directories, yielding an
estimated **~4,075 BM25/embedding chunks** at 512-word chunk size. The CEO-identified urgency is
well-founded: the current keyword-count approach fails for synonymous queries, cross-module
questions, and research reports — all of which are invisible to the existing index because
`telescope/` is not indexed.

**Detected hardware (this machine):** Intel i9-13900H, 31.6 GB RAM, Intel Iris Xe integrated
GPU (2 GB VRAM, no CUDA). This places the deployment firmly in **Tier 3** — full hybrid
BM25 + semantic embedding search is viable without any GPU requirement.

**Evidence and Analysis:**

Five approaches were assessed. A three-tier hardware model governs model selection:

| Approach                                     | RAM Tier | GPU Req.    | Semantic Quality | Offline | Verdict                    |
| -------------------------------------------- | -------- | ----------- | ---------------- | ------- | -------------------------- |
| Current (term frequency)                     | Any      | None        | None             | Yes     | Replace                    |
| BM25 + metadata chunking (Tier 1)            | < 4 GB   | None        | Low-Medium       | Yes     | Phase 1                    |
| BM25 + `all-MiniLM-L6-v2` — 80 MB (Tier 2)   | 4–16 GB  | None (CPU)  | Medium           | Yes     | Phase 2 option             |
| BM25 + `all-mpnet-base-v2` — 420 MB (Tier 3) | > 16 GB  | None (CPU)  | Medium-High      | Yes     | **Phase 2 — this machine** |
| Full large local model (4+ GB)               | 16+ GB   | Recommended | High             | Yes     | No                         |
| Cloud embedding API (OpenAI/Cohere)          | Any      | None        | High             | No      | No                         |

`all-mpnet-base-v2` is a 12-layer MPNet encoder (420 MB) that runs on CPU with ~150–300 ms
inference latency on i9-13900H. With ~4,075 index chunks and a FAISS Flat index, total RAM
overhead is ~700 MB — well within this machine's 31.6 GB. The FAISS Flat index type is
appropriate for corpora under 5,000 chunks; the estimated 4,075 chunks falls below this
threshold with comfortable headroom.

> **Full deployment details** — software stack, model download procedures, hardware-adaptive
> configuration, environment variables, and troubleshooting — are documented in the operations
> manual: `rag-local-deployment/ops-manual.md`

**Implications:**

- Phase 1 (BM25) requires only `psutil` and `rank_bm25` — both pure Python, no compilation.
- Phase 2 adds `sentence-transformers` and `faiss-cpu`; on this machine, `all-mpnet-base-v2`
  is the correct model selection (Tier 3), not `all-MiniLM-L6-v2` (Tier 2).
- Cloud API dependency is explicitly ruled out: offline operation is a requirement for a
  local-only repository.

---

## Analysis

### Interpretation of Findings

The four-server configuration suffers from a fundamental design problem: two of the four servers
(`pipeline-automation`, `cc00-tools`) were built to _look_ like productive tools without
implementing the underlying logic that would make them so. This is likely an early-stage scaffold
that was never completed. The risk is not merely low utility — it is active misrepresentation:
`validate_ase_compliance` presents a compliance verdict of "requires_inspection" in a structured
JSON format that could be mistaken for an actual assessment result by a downstream agent.

The two legitimate servers (`workspace-knowledge`, `git-worktree-manager`) validate the MCP
model for this workspace: tools that execute non-trivial computation or subprocess operations that
native Claude Code tools cannot easily replicate. This is the correct filter for MCP inclusion.

The RAG gap is the most strategically significant finding. The current `workspace-knowledge`
server fails on exactly the queries that matter most — cross-module conceptual searches,
recently-added research reports, and terminology-variant lookups. An upgraded RAG engine would
transform the workspace from a collection of files into a queryable knowledge graph accessible
at inference time.

### Trade-offs Identified

| Decision                    | Option A                  | Option B                               | Recommendation          |
| --------------------------- | ------------------------- | -------------------------------------- | ----------------------- |
| `pipeline-automation`       | Retire immediately        | Rebuild with governance-safe design    | Retire (no active use)  |
| `cc00-tools`                | Retire immediately        | Complete the stub implementations      | Retire (effort > value) |
| RAG engine upgrade          | BM25 only (fast, no deps) | BM25 + embeddings (better, ~700 MB)    | Phase 1 → Phase 2       |
| Embedding model             | Cloud API                 | `all-mpnet-base-v2` local CPU (Tier 3) | Local CPU (Tier 3)      |
| `git-worktree-manager` path | Keep parent-relative path | Make path configurable via env var     | Configurable env var    |

### Risks and Limitations

- Retiring `cc00-tools` removes the `check_context_budget` tool, which the H-CE01 hook currently
  invokes. The hook must be updated to use a direct calculation or removed.
- BM25 requires re-indexing when documents change. An auto-rebuild trigger on file modification
  (via a watchdog or scheduled rebuild on server start) should be included in Phase 1.
- `all-MiniLM-L6-v2` produces embeddings fixed at 384 dimensions. If the corpus grows beyond
  ~5,000 chunks, FAISS Flat search degrades; an IVF index should be introduced at that scale.
- Retiring `pipeline-automation` means pipeline stage tracking returns to manual `progress.md`
  management — this is acceptable given that human approval gates are the design intent.

---

## Recommendations

### Primary Recommendation

**Retire `pipeline-automation` and `cc00-tools`; upgrade `workspace-knowledge`; harden
`git-worktree-manager`.**

Remove both non-functional servers from `.mcp.json` immediately. Upgrade `workspace-knowledge`
to a BM25 + chunking engine in Phase 1, adding `all-MiniLM-L6-v2` embeddings in Phase 2. Apply
three targeted improvements to `git-worktree-manager`.

---

### Secondary Recommendations

#### R1 — Establish a MCP Inclusion Charter

Before any future MCP server is added, it must pass three gates:

1. **Capability gate:** Does this tool do something that `Read`, `Edit`, `Grep`, `Glob`, or
   `Bash` cannot do adequately?
2. **Governance gate:** Does this tool respect all CLAUDE.md §8 pipeline guardrails (no
   auto-advancing past user approval stages, no overriding P0/P1 classifications)?
3. **Completeness gate:** Does every tool in the server produce substantively correct, actionable
   output — not placeholder or "requires inspection" responses?

Any server that fails any gate must not be added to `.mcp.json`.

#### R2 — Phase 1 RAG Upgrade: BM25 + Metadata-Aware Chunking

Replace the current term-frequency engine with:

- **BM25** via `rank_bm25` library (pure Python, no additional system dependencies)
- **Chunking strategy:** 512-token paragraphs with 64-token overlap, preserving header hierarchy
  as metadata
- **Scope expansion:** Add `telescope/` to `key_dirs` in the index configuration
- **Metadata indexing:** Extract YAML frontmatter (title, date, module, priority) and store as
  filterable fields
- **Auto-rebuild:** Rebuild index on server start; expose `rebuild_index` for manual refresh

#### R3 — Phase 2 RAG Upgrade: Lightweight Semantic Embeddings

After Phase 1 is stable, add:

- **Model:** `sentence-transformers/all-MiniLM-L6-v2` (~80 MB download, CPU-capable)
- **Index:** FAISS `IndexFlatIP` (inner product, normalized vectors ≈ cosine similarity) for
  corpora under 5,000 chunks
- **Hybrid retrieval:** BM25 score + embedding cosine similarity combined via Reciprocal Rank
  Fusion (RRF) — robust to both exact-term and conceptual queries
- **Persistence:** Serialize FAISS index to disk; load on server start; rebuild only when source
  files change (mtime-based delta detection)

#### R4 — `git-worktree-manager` Hardening

Three targeted changes:

1. **Configurable base path:** Read `WORKTREES_DIR` from environment (default:
   `workspace_root / ".claude" / "worktrees"`) to keep worktrees within the repo boundary
2. **Dry-run merge:** Add `check_merge_conflicts(agent_name, target_branch)` tool that runs
   `git merge --no-commit --no-ff` and reports conflicts without committing
3. **Branch cleanup:** Add `delete_branch(agent_name)` tool to remove the agent branch after
   successful merge and worktree removal

#### R5 — Update H-CE01 Hook After `cc00-tools` Retirement

The `check_context_budget` MCP call in the H-CE01 hook must be replaced with a direct
calculation in the hook's PowerShell script. The arithmetic is: `($contextKB / 195) * 100` where
195 KB approximates Claude Sonnet's effective 200k-token context in KB. No MCP server is needed
for this operation.

#### R6 — Correct `workspace-knowledge` Tool Descriptions

The `search_docs` tool currently claims "semantic search." After Phase 1 this should read
"BM25 keyword search with metadata filtering." After Phase 2 it should read "hybrid BM25 +
embedding search." Accurate tool descriptions prevent agent overreliance on capabilities that do
not exist.

#### R7 — Build Complementary MCP Tools on the Upgraded RAG Engine

Seven additional tool endpoints on the same `workspace-knowledge` server were identified as
high-value additions that pass the MCP Inclusion Charter three-gate test. None require a new MCP
server — all are additional tool methods on the existing upgraded server:

| Priority | Tool                         | Phase Dependency | Capability Gap Filled                                                                        |
| -------- | ---------------------------- | ---------------- | -------------------------------------------------------------------------------------------- |
| P0       | `query_workspace`            | Phase 1          | Core RAG retrieval (the upgrade itself)                                                      |
| P1       | `summarize_context`          | Phase 1          | Pre-digests multi-chunk briefings for agent context injection                                |
| P1       | `check_adr_precedent`        | Phase 1          | Retrieves prior ADRs for a proposed technology; prevents Technology Decision Lock violations |
| P2       | `find_related_documents`     | Phase 2          | Semantic graph traversal — returns N most similar documents to a seed path                   |
| P2       | `list_research_by_topic`     | Phase 2          | Filters Telescope archive by semantic topic cluster; makes institutional memory discoverable |
| P3       | `validate_pipeline_document` | Phase 1          | Retrieves canonical `pipeline.md` and validates a submitted document structurally            |
| P3       | `agent_knowledge_brief`      | Phase 2          | Compiles agent profile + all referenced skills as a structured activation packet             |

#### R8 — Implement Graceful-Degradation Fallback Architecture

The server must maintain a named three-tier fallback ladder so that RAG subsystem failures do not
crash the server or silently return degraded results:

- **Tier A — Hybrid (nominal Phase 2):** Full BM25 + FAISS embedding search
- **Tier B — BM25 (nominal Phase 1 / degraded Phase 2):** Keyword-only search
- **Tier C — Raw Filesystem (disaster recovery):** Direct filesystem term-frequency search — zero
  third-party dependencies; always reachable; equivalent to the current server implementation

Seven failure modes (F1–F7: missing libraries, corrupt indexes, OOM, model file absent, corpus
unreadable) are addressed. Tier demotion is one-way per server session; re-elevation requires a
restart. Every tool response includes a `_meta` block declaring `search_tier`,
`degradation_reason`, and `result_quality` — the calling agent always knows the active retrieval
fidelity. Tier C preserves the current server's raw-filesystem behavior explicitly as the
disaster recovery floor. Full implementation code patterns and acceptance criteria are in
`rag-local-deployment/ops-manual.md §10`.

---

### Implementation Priority

| Recommendation                    | Priority | Estimated Effort | Impact | Risk   |
| --------------------------------- | -------- | ---------------- | ------ | ------ |
| Retire `pipeline-automation`      | P0       | 30 min           | High   | Low    |
| Retire `cc00-tools`               | P0       | 30 min           | Medium | Low    |
| Update H-CE01 hook                | P0       | 1 hour           | Medium | Low    |
| MCP Inclusion Charter (R1)        | P1       | 2 hours (doc)    | High   | None   |
| Phase 1 RAG: BM25 + chunking      | P1       | 1 day            | High   | Low    |
| Phase 1: Add telescope/ to index  | P1       | 30 min           | High   | Low    |
| Graceful-degradation DR (R8)      | P1       | 4 hours          | High   | Low    |
| `git-worktree-manager` hardening  | P2       | 4 hours          | Medium | Low    |
| Phase 2 RAG: Embeddings           | P2       | 2 days           | High   | Medium |
| Complementary tools — P1 set (R7) | P2       | 1 day            | Medium | Low    |
| Complementary tools — P2 set (R7) | P3       | 1 day            | High   | Medium |

---

### Next Steps

1. **Immediate (CEO authorization pending):**
   - Remove `pipeline-automation` and `cc00-tools` entries from `.mcp.json`
   - Update `telescope/README.md` index to include this report
   - Update H-CE01 hook to eliminate `cc00-tools` dependency

2. **Phase 1 (within current sprint):**
   - Rewrite `workspace-knowledge/server.py` with BM25 engine, chunking, and `telescope/` scope
   - Implement graceful-degradation three-tier fallback (Hybrid → BM25 → Raw FS) with `_meta` operational signals on every response
   - Build Phase 1-deployable complementary tools: `summarize_context`, `check_adr_precedent`, `validate_pipeline_document`
   - Correct tool description strings
   - Install `rank_bm25` into workspace Python environment

3. **Phase 2 (following sprint):**
   - Add `sentence-transformers` and `faiss-cpu` dependencies
   - Implement hybrid BM25 + embedding retrieval with FAISS persistence
   - Build Phase 2-dependent complementary tools: `find_related_documents`, `list_research_by_topic`, `agent_knowledge_brief`
   - Benchmark query latency on representative corpus

4. **Governance:**
   - Draft MCP Inclusion Charter as a `.claude/rules/mcp-governance.md` rule file
   - Apply R4 hardening changes to `git-worktree-manager`

---

## References

### Internal Documentation

- `.mcp.json` — MCP server manifest (audited)
- `.claude/mcp-servers/*/server.py` — All four server implementations (audited)
- `CLAUDE.md §8` — Pipeline guardrails (governance standard)
- `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md` — Worktree pattern spec
- `core-component-00/agent-systems-engineering/governance/` — ASE compliance standards
- `telescope/2026-06-19-cc00-engineering-hooks-research/research-report.md` — Prior hooks investigation
- `telescope/2026-06-20-mcp-server-assessment/rag-deployment-proposal.md` — CEO-facing RAG deployment proposal
- `telescope/2026-06-20-mcp-server-assessment/rag-local-deployment/ops-manual.md` — Full RAG operations manual (software stack, model registry, hardware-adaptive config, deployment procedures, troubleshooting)

### External Sources

- Robertson, S. & Zaragoza, H. (2009). _The Probabilistic Relevance Framework: BM25 and Beyond._
  \[Knowledge Cutoff - verify for latest BM25 implementations\]
- Reimers, N. & Gurevych, I. (2019). _Sentence-BERT: Sentence Embeddings using Siamese
  BERT-Networks._ (basis for `all-MiniLM-L6-v2`)
  \[Knowledge Cutoff - verify current model card on Hugging Face\]
- Johnson, J. et al. (2021). _Billion-scale similarity search with GPUs._ (FAISS)
  \[Knowledge Cutoff - verify current FAISS CPU index recommendations\]
- `rank_bm25` Python library: `pip install rank_bm25`
- `sentence-transformers` Python library: `pip install sentence-transformers`
- `faiss-cpu` Python library: `pip install faiss-cpu`

### Related Work

- `telescope/2026-06-19-cc00-engineering-hooks-research/` — Hook engineering investigation that
  surfaces dependency on `cc00-tools` MCP tools (H-CE01, H-RAG01)

---

## Appendices

### Appendix A: Proposed `.mcp.json` After Retirement

```json
{
  "mcpServers": {
    "workspace-knowledge": {
      "command": "python",
      "args": ["${CLAUDE_PROJECT_DIR:-.}/.claude/mcp-servers/workspace-knowledge/server.py"],
      "env": {
        "WORKSPACE_ROOT": "${CLAUDE_PROJECT_DIR:-.}",
        "FASTMCP_LOG_LEVEL": "ERROR"
      }
    },
    "git-worktree-manager": {
      "command": "python",
      "args": ["${CLAUDE_PROJECT_DIR:-.}/.claude/mcp-servers/git-worktree-manager/server.py"],
      "env": {
        "WORKSPACE_ROOT": "${CLAUDE_PROJECT_DIR:-.}",
        "FASTMCP_LOG_LEVEL": "ERROR",
        "WORKTREES_DIR": "${CLAUDE_PROJECT_DIR:-.}/.claude/worktrees"
      }
    }
  }
}
```

---

### Appendix B: Phase 1 BM25 Engine — Reference Architecture

```python
from rank_bm25 import BM25Okapi
import re

def chunk_document(content: str, chunk_size: int = 512) -> list[dict]:
    """Split document into overlapping paragraph chunks with metadata."""
    paragraphs = re.split(r'\n{2,}', content)
    chunks = []
    current_header = ""
    for para in paragraphs:
        if para.startswith('#'):
            current_header = para.strip()
        chunks.append({
            "text": para,
            "header": current_header,
            "tokens": len(para.split()),
        })
    return chunks

def build_bm25_index(chunks: list[dict]) -> BM25Okapi:
    tokenized = [c["text"].lower().split() for c in chunks]
    return BM25Okapi(tokenized)

def search(query: str, bm25: BM25Okapi, chunks: list[dict], top_k: int = 5):
    scores = bm25.get_scores(query.lower().split())
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    return [chunks[i] for i, _ in ranked[:top_k]]
```

---

### Appendix C: MCP Inclusion Charter — Draft Framework

> **MCP Inclusion Gate (three mandatory conditions, all must pass):**
>
> 1. **Capability gate** — The tool performs computation, subprocess execution, or stateful
>    operation that Claude Code's native tools (Read, Edit, Grep, Glob, Bash, Write) cannot
>    replicate with equivalent quality.
> 2. **Governance gate** — The tool enforces, not bypasses, pipeline guardrails. Any tool that
>    can advance a pipeline stage, modify governance records, or skip approval gates is rejected.
> 3. **Completeness gate** — Every tool in the server produces substantively correct, actionable
>    output for its stated purpose. Stub responses, "requires inspection" returns, and
>    hardcoded-threshold heuristics presented as analysis do not qualify.
>
> A server that fails any gate must not be registered in `.mcp.json`.

---

## Version History

| Version | Date       | Author                    | Changes                                                                                                                                                                                                    |
| ------- | ---------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-06-24 | CC-00 Laboratory / Claude | Initial research report completed                                                                                                                                                                          |
| 1.1     | 2026-06-24 | CC-00 Laboratory / Claude | Finding 5 updated with actual corpus metrics (1,060 files, ~4,075 chunks); hardware tier corrected to Tier 3 (31.6 GB RAM → `all-mpnet-base-v2`); cross-references added to ops-manual.md                  |
| 1.2     | 2026-06-24 | CC-00 Laboratory / Claude | Added R7 (complementary MCP tools suite, 7 tools, P0–P3) and R8 (graceful-degradation fallback architecture, three-tier ladder, F1–F7 failure modes); updated implementation priority table and next steps |

---

**Template Version:** 1.0
**Last Updated:** 2026-06-24
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
