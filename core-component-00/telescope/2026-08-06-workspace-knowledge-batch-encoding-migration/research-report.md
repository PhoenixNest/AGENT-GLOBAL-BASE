# Research Report — Workspace-Knowledge Batch-Encoding Migration onto `embedder-service`

---

## Metadata

| Field                | Value                                                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------------------- |
| **Investigation ID** | `2026-08-06-workspace-knowledge-batch-encoding-migration`                                               |
| **Date Started**     | 2026-08-06                                                                                              |
| **Date Completed**   | 2026-08-06                                                                                              |
| **Status**           | Implemented and closed 2026-08-06 — all 5 phases complete; see `supporting/implementation-plan.md` §10  |
| **Investigator**     | Dr. Elias Vance, Laboratory Director                                                                    |
| **Laboratory**       | Core Component 00                                                                                       |
| **Module(s)**        | MCP server infrastructure (`workspace-knowledge`, `embedder-service`); `retrieval-augmented-generation` |
| **Priority**         | Medium — disk/efficiency gap, not an outage                                                             |
| **Requestor**        | CEO                                                                                                     |

---

## Executive Summary

> `workspace-knowledge/embedding/model/` carries a 418.4 MB private copy of `all-mpnet-base-v2`
> that byte-for-byte duplicates the shared cache at `_shared/models/`. Two prior investigations
> (2026-08-06, ad hoc) established why: the 2026-07-13/14 `embedder-service` build's Phase 4
> (commit `33e3a796`) deliberately migrated only `workspace-knowledge`'s query-time embedding,
> leaving the batch index-build/reseed/upsert paths on the local loader by explicit, documented
> design choice — not as an unfinished or interrupted migration. This report formally scopes what
> completing that migration ("Phase 6") would require, and the accompanying
> `supporting/implementation-plan.md` proposes a five-phase plan, gated on first completing the
> full-corpus throughput benchmark that Phase 4 itself abandoned unfinished. Nothing in either
> document authorizes work to start.

---

## Investigation Scope

### What Was Investigated

Whether and how `workspace-knowledge`'s batch-encoding call sites — `_build_or_load_faiss_index`,
`_seed_qdrant_collection`, `_upsert_file_to_qdrant` in `mcp-servers/workspace-knowledge/server.py`
— can be migrated onto the existing `embedder-service`, to eliminate the private
`all-mpnet-base-v2` copy these paths are now the sole remaining reason to keep.

### Why This Investigation Was Needed

Following two ad hoc CEO queries (2026-08-06): first, why the duplicate model copy exists and
whether it is safe to delete (answer: no — it is required by the batch paths); second, what would
need to be prepared to complete the deferred migration. This report is the formal scoping response
requested to close that second question, and its companion implementation plan is presented for
sign-off per this workspace's User Approval Gate convention (`.claude/rules/workspace-conventions.md`
§ User Approval Gates).

### Out of Scope

- Query-time embedding — already migrated and closed (Phase 4, commit `33e3a796`, 2026-07-14).
- `agent-memory` — its embedding paths are already fully migrated (Phase 2, 2026-07-13); unaffected
  by this proposal.
- Any change to the Qdrant hard-timeout watchdog, the disaster-recovery replay path, or the
  degrade-never-block contract established by the original `embedder-service` build — all remain
  correct and are not revisited here.
- Resolving the two open Required-level ASGF gaps (PII scrubbing on the embed path;
  merge-integration-agent designation) — referenced as a dependency this plan must account for,
  not solved by this report.

---

## Research Questions

1. Can `embedder-service`'s existing `/embed` endpoint — already batch-capable up to
   `MAX_TEXTS_PER_REQUEST` (256) texts per call — support `workspace-knowledge`'s full-corpus
   batch-encoding workload without protocol changes, or does the endpoint itself need extending?
2. What is the actual throughput of HTTP-batched encoding via `embedder-service` against the full
   ~1,770-file workspace corpus, compared to local in-process CUDA batch encoding — the comparison
   Phase 4 attempted and abandoned after 30+ minutes without completing?
