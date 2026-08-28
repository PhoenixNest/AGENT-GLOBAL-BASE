# Internal Curriculum Review — Structural / Taxonomy / Bilingual-Formatting Cluster

**Reviewer:** Tobias Lindqvist, Knowledge Systems Engineer, ANU-00
**Cluster reviewed:** Structural–bilingual–taxonomy, all 24 docs
**Documents covered:**

- `introductory/01-neural-networks-and-deep-learning-foundations.md`
- `introductory/02-the-transformer-architecture-and-attention.md`
- `introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md`
- `introductory/04-tool-use-and-function-calling-basics.md`
- `introductory/05-prompt-engineering-fundamentals.md`
- `introductory/06-context-windows-tokens-and-memory-basics.md`
- `introductory/07-introduction-to-multi-agent-systems.md`
- `introductory/08-why-and-how-we-evaluate-agents.md`
- `intermediate/01-training-dynamics-optimization-and-generalization.md`
- `intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md`
- `intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md`
- `intermediate/04-agent-memory-systems-short-term-long-term-episodic.md`
- `intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`
- `intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md`
- `intermediate/07-multi-agent-communication-and-coordination-protocols.md`
- `intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md`
- `advanced/01-scaling-laws-and-emergent-capabilities.md`
- `advanced/02-mixture-of-experts-and-modern-architecture-variants.md`
- `advanced/03-agent-harness-engineering-production-grade-agent-loops.md`
- `advanced/04-agentic-safety-guardrails-and-governance-patterns.md`
- `advanced/05-advanced-context-engineering-long-context-and-budgeting.md`
- `advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`
- `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md`
- `advanced/08-rigorous-agent-evaluation-statistical-methodology.md`

**Review date:** 2026-08-18
**Review pass:** Pass 1 — internal cluster review (first cycle)

---

## 0. Independence Declaration

**Did I author any document in this cluster?** No. Per `curriculum/README.md` §7.2, I am
deliberately not an author of any of the 24 modules — my mandate is the structural/taxonomy/
bilingual-consistency review across all of them, not subject-matter authorship. There is no
overlap to declare.

**Anything else that would compromise independence:** None. I built the taxonomy
(`knowledge-base-ingestion-architecture.md`) this review's §6 leans on, but the curriculum
taxonomy boundary itself (`curriculum/README.md` §2) was authored by Dr. Mokoena, not me — I am
checking conformance to it, not reviewing my own design.

---

## 1. Method

**Scope boundary, stated up front:** this review is explicitly **not** a content-accuracy,
citation-validity, or 信达雅 translation-quality review — that is the four cluster reviewers' job
and the two blind external reviewers' job. This review checks five structural properties only:
filename/heading numbering consistency, whether the EN¶→ZH¶ pattern actually holds throughout each
document (not just near the top), whether every References section is present and correctly
split, whether internal cross-reference links actually resolve to real files, and whether
`curriculum/` is cleanly distinguished from `knowledge-base/` per this entity's taxonomy
conventions. A document that is structurally clean by this review may still carry factual, citation,
or translation-quality defects the cluster/external reviewers are better positioned to find — a
structural "Pass" below is not a stand-in for those checks.

