# Pass 4 Remediation Review — ANU-00 Agent Development Curriculum (24 Modules)

**Requested by:** CEO, closing the scoped Pass 4 remediation run recommended by
`academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` (Joint Recommendation).

**Author:** Dr. Naledi Mokoena, ANU-00 Lead.

**Inputs:** the four independent re-reviews in this folder (Bhandari on `intermediate/04`,
Ibarra-Costa on `intermediate/07` and `advanced/08`, Baek on `advanced/05`); the eight authors'
remediation of their own modules; `academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` (Pass 3); `curriculum/README.md`
as amended 2026-08-18 (Amendment 1).

**Date:** 2026-08-19 — the date carried by all four re-reviews. I have not inferred any later date.

**Scope:** Whether the Pass 4 remediation run actually landed — across all 24 modules, not only
the ten flagged ones — and an updated per-document status with a shipping recommendation for the
CEO.

**Status:** For CEO decision. Closes Pass 4.

---

## 1. Method — what I personally checked

None of this section is restated from the eight authors' self-reports or from the four
re-reviewers. Pass 3 taught me that the defects that survive a review round are the ones nobody
was assigned, so I ran my own mechanical sweeps across the full 24-file corpus first and read the
sub-reports second.

| What I did myself                                                                | How                                                                                                                                                                                                                    |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C-1 — deprecated `执行框架` across **all 24** files, not just the 8 named        | Counted `执行框架` and `运行框架` per file and compared each count against Pass 3's own per-file audit (`academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` l. 61)      |
| C-2 — metadata block on **all 24** files (not a 12-file sample)                  | Read the first 12 lines of every module and diffed the block field-by-field against README §4.1's canonical Format B: three fields, bold `·`-separated line, Chinese mirror line, full roster identity, trailing `---` |
| C-3 — remaining inline glosses across **all 24** files                           | Regex sweep for the `English term（中文）` shape §4 names — an ASCII token immediately followed by a parenthesis containing CJK — then hand-classified every one of the 42 hits against the narrowed §4 rule           |
| Bilingual typography across **all 24** files                                     | Counted half-width `,` `:` `;` directly following a CJK character against their full-width counterparts, per file — the same scan that produced the 868-instance finding at Pass 3, rerun identically                  |
| H1 conformance across **all 24** files                                           | Extracted every H1 line and compared it to the README §7 module-index title                                                                                                                                            |
| The two rendering defects (`intermediate/01` l. 119, `advanced/02` l. 281)       | Read the corrected passages in both languages, then reran the corpus-wide scan for the blank-line-plus-leading-dash pattern that caused them                                                                           |
| The stray-blockquote defect (`intermediate/06`)                                  | `grep -rn "^>"` across all 24 files                                                                                                                                                                                    |
| The three orphan citations (`intermediate/01`, `advanced/01`, `introductory/08`) | Traced each cited name through the whole document body, not just the reference list — the same method as Pass 3                                                                                                        |
| `intermediate/06`'s Lewis et al. co-author count                                 | Read the corrected sentence in both languages                                                                                                                                                                          |
| `advanced/06`'s stale prerequisite note                                          | Read the current opening in both languages and checked what replaced the false statement                                                                                                                               |
| `introductory/05` and `intermediate/05` (Tan, no independent re-review)          | Metadata block, H1, and typography checked directly; §4 conformance of the one parenthetical definition at `intermediate/05` l. 173                                                                                    |
| The four re-review records                                                       | Read in full, including each reviewer's independence declaration and declared scope boundary                                                                                                                           |

**One stated limit on my own sweep, so it is not read as more than it is.** My C-3 regex targets
the direction §4 actually names — an English term glossed with a Chinese parenthetical. It would
not catch the reverse shape (`中文（English）`) applied to an ordinary concept. I did not sweep for
that shape exhaustively, and I am not claiming a proof of zero; I am claiming that the 310
instances Pass 3 counted are down to 42 candidates of the named shape, of which three are genuine
residuals. Neither is `advanced/01`'s or `introductory/08`'s content re-audited here — those
documents passed Pass 3 and were never in the Pass 4 scope.

---

## 2. The four independent re-reviews — verdicts

All four are **Pass**. All four went back to a primary source or to a hand recomputation rather
than to the diff, which is the property that makes me accept them.

