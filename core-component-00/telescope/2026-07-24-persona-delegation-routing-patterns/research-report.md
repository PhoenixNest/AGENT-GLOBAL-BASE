# Research Report — Persona Resolution & Delegation Routing: New CC-00 Prompt Engineering Patterns, Reference-Implemented in H-P01

---

## Metadata

| Field                | Value                                                                                         |
| -------------------- | --------------------------------------------------------------------------------------------- |
| **Investigation ID** | `2026-07-24-persona-delegation-routing-patterns`                                              |
| **Date Started**     | 2026-07-23                                                                                    |
| **Date Completed**   | 2026-07-24                                                                                    |
| **Status**           | Implemented — live-verified 2026-07-24; false-routing-rate instrumentation live, no data yet  |
| **Investigator**     | Dr. Elias Vance, Laboratory Director — Core Component 00                                      |
| **Laboratory**       | Core Component 00                                                                             |
| **Module(s)**        | Prompt Engineering (Layer 1) · Harness Engineering (Layer 3, hook mechanics) · ASE Governance |
| **Priority**         | High                                                                                          |
| **Requestor**        | CEO (relaying user feedback)                                                                  |

---

## Executive Summary

> This report formalizes two new CC-00 Prompt Engineering (Layer 1) patterns — Persona Resolution
> and Delegation Routing — that ground a request's persona or domain match in the workspace's
> existing Activation Protocols (`CLAUDE.md` §7, `crew/CLAUDE.md`) rather than free-form role-play
> or silent task handoff, with H-P01 specified as their first reference implementation (Layer 3).
> Resolving fallback ownership for the broad/uncategorizable case surfaced a governance defect in
> an earlier proposal to pair Dr. Vance with Dr. Mokoena: she leads Academic Neural Unit 00, an
> entity chartered as architecturally independent of CC-00, so a standing CC-00 routing default to
> her would recreate the "direct link" the CEO's own ANU-00 ruling prohibits. The corrected
> fallback is Dr. Vance paired with Dr. Amara Nwosu-Chen, CC-00's cross-cutting Staff Research
> Scientist.

---

## Investigation Scope

### What Was Investigated

> Whether CC-00 should formalize Persona Resolution and Delegation Routing as reusable Layer 1
> prompt-engineering patterns — grounding persona/domain matches in real agent identities rather
> than free-form role-play, and deciding whether a request should route to a single agent, a team
> of module/department leads, or a broad/uncategorizable fallback — with H-P01 (Layer 3) as their
> first reference implementation.

### Why This Investigation Was Needed

> The CEO relayed direct user feedback that the current optimizer does not recognize persona
> intent in user input, and separately asked whether H-P01 should gain domain-delegation logic
> built on the same framework. Both are Layer 1 (prompt architecture) design questions with a
> Layer 3 (harness/hook) implementation surface, and the specific fallback-ownership proposal
> touches an active organizational-boundary ruling (the ANU-00/CC-00 independence mandate), so
> this needed to be resolved with documentation review before any implementation, not assumed.

### Out of Scope

> - Actual code changes to `.claude/hooks/prompt-optimizer.ps1`, `prompt-gate-enforcer.ps1`, or
>   `prompt-gate-clear.ps1` — this report is the approval gate for that work, not the work itself.
> - Any decision to give ANU-00 a standing role in CC-00-facing infrastructure — flagged as an
>   open question requiring separate, explicit CEO direction if still desired.
> - Workspace-wide (cross-system: Company/Studio/CC-00/ANU-00) delegation routing — this
>   investigation is scoped to CC-00's own request handling.

---

## Research Questions

1. Can H-P01 make persona intent produce a genuinely persona-grounded response, not just a
   labeled one, without duplicating the existing Activation Protocol mechanism?
2. Should H-P01 gain a delegation-routing step that hands a request to a specific agent or team of
   module/department leads based on detected domain?
3. Who should own the "input too broad or uncategorizable" fallback case, and does the proposed
   Dr. Vance + Dr. Mokoena pairing hold up against workspace governance?

---

## Methodology

### Approach

