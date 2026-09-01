# Final Review — ANU-00 Agent Development Curriculum, First Draft (24 Modules)

**Requested by:** CEO, under approval of `academic-neural-unit-00/plans/2026-08-17-curriculum-first-production-run/curriculum-development-plan.md` (relocated from `curriculum/curriculum-development-plan.md` after this review was filed); executed as Pass 3 of `curriculum/README.md` §6.

**Reviewers:** Dr. Mireille Dubois (Research Scientist — LLM Systems; Foundations cluster), Dr. Aditi Bhandari (Staff Research Scientist — Foundational AI Lead; Agent Architecture & Design Patterns cluster), Dr. Yuna Baek (Research Scientist — AI / Neural Networks; Prompt & Context Engineering cluster), Dr. Rafael Ibarra-Costa (Research Scientist — Generalist; Multi-Agent Systems & Evaluation cluster), Tobias Lindqvist (Knowledge Systems Engineer; structural / taxonomy / bilingual-formatting pass across all 24), External Reviewer A (independent PhD-level AI/ML researcher; technical accuracy and citation validity), External Reviewer B (hiring manager / technical interviewer at a top AI lab; interview readiness), and Dr. Naledi Mokoena (ANU-00 Lead; Pass 3 synthesis).

Per `curriculum/README.md` §6, Pass 3 sign-off is the Lead's alone. The seven reports listed above are **inputs** to this record, not co-signatures on it — where I override one of their verdicts below, I say so and give the evidence.

**Date:** 2026-08-18 — the date carried by all seven sub-reports, one day after this curriculum's README was ratified (2026-08-17). This synthesis was run the same day the last sub-report was filed; I have not inferred any later date.

**Scope:** Whether the first complete draft of the 24-module bilingual curriculum is fit to ship to the audience `curriculum/README.md` §1 defines, and a per-document pass / needs-revision verdict on all 24 modules.

**Status:** For CEO decision. Closes Pass 3 and completes this review cycle. Author remediation and any re-review are a separately scoped follow-up run, per `curriculum/README.md` §6's own scope boundary — a "needs revision" verdict here is a complete result of this cycle, not an unfinished one.

---

## Method

None of this is restated from the sub-reports. I read all seven review reports in full, and then went back to the curriculum source myself for three categories of claim: (a) every finding where two reviewers covering the same text reached opposite conclusions, (b) every finding any reviewer classified as blocking, and (c) every finding one reviewer raised that another reviewer looking at the same document did not. Where a defect was mechanically checkable, I checked it mechanically across all 24 files rather than trusting a per-cluster sample — which is how I found the one substantial defect no sub-report contains.

Three of my own checks changed a verdict a sub-report reached. One produced a finding that appears in none of the seven reports.

| Record checked                                                                            | What it was checked for                                                                                                                                                                                                                             |
| ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `internal/foundations-cluster-review.md`                                                  | Dubois's 8 recorded problems; her Pass verdicts on all 6 Foundations documents; her flag that the rendering defect might recur outside her cluster                                                                                                  |
| `internal/agent-architecture-cluster-review.md`                                           | Bhandari's cluster-wide harness-translation finding; her Pass verdicts on all 6 Agent Architecture documents; what her exhaustive check of `intermediate/04` §5 did and did not cover                                                               |
| `internal/prompt-context-cluster-review.md`                                               | Baek's P0 against `advanced/05`; her three needs-revision verdicts; her 信达雅 Pass on Dr. Tan's four modules                                                                                                                                       |
| `internal/multi-agent-evaluation-cluster-review.md`                                       | Ibarra-Costa's P0 against `advanced/08` §11 and P1 against `intermediate/07` §6 — both directly contradicted by an external reviewer                                                                                                                |
| `internal/structural-bilingual-taxonomy-review.md`                                        | Lindqvist's 12 structural findings, his 7 needs-revision verdicts, and the scope boundary he declared (which is where the gap below opens)                                                                                                          |
| `external/external-technical-accuracy-review.md`                                          | External A's 17-claim spot-check and 24-citation audit; the `intermediate/04` arithmetic slip it found that no internal report contains; its blanket claim that every worked example recomputes correctly                                           |
| `external/external-interview-readiness-review.md`                                         | External B's parochialism finding, the zero-code and zero-RLHF gaps, and its verdicts on the two claims the internal reviewers called blocking                                                                                                      |
| `advanced/08-rigorous-agent-evaluation-statistical-methodology.md` §11 (l. 491–523)       | The WebArena McNemar table, its footnote, and the section's closing prose — both χ² formulas recomputed by hand from the stated `b=16, c=6`, and the EN footnote read against its ZH pair                                                           |
| `intermediate/07-multi-agent-communication-and-coordination-protocols.md` §6 (l. 261–285) | The disputed Anthropic "up to 90%" sentence, read in full in both languages against what the cited post actually attributes that figure to                                                                                                          |
| `advanced/05-advanced-context-engineering-long-context-and-budgeting.md` §6 (l. 195–211)  | The disputed RULER sentence, read in full in both languages, and compared against the neighbouring sentence External B actually spot-checked                                                                                                        |
| `advanced/08` §6 (l. 259–262), `advanced/08` §3, `introductory/01` §6–§9                  | Three worked examples I recomputed by hand as controls — McNemar at `b=7, c=2`; the Wilson interval at `p̂=0.84, n=50`; the full sigmoid forward/backward pass — to establish whether §11's defect is isolated or symptomatic                        |
| `intermediate/04-agent-memory-systems-short-term-long-term-episodic.md` §5 (l. 267–290)   | External A's "5 天（200 小时）" finding, absent from the internal review of that same worked example                                                                                                                                                |
| `intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md` §11, §1          | The stray-blockquote defect (`grep -n "^>"`, run corpus-wide), and the Lewis et al. co-author count                                                                                                                                                 |
| `intermediate/01` §3 (l. 119), `advanced/02` §6 (l. 281)                                  | The two blank-line-plus-leading-dash rendering defects, plus a corpus-wide scan for further instances of the same pattern                                                                                                                           |
| `intermediate/01` l. 432, `advanced/01` l. 321, `introductory/08` l. 353                  | The three reported orphan citations — each traced through its whole document body, not just confirmed present in the reference list                                                                                                                 |
| All 24 module files (mechanical scans)                                                    | Half-width vs. full-width punctuation adjacent to CJK (878 instances found, 868 of them in four files); `执行框架`/`运行框架` counts per file; all 24 H1 lines against README §7; the metadata block on every flagged document; code-fence presence |
| `curriculum/README.md` §1, §4, §5, §6, §7                                                 | The bar this draft is judged against, the severity scale the sub-reports were meant to apply, and the Pass 3 output specification                                                                                                                   |
| All 24 module files, first ~15 lines                                                      | Presence, field set, structural format, and language of the opening metadata block                                                                                                                                                                  |
| All 24 module files, ≥3 sampled passages each, plus a corpus-wide regex sweep             | Whether English/Chinese content is separated at the paragraph level throughout or mixed within one paragraph, and every parenthetical bilingual gloss                                                                                               |

