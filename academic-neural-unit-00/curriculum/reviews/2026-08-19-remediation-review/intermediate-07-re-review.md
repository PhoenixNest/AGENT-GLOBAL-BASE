# Pass 4 Re-Review — `intermediate/07-multi-agent-communication-and-coordination-protocols.md`

**Reviewer:** Dr. Rafael Ibarra-Costa, Research Scientist — Generalist, ANU-00
**Document re-reviewed:** `academic-neural-unit-00/curriculum/intermediate/07-multi-agent-communication-and-coordination-protocols.md`
**Document author:** Dr. Kaito Fujimori (Agent Systems Research) — not this reviewer
**Review date:** 2026-08-19
**Review pass:** Pass 4 remediation re-review, per `academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` (Joint
Recommendation, l. 251): "the four documents with blocking-severity findings (`intermediate/07`,
`advanced/05`, `advanced/08`, and `intermediate/04`) should be re-reviewed by a reviewer other than
their author before close, per README §6's independence rule." This is a re-review of one prior
finding against one document, not a fresh full-document cluster review — item scope is the P1
recorded against `intermediate/07` §6 in `academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/internal/multi-agent-evaluation-cluster-review.md` and
upheld in `academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` (l. 87, l. 202), plus a bounded spot-check of the
corpus-wide C-1/C-2/C-3 harmonization items as they apply to this one file.

---

## 0. Independence Declaration

**Did I author this document?** No — Dr. Kaito Fujimori is the author of record
(`curriculum/README.md` §7). I authored `introductory/06` and `intermediate/06`, neither of which
is this document.

**Relationship to the original finding:** I am the same reviewer who raised the original P1 against
this document's §6 in Pass 1 (`academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/internal/multi-agent-evaluation-cluster-review.md`), as the
ratified cluster reviewer for Multi-Agent Systems & Evaluation (`curriculum/README.md` §6, §7.2 —
"Ibarra-Costa reviews Multi-Agent & Evaluation (Fujimori, Dubois, Bhandari)"). Being the original
flagger of a defect is not the independence conflict README §6 and the CEO's re-review instruction
guard against — the conflict guarded against is an author re-reviewing their own fix. I am not the
author, so the independence rule is satisfied. I have treated this as an obligation to verify the
fix as skeptically as I would anyone else's, not to wave through my own earlier finding.

**Anything else that would compromise independence:** None.

---

## 1. Method

I did not trust the Pass 3→4 changelog or take "fixed" on faith. For the core defect (item (a)
below) I went back to the primary source myself, independent of what the document now cites.

| What I did                                | Detail                                                                                                                                                                                                                                                                                                                                                             |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Independent source consulted              | Fetched `https://www.anthropic.com/engineering/multi-agent-research-system` directly (three separate targeted fetches: full inventory of every "90%"/"90.2%" occurrence and its comparison; the paragraph establishing the baseline for the time-reduction claim; and the exact "orchestrator-worker pattern" quote) — not the document's own citation, read fresh |
| Publication date verified                 | Web search confirmed the post's publish date as 13 June 2025, consistent with the document's "June 2025" attribution                                                                                                                                                                                                                                               |
| Author-supplied citations opened          | 1 of 1 relevant to this finding (the Anthropic post itself); also re-confirmed the References-section entry resolves and is titled/authored correctly                                                                                                                                                                                                              |
| Claims spot-checked against those sources | Both "90%" figures in §6 (time-reduction and quality-improvement), the orchestrator-worker direct quote, and the June 2025 date                                                                                                                                                                                                                                    |
| Chinese-language read                     | §6 read in full, paragraph-by-paragraph against its English counterpart; remainder of the document (§§1–5, 7–9, References) read in full in both languages for the coherence and metadata/gloss spot-checks in (c)/(d)                                                                                                                                             |

---

## 2. (a) Independent Verification of the Core Defect

### 2.1 What the original finding said

