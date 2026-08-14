# Log Entry [NN] — [Stage Name, e.g. "Discovery" / "Remediation" / "Incident & Revert"] — [YYYY-MM-DD]

<!-- Copy this file into a topic's log/ subfolder as log/NN-<slug>.md, numbered sequentially
     (01, 02, 03...) in the order stages/developments actually happened. Never edit or delete a
     prior entry when adding a new one — if a later entry contradicts an earlier claim, say so
     explicitly in the new entry instead of quietly rewriting the old one. Add a corresponding row
     to the topic's maintenance-record.md Pipeline Stage Log table (full path:
     core-component-00/maintenance-records/YYYY-MM-DD-<slug>/maintenance-record.md) and update its
     header Status field. -->

Part of `core-component-00/maintenance-records/YYYY-MM-DD-<slug>/maintenance-record.md`. Pipeline
stage [N — Stage Name] (`core-component-00/maintenance-records/pipeline.md`).

**Trigger:** [What made this development happen — a schedule, an incident, a CEO/user request, a
finding during a prior log/ entry's work. Link the prior entry if relevant.]

**State before:** [What state the system/resource was in immediately before this entry's actions
— version numbers, observed symptoms, configuration values, or "nominal, routine schedule" if
there was no issue.]

**Actions taken:**

1. [Action taken]
2. [Action taken]

**Verification:**

| Check performed                                                                         | Result                       |
| --------------------------------------------------------------------------------------- | ---------------------------- |
| [Specific check, e.g. `torch.cuda.is_available()`, pytest suite, health-check endpoint] | [Pass/Fail + observed value] |

<!-- Independent-review gate (pipeline.md stage 4): for any change touching a shared production
     resource other agents/sessions depend on, note here who reviewed this besides the person who
     executed it — self-verification alone is not sufficient for that class of change. -->

**Outcome:** [What changed as a result of this entry, in plain terms. Distinguish a fully closed
development from one with a genuine open item — don't let the two read the same way.]

**Handoff to next stage:** [What happens next — Close, or which pipeline stage this routes back
to if a new problem was found (see `core-component-00/maintenance-records/pipeline.md`'s Reopen
edge). If this entry closes the topic, say so and point to this topic's `maintenance-record.md`
Open Follow-Up Items for what (if anything) remains.]
