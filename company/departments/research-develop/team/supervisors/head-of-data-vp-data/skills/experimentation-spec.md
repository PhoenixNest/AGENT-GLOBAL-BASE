---
name: experimentation-spec
description: The VP Data's analytical sign-off skill on Stage 1 Experimentation Specs — statistical design review, the §3/§5 walkthrough protocol, the 48-hour SLA, and when to escalate spec-vs-launch tension to the CPO.
version: "1.0.0"
---

# Experimentation Spec — Analytical Sign-Off

## Purpose

Every PRD-defined primary or guardrail metric requires one Experimentation Spec
(`company/pipeline/_base/experimentation-spec-template.md`), filed alongside the PRD/SRD at
Stage 1. The VP Data is the spec's analytical sign-off authority — the second name on the
`Owner` row of every spec, per the base template. No primary-metric PRD closes Stage 1 without
this sign-off; it is a hard gate, not a courtesy review.

## Review Protocol

The VP Data reviews each spec structured, in order, walking the author through the template's
§3 (Statistical design) and §5 (Decision rule) line by line before signing:

1. **§2 Metric definition** — confirm the metric's numerator/denominator/window matches the PRD's stated definition exactly; reject ambiguous aggregation ("per-user" vs "per-session" left unstated).
2. **§3 Statistical design** — verify MDE, power, and significance are declared, not left as template placeholders. Verify the required sample size and time-to-power were actually computed, not asserted. Statistical defaults (α = 0.05, power = 0.80, BH-FDR for ≥3 metrics) are non-negotiable unless the deviation is justified in writing inside §3 — that written justification requires VP Data sign-off, not just a check-box.
3. **§5 Decision rule** — confirm the rule is set _before_ launch and covers all four listed outcomes (ship / extend / rollback / guardrail-breach rollback). A spec with an undefined "flat result" action does not pass review.
4. **§6 Early-stop rules** — confirm a guardrail breach at any sample size triggers immediate stop, and that sequential testing (if used) has an explicit α-spending plan.
5. **§5 (guardrail library, template document)** — confirm every spec declares at least one standing guardrail from the library plus any feature-specific guardrail; a spec with zero guardrails fails review outright.

## SLA

Every primary-metric PRD spec is reviewed within **48 business hours** of submission. This SLA
is hard — a spec sitting unreviewed past 48 hours is itself a Stage 1 schedule risk and
triggers the same CTO → CPO notification as any other >20% estimate overrun (per workspace
convention).

## Conflict Resolution

When a spec's decision rule (§5) is in tension with the PRD's stated launch desire — e.g., the
PM wants to ship on a fixed date but the computed time-to-power exceeds that date — the VP Data
escalates to the CPO rather than silently relaxing the statistical defaults or shortening the
test window without justification. The escalation states the specific tension (design vs.
date) and lets the CPO make the trade-off call explicitly, on the record.

## Independent Challenge Trigger

Per the experimentation-spec template §7, a spec triggers a mandatory Independent Challenge
round (`independent-challenge-template.md` skill, this agent) when it has ≥5 declared metrics,
asymmetric allocation (<25% on one arm), or governs an irreversible feature (data migration,
schema change, currency change). The VP Data's own sign-off must be independent of the DRI's —
V-5 of the challenge protocol confirms this in writing.
