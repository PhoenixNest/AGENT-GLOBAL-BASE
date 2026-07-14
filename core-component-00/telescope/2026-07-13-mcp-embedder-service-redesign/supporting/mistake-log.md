# Mistake Log — 2026-07-13-mcp-embedder-service-redesign

> **Status of this document:** temporary. The workspace's _reflexion_ framework, which will
> formally capture errors and violations as part of a structured reflection process, is not yet
> operational. Until it is, errors and violations arising from this investigation are logged here
> directly. When reflexion is established, these entries are migrated into it and this file is
> superseded, not deleted.

---

## MISTAKE-001 — Progress-Tracking Files Not Created During Execution

| Field                    | Value                                                                                                                                                                        |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Classification**       | Process violation                                                                                                                                                            |
| **Date of violation**    | 2026-07-14 (spans the full build window)                                                                                                                                     |
| **Date logged**          | 2026-07-14                                                                                                                                                                   |
| **Logged by**            | Dr. Elias Vance, Laboratory Director                                                                                                                                         |
| **Requirement violated** | `.claude/rules/workspace-conventions.md` § Company Pipeline Progress Monitoring — `progress.md`, `session-log.md`, `checkpoint.json` required for active implementation work |

**What happened:** Dr. Vance decided, in writing, exactly where the required progress-tracking
files should live for this build (`implementation-plan.md` §6 — `supporting/implementation-tracking/`,
created once Phase 1 began). All six phases plus the EX-001 remediation task then executed and
merged in full — with zero tracking artifacts ever created. The CEO went looking for the required
documentation and found nothing. This is not an edge case or an oversight in a peripheral area; it
is a direct violation of a workspace requirement that Dr. Vance himself had already acknowledged in
writing before execution began.

**Root cause:** the orchestrator briefs issued to every worker agent in this build specified phase
gates, acceptance criteria, and git-worktree conventions in exacting detail — but never once
included tracking-file creation or maintenance as a deliverable. A location decision recorded in a
planning document is not an execution instruction. No one was ever told to do it, including Dr.
Vance himself, who did not do it either.

**Remediation:**

1. The three tracking files were compiled after the fact as the official record for this build
   (`supporting/implementation-tracking/`), verified against git commit history — not a
   substitute for the violation, a record of what happened despite it.
2. `core-component-00/multi-agent-engineering/fundamentals/git-worktree-orchestration.md` now
   documents this violation and a corrected rule: any orchestrator brief covering work subject to
   the progress-monitoring convention must include tracking-file creation as an explicit, checked
   deliverable in the first code-producing phase, with the orchestrator itself as the default owner
   if no worker agent is the obvious fit.

**Status:** Remediated. Logged here pending migration into the reflexion framework once
established.
