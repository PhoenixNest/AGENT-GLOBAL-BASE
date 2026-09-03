---
description: Documentation Style Protocol — descriptive material and code state current status exclusively; no revision narrative, no external reference pointers — always active
---

# Documentation Style Protocol — Prohibition of Embedded Revision Narrative

**Classification:** CC-00 Laboratory Governance Rule
**Applicability:** All descriptive and reference material within this workspace, including
source-code comments and docstrings
**Status:** Always active

---

## 1. Purpose

This protocol establishes the requirement that descriptive and reference material within this
workspace state current status exclusively, and prohibits the embedding of revision-history
narrative within such material. It further establishes the designated locations in which
revision-history content shall instead be recorded, and prohibits the citation of those locations
by file-path reference from within current-state material.

---

## 2. Definitions

For the purposes of this protocol:

1. **Descriptive or Reference Material** means any document, rule file, docstring, or code
   comment whose function is to state the current condition, configuration, or behavior of a
   system, process, or artifact within this workspace.
2. **Revision-History Content** means any statement narrating a change to a document or to code —
   including, without limitation, a stated date of change, a reference to a commit hash, a
   statement of prior wording, or a description of when, why, or by whom a change was made.
3. **Designated Record** means a file or file class enumerated in Section 7, whose function is to
   hold Revision-History Content.
4. **External Reference Pointer** means a citation, within Descriptive or Reference Material, of
   the file path of a Designated Record, offered for the purpose of directing the reader to
   historical detail.

---

## 3. Requirement — Current-State Description

Descriptive or Reference Material shall describe current status exclusively. It shall not contain
Revision-History Content, including but not limited to constructions of the form "closed on
`<date>` via commit `<hash>`," "as of this change," or "flagged for `<owner>` decision."

This requirement applies without exception to code. A docstring or inline comment is held to the
same standard as a Markdown document.

A statement of current fact that incorporates a date — including a "Last Updated" stamp, a
founding date, or a status-table entry — does not constitute Revision-History Content and is not
restricted by this Section. The prohibition addresses the narration of change; it does not
address the presence of a date within a statement of present fact.

This protocol governs Descriptive or Reference Material concerning this workspace's own systems
and history. Fictional or illustrative example data — including teaching examples contained
within a skill's reference documents — falls outside the scope of this protocol.

---

## 4. Permitted Structure — Phases of the Subject

Phased or staged structure is permitted where the phases are an attribute of the subject itself:
a pipeline's numbered stages, a runtime's own startup sequence (for example, `# Phase 1 —
connect`, `# Phase 2 — fallback build`), or the rounds of an assessment. Such structure describes
the present operation of the system or process and does not constitute Revision-History Content.

A `pipeline.md` file, and a code comment narrating a system's own multi-step process (for
example, `workspace-knowledge/server.py`'s `# Phase 1/2/3` startup sequence), describes the
subject's own structure and does not violate this protocol.

---

## 5. Prohibited Structure — Phases of the Edit History

Phased or staged structure is prohibited where the phases describe work performed upon the
document or code itself — for example, "as of this change," "since the Phase 3 cutover," or
"closed in Phase 6 of a migration." Such language constitutes Revision-History Content and shall
be recorded in a Designated Record pursuant to Section 7, not embedded within the artifact
itself.

---

## 6. Exemption — Research Documents

This protocol does not apply to research documents — Telescope research reports and their
supporting analysis, together with materially similar thesis-form works. The investigative
phases, methodology, and progression of findings recorded in a research document constitute its
substantive content and do not constitute incidental Revision-History Content describing changes
to some other artifact. The narration of investigative stages is intrinsic to the function of a
research document.

The governing distinction is the subject of the narrative: a research document narrates the
investigation itself, whereas Descriptive or Reference Material narrates the history of edits
made to that same material. The former is the purpose of the document; the latter is prohibited
under Section 3.

This exemption attaches to the research report and its analysis specifically. It does not attach
to every file located beneath a `telescope/` path. A `CLAUDE.md`, `README.md`, or template file
within a telescope directory remains Descriptive or Reference Material and remains subject to
this protocol. A `progress.md`-form edit-tracking file within a research entry's `supporting/`
directory remains Revision-History Content and shall be recorded pursuant to Section 7, not
narrated as though it constituted part of the research itself.

---

## 7. Designated Record and Log Locations

Revision-History Content concerning Descriptive or Reference Material or code shall be recorded
exclusively within one of the following Designated Records:

1. Maintenance records (`core-component-00/platform/maintenance-records/`)
2. Session logs, `progress.md`, `checkpoint.json`
3. ADR amendment logs
4. Git commit messages
5. Append-only archives (`company/optimization-history/`)
6. A self-declared canonical history record (`academic-neural-unit-00/formation/**`)
7. A dated-folder-per-cycle planning artifact functioning as its own amendment log (for example,
   `recruitment-plan.md`, `plans/**`)
8. A document's own dedicated Amendments or Exceptions Log section, clearly separated from its
   current-state description (for example, an ADR's Amendments table, a crew `profile.md`'s
   `### Amendment (...)` section)

Revision-History Content concerning a change to Descriptive or Reference Material or to code
shall be recorded within one of the foregoing locations. It shall not be recorded inline within
the document or code that the change affected.

---

## 8. Prohibition of External Reference Pointers

The proper recording of Revision-History Content pursuant to Section 7 does not authorize an
External Reference Pointer to that Designated Record from within the Descriptive or Reference
Material or code it concerns. A code comment or descriptive-document statement shall be
self-contained: it shall state the current-state fact directly and shall not direct the reader to
an external Designated Record for verification. An External Reference Pointer becomes inaccurate
upon the relocation, archival, or renaming of the record to which it refers — an event this
protocol does not guarantee against.

This prohibition does not extend to a functional cross-reference to another current document a
reader would reasonably navigate to in the course of using or maintaining the artifact — an
implementation file the code mirrors, the relevant section of an architecture document, or
another rule file. It applies specifically to a pointer directed at a Designated Record whose
sole function is the retention of historical provenance.

The reciprocal reference belongs on the side of the Designated Record. A maintenance record's own
"Related Records" section, or a Maintenance Log Index entry, shall identify the files it
concerns. Such a reference requires correction in only one location upon change, rather than at
every location where the Designated Record is relevant.

A reference to a document's own dedicated Amendments or Exceptions Log section (Section 7, item 8) does not constitute an External Reference Pointer and is not restricted by this Section.

---

## 9. Rationale

Revision-history narrative embedded within Descriptive or Reference Material introduces
unnecessary reading-comprehension obstacles and creates ambiguity between what is presently true
and what was formerly true. An External Reference Pointer introduces a materially similar risk in
different form: it directs the reader's attention away from the artifact under examination, and
its accuracy is not assured to persist as the referenced record is relocated, archived, or
renamed. Descriptive and reference material, and code, shall remain legible and accurate upon
their own terms, without reliance upon external verification.

---

**Authority:** CEO → CC-00 Laboratory Director (Dr. Elias Vance)
