# Log Entry 03 — Execution — 2026-09-02 (recorded 2026-09-03)

Part of `core-component-00/platform/remediation/model-context-protocol-servers/2026-09-02-mcp-servers-enterprise-assessment-remediation/implementation-plan.md`.
Pipeline stage 3 — Execution (`core-component-00/platform/remediation/pipeline.md`).

**Trigger:** `log/02-approval-i1-i5-approved.md` approved the Approach for all five items. Ravi
executed this stage on 2026-09-02; this entry documents that execution as part of the plan's
record.

**Items covered:** I1, I2, I3, I4, I5.

**Actions taken:**

1. **I2** — `e7e8c33c` (00:37, 2026-09-02): added `_embedder_service_state_confirmed_at`, updated
   at both real probe sites; `_get_search_capability_snapshot()` now reports it.
   `agent-memory/server.py` +45, `tests/conftest.py` +9, `tests/test_server.py` +55.
2. **I1** — `baa55fd7` (00:39): added `tests/test_search_tier_degradation.py` (+444 lines),
   closing the "zero regression coverage" gap. Running the new suite exposed two real defects,
   fixed the same session:
   - `1d0b5ac9` (02:25): a query-time Qdrant failure now demotes to `HYBRID` (local FAISS) before
     falling to `BM25`, instead of skipping it.
   - `ff1de71a` (02:25): a cooldown-gated single-tier reprobe climbs a demoted tier back toward
     `_max_tier` once the dependency recovers, instead of staying demoted indefinitely.
   - `a5250bb0` (02:26): merge of the above into `core00/dev/engineering`
     (`agent/infrastructure/workspace-knowledge-tier-fixes`) — `workspace-knowledge/server.py`
     +143, `tests/test_search_tier_degradation.py` extended to 356 net lines covering the new
     behavior.
3. **I3** — `39063cd4` (00:45): added `pii_redaction.py` (`redact_pii()`, +88 lines) and wired it
   into `write_tool.py` (+19 lines) immediately after input validation, before the embed call;
   added `tests/test_pii_redaction.py` (+134) and extended `tests/test_write_memory.py` (+145,
   `TestPiiRedactionBeforeEmbed`).
4. **I5** — `1a3ab2f0` (00:50): added `tests/test_tool_conformance.py` (+200), registering
   `search_memory`, `health_check`, and `write_memory` into a scratch FastMCP instance to validate
   declared input schema against actual signature.
5. **I4** — `79d924e0` (02:02, `agent-memory`) and `310b5a3e` (02:02, `workspace-knowledge`):
   added a module-level `logging.getLogger(__name__)` reading `FASTMCP_LOG_LEVEL` in each server,
   plus a decorator recording `tool_name`/`duration_ms`/ok-or-error outcome on every registered
   tool, with argument summarizers logging lengths and identifiers only — never raw query or
   content text. `agent-memory/server.py` +195, `tests/test_structured_logging.py` +273;
   `workspace-knowledge/server.py` +189, `tests/test_structured_logging.py` +241. `79d924e0` also
   fixed a brittle text-boundary anchor in `test_read_constraints_reverification.py` (made
   decorator-count-agnostic) so the pre-existing write-path-isolation invariant test would keep
   passing after `search_memory` gained a decorator.

**Verification:**

| Check performed                                                                   | Result                                                      |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `git log` cross-reference, each commit message against its cited Benchmark Row ID | All five commit messages explicitly cite the row they close |

Test execution itself is Stage 4's responsibility, not restated here.

**Outcome:** All five items' code changes are present on `core00/dev/engineering` as of
2026-09-02. `Status: Executed, pending verification`.

**Handoff to next stage:** Stage 4 — Verification, independent of the executing Owner. See
`log/04-verification-i1-i5-verified.md`.
