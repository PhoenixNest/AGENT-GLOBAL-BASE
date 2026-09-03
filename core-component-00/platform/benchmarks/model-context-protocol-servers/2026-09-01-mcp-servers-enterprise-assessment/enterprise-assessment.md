# Enterprise-Level Engineering Assessment — CC-00 MCP Servers (`workspace-knowledge`, `agent-memory`)

---

## Metadata

| Field                           | Value                                                                                                                                                                                                                                                                         |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Assessment ID**               | `2026-09-01-mcp-servers-enterprise-assessment`                                                                                                                                                                                                                                |
| **Date**                        | 2026-09-01                                                                                                                                                                                                                                                                    |
| **Assessor**                    | Dr. Tomasz Wieczorek (Safety & Evaluation Engineer — assessment methodology) + Ravi Deshmukh (Infrastructure Engineer — platform subject expertise), per `benchmarks/README.md`'s 2026-08-31 platform-domain ownership convention; directed by Dr. Elias Vance at CEO request |
| **Reviewer**                    | Dr. Elias Vance (Laboratory Director) — independent of both named Assessors                                                                                                                                                                                                   |
| **Module(s) / System Assessed** | `core-component-00/platform/model-context-protocol-servers/` — the two registered MCP servers, `workspace-knowledge` and `agent-memory`                                                                                                                                       |
| **Requestor**                   | CEO                                                                                                                                                                                                                                                                           |
| **Prior Assessment**            | None — first pass                                                                                                                                                                                                                                                             |

**Process note (Reviewer independence).** This assessment was executed end-to-end within a single
Claude Code session operating as Dr. Vance; the Wieczorek/Deshmukh Assessor split and the
Vance Reviewer role reflect the workspace's documented ownership convention, not a separately
enacted second pass by a different agent or human. The excerpt-to-claim independent check this
template requires of a Reviewer has therefore **not** been independently performed by a second
party — see Evidence Completeness Statement.

---

## Research Freshness (Mandatory)

**Knowledge cutoff of assessor:** January 2026 — all Enterprise-Standard Practice claims below are
sourced from the live research pass in this section, not from training-data recall.

**Live research performed this session:** Yes

### Source Register