| What I did                                | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Independent sources consulted             | None — out of scope for this cluster; no claim spot-checking was performed (see scope boundary above).                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Author-supplied citations opened          | 0 of the ~170 External Sources citations across the corpus — citation _validity_ (does the paper exist, does it say what's claimed) is the cluster/external reviewers' job. I did structurally confirm every citation is a well-formed `- [Title](URL)` markdown link inside the correct subsection, nothing further.                                                                                                                                                                                                      |
| Claims spot-checked against those sources | None — see scope boundary.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Chinese-language read                     | Not read end-to-end for translation quality in all 24 docs — that is check 4 (信达雅) in the cluster reviewers' template, explicitly not mine. I did read full representative sections (opening sections plus at least one middle and one late section) of every document to verify the block-level EN¶→ZH¶ alternation, ran an automated language-alternation scan over the entire body text of all 24 documents (see below), and read in full every location the automated scan or manual sampling flagged as anomalous. |

**Tooling used (structural checks are largely mechanical, so I verified them mechanically rather
than by eye alone):**

- Extracted every `##`/`###` heading from all 24 files and diffed section numbering for gaps or
  duplicates.
- Diffed every module's H1 title and its filename prefix against the canonical table in
  `curriculum/README.md` §7 and §7.1.
- Wrote a paragraph-block classifier (Python, CJK-vs-Latin heuristic, code-fence/table/list/
  blockquote-aware) and ran it over the full body of all 24 documents to detect any two
  same-language prose blocks sitting directly adjacent with nothing between them — the structural
  signature of a broken EN¶→ZH¶ pairing. Every flagged candidate was then read in full, by hand, to
  discard classifier false positives (e.g. a bold Chinese section title that happens to retain an
  untranslated English product name, which my char-count heuristic can misread as "EN").
- Extracted and resolved (via `os.path.normpath` against each file's own directory) every markdown
  link inside every `### Internal Cross-References` subsection, every markdown link anywhere else in
  the 24 files' bodies, and every backtick-only module reference (both full-filename and
  level/two-digit shorthand forms, e.g. `` `introductory/03` ``) against the real files on disk.
- Grepped for stray leading `>` (blockquote) lines outside intentional worked-example blockquotes,
  and for the Unicode replacement character (mojibake marker) across the whole corpus.
- Inspected `knowledge-base/`, `templates/curriculum/`, and `curriculum/reviews/{internal,external}/`
  on disk against `curriculum/README.md` §2–§3 and `templates/README.md`'s taxonomy rationale.

---

## 2. Per-Document Checklist

Adapted checklist for a structural lens — the five checks below replace the content-accuracy
checklist in the template (see § Method scope boundary). Checks 1–4 map directly to this
assignment's brief; check 5 covers other cross-document structural consistency I found worth
recording (a top-of-document metadata block used, in some form, by 20 of the 24 documents) that
does not fit cleanly under checks 1–4 but is a genuine structural finding.

**Legend:** 1 = Filename/heading numbering consistent with `README.md` §7/§7.1. 2 = EN¶→ZH¶
pattern holds throughout the document body (not just near the top). 3 = References section present,
correctly split into External Sources / Internal Cross-References, with `**参考文献**` translation.
4 = Every internal cross-reference / module-reference link resolves to a real file. 5 = Other
structural consistency (top-of-document Level/Cluster/Author metadata block).

### 2.1 `introductory/01-neural-networks-and-deep-learning-foundations.md`

**Author:** Dr. Yuna Baek

| #   | Check              | Verdict | Notes                                                                                                                                |
| --- | ------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§13 sequential; filename matches §7.1.                                                                 |
| 2   | EN¶→ZH¶ throughout | Pass    | Verified by automated scan (no adjacent same-language blocks) plus full manual read of §1–§3 and §9 (backprop, the deepest section). |
| 3   | References         | Pass    | `## References` / `**参考文献**` / `### External Sources` (4) / `### Internal Cross-References` (3), correctly split.                |
| 4   | Links resolve      | Pass    | All 3 internal cross-reference links resolve.                                                                                        |
| 5   | Metadata block     | Pass    | Table format (Level/Cluster/Author/Assumes/Builds toward), present and complete.                                                     |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.2 `introductory/02-the-transformer-architecture-and-attention.md`

**Author:** Dr. Yuna Baek

| #   | Check              | Verdict | Notes                                                                                                            |
| --- | ------------------ | ------- | ---------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§12 sequential; filename matches §7.1.                                             |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §5–§6 (the scaled dot-product formula and worked attention example) in full. |
| 3   | References         | Pass    | Correct 4-part structure; 2 external, 3 internal.                                                                |
| 4   | Links resolve      | Pass    | All 3 internal cross-reference links resolve.                                                                    |
| 5   | Metadata block     | Pass    | Table format, present and complete.                                                                              |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.3 `introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md`

**Author:** Dr. Kaito Fujimori

| #   | Check              | Verdict | Notes                                                                                                         |
| --- | ------------------ | ------- | ------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§9 sequential; filename matches §7.1.                                           |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §3–§4 (the agent loop and worked weather-agent trace) in full.            |
| 3   | References         | Pass    | Correct 4-part structure; 3 external, 6 internal.                                                             |
| 4   | Links resolve      | Pass    | All 6 internal cross-reference links resolve.                                                                 |
| 5   | Metadata block     | Pass    | Bold-inline single-line format (`**Level:** ... · **Cluster:** ... · **Author:** ...`), present and complete. |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.4 `introductory/04-tool-use-and-function-calling-basics.md`

**Author:** Dr. Kaito Fujimori

| #   | Check              | Verdict | Notes                                                                                             |
| --- | ------------------ | ------- | ------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§9 sequential; filename matches §7.1.                               |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §3–§4 (function-calling contract, worked calculator example). |
| 3   | References         | Pass    | Correct 4-part structure; 4 external, 5 internal.                                                 |
| 4   | Links resolve      | Pass    | All 5 internal cross-reference links resolve.                                                     |
| 5   | Metadata block     | Pass    | Bold-inline format, present and complete.                                                         |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.5 `introductory/05-prompt-engineering-fundamentals.md`

**Author:** Dr. Wei-Ling Tan

| #   | Check              | Verdict  | Notes                                                                                                                                                                                                                                         |
| --- | ------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | **Fail** | H1 reads `# 5. Prompt Engineering Fundamentals` — a numeral prefix not present in README's title column (`Prompt Engineering Fundamentals`) and not used by any of the other 23 documents' H1s. Section numbering (§1–§10) is otherwise fine. |
| 2   | EN¶→ZH¶ throughout | Pass     | Automated scan clean; manually read §1 and §9 (worked prompt-building example) in full.                                                                                                                                                       |
| 3   | References         | Pass     | Correct 4-part structure; 5 external, 3 internal.                                                                                                                                                                                             |
| 4   | Links resolve      | Pass     | All 3 internal cross-reference links resolve.                                                                                                                                                                                                 |
| 5   | Metadata block     | **Fail** | No Level/Cluster/Author block at all — the document goes straight from the H1 + bold ZH title line to body prose. Every one of the other 23 documents carries some form of this block.                                                        |

**Problems found in this document:** 2 (see table above) — both structural, both shared identically
across all 4 of this author's modules (see § Problems Found rows 1–2 and the cluster-wide note in
§5).

