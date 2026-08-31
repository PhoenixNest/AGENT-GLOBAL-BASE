# Curriculum Books/Numbering Restructure — Plan

**Status:** Approved — CEO sign-off recorded below; executed same day
**Prepared:** 2026-08-31
**Scope:** Group the curriculum's readable content under a new `books/` subfolder, number the
four content folders for reading order, and correct every cross-reference and citation URL the
move touches. No change to `plans/` filing location, `curriculum/reviews/`, or any module content
beyond path references.

---

## 1. Context

The CEO reviewed the ANU-00 file tree (raised via Dr. Mokoena's tree-clutter memo, 2026-08-30) and
made three follow-up requests:

1. File `plans/` entries relating to the curriculum inside `curriculum/` itself.
2. Add a `Books` subfolder under `curriculum/` to hold the three proficiency levels plus the
   practicum (experimental exercises).
3. Add sequence numbers to the level and exercise folders so a reader can tell reading order
   directly from the file tree.

Dr. Mokoena's response (memo, 2026-08-30/31):

- **Recommended against #1.** `plans/README.md` documents that plans and deliverables were
  deliberately split apart after the opposite arrangement caused exactly the ambiguity this would
  reintroduce — `plans/` is built to generalize beyond curriculum, not to be a curriculum
  subfolder.
- **Endorsed #2 and #3** as a combined restructure, since both touch the same 32 module files'
  citation URLs and needed to be scoped and executed together rather than as two separate passes.

## 2. CEO Decision Record

| Item                              | CEO Decision                                                                                                                                                                                                                                                                                          |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Plans location                    | **Approved** — keep `plans/` at its current top level, unchanged                                                                                                                                                                                                                                      |
| `Books/` subfolder                | **Approved** — proceed despite the cross-reference update cost; accepted as worthwhile for a more intuitive tree                                                                                                                                                                                      |
| Folder numbering                  | **Approved** — agreed with the proposal; asked for the most efficient execution method                                                                                                                                                                                                                |
| Worktree-based parallel execution | **Declined**, per Dr. Mokoena's recommendation (memo, 2026-08-31) — the work has a strict sequential dependency (convention ratified before the scripted pass can run) and cross-cutting references between the four folders that prevent a clean per-folder split. Executed single-threaded instead. |

## 3. Practicum Placement Decision

`curriculum/practicum/README.md` §5's own module→prerequisite table shows all six practicum
modules pairing with an `introductory` or `intermediate` concept — none with `advanced`. This is
direct evidence, not a guess, that practicum's role is to consolidate introductory/intermediate
material hands-on before the reader proceeds to advanced theory.

**Decision (Dr. Mokoena, within her documented curriculum-structure authority):** practicum is
numbered third, immediately after intermediate and before advanced.

## 4. Final Structure

```
curriculum/
├── README.md
├── books/
│   ├── 01-introductory/    (8 modules)
│   ├── 02-intermediate/    (8 modules)
│   ├── 03-practicum/       (6 modules)
│   └── 04-advanced/        (10 modules)
└── reviews/                 (unchanged — process records, not reading content)
```

## 5. Scope of File Changes

| Location                                                                        | Files | Treatment                                                                                                 |
| ------------------------------------------------------------------------------- | ----- | --------------------------------------------------------------------------------------------------------- |
| `curriculum/README.md`                                                          | 1     | Amendment 6: new §3 diagram, corrected §5 citation-URL pattern                                            |
| `curriculum/books/*/*.md` (all module content + `books/03-practicum/README.md`) | 33    | Scripted URL path correction                                                                              |
| `curriculum/reviews/**`                                                         | 23    | **Untouched** — point-in-time records; edited only when they document what existed at the time of writing |
| `plans/*.md` (incl. this folder's own future entries)                           | —     | **Untouched** — same point-in-time rule                                                                   |
| `templates/curriculum/*.md`                                                     | 2     | Checked — no literal path references, no change needed                                                    |

## 6. Execution Method

1. Ratify Amendment 6 in `curriculum/README.md` (directory diagram + citation-URL rule) first, so
   the corpus pass has an exact target pattern.
2. `git mv` the four folders into `curriculum/books/<NN-name>/`, preserving file history.
3. One scripted find-replace pass over the citation URL pattern
   (`anu00.dev/curriculum/<old-name>/` → `anu00.dev/curriculum/books/<NN-old-name>/`) across the
   34 living files only.
4. Verify zero leftover old-path URL occurrences in the living files (`reviews/` and `plans/`
   correctly still contain the old pattern, as historical snapshots).
5. Prettier pass on every modified file.

## 7. What Was Deliberately Not Changed

Inline shorthand citation labels such as ``[`introductory/01` — Title]`` are a conceptual
level+number identifier, not a filesystem path, and are unaffected by this restructure — only the
machine-resolvable URL each label links to was corrected. Relabeling the shorthand text itself to
match the new folder name would misrepresent it as a literal path and was not done.

---

**Ratified by:** Dr. Naledi Mokoena, ANU-00 Lead — 2026-08-31
**Under:** CEO approval recorded in §2 above (conversational sign-off across three memo exchanges,
2026-08-30–31)