| Document                         | Re-reviewer      | Verdict | What was independently verified                                                                                                                                                                                                                                     |
| -------------------------------- | ---------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `intermediate/04` (Roldán, P1)   | Dr. Bhandari     | Pass    | Recomputed 200 ÷ 24 = 8.333…; text now reads `约 8.3 天（200 小时）`, correctly hedged. Re-derived the three decay controls (0.995⁵, 0.995², 0.995²⁰⁰) — undisturbed by the fix.                                                                                    |
| `intermediate/07` (Fujimori, P1) | Dr. Ibarra-Costa | Pass    | Re-fetched the Anthropic post directly and inventoried every "90%" occurrence; the 90% time figure is now correctly baselined against the team's own sequential execution, and the 90.2% quality figure correctly identified as the actual single-agent comparison. |
| `advanced/05` (Tan, P1)          | Dr. Baek         | Pass    | Re-fetched arXiv:2404.06654; text now reads "only about half" / `大约只占一半`, matching the paper's "only half of them". Zero remaining `只占少数`.                                                                                                                |
| `advanced/08` (Dubois, P0)       | Dr. Ibarra-Costa | Pass    | Recomputed 81/22 ≈ 3.68 by hand and by script, and derived the Bonferroni critical χ² ≈ 5.73 independently. Table, footnote, and closing prose now all agree; "5.14" and "4.55" absent from the file.                                                               |

**All four blocking findings — the P0 and the three P1s — are closed.** That is the most
consequential result in this pass, and it is the one I am most confident in, because it is the one
that was checked hardest.

**One process observation, recorded rather than charged as a defect.** Two of the four re-reviews
(`advanced/05`, `intermediate/07`) were performed by the reviewer who originally raised the
finding, and the third (`intermediate/04`) by the Pass 1 reviewer of that document's cluster. All
three declared this openly and reasoned it correctly: README §6's independence rule bars an
**author** from reviewing their own work, not a reviewer from verifying their own finding. So all
four are compliant as the rule is written. But a reviewer confirming their own finding is a
structurally weaker check than a cold one, and the rule is currently silent on it. Before the next
cycle, README §6 should say explicitly which of the two it intends. I am not reopening any of the
four verdicts on this basis — each rests on a fresh primary-source check, not on a memory of the
original finding.

---

## 3. My own corpus-wide verification — C-1, C-2, C-3

### C-1 — `harness` → `运行框架`: fully applied

I checked all 24 files, not the 8 named. **`执行框架` occurs zero times anywhere in the corpus.**
The canonical `运行框架` is present where Pass 3 found the term: `introductory/03` (5),
`introductory/04` (11), `intermediate/03` (3), `intermediate/04` (3), `intermediate/07` (2),
`advanced/03` (39), `advanced/04` (16), `advanced/08` (14). Two counts drifted by one against Pass
3's audit (`introductory/03` 7→5 combined, `advanced/03` 40→39), consistent with ordinary editing
around those sentences and not with a missed instance. The four documents the amendment named by
file (`introductory/03`, `introductory/04`, `intermediate/07`, `advanced/08`) are clean, and so are
the four it did not.

**C-1 is closed.** This is the one item I can report to the CEO as complete without a caveat.

### C-2 — metadata block: applied to all 24, with two P3 residuals

