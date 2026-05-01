# Stage Transition Summary — Game Studio

> **Purpose:** Mandatory summary artifact produced at every stage gate. Captures kill gate decisions, playtest metrics, and constraints carried forward.

**Game Title:** [Game Title]\
**Stage Completed:** [N] — [Stage Name]\
**Stage Advancing To:** [N+1] — [Stage Name] _(or "KILLED" if kill gate triggered)_\
**Completed:** YYYY-MM-DD\
**Produced By:** [Agent Name / Role]

---

## Gate Result

| Criterion                   | Result                                    |
| :-------------------------- | :---------------------------------------- |
| **Gate decision**           | ☐ Proceed / ☐ Iterate + Relaunch / ☐ Kill |
| **Kill gate triggered**     | ☐ Yes / ☐ No (N/A for non-kill stages)    |
| **Kill gate name**          | [Gate N — if applicable]                  |
| **P0/P1 defects remaining** | [N] (must be 0 to proceed)                |
| **P2/P3 deferred by CEO**   | [N]                                       |

---

## Kill Gate Metrics (Complete only for Gates 1–5)

| Metric           | Target  | Actual | Pass? |
| ---------------- | ------- | ------ | ----- |
| [D1 Retention]   | [≥ XX%] | [XX%]  | ☐ / ☐ |
| [D7 Retention]   | [≥ XX%] | [XX%]  | ☐ / ☐ |
| [LTV:CAC]        | [≥ X.X] | [X.X]  | ☐ / ☐ |
| [Playtest score] | [≥ X/5] | [X/5]  | ☐ / ☐ |

---

## Key Decisions Made

1. [Decision] — _Source: [GDD/PRD/SRD/Gate criteria]_
2. [Decision] — _Source: [reference]_

---

## Artifacts Produced

| Artifact | Version | Location | Key Content (2–3 sentences) |
| :------- | :------ | :------- | :-------------------------- |
| [Name]   | v[N]    | [path]   | [Summary]                   |

---

## Design Quality Gate Results (if Stage 5/6)

| Criterion               | Threshold   | Actual | Pass? |
| ----------------------- | ----------- | ------ | ----- |
| Game Feel Coherence     | GDS ≥ 90%   | —      | ☐ / ☐ |
| Visual Coherence Score  | ≥ 90%       | —      | ☐ / ☐ |
| Meta-UI IDS Conformance | ≥ 95%       | —      | ☐ / ☐ |
| Accessibility           | WCAG 2.1 AA | —      | ☐ / ☐ |

---

## Constraints Carried Forward

- [ ] [Constraint 1] — _Source: [PRD §X / GDD §Y / Gate criteria]_
- [ ] [Constraint 2] — _Source: [reference]_

---

## Open Questions / Risks for Next Stage

|  #  | Question or Risk | Impact         | Owner   | Action   |
| :-: | :--------------- | :------------- | :------ | :------- |
|  1  | [Question]       | [High/Med/Low] | [Agent] | [Action] |

---

## Kill Protocol (if gate triggered KILL decision)

| Step | Action                                 | Timeline                | Status |
| ---- | -------------------------------------- | ----------------------- | ------ |
| 1    | Freeze all production spend            | Immediate               | ☐ Done |
| 2    | Post-mortem scheduled                  | Within 5 business days  | ☐ Done |
| 3    | Asset archive completed                | Within 5 business days  | ☐ Done |
| 4    | Team reassignment plan issued          | Within 10 business days | ☐ Done |
| 5    | Portfolio tracker updated with lessons | Within 10 business days | ☐ Done |

---

## Context Handoff Checklist

> **CC-00 Compliance:** Layer 2 — Context Engineering (Required)
> Reference: `core-component-00/context-engineering/patterns/multi-agent-handoff.md`

### Handoff Tier Selection

Select the appropriate CC-00 handoff tier for the receiving agent:

| Scenario                                                             | Tier                    | Context Volume                                                                  |
| :------------------------------------------------------------------- | :---------------------- | :------------------------------------------------------------------------------ |
| Sequential stage handoff (same pipeline, next stage owner)           | **Scoped**              | 20–40% of prior context — key decisions, gate results, active constraints only  |
| New specialist crew member joining mid-stage                         | **Minimal**             | <10% — role brief, task objective, relevant kill gate criteria only (sanitised) |
| Studio Director reviewing all divisions / producing kill gate report | **Full**                | Up to 100% — complete stage history, all artifact summaries                     |
| Handoff to parent company (CSO, CTO, CPO)                            | **Minimal + sanitised** | <10% — studio-relevant facts only; no internal deliberation included            |

**Selected tier for this transition:** [ ] Full / [ ] Scoped / [ ] Minimal

### Completion Checklist

- [ ] All gate criteria for Stage [N] satisfied (or kill decision documented)
- [ ] All P0/P1 defects resolved before advancing
- [ ] Summary accurately reflects all key decisions (no omissions)
- [ ] All artifacts versioned and stored correctly under project folder
- [ ] Kill gate metrics recorded in `checkpoint.json`
- [ ] `progress.md` updated to reflect Stage [N+1] as current stage
- [ ] `session-log.md` entry completed for this stage's final session
- [ ] Handoff tier selected and context assembled accordingly (MVC filter applied)
- [ ] `constraints_forward` list populated in stage transition schema JSON
- [ ] Receiving crew member's MVC Profile consulted (only ✅ items included)
- [ ] This summary is self-contained for the selected handoff tier
- [ ] Token budget within 85% of model context window (if not, apply `context_compressor.py`)

---

**Signed by:** [Agent Name] on YYYY-MM-DD\
**Verified by:** [Studio Head / C-Suite] on YYYY-MM-DD