3. Does `embedder-service`'s idle-timeout/lifecycle model (built and tuned around many short
   query-shaped calls) hold correctly under one long-running batch index-rebuild call instead?
4. What governance prerequisites — specifically the two open Required-level ASGF gaps carried
   from the 2026-07-13 build — must close before this work begins, versus being trackable in
   parallel?
5. What is the actual disk-space benefit of completing this migration, weighed against its
   implementation and ongoing-operational cost?

---

## Methodology

### Approach

Documentary and code review only — no implementation, benchmarking, or experimentation was
performed for this report, by design: this is the scoping document that precedes a build, matching
the same plan-first, CEO-sign-off-then-build sequencing the original `embedder-service` programme
used.

1. Re-verified the disk-duplication finding directly against the current branch
   (`core00/dev/engineering`).
2. Reviewed git history for every commit touching `embedder-service` and
   `workspace-knowledge/server.py` (`git log --oneline --all`), confirming no later commit revisited
   the batch-path scoping decision made in `33e3a796`.
3. Read the full governing plan and closeout review for the 2026-07-13 build
   (`2026-07-13-mcp-embedder-service-redesign/supporting/implementation-plan.md`) to confirm current
   open items and the personnel/phase-gate pattern to reuse.
4. Confirmed current ASGF exception/gap status directly against
   `agent-systems-governance-framework/governance/adr-asgf-001.md`.
5. Cross-checked current crew roster and authority scope (`crew/README.md`, `crew/CLAUDE.md`) for
   personnel assignment, since the crew has grown since the 2026-07-13 build (8 assigned then; 12
   total today).

### Tools and Resources

- `git log`, `git show` against `core00/dev/engineering`
- Direct code reads: `workspace-knowledge/server.py`, `_shared/embedder-service/server.py`
- Prior telescope reports: `2026-07-13-mcp-embedder-service-redesign/` (report + implementation
  plan + closeout review)
- `agent-systems-governance-framework/governance/adr-asgf-001.md`

### Constraints

- No implementation or live benchmarking performed in this report — intentional; see Executive
  Summary.
- Disk and throughput figures are measured on this machine only; not validated against any other
  deployment target.

---

## Findings

### Finding 1: The duplication is real, current, and unaffected by the branch switch

**Evidence:** Both `workspace-knowledge/embedding/model/` and
`_shared/models/sentence-transformers--all-mpnet-base-v2/` measure 418.4 MB on
`core00/dev/engineering`, identical to the prior measurement.

**Implications:** The finding is stable — not an artifact of a stale branch or an in-progress
change.

### Finding 2: The gap is a deliberate scope boundary, not an interrupted migration

**Evidence:** Commit `33e3a796` ("agent/sofia: migrate workspace-knowledge query embedding to
embedder-service", 2026-07-14) states directly in its own commit body: _"deliberately left the
batch index-build/reseed/upsert paths... unmigrated: they already run off the critical
MCP-handshake path... and need a local SentenceTransformer instance for efficient batch
encoding regardless — migrating those too would be a larger architecture change than 'the same
client pattern as Phase 2' calls for."_ The governing `implementation-plan.md`'s Phase 4 gate
("no retrieval-quality regression") was scoped to query embedding only, from before the phase
began — never to the batch paths.

**Implications:** There is no stalled or abandoned work to resume. A batch-path migration is new
scope requiring its own plan and sign-off, which is what this report and its companion
implementation plan provide.

### Finding 3: No follow-up proposal exists anywhere in the archive

**Evidence:** A search of `core-component-00/telescope/` for any report proposing or tracking a
batch-encoding migration returned no results prior to this report.

**Implications:** This is the first formal scoping of the idea raised in the prior ad hoc
investigation — confirms it was correctly characterized as "not outstanding work" at the time.

### Finding 4: The batching primitive may already exist — throughput at scale is the open question

**Evidence:** `embedder-service/server.py`'s `/embed` endpoint already accepts up to
`MAX_TEXTS_PER_REQUEST = 256` texts per call, with a 20,000-char-per-text cap
(`MAX_TEXT_LENGTH_CHARS`). Nothing in the endpoint's contract limits it to single-text query
calls; workspace-knowledge's batch paths could in principle call it in chunks of ≤256 chunks per
request.

**Implications:** The likely shape of this migration is chunked-HTTP-batch-calls-in-a-loop, not a
new endpoint. What is genuinely unverified is whether that shape's throughput is acceptable at
full-corpus scale — see Finding 5.

### Finding 5: The decisive benchmark was never completed, for either path

**Evidence:** Phase 4's own commit message and the closeout review (`implementation-plan.md` §10.1,
§10.3.2) both disclose that the full-corpus (~1,770-file) `search_docs` comparison was "abandoned
after 30+ minutes of CPU-bound encoding without completing" — and that abandonment was for the
_local_ encoding path being benchmarked, not even the HTTP path this proposal would add.

