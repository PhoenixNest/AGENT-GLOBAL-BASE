# Phase 1 Audit — Workspace-Internal Jargon & Context-Assuming Passages

**Round:** 2026-08-26 external-audience remediation
**Scope:** All 24 curriculum modules plus `curriculum/README.md`, per
`academic-neural-unit-00/plans/2026-08-26-curriculum-external-audience-remediation/external-audience-remediation-plan.md`
§6 Phase 1, item: "full-text (non-grep) read for workspace-internal jargon, tooling, or
org-structure references in body text beyond the already-known `advanced/07` passage."
**Method:** Every module was read in full for tone and framing, not sampled. Targeted pattern
scans (workspace, repository, internal file-path prefixes, org-process vocabulary, EN and ZH)
were used to cross-check the manual read for anything missed, not as a substitute for it.

---

## 1. Confirmed: the known `advanced/07` §4 passage

`advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md` §4 ("Git Worktree
Isolation as Multi-Agent Infrastructure," lines ~138–251) is the only module whose body prose
assumes workspace-internal context, beyond citation paths already covered in the companion
links-and-citations audit. Specifically:

- Lines 138, 168, 171, 240, 247 (EN) and their ZH counterparts at lines ~134, 237, 247 refer to
  "this workspace's own multi-agent engineering practice," "this workspace's own five-phase
  lifecycle," and "the rule this workspace now enforces" — all describing a real internal incident
  (a Windows directory junction accidentally deleting shared cache content via
  `git worktree remove`) as if the reader is a member of this workspace and can look the incident
  up. An outside reader has no way to verify this happened, or that the described rule is actually
  enforced anywhere.
- This is the same defect class as the citation finding in the companion report, applied to prose
  rather than a citation path — confirms this is one coherent passage to remediate, not two
  separate defects.

No comparable passage exists anywhere else in the 24 modules — every other module's worked
examples, case studies, and failure-mode discussions use either a generic/hypothetical scenario or
a citable public source (per README §5's citation rule), which is why Pass 1–4 never flagged
anything beyond this one passage: it is genuinely the only one.

## 2. New finding: `curriculum/README.md` §6 mixes reader-facing and ANU-00-internal content

Not a module, and not previously in scope for Pass 1–4 (which reviewed modules, not the README),
but explicitly named as in-scope for this remediation round by plan §2 item 1 (the link mesh
includes `curriculum/README.md`). Reading the whole file surfaced something beyond links: §6
("Review Process," lines ~320–420) describes ANU-00's internal review pipeline in operational
detail — naming Dr. Mokoena by name and role, citing
`crew/lead/naledi-mokoena/skills/research-programme-chartering.md` (a workspace-relative path to a
non-curriculum file, outside the pattern the companion links audit scripted for), describing what
gets escalated "to the CEO," and instructing a reader to "raise the conflict with Dr. Mokoena."

This reads as internal process documentation for whoever runs ANU-00's own review cycles, embedded
in the same file as the curriculum's public-facing overview and module index. It is a materially
different kind of content from the `advanced/07` passage (that was a case study inside a lesson;
this is the README's own "how we produce this" appendix) and raises a scoping question this audit
should surface rather than resolve unilaterally, per the plan's standing instruction not to decide
the author-metadata question (§2 item 5) without the Lead/CEO: **should README §6 travel to the
hosted site as-is (an outside reader sees ANU-00's internal review mechanics), be marked
internal-only / excluded from the hosted export, or be rewritten as a generic "how these modules
are reviewed" description without named individuals and internal file paths?** Flagged for Phase 2
/ Phase 4 Lead synthesis to rule on. Not counted as a body-text jargon defect requiring the same
fix as `advanced/07`, because it may not be a defect at all depending on how that scoping question
is resolved — but it cannot be silently left unaddressed either.

## 3. Checked and cleared: everything else

The following were checked corpus-wide and found **not** to be defects:

- **`curriculum/README.md` line 25**, "a curriculum benchmarked only against this workspace's own
  conventions would teach a reader to pass here and nowhere else" — this is the README's own
  citation-rule rationale, actively warning against the exact defect this remediation exists to
  fix. Correctly framed; not a violation.
- **`curriculum/README.md`'s framing of the intended reader** ("a new ANU-00 or CC-00 joiner with
  no prior background...", line 15) — this is a positioning/audience statement, not a
  repository-dependent reference. It may be worth revisiting given the CEO's broader-audience
  ruling, but that is a scope/positioning question for the Lead, not a "reader can't follow a
  citation" defect this audit is scoped to find. Flagged for awareness, not treated as an item
  needing a mechanical fix.
- **`advanced/05`'s `core-component-00/engineering/context-engineering/` mention** — a citation-
  path defect, already captured in the companion links-and-citations audit (§2 there); not
  duplicated here since it's a citation, not free-standing jargon.
- No other module contains the strings "this repository," "this workspace," "AGENT-GLOBAL-BASE,"
  "CLAUDE.md," ".claude/," "company/," or "studio/" anywhere in body text (verified by full-corpus
  grep, zero hits outside the two flagged locations).
- No module assumes the reader has access to any other workspace-internal document, tool, or named
  individual beyond the two findings above.

---

**Handoff to Phase 3:** one substantive rewrite needed (`advanced/07` §4, per the companion
citations audit's recommended treatment), one open scoping question to raise at Phase 2
(`curriculum/README.md` §6), and everything else in the 24-module corpus is already clean on this
dimension.
