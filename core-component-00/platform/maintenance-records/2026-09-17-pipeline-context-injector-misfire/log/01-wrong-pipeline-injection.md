# Log Entry 01 — Wrong Pipeline Injected on Every Qualifying Prompt

**Topic:** H-P02 Pipeline Context Injector
**Stages covered:** 1 Investigation · 2 Approval · 3 Execution · 4 Verification
**Date:** 2026-09-17
**Author:** Dr. Elias Vance, CC-00 Laboratory Director

---

## 1. Investigation

The H-P02 hook injects a pipeline-stage reference into the prompt when it detects a stage signal.
Over one working session it fired incorrectly three times:

| Occurrence | Prompt subject                                               | Injected                                                                          |
| ---------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| 1          | Recruitment pipeline Stage 8, the Hiring Outcome Report gate | Development pipeline Stage 8 — Integrity Verification, with the Trim-to-Pass rule |
| 2          | The same, in a commit-message question                       | The same                                                                          |
| 3          | Delegation of decision-making authority                      | Stage 10 — Release                                                                |

Two distinct defects account for these.

### Defect A — a regular expression missing a leading word boundary

The Stage 10 pattern read:

```
(Stage 10\b|release\b|deploy\b|ship\b|launch\b|go.no.go|store submission|production deploy)
```

`ship\b` has a trailing boundary and no leading one, so it matches any word **ending** in "ship".
Verified directly against the prompt text that triggered occurrence 3:

```
"full ownership and decision-making authority"  ->  matched 'ship' at index 10
"leadership signal"                             ->  matched 'ship' at index 6
"the relationship between"                      ->  matched 'ship' at index 12
```

This workspace scores **Leadership Signal** as a named vetting dimension in every candidate record
and uses "ownership" throughout its governance documents. The pattern therefore fires on ordinary
prose, silently, and had been doing so since the hook was written.

### Defect B — a bare stage number treated as unambiguous

Three pipelines here number their stages independently: Company development (13 stages),
Recruitment (9) and the Casual Games Studio (11). `STAGE_SIGNALS` matched a bare `Stage 8\b` and
resolved it to the development pipeline unconditionally. `PIPELINE_RELATIVE_PATHS` lists only the
four development pipelines, so even the documents it pointed at were the wrong ones.

The result is that the hook performed, automatically and on every qualifying prompt, precisely the
conflation `CLAUDE.md` § 8 forbids: _"Three distinct pipelines exist — do not conflate their stage
numbers."_

## 2. Approval

Directed by the CEO under delegated authority to resolve root causes rather than symptoms. Hook
behaviour affects every pipeline in the workspace, which places it outside the Infrastructure
Engineer's unilateral scope per `crew/CLAUDE.md` § Authority Scope.

## 3. Execution

Three changes to `.claude/hooks/pipeline-context-injector.py`:

1. **Anchored the Stage 10 keywords** — `\brelease\b`, `\bdeploy\b`, `\bship\b`, `\blaunch\b`,
   `\bgo.no.go\b`.
2. **Added `FOREIGN_PIPELINE_SIGNALS`** — where the prompt names a recruitment or studio subject,
   the hook logs `suppressed_foreign_pipeline` and stays silent rather than guess which pipeline a
   stage number belongs to.
3. **Added an ambiguity path** — where a match rests on the stage number alone, with none of the
   pattern's subject keywords present, the hook injects a note naming all three pipelines and their
   stage counts instead of asserting one. Detection strips the `Stage N\b` alternative from the
   pattern and re-tests; if nothing else matches, the signal was the number alone.

The hook now has three outcomes where it had two: inject, stay silent, or say it cannot tell.

## 4. Verification

`ast.parse` confirms the file parses. Behaviour checked by loading the module and running the
detection logic against seven cases:

| Case                                                 | Before               | After                |
| ---------------------------------------------------- | -------------------- | -------------------- |
| "Stage 8 approved with conditions" (recruitment)     | Dev Stage 8 asserted | Ambiguity note       |
| "commit message of Stage 8" (recruitment)            | Dev Stage 8 asserted | Ambiguity note       |
| "full ownership and decision-making authority"       | Stage 10 — Release   | Nothing injected     |
| "ADR and lock the tech stack"                        | Stage 3              | Stage 3 — unchanged  |
| "ship the release to production"                     | Stage 10             | Stage 10 — unchanged |
| "Stage 6 code review of the payment module"          | Stage 6              | Stage 6 — unchanged  |
| "recruitment pipeline Stage 8 hiring outcome report" | Dev Stage 8 asserted | Suppressed           |

All three observed misfires produce corrected behaviour; all four true positives are preserved.

## 5. Open Items Carried Forward

Two, both recorded in the topic's `maintenance-record.md`: the hook has no test file, so this
verification is not held anywhere a regression would fail it; and the remaining `STAGE_SIGNALS`
patterns were not audited for the same missing-boundary defect beyond Stage 10.