---

## Dr. Mireille Dubois — Foundations Cluster (`introductory/01–02`, `intermediate/01–02`, `advanced/01–02`)

- I re-opened both rendering defects she logged. Both are real and both sit inside the load-bearing formula of their section. `intermediate/01` line 119 begins `- ε) 更新参数，…`, which splits the Adam update rule mid-formula and renders the remainder as a bullet-list item; `advanced/02` line 281 begins `- (0.125)(0.2) + …`, doing the same to the load-balancing-loss sum. Her description of both is exact.
- I confirmed both orphan citations she reported by tracing them through the whole document, not just the reference list. `Ioffe & Szegedy (2015)` occurs in `intermediate/01` only at line 432; batch normalization is named nowhere in the body. `Brown et al. (2020)` occurs in `advanced/01` only at line 321; the only other "Brown" in that file is a co-author inside the Kaplan et al. author list, exactly as she says.
- **A check that could have gone wrong but did not:** she flagged, without ruling on it, that the rendering defect might recur outside her cluster if it came from a shared formatting step. I scanned all 24 files for the pattern. There are exactly two instances, and both are the two she found. It is a local wrapping artifact in two files, not a corpus-wide production fault — her instinct to flag it was right, and the answer is reassuring.
- I re-derived her hardest arithmetic myself rather than accepting it: the `introductory/01` §6–§9 forward/backward pass (`z=0.2`, `σ(0.2)≈0.5498`, `L≈0.1014`, `∂L/∂w₁≈−0.1114`, `w₁_new≈0.4111`) recomputes exactly. Her cluster's numeric verification is sound.
- **One open item, named plainly:** her four half-width-comma instances in `intermediate/01` and four in `advanced/01` are recorded as an isolated, minor P2. My corpus-wide scan says otherwise — see the Baek and Lindqvist sections below, where the same defect class turns out to affect 868 further instances in four documents she was never assigned. Her finding was correct and her scope was correct; the inference that it was isolated was not available to her.

**My conclusion:** Findings sound and independently reproduced; nothing in her report failed re-checking. I override her Pass verdicts on `intermediate/01` and `advanced/02` — not on her evidence, which I accept in full, but on severity consistency: Lindqvist rated a defect of the identical class (a stray Markdown character corrupting one rendered paragraph in `intermediate/06`) as needs-revision in this same cycle. The same defect class cannot yield two different verdicts in one review round, and a corrupted formula is the more damaging of the two. Her own "the one thing I would fix first" names exactly these two defects.

---

## Dr. Aditi Bhandari — Agent Architecture & Design Patterns Cluster (`introductory/03–04`, `intermediate/03–04`, `advanced/03–04`)

