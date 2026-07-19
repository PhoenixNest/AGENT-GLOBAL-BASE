# ADR-ASE-001 — Ratify Agent Systems Engineering as the Mandatory Governing Framework

| Field              | Value                                              |
| ------------------ | -------------------------------------------------- |
| **ADR ID**         | ADR-ASE-001                                        |
| **Status**         | Ratified                                           |
| **Date**           | 2026-04-28                                         |
| **Governing Body** | Core Component 00 Laboratory                       |
| **Authority**      | Dr. Elias Vance, Laboratory Director               |
| **Applies To**     | All LLM-powered systems built in this organisation |
| **Supersedes**     | None (inaugural decision)                          |

---

## Context

This organisation builds LLM-powered systems across four company development pipelines
(Mobile, Web, Backend API, Full-Stack), a creative studio pipeline, and internal tooling.
As of April 2026, no unified engineering standard governs how these systems are designed
and evaluated.

In the absence of a governing standard, teams independently implement LLM integrations
with the following recurring failure modes observed across projects:

| Failure Mode                    | Root Cause                                           | Observed Consequence                                       |
| ------------------------------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| Silent context overflow         | No token budget monitoring (missing Harness Layer)   | Long sessions degrade without user-visible error           |
| Hallucination under load        | No retrieval pipeline (missing RAG Layer)            | Parametric knowledge exhausted; model fabricates facts     |
| Inconsistent agent behaviour    | No structured identity design (missing Prompt Layer) | Same agent produces different outputs for identical inputs |
| Cascading failure on tool error | No error boundary (missing Harness Layer)            | Tool timeout propagates as unhandled exception to user     |
| Agent context mismatch          | No handoff protocol (missing Context Layer)          | Subagents lack decisions made by orchestrators             |

These failures share a common cause: **each engineering concern (prompts, context,
execution, knowledge) is addressed in isolation without integration design**. A system
that passes functional testing can fail in production because the layers do not compose
correctly even if each layer is individually adequate.

The emerging field of Agent Systems Engineering (ASE) addresses this gap. ASE is the
convergence of four foundational engineering disciplines — Prompt, Context, Harness, and
RAG Engineering — into a unified architecture discipline that governs how they compose.

The theoretical basis is documented in:
[_Agent Systems Engineering: The Convergence of Four Disciplines_](core-component-00/agent-systems-engineering/CONCEPTS.md)

---

## Decision

**Agent Systems Engineering is ratified as the mandatory governing framework for all
LLM-powered systems built in this organisation.**

| Clause                        | Mandate                                                                                                                                                                                                                                                                                              |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1 — Four-layer coverage**   | Every LLM-powered system must address Prompt Engineering (Layer 1), Context Engineering (Layer 2), Harness Engineering (Layer 3), and RAG / Memory (Layer 4) before it is considered production-ready. Layer 4 may be intentionally absent with documented rationale; Layers 1–3 are non-negotiable. |
| **2 — Multi-Agent (Layer 5)** | Additionally required when a system involves more than one coordinated LLM agent. Governs swarm topology, task decomposition, context handoff, and parallel execution safety.                                                                                                                        |
| **3 — Compliance Standard**   | `compliance-standard.md` defines per-layer requirements. Maintained by CC-00 and updated as requirements evolve.                                                                                                                                                                                     |
| **4 — Mandatory audit**       | ASE Compliance Audits are required before production deployment, conducted using `crew/director/elias-vance/skills/ase-compliance-audit.md`. Systems with P0 or P1 gaps may not enter production.                                                                                                    |
| **5 — Governing authority**   | The CC-00 laboratory (Director: Dr. Elias Vance) holds authority over interpretation of the standard, architectural exceptions, and evolution of compliance requirements.                                                                                                                            |

---

## Rationale

### Why mandate all four layers?

Each layer addresses a failure mode that cannot be detected by functional testing alone:

