# Reader Feedback Log

A continuous, append-only record of issues external readers report against the shipped
curriculum, and the revisions made in response. This is distinct from the formal review rounds
under `reviews/YYYY-MM-DD-<round-slug>/` (`reviews/README.md`), but lives in the same category —
`reviews/` — because it is still evidence of what the curriculum's actual quality bar has been in
practice.

**How this differs from a formal review round:** a round in `reviews/YYYY-MM-DD-<round-slug>/` is
a point-in-time, named-reviewer verdict against `templates/curriculum/internal-review-report.md` —
independence declaration, per-document pass/fail, severity-graded problems table. This log is
none of that. It has no reviewer-of-record and no pass/fail verdict; it exists purely to capture
**what a reader reported, why it happened, and what was done about it**, as one running document
rather than a new dated folder per report. Its purpose, per the CEO's request that opened this
log, is to build institutional memory so the same defect class is caught earlier — ideally at
authoring time — in future textbook development, not to gate a release.

**Maintenance rule:** append new entries; do not edit or delete prior entries once filed, for the
same reason a filed review report is never edited (`templates/curriculum/internal-review-report.md`
header note) — this log is only useful as a history if it stays one.

---

## Defect Classes Identified So Far

Patterns worth watching for at authoring time, extracted from the entries below. These are the
actionable takeaways for future module authors, not just a changelog.

| Class                                                        | What it looks like                                                                                                                                                                       | Why it happens                                                                                                                                                                                                                                                                                                       | Prevention                                                                                                                                                                                    |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bilingual bold-text CommonMark break**                     | `**TERM（GLOSS）**紧跟中文` renders literally as `**...**` instead of bold                                                                                                               | A closing `**` immediately preceded by punctuation (`）`, quotes, etc.) and immediately followed by CJK text with no space fails CommonMark's right-flanking test — this is _not_ the same as ordinary bold-next-to-Chinese (which is fine when the character before the closer is a CJK ideograph, not punctuation) | When a bolded span ends in a parenthetical gloss like `（ACRONYM）`, always leave a space between the closing `**` and the Chinese text that follows                                          |
| **Bilingual enumerated lists colliding in numbering**        | An English `1.–4.` ordered list immediately followed by a Chinese ordered list meant to restart at 1, rendering as `5.–8.` instead                                                       | Two adjacent Markdown ordered lists with no non-list content between them share one numbering namespace under CommonMark's loose-list rules                                                                                                                                                                          | Never present bilingual enumerated/parallel content as two adjacent ordered lists — use one bilingual table instead (also solves the next class)                                              |
| **Prose bundling of parallel "type/stage/category" content** | 3–6 short, parallel items (bold term + ~1 paragraph each) bundled into one dense EN paragraph + one dense CN paragraph                                                                   | Natural first-draft shape for enumerable content; not caught by looking at any single paragraph in isolation                                                                                                                                                                                                         | Default to a table (`Term \| EN \| 中文`, `#` column only when order matters) whenever a passage names 3+ parallel items each with a short description                                        |
| **Canonical-term drift**                                     | A module establishes a precise translation (e.g. `提示词` for "a prompt") but an earlier passage in the _same document_ (often the title) still uses a looser/ambiguous synonym (`提示`) | The canonical term is usually decided while drafting the body, and titles/intros written first or last aren't swept back over                                                                                                                                                                                        | Fix the canonical term once, early in the document (ideally in the title/§1), then grep the rest of the same document for looser synonyms before filing                                       |
| **Half-width ASCII punctuation in Chinese prose**            | `?` `!` `,` `:` `;` `(` `)` used as sentence/heading punctuation in Chinese text, instead of `？` `！` `，` `：` `；` `（` `）`                                                          | Appears concentrated by author, not randomly — one contributor's four modules account for the large majority of instances found so far                                                                                                                                                                               | Needs a per-author style pass, not a blanket find-replace (ASCII punctuation is correct inside code spans, tool names, and genuine English/acronym text) — see the still-open item in Entry 2 |

---

## Log Entries

### Entry 1 — 2026-08-20 — Loop-mechanism table + bilingual numbering (introductory/03)

**Reported:** (1) `introductory/03`'s loop-mechanism content ("types" of loop stages) would read
better as a table than prose. (2) Chapter 3's Chinese list numbering starts at 5 instead of 1,
caused by bilingual Markdown list continuation.

**Investigation:** both complaints traced to the same passage — §3 "The Agent Loop"
(Perceive/Think/Act/Observe) presented as two adjacent ordered lists (EN `1.–4.`, CN literal
`5.–8.`). Confirmed via corpus scan that this two-adjacent-ordered-lists shape was isolated to
this one section — not repeated elsewhere in the curriculum at the time.

**Resolution:** restructured into a single bilingual table (`# \| Stage \| EN \| 中文`). Eliminates
the numbering-collision defect structurally, not just cosmetically.