**Implications:** There is currently zero throughput data at real-corpus scale for either
encoding path. Any Phase 6 plan that skips completing this benchmark first would be scoping a
performance-sensitive change on data that has never been gathered, repeating the same gap Phase 4
closed out with, not silently inheriting.

### Finding 6: Two Required-level ASGF gaps from the original build remain open on the same code surface

**Evidence:** `agent-systems-governance-framework/governance/adr-asgf-001.md` records the embedder-
service build's overall verdict as **Conditional**, not ASGF-Compliant, with two Required-level
gaps still open: PII scrubbing on the embed path (no owner assigned), and merge-integration-agent
designation for parallel multi-agent builds. EX-001 (a separate, Mandatory-level catch-all
exception-handling gap) was remediated and closed 2026-07-14 — that one is resolved and not
relevant here.

**Implications:** A batch-path migration deepens reliance on the same embed path the open
PII-scrubbing gap concerns. Whether to close that gap first, or track it in parallel, is a
decision for the CEO or Dr. Vance under Clause 5 authority — not a call this report makes
unilaterally, since no delegation for this specific matter has yet been granted (contrast with the
2026-07-13 build, where the CEO had explicitly delegated full responsibility before the
implementation plan resolved its own blocker decisions).

---

## Analysis

### Interpretation of Findings

This is a bounded, well-precedented follow-on to a proven pattern — Phase 4 already validated
retrieval-quality parity for query embedding using the same service, and the client-side
bounded-timeout-then-degrade contract already exists and is reusable as-is. The primary technical
risk is **performance at scale**, not correctness: the batching primitive appears to already exist
in `embedder-service`'s contract, but no one has measured whether chunked HTTP calls match local
CUDA batch-encoding throughput closely enough for a ~1,770-file corpus rebuild. The primary
governance question is whether the CEO wants the two open Required-level gaps closed before this
work proceeds, given it extends usage of the same embed path.

### Trade-offs Identified

| Approach                                                 | Removes duplication? | Throughput risk                                                                        | New governance surface                         | Effort (estimate) |
| -------------------------------------------------------- | -------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------- | ----------------- |
| Status quo (keep local batch loader)                     | No                   | None — known-good today                                                                | None                                           | None              |
| Chunked HTTP batch calls through existing `/embed`       | Yes                  | Unverified — Phase 0 benchmark gate required first                                     | Deepens exposure on the open PII-scrubbing gap | ~1.5–2 sessions   |
| Extend `embedder-service` with a dedicated bulk-mode API | Yes                  | Lower risk if built for the purpose, but new surface to build and adversarially review | Same, plus a larger new endpoint to audit      | ~2.5–3 sessions   |

### Risks and Limitations

- **The benchmark must actually complete this time.** Phase 4's abandoned attempt is a documented
  precedent for this exact failure mode; the implementation plan makes completing it a hard Phase 0
  gate rather than an optional nice-to-have.
- **Failure-mode shape changes.** Batch indexing currently tolerates slowness silently (it runs off
  a background thread with no caller waiting synchronously). A hung HTTP call to `embedder-service`
  has different failure characteristics and needs the same bounded-timeout-then-degrade discipline
  Kwame Asante's client pattern already established — reused, not reinvented.