| Layer       | Why it cannot be skipped                                                                                                  |
| ----------- | ------------------------------------------------------------------------------------------------------------------------- |
| 1 — Prompt  | Unstructured prompts produce consistent outputs in testing but degrade under input variation in production                |
| 2 — Context | Context issues manifest only across long sessions or multi-agent handoffs, not in unit tests                              |
| 3 — Harness | Timeout, rate-limit, and token overflow failures are infrastructure conditions absent in test environments                |
| 4 — RAG     | Knowledge staleness and hallucination cannot be detected until the domain knowledge required is not in parametric weights |

### Why is this a cross-organisational mandate rather than a team-level guideline?

Inconsistent implementation creates inter-team incompatibilities. When Team A builds a
context-engineered orchestrator that hands off to Team B's unengineered subagent, the
handoff fails at the boundary — not within either team's system individually. The
mandate creates a shared contract that makes inter-team integration safe.

### Why CC-00 as the governing authority?

CC-00 is the organisation's centralised LLM engineering laboratory. Its five modules
are the reference implementations that the compliance standard points to. Having the
same team own both the standard and the reference implementations ensures that the
standard is always achievable and that the implementations always satisfy the standard.

---

## Consequences

| Stakeholder               | Obligations                                                                                                                                                                                                                                                                                                                       |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **All development teams** | Design LLM integrations against the ASE Compliance Standard from the outset — not retrofitted after functional development. Pre-production ASE audits are a hard gate, not a recommendation. Build against CC-00 patterns; do not create parallel implementations of harness, context, or RAG functionality without CC-00 review. |
| **CC-00 laboratory**      | Keep the Compliance Standard current as engineering modules evolve. Maintain `ase-compliance-audit.md` as the primary audit instrument. Remain available to consult on architectural exceptions and edge cases.                                                                                                                   |
| **Company pipelines**     | ASE compliance is a mandatory input to Stage 3 (_Prototype → UML Engineering Package_) of all four development pipelines for any LLM-powered feature.                                                                                                                                                                             |
| **Studio pipelines**      | ASE compliance is required before Stage 5 (_Full Production_) of the Casual Games Studio pipeline for any agent-powered feature.                                                                                                                                                                                                  |

---

## Exceptions

Architectural exceptions to this decision (e.g., a system where Layer 3 — Harness — is
demonstrably unnecessary) must be:

1. Documented in writing with technical rationale.
2. Reviewed and approved by the CC-00 Laboratory Director.
3. Recorded as an addendum to this ADR.

No exception overrides the requirement to audit; the audit documents the intentional
absence.

---

## Exceptions Log

### EX-001 — Catch-all exception handling in the bounded-timeout-then-degrade harness pattern — **REMEDIATED, CLOSED 2026-07-14**

| Field           | Value                                                                                                                                                                                                                                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Date**        | 2026-07-14                                                                                                                                                                                                                                                                                                         |
| **Requirement** | Layer 3 — "Error boundary with typed recovery" (Mandatory)                                                                                                                                                                                                                                                         |
| **Scope**       | `_call_with_hard_timeout` and its call sites: `core-component-00/engineering/context-engineering/implementations/memory_vector_store.py` (pre-existing — corrected path, was misstated as `agent-memory/...` in the original entry), `core-component-00/mcp-servers/_shared/embedder_client.py` (new, reuses the same pattern) |
| **Finding**     | These call sites use `except Exception` rather than distinct `TimeoutError`/`RateLimitError`/`ValidationError` recovery paths, which `compliance-standard.md` states plainly "are not acceptable."                                                                                                                 |
| **Approved by** | Dr. Elias Vance, Laboratory Director (authority: Clause 5 of this ADR)                                                                                                                                                                                                                                             |

