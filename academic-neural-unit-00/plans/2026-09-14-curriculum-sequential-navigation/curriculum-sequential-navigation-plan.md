# Curriculum Sequential Navigation ("Previous Module" / "Next Module") — Plan

**Status:** Approved — CEO sign-off recorded below (relayed by the reader); executed same day
**Prepared:** 2026-09-14
**Scope:** Add a structured "Previous module / Next module" navigation element to each of the 32
curriculum modules under `curriculum/books/` (8 introductory + 8 intermediate + 6 practicum + 10
advanced), reflecting the single reading order already ratified in `curriculum/README.md`
Amendment 6. No change to module body content, citation format, or the existing `References` /
`Internal Cross-References` section.

---

## 1. Context

A reader working through `introductory/01-neural-networks-and-deep-learning-foundations.md`
reported two navigation defects (the anchor-link issues closed in
`curriculum/reviews/reader-feedback-log.md` Entries 15–16), then separately suggested that each
module end with a "Next book" / "Previous book" pointer, the way a printed textbook series would.
This plan is the write-up of that suggestion for CEO review, following the standard gate this
folder exists to enforce: a corpus-wide structural change to all module files needs the same
sign-off past changes received (the interactive link mesh, the `§`/`§§` convention, the
`books/` restructure — see `plans/README.md`'s existing-plans table).

## 2. Current-State Findings

- **No sequential-navigation element exists today.** Every module ends the same way:
  `## References` → `### External Sources` → `### Internal Cross-References`.
- **The closing `Internal Cross-References` list is topical, not reading-order, and does not
  substitute for one.** Example: `introductory/08` (the last introductory module) closes with
  cross-references to `introductory/03`, `04`, `07`, `intermediate/08`, and `advanced/08` — every
  one of them earlier or topically related. `intermediate/01`, the module that actually comes
  next, is not listed. A reader relying on the closing section for "what do I read next" gets no
  signal there.
- **Continuity between adjacent modules exists only as informal prose, inconsistently applied.**
  `introductory/01` §13 ("Summary and What Comes Next") explicitly names `introductory/02` as the
  next module, and `intermediate/01` §1 opens by building on `introductory/01` — but this is each
  author's individual choice, not a structural guarantee present at both ends of every module.
- **The reading order is not derivable from filenames alone.** Per `curriculum/README.md`
  Amendment 6, the order is `01-introductory` (01–08) → `02-intermediate` (01–08) →
  `03-practicum` (01–06) → `04-advanced` (01–10); within a level, the two-digit number groups
  topic clusters in pairs rather than following one continuous narrative thread. `introductory`,
  `intermediate`, and `advanced` are fully specified in `README.md` §7's Module Index table;
  `practicum`'s own order is specified in `practicum/README.md` instead, since §7 excludes it.
- **Edge cases requiring an explicit design decision:** the three tier boundaries
  (`introductory/08 → intermediate/01`, `intermediate/08 → practicum/01`,
  `practicum/06 → advanced/01`) cross folders; `introductory/01` has no previous module;
  `advanced/10` has no next module.

## 3. Proposal

Add a new `## Continue Reading` / `**继续阅读**` section, generated mechanically from the full
32-module reading order (`README.md` §7's Module Index for `introductory`/`intermediate`/
`advanced`, plus `practicum/README.md` for the practicum tier — the single existing sources of
truth for order) rather than hand-authored per module:

```
## Continue Reading

**继续阅读**

**Previous:** [`introductory/07` — Introduction to Multi-Agent Systems](...) · **Next:** [`introductory/08` — Why & How We Evaluate Agents](...)

**上一模块：** [`introductory/07` — 多智能体系统导论](...) · **下一模块：** [`introductory/08` — 为什么以及如何评估智能体](...)
```

using the same shorthand-label and URL convention already ratified for
`Internal Cross-References` links. **Placement correction from the original draft:** rather than
inserting inside `References` (which §5's mandatory rule requires to be `## References` heading
immediately followed by `**参考文献**`, split into exactly the two named subsections — inserting
anything else there would break that binding structure), the new section is placed as its own
heading immediately _before_ `## References`. This is additive: `Internal Cross-References`
itself is untouched and keeps its topical-relevance role; the new section answers a different
question ("what's next in the sequence") that section was never designed to answer.

## 4. CEO Decision Record

**Approved 2026-09-14**, relayed jointly by the CEO and the reporting reader. No alternative
answers were given to the four open questions raised in the original draft, so each is resolved
using this plan's own stated recommendation as the default:

| Question                         | Decision                                                                                                                                                                                                                                     |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Terminal module (`advanced/10`)  | **Adopted (b)** — prints `**Next:** This is the final module in the curriculum.` / `**下一模块：** 这是课程的最后一个模块。`                                                                                                                 |
| First module (`introductory/01`) | **Adopted (b)** — prints `**Previous:** This is the first module in the curriculum.` / `**上一模块：** 这是课程的第一个模块。`                                                                                                               |
| Tier boundaries                  | **Adopted as-is** — treated as ordinary previous/next, no special-cased wording                                                                                                                                                              |
| Practicum → advanced crossing    | **Confirmed intended** — `practicum/06`'s `Next` points to `advanced/01`, following Amendment 6's ratified reading order, notwithstanding that `practicum/README.md` §5 pairs practicum modules with introductory/intermediate concepts only |

**Worktree-based parallel execution:** not used, for the same reason the `books/` restructure
plan declined it — a corpus-wide scripted pass generated from one canonical order has a strict
"convention ratified, then script runs" dependency and touches no independent per-folder slice.
Executed single-threaded instead.

## 5. Scope of File Changes

| Location                                                                | Files | Treatment                                                                |
| ----------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------ |
| `curriculum/books/*/*.md` (all 32 modules)                              | 32    | Insert `## Continue Reading` section immediately before `## References`  |
| `curriculum/README.md`                                                  | 1     | New §4.5 format rule + Amendment 7                                       |
| `curriculum/reviews/reader-feedback-log.md`                             | 1     | New entry recording the reader's suggestion, CEO approval, and execution |
| `plans/README.md`                                                       | 1     | Existing-plans table entry status updated to Approved/executed           |
| `curriculum/practicum/README.md`, `curriculum/reviews/**` (other files) | —     | **Untouched** — out of scope                                             |

## 6. Execution Method

1. Ratify the `README.md` §4.5 format rule and Amendment 7 first, so the corpus pass has an exact
   target pattern to follow — same sequencing the `books/` restructure's Amendment 6 used.
2. Script-generate all 32 Previous/Next section pairs directly from the full reading order (not
   hand-typed per file), to guarantee the inserted order matches the ratified sequence exactly.
3. Insert each section immediately before that module's `## References` heading.
4. Verify: every `Previous`/`Next` target resolves to a real module file and title; the chain is
   walkable end-to-end from `introductory/01` to `advanced/10` with no gaps or cycles; terminal
   wording appears only at the two true endpoints.
5. Prettier pass on all modified files.
6. Record execution in `reader-feedback-log.md`.

## 7. What This Does Not Change

The existing `Internal Cross-References` section, the `anu00.dev` citation URL scheme, the
`§`/`§§` section-citation convention, and the `books/` folder structure are all unaffected. This
plan adds one new, mechanically-generated element; it does not revise how any other part of a
module is authored or cited.

---

**Prepared by:** workspace assistant, on a reader-submitted suggestion
**Approved by:** CEO (relayed jointly with the reader, 2026-09-14)
**Ratifying:** README.md Amendment 7