**Follow-up (same session):** user asked about §8 "Common Failure Modes," which had the identical
bundled-prose shape and had been missed because the first pass only reviewed §3. Fixed the same
way (table, no `#` column — order doesn't matter for failure modes).

**Broader sweep — first pass:** applying the same two-lens check (table-vs-prose, bilingual
list-numbering) across the rest of the curriculum found 4 more table candidates:
`introductory/07` §3 "Types of Agent Interaction" and §4 "Architectures," `advanced/05` §7
"Context Budgeting," `advanced/04` §2 "The Threat Model" (two-level table). All fixed. The
bilingual-numbering defect itself was confirmed isolated to `introductory/03`'s original §3 — no
recurrence found elsewhere.

**Broader sweep — second pass:** a full-text (non-keyword-guided) re-read of all 24 curriculum
files, done specifically to close the coverage gap that let §8 get missed by the first pass's
grep-guided search, found 13 more instances across 10 files: `introductory/05` §8,
`introductory/08` §7, `intermediate/01` §6, `intermediate/05` §7, `intermediate/07` §8,
`intermediate/08` §5, `advanced/03` §2, `advanced/05` §7 (technique list) and §9,
`advanced/06` §7 and §8, `advanced/08` §1 and §12.

**Status:** Closed. 19 sections converted to bilingual tables total across this entry's two sweep
passes. One deliberately-not-fixed candidate noted and left as-is:
`intermediate/04`'s episodic/semantic/procedural memory preview (lines ~108–117) — each kind
already gets a full dedicated section immediately after, so a table there would be a redundant
summary rather than a primary presentation. Not a defect; recorded here so a future pass doesn't
re-flag it without re-deriving this reasoning.

---

### Entry 2 — 2026-08-21 — Bold-rendering bug, prompt-anatomy table, title translation (introductory/04, introductory/05)

**Reported:** (1) In `introductory/04`, bold text around "JSON (JavaScript Object Notation)"
doesn't render as bold, even in Markdown preview — reader suspected a missing-space issue common
in Chinese formatting. (2) In `introductory/05` §2 "The Anatomy of a Prompt," the prompt's
structural composition is explained in prose and would read better as a table. (3) In
`introductory/05`'s Chapter 1 title, the Chinese translation uses half-width `?` instead of
full-width `？`, and translates "Prompt" as `提示` (a generic "hint/cue") rather than the more
precise `提示词` used elsewhere.

**Investigation:**

- **(1)** confirmed root cause: not a generic "bold next to Chinese" problem (that pattern is
  common throughout this curriculum and renders fine) — specifically, a closing `**` immediately
  preceded by punctuation (`）` from an acronym gloss) and immediately followed by CJK text with no
  space fails CommonMark's right-flanking emphasis rule. A full-corpus structural scan (not
  grep-only) found 9 confirmed instances of this exact trigger across 8 files:
  `introductory/04`, `intermediate/01`, `intermediate/02` (×3), `intermediate/07`, `advanced/07`
  (×2). See Defect Classes table above for the general rule.
- **(2)** confirmed: `introductory/05` §2 bundles 4 parallel items (Instruction / Context / Input
  data / Output indicator) as parallel EN/CN bullet lists. The same file's §8 (fixed in Entry 1)
  already uses a table for identically-shaped content, so this reads as an oversight, not a
  judgment call.
- **(3)** confirmed both parts of the title issue. Cross-checked against `提示词` used
  consistently as the file's own canonical term from §1 onward — the title's bare `提示` directly
  contradicts the term the file itself establishes one paragraph later. Checking the rest of the
  curriculum for the same drift found 4 more candidates needing human judgment (not mechanical —
  `提示` legitimately means something else in several of these), plus 2 more headings with the
  same half-width-punctuation issue (`advanced/06` H1 subtitle, `advanced/05`'s YaRN subsection
  heading).
- **Prior-review cross-check:** found and read the existing `reviews/2026-08-18-first-review-cycle/`
  and `reviews/2026-08-19-remediation-review/` rounds. None of these three issues were previously
  tracked, **except** that the half-width-punctuation half of issue (3) is the same defect class
  as an already-identified, already-approved-in-principle-but-never-executed finding from Pass 4:
  864 instances of half-width `,`/`:`/`;` after CJK text, concentrated entirely in one
  contributor's four modules (`introductory/05`, `intermediate/05`, `advanced/05`, `advanced/06`).
  That prior scan never checked `?`/`!`, which is why this title's `?` wasn't already on record.

**Resolution — applied:**

- All 9 confirmed bold-rendering breaks fixed (space inserted after the closing `**`).
- `introductory/05` §2 converted to a table matching §8's exact format.
- Title fixed: `**什么是大语言模型?什么是提示?**` → `**什么是大语言模型？什么是提示词？**`.
- The 2 additional heading-punctuation instances fixed (`advanced/06` H1, `advanced/05` YaRN
  heading).

**Resolution — deliberately deferred, not fixed:**

- The 4 secondary `提示`→`提示词` candidates (`introductory/05:216`, `advanced/03:345`,
  `advanced/07:639`, `intermediate/08:199`) — each needs a human judgment call on whether that
  instance means "the LLM prompt" (should change) or a different legitimate sense of `提示`
  ("notice," "indication," a different compound) — not appropriate for a mechanical fix.