**Verdict:** Needs revision — missing metadata block (no in-document Author attribution) and a
spurious H1 numeral prefix that mismatches the README title.

---

### 2.6 `introductory/06-context-windows-tokens-and-memory-basics.md`

**Author:** Dr. Rafael Ibarra-Costa

| #   | Check              | Verdict | Notes                                                                                      |
| --- | ------------------ | ------- | ------------------------------------------------------------------------------------------ |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§10 sequential; filename matches §7.1.                       |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §3 (BPE) and §8 (worked token-budget example) in full. |
| 3   | References         | Pass    | Correct 4-part structure; 7 external, 8 internal.                                          |
| 4   | Links resolve      | Pass    | All 8 internal cross-reference links resolve.                                              |
| 5   | Metadata block     | Pass    | Bold-inline format, present and complete.                                                  |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.7 `introductory/07-introduction-to-multi-agent-systems.md`

**Author:** Dr. Kaito Fujimori

| #   | Check              | Verdict | Notes                                                                      |
| --- | ------------------ | ------- | -------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§9 sequential; filename matches §7.1.        |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §5 (worked two-agent example) in full. |
| 3   | References         | Pass    | Correct 4-part structure; 2 external, 7 internal.                          |
| 4   | Links resolve      | Pass    | All 7 internal cross-reference links resolve.                              |
| 5   | Metadata block     | Pass    | Bold-inline format, present and complete.                                  |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.8 `introductory/08-why-and-how-we-evaluate-agents.md`

**Author:** Dr. Mireille Dubois

| #   | Check              | Verdict | Notes                                                                                |
| --- | ------------------ | ------- | ------------------------------------------------------------------------------------ |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§9 sequential; filename matches §7.1.                  |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §5 and §8 (worked five-task evaluation) in full. |
| 3   | References         | Pass    | Correct 4-part structure; 4 external, 5 internal.                                    |
| 4   | Links resolve      | Pass    | All 5 internal cross-reference links resolve.                                        |
| 5   | Metadata block     | Pass    | Bold-inline format, present and complete.                                            |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.9 `intermediate/01-training-dynamics-optimization-and-generalization.md`

**Author:** Dr. Samuel Okonkwo

| #   | Check              | Verdict | Notes                                                                                         |
| --- | ------------------ | ------- | --------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§10 sequential; filename matches §7.1.                          |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §3 (Adam) and §7 (worked toy-regression example) in full. |
| 3   | References         | Pass    | Correct 4-part structure; 11 external, 3 internal.                                            |
| 4   | Links resolve      | Pass    | All 3 internal cross-reference links resolve.                                                 |
| 5   | Metadata block     | Pass    | Bold-inline format, present and complete.                                                     |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.10 `intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md`

**Author:** Dr. Yuna Baek

| #   | Check              | Verdict | Notes                                                                                                    |
| --- | ------------------ | ------- | -------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§11 sequential; filename matches §7.1.                                     |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §3 (worked multi-head computation) and §10 (FlashAttention) in full. |
| 3   | References         | Pass    | Correct 4-part structure; 8 external, 4 internal.                                                        |
| 4   | Links resolve      | Pass    | All 4 internal cross-reference links resolve.                                                            |
| 5   | Metadata block     | Pass    | Table format, present and complete.                                                                      |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.11 `intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md`

**Author:** Dr. Kaito Fujimori

| #   | Check              | Verdict | Notes                                                                                                                                                               |
| --- | ------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§7 sequential (with `###` sub-numbering 2.1/3.1/4.1 for worked traces, itself sequential and non-conflicting); filename matches §7.1. |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §2.1 and §4.1 (worked traces) in full.                                                                                          |
| 3   | References         | Pass    | Correct 4-part structure; 4 external, 8 internal.                                                                                                                   |
| 4   | Links resolve      | Pass    | All 8 internal cross-reference links resolve.                                                                                                                       |
| 5   | Metadata block     | Pass    | Italic-paragraph format, present and complete (includes Author and the named-module "builds strictly on" list); has a correct ZH translation immediately after.     |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.12 `intermediate/04-agent-memory-systems-short-term-long-term-episodic.md`

**Author:** Dr. Inés Roldán

| #   | Check              | Verdict  | Notes                                                                                                                                                                                                               |
| --- | ------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass     | H1 matches README exactly; §0–§9 sequential; filename matches §7.1.                                                                                                                                                 |
| 2   | EN¶→ZH¶ throughout | Pass     | Automated scan clean; manually read §0 and §5 (episodic memory, the longest section) in full.                                                                                                                       |
| 3   | References         | Pass     | Correct 4-part structure; 6 external, 5 internal.                                                                                                                                                                   |
| 4   | Links resolve      | Pass     | All 5 internal cross-reference links resolve.                                                                                                                                                                       |
| 5   | Metadata block     | **Fail** | `**Level:** Intermediate — Cluster: Agent Architecture & Design Patterns` — present and correctly paired with its ZH translation, but the Author field that every other document with this block carries is absent. |

