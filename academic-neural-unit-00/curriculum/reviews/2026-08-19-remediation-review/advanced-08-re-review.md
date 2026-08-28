# Pass 4 Re-Review — `advanced/08-rigorous-agent-evaluation-statistical-methodology.md`

**Reviewer:** Dr. Rafael Ibarra-Costa, Research Scientist — Generalist, ANU-00
**Document under re-review:** `academic-neural-unit-00/curriculum/advanced/08-rigorous-agent-evaluation-statistical-methodology.md`
**Document author:** Dr. Mireille Dubois, Research Scientist — LLM Systems, ANU-00
**Review date:** 2026-08-19
**Review pass:** Pass 4 — independent re-review of a Pass 3 finding's fix (single-document, targeted
scope, not a full cluster review)

---

## 0. Independence Declaration

**Did I author any document in this cluster?** No. `advanced/08` was authored by Dr. Mireille
Dubois. I am the ratified Pass 1 reviewer for the Multi-Agent Systems & Evaluation cluster
(`curriculum/README.md` §6, §7.2), which already excludes me from having authored into it — Dubois,
Fujimori, and Bhandari are this cluster's authors, not me. This re-review satisfies
`curriculum/README.md`'s independence rule that a re-reviewer must not be the document's own
author.

**Anything else that would compromise independence:** None.

---

## 1. The Pass 3 Finding Under Re-Review

> Section 11 (lines ~491-523): the WebArena row states McNemar χ²=5.14 with "Yes" in the
> significance column, but the stated inputs b=16, c=6 actually give a continuity-corrected
> χ²≈3.68 (or ≈4.55 uncorrected) — neither is 5.14. The footnote also self-contradicts itself (it
> announces using the uncorrected ≈4.55 value, then two lines later reasons about "5.14"). The
> section's closing prose says none of the three comparisons clear a significance bar, which
> contradicts the table's own "Yes". Recompute the McNemar statistic correctly from the stated
> b=16, c=6 inputs using the continuity-corrected formula this document itself teaches in §6, fix
> the table entry and the footnote, and make the table, footnote, and closing prose all agree with
> each other and with the correct recomputation.

---

## 2. Method

I read the full current document (635 lines, both language streams) before checking anything else.
I did not treat the presence of an edit as evidence the edit was correct.

| What I did                   | Detail                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Independent recomputation    | Recomputed the continuity-corrected McNemar χ² from b=16, c=6 by hand and by script, independent of the document's own arithmetic. Also independently derived the df=1 critical χ² for the Bonferroni-adjusted α = 0.05/3, via the standard normal inverse (`chi²(df=1)` is the square of a standard normal variate), rather than trusting the document's stated 5.73. |
| Independent source consulted | WebSearch on the continuity-corrected McNemar formula itself (not a source the document cites) to confirm `χ² = (\|b−c\|−1)²/(b+c)` is the standard continuity-corrected form the document uses throughout §6 and §11 — confirmed against CRAN's `exact2x2` McNemar vignette (Fay) and the LibreTexts biostatistics chapter on McNemar's test.                         |
| Recomputation tool           | Verified numerically with a short Python script (`abs(16-6)-1)**2/(16+6)` and a bisection solve of `Φ(z)=1-α/2` for `α=0.05/3`), not by re-reading the document's own stated numbers.                                                                                                                                                                                  |
| Chinese-language text read   | Read in full (all of §0–§13 and References, both EN and ZH paragraphs), not sampled — the finding required checking that the fix is consistent in both languages, not only in English.                                                                                                                                                                                 |
| Scope                        | Targeted to the four checks the task specifies (recomputation, bilingual consistency, no new error / coherence, metadata + gloss spot-check). A full C-2/C-3 corpus-wide audit is out of scope here per the task's own instruction.                                                                                                                                    |

---

## 3. (a) Independent Verification of the Core Defect

**Recomputation.** With `b = 16`, `c = 6` (as stated in the WebArena footnote, unchanged from Pass
3):

```
χ² (continuity-corrected) = (|16 − 6| − 1)² / (16 + 6) = (10 − 1)² / 22 = 81 / 22 ≈ 3.6818
```

This is a standard result — I confirmed the continuity-corrected McNemar formula
`χ² = (|b−c|−1)²/(b+c)` independently via WebSearch against the CRAN `exact2x2` vignette and the
LibreTexts biostatistics chapter, and it matches exactly the formula the document itself states in
§6 ("`χ² = (|b − c| − 1)² / (b + c)`, with 1 degree of freedom").

**Current document state (§11 table, line 492):**

```
WebArena | 30/50 (60%) | 20/50 (40%) | No | 3.68 | No
```

**Current document state (§11 footnote, EN, lines 496–502):**

> `χ² = (|16−6|−1)²/(16+6) = 81/22 ≈ 3.68`. That falls short even of the unadjusted `α = 0.05`
> critical value of 3.84 (§6) — so it is, a fortiori, also short of the stricter
> Bonferroni-adjusted threshold from §7's `α/m` logic at `m = 3`, which requires
> `α = 0.05/3 ≈ 0.0167`, corresponding to a critical χ² ≈ 5.73.

