# Final Review — Curriculum External-Audience Remediation (2026-08-26)

**Requested by:** CEO, via the approved implementation plan at
`academic-neural-unit-00/plans/2026-08-26-curriculum-external-audience-remediation/external-audience-remediation-plan.md`.
**Reviewers:** Cross-cluster internal reviewer (audience-independence scope, per
`curriculum/README.md` §6's standing rule that reviewers do not review their own module — see
`internal-review-cross-cluster.md`), blind external reviewer (briefed with zero repository access,
per plan §5 — see `external-review-blind-read.md`), Dr. Naledi Mokoena (ANU-00 Lead, synthesis).
**Date:** 2026-08-26
**Scope:** Confirm the Phase 3 remediation (link-mesh conversion across all 24 modules, the
`advanced/07` case-study reframe, the `advanced/05` citation trim) actually closes the Pass 3 S-1
finding and this round's own expanded scope (plan §2), and surface — not resolve — anything it
does not close.
**Status:** For CEO sign-off. Closes out this round's Phase 4; two items below are explicitly not
closed by this review and are escalated rather than decided here.

---

## Method

Neither review restated the Phase 1 audit's or Phase 3's own claims from memory. Each reviewer
re-derived its findings against the actual current state of the files.

| Record checked                                                 | What it was checked for                                                                     |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| All 24 modules + `curriculum/README.md` (structural link scan) | Every hosted-site link resolves to a real target file and a real heading anchor             |
| All 24 modules + `curriculum/README.md` (citation grep)        | Zero remaining `core-component-00`, `this workspace`, `本工作区`, `this repository` matches |
| `advanced/07` §3–4, in full                                    | Whether the reframed case study reads as self-contained to a cold reader                    |
| `advanced/05`'s edited table row                               | Whether the citation trim leaves the sentence coherent                                      |
| `curriculum/README.md`, in full                                | Whether the file itself reads as reachable/self-contained to a cold outside reader          |
| `introductory/03`, in full                                     | Baseline: does an already-clean module still read clean (no false-positive concern)         |

---

## Cross-Cluster Internal Reviewer — Mechanical & Structural Verification

- Ran a script-based check of all 694 hosted-site links: confirmed every one resolves to an actual
  module file under `curriculum/`, and every anchor fragment matches a real heading in that file.
  Zero broken targets, zero broken anchors.
- Corpus-wide grep for the citation defect class (`core-component-00`, `this workspace`, `本工作区`,
  `this repository`, `AGENT-GLOBAL-BASE`): zero matches anywhere in the 24 modules or
  `curriculum/README.md`.
- Independently re-read `advanced/07` §3–4 and confirmed the two remaining internal-framing sites
  Phase 3 was meant to fix are actually gone, not just reworded around.
- **One open item, named plainly rather than smoothed over:** `curriculum/README.md` §6 (its
  internal review-process description) still names Dr. Mokoena, cites a non-public crew-skill file,
  and describes escalation to the CEO — flagged, not fixed, because it is a scoping question this
  reviewer's mandate does not cover.

**Conclusion: Complete**, for everything within Phase 3's actual scope. The one open item is a
scoping question, not a defect this reviewer's checks failed to catch.

## Blind External Reviewer — Cold-Read Verification (Zero Repository Access)

- Read `advanced/07` in full: the reframed §4 case study holds up under a genuinely cold read — the
  filesystem-behavior claim is independently verifiable, and the remaining internal aside reads as
  a non-load-bearing real-world footnote, not evidence the argument depends on.
- Read `introductory/03` in full as a baseline: clean, no defects of this class, confirming the
  review method isn't simply failing to find things.
- Read `curriculum/README.md` in full, cold: found it is **not** currently a clean landing page for
  an outside reader. The very first substantive sentence (line 4–5) cites a `plans/` document
  outside `curriculum/` entirely, using a bare backtick path rather than a converted markdown link —
  invisible to both the Phase 1 links audit and the Phase 3(a) conversion script, since neither was
  scoped to catch a non-link-syntax citation pointing outside `curriculum/`. The file cites `plans/`,
  `reviews/`, `templates/curriculum/`, `crew/`, `formation-report.md`, and the repository's own
  `CLAUDE.md` throughout — not confined to §6 as the Phase 1 audit's own citation implied.
- **One open item, named plainly rather than smoothed over:** whether `README.md` should be split
  (an internal process appendix plus a short, separately authored public landing page) or edited in
  place is explicitly not this reviewer's call — flagged as the single highest-severity open item
  from this round.

**Conclusion: Complete** for the module content Phase 3 was scoped to fix (`advanced/07`,
`advanced/05`, and the link mesh). **Not complete** as a claim that the curriculum's front door
(`curriculum/README.md`) is itself ready for an external reader — that was never Phase 3's brief,
and this review does not retroactively expand Phase 3's scope by finding it.

---

## Joint Recommendation

Both reviewers agree: everything this remediation round was actually chartered to fix — the
694-link cross-reference mesh, the `advanced/07` case study Pass 3 originally flagged, and the one
additional citation the Phase 1 audit surfaced in `advanced/05` — is fixed, verified by an
independent structural check and by a genuinely cold read, and does not reintroduce the defect
class it was meant to remove. That work is complete.

Two items are open, and I am distinguishing them from each other rather than letting them read the
same way, because they carry different weight and need different owners:

1. **The author-metadata question (plan §2 item 5)** — a small, contained editorial decision (what
   the "ANU-00" institutional tag in each module's byline should say to an outside reader). This was
   always a known, already-scoped-as-deferred item in the plan itself, not a new finding. It does
   not block anything and can be resolved whenever the CEO or I take it up next.

2. **`curriculum/README.md`'s own readiness as a landing page** — a genuinely new finding from this
   round's blind external review, materially larger in scope than item 1: it is a structural
   question about whether the curriculum's entry-point document needs to be split into a public
   page and an internal appendix, not a citation that needs converting. I am **not** ruling on this
   myself. Recommending the CEO treat it as a follow-up scoping decision — most likely its own short
   plan under `plans/`, scoped narrowly to `curriculum/README.md` alone, rather than folded into
   this round after the fact or left to accumulate the way the reader-feedback-log's entries did
   before Pass 3 caught the pattern this remediation exists to break.

**We recommend the CEO accept this round's remediation as complete and closed, sign off on Phase 5
verification below, and treat the `curriculum/README.md` landing-page question as a new, separate,
not-yet-scoped item for a future decision — not a blocker on anything delivered here.**

**Cross-Cluster Internal Reviewer — 2026-08-26**
**Blind External Reviewer — 2026-08-26**
**Dr. Naledi Mokoena, ANU-00 Lead — 2026-08-26**
