# ANU-00 Curriculum — External-Audience Content Independence Remediation — Implementation Plan

**Status:** Approved by CEO 2026-08-26 (directed execution via git-worktree-isolated personnel) —
**executed and closed the same day**
**Prepared:** 2026-08-26
**Scope:** Remediate the curriculum so its 24 existing modules are independently understandable to
a reader with no access to this repository, per CEO direction that the curriculum now serves as
general-purpose teaching material. Bounded to content-independence remediation only — no new
modules, no S-2 practicum/post-training content, no broader expansion.

> This document authorized the remediation executed the same day it was approved. All five phases
> in §6 ran to completion: audit reports, the link-mesh conversion script, the `advanced/07`/
> `advanced/05` edits, both Phase 4 reviews, and Phase 5 verification all live under
> `curriculum/reviews/2026-08-26-external-audience-remediation/`, filed in per-phase subfolders
> (`phase-1-audit/`, `phase-4-review/`, `phase-5-verification/`) per that folder's own README.
> Per `phase-4-review/final-review.md`'s Joint Recommendation, two items were escalated to the CEO
> rather than resolved by this plan: the already-deferred author-metadata question (§2 item 5) and
> a new finding that `curriculum/README.md` itself is not yet a clean external landing page —
> neither blocks this plan's closure.

---

## 1. Context

`academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md`
recorded, under scope decision **S-1**, that both blind external reviewers — reading cold,
independently, with no ANU-00/CC-00 context — flagged the same passage: `advanced/07`
("Multi-Agent Orchestration: Worktree Isolation & Consensus") §4 builds an extended case study
around a real workspace-internal git-worktree incident, citing
`core-component-00/engineering/multi-agent-engineering/fundamentals/git-worktree-orchestration.md`.
The internal cluster reviewer (Dr. Ibarra-Costa) independently confirmed the case study represents
its source accurately — this was never a factual defect. Pass 3 recorded it as a pure audience
question: fine for an internal ANU-00/CC-00 readership, a visible seam if the curriculum is ever
read outside the workspace. The CEO's ruling on that question was left open at Pass 3 and remained
open through Pass 4 (2026-08-19) and the 15 reader-feedback-log entries filed since.

**CEO direction, this session:** the curriculum's audience question is now settled. The content
must be independently understandable to a reader with no repository access, and the curriculum is
now positioned as general-purpose teaching material rather than workspace-internal documentation.
The CEO has also approved the S-2 extension plan
(`academic-neural-unit-00/plans/2026-08-19-curriculum-coding-and-post-training-extension/curriculum-extension-plan.md`)
but directed that this remediation happens first, with S-2's execution and any broader expansion
scheme deferred to a later stage.

**Why this remediation turns out to be bigger than the one flagged passage.** Pass 3's external reviewers were
briefed to read as outside subject-matter experts, not as readers with zero access to this
repository — so nothing in Pass 1–4 checked for repository-dependence specifically. Since Pass 4,
the reader-feedback-log's Entries 12–13 (2026-08-24) built an internal cross-reference link mesh —
~700 links, all resolved as workspace-root-relative paths (`academic-neural-unit-00/curriculum/...`)
— that only work inside this repository. That work was correct under the audience assumption in
force at the time; it is now, under the CEO's new ruling, itself part of what this remediation has
to fix. This plan scopes the work as full content-independence remediation across the corpus, not a
one-file edit.

---

## 2. What's in scope

1. **The internal cross-reference link mesh.** ~700 links across all 24 modules and
   `curriculum/README.md` (reader-feedback-log Entries 12–13) resolve only inside this repository.
   Per the CEO's distribution-target ruling (§4), every one needs to become a real, resolvable
   `https://` URL against the hosted site.
2. **`advanced/07`'s citation of a non-public internal document.** The git-worktree-orchestration.md
   citation is unreachable and unverifiable by an outside reader — the same defect §5's citation
   rule is written to prevent, applied here to an internal source rather than an external paper.
   Either the case study is reframed around a citable, publicly verifiable example, or the internal
   citation is kept only as a secondary internal note with a public-source primary example carrying
   the pedagogical weight.
