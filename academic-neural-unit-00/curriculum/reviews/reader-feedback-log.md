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

| Class                                                        | What it looks like                                                                                                                                                                                                                | Why it happens                                                                                                                                                                                                                                                                                                       | Prevention                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bilingual bold-text CommonMark break**                     | `**TERM（GLOSS）**紧跟中文` renders literally as `**...**` instead of bold                                                                                                                                                        | A closing `**` immediately preceded by punctuation (`）`, quotes, etc.) and immediately followed by CJK text with no space fails CommonMark's right-flanking test — this is _not_ the same as ordinary bold-next-to-Chinese (which is fine when the character before the closer is a CJK ideograph, not punctuation) | When a bolded span ends in a parenthetical gloss like `（ACRONYM）`, always leave a space between the closing `**` and the Chinese text that follows                                                                                                                                                                                                                                                              |
| **Bilingual enumerated lists colliding in numbering**        | An English `1.–4.` ordered list immediately followed by a Chinese ordered list meant to restart at 1, rendering as `5.–8.` instead                                                                                                | Two adjacent Markdown ordered lists with no non-list content between them share one numbering namespace under CommonMark's loose-list rules                                                                                                                                                                          | Never present bilingual enumerated/parallel content as two adjacent ordered lists — use one bilingual table instead (also solves the next class)                                                                                                                                                                                                                                                                  |
| **Prose bundling of parallel "type/stage/category" content** | 3–6 short, parallel items (bold term + ~1 paragraph each) bundled into one dense EN paragraph + one dense CN paragraph                                                                                                            | Natural first-draft shape for enumerable content; not caught by looking at any single paragraph in isolation                                                                                                                                                                                                         | Default to a table (`Term \| EN \| 中文`, `#` column only when order matters) whenever a passage names 3+ parallel items each with a short description                                                                                                                                                                                                                                                            |
| **Canonical-term drift**                                     | A module establishes a precise translation (e.g. `提示词` for "a prompt") but an earlier passage in the _same document_ (often the title) still uses a looser/ambiguous synonym (`提示`)                                          | The canonical term is usually decided while drafting the body, and titles/intros written first or last aren't swept back over                                                                                                                                                                                        | Fix the canonical term once, early in the document (ideally in the title/§1), then grep the rest of the same document for looser synonyms before filing                                                                                                                                                                                                                                                           |
| **Half-width ASCII punctuation in Chinese prose**            | `?` `!` `,` `:` `;` `(` `)` used as sentence/heading punctuation in Chinese text, instead of `？` `！` `，` `：` `；` `（` `）`                                                                                                   | Appears concentrated by author, not randomly — one contributor's four modules account for the large majority of instances found so far                                                                                                                                                                               | Needs a per-author style pass, not a blanket find-replace (ASCII punctuation is correct inside code spans, tool names, and genuine English/acronym text) — see the still-open item in Entry 2                                                                                                                                                                                                                     |
| **Straight quotation marks in Chinese prose**                | `"..."` (ASCII straight quotes) used inside Chinese-language text, instead of `“…”` (full-width curly, GB/T 15834)                                                                                                                | First-draft authoring habit carried over from English typing conventions; not visually obvious in a monospace editor since straight and curly quotes both look like "quotes"                                                                                                                                         | Convert a straight-quote pair to curly only when the quoted content contains a CJK character (mask code/math/link spans first); quotes wrapping genuine English words/acronyms/code stay straight — see Entry 4                                                                                                                                                                                                   |
| **Mid-paragraph CJK-CJK line break**                         | A paragraph hard-wrapped mid-sentence where both the character before and after the line break are CJK ideographs; CommonMark renders the break as a literal space, visible as a stray gap between two Chinese characters         | Leftover hard wraps from before `proseWrap: preserve` was set in `.prettierrc` (2026-06-18) — the current config prevents new instances but never touched pre-existing ones                                                                                                                                          | Join only at CJK-CJK boundaries (no space); leave non-CJK boundaries alone since they render identically as a space either way — see Entry 4                                                                                                                                                                                                                                                                      |
| **Hand-typed curly quote direction mismatch**                | A hand-authored edit types `”…”` (both characters the _closing_ glyph, U+201D) instead of `“…”` (opening U+201C, closing U+201D) — renders visually indistinguishable from correct curly quotes in most editors/terminals         | Copy-pasting or re-typing already-curly text from a prior Read/tool-output render can silently drop the open/close distinction, since both glyphs read as "a curly quote" to the eye                                                                                                                                 | After any hand-typed curly-quote edit, run a nesting-depth balance scan (`“` +1 / `”` −1, flag any point the count goes negative) rather than eyeballing the diff — see Entry 4                                                                                                                                                                                                                                   |
| **Non-ordinal-marked prose bundling**                        | 2+ parallel bold-term definitions bundled into one paragraph with no "first/second/third" or "第一/第二/第三" marker at all — e.g. `introductory/02` §4's "a **query** vector...; a **key** vector...; and a **value** vector..." | A grep-based sweep for ordinal markers only finds enumerations that happen to use them — this shape is common even without markers, and earlier searches (`第一...第二` grep) structurally could not find it                                                                                                         | Full-text (non-grep) close-reads are required to close this gap; the teachable signal is 2+ occurrences of `a/an **BOLD_TERM** ... represents/means/is "..."` joined by semicolons in one paragraph, independent of numbering — see Entry 6. Guardrail: don't table a passage where the bold terms are bound by one continuous narrative metaphor rather than standing as independently substitutable definitions |

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