Every one of the 24 modules now opens with README §4.1's Format B: a bold `Level · Cluster ·
Author` line, all three fields present, immediately followed by its Chinese mirror line, with
Author given as full roster identity. All five deprecated shapes are gone — the pipe-tables, both
narrative-paragraph variants, Roldán's two-field partial blocks, and Dr. Tan's four
no-block-at-all cases. Six formats across eight authors became one. This was the largest single
piece of mechanical work in the pass and it was done properly.

Two residuals, named plainly because neither reviewer was scoped to catch them:

1. **Three modules omit the `---` rule §4.1 requires after the block** — `introductory/02`,
   `intermediate/02`, `advanced/02`, all Dr. Baek's, all of which run body text directly on from
   the Chinese mirror line. Her fourth module (`introductory/01`) has the rule, and so do the
   other twenty. §4.1 states the rule as a binding detail of the format, so this is
   non-conformance, not a matter of taste — but it is P3 and it is a one-line insertion in three
   files.
2. **Two modules transliterate the author's name on the Chinese mirror line** —
   `introductory/06` and `intermediate/06` render Dr. Ibarra-Costa as
   `ANU-00 通才研究科学家 拉斐尔·伊瓦拉-科斯塔博士`, where the other twenty-two keep the
   Latin-script surname plus `博士`, matching §4.1's own canonical example
   (`Kaito Fujimori 博士`). §4.1 does not literally forbid transliteration, so I record this as an
   ambiguity in the convention I ratified rather than as a defect against the author. It should be
   settled one way in the next README amendment.

### C-3 — inline term glosses: substantively applied, with one new defect introduced

Pass 3 counted **310** inline parenthetical glosses of the `English term（中文）` shape across all
24 files. My sweep now returns **42 candidates**, and I classified every one by hand rather than
reporting the count:

- **6** are tool-call traces inside worked examples (`search("巴西的首都")` and similar,
  `intermediate/03`) — code, not prose glosses.
- **~14** are cross-references or ordinary explanatory asides, which §4 never restricted:
  `softmax（introductory/01 第 4 节）`, `MLA（第 7 至第 8 节）`, `D（以词元数计）`,
  `LLM（该文章使用的是 Claude）`.
- **~19** are proper-noun or named-method glosses the narrowed §4 explicitly permits on first use:
  `Chinchilla（龙猫模型）`, `Wilson score interval`, `Bonferroni correction`, `Cohen's kappa`,
  `Goodhart's law`, `FLP`, `Paxos`, `Raft`, `RRF`, `RAG`, `self-consistency`,
  `multiagent debate`, `MMLU`.

That is a genuine, substantive cleanup applied across the whole corpus and not only against the
ten flagged documents — which is exactly what I asked to be verified and what I was least willing
to assume. Three residuals remain:

1. **`introductory/08` glosses `MMLU（大规模多任务语言理解基准）` twice** (l. 79 and l. 86). The
   term is permitted; the repetition breaches §4's "first use only". P3.
2. **`advanced/07` glosses `AutoGen（AutoGen 框架）` twice** (l. 486 and l. 508). Same breach,
   same severity. (The same document's `Paxos（Paxos 算法）` and `Raft（Raft 算法）` are
   self-glosses that add nothing, but they are not rule breaches and I am not charging them.)
3. **`intermediate/06` l. 312 — a new defect, not a survivor.** The English sentence now reads:

   > The dominant sparse scoring algorithm in production search systems is BM25（BM25 算法, short
   > for "Best Matching 25"), whose modern, authoritative treatment is …

   A Chinese gloss is sitting inside an English paragraph, opened with a full-width `（` and closed
   with a half-width `)`. This looks like a gloss that was half-removed during the C-3 cleanup and
   left in a broken state. It breaches two rules at once — §4's gloss restriction and §4's
   EN-paragraph-then-ZH-paragraph separation — and it is the sole source of the one
   half-width-after-CJK hit my typography scan found in that file. Small, but it is damage the
   remediation caused rather than damage it failed to remove, and it re-opens a document that had
   otherwise been fixed correctly.

---

## 4. What was NOT fixed — named plainly

### 4.1 The 864-instance bilingual punctuation deviation stands, essentially untouched

This is the most important thing in this report and I will not soften it.

Pass 3 recorded 868 instances of half-width ASCII punctuation directly following a CJK character
across Dr. Wei-Ling Tan's four modules — a wholesale deviation from Chinese typographic convention
spanning one author's entire output. I reran the identical scan across all 24 files today:

| Module            | Half-width after CJK | Full-width | Pass 3 count |
| ----------------- | -------------------- | ---------- | ------------ |
| `introductory/05` | **192**              | 3          | 192          |
| `intermediate/05` | **166**              | 3          | 167          |
| `advanced/05`     | **256**              | 3          | 255          |
| `advanced/06`     | **250**              | 3          | 254          |
| **Total**         | **864**              | 12         | 868          |

The four-instance net change is incidental drift from edits made for other reasons. **Nothing was
done about this.** The other twenty modules remain clean — zero half-width instances in eighteen
of them, four in `advanced/01` (a P2 carried unchanged from Pass 3 in a document that passed and
was never in scope), and the single BM25 artifact in `intermediate/06` described above.

