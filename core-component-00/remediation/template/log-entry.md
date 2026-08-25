# Log Entry [NN] — [Stage Name, e.g. "Drafting" / "Approval" / "Execution" / "Verification" / "Incident"] — [YYYY-MM-DD]

<!-- Copy this file into a topic's log/ subfolder as log/NN-<stage-slug>-<items>-<outcome>.md
     (e.g. 02-approval-i1-i5-approved.md, 03-hook-change-gate-i4-i5-granted.md) — see
     pipeline.md § Log File Naming. NN numbers sequentially (01, 02, 03...) in the order
     stages/developments actually happened; stage-slug, items, and outcome must let a reader
     judge this entry's content from a directory listing alone, without opening the file. Never
     edit or delete a prior entry when adding a new one — if a later entry contradicts an earlier
     claim, say so explicitly in the new entry instead of quietly rewriting the old one. Add a
     corresponding row to the topic's implementation-plan.md Gate Log table and update its header
     Status field. -->

Part of `core-component-00/remediation/.../implementation-plan.md`. Pipeline stage
[N — Stage Name] (`core-component-00/remediation/pipeline.md`).

**Trigger:** [What made this development happen — the plan's own prior stage, a Reviewer
decision, a User Hook-Change Gate grant, an incident found during execution.]

**Items covered:** [Which Included Items row ID(s) this entry concerns — one entry may cover one
item or several, but state explicitly which.]

**Actions taken:**

1. [Action taken]
2. [Action taken]

**Verification:**

| Check performed                                                                                             | Result                       |
| ----------------------------------------------------------------------------------------------------------- | ---------------------------- |
| [Specific check — e.g. `pytest engineering/harness-engineering/testing/ -v`, a live-execution reproduction] | [Pass/Fail + observed value] |

<!-- Independent-review gate (pipeline.md stage 4): mandatory for every item in this folder, no
     severity-based exception. Name who reviewed this besides the item's Owner. -->

**Outcome:** [What changed as a result of this entry, in plain terms.]

**Handoff to next stage:** [What happens next — the next pipeline stage, Close, or which stage
this routes back to if a new problem was found (see pipeline.md's Reopen edge).]
