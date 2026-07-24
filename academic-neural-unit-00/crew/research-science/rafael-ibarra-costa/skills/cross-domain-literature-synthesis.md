# Skill: Cross-Domain Literature Synthesis

**Owner:** Dr. Rafael Ibarra-Costa, Research Scientist (Generalist)
**Purpose:** Synthesize literature that spans more than one of ANU-00's four charter fields
(computer science, AI, neural networks, software engineering) into a single coherent
knowledge-base entry, rather than forcing a cross-cutting question into one narrow specialty's
silo.

---

## When to Use

Any chartered research programme (per `research-programme-chartering.md`) whose question
genuinely spans two or more charter fields — e.g., "how does neural architecture choice affect
software maintainability of the surrounding codebase" spans neural networks and software
engineering.

## Process

1. **Decompose by field.** Identify which sub-claims of the research question belong to each
   field involved. Do not synthesize before decomposing — a merged claim that silently conflates
   two fields' evidence standards is a common failure mode.
2. **Source per field at that field's own rigor bar.** Neural-network claims need the same
   evidentiary standard a neural-network specialist would apply; software-engineering claims need
   the same standard a software-engineering specialist would apply. Do not lower the bar for the
   field outside your primary depth.
3. **Escalate depth gaps.** If a sub-claim requires depth beyond generalist level, route it to the
   relevant domain specialist (Dr. Baek for neural networks/AI, Dr. Roldán for software
   engineering/CS) for review before publishing, rather than publishing a shallow treatment.
4. **Synthesize the cross-cutting claim.** Only after each field's sub-claims are independently
   sound, state the combined finding and its cross-field implication explicitly — this is the
   value a generalist adds that a single-field specialist cannot.
5. **File the knowledge-base entry** under the dated `YYYY-MM-DD-<slug>/research-report.md`
   convention, tagged with all charter fields it touches so it surfaces under any relevant future
   taxonomy lookup.

## What This Skill Does Not Cover

- Single-field-depth research within one charter field alone — that follows the relevant
  specialist's own research-design skill.
- Knowledge-base ingestion/indexing mechanics — that is the Knowledge Systems Engineer's mandate.