Both the table entry (3.68) and the footnote's recomputation (81/22 ≈ 3.68) match my independent
recomputation exactly. The old 5.14 figure and the old "Yes" significance mark are both gone; no
trace of either remains in the table or the footnote.

**The Bonferroni-adjusted critical value is also independently correct.** I derived the df=1
critical χ² for α = 0.05/3 ≈ 0.01667 myself (chi-square with 1 degree of freedom is the square of
a standard normal variate, so the critical value is `z²` where `Φ(z) = 1 − α/2`). Solving
numerically gives `z ≈ 2.394`, `z² ≈ 5.731` — matching the document's stated "critical χ² ≈ 5.73"
to the precision given. 3.68 falls well short of both 3.84 (unadjusted) and 5.73
(Bonferroni-adjusted), so "No" in the significance column is correct under either threshold, not
just technically defensible under one of them.

**The self-contradiction is resolved, not merely hidden.** The Pass 3 finding noted the old
footnote announced using the _uncorrected_ ≈4.55 value and then reasoned about "5.14" — two
different, both-wrong numbers in the same footnote. The current footnote uses exactly one number
throughout (3.68, the continuity-corrected value) and only ever compares it against two _critical
thresholds_ (3.84 and 5.73), never against a second, different computed χ² statistic. There is no
remaining instance of an uncorrected 4.55 figure anywhere in §11 (I grep-verified this — the string
"4.55" does not occur in the document).

**Table, footnote, and closing prose now agree.** The table says "No" for all three benchmark rows
(SWE-bench, WebArena, AgentBench). The closing prose (lines 512–517, EN) states: "after correcting
for having tested three benchmarks, none of the three individual comparisons clears a properly
adjusted significance bar at this sample size." This now matches the table's three "No" entries and
the corrected WebArena footnote. The three-way contradiction the Pass 3 finding identified
(table "Yes" vs. footnote self-contradiction vs. closing-prose "none clear the bar") is fully
resolved — the document is now internally consistent everywhere I checked.

**Verdict on (a): defect resolved**, independently recomputed and confirmed correct.

---

## 4. (b) Consistency Across English and Chinese

The §11 footnote is written in the required EN-paragraph-then-ZH-paragraph pairing (lines
496–502 English, 504–510 Chinese). I read both in full and checked the Chinese independently rather
than assuming it mirrors the English:

> 得出 `b = 16`、`c = 6`。使用本模块通篇采用的连续性校正公式（见第 6 节）：
> `χ² = (|16−6|−1)²/(16+6) = 81/22 ≈ 3.68`。这一数值甚至未能越过未经调整的 α=0.05 对应的临界值
> 3.84（第 6 节）——因此更不必说更严格的、按第 7 节 `α/m` 逻辑在 `m=3` 时得出的 Bonferroni
> 校正阈值了：后者要求 `α = 0.05/3 ≈ 0.0167`，对应的临界 χ² 约为 5.73。

This carries the identical numbers (3.68, 3.84, 0.0167, 5.73) and the identical logical structure
("falls short of the unadjusted threshold, therefore also short of the stricter one") as the
English. No stray 5.14, 4.55, or "是"/"Yes"-equivalent significance claim remains in the Chinese
text.