> Three-part document review, conducted directly against primary sources rather than summary
> docs, per the workspace's document-precedence rule:
>
> 1. **Mechanism review** — read the live H-P01 implementation (`prompt-gate-enforcer.ps1`) and
>    the root `CLAUDE.md` §11 hook-resilience specification to establish what the gate actually
>    does today (a deterministic, heuristic PreToolUse block plus advisory `additionalContext`)
>    versus what requires model judgment.
> 2. **Compliance review** — checked the proposed persona requirement against
>    `agent-systems-engineering/governance/compliance-standard.md`'s Layer 1 "Role/persona
>    defined" Mandatory requirement.
> 3. **Governance/identity verification** — before accepting the CEO's proposed fallback pairing
>    at face value, searched the workspace for "Mokoena" and read the resulting profile
>    (`academic-neural-unit-00/crew/lead/naledi-mokoena/agent/profile.md`) and the ANU-00 boundary
>    statement (`academic-neural-unit-00/README.md`, `academic-neural-unit-00/CLAUDE.md`), then
>    read an internal alternative's profile (`core-component-00/crew/research-science/amara-nwosu-chen/agent/profile.md`)
>    for fit.

### Tools and Resources

> - Root `CLAUDE.md` (§7 Activating an Organizational Agent, §11 Hook Resilience)
> - `core-component-00/crew/CLAUDE.md` and `crew/README.md` (Activation Protocol, roster,
>   authority scope)
> - `core-component-00/engineering/prompt-engineering/CLAUDE.md` and
>   `patterns/advanced-patterns.md`
> - `agent-systems-engineering/governance/compliance-standard.md` (Layer 1 requirements)
> - `.claude/hooks/prompt-gate-enforcer.ps1` (live mechanism)
> - `academic-neural-unit-00/README.md`, `academic-neural-unit-00/CLAUDE.md`,
>   `academic-neural-unit-00/crew/lead/naledi-mokoena/agent/profile.md`
> - `core-component-00/crew/research-science/amara-nwosu-chen/agent/profile.md`

### Constraints

> - Document-review investigation only — no prototype implementation or live testing of a
>   modified hook was performed.
> - Persona/domain-detection accuracy (false-positive/false-negative rate of the heuristic) is
>   assessed qualitatively from the existing hook's design, not empirically benchmarked.

---

## Findings

### Finding 1: The persona dimension already exists in H-P01 but stops at labeling

**H-P01's five scored dimensions already include "role/persona context."** A prompt like "review
the auth module" is flagged and rewritten to "As the backend engineer, review...". But nothing
downstream forces that label to be grounded in a real, documented identity.

**Evidence:**

- `agent-systems-engineering/governance/compliance-standard.md` Layer 1: _"Role / persona
  defined — Mandatory... Vague role definitions ('You are a helpful assistant') do not satisfy
  this requirement."_
- The existing Activation Protocol (`CLAUDE.md` §7, `crew/CLAUDE.md`) already specifies the fix:
  read `profile.md`, read referenced `skills/*.md`, stay within documented authority — but nothing
  currently wires H-P01's confirmed prompt into that protocol automatically.

**Implications:**

- The user-reported gap ("role-play" instead of persona-consistent handling) is exactly this: a
  label without grounding. Closing it doesn't require new machinery, only connecting two systems
  that already exist.

---

### Finding 2: Detection must stay heuristic; resolution must stay with the model

**`prompt-gate-enforcer.ps1` is a deterministic PowerShell PreToolUse hook** — it reads the tool
call, checks a session-scoped pending-marker file, and denies non-`AskUserQuestion` tool calls
while that marker exists. It performs no semantic reasoning about prompt content; scoring and
rewriting happen in the advisory `additionalContext` step and in the model's own optimize pass.

**Evidence:**

- Full script logic reviewed line-by-line: marker check, 15-minute stale-marker fail-safe,
  `permissionDecision: deny` output — no NLU, no persona/domain classification of any kind.

**Implications:**