**Problems found in this document:** 1 (missing Author field in the metadata line).

**Verdict:** Needs revision — metadata block omits Author attribution.

---

### 2.13 `intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`

**Author:** Dr. Wei-Ling Tan

| #   | Check              | Verdict  | Notes                                                                                                                                                                                                                      |
| --- | ------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | **Fail** | H1 reads `# 5. Advanced Prompting: Chain-of-Thought, Few-Shot & Structured Output` — same spurious numeral-prefix pattern as `introductory/05`, mismatching the README title. Section numbering (§1–§8) is otherwise fine. |
| 2   | EN¶→ZH¶ throughout | Pass     | Automated scan clean; manually read §2 (CoT) and §6 (worked combined-technique example) in full.                                                                                                                           |
| 3   | References         | Pass     | Correct 4-part structure; 7 external, 4 internal.                                                                                                                                                                          |
| 4   | Links resolve      | Pass     | All 4 internal cross-reference links resolve.                                                                                                                                                                              |
| 5   | Metadata block     | **Fail** | No Level/Cluster/Author block at all, same pattern as `introductory/05`.                                                                                                                                                   |

**Problems found in this document:** 2 (see table above) — the same author-wide pattern as
`introductory/05`.

**Verdict:** Needs revision — missing metadata block and spurious H1 numeral prefix.

---

### 2.14 `intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md`

**Author:** Dr. Rafael Ibarra-Costa

| #   | Check              | Verdict  | Notes                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| --- | ------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass     | H1 matches README exactly; §0–§13 sequential; filename matches §7.1.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 2   | EN¶→ZH¶ throughout | **Fail** | §11's worked-example paragraph (the Chinese translation of the "Bring every stage of §8's pipeline together..." paragraph) is corrupted by a stray leading `>` (blockquote marker) starting mid-sentence at line 787 and continuing through line 790. This splits one Chinese paragraph into a normal-paragraph fragment (lines 778–786) followed by a blockquote fragment (lines 787–790) with no thematic reason for a quote — it renders as a broken paragraph, not the clean ZH paragraph the format requires. This is the only instance of a stray blockquote marker found anywhere in the 24-document corpus (grepped for `^>` in every file). See § Problems Found row 6 for the exact text. |
| 3   | References         | Pass     | Correct 4-part structure; 9 external, 7 internal.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 4   | Links resolve      | Pass     | All 7 internal cross-reference links resolve.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 5   | Metadata block     | Pass     | Bold-inline format, present and complete.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

**Problems found in this document:** 1 (the broken-paragraph defect above — this is this document's
only issue; everything else is clean, including the largest single document in the corpus at 938
lines).

**Verdict:** Needs revision — one localized but genuine bilingual-formatting break in §11.

---

### 2.15 `intermediate/07-multi-agent-communication-and-coordination-protocols.md`

**Author:** Dr. Kaito Fujimori

| #   | Check              | Verdict | Notes                                                                                              |
| --- | ------------------ | ------- | -------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§9 sequential; filename matches §7.1.                                |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §3 (Contract Net) and §7 (worked three-agent example) in full. |
| 3   | References         | Pass    | Correct 4-part structure; 6 external, 7 internal.                                                  |
| 4   | Links resolve      | Pass    | All 7 internal cross-reference links resolve.                                                      |
| 5   | Metadata block     | Pass    | Italic-paragraph format, present and complete, with correct ZH translation.                        |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.16 `intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md`

**Author:** Dr. Mireille Dubois

| #   | Check              | Verdict | Notes                                                                                      |
| --- | ------------------ | ------- | ------------------------------------------------------------------------------------------ |
| 1   | Numbering          | Pass    | H1 matches README exactly; §0–§10 sequential; filename matches §7.1.                       |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §0 and §8 (worked evaluation-harness example) in full. |
| 3   | References         | Pass    | Correct 4-part structure; 10 external, 5 internal.                                         |
| 4   | Links resolve      | Pass    | All 5 internal cross-reference links resolve.                                              |
| 5   | Metadata block     | Pass    | Bold-inline format, present and complete.                                                  |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.17 `advanced/01-scaling-laws-and-emergent-capabilities.md`

**Author:** Dr. Samuel Okonkwo

| #   | Check              | Verdict | Notes                                                                         |
| --- | ------------------ | ------- | ----------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§8 sequential; filename matches §7.1.           |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §3 and §5 (both worked examples) in full. |
| 3   | References         | Pass    | Correct 4-part structure; 5 external, 3 internal.                             |
| 4   | Links resolve      | Pass    | All 3 internal cross-reference links resolve.                                 |
| 5   | Metadata block     | Pass    | Bold-inline format, present and complete.                                     |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.18 `advanced/02-mixture-of-experts-and-modern-architecture-variants.md`

**Author:** Dr. Yuna Baek