The closing prose is likewise paired (EN lines 512–517, ZH lines 519–522) and both state the same
"none of the three clears the bar" conclusion — I checked this is not a case where the English was
fixed but the Chinese mirror was left stale, which is exactly the kind of drift a single-file
bilingual document is supposed to make cheap to catch (`curriculum/README.md` §4: "a reader
comparing a paragraph against its translation is the cheapest error check this curriculum has").

The table itself (lines 490–494) is written once, language-neutral, per the bilingual convention's
explicit allowance ("Code blocks, math/formulas, and tables are written once … but any prose
sentence introducing or explaining them still follows the EN-paragraph-then-ZH-paragraph pattern")
— correctly so; both the EN and ZH footnotes explain the same single table.

**Verdict on (b): consistent in both languages.**

---

## 5. (c) No New Error Introduced; Surrounding Text Reads Coherently

I re-read all of §11 (lines 477–523) and re-checked the other two table rows for consistency, since
a targeted fix to one row is exactly the kind of change that can silently break an adjacent one:

- **SWE-bench row** (b=7, c=2, from §6): `χ² = (|7−2|−1)²/(7+2) = 16/9 ≈ 1.78` — matches the
  table's stated 1.78 and §6's own worked derivation. Unaffected by the WebArena fix, correctly
  still "No."
- **AgentBench row**: stated χ²=0.20, "No." No paired-cell breakdown is given for this row (unlike
  WebArena), consistent with how the document already treated AgentBench before this fix — this is
  not something the Pass 3 finding asked to be changed, and I did not find any inconsistency
  introduced around it. I note it only as an observation, not a defect: a b/c breakdown for
  AgentBench would let a future reader recompute all three rows uniformly, but its absence predates
  and is outside the scope of the Pass 3 finding.
- **§11's opening and closing prose** (lines 481–483, 512–517) both describe the table's structure
  and conclusion accurately against the table as it now stands — no leftover reference to a
  "Harness A wins" framing or to the old 5.14/Yes result anywhere in the surrounding narrative.
- **§6 and §7**, which §11's footnote explicitly leans on (the continuity-corrected formula and the
  Bonferroni `α/m` logic respectively), are unchanged and still support the recomputation exactly
  as before — the fix did not require, and did not receive, any drive-by edit to those sections
  that might have introduced a new inconsistency.

I found no new arithmetic, formatting, or narrative defect introduced by the fix.

**Verdict on (c): no new error; the section reads coherently.**

---

## 6. (d) Metadata Block and Inline-Gloss Spot Check

**Metadata block (lines 1–9).** Current state:

```
# Rigorous Agent Evaluation: Statistical Methodology

**智能体评估的统计学方法论**

**Level:** Advanced · **Cluster:** Multi-Agent Systems & Evaluation · **Author:** Dr. Mireille Dubois, Research Scientist — LLM Systems, ANU-00

**级别：** 高级 · **主题群：** 多智能体系统与评估 · **作者：** ANU-00 LLM 系统研究员 Mireille Dubois 博士

---
```

This matches `curriculum/README.md` §4.1's canonical Format B exactly: compact bold `Level ·
Cluster · Author` line immediately followed by its Chinese mirror, all three fields present, full
roster identity ("Dr. Mireille Dubois, Research Scientist — LLM Systems, ANU-00") rather than a
bare surname, and the `---` rule before the first section heading. Author and cluster both match
`curriculum/README.md` §7 (module index) and §7.2 (roster cross-check) exactly.

**`harness` → 运行框架 (C-1 harmonization).** `curriculum/README.md` §4.2 flags this document by
name as one of four with the deprecated `执行框架` rendering. I grepped the current file for
`执行框架`: zero occurrences. Every instance of "harness" in the Chinese text (`运行框架`, e.g.
lines 120, 127–128, 479, 485, 519) uses the canonical rendering consistently.

**Inline gloss spot-check.** I grepped for the `English（中文）` gloss pattern. Occurrences found:
`Wilson score interval（Wilson 得分区间）` (line 84, a named statistical method, first use),
`bootstrap（自助法 / 自助抽样法）` (line 199, a named method, first use), `Bonferroni
correction（Bonferroni 校正）` (line 290, a named method, first use), and `pass^k（读作
"pass-hat-k"）` (lines 335 and 347 — a pronunciation note on a named metric, appearing once in the
English paragraph and once in its paired Chinese translation, not a duplicate gloss). All of these
are named methods/metrics carrying an established name, which §4's rule explicitly permits to be
glossed on first use ("a named model, framework, benchmark, paper, or method that carries an
established name"). I found no gloss of an ordinary technical concept (e.g. no
"success rate（成功率）" or "confidence interval（置信区间）"-style instance) — nothing obviously
out of conformance with the narrowed C-3 rule turned up in this pass.

**Verdict on (d): metadata block matches the canonical format; no obviously-wrong inline gloss
found.** (Per the task's own scoping, this is a quick spot-check, not the exhaustive corpus-wide
C-2/C-3 audit, which belongs in the closing synthesis.)

---

## 7. Overall Verdict

**PASS — the Pass 3 defect is resolved.**

- The WebArena McNemar χ² is correctly recomputed from the stated b=16, c=6 inputs using the
  document's own continuity-corrected formula: 3.68, independently verified by me via a fresh
  hand/script computation and a fresh check of the correction formula itself against an external
  source (CRAN `exact2x2` vignette; LibreTexts).
- The table entry, the footnote's recomputation, and the closing prose all now agree with each
  other and with the correct value: "No" significance, consistently, everywhere in the section.
- The old, wrong 5.14 figure and the footnote's self-contradictory 4.55/5.14 juxtaposition are both
  fully gone — not just superseded but absent from the text.
- The fix is present and consistent in both the English and Chinese text.
- No new error was introduced; §11's surrounding rows, prose, and its dependencies on §6/§7 remain
  internally coherent.
- The metadata block conforms to `curriculum/README.md` §4.1's canonical Format B, and the
  document's `harness` renderings are fully harmonized to `运行框架` with zero remaining
  `执行框架` occurrences. No obviously-wrong inline gloss surfaced in a quick pass.

---

## 8. Scope Boundary

**Did I edit any curriculum document?** No — this file is a review record only, per
`curriculum/README.md` §8 rule 4 (point-in-time discipline for reviews).

**Out of scope for this review:** A full C-2/C-3 corpus-wide metadata-format and inline-gloss audit
(reserved for the closing synthesis review, per the task's own instruction); re-review of any other
document or finding from Pass 3; the AgentBench row's missing b/c breakdown, noted above as an
observation but not evaluated as a defect since it is unrelated to the finding this re-review was
scoped to.

---

**Dr. Rafael Ibarra-Costa, Research Scientist — Generalist, ANU-00 — 2026-08-19**