- A keyword-level hook can _trigger_ on a persona or domain cue ("as the CTO," "review the RAG
  pipeline") but cannot reliably _resolve_ it. That resolution — which real agent is meant, or
  whether one is meant at all — has to stay a model-judgment step, gated by the same
  negation-preservation and relevance-guardrail rules H-P01 already applies. This is a design
  constraint, not a gap to engineer around.

---

### Finding 3: The proposed Vance + Mokoena fallback breaches the ANU-00 independence ruling

**Dr. Naledi Mokoena is the Lead of Academic Neural Unit 00 (ANU-00), not CC-00 crew**, and ANU-00
was chartered by the CEO as architecturally independent of CC-00.

**Evidence:**

- `academic-neural-unit-00/README.md`: _"CC-00 and its Director, Dr. Elias Vance, hold no
  governing authority over ANU-00; their role is limited to incubation... not organizational
  ownership."_
- `academic-neural-unit-00/CLAUDE.md`: _"ANU-00 being tasked by CC-00, Dr. Vance, or the CEO to
  de-risk a specific item already on CC-00's roadmap, on request, recreates the 'direct link' the
  CEO's original ruling prohibits — decline or escalate to the CEO instead."_
- Dr. Mokoena's own profile records that she was specifically tested at interview for catching
  and rejecting exactly this class of dependency risk: _"she independently identified and pushed
  back on a scoping question that would have made ANU-00 operationally dependent on ongoing
  technical support from Core Component 00."_
- ANU-00's own stage-of-inquiry test (`academic-neural-unit-00/CLAUDE.md`) scopes her entity to
  pre-implementation research questions; an unrouted, uncategorizable prompt is neither a research
  question nor pre-implementation in nature, so there is no legitimate domain-match for her
  involvement even setting the boundary issue aside.

**Implications:**

- A standing hook default that routes CC-00's unclassified overflow to Dr. Mokoena, every time
  the heuristic misses, is not a one-off task request — it is the prohibited direct link, built
  into infrastructure rather than requested ad hoc. This should not ship as specified.

---

### Finding 4: Dr. Amara Nwosu-Chen is the correctly-shaped internal alternative

**Dr. Nwosu-Chen (Staff Research Scientist, CC-00) is cross-cutting across all four
production-grade modules and reports to Dr. Vance.**

**Evidence:**

- Her profile: _"Cross-Module Research Synthesis: Comfortable framing research questions that
  span more than one CC-00 module, rather than staying inside a single implementation's
  boundary."_
- `crew/CLAUDE.md` roster confirms her reporting line (`Dr. Vance`) and cross-cutting scope,
  distinct from the four module leads who each own a single domain.

**Implications:**

- Pairing Dr. Vance with Dr. Nwosu-Chen reproduces the CEO's intended shape — a senior generalist
  plus the Director catching what a single-module lead shouldn't own alone — without an
  organizational-boundary violation.

---

## Analysis

### Interpretation of Findings

> The two halves of the CEO's ask decompose cleanly. Persona-grounding (Finding 1) is a wiring
> problem: connect H-P01's existing persona dimension to the existing Activation Protocol instead
> of inventing new persona logic. Delegation routing (Finding 2) extends the same wiring pattern
> to task ownership, not just voice, and must respect the same detect-heuristically /
> resolve-with-judgment split the hook already uses. The fallback-ownership question (Findings 3–4)
> is not a design question at all — it is a governance-compliance question, and the proposed
> pairing does not pass. Both problems are more "connect what already exists correctly" than
> "build something new."

### Trade-offs Identified

| Option                                                              | Persona grounding                  | Governance risk                                | New machinery required                                      |
| ------------------------------------------------------------------- | ---------------------------------- | ---------------------------------------------- | ----------------------------------------------------------- |
| Status quo (label only, no delegation step)                         | Weak — vague per Layer 1 standard  | None                                           | None                                                        |
| Persona/delegation step, defers to existing protocols (recommended) | Strong — grounded in real profiles | Low, provided fallback is corrected            | Minimal — routing glue only                                 |
| Persona/delegation step, fallback = Vance + Mokoena (as proposed)   | Strong                             | **High — breaches ANU-00 independence ruling** | Minimal                                                     |
| Build a new, independent persona/routing engine                     | Strong                             | Low                                            | High — duplicates Activation Protocol, risks identity drift |

### Risks and Limitations

> - **Identity drift / impersonation:** an under-grounded rewrite could let a named agent's voice
>   be freehanded rather than sourced from their actual profile — the `canonical-source-of-truth`
>   ASE pattern exists to prevent exactly this.
> - **False routing on heuristic misses:** since detection stays keyword-level, "no confident
>   domain match" will sometimes be a misclassification, not a genuinely broad prompt. The
>   fallback pair should be framed and monitored as a low-confidence catch-all, not assumed rare.
> - **Cross-layer ownership ambiguity:** the persona/domain rubric is Layer 1 content (mine); the
>   hook mechanics that enforce it are Layer 3 (Kwame Asante, Harness Engineering). This pairing
>   is not yet reflected in `compliance-standard.md`'s Cross-Layer Integration table.
> - **Scope-creep re-litigation:** if the CEO's actual intent is a _workspace-wide_ fallback
>   (spanning Company/Studio/CC-00/ANU-00), that is materially bigger than what this report
>   approves and needs its own explicit decision — see Open Questions.

---

## Recommendations

### Primary Recommendation

> **Approve a two-tier deliverable.** Persona resolution and delegation routing are Layer 1
> prompt-engineering patterns in their own right — not a bespoke H-P01 feature — so they should be
> authored once, at the pattern level, and consumed by H-P01 as the first caller, not defined
> inside the hook.

**Tier 1 — Layer 1 (Prompt Engineering), mine to author:** add two new entries to
`engineering/prompt-engineering/patterns/advanced-patterns.md`, following the existing P-001–P-012
catalog format:

- **P-013 — Persona Resolution:** resolves a detected named-agent persona to its real `profile.md`
  via the existing Activation Protocols (`CLAUDE.md` §7, `crew/CLAUDE.md`, and the equivalent
  ANU-00/Studio/Company protocols) rather than freehanding voice or identity.
- **P-014 — Delegation Routing:** decides whether a request should be handled by a single agent, a
  team of module/department leads, or a broad/uncategorizable fallback, and surfaces the decision
  for confirmation rather than applying it silently.
  - Sets the broad/uncategorizable fallback to **Dr. Vance + Dr. Nwosu-Chen**, scoped to CC-00
    requests only. **Dr. Mokoena / ANU-00 must not be used as a standing fallback** under the
    current ANU-00 independence ruling.

**Tier 2 — Layer 3 (Harness Engineering), Kwame Asante's:** wire H-P01's existing step 1
(optimize) / step 2 (confirm) flow to consume P-013/P-014 — surfacing the proposed owner inside
the same `AskUserQuestion` confirmation already required for every H-P01 pass, so routing is
confirmed alongside the rewrite. H-P01 is the reference implementation; any future gate or
non-hook consumer can reuse the same pattern docs without re-deriving them.

### Secondary Recommendations

1. **Document the Prompt → Harness interface** in
   `agent-systems-engineering/governance/compliance-standard.md`'s Cross-Layer Integration table,
   since this feature makes that pairing load-bearing for the first time.
2. **Instrument false-routing rate** once shipped, before treating the fallback path as low-volume
   by assumption.
3. If a **workspace-wide** fallback (beyond CC-00) is still wanted, escalate that as its own
   explicit CEO decision rather than folding it into this approval.

### Implementation Priority

| Recommendation                                              | Priority | Effort       | Impact            |
| ----------------------------------------------------------- | -------- | ------------ | ----------------- |
| Persona-resolution sub-step (defers to Activation Protocol) | P0       | Small        | High              |
| Delegation-routing sub-step + confirmation surfacing        | P0       | Small–Medium | High              |
| Fallback correction (Vance + Nwosu-Chen, not Mokoena)       | P0       | Trivial      | High (governance) |
| Cross-Layer Integration table update                        | P1       | Trivial      | Medium            |
| False-routing-rate instrumentation                          | P1       | Small        | Medium            |

### Next Steps

1. ~~CEO approval of this report (gates all implementation work below).~~ **Done 2026-07-24.**
2. ~~**Owner: Dr. Elias Vance** — author P-013 (Persona Resolution) and P-014 (Delegation Routing)
   in `engineering/prompt-engineering/patterns/advanced-patterns.md`, and update
   `compliance-standard.md`'s Cross-Layer Integration table.~~ **Done 2026-07-24** — both patterns
   added to the catalog (v1.2), Cross-Layer table updated with a Prompt → Harness row.
3. ~~**Owner: Kwame Asante** (Harness Engineering lead) — implement the routing/confirmation glue
   in `.claude/hooks/prompt-optimizer.ps1` / `prompt-gate-enforcer.ps1` consuming P-013/P-014.~~
   **Done 2026-07-24** — added a `persona_and_delegation_resolution` rule to the gate's
   `additionalContext`, referencing P-013/P-014 directly; scoring logic (the heuristic trigger)
   left untouched per the design constraint that detection stays heuristic and resolution stays
   with the model.
4. **Owner: Connor O'Malley** (Senior Research Engineer II, Harness Engineering, reports to
   Asante) — false-routing-rate instrumentation. **Partially done 2026-07-24:** logging
   (`h-p01-telemetry.jsonl`: timestamp, score, persona/domain signal booleans, missing dimensions)
   is live in `prompt-optimizer.ps1`, best-effort and non-fatal to the gate. No data has
   accumulated yet — O'Malley's remaining work is the actual rate analysis once real sessions
   populate the log.
