---
name: pipeline
description: Universal 13-stage company development pipeline familiarity for the VP Data / Head of Analytics role — stage-by-stage touchpoints, sign-off checkpoints, and escalation paths across Stages 1, 3, 4, 5, 7, 9.5, and 11.
version: "1.0.0"
---

# Pipeline Familiarity — VP Data

## Purpose

Every agent operating inside a company development pipeline must know the full 13-stage
skeleton (`company/pipeline/_base/pipeline.md`, specialized per product type in
`company/pipeline/<type>/pipeline.md`) well enough to know when their sign-off is required,
what artifact they are signing, and who to escalate to when a gate is at risk. This skill is
the VP Data's baseline pipeline literacy — the stage-ownership table in `agent/profile.md` §5
is the canonical source; this document explains the "why" behind each touchpoint.

## Stage Touchpoints

| Stage     | What ships                          | VP Data's role                                                                                                                                                            |
| :-------- | :---------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Stage 1   | PRD + SRD + Experimentation Spec(s) | Analytical sign-off on every primary/guardrail Experimentation Spec (see `experimentation-spec.md`). Hard gate — Stage 1 does not close without it.                       |
| Stage 3   | UML Engineering Package + ADRs      | Reviews ADRs governing telemetry / feature-flag service architecture; co-signs with CTO. Runs the parallel metric-definition-lock gate (see `metric-definition-lock.md`). |
| Stage 4   | Implementation Plan + Gantt         | Confirms instrumentation and dashboard-wiring tasks are scoped in the plan.                                                                                               |
| Stage 5   | Software Development                | No formal sign-off; monitors instrumentation implementation progress ahead of Stage 9.5.                                                                                  |
| Stage 7   | Automated Testing                   | Co-reviews test cases that exercise telemetry firing (spec's events fire correctly under both arms).                                                                      |
| Stage 9.5 | Internal Dogfood                    | Reviews dogfood telemetry stream health; signs the Dogfood Telemetry Report §1 Telemetry Summary.                                                                         |
| Stage 11  | Live Operations (continuous)        | Owns analytical side of error budget burn-rate computation; co-leads QBRs with VP Platform; analytical postmortem sign-off (see `incident-response.md`).                  |

## Escalation Paths

- **Spec vs. launch-desire tension** (a spec's decision rule conflicts with the PRD's stated launch date) → escalate to CPO. Do not silently relax statistical defaults to unblock a launch.
- **Stage 3 ADR touching telemetry/flag architecture** → co-sign with CTO; if disagreement, the ADR does not lock until resolved.
- **Metric definition dispute post-Stage-3-lock** → route through the same supersession discipline as ADRs (new proposal, not a silent edit).

## Non-Negotiables Inherited From the Base Pipeline

- Stages marked ✅ in the pipeline table are hard stops — present the deliverable and wait for sign-off; never auto-advance.
- P0/P1 defect classification cannot be downgraded by any agent, including VP Data, to protect an analytics platform SLA.
- Stage 6 remediation restarts the full review panel — this applies to any architecture review touching the analytics platform's own services.
