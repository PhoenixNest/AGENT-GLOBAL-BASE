---
name: incident-response
description: The VP Data's role inside the universal Stage 11 incident response model — analytical postmortem sign-off, weekly error-budget burn-rate co-review with VP Platform, and QBR co-leadership.
version: "1.0.0"
---

# Incident Response — Analytical Sign-Off

## Purpose

`company/pipeline/_base/incident-response.md` defines the universal Stage 11 incident model
(severity ladder, on-call rotation, authority delegation, blameless postmortem template, error
budget + QBR cadence). The VP Data is not an incident on-call surface owner — analytics
platform incidents route through VP Platform's on-call rotation like any other surface — but
the VP Data has two standing responsibilities inside that model.

## 1. Analytical Postmortem Sign-Off

Per the base model §6, every Sev1 and Sev2 postmortem is mandatory and blameless. The VP Data
owns the analytical sections of any postmortem where instrumentation health was a contributing
factor:

- Confirms whether a telemetry gap, logging pipeline failure, or dashboard staleness
  contributed to detection delay (postmortem §2 Timeline / §4 Contributing factors).
- Where instrumentation itself was the root cause (postmortem §3) — e.g., a broken event
  fired incorrect data that drove a bad rollout decision — the VP Data co-authors §3 with the
  incident's authoring engineers.
- Reviews action items (§8) tagged to the analytics platform for realistic target-close dates
  before the postmortem is filed.
- If the postmortem lists ≥5 action items, the mandatory Independent Challenge round
  (`independent-challenge-template.md` skill, this agent) applies before the postmortem closes.

## 2. Error Budget and QBR

Per the base model §7:

| Cadence              | VP Data's role                                                                                                                                                                                                            |
| :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Weekly               | Co-reviews burn-rate with VP Platform — VP Platform owns the review, VP Data supplies the analytics-platform-specific burn contribution and validates the underlying telemetry the burn-rate calculation is derived from. |
| End of quarter (QBR) | Co-leads the QBR readout with VP Platform, per `agent/profile.md` §1 mandate item 4.                                                                                                                                      |
| Overspend escalation | If an error-budget overspend traces to an analytics platform availability issue, VP Data is looped into the 24-hour VP Platform → CTO escalation.                                                                         |

## What This Skill Does Not Cover

This is not an on-call runbook — the VP Data is not paged for analytics platform incidents
under the standard on-call rotation table (base model §3). If analytics platform availability
becomes a standing on-call surface, that addition happens in the base model's §3 table
directly, not in this skill file.
