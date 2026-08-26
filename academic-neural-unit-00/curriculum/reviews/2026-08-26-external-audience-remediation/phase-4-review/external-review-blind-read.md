# Phase 4 External Review — Blind Read

**Round:** 2026-08-26 external-audience remediation
**Reviewer briefing (per plan §5):** a reader with no access to this repository or any other
ANU-00/CC-00 material, evaluating only the file(s) actually in front of them — deliberately
narrower than Pass 3's "outside subject-matter expert" brief, since that framing is exactly what
let the repository-dependence problem through Pass 1–4 unflagged.
**Method:** Close, cold read of `curriculum/README.md` in full, plus `advanced/07` (the module this
whole remediation round exists because of) in full, plus a spot-check of one introductory module
(`introductory/03`) for baseline sanity. Not a re-run of the mechanical checks the internal review
already performed (link resolution, citation-path grepping) — this pass is for what only a human
(or a human-simulating) read catches: does anything _read_ as written for an insider, even where no
script would flag it.

---

## 1. `advanced/07` — the module this round exists to fix

Read in full, §1 through the end of §4 (the section that was actually rewritten) closely, §5
onward at normal reading pace. **Reads cleanly as a cold reader with no repository access.** The
directory-junction/symlink failure mode in §4 now stands on its own: I could follow and verify the
claim ("recursive delete follows a reparse point/symlink by default") without needing to trust
anything about who wrote this or where they work. The one internal-organization mention left in §4
("this curriculum's own producing organization ran into exactly this failure mode once in
practice...") reads exactly as advertised — a throwaway real-world aside, not something the
argument leans on. I did the test the internal reviewer suggested: mentally deleting that
parenthetical changes nothing about whether the paragraph's claim holds. **Pass.**

The five-phase lifecycle table and diagram in §4 also read fine cold — the table is fully
self-contained (I can verify its own internal consistency: five commands, five actions, nothing
unexplained), and it no longer claims to be "this workspace's own" anything.

## 2. `introductory/03` — baseline sanity check

Read in full. No defects of this class found — every term is defined before use, cross-references
resolve to the hosted-site URL pattern, nothing assumes I have repository access or organizational
context. This is what "clean" looks like, useful as a baseline against the next finding.

## 3. New finding: `curriculum/README.md` is not a clean landing page for an outside reader

This is the most consequential finding from this review pass, and it goes beyond what Phase 1's
jargon-sweep audit scoped (that audit named §6 specifically as containing ANU-00-internal process
detail; a full cold read of the whole file shows the problem is not confined to §6).

Reading `README.md` top to bottom as someone with zero repository access:

- **Line 4–5**, the very first substantive sentence, cites
  `academic-neural-unit-00/plans/2026-08-17-curriculum-first-production-run/curriculum-development-plan.md`
  — a bare backtick path, not a markdown link, pointing outside `curriculum/` entirely into
  `plans/`. This was not caught by the Phase 1 links audit or the Phase 3(a) conversion script,
  because it is not markdown-link syntax and it is not under `curriculum/` — both the audit's
  pattern and the conversion script's target prefix were scoped to `curriculum/`-internal links, and
  correctly so per the plan's own stated scope, but that means this citation fell outside both
  nets. As a cold reader, I have no way to know what this document is or reach it.
- **Line 48**, in §2, cites `crew/lead/naledi-mokoena/skills/research-programme-chartering.md` —
  the same file Phase 1's audit already flagged at §6 (line ~345), but this is a _second_,
  independent occurrence the Phase 1 audit's own line-number citation did not capture. The finding
  "README §6 cites this file" undersells how many places it (and files like it) appear.
- **Lines 97, 99, 152, 192, 240, 302–329, 386, 388, 420, 423, 429–433, 465** (a non-exhaustive list
  from a single grep, not a full manual count) cite `plans/`, `reviews/`, `templates/curriculum/`,
  `crew/`, `formation-report.md`, and the repository's own `CLAUDE.md` — the file is, start to
  finish, written as ANU-00's own internal production and governance record for how this
  curriculum gets made, with a module index and a short audience statement (§1) embedded inside it,
  not the reverse.
- By contrast, **lines 379–381** (the per-module file-slug lists) and the audience statement in §1
  itself read fine — those are exactly the kind of content a landing page for this curriculum
  should have.

**As a cold reader arriving at this file first (which is what "curriculum/README.md" as a filename
invites), I would not be able to tell, within the first screen, whether this is a page written for
me or an internal team's process document that happens to also contain a module list.** That is a
different, larger kind of defect than "a citation doesn't resolve" — it's a structural framing
problem, not a mechanical one, and no scripted pass catches it.

**I am not recommending a fix here** — per this round's own stated boundaries (the plan's
instruction not to resolve the author-metadata question unilaterally, and the same logic applies
here even more strongly since this is a bigger structural call than a metadata tag): whether
`README.md` needs a substantial split (an internal process appendix plus a short, separately
authored public landing page) or can be brought into scope with a lighter edit is a scoping
decision for the Lead, and arguably for the CEO, not something a review pass should decide by
itself. Flagging it as the single highest-severity open item from this review round.

---

**Verdict: Pass on everything Phase 3 was actually scoped to fix — the `advanced/07` reframe holds
up under a genuinely cold read. Not a clean pass on `curriculum/README.md` as a whole, though this
finding is explicitly outside what Phase 3 was asked to remediate — it belongs to the same open
scoping question the internal review already flagged, now shown to be broader than §6 alone.**