**Technical rationale:** the catch-all pattern predates this exception request — it originates in
the Qdrant hard-timeout watchdog fixed 2026-07-13 (`.claude/rules/mcp-governance.md`, `agent-memory`
row) and was never audited against this standard at the time, since `agent-memory` entered
production before any ASE compliance audit was run against it. The 2026-07-13/14 embedder-service
build (`telescope/2026-07-13-mcp-embedder-service-redesign/`) was explicitly instructed to reuse
this existing pattern rather than invent a parallel one, and did so faithfully — it did not
introduce this gap, and did not expand its blast radius beyond one new call site using an already-
accepted pattern. Fault-injection testing in that build's Phase 3 (service kill mid-request,
restart-after-kill, 20-way saturation) confirms the _functional_ guarantee — bounded timeout, clean
degrade, never hang or crash — holds correctly today; the gap is diagnostic granularity (a timeout
and a validation failure both surface identically as "degraded: true, reason: exception string"),
not a reliability or safety defect.

**Why an exception rather than immediate remediation:** proper remediation means adding typed
`TimeoutError`/`RateLimitError`/`ValidationError` recovery paths across every call site using this
pattern, including ones the embedder-service build never touched. That is a harness-engineering
initiative in its own right, not a one-file fix, and belongs with `harness-engineering/`'s module
owner rather than folded into this build's closeout under time pressure.

**Conditions of this exception:**

1. This exception covers the _existing_ catch-all pattern at the scope listed above only. It does
   not extend to new harness code written outside that reused pattern.
2. A remediation task — typed recovery paths for `_call_with_hard_timeout` and its call sites — is
   tracked as CC-00 harness-engineering backlog, owned by Kwame Asante (module lead), not closed by
   this exception. Full scope below.
3. This exception is revisited at the next ASE compliance audit of `agent-memory` or
   `harness-engineering/`, whichever comes first.

#### Remediation task — scoped 2026-07-14 (Dr. Vance)

**Root cause, not just symptom:** `_call_with_hard_timeout` and `embedder_client.py` are bespoke
timeout-watchdog implementations that never route through `error_boundary.py` —
`harness-engineering/implementations/error_boundary.py` — the canonical Layer 3 reference
implementation Kwame already owns and which **already defines** `TimeoutError`, `RateLimitError`,
`ValidationError`, and `ContextOverflowError` as typed exception classes, plus the
`SafeModelCall`/`SafeToolCall`/`CircuitBreaker` patterns that use them. This gap exists because the
Qdrant/embedder call sites were built as a parallel, ad-hoc mechanism instead of extending the
canonical one — the task is reconciliation, not invention from scratch.

**Current state is inconsistent, not uniformly absent** (verified by direct read, 2026-07-14):
in `memory_vector_store.py`, `search()`, `count_points()`, and `check_reachable()` already
special-case `concurrent.futures.TimeoutError` ahead of a generic `except Exception` fallback;
`ensure_collection()` and `upsert()` do not — both timeouts and every other failure fall into one
generic warning branch. `embedder_client.py`'s `embed()` (line ~204) has no typed branch at all.

**Domain-mismatch call Kwame needs to make, not just apply labels mechanically:**
`error_boundary.py`'s `RateLimitError`/`ValidationError` were designed for remote LLM-provider
calls (HTTP 429s, prompt/response schema mismatches). Local Qdrant and the local embedder-service
have no provider rate limit — mapping onto those exact class names verbatim would misrepresent the
failure. As module owner, Kwame decides the right typed taxonomy for _this_ call shape — at
minimum, distinguish: (a) timeout, (b) connection/service-unavailable, (c) malformed or
unexpected response shape. Extending `error_boundary.py` with a `ServiceUnavailableError` (or
reusing `RateLimitError` if he judges the "backpressure/unavailable" semantics close enough) is
his call to make, not mine to prescribe. Also flag and resolve the naming collision between
stdlib `concurrent.futures.TimeoutError` and `error_boundary.TimeoutError` — pick one canonical
name at each call site rather than leaving both in play.

**Acceptance criteria:**

1. No call site in `memory_vector_store.py` or `embedder_client.py` has a bare `except Exception`
   as its _only_ branch — typed cases come first; a final narrow catch-all is acceptable only as a
   last-resort fallback after them, per `error_boundary.py`'s own pattern.