3. **Module-to-module prerequisite references** ("as covered in `introductory/02`") — these become
   real hyperlinks to the corresponding page on the hosted site, per §4.
4. **A corpus-wide sweep for other internal-workspace body-text references beyond the one flagged
   passage.** Pass 3 only checked `advanced/07`, because that's the passage the external reviewers
   happened to hit; nothing has ever audited the other 23 modules for the same defect class,
   including the more technical advanced-tier modules (harness engineering, agentic safety,
   orchestration, evaluation) most likely to reach for a workspace-internal example the way
   `advanced/07` did.
5. **The author-metadata institutional-framing question.** Every module's metadata block credits
   its author as, e.g., "Dr. Kaito Fujimori, Research Scientist — Agent Systems Research, ANU-00."
   Author attribution is normal for teaching material; "ANU-00" as a bare institutional tag is not
   self-explanatory to an outside reader. This is a separate, still-open CEO decision point — the
   distribution-target ruling in §4 does not resolve it — and this plan does not resolve it
   unilaterally.

## 3. What's explicitly out of scope

- **S-2's practicum and post-training modules.** Approved but deferred by CEO direction — no part
  of this plan.
- **The broader expansion scheme** referenced in the CEO's direction — deferred, not scoped here.
- **The bilingual EN/ZH convention and the citation-to-real-external-sources rule (README §5).**
  Both are already aligned with an external, verifiable-source standard; nothing about the external-
  audience ruling argues for changing either, and this plan does not touch them.
- **Content accuracy.** Pass 4 closed every content defect in the corpus with independent
  re-verification; this plan does not reopen content accuracy, only audience-independence.

---

## 4. Distribution target — resolved by CEO ruling, this session

This plan originally flagged the distribution target as an open decision, since the mechanical fix
for the ~700-link cross-reference mesh (§2 item 1) differs completely depending on how the
curriculum reaches a reader:

| Target                             | What "external-ready" means for the link mesh                                                                                                                                                                              |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Hosted public site**             | Links become real, resolvable `https://` URLs against the hosted domain.                                                                                                                                                   |
| **Self-contained export bundle**   | Links stay relative, but relative _within the exported bundle's own folder structure_ — not this repository's absolute paths.                                                                                              |
| **Individually distributed files** | A single module handed out alone can't assume its cross-references are reachable at all — links likely need to degrade to plain-prose references ("see the module on RAG fundamentals") rather than assuming clickability. |

**CEO ruling, this session: Hosted public site — selected.** The curriculum will be published as a
single hosted webpage, with both internal (ANU-00/CC-00) and external readers studying it from the
same site rather than from two separately maintained editions. This clears the Phase 3 blocker
below: the link-mesh fix is now fixed as **convert every internal cross-reference link to a real,
resolvable `https://` URL against the hosted site**, and the module-prerequisite references in §2
item 3 resolve the same way.

**What this ruling does not decide, and is out of this plan's scope:** the concrete hosting
mechanism (site generator, hosting provider, build/publish pipeline) is an execution detail for
whoever runs Phase 3, not a content-remediation question — this plan governs what the curriculum's
own content and internal links need to say, not how the pages get served. One consequence worth
naming plainly: because internal and external readers now share one page per module, there is no
"internal-only" variant to fall back on — every item in §2 (the link mesh, the `advanced/07`
citation, prerequisite references, the body-text sweep, and the still-open author-metadata question)
applies to the whole reader base, not a subset of it.

---

## 5. Review process for this run

