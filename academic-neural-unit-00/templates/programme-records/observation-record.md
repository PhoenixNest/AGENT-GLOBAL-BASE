# Observation Record — [Short Title of What Was Observed]

<!-- Copy to academic-neural-unit-00/knowledge-base/YYYY-MM-DD-<slug>/observations/<short-slug>.md,
     alongside the programme that produced it. One file per distinct observation.

     WHAT THIS DOCUMENT IS: the raw, reproducible record of something that happened during research
     — a run that behaved unexpectedly, a configuration that failed, an example worth keeping. It
     exists so a second researcher can reproduce the same thing from this file alone, without asking
     the first one what they ran.

     WHAT IT IS NOT: a finding, and not a task. An observation becomes a finding only through the
     research report's §4 claim register, and only with the evidence standard that register demands.
     An unresolved observation is parked in open-question-log.md, never assigned to anyone. Nobody
     is ever handed an observation record as work — filing one creates no obligation on any ANU-00
     member, and no field here accepts an assignment from outside ANU-00.

     Point-in-time record. A later, different observation is a new file with a cross-reference —
     never an edit to this one. Editing a filed observation destroys the reproducibility it exists
     to provide. -->

**Observation ID:** [OBS-NN — unique within this programme]
**Recorded:** [YYYY-MM-DD]
**Recorded by:** [Name, ANU-00 role]
**Programme:** [`YYYY-MM-DD-<slug>`]
**Disposition:** [Open / Feeds claim C# / Parked as OQ-NN / Discarded — environmental. See §5]

---

## 1. What Was Observed

<!-- One paragraph, factual. Describe what happened, not what you think it means — interpretation
     belongs in the research report, behind the claim register's evidence standards. An observation
     that can only be stated as a conclusion has already skipped the step this document exists for. -->

**Expected:** [What the run, evaluation, or analysis was expected to produce.]

**Actual:** [What it produced instead. Quote or attach the actual output where practical — a
paraphrase of an error is not reproducible.]

---

## 2. Exact Conditions

<!-- The reproducibility core. A reader who has never seen this programme must be able to recreate
     the setup from this section alone. "Same as usual" and "the standard config" are not entries;
     they are the reason a reproduction attempt fails six months later. -->

| Field                      | Value                                                                          |
| -------------------------- | ------------------------------------------------------------------------------ |
| Inputs / configuration     | [Exact values. Prompts verbatim, parameters with their settings, data slice]   |
| Model / system under study | [Name and version identifier, if applicable]                                   |
| Environment                | [Runtime, library versions, hardware — whatever materially affects the result] |
| Date and time of run       | [YYYY-MM-DD, and time if the behavior may be time- or service-dependent]       |
| Scale                      | [Number of runs, size of the evaluation set, population — see §3]              |

<!-- For LLM-behavior observations specifically, the prompting setup is part of the conditions, not
     an incidental detail — llm-behavior-evaluation-design.md §1 requires the conditions and
     prompting setup be stated for a capability claim to be scoped at all. Record them here so the
     eventual claim inherits them rather than reconstructing them from memory. -->

---

## 3. Reproduction

<!-- The single most important section, and the one that decides whether this observation can ever
     support a claim. dubois §3 is explicit that a handful of impressive examples is not evidence —
     the reproduction rate below is what separates a systematic observation from an anecdote.
     Record the rate honestly, including 1-of-1: a one-off is a legitimate record, it is simply not
     yet evidence, and §5 will route it accordingly. -->

**Steps to reproduce:**

1. [Step]
2. [Step]

**Reproduction rate:** [N of M attempts] — [If M = 1, say so plainly. Do not describe a single
occurrence as a pattern.]

**Conditions under which it did NOT occur:** [Which variations were tried and did not reproduce it.
This is the same discipline `agent-coordination-theory-research.md` §4 requires of emergence
findings — the boundary of a phenomenon is part of the phenomenon, and it is far cheaper to record
here, while the setup is still live, than to reconstruct later.]

---

## 4. Tooling Used

<!-- agent-coordination-theory-research.md §3: a one-off harness built to observe behavior is fine;
     a reusable framework is not an ANU-00 deliverable. Recording this here keeps instrumentation
     honest — a "temporary" harness that three observations depend on has become a tool, and the
     boundary check should catch that here rather than after it is maintained. -->

- [ ] No instrumentation beyond one-off, non-reusable scripting.
- [ ] Instrumentation is being reused across observations → check whether it has become reusable
      infrastructure. If so, file `referral-note.md` and state the path here: [`../referrals/...`]

---

## 5. Disposition

<!-- Every observation ends in exactly one of these. An observation left permanently "Open" is a
     bookkeeping failure — it is either evidence, a question, or environmental noise. Decide, and
     record which. -->

| Outcome                         | When it applies                                                                       | Where it goes next                                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **Feeds a claim**               | Reproduces reliably enough to serve as evidence at the claim's declared evidence type | Cited from `research-report.md` §4, row C# — record it there                                              |
| **Parked as an open question**  | Interesting, but has no falsifiability condition yet — so it cannot be chartered      | New row in `knowledge-base/open-question-log.md`, per `research-programme-chartering.md` §2               |
| **Supports a negative finding** | Shows where the hypothesis fails or a technique does not hold                         | `research-report.md` §6.2 — a complete finding, not a shortfall (`applied-ai-feasibility-research.md` §4) |
| **Discarded as environmental**  | Traced to the setup rather than the object of study                                   | Recorded here and closed. **Keep the file** — knowing something was ruled out is itself reusable          |

**Decision:** [Which of the above, and the one-sentence reason.]
**Decided by:** [Name] — [YYYY-MM-DD]

<!-- Discarding is a legitimate, common, and valuable outcome. Do not delete a discarded
     observation and do not pad one to look more significant than it was — both corrupt the record
     the next researcher relies on. -->

---

## 6. Cross-References

| Direction       | Target                                 | Relationship                                   |
| --------------- | -------------------------------------- | ---------------------------------------------- |
| This relates to | [OBS-NN / `YYYY-MM-DD-<slug>` / OQ-NN] | [Same phenomenon / Contradicts / Follows from] |

<!-- If this observation relates to an entry in another programme, record the reciprocal link there
     in the same sitting — knowledge-base-ingestion-architecture.md §3 makes bidirectional
     cross-referencing an ingestion-time obligation, not a later cleanup pass. -->