This was not a corpus-wide C-item that could be missed on a technicality. It is written into the
per-document reason column of `academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` rows 5, 13, 21 and 22 as a named cause
of those four documents' needs-revision verdicts. It was in scope, it was specific, and it was not
done. Dr. Baek recorded it in her `advanced/05` re-review as an out-of-scope observation so it
would not be lost — correctly, given her assigned scope — and my scan confirms it holds for all
four of Dr. Tan's modules, not just the one she read.

### 4.2 All four H1 numeral prefixes stand

`introductory/05` still opens `# 5. Prompt Engineering Fundamentals`; `intermediate/05`
`# 5. Advanced Prompting: …`; `advanced/05` `# 5. Advanced Context Engineering: …`;
`advanced/06` `# 6. RAG at Scale: …`. Zero of the four were corrected. The other twenty H1 lines
match their README §7 titles exactly, as they did at Pass 3. This too is a named per-document
reason in rows 5, 13, 21 and 22.

Related and unrecorded until now: the bold Chinese title lines of three of those four modules also
carry half-width colons (`进阶提示工程:思维链…`, `高级上下文工程:长上下文…`,
`规模化 RAG:混合检索…`) — the same punctuation deviation, in the document's most visible line.

### 4.3 What this pattern actually is

Dr. Tan's four modules received the C-2 metadata block and their content fixes — the RULER
correction in `advanced/05` (independently verified by Dr. Baek) and the stale-prerequisite
replacement in `advanced/06` (which I verified myself; the false "had not yet been written"
statement is gone and is replaced by a scope note naming `intermediate/06` as the designated
prerequisite and framing §1 as a compatible recap — the better of the two available fixes). What
they did not receive is anything on the presentation layer: no typography, no H1.

So the split is clean and it is worth stating precisely for the CEO: **every content defect in
this corpus is fixed. One author's presentation defects are untouched.** That is a much better
position than Pass 3, and it is not the same as done.

### 4.4 The process seam reproduced itself

Pass 3 escalated a process finding: the punctuation defect went unrecorded by all seven reviewers
because it sat between the content reviewers' meaning-and-fluency mandate and the structural
reviewer's declared exclusion of translation quality. Pass 4 has now demonstrated that finding a
second time from the other direction. The four independent re-reviews were scoped to blocking
findings; the six non-blocking documents received no independent check at all; and the two defect
classes that fell out of the work are precisely the two that no one was assigned. My Pass 3
recommendation — that README §6 add a mechanical bilingual-typography sweep to the structural
reviewer's standing mandate — is no longer a precaution. It is a demonstrated requirement, and it
would have taken a script under a second to catch all 864 instances on either pass.

---

## 5. Per-document status — all 24

Status rule, unchanged from Pass 3 so the two tables can be read against each other:
**Needs revision** = the document contains at least one defect that is factually wrong,
misrepresents a source, corrupts its own rendered output, or breaches a mandatory README §4/§5
requirement inside that document. **Pass** = remaining defects are polish-level.