Every formal review round to date (Pass 1–4, `curriculum/README.md` §6) used independent,
adversarial reviewers who did not review their own work, plus a blind external pass. Since Pass 4
closed (2026-08-19), the 15 reader-feedback-log entries have instead been self-authored and
self-verified by Dr. Mokoena alone, with no independent reviewer — a real departure from README §6's
own standard. That pattern twice produced full-corpus regressions the log itself had to catch and
fix afterward: Entry 11 (all 24 modules' metadata tables collapsed by an earlier automated pass) and
Entry 15 (54 body tables across 20 modules collapsed the same way). Both were self-caught, not
independently caught.

Given this remediation is now explicitly audience-facing — a mistake here is visible to a reader who
cannot come back and ask what was meant, unlike an internal defect — **this plan reverts to README
§6's independent-review standard, not the reader-feedback-log pattern:**

- **Internal review** — cross-cluster reviewers (not authors of the modules they review, per README
  §6's standing rule), scoped specifically to audience-independence: does every link resolve under
  the chosen distribution target, is every citation reachable by an outside reader, does any passage
  assume workspace-internal context.
- **One blind external review**, briefed explicitly as "a reader with no access to this repository or
  any other ANU-00/CC-00 material, evaluating only the file(s) actually in front of them" — a
  narrower and more literal brief than Pass 3's "outside subject-matter expert" framing, since that
  framing is exactly what let the repository-dependence issue through Pass 1–4 unflagged.
- **Lead synthesis**, reusing root `templates/review-records/final-review.md` per ANU-00's standing
  convention, same as Pass 3 and Pass 4.

Filed as a new dated round, `curriculum/reviews/YYYY-MM-DD-external-audience-remediation/`, per
`reviews/README.md`'s dated-round convention — not appended to `reader-feedback-log.md`, since this
is a point-in-time reviewer verdict, not a continuous log entry.

---

## 6. Production workflow (to run only after CEO approval of this plan)

**Phase 1 — Audit (2 agents, Sonnet/high, parallel):** full-corpus sweep across all 24 modules,
independent of the distribution-target decision. One agent inventories every internal cross-
reference link and every citation to a non-public internal document; the second does a full-text
(non-grep) read for workspace-internal jargon, tooling, or org-structure references in body text
beyond the already-known `advanced/07` passage. Output: a single audit report — counts, locations,
and a classification of each finding (link / internal citation / body-text reference) — no fixes
applied yet.

**Phase 2 — CEO decision point (not an agent phase):** present the audit findings plus the
author-metadata question in §2 item 5. The distribution-target decision this phase originally
gated is now resolved (§4 — hosted public site); the remaining open item at this checkpoint is
author-metadata only, and it does not block Phase 3 from starting.

**Phase 3 — Remediation authoring (agent count set by audit results, Sonnet/high):** link-mesh
conversion to real `https://` URLs against the hosted site, executed as a masked, scripted pass
(mirroring the approach already proven safe in reader-feedback-log Entries 3 and 4 — mask
code/math/URL spans, convert only the targeted pattern, verify via diff review) rather than by
hand. Content-level fixes (the `advanced/07` case study reframe, and any further body-text passages
the audit surfaces) go to each module's original author, per README's own standing convention that
authors remediate their own modules.

**Phase 4 — Review (internal reviewers + 1 external reviewer + Lead synthesis, Sonnet/high for
reviewers, Opus/high for the Lead's synthesis):** per §5 above.

**Phase 5 — Verification:**

- Confirm zero internal cross-reference links fail to resolve under the chosen distribution target.
- Confirm zero remaining citations to non-public internal documents (or, where kept as a secondary
  note, confirm a public-source primary example carries the pedagogical claim instead).
- Confirm the audit's body-text findings are each either fixed or explicitly ruled non-issues by the
  Lead's synthesis, not silently dropped.
- Run `prettier --write` over every created/modified file per root `CLAUDE.md` §1.
- Report back: what passed, what needed revision, using the same per-document verdict format Pass 3
  and Pass 4 established, plus the CEO's outstanding decision on the author-metadata question if
  still unresolved at that point.

---

## 7. Approval gate

**Next step:** CEO reviews this plan — the confirmed-in-scope items, the deferred-scope boundary
against S-2 and the broader expansion, the now-resolved distribution-target ruling (§4), and the
reinstated §6-style independent review process. Implementation (Phase 1 audit) may begin on
approval of this plan; Phase 3 (remediation authoring) may follow immediately after Phase 1, since
the distribution-target blocker that previously gated it is cleared. The author-metadata question
(§2 item 5) remains open and should be resolved at the Phase 2 checkpoint, but does not block
Phase 3.
