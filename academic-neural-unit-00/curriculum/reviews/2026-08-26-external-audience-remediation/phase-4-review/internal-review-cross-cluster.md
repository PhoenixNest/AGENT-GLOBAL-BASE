# Phase 4 Internal Review — Cross-Cluster, Audience-Independence Scope

**Round:** 2026-08-26 external-audience remediation
**Reviewer role:** Cross-cluster internal reviewer, per `curriculum/README.md` §6 and this
remediation's own §5 (plan). Not an author of any of the modules touched by this round's
remediation (Phase 3 work: link-mesh conversion across all 24 modules, `advanced/07` case-study
reframe, `advanced/05` citation trim).
**Scope:** Only audience-independence — does every link resolve under the chosen distribution
target, is every citation reachable, does any passage still assume workspace-internal context.
Content accuracy is explicitly out of scope (closed by Pass 4, per remediation plan §3) and not
re-litigated here.

---

## 1. Link resolution

Ran a structural verification script over all 25 files (24 modules + `curriculum/README.md`):
for every `https://anu00.dev/curriculum/...` link, confirmed (a) the referenced module file exists
under `curriculum/`, and (b) if the link carries a `#anchor`, that anchor matches an actual heading
in the target file (using standard heading-to-slug conversion).

**Result: 694/694 links resolve to a real target file and a real anchor. Zero broken targets, zero
broken anchors.**

## 2. Citation reachability

Corpus-wide scan for `core-component-00`, `this workspace`, `本工作区`, `this repository`, and
`AGENT-GLOBAL-BASE` across all 25 files: **zero matches.** Every citation remaining in the corpus
is either a public external source (arXiv, USENIX, ACM, official vendor documentation) or a
same-corpus module reference converted to a real hosted-site URL in Phase 3(a).

Spot-checked `advanced/07` §3–4 specifically, since that is where both of this round's substantive
citation fixes landed:

- The §3→§4 transition sentence no longer names `core-component-00`'s engineering practice as the
  source of the isolation-and-reconciliation pattern; it now just forward-references §4 directly.
- §4's lifecycle-table citation no longer names the non-public `git-worktree-orchestration.md`
  file; the five-phase pattern is now presented as a standard production pattern, fully specified
  by the table itself (self-contained, no external citation load-bearing on it).
- §4's directory-junction incident now leads with the publicly verifiable filesystem mechanism
  (Windows reparse-point handling, Unix `rm -r` symlink-following) as primary evidence, with the
  internal anecdote demoted to an explicitly-flagged, non-load-bearing aside ("mentioned here only
  as a real-world data point, not as something a reader needs to verify"). This reviewer confirms
  the paragraph reads correctly even with the parenthetical removed entirely — a good sign the
  demotion is real, not just relabeled.
- §10's summary no longer says "this workspace's own five-phase lifecycle"; it now cross-references
  §4 by anchor.

`advanced/05`'s citation trim: confirmed the `core-component-00/framework/02-context-engineering/`
path reference is gone from both the EN and ZH cells of the table row; the sentence still reads
coherently without it.

## 3. Residual context-assumption sweep (independent of Phase 1's own sweep)

Re-ran the same class of check Phase 1's jargon-sweep audit used (full-text read, not grep-only,
of every module) as an independent check rather than trusting Phase 1's own clean result at face
value — this is what cross-cluster review is for. Confirms Phase 1's finding: no module body text
outside the two now-fixed `advanced/07`/`advanced/05` passages assumes the reader has repository
access, and no new such passage was introduced by the Phase 3 edits themselves (link conversion is
purely mechanical and does not change surrounding prose; the two reframes were read in full above).

## 4. Open item not resolved by this review, flagged forward

`curriculum/README.md` §6 (its internal review-process section — named individuals, a citation to
`crew/lead/naledi-mokoena/skills/research-programme-chartering.md`, "raise the conflict with Dr.
Mokoena," escalation "to the CEO") remains exactly as Phase 1's jargon-sweep audit found it. This
reviewer confirms the finding is accurate and did not attempt to resolve it — per the plan, this is
a scoping question for the Lead, not a mechanical audience-independence defect this review round
fixes on its own authority.

---

**Verdict: Pass, subject to the Lead's ruling on the one open README §6 scoping item.** Every
mechanical fix required by Phase 3 is present, correct, and does not reintroduce the defect class
this round exists to remove.