### Entry 4 — 2026-08-21 — Quote-mark convention, mid-paragraph CJK line breaks, temperature-parameter currency, bundled enumerations

**Reported (7 items, this round):** (1) curly-quote/punctuation issues in Chinese content — readers
specifically called out "curly braces" and straight double quotation marks — remain unresolved. (2)
`提示注入` (should be `提示词注入`) still findable somewhere in the curriculum. (3) the newest Claude
models no longer support adjusting `temperature`, but `introductory/05` doesn't mention this. (4)
Prettier-formatted Markdown line breaks produce awkward spacing in Chinese text. (5) `Introductory
06`'s "Memory Types" content should be a table, not one dense paragraph. (6) the corpus uses the
English-style em dash (`——`) in Chinese text, reading like raw machine translation. (7)
first/second/third-style enumerations should be lists or separate paragraphs, not bundled prose.
The CEO authorized consulting the company's Chinese and English linguists (Localization
Department) for the judgment calls this round required.

**Investigation and resolution, item by item:**

- **(1) Quote marks.** Consulted Wei-Chen Liu (Chinese Linguist) — full response recorded below.
  Ruling: ZH-CN prose under GB/T 15834 uses full-width curly quotes `“…”` (U+201C/U+201D), not
  corner brackets `「」` (a ZH-TW/HK convention). The entire curriculum — 1,513 straight-quote
  characters across every file — used straight ASCII `"..."` even in Chinese content; zero curly
  quotes or corner brackets existed anywhere in the corpus before this entry. Wrote a masked
  conversion script (fenced/inline code, `$...$`/`$$...$$` math, Markdown link targets, and bare
  URLs protected, mirroring Entry 3's masking approach) that converts a straight-quote pair to
  curly only when the quoted content contains a CJK character, leaving quotes wrapping genuine
  English words/acronyms/code untouched, per the linguist's boundary ruling. Converted 563 quote
  pairs across 24 curriculum files + `README.md`; verified 0 remaining straight-CJK pairs after.
  Also investigated the readers' "curly braces" wording literally: excluding fenced/inline code and
  LaTeX math spans (which legitimately use `{}` for subscripts/superscripts), the corpus has zero
  genuine stray `{}` in prose — concluded this was reader shorthand for "curly quotation marks,"
  the defect actually addressed above, not a separate brace-glyph issue.
- **(2) `提示注入` → `提示词注入`.** Found and fixed the one remaining instance
  (`introductory/05:260`, inside the Common Pitfalls table's parenthetical gloss on prompt
  injection). Re-swept the full corpus after: 0 remaining instances of the incorrect form, 9
  (now correct) instances of `提示词注入`. Wei-Chen Liu independently confirmed both `提示词` (not
  `提示`) and `提示词注入` (not `提示注入`) as the correct standing terms for this curriculum's
  register.
- **(3) Temperature-parameter currency.** Verified against current Anthropic documentation and the
  Claude API migration guide (retrieved 2026-08-21): `temperature` remains a supported, adjustable
  parameter for most current models, but Anthropic's newest releases — Claude Opus 4.7 and later,
  and Claude Sonnet 5 — reject a non-default `temperature` (and `top_p`/`top_k`) with a request
  error, on the stated rationale that prompting is now a more reliable behavior lever than
  sampling-layer tuning for these models. Rewrote `introductory/05`'s temperature passage (both EN
  and CN) to keep the underlying sampling-randomness concept intact (still universally applicable)
  while adding an accurate, hedged, dated caveat that direct adjustability is model- and
  provider-specific and changes over time, directing readers to check the current API reference for the model they're
  actually calling rather than asserting a single fixed fact that will itself go stale.
