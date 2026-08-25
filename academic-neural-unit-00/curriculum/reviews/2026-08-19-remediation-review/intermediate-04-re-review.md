# Pass 4 Re-Review — `intermediate/04-agent-memory-systems-short-term-long-term-episodic.md`

**Reviewer:** Dr. Aditi Bhandari, Staff Research Scientist — Foundational AI Lead, ANU-00
**Document reviewed:** `academic-neural-unit-00/curriculum/intermediate/04-agent-memory-systems-short-term-long-term-episodic.md`
**Author:** Dr. Inés Roldán, Research Scientist — Software Engineering / Computer Science, ANU-00
**Review date:** 2026-08-19
**Review pass:** Pass 4 re-review, targeted — verifying the fix for the single blocking finding
recorded against this document in `academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` (row 12: "Chinese gloss states
'5 天（200 小时）'; 200 h is 8.33 days — false numeric claim in a worked example"), originally
surfaced by External Reviewer A and independently confirmed by Dr. Mokoena at (then) line 280.

---

## 0. Independence Declaration

**Did I author this document?** No. Dr. Inés Roldán is the sole author of record
(`curriculum/README.md` §7). I am the Pass 1 cluster reviewer for Agent Architecture & Design
Patterns, the cluster this document belongs to — that is a reviewing role, not an authoring one,
so it does not create the conflict README §6 prohibits ("no reviewer reviews a cluster they
authored into" bars authors from reviewing, not reviewers from re-reviewing their own earlier
cluster). I did not write, edit, or suggest wording for this document at any point before this
re-review.

**Anything else that would compromise independence:** None.

---

## 1. Method

I did not trust the Pass 4 label as evidence the fix was made. I opened the current file in full
(all 472 lines) and checked the specific defect location directly, then read the rest of the
document for consistency and new-error risk.

| What I did                      | Detail                                                                                                                                                                                                                                       |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Independent recomputation       | 200 hours ÷ 24 = 8.333… days, computed directly (not read off any prior report) and cross-checked against the original Pass 3 finding's own suggested figure ("approximately 8.3 天")                                                        |
| Location of the original defect | Located by content search (`grep -n "天"` and `grep -n "（"` across the full file), not by trusting the old line number — line numbers shift when other passes edit the same file                                                            |
| English/Chinese consistency     | Compared the English worked-example paragraph (§5, "Memory A … was accessed 200 hours ago") against its Chinese counterpart word for word                                                                                                    |
| Surrounding math re-derived     | Independently recomputed the three recency values in the same worked example: 0.995⁵, 0.995², 0.995²⁰⁰                                                                                                                                       |
| Chinese-language read           | Read in full (all ZH paragraphs, not sampled) — bilingual pairing is structural per README §4, and a targeted fix is exactly where an editor is likeliest to touch one language and miss the other                                           |
| Metadata block                  | Diffed the document's opening block against README §4.1's canonical Format B example, field by field                                                                                                                                         |
| Inline-gloss spot check         | Searched every `（…）` occurrence in the document (18 hits) and classified each against README §4's proper-noun-only rule                                                                                                                    |
| C-1 term check                  | Searched for the deprecated `执行框架` rendering (0 hits) and the canonical `运行框架` (3 hits), against the corpus-wide count in `academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` line 61 |

---

## 2. Finding (a) — Is the specific defect actually corrected?

**Yes, verified by independent recomputation.**

Current text, §5, worked example (Memory A):

> EN (l. 251): "Memory A, 'user prefers tabs over spaces,' was accessed **200 hours ago**, rated
> importance 2 by the LLM, and has a query-similarity of 0.30."
>
> ZH (l. 264): "记忆 A：'用户偏好使用制表符而非空格'，**约 8.3 天（200 小时）**前被访问过，LLM
> 给出的重要性评分为 2，与当前查询的相似度为 0.30。"

I recomputed the conversion myself rather than accepting the file's number: 200 / 24 =
8.3333…, which rounds to **8.3** at one decimal place. The document now states "约 8.3
天（200 小时）" — "approximately 8.3 days (200 hours)" — with the hedge word 约 ("approximately")
correctly signaling a rounded figure rather than an exact one. This matches the number the
original Pass 3 finding itself proposed as the correct fix, and it is arithmetically correct.

I also re-derived the three recency multipliers used later in the same paragraph as a control
(these were never flagged, but a re-reviewer should not assume a fix touched only the flagged
line and nothing else nearby):

- 0.995⁵ ≈ 0.9752 → document states "≈ 0.975" — correct
- 0.995² ≈ 0.9900 → document states "≈ 0.990" — correct
- 0.995²⁰⁰ ≈ 0.3670 → document states "≈ 0.367" — correct

All three were already correct and remain correct; the fix did not disturb them.

I searched the rest of the document for any other hour→day (or similar) unit conversion that
might carry the same class of error. There is no other such conversion anywhere in the file —
the two other "5 小时" / "2 小时" figures in the same worked example are left as hours only, with
no day conversion attached, so there was nothing else to be wrong.

---

## 3. Finding (b) — Is the fix present and consistent in both languages?

**Yes, and there is no cross-language inconsistency to find, for a structural reason worth
recording rather than assuming.** The English paragraph (l. 251) never asserted a day-count for
Memory A at all — it states only "200 hours ago." The false claim was Chinese-only, exactly as
the original finding said ("The English at line 267 says only '200 hours ago' and makes no day
claim — the error exists solely in the Chinese," per `academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` line 63). So
"consistency" here does not mean the two languages must state the same day figure — it means the
Chinese must not assert something the English doesn't and that is also false. It no longer does:
the Chinese states a correctly-computed approximation, hedged with 约, and the English states the
same underlying fact (200 hours) without needing a day conversion at all. I checked the paired
EN¶→ZH¶ structure immediately around this sentence and found no other divergence — the two
paragraphs describe the same three memories (A, B, C) with the same importance scores and
similarity values throughout.

---

## 4. Finding (c) — No new error, and the surrounding text still reads coherently

**Confirmed.** I read the full paragraph (§5, the "worked example" paragraph, l. 249–261 EN /
263–277 ZH) start to finish in both languages. The sentence carrying the fix sits mid-paragraph,
introducing Memory A alongside Memories B and C; the fix is a single inserted clause ("约 8.3
天（") and does not disturb sentence boundaries, punctuation, or the paragraph's logical flow —
it reads as a native Chinese sentence, not as a patched-in fragment. The paragraph's conclusion
("memory B … comes out on top by a wide margin, even though memory C is technically the most
recent of the three") still follows correctly from the (unchanged, correct) recency/importance/
relevance values for B and C — the fix touched only Memory A's clause, which is not the memory
the paragraph's punchline turns on, so the argument the worked example is making is unaffected
either way.

I also checked that the fix did not introduce a new numeric inconsistency elsewhere: the "200
小时" figure still appears, unchanged, at l. 264 (recency-value passage, "记忆 A 经过 200 小时,
为 0.995²⁰⁰ ≈ 0.367") a few lines later, and 200 hours is what both the corrected day-approximation
and the recency exponent are computed from — one shared number, no drift between the two
mentions.

---

## 5. Finding (d) — Metadata block and inline-gloss spot check

**Metadata block: conforms to README §4.1 Format B.** Diffed field-by-field against the canonical
example in `curriculum/README.md` §4.1:

| Field               | README canonical example                                        | This document (l. 5, 7)                                                                                                                                                                                    |
| ------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Structure           | Bold key-value line, 3 fields, `·`-separated, EN then ZH mirror | Same structure, same separator                                                                                                                                                                             |
| Level               | `**Level:** Introductory`                                       | `**Level:** Intermediate` — correct for this module (matches `curriculum/README.md` §7 module-index row)                                                                                                   |
| Cluster             | `**Cluster:** Agent Architecture & Design Patterns`             | `**Cluster:** Agent Architecture & Design Patterns` — exact match                                                                                                                                          |
| Author              | Full name, roster role, `ANU-00`                                | `Dr. Inés Roldán, Research Scientist — Software Engineering / Computer Science, ANU-00` — full roster identity, matches `crew/README.md` row for Roldán (`Research Scientist — Software Engineering / CS`) |
| Chinese mirror line | Same 3 fields, same order, Chinese                              | Present, all 3 fields, correct order (l. 7)                                                                                                                                                                |
| Placement           | Beneath H1 + bold ZH title, before `---` rule                   | Same placement (l. 1–9)                                                                                                                                                                                    |

This resolves the specific C-2 gap the comprehensive review recorded against this document
("`intermediate/04` and `advanced/03` … carry a correctly-paired bilingual Level/Cluster line
with the Author field absent" — comprehensive-review.md l. 98). The Author field is now present
and correctly populated; the block is fully conformant.

**Inline-gloss spot check: no violating gloss found.** I located all 18 `（…）` occurrences in the
document and classified each:

- Named models/papers, first use only — permitted under README §4 ("proper nouns and named
  entities"): the Atkinson–Shiffrin "multi-store model," the Tulving 1972 paper title, the CoALA
  paper title and its acronym introduction, the Generative Agents paper title, the Reflexion paper
  title.
- Non-gloss parentheticals — ordinary explanatory asides, not `English term（中文）` glosses of an
  ordinary concept: an example list ("如文档库"), an example enumeration ("日常琐事，例如刷牙" /
  "分手或收到录取通知"), a variable-name aside ("三个权重（α）"), a threshold value ("阈值为
  150"), scope clarifiers ("而非某一片段专属的记忆", "二者完全可以存放在同一个向量存储中", "即其
  上下文窗口", "即向量存储本身"), and the unit-conversion clause under review here
  ("约 8.3 天（200 小时）"), which is a converted figure, not a bilingual term gloss.
- I found **zero** instances of the banned pattern — an ordinary technical concept (loss function,
  embedding, token, context window, etc.) glossed as `English（中文）` in violation of the
  narrowed §4 rule. `embedding` itself, for instance, is introduced by a full explanatory sentence
  in both languages (l. 167–168 EN, l. 173 ZH), exactly as §4 prescribes, with no parenthetical
  gloss attached.

**C-1 term check (harness):** 0 occurrences of the deprecated `执行框架`; 3 occurrences of the
canonical `运行框架` (l. 199, 416, 448 in this reading). This matches the corpus-wide audit in
`academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` (l. 61: "intermediate/04 (0 / 3)") — this document was already
compliant before Pass 4 and remains so; no regression.

This was a spot check, not the exhaustive corpus-wide C-2/C-3 audit — that is explicitly
Dr. Mokoena's closing-synthesis scope, not mine here.

---

## 6. Verdict

**Pass — the defect is resolved.**

The single blocking finding against this document (the false "5 天（200 小时）" claim) is
corrected: the Chinese now states "约 8.3 天（200 小时）," a figure I independently recomputed
and confirmed correct (200 ÷ 24 = 8.33…), correctly hedged with 约, consistent with the English
text (which makes no day claim to be inconsistent with), and it introduces no new numeric or
textual defect in the surrounding paragraph. The metadata-block C-2 gap previously recorded
against this document (missing Author field) is also resolved and now conforms exactly to
README §4.1 Format B. No inline-gloss violation and no `执行框架` regression were found on
spot check.

I found nothing else wrong with this document in the course of this targeted check. I am not
issuing a general clean bill for the whole document beyond the scope actually re-checked here —
this was a targeted re-review of one prior finding plus a bounded spot check (d), not a full
Pass-1-style five-check pass over factual accuracy, citation validity, and pedagogical fit
end to end.

---

## 7. Scope Boundary

**Did I edit the document?** No — this file is a review record only, per README §8 rule 4
(point-in-time discipline: a re-review is a new file, never an edit to the document or to a prior
report).

**Out of scope for this re-review:** A full re-audit of the document's ~90-word citation list, a
fresh independent verification of every worked-example claim beyond the one flagged and its
immediate numeric neighbors, and the corpus-wide C-2/C-3 harmonization audit across all 24
modules — all reserved for Dr. Mokoena's closing Pass 4 synthesis, per this task's own
instruction and per `curriculum/README.md` §6.

---

**Dr. Aditi Bhandari, Staff Research Scientist — Foundational AI Lead, ANU-00 — 2026-08-19**
