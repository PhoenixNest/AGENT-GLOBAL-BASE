# Skill: Agent Coordination Theory Research

**Owner:** Dr. Kaito Fujimori, Research Scientist (Agent Systems Research)
**Purpose:** Design falsifiable research questions about emergent multi-agent coordination
behavior, with an explicit, checked-every-time boundary against Core Component 00's
`multi-agent-engineering/` orchestration-implementation mandate.

---

## When to Use

Any chartered research programme (per `research-programme-chartering.md`) whose primary question
is whether or under what conditions a coordination pattern emerges among agents — not how to
implement, orchestrate, or ship one.

## Process

1. **State the emergence question and its conditions.** "Does coordination pattern X emerge" is
   not chartered until scoped to a specific agent population, environment, and observation
   criteria.
2. **Boundary-check against CC-00 explicitly, every time, by name.** Before starting, state in one
   sentence why this question is theoretical/investigative and not a reusable implementation
   pattern — and check it specifically against `core-component-00/engineering/multi-agent-engineering/`
   and Dr. Farouk's mandate, not just against "production engineering" abstractly. This role exists
   because that specific boundary is the one most likely to blur; treat the check as mandatory, not
   optional, given this role's own vetting record flagged it as the central risk.
3. **Study behavior, don't build tooling to study it.** If answering the question requires
   building reusable orchestration infrastructure, that infrastructure need is a referral to CC-00,
   not an ANU-00 deliverable — a one-off simulation harness to observe behavior is fine; a reusable
   framework is not.
4. **Report emergence conditions, not just the phenomenon.** "Coordination emerges" is incomplete
   without stating under what conditions it does not.
5. **File the knowledge-base entry** under the dated `YYYY-MM-DD-<slug>/research-report.md`
   convention.

## What This Skill Does Not Cover

- Any implementation of orchestration patterns, swarm topology tooling, or context-handoff
  protocols — that is CC-00's `multi-agent-engineering/` mandate entirely, not a shared boundary.
- LLM-specific or applied-AI-specific research questions — route to Dr. Dubois or Dr. Tan.