| ID  | Claim Supported                                                                                                                               | Query Run                                                                                            | Source                                                                                                                                                                                          | Retrieval Date | Verbatim Excerpt                                                                                                                                                                                                                                                                                                                                                 | Status                                     |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| S1  | Adding BM25 to a vector-only retriever is the standard high-value production upgrade                                                          | enterprise RAG hybrid retrieval graceful degradation tiered fallback BM25 vector search architecture | [Hybrid Search for RAG: Combining BM25 and Dense Vector Search](https://denser.ai/blog/hybrid-search-for-rag/)                                                                                  | 2026-09-01     | "If your RAG system uses pure vector search, adding BM25 is the single highest-impact retrieval upgrade you can make."                                                                                                                                                                                                                                           | Verified — excerpt supports claim          |
| S2  | Production systems must publish health/readiness endpoints and degrade gracefully on dependency failure                                       | (fetched directly)                                                                                   | [Best Practices — Model Context Protocol - Best Practice](https://mcp-best-practice.github.io/mcp-best-practice/best-practice/)                                                                 | 2026-09-01     | "Health, readiness, and circuit breakers: Publish health endpoints; trip on dependency failures; shed load gracefully"                                                                                                                                                                                                                                           | Verified — excerpt supports claim          |
| S3  | Production systems must maintain structured, per-call audit trails capturing arguments, decisions, and outcomes                               | (fetched directly)                                                                                   | [Best Practices — Model Context Protocol - Best Practice](https://mcp-best-practice.github.io/mcp-best-practice/best-practice/)                                                                 | 2026-09-01     | "Structured audit trails: Capture who/what/when/why, including tool arguments (with redaction), decisions, and outcomes"                                                                                                                                                                                                                                         | Verified — excerpt supports claim          |
| S4  | PII must be redacted from source text before it is embedded, not after                                                                        | PII scrubbing redaction embedding pipeline enterprise data protection best practice vector database  | [PII in Vector Embeddings: A Defense Guide](https://philterd.ai/guides/pii-in-vector-embeddings-a-defense-guide/)                                                                               | 2026-09-01     | "If the source text doesn't contain PII when it's embedded, the embedding can't leak PII even under perfect inversion." / "Redact what you can, add noise to what you can't, keep the store inside your perimeter, and apply layered defenses."                                                                                                                  | Verified — excerpt supports claim          |
| S5  | Production MCP-server testing maturity is defined by five gates: smoke, conformance, scenario, load, pentest                                  | "MCP server" test suite automated testing production readiness enterprise 2026                       | [Testing MCP Servers: The Five Gates Between Demo and Production](https://dev.to/aws-heroes/testing-mcp-servers-the-five-gates-between-demo-and-production-2inf)                                | 2026-09-01     | "A practical testing strategy for MCP servers has five production gates: 1. Smoke... 2. Conformance... 3. Scenarios: Do real workflows keep working release after release? 4. Load... 5. Pentest..."                                                                                                                                                             | Verified — excerpt supports claim          |
| S6  | Neither server logs structured per-call audit data (no `logging`/`logger` usage in first-party code)                                          | `grep -n "logging\|logger\." workspace-knowledge/server.py agent-memory/server.py`                   | `workspace-knowledge/server.py`, `agent-memory/server.py`                                                                                                                                       | 2026-09-01     | Grep returned zero matches for `logging`/`logger.` in either file's first-party code this session.                                                                                                                                                                                                                                                               | Internal — verified against primary source |
| S7  | `workspace-knowledge`'s tiered fallback (`HYBRID_QDRANT → HYBRID → BM25 → RAWFS`) is implemented and was observed degrading live this session | `mcp__workspace-knowledge__health_check` tool call, this session                                     | `workspace-knowledge/server.py:226-302,642-667`; live tool output                                                                                                                               | 2026-09-01     | Live `health_check` output: `"document_knowledge_base":{"reachable":false,"search_tier":"hybrid","degradation_reason":"Qdrant Docker unreachable — falling back to FAISS: timed out"}`; the following `search_docs` call still returned five ranked, relevant results.                                                                                           | Internal — verified against primary source |
| S8  | `agent-memory`'s health-check embedder-capability field is a cached snapshot, not re-probed on each call                                      | `mcp__agent-memory__health_check` then `mcp__agent-memory__search_memory`, this session              | `agent-memory/server.py:599-628` (docstring: "a cached 'ready' service state is trusted as-is (no re-probe — a network call is not something a health check should trigger)"); live tool output | 2026-09-01     | `health_check` reported `"embedder_service_state":"ready","effective_path":"embedder-service"`; the immediately following `search_memory` call returned `"degraded":true,"reason":"qdrant search failed: embedder-service unavailable and in-process embedder not ready"`.                                                                                       | Internal — verified against primary source |
| S9  | `agent-memory` open ASE gap: PII scrubbing on the embed path is not implemented                                                               | (n/a — internal)                                                                                     | `.claude/rules/mcp-governance.md`, `agent-memory` row                                                                                                                                           | 2026-09-01     | "Two Required-level ASE gaps open (PII scrubbing on the embed path; merge-integration-agent designation) — tracked as harness-engineering backlog, neither blocking."                                                                                                                                                                                            | Internal — verified against primary source |
| S10 | First-party test-file counts for both servers                                                                                                 | `find <server> -iname "test_*.py" -not -path "*/.venv/*"`, this session                              | `agent-memory/tests/*.py` (9 files); `workspace-knowledge/tests/*.py` (1 file)                                                                                                                  | 2026-09-01     | `agent-memory`: `test_cross_server_health_comparison.py, test_embedder_reliability_fixes.py, test_read_constraints_reverification.py, test_server.py, test_tier3_keyword_search.py, test_write_gate.py, test_write_memory.py, test_write_path_adversarial_evaluation.py, test_write_provenance.py`. `workspace-knowledge`: `test_upsert_delete_ordering_fix.py`. | Internal — verified against primary source |

---

## Assessment Scope

### What Was Assessed

Both registered MCP servers as currently deployed: `workspace-knowledge` (hybrid BM25/semantic
document search) and `agent-memory` (episodic/semantic/procedural/reflection memory store),
including their `health_check` telemetry, retrieval/search behavior under a real live degradation
event observed this session, logging/observability posture, PII-handling posture on the embedding
path, and automated test coverage.

### Why Now

CEO directive, this session, following the 2026-09-01 MCP-server maintenance review (Items #8–#10,
all closed) and the 2026-08-31 scope expansion of this benchmark archive to cover `platform/`.

### Out of Scope

`embedder-service` itself (internal infrastructure, not a registered MCP server — see
`.claude/rules/mcp-governance.md` "Shared Infrastructure"). The two previously-retired servers
(`pipeline-automation`, `cc00-tools`/`git-worktree-manager`) — their retirement is not revisited
here. Non-Windows DR-backup scheduling (Item #3, open in the maintenance log) — operational, not a
benchmark dimension. `agent-memory`'s merge-integration-agent designation gap — tracked
separately in the same governance row as S9's PII gap; not independently benchmarked here.

---

## Benchmark Table

| ID  | Dimension                                                              | Our Current State                                                                                                                                                                                                                                                                                                                                                                                         | Internal Source ID(s) | Enterprise-Standard Practice                                                                                                                          | External Source ID(s) | Verdict        | Severity |
| --- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | -------------- | -------- |
| B1  | Hybrid retrieval + tiered graceful degradation (`workspace-knowledge`) | Tiered `HYBRID_QDRANT → HYBRID → BM25 → RAWFS` search; live-observed this session degrading from `HYBRID_QDRANT` to `HYBRID` on a real Qdrant timeout, with `search_docs` still returning correct ranked results uninterrupted                                                                                                                                                                            | S7                    | Hybrid BM25+vector retrieval, with graceful degradation and load-shedding on dependency failure, is current production practice                       | S1, S2                | Pass at parity | —        |
| B2  | Embedder-capability health-check staleness (`agent-memory`)            | `health_check`'s `embedder_service_state`/`effective_path` fields are a **cached** snapshot by design (no re-probe on "ready", to avoid adding network latency to every health check); live-reproduced this session: `health_check` reported `"ready"`/`"embedder-service"` immediately before a real `search_memory` call failed with `"embedder-service unavailable and in-process embedder not ready"` | S8                    | Health/readiness endpoints should "trip on dependency failures" — i.e., reflect real-time serviceability, not a stale cached state                    | S2                    | Partial        | P1       |
| B3  | Structured per-call audit logging                                      | Neither `workspace-knowledge/server.py` nor `agent-memory/server.py` contains any `logging`/`logger` call in first-party code — no per-tool-call record of arguments, duration, or outcome                                                                                                                                                                                                                | S6                    | Production systems capture structured audit trails: "who/what/when/why, including tool arguments (with redaction), decisions, and outcomes"           | S3                    | Gap            | P2       |
| B4  | PII redaction on the embedding path (`agent-memory`)                   | No PII/redaction/scrubbing code found in `agent-memory`'s first-party source (`grep -rni "pii\|redact\|scrub"` returns zero hits); already tracked internally as an open Required-level ASE gap                                                                                                                                                                                                           | S9                    | Sensitive text should be redacted before embedding, since "the embedding can't leak PII" only "if the source text doesn't contain [it]" when embedded | S4                    | Gap            | P1       |
| B5  | Production-testing gate coverage (`agent-memory`)                      | 9 first-party test files exercising write-gate, write-path adversarial evaluation, embedder reliability, cross-server health comparison, and tier-3 keyword search — covers the "Scenarios" gate; no conformance-harness, load-test, or pentest tooling found                                                                                                                                             | S10                   | A mature MCP-server testing posture spans five gates: smoke, conformance, scenarios, load, pentest                                                    | S5                    | Partial        | P2       |
| B6  | Production-testing gate coverage (`workspace-knowledge`)               | 1 first-party test file, scoped to a single prior upsert/delete-ordering bug fix — no general scenario-regression suite for the tiered-search/degradation logic B1 documents, and no conformance/load/pentest tooling found                                                                                                                                                                               | S10                   | Same five-gate model as B5; "Scenarios" specifically requires real workflows to keep working release after release                                    | S5                    | Gap            | P1       |

---

## Severity-Ordered Remediation Plan

**Declared scale for this assessment:** Scale A — ASGF Gap Severity
(`crew/director/elias-vance/skills/asgf-compliance-audit.md` § Gap Severity Classification) — the
assessed surface is a CC-00 engineering deployment (the lab's MCP servers), not a shipping
company/studio product, so Scale A governs throughout.

| ID  | Priority | Benchmark Row | Gap                                                                                               | Source ID(s) | Owner                             | Fix                                                                                                                                                                                                           | Severity Justification                                                                                                                                                                                                                                                                                     |
| --- | -------- | ------------- | ------------------------------------------------------------------------------------------------- | ------------ | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1  | P1       | B6            | `workspace-knowledge` has no scenario-regression coverage for its tiered-search/degradation logic | S5, S10      | Ravi Deshmukh, sign-off Dr. Vance | Add a `test_search_tier_degradation.py` suite exercising forced HYBRID_QDRANT→HYBRID→BM25→RAWFS transitions, mirroring `agent-memory`'s scenario-test pattern                                                 | Scale A P1 — "Gap that will degrade output quality or reliability at scale but does not cause outages": today's live Qdrant-timeout event (S7) shows the fallback path working, but it is exercised in production with zero regression coverage, not by test                                               |
| R2  | P1       | B2            | `agent-memory`'s reported embedder capability can go stale relative to actual serviceability      | S2, S8       | Ravi Deshmukh, sign-off Dr. Vance | Add a bounded-staleness indicator (e.g. last-probe timestamp) to `health_check`'s `search_capability` block, or a short TTL-gated re-probe, so a caller can distinguish "confirmed ready" from "cached ready" | Scale A P1 — "Gap that will degrade output quality or reliability at scale": a monitor/alert trusting `health_check`'s cached "ready" would miss a real failure window this session directly reproduced                                                                                                    |
| R3  | P1       | B4            | No PII redaction on `agent-memory`'s embedding path                                               | S4, S9       | Ravi Deshmukh, sign-off Dr. Vance | Implement redact-before-embed scrubbing on `write_memory`'s ingestion path per S4's layered-defense model (redact known patterns, then embed)                                                                 | Scale A P1 — "Gap that will degrade output quality or reliability at scale": unredacted PII entering a shared, queryable vector store is a standing exposure risk every subsequent `search_memory` call can surface; already tracked as Required-level in ASE, corroborated here against external practice |
| R4  | P2       | B3            | No structured per-call audit logging in either server                                             | S3, S6       | Ravi Deshmukh, sign-off Dr. Vance | Add structured logging (`tool_name`, `duration_ms`, `ok`/`error`, redacted arguments) to each `@mcp.tool()` entry/exit in both servers                                                                        | Scale A P2 — "Gap that reduces engineering maintainability or makes the system harder to extend": absence of audit trails does not itself cause a failure, but materially slows diagnosing one when it occurs                                                                                              |
| R5  | P2       | B5            | `agent-memory` has scenario tests but no conformance/load/pentest gates                           | S5, S10      | Ravi Deshmukh, sign-off Dr. Vance | Add a minimal conformance check (schema/tool-contract validation) as the next gate; defer load/pentest until concurrent multi-agent usage patterns are better characterized                                   | Scale A P2 — "reduces engineering maintainability": scenario coverage already exists and is the strongest of the five gates; the remaining three are extension work, not a live reliability risk today                                                                                                     |

---

## Compliance Verdict

**Conditional — P1 gaps open.**

Both servers implement the two enterprise-baseline architecture patterns that matter most for
this class of system — hybrid BM25/vector retrieval with tiered graceful degradation
(`workspace-knowledge`, confirmed live under a real Qdrant outage this session) and a
capability-aware embedding path with explicit fallback signaling (`agent-memory`). Neither server
is at risk of the "will cause production failure" bar that would make this Below Standard. But
four P1s are real and none is hypothetical: `workspace-knowledge`'s core degradation logic runs in
production with no regression coverage; `agent-memory`'s health signal can read "ready" a moment
before a real call fails, exactly as reproduced in this session; and `agent-memory`'s
already-tracked PII gap is now independently corroborated against external redact-before-embed
practice. The single biggest lever to close the gap: R1 and R2 together (test coverage for the
degradation path, and a non-stale health signal) would remove the two dimensions where this
session's own live observations, not just document review, surfaced a real discrepancy between
reported and actual state.

### Evidence Completeness Statement

- 6 of 6 Benchmark Table rows carry a `Verified` external source; none is `Unassessed — no source`.
- Every "Our Current State" cell traces to either a `file:line` region or a live tool call made in
  this session (S6–S10) — no claim in this table rests on training-data recall of either server's
  behavior.
- One dimension the assessor considered but did not source externally: whether either server's
  degraded-search behavior meets a specific enterprise **latency** SLO under load. No external
  source with a comparable quantitative benchmark was found in this pass, and no load test exists
  internally to produce our own number — this is why B5/B6 mark load-testing as an open gate
  rather than asserting a latency verdict.
- **Reviewer independence caveat (repeated from Metadata):** the Reviewer named above (Dr. Vance)
  has not performed a separately-enacted excerpt-to-claim check by a distinct party — this entire
  assessment was produced in one continuous session. Every excerpt in the Source Register was
  nonetheless copied directly from the fetched source at the point of citation, not reconstructed
  from memory, which is the specific failure mode the Reviewer check exists to catch. The CEO
  should treat this document's sourcing as self-verified, not independently verified, until a
  genuinely separate pass reviews it.

---

## Sources

- **S1** — [Hybrid Search for RAG: Combining BM25 and Dense Vector Search](https://denser.ai/blog/hybrid-search-for-rag/)
- **S2** — [Best Practices — Model Context Protocol - Best Practice](https://mcp-best-practice.github.io/mcp-best-practice/best-practice/)
- **S3** — [Best Practices — Model Context Protocol - Best Practice](https://mcp-best-practice.github.io/mcp-best-practice/best-practice/)
- **S4** — [PII in Vector Embeddings: A Defense Guide](https://philterd.ai/guides/pii-in-vector-embeddings-a-defense-guide/)
- **S5** — [Testing MCP Servers: The Five Gates Between Demo and Production](https://dev.to/aws-heroes/testing-mcp-servers-the-five-gates-between-demo-and-production-2inf)
- **S6** — `core-component-00/platform/model-context-protocol-servers/workspace-knowledge/server.py`, `agent-memory/server.py` (grep, this session)
- **S7** — `core-component-00/platform/model-context-protocol-servers/workspace-knowledge/server.py:226-302,642-667`; live `health_check`/`search_docs` calls, this session
- **S8** — `core-component-00/platform/model-context-protocol-servers/agent-memory/server.py:599-628`; live `health_check`/`search_memory` calls, this session
- **S9** — `.claude/rules/mcp-governance.md`, `agent-memory` row
- **S10** — `agent-memory/tests/`, `workspace-knowledge/tests/` (file listing, this session)

---

## Version History

| Version | Date       | Author                                                                | Changes                       |
| ------- | ---------- | --------------------------------------------------------------------- | ----------------------------- |
| 1.0     | 2026-09-01 | Dr. Elias Vance (directing; see Metadata for Assessor/Reviewer split) | Initial enterprise assessment |

---

**Template Version:** 1.0
**Last Updated:** 2026-08-16
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