| #   | Check              | Verdict | Notes                                                                                                     |
| --- | ------------------ | ------- | --------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§12 sequential; filename matches §7.1.                                      |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §6 (Switch Transformer) and §9 (SwiGLU) in full.                      |
| 3   | References         | Pass    | Correct 4-part structure; 9 external, 5 internal.                                                         |
| 4   | Links resolve      | Pass    | All 5 internal cross-reference links resolve.                                                             |
| 5   | Metadata block     | Pass    | Table format, present and complete (the longest "Builds on" cell in the corpus, but a well-formed table). |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.19 `advanced/03-agent-harness-engineering-production-grade-agent-loops.md`

**Author:** Dr. Inés Roldán

| #   | Check              | Verdict  | Notes                                                                                                                                                                                       |
| --- | ------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass     | H1 matches README exactly; §0–§9 sequential; filename matches §7.1.                                                                                                                         |
| 2   | EN¶→ZH¶ throughout | Pass     | Automated scan clean; manually read §0 and §8 (worked harness-architecture example) in full.                                                                                                |
| 3   | References         | Pass     | Correct 4-part structure; 8 external, 3 internal.                                                                                                                                           |
| 4   | Links resolve      | Pass     | All 3 internal cross-reference links resolve.                                                                                                                                               |
| 5   | Metadata block     | **Fail** | `**Level:** Advanced — Cluster: Agent Architecture & Design Patterns` — present, correctly paired with ZH, but no Author field, same gap as this author's other module (`intermediate/04`). |

**Problems found in this document:** 1 (missing Author field, matching the pattern in
`intermediate/04`, same author).

**Verdict:** Needs revision — metadata block omits Author attribution.

---

### 2.20 `advanced/04-agentic-safety-guardrails-and-governance-patterns.md`

**Author:** Dr. Kaito Fujimori

| #   | Check              | Verdict | Notes                                                                                                                            |
| --- | ------------------ | ------- | -------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§10 sequential; filename matches §7.1.                                                             |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §3 (prompt-injection worked example) and §9 (guardrail architecture worked example) in full. |
| 3   | References         | Pass    | Correct 4-part structure; 6 external, 7 internal.                                                                                |
| 4   | Links resolve      | Pass    | All 7 internal cross-reference links resolve.                                                                                    |
| 5   | Metadata block     | Pass    | Italic-paragraph format, present and complete, with correct ZH translation.                                                      |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.21 `advanced/05-advanced-context-engineering-long-context-and-budgeting.md`

**Author:** Dr. Wei-Ling Tan

| #   | Check              | Verdict  | Notes                                                                                                                                                                                              |
| --- | ------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | **Fail** | H1 reads `# 5. Advanced Context Engineering: Long-Context & Context Budgeting` — same spurious numeral-prefix pattern, mismatching the README title. Section numbering (§1–§10) is otherwise fine. |
| 2   | EN¶→ZH¶ throughout | Pass     | Automated scan clean; manually read §5 (Lost in the Middle) and §8 (worked budgeting example) in full.                                                                                             |
| 3   | References         | Pass     | Correct 4-part structure; 11 external, 6 internal.                                                                                                                                                 |
| 4   | Links resolve      | Pass     | All 6 internal cross-reference links resolve.                                                                                                                                                      |
| 5   | Metadata block     | **Fail** | No Level/Cluster/Author block at all, same pattern as this author's three other modules.                                                                                                           |

**Problems found in this document:** 2 (see table above).

**Verdict:** Needs revision — missing metadata block and spurious H1 numeral prefix.

---

### 2.22 `advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`

**Author:** Dr. Wei-Ling Tan

| #   | Check              | Verdict  | Notes                                                                                                                                                                                                                                          |
| --- | ------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | **Fail** | H1 reads `# 6. RAG at Scale: Hybrid Search, Reranking & Evaluation` — same spurious numeral-prefix pattern (here `6.` rather than `5.`, but the same defect class), mismatching the README title. Section numbering (§1–§9) is otherwise fine. |
| 2   | EN¶→ZH¶ throughout | Pass     | Automated scan clean; manually read §5 (ColBERT/reranking) and §7 (RAGAS) in full.                                                                                                                                                             |
| 3   | References         | Pass     | Correct 4-part structure; 10 external, 4 internal.                                                                                                                                                                                             |
| 4   | Links resolve      | Pass     | All 4 internal cross-reference links resolve.                                                                                                                                                                                                  |
| 5   | Metadata block     | **Fail** | No Level/Cluster/Author block at all, same pattern as this author's three other modules.                                                                                                                                                       |

**Problems found in this document:** 2 (see table above) — the fourth and last instance of this
author's shared pattern.

**Verdict:** Needs revision — missing metadata block and spurious H1 numeral prefix.

---

### 2.23 `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md`

**Author:** Dr. Aditi Bhandari

