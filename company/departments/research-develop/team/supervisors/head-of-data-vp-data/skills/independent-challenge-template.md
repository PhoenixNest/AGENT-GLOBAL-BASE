---
name: independent-challenge-template
description: The VP Data's involvement in Independent Challenge rounds — primarily as the structurally-independent analytical sign-off for high-blast-radius Experimentation Specs, per the trigger conditions in the Stage 1 spec template.
version: "1.0.0"
---

# Independent Challenge — VP Data's Involvement

## Purpose

`company/pipeline/_base/independent-challenge-template.md` defines the universal five-attack-vector
challenge protocol invoked at multi-condition closure gates (Stages 6/8/10/11 per its own §2
table). The VP Data's involvement is narrower and comes from a different trigger: the
Experimentation Spec template's own challenge clause.

## The Trigger That Applies to VP Data

Per `_base/experimentation-spec-template.md` §7, a Stage 1 Experimentation Spec must pass an
Independent Challenge round before Stage 1 close when **any** of:

- The spec declares ≥5 metrics across primary + guardrails.
- The test allocation is asymmetric (one arm <25%).
- The feature is irreversible (data migration, schema change, currency change).

This is a Stage 1 trigger, distinct from the base template's own §2 table (which enumerates
Stage 6/8/10/11/plan-step gates and does not separately list Stage 1). The two documents
compose: the spec template supplies the _when_, the base template supplies the _how_ (the five
attack vectors, the 48-hour window, the report shape).

## The VP Data's Role

The VP Data is **not automatically the challenger** — per the base template §3, a challenger
must be structurally independent of the DRI cluster that authored the work, and the VP Data is
already the spec's analytical sign-off (§5 Owner row of the spec template), which is part of
the authoring/closure chain. Instead, the VP Data's standing responsibilities when a spec
triggers a challenge round are:

1. **Confirm the trigger fired.** Before Stage 1 close, verify whether any of the three
   conditions above are met and flag it to the CTO (who confirms challenger assignment per the
   base template §6) if the spec's author has not already done so.
2. **Supply evidence, not verdict.** The VP Data provides the statistical design artifacts
   (MDE calculation, guardrail library cross-check, sample-size derivation) the challenger
   needs to execute V-1 (Completeness) and V-2 (Sufficiency) — but does not sit on the
   challenge panel for a spec they signed.
3. **V-5 same-parties audit.** The VP Data's sign-off is explicitly named in V-5 (per
   `experimentation-spec.md` skill, this agent) — the challenger must confirm in writing that
   the VP Data's analytical sign-off was independent of the requesting DRI, not rubber-stamped.
4. **When VP Data _is_ eligible to challenge.** For challenges outside the VP Data's own
   specs — e.g., a Stage 11 postmortem challenge per the base template §3's Stage 11 row (VP
   Quality / VP Platform rotation) — VP Data is not a listed default challenger and is not
   assigned unless the CTO explicitly delegates it to avoid a same-parties conflict elsewhere.