- **Governance exposure grows, not shrinks.** Routing more traffic through the one embed path
  increases the audit surface for the still-open PII-scrubbing gap. This is a real cost of
  proceeding without resolving that gap first, not a hypothetical one.

---

## Recommendations

### Primary Recommendation

> Approve the five-phase plan in `supporting/implementation-plan.md`, gated first on completing
> the full-corpus throughput benchmark Phase 4 left unfinished. Do not authorize implementation
> work (Phase 1 onward) until that benchmark gate clears with real numbers.

### Secondary Recommendations

1. **Decide the governance-gap sequencing question explicitly** — should the PII-scrubbing and
   merge-integration-agent gaps close before Phase 1, or track in parallel? This report does not
   resolve it; the implementation plan presents it as an open blocker decision for CEO review.
2. **Reuse existing personnel and patterns rather than reinventing them** — the harness client
   pattern, the phased-gate structure, and the adversarial-review step from the 2026-07-13 build
   all transfer directly.
3. **Make the disk-reclaim outcome an explicit, measured deliverable** — not an assumed side
   effect — since that is the entire business justification for this work.

### Implementation Priority

| Recommendation                                    | Priority          | Effort                        | Impact                                            |
| ------------------------------------------------- | ----------------- | ----------------------------- | ------------------------------------------------- |
| Complete the full-corpus throughput benchmark     | Blocker (Phase 0) | ~0.5 session                  | Determines whether the rest of the plan is viable |
| Governance-gap sequencing decision                | Blocker           | N/A                           | Determines Phase 1 start condition                |
| Batch-path client migration (if benchmark clears) | P2                | ~1–2 sessions                 | Removes the 418.4 MB duplication                  |
| Disk-reclaim verification                         | P2                | Trivial, folded into closeout | Confirms the stated business benefit              |

### Next Steps

1. CEO review of this report and `supporting/implementation-plan.md`.
2. CEO decision on the governance-gap sequencing question (§ Finding 6 / plan §2.1).
3. On sign-off, Phase 0 (benchmark) begins — implementation-tracking files created at that point,
   not before, per `.claude/rules/workspace-conventions.md` § Context and Session Management.

---

## References

### Internal Documentation

- `core-component-00/telescope/2026-07-13-mcp-embedder-service-redesign/research-report.md` and
  `supporting/implementation-plan.md` — the parent programme this report extends
- `.claude/rules/mcp-governance.md` — `agent-memory` row (embedder-service shared-infrastructure
  history); `workspace-knowledge` `.mcp.json` registration context
- `core-component-00/mcp-servers/CLAUDE.md` — shared `.venv` / CUDA torch requirement, applies
  unchanged to any Phase 6 build
- `core-component-00/agent-systems-governance-framework/governance/adr-asgf-001.md` — EX-001 and
  the two open Required-level gaps

### Related Work

- `core-component-00/mcp-servers/_shared/embedder-service/server.py` — the existing `/embed`
  endpoint this proposal would extend usage of
- `core-component-00/mcp-servers/workspace-knowledge/server.py` — the three batch call sites in
  scope

---

## Open Questions

1. **Governance-gap sequencing** — must the two open Required ASGF gaps close before Phase 1?
   - Status: Presented for CEO decision, not resolved here
   - Priority: Blocker
   - Assigned: CEO / Dr. Vance (Clause 5, pending delegation for this matter)

2. **Benchmark outcome** — will chunked HTTP-batch throughput be acceptable at full-corpus scale?
   - Status: Not yet measured — Phase 0 of the implementation plan
   - Priority: Blocker
   - Assigned: Dr. Amara Nwosu-Chen (methodology), Ravi Deshmukh (infra support)

---

## Version History

| Version | Date       | Author                               | Changes                                                                       |
| ------- | ---------- | ------------------------------------ | ----------------------------------------------------------------------------- |
| 1.0     | 2026-08-06 | Dr. Elias Vance, Laboratory Director | Initial report — scopes the deferred batch-encoding migration per CEO request |

---

**Template Version:** 1.0
**Last Updated:** 2026-08-06
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