Pass 3, upheld in `academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` (l. 87): the document attributed Anthropic's
"up to 90%" figure to a single-agent-vs-multi-agent comparison, when in the source the 90% figure
is a **time reduction** from a **parallelization change** (parallel subagent dispatch and parallel
tool calls, replacing the team's own earlier **sequential** execution) — not a single-agent
baseline at all. The source's actual single-agent-vs-multi-agent number is a separate **90.2%
quality** improvement on an internal research eval.

### 2.2 What I found at the primary source, independently

I fetched the Anthropic post myself and extracted every occurrence of "90%"/"90.2%":

- **Time figure:** "Our early agents executed sequential searches, which was painfully slow. For
  speed, we introduced two kinds of parallelization: (1) the lead agent spins up 3-5 subagents in
  parallel rather than serially; (2) the subagents use 3+ tools in parallel. These changes cut
  research time by up to 90% for complex queries... " — baseline is explicitly "our early agents
  executed sequential searches," i.e. the team's own prior architecture. **Not** a single-agent
  vs. multi-agent comparison.
- **Quality figure:** "We found that a multi-agent system with Claude Opus 4 as the lead agent and
  Claude Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2%" — this is the
  source's actual single-agent-vs-multi-agent comparison, and it is a performance/quality metric,
  not a time metric.
- I also independently confirmed the post's publish date (13 June 2025) and the exact wording of
  the "orchestrator-worker pattern... lead agent coordinates the process while delegating to
  specialized subagents that operate in parallel" quote the document uses — verbatim match.

This independent recomputation reproduces the original finding exactly: two distinct "90%"-family
figures, different mechanisms, different baselines, and the document must not conflate them.

### 2.3 What the document now says (current text, §6, EN)

> "That post reports two different '90%' figures, and they measure two different things, so it is
> worth keeping them apart precisely: parallelizing subagent dispatch and tool calls — running
> several subagents at once, and letting each subagent call several tools at once, rather than
> running everything serially as the team's system originally did — cut research time by up to 90%
> for complex queries, a speed comparison against the team's own earlier _sequential_ execution,
> not against a single-agent baseline. Separately, on an internal research evaluation, a
> multi-agent system with a Claude Opus 4 lead agent and Claude Sonnet 4 subagents outperformed a
> single-agent Claude Opus 4 baseline by 90.2% — a quality figure, and the post's actual
> single-agent-versus-multi-agent comparison (Anthropic, 2025)."

This matches what I independently verified at the source, point for point: mechanism (parallel
dispatch + parallel tool calls), baseline (the team's own prior sequential execution, not
single-agent), and the correct attribution of the 90.2% figure as the actual
single-agent-vs-multi-agent comparison. **The defect described in the Pass 3 finding is resolved.**

---

## 3. (b) English/Chinese Consistency of the Fix

The Chinese paragraph immediately following (§6, ZH) carries the identical correction, not a
looser or drifted paraphrase:

> "该文中报告了两个不同的'90%'数字，二者衡量的是完全不同的东西，值得在此精确区分开来：...把复杂查询
> 的研究耗时最多缩短了 90%，这是与该团队自身此前的*串行*执行方式相比较所得出的速度提升，而并非与单
> 智能体基线的比较。另外，在一项内部研究评测中，...相较于单智能体 Claude Opus 4 基线，表现提升了
> 90.2%——这是一个质量指标，也是该文中真正意义上'单智能体对比多智能体'的数字（Anthropic, 2025）。"

Checked clause-by-clause against the English: "并非与单智能体基线的比较" mirrors "not against a
single-agent baseline"; "这是一个质量指标，也是...真正意义上'单智能体对比多智能体'的数字" mirrors "a
quality figure, and the post's actual single-agent-versus-multi-agent comparison." No drift, no
softening, no omission in either direction. The fix is present and consistent in both languages.

---

## 4. (c) No New Error Introduced; Coherence Check

- The corrected sentences are internally consistent with the rest of §6: the paragraph still
  correctly identifies the topology as hierarchical/orchestrator-worker, still cites the two
  parallelization mechanisms accurately, and the transition into "In a flat topology..." reads
  cleanly immediately after the corrected material — no orphaned clause or dangling reference left
  over from the edit.
- The direct quote ("orchestrator-worker pattern, where a lead agent coordinates the process while
  delegating to specialized subagents that operate in parallel") is verbatim-correct against the
  source — re-verified independently in this pass, not just carried over from Pass 3.
- The "June 2025" date attribution is correct — the source was published 13 June 2025, confirmed
  independently via web search — no error.
- The References-section entry — `Anthropic (2025). How We Built Our Multi-Agent Research System
(Anthropic Engineering)`, linking to the exact URL fetched in this review — resolves correctly
  and is not misattributed.
- No new numeric, attributional, or citation error was introduced by the rewrite. The surrounding
  prose (topology definitions in §6, the transition to §7's worked example) reads coherently; the
  fix is a contained, well-integrated correction, not a patch that reads as bolted on.

---

## 5. (d) Metadata Block and Inline-Gloss Spot Check

**Metadata block.** The document's opening block:

```
# Multi-Agent Communication & Coordination Protocols
**多智能体通信与协调协议**
**Level:** Intermediate · **Cluster:** Multi-Agent Systems & Evaluation · **Author:** Dr. Kaito
Fujimori, Research Scientist — Agent Systems Research, ANU-00
**级别：** 中级 · **主题群：** 多智能体系统与评估 · **作者：** ANU-00 智能体系统研究员 Kaito
Fujimori 博士
---
```

This matches `curriculum/README.md` §4.1's one canonical format exactly: three required fields
(Level, Cluster, Author) on a bold middle-dot-separated line, immediately followed by its Chinese
mirror line carrying the same three fields in the same order, Author given as full roster identity
(name + role + ANU-00, matching `crew/README.md`), then the `---` rule. Conformant — no defect.

**C-1 (harness → 运行框架) check.** `curriculum/README.md` §4.2 names `intermediate/07` as one of
four documents that needed the deprecated `执行框架` corrected to the canonical `运行框架`. I
grepped the current file for both strings: `执行框架` returns zero matches; `运行框架` appears twice
(§2, both instances correctly rendered — "这与运行框架先根据工具名称进行分派..." and "...在 LLM 与
运行框架之间的脆弱程度"). The C-1 harmonization is applied correctly in this document.

**C-3 (inline-gloss) quick pass.** Scanned every `（English...）`-style inline gloss in the
document. All instances found are proper nouns or named works on first use, per the narrowed §4
rule — FIPA / FIPA ACL (named organization and named specification), the Smith 1980 and
Hayes-Roth 1985 paper titles, the Eugster et al. 2003 paper title and venue (_ACM Computing
Surveys_), and the Wu et al. citation. No ordinary technical concept (e.g. "message,"
"blackboard," "publish-subscribe," "performative") carries a spurious parenthetical English gloss
— those are correctly left to the paired EN-paragraph/ZH-paragraph structure alone, as §4 requires.
I did not find an obviously-wrong inline gloss. This is a spot-check only, not the exhaustive
corpus-wide C-2/C-3 audit, which belongs to the closing synthesis.

---

## 6. Verdict

**PASS — the Pass 3 defect is resolved.**

- (a) Independently re-verified against the primary source (not the document's own citation): the
  90% figure is correctly attributed as a time reduction from parallelization, baselined against
  the team's own earlier sequential execution — not a single-agent comparison; the 90.2% figure is
  correctly identified as the source's actual single-agent-vs-multi-agent comparison and correctly
  labeled a quality metric. Confirmed.
- (b) The fix is present and word-for-word consistent in meaning between the English and Chinese
  paragraphs of §6. Confirmed.
- (c) No new error was introduced; the corrected passage reads coherently with the surrounding
  text, the direct quote and date remain verbatim-correct, and the citation resolves. Confirmed.
- (d) The metadata block conforms to the README §4.1 canonical format; the C-1 harness-term
  correction is applied cleanly (zero remaining `执行框架` occurrences); no obviously-wrong inline
  gloss was found in a non-exhaustive spot-check. Confirmed.

No blocking or non-blocking issue remains against this document from the Pass 3 finding. I am not
aware of any other open item against `intermediate/07` from Pass 1–3 records (its only recorded
blocking finding was this one, per `academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` l. 202).

---

## 7. Scope Boundary

**Did I edit the document?** No — this file records findings only, per README §6/rule 4 (a
re-review is a new file, never an edit to the document or to the report it follows up on).

**Out of scope for this review:** A full fresh read of `intermediate/07` against every C-2/C-3
harmonization dimension across the whole corpus (that is the closing synthesis's job, not a
single-document re-review); the remediation status of the other three Pass-4-flagged documents
(`advanced/05`, `advanced/08`, `intermediate/04`) — each requires its own independent re-review;
and any item in `academic-neural-unit-00/curriculum/reviews/2026-08-18-first-review-cycle/comprehensive-review.md` not connected to the specific finding this
re-review was scoped to verify.

---

**Dr. Rafael Ibarra-Costa, Research Scientist — Generalist, ANU-00 — 2026-08-19**