| #   | Document          | Author       | Pass 3 verdict | **Pass 4 status**  | What changed / what remains                                                                                                                                                                                                                           |
| --- | ----------------- | ------------ | -------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `introductory/01` | Baek         | Pass           | **Pass**           | Metadata conformant. Clean.                                                                                                                                                                                                                           |
| 2   | `introductory/02` | Baek         | Pass           | **Pass**           | P3: metadata block not followed by the `---` rule (§4.1).                                                                                                                                                                                             |
| 3   | `introductory/03` | Fujimori     | Pass           | **Pass**           | C-1 applied (0 / 5). Metadata conformant.                                                                                                                                                                                                             |
| 4   | `introductory/04` | Fujimori     | Pass           | **Pass**           | C-1 applied (0 / 11). Metadata conformant.                                                                                                                                                                                                            |
| 5   | `introductory/05` | Tan          | Needs revision | **Needs revision** | Metadata block added ✅. **H1 `5.` prefix stands; 192 half-width punctuation instances stand.**                                                                                                                                                       |
| 6   | `introductory/06` | Ibarra-Costa | Pass           | **Pass**           | P3: ZH mirror line transliterates the author's name (§4.1 ambiguity).                                                                                                                                                                                 |
| 7   | `introductory/07` | Fujimori     | Pass           | **Pass**           | Clean.                                                                                                                                                                                                                                                |
| 8   | `introductory/08` | Dubois       | Pass           | **Pass**           | P3 ×2: `MMLU` glossed twice; HELM orphan citation unchanged (carried from Pass 3, never in Pass 4 scope).                                                                                                                                             |
| 9   | `intermediate/01` | Okonkwo      | Needs revision | **Pass** ✅        | Adam update rule renders continuously (l. 97 EN / l. 107 ZH); corpus-wide fragment scan returns zero. Orphan Ioffe & Szegedy citation struck entirely. `模型family` gone. Half-width commas 4 → 0.                                                    |
| 10  | `intermediate/02` | Baek         | Pass           | **Pass**           | P3: missing `---` rule after metadata block.                                                                                                                                                                                                          |
| 11  | `intermediate/03` | Fujimori     | Pass           | **Pass**           | C-1 applied (0 / 3).                                                                                                                                                                                                                                  |
| 12  | `intermediate/04` | Roldán       | Needs revision | **Pass** ✅        | `约 8.3 天（200 小时）` — independently recomputed by Dr. Bhandari and by me. Author field added to metadata.                                                                                                                                         |
| 13  | `intermediate/05` | Tan          | Needs revision | **Needs revision** | Metadata block added ✅. **H1 `5.` prefix stands; 166 half-width instances stand;** l. 173 defines JSON Schema inside a parenthesis, the pattern §4 names.                                                                                            |
| 14  | `intermediate/06` | Ibarra-Costa | Needs revision | **Needs revision** | Stray blockquote gone (corpus-wide `^>` scan returns zero) ✅; Lewis et al. now "eleven co-authors" / `另外十一位合著者` ✅. **New defect at l. 312: half-removed `BM25（BM25 算法, …)` gloss inside an English paragraph, mismatched paren widths.** |
| 15  | `intermediate/07` | Fujimori     | Needs revision | **Pass** ✅        | Both 90% figures correctly separated and attributed; verified by Dr. Ibarra-Costa against the primary source. C-1 applied (0 / 2).                                                                                                                    |
| 16  | `intermediate/08` | Dubois       | Pass           | **Pass**           | Clean.                                                                                                                                                                                                                                                |
| 17  | `advanced/01`     | Okonkwo      | Pass           | **Pass**           | Unchanged, as expected — not in Pass 4 scope. Brown et al. still reference-only; 4 half-width commas remain. P2/P3.                                                                                                                                   |
| 18  | `advanced/02`     | Baek         | Needs revision | **Pass** ✅        | Load-balancing-loss sum renders continuously (EN l. 271–273 / ZH l. 285–286). P3: missing `---` rule.                                                                                                                                                 |
| 19  | `advanced/03`     | Roldán       | Pass           | **Pass**           | C-1 applied (0 / 39). Metadata conformant — the C-2 gap folded in at Pass 3 is closed.                                                                                                                                                                |
| 20  | `advanced/04`     | Fujimori     | Pass           | **Pass**           | C-1 applied (0 / 16).                                                                                                                                                                                                                                 |
| 21  | `advanced/05`     | Tan          | Needs revision | **Needs revision** | RULER claim corrected and independently re-verified ✅; metadata block added ✅. **H1 `5.` prefix stands; 256 half-width instances stand.**                                                                                                           |
| 22  | `advanced/06`     | Tan          | Needs revision | **Needs revision** | Stale prerequisite statement replaced with a correct scope note ✅; metadata added ✅. **H1 `6.` prefix stands; 250 half-width instances stand.**                                                                                                     |
| 23  | `advanced/07`     | Bhandari     | Pass           | **Pass**           | P3: `AutoGen` glossed twice. S-1 (internal case study) remains a CEO scope call, not a defect.                                                                                                                                                        |
| 24  | `advanced/08`     | Dubois       | Needs revision | **Pass** ✅        | §11 WebArena row recomputed to 3.68; table, footnote and closing prose agree; "5.14"/"4.55" absent. C-1 applied (0 / 14).                                                                                                                             |