- **(4) Mid-paragraph CJK line breaks.** Root cause: 784 mid-paragraph line breaks where both the
  character before and after the break are CJK ideographs, spread across 12 files — leftover hard
  wraps from before this repo's `.prettierrc` set `proseWrap: preserve` (2026-06-18 per git
  history); Prettier itself was not the ongoing cause; the current config already prevents new
  instances. CommonMark renders a soft line break as a literal space in HTML, which is invisible
  and correct between English words but reads as a stray gap between two Chinese characters that
  have no natural word boundary. Considered and rejected a full paragraph-per-line unwrap (a dry
  run found 6,229 non-CJK boundary breaks that render identically whether joined or not — unwrapping
  those would have been a much larger, cosmetic-only diff, and would have touched historical
  `reviews/` records that should never be edited per this log's own maintenance rule); scoped the
  fix to exactly the CJK-CJK boundary joins that produce a visible rendering defect. Applied and
  spot-checked; `prettier --check` clean afterward.
- **(5) `introductory/06` Memory Types.** Confirmed §7 "Two Kinds of Memory" bundled 2 parallel
  concepts (working memory / persistent memory, the latter itself naming a short-term/long-term
  split) into one dense EN paragraph + one dense CN paragraph — the same "prose bundling of
  parallel type/category content" defect class from Entry 1. Converted to a `Term | EN | 中文`
  table, preserving the explanatory "why this distinction matters" paragraph as prose since it is
  narrative, not enumerable.
- **(6) Em dash.** Consulted Wei-Chen Liu jointly with Amelia Hartington (English Linguist) —
  full response recorded below. Ruling: `——` (doubled U+2014) **is** the correct GB/T 15834 standard
  for ZH-CN prose; the corpus's 968 doubled-dash instances are compliant, not a defect. No genuine
  stray single `—` mid-Chinese-sentence was found; the earlier raw grep's ~3,959 "single dash"
  count was an artifact of naive character counting on already-doubled dashes plus legitimate
  single em dashes inside English-language table cells. **No mechanical fix applied** — this is a
  closed non-defect, not a deferred item. The linguists' joint diagnosis of the actual "reads like
  MT" signal: appositive clauses transplanted sentence-for-sentence from English via `——` instead of
  being restructured into two shorter Chinese sentences — a sentence-construction/rhythm concern,
  not a punctuation-mark defect, and out of scope for a mechanical pass (would require a
  clause-by-clause native-flow rewrite across the corpus). Recorded as a new Defect Class below for
  future authoring awareness, not as an action item.
- **(7) Bundled first/second/third enumerations.** Grep for `第一...第二[...第三]` and
  `First,...Second,` found 9 files with the pattern; most were false positives (`第一行`/`第二维` =
  "first row"/"second dimension" in worked math examples, not enumerated lists). Of the genuine
  enumerations, converted the four **3+-item** cases to tables, matching this log's established
  convention (`intermediate/08`'s 4-item worked-example checklist, `advanced/06`'s 4-stage RAG
  pipeline, `advanced/07`'s 3 worktree-lifecycle properties, `advanced/05`'s 3 foundational facts).
  Left the **2-item** "first/second" instances as connected prose
  (`intermediate/05`, `intermediate/06`, `advanced/05`'s YaRN passage) — a 2-item enumeration reads
  naturally as one sentence in both languages and the reader's own example (First/Second/**Third**)
  implies 3+ items as the actual pattern of concern; recording this boundary explicitly so a future
  pass doesn't re-flag 2-item prose as a defect. One incidental finding: `advanced/07`'s 3-property
  passage had **no English counterpart at all** in the source (Chinese-only prose, unlike the
  rest of the file's strict paragraph-by-paragraph bilingual structure) — added a translated EN
  column to complete the table rather than leaving one column empty, since every other table in the
  curriculum is fully bilingual.

**Linguist consultation (Localization Department, activated per CEO authorization):**

> **Q1 — Quote marks: rule is `“ ”` (U+201C/U+201D), not `「」`.** `「」` corner brackets are the
> Taiwan/Hong Kong (and classical vertical-text) convention, not Mainland. GB/T 15834 for ZH-CN
> horizontal-text prose specifies full-width curly quotes as primary (`“…”`, nested `‘…’`). Since
> this curriculum is ZH-CN only, that's a one-line rule: every straight `"..."` wrapping
> Chinese-language content → `“…”`. Boundary: quotes wrapping genuine embedded English
> words/acronyms/code stay straight ASCII — standard mixed-script practice.
>
> **Q2 — `——` is correct standard; don't mechanically "fix" singles.** The corpus has essentially
> no genuine stray single `—` mid-Chinese-sentence acting as a parenthetical break — the scanner's
> hits are English-language table cells (correct English style) and chain/sequence usage like
> `感知—思考—行动—观察` (a linking dash, closer to a range-dash, which GB/T 15834 permits). The
> "reads like MT" complaint isn't the dash glyph — it's sentence construction: long English-style
> appositive clauses transplanted via `——` instead of being restructured into two shorter Chinese
> sentences with 句号/分号. Flag any `——`-bounded clause over ~25 characters for a native-flow read;
> don't touch the mark itself. (Amelia Hartington, English Linguist: agreed from the English side —
> a reader trained on English prose pattern-matches `—` to "raw MT," but the actual signal to audit
> is appositive-clause length, not dash presence.)
>
> **Q3 — Confirmed, both terms, corpus already compliant.** `提示词` (not `提示`) is correct —
> `提示` alone reads as generic "hint," ambiguous with UI tooltips. `提示词注入` (not `提示注入`) is
> the standard security-literature rendering. Grepped: 9/9 instances already use `提示词注入`
> (after this entry's item (2) fix), zero use the bare incorrect form.
>
> — Wei-Chen Liu, Chinese Linguist (ZH-CN/ZH-TW), Localization Department

**Self-caught defect during this entry (not reader-reported):** two of the hand-authored table
edits for items (5) and (7) introduced curly quote pairs where both the opening and closing
character were typed as U+201D (closing) instead of U+201C/U+201D — invisible in the editor,
detectable only by scanning actual codepoints. Caught by a post-edit balance scan (tracking curly
quote nesting depth across each file; a `”` at depth 0 flags a malformed pair) run specifically
because manual quote-typing is more error-prone than the scripted conversion used for item (1).
Found and fixed 2 instances (`introductory/05`, `advanced/05`). Added as a new Defect Class below.

**Status:** Closed. Items (2), (3), (4), (5), (7) fixed and verified; item (1) fixed and verified
corpus-wide; item (6) investigated and closed as a non-defect (correct standard punctuation, not a
mechanical fix candidate). No standing open items from this entry.

---

### Entry 5 — 2026-08-21 — Non-curriculum ANU-00 documents audited for the same defect classes (null result)

**Reported:** request to check whether the defect classes from Entry 4 also exist in ANU-00
documents outside `curriculum/`.

**Investigation:** scanned every ANU-00 document outside `curriculum/` — `formation/`, `crew/`,
`knowledge-base/` (README only; no research entries filed yet), `templates/`, `plans/` — 26
markdown files total, plus a workspace-wide sweep of `company/`, `studio/`, and
`core-component-00/` as an FYI check beyond the confirmed scope.

**Finding:** none of the catalogued defect classes exist anywhere outside `curriculum/`, because
no other document set in this workspace is bilingual. The only CJK characters found anywhere
outside `curriculum/` are 3 isolated mentions of **信达雅** (the classical Chinese
translation-quality principle), used correctly as an embedded English-language citation term
inside review-template prose — not bilingual paragraph content, so none of the quote/line-break/
enumeration defect classes have any Chinese prose to occur in. A workspace-wide sweep for files
with more than 20 CJK characters returned zero hits outside `curriculum/`.

**Status:** Closed, no defect found, no files changed. `curriculum/` is confirmed as the entire
bilingual surface area in this workspace.

---

### Entry 6 — 2026-08-21 — Bundled-prose-to-table sweep beyond ordinal markers (28 conversions)

**Reported:** a reader found further readability candidates beyond the tables added in Entry 1–4 —
specifically `introductory/02` §4 "Queries, Keys, and Values," which bundles three parallel
term-definitions (query/key/value) into one dense paragraph per language with **no ordinal
markers at all** ("first/second/third"), unlike every candidate the earlier entries' grep-based
searches had found.

**Investigation:** the earlier sweeps (Entry 1's two passes, Entry 2's structural scan) searched
specifically for `第一...第二` / `First,...Second,` patterns. That methodology has a real blind
spot: it misses (a) bundled definitions with no ordinal markers at all (the query/key/value
shape), (b) ordinal enumerations written as 首先/其次/第三/第四 instead of 第一/第二/第三, and (c)
English "First,...Second," pairs split across wrapped physical lines, invisible to single-line
grep. Dispatched 6 parallel full-text (non-grep) reads across all 24 curriculum files to find
every remaining instance of the underlying pattern — "2+ parallel items, each a bold term plus a
short description, bundled into one paragraph" — regardless of marker style. Consulted Wei-Chen
Liu (Chinese Linguist) and Amelia Hartington (English Linguist) to confirm the rule itself was
sound and only the search method was too narrow, to get a general non-ordinal-dependent detection
signal for future authoring, and to flag the over-application risk: a paragraph with 2-3 bold
terms bound by one continuous narrative metaphor (e.g. the library-catalog analogy immediately
after `introductory/02` §4) should **not** be tabled, since tabling breaks the connective tissue
the metaphor depends on — the signal is whether clauses are independently substitutable, not raw
bold-term count.

**Result:** 25 confirmed candidates + 9 borderline cases across 18 files. Reported to the reader
and CEO for scope sign-off before any edits, per instruction. Approved scope: 27 conversions to
table (25 confirmed + 2 borderline 2-item cases matching an existing sibling-table precedent —
`introductory/07` §6, `introductory/08` §3), 1 conversion to a bullet list instead of a table
(`introductory/06` §1's unlabeled skill-objective list, which has no "Term" column to speak of),
6 left as prose (each with a specific disqualifying reason — sequential rather than parallel
build, argumentative definition-by-negation, independent binary pairs, technical content too long
for table cells, glossary-shaped, or a clean 2-item case with no sibling-table precedent).

**Resolution:** executed via 7 parallel editing passes (1 done directly, 6 dispatched agents) across
15 files:

| File              | Sections converted                                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `introductory/01` | §4 Activation Functions, §5 Layers and Forward Propagation                                                                           |
| `introductory/02` | §4 Queries, Keys, and Values; §9 The Transformer Block                                                                               |
| `introductory/04` | §2 What Is a Tool or Function; §3 The Function-Calling Contract; §8 Tool Use Across Providers                                        |
| `introductory/05` | §3 Roles: System, User, and Assistant                                                                                                |
| `introductory/06` | §9 Practical Takeaways (table); §1 Why This Module Exists (bullet list, not table)                                                   |
| `introductory/07` | §6 Communication; §8 Risks Unique to Multi-Agent Systems                                                                             |
| `introductory/08` | §2 Defining "Evaluate"; §3 Two Different Questions                                                                                   |
| `intermediate/01` | §5 The Bias–Variance Tradeoff                                                                                                        |
| `intermediate/05` | §6 Worked Example                                                                                                                    |
| `intermediate/06` | §3 Measuring Meaning; §8 The Full RAG Pipeline; §12 Failure Modes and Practical Takeaways                                            |
| `intermediate/07` | §6 Coordinator Role and Swarm Topologies (restates a passage `introductory/07` §4 already tabled in Entry 1 — this copy hadn't been) |
| `intermediate/08` | §1 Informal Test Set → Formal Benchmark; §3 A Tour of Named Agent Benchmarks                                                         |
| `advanced/03`     | §5 Circuit Breaker states                                                                                                            |
| `advanced/04`     | §4 Harness-Level Guardrail Patterns; §7 Governance Frameworks (NIST AI RMF)                                                          |
| `advanced/07`     | §2 Recap: Orchestration Topologies; §5 Foundations of Distributed Consensus; §6 Raft sub-problems                                    |

All EN/中文 cell text is a near-verbatim split of the original prose — no paraphrasing, no content
addition. `advanced/07`'s three new tables did not hit the "CN-only source, no EN counterpart"
quirk found in a prior round's table there — all three had matching EN and CN prose to draw from.
Centralized post-processing (masked curly-quote conversion, CJK-CJK line-join check, `prettier
--write`) was re-run across every touched file afterward; two self-caught instances of the
hand-typed curly-quote-direction defect (both quote characters typed as the closing glyph) were
found via the balance-scan check from Entry 4 and fixed — both in `introductory/02`, in content
this session authored directly rather than via a dispatched agent.

**Linguist verification (per explicit instruction, run after all edits landed):** Wei-Chen Liu and
Amelia Hartington sampled 8 of the 28 conversions across 5 files (including the bullet-list
conversion and the densest tables — `intermediate/08` §3's 5-benchmark table and `advanced/07`
§5–§6's consensus-theory tables) plus a targeted terminology grep across the newly-touched files.
**Verdict: GO.** Translation fidelity clean across the sample (no drift, no silent omission, no
compression that drops meaning); canonical terminology held correctly (提示词注入, 共识, 词元,
自洽性, etc.); curly-quote convention correctly applied inside table cells; no case where
tabularization forced meaning-losing terseness. One non-blocking style note: `intermediate/05` §6
uses half-width parentheses for section references, matching the surrounding prose in that same
document rather than introducing a new inconsistency — not a defect from this round, and a
document-wide full-width-parens sweep (if ever wanted) would be a separate, deliberately scoped
effort, not something to retrofit here.

**Status:** Closed. All 28 approved conversions applied and linguist-verified. No standing open
items from this entry.

---

## Standing Open Items

Carried forward across entries until resolved — check this list before filing a new entry, in
case a new reader report turns out to be the same already-known item.

None currently open.