5. ~~**Owner: Dr. Vance + Kwame Asante jointly** — short live-verification pass.~~ **Done
   2026-07-24** — 3 synthetic prompts (named-agent/multi-domain, vague/low-score,
   already-high-scoring) run against the modified `prompt-optimizer.ps1` from outside the repo
   (avoids writing test state into the real session): valid JSON output in all 3, scoring/dimension
   logic unchanged, new rule text present and correctly worded in every case.

---

## References

### Internal Documentation

- `CLAUDE.md` (root) §7 Activating an Organizational Agent, §11 Hook Resilience
- `core-component-00/crew/CLAUDE.md`, `core-component-00/crew/README.md`
- `core-component-00/engineering/prompt-engineering/CLAUDE.md`,
  `patterns/advanced-patterns.md`
- `agent-systems-engineering/governance/compliance-standard.md`
- `.claude/hooks/prompt-optimizer.ps1`, `.claude/hooks/prompt-optimizer.sh`,
  `.claude/hooks/prompt-gate-enforcer.ps1`, `.claude/hooks/prompt-gate-clear.ps1`
- `academic-neural-unit-00/README.md`, `academic-neural-unit-00/CLAUDE.md`
- `academic-neural-unit-00/crew/lead/naledi-mokoena/agent/profile.md`
- `core-component-00/crew/research-science/amara-nwosu-chen/agent/profile.md`

