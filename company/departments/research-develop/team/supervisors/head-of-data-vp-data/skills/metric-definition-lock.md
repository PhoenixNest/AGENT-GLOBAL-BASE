---
name: metric-definition-lock
description: "IN FORMATION — provisional protocol for the Stage 3 metric-definition-lock gate the VP Data runs in parallel with the Technology Decision Lock. Documents what is settled and what is still open."
version: "0.1.0-draft"
---

# Metric Definition Lock — Provisional

> **Status: in formation.** This mirrors the status already declared in `agent/profile.md` §6
> ("`metric-definition-lock` (in formation)"). What follows is the settled scope and the open
> questions as of this document's publication — not a finished, binding protocol. Treat any
> gap below as "ask the VP Data / CTO before assuming," not as silent permission.

## Settled Scope

- **What locks.** PRD metric definitions (name, computation, aggregation window — the same
  fields captured in an Experimentation Spec's §2) are pinned at Stage 3, the same stage the
  Technology Decision Lock (`company/pipeline/CLAUDE.md`) freezes the ADRs and TSD.
- **Why it runs alongside the tech lock, not Stage 1.** A metric's _definition_ can still shift
  during Stage 1→3 as the PRD is refined; Stage 3 is chosen as the lock point because that is
  when the instrumentation architecture (which events, which service, which schema) itself
  locks via ADR — locking the metric definition at the same moment keeps the two in sync.
- **Revision discipline.** Once locked, a metric definition may only be revised through the
  same supersession discipline as an ADR: a new proposal, not a silent edit to the existing
  definition. This mirrors the Technology Decision Lock's "new ADR + full Stage 3 re-entry"
  rule.

## Open Questions (not yet resolved — do not assume an answer)

1. **Formal artifact.** Unlike the Experimentation Spec, there is no dedicated
   `metric-definition-lock-template.md` in `company/pipeline/_base/` yet. Until one exists, the
   lock is recorded as a dated note inside the relevant ADR's "Metrics" section — not a
   standalone document.
2. **Sign-off pairing.** Whether metric-definition lock requires the same two-party sign-off as
   the Technology Decision Lock (CTO + CIO) or is VP Data's unilateral call is undecided.
3. **Conflict with Experimentation Spec timing.** Experimentation Specs are authored at Stage 1
   and can name metrics before Stage 3 lock exists. The reconciliation process (does the spec's
   §2 metric definition automatically become the locked definition, or is it re-reviewed at
   Stage 3?) is not yet specified.
4. **Studio applicability.** Whether this gate applies to the Casual Games Studio's own
   pipeline (which has different stage numbering) or is Company-pipeline-only is undecided.

## What the VP Data Does Today, Pending Formalization

Until the above is resolved, the VP Data's practical Stage 3 responsibility is: review every
Stage 3 ADR that references a PRD metric, confirm the metric's definition text in the ADR
matches what was reviewed at Stage 1 Experimentation Spec sign-off (if a spec exists for that
metric), and flag any drift to the CTO before the ADR locks — rather than let an
inconsistency slip through Stage 3 unexamined.