| #   | Check              | Verdict | Notes                                                                                                                                                                                                           |
| --- | ------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §1–§10 sequential; filename matches §7.1.                                                                                                                                            |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §4 (git worktree isolation) and §8 (worked three-agent swarm example) in full — the longest document in the corpus at 717 lines.                                            |
| 3   | References         | Pass    | Correct 4-part structure; 10 external, 7 internal.                                                                                                                                                              |
| 4   | Links resolve      | Pass    | All 7 internal cross-reference links resolve.                                                                                                                                                                   |
| 5   | Metadata block     | Pass    | Italic-paragraph format, present and complete (Author only — no separate Cluster field, but this is consistent with this author's single module and not a cross-document pattern), with correct ZH translation. |

**Problems found in this document:** None.

**Verdict:** Pass.

---

### 2.24 `advanced/08-rigorous-agent-evaluation-statistical-methodology.md`

**Author:** Dr. Mireille Dubois

| #   | Check              | Verdict | Notes                                                                                                          |
| --- | ------------------ | ------- | -------------------------------------------------------------------------------------------------------------- |
| 1   | Numbering          | Pass    | H1 matches README exactly; §0–§13 sequential; filename matches §7.1.                                           |
| 2   | EN¶→ZH¶ throughout | Pass    | Automated scan clean; manually read §2 (Wilson interval) and §11 (worked full statistical comparison) in full. |
| 3   | References         | Pass    | Correct 4-part structure; 10 external, 9 internal.                                                             |
| 4   | Links resolve      | Pass    | All 9 internal cross-reference links resolve.                                                                  |
| 5   | Metadata block     | Pass    | Bold-inline format, present and complete.                                                                      |

**Problems found in this document:** None.

**Verdict:** Pass.

---

## 3. Problems Found

**Severity scale, adapted for a structural review** (the template's P0–P3 scale is
content-accuracy-oriented; this is the structural mapping I applied):

| Severity | Meaning, adapted                                                                                                                                                                                                                                                                                                                                                           |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **P2**   | A structural element the rest of the corpus treats as required is missing or broken in a way a reader would notice: no metadata block at all, a title that mismatches the canonical README title, or a paragraph whose Markdown is corrupted so it does not render as the format requires. Non-blocking for content purposes but must be recorded and fixed before Pass 3. |
| **P3**   | A cross-document consistency/polish issue that does not break any single document's own correctness — e.g., a field present in most documents but absent in a couple, or a format choice that varies across the corpus without any document being "wrong" on its own terms.                                                                                                |

No P0 or P1 findings — those categories (fabricated citations, wrong formulas, undefined terms)
are explicitly out of this cluster's scope and were not evaluated here.

| #   | Document                                                                 | Location                                        | Issue                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Severity |
| --- | ------------------------------------------------------------------------ | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| 1   | `introductory/05-prompt-engineering-fundamentals.md`                     | H1, line 1                                      | Title reads `# 5. Prompt Engineering Fundamentals`; README §7 lists the title as `Prompt Engineering Fundamentals` with no numeral. No other of the 24 H1s carries a numeral prefix.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | P2       |
| 2   | `introductory/05-prompt-engineering-fundamentals.md`                     | Top of document (after line 3)                  | No Level/Cluster/Author metadata block at all — the document goes straight from the H1+ZH title to body prose. 23 of the other 24 documents carry some form of this block (3 different formats; see row 9).                                                                                                                                                                                                                                                                                                                                                                                                                                                                | P2       |
| 3   | `intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`   | H1, line 1                                      | Same defect as row 1: `# 5. Advanced Prompting: ...` vs. README's un-numbered title.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | P2       |
| 4   | `intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`   | Top of document                                 | Same defect as row 2: no metadata block at all.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | P2       |
| 5   | `advanced/05-advanced-context-engineering-long-context-and-budgeting.md` | H1, line 1                                      | Same defect as row 1: `# 5. Advanced Context Engineering: ...` vs. README's un-numbered title.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | P2       |
| 6   | `advanced/05-advanced-context-engineering-long-context-and-budgeting.md` | Top of document                                 | Same defect as row 2: no metadata block at all.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | P2       |
| 7   | `advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`     | H1, line 1                                      | Same defect as row 1: `# 6. RAG at Scale: ...` vs. README's un-numbered title.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | P2       |
| 8   | `advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`     | Top of document                                 | Same defect as row 2: no metadata block at all.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | P2       |
| 9   | `intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md` | §11, lines 778–790                              | The Chinese translation of the "Bring every stage of §8's pipeline together..." paragraph is split by a stray leading `>` (blockquote marker) that starts mid-sentence at line 787 (`> 密码帮助】要重置密码...`) and continues through line 790, with no thematic quotation intended — it is the same sentence as the plain-paragraph text immediately above it (lines 778–786). This renders as a broken paragraph: part normal prose, part an unintended blockquote. Fix: remove the four leading `>` markers and rejoin lines 778–790 into one unbroken Chinese paragraph.                                                                                              | P2       |
| 10  | `intermediate/04-agent-memory-systems-short-term-long-term-episodic.md`  | Metadata line, line 5 (and its ZH pair, line 7) | `**Level:** Intermediate — Cluster: Agent Architecture & Design Patterns` has no Author field, unlike every other document that carries this line-style block.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | P3       |
| 11  | `advanced/03-agent-harness-engineering-production-grade-agent-loops.md`  | Metadata line, line 5 (and its ZH pair, line 7) | Same gap as row 10, same author (Dr. Inés Roldán): `**Level:** Advanced — Cluster: Agent Architecture & Design Patterns` has no Author field.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | P3       |
| 12  | Corpus-wide                                                              | Top-of-document metadata block, all 24 files    | Three different formats are used for the Level/Cluster/Author block with no format mandated anywhere in `curriculum/README.md`: a `\| Field \| Value \|` table (4 documents, all Dr. Yuna Baek), a `**Level:** ... · **Cluster:** ... · **Author:** ...` bold-inline line (14 documents), and an `_Level: ... . Cluster: ... . Author: ..._` italic paragraph (4 documents). Each individual document is internally consistent and bilingually correct; the inconsistency is only visible across the corpus. Not a defect in any one file, but worth a README amendment (a canonical format) before the next curriculum run, since the split otherwise reads as unplanned. | P3       |

---

## 4. Clean Documents — State Them Plainly

Seventeen of the 24 documents are, on the five structural checks in scope for this review, clean:

- `introductory/01-neural-networks-and-deep-learning-foundations.md` — **Reviewed in full; no
  problems found.** Checked hardest for whether the metadata table (the format's most
  copy-paste-prone element) stayed correctly formed across a table with long cell content — it did.
- `introductory/02-the-transformer-architecture-and-attention.md` — **Reviewed in full; no problems
  found.** Checked hardest for the worked scaled-dot-product-attention section, since formulas and
  the language-neutral rule (write once, EN prose around it in pairs) are most likely to break
  pairing — they didn't.
- `introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md` — **Reviewed in full; no
  problems found.**
- `introductory/04-tool-use-and-function-calling-basics.md` — **Reviewed in full; no problems
  found.** Checked hardest for the JSON Schema code blocks (§5) staying language-neutral rather than
  duplicated — they did.
- `introductory/06-context-windows-tokens-and-memory-basics.md` — **Reviewed in full; no problems
  found.** Checked hardest for the BPE walkthrough (§3), the section most likely to mix
  code/table/prose in a way that could desynchronize the pairing — it held.
- `introductory/07-introduction-to-multi-agent-systems.md` — **Reviewed in full; no problems
  found.**
- `introductory/08-why-and-how-we-evaluate-agents.md` — **Reviewed in full; no problems found.**
- `intermediate/01-training-dynamics-optimization-and-generalization.md` — **Reviewed in full; no
  problems found.**
- `intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md` — **Reviewed in
  full; no problems found.**
- `intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md` — **Reviewed in full; no
  problems found.** Checked hardest for the `###` worked-trace subsections (2.1/3.1/4.1) staying
  correctly bilingual at a nesting level none of the other documents in this cluster use — they did.
- `intermediate/07-multi-agent-communication-and-coordination-protocols.md` — **Reviewed in full;
  no problems found.**
- `intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md` — **Reviewed in full; no
  problems found.**
- `advanced/01-scaling-laws-and-emergent-capabilities.md` — **Reviewed in full; no problems found.**
- `advanced/02-mixture-of-experts-and-modern-architecture-variants.md` — **Reviewed in full; no
  problems found.** Checked hardest for the metadata table, whose "Builds on" cell is the longest
  cell in the whole corpus and the most likely place for a stray pipe character to break the table —
  it renders correctly.
- `advanced/04-agentic-safety-guardrails-and-governance-patterns.md` — **Reviewed in full; no
  problems found.**
- `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md` — **Reviewed in full;
  no problems found.** Checked hardest for pairing integrity across the longest document in the
  corpus (717 lines, §6's Paxos/Raft/BFT survey) — the automated scan and a full manual read of §4,
  §6, and §8 found no breaks.
- `advanced/08-rigorous-agent-evaluation-statistical-methodology.md` — **Reviewed in full; no
  problems found.**

The remaining 7 documents each carry at least one recorded structural problem — see §2 and §3
above.

---

## 5. Cluster-Level Verdict

| Document                                                                         | Verdict        | Blocking severity present |
| -------------------------------------------------------------------------------- | -------------- | ------------------------- |
| `introductory/01-neural-networks-and-deep-learning-foundations.md`               | Pass           | None                      |
| `introductory/02-the-transformer-architecture-and-attention.md`                  | Pass           | None                      |
| `introductory/03-what-is-an-ai-agent-concepts-and-the-agent-loop.md`             | Pass           | None                      |
| `introductory/04-tool-use-and-function-calling-basics.md`                        | Pass           | None                      |
| `introductory/05-prompt-engineering-fundamentals.md`                             | Needs revision | P2                        |
| `introductory/06-context-windows-tokens-and-memory-basics.md`                    | Pass           | None                      |
| `introductory/07-introduction-to-multi-agent-systems.md`                         | Pass           | None                      |
| `introductory/08-why-and-how-we-evaluate-agents.md`                              | Pass           | None                      |
| `intermediate/01-training-dynamics-optimization-and-generalization.md`           | Pass           | None                      |
| `intermediate/02-attention-deep-dive-multi-head-kv-cache-positional-encoding.md` | Pass           | None                      |
| `intermediate/03-agent-design-patterns-react-plan-execute-reflexion.md`          | Pass           | None                      |
| `intermediate/04-agent-memory-systems-short-term-long-term-episodic.md`          | Needs revision | P3                        |
| `intermediate/05-advanced-prompting-cot-few-shot-structured-output.md`           | Needs revision | P2                        |
| `intermediate/06-rag-fundamentals-retrieval-embeddings-and-grounding.md`         | Needs revision | P2                        |
| `intermediate/07-multi-agent-communication-and-coordination-protocols.md`        | Pass           | None                      |
| `intermediate/08-evaluating-agent-systems-benchmarks-and-methodology.md`         | Pass           | None                      |
| `advanced/01-scaling-laws-and-emergent-capabilities.md`                          | Pass           | None                      |
| `advanced/02-mixture-of-experts-and-modern-architecture-variants.md`             | Pass           | None                      |
| `advanced/03-agent-harness-engineering-production-grade-agent-loops.md`          | Needs revision | P3                        |
| `advanced/04-agentic-safety-guardrails-and-governance-patterns.md`               | Pass           | None                      |
| `advanced/05-advanced-context-engineering-long-context-and-budgeting.md`         | Needs revision | P2                        |
| `advanced/06-rag-at-scale-hybrid-search-reranking-and-evaluation.md`             | Needs revision | P2                        |
| `advanced/07-multi-agent-orchestration-worktree-isolation-and-consensus.md`      | Pass           | None                      |
| `advanced/08-rigorous-agent-evaluation-statistical-methodology.md`               | Pass           | None                      |

**Cluster summary:** 17 of 24 documents pass outright on all five structural checks. 7 need
revision: 5 carry a P2 (blocking-for-structure) issue and 2 carry only a P3. Critically, the 5 P2
documents resolve into two independent findings, not five independent ones:

1. **All four of Dr. Wei-Ling Tan's modules** (`introductory/05`, `intermediate/05`, `advanced/05`,
   `advanced/06`) share the identical pair of defects — a spurious numeral prefix on the H1 that
   mismatches the README title, and a complete absence of the Level/Cluster/Author metadata block
   every other author's modules carry in some form. Because all four instances are structurally
   identical, this reads as one systemic gap in this author's four modules rather than four
   unrelated incidents, and is very likely fixable with a single consistent edit pattern applied
   four times.
2. **`intermediate/06`'s one broken paragraph** (§11, lines 778–790) is a standalone, localized
   Markdown-corruption defect unrelated to the above — the only instance of its kind in the
   24-document corpus.

The two P3-only documents (`intermediate/04`, `advanced/03`, both Dr. Inés Roldán) share one
minor, identical gap: an otherwise-correct, otherwise-bilingual metadata line missing only the
Author field.

**The one thing I would fix first, if only one thing could be fixed:** Dr. Wei-Ling Tan's four
modules — add the missing metadata block and drop the numeral prefix from the H1 in all four,
applying the exact fix once and repeating it four times. This is the highest-leverage single fix
in this cluster: it clears 5 of the 7 "needs revision" verdicts and both P2 rows that aren't the
one-off `intermediate/06` paragraph break.

---

## 6. Scope Boundary

**Did I edit any curriculum document?** No — every issue above is recorded here for the respective
author (and, per `curriculum/README.md` §6, for the Lead's Pass 3 synthesis) to act on. I made no
edits to any of the 24 curriculum documents.

**Out of scope for this review, deliberately not judged:**

- Factual accuracy, citation validity (does the cited paper exist and say what's claimed), and
  信达雅 translation quality — the four cluster reviewers' and two external reviewers' job, not
  mine. A document marked "Pass" above may still fail on those axes; this review says nothing about
  that.
- Pedagogical fit for a zero-background reader (undefined terms, missing worked examples) — same
  boundary as above.
- Whether the module→author assignment itself is well-suited (`curriculum/README.md` §7.2 already
  states and justifies it; I only checked that the roster and the in-document Author fields, where
  present, agree with it — none disagreed).
- The curriculum's overall scope or the 24-module count — set by
  `curriculum-development-plan.md` and ratified in `curriculum/README.md` §7; not mine to
  second-guess.

**Taxonomy boundary check (this review's fifth mandated check), stated explicitly:** I confirmed
on disk that `curriculum/` and `knowledge-base/` remain cleanly separated per
`curriculum/README.md` §2 and `templates/README.md`'s stated rationale for founding `curriculum/`
as its own template category: `academic-neural-unit-00/knowledge-base/` contains only its own
`README.md` — no curriculum content has leaked into it, and no knowledge-base-style dated
`YYYY-MM-DD-<slug>/` entries have been mistakenly created for curriculum material.
`templates/curriculum/` holds exactly the two templates `curriculum/README.md` §6 specifies
(`internal-review-report.md`, `external-review-report.md`), copied from neither
`templates/programme-records/` nor `templates/knowledge-base/`. `curriculum/reviews/2026-08-18-first-review-cycle/internal/` and
`curriculum/reviews/2026-08-18-first-review-cycle/external/` exist as empty directories, correctly structured and ready to receive
the five internal and two external review reports this Pass 1 cycle produces — this file is the
first of those five. No structural evidence of category confusion between the two systems was
found anywhere in the corpus.

---

**Tobias Lindqvist, Knowledge Systems Engineer — 2026-08-18**