### Related Work

- Formalized here per telescope archival convention, following an in-session opinion exchange
  with the CEO on persona-aware and delegation-aware prompt engineering design.

---

## Open Questions

1. **Does the CEO want workspace-wide (cross-system) fallback routing, not just CC-00-scoped?**
   - Status: Explicitly out of scope for this approval
   - Priority: Medium
   - Assigned: CEO decision required before any broader fallback is built

2. **What is the actual false-routing rate of a keyword-heuristic domain/persona detector in
   production?**
   - Status: Instrumentation live and collecting real data (`h-p01-telemetry.jsonl`) as of
     2026-07-24; rate analysis not yet performed
   - Priority: Medium
   - Assigned: Connor O'Malley — analysis once enough sessions have accumulated

---

## Version History

| Version | Date       | Author          | Changes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------- | ---------- | --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 2026-07-24 | Dr. Elias Vance | Initial report submitted for CEO approval, consolidated per CEO direction to remove in-session editing residue (superseded title/framing, version count)                                                                                                                                                                                                                                                                                                                                                                                                       |
| 1.1     | 2026-07-24 | Dr. Elias Vance | CEO approved implementation; Status updated to Approved, Next Steps assigned named owners (Vance, Asante, O'Malley) with sequencing                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 1.2     | 2026-07-24 | Dr. Elias Vance | Implementation executed: P-013/P-014 authored (`advanced-patterns.md` v1.2), Cross-Layer Integration table updated, H-P01 gate wired via a new rule in `prompt-optimizer.ps1`, false-routing-rate telemetry added, 3-case live-verification pass run clean. Status → Implemented. Instrumentation live but no data yet — Open Question 2 updated accordingly                                                                                                                                                                                                   |
| 1.3     | 2026-07-24 | Dr. Elias Vance | CEO code review: removed a revision-history-style code comment from `prompt-optimizer.ps1` in favor of a purpose-only comment; ported the same `persona_and_delegation_resolution` rule and telemetry logging into the pre-existing `prompt-optimizer.sh` bash mirror for parity (syntax- and live-tested via WSL bash from outside the repo). Pre-existing pass-path confirmation divergence between the `.ps1`/`.sh` variants noted but explicitly left unfixed — separate, already-flagged item. Telemetry log has since begun collecting real session data |

---

**Template Version:** 1.0
**Last Updated:** 2026-05-09
**Maintained By:** Core Component 00 Laboratory
**Authority:** AGENTS.md § 6. Core Component 00