- Her central finding — that "harness" carries two competing standing Chinese translations — is correct, and it is broader than the cluster she was given. I counted both renderings across all 24 files. The split runs through **eight documents in three clusters**: `introductory/03` (执行 6 / 运行 1), `introductory/04` (11 / 0), `intermediate/03` (1 / 2), `intermediate/04` (0 / 3), `intermediate/07` (2 / 0), `advanced/03` (0 / 40), `advanced/04` (0 / 16), `advanced/08` (14 / 0).
- This changes the remediation scope materially. Her recommended fix — standardize on `运行框架`, update `introductory/03` and `introductory/04` — would leave `intermediate/07` and `advanced/08` stranded on `执行框架`, and `advanced/08` is the second-heaviest user of the term in the entire corpus at 14 occurrences. Neither document is in her cluster; Ibarra-Costa reviewed both and passed their bilingual check without noting the term. This is a defect only a cross-cluster pass can see, and none of the seven reports contains it. I have therefore promoted it out of the per-document tables into a corpus-wide item (C-1 below), so the fix is scoped once and applied to all eight.
- I confirmed External Reviewer A's `intermediate/04` §5 finding, which her cluster review does not contain: line 280 glosses "accessed 200 hours ago" as "5 天（200 小时）前". 200 hours is 8.33 days. The English at line 267 says only "200 hours ago" and makes no day claim — the error exists solely in the Chinese. It sits inside the very worked example she checked, in her words, exhaustively.
- **A check that could have gone wrong but did not:** I re-checked whether that slip undermines her verification of the rest of that example. It does not. The retrieval-scoring formula, the 0.995-per-hour decay, the 1–10 importance scale, the 150-point reflection threshold, and the recomputed decay values (`0.995⁵ ≈ 0.975`, `0.995²⁰⁰ ≈ 0.367`) all hold exactly as she reported. Her verification was rigorous; the blind spot is specific and instructive — she checked the translation against its source **for meaning**, which is what §4 asks for, and the defect is an arithmetic claim the Chinese adds that the English never makes. No meaning-level check would catch it.
- **One open item, named plainly:** on my verdict rule, that gloss moves `intermediate/04` to needs-revision — it states something numerically false to a Chinese-reading student inside a worked example, in a chapter about memory scoring. Her Pass verdict on that one document is overridden on evidence she did not have, not on a disagreement with her reasoning.

**My conclusion:** Findings sound; one verdict overridden on new evidence. Her independent verification of `intermediate/04` §5 against the Generative Agents paper and of `advanced/04`'s OWASP category IDs, the three-way Excessive Agency breakdown, and the NIST AI RMF functions is the most demanding citation work in the internal set, and none of it failed re-checking.

---

## Dr. Yuna Baek — Prompt & Context Engineering Cluster (`introductory/05–06`, `intermediate/05–06`, `advanced/05–06`)

- **On the disputed RULER claim she is right, and she is not actually in conflict with the external reviewer.** `advanced/05` §6 lines 203–205 read: "among models claiming context windows of 32K tokens or more, only a small number actually maintained satisfactory performance at 32K on RULER's fuller task suite" — with the Chinese at line 211 carrying the same understatement (`只占少数`). Hsieh et al.'s own headline finding is that **half** of them do. External Reviewer B marked this section "Correct", but the sentence B spot-checked is the _preceding_ clause — that models scoring near-perfect on needle-in-a-haystack degrade well before their claimed length — which is accurate. Two reviewers checked two different sentences in the same paragraph. There is no genuine disagreement here to adjudicate, only a coverage gap in the external pass, and I want that on the record so this does not read to the CEO as an unresolved expert dispute.
- I do reclassify its severity, downward within the blocking band. Understating a cited paper's headline number is not fabrication, not misattribution, and not a wrong formula; it is a factual claim that is wrong, which is P1 on §5's own scale, not P0. Both are blocking and the document's verdict is unchanged — but the CEO should not be told this corpus contains a fabricated citation, because after seven reviews and my own re-check, it does not.
- I confirmed the `intermediate/06` §11 blockquote defect directly: `grep -n "^>"` returns lines 787–790 of that file and nothing else in any of the 24 files. I also confirmed the Lewis et al. co-author miscount at line 119 ("Patrick Lewis and twelve co-authors" for a 12-author paper) and the stale prerequisite note in `advanced/06` at lines 17–18 and 326.
- **The finding no sub-report contains, and it is hers by cluster:** I ran a mechanical punctuation scan across all 24 files. Dr. Wei-Ling Tan's four modules — `introductory/05`, `intermediate/05`, `advanced/05`, `advanced/06` — contain **zero full-width commas**. Their entire Chinese text uses half-width ASCII punctuation: 868 instances of a half-width comma, colon, or semicolon directly following a CJK character (192 / 167 / 255 / 254 respectively). Every one of the other twenty documents uses full-width punctuation throughout (`introductory/06`, by comparison: 175 full-width commas, zero half-width). This is not a scattering of typos — it is a wholesale deviation from Chinese typographic convention across one author's entire output, and it is exactly the "machine-like" tell §4 forbids and that Dubois's regex sweep was built to catch. Baek read all four documents in full and passed them on 信达雅; the prose itself genuinely is fluent, which is what she was scoring. The punctuation layer fell between her content-quality read and Lindqvist's explicitly declared exclusion of translation quality. I am recording this against the four documents and, separately, as a process finding.
- **One open item, named plainly:** her `advanced/06` verdict rests on the stale-prerequisite note causing "unacknowledged duplication". I checked the duplication claim itself and it is fair — §1 does re-derive RAG, BM25, SBERT and DPR — but I would not have blocked the document on the duplication alone, only on the now-false statement of fact in reader-facing prose. The verdict stands; the reason narrows.

