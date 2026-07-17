# Supporting Document 04 — Reflection Record Authoring Template

**Programme:** `2026-07-14-reflexion-memory-system`
**Purpose:** The canonical Investigator-Authored Write Path authoring template (`01-technical-options.md` §4) — the literal
artifact a named investigator fills out by hand before the write-through helper script constructs
and validates a `ReflectionRecord` (`01-technical-options.md` §1). This document answers "what do I
actually write," where `01-technical-options.md` answers "what does the software do with it."
**Author:** Dr. Elias Vance, Laboratory Director, under CEO-delegated full authority over this
Programme (2026-07-15).

---

## 1. Design Basis

This template is not invented from nothing. It reconciles two things that already exist and were
never previously made to match field-for-field:

1. **This workspace's own empirically-used pattern.** `research-report.md` § Audit History's
   mistake log — its first two entries, `MISTAKE-2026-07-14-001` and `MISTAKE-2026-07-14-002` —
   already converged, independently, on a structure — Classification, Dates, Logged by,
   Requirement violated, What happened, Root cause, Remediation, Status, and dated Update blocks
   appended rather than silently rewritten. That structure was arrived at under real use, twice,
   before this template existed — it is evidence, not a guess.
2. **Professional incident-review practice**, specifically the parts of it that this workspace's
   own emergent pattern already independently reproduced, which is itself a signal those parts are
   load-bearing rather than ceremony:
   - **Blameless postmortems** (Google SRE Workbook): the record documents systemic contributing
     factors and the accountable investigator-of-record, not a blamed individual. This maps onto
     `logged_by` being about attribution/accountability for the record itself, not about naming
     who caused the underlying event.
   - **Five Whys**: `root_cause` must name a systemic factor reached by drilling past the first
     symptom, not the first symptom itself. "Human error" or "the hook didn't fire" are starting
     points, not root causes, unless the drilling actually terminates there and that termination is
     shown.
   - **Correction-of-error discipline** (the Amazon COE pattern of separating what-happened /
     root-cause / corrective-action into distinct fields rather than one narrative blob): matches
     `ReflectionRecord`'s field separation exactly, which is why this template keeps them as
     distinct fields rather than prose.
   - **Append-only, honestly-labeled updates**: this Programme's own `mistake-log.md` already
     demonstrated the failure mode this guards against — `MISTAKE-2026-07-14-002` was marked
     "Remediated" before its remediation was actually complete, then corrected via an honest
     "Update — remediation was incomplete" block rather than silently editing the original verdict.
     This template makes that the standard authoring rule, not an exception handled after the fact.

---

## 2. The Template

Copy this block per new reflection. One record per distinct lesson — if a single incident produces
two genuinely separable lessons with different `scope_of_applicability`, author two records, not
one with a compound scope.

```markdown
## REFLECT-<NNN> — <one-line, specific, greppable title>

| Field                      | Value                                                                                                                    |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **reflection_id**          | `REFLECT-<NNN>`                                                                                                          |
| **trigger_type**           | one of: `process_violation` / `defect_root_cause` / `ase_exception_closure` / `adversarial_finding` / `director_flagged` |
| **source_event_ref**       | full workspace-root-relative path (never `../`, never a bare ambiguous root) + anchor to the originating report or entry |
| **severity**               | `P0` / `P1` / — (only set for `defect_root_cause`; leave blank otherwise, per schema)                                    |
| **logged_by**              | named investigator of record — a real person, never `"agent"`                                                            |
| **sacred**                 | `true` (default and enforced for `process_violation` / `defect_root_cause` / `ase_exception_closure`) / `false`          |
| **status**                 | `active` at authoring time                                                                                               |
| **migrated_from** (if any) | e.g. `mistake-log.md#MISTAKE-001` — omit entirely if this is not a migration                                             |

**What happened (factual, blameless — describe the event and its systemic context, not who is at
fault):**

<one paragraph>

**Root cause (the systemic factor reached by drilling past the first symptom — show the drilling
if the first answer isn't obviously terminal):**

<one paragraph; if Five-Whys reasoning was used, the intermediate whys may be shown as a short
list before the terminal cause>

**Remediation (the corrective action actually taken — distinct from the finding; "logging this
record" does not count as remediation unless logging genuinely was the fix):**

<one paragraph or numbered list>

**Scope of applicability (what future situations should surface this record — specific enough
that a retrieval query would actually match it; not so broad it always matches and therefore never
informs anything):**

<one or two sentences>

**Summary (the synthesized, Reflexion-style verbal lesson — this is the field that gets embedded
and retrieved; it must stand alone without requiring the reader to open `source_event_ref`):**

<two to four sentences>

---

**Update (`<YYYY-MM-DD>`) — `<what changed and why, stated directly, never "see below">`:**

<Only added when something about this record's status, scope, or verdict genuinely changes after
initial authoring. Never edit the original fields above in place — append a dated Update block
instead, exactly as this Programme's own `mistake-log.md` already does. If `status` changes,
state the new value here and update the table's `status` row to match; do not let the two go out
of sync.>
```

---

## 3. Authoring Rules

Non-negotiable — checked at write-time by `__post_init__` where the schema can enforce them, and
by the investigator where it can't.

| Rule                                                                                     | Enforced by                                                                                                                  |
| ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `trigger_type` must be one of the five defined values                                    | `ReflectionRecord.__post_init__` (raises `ValueError`)                                                                       |
| `logged_by` must be non-empty and a real person, never `"agent"`                         | `__post_init__` enforces non-empty; "real person, not agent" is an investigator-side rule the dataclass cannot itself verify |
| `GOVERNANCE_TRIGGERS` records default `sacred=True`                                      | `__post_init__`                                                                                                              |
| `summary` must stand alone (it is the embedded field — see `01-technical-options.md` §2) | Investigator judgment at authoring time                                                                                      |
| `root_cause` must name a systemic factor, not restate the symptom in `What happened`     | Investigator judgment at authoring time                                                                                      |
| One record per distinct lesson, not per document                                         | Investigator judgment at authoring time                                                                                      |
| Status changes are appended as dated Update blocks, never silently rewritten in place    | Investigator judgment at authoring time — this is the rule `MISTAKE-2026-07-14-002` demonstrated the cost of skipping        |
| All paths in `source_event_ref` and prose are full workspace-root-relative paths         | Investigator judgment at authoring time — this Programme's own path-ambiguity mistake log entry is the precedent             |

---

## 4. Relationship to `mistake-log.md`

This template supersedes the ad hoc structure `mistake-log.md` entries have used by convention,
once the reflexion system is operational (per that file's own stated terms: "migrated into it and
this file is superseded, not deleted"). Until Phase 3 migration (`03-deployment-guidelines.md`)
runs, `mistake-log.md` remains the actual logging location and may continue using its existing
structure — this template does not require retroactively reformatting entries already logged
there; Phase 3's migration step is the one place that translation happens, and it happens once,
deliberately, not entry-by-entry as new mistakes occur before then.

---

**Maintained By:** Core Component 00 Laboratory
**Programme:** `2026-07-14-reflexion-memory-system`