- The 864-instance half-width-punctuation backlog across the same contributor's four modules —
  substantially larger in scope than this entry's reader-reported issues, was flagged by Pass 4
  but never formally approved for execution. **Still open; needs an explicit go/no-go decision**,
  independent of this log.

**Status:** Closed for the items listed as applied. Two items remain open and are carried forward
as standing action items below, not closed by this entry.

---

### Entry 3 — 2026-08-21 — Standing open items resolved: punctuation tidy + terminology fixes

**Reported:** N/A — this entry closes out both items the CEO left standing at the end of Entry 2,
rather than responding to a new external reader report.

**Item 1 — half-width→full-width punctuation tidy (Dr. Tan's 4 modules).** Executed as a scoped
mechanical tidy using a Python script rather than by hand, per the reliable signal established
during Entry 2's bold-rendering-bug investigation: a half-width `,`/`:`/`;`/`?`/`!` is genuine
Chinese prose punctuation — and safe to convert — only when the character immediately before it
or immediately after it is a CJK ideograph (U+4E00–U+9FFF); everything else (fenced code blocks,
inline code spans, URLs, and markdown link targets) was masked out before the conversion pass and
restored unchanged afterward. Widened scope beyond the original `,`/`:`/`;`-only count to the full
character set (`?`/`!` included), per Entry 2's finding that Pass 4 never checked those two marks.

Per-file conversion counts (genuine, CJK-adjacent instances only — not a raw substring count):

| File                                                                     | Conversions |
| ------------------------------------------------------------------------ | ----------: |
| `introductory/05-prompt-engineering-fundamentals.md`                     |          14 |
| `intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`   |          20 |
| `advanced/05-advanced-context-engineering-long-context-and-budgeting.md` |          25 |
| `advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`     |          24 |
| **Total**                                                                |      **83** |

This total is much smaller than the raw ~864+ figure Pass 4 originally reported — that earlier
figure was a naive substring count of `,`/`:`/`;` across each file in its entirety (references,
citations, inline code, everything), not a count filtered to genuine CJK-adjacent prose
punctuation; a same-method raw recount post-conversion still shows 987 raw `,`/`:`/`;` characters
remaining across the 4 files, confirming the vast majority of the original raw count was always
legitimate half-width punctuation inside English citations, inline code spans, and reference
URLs — never a defect, and correctly left untouched by this pass.

Verified via `git diff` review (well beyond the 10–15-instance-per-file spot-check called for):
every conversion is triggered by genuine CJK adjacency on at least one side (matching cases like
`token，呈现` and `JSON Schema，有时`, where an English word or acronym sits on one side and CJK
prose on the other, are correctly converted per the OR rule); citations and inline identifiers
that have no CJK neighbor at all (`Robertson & Zaragoza,2009`, `` `strict: true` ``,
`` `input_schema` ``) were correctly left half-width. Confirmed by direct grep that the
References-section markdown link targets (`](https://...)`) in all 4 files show zero diff lines,
and that inline code spans containing example JSON
(`` `{"sentiment": "positive"|"negative"|"mixed", "feature": "<...>"}` ``) retain their original
half-width punctuation untouched. No false-positive conversions found; no manual corrections were
needed. `npx prettier --write` then `--check` run clean on all 4 files.

**Item 2 — 4 secondary `提示`→`提示词` candidates.** Each location was read in full paragraph
context before deciding, per the instruction that these needed human judgment rather than a
mechanical fix. All 4 confirmed as the genuine "LLM prompt" sense and changed:

- `introductory/05-prompt-engineering-fundamentals.md:206` — `把提示写作当作一个设计过程`
  → `把提示词写作当作一个设计过程` (heading for "Prompting as a Design Process" — unambiguously
  about prompt-writing as an iterative practice).
- `advanced/03-agent-harness-engineering-production-grade-agent-loops.md:345` —
  `一个恶意提示无法突破沙箱` → `一个恶意提示词无法突破沙箱` (a malicious prompt attempting to
  make generated code escape the sandbox — the LLM-input sense, not a UI notice).
- `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md:639` —
  `被对抗性提示操纵` → `被对抗性提示词操纵` (an agent manipulated by an adversarial prompt in a
  multi-agent voting scenario; the same paragraph two sentences later already uses `提示词`
  correctly for the same concept, reinforcing this was drift, not a deliberate different sense).
- `intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md:199` —
  `提示设计、偏差与校准` → `提示词设计、偏差与校准` (heading translating "Prompting, Bias, and
  Calibration" — about designing the prompt given to an LLM judge).

No candidates were left unchanged — none of the 4 turned out to be a different sense of `提示` on
closer reading.

**Status:** Both standing open items below are now closed. The Standing Open Items table has been
cleared accordingly.

---

## Standing Open Items

Carried forward across entries until resolved — check this list before filing a new entry, in
case a new reader report turns out to be the same already-known item.

None currently open.