**My conclusion:** Findings sound, all three needs-revision verdicts upheld, one severity reclassified P0 → P1. The one thing her report misses is in her own cluster and is the largest single defect in the corpus by instance count — recorded here, with no implication that her content review was less than thorough.

---

## Dr. Rafael Ibarra-Costa — Multi-Agent Systems & Evaluation Cluster (`introductory/07–08`, `intermediate/07–08`, `advanced/07–08`)

- **`advanced/08` §11 — I recomputed it and his P0 is correct, and understated.** The table at line 494 prints WebArena `McNemar χ² = 5.14` with the `p < 0.05/3?` column reading **Yes**. The footnote at lines 498–505 states the inputs `b = 16, c = 6`, and from those inputs the continuity-corrected formula this document teaches in §6 gives `(|16−6|−1)²/22 = 81/22 ≈ 3.68` and the uncorrected form gives `100/22 ≈ 4.55` — I derived both by hand. Neither is 5.14, and no derivation of 5.14 is offered anywhere. Worse than he records: the footnote announces it is "using the uncorrected `χ² = 100/22 ≈ 4.55` here", then two lines later reasons about "5.14 falls short of that stricter bar", so the footnote contradicts _itself_ as well as the table. And its conclusion (not significant), plus the section's closing prose at lines 513–518 ("none of the three individual comparisons clears a properly adjusted significance bar"), both contradict the table's own **Yes**. That is a four-way inconsistency in one worked example.
- **A check that could have gone wrong but did not, and it matters for scoping:** I recomputed two other worked examples in the same document as controls. §6's McNemar at `b=7, c=2` gives `(|7−2|−1)²/9 = 16/9 ≈ 1.78`, exactly as printed. §3's Wilson interval at `p̂=0.84, n=50` gives `[0.715, 0.917]`, exactly as printed. The defect is localized to §11's illustrative table, not symptomatic of the document's statistics. This is why External Reviewer A's blanket claim that "every one independently recomputed... reproduces correctly to the stated precision" is not dishonest — A checked the §6 example, which is correct — but it is not true of §11, which A did not check. His finding stands over A's generalization.
- **`intermediate/07` §6 — I side with him against both external reviewers, and the reason is specific.** I read lines 261–285 in both languages. The document says Anthropic's post describes the orchestrator-worker pattern "reporting that this design reduced research time by up to 90% for complex queries compared to a single-agent approach on the same task." In the cited post, the 90% time reduction is attributed to a parallelization change — the lead agent spinning up subagents in parallel rather than serially, and subagents calling tools in parallel — measured against the team's own earlier sequential execution, not against a single-agent baseline. The post's actual single-agent-versus-multi-agent number is a **90.2% improvement on an internal research eval**, a quality figure, not a time figure. Two adjacent numbers, both "90", one of which is being asked to do the other's work. Both external reviewers confirmed that a "90%" figure appears in the post and stopped there; neither checked what it was measured against. That is the whole of the disagreement, and it resolves in his favour. P1 upheld.
- I confirmed the internal-workspace citation he checked in `advanced/07`: §4 does cite `core-component-00/framework/05-multi-agent-engineering/fundamentals/git-worktree-orchestration.md` and does narrate the directory-junction incident, and his conclusion that the module represents that source accurately holds.
- **One open item, named plainly:** he records the HELM entry in `introductory/08` as a P3 orphan citation and I confirmed it — line 353 in the reference list, nowhere in the body. It is the third orphan citation of the identical kind in this corpus (with Dubois's two). Individually each is a P3; three of them across three authors is a pattern in the authoring process worth naming rather than filing three times.

**My conclusion:** Both blocking findings independently reproduced and both upheld against contrary external opinion. This report did the single most valuable thing in the cycle — it re-derived a number instead of reading it — and that is what separated a real defect from two external "verified" marks.

---

## Tobias Lindqvist — Structural / Taxonomy / Bilingual-Formatting Pass (all 24 documents)

- I verified all 24 H1 lines against README §7 myself. Exactly four carry a spurious numeral prefix — `# 5. Prompt Engineering Fundamentals`, `# 5. Advanced Prompting: …`, `# 5. Advanced Context Engineering: …`, `# 6. RAG at Scale: …` — and all four are Dr. Wei-Ling Tan's. The other twenty match the README title exactly. His finding is precise.
- I verified the metadata blocks on all six documents he flagged. Tan's four have no Level/Cluster/Author block of any kind; `intermediate/04` and `advanced/03` (both Dr. Inés Roldán) carry a correctly-paired bilingual Level/Cluster line with the Author field absent. Exactly as reported.
- **A check that could have gone wrong but did not:** his claim that the `intermediate/06` blockquote is the only stray `^>` in the corpus is one I could disprove cheaply, so I ran it — `grep -rn "^>"` across all 24 files returns four lines, all of them lines 787–790 of that one file. He is right, and I note that his structural review and Baek's content review found this same defect independently, which is the cross-check the two-pass design exists to produce.
- **This is where I record the process gap, and it is not a criticism of his execution.** He declared his scope in writing and honoured it: no content accuracy, no citation validity, no 信达雅. His automated tooling was a language-alternation classifier — it detects _whether_ a Chinese block is present, not what punctuation convention it uses. So the 868-instance half-width punctuation deviation described in the Baek section above sits precisely in the seam: too typographic for the four content reviewers, who were scoring meaning and fluency; too translation-adjacent for the structural reviewer, who correctly excluded translation quality. Seven reviewers, twenty-four documents, and a defect visible to any fluent reader at a glance went unrecorded. The fault is in the process design, not in any reviewer's work.
- **One open item, named plainly:** his §5 corpus-wide P3 (three competing metadata block formats, none mandated by the README) is a real finding and the README genuinely does not specify one. I am accepting it as a README amendment rather than a document defect, and folding the two missing-Author cases into it — see C-2.

**My conclusion:** Structural findings all reproduced; his diagnosis that Tan's four modules are one systemic gap rather than four incidents is exactly right, and my punctuation scan independently corroborates it from a third direction. I override two of his verdicts downward: `intermediate/04` and `advanced/03` were rated needs-revision on P3-only findings, which is inconsistent with the severity scale this cycle used everywhere else. `advanced/03`'s sole finding is a missing Author line — that is polish, and it moves to Pass under C-2. `intermediate/04` remains needs-revision, but for the `5 天` gloss, not for its metadata.

---

## External Reviewer A — Independent PhD-Level Researcher, Technical Accuracy & Citation Validity

- Its 24-citation deep audit and 17-claim spot-check are the strongest independent evidence in this cycle that the corpus has no fabricated or misrepresented citations. I did not attempt to reproduce all forty facts; I did trace the three orphan-citation cases and the two disputed-claim cases through the source, and nothing in A's audit contradicts what I found.
- **Its most valuable contribution is a finding no internal reviewer produced:** the `intermediate/04` §5 Chinese gloss of "200 hours" as "5 天（200 小时）". I confirmed it at line 280. This is exactly what Pass 2 exists for — an outside reader with no stake in the authorship checked an arithmetic claim in the translation layer that the internal reviewer of that cluster, checking the same passage rigorously for meaning, had no reason to convert.
- **A check that could have gone wrong but did not, in the other direction:** I tested A's blanket claim that every worked numerical example in the corpus recomputes correctly, because Ibarra-Costa's P0 directly contradicts it. It does not survive: `advanced/08` §11's WebArena row cannot be derived from its own stated inputs. A checked §6's McNemar example, which is correct, and generalized from it. I am recording this because a CEO reading A's Overall Verdict alone — "passes cleanly and at an unusually high standard" — would not learn that the corpus's one arithmetic self-contradiction sits in the chapter about not trusting unchecked arithmetic.
- Its structural criticisms hold on inspection: four modules do cite `curriculum/README.md` as authority for claims an outside reader cannot verify, and `advanced/07` §4 does build an extended case study on a non-public internal incident report.
- **One open item, named plainly:** A explicitly declined to audit all ~90 external sources, sampling 24 instead. That is a stated limit, honestly declared, not a defect — but it means "no fabricated citation exists in this corpus" is a well-supported inference across two independent samples plus five internal reviews, not an exhaustive proof, and I will not report it to the CEO as one.

**My conclusion:** Sound, useful, and it earned its place by finding something all five internal reviewers missed. Its one over-generalization is identified above and does not affect its citation verdict, which I accept.

---

## External Reviewer B — Hiring Manager / Technical Interviewer, Interview-Readiness & International Standards

- **I verified its most consequential claim mechanically rather than accepting it.** B reports there is not one runnable line of code anywhere in the 24 documents. A corpus-wide scan for Python code fences returns **zero**. I also grepped every document for reinforcement learning, RLHF, DPO, PPO, GRPO, and reward modelling: the only hits in the entire corpus are the words "Reinforcement Learning" appearing inside the _titles_ of cited papers in reference lists. There is no body treatment of post-training anywhere. Both gaps are exactly as B describes them.
- These are scope findings, not defects. Neither `curriculum-development-plan.md` nor README §1 promises a coding track or RLHF coverage, and a fair review does not penalize a deliverable for scope it never claimed. But B is right that the two gaps bear directly on the question the CEO will actually ask, which is whether this prepares a reader for a real interview loop — so I have carried them forward as scope decisions (S-2), not as revision items against any document.
- Its parochialism finding on `advanced/07` §4 is independently confirmed (see the Ibarra-Costa section) and is the second reviewer to reach it from a cold outside reading. Two independent external readers flagging the same passage is a stronger signal than either alone.
- **A check that could have gone wrong but did not:** B's report on the Chinese text says the translation is fluent and correctly terminologized throughout, and separately flags hard-wrapping in `intermediate/01`, `intermediate/04`, and `intermediate/06` as a visible machine-produced artifact. I checked whether B had, in effect, already caught the punctuation defect under a different name. It had not — the files B names for wrapping are not the four files carrying the punctuation deviation, and the two defects are unrelated. B's wrapping observation is real and separate; it corroborates Bhandari's P3 on `intermediate/04` from an outside reading.
- **One open item, named plainly:** B marked the `intermediate/07` 90% claim and the `advanced/05` RULER claim as "Correct, web-verified" when both are, on my own reading of the documents, wrong in the specific ways two internal reviewers identified. B verified that the cited figure exists in the cited source, which is the floor README §6 explicitly names as insufficient. This is worth knowing before external review output is ever treated as a higher authority than internal review output.

**My conclusion:** Its scope findings are the most decision-relevant material in the entire cycle and I have escalated both to the CEO. Its claim-level spot-checks are the weakest verification work in the seven reports — accurate on existence, silent on attribution — and where it conflicts with an internal reviewer who re-derived the number, the internal reviewer wins.

---

## Metadata Formatting and Inline Bilingual Glossing — Corpus-Wide Findings

At the CEO's request, a small set of selected external users read the finished materials and
surfaced two items. Neither is accepted on assertion here; both were checked against the corpus
the same way every finding above was.

**Metadata block format.** The users are right, and field presence alone undercounts the problem.
Reading all 24 opening blocks by actual structure finds **six distinct formats**, each internally
consistent within one author's own modules but divergent across authors — an authoring-process
gap, not random inconsistency:

| Format | Style                                                                                   | Author(s) / modules                                                                                                             |
| ------ | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| A      | Markdown pipe-table, 5 fields (Level/Cluster/Author/Assumes-or-Builds-on/Builds-toward) | Baek — `intro/01`, `intro/02`, `inter/02`, `adv/02`                                                                             |
| B      | Compact bold key-value line + its Chinese mirror line, 3 fields (Level/Cluster/Author)  | Fujimori — `intro/03`, `intro/04`, `intro/07`; Dubois — `intro/08`, `inter/08`, `adv/08`; Ibarra-Costa — `intro/06`, `inter/06` |
| C      | Italicized flowing narrative paragraph merging all fields into prose                    | Fujimori — `inter/03`, `inter/07`, `adv/04`; Bhandari — `adv/07` (also omits Cluster entirely)                                  |
| D      | Same narrative-paragraph style, not italicized                                          | Okonkwo — `inter/01`, `adv/01`                                                                                                  |
| E      | Partial bold-line, 2 fields only (Level/Cluster — no Author), em-dash separator         | Roldán — `inter/04`, `adv/03`                                                                                                   |
| F      | No metadata block at all                                                                | Tan — `intro/05`, `inter/05`, `adv/05`, `adv/06`                                                                                |

Format B is the closest fit to a workable standard: already used by 3 of 8 authors, bilingual, and
the most compact of the structured formats. See C-2 below: six formats to reconcile, across the
full 24-document corpus.

**Bilingual convention.** Here the literal complaint — that English and Chinese are interspersed
within the body of paragraphs — does not describe what is actually in the corpus, and that is
worth stating precisely rather than smoothing over. A corpus-wide regex sweep for sentence- or
clause-level EN/ZH interleaving outside parentheses returned **zero hits** across all 24 files; the
mandated "full English paragraph, then its full Chinese paragraph" structure holds throughout every
document, not just its opening section. What the users are actually responding to is different and
real: **310 instances across all 24 files** (1–32 per file, present in every module) of inline
parenthetical bilingual glossing applied to ordinary technical terms — `loss function（损失函数）`,
`embedding vector（嵌入向量）`, `token（词元）`, `context window（上下文窗口）`, and similar — not
proper nouns. Only a small minority, genuine proper-noun glosses such as `Chinchilla（龙猫模型）`
and `ReAct（"推理与行动协同"）`, should be kept under the rule the users are actually asking for.
The cause traces to `curriculum/README.md`'s own style guide, which told every author to gloss
"technical terms" generally with no proper-noun restriction — all 8 followed it faithfully, so this
is a convention defect, not an authoring one, the same pattern already seen once in this cycle.

**Verdict impact:** neither item moves any of the 24 per-document verdicts below. Both are uniform,
corpus-wide consequences of a single convention statement, not per-document authoring defects, and
the verdict rule already scopes that kind of item once (see C-1/C-2/C-3) rather than per file. What
they do change is how much of the corpus is ship-ready untouched — see the Overall recommendation
below.

---

## Joint Recommendation

The seven reviewers do **not** all agree, and I have not smoothed that over. Three verdict conflicts existed on entry to this pass; I resolved each by returning to the source, and in all three the reviewer who re-derived or re-read the specific sentence was right and the reviewer who confirmed the citation's existence was not. I have additionally overridden four sub-report verdicts on consistency grounds (two upward, two downward) and added one finding of my own.

### Per-document verdict — all 24

Verdict rule, stated so it can be checked: **Needs revision** = the document contains at least one defect that is factually wrong, misrepresents a source, corrupts its own rendered output, or breaches a mandatory README §4/§5 requirement inside that document. **Pass** = any remaining defects are polish-level, or belong to a corpus-wide harmonization item (C-1/C-2/C-3) that is scoped once below rather than charged to each document.

| #   | Document                                                                         | Author       | My verdict         | Reason (blank = no finding)                                                                                                                   |
| --- | -------------------------------------------------------------------------------- | ------------ | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `introductory/01-neural-networks-and-deep-learning-foundations.md`               | Baek         | **Pass**           | Clean in all three reviews; one P3 (theorem without its own primary citation)                                                                 |
| 2   | `introductory/02-the-transformer-architecture-and-attention.md`                  | Baek         | **Pass**           | Clean in all three reviews                                                                                                                    |
| 3   | `introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md`             | Fujimori     | **Pass**           | Only finding is C-1 (harness term)                                                                                                            |
| 4   | `introductory/04-tool-use-and-function-calling-basics.md`                        | Fujimori     | **Pass**           | Only finding is C-1                                                                                                                           |
| 5   | `introductory/05-prompt-engineering-fundamentals.md`                             | Tan          | **Needs revision** | 192 half-width punctuation instances / zero full-width (§4 breach); H1 numeral prefix; no metadata block                                      |
| 6   | `introductory/06-context-windows-tokens-and-memory-basics.md`                    | Ibarra-Costa | **Pass**           | Clean in all three reviews; the strongest document in the corpus                                                                              |
| 7   | `introductory/07-introduction-to-multi-agent-systems.md`                         | Fujimori     | **Pass**           | Clean in all three reviews                                                                                                                    |
| 8   | `introductory/08-why-and-how-we-evaluate-agents.md`                              | Dubois       | **Pass**           | One P3 orphan citation (HELM)                                                                                                                 |
| 9   | `intermediate/01-training-dynamics-optimization-and-generalization.md`           | Okonkwo      | **Needs revision** | Rendering defect fragments the Adam update rule (l. 119); orphan citation; `模型family`; 4 half-width commas                                  |
| 10  | `intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md` | Baek         | **Pass**           | One stray half-width comma (P3)                                                                                                               |
| 11  | `intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md`          | Fujimori     | **Pass**           | Only finding is C-1                                                                                                                           |
| 12  | `intermediate/04-agent-memory-systems-short-term-long-term-episodic.md`          | Roldán       | **Needs revision** | Chinese gloss states "5 天（200 小时）"; 200 h is 8.33 days — false numeric claim in a worked example                                         |
| 13  | `intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`           | Tan          | **Needs revision** | 167 half-width punctuation instances (§4 breach); H1 numeral prefix; no metadata block; one P3 imprecision                                    |
| 14  | `intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md`         | Ibarra-Costa | **Needs revision** | Stray blockquote breaks a ZH paragraph (l. 787–790); Lewis et al. co-author miscount; FAISS timing P3                                         |
| 15  | `intermediate/07-multi-agent-communication-and-coordination-protocols.md`        | Fujimori     | **Needs revision** | §6 attributes Anthropic's 90% time figure to the wrong mechanism and the wrong baseline (P1)                                                  |
| 16  | `intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md`         | Dubois       | **Pass**           | Clean in all three reviews                                                                                                                    |
| 17  | `advanced/01-scaling-laws-and-emergent-capabilities.md`                          | Okonkwo      | **Pass**           | Orphan citation (Brown et al.) and 4 half-width commas — both P2/P3, no rendering or factual defect                                           |
| 18  | `advanced/02-mixture-of-experts-and-modern-architecture-variants.md`             | Baek         | **Needs revision** | Rendering defect fragments the load-balancing-loss sum (l. 281); otherwise the cleanest advanced module                                       |
| 19  | `advanced/03-agent-harness-engineering-production-grade-agent-loops.md`          | Roldán       | **Pass**           | Sole finding is the missing Author field — folded into C-2 (Lindqvist verdict overridden downward)                                            |
| 20  | `advanced/04-agentic-safety-guardrails-and-governance-patterns.md`               | Fujimori     | **Pass**           | Only finding is C-1                                                                                                                           |
| 21  | `advanced/05-advanced-context-engineering-long-context-and-budgeting.md`         | Tan          | **Needs revision** | §6 understates RULER's headline finding ("a small number" vs. "half") — P1; plus 255 half-width instances, H1 prefix, no metadata block       |
| 22  | `advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`             | Tan          | **Needs revision** | Reader-facing statement that its prerequisite "had not yet been written" is now false; 254 half-width instances; H1 prefix; no metadata block |
| 23  | `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md`      | Bhandari     | **Pass**           | Clean on content and structure; §4's workspace-internal case study is a shipping decision (S-1), not a defect                                 |
| 24  | `advanced/08-rigorous-agent-evaluation-statistical-methodology.md`               | Dubois       | **Needs revision** | §11's WebArena row contradicts its own inputs, its own footnote, and the section's conclusion (P0)                                            |

**14 pass. 10 need revision.** Nine of the ten are one-file, one-location fixes. The tenth (`intermediate/07`) needs a sentence rewritten against the source.

### Corpus-wide items — scoped once, not charged per document

- **C-1 — "harness" terminology.** Eight documents across three clusters split between `执行框架` and `运行框架`. Standardize on `运行框架` (majority, and the choice of both modules that make harnesses their subject), then update `introductory/03`, `introductory/04`, `intermediate/07`, and `advanced/08`. Bhandari's fix covered two of these four; the other two are outside any cluster reviewer's assignment.
- **C-2 — metadata block.** Six competing formats are in use (see above), and the README mandates
  none. Amend README §4 to specify one canonical format (recommend Format B — bilingual, compact,
  already used by 3 of 8 authors). Reformat the opening block of all 24 modules to match, folding
  in the two previously-missing-Author cases (`inter/04`, `adv/03`) and Tan's four no-block cases
  into one harmonization pass.
- **C-3 — inline term-gloss over-use.** 310 instances across all 24 documents of inline
  parenthetical bilingual glossing applied to ordinary technical terms rather than proper nouns —
  a consequence of README §4's own style guide as written, not an authoring inconsistency. Amend
  README §4/§5 to restrict inline glossing to proper nouns and named entities on first use only;
  ordinary terms rely solely on the paired EN/ZH paragraph structure. Then run a corpus-wide
  cleanup pass against all 310 instances: remove the gloss where the term is ordinary (the large
  majority), keep it where genuinely a proper noun (the minority).

### Scope decisions for the CEO — not defects, do not treat as revision items

- **S-1 — `advanced/07` §4's internal case study.** Both external reviewers, reading cold and independently, flagged the workspace-internal git-worktree incident as the one passage that reads as parochial. Its technical content is sound and Ibarra-Costa verified it represents its source accurately. This is purely a question of audience: fine for an internal ANU-00 readership, a visible seam if this is ever published outside the workspace. **The CEO's call, not mine.**
- **S-2 — what this curriculum deliberately is not.** Zero lines of runnable code (mechanically confirmed) and zero coverage of RLHF/DPO/PPO/reward modelling (mechanically confirmed) across all 24 modules. Neither was in the ratified scope, so neither is a defect against any author. But External Reviewer B is right that both bear on whether a reader finishes interview-ready. If the CEO wants that claim to hold, it needs a second production run — a hands-on track and a post-training module — not edits to these 24.

### Overall recommendation

**This first draft needs a scoped revision pass. It is not ready to ship as-is, and it does not have a systemic problem requiring escalation.**

That distinction is the substance of my recommendation, so I will be precise about it. Across seven reviews and my own re-checking, this corpus contains **zero fabricated citations, zero misattributed papers, and zero wrong formulas** — a result independently reached by two external reviewers and five internal ones, and one I tested rather than assumed by re-deriving three worked examples by hand and tracing every reported orphan citation through its whole document. Every worked example I recomputed except one is exactly right. That is a genuinely unusual outcome for a corpus this size and this citation-dense, and it is the finding that makes this a revision pass rather than a rebuild.

The ten flagged documents fail on ten specific, locatable, individually cheap defects — one incoherent table, two misstated source findings, two fragmented formulas, one broken paragraph, one false day-conversion, one stale production note, and one author's punctuation convention. Nine of the ten are single-location fixes. None of them requires re-researching, re-sourcing, or rethinking any chapter.

This does not change the content-accuracy verdict, but it does change the shape of remediation:
**zero documents are clear to ship untouched** — every one of the 24 carries at least one
corpus-wide presentation item (a metadata-block reformat, a term-gloss cleanup, or both), even
where its content is fully sound. The 10 content-flagged documents still need their original
author's attention against the source; the remaining 14 need only a mechanical harmonization pass
against the corrected README convention, not a content review.

**I recommend the CEO approve a scoped Pass 4 remediation run covering exactly:** the ten documents in the table above; the three corpus-wide harmonization items C-1, C-2, and C-3; and a decision on S-1 and S-2, which are the CEO's to make and which no reviewer should pre-empt. Authors remediate their own modules; the four documents with blocking-severity findings (`intermediate/07`, `advanced/05`, `advanced/08`, and `intermediate/04`) should be re-reviewed by a reviewer other than their author before close, per README §6's independence rule, and per README rule 4 that re-review is a new file, never an edit to an existing one.

**One item I am escalating that is not about the curriculum.** The review process itself has a real seam, and I would rather name it than let it recur. A wholesale bilingual punctuation deviation spanning 868 instances in four documents — visible to any fluent Chinese reader at a glance — was reported by none of the seven reviewers, because it sat between the content reviewers' meaning-and-fluency mandate and the structural reviewer's explicit exclusion of translation quality. Every reviewer honoured their stated scope correctly; the scopes did not meet. Before the next curriculum run, README §6 should add a mechanical bilingual-typography sweep to the structural reviewer's mandate, since it is exactly the kind of check a script does perfectly and a careful human reader glides past. Separately, this cycle produced three cases where an external reviewer marked a claim "verified" on the strength of the cited source existing — the floor README §6 already names as insufficient — while an internal reviewer who re-derived the number found it wrong. External review remains valuable (Reviewer A found a real defect all five internal reviewers missed), but its verdicts should not outrank an internal reviewer who showed their arithmetic.

One small process note for the record, since resolved: Ibarra-Costa's report was originally filed as `multi-agent-eval-cluster-review.md`, where README §6 specifies `multi-agent-evaluation-cluster-review.md`. The file has since been renamed to match; content was never affected.

**We recommend CEO approval of a scoped Pass 4 remediation run on the ten named documents plus items C-1, C-2, and C-3, a CEO ruling on S-1 and S-2, and the README §6 amendment above — not a shipping sign-off on this draft in its current state, and not an escalation.**

**Dr. Naledi Mokoena, ANU-00 Lead — 2026-08-18**