**19 pass. 5 need revision** — down from 14 / 10 at Pass 3.

Of the ten documents flagged at Pass 3: **five are fully fixed** (`intermediate/01`,
`intermediate/04`, `intermediate/07`, `advanced/02`, `advanced/08`); **four are partially fixed**
— all four of Dr. Tan's, all four on presentation only (`introductory/05`, `intermediate/05`,
`advanced/05`, `advanced/06`); and **one was fixed and then re-broken** by the C-3 cleanup
(`intermediate/06`).

---

## 6. Overall recommendation to the CEO

**Not ready to ship today. Ready to ship after one short, mechanical tidy that needs no author
research and no further review round.**

I want to be precise about how much better this is than Pass 3, because the headline count
understates it.

**Every content defect in this corpus is closed.** The P0 arithmetic self-contradiction in
`advanced/08`, both misstated source findings (`intermediate/07`, `advanced/05`), the false
day-conversion in `intermediate/04`, the two fragmented formulas, the broken paragraph, the
co-author miscount, the stale production note, two of the three orphan citations — all fixed, and
the four that mattered most were independently re-verified by a reviewer who went back to the
paper or redid the arithmetic rather than reading the diff. All three corpus-wide harmonization
items landed: C-1 completely, C-2 across all 24 modules, C-3 from 310 instances down to three
residuals. That is a real remediation run, executed well by eight authors on the substance.

What is left is one author's presentation layer and one small piece of self-inflicted damage:

1. **`introductory/05`, `intermediate/05`, `advanced/05`, `advanced/06` (Dr. Tan)** — convert 864
   half-width `,` `:` `;` following CJK characters to their full-width forms, including the three
   Chinese title lines, and strip the numeral prefix from all four H1s. This is a scripted
   find-and-replace plus four one-line edits. It requires no judgment about meaning and no
   re-reading of any source. It should not go back through a content review; it needs one
   structural check by Tobias Lindqvist against the same scan I ran here.
2. **`intermediate/06` l. 312** — repair the half-removed `BM25（BM25 算法, …)` gloss. Two
   characters' worth of edit, in a document that is otherwise fully remediated.
3. **P3 tail, optional before ship** — insert the missing `---` rule in `introductory/02`,
   `intermediate/02`, `advanced/02`; de-duplicate the second `MMLU` gloss in `introductory/08` and
   the second `AutoGen` gloss in `advanced/07`; settle the transliterated-author-name question in
   `introductory/06` / `intermediate/06` by amending §4.1 rather than editing the files.

I am **not** recommending a Pass 5 in the sense Pass 4 was — a full remediation round with
independent re-reviews. That would be disproportionate to what remains. I recommend a scoped
mechanical tidy on items 1 and 2, verified by a single structural sweep, with item 3 at the CEO's
discretion.

**Two things remain open that are not mine to close.** S-1 (`advanced/07` §4's workspace-internal
case study — fine internally, a visible seam if this is ever published outside the workspace) and
S-2 (zero runnable code, zero RLHF/post-training coverage — both outside the ratified scope, both
bearing directly on whether a reader finishes interview-ready) were escalated at Pass 3 and have
not been ruled on. Neither blocks the tidy above. S-2 in particular would require a second
production run, not edits to these 24, and the CEO should decide it before the curriculum is
described to anyone as interview-preparation.

**One process amendment I am making regardless of the CEO's decision on the above.** README §6
will be amended before the next curriculum run in two places: a mechanical bilingual-typography
sweep becomes part of the structural reviewer's standing mandate, and the independence rule will
state explicitly whether a reviewer may verify the fix to a finding they themselves raised. The
first is the same recommendation I made at Pass 3, now demonstrated twice rather than argued once
— 864 instances survived two full review cycles because they belonged to no one's scope, and a
script would have caught every one of them in under a second. The second is a gap the four
re-reviewers each had to reason around in writing, which is a sign the rule is underspecified, not
that they got it wrong.

**I recommend the CEO approve the scoped mechanical tidy described above, treat the curriculum as
content-complete and content-verified as of today, and rule on S-1 and S-2 — and I recommend
against a further full review round, which the remaining defects do not warrant.**

---

**Dr. Naledi Mokoena, ANU-00 Lead — 2026-08-19**
