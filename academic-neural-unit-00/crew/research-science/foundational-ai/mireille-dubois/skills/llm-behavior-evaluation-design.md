# Skill: LLM Behavior Evaluation Design

**Owner:** Dr. Mireille Dubois, Research Scientist (LLM Systems)
**Purpose:** Design rigorous, falsifiable evaluations of large-language-model capability and
behavior claims — the pre-implementation "does this actually hold up" question the stage-of-inquiry
charter test assigns to ANU-00.

---

## When to Use

Any chartered research programme (per `research-programme-chartering.md`) whose primary question
is whether a claimed LLM capability, behavior, or emergent property genuinely holds, rather than
how to build a system around it.

## Process

1. **State the capability claim precisely and its evaluation conditions.** "Model X can do Y" is
   not chartered until scoped to specific conditions, prompting setup, and what would count as the
   capability failing to hold.
2. **Distinguish emergent-capability claims from engineered-behavior claims.** A capability that
   appears without explicit design is a different research object than a behavior CC-00 might
   engineer via context or harness patterns — keep the two apart explicitly in every write-up.
3. **Design against anecdote, not for it.** A handful of impressive examples is not evidence;
   require a systematic evaluation set and report failure modes alongside successes.
4. **Apply the stage-of-inquiry boundary check.** If the finding leads naturally to "so we should
   build a reusable pattern for this," flag that as a referral to CC-00, not as ANU-00 scope
   creeping into implementation.
5. **File the knowledge-base entry** under the dated `YYYY-MM-DD-<slug>/research-report.md`
   convention.

## What This Skill Does Not Cover

- Training-time interventions or learning theory — route to Dr. Okonkwo.
- Broader applied-AI feasibility questions outside LLM-specific behavior — route to Dr. Tan.