2. The existing degrade-never-block guarantee is unchanged — this is diagnostic refinement, not a
   behavior change. All 26/26 `agent-memory` tests and the 180/181-passing context-engineering
   suite (§10.1) must still pass unmodified in their assertions about external behavior.
3. New unit tests in `harness-engineering/testing/` cover each new typed path (timeout,
   unavailable, malformed-response) at both the `memory_vector_store.py` and `embedder_client.py`
   call sites.
4. Once merged, this task closes EX-001 — the exception is revisited (§ condition 3) and the ASE
   verdict re-run against the fixed state.

**Out of scope:** changing `QDRANT_CALL_TIMEOUT_S`/the embedder-service's own timeout values, retry
counts, or the degrade contract itself — only the exception-handling granularity is in scope.

**Net effect on the embedder-service build's compliance verdict:** with this exception granted, the
build's verdict is **Conditional** (two Required-level gaps — PII scrubbing on the embed path,
merge-integration-agent designation — remain open with a tracked remediation plan). Without this
exception, the correct verdict per `compliance-standard.md`'s own criteria would be
**Non-Compliant**, since Conditional requires zero unmet Mandatory requirements — the build's own
self-report proposed "Conditional" without formally excepting the Mandatory-level finding it had
just disclosed; this addendum closes that gap in the paperwork, not in the underlying code.

#### Remediation closed — 2026-07-14

Kwame Asante's remediation task (scoped above) is complete and merged: commit `60156b46`
(`agent/kwame/ex001-typed-error-boundary`), merged `--no-ff` as `15724248` into
`core00/dev/engineering`. Verified independently by Dr. Vance, not taken on the report alone:

- Direct code read confirms every flagged call site (`ensure_collection`, `upsert_record`,
  `search`, `count_points`, `check_reachable` in `memory_vector_store.py`; `embed`,
  `probe_health`, `_probe_health_once` in `embedder_client.py`) now classifies timeout,
  connection/service-unavailable (new `ServiceUnavailableError`), and malformed-response before a
  narrow last-resort `except Exception` — no bare catch-all remains as the sole handler anywhere
  in scope.
- Both test suites independently re-run, not just trusted from the report:
  `context-engineering/testing/` — 180 passed, 1 failed (`test_acon_vs_context_compressor`,
  confirmed pre-existing and unrelated); `harness-engineering/testing/` — 57 passed (37 existing +
  20 new EX-001 tests), 4 failed (pre-existing `SafeModelCall` stub-kwarg bug, confirmed unrelated
  and untouched by this change). Both match the merge commit's claims exactly.
- Domain-mismatch judgment call (add `ServiceUnavailableError` rather than reuse `RateLimitError`)
  and the `TimeoutError` naming-collision resolution (keep `concurrent.futures.TimeoutError` as the
  one canonical name at every call site; do not import `error_boundary.TimeoutError` into either
  file) both reviewed and accepted as sound.

**Effect on the underlying gap:** the Mandatory-level finding this exception covered no longer
exists in the code — this is a genuine fix, not a re-labeling. EX-001 itself now documents closed,
historical rationale rather than an active exception.

**Effect on the embedder-service build's overall verdict:** remains **Conditional**, not upgraded
to ASE-Compliant — the two Required-level gaps (PII scrubbing on the embed path,
merge-integration-agent designation) are still open and unrelated to this remediation.

---

## Amendments

| Date       | Change                                                                             | Authority              |
| ---------- | ---------------------------------------------------------------------------------- | ---------------------- |
| 2026-04-28 | Initial ratification                                                               | Dr. Elias Vance, CC-00 |
| 2026-07-14 | Added Exceptions Log; recorded EX-001 (embedder-service ASE closeout)              | Dr. Elias Vance, CC-00 |
| 2026-07-14 | Closed EX-001 - typed error-boundary remediation merged and independently verified | Dr. Elias Vance, CC-00 |
