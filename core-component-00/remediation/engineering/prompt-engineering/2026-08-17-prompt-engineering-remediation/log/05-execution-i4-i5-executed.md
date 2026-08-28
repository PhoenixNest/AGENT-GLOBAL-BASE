# Log Entry 05 — Execution — 2026-08-24

Part of `core-component-00/remediation/engineering/prompt-engineering/2026-08-17-prompt-engineering-remediation/implementation-plan.md`.
Pipeline stage 3 — Execution (`core-component-00/remediation/pipeline.md`).

**Trigger:** Stage 2 Approval complete for I4 and I5 (`log/02-approval-i1-i5-approved.md`); User
instruction to execute the approved plan. Executed together because both are doc-only changes to
`fundamentals/research.md`.

**Items covered:** I4, I5.

**Actions taken (I4):**

1. Added new § 3.7 "Prompt Injection Defense (Structural, Not Prompt-Level)" to
   `fundamentals/research.md`, immediately after § 3.6 (no renumbering of existing sections —
   inserted at the end of § 3 rather than between numbered top-level sections, since § 3.4 is
   cross-referenced by number from I5's own change below and from the new catalog entry).
2. Grounded the section in the benchmark's external sources: stated plainly, in wording matching
   the sourced excerpt, that a system prompt telling the model to ignore untrusted-content
   instructions is **not** a security control, and that no single defense prevents all indirect
   prompt injection.
3. Covered the four-part defense-in-depth composition from the same source: provenance tracking
   and structural separation of untrusted content, capability scoping, deterministic policy
   enforced outside the model (naming CaMeL/FIDES as the architectural-pattern examples the source
   names), and egress constraints.
4. Added an explicit "Relationship to this module's scope" note: Layer 1 can only specify the
   prompt-level half (delimiting/labeling untrusted content, § 3.5) — capability scoping,
   out-of-model policy enforcement, and egress constraints are CC-00 Layer 3+ concerns, not
   something this doc-only module can implement. This prevents the section from reading as a
   complete implementation when it is guidance for one layer of a multi-layer control.

**Actions taken (I5):**

1. Retitled and rewrote § 3.4 from "Structured Output Prompting" to "Structured Output:
   Constrained Decoding (Primary) vs. Prompt-Level Instruction (Fallback)".
2. Led with constrained decoding: stated that every major provider now offers a mode constraining
   token sampling itself to a schema (schema-invalid output cannot be emitted), that prompt-only
   JSON is a legacy pattern, and that this should be the default whenever the target
   model/provider supports it.
3. Demoted the prior prompt-level instruction content to an explicit "Fallback" subsection, scoped
   to when constrained decoding is unavailable or the schema is too dynamic/complex for the
   provider's constraint mechanism — kept the original JSON example and best-practices list there,
   adding a note that prompt-level output must still be validated programmatically.
4. Added catalog entry P-015 ("Constrained-Decoding Request") to
   `patterns/advanced-patterns.md`'s Pattern Catalog table, Pattern Selection Guide table, and as a
   full pattern section with its own template — linked back to `research.md` § 3.4 and vice versa,
   satisfying the plan's "discoverable from `patterns/advanced-patterns.md`" requirement.

**Verification:**

| Check performed                                                                                                                                                | Result                                                                                                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Re-read `research.md` § 3.4 and § 3.7 after edit for internal consistency (fallback content preserved, not duplicated)                                         | Pass — original JSON example and best-practices list intact under "Fallback," no duplicated content      |
| Grep `research.md` for "not a security control" and "No single defense"                                                                                        | Pass — both present in § 3.7, matching the benchmark's sourced excerpts (S16, S17)                       |
| Grep `advanced-patterns.md` for "P-015"                                                                                                                        | Pass — present in the catalog table, the Pattern Selection Guide table, and its own `### P-015:` section |
| Confirmed § 3.4's cross-reference to `patterns/advanced-patterns.md` and P-015's cross-reference to `research.md` § 3.4 both resolve to real, existing anchors | Pass — both files exist at the referenced paths; section/entry both present                              |
| Confirmed no other section's numbering shifted (§ 4 "Prompt Optimization Framework" still immediately follows § 3, now via the new § 3.7 rather than § 3.6)    | Pass — sections 4–10 unchanged; only new § 3.7 inserted                                                  |

**Outcome:** I4 — the module's documentation-coverage table already claims "Prompt robustness —
handling adversarial inputs" (`CLAUDE.md`); § 3.7 now backs that claim with real injection-defense
content instead of the two one-line mentions the benchmark found. I5 — structured-output guidance
now leads with constrained decoding as the primary, provider-enforced mechanism and treats
prompt-level instruction as the explicitly scoped fallback it actually is, with a discoverable
catalog entry.

**Note on Owner-≠-Reviewer for I4:** per the plan's per-item reviewer exception, I4's Approach was
reviewed by Dr. Vance (not Wieczorek, who owns I4) at Stage 2. This entry executes I4's Approach;
per `pipeline.md` stage 4, Verification for I4 still requires Dr. Vance's independent review of the
executed section for excerpt-to-claim accuracy, distinct from this Execution-stage entry.

**Handoff to next stage:** Stage 4 — Verification, alongside I1–I3. Owner has not marked this
`Verified` — that requires independent Reviewer sign-off (Wieczorek for I5; Vance for I4 per the
per-item exception).
